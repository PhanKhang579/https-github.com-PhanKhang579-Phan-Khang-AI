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
		{"fieldname": "customer", "label": _("Khách hàng"), "fieldtype": "Link", "options": "Customer", "width": 130},
		{"fieldname": "customer_name", "label": _("Tên khách hàng"), "fieldtype": "Data", "width": 200},
		{"fieldname": "customer_group", "label": _("Nhóm"), "fieldtype": "Link", "options": "Customer Group", "width": 120},
		{"fieldname": "invoice_count", "label": _("Số hóa đơn"), "fieldtype": "Int", "width": 90},
		{"fieldname": "net_total", "label": _("Doanh thu (chưa thuế)"), "fieldtype": "Currency", "width": 150},
		{"fieldname": "tax", "label": _("Thuế"), "fieldtype": "Currency", "width": 110},
		{"fieldname": "grand_total", "label": _("Tổng cộng"), "fieldtype": "Currency", "width": 140},
		{"fieldname": "outstanding", "label": _("Còn phải thu"), "fieldtype": "Currency", "width": 130},
		{"fieldname": "percent", "label": _("Tỷ trọng (%)"), "fieldtype": "Percent", "width": 100},
		{"fieldname": "last_invoice_date", "label": _("Hóa đơn gần nhất"), "fieldtype": "Date", "width": 120},
	]


def get_data(filters):
	conditions = ["si.docstatus = 1", "si.company = %(company)s", "si.posting_date BETWEEN %(from_date)s AND %(to_date)s"]
	if filters.get("customer"):
		conditions.append("si.customer = %(customer)s")
	if filters.get("customer_group"):
		conditions.append("c.customer_group = %(customer_group)s")

	# Hóa đơn trả hàng (is_return) mang giá trị âm nên tự trừ vào doanh thu.
	rows = frappe.db.sql(
		f"""
		SELECT si.customer, si.customer_name, c.customer_group,
			COUNT(si.name) AS invoice_count,
			SUM(si.base_net_total) AS net_total,
			SUM(si.base_total_taxes_and_charges) AS tax,
			SUM(si.base_grand_total) AS grand_total,
			SUM(si.outstanding_amount) AS outstanding,
			MAX(si.posting_date) AS last_invoice_date
		FROM `tabSales Invoice` si
		JOIN `tabCustomer` c ON c.name = si.customer
		WHERE {' AND '.join(conditions)}
		GROUP BY si.customer
		ORDER BY net_total DESC
		""",
		filters,
		as_dict=True,
	)
	total = sum(r.net_total or 0 for r in rows)
	for r in rows:
		r.percent = (r.net_total or 0) / total * 100 if total else 0
	return rows


def get_chart(data):
	top = data[:10]
	return {
		"data": {
			"labels": [r.customer_name for r in top],
			"datasets": [{"name": _("Doanh thu"), "values": [r.net_total for r in top]}],
		},
		"type": "bar",
	}


def get_summary(data):
	net = sum(r.net_total or 0 for r in data)
	return [
		{"label": _("Tổng doanh thu"), "value": net, "datatype": "Currency"},
		{"label": _("Số khách hàng"), "value": len(data), "datatype": "Int"},
		{"label": _("Còn phải thu"), "value": sum(r.outstanding or 0 for r in data), "datatype": "Currency"},
	]
