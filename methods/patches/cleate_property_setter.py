import frappe

def execute():
    frappe.get_doc({
            "is_system_generated": 1,
            "doctype_or_field": "DocField",
            "doc_type": "Payment Entry",
            "field_name": "clearance_date",
            "property": "allow_on_submit",
            "property_type": "Check",
            "value": "1",
            "doctype": "Property Setter",
        }).insert()