import frappe
from frappe.utils import nowdate, add_days, get_first_day

def execute(filters=None):
    yesterday = add_days(nowdate(), -1)
    month_start = get_first_day(yesterday)

    columns = [
        {"label": "Supplier", "fieldname": "supplier", "fieldtype": "Link", "options": "Supplier", "width": 200},
        {"label": "Orders (Yesterday)", "fieldname": "orders_yesterday", "fieldtype": "Int", "width": 150},
        {"label": "Order Value (Yesterday)", "fieldname": "value_yesterday", "fieldtype": "Currency", "width": 180},
        {"label": "Orders (Month to Yesterday)", "fieldname": "orders_mtd", "fieldtype": "Int", "width": 200},
        {"label": "Order Value (Month to Yesterday)", "fieldname": "value_mtd", "fieldtype": "Currency", "width": 220},
    ]

    conditions = ["po.docstatus < 2"]
    params = {
        "yesterday": yesterday,
        "month_start": month_start
    }

    # Filter: Supplier (single select)
    if filters.get("supplier"):
        conditions.append("po.supplier = %(supplier)s")
        params["supplier"] = filters.get("supplier")

    # Filter: Exclude Supplier (multi-select)
    # Filter: Exclude Supplier (multi-select)
    if filters.get("exclude_supplier"):
        exclude_suppliers = filters.get("exclude_supplier")
        if isinstance(exclude_suppliers, list) and exclude_suppliers:
            conditions.append("po.supplier NOT IN %(exclude_suppliers)s")
            params["exclude_suppliers"] = tuple(exclude_suppliers)

    # Filter: Exclude Supplier Group (multi-select)
    if filters.get("exclude_supplier_group"):
        exclude_groups = filters.get("exclude_supplier_group")
        if isinstance(exclude_groups, list) and exclude_groups:
            conditions.append("""
                po.supplier NOT IN (
                    SELECT name FROM `tabSupplier`
                    WHERE supplier_group IN %(exclude_groups)s
                )
            """)
            params["exclude_groups"] = tuple(exclude_groups)


    where_clause = " AND ".join(conditions)

    data = frappe.db.sql(f"""
        SELECT
            po.supplier,
            SUM(CASE WHEN Date(po.creation) = %(yesterday)s THEN 1 ELSE 0 END) AS orders_yesterday,
            SUM(CASE WHEN Date(po.creation) = %(yesterday)s THEN po.base_grand_total ELSE 0 END) AS value_yesterday,
            SUM(CASE WHEN Date(po.creation) BETWEEN %(month_start)s AND %(yesterday)s THEN 1 ELSE 0 END) AS orders_mtd,
            SUM(CASE WHEN Date(po.creation) BETWEEN %(month_start)s AND %(yesterday)s THEN po.base_grand_total ELSE 0 END) AS value_mtd
        FROM
            `tabPurchase Order` po
        WHERE {where_clause}
        GROUP BY po.supplier
        HAVING orders_mtd > 0
        ORDER BY po.supplier
    """, params, as_dict=True)


    return columns, data
