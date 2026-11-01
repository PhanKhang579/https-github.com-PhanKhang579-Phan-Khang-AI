import frappe
from frappe import _


def execute(filters=None):
	filters = frappe._dict(filters or {})
	if not (filters.from_date and filters.to_date):
		frappe.throw(_("Vui lòng chọn khoảng thời gian"))
	if filters.from_date > filters.to_date:
		frappe.throw(_("Từ ngày phải nhỏ hơn hoặc bằng Đến ngày"))
	data = get_data(filters)
	return get_columns(filters.detail), data, None, get_chart(data), get_summary(data)


def get_columns(detail):
	cols = []
	if detail:
		cols += [
			{"fieldname": "work_order", "label": _("Lệnh sản xuất"), "fieldtype": "Link", "options": "Work Order", "width": 150},
			{"fieldname": "posting_date", "label": _("Ngày"), "fieldtype": "Date", "width": 95},
		]
	cols += [
		{"fieldname": "item_code", "label": _("Mã thành phẩm"), "fieldtype": "Link", "options": "Item", "width": 130},
		{"fieldname": "item_name", "label": _("Tên thành phẩm"), "fieldtype": "Data", "width": 180},
		{"fieldname": "qty", "label": _("SL sản xuất"), "fieldtype": "Float", "width": 100},
		{"fieldname": "material_cost", "label": _("Chi phí nguyên vật liệu"), "fieldtype": "Currency", "width": 150},
		{"fieldname": "additional_cost", "label": _("Chi phí khác"), "fieldtype": "Currency", "width": 120},
		{"fieldname": "total_cost", "label": _("Tổng giá thành"), "fieldtype": "Currency", "width": 140},
		{"fieldname": "unit_cost", "label": _("Giá thành đơn vị"), "fieldtype": "Currency", "width": 130},
		{"fieldname": "standard_unit_cost", "label": _("Giá thành theo BOM"), "fieldtype": "Currency", "width": 130},
		{"fieldname": "variance_percent", "label": _("Chênh lệch so với BOM (%)"), "fieldtype": "Percent", "width": 150},
	]
	return cols


def get_data(filters):
	conditions = [
		"se.docstatus = 1",
		"se.purpose = 'Manufacture'",
		"se.company = %(company)s",
		"se.posting_date BETWEEN %(from_date)s AND %(to_date)s",
	]
	if filters.get("item_code"):
		conditions.append("wo.production_item = %(item_code)s")
	group_by = "se.name" if filters.get("detail") else "wo.production_item"

	rows = frappe.db.sql(
		f"""
		SELECT wo.production_item AS item_code, wo.item_name,
			MAX(se.work_order) AS work_order, MAX(se.posting_date) AS posting_date,
			SUM(se.fg_completed_qty) AS qty,
			SUM(se.total_outgoing_value) AS material_cost,
			SUM(se.total_additional_costs) AS additional_cost,
			SUM(se.fg_completed_qty * IFNULL(b.total_cost / NULLIF(b.quantity, 0), 0)) AS standard_total
		FROM `tabStock Entry` se
		JOIN `tabWork Order` wo ON wo.name = se.work_order
		LEFT JOIN `tabBOM` b ON b.name = IFNULL(se.bom_no, wo.bom_no)
		WHERE {' AND '.join(conditions)}
		GROUP BY {group_by}
		ORDER BY MAX(se.posting_date) DESC, wo.production_item
		""",
		filters,
		as_dict=True,
	)
	for r in rows:
		r.material_cost = r.material_cost or 0
		r.additional_cost = r.additional_cost or 0
		r.total_cost = r.material_cost + r.additional_cost
		r.unit_cost = r.total_cost / r.qty if r.qty else 0
		r.standard_unit_cost = (r.standard_total or 0) / r.qty if r.qty else 0
		r.variance_percent = (r.unit_cost - r.standard_unit_cost) / r.standard_unit_cost * 100 if r.standard_unit_cost else 0
	return rows


def get_chart(data):
	top = sorted(data, key=lambda r: -r.total_cost)[:10]
	return {
		"data": {
			"labels": [r.item_name for r in top],
			"datasets": [{"name": _("Tổng giá thành"), "values": [r.total_cost for r in top]}],
		},
		"type": "bar",
	}


def get_summary(data):
	return [
		{"label": _("Tổng giá thành"), "value": sum(r.total_cost for r in data), "datatype": "Currency"},
		{"label": _("Chi phí nguyên vật liệu"), "value": sum(r.material_cost for r in data), "datatype": "Currency"},
		{"label": _("Chi phí khác"), "value": sum(r.additional_cost for r in data), "datatype": "Currency"},
	]
