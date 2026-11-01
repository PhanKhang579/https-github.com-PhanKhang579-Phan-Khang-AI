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

## Báo cáo
- **Ton kho theo lo va han dung** (Stock → Report): tồn theo lô/kho, hạn dùng, số ngày còn lại, tình trạng (Đã hết hạn / Sắp hết hạn ≤90 ngày / Còn hạn); lọc công ty, mặt hàng, kho, hết hạn trong N ngày.

- **Doanh thu theo khach hang** (Accounts → Report): doanh thu, thuế, còn phải thu, tỷ trọng theo khách hàng; lọc kỳ, khách hàng, nhóm; có biểu đồ top 10; hóa đơn trả hàng tự trừ.

- **Doanh thu theo san pham** (Accounts → Report): số lượng, giá bán TB, doanh thu, số khách mua, tỷ trọng theo sản phẩm; lọc kỳ, sản phẩm, nhóm, khách hàng; biểu đồ top 10.

- **Cong no phai thu theo tuoi no** (Accounts → Report): công nợ theo khách hàng chia nhóm Chưa đến hạn / 1-30 / 31-60 / 61-90 / trên 90 ngày; tính theo ngày đến hạn hoặc ngày hóa đơn; xem chi tiết từng hóa đơn. Lấy từ Sales Invoice còn dư nợ (chưa gồm bút toán Journal/thanh toán chưa phân bổ — đối chiếu với báo cáo "Accounts Receivable" chuẩn của ERPNext).

## Bước tiếp theo
- Nút "Tạo BOM" đã có: công thức Approved + có sản phẩm → BOM (qty = tỷ lệ% × khối lượng mẻ)
- Mẫu in tiếng Việt đã có: Báo giá, Hóa đơn bán hàng, Phiếu sản xuất, Công thức mỹ phẩm, Phiếu nhập kho (Purchase Receipt), Phiếu xuất kho (Delivery Note), Phiếu kho (Stock Entry), Phiếu thu/chi (Payment Entry), Đơn đặt hàng bán (Sales Order), Đơn mua hàng (Purchase Order) — chọn trong Print, tên "... VN"
- Hóa đơn điện tử theo chuẩn VN (kết nối nhà cung cấp HĐĐT)
