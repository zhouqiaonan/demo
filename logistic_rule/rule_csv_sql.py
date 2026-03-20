

def rule_sql(wf):
    with open('erp_import_rules.csv', 'r', encoding="utf-8") as rf:
        cnt = 0
        for line in rf:
            if cnt > 0:

                line_lst = line.strip().split(",")
                data = {
                    "id": line_lst[0],
                    "name": line_lst[1],
                    "sort_order": line_lst[2],
                    "is_active": line_lst[3],
                    "order_type": line_lst[4],
                    "is_prime": line_lst[5],
                    "warehouse_name": line_lst[6],
                }
                if data["warehouse_name"] in ["FBA-Linyu-AU", "FBA-Petnniko-AU", "BGE-FR", "BS-DE", "Unknown_Warehouse"]:
                    continue
                insert_str = f"insert into logistics_rules(id,name,sort_order,is_active,order_type,is_prime,warehouse_id,created_time,updated_time,is_deleted) values({data['id']},'{data["name"]}',{data["sort_order"]},{data["is_active"]},'{data["order_type"]}',{data["is_prime"]},(select id from basedata_warehouses where name='{data["warehouse_name"]}'),NOW(),NOW(),FALSE);\n"
                wf.write(insert_str)
            cnt += 1


def rule_product_item_skus(wf):
    with open('erp_import_conditions_skus.csv', 'r', encoding="utf-8") as rf:
        cnt = 0
        for line in rf:
            if cnt > 0:
                line_lst = line.strip().split(",")
                data = {
                    "rule_id": line_lst[0],
                    "product_item_sku": line_lst[1]
                }
                insert_str = f"insert into logistics_rule_product_item_sku_relations(rule_id,product_item_id,created_time,updated_time,is_deleted,remarks) values({data['rule_id']},(select id from product_items where item_sku='{data["product_item_sku"]}'),NOW(),NOW(),FALSE,\'\');\n"
                wf.write(insert_str)
            cnt += 1


def rule_shops(wf):
    with open('erp_import_conditions_shops.csv', 'r', encoding="utf-8") as rf:
        cnt = 0
        for line in rf:
            if cnt > 0:
                line_lst = line.strip().split(",")
                data = {
                    "rule_id": line_lst[0],
                    "shop_name": line_lst[1]
                }
                insert_str = f"insert into logistics_shop_relations(rule_id,shop_id,created_time,updated_time,is_deleted,remarks) values({data['rule_id']},(select id from basedata_shops where name_ningbo like '%{data["shop_name"]}%'),NOW(),NOW(),FALSE,\'\');\n"
                wf.write(insert_str)
            cnt += 1


def rule_territories(wf):
    with open('erp_import_conditions_countries.csv', 'r', encoding="utf-8") as rf:
        names = ["FBA-Linyu-AU", "FBA-Petnniko-AU", "BGE-FR", "BS-DE", "Unknown_Warehouse"]
        ids = [459, 458, [253, 425], [317, 340, 258], 460]
        exclusive_data = dict(zip(names, ids))
        print(exclusive_data)
        exclusive_ids = []
        for id_a in ids:
            if isinstance(id_a, list):
                exclusive_ids.extend(id_a)
            else:
                exclusive_ids.append(id_a)
        exclusive_lst = []
        cnt = 0
        for line in rf:
            if cnt > 0:
                line_lst = line.strip().split(",")
                data = {
                    "rule_id": line_lst[0],
                    "alpha_2": line_lst[1]
                }
                if int(data["rule_id"]) in exclusive_ids:
                    exclusive_lst.append(data)
                    continue
                insert_str = f"insert into logistics_rule_territory_relations(rule_id,territory_id,created_time,updated_time,is_deleted,remarks) values({data['rule_id']},(select id from basedata_territories where alpha_2='{data["alpha_2"]}'),NOW(),NOW(),FALSE,\'\');\n"
                wf.write(insert_str)
            cnt += 1
        print(f"exclusive_lst = {exclusive_lst}")


def rule_postcode(wf):
    with open('erp_import_conditions_postcodes.csv', 'r', encoding="utf-8") as rf:
        cnt = 0
        for line in rf:
            if cnt > 0:
                line_lst = line.strip().split(",")
                data = {
                    "rule_id": line_lst[0],
                    "range_start": line_lst[1],
                    "range_end": line_lst[2]
                }
                insert_str = f"insert into logistics_rule_postcodes(rule_id,range_start,range_end,created_time,updated_time,is_deleted) values({data['rule_id']},{data['range_start']},{data['range_end']},NOW(),NOW(),FALSE);\n"
                print(insert_str)
                wf.write(insert_str)
            cnt += 1


if __name__ == '__main__':
    print("Start")
    with open("rule_csv_sql.txt", "w", encoding="utf-8") as wf:
        # rule_sql(wf)
        # rule_product_item_skus(wf)
        rule_shops(wf)
        # rule_territories(wf)
        # rule_postcode(wf)
    print("Success!")

