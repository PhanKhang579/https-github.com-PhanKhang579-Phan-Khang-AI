import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class CosmeticFormula(Document):
	def validate(self):
		self.total_percentage = sum(flt(row.percentage) for row in self.items)
		if self.status == "Approved" and abs(self.total_percentage - 100) > 0.001:
			frappe.throw(_("Cong thuc phai co tong ty le bang 100% truoc khi duyet (hien tai: {0}%)").format(self.total_percentage))

	@frappe.whitelist()
	def make_bom(self):
		"""Tao BOM tu cong thuc: qty nguyen lieu = ty le% x khoi luong me."""
		if self.status != "Approved":
			frappe.throw(_("Chi tao BOM tu cong thuc da duyet (Approved)"))
		if not self.product:
			frappe.throw(_("Chon san pham truoc khi tao BOM"))
		if self.bom:
			frappe.throw(_("Cong thuc nay da co BOM: {0}").format(self.bom))
		batch = flt(self.batch_size)
		if batch <= 0:
			frappe.throw(_("Khoi luong me phai lon hon 0"))

		bom = frappe.new_doc("BOM")
		bom.item = self.product
		bom.quantity = batch
		bom.company = frappe.defaults.get_user_default("Company") or frappe.db.get_single_value("Global Defaults", "default_company")
		for row in self.items:
			bom.append("items", {"item_code": row.item_code, "qty": flt(row.percentage) * batch / 100})
		bom.insert()
		self.db_set("bom", bom.name)
		return bom.name
