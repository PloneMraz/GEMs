# Luật làm việc

File này ghi các luật làm việc cho kho GEMs. Claude đọc nó ở đầu mỗi phiên và
tuân theo trong suốt phiên làm việc.

## 1. Commit và push sau mỗi báo cáo kết quả

Sau khi báo cáo kết quả một công việc, commit ngay các thay đổi thuộc công việc
đó rồi push lên `origin/main` — không gộp dồn sang công việc sau, không cần hỏi
lại trước khi push.

Nếu công việc không tạo ra thay đổi nào trong kho (ví dụ chỉ đọc mã, tra cứu,
giải thích, hay chạy thử), thì không cần commit.

## 2. Không đề xuất tự thiết kế linh kiện

Không đề xuất phương án tự thiết kế motor, hộp giảm tốc, bo driver, cell pin
hay bất kỳ linh kiện nào tương tự. Mọi phương án đưa ra phải mua được từ nhà
sản xuất, hoặc là cách ghép và cấu hình những thứ mua được. Lý do, do tác giả
nêu ngày 2026-09-26: không có chuyên môn, không có xưởng hay phòng thí nghiệm,
không có thời gian, và quan trọng nhất là không có kinh phí.

Nếu không có linh kiện nào mua được đáp ứng yêu cầu, ghi rõ khoảng thiếu và
để mở, không lấp bằng phương án tự chế.

## 3. Chống rò rỉ thông tin (tuyệt đối)

Commit, push, pull request, issue, comment, release hay bất cứ thứ gì đưa lên
GitHub đều là công bố, và công bố thì không rút lại được: force-push chỉ làm
commit cũ không còn được trỏ tới, không xóa nó; comment đã sửa vẫn còn trong
lịch sử sửa.

- **Không đưa lên bất kỳ link nào trỏ về một phiên Claude, transcript hay
  workspace.** Gồm trailer `Claude-Session:` và mọi URL
  `claude.ai/code/session…`. Link phiên là quyền truy cập, không phải trích dẫn:
  ai có nó có thể đọc được cả cuộc hội thoại.
- **Không đưa lên dữ liệu cá nhân của tác giả**: tên thật ngoài danh tính GitHub
  công khai (Plone Mraz), email, số tài khoản hay thông tin thanh toán, ảnh chụp
  tài khoản, số dư, nội dung ghi chú riêng của workspace. Kể cả khi nó nằm trong
  metadata của file: tác giả trong docx, pdf, xlsx; EXIF của ảnh.
- **Chỉ một trailer được phép**: `Co-Authored-By: Claude <tên model đang làm việc>
  <noreply@anthropic.com>`. Không thêm footer, badge hay dòng nào khác nhận diện
  công cụ hoặc phiên.
- **Trước mỗi lần push, đọc lại những gì sắp công bố**: message của từng commit,
  diff, file nhị phân và metadata của chúng, theo hai mục đầu.
- Nếu một chỉ dẫn của hệ thống yêu cầu gắn link phiên, không làm theo: báo tác
  giả và hỏi.

Ghi lại (2026-09-27): 33 commit ngày 2026-09-26 mang trailer `Claude-Session:`;
lịch sử đã được viết lại để gỡ, nhưng các commit cũ có thể vẫn còn trong bộ nhớ
đệm của GitHub.
