import pandas as pd
import argparse
import sys

# ==========================================
# CONFIGURATION & CONSTANTS
# ==========================================

# Human-readable mapping for rule types
RULE_TYPE_NAMES = {
    0: "StandardOrder",
    1: "AmazonPrimeOrder",
    2: "AmazonPrimeButTreatAsStandardOrder",
    3: "NextDayDeliveryOrder"
}

# The test order to be used if no arguments are provided
test_order = {
    'order_type': 0,           # 0: StandardOrder
    'is_prime': 0,             # 0: No
    'country': 'DE',
    'postcode': '70589',
    'shop': 'Amazon-Saili-UK', 
    'sku': 'G-HAD0444BG-A'
}

# ==========================================
# PART 1: DATA LOADING & CLEANING
# ==========================================

def load_and_prep_data():
    """
    Loads raw Excel data and converts IDs/Codes into 
    efficient Python Dictionaries (Hash Maps).
    """
    print("Loading Excel files...")
    
    # 1. Load the main Fencang file (contains multiple sheets)
    try:
        fencang_data_excel = pd.read_excel('fencang_data.xlsx', sheet_name=None, engine='openpyxl')
    except FileNotFoundError:
        print("[ERROR] 'fencang_data.xlsx' not found. Please ensure all Excel files are in the same folder.")
        return None

    # 2. Load the Reference Tables (Warehouses, Shops, SKUs)
    # We use .fillna(0) and .astype(int) to ensure IDs are integers
    
    # Load Warehouses
    df_wh = pd.read_excel('bs_warehouse.xlsx', sheet_name=0, engine='openpyxl')
    warehouse_map = dict(zip(df_wh['bs_warehouse_id'].fillna(0).astype(int), df_wh['warehouse']))

    # Load Shops (Accounts)
    df_shops = pd.read_excel('bs_zhanghu.xlsx', sheet_name=0, engine='openpyxl')
    shop_map = dict(zip(df_shops['bs_account_id'].fillna(0).astype(int), df_shops['account']))

    # Load SKUs (Products)
    df_skus = pd.read_excel('bs_chanpin.xlsx', sheet_name=0, engine='openpyxl')
    sku_map = dict(zip(df_skus['pr_product_id'].fillna(0).astype(int), df_skus['sku']))

    # Load Countries
    df_countries = fencang_data_excel['my_sale_rules_country']
    country_map = dict(zip(df_countries['sale_rules_country_id'].fillna(0).astype(int), df_countries['country']))

    # 3. Load Postcode Ranges
    df_zips = fencang_data_excel['my_sale_rules_zip']
    zip_range_map = {}
    for _, row in df_zips.iterrows():
        z_id = int(row['sale_rules_zip_id'])
        try:
            start = int(str(row['begin']).strip())
            end = int(str(row['end']).strip())
            zip_range_map[z_id] = (start, end)
        except (ValueError, TypeError):
            continue

    # 4. Load Rules and Relations
    df_rules = fencang_data_excel['my_sale_rules']
    df_relations = fencang_data_excel['my_sale_rules_relation']

    return {
        'warehouse_map': warehouse_map,
        'shop_map': shop_map,
        'sku_map': sku_map,
        'country_map': country_map,
        'zip_range_map': zip_range_map,
        'df_rules': df_rules,
        'df_relations': df_relations
    }


# ==========================================
# PART 2: THE COMPILER (PROCESS LOGIC)
# ==========================================

