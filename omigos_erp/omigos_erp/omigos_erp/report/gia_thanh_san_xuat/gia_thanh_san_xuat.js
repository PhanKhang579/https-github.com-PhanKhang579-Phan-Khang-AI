frappe.query_reports["Gia thanh san xuat"] = {
	filters: [
		{ fieldname: "company", label: __("Công ty"), fieldtype: "Link", options: "Company", default: frappe.defaults.get_user_default("Company"), reqd: 1 },
		{ fieldname: "from_date", label: __("Từ ngày"), fieldtype: "Date", default: frappe.datetime.add_months(frappe.datetime.get_today(), -1), reqd: 1 },
		{ fieldname: "to_date", label: __("Đến ngày"), fieldtype: "Date", default: frappe.datetime.get_today(), reqd: 1 },
		{ fieldname: "item_code", label: __("Thành phẩm"), fieldtype: "Link", options: "Item" },
		{ fieldname: "detail", label: __("Chi tiết từng lệnh sản xuất"), fieldtype: "Check", default: 0 },
	],
};
