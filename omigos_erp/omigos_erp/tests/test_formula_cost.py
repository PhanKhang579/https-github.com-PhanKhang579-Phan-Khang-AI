import frappe
from frappe.tests.utils import FrappeTestCase

from omigos_erp.omigos_erp.report.gia_thanh_theo_cong_thuc.gia_thanh_theo_cong_thuc import cost_formula, get_detail


def make_formula():
	return frappe._dict(
		name="F1", batch_size=100, total_percentage=100, labor_cost=500, overhead_cost=300, loss_percent=2,
		ingredients=[
			frappe._dict(item_code="A", item_name="A", percentage=60, phase="A"),
			frappe._dict(item_code="B", item_name="B", percentage=40, phase="B"),
		],
		packaging=[frappe._dict(item_code="P", item_name="Chai", qty_per_unit=0.5)],
	)


class TestFormulaCost(FrappeTestCase):
	def test_cost_breakdown(self):
		f = cost_formula(make_formula(), {"A": 10, "B": 20, "P": 100})
		self.assertEqual(f.material_cost, 1400)
		self.assertAlmostEqual(f.loss_cost, 1400 * 2 / 98, places=6)
		self.assertEqual(f.packaging_cost, 5000)
		self.assertAlmostEqual(f.batch_cost, 1400 + 1400 * 2 / 98 + 5000 + 800, places=6)
		self.assertAlmostEqual(f.unit_cost, f.batch_cost / 100, places=6)
		self.assertEqual(f.missing_price, 0)

	def test_missing_price_is_flagged(self):
		f = cost_formula(make_formula(), {"A": 10, "P": 100})
		self.assertEqual(f.missing_price, 1)

	def test_detail_rows(self):
		f = cost_formula(make_formula(), {"A": 10, "B": 20, "P": 100})
		rows = get_detail([f])
		# 2 nguyên liệu + 1 bao bì + hao hụt + nhân công + chi phí chung
		self.assertEqual(len(rows), 6)
		self.assertAlmostEqual(sum(r.share for r in rows), 100, places=6)
