console.log("llll")
frappe.ui.form.on("Stock Entry", {
    stock_entry_type : (frm)=>{
        console.log("jjjj")
    },
    refresh:(frm)=>{
        if (frm.doc.stock_entry_type == "Material Transfer"){
            frm.doc.items.forEach(e => {
                frappe.model.set_value(e.doctype, e.name, "custom_is_material_transfer", 1)
            });
        }
    }
})


frappe.ui.form.on('Stock Entry Detail', {
    item_code:(frm, cdt, cdn)=>{
        let d = locals[cdt][cdn]
        d.set_df_property("additional_cost" , "hidden", 1)
    }
})