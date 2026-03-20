hangzhou_carrierserviceid_conversion_README.txt
Generated: 2026-03-05
===============================================================

This file documents rows in hangzhou_carrierserviceid_conversion.csv
that carry a *NOTE* and require further attention before or during
the final PostgreSQL import.

There are two categories of issues:


===============================================================
CATEGORY A — Carrier service needs splitting by destination
           (12 rows, 9 warehouse/service combinations)
===============================================================

These combinations have been assigned a single hangzhou_carrierservice_id
in the workfile, but in reality the correct ID depends on the destination
country (domestic vs. international, or by region).

The current CSV only stores one ID per (warehouse, express_service) pair.
The import script — or a pre-import enrichment step — will need to
distinguish by the ship-to country and route to the correct ID.

The required splits are listed below. "Domestic" refers to shipments
within the carrier's home country; "intl" to cross-border shipments
within Europe.

  1. YDY-DE  /  DHL > DHL-欧洲仓库生成
     Currently assigned ID : 68  (domestic)
     Also requires         : 69  (international)
     Split logic           : domestic → 68  |  international → 69

  2. YDY-DE  /  DHL > PAKET_INTERNATIONAL > 德国发欧盟
     Currently assigned ID : 69  (international)
     Also requires         : 68  (domestic)
     Split logic           : domestic → 68  |  international → 69
     NOTE: This is the counterpart row to item 1 above.
           Together they cover the full domestic+international range.

  3. YDY-DE  /  DPD > DPD-欧洲仓库生成
     Currently assigned ID : 70  (domestic)
     Also requires         : 71  (international)
     Split logic           : domestic → 70  |  international → 71

  4. YDY-DE  /  GLS > GLS-欧洲仓库生成
     Currently assigned ID : 72  (domestic)
     Also requires         : 73  (international)
     Split logic           : domestic → 72  |  international → 73

  5. YC-FR  /  GLS > GLS-欧洲仓库生成
     Currently assigned ID : 45  (domestic)
     Also requires         : 46  (international)
     Split logic           : domestic → 45  |  international → 46

  6. YC-FR-LEH  /  GLS > GLS-欧洲仓库生成
     Currently assigned ID : 45  (domestic)
     Also requires         : 46  (international)
     Split logic           : domestic → 45  |  international → 46

  7. WP-DE02  /  DHL > DHL-欧洲仓库生成
     Currently assigned ID : 28  (domestic)
     Also requires         : 29  (international)
     Split logic           : domestic → 28  |  international → 29

  8. WP-DE02  /  GLS > GLS-欧洲仓库生成
     Currently assigned ID : 32  (domestic)
     Also requires         : 33  (international)
     Split logic           : domestic → 32  |  international → 33

  9. WP-DE02  /  DPD > DPD-欧洲仓库生成
     Currently assigned ID : 30  (domestic)
     Also requires         : 31  (international)
     Split logic           : domestic → 30  |  international → 31

 10. YC-FR  /  DPD > DPD-欧洲仓库生成
     Currently assigned ID : 47  (domestic)
     Also requires         : 48  (international)
     Split logic           : domestic → 47  |  international → 48

 11. YC-FR  /  Geodis > Geodis-法国遨森
     Currently assigned ID : 49  (domestic France)
     Also requires         : 50  (DE + ES)
                             51  (IT + Benelux)
     Split logic           : France (domestic) → 49
                             Germany, Spain     → 50
                             Italy, Benelux     → 51

 12. YC-FR-LEH  /  Geodis > Geodis-法国遨森
     Currently assigned ID : 49  (domestic France)
     Also requires         : 50  (DE + ES)
                             51  (IT + Benelux)
     Split logic           : France (domestic) → 49
                             Germany, Spain     → 50
                             Italy, Benelux     → 51

Action required:
  The import script must not use a flat hangzhou_carrierservice_id lookup
  for these combinations. Instead it must evaluate the ship-to country
  (from the countries junction table) and select the correct ID accordingly.


===============================================================
CATEGORY B — Placeholder ID: carrier service not yet in DB
           (1 row)
===============================================================

  SHAOKE-FR  /  GLS > GLS-欧洲仓库生成
     Assigned ID : 100  ← PLACEHOLDER, does not exist in production yet

  This carrier service entry still needs to be created in the Hangzhou
  production PostgreSQL database. The ID 100 is a temporary placeholder
  used in the workfile to keep the row processable.

Action required:
  1. Create the carrier service record in the production DB.
  2. Update hangzhou_carrierserviceid_conversion.csv with the real ID.
  3. Re-run the pipeline (--merge → --countrycsv) to regenerate the CSVs.


===============================================================
END OF README
===============================================================
