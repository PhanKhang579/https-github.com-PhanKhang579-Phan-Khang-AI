"""Ham dung chung cho mau in (goi tu Jinja)."""
from frappe.utils import flt

CURRENCY_NAMES = {"VND": "đồng"}


def vn_money_in_words(amount, currency="VND"):
	"""Doc so tien bang chu tieng Viet, khong phu thuoc ngon ngu he thong.

	1100000 -> "Một triệu một trăm nghìn đồng chẵn."
	"""
	from num2words import num2words

	value = int(round(flt(amount)))
	if value == 0:
		words = "không"
	else:
		words = num2words(abs(value), lang="vi")
		if value < 0:
			words = "âm " + words
	unit = CURRENCY_NAMES.get(currency or "VND", currency)
	text = f"{words} {unit}"
	if (currency or "VND") == "VND":
		text += " chẵn"
	text = text.replace("-", " ")
	return text[:1].upper() + text[1:] + "."
