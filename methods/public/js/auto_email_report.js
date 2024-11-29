frappe.ui.form.on("Auto Email Report", {
    refresh:function(frm){
        if (frm.doc.name == "General Ledger"){
            frm.remove_custom_button("Send Now");
            frm.remove_custom_button("Download");
            frm.doc.set_value("enabled", 0)
            frm.set_df_property("enabled", "hidden", 1)
        }
    }
})