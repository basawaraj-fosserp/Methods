import frappe


def onload(self, method):
    if self.docstatus != 1:
        return

    if self.gst_category == "Overseas":
        self.set_onload(
            "bill_of_entry_exists", 0
        )