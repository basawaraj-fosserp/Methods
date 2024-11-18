import frappe
from frappe.utils.pdf import get_pdf
from erpnext.accounts.report.general_ledger.general_ledger import get_columns, execute
import json
from frappe.utils import flt, getdate, get_datetime

def generate_pdf_from_report(report_name, filters=None, file_name="Report.pdf", email_id=None):
    # Get the report data in HTML format
    columns = [
        "Posting Date",
        "Account", 
        "Debit (INR)",
        "Credit (INR)",
        "Balance (INR)",
        "Voucher Type",
        "Voucher No",
        "Against Account",
    ]
    pdf_columns = []
    for row in get_columns(filters):
        for d in columns:
            if row.get('label') == d:
                pdf_columns.append(row)
    data = list(execute(filters))
    # Generate HTML from report data
    html = frappe.render_template("methods/public/js/general_ledger.html", {
        "title": "General Ledger",
        "filters": filters,
        "report_name": report_name,
        "columns": pdf_columns,
        "data": list(execute(filters)),
        "head_columns" : columns
    })
    
    pdf = get_pdf(html, {"orientation": "Landscape"})
    
    file = frappe.get_doc({
        "doctype": "File",
        "file_name": file_name,
        "content": pdf,
        "is_private": 1
    })
    file.insert(ignore_permissions=True)

    message = f"""Dear { filters.party_name } <br><br>

                Greetings from Methods Automotive!<br><br>

                The balance as per our books of account as on { filters.to_date } in your ledger is  { round(data[-1][-1].balance, 2) }. Herewith Attached copy of ledger for reference
                In the event of disagreement, please record the balance/(s) shown by your records and provide copy of relevant ledgers.<br><br>

                You can e-mail the information to accounts.team@methods.co.in<br><br>


                If no response is received within 7 days, the balance stated in the mail will be considered correct.
                Thank you for your business - we appreciate it very much.<br><br>

                Awaiting your revert.<br><br>

                Sincerely,<br><br>

                Methods Automotive Private Limited"""
    
    frappe.sendmail(
        recipients=["vinayak.hegde@methods.co.in"],
        subject="Ledger",
        message=message,
        attachments=[{
            "fname": 'report.pdf',
            "fcontent": pdf
        }]
    )

   
    

def send_customer_ledger():
    filters = get_auto_email_report_details()
    filters = filters.update({'party_type' : 'Customer'})
    customer_data = frappe.db.sql("""
                    Select cu.name , co.email_id as first_email 
                    From `tabCustomer` as cu
                    Left Join `tabDynamic Link` as dl ON dl.parenttype = 'Contact' and dl.link_name = cu.name and dl.link_doctype = 'Customer'
                    Left Join `tabContact` as co on dl.parent = co.name
                    Where cu.disabled = 0
            """, as_dict=1)
    
    for row in customer_data:
        if row.first_email:
            filters = filters.update({
                        'party' : [row.name],
                        'party_name' : row.name
                    })
            
            generate_pdf_from_report("General Ledger", filters = frappe._dict(filters),
                file_name="Report.pdf", email_id=row.first_email
            )
            frappe.db.commit()


def get_auto_email_report_details():
    doc = frappe.get_doc("Auto Email Report","General Ledger")
    doc.prepare_dynamic_filters()
    return doc.filters


#run a function on 31 of the qualter end
def send_on_31_of_the_month():
    if getdate().month in [3, 12]:
        send_customer_ledger()

#run a function on 30 of the qualter end
def send_on_30_of_the_month():
    if getdate().month in [6, 9]:
        send_customer_ledger()