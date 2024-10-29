import frappe
from frappe import _
from ecommerce_integrations.amazon.doctype.amazon_sp_api_settings.amazon_sp_api_settings import AmazonSPAPISettings

class MethodAmazonSPAPISetting(AmazonSPAPISettings):
    @frappe.whitelist()
    def get_order_details(self):
        frappe.throw(str("helo"))
        from methods.methods.amazon_repository import get_orders

        if self.is_active == 1:
            job_name = f"Get Amazon Orders - {self.name}"

            if frappe.db.get_all("RQ Job", {"job_name": job_name, "status": ["in", ["queued", "started"]]}):
                return frappe.msgprint(_("The order details are currently being fetched in the background."))

            frappe.enqueue(
                job_name=job_name,
                method=get_orders,
                amz_setting_name=self.name,
                created_after=self.after_date,
                timeout=4000,
                now=frappe.flags.in_test,
            )

            frappe.msgprint(_("Order details will be fetched in the background."))
        else:
            frappe.msgprint(
                _("Please enable the Amazon SP API Settings {0}.").format(frappe.bold(self.name))
            )