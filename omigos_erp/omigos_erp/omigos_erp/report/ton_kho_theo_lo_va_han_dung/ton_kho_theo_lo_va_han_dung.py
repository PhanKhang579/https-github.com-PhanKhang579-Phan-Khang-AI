import frappe
from frappe import _
from frappe.utils import date_diff, getdate, nowdate


def execute(filters=None):
	filters = frappe._dict(filters or {})
	return get_columns(), get_data(filters)


def get_columns():
	return [
		{"fieldname": "item_code", "label": _("Mã hàng"), "fieldtype": "Link", "options": "Item", "width": 130},
		{"fieldname": "item_name", "label": _("Tên hàng"), "fieldtype": "Data", "width": 180},
		{"fieldname": "batch_no", "label": _("Số lô"), "fieldtype": "Link", "options": "Batch", "width": 130},
		{"fieldname": "warehouse", "label": _("Kho"), "fieldtype": "Link", "options": "Warehouse", "width": 150},
		{"fieldname": "qty", "label": _("Tồn"), "fieldtype": "Float", "width": 90},
		{"fieldname": "stock_uom", "label": _("ĐVT"), "fieldtype": "Link", "options": "UOM", "width": 70},
		{"fieldname": "manufacturing_date", "label": _("Ngày sản xuất"), "fieldtype": "Date", "width": 110},
		{"fieldname": "expiry_date", "label": _("Hạn dùng"), "fieldtype": "Date", "width": 110},
		{"fieldname": "days_left", "label": _("Số ngày còn lại"), "fieldtype": "Int", "width": 110},
		{"fieldname": "status", "label": _("Tình trạng"), "fieldtype": "Data", "width": 110},
	]


def get_data(filters):
	conditions = ["sle.is_cancelled = 0", "sle.batch_no != ''"]
	values = {}
	for key, field in (("company", "sle.company"), ("item_code", "sle.item_code"), ("warehouse", "sle.warehouse")):
		if filters.get(key):
			conditions.append(f"{field} = %({key})s")
			values[key] = filters[key]

	having = "" if filters.get("show_zero") else "HAVING qty > 0"
	rows = frappe.db.sql(
		f"""
		SELECT sle.item_code, i.item_name, i.stock_uom, sle.batch_no, sle.warehouse,
			SUM(sle.actual_qty) AS qty, b.manufacturing_date, b.expiry_date
		FROM `tabStock Ledger Entry` sle
		JOIN `tabBatch` b ON b.name = sle.batch_no
		JOIN `tabItem` i ON i.name = sle.item_code
		WHERE {' AND '.join(conditions)}
		GROUP BY sle.item_code, sle.batch_no, sle.warehouse
		{having}
		ORDER BY b.expiry_date IS NULL, b.expiry_date, sle.item_code
		""",
		values,
		as_dict=True,
	)

	today = getdate(nowdate())
	limit = filters.get("expiring_in_days")
	out = []
	for r in rows:
		if r.expiry_date:
			r.days_left = date_diff(r.expiry_date, today)
			if r.days_left < 0:
				r.status = "Đã hết hạn"
			elif r.days_left <= 90:
				r.status = "Sắp hết hạn"
			else:
				r.status = "Còn hạn"
		else:
			r.days_left, r.status = None, "Không có hạn"
		if limit not in (None, "") and r.days_left is not None and r.days_left > int(limit):
			continue
		if limit not in (None, "") and r.days_left is None:
			continue
		out.append(r)
	return out
