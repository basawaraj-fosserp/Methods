console.log("generated")
frappe.ui.form.on("Purchase Receipt", {
    refresh:function(frm){
        frm.remove_custom_button("Make Stock Entry", "Create");
        frm.add_custom_button(
            __("Make Stock Entry"),
            () => {
                console.log("enter")
                frappe.call({
                    method : "methods.methods.docevents.stock_entry.check_if_lcv",
                    args:{
                        doc:frm.doc
                    },
                    callback:(r)=>{
                        if(r.message){
                            frappe.model.open_mapped_doc({
                                method: "erpnext.stock.doctype.purchase_receipt.purchase_receipt.make_stock_entry",
                                frm: cur_frm,
                            });
                        }else{
                            frappe.throw(r.message)
                        }
                    }
                })
            },
            __("Create")
        );
        
    }
})