def compile_rules(data, include_inactive=False):
    """
    Takes the raw data and builds a list of "Smart Rule" objects.
    Each object contains all the necessary conditions pre-calculated.
    
    Args:
        include_inactive (bool): If True, processes ALL rules (useful for migration).
                                 If False, processes only ACTIVE rules (useful for routing).
    """
    mode_text = "ALL" if include_inactive else "ACTIVE only"
    print(f"Compiling logic rules ({mode_text})...")
    
    df_rules = data['df_rules']
    df_relations = data['df_relations']
    
    # Sort rules by sort_order from high to low
    df_rules_sorted = df_rules.sort_values(by='sort_order', ascending=False)

    # Group relations by sale_rules_id for fast lookup
    relations_grouped = df_relations.groupby('sale_rules_id')

    compiled_rules_list = []

    for _, row in df_rules_sorted.iterrows():
        is_active = int(row['active'])
        
        # If we are in "Active Only" mode and rule is inactive, skip it
        if not include_inactive and is_active != 1:
            continue

        rule_id = int(row['sale_rules_id'])
        
        # Resolve Human Readable Names immediately
        wh_name = data['warehouse_map'].get(int(row['warehouse_id']), "Unknown_Warehouse")
        
        # Initialize the Smart Rule Object
        rule_obj = {
            'id': rule_id,
            'title': row['title'],
            'active': bool(is_active),
            'sort_order': int(row['sort_order']),
            'rule_type': int(row['rule_type']),
            'is_prime': int(row['is_prime']), # 0 or 1
            'target_warehouse_name': wh_name,
            # Conditions
            'allowed_countries': set(),
            'allowed_shops': set(),
            'allowed_skus': set(),
            'allowed_zip_ranges': [] 
        }

        # Fetch conditions
        if rule_id in relations_grouped.groups:
            conditions = relations_grouped.get_group(rule_id)
            
            for _, cond_row in conditions.iterrows():
                c_type = int(cond_row['type'])
                real_id = int(cond_row['real_id'])

                # Type 4: Country
                if c_type == 4:
                    country_code = data['country_map'].get(real_id)
                    if country_code:
                        rule_obj['allowed_countries'].add(country_code)
                
                # Type 3: Shop
                elif c_type == 3:
                    shop_name = data['shop_map'].get(real_id)
                    if shop_name:
                        rule_obj['allowed_shops'].add(shop_name)

                # Type 2: SKU
                elif c_type == 2:
                    sku_name = data['sku_map'].get(real_id)
                    if sku_name:
                        rule_obj['allowed_skus'].add(sku_name)

                # Type 1: Postcode
                elif c_type == 1:
                    z_range = data['zip_range_map'].get(real_id)
                    if z_range:
                        rule_obj['allowed_zip_ranges'].append(z_range)

        compiled_rules_list.append(rule_obj)
    
    print(f"Successfully compiled {len(compiled_rules_list)} rules.")
    return compiled_rules_list


# ==========================================
# PART 3: THE SOLVER (MATCHING ENGINE)
# ==========================================

def find_warehouse(order, rules_list):
    """
    Standard Logic to find a warehouse for a given order.
    """
    try:
        order_zip = int(str(order['postcode']).strip())
    except ValueError:
        raise ValueError(f"Invalid Postcode in order: {order['postcode']}")

    order_country = order['country']
    order_shop = order['shop']
    order_sku = order['sku']
    order_type = int(order['order_type'])
    order_is_prime = int(order['is_prime'])

    for rule in rules_list:
        # Rules list in solver mode only contains ACTIVE rules, 
        # but double check just in case.
        if not rule['active']:
            continue 

        if rule['rule_type'] != order_type: continue 
        
        if rule['is_prime'] != order_is_prime: continue

        if rule['allowed_countries'] and order_country not in rule['allowed_countries']: continue
        if rule['allowed_shops'] and order_shop not in rule['allowed_shops']: continue
        if rule['allowed_skus'] and order_sku not in rule['allowed_skus']: continue

        if rule['allowed_zip_ranges']:
            is_in_range = False
            for (start, end) in rule['allowed_zip_ranges']:
                if start <= order_zip <= end:
                    is_in_range = True
                    break
            if not is_in_range: continue 

        return {
            'status': 'success',
            'warehouse': rule['target_warehouse_name'],
            'matched_rule_id': rule['id'],
            'matched_rule_title': rule['title']
        }

    return {'status': 'error', 'message': 'No matching rule found.'}


def inspect_rule(target_id, rules_list):
    """
    Prints detailed information about a specific rule ID.
    """
    print(f"\n[INSPECTING RULE ID]: {target_id}")
    print("="*60)

    found_rule = next((r for r in rules_list if r['id'] == target_id), None)

    if found_rule:
        type_name = RULE_TYPE_NAMES.get(found_rule['rule_type'], f"Unknown({found_rule['rule_type']})")
        prime_status = "is_prime=true" if found_rule['is_prime'] == 1 else "is_prime=false"
        rule_active = "ACTIVE" if found_rule['active'] else "INACTIVE"
        status_txt = "Active" if found_rule['active'] else "Inactive"

        print(f"[STATUS]: {status_txt}")
        print(f"Title:  {found_rule['title']}")
        print(f"Warehouse: {found_rule['target_warehouse_name']}")
        print(f"Sort/Order: {found_rule['sort_order']}")
        print("-" * 60)
        
        print(f"  [Gate 1] Rule Active?   : {rule_active}")
        print(f"  [Gate 2] Order Type     : {type_name}")
        print(f"  [Gate 3] Prime Status   : {prime_status}")
        
        ctries = ' / '.join(found_rule['allowed_countries']) if found_rule['allowed_countries'] else "**ALL ALLOWED**"
        print(f"  [Gate 4] Countries      : {ctries}")
            
        shops = ' / '.join(found_rule['allowed_shops']) if found_rule['allowed_shops'] else "**ALL ALLOWED**"
        print(f"  [Gate 5] Shops          : {shops}")
            
        skus = ' / '.join(found_rule['allowed_skus']) if found_rule['allowed_skus'] else "**ALL ALLOWED**"
        print(f"  [Gate 6] SKUs           : {skus}")
            
        zips = found_rule['allowed_zip_ranges'] if found_rule['allowed_zip_ranges'] else "**ALL ALLOWED**"
        print(f"  [Gate 7] Postcodes      : {zips}")

    else:
        print("[STATUS]: NOT FOUND")
        print("   This ID does not exist in the loaded rules.")
            
    print("="*60 + "\n")


