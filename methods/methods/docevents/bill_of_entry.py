import frappe

def check_quantity_overflow(self, method):
    for row in self.items:
        if row.pi_detail:
            pi_data = frappe.db.sql("Select sum(qty) as total_qty From `tabBill of Entry Item` where docstatus = 1 and pi_detail = '{0}' and parent != '{1}' ".format(row.pi_detail, self.name), as_dict=True)
            total_qty = frappe.db.get_value("Purchase Invoice Item", row.pi_detail, 'qty')
            if pi_data[0].get("total_qty"):
                if pi_data[0].get("total_qty") + row.qty > total_qty:
                    frappe.throw(f"Row #{row.idx} : Bill of Entry already created for {pi_data[0].get('total_qty')} qty. Not allowed to create Bill of Entry greater then purchase invoice qty {total_qty}.")




from india_compliance.gst_india.doctype.bill_of_entry.bill_of_entry import BillofEntry, set_missing_values

class CustomBillofEntry(BillofEntry):
    @frappe.whitelist()
    def get_items_from_purchase_invoice(self, purchase_invoices):
        frappe.has_permission("Bill Of Entry", "write")
        frappe.has_permission("Purchase Invoice", "read")

        existing_items = [
            item.pi_detail for item in self.get("items") if item.pi_detail
        ]
        item_to_add = get_pi_items(purchase_invoices)

        if not existing_items:
            self.items = []

        for item in item_to_add:
            if item.pi_detail not in existing_items:
                self.append("items", {**item})

        set_missing_values(self)

def get_pi_items(purchase_invoices):
    pi_item = frappe.qb.DocType("Purchase Invoice Item")

    return (
        frappe.qb.from_(pi_item)
        .select(
            pi_item.item_code,
            pi_item.item_name,
            pi_item.parent.as_("purchase_invoice"),
            pi_item.pending_boe_qty.as_("qty"),
            pi_item.uom,
            pi_item.qty,
            pi_item.amount,
            pi_item.rate,
            pi_item.cost_center,
            pi_item.item_tax_template,
            pi_item.gst_treatment,
            pi_item.taxable_value.as_("assessable_value"),
            pi_item.taxable_value,
            pi_item.project,
            pi_item.name.as_("pi_detail"),
        )
        .where(pi_item.parent.isin(purchase_invoices))
        .where(pi_item.pending_boe_qty > 0)
        .run(as_dict=True)
    )