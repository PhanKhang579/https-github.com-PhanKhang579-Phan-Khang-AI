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
		{"fieldname": "stock_uom", "label": _("ĐVT"), "fieldtype": "Link", "options": "UOM", "width": 70},
		{"fieldname": "qty", "label": _("Số lượng bán"), "fieldtype": "Float", "width": 110},
		{"fieldname": "avg_rate", "label": _("Giá bán TB"), "fieldtype": "Currency", "width": 110},
		{"fieldname": "revenue", "label": _("Doanh thu (chưa thuế)"), "fieldtype": "Currency", "width": 150},
		{"fieldname": "customer_count", "label": _("Số khách mua"), "fieldtype": "Int", "width": 100},
		{"fieldname": "percent", "label": _("Tỷ trọng (%)"), "fieldtype": "Percent", "width": 100},
	]


def get_data(filters):
	conditions = ["si.docstatus = 1", "si.company = %(company)s", "si.posting_date BETWEEN %(from_date)s AND %(to_date)s"]
	if filters.get("item_code"):
		conditions.append("sii.item_code = %(item_code)s")
	if filters.get("item_group"):
		conditions.append("sii.item_group = %(item_group)s")
	if filters.get("customer"):
		conditions.append("si.customer = %(customer)s")

	# Hóa đơn trả hàng (is_return) có số lượng/tiền âm nên tự trừ vào kết quả.
	rows = frappe.db.sql(
		f"""
		SELECT sii.item_code, sii.item_name, sii.item_group, sii.stock_uom,
			SUM(sii.stock_qty) AS qty,
			SUM(sii.base_net_amount) AS revenue,
			COUNT(DISTINCT si.customer) AS customer_count
		FROM `tabSales Invoice Item` sii
		JOIN `tabSales Invoice` si ON si.name = sii.parent
		WHERE {' AND '.join(conditions)}
		GROUP BY sii.item_code, sii.stock_uom
		ORDER BY revenue DESC
		""",
		filters,
		as_dict=True,
	)
	total = sum(r.revenue or 0 for r in rows)
	for r in rows:
		r.avg_rate = (r.revenue or 0) / r.qty if r.qty else 0
		r.percent = (r.revenue or 0) / total * 100 if total else 0
	return rows


def get_chart(data):
	top = data[:10]
	return {
		"data": {
			"labels": [r.item_name for r in top],
			"datasets": [{"name": _("Doanh thu"), "values": [r.revenue for r in top]}],
		},
		"type": "bar",
	}


def get_summary(data):
	return [
		{"label": _("Tổng doanh thu"), "value": sum(r.revenue or 0 for r in data), "datatype": "Currency"},
		{"label": _("Số sản phẩm bán ra"), "value": len(data), "datatype": "Int"},
	]