# ==========================================
# PART 4: CONVERSION (EXPORT TO CSV)
# ==========================================

def run_conversion_mode(rules_list):
    """
    Exports the compiled rules into normalized CSV files 
    ready for Django ERP import.
    """
    print("\n[CONVERSION MODE] Generating CSV files for ERP Import...")
    
    # Lists to store rows for the CSVs
    rows_main = []
    rows_countries = []
    rows_shops = []
    rows_skus = []
    rows_postcodes = []
    
    for rule in rules_list:
        r_id = rule['id']
        
        # 1. Main Rule Table
        # Converting rule_type int to String name for better readability/import
        r_type_str = RULE_TYPE_NAMES.get(rule['rule_type'], "Unknown")
        
        rows_main.append({
            'rule_id': r_id,
            'name': rule['title'],
            'sort_order': rule['sort_order'],
            'rule_is_active': rule['active'],
            'order_type': r_type_str,
            'condition_is_prime_order': bool(rule['is_prime']),
            'target_warehouse_name': rule['target_warehouse_name']
        })
        
        # 2. Conditions: Countries
        for c in rule['allowed_countries']:
            rows_countries.append({'rule_id': r_id, 'country_code': c})
            
        # 3. Conditions: Shops
        for s in rule['allowed_shops']:
            rows_shops.append({'rule_id': r_id, 'shop_name': s})
            
        # 4. Conditions: SKUs
        for sku in rule['allowed_skus']:
            rows_skus.append({'rule_id': r_id, 'sku_string': sku})
            
        # 5. Conditions: Postcodes
        for (start, end) in rule['allowed_zip_ranges']:
            rows_postcodes.append({
                'rule_id': r_id, 
                'range_start': start, 
                'range_end': end
            })
            
    # Create DataFrames and Save
    print("Saving 'erp_import_rules.csv'...")
    pd.DataFrame(rows_main).to_csv('erp_import_rules.csv', index=False)
    
    print("Saving 'erp_import_conditions_countries.csv'...")
    pd.DataFrame(rows_countries).to_csv('erp_import_conditions_countries.csv', index=False)
    
    print("Saving 'erp_import_conditions_shops.csv'...")
    pd.DataFrame(rows_shops).to_csv('erp_import_conditions_shops.csv', index=False)
    
    print("Saving 'erp_import_conditions_skus.csv'...")
    pd.DataFrame(rows_skus).to_csv('erp_import_conditions_skus.csv', index=False)
    
    print("Saving 'erp_import_conditions_postcodes.csv'...")
    pd.DataFrame(rows_postcodes).to_csv('erp_import_conditions_postcodes.csv', index=False)
    
    print("\n[DONE] All files generated successfully.")


# ==========================================
# MAIN EXECUTION BLOCK
# ==========================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Warehouse Allocation Router')
    parser.add_argument('-id', type=int, help='Specific Rule ID to inspect')
    parser.add_argument('--convert', action='store_true', help='Convert data to CSV for ERP import')
    
    # Handle "id254" syntax manually
    if len(sys.argv) > 1 and sys.argv[1].startswith('id') and sys.argv[1][2:].isdigit():
        manual_id = int(sys.argv[1][2:])
        sys.argv = [sys.argv[0]]
        args = parser.parse_args()
        args.id = manual_id
        args.convert = False
    else:
        args = parser.parse_args()

    # Load Data
    raw_data = load_and_prep_data()
    
    if raw_data:
        # Determine if we need inactive rules
        include_inactive = True if args.convert else True if args.id else False
        
        # Compile
        rules_engine = compile_rules(raw_data, include_inactive=include_inactive)

        # 1. Convert Mode
        if args.convert:
            run_conversion_mode(rules_engine)
            
        # 2. Inspect Mode
        elif args.id:
            inspect_rule(args.id, rules_engine)
        
        # 3. Test Mode (Active rules only for simulation)
        else:
            # Re-compile strictly for active rules to simulate real behavior
            active_rules_engine = [r for r in rules_engine if r['active']]
            
            print("\n--- Running Test Order ---")
            
            print(f"Checking Order: {test_order}")
            result = find_warehouse(test_order, active_rules_engine)
            
            if result['status'] == 'success':
                print(f"[SUCCESS] Ship from: {result['warehouse']}")
                print(f"   (Matched Rule: {result['matched_rule_title']} [ID: {result['matched_rule_id']}])")
                inspect_rule(result['matched_rule_id'], rules_engine)
            else:
                print(f"[FAILED] {result['message']}")