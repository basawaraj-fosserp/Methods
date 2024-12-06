import frappe
import json

@frappe.whitelist(allow_guest=True)
def get_so_ref(sales_order, data):
	data = json.loads(data)
	name = frappe.db.get_value("Sales Order Item", {"item_code": data.get('item_code'), "parent": sales_order},'name')
	if name:
		data.update({"against_sales_order": sales_order, "so_detail" : name})
		return {}
	return data