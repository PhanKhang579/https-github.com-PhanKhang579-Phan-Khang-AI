frappe.query_reports["Gia thanh theo cong thuc"] = {
	filters: [
		{ fieldname: "formula", label: __("Công thức"), fieldtype: "Link", options: "Cosmetic Formula" },
		{ fieldname: "product", label: __("Sản phẩm"), fieldtype: "Link", options: "Item" },
		{ fieldname: "customer", label: __("Khách hàng"), fieldtype: "Link", options: "Customer" },
		{ fieldname: "status", label: __("Trạng thái"), fieldtype: "Select", options: "\nDraft\nApproved\nObsolete", default: "Approved" },
		{ fieldname: "price_source", label: __("Nguồn đơn giá nguyên liệu"), fieldtype: "Select", options: "Giá vốn kho\nGiá mua gần nhất", default: "Giá vốn kho" },
		{ fieldname: "detail", label: __("Chi tiết từng nguyên liệu"), fieldtype: "Check", default: 0 },
	],
	formatter(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (column.fieldname === "missing_price" && data && data.missing_price) {
			value = `<span style="color:red;font-weight:bold">${value}</span>`;
		}
		if (column.fieldname === "unit_price" && data && data.unit_price === 0) {
			value = `<span style="color:red">${value}</span>`;
		}
		return value;
	},
};
