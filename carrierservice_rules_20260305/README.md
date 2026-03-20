# Carrier Service Rules — ERP Migration Converter

## Background

The legacy ERP system (MySQL) stores carrier service routing rules in the table
`my_sale_express_rules`. These rules determine which carrier and service level
applies to a shipment based on warehouse, destination country, and parcel
dimensions/weight.

The goal of this project is to migrate these rules into the new Hangzhou
PostgreSQL database. The two systems use incompatible foreign keys:

| Legacy ERP | Hangzhou DB |
|---|---|
| `bs_warehouse_id` (integer) | warehouse label (human-readable) |
| `bs_express_service_id` (integer) | `hangzhou_carrierservice_id` (integer, different IDs) |

The Python script `carrierservice_rules_converter.py` bridges this gap through
a four-step pipeline that converts, cleans, maps, and normalises the data into
two CSV files ready for import.

---

## File Inventory

### Source data (do not modify)
| File | Description |
|---|---|
| `my_sale_express_rules.xlsx` | Source rules — 446 rows, 32 cols, sheet `my_sale_express_rules` |
| `bs_warehouse.xlsx` | Warehouse lookup: `bs_warehouse_id` → warehouse label |
| `express_service.xlsx` | Express service lookup: `bs_express_service_id` → `express>service>show_name` label |
| `my_sale_express_rules.sql` | MySQL table definition — reference only |

### Reference data (gathered during analysis, not used directly in pipeline)
| File | Description |
|---|---|
| `express.xlsx` | Express carrier master data |
| `bs_chanpin.xlsx` | Product reference data |
| `bs_zhanghu.xlsx` | Account reference data |

### Workfiles (manually maintained — handle with care)
| File | Description |
|---|---|
| `hangzhou_carrierserviceid_conversion.csv` | **Critical.** Maps each (warehouse, express_service) combination to its Hangzhou `hangzhou_carrierservice_id`. Manually filled from the production PostgreSQL DB. The converter will **never overwrite this file** if it already exists. |
| `hangzhou_carrierserviceid_conversion_README.txt` | Documents rows with `*NOTE*` annotations: routing splits (domestic vs. international IDs) and the placeholder ID 100. Read before import. |

### Scripts
| File | Description |
|---|---|
| `carrierservice_rules_converter.py` | Main pipeline script — see usage below |
| `analyse_note_routing.py` | One-off analysis script used during development to verify routing resolution. Not part of the pipeline; kept for reference. |

### Generated outputs (timestamped)
All output files are written with a `_YYYYMMDD-HHMMSS` timestamp suffix so
that re-runs never overwrite previous results.

| Pattern | Produced by | Description |
|---|---|---|
| `my_sale_express_rules_TIMESTAMP.csv` | Step 1 (default) | Cleaned, denormalised rules with empty `hangzhou_carrierservice_id` |
| `..._merged_TIMESTAMP.csv` | Step 3 (`--merge`) | IDs filled, defunct warehouse rows removed |
| `..._routed_TIMESTAMP.csv` | Step 4 (`--fixrouting`) | Per-row carrier IDs corrected by destination country |
| `..._deduped_TIMESTAMP.csv` | Step 5 (`--countrycsv`) | **Final main table** — deduplicated, `country` column removed |
| `..._countries_TIMESTAMP.csv` | Step 5 (`--countrycsv`) | **Final junction table** — `sale_express_rules_id` + `country` |
| `..._countrycsv_TIMESTAMP.log` | Step 5 (`--countrycsv`) | Log of deduplicated/dropped rule IDs |
| `..._fixrouting_TIMESTAMP.log` | Step 4 (`--fixrouting`) | Log of every corrected `hangzhou_carrierservice_id` cell |

---

## Pipeline Overview

```
XLSX source
    │
    ▼
[Step 1 — default]  Clean + denormalise → timestamped CSV
                                        → hangzhou_carrierserviceid_conversion.csv (blank, first run only)
    │
    ▼
[Step 2 — MANUAL]   Fill hangzhou_carrierserviceid_conversion.csv
                    with real Hangzhou PostgreSQL IDs
    │
    ▼
[Step 3 — --merge]  Transpose IDs into CSV; remove defunct warehouse rows
    │
    ▼
[Step 4 — --fixrouting]  Correct IDs per destination country (domestic vs. intl)
    │
    ▼
[Step 5 — --countrycsv]  Split country into junction table; deduplicate rules
    │
    ▼
_deduped_.csv   +   _countries_.csv   →   ready for PostgreSQL import
```

---

## Detailed Steps

### Step 1 — Convert (default mode)

**Command:**
```bash
python3 carrierservice_rules_converter.py
```

