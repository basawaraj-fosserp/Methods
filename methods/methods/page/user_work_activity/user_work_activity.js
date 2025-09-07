frappe.pages['user-work-activity'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'User Work Activity',
		single_column: true
	});
	frappe.UserActivity.init(wrapper, page)

}


frappe.UserActivity = {
	init:(wrapper, page)=>{
		frappe.UserActivity.setupfield(wrapper, page)
		let parent = $(".page-content")
		parent.append(`<div class="user-activity"></div>`)
		frappe.UserActivity.fetch_data(wrapper, page)
	},
	fetch_data:(wrapper, page)=>{
		let from_date = this.from_date_field.get_value()
		let to_date = this.to_date_field.get_value()
		frappe.call({
			method : "methods.methods.page.user_work_activity.get_doctype_data",
			args:{
				from_date : from_date,
				to_date : to_date
			},
			callback:(r)=>{

				let child_parent = $(".page-content").find('.user-activity')
				child_parent.empty()
				let html = `<style>th{background-color: #aababeff;}</style><div style="overflow-x: auto; width: 100%;">
								<table class="table" border="1" 
									style="min-width: 800px; border-collapse: collapse; table-layout: fixed; width: 100%;">
									<tr>
										<th style="width: 200px;">Accounting Voucher</th> 
										<th style="width: 80px; text-align:center;">Count</th> 
										<th style="width: 140px; text-align:center;">Value</th>
							`
				
							r.message.user_list.forEach(e=>{
								html+=`<th style="width: 160px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;"><p align="center" >${e}</p></th>`
							})
				html += `</tr>`

				r.message.doctype_list.forEach(e=>{
					let value = Math.round(r.message.data[e].value)
					let formatted = new Intl.NumberFormat('en-IN', {
						style: 'currency',
						currency: 'INR',
						maximumFractionDigits: 0
					}).format(value);
					html += `<tr>
								<td width="40px;">${e}</td>
								<td>
									<p style="margin: 0; color: #333; font-weight: bold;" align="center">${r.message.data[e].count}</p>
								</td>
								<td width="180px"><p style="margin: 0; color: #333; font-weight: bold;" align="center">${formatted}</p></td>		
					`
					r.message.user_list.forEach(user => {
						if (r.message.data[e][user]) {
							html += `<td style="background-color: #82d4f5ff;">
										<div class="user-record"
											style="
												display: flex; 
												align-items: center; 
												justify-content: center; 
												height: 100%; 
												padding: 20 10px; 
												background-color: #f0f0f0; 
												border: 1px solid #ccc; 
												border-radius: 8px; 
											"
											data-fromdate="${from_date}" 
											data-todate="${to_date}" 
											data-user="${r.message.data[e][user].owner}" 
											data-doctype ="${e}"
										>
											<p style="margin: 0; color: #333; font-weight: bold;">${r.message.data[e][user][user]}</p>
										</div>
									</td>`;
						} else {
							html += `<td></td>`;
						}
					});
					html += `</tr>`
				})
				html+=` </table></div>`
				// append new HTML
				child_parent.append(html);
				const userRecords = document.querySelectorAll(".user-record");

				userRecords.forEach(record => {
					record.addEventListener("click", function() {
						// Access data attributes using the .dataset property
						const fromDate = this.dataset.fromdate;
						const toDate = this.dataset.todate;
						const user = this.dataset.user;
						const doctype = this.dataset.doctype;
						const url = `/app/${frappe.router.slug(doctype)}?creation=%5B%22Between%22%2C%5B%22${encodeURIComponent(fromDate)}%22%2C%22${encodeURIComponent(toDate)}%22%5D%5D&owner=${encodeURIComponent(user)}`;
        
        				window.open(frappe.urllib.get_full_url(url));
					});
				});

			}
		})
	},
	setupfield:(wrapper, page)=>{

		this.from_date_field = page.add_field({
			label: 'From Date',
			fieldtype: 'Date',
			fieldname: 'from_date',
			default: frappe.datetime.add_days(frappe.datetime.get_today(), -7), // last 7 days
			onchange() {
				frappe.UserActivity.fetch_data(wrapper, page)
			}
		});

		this.to_date_field = page.add_field({
			label: 'To Date',
			fieldtype: 'Date',
			fieldname: 'to_date',
			default: frappe.datetime.get_today(),
			onchange() {
				frappe.UserActivity.fetch_data(wrapper, page)
			}
		});
	
	}
}