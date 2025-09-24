import frappe

def execute():
    frappe.get_doc({
        "doctype" : "Custom Field",
        "is_system_generated" : 1,
        "dt" : "Buying Settings",
        "fieldname" : "send_email_tab",
        "label" : "Send Emails",
        "fieldtype" : "Tab Break",
        "insert_after" : "fixed_email"
    }).insert()

    frappe.get_doc({
        "doctype" : "Custom Field",
        "is_system_generated" : 1,
        "dt" : "Buying Settings",
        "fieldname" : "email_list",
        "label" : "Email list to sent Vendo Order Report",
        "fieldtype" : "Small Text",
        "description" : "Add every email in New Line",
        "module" : "Methods",
        "insert_after" : "send_email_tab"
    }).insert()