**What it does:**
- Reads `my_sale_express_rules.xlsx` (sheet `my_sale_express_rules`), keeping all values as strings to prevent numeric coercion
- Drops the 9 columns that are 100% NULL in the dataset (detected dynamically)
- Fixes whitespace bugs in range-notation values — e.g. `LTE_ 39.5` → `LTE_39.5`, spaces around `@` separator
- Denormalises `bs_warehouse_id` → warehouse label (from `bs_warehouse.xlsx`)
- Denormalises `bs_express_service_id` → `express>service>show_name` label (from `express_service.xlsx`)
- Inserts an empty `hangzhou_carrierservice_id` column immediately after `bs_express_service_id`
- Writes a timestamped UTF-8 CSV (446 rows → 24 columns after drop + insert)
- **On first run only:** writes a blank `hangzhou_carrierserviceid_conversion.csv` — one row per unique `(bs_warehouse_id, bs_express_service_id)` combination, sorted by frequency. On subsequent runs the workfile is left untouched.

**Known data quality issues left as-is (handled downstream):**
- 102 rows with `ctime = 0` (no creation timestamp recorded in legacy system)
- 1 row with null `country`
- `auto_refresh_count`: only value present is `2` (250 rows); remainder null

---

### Step 2 — Manual: Fill the ID workfile

**File:** `hangzhou_carrierserviceid_conversion.csv`

This is the critical manual step. A person with access to the Hangzhou
production PostgreSQL database opened the workfile and filled in the
`hangzhou_carrierservice_id` column for each (warehouse, express_service) pair.

The workfile has 69 rows. Three types of entries were made:

| Entry type | Example value | Meaning |
|---|---|---|
| Valid integer ID | `68` | Maps to a real carrier service in the Hangzhou DB |
| Removal marker | `REMOVE_THESE_RULES (Warehouse not in use anymore)` | Warehouse is decommissioned; all matching rules will be dropped |
| Placeholder | `100` | Carrier service not yet created in the Hangzhou DB; see README.txt |

A `*NOTE*` column was also added manually for entries that require the
import script to distinguish by destination country (see Step 4).

**Result of this run:**
- 65 valid integer IDs (later updated to 66 after warehouse `189` was added to `bs_warehouse.xlsx`)
- 3 removal markers (BS-DE and BGE-FR warehouses, 44 rules rows removed)
- 1 placeholder (SHAOKE-FR / GLS → ID 100, not yet in production)

> ⚠ The script guards against accidentally running `--merge` before this step
> is complete: if all `hangzhou_carrierservice_id` values in the workfile are
> blank, `--merge` will exit with a clear error.

---

### Step 3 — Merge (`--merge`)

**Command:**
```bash
python3 carrierservice_rules_converter.py --merge
# or specify file explicitly:
python3 carrierservice_rules_converter.py --merge my_sale_express_rules_TIMESTAMP.csv
```

**What it does:**
- Loads the workfile; splits entries into valid integer IDs vs. removal markers
- Drops all rules rows whose `(bs_warehouse_id, bs_express_service_id)` matches a removal marker
- Left-joins the valid IDs into the remaining rows on `(bs_warehouse_id, bs_express_service_id)`
- Warns about any `(warehouse, service)` combination present in the rules CSV but missing from the workfile
- Auto-detects the latest `my_sale_express_rules_*.csv` in the current directory if no file is given (excludes already-merged files)
- Output: `..._merged_TIMESTAMP.csv`

**Result of this run:** 446 rows → 402 rows (44 removed); all 402 remaining rows filled.

---

### Step 4 — Fix Routing (`--fixrouting`)

**Command:**
```bash
python3 carrierservice_rules_converter.py --fixrouting
# or specify file explicitly:
python3 carrierservice_rules_converter.py --fixrouting ..._merged_TIMESTAMP.csv
```

**Background:**
The initial merge assigns one `hangzhou_carrierservice_id` per
`(warehouse, express_service)` pair. However, 12 such combinations require
different carrier IDs depending on the destination country — for example,
`YDY-DE / DHL` should use ID `68` for domestic Germany shipments but ID `69`
for all other European destinations. This split information was captured in the
`*NOTE*` column of the workfile during the manual step.

**What it does:**
- Parses `*NOTE*` routing strings into structured rules:
  - `domestic68+intl69` → DE→68, all other countries→69
  - `domestic49+de_es50+it_benelux51` → FR→49, DE/ES→50, IT/BE/NL/LU→51
