
frappe.ui.form.on("Bill of Entry", {
    custom_exchange_rate : (frm)=>{
        frm.trigger("calculate_assessable_value")        
    },
    calculate_assessable_value : (frm) =>{
        let freight = frm.doc.freight
        let custom_exchange_rate = frm.doc.custom_exchange_rate
        let insurance = frm.doc.insurance/100

        frm.doc.items.forEach(e => {
            assessable_value = (e.qty * e.rate * custom_exchange_rate) + freight + (e.qty * e.rate * custom_exchange_rate * insurance)
            frappe.model.set_value(e.doctype, e.name, "assessable_value", assessable_value)
            frappe.model.get_value("Item", e.item_code, "duty_and_charges", r=>{
                let custom_duty  = assessable_value * r.duty_and_charges /100
                frappe.model.set_value(e.doctype, e.name, "customs_duty",  custom_duty)
            })
            frm.refresh_field("items")
        });
    },
    freight : (frm) =>{
        frm.trigger("calculate_assessable_value")
    },
    insurance : (frm) =>{
        frm.trigger("calculate_assessable_value")
    },
    qty : (frm) =>{
        frm.trigger("calculate_assessable_value")
    }
})


frappe.ui.form.on("Bill of Entry Item", {
    qty : (frm) =>{
        console.log("hh")
        frm.trigger("calculate_assessable_value")
    },
    calculate_assessable_value : (frm) =>{
        let freight = frm.doc.freight
        let custom_exchange_rate = frm.doc.custom_exchange_rate
        let insurance = frm.doc.insurance/100

        frm.doc.items.forEach(e => {
            assessable_value = (e.qty * e.rate * custom_exchange_rate) + freight + (e.qty * e.rate * custom_exchange_rate * insurance)
            frappe.model.set_value(e.doctype, e.name, "assessable_value", assessable_value)
            frappe.model.get_value("Item", e.item_code, "duty_and_charges", r=>{
                let custom_duty  = assessable_value * r.duty_and_charges /100
                frappe.model.set_value(e.doctype, e.name, "customs_duty", assessable_value + custom_duty)
            })
            frm.refresh_field("items")
        });
    },
})
