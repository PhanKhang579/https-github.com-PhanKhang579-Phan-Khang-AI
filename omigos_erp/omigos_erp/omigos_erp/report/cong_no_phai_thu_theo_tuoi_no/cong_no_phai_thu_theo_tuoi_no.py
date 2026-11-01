import frappe
from frappe import _
from frappe.utils import date_diff, getdate

BUCKETS = [("b0", "Chưa đến hạn", None, 0), ("b1", "1-30 ngày", 1, 30), ("b2", "31-60 ngày", 31, 60), ("b3", "61-90 ngày", 61, 90), ("b4", "Trên 90 ngày", 91, None)]


def execute(filters=None):
	filters = frappe._dict(filters or {})
	if not filters.as_of_date:
		frappe.throw(_("Vui lòng chọn ngày"))
	invoices = get_invoices(filters)
	data = get_detail(invoices) if filters.detail else get_summary(invoices)
	return get_columns(filters.detail), data, None, get_chart(invoices), get_report_summary(invoices)


def get_columns(detail):
	cols = []
	if detail:
		cols += [
			{"fieldname": "invoice", "label": _("Hóa đơn"), "fieldtype": "Link", "options": "Sales Invoice", "width": 150},
			{"fieldname": "posting_date", "label": _("Ngày HĐ"), "fieldtype": "Date", "width": 100},
			{"fieldname": "due_date", "label": _("Đến hạn"), "fieldtype": "Date", "width": 100},
		]
	cols += [
		{"fieldname": "customer", "label": _("Khách hàng"), "fieldtype": "Link", "options": "Customer", "width": 120},
		{"fieldname": "customer_name", "label": _("Tên khách hàng"), "fieldtype": "Data", "width": 190},
		{"fieldname": "outstanding", "label": _("Tổng còn nợ"), "fieldtype": "Currency", "width": 130},
	]
	cols += [{"fieldname": f, "label": _(l), "fieldtype": "Currency", "width": 120} for f, l, _a, _b in BUCKETS]
	return cols


def get_invoices(filters):
	conditions = ["si.docstatus = 1", "si.outstanding_amount != 0", "si.company = %(company)s", "si.posting_date <= %(as_of_date)s"]
	if filters.get("customer"):
		conditions.append("si.customer = %(customer)s")
	if filters.get("customer_group"):
		conditions.append("c.customer_group = %(customer_group)s")
	rows = frappe.db.sql(
		f"""
		SELECT si.name AS invoice, si.customer, si.customer_name, si.posting_date,
			COALESCE(si.due_date, si.posting_date) AS due_date, si.outstanding_amount AS outstanding
		FROM `tabSales Invoice` si JOIN `tabCustomer` c ON c.name = si.customer
		WHERE {' AND '.join(conditions)}
		ORDER BY si.customer, si.posting_date
		""",
		filters,
		as_dict=True,
	)
	as_of = getdate(filters.as_of_date)
	base = "posting_date" if filters.ageing_based_on == "Ngày hóa đơn" else "due_date"
	for r in rows:
		days = date_diff(as_of, r[base])
		r.age = days
		for f, _l, lo, hi in BUCKETS:
			r[f] = 0
			if (lo is None or days >= lo) and (hi is None or days <= hi):
				r[f] = r.outstanding
	return rows


def get_detail(invoices):
	return invoices


def get_summary(invoices):
	by_cust = {}
	for r in invoices:
		row = by_cust.setdefault(r.customer, frappe._dict(customer=r.customer, customer_name=r.customer_name, outstanding=0, **{f: 0 for f, *_ in BUCKETS}))
		row.outstanding += r.outstanding
		for f, *_ in BUCKETS:
			row[f] += r[f]
	return sorted(by_cust.values(), key=lambda x: -x.outstanding)


def get_chart(invoices):
	return {
		"data": {
			"labels": [l for _f, l, *_ in BUCKETS],
			"datasets": [{"name": _("Còn nợ"), "values": [sum(r[f] for r in invoices) for f, *_ in BUCKETS]}],
		},
		"type": "bar",
	}


def get_report_summary(invoices):
	total = sum(r.outstanding for r in invoices)
	overdue = sum(r.outstanding for r in invoices if r.age > 0)
	return [
		{"label": _("Tổng công nợ"), "value": total, "datatype": "Currency"},
		{"label": _("Quá hạn"), "value": overdue, "datatype": "Currency"},
		{"label": _("Số khách còn nợ"), "value": len({r.customer for r in invoices}), "datatype": "Int"},
	]
