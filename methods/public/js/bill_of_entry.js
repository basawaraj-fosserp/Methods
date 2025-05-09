
frappe.ui.form.on("Bill of Entry", {
    custom_exchange_rate : (frm)=>{
        calculate_assessable_value(frm)        
    },
    freight : (frm) =>{
        calculate_assessable_value(frm)
    },
    insurance : (frm) =>{
        calculate_assessable_value(frm)
    },
    qty : (frm) =>{
        calculate_assessable_value(frm)
    }
})


frappe.ui.form.on("Bill of Entry Item", {
    qty : (frm) =>{
        calculate_assessable_value(frm)
    },
    calculate_assessable_value : (frm) =>{
        
    },
})

function calculate_assessable_value(frm){
    let freight = frm.doc.freight || 0
    let custom_exchange_rate = frm.doc.custom_exchange_rate || 0
    let insurance = 0

    if(flt(frm.doc.insurance)){
        insurance = frm.doc.insurance/100 
    }

    let total_assessable_value = 0

    frm.doc.items.forEach(e => {
        total_assessable_value += e.assessable_value
    })
    let assessable_value = 0;
    frm.doc.items.forEach(e => {
        percentage_of_amount = e.assessable_value * 100 / total_assessable_value
        devided_freight = percentage_of_amount * freight / 100 || 0
        assessable_value = (e.qty * e.rate * custom_exchange_rate) + devided_freight + (e.qty * e.rate * custom_exchange_rate * insurance)
        console.log(assessable_value)
        frappe.model.set_value(e.doctype, e.name, "assessable_value", assessable_value)

        frappe.model.get_value("Item", e.item_code, "duty_and_charges", r=>{
            if(r.duty_and_charges){
                console.log(e.duty_and_charges)
                console.log(assessable_value)
                let custom_duty  = assessable_value * r.duty_and_charges /100
                frappe.model.set_value(e.doctype, e.name, "customs_duty", custom_duty)
            }
        })
        frm.refresh_field("items")
    });
}
