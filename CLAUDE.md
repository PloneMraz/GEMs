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
