app_name = "methods"
app_title = "Methods"
app_publisher = "viral Patel"
app_description = "Test"
app_email = "viral@fosserp.com"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/methods/css/methods.css"
# app_include_js = ["/assets/methods/js/utils/barcode_scanner.js","methods.bundle.js"]

# include js, css files in header of web template
# web_include_css = "/assets/methods/css/methods.css"
# web_include_js = "/assets/methods/js/methods.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "methods/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Stock Entry" : "public/js/stock_entry.js",
    "Sales Order" : "public/js/sales_order.js",
    "Auto Email Report" : "public/js/auto_email_report.js",
    "Delivery Note" : "public/js/delivery_note.js",
    "Purchase Receipt" : "public/js/purchase_receipt.js"
	}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "methods/public/icons.svg"
scheduler_events = {
    "cron": {
		"0 0 30 * *": [
			"methods.methods.auto_email_report.send_on_30_of_the_month"
		],
        "0 0 31 * *": [
			"methods.methods.auto_email_report.send_on_31_of_the_month"
		],
	},
	"hourly": [
		"methods.methods.api.delete_communications"
	]
	
}
# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "methods.utils.jinja_methods",
# 	"filters": "methods.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "methods.install.before_install"
# after_install = "methods.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "methods.uninstall.before_uninstall"
# after_uninstall = "methods.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "methods.utils.before_app_install"
# after_app_install = "methods.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "methods.utils.before_app_uninstall"
# after_app_uninstall = "methods.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "methods.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

permission_query_conditions = {
	"Payment Entry": "methods.methods.api.get_permission_query_conditions",
}
#
has_permission = {
	"Payment Entry": "methods.methods.api.has_permission",
	"Supplier" : "methods.methods.api.has_permission_supplier"
}

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Amazon SP API Settings": "methods.methods.amazon_sp_api_settings.MethodAmazonSPAPISetting",
    "Bill of Entry" : "methods.methods.docevents.bill_of_entry.CustomBillofEntry"
}

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }
doc_events = {
    "Purchase Invoice": {
        "onload" : "methods.methods.docevents.purchase_invoice.onload"
	},
    "Bill of Entry" : {
        "on_submit" : "methods.methods.docevents.bill_of_entry.check_quantity_overflow"
	},
    "Stock Entry" : {
        "validate" : "methods.methods.docevents.stock_entry.check_pr_vs_se_qty"
	}
}

# Scheduled Tasks
# ---------------



# Testing
# -------

# from ecommerce_integrations.amazon.doctype.amazon_sp_api_settings import amazon_repository 
# from methods.methods.amazon_repository import get_orders as method_get_orders
# amazon_repository.get_orders = method_get_orders

# before_tests = "methods.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
	"ecommerce_integrations.amazon.doctype.amazon_sp_api_settings.amazon_sp_api_settings.AmazonSPAPISettings.get_order_details": "methods.methods.amazon_sp_api_settings.MethodAmazonSPAPISetting.get_order_details",
    "erpnext.stock.doctype.purchase_receipt.purchase_receipt.make_stock_entry" : "methods.methods.docevents.stock_entry.make_stock_entry"
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "methods.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["methods.utils.before_request"]
# after_request = ["methods.utils.after_request"]

# Job Events
# ----------
# before_job = ["methods.utils.before_job"]
# after_job = ["methods.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"methods.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