- Infers the domestic country from the warehouse ID suffix: `YDY-DE`→DE, `YC-FR`→FR, `YC-FR-LEH`→FR, `WP-DE02`→DE
- Updates `hangzhou_carrierservice_id` row-by-row based on the `country` column
- Rows not covered by any `*NOTE*` routing rule are left unchanged
- Writes a detailed log of every changed cell
- Output: `..._routed_TIMESTAMP.csv`

**Result of this run:** 34 cells corrected, all in `YDY-DE` warehouse
(DHL: 22 rows `68→69`; DPD: 12 rows `70→71` for non-DE destinations).
All other NOTE-affected warehouses had only domestic-country rows in this
dataset, so their IDs required no correction.

> See `hangzhou_carrierserviceid_conversion_README.txt` for the full list of
> routing splits and the outstanding placeholder ID.

---

### Step 5 — Country CSV (`--countrycsv`)

**Command:**
```bash
python3 carrierservice_rules_converter.py --countrycsv
# or specify file explicitly:
python3 carrierservice_rules_converter.py --countrycsv ..._routed_TIMESTAMP.csv
```

**What it does:**
- Identifies rows that are identical on all 22 rule-logic columns (every column
  except `sale_express_rules_id` and `country`) — these represent the same rule
  applied to multiple countries, stored redundantly in the legacy system
- Collapses each duplicate group to one row, keeping the lowest
  `sale_express_rules_id` as the canonical primary key; dropped IDs are logged
- Removes the `country` column from the main table
- Builds a junction table: `sale_express_rules_id` (FK) + `country`
- Auto-detects the latest `*_routed_*.csv`; falls back to `*_merged_*.csv`
- Outputs:
  - `..._deduped_TIMESTAMP.csv` — main rules table
  - `..._countries_TIMESTAMP.csv` — country junction table
  - `..._countrycsv_TIMESTAMP.log` — log of dropped IDs

**Result of this run:**
- 4 duplicate groups found (14 rows → 4 canonical rows; 10 rows dropped)
- **392 rows** in the deduped main table (23 columns)
- **402 rows** in the countries junction table (2 columns)
- 1 row with blank country included in junction table as-is

---

## Final Import Files

The two files produced by Step 5 are the import targets:

| File | Rows | Columns | Role in DB |
|---|---|---|---|
| `..._routed_..._deduped_TIMESTAMP.csv` | 392 | 23 | Main rules table — one row per unique rule, PK: `sale_express_rules_id` |
| `..._routed_..._countries_TIMESTAMP.csv` | 402 | 2 | Junction table — FK: `sale_express_rules_id` → country |

Range columns (`gross_weight`, `max_length`, etc.) still carry their
`GT_`/`GTE_`/`LT_`/`LTE_`/`@` notation and are converted to PostgreSQL range
types by the existing import script.

---

## Known Issues & Outstanding Items

1. **Placeholder ID 100** — `SHAOKE-FR / GLS > GLS-欧洲仓库生成` uses ID `100`
   which does not yet exist in the Hangzhou production DB. Create the carrier
   service record, update `hangzhou_carrierserviceid_conversion.csv`, and
   re-run the pipeline from `--merge` onwards.

2. **Blank country row** — 1 rule has a null destination country (inherited
   from the legacy system). It appears in the junction table with an empty
   `country` field. The import script must handle or skip this row explicitly.

3. **Routing splits not fully exercised** — Several `*NOTE*` combinations
   (YC-FR, WP-DE02, YC-FR-LEH) currently only have domestic-country rows in
   the dataset. If new international rules are added to these warehouses in
   future, `--fixrouting` will correctly assign the international IDs
   automatically — but the routing logic should be verified at that point.

4. **`ctime`/`mtime = 0`** — 102 rows carry Unix timestamp `0` (no creation
   time recorded). These are passed through as-is; the import script should
   treat `0` as NULL.

---

## Quick Command Reference

```bash
# Full pipeline (first run — workfile does not yet exist)
python3 carrierservice_rules_converter.py          # Step 1: convert
# → manually fill hangzhou_carrierserviceid_conversion.csv
python3 carrierservice_rules_converter.py --merge       # Step 3: merge IDs
python3 carrierservice_rules_converter.py --fixrouting  # Step 4: fix routing
python3 carrierservice_rules_converter.py --countrycsv  # Step 5: normalise

# Re-run from merge onwards (workfile already filled)
python3 carrierservice_rules_converter.py --merge       --merge FILE.csv (optional)
python3 carrierservice_rules_converter.py --fixrouting  --fixrouting FILE.csv (optional)
python3 carrierservice_rules_converter.py --countrycsv  --countrycsv FILE.csv (optional)

# Help
python3 carrierservice_rules_converter.py --help
```

All modes auto-detect their input file (latest matching pattern in the current
directory) when no file argument is given.
