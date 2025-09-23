// Copyright (c) 2025, viral Patel and contributors
// For license information, please see license.txt

frappe.query_reports["Vendor Orders Report"] = {
	"filters": [
		{
			"fieldname": "supplier",
			"label": "Supplier",
			"fieldtype": "Link",
			"options": "Supplier"
		},
		{
			"fieldname": "exclude_supplier",
			"label": "Exclude Supplier",
			"fieldtype": "MultiSelectList",
			"options": "Supplier",
			get_data: function (txt) {
				if (!frappe.query_report.filters) return;

				return frappe.db.get_link_options("Supplier", txt);
			},
		},
		{
			"fieldname": "exclude_supplier_group",
			"label": "Exclude Supplier Group",
			"fieldtype": "MultiSelectList",
			"options": "Supplier Group",
			get_data: function (txt) {
				if (!frappe.query_report.filters) return;

				return frappe.db.get_link_options("Supplier Group", txt);
			},
		}
	]
};
