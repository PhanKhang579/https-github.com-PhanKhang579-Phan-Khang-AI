import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
	filters = frappe._dict(filters or {})
	formulas = get_formulas(filters)
	prices = get_prices(filters.get("price_source"))
	costed = [cost_formula(f, prices) for f in formulas]
	data = get_detail(costed) if filters.detail else costed
	return get_columns(filters.detail), data, None, get_chart(costed), get_summary(costed)


def get_columns(detail):
	if detail:
		return [
			{"fieldname": "formula", "label": _("Công thức"), "fieldtype": "Link", "options": "Cosmetic Formula", "width": 160},
			{"fieldname": "phase", "label": _("Pha"), "fieldtype": "Data", "width": 50},
			{"fieldname": "item_code", "label": _("Nguyên liệu"), "fieldtype": "Link", "options": "Item", "width": 130},
			{"fieldname": "item_name", "label": _("Tên nguyên liệu"), "fieldtype": "Data", "width": 190},
			{"fieldname": "percentage", "label": _("Tỷ lệ (%)"), "fieldtype": "Percent", "width": 90},
			{"fieldname": "qty", "label": _("Khối lượng/mẻ"), "fieldtype": "Float", "width": 110},
			{"fieldname": "unit_price", "label": _("Đơn giá"), "fieldtype": "Currency", "width": 110},
			{"fieldname": "amount", "label": _("Thành tiền"), "fieldtype": "Currency", "width": 120},
			{"fieldname": "share", "label": _("Tỷ trọng chi phí (%)"), "fieldtype": "Percent", "width": 130},
		]
	return [
		{"fieldname": "formula", "label": _("Công thức"), "fieldtype": "Link", "options": "Cosmetic Formula", "width": 170},
		{"fieldname": "version", "label": _("Phiên bản"), "fieldtype": "Data", "width": 80},
		{"fieldname": "product", "label": _("Sản phẩm"), "fieldtype": "Link", "options": "Item", "width": 130},
		{"fieldname": "customer", "label": _("Khách hàng"), "fieldtype": "Link", "options": "Customer", "width": 130},
		{"fieldname": "status", "label": _("Trạng thái"), "fieldtype": "Data", "width": 90},
		{"fieldname": "batch_size", "label": _("Khối lượng mẻ"), "fieldtype": "Float", "width": 100},
		{"fieldname": "total_percentage", "label": _("Tổng tỷ lệ (%)"), "fieldtype": "Percent", "width": 100},
		{"fieldname": "batch_cost", "label": _("Giá thành/mẻ"), "fieldtype": "Currency", "width": 130},
		{"fieldname": "unit_cost", "label": _("Giá thành/đơn vị"), "fieldtype": "Currency", "width": 130},
		{"fieldname": "missing_price", "label": _("Nguyên liệu thiếu giá"), "fieldtype": "Int", "width": 130},
	]


def get_formulas(filters):
	conditions, values = ["1=1"], {}
	for key, field in (("formula", "name"), ("product", "product"), ("customer", "customer"), ("status", "status")):
		if filters.get(key):
			conditions.append(f"{field} = %({key})s")
			values[key] = filters[key]
	formulas = frappe.db.sql(
		f"SELECT name, version, product, customer, status, batch_size, total_percentage FROM `tabCosmetic Formula` WHERE {' AND '.join(conditions)} ORDER BY name",
		values,
		as_dict=True,
	)
	for f in formulas:
		f.items = frappe.get_all(
			"Cosmetic Formula Item",
			filters={"parent": f.name, "parenttype": "Cosmetic Formula"},
			fields=["item_code", "item_name", "percentage", "phase", "idx"],
			order_by="idx",
		)
	return formulas


def get_prices(source):
	"""Đơn giá theo mặt hàng. Mặc định: giá vốn bình quân trong kho (Bin), thiếu thì lấy giá mua gần nhất."""
	last = {r.name: flt(r.last_purchase_rate) for r in frappe.get_all("Item", fields=["name", "last_purchase_rate"])}
	if source == "Giá mua gần nhất":
		return last
	stock = frappe.db.sql(
		"SELECT item_code, SUM(stock_value) AS value, SUM(actual_qty) AS qty FROM `tabBin` WHERE actual_qty > 0 GROUP BY item_code",
		as_dict=True,
	)
	prices = dict(last)
	for r in stock:
		if flt(r.qty) > 0 and flt(r.value) > 0:
			prices[r.item_code] = flt(r.value) / flt(r.qty)
	return prices


def cost_formula(f, prices):
	batch = flt(f.batch_size)
	f.missing_price = 0
	f.batch_cost = 0
	for row in f.items:
		row.qty = flt(row.percentage) * batch / 100
		row.unit_price = flt(prices.get(row.item_code))
		row.amount = row.qty * row.unit_price
		if not row.unit_price:
			f.missing_price += 1
		f.batch_cost += row.amount
	f.unit_cost = f.batch_cost / batch if batch else 0
	for row in f.items:
		row.share = row.amount / f.batch_cost * 100 if f.batch_cost else 0
	return f


def get_detail(costed):
	rows = []
	for f in costed:
		for r in f.items:
			rows.append(frappe._dict(formula=f.name, phase=r.phase, item_code=r.item_code, item_name=r.item_name,
				percentage=r.percentage, qty=r.qty, unit_price=r.unit_price, amount=r.amount, share=r.share))
	return rows


def get_chart(costed):
	top = sorted(costed, key=lambda f: -f.unit_cost)[:10]
	return {
		"data": {
			"labels": [f.name for f in top],
			"datasets": [{"name": _("Giá thành/đơn vị"), "values": [f.unit_cost for f in top]}],
		},
		"type": "bar",
	}


def get_summary(costed):
	return [
		{"label": _("Số công thức"), "value": len(costed), "datatype": "Int"},
		{"label": _("Công thức thiếu giá nguyên liệu"), "value": sum(1 for f in costed if f.missing_price), "datatype": "Int", "indicator": "Red"},
		{"label": _("Công thức tổng tỷ lệ khác 100%"), "value": sum(1 for f in costed if abs(flt(f.total_percentage) - 100) > 0.001), "datatype": "Int", "indicator": "Orange"},
	]
