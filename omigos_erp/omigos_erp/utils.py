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


def company_header(company):
	"""Khối đầu mẫu in: logo, tên công ty, địa chỉ, MST, điện thoại, email, website.

	Lấy từ Company (logo, Tax ID, phone, email, website) và địa chỉ mặc định gắn với công ty.
	"""
	import re

	import frappe
	from frappe.utils import escape_html

	# Chứng từ không có trường công ty (vd Cosmetic Formula) thì dùng công ty mặc định.
	company = company or frappe.defaults.get_user_default("Company") or frappe.db.get_single_value("Global Defaults", "default_company")
	if not company or not frappe.db.exists("Company", company):
		return f"<b>{escape_html(company or '')}</b>"
	c = frappe.get_cached_doc("Company", company)

	lines = []
	try:
		from frappe.contacts.doctype.address.address import get_address_display, get_default_address

		addr = get_default_address("Company", company)
		if addr:
			shown = re.sub(r"(<br>\s*|\n)+", ", ", get_address_display(addr)).strip(", ")
			lines.append(shown)
	except Exception:
		pass
	if c.get("tax_id"):
		lines.append(f"MST: {escape_html(c.tax_id)}")
	contact = [escape_html(v) for v in (c.get("phone_no") and f"ĐT: {c.phone_no}", c.get("email") and f"Email: {c.email}", c.get("website")) if v]
	if contact:
		lines.append(" &nbsp;|&nbsp; ".join(contact))

	logo = f'<img src="{escape_html(c.company_logo)}" style="max-height:56px;max-width:140px">' if c.get("company_logo") else ""
	logo_cell = f'<td style="width:150px;vertical-align:top;border:none;padding:0 12px 0 0">{logo}</td>' if logo else ""
	text = f'<b style="font-size:14px">{escape_html(c.company_name)}</b>' + "".join(f"<br><span>{x}</span>" for x in lines)
	return (
		'<table class="noborder" style="width:100%;margin:0 0 4px"><tr>'
		f'{logo_cell}<td style="vertical-align:top;border:none;padding:0">{text}</td></tr></table>'
	)
