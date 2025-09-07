import frappe

@frappe.whitelist()
def get_doctype_data(from_date, to_date):
    if not from_date or not to_date:
        frappe.throw("<b>From Date</b> and <b>To Date</b> is required")
    
    user_list = []
    final_data_map = {}
    final_data_map["data"]= {}
    doctype_list = [
        
    ]
    purchase_invoice_data = frappe.db.sql(
        """
            Select 
                COUNT(*) AS number_of_document,
                SUM(base_grand_total) AS value,
                owner
            From `tabPurchase Invoice`

            Where creation BETWEEN %(from_date)s AND %(to_date)s
            Group By Owner
        """,{
                "from_date" : from_date,
                "to_date" : to_date
            }, as_dict=1
    )
    count = 0
    value = 0
    for row in purchase_invoice_data:
        value += row.value
        count += row.number_of_document
        row.update({
            frappe.db.get_value("User", row.owner, "full_name") : row.number_of_document,
            "doctype" : "Purchase Invoice"
        })
        if frappe.db.get_value("User", row.owner, "full_name") not in user_list:
            user_list.append(frappe.db.get_value("User", row.owner, "full_name"))
    
    final_data_map["data"]['Purchase Invoice'] = {}
    for row in purchase_invoice_data:
        final_data_map["data"]["Purchase Invoice"][frappe.db.get_value("User", row.owner, "full_name")] = row
    
    doctype_list.append("Purchase Invoice")
    final_data_map["data"]["Purchase Invoice"]["count"] = count
    final_data_map["data"]["Purchase Invoice"]["value"] = value
    
    sales_invoice_data = frappe.db.sql(
        """
            SELECT 
                COUNT(*) AS number_of_document,
                SUM(base_grand_total) AS value,
                owner
            FROM `tabSales Invoice`
            WHERE creation BETWEEN %(from_date)s AND %(to_date)s
            GROUP BY  owner
        """,
        {
            "from_date": from_date,
            "to_date": to_date
        },
        as_dict=1
    )
    count = 0
    value = 0
    for row in sales_invoice_data:
        value += row.value
        count += row.number_of_document
        row.update({
            frappe.db.get_value("User", row.owner, "full_name") : row.number_of_document,
            "doctype" : "Payment Entry"
        })
        if frappe.db.get_value("User", row.owner, "full_name") not in user_list:
            user_list.append(frappe.db.get_value("User", row.owner, "full_name"))

    final_data_map["data"]['Sales Invoice'] = {}
    for row in sales_invoice_data:
        final_data_map["data"]["Sales Invoice"][frappe.db.get_value("User", row.owner, "full_name")]= row
    
    doctype_list.append("Sales Invoice")
    final_data_map["data"]["Sales Invoice"]["count"] = count
    final_data_map["data"]["Sales Invoice"]["value"] = value
    
    journal_entry_data = frappe.db.sql(
        """
            Select 
                COUNT(*) AS number_of_document,
                SUM(total_debit) AS value,
                owner
            From `tabJournal Entry`

            Where creation BETWEEN %(from_date)s AND %(to_date)s
            Group By Owner
        """,{
                "from_date" : from_date,
                "to_date" : to_date
            }, as_dict=1
    )
    count = 0
    value = 0
    for row in journal_entry_data:
        value += row.value
        count += row.number_of_document
        row.update({
            frappe.db.get_value("User", row.owner, "full_name") : row.number_of_document,
            "doctype" : "Journal Entry"
        })
        if frappe.db.get_value("User", row.owner, "full_name") not in user_list:
            user_list.append(frappe.db.get_value("User", row.owner, "full_name"))
    
    final_data_map["data"]['Journal Entry'] = {}
    for row in journal_entry_data:
        final_data_map["data"]["Journal Entry"][frappe.db.get_value("User", row.owner, "full_name")]= row

    doctype_list.append("Journal Entry")
    final_data_map["data"]["Journal Entry"]["count"] = count
    final_data_map["data"]["Journal Entry"]["value"] = value
    
    
    payment_entry_data = frappe.db.sql(
        """
            SELECT 
                COUNT(*) AS number_of_document,
                SUM(paid_amount) AS value,
                owner,
                payment_type
            FROM `tabPayment Entry`
            WHERE creation BETWEEN %(from_date)s AND %(to_date)s
            GROUP BY payment_type, owner
        """,
        {
            "from_date": from_date,
            "to_date": to_date
        },
        as_dict=1
    )
    count = 0
    value = 0
    for row in payment_entry_data:
        value += row.value
        count += row.number_of_document
        row.update({
            frappe.db.get_value("User", row.owner, "full_name") : row.number_of_document,
            "doctype" : "Payment Entry"
        })
        if frappe.db.get_value("User", row.owner, "full_name") not in user_list:
            user_list.append(frappe.db.get_value("User", row.owner, "full_name"))
    
    final_data_map["data"]['Payment Entry'] = {}
    for row in payment_entry_data:
        final_data_map["data"]["Payment Entry"][frappe.db.get_value("User", row.owner, "full_name")]= row

    doctype_list.append("Payment Entry")
    final_data_map["data"]["Payment Entry"]["count"] = count
    final_data_map["data"]["Payment Entry"]["value"] = value
    
    purchase_order_data = frappe.db.sql(
        """
            Select 
                COUNT(*) AS number_of_document,
                SUM(base_grand_total) AS value,
                owner
            From `tabPurchase Order`

            Where creation BETWEEN %(from_date)s AND %(to_date)s
            Group By Owner
        """,{
                "from_date" : from_date,
                "to_date" : to_date
            }, as_dict=1
    )
    count = 0
    value = 0
    for row in purchase_order_data:
        value += row.value
        count += row.number_of_document
        row.update({
            frappe.db.get_value("User", row.owner, "full_name") : row.number_of_document,
            "doctype" : "Purchase Order"
        })
        if frappe.db.get_value("User", row.owner, "full_name") not in user_list:
            user_list.append(frappe.db.get_value("User", row.owner, "full_name"))
        
    final_data_map["data"]['Purchase Order'] = {}
    for row in purchase_order_data:
        final_data_map["data"]["Purchase Order"][frappe.db.get_value("User", row.owner, "full_name")]= row

    doctype_list.append("Purchase Order")
    final_data_map["data"]["Purchase Order"]["count"] = count
    final_data_map["data"]["Purchase Order"]["value"] = value
    
    sales_order_data = frappe.db.sql(
        """
            Select 
                COUNT(*) AS number_of_document,
                SUM(base_grand_total) AS value,
                owner
            From `tabSales Order`

            Where creation BETWEEN %(from_date)s AND %(to_date)s
            Group By Owner
        """,{
                "from_date" : from_date,
                "to_date" : to_date
            }, as_dict=1
    )
    count = 0
    value = 0
    for row in sales_order_data:
        value += row.value
        count += row.number_of_document
        row.update({
            frappe.db.get_value("User", row.owner, "full_name") : row.number_of_document,
            "doctype" : "Sales Order"
        })
        if frappe.db.get_value("User", row.owner, "full_name") not in user_list:
            user_list.append(frappe.db.get_value("User", row.owner, "full_name"))

    final_data_map["data"]['Sales Order'] = {}
    for row in sales_order_data:
        final_data_map["data"]["Sales Order"][frappe.db.get_value("User", row.owner, "full_name")] = row

    doctype_list.append("Sales Order")
    final_data_map["data"]["Sales Order"]["count"] = count
    final_data_map["data"]["Sales Order"]["value"] = value

    
    purchase_receipt_data = frappe.db.sql(
        """
            Select 
                COUNT(*) AS number_of_document,
                SUM(base_grand_total) AS value,
                owner
            From `tabPurchase Receipt`

            Where creation BETWEEN %(from_date)s AND %(to_date)s
            Group By Owner
        """,{
                "from_date" : from_date,
                "to_date" : to_date
            }, as_dict=1
    )
    count = 0
    value = 0
    for row in purchase_receipt_data:
        value += row.value
        count += row.number_of_document
        row.update({
            frappe.db.get_value("User", row.owner, "full_name") : row.number_of_document,
            "doctype" : "Purchase Receipt"
        })
        if frappe.db.get_value("User", row.owner, "full_name") not in user_list:
            user_list.append(frappe.db.get_value("User", row.owner, "full_name"))
        
    final_data_map["data"]['Purchase Receipt'] = {}
    for row in purchase_receipt_data:
        final_data_map["data"]["Purchase Receipt"][frappe.db.get_value("User", row.owner, "full_name")]= row

    doctype_list.append("Purchase Receipt")
    final_data_map["data"]["Purchase Receipt"]["count"] = count
    final_data_map["data"]["Purchase Receipt"]["value"] = value
    
    landed_cost_voucher = frappe.db.sql(
        """
            Select 
                COUNT(*) AS number_of_document,
                SUM(total_taxes_and_charges) AS value,
                owner
            From `tabLanded Cost Voucher`

            Where creation BETWEEN %(from_date)s AND %(to_date)s
            Group By Owner
        """,{
                "from_date" : from_date,
                "to_date" : to_date
            }, as_dict=1
    )
    count = 0
    value = 0
    for row in landed_cost_voucher:
        value += row.value
        count += row.number_of_document
        row.update({
            frappe.db.get_value("User", row.owner, "full_name") : row.number_of_document,
            "doctype" : "Landed Cost Voucher"
        })
        if frappe.db.get_value("User", row.owner, "full_name") not in user_list:
            user_list.append(frappe.db.get_value("User", row.owner, "full_name"))
    
    final_data_map["data"]['Landed Cost Voucher'] = {}
    for row in landed_cost_voucher:
        final_data_map["data"]["Landed Cost Voucher"][frappe.db.get_value("User", row.owner, "full_name")]= row

    doctype_list.append("Landed Cost Voucher")
    final_data_map["data"]["Landed Cost Voucher"]["count"] = count
    final_data_map["data"]["Landed Cost Voucher"]["value"] = value
    
    bill_of_entry_data = frappe.db.sql(
        """
            Select
                COUNT(*) AS number_of_document,
                SUM(total_amount_payable) AS value,
                owner 
            From `tabBill of Entry`

            Where creation BETWEEN %(from_date)s AND %(to_date)s

            Group By owner
        """,{
                "from_date" : from_date,
                "to_date" : to_date
            }, as_dict=1
    )
    count = 0
    value = 0
    for row in bill_of_entry_data:
        value += row.value
        count += row.number_of_document
        row.update({
            frappe.db.get_value("User", row.owner, "full_name") : row.number_of_document,
            "doctype" : "Bill of Entry"
        })
        if frappe.db.get_value("User", row.owner, "full_name") not in user_list:
            user_list.append(frappe.db.get_value("User", row.owner, "full_name"))

    final_data_map["data"]['Bill of Entry'] = {}
    for row in bill_of_entry_data:
        final_data_map["data"]["Bill of Entry"][frappe.db.get_value("User", row.owner, "full_name")]= row
    
    doctype_list.append("Bill of Entry")
    final_data_map["data"]["Bill of Entry"]["count"] = count
    final_data_map["data"]["Bill of Entry"]["value"] = value
    
    delivery_note_data = frappe.db.sql(
        """
            Select
                COUNT(*) AS number_of_document,
                SUM(base_grand_total) AS value,
                owner 
            From `tabDelivery Note`

            Where creation BETWEEN %(from_date)s AND %(to_date)s

            Group By Owner
        """,{
                "from_date" : from_date,
                "to_date" : to_date
            }, as_dict=1
    )
    count = 0
    value = 0
    for row in delivery_note_data:
        value += row.value
        count += row.number_of_document
        row.update({
            frappe.db.get_value("User", row.owner, "full_name") : row.number_of_document,
            "doctype" : "Delivery Note"
        })
        if frappe.db.get_value("User", row.owner, "full_name") not in user_list:
            user_list.append(frappe.db.get_value("User", row.owner, "full_name"))
    
    final_data_map["data"]['Delivery Note'] = {}
    
    for row in delivery_note_data:
        final_data_map["data"]["Delivery Note"][frappe.db.get_value("User", row.owner, "full_name")] = row
    doctype_list.append("Delivery Note")
    final_data_map["data"]["Delivery Note"]["count"] = count
    final_data_map["data"]["Delivery Note"]["value"] = value
    stock_entry_data = frappe.db.sql(
        """
            Select
                COUNT(*) AS number_of_document,
                SUM(base_grand_total) AS value,
                owner 
            From `tabStock Entry`

            Where creation BETWEEN %(from_date)s AND %(to_date)s

            Group By Owner
        """,{
                "from_date" : from_date,
                "to_date" : to_date
            }, as_dict=1
    )
    count = 0
    value = 0
    for row in stock_entry_data:
        value += row.value
        count += row.number_of_document
        row.update({
            frappe.db.get_value("User", row.owner, "full_name") : row.number_of_document,
            "doctype" : "Stock Entry"
        })
        if frappe.db.get_value("User", row.owner, "full_name") not in user_list:
            user_list.append(frappe.db.get_value("User", row.owner, "full_name"))
        
    final_data_map["data"]['Stock Entry'] = {}

    for row in stock_entry_data:
        final_data_map["data"]["Stock Entry"][frappe.db.get_value("User", row.owner, "full_name")] = row

    final_data_map.update({'user_list' : user_list})
    doctype_list.append("Stock Entry")
    final_data_map["data"]["Stock Entry"]["count"] = count
    final_data_map["data"]["Stock Entry"]["value"] = value
    final_data_map.update({
        "doctype_list" : doctype_list
    })

    return final_data_map

    


    
    

    


    
    

    



    
