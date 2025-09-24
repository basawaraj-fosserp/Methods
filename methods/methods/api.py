import frappe
from frappe.utils import nowdate, add_days, get_first_day, fmt_money, getdate, formatdate
from frappe import _


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

def has_permission_supplier(doc, user):
    if frappe.db.exists("User Permission", { "allow" : user, "for_value": "Supplier" }):
        allowed_suppliers =  frappe.db.get_all("User Permission", {
            "allow" : "Suppluer",
            "user" : user
         }, pluck="for_value")
        
        if doc.name in allowed_suppliers:
            return True
        else:
            return False
    else:
        return True



# update account settings clossing date 
def set_clossing_date():
    date = frappe.db.get_single_value("Accounts Settings", "acc_frozen_upto")
    date = frappe.utils.getdate(date)
    next_date = frappe.utils.add_days(str(date), 1)
    print(next_date)
    frappe.db.set_value("Accounts Settings", "Accounts Settings", "acc_frozen_upto", next_date)

from methods.methods.report.vendor_orders_report.vendor_orders_report import execute as execure_vendor_report

@frappe.whitelist()
def send_order_details():
    buying_doc = frappe.get_doc("Buying Settings", "Buying Settings")
    supplier = buying_doc.supplier
    exclude_supplier = []
    exclude_supplier_group = []

    for row in buying_doc.exclude_supplier:
        exclude_supplier.append(row.supplier)
    for row in buying_doc.exclude_supplier_group:
        exclude_supplier_group.append(row.supplier_group)

    filters_dict = {
        'supplier' : supplier,
        'exclude_supplier' : exclude_supplier,
        'exclude_supplier_group' : exclude_supplier_group 
    }
    columns, data = execure_vendor_report(filters=filters_dict)
    if not data:
        return
    yesterday = add_days(nowdate(), -1)
    total_value = sum([
        row.value_yesterday for row in data
    ])
    total_order = sum ([
        row.orders_yesterday for row in data
    ])
   
    html = '''
            <style>
                body { margin:0; padding:0; background:#f4f6f8; font-family: Arial, Helvetica, sans-serif; -webkit-text-size-adjust:100%; }
                .email-wrapper { width:100%; background:#f4f6f8; padding:24px 12px; box-sizing:border-box; }
                .email-container { width:100%; margin:0 auto; background:#ffffff; border-radius:8px; overflow:hidden; box-shadow:0 2px 6px rgba(16,24,40,0.08); }
                .header { padding:20px 28px; border-bottom:1px solid #eef1f5; background: linear-gradient(90deg, #0f749b 0%, #05a1a6 100%); color:#fff; }
                .header h1 { margin:0; font-size:20px; font-weight:600; }
                .preheader { display:none !important; visibility:hidden; opacity:0; color:transparent; height:0; width:0; }
                .content { padding:20px 28px; color:#102a43; }
                .intro { margin:0 0 16px 0; line-height:1.45; color:#334e68; }
                .summary { display:flex; gap:12px; flex-wrap:wrap; margin-bottom:18px; }
                .card { background:#f8fafc; padding:12px; border-radius:6px; min-width:150px; box-sizing:border-box; border:1px solid #e6eef6; }
                .card .label { font-size:12px; color:#627d98; margin-bottom:6px; }
                .card .value { font-size:16px; font-weight:600; color:#102a43; }

                table { width:100%; border-collapse:collapse; margin-top:8px; }
                th, td { padding:10px 12px; text-align:left; border-bottom:1px solid #eef1f5; font-size:14px; }
                th { background:#fbfdff; color:#0b2545; font-weight:700; }
                tfoot td { border-top:2px solid #e6eef6; font-weight:600; }

                .footer { padding:16px 28px; font-size:12px; color:#6b7c93; background:#fbfdff; border-top:1px solid #eef1f5; }
                .muted { color:#7b8794; font-size:13px; }

                @media only screen and (max-width:480px){
                .header h1 { font-size:18px; }
                .card { min-width:48%; }
                th, td { padding:10px 8px; font-size:13px; }
                }
            </style>
            '''
    html += f'''
            <div class="email-wrapper">
                <div class="email-container" role="article" aria-roledescription="email">
                <div class="header">
                    <h1>Supplier Wise Purchase Orders Summary for {getdate(yesterday).strftime("%B")}</h1>
                </div>

                <div class="content">
                    <p class="intro">Hello,</p>
                    <p class="intro">Below is the summary of suppliers who had orders yesterday.</p>

                    <!-- Summary cards (optional totals) -->
                    <div class="summary" aria-hidden="true">
                    <div class="card">
                        <div class="label">Date</div>
                        <div class="value">{formatdate(yesterday)}</div>
                    </div>
                    <div class="card">
                        <div class="label">Total Orders On {formatdate(yesterday)}</div>
                        <div class="value">{total_order}</div>
                    </div>
                    <div class="card">
                        <div class="label">Total value On {formatdate(yesterday)}</div>
                        <div class="value">{fmt_money(int(total_value)).replace(".00",'')}</div>
                    </div>
                    </div>

                    <!-- Table -->
                    <table role="table" cellpadding="0" cellspacing="0">
                    <thead>
                        <tr>
                        <th>Supplier</th>
                        <th style="text-align:center">Orders on<br>{formatdate(yesterday)}</th>
                        <th style="text-align:center">Total Value of Orders<br>{formatdate(yesterday)}</th>
                        <th style="text-align:center">Total Orders<br><b>{getdate(yesterday).strftime("%B")}</b></th>
                        <th style="text-align:center">Total Value<br><b>{getdate(yesterday).strftime("%B")}</th>
                        </tr>
                    </thead>
                    <tbody>'''
    for row in data:
        html += f'''    
                            <!-- Row(s) -->
                            <tr>
                                <td>{row.supplier}</td>
                                <td style="text-align:center">{row.orders_yesterday}</td>
                                <td style="text-align:center">{fmt_money(int(row.value_yesterday), currency="INR").replace(".00",'')}</td>
                                <td style="text-align:center">{row.orders_mtd}</td>
                                <td style="text-align:center">{fmt_money(int(row.value_mtd), currency="INR").replace(".00",'')}</td>
                            </tr>
            '''
    html += f'''
                    </tbody>
                    </table>

                </div>
                </div>
            </div>
    '''

    frappe.sendmail(
			recipients=["viral.kansodiya77@gmail.com"],
			message=html,
			subject=_(f"Order Summery For {yesterday}"),
		)