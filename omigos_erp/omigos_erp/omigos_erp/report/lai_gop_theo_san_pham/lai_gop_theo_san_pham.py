import frappe
from frappe import _


def execute(filters=None):
	filters = frappe._dict(filters or {})
	if not (filters.from_date and filters.to_date):
		frappe.throw(_("Vui lòng chọn khoảng thời gian"))
	if filters.from_date > filters.to_date:
		frappe.throw(_("Từ ngày phải nhỏ hơn hoặc bằng Đến ngày"))
	data = get_data(filters)
	return get_columns(), data, None, get_chart(data), get_summary(data)


def get_columns():
	return [
		{"fieldname": "item_code", "label": _("Mã hàng"), "fieldtype": "Link", "options": "Item", "width": 130},
		{"fieldname": "item_name", "label": _("Tên sản phẩm"), "fieldtype": "Data", "width": 200},
		{"fieldname": "item_group", "label": _("Nhóm"), "fieldtype": "Link", "options": "Item Group", "width": 120},
		{"fieldname": "qty", "label": _("Số lượng bán"), "fieldtype": "Float", "width": 100},
		{"fieldname": "revenue", "label": _("Doanh thu (chưa thuế)"), "fieldtype": "Currency", "width": 150},
		{"fieldname": "cogs", "label": _("Giá vốn"), "fieldtype": "Currency", "width": 130},
		{"fieldname": "gross_profit", "label": _("Lãi gộp"), "fieldtype": "Currency", "width": 130},
		{"fieldname": "margin", "label": _("Biên lãi gộp (%)"), "fieldtype": "Percent", "width": 120},
		{"fieldname": "estimated", "label": _("Giá vốn ước tính"), "fieldtype": "Check", "width": 110},
	]


def get_data(filters):
	conditions = ["si.docstatus = 1", "si.company = %(company)s", "si.posting_date BETWEEN %(from_date)s AND %(to_date)s"]
	if filters.get("item_code"):
		conditions.append("sii.item_code = %(item_code)s")
	if filters.get("item_group"):
		conditions.append("sii.item_group = %(item_group)s")
	if filters.get("customer"):
		conditions.append("si.customer = %(customer)s")

	# Giá vốn dòng hàng = incoming_rate (giá vốn tại thời điểm xuất, ERPNext ghi khi hóa đơn cập nhật kho).
	# Nếu incoming_rate = 0 (xuất kho qua Delivery Note) thì tạm dùng giá vốn hiện hành của mặt hàng -> đánh dấu "ước tính".
	# Hàng dịch vụ (không quản lý kho) không có giá vốn. Hóa đơn trả hàng mang số âm nên tự trừ.
	rows = frappe.db.sql(
		f"""
		SELECT sii.item_code, sii.item_name, sii.item_group,
			SUM(sii.stock_qty) AS qty,
			SUM(sii.base_net_amount) AS revenue,
			SUM(CASE WHEN i.is_stock_item = 0 THEN 0
				ELSE sii.stock_qty * IF(sii.incoming_rate > 0, sii.incoming_rate, i.valuation_rate) END) AS cogs,
			MAX(i.is_stock_item = 1 AND sii.incoming_rate <= 0) AS estimated
		FROM `tabSales Invoice Item` sii
		JOIN `tabSales Invoice` si ON si.name = sii.parent
		JOIN `tabItem` i ON i.name = sii.item_code
		WHERE {' AND '.join(conditions)}
		GROUP BY sii.item_code
		ORDER BY SUM(sii.base_net_amount) DESC
		""",
		filters,
		as_dict=True,
	)
	for r in rows:
		r.revenue = r.revenue or 0
		r.cogs = r.cogs or 0
		r.gross_profit = r.revenue - r.cogs
		r.margin = r.gross_profit / r.revenue * 100 if r.revenue else 0
	rows.sort(key=lambda r: -r.gross_profit)
	return rows


def get_chart(data):
	top = data[:10]
	return {
		"data": {
			"labels": [r.item_name for r in top],
			"datasets": [{"name": _("Lãi gộp"), "values": [r.gross_profit for r in top]}],
		},
		"type": "bar",
	}


def get_summary(data):
	revenue = sum(r.revenue for r in data)
	profit = sum(r.gross_profit for r in data)
	return [
		{"label": _("Doanh thu"), "value": revenue, "datatype": "Currency"},
		{"label": _("Giá vốn"), "value": sum(r.cogs for r in data), "datatype": "Currency"},
		{"label": _("Lãi gộp"), "value": profit, "datatype": "Currency"},
		{"label": _("Biên lãi gộp (%)"), "value": profit / revenue * 100 if revenue else 0, "datatype": "Percent"},
	]
