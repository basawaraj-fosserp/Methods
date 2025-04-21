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



def has_permission_controller(doc, ptype, user):
    if doc.party_type == "Supplier":
        allowed_suppliers = frappe.get_all("User Permission", filters={
            "user": user,
            "allow": "Supplier"
        }, pluck="for_value")

        if doc.party not in allowed_suppliers:
            return False

    return True
