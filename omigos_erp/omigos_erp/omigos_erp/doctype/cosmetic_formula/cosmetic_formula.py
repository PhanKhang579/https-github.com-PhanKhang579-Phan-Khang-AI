import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class CosmeticFormula(Document):
	def validate(self):
		self.total_percentage = sum(flt(row.percentage) for row in self.items)
		if self.status == "Approved" and abs(self.total_percentage - 100) > 0.001:
			frappe.throw(_("Cong thuc phai co tong ty le bang 100% truoc khi duyet (hien tai: {0}%)").format(self.total_percentage))
