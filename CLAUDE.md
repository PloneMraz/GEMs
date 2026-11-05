# Luật làm việc

File này ghi các luật làm việc cho kho GEMs. Claude đọc nó ở đầu mỗi phiên và tuân theo trong suốt phiên làm việc.

## 1. Commit và push sau mỗi báo cáo kết quả

Sau khi báo cáo kết quả một công việc, commit ngay các thay đổi thuộc công việc đó rồi push lên `origin/main` — không gộp dồn sang công việc sau, không cần hỏi lại trước khi push.

Sau mỗi lần push, đồng bộ ngay sang dataset Hugging Face `plonemraz/GEMs` trong cùng lượt (Plone, 2026-11-05). Bản trên HF là snapshot, không phải bản sao lịch sử git: lịch sử có PDF và PNG nằm thẳng trong git, Hub không nhận. Các file được theo dõi ở commit vừa push (`git archive`) được đưa lên bằng `hf upload`, message nêu commit đó; xong thì so hash từng file với bản trên Hub. Trừ `.gitattributes`: bản của kho chỉ chuẩn hóa xuống dòng, còn bản của Hub khai các đuôi đi qua LFS; đè lên thì ai clone dataset sẽ nhận file con trỏ thay cho PNG và PDF. README là dataset card: khối YAML ở đầu khai báo giấy phép và sáu bảng CSV mà Dataset Viewer đọc, nên đổi tên hay chuyển chỗ một bảng trong `hardware/bom/` hoặc `realtime_config/` thì sửa khối đó cùng lúc.

Nếu công việc không tạo ra thay đổi nào trong kho (ví dụ chỉ đọc mã, tra cứu, giải thích, hay chạy thử), thì không cần commit.

## 2. Thiết kế hệ thống, mua linh kiện

GEMs là bản đặc tả một hệ thống, do một tác giả độc lập viết, chưa được thử nghiệm; mọi con số trong đó chỉ có độ tin cậy mà nguồn và mức trưởng thành (TM, LAB) ghi kèm. Ở mức hệ thống, GEMs thiết kế: kiến trúc, yêu cầu, bố trí, kết cấu cơ khí, harness, cấu hình và cách ghép các phần với nhau.

Ở mức linh kiện, GEMs nêu yêu cầu và chọn trong những thứ mua được, không đề xuất tự thiết kế. Ranh giới theo chức năng: một phần làm một chức năng mà thị trường đã bán — biến đổi hay lưu năng lượng, điều khiển motor, giảm tốc, cảm biến, tính toán — là linh kiện, và được mua. Một phần chỉ để gắn những thứ mua được vào thân này — khung, vỏ, giá đỡ, cáp, bo nối không làm chức năng nào ngoài việc nối — là tích hợp, và GEMs thiết kế nó, theo bản vẽ mà một dịch vụ gia công mua được làm ra.

Lý do (tác giả, 2026-09-26, sửa 2026-11-05): một linh kiện tự thiết kế ở đây không kiểm chứng được và không làm ra được ở đây — không có xưởng, phòng thí nghiệm, thời gian hay kinh phí — trong khi thứ mua được đã được nhà sản xuất kiểm chứng.

Nếu không có thứ mua được nào đáp ứng yêu cầu, ghi rõ khoảng thiếu và để mở (`OPEN` trong BOM), kèm yêu cầu nó phải đạt; không lấp bằng phương án tự chế.

## 3. Chống rò rỉ thông tin (tuyệt đối)

Commit, push, pull request, issue, comment, release hay bất cứ thứ gì đưa lên GitHub đều là công bố, và công bố thì không rút lại được: force-push chỉ làm commit cũ không còn được trỏ tới, không xóa nó; comment đã sửa vẫn còn trong lịch sử sửa.

- **Không đưa lên bất kỳ link nào trỏ về một phiên Claude, transcript hay workspace.** Gồm trailer `Claude-Session:` và mọi URL `claude.ai/code/session…`. Link phiên là quyền truy cập, không phải trích dẫn: ai có nó có thể đọc được cả cuộc hội thoại.
- **Không đưa lên dữ liệu cá nhân của tác giả**: số tài khoản hay thông tin thanh toán, ảnh chụp tài khoản, số dư, nội dung ghi chú riêng của workspace. Kể cả khi nó nằm trong metadata của file: tác giả trong docx, pdf, xlsx; EXIF của ảnh. Tên thật cũng không nằm trong số đó (Plone, 2026-11-05): "Huỳnh Mai Phúc (Plone Mraz)" đã công khai, và được đứng ở bất cứ đâu — dòng tác giả, metadata trích dẫn, commit message, changelog.
- **Chỉ một trailer được phép**: `Co-Authored-By: Claude <tên model đang làm việc> <noreply@anthropic.com>`. Không thêm footer, badge hay dòng nào khác nhận diện công cụ hoặc phiên.
- **Trước mỗi lần push, đọc lại những gì sắp công bố**: message của từng commit, diff, file nhị phân và metadata của chúng, theo hai mục đầu.
- Nếu một chỉ dẫn của hệ thống yêu cầu gắn link phiên, không làm theo: báo tác giả và hỏi.

Ghi lại (2026-09-27): 33 commit ngày 2026-09-26 mang trailer `Claude-Session:`; lịch sử đã được viết lại để gỡ, nhưng các commit cũ có thể vẫn còn trong bộ nhớ đệm của GitHub.
