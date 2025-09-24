import frappe

def execute():
    frappe.get_doc({
        "doctype" : "Custom Field",
        "is_system_generated" : 1,
        "dt" : "Buying Settings",
        "fieldname" : "supplier",
        "label" : "Supplier",
        "fieldtype" : "Link",
        "options" : "Supplier",
        "insert_after" : "email_list",
    }).insert()

    frappe.get_doc({
        "doctype" : "Custom Field",
        "is_system_generated" : 1,
        "dt" : "Buying Settings",
        "fieldname" : "exclude_supplier",
        "label" : "Exclude Supplier",
        "fieldtype" : "Table MultiSelect",
        "options" : "Supplier Multiselect",
        "module" : "Methods",
        "insert_after" : "supplier"
    }).insert()

    frappe.get_doc({
        "doctype" : "Custom Field",
        "is_system_generated" : 1,
        "dt" : "Buying Settings",
        "fieldname" : "exclude_supplier_group",
        "label" : "Exclude Supplier Group",
        "fieldtype" : "Table MultiSelect",
        "options" : "Supplier Group Multiselect",
        "module" : "Methods",
        "insert_after" : "exclude_supplier"
    }).insert()