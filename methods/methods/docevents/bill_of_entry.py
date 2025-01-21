import frappe

def check_quantity_overflow(self, method):
    for row in self.items:
        if row.pi_detail:
            pi_data = frappe.db.sql("Select sum(qty) as total_qty From `tabBill of Entry Item` where docstatus = 1 and pi_detail = '{0}' and parent != '{1}' ".format(row.pi_detail, self.name), as_dict=True)
            total_qty = frappe.db.get_value("Purchase Invoice Item", row.pi_detail, 'qty')
            if pi_data[0].get("total_qty"):
                if pi_data[0].get("total_qty") + row.qty > total_qty:
                    frappe.throw(f"Row #{row.idx} : Bill of Entry already created for {pi_data[0].get('total_qty')} qty. Not allowed to create Bill of Entry greater then purchase invoice qty {total_qty}.")