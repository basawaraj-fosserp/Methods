# Copyright (c) 2024, viral Patel and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from erpnext.stock.utils import get_stock_balance

def execute(filters=None):
	columns, data = [], []
	columns, data = get_sold_sle_data(filters)
	return columns, data


def get_sold_sle_data(filters):
	condition = ''
	if filters.get("company"):
		condition += f" and sle.company = '{filters.get('company')}'"
	if filters.get("item_code"):
		condition += f" and sle.item_code = '{filters.get('item_code')}'"
	if filters.get("warehouse"):
		condition += f" and sle.warehouse = '{filters.get('warehouse')}'"
	if filters.get("from_date"):
		condition += f" and sle.posting_date >= '{filters.get('from_date')}'"
	if filters.get("to_date"):
		condition += f" and sle.posting_date <= '{filters.get('to_date')}'"
	
	data = frappe.db.sql(f"""
			Select  sle.warehouse, sle.item_code, sum(sle.actual_qty) * -1 as actual_qty, sum(dni.amount) as amount, dni.item_group, dni.item_name
			From `tabStock Ledger Entry` as sle
			Left Join `tabDelivery Note Item` as dni ON dni.parent = sle.voucher_no and sle.item_code = dni.item_code and sle.warehouse = dni.warehouse
			left Join `tabDelivery Note Item` as dn ON dn.name = dni.parent and dn.customer != 'Methods Automotive Pvt Ltd - GGN'
			Where sle.is_cancelled = 0  and sle.voucher_type in ('Delivery Note', 'Sales Invoice') and dn.customer != 'Methods Automotive Pvt Ltd - GGN' {condition}
			Group By sle.item_code
			Order by sle.item_code
		""", as_dict=1)

	warehouse = []
	for row in data:
		if row.warehouse not in warehouse:
			warehouse.append(row.warehouse)
		
	warehouse_list = frappe.db.get_list("Warehouse", { "is_group" : 0 , "company" : filters.get("company")}, pluck="name")

	columns = get_columns(filters, warehouse)
	warehouse_column = []
	
	for row in data:
		warehouse_column.append(row.warehouse)
		warehouse_qty = get_stock_balance(
							row.item_code,
							row.warehouse,
							posting_date = filters.get("to_date")
						)
		row.update({ row.warehouse : warehouse_qty })

		for d in warehouse_list:
			if row.warehouse != d:
				warehouse_qty = get_stock_balance(
									row.item_code,
									d,
									posting_date = filters.get("to_date")
								)
				if warehouse_qty:
					if d not in warehouse_column:
						columns.append({
							"fieldname" : d,
							"label" : d,
							"fieldtype" : "Float",
							"width" : 150
						})
						warehouse_column.append(d)
						row.update({ d : warehouse_qty })

	return columns, data

def get_columns(filters, warehouse):
	columns = [
		{
			"fieldname": "item_group",
			"label": "Item Group",
			"fieldtype": "Link",
			"options": "Item Group",
			"width" : 150
		},
		{
			"fieldname": "item_code",
			"label": "Item",
			"fieldtype": "Link",
			"options": "Item",
			"width" : 150
		},
		{
			"fieldname": "item_name",
			"label": "Item Name",
			"fieldtype": "Data",
			"width" : 150
		},
		{
			"fieldname": "warehouse",
			"label": "warehouse",
			"fieldtype": "Link",
			"options": "Warehouse",
			"width" : 150
		},
		{
			
			"fieldname": "actual_qty",
			"label": "Quantity",
			"fieldtype": "Float",
			"width" : 150
		},
		{
			
			"fieldname": "amount",
			"label": "Amount",
			"fieldtype": "Float",
			"width" : 150
		},
	]
	if not filters.get("warehouse"):
		for row in warehouse:
			columns.append({
				"fieldname" : row,
				"label" : row,
				"fieldtype" : "Float",
				"width" : 150
			})
	else:
		columns.append({
			"fieldname" : filters.get("warehouse"),
			"label" : filters.get("warehouse"),
			"fieldtype" : "Float",
			"width" : 150
		})
	return columns