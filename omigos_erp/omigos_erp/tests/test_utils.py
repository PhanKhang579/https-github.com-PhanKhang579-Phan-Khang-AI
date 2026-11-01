from frappe.tests.utils import FrappeTestCase

from omigos_erp.utils import vn_money_in_words


class TestVnMoneyInWords(FrappeTestCase):
	def test_vnd(self):
		cases = {
			0: "Không đồng chẵn.",
			21: "Hai mươi mốt đồng chẵn.",
			105: "Một trăm lẻ năm đồng chẵn.",
			1100: "Một nghìn một trăm đồng chẵn.",
			1500000: "Một triệu năm trăm nghìn đồng chẵn.",
			-2000: "Âm hai nghìn đồng chẵn.",
		}
		for amount, expected in cases.items():
			self.assertEqual(vn_money_in_words(amount, "VND"), expected)

	def test_other_currency(self):
		self.assertEqual(vn_money_in_words(12.4, "USD"), "Mười hai USD.")


class TestCompanyHeader(FrappeTestCase):
	def test_unknown_company_falls_back_to_name(self):
		from omigos_erp.utils import company_header

		self.assertEqual(company_header("Khong Ton Tai <x>"), "<b>Khong Ton Tai &lt;x&gt;</b>")
