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

## Ngôn ngữ và định dạng
- Dòng "Bằng chữ" trên các mẫu in dùng hàm riêng `vn_money_in_words` (omigos_erp/utils.py), luôn đọc bằng tiếng Việt, không phụ thuộc ngôn ngữ hệ thống: ví dụ 1.100.000 → "Một triệu một trăm nghìn đồng chẵn." Tiền khác VND đọc phần nguyên kèm mã tiền (vd "Mười hai USD."), chưa đọc phần lẻ.
- Muốn số tiền hiển thị kiểu `1.100,00`: System Settings → Number Format.

## Báo cáo
- **Ton kho theo lo va han dung** (Stock → Report): tồn theo lô/kho, hạn dùng, số ngày còn lại, tình trạng (Đã hết hạn / Sắp hết hạn ≤90 ngày / Còn hạn); lọc công ty, mặt hàng, kho, hết hạn trong N ngày.

- **Doanh thu theo khach hang** (Accounts → Report): doanh thu, thuế, còn phải thu, tỷ trọng theo khách hàng; lọc kỳ, khách hàng, nhóm; có biểu đồ top 10; hóa đơn trả hàng tự trừ.

- **Doanh thu theo san pham** (Accounts → Report): số lượng, giá bán TB, doanh thu, số khách mua, tỷ trọng theo sản phẩm; lọc kỳ, sản phẩm, nhóm, khách hàng; biểu đồ top 10.

- **Cong no phai thu theo tuoi no** (Accounts → Report): công nợ theo khách hàng chia nhóm Chưa đến hạn / 1-30 / 31-60 / 61-90 / trên 90 ngày; tính theo ngày đến hạn hoặc ngày hóa đơn; xem chi tiết từng hóa đơn. Lấy từ Sales Invoice còn dư nợ (chưa gồm bút toán Journal/thanh toán chưa phân bổ — đối chiếu với báo cáo "Accounts Receivable" chuẩn của ERPNext).

- **Lai gop theo san pham** (Accounts → Report): doanh thu, giá vốn, lãi gộp, biên lãi gộp (%) theo sản phẩm, sắp theo lãi gộp; lọc kỳ, sản phẩm, nhóm, khách hàng. Giá vốn lấy từ giá vốn lúc xuất (incoming_rate) của dòng hóa đơn; nếu bằng 0 (xuất kho qua Delivery Note) thì dùng giá vốn hiện hành của mặt hàng và đánh dấu "Giá vốn ước tính". Hàng dịch vụ không tính giá vốn.

- **Cong no phai tra theo tuoi no** (Accounts → Report): công nợ phải trả theo nhà cung cấp, chia nhóm Chưa đến hạn / 1-30 / 31-60 / 61-90 / trên 90 ngày; tính theo ngày đến hạn hoặc ngày hóa đơn; xem chi tiết từng hóa đơn mua. Lấy từ Purchase Invoice còn dư nợ (chưa gồm thanh toán chưa phân bổ và Journal — đối chiếu với báo cáo "Accounts Payable" chuẩn).

- **Gia thanh san xuat** (Manufacturing → Report): giá thành thực tế theo thành phẩm (hoặc từng lệnh sản xuất) từ các Stock Entry loại Manufacture: chi phí NVL + chi phí khác, giá thành đơn vị, so với giá thành theo BOM (chênh lệch %). Lọc kỳ, thành phẩm.

- **Gia thanh theo cong thuc** (Manufacturing → Report): giá thành mỗi mẻ và mỗi đơn vị của từng Cosmetic Formula = nguyên liệu (tỷ lệ % × khối lượng mẻ × đơn giá) + hao hụt + bao bì + nhân công + chi phí chung. Đơn giá lấy từ giá vốn kho bình quân hoặc giá mua gần nhất; có chi tiết từng khoản và cảnh báo mặt hàng thiếu giá. Nhập bao bì (số lượng trên 1 đơn vị thành phẩm), nhân công/chi phí chung (mỗi mẻ) và hao hụt % ngay trên form Cosmetic Formula; nút "Tạo BOM" cũng đưa bao bì vào BOM.

## Bước tiếp theo
- Nút "Tạo BOM" đã có: công thức Approved + có sản phẩm → BOM (qty = tỷ lệ% × khối lượng mẻ)
- Mẫu in tiếng Việt đã có: Báo giá, Hóa đơn bán hàng, Phiếu sản xuất, Công thức mỹ phẩm, Phiếu nhập kho (Purchase Receipt), Phiếu xuất kho (Delivery Note), Phiếu kho (Stock Entry), Phiếu thu/chi (Payment Entry), Đơn đặt hàng bán (Sales Order), Đơn mua hàng (Purchase Order) — chọn trong Print, tên "... VN"
- Hóa đơn điện tử theo chuẩn VN (kết nối nhà cung cấp HĐĐT)
