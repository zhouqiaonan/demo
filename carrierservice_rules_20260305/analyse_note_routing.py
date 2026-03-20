#!/usr/bin/env python3
"""
analyse_note_routing.py

Analyses whether *NOTE* routing rules in hangzhou_carrierserviceid_conversion.csv
can be automatically resolved to per-row hangzhou_carrierservice_id values using
the country column still present in the merged CSV.

Domestic country is inferred from the warehouse ID suffix:
  e.g. YDY-DE → DE,  YC-FR → FR,  YC-FR-LEH → FR,  WP-DE02 → DE
"""

import re
import pandas as pd
from pathlib import Path

MERGED_CSV     = "my_sale_express_rules_20260305-130436_merged_20260305-131028.csv"
WORKFILE_CSV   = "hangzhou_carrierserviceid_conversion.csv"
MERGE_KEY      = ["bs_warehouse_id", "bs_express_service_id"]

# ------------------------------------------------------------------ #
# Known Benelux countries (for Geodis 3-way split)                    #
# ------------------------------------------------------------------ #
BENELUX = {"BE", "NL", "LU"}


# ------------------------------------------------------------------ #
# Parse NOTE strings into routing dicts                               #
# ------------------------------------------------------------------ #

def parse_note(note: str, domestic_country: str) -> dict | None:
    """
    Parse a *NOTE* value into a {country_set_or_tag -> carrier_id} dict.

    Supported formats:
      "domesticX+intlY"                     → {domestic_country: X, intl: Y}
      "domesticX+intlY+..."                 → same pattern extended
      "domesticX+de_esY+it_beneluxZ"        → {FR:X, DE+ES:Y, IT+BE+NL+LU:Z}
      "New CarrierService"                  → None (not a routing rule)
    """
    note = note.strip()

    # Not a routing rule
    if not re.search(r"domestic\d+", note):
        return None

    parts = note.split("+")
    routing = {}

    for part in parts:
        m_domestic = re.fullmatch(r"domestic(\d+)", part)
        m_intl     = re.fullmatch(r"intl(\d+)", part)
        m_de_es    = re.fullmatch(r"de_es(\d+)", part)
        m_it_benelux = re.fullmatch(r"it_benelux(\d+)", part)

        if m_domestic:
            routing[frozenset([domestic_country])] = m_domestic.group(1)
        elif m_intl:
            routing["intl"] = m_intl.group(1)
        elif m_de_es:
            routing[frozenset(["DE", "ES"])] = m_de_es.group(1)
        elif m_it_benelux:
            routing[frozenset(["IT"] + list(BENELUX))] = m_it_benelux.group(1)
        else:
            routing[f"UNKNOWN_PART:{part}"] = None

    return routing


def infer_domestic_country(warehouse_id: str) -> str | None:
    """
    Infer the domestic country code from a warehouse ID.
    Uses the first 2-letter uppercase token after a hyphen that looks like
    a country code (e.g. YDY-DE → DE, YC-FR-LEH → FR, WP-DE02 → DE).
    """
    tokens = warehouse_id.split("-")
    for token in tokens[1:]:           # skip the first part (warehouse prefix)
        clean = re.sub(r"\d+$", "", token)   # strip trailing digits (e.g. DE02 → DE)
        if re.fullmatch(r"[A-Z]{2}", clean):
            return clean
    return None


def resolve_country(country: str, routing: dict, domestic_country: str) -> str | None:
    """
    Given a ship-to country and a routing dict, return the correct carrier ID.
    Returns None if the country cannot be resolved.
    """
    for key, carrier_id in routing.items():
        if key == "intl":
            continue   # fallback, handled below
        if isinstance(key, frozenset) and country in key:
            return carrier_id

    # Fall back to intl if present and country is not domestic
    if "intl" in routing and country != domestic_country:
        return routing["intl"]

    return None


# ------------------------------------------------------------------ #
# Main analysis                                                        #
# ------------------------------------------------------------------ #

def main():
    merged  = pd.read_csv(MERGED_CSV, dtype=str).fillna("")
    wf      = pd.read_csv(WORKFILE_CSV, dtype=str).fillna("")

    note_rows = wf[wf["*NOTE*"] != ""].copy()
    print(f"Workfile rows with *NOTE*: {len(note_rows)}\n")

    # Only routing-type notes (not "New CarrierService")
    note_rows = note_rows[note_rows["*NOTE*"].str.contains(r"domestic\d+", regex=True)]
    print(f"Routing-type NOTE rows   : {len(note_rows)}")
    print("=" * 70)

    all_resolvable   = []
    all_unresolvable = []

    for _, wf_row in note_rows.iterrows():
        warehouse   = wf_row["bs_warehouse_id"]
        service     = wf_row["bs_express_service_id"]
        current_id  = wf_row["hangzhou_carrierservice_id"]
        note        = wf_row["*NOTE*"]

        domestic_cc = infer_domestic_country(warehouse)
        routing     = parse_note(note, domestic_cc) if domestic_cc else None

        # Get the actual rows from the merged CSV for this combo
        mask = (
            (merged["bs_warehouse_id"] == warehouse) &
            (merged["bs_express_service_id"] == service)
        )
        combo_rows = merged[mask][["sale_express_rules_id", "country",
                                   "hangzhou_carrierservice_id"]].copy()

        print(f"\n{'─'*70}")
        print(f"Warehouse : {warehouse}  (inferred domestic: {domestic_cc})")
        print(f"Service   : {service}")
        print(f"NOTE      : {note}")
        print(f"Current hangzhou_carrierservice_id: {current_id}")
        print(f"Routing parsed: {dict(routing) if routing else 'FAILED'}")
        print(f"Rows in merged CSV: {len(combo_rows)}")

        if routing is None or combo_rows.empty:
            print("  → SKIP (no routing rule or no data rows)")
            continue

        # Try to resolve each row
        resolved   = []
        unresolved = []
        for _, row in combo_rows.iterrows():
            country    = row["country"]
            new_id     = resolve_country(country, routing, domestic_cc)
            status     = "OK" if new_id else "UNRESOLVED"
            resolved.append({
                "sale_express_rules_id" : row["sale_express_rules_id"],
                "country"               : country,
                "old_id"                : row["hangzhou_carrierservice_id"],
                "new_id"                : new_id or "?",
                "changed"               : new_id and new_id != row["hangzhou_carrierservice_id"],
                "status"                : status,
            })
            if not new_id:
                unresolved.append(country)

        res_df = pd.DataFrame(resolved)
        print(res_df[["sale_express_rules_id","country","old_id","new_id","status"]].to_string(index=False))

        if unresolved:
            print(f"  *** UNRESOLVED countries: {sorted(set(unresolved))}")
            all_unresolvable.extend([(warehouse, service, c) for c in unresolved])
        else:
            print(f"  ✓ All {len(resolved)} row(s) resolvable automatically")
            all_resolvable.extend(resolved)

    # ------------------------------------------------------------------ #
    # Summary                                                             #
    # ------------------------------------------------------------------ #
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    total = len(all_resolvable) + len(all_unresolvable)
    print(f"  Total rows analysed  : {total}")
    print(f"  Automatically resolved : {len(all_resolvable)}")
    print(f"  Unresolvable           : {len(all_unresolvable)}")
    if all_unresolvable:
        print(f"  Unresolvable details:")
        for warehouse, service, country in all_unresolvable:
            print(f"    {warehouse} / {service} / country={repr(country)}")


if __name__ == "__main__":
    main()
