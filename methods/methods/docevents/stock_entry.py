import frappe
from frappe.utils import get_link_to_form

def check_pr_vs_se_qty(self, method):
    if self.stock_entry_type == "Material Transfer":
        #Check Landed cost voucher exist or not
        #stock transfer should not allow greater then purchase receipt
        for row in self.items:
            if row.reference_purchase_receipt and row.pr_details:
                if not frappe.db.exists('Landed Cost Purchase Receipt', { "receipt_document" : row.reference_purchase_receipt, "docstatus" : 1, "parenttype": 'Landed Cost Voucher' }):
                    frappe.throw("Landed Cost Voucher is not submitted against purchase receipt {0}, Please submit Landed Cost Voucher to create Material transfer.".format(get_link_to_form("Purchase Receipt", row.reference_purchase_receipt)))
                pr_qty = frappe.db.get_value("Purchase Receipt Item", row.pr_details, "qty")
                if row.qty > pr_qty:
                    frappe.throw(f"Row #{row.idx} : Material transfer Qty should not be greater than Purchase receipt Qty")
        

from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def make_stock_entry(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.stock_entry_type = "Material Transfer"
		target.purpose = "Material Transfer"
		target.set_missing_values()

	doclist = get_mapped_doc(
		"Purchase Receipt",
		source_name,
		{
			"Purchase Receipt": {
				"doctype": "Stock Entry",
			},
			"Purchase Receipt Item": {
				"doctype": "Stock Entry Detail",
				"field_map": {
					"warehouse": "s_warehouse",
					"parent": "reference_purchase_receipt",
					"batch_no": "batch_no",
                    "name" : "pr_details"
				},
			},
		},
		target_doc,
		set_missing_values,
	)

	return doclist