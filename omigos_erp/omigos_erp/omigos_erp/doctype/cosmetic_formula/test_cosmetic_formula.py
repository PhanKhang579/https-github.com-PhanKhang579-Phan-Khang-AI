import frappe
from frappe.tests.utils import FrappeTestCase


def make_item(code):
	if not frappe.db.exists("Item", code):
		frappe.get_doc({"doctype": "Item", "item_code": code, "item_name": code,
			"item_group": "All Item Groups", "stock_uom": "Nos", "is_stock_item": 0}).insert()


class TestCosmeticFormula(FrappeTestCase):
	def setUp(self):
		for code in ("TF-A", "TF-B"):
			make_item(code)

	def new_formula(self, pct_a, pct_b, **kw):
		return frappe.get_doc({"doctype": "Cosmetic Formula", "formula_name": frappe.generate_hash(length=8),
			"items": [{"item_code": "TF-A", "percentage": pct_a}, {"item_code": "TF-B", "percentage": pct_b}], **kw})

	def test_total_percentage(self):
		f = self.new_formula(70, 30).insert()
		self.assertEqual(f.total_percentage, 100)

	def test_cannot_approve_unless_100(self):
		f = self.new_formula(70, 20, status="Approved")
		self.assertRaises(frappe.ValidationError, f.insert)

	def test_loss_percent_range(self):
		f = self.new_formula(70, 30, loss_percent=100)
		self.assertRaises(frappe.ValidationError, f.insert)

	def test_make_bom_requires_approved_and_product(self):
		f = self.new_formula(70, 30).insert()
		self.assertRaises(frappe.ValidationError, f.make_bom)
