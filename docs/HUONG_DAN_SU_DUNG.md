# Hướng dẫn thiết lập và dùng Omigos ERP

Dành cho lần đầu đưa vào dùng thật. Các bước dưới đây dựa trên những gì đã chạy thử trên site thử; phần giao diện ERPNext có thể đổi tên nhẹ giữa các bản.

## 1. Thiết lập ban đầu (một lần)

1. **Setup Wizard**: chọn ngôn ngữ **Vietnamese**, quốc gia Vietnam, tiền tệ **VND**, nhập tên công ty và năm tài chính. Ở bước hệ thống tài khoản, chọn mẫu phù hợp với kế toán của bạn (nếu có mẫu Việt Nam thì dùng; cần xác nhận với kế toán trước khi chọn vì khó đổi về sau).
2. **System Settings → Number Format**: chọn `#.###,##` để số hiển thị dạng `1.100,00`. Đặt **Float Precision** = 2 hoặc 3 tùy nhu cầu.
3. **Người dùng và vai trò** (Users): tạo từng người, gán vai trò.

| Vai trò | Dùng cho |
|---|---|
| Sales User / Sales Manager | Báo giá, đơn hàng, hóa đơn bán |
| Purchase User / Purchase Manager | Đơn mua, nhập hàng |
| Stock User / Stock Manager | Phiếu kho, tồn kho theo lô |
| Manufacturing User / Manufacturing Manager | Công thức, BOM, lệnh sản xuất |
| Accounts User / Accounts Manager | Hóa đơn, thu chi, công nợ |

4. **Kho (Warehouse)**: tạo các kho thực tế, ví dụ kho nguyên liệu, kho bao bì, kho thành phẩm, kho bán thành phẩm (WIP).
5. **Đơn vị tính (UOM)**: kiểm tra có `Kg`, `Gram`, `Lít`, `Cái`; thêm nếu thiếu.

### Thông tin công ty trên mẫu in

Đầu mỗi mẫu in tự lấy từ hồ sơ công ty: logo, tên, địa chỉ, MST, điện thoại, email, website. Điền ở:
- **Company**: Company Logo, Tax ID (mã số thuế), Phone No, Email, Website.
- **Address**: tạo địa chỉ trụ sở, trong mục Links thêm dòng `Company` = tên công ty, đánh dấu Preferred/Primary.

Trường nào để trống thì dòng đó không hiện.

## 2. Nhập dữ liệu nền

Thứ tự khuyến nghị, vì cái sau cần cái trước:

1. **Nhóm mặt hàng** (Item Group): Nguyên liệu, Bao bì, Bán thành phẩm, Thành phẩm.
2. **Mặt hàng** (Item). Với nguyên liệu, bao bì và thành phẩm cần theo dõi hạn dùng, bật **Has Batch No** và **Has Expiry Date**, đặt **Shelf Life In Days**. Có thể nhập hàng loạt bằng Data Import (Tools → Data Import).
3. **Nhà cung cấp** (Supplier) và **Khách hàng** (Customer), kèm mã số thuế trong trường Tax ID để mẫu hóa đơn in ra đúng.
4. **Tồn đầu kỳ**: dùng Stock Entry loại Material Receipt (hoặc Stock Reconciliation), nhập kèm số lô, hạn dùng và giá vốn. Giá vốn ở bước này quyết định giá thành về sau, nên nhập cẩn thận.
5. **Công nợ đầu kỳ**: nhập qua hóa đơn mở đầu hoặc Journal Entry theo hướng dẫn của kế toán.

## 3. Quy trình gia công mỹ phẩm

1. **Cosmetic Formula**: nhập công thức theo %, chia pha A/B/C/D; thêm bao bì (số lượng trên 1 đơn vị thành phẩm), nhân công và chi phí chung mỗi mẻ, hao hụt %. Đặt **Khối lượng mẻ** theo đơn vị tồn kho của thành phẩm.
2. Xem **Giá thành theo công thức** (Manufacturing → Report) để biết giá thành mỗi mẻ và mỗi đơn vị, dùng cho báo giá. Cột "Mặt hàng thiếu giá" phải bằng 0 thì số mới đáng tin.
3. Gửi **Báo giá** cho khách (mẫu in Bao Gia VN), khách chốt thì tạo **Đơn đặt hàng bán**.
4. Duyệt công thức (status Approved, tổng tỷ lệ đúng 100%), bấm **Tạo BOM**, kiểm tra BOM rồi **Submit**. Khi giá nguyên liệu đổi, bấm **Update Cost** trên BOM.
5. Mua nguyên liệu: **Đơn mua hàng** → **Phiếu nhập kho** (Purchase Receipt) → **Hóa đơn mua**. Nhập số lô và hạn dùng ở dòng hàng.
6. Sản xuất: **Work Order** từ BOM → chuyển nguyên liệu và hoàn thành bằng **Stock Entry** loại Manufacture (mẫu in Phiếu Kho VN, Phiếu Sản Xuất VN). Điền số lô và hạn dùng cho thành phẩm.
7. Giao hàng: **Delivery Note** (Phiếu xuất kho) → **Hóa đơn bán** (mẫu Hoa Don Ban Hang VN). Nhớ rằng đây là bản in nội bộ, chưa phải hóa đơn điện tử.
8. Thu tiền, chi tiền: **Payment Entry** (mẫu Phieu Thu Chi VN) gắn với hóa đơn để công nợ được trừ.

## 4. Báo cáo dùng hằng ngày

| Việc cần biết | Báo cáo |
|---|---|
| Lô nào sắp hết hạn, đã hết hạn | Ton kho theo lo va han dung (lọc "Hết hạn trong N ngày") |
| Khách nào còn nợ, quá hạn bao lâu | Cong no phai thu theo tuoi no |
| Còn nợ nhà cung cấp bao nhiêu | Cong no phai tra theo tuoi no |
| Bán được gì, cho ai | Doanh thu theo san pham, Doanh thu theo khach hang |
| Lời bao nhiêu | Lai gop theo san pham (cột "Giá vốn ước tính" cho biết dòng nào chưa có giá vốn thật) |
| Sản xuất thực tế đắt hơn BOM bao nhiêu | Gia thanh san xuat |

Mẹo: lưu bộ lọc hay dùng bằng nút **Save** ở thanh bộ lọc, và đặt báo cáo vào **Workspace** của từng phòng ban.

## 5. Vận hành

- **Worker nền phải chạy** (Docker compose đã có). Nếu tắt, số tồn kho và giá thành sẽ lệch sau các phiếu nhập lùi ngày.
- **Sao lưu mỗi ngày**: `docker/backup.sh`, kèm sao chép file sao lưu ra ngoài máy chủ.
- **Cập nhật**: sao lưu trước, rồi `git pull` và `docker compose up -d --build`.
- **Đổi mật khẩu** Administrator ngay sau khi đăng nhập lần đầu, và không dùng chung tài khoản.

## 6. Chưa có sẵn

- Hóa đơn điện tử hợp lệ theo quy định (cần kết nối nhà cung cấp hóa đơn điện tử).
- Báo cáo thuế và sổ sách theo chuẩn Việt Nam, cần làm cùng kế toán.
