import frappe
from datetime import datetime
import ast
from frappe.utils import getdate, get_url
from frappe.model.naming import make_autoname


@frappe.whitelist()
def get_sales_invoice(from_date, to_date):
    condition = ''
    if from_date:
        condition += f" and si.posting_date >= '{from_date}'"
    if to_date:
        condition += f" and si.posting_date <= '{to_date}'"

    data = frappe.db.sql(f"""
            Select si.name, 
            si.posting_date, 
            si.customer, 
            si.customer_name,
            si.irn, 
            si.schedule_no, 
            si.po_no, 
            si.company_gstin
            From `tabSales Invoice` as si
            Where si.docstatus=1 and si.spool_file_created = 1 and si.customer_name like '%Maruti Suzuki%' {condition} 
    """, as_dict=1 )
    
    return data


import frappe
import ast
from frappe.utils import get_files_path

@frappe.whitelist()
def create_spool_file(invoices):
    actual_list = ast.literal_eval(invoices)
    if not actual_list:
        frappe.throw("Invoice Not Selected")
    
    conditions = ''
    if actual_list:
        conditions = " and si.name in {} ".format(
                    "(" + ", ".join([f'"{l}"' for l in actual_list]) + ")")
        
    data = frappe.db.sql(f"""
                SELECT si.name, si.schedule_no, si.posting_date, si.company_gstin, si.irn,
                sii.item_code, sii.qty, item.per_bin_qty, item.batch_no, sii.gst_hsn_code,
                sii.item_tax_template, sii.igst_rate, sii.igst_amount, sii.cgst_rate, sii.cgst_amount,
                sii.sgst_rate, sii.sgst_amount
                FROM `tabSales Invoice` AS si
                LEFT JOIN `tabSales Invoice Item` AS sii ON sii.parent = si.name
                LEFT JOIN `tabItem` AS item ON sii.item_code = item.name
                WHERE si.docstatus = 1 {conditions}
            """, as_dict=1)
    
    # Define the path where you want to save the file
    file_path = get_files_path('spool.txt')  # Saves in /sites/[site_name]/public/files/spool.txt
    
    with open(file_path, 'w') as f:
        for row in data:
            gst = 0
            if row.igst_amount:
                gst += row.igst_amount
            if row.cgst_amount:
                gst += row.cgst_amount
            if row.sgst_amount:
                gst += row.sgst_amount
            f.write("{0}{1}{2}{1}{2}                        {3}   {4}        {5}          {6}                                                   {7}\n".format(
                "M061", row.name, row.posting_date.strftime('%d-%b-%Y').upper(), row.schedule_no, row.item_code, row.po_no, row.per_bin_qty, row.batch_no))
            f.write("{0}{1}{2}                               {2}                         NA             {3}\n".format(row.company_gstin,row.gst_hsn_code ,gst,row.irn))
            frappe.db.set_value("Sales Invoice", row.name, "spool_file_created", 1)
    return file_path


#https://methods.fosscrm.com
