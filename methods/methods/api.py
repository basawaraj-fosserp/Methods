import frappe
from frappe.utils import nowdate, add_days

def delete_communications():

    # Get today's date
    current_date = nowdate()

    # Calculate the date 30 days ago
    date_30_days_ago = add_days(current_date, -30)

    print(date_30_days_ago)

    data = frappe.db.sql(f""" Select name From `tabCommunication` Where creation < '{date_30_days_ago}' Limit 3000 """, as_dict=1)
    print(data)
    for row in data:
        frappe.db.delete("Communication", row.get("name"))



import frappe

def get_permission_query_conditions(user):
    if not user or frappe.session.user == "Administrator":
        return ""

    # Get allowed suppliers for this user
    allowed_suppliers = frappe.get_all("User Permission", filters={
        "user": user,
        "allow": "Supplier"
    }, pluck="for_value")

    if not allowed_suppliers:
        return ""  # Don't show anything if no access

    suppliers_str = "', '".join(allowed_suppliers)
    return f"""(
        party_type = 'Supplier' AND party IN ('{suppliers_str}')
    )"""


def has_permission(doc, user):
    return True
    if frappe.db.exists("User Permission", { "allow" : user, "for_value": "Supplier" }):
        allowed_suppliers =  frappe.db.get_all("User Permission", {
            "allow" : "Suppluer",
            "user" : user
         }, pluck="for_value")
        
        if doc.party in allowed_suppliers:
            return True
        else:
            return False
    else:
        return True
