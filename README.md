# Omigos ERP (ERPNext/Frappe)

ERP dạng Odoo xây trên **ERPNext** (mã nguồn mở, Frappe Framework).

## Phân chia module
| Nghiệp vụ | Nguồn |
|---|---|
| Bán hàng + Khách hàng | ERPNext: Selling, CRM |
| Kho | ERPNext: Stock (lô, hạn dùng) |
| Sản xuất mỹ phẩm | ERPNext: Manufacturing (BOM, Work Order) + app `omigos_erp` (Cosmetic Formula) |
| Hóa đơn / Kế toán | ERPNext: Accounts |

App `omigos_erp` thêm DocType **Cosmetic Formula** (công thức theo % + pha A/B/C/D, kiểm tra tổng = 100% trước khi duyệt).

## Cài đặt
```bash
./scripts/install.sh   # cần bench, Python 3.10+, Node 18, MariaDB, Redis
```
Truy cập http://omigos.localhost:8000 (Administrator / admin) rồi chạy Setup Wizard, bật các module trên.

## Bước tiếp theo
- Nút "Tạo BOM" đã có: công thức Approved + có sản phẩm → BOM (qty = tỷ lệ% × khối lượng mẻ)
- Mẫu in tiếng Việt đã có: Báo giá, Hóa đơn bán hàng, Phiếu sản xuất, Công thức mỹ phẩm, Phiếu nhập kho (Purchase Receipt), Phiếu xuất kho (Delivery Note), Phiếu kho (Stock Entry: nhập/xuất/chuyển/sản xuất) — chọn trong Print, tên "... VN"
- Hóa đơn điện tử theo chuẩn VN (kết nối nhà cung cấp HĐĐT)
