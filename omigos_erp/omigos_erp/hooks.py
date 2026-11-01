app_name = "omigos_erp"
app_title = "Omigos ERP"
app_publisher = "Omigos"
app_description = "ERP tuy bien cho gia cong my pham tren ERPNext"
app_email = "rykerphan579@gmail.com"
app_license = "mit"
required_apps = ["erpnext"]

# Cac module chuan (Selling, Stock, Manufacturing, Accounts) da co san trong ERPNext.
# App nay chi bo sung phan dac thu my pham: Cong thuc (Cosmetic Formula).

# Ham dung trong mau in: {{ vn_money_in_words(doc.grand_total, doc.currency) }}
jinja = {"methods": ["omigos_erp.utils.vn_money_in_words"]}
