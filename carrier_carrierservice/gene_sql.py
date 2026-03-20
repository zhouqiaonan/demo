

def gene_fulfillment_supplier():
    with open("./fulfilment_supplier.csv", "r") as f:
        with open("carrier_carrierservice.sql", "w") as wf:
            cnt = 0
            insert_str = f"insert into logistics_fulfilment_suppliers(\nid,code,name_en,name_cn,created_time,updated_time,is_deleted) \nvalues\n"
            for line in f:
                line = line.strip()
                print(line)
                cnt += 1
                line_lst = line.split(",")
                print(line_lst)
                id = line_lst[0]
                code = line_lst[1] if line_lst[1] else None
                name_en = line_lst[2] if line_lst[2] else None
                name_cn = line_lst[3] if line_lst[3] else None
                if cnt == 1:
                    continue
                else:
                    insert_str = f"{insert_str}({sql_val(id)},{sql_val(code)},{sql_val(name_en)},{sql_val(name_cn)},NOW(),NOW(),FALSE),\n"
            insert_str = insert_str[:-2] + ";"
            print(f"{'='*80}")
            print(insert_str)
            wf.write(insert_str)

def sql_val(val):
    if val is None:
        return 'NULL'
    if isinstance(val, str):
        return f'{val.replace("\"", "'")}'
    return str(val)


def gene_carrier():
    with open("./carrier.csv", "r") as f:
        with open("carrier_carrierservice.sql", "w") as wf:
            cnt = 0
            insert_str = f"insert into logistics_carriers(\nid,fulfilment_supplier_id,code,name_en,name_cn,created_time,updated_time,is_deleted) \nvalues\n"
            for line in f:
                line = line.strip()
                line_lst = line.split(",")
                id = line_lst[0]
                fulfilment_supplier_id = line_lst[1] if line_lst[1] else None
                code = line_lst[2] if line_lst[2] else None
                name_en = line_lst[3] if line_lst[3] else None
                name_cn = line_lst[4] if line_lst[4] else None
                print(line_lst)
                cnt += 1
                if cnt == 1:
                    continue
                else:
                    insert_str = f"{insert_str}({sql_val(id)},{sql_val(fulfilment_supplier_id)},{sql_val(code)},{sql_val(name_en)},{sql_val(name_cn)},NOW(),NOW(),FALSE),\n"
            insert_str = insert_str[:-2] + ";"
            print(f"{'=' * 80}")
            print(insert_str)
            wf.write(insert_str)


def gene_carrier_carrierservice():
    with open("./carrier_service.csv", "r") as f:
        with open("carrier_carrierservice.sql", "w") as wf:
            cnt = 0
            insert_str = f"insert into logistics_carrier_services(\nid,carrier_id,code,name_en,name_cn,service_type,destination_type,created_time,updated_time,is_deleted) \nvalues\n"
            for line in f:
                line = line.strip()
                line_lst = line.split(",")
                id = line_lst[0]
                carrier_id = line_lst[1] if line_lst[1] else None
                code = line_lst[2] if line_lst[2] else None
                name_en = line_lst[3] if line_lst[3] else None
                name_cn = line_lst[4] if line_lst[4] else None
                service_type = line_lst[5] if line_lst[5] else None
                destination_type = line_lst[6] if line_lst[6] else None
                cnt += 1
                if cnt == 1:
                    continue
                else:
                    insert_str = f"{insert_str}({sql_val(id)},{sql_val(carrier_id)},{sql_val(code)},{sql_val(name_en)},{sql_val(name_cn)},{sql_val(service_type)},{sql_val(destination_type)},NOW(),NOW(),FALSE),\n"
            insert_str = insert_str[:-2] + ";"
            print(f"{'=' * 80}")
            print(insert_str)
            wf.write(insert_str)


def gene_carrier_service_api_parameter():
    with open("./carrier_service_api_parameter.csv", "r") as f:
        with open("carrier_carrierservice.sql", "w") as wf:
            cnt = 0
            insert_str = f"insert into logistics_carrier_service_api_parameters(\nid,carrier_service_id,api_key,api_value,created_time,updated_time,is_deleted) \nvalues\n"
            for line in f:
                line = line.strip()
                line_lst = line.split(",")
                id = line_lst[0]
                carrier_service_id = line_lst[1] if line_lst[1] else None
                api_key = line_lst[2] if line_lst[2] else None
                api_value = line_lst[3] if line_lst[3] else None
                cnt += 1
                if cnt == 1:
                    continue
                else:
                    insert_str = f"{insert_str}({sql_val(id)},{sql_val(carrier_service_id)},{sql_val(api_key)},{sql_val(api_value)},NOW(),NOW(),FALSE),\n"
            insert_str = insert_str[:-2] + ";"
            print(f"{'=' * 80}")
            print(insert_str)
            wf.write(insert_str)


def gene_carrier_service_warehouse_relation():
    with open("./carrier_service_warehouse_relation.csv", "r") as f:
        with open("carrier_carrierservice.sql", "w") as wf:
            cnt = 0
            insert_str = f"insert into logistics_carrier_service_warehouse_relations(\nid,carrier_service_id,warehouse_id) \nvalues\n"
            for line in f:
                line = line.strip()
                line_lst = line.split(",")
                id = line_lst[0]
                carrier_service_id = line_lst[1] if line_lst[1] else None
                warehouse_name = line_lst[3] if line_lst[3] else None
                cnt += 1
                if cnt == 1:
                    continue
                else:
                    insert_str = f"{insert_str}({sql_val(id)},{sql_val(carrier_service_id)},(select id from basedata_warehouses where name={sql_val(warehouse_name)})),\n"
            insert_str = insert_str[:-2] + ";"
            print(f"{'=' * 80}")
            print(insert_str)
            wf.write(insert_str)

if __name__ == '__main__':
    # gene_fulfillment_supplier()
    # gene_carrier()
    gene_carrier_carrierservice()
    # gene_carrier_service_api_parameter()
    # gene_carrier_service_warehouse_relation()
