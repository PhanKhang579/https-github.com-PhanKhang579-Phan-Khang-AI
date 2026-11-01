frappe.query_reports["Ton kho theo lo va han dung"] = {
	filters: [
		{ fieldname: "company", label: __("Công ty"), fieldtype: "Link", options: "Company", default: frappe.defaults.get_user_default("Company") },
		{ fieldname: "item_code", label: __("Mặt hàng"), fieldtype: "Link", options: "Item" },
		{ fieldname: "warehouse", label: __("Kho"), fieldtype: "Link", options: "Warehouse" },
		{ fieldname: "expiring_in_days", label: __("Hết hạn trong (ngày)"), fieldtype: "Int", description: __("Để trống = tất cả; lô đã hết hạn luôn được hiển thị") },
		{ fieldname: "show_zero", label: __("Hiện lô đã hết tồn"), fieldtype: "Check", default: 0 },
	],
	formatter(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (column.fieldname === "status" && data) {
			const color = { "Đã hết hạn": "red", "Sắp hết hạn": "orange", "Còn hạn": "green" }[data.status];
			if (color) value = `<span style="color:${color};font-weight:bold">${value}</span>`;
		}
		return value;
	},
};
