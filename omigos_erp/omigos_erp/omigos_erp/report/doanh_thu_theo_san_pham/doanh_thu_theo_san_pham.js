frappe.query_reports["Doanh thu theo san pham"] = {
	filters: [
		{ fieldname: "company", label: __("Công ty"), fieldtype: "Link", options: "Company", default: frappe.defaults.get_user_default("Company"), reqd: 1 },
		{ fieldname: "from_date", label: __("Từ ngày"), fieldtype: "Date", default: frappe.datetime.add_months(frappe.datetime.get_today(), -1), reqd: 1 },
		{ fieldname: "to_date", label: __("Đến ngày"), fieldtype: "Date", default: frappe.datetime.get_today(), reqd: 1 },
		{ fieldname: "item_code", label: __("Sản phẩm"), fieldtype: "Link", options: "Item" },
		{ fieldname: "item_group", label: __("Nhóm sản phẩm"), fieldtype: "Link", options: "Item Group" },
		{ fieldname: "customer", label: __("Khách hàng"), fieldtype: "Link", options: "Customer" },
	],
};
