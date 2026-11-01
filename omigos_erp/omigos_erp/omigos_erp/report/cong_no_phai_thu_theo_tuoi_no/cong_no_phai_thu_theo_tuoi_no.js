frappe.query_reports["Cong no phai thu theo tuoi no"] = {
	filters: [
		{ fieldname: "company", label: __("Công ty"), fieldtype: "Link", options: "Company", default: frappe.defaults.get_user_default("Company"), reqd: 1 },
		{ fieldname: "as_of_date", label: __("Tính đến ngày"), fieldtype: "Date", default: frappe.datetime.get_today(), reqd: 1 },
		{ fieldname: "customer", label: __("Khách hàng"), fieldtype: "Link", options: "Customer" },
		{ fieldname: "customer_group", label: __("Nhóm khách hàng"), fieldtype: "Link", options: "Customer Group" },
		{
			fieldname: "ageing_based_on", label: __("Tính tuổi nợ theo"), fieldtype: "Select",
			options: "Ngày đến hạn\nNgày hóa đơn", default: "Ngày đến hạn",
		},
		{ fieldname: "detail", label: __("Chi tiết từng hóa đơn"), fieldtype: "Check", default: 0 },
	],
};
