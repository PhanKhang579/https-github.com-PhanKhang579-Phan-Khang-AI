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
	values = {}
	bundle_cond, legacy_cond = ["sbb.docstatus = 1", "sbb.is_cancelled = 0", "sbe.batch_no IS NOT NULL", "sbe.batch_no != ''"], [
		"sle.is_cancelled = 0", "sle.batch_no IS NOT NULL", "sle.batch_no != ''", "IFNULL(sle.serial_and_batch_bundle, '') = ''"]
	for key, bfield, lfield in (("company", "sbb.company", "sle.company"), ("item_code", "sbb.item_code", "sle.item_code"), ("warehouse", "sbe.warehouse", "sle.warehouse")):
		if filters.get(key):
			bundle_cond.append(f"{bfield} = %({key})s")
			legacy_cond.append(f"{lfield} = %({key})s")
			values[key] = filters[key]

	having = "" if filters.get("show_zero") else "HAVING qty > 0"
	# ERPNext v15 ghi số lô trong Serial and Batch Bundle (sổ kho không còn batch_no);
	# phần UNION thứ hai giữ lại dữ liệu cũ ghi trực tiếp batch_no trên Stock Ledger Entry.
	rows = frappe.db.sql(
		f"""
		SELECT m.item_code, i.item_name, i.stock_uom, m.batch_no, m.warehouse,
			SUM(m.qty) AS qty, b.manufacturing_date, b.expiry_date
		FROM (
			SELECT sbb.item_code, sbe.batch_no, sbe.warehouse, sbe.qty
			FROM `tabSerial and Batch Entry` sbe
			JOIN `tabSerial and Batch Bundle` sbb ON sbb.name = sbe.parent
			WHERE {' AND '.join(bundle_cond)}
			UNION ALL
			SELECT sle.item_code, sle.batch_no, sle.warehouse, sle.actual_qty
			FROM `tabStock Ledger Entry` sle
			WHERE {' AND '.join(legacy_cond)}
		) m
		JOIN `tabBatch` b ON b.name = m.batch_no
		JOIN `tabItem` i ON i.name = m.item_code
		GROUP BY m.item_code, m.batch_no, m.warehouse
		{having}
		ORDER BY b.expiry_date IS NULL, b.expiry_date, m.item_code
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
