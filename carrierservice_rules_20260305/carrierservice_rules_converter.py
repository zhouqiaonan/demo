#!/usr/bin/env python3
"""
carrierservice_rules_converter.py

Default mode (no flags):
  Converts my_sale_express_rules.xlsx to a UTF-8 CSV file:
  - Output filename gets a _YYYYMMDD-HHMMSS suffix before .csv
  - Removes columns that are 100% empty (detected dynamically)
  - Fixes whitespace bugs: strips leading/trailing whitespace and removes
    spaces in range notation (e.g. "LTE_ 39.5" -> "LTE_39.5")
  - All other values kept as-is (ctime/mtime=0, null country, auto_refresh_count)
  - Denormalisation:
      bs_warehouse_id      -> warehouse name from bs_warehouse.xlsx
      bs_express_service_id -> "express>service>show_name" from express_service.xlsx
                              (show_name omitted when null)
  - Inserts empty column 'hangzhou_carrierservice_id' after bs_express_service_id
  - Writes hangzhou_carrierserviceid_conversion.csv: one row per unique
    (bs_warehouse_id, bs_express_service_id) combination with usage count,
    for manual ID mapping

--merge [CSV_FILE] mode:
  Reads the manually-filled hangzhou_carrierserviceid_conversion.csv and
  transposes the hangzhou_carrierservice_id values into a previously-generated
  rules CSV:
  - CSV_FILE: path to a my_sale_express_rules_*.csv (default: auto-detects the
    latest file matching that pattern in the current directory)
  - Workfile rows whose hangzhou_carrierservice_id is not a plain integer
    (e.g. "REMOVE_THESE_RULES ...") are treated as removal markers: all
    matching rules rows are dropped from the output.
  - Remaining rows get their hangzhou_carrierservice_id filled from the workfile.
  - Output: <stem>_merged_YYYYMMDD-HHMMSS.csv (preserves source filename lineage)

--fixrouting [CSV_FILE] mode:
  Corrects hangzhou_carrierservice_id per row using the *NOTE* routing rules
  in hangzhou_carrierserviceid_conversion.csv and the country column in the
  merged CSV (run after --merge, before --countrycsv):
  - CSV_FILE: path to a *_merged_*.csv (default: auto-detects the latest such
    file in the current directory)
  - For each (warehouse, express_service) combo whose *NOTE* encodes a routing
    rule (e.g. "domestic68+intl69"), the domestic country is inferred from the
    warehouse ID suffix (YDY-DE → DE, YC-FR → FR, etc.) and each row's
    hangzhou_carrierservice_id is set to the correct ID for its ship-to country.
  - Rows not covered by any routing NOTE are left unchanged.
  - Output: <stem>_routed_YYYYMMDD-HHMMSS.csv
  - Log:    <stem>_fixrouting_YYYYMMDD-HHMMSS.log (lists every changed cell)

--countrycsv [CSV_FILE] mode:
  Normalises a previously-merged rules CSV by splitting country into a separate
  junction table, and deduplicating rows that are identical on all rule-logic
  columns (i.e. every column except sale_express_rules_id and country):
  - CSV_FILE: path to a *_merged_*.csv (default: auto-detects the latest such
    file in the current directory)
  - Duplicate rule groups are collapsed to one row, keeping the lowest
    sale_express_rules_id as the canonical PK; the others are dropped.
  - Outputs (all timestamped, written next to the source file):
      <stem>_deduped_YYYYMMDD-HHMMSS.csv   — main table, country column removed
      <stem>_countries_YYYYMMDD-HHMMSS.csv — junction: sale_express_rules_id, country
      <stem>_countrycsv_YYYYMMDD-HHMMSS.log — human-readable log of dropped IDs
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

INPUT_FILE = "my_sale_express_rules.xlsx"
SHEET_NAME = "my_sale_express_rules"

WAREHOUSE_FILE = "bs_warehouse.xlsx"
EXPRESS_SERVICE_FILE = "express_service.xlsx"
CONVERSION_FILE = "hangzhou_carrierserviceid_conversion.csv"

MERGE_KEY = ["bs_warehouse_id", "bs_express_service_id"]


# ------------------------------------------------------------------ #
# Helpers                                                             #
# ------------------------------------------------------------------ #

def fix_whitespace(value: str) -> str:
    """Fix whitespace bugs in a string value:
    - Strip leading/trailing whitespace
    - Remove spaces between an underscore and a digit in range notation
      e.g. "LTE_ 39.5"  ->  "LTE_39.5"
           "GT_ 13@LT_ 31.5"  ->  "GT_13@LT_31.5"
    - Remove spaces around the @ range separator
      e.g. "GT_13 @ LT_31.5"  ->  "GT_13@LT_31.5"
    """
    if not isinstance(value, str):
        return value
    value = value.strip()
    # spaces between underscore and digit (the confirmed bug pattern)
    value = re.sub(r"_\s+(\d)", r"_\1", value)
    # spaces around @ range separator (defensive, handles similar future issues)
    value = re.sub(r"\s*@\s*", "@", value)
    return value


def load_warehouse_lookup(path: Path) -> dict:
    """Return {bs_warehouse_id_str: warehouse_name} from bs_warehouse.xlsx."""
    df = pd.read_excel(path, sheet_name="Sheet1", dtype=str)
    return dict(zip(df["bs_warehouse_id"], df["warehouse"]))


def load_express_service_lookup(path: Path) -> dict:
    """Return {bs_express_service_id_str: concatenated_label} from express_service.xlsx.

    Label format: "express>service>show_name"  (show_name omitted when null)
    """
    df = pd.read_excel(path, sheet_name="Sheet1", dtype=str)
    lookup = {}
    for _, row in df.iterrows():
        parts = [row["express"], row["service"]]
        if pd.notna(row["show_name"]):
            parts.append(row["show_name"])
        lookup[row["bs_express_service_id"]] = ">".join(parts)
    return lookup


def apply_lookup(series: pd.Series, lookup: dict, col_name: str) -> pd.Series:
    """Replace values using lookup dict; warn about any unmapped IDs."""
    missing = sorted(set(series.dropna().unique()) - set(lookup.keys()))
    if missing:
        print(f"  WARNING: {len(missing)} ID(s) in '{col_name}' not found in lookup "
              f"— original value kept: {missing}")

    def _replace(val):
        if pd.isna(val):
            return val
        return lookup.get(val, val)   # keep original if not in lookup

    return series.apply(_replace)


# ------------------------------------------------------------------ #
# Merge mode                                                          #
# ------------------------------------------------------------------ #

def _is_integer(val: str) -> bool:
    try:
        int(str(val).strip())
        return True
    except (ValueError, TypeError):
        return False


def merge_ids(csv_path: Path) -> None:
    """Merge hangzhou_carrierservice_id from the conversion workfile into csv_path.

    - Workfile rows with a non-integer ID are treated as removal markers:
      matching rules rows are dropped from the output.
    - Remaining rows get hangzhou_carrierservice_id filled from the workfile.
    - Writes <stem>_merged_YYYYMMDD-HHMMSS.csv next to the source file.
    """
    here = csv_path.parent
    conversion_path = here / CONVERSION_FILE

    # -- Load workfile ------------------------------------------------
    if not conversion_path.exists():
        print(f"ERROR: Conversion workfile not found: {conversion_path.resolve()}",
              file=sys.stderr)
        sys.exit(1)

    wf = pd.read_csv(conversion_path, dtype=str)
    print(f"Conversion workfile: {conversion_path.name}  ({len(wf)} rows)")

    id_col = "hangzhou_carrierservice_id"
    wf[id_col] = wf[id_col].fillna("").str.strip()

    if wf[id_col].eq("").all():
        print(
            f"ERROR: All rows in '{id_col}' are still blank — "
            f"the workfile has not been filled in yet.\n"
            f"  Please open {conversion_path.name}, add the hangzhou_carrierservice_id "
            f"values, then re-run --merge.",
            file=sys.stderr,
        )
        sys.exit(1)

    valid_wf  = wf[wf[id_col].apply(_is_integer)][MERGE_KEY + [id_col]].copy()
    remove_wf = wf[~wf[id_col].apply(_is_integer)][MERGE_KEY + [id_col]].copy()

    print(f"  Valid integer IDs : {len(valid_wf)} combos")
    if not remove_wf.empty:
        print(f"  Removal markers   : {len(remove_wf)} combos")
        for _, r in remove_wf.iterrows():
            print(f"    REMOVE  {r['bs_warehouse_id']} / {r['bs_express_service_id']}"
                  f"  (value: {repr(r[id_col])})")

    # -- Load target CSV ----------------------------------------------
    if not csv_path.exists():
        print(f"ERROR: Target CSV not found: {csv_path.resolve()}", file=sys.stderr)
        sys.exit(1)

    df = pd.read_csv(csv_path, dtype=str)
    print(f"\nTarget CSV: {csv_path.name}  ({len(df)} rows, {df.shape[1]} cols)")

    for col in MERGE_KEY:
        if col not in df.columns:
            print(f"ERROR: Column '{col}' not found in target CSV.", file=sys.stderr)
            sys.exit(1)
    if id_col not in df.columns:
        print(f"ERROR: Column '{id_col}' not found in target CSV.", file=sys.stderr)
        sys.exit(1)

    # -- Drop removal rows --------------------------------------------
    if not remove_wf.empty:
        remove_keys = set(
            zip(remove_wf["bs_warehouse_id"], remove_wf["bs_express_service_id"])
        )
        mask_remove = df.apply(
            lambda row: (row["bs_warehouse_id"], row["bs_express_service_id"])
                        in remove_keys,
            axis=1,
        )
        n_removed = mask_remove.sum()
        df = df[~mask_remove].copy()
        print(f"\nRemoved {n_removed} rules row(s) matching removal-marker combos")
    else:
        print("\nNo removal markers — no rows dropped")

    # -- Fill hangzhou_carrierservice_id via merge --------------------
    # Drop any existing value in the column first, then left-join workfile
    df[id_col] = ""
    before_len = len(df)
    df = df.merge(
        valid_wf.rename(columns={id_col: "_new_id"}),
        on=MERGE_KEY,
        how="left",
    )
    assert len(df) == before_len, "Merge unexpectedly changed row count"

    filled = df["_new_id"].notna() & (df["_new_id"] != "")
    df.loc[filled, id_col] = df.loc[filled, "_new_id"]
    df.drop(columns=["_new_id"], inplace=True)

    n_filled   = filled.sum()
    n_unfilled = (~filled).sum()
    print(f"Filled hangzhou_carrierservice_id: {n_filled} row(s)")
    if n_unfilled:
        print(f"  WARNING: {n_unfilled} row(s) had no match in workfile "
              f"— hangzhou_carrierservice_id left blank")
        unmatched = df[~filled][MERGE_KEY].drop_duplicates()
        for _, r in unmatched.iterrows():
            print(f"    {r['bs_warehouse_id']} / {r['bs_express_service_id']}")

    # -- Write output -------------------------------------------------
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_name = f"{csv_path.stem}_merged_{timestamp}.csv"
    out_path = here / out_name
    df.to_csv(out_path, index=False, encoding="utf-8")
    print(f"\nOutput written: {out_path.resolve()}")
    print(f"  {len(df)} rows, {df.shape[1]} columns, encoding: UTF-8")


# ------------------------------------------------------------------ #
# Fix-routing mode                                                    #
# ------------------------------------------------------------------ #

BENELUX = {"BE", "NL", "LU"}


def _infer_domestic_country(warehouse_id: str) -> str | None:
    """Return the 2-letter country code from a warehouse ID suffix.
    e.g. YDY-DE → DE,  YC-FR-LEH → FR,  WP-DE02 → DE
    """
    for token in warehouse_id.split("-")[1:]:
        clean = re.sub(r"\d+$", "", token)
        if re.fullmatch(r"[A-Z]{2}", clean):
            return clean
    return None


def _parse_routing_note(note: str, domestic_country: str) -> dict | None:
    """Parse a *NOTE* routing string into {frozenset_of_countries | 'intl' -> id}.

    Supported patterns (may be combined with +):
      domesticN       → {domestic_country}: N
      intlN           → 'intl': N  (fallback for all non-domestic countries)
      de_esN          → {DE, ES}: N
      it_beneluxN     → {IT, BE, NL, LU}: N

    Returns None if the note contains no routing pattern.
    """
    if not re.search(r"domestic\d+", note):
        return None

    routing = {}
    for part in note.strip().split("+"):
        m = re.fullmatch(r"(domestic|intl|de_es|it_benelux)(\d+)", part)
        if not m:
            routing[f"UNKNOWN:{part}"] = None
            continue
        tag, cid = m.group(1), m.group(2)
        if tag == "domestic":
            routing[frozenset([domestic_country])] = cid
        elif tag == "intl":
            routing["intl"] = cid
        elif tag == "de_es":
            routing[frozenset(["DE", "ES"])] = cid
        elif tag == "it_benelux":
            routing[frozenset(["IT"] + list(BENELUX))] = cid
    return routing


def _resolve_country_id(country: str, routing: dict, domestic_country: str) -> str | None:
    """Return the correct carrier ID for a ship-to country given a routing dict."""
    for key, cid in routing.items():
        if isinstance(key, frozenset) and country in key:
            return cid
    if "intl" in routing and country != domestic_country:
        return routing["intl"]
    return None


def fix_routing(csv_path: Path) -> None:
    """Apply *NOTE* routing rules to correct hangzhou_carrierservice_id per row."""
    here = csv_path.parent
    conversion_path = here / CONVERSION_FILE

    if not csv_path.exists():
        print(f"ERROR: Input CSV not found: {csv_path.resolve()}", file=sys.stderr)
        sys.exit(1)
    if not conversion_path.exists():
        print(f"ERROR: Workfile not found: {conversion_path.resolve()}", file=sys.stderr)
        sys.exit(1)

    df = pd.read_csv(csv_path, dtype=str).fillna("")
    wf = pd.read_csv(conversion_path, dtype=str).fillna("")
    print(f"Input CSV : {csv_path.name}  ({len(df)} rows)")
    print(f"Workfile  : {conversion_path.name}  ({len(wf)} rows)")

    for required in ("bs_warehouse_id", "bs_express_service_id", "country",
                     "hangzhou_carrierservice_id"):
        if required not in df.columns:
            print(f"ERROR: Column '{required}' not found in input CSV.\n"
                  f"  --fixrouting requires the merged CSV (not the deduped or countries file).",
                  file=sys.stderr)
            sys.exit(1)

    # Build routing table from workfile NOTE rows
    routing_table = {}   # (warehouse, service) -> routing dict
    note_rows = wf[wf["*NOTE*"].str.contains(r"domestic\d+", regex=True, na=False)]
    for _, row in note_rows.iterrows():
        wh  = row["bs_warehouse_id"]
        svc = row["bs_express_service_id"]
        dom = _infer_domestic_country(wh)
        if dom is None:
            print(f"  WARNING: Cannot infer domestic country for warehouse '{wh}' — skipped")
            continue
        routing = _parse_routing_note(row["*NOTE*"], dom)
        if routing:
            routing_table[(wh, svc)] = (routing, dom)

    print(f"Routing rules loaded: {len(routing_table)} combo(s)")

    # Apply routing rules row by row
    id_col   = "hangzhou_carrierservice_id"
    changes  = []   # for log

    for idx, row in df.iterrows():
        key = (row["bs_warehouse_id"], row["bs_express_service_id"])
        if key not in routing_table:
            continue
        routing, dom = routing_table[key]
        new_id = _resolve_country_id(row["country"], routing, dom)
        if new_id and new_id != row[id_col]:
            changes.append({
                "sale_express_rules_id" : row["sale_express_rules_id"],
                "bs_warehouse_id"       : row["bs_warehouse_id"],
                "bs_express_service_id" : row["bs_express_service_id"],
                "country"               : row["country"],
                "old_id"                : row[id_col],
                "new_id"                : new_id,
            })
            df.at[idx, id_col] = new_id

    print(f"Cells updated: {len(changes)}")

    # Write output CSV
    timestamp  = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_path   = here / f"{csv_path.stem}_routed_{timestamp}.csv"
    log_path   = here / f"{csv_path.stem}_fixrouting_{timestamp}.log"

    df.to_csv(out_path, index=False, encoding="utf-8")
    print(f"\nOutput written : {out_path.resolve()}")
    print(f"  {len(df)} rows, {df.shape[1]} columns, encoding: UTF-8")

    # Write log
    log_lines = []
    log_lines.append(f"fixrouting run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log_lines.append(f"Input  : {csv_path.resolve()}  ({len(df)} rows)")
    log_lines.append(f"Changes: {len(changes)}")
    log_lines.append("")
    if changes:
        log_lines.append(f"{'sale_express_rules_id':<24} {'warehouse':<14} {'service':<40} "
                         f"{'country':<8} {'old_id':<8} {'new_id'}")
        log_lines.append("-" * 110)
        for c in changes:
            log_lines.append(
                f"{c['sale_express_rules_id']:<24} {c['bs_warehouse_id']:<14} "
                f"{c['bs_express_service_id']:<40} {c['country']:<8} "
                f"{c['old_id']:<8} → {c['new_id']}"
            )
    else:
        log_lines.append("No cells changed.")

    log_path.write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    print(f"Log written    : {log_path.resolve()}")


# ------------------------------------------------------------------ #
# Country-CSV mode                                                    #
# ------------------------------------------------------------------ #

def countrycsv(csv_path: Path) -> None:
    """Split country into a junction table and deduplicate the main table.

    Rows identical on all rule-logic columns (every column except
    sale_express_rules_id and country) are collapsed into one row.
    The row with the lowest sale_express_rules_id (as integer) is kept;
    the rest are dropped and logged.

    Outputs next to csv_path:
      <stem>_deduped_TIMESTAMP.csv    — main table, country column removed
      <stem>_countries_TIMESTAMP.csv  — junction: sale_express_rules_id, country
      <stem>_countrycsv_TIMESTAMP.log — human-readable dropped-ID log
    """
    if not csv_path.exists():
        print(f"ERROR: Input CSV not found: {csv_path.resolve()}", file=sys.stderr)
        sys.exit(1)

    df = pd.read_csv(csv_path, dtype=str)
    df = df.fillna("")
    print(f"Input: {csv_path.name}  ({len(df)} rows, {df.shape[1]} cols)")

    if "sale_express_rules_id" not in df.columns:
        print("ERROR: Column 'sale_express_rules_id' not found.", file=sys.stderr)
        sys.exit(1)
    if "country" not in df.columns:
        print("ERROR: Column 'country' not found.", file=sys.stderr)
        sys.exit(1)

    rule_cols = [c for c in df.columns if c not in ("sale_express_rules_id", "country")]

    # ------------------------------------------------------------------ #
    # 1. Identify duplicate groups on rule-logic columns                  #
    # ------------------------------------------------------------------ #
    # Assign a canonical ID (lowest integer) to every row via group key
    df["_group_key"] = df.groupby(rule_cols, sort=False, dropna=False).ngroup()

    dropped_ids   = []   # list of dicts for logging
    canonical_map = {}   # group_key -> canonical sale_express_rules_id (str)

    for gkey, grp in df.groupby("_group_key"):
        ids_sorted = sorted(grp["sale_express_rules_id"].tolist(), key=lambda x: int(x) if x.lstrip("-").isdigit() else float("inf"))
        canonical_map[gkey] = ids_sorted[0]
        if len(ids_sorted) > 1:
            countries = sorted(grp["country"].tolist())
            for dropped_id in ids_sorted[1:]:
                dropped_ids.append({
                    "dropped_id"   : dropped_id,
                    "canonical_id" : ids_sorted[0],
                    "group_size"   : len(ids_sorted),
                    "countries"    : countries,
                })

    df["_canonical_id"] = df["_group_key"].map(canonical_map)

    n_groups    = df["_group_key"].nunique()
    dup_groups  = [g for g, grp in df.groupby("_group_key") if len(grp) > 1]
    n_dropped   = len(dropped_ids)

    print(f"  Rule-logic groups : {n_groups}  (of which {len(dup_groups)} have duplicates)")
    print(f"  Rows to drop      : {n_dropped}")

    # ------------------------------------------------------------------ #
    # 2. Build countries junction table (before deduplication)            #
    # ------------------------------------------------------------------ #
    # Use canonical ID for all rows in each group
    countries_df = df[["_canonical_id", "country"]].copy()
    countries_df.columns = ["sale_express_rules_id", "country"]
    countries_df = countries_df.sort_values(
        ["sale_express_rules_id", "country"],
        key=lambda col: col.apply(lambda v: int(v) if v.lstrip("-").isdigit() else 0)
                        if col.name == "sale_express_rules_id" else col
    ).reset_index(drop=True)

    blank_country = (countries_df["country"] == "").sum()
    if blank_country:
        print(f"  WARNING: {blank_country} row(s) with blank country included in junction table as-is")

    # ------------------------------------------------------------------ #
    # 3. Build deduped main table                                         #
    # ------------------------------------------------------------------ #
    # Keep only the canonical row per group, drop country column
    keep_mask = df["sale_express_rules_id"] == df["_canonical_id"]
    deduped = df[keep_mask].drop(columns=["country", "_group_key", "_canonical_id"]).copy()
    deduped = deduped.sort_values(
        "sale_express_rules_id",
        key=lambda col: col.apply(lambda v: int(v) if v.lstrip("-").isdigit() else 0)
    ).reset_index(drop=True)

    print(f"  Output rows (deduped main) : {len(deduped)}")
    print(f"  Output rows (countries)    : {len(countries_df)}")

    # ------------------------------------------------------------------ #
    # 4. Write outputs                                                     #
    # ------------------------------------------------------------------ #
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    here      = csv_path.parent
    stem      = csv_path.stem

    deduped_path   = here / f"{stem}_deduped_{timestamp}.csv"
    countries_path = here / f"{stem}_countries_{timestamp}.csv"
    log_path       = here / f"{stem}_countrycsv_{timestamp}.log"

    deduped.to_csv(deduped_path, index=False, encoding="utf-8")
    print(f"\nDeduped main table written : {deduped_path.resolve()}")

    countries_df.to_csv(countries_path, index=False, encoding="utf-8")
    print(f"Countries junction written : {countries_path.resolve()}")

    # ------------------------------------------------------------------ #
    # 5. Write log                                                         #
    # ------------------------------------------------------------------ #
    log_lines = []
    log_lines.append(f"countrycsv run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log_lines.append(f"Input : {csv_path.resolve()}  ({len(df)} rows)")
    log_lines.append("")

    if not dropped_ids:
        log_lines.append("No duplicate rule groups found — no rows dropped.")
    else:
        # Group dropped entries by canonical_id for readability
        from itertools import groupby as igrp
        by_canonical = {}
        for entry in dropped_ids:
            by_canonical.setdefault(entry["canonical_id"], []).append(entry)

        log_lines.append(f"Duplicate rule groups collapsed: {len(dup_groups)} group(s), {n_dropped} row(s) dropped")
        log_lines.append("")
        for canonical_id, entries in sorted(by_canonical.items(), key=lambda x: int(x[0]) if x[0].isdigit() else 0):
            countries  = entries[0]["countries"]
            group_size = entries[0]["group_size"]
            dropped    = [e["dropped_id"] for e in entries]
            log_lines.append(
                f"  Canonical ID {canonical_id:>6}  |  group size {group_size}"
                f"  |  countries: {countries}"
            )
            log_lines.append(f"    Kept   : {canonical_id}")
            for did in dropped:
                log_lines.append(f"    Dropped: {did}")
            log_lines.append("")

    log_lines.append("--- Summary ---")
    log_lines.append(f"  Input rows             : {len(df)}")
    log_lines.append(f"  Duplicate groups found : {len(dup_groups)}")
    log_lines.append(f"  Rows dropped           : {n_dropped}")
    log_lines.append(f"  Output rows (deduped)  : {len(deduped)}")
    log_lines.append(f"  Output rows (countries): {len(countries_df)}")
    log_lines.append(f"  Deduped CSV  : {deduped_path.name}")
    log_lines.append(f"  Countries CSV: {countries_path.name}")
    log_lines.append(f"  This log     : {log_path.name}")

    log_path.write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    print(f"Log written                : {log_path.resolve()}")


# ------------------------------------------------------------------ #
# Main                                                                #
# ------------------------------------------------------------------ #

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert my_sale_express_rules.xlsx to CSV, or merge IDs into one."
    )
    parser.add_argument(
        "--merge",
        metavar="CSV_FILE",
        nargs="?",
        const="",           # flag present but no value given → auto-detect
        default=None,       # flag absent → default convert mode
        help=(
            "Merge hangzhou_carrierservice_id from the conversion workfile into "
            "CSV_FILE. If CSV_FILE is omitted, the latest my_sale_express_rules_*.csv "
            "in the current directory is used."
        ),
    )
    parser.add_argument(
        "--fixrouting",
        metavar="CSV_FILE",
        nargs="?",
        const="",
        default=None,
        help=(
            "Correct hangzhou_carrierservice_id per row using *NOTE* routing rules. "
            "CSV_FILE should be a *_merged_*.csv; if omitted, the latest such file "
            "in the current directory is used."
        ),
    )
    parser.add_argument(
        "--countrycsv",
        metavar="CSV_FILE",
        nargs="?",
        const="",           # flag present but no value given → auto-detect
        default=None,
        help=(
            "Normalise country into a junction table and deduplicate the main table. "
            "CSV_FILE should be a *_routed_*.csv (after --fixrouting) or a "
            "*_merged_*.csv; if omitted, the latest *_routed_*.csv is used, "
            "falling back to the latest *_merged_*.csv."
        ),
    )
    args = parser.parse_args()

    if args.merge is not None:
        # --merge mode
        if args.merge == "":
            # auto-detect latest matching CSV
            candidates = sorted(
                Path(".").glob("my_sale_express_rules_*.csv"),
                key=lambda p: p.stat().st_mtime,
                reverse=True,
            )
            # exclude already-merged files
            candidates = [p for p in candidates if "_merged_" not in p.name]
            if not candidates:
                print(
                    "ERROR: No my_sale_express_rules_*.csv file found in the current "
                    "directory. Specify the file explicitly: --merge FILE.csv",
                    file=sys.stderr,
                )
                sys.exit(1)
            csv_path = candidates[0]
            print(f"Auto-detected target CSV: {csv_path.name}")
        else:
            csv_path = Path(args.merge)
        merge_ids(csv_path)
        return

    if args.fixrouting is not None:
        # --fixrouting mode
        if args.fixrouting == "":
            candidates = sorted(
                Path(".").glob("my_sale_express_rules_*_merged_*.csv"),
                key=lambda p: p.stat().st_mtime,
                reverse=True,
            )
            # exclude derivative files produced by later pipeline steps
            candidates = [
                p for p in candidates
                if not any(tag in p.name for tag in ("_routed_", "_deduped_", "_countries_"))
            ]
            if not candidates:
                print(
                    "ERROR: No *_merged_*.csv file found. "
                    "Specify the file explicitly: --fixrouting FILE.csv",
                    file=sys.stderr,
                )
                sys.exit(1)
            csv_path = candidates[0]
            print(f"Auto-detected target CSV: {csv_path.name}")
        else:
            csv_path = Path(args.fixrouting)
        fix_routing(csv_path)
        return

    if args.countrycsv is not None:
        # --countrycsv mode
        if args.countrycsv == "":
            # auto-detect: prefer *_routed_*.csv, fall back to *_merged_*.csv
            candidates = sorted(
                Path(".").glob("my_sale_express_rules_*_routed_*.csv"),
                key=lambda p: p.stat().st_mtime,
                reverse=True,
            )
            if not candidates:
                candidates = sorted(
                    Path(".").glob("my_sale_express_rules_*_merged_*.csv"),
                    key=lambda p: p.stat().st_mtime,
                    reverse=True,
                )
            if not candidates:
                print(
                    "ERROR: No *_merged_*.csv file found in the current directory. "
                    "Specify the file explicitly: --countrycsv FILE.csv",
                    file=sys.stderr,
                )
                sys.exit(1)
            csv_path = candidates[0]
            print(f"Auto-detected target CSV: {csv_path.name}")
        else:
            csv_path = Path(args.countrycsv)
        countrycsv(csv_path)
        return

    # ------------------------------------------------------------------
    # Default convert mode (original behaviour below, unchanged)
    # ------------------------------------------------------------------
    input_path = Path(INPUT_FILE)
    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_path.resolve()}", file=sys.stderr)
        sys.exit(1)

    # ------------------------------------------------------------------ #
    # 1. Read — keep everything as strings to avoid numeric coercion      #
    # ------------------------------------------------------------------ #
    print(f"Reading: {input_path.resolve()}")
    df = pd.read_excel(input_path, sheet_name=SHEET_NAME, dtype=str)
    print(f"  Loaded {df.shape[0]} rows x {df.shape[1]} columns")

    # ------------------------------------------------------------------ #
    # 2. Drop columns that are 100% empty (all NaN / blank)               #
    #    Tested dynamically on the actual file contents.                  #
    # ------------------------------------------------------------------ #
    all_null_cols = [col for col in df.columns if df[col].isnull().all()]
    if all_null_cols:
        print(f"\nDropping {len(all_null_cols)} fully-empty column(s):")
        for col in all_null_cols:
            print(f"  - {col}")
        df = df.drop(columns=all_null_cols)
    else:
        print("\nNo fully-empty columns found — nothing to drop.")
    print(f"  Shape after drop: {df.shape[0]} rows x {df.shape[1]} columns")

    # ------------------------------------------------------------------ #
    # 3. Fix whitespace bugs                                               #
    # ------------------------------------------------------------------ #
    print("\nScanning for whitespace bugs ...")
    total_fixes = 0
    for col in df.columns:
        original = df[col].copy()
        df[col] = df[col].apply(fix_whitespace)
        # only compare non-null cells that actually changed
        changed_mask = df[col].notna() & (df[col] != original)
        n = changed_mask.sum()
        if n:
            print(f"  Column '{col}': {n} fix(es)")
            for idx in df.index[changed_mask]:
                print(f"    row {idx}: {repr(original[idx])} -> {repr(df[col][idx])}")
            total_fixes += n

    if total_fixes == 0:
        print("  No whitespace bugs found.")
    else:
        print(f"  Total fixes: {total_fixes}")

    # ------------------------------------------------------------------ #
    # 4. Denormalise: bs_warehouse_id -> warehouse name                   #
    # ------------------------------------------------------------------ #
    warehouse_path = input_path.parent / WAREHOUSE_FILE
    print(f"\nLoading warehouse lookup: {warehouse_path.name}")
    wh_lookup = load_warehouse_lookup(warehouse_path)
    print(f"  {len(wh_lookup)} entries loaded")
    df["bs_warehouse_id"] = apply_lookup(df["bs_warehouse_id"], wh_lookup, "bs_warehouse_id")
    print("  bs_warehouse_id replaced with warehouse names")

    # ------------------------------------------------------------------ #
    # 5. Denormalise: bs_express_service_id -> express>service>show_name  #
    # ------------------------------------------------------------------ #
    es_path = input_path.parent / EXPRESS_SERVICE_FILE
    print(f"\nLoading express service lookup: {es_path.name}")
    es_lookup = load_express_service_lookup(es_path)
    print(f"  {len(es_lookup)} entries loaded")
    df["bs_express_service_id"] = apply_lookup(
        df["bs_express_service_id"], es_lookup, "bs_express_service_id"
    )
    print("  bs_express_service_id replaced with express>service>show_name labels")

    # ------------------------------------------------------------------ #
    # 6. Insert empty 'hangzhou_carrierservice_id' after bs_express_service_id #
    # ------------------------------------------------------------------ #
    insert_after = "bs_express_service_id"
    insert_pos = df.columns.get_loc(insert_after) + 1
    df.insert(insert_pos, "hangzhou_carrierservice_id", "")
    print(f"\nInserted empty column 'hangzhou_carrierservice_id' "
          f"at position {insert_pos} (after '{insert_after}')")

    # ------------------------------------------------------------------ #
    # 7. Write UTF-8 CSV with timestamp suffix                            #
    # ------------------------------------------------------------------ #
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_name = f"{input_path.stem}_{timestamp}.csv"
    output_path = input_path.parent / output_name

    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"\nOutput written: {output_path.resolve()}")
    print(f"  {df.shape[0]} rows, {df.shape[1]} columns, encoding: UTF-8")

    # ------------------------------------------------------------------ #
    # 8. Write conversion helper CSV for manual hangzhou_carrierservice_id #
    #    mapping — one row per unique (bs_warehouse_id, bs_express_service_id) #
    #    combination, sorted by rules_qty descending.                      #
    #    Skipped if the file already exists (protect manual edits).        #
    # ------------------------------------------------------------------ #
    conversion_path = input_path.parent / CONVERSION_FILE
    if conversion_path.exists():
        print(f"\nConversion workfile already exists — NOT overwritten: {conversion_path.name}")
        print(f"  (Delete it manually if you want a fresh one.)")
    else:
        counts = (
            df.groupby(["bs_warehouse_id", "bs_express_service_id"], dropna=False)
            .size()
            .reset_index(name="rules_qty")
            .sort_values("rules_qty", ascending=False)
            .reset_index(drop=True)
        )
        counts["hangzhou_carrierservice_id"] = ""
        counts.to_csv(conversion_path, index=False, encoding="utf-8")
        print(f"\nConversion workfile written: {conversion_path.resolve()}")
        print(f"  {len(counts)} unique express service labels")


if __name__ == "__main__":
    main()
