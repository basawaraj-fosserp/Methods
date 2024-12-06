frappe.ui.form.on("Delivery Note", {
    refresh:function(frm){
        console.log("shhhh")
    },
    items_add:function(frm){
        console.log("hello")
    }
})
// frappe.ready(() => {
//     console.log("Helo")
//     erpnext.utils.BarcodeScanner = methods.utils.CustomBarcodeScanner;
// });
