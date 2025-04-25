import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def setup_custom_fields():
	custom_fields = {
		"Bill of Entry Item": [
			dict(
				fieldname="amount",
				label="Amount",
				fieldtype="Currency"
			),
			dict(
				fieldname="rate",
				label="rate",
				fieldtype="Currency"
			)
		],
		"Item": [
			dict(
				fieldname="duty_and_charges",
				label="Duty and Charges",
				fieldtype="Percent",
                insert_after="taxes"
			)
		],
		"Bill of Entry": [
            dict(
				fieldname="col_break_09909",
				label="",
				fieldtype="Column Break",
                insert_after="get_items_from_purchase_invoice"
			),
			dict(
				fieldname="custom_exchange_rate",
				label="Custom Exchange Rate",
				fieldtype="Float",
                insert_after="col_break_09909"
			),
            dict(
				fieldname="col_break_09908",
				label="",
				fieldtype="Column Break",
                insert_after="custom_exchange_rate"
			),
            dict(
				fieldname="freight",
				label="Freight",
				fieldtype="Currency",
                insert_after="col_break_09908"
			),
            dict(
				fieldname="col_break_09907",
				label="",
				fieldtype="Column Break",
                insert_after="freight"
			),
            dict(
				fieldname="insurance",
				label="Insurance",
				fieldtype="Percent",
                insert_after="col_break_09907"
			),
             dict(
				fieldname="sec_break_09907",
				label="",
				fieldtype="Section Break",
                insert_after="insurance"
			)
		],
	}

	create_custom_fields(custom_fields)