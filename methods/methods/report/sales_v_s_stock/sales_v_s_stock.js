// Copyright (c) 2024, viral Patel and contributors
// For license information, please see license.txt

frappe.query_reports["Sales V-S Stock"] = {
	"filters": [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company"),
			reqd: 1,
		},
		{
			fieldname: "from_date",
			reqd: 1,
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
		},
		{
			fieldname: "to_date",
			reqd: 1,
			default: frappe.datetime.get_today(),
			label: __("To Date"),
			fieldtype: "Date",
		},
		{
			fieldname: "item_code",
			label: __("Item"),
			fieldtype: "Link",
			options: "Item",
			get_query: () => {
				return {
					query: "erpnext.controllers.queries.item_query",
				};
			},
		},
		{
			fieldname: "warehouse",
			label: __("Warehouse"),
			fieldtype: "Link",
			options: "Warehouse",
		},

	]
};
