# Carrier Service Rules — Import Quick Start

## The two files you need

| File | Description |
|---|---|
| `..._routed_..._deduped_....csv` | **Main rules table.** One row per unique carrier routing rule. PK: `sale_express_rules_id`. Range columns (`gross_weight`, `max_length`, etc.) use `GT_`/`GTE_`/`LT_`/`LTE_`/`@` notation — convert to PostgreSQL range types as usual. |
| `..._routed_..._countries_....csv` | **Destination country junction table.** Two columns: `sale_express_rules_id` (FK → main table) and `country` (ISO 2-letter code). One row per rule–country pair. |

The main table has no `country` column — the one-to-many relationship is fully
expressed through the junction table.

## Carrier service foreign key

Use `hangzhou_carrierservice_id` as the FK to the carrier service table in the
Hangzhou DB.

The column `bs_express_service_id` contains a human-readable label
(`express>service>show_name`) carried over from the legacy ERP for traceability.
**It does not need to be imported** and can be dropped before or during import.

## Known issues to handle in the import script

- **1 row** in the junction table has a blank `country` — treat as NULL or skip.
- **ID 100** (`SHAOKE-FR / GLS`) is a placeholder; the carrier service record
  does not yet exist in the Hangzhou DB. Skip or handle separately.
- `ctime`/`mtime` values of `0` should be treated as NULL.

## Steps to reproduce (if re-running from scratch)

```bash
python3 carrierservice_rules_converter.py            # convert XLSX → CSV
# manually fill hangzhou_carrierserviceid_conversion.csv
python3 carrierservice_rules_converter.py --merge
python3 carrierservice_rules_converter.py --fixrouting
python3 carrierservice_rules_converter.py --countrycsv
```

See `README.md` for full documentation.
