frappe.pages['spool-file-creation-'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Spool File Creation Tool',
		single_column: true
	});
	frappe.SpoolDoc.init(wrapper, page)
}


frappe.SpoolDoc = {
	init:function(wrapper, page){
		this.wrapper = $(wrapper).find('.layout-main-section');
		this.wrapper.append(`
			<div class="invoice_data"></div>
			`)
		this.page = wrapper.page;
		this.setup_fields(wrapper, page)
		this.setup_data(wrapper, page)
		$(".refresh").click(function() {
			location.reload();
		});
		
		
	
	},
	setup_fields:function(wrapper, page){
		this.from_date_field = page.add_field({
			fieldname: 'from_date',
			label: __('From Date'),
			fieldtype:'Date',
			default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			change: function () {
				frappe.SpoolDoc.setup_data(wrapper, page)
			}
		})
		this.to_date_field = page.add_field({
			fieldname: 'to_date',
			label: __('To Date'),
			fieldtype:'Date',
			default: frappe.datetime.get_today(),
			change: function () {
				frappe.SpoolDoc.setup_data(wrapper, page)
			}
		})
	},
	setup_data:function(wrapper, page){
		frappe.call({
			 method:"methods.methods.page.spool_file_creation_.get_sales_invoice",
			 args:{
				'from_date': this.from_date_field.get_value(),
				'to_date': this.from_date_field.get_value(),
			 },
			 callback:function(r){
				let data = r.message
				$(wrapper).find(".invoice_data").empty();
				frappe.SpoolDoc.update_header(wrapper, page)
				frappe.SpoolDoc.update_invoice_row(wrapper, page, data)
				// Attach a change event handler to the 'selectall' checkbox
				$('.selectall').on('change', function() {
					// Determine if the 'selectall' checkbox is checked
					var isChecked = $(this).is(':checked');
					// Select all checkboxes with the ID 'method_invoice' and set their state
					$('input[id="method_invoice"]').prop('checked', isChecked);
				});
				$('.create').on('click', function(){
					frappe.SpoolDoc.create_file()
				})
			 }
		})
	},
	update_header:function(wrapper, page){
		this.wrapper = $(wrapper).find('.invoice_data');
		this.wrapper.append(`
			<style>
				.onbottom {
					border-bottom:2px solid black;
				}
				.invoice_data{
					padding:10px;
				}	
				p{
					margin-bottom:0px !important;
				}
				td{
					padding:5px;
				}
				.row_bottom {
					border-bottom : solid ;
				}
			</style>
			
			`)
	},
	update_invoice_row:function(wrapper, page, data){
		this.wrapper = $(wrapper).find('.invoice_data');
		let invoice_html = `<table width="100%">
								<tr>
									<td class="onbottom"><input type="checkbox" class="selectall"></td>
									<td class="onbottom"><p style="font-size:16px;"><b>Invoice No</b></p></td>
									<td class="onbottom"><p style="font-size:16px;"><b>Invoice Date</b></p></td>
									<td class="onbottom"><p style="font-size:16px;"><b>Customer Name</b></p></td>
								</tr>`
		data.forEach(r => {
			invoice_html += `<tr>
								<td class="row_bottom"><input type="checkbox" class=${r.name} id="method_invoice"></td>
								<td class="row_bottom">
									<p><a href='sales-invoice/${r.name}'>${r.name}</a></p>
								</td>
								<td class="row_bottom">
									<p>${r.posting_date}</p>
								</td>
								<td class="row_bottom">
									<p><a href='customer/${r.customer}'>${r.customer_name}</a></p>
								</td>
							</tr>`
			});
		invoice_html += `</table>
						<div width="100%" style="height:10px;"></div>	
					`
							
		if(data.length){
			invoice_html += `<div class="row">
								<div class="col-2"><button class="btn btn-primary create">Create</button></div>
								<div class="col-2"><button class="btn btn-primary refresh">Refresh</button></div>
							</div>`
			}			
		this.wrapper.append(invoice_html)
		
		
	},
	create_file:function(){
		let invoices = []
		$('input[id="method_invoice"]').each(function() {
			if ($(this).is(':checked')) {  // Check if the checkbox is checked
				var classNames = $(this).attr('class');
				invoices.push(classNames);  // Push the class names to the invoices array
			}
		});		
		frappe.call({
			method:"methods.methods.page.spool_file_creation_.create_spool_file",
			args:{
				"invoices" : invoices 
			},
			callback:(r)=>{
				$(".create").css("display", "none");
				const fileUrl = '/files/spool.txt';  // Relative URL from your public folder
				const a = document.createElement('a');
				a.href = fileUrl;
				a.download = 'spool.txt';  // Specify the file name for download
				document.body.appendChild(a);
				a.click();
				document.body.removeChild(a);
				frappe.SpoolDoc.setup_data(wrapper, page)
			}
		})
	}
}