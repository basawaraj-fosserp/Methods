import frappe

def check_pr_vs_se_qty(self, method):
    for row in self.items:
        if row.reference_purchase_receipt and row.pr_details:
            pr_qty = frappe.db.get_value("Purchase Receipt Item", row.pr_details, "qty")
            if row.qty > pr_qty:
                  frappe.throw(f"Row #{row.idx} : Material Transfer not allow greater then purchase receipt qty")
        

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