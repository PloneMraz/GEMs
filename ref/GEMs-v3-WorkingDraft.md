# GEMs-v3 — Khung thiết kế & Bảng ánh xạ

*Bản làm việc (working draft). Trạng thái: **mọi cụm đã đóng, mọi mục treo đã đóng.** Bảy cụm: kiến trúc nền, liên kết, năng lượng, kết cấu–vận động, dấu vết thân, vỏ/da/morph, cảm biến.*

***Vị trí phiên bản:** GEMs-v3 kế tiếp GEMs-v2 trong cùng một chuỗi định danh. Khác biệt hạng: v2 là spec sci-fi (hệ tiêu chuẩn giả định Hậu-Kỳ-Dị); **v3 là bản grounded — mọi cơ chế phải qua hai tiêu chí nghiệm thu ở §0.** v3 không thay thế v2 mà là một phái sinh dưới trần vật lý hiện hành. RSIL-en-v1 không còn tham chiếu GEMs; quan hệ hai tài liệu nay là **hợp đồng nền tảng** — xem §6.*

*Tài liệu này đặc tả **dải năng lực và đánh đổi** của một thân vật lý. Nó KHÔNG đặt điểm vận hành. Mọi chỗ đánh dấu `⟦CTRL⟧` là biến thuộc phán định của controller, cố ý để trống.*

---

## 0. HAI TIÊU CHÍ NGHIỆM THU

Mọi spec trong bản này phải qua hai cửa:

**Tiêu chí 1 — trần vật lý.** Không đòi vật lý hư cấu. Được dùng công nghệ phòng lab chưa scale, đắt, chưa thương mại — miễn không vi phạm định luật đã biết. Mức nhắm: **tối đa khả thi, chạm hoặc vượt nhẹ tương lai gần.**

**Tiêu chí 2 — phục vụ trải nghiệm.** Spec phải đóng góp vào *thu thập trải nghiệm vật lý trọn vẹn như một cơ thể người, cộng năng lực vượt người có chọn lọc*. Cái ngả sang công nghiệp/chiến đấu/trinh sát thuần thì giảm về mức trải-nghiệm.

**Phân vai tuyệt đối:** phần cứng **cấp năng lực và khai báo đánh đổi**; controller **quyết định dùng thế nào**. Đạo đức, thời lượng, chế độ vận hành, mức rủi ro chấp nhận — tất cả thuộc controller. Không spec nào bị cắt ở tầng phần cứng vì lý do đạo đức.

### Ký hiệu

| Ký hiệu | Nghĩa |
|---|---|
| **TM** | Đã thương mại hóa |
| **LAB** | Có trong phòng thí nghiệm, chưa scale |
| **HẠ** | Giữ mục tiêu, hạ mức so với bản gốc |
| **BỎ** | Loại bỏ (vi phạm vật lý, hoặc không còn cần) |
| `⟦CTRL⟧` | Biến thuộc phán định controller — cố ý để trống |
| `⟦IMPL⟧` | Hằng số chưa dẫn xuất được, quyết ở khâu triển khai |

---

## 1. TRỤ BẤT BIẾN

### Trụ 1 — GEMs là thiết bị đầu cuối vật lý

**Phát biểu (bản đã tinh chỉnh):** Trí tuệ vận hành **không cư trú toàn bộ trên thân**. Controller phân tán **hai cư trú**:

- **Phần-tại-thân** — vòng phản xạ, giữ thăng bằng, xử lý và trích đặc trưng tín hiệu cảm biến, độ trễ thấp.
- **Phần-tại-hệ-ngoài** — ký ức, mô hình thế giới, kho kinh nghiệm, tích hợp dài hạn.

**Một trí tuệ, hai chỗ ngồi.** Không phải hai tác nhân.

**Liên kết tải dữ liệu đã xử lý, KHÔNG tải dữ liệu thô.**

Hệ quả kéo theo:
- (a) Trạm điều khiển trong bán kính **~vài km**, liên kết vô tuyến trực tiếp.
- (b) Uplink là cơ quan sống còn; bắt buộc có lõi cục bộ khi mất link.
- (c) Thân thay thế được. *Lưu ý đánh đổi:* càng đẩy compute về thân, càng nhiều trạng thái mất khi mất thân. Núm compute thân/ngoài mặc định **ở khoảng giữa**; bài toán mất mát dữ liệu thuộc `⟦CTRL⟧`.
- (d) Cho phép nhiều thân trên một hệ điều khiển.

---

## 2. KHUNG MỤC TIÊU ỨNG DỤNG

**Mục tiêu chủ đạo:** thân thể đa dụng cho một cá nhân điều khiển, hoạt động trong **môi trường tương tác xã hội bình thường**, nhằm **thu thập trải nghiệm vật lý**.

**Định nghĩa "giống người tối đa":** giống về **băng thông giác quan**, không phải về hình thức. Thân thu được mọi loại thông tin vật lý mà một cơ thể người thu được, cộng quyền biến hình để có trải nghiệm con người không có.

| Nhóm | Trạng thái | Mức |
|---|---|---|
| **1 — Cảm biến / thu thập trải nghiệm** | **GIỮ REQ** — trục chính | Ngang hoặc trên người. Chỉ cắt phần cực đoan trinh sát. |
| **2 — Thao tác kỹ thuật** | Giảm nhẹ | Sinh hoạt + tinh xảo vừa. Bỏ lực công nghiệp. |
| **3 — Môi trường khắc nghiệt** | **HẠ MẠNH** | Chỉ cứu hộ dân sự: lửa đám cháy nhà, lặn/bơi độ sâu thường. Bỏ chân không, bức xạ, đáy biển sâu, lò luyện kim. |
| **4 — Tương tác / đồng hành** | **LÕI** | Tiếp xúc người an toàn, hiện diện xã hội. |
| **5 — Độ bền / phòng vệ** | Trung bình, thống nhất | Một mức bền vật liệu chịu **mọi va chạm vật lý đời thường**: đấm, dao đâm, xe va, đạn súng ngắn, va đập luyện tập. |

**Ranh giới cắt của Nhóm 1:** giữ mọi thứ làm giàu trải nghiệm vật lý trực tiếp. Giảm phần cực đoan mang tính do thám xuyên vật cản. **Ngoại lệ đã chốt:** RF/Wi-Fi sensing **giữ nguyên năng lực ở tầng phần cứng** — việc dùng vào đâu thuộc `⟦CTRL⟧`.

---

## 3. BẢNG ÁNH XẠ

### 3.1 Kiến trúc nền

| Spec gốc | Cơ chế gốc | Phán định | Thay thế thực |
|---|---|---|---|
| Đầu cuối, trí tuệ ở xa | — | Giữ (Trụ 1) | Trạm ~vài km + vô tuyến trực tiếp. **TM** |
| Thân thay thế được | đồng bộ tức thời | Giữ mục tiêu | Đồng bộ liên tục, có độ trễ thật. **TM** |
| Fully solid-state | — | Giữ | Robot điện toàn phần, không thủy lực. **TM** |
| Hình người ~1750mm | — | Giữ | Có tiền lệ humanoid thật cùng cỡ. **TM** |

### 3.2 Kết cấu, khối lượng, độ bền *(bảng ánh xạ; cụm đóng ở §5)*

| Spec gốc | Cơ chế gốc | Phán định | Thay thế thực |
|---|---|---|---|
| 118kg "trọng lượng biểu kiến" | Quantum Mass Cancellation | **BỎ** — vi phạm vật lý | Khối lượng thật. Không có triệt khối lượng. **BỎ** |
| Khung siêu cứng | Proto-Adamantium | HẠ | Khung hợp kim + composite. **TM** |
| Triệt tiêu động năng | kinetic nullification | **BỎ** — vi phạm bảo toàn | Hấp thụ–phân tán thường. **BỎ** |
| Ổn định quán tính cảm biến | — | Giữ mục tiêu | Chống rung cơ-điện, bù IMU. **TM** |
| Khớp đệm 50µm | MagLev | HẠ | Ổ bi chính xác + harmonic/cycloidal reducer. **TM** |
| **Nhóm 5 — bền thống nhất** | — | Giữ, định lượng | Giáp đa tầng: UHMWPE (đạn súng ngắn, cỡ NIJ IIIA) + lớp gốm/cứng riêng (chống đâm). **TM** |

> **Ghi chú Nhóm 5:** đạn và dao phá theo hai cơ chế khác nhau — mũi dao xuyên qua sợi mềm mà đạn thì không. Một thân chịu *cả cụm* đòi giáp đa tầng. Chặn đạn súng trường (NIJ III/IV) khả thi nhưng đội khối lượng đáng kể; **mức neo đề xuất: đạn súng ngắn + dao + va đập đời thường.** Mức cao hơn: `⟦CTRL⟧`.

### 3.3 Vỏ / da / morph

| Spec gốc | Cơ chế gốc | Phán định | Thay thế thực |
|---|---|---|---|
| Vỏ độ cứng lập trình tức thời | Programmable **Pico**-Matter | **HẠ** (không bỏ) | **Nano-matter lập trình** — biên độ độ cứng giới hạn (mềm↔cứng vừa), tốc độ chục–trăm ms. Cơ chế thật: electro/magnetorheological, jamming, polymer nhớ hình. **LAB** |
| Chịu −270…7500°C | — | **HẠ MẠNH** | Lớp chịu lửa đám cháy dân sự, thời gian giới hạn. **TM/LAB** |
| Biến hình bề mặt (màu/kết cấu) | Pico | HẠ → add-on | Đổi màu: e-skin/điện sắc. Đổi kết cấu: hạn chế. **LAB một phần** |
| Tự vá tức thời | Pico | Giữ mục tiêu, hạ tốc độ | Polymer tự lành graphene-PEDOT:PSS — tự lành trong **giây**, co giãn ~**600%**, cảm được áp suất/nhiệt/pH. **LAB** *(số tra được, công bố 2025)* |
| Tự khử trùng + điều nhiệt bề mặt | Pico | Giữ | Lớp phủ kháng khuẩn + vi điều nhiệt. **TM/LAB** |
| Morph bảo-toàn-khối | Pico | **HẠ MẠNH** | Cơ cấu gập/khớp định sẵn. Vật chất rắn không tái sắp xếp tức thời. **HẠ** |
| Morph tăng/giảm khối | *bản gốc cũng chưa giải* | **BỎ** | Không khả thi. **BỎ** |

> **Phân tách bắt buộc:** vật liệu tự-lành-cảm-giác và vật liệu chịu-lực-kết-cấu là **hai lớp khác nhau**. Không một vật liệu thật nào làm cả hai như Pico-matter giả định.

### 3.4 Vận động & thao tác *(bảng ánh xạ; cụm đóng ở §5)*

| Spec gốc | Cơ chế gốc | Phán định | Thay thế thực |
|---|---|---|---|
| 80 kW/kg, 0.004ms, nâng 15 tấn | Nano-Myomer | **HẠ MẠNH** | Actuator thật: **3–5 kW/kg**, ~30–36 Nm/kg, hiệu suất 75–82%. Phản ứng cỡ ms. **TM** *(số tra được)* |
| Bàn tay đa hình | Pico | Giữ mục tiêu, hạ cơ chế | Nhiều bậc tự do + đầu ngón đổi độ bám. **TM/LAB** |
| Cổng dữ liệu lòng bàn tay | NFC | Giữ | NFC/USB-C. **TM** |
| Chân giảm chấn | MagLev | HẠ | Đệm cơ học + actuator hấp thụ. **TM** |
| Bám tường/trần tải lớn | Van der Waals nhân tạo | HẠ | Gecko-adhesive thật, tải vừa. **LAB** |
| Con quay 3 trục mắt cá | — | Giữ | IMU + điều khiển ZMP/bánh đà. **TM** |

> **Khoảng cách actuator:** 3–5 kW/kg so với 80 kW/kg của bản gốc là **cách 16–26 lần**. Hệ quả: thân mạnh ngang người khỏe tới vài lần người, không phải nâng-15-tấn. Phù hợp mục tiêu đa dụng đời thường.

### 3.5 Liên kết *(đã đóng)*

| Spec gốc | Cơ chế gốc | Phán định | Thay thế thực |
|---|---|---|---|
| Uplink độ trễ ≈0, băng thông vô hạn | Quantum Entanglement | **BỎ** — rối lượng tử **không** truyền tin nhanh hơn ánh sáng (vật lý cấm tuyệt đối) | mmWave/60GHz (WiGig): tới **~8 Gbps**, độ trễ PHY **~1ms** ở tầm gần lý tưởng; tầm vài km cần anten định hướng + beam-tracking. **TM/LAB** |
| Đồng bộ liên tục ≤0.01s | — | Giữ mục tiêu, nới ngưỡng | Độ trễ thật. Người điều khiển **thích nghi được dưới ~170ms**, **quản lý được tới ~300ms**. **TM** *(số tra được)* |
| Dự phòng LEO / 6G / VLF | — | Giữ | Vệ tinh LEO, 5G/6G, VLF dưới nước. **TM** |
| Firewall chống xâm nhập | Observer-Effect | **BỎ cơ chế** | Mã hóa đầu-cuối + xác thực. **TM** |
| Bộ phận tách rời vẫn nhận lệnh | rối lượng tử | **BỎ** | Mỗi bộ phận cần link vô tuyến riêng. **HẠ** |

> **Đây là cổng quyết định kiến trúc.** 8 Gbps đủ tải nhiều luồng cảm biến độ phân giải cao, nhưng **không** tải nổi toàn bộ cảm biến thô full-rate đồng thời. Chính ràng buộc này đẻ ra kiến trúc hai cư trú: thân trích đặc trưng/nén trước, link tải cái đã xử lý. Dữ liệu đã trích đặc trưng nhỏ hơn thô hàng chục–trăm lần → băng thông thừa.

### 3.6 Tính toán & sống còn

| Spec gốc | Cơ chế gốc | Phán định | Thay thế thực |
|---|---|---|---|
| CPU lượng tử trên thân | QSC-9000 | **BỎ** | Compute biên: phản xạ + nén/trích đặc trưng + giữ vận động khi mất link. **TM** |
| Lưu trữ khổng lồ | Holographic Crystal | **BỎ** | SSD + đệm. Dữ liệu chính ở hệ ngoài. **TM** |
| Lõi phản xạ khi mất link | Protocol-ZERO | Giữ — **bắt buộc** | Phần-tại-thân của controller. **TM** |
| Né tốc độ cao | Neural-Flash + micro-warp | **BỎ micro-warp** | Né bằng vận động thường + dự báo quỹ đạo. **HẠ** |
| Hủy dữ liệu khi mất thân | Memory Wipe laser | Giữ mục tiêu, hạ cơ chế | Mã hóa + xóa an toàn. **TM** |
| Kill-switch chống tự sao chép | Pico self-replication | **BỎ — không cần** | Không có nano tự sao chép. **BỎ** |

### 3.7 Cảm biến *(trục trải nghiệm — GIỮ REQ)*

| Spec gốc | Phán định | Thay thế thực |
|---|---|---|
| Thị giác zoom 100x / nhiệt / terahertz | Giữ phần người+; hạ ứng dụng xuyên tường | Camera đa phổ, zoom quang, nhiệt IR. **TM/LAB** |
| **RF-Spatial** | **GIỮ** (đã chốt) | Wi-Fi/mmWave CSI sensing. Tầm & độ phân giải khiêm tốn hơn bản gốc. **LAB** |
| Dự báo quỹ đạo ~1.5s | Giữ | Computer vision + human trajectory prediction. **TM** |
| Khứu giác ppb | Giữ mục tiêu, hạ độ nhạy | E-nose / phổ kế vi mô. **TM/LAB** |
| Vị giác phân tử | Giữ mục tiêu, hạ | Lab-on-chip vi lưu. **LAB** |
| Thính giác xuyên tường | Giữ phần người+; hạ xuyên tường | Mic array siêu nhạy + định hướng. **TM** |
| Giọng + siêu/hạ âm | Giữ | Tổng hợp giọng + siêu âm. **TM** |
| RF đa dải | Giữ | SDR. **TM** |
| Xúc giác 1000× da người | **HẠ → đọc theo trục** *(đã chốt lại; xem §9.1)* | Mật độ **ngang da người** ở vùng tinh (bàn tay, mặt), thưa dần ở thân; **vượt người 20–100× ở băng thông thời gian**, và vượt ở ngưỡng nhạy, dải động, số đại lượng đo đồng thời. **LAB** |
| Nhiệt ±0.0001°C | HẠ | Quá nhạy; hạ về mức thật. **LAB** |
| Đáp ứng sinh học (đồng tử, biểu cảm) | Giữ | Actuator mặt vi mô + vi lưu. **TM/LAB** |
| **Cardiac co-regulation** | Giữ — **ADD-ON** *(đã chốt)* | Rung + ấm + nhịp. Module tùy chọn, không luôn-bật. **TM** |
| **Cảm biến bản thể (MỚI)** | **THÊM — bắt buộc** | Encoder khớp + IMU + cảm biến lực/mô-men, đủ dày để phân biệt "tôi vừa cử động" với "ai đó chạm tôi". **TM** |

### 3.8 Nhiều unit & bảo trì

| Spec gốc | Phán định | Thay thế thực |
|---|---|---|
| 1 Active + N Standby | Giữ mục tiêu | Khả thi như đội robot. **TM** |
| Standby ngủ đông tầng địa chất sâu | **BỎ** | Không nạp/bảo trì được. Standby ở trạm/kho. **HẠ** |
| Hot-swap unit | Giữ | **TM** |
| Auto-replenishment | HẠ | Sản xuất bổ sung thường. **HẠ** |
| Đa unit phối hợp | Giữ | Multi-robot coordination. **TM** |

---

## 4. CỤM NĂNG LƯỢNG *(ĐÃ ĐÓNG)*

### 4.1 Nguồn chính — hai cấu hình khai báo

Bản gốc dùng nguồn Lỗ Trắng vi mô (UDPA) — công suất gần vô hạn, vô thời hạn. **BỎ hoàn toàn.** Thay bằng pin thể rắn, hai tầng:

| Cấu hình | Mật độ | Đánh đổi |
|---|---|---|
| **Mức vững** | **~400–500 Wh/kg** | Tuổi thọ chu kỳ tốt, an toàn nhiệt tốt (hợp thân tiếp xúc người). **Khuyến nghị làm thiết kế-đích.** |
| **Mức trần** | **~700–1100 Wh/kg** (Li-S thể rắn) | Thời lượng cực đại. **Nợ tuổi thọ: hiện ~100 chu kỳ sạc** — pin thành vật tiêu hao, thay thường xuyên. |

*Số tra được để định vị ba tầng độ chín:*
- Li-ion thương mại hôm nay: ~250–260 Wh/kg (mức cell).
- Bán rắn **đã lên xe đang bán**: ~300–350 Wh/kg (pack 150 kWh, tầm ~930km).
- Kỳ vọng pack solid-state: 300–500+ Wh/kg; đã có demo cell solid-state ở **600 Wh/kg**.
- Li-S: lý thuyết ~2600 Wh/kg; lab đạt **743 Wh/kg** (tải cathode 6 mg/cm²) tới **1100 Wh/kg** (18 mg/cm²); cell kỷ lục **695 Wh/kg** nhưng **dưới 100 chu kỳ** (so với >1000 của Li-ion).

**Hot-swap <2 phút** — pin là module đổi được.

**Siêu tụ xung đỉnh: OPTION.** Lắp khi nhiệm vụ cần vận động mạnh đột ngột (đỡ, nhảy, phản xạ nhanh); bỏ khi ưu tiên nhẹ. Vai trò: xả nhanh cho xung mili-giây, tránh sụt áp pin. Không mặc định cứng.

### 4.2 Sáu đòn quản lý năng lượng

| # | Đòn | Cơ chế | Hiệu quả |
|---|---|---|---|
| 1 | **Gating động theo trạng thái** | Bật/tắt theo nhu cầu: actuator chỉ gồng khi cần; cảm biến full-rate chỉ ở kênh đang chú ý; compute biên hạ xung khi tĩnh | **Mạnh nhất.** Tiêu thụ dao động tỉ lệ ~1:8 giữa nghỉ và tải đỉnh |
| 2 | **Thu hồi khi giảm tốc** | Nạp ngược khi hạ chi/giảm tốc | tới **~30%** *(số tra được)* |
| 3 | **Phân tầng nguồn** | Pin chính (vận động) + siêu tụ (xung đỉnh) + nạp nền | Mỗi tầng làm đúng việc nó giỏi |
| 4 | **Khóa cơ khí khớp** | Chốt khớp khi giữ tư thế lâu, actuator buông | Xóa khoản "điện đổ vào việc đứng yên" |
| 5 | **Điểm vận hành actuator** | Đàn hồi nối tiếp (series-elastic) trữ–nhả năng lượng bước đi | Giảm phí ở chế độ giữ tĩnh |
| 6 | **Ngủ phân tầng + canh-gác-ủy-nhiệm** | Xem §4.3 | Đòn duy nhất tấn công **tổng năng lượng theo lịch** |

### 4.3 Đòn 6 — ngủ phân tầng

**Cơ chế:** thân hạ về công suất sàn theo chu kỳ. Tắt actuator (thân tựa vào điểm đỡ cơ học), tắt cảm biến full-rate, tắt compute nặng. Giữ mạch cảnh giác công suất cực thấp + wake-on-event.

**Điểm then chốt — canh-gác-ủy-nhiệm:** khi thân ngủ, **phần-tại-hệ-ngoài của controller vẫn thức**, vẫn quan sát qua nguồn khác (thiết bị môi trường, unit khác, mạng tín hiệu). Thân ngủ **mà hệ không mù.** Đây là lợi thế kiến trúc sinh học không có, và nó chỉ khả thi *nhờ* Trụ 1 (trí tuệ phân tán).

**Điều kiện & hệ quả — khai báo đầy đủ:**

| # | Ràng buộc | Nội dung |
|---|---|---|
| 1 | **Đánh đổi độ-sâu ↔ độ-trễ-dậy** | Ngủ càng sâu, dậy càng lâu: từ ~chục ms (ngủ nông) tới ~giây (ngủ sâu). Đề xuất nhiều mức ngủ; chọn mức nào là `⟦CTRL⟧` |
| 2 | **Tư thế ngủ là ràng buộc vật lý** | Tắt actuator hoàn toàn đòi một **cấu trúc thụ động gánh trọng lực**. Ngủ sâu cần điểm tựa/nằm — không ngủ sâu được giữa lúc đứng trơ |
| 3 | **Sàn > 0** | Mạch cảnh giác vẫn rút điện. Ngủ rất dài nhưng **không vĩnh viễn**. Con số cụ thể: `⟦IMPL⟧` — phụ thuộc spec mạch cảnh giác |
| 4 | **Hạ tích phân, không hạ đỉnh** | Đòn này cắt *tổng năng lượng dùng trong một chu kỳ lịch*, không cắt công suất tức thời |

### 4.4 Bốn mức trạng thái năng lượng

| Mức | Nguồn | Actuator | Cảm biến | Đặc tính |
|---|---|---|---|---|
| **1. Hoạt động** | Pin | Chạy | Full theo gating | Sáu đòn áp dụng |
| **2. Ngủ tự do** | Pin (sàn) | Tắt, thân tựa | Chỉ mạch cảnh giác | Tiết kiệm tối đa; hệ ngoài canh |
| **3. Nghỉ-sạc** | **Nguồn ngoài** | Đỡ nhẹ | **Giữ cảm biến không gian** | **Nghỉ mà không mù, sạc mà không chết** |
| **4. Ngủ sâu trên dock** | Nguồn ngoài | Tắt | Tối thiểu | Nạp đầy nhanh + nghỉ tối đa; hợp standby |

> **Mức 3 là trạng thái đặc trưng của kiến trúc này.** Khi đang cắm nguồn ngoài, ràng buộc "phải tắt actuator/cảm biến để tiết kiệm pin" **biến mất** — không tiêu vào pin nữa. Thân phục hồi năng lượng *trong khi vẫn duy trì hiện diện quan sát*. Sinh vật không làm được điều này.
>
> *Lưu ý:* kể cả khi điện "miễn phí", vẫn nên để dock gánh phần lớn trọng lực — không vì điện, mà vì **nhiệt** (actuator gồng lâu thì nóng) và **hao mòn cơ khí**.

### 4.5 Dock nghỉ-sạc

| Dạng | Vai trò | Cơ chế gánh trọng lực | Ưu / nhược |
|---|---|---|---|
| **Ghế dựa / sofa** *(mặc định)* | Unit active nghỉ-sạc | Đỡ từ dưới, chịu nén | Trọng tâm thấp, tư thế tự nhiên, thuận cho quan sát, dậy nhanh |
| **Móc treo chịu lực** | Unit standby cất kho | Treo từ trên, chịu kéo | Chiếm ít diện tích sàn, xếp được nhiều unit; điểm tiếp xúc sạc nhỏ hơn, tư thế kém thuận cho quan sát |

**Cả hai phương thức sạc:**
- **Không dây** — nạp chậm/duy trì trong quãng nghỉ dài. Tiện, không mòn cổng. *Hạn chế: hiệu suất thấp hơn dây, sinh nhiệt ở mặt tiếp xúc khi công suất cao.*
- **Tiếp điểm có dây** — nạp nhanh khi cần xoay vòng gấp.

Phương thức dùng khi nào: `⟦CTRL⟧`.

### 4.6 Nguồn môi trường — ADD-ON

**Pin mặt trời tích hợp:** bức xạ mặt trời đỉnh ~1000 W/m²; diện tích hứng hiệu dụng của một thân ~1.75m là ~0.5–0.7 m²; hiệu suất pin tốt ~20–25% → **công suất thu tối đa ~100–175 W** *(ước lượng từ các con số trên)*.

Đối chiếu: một humanoid vận động tiêu **hàng trăm tới hơn 1000 W**. → Pin mặt trời **nới thời lượng, không nuôi thân đang hoạt động.** Không tính vào ngân sách vận hành; chỉ tính vào kéo dài thời gian chờ và nạp khi nghỉ.

### 4.7 Ràng buộc cứng — khai báo thẳng

**Không cấu hình nào cho năng lượng vô hạn ở chế độ tự do.** Đây là vật lý mật độ pin, không lách được — chỉ nới bằng sáu đòn + hạ tầng sạc.

"Vô hạn" chỉ đạt ở **Mức 3/4**, khi cắm nguồn ngoài — lúc đó trần là nguồn ngoài, không phải pin.

Đây là thay thế trung thực cho UDPA: **không phải một nguồn vô tận, mà một ngân sách hữu hạn cộng một hạ tầng sạc khiến nó đủ dùng.**

**Thời lượng hoạt động: `⟦CTRL⟧`.** Không đặt con số trong tài liệu này. Nhà thiết kế cấp dải khả năng và đánh đổi; controller chọn điểm vận hành theo nhiệm vụ (pin lớn cho chuyến dài, pin nhẹ cho việc ngắn, ngủ nhiều hay ít tùy ngữ cảnh).

---

### 4.8 Công suất sàn và trần thời gian ngủ *(R-6 — ĐÃ ĐÓNG)*

§4.3 ràng buộc 3 để trống con số: *"Mạch cảnh giác vẫn rút điện. Ngủ rất dài nhưng không vĩnh viễn. Con số cụ thể: `⟦IMPL⟧`."* Nay đóng được — và kết luận ngược với cái ràng buộc ấy ngụ ý.

**Thành phần của sàn:**

| Thành phần | Công suất | Ghi chú |
|---|---|---|
| Wake-up receiver sub-GHz | **3–30 µW** | *(số tra được)* — các thiết kế công bố từ 305 nW đến ~6 µW; loại dựa trên Wi-Fi thì ~30 mW |
| Giữ RAM + đồng hồ đơn điệu của neo tin cậy (§7.2) | ~10–50 µW | `⟦IMPL⟧` |
| Đường phát dấu vết C5 (§7.5) | **< 1 mW** | §7.5 |
| T1 Wi-Fi sensing, chế độ thụ động | **~18 µW** | *(số tra được)* |
| T1 CSI đầy đủ, chu-kỳ-hóa | **~50–200 mW** | `⟦IMPL⟧` — số hạng đắt nhất |

**Nhưng mạch cảnh giác không phải số hạng chi phối.** Pin tự phóng điện **1–3%/tháng** *(số tra được; chuẩn ô tô đòi dưới 2%/tháng, thể rắn về lý thuyết thấp hơn nhưng chưa chứng)*. Trên một pack 4 kWh:

| Tự phóng điện | Công suất tương đương |
|---|---|
| 1%/tháng | **56 mW** |
| 2%/tháng | **111 mW** |
| 3%/tháng | **167 mW** |

Mạch cảnh giác ở mức ngủ sâu tốn cỡ **chục µW** — **nhỏ hơn tự phóng điện khoảng ba bậc độ lớn.**

**Thời gian ngủ** (pack 4 kWh, tự phóng điện 2%/tháng, xấp xỉ tuyến tính):

| Chế độ | Sàn tổng | Thời gian |
|---|---|---|
| Ngủ sâu — chỉ wake-up receiver + giữ RAM | ~112 mW *(99% là tự phóng điện)* | **~4 năm** |
| Ngủ + T1 thụ động | ~130 mW | ~3.5 năm |
| Ngủ + T1 CSI đầy đủ | ~310 mW | **~1.5 năm** |

> **Hai hệ quả thiết kế, và cái thứ nhất tiết kiệm công vô ích.**
>
> **(1)** Tối ưu mạch cảnh giác xuống dưới ~10 mW là **công bỏ phí** — nó biến mất dưới tự phóng điện. Chỗ duy nhất đáng tối ưu là **T1 CSI**, vì chỉ nó mới cùng bậc với hóa học pin.
>
> **(2)** §4.3 ràng buộc 3 phát biểu đúng kết luận nhưng sai nguyên nhân. Cái chặn thời gian ngủ **không phải mạch cảnh giác — mà là hóa học của pin.** Một thân ngủ sâu hết pin sau vài năm kể cả khi mạch cảnh giác tiêu thụ bằng không.
>
> Ràng buộc này biến mất ở Mức 3 và 4 (§4.4) vì có nguồn ngoài — dock vừa gánh trọng lực vừa bù tự phóng điện.

**Còn `⟦IMPL⟧`:** con số chính xác theo hóa học pin cụ thể. **Đã xác định:** bậc độ lớn và *số hạng nào chi phối* — đủ để tính thời gian ngủ, vốn là điều R-6 cần.

---

## 5. CỤM KẾT CẤU & VẬN ĐỘNG *(ĐÃ ĐÓNG)*

*Cụm này đóng R-1 và R-2 cùng một lượt. Chúng không đóng riêng được: khối lượng, actuator và pin nằm trên một vòng ghép kín, và cắt vòng ở bất cứ đâu cũng làm hai đầu còn lại mất nghĩa.*

> **Hệ quả ngược lên §4.** Cụm năng lượng đã đóng về *cơ chế* từ trước, nhưng mọi con số công suất trong nó treo cho tới khi có khối lượng — §4.6 đối chiếu pin mặt trời với "hàng trăm tới hơn 1000 W" mà chưa có thân nào sinh ra con số ấy. §5.3 dưới đây trả cho §4.7 một trần thời lượng mà §4.7 chưa có.

### 5.1 Vòng ghép khối lượng — phát biểu hình thức

Khối lượng thân chia làm hai loại khác hạng:

- **Theo tỉ lệ** — kết cấu, actuator, pin. Càng nặng càng cần nhiều, vì chúng tồn tại để *gánh và chuyển động chính khối lượng đó*.
- **Không theo tỉ lệ** — giáp, compute, cảm biến, bàn tay, da, dây. Chúng được đặt lên thân từ ngoài; kích cỡ do nhiệm vụ quyết, không do khối lượng thân quyết.

Gọi `m` là tổng khối lượng, `m_ngoài` là phần không theo tỉ lệ:

```
m  =  f_kc·m  +  f_ac·m  +  f_pin·m  +  m_ngoài

     f_pin = p·t / e
     p = công suất riêng khi vận động (W/kg)
     t = thời lượng tự do yêu cầu (giờ)
     e = mật độ năng lượng pin (Wh/kg)
```

Giải ra:

```
m  =  m_ngoài / (1 − Σf)        với  Σf = f_kc + f_ac + p·t/e
γ  =  1 / (1 − Σf)              — hệ số nở
```

**Điều kiện hội tụ: `Σf < 1`.** Đây là ràng buộc trung tâm của cả cụm, và nó là một phát biểu *cấu trúc*, không phải một điểm thiết kế: nếu ba phần theo tỉ lệ cộng lại chiếm trọn thân thì không còn chỗ cho giáp, cảm biến hay bàn tay — **không khối lượng nào thỏa mãn được, ở bất cứ giá nào.** Thiết kế khi đó không "nặng quá"; nó *không tồn tại*.

`γ` đọc thẳng là **giá khối lượng của mỗi kg chức năng**: thêm 1 kg giáp không tốn 1 kg, nó tốn `γ` kg thân.

### 5.2 Bốn hệ số — dải khai báo

| Hệ số | Dải | Trạng thái |
|---|---|---|
| `f_kc` — kết cấu | ~0.25–0.35 | `⟦IMPL⟧` — tùy vật liệu và hệ số an toàn |
| `f_ac` — actuator | ~0.25–0.35 | `⟦IMPL⟧` — tùy số bậc tự do và tỉ số truyền |
| `p` — công suất riêng | **~10–25 W/kg** khi vận động | *(số tra được)* — humanoid thương mại tiêu **300–1500 W** khi đi; Optimus Gen 2 mang ~2.3 kWh cho ~2h vận động ⇒ ~1.1 kW liên tục. Quy về thân cỡ 100–150 kg ra dải này; thân có giáp nằm ở nửa trên |
| `e` — mật độ pin | **450** (mức vững) / **900** (mức trần) Wh/kg | §4.1, đã chốt |

Hai hệ số đầu để `⟦IMPL⟧` vì chúng phụ thuộc lựa chọn vật liệu chưa làm. **Nhưng dải của chúng đủ hẹp để mọi kết luận dưới đây không đổi dấu** — đó là lý do cụm đóng được mà không cần chốt vật liệu trước.

### 5.3 Trần thời lượng — một ràng buộc cứng mới

Đặt `Σf = 1` rồi giải ngược ra `t`:

```
t_max  =  (1 − f_kc − f_ac) · e / p
```

Với `f_kc + f_ac = 0.60`:

| | `p`=10 | `p`=15 | `p`=20 | `p`=25 W/kg |
|---|---|---|---|---|
| **e = 450** Wh/kg | 18.0 h | 12.0 h | **9.0 h** | 7.2 h |
| **e = 900** Wh/kg | 36.0 h | 24.0 h | **18.0 h** | 14.4 h |

Và `γ` nở rất nhanh khi tới gần trần (`e`=450, `f_kc+f_ac`=0.60):

| `p` \ `t` | 2h | 4h | 6h | 8h | 10h |
|---|---|---|---|---|---|
| 10 W/kg | 2.8 | 3.2 | 3.7 | 4.5 | 5.6 |
| 15 W/kg | 3.0 | 3.7 | 5.0 | 7.5 | 15.0 |
| **20 W/kg** | 3.2 | 4.5 | 7.5 | **22.5** | *phân kỳ* |
| 25 W/kg | 3.5 | 5.6 | 15.0 | *phân kỳ* | *phân kỳ* |

> **Đọc bảng này cho đúng.** Nó **không** nói "thân chạy được 9 giờ". Nó nói: ở `p`=20 W/kg và pin mức vững, **không tồn tại** một thân tự do quá 9 giờ — và từ khoảng 6 giờ trở đi cái giá đã dốc tới mức vô nghĩa (γ=7.5 nghĩa là mỗi kg giáp tốn 7.5 kg thân).
>
> §4.7 viết *"Thời lượng hoạt động: `⟦CTRL⟧`. Không đặt con số trong tài liệu này."* Điều đó vẫn đúng — controller vẫn chọn điểm vận hành. Cái §5.3 thêm vào là **trần mà controller không chọn vượt được**, vì bên kia trần không phải một thiết kế đắt, mà là không có thiết kế nào.

### 5.4 Giáp Nhóm 5 — mật độ diện tích

§3.2 đã chốt hướng (đa tầng: UHMWPE + lớp chống đâm riêng) nhưng chưa định lượng. Số tra được:

| Lớp | Mật độ diện tích | Ghi chú |
|---|---|---|
| Đạn súng ngắn — NIJ IIIA (UHMWPE/aramid mềm) | **3.8–5.6 kg/m²** | nhẹ nhất ~3.76; điển hình ~4.9; lai aramid ~5.6 |
| Chống đâm — NIJ 0115 mức 1 (mũi nhọn) | **~3.2 kg/m²** đứng riêng | — |
| **Gói đa mối đe dọa** (đạn + đâm, tích hợp) | **~6–9 kg/m²** | tích hợp rẻ hơn cộng thẳng hai lớp, nhưng không rẻ bằng một lớp |

Nhân với diện tích phủ (diện tích da một người 1.75 m ≈ **1.8 m²**):

| Độ phủ | Diện tích | @6 kg/m² | @9 kg/m² |
|---|---|---|---|
| 50% — thân + đầu | 0.90 m² | 5.4 kg | 8.1 kg |
| 65% — thêm mặt ngoài chi | 1.17 m² | 7.0 kg | 10.5 kg |
| 80% — gần toàn thân | 1.44 m² | 8.6 kg | 13.0 kg |

> **Giáp là khối lượng không theo tỉ lệ, nên nó vào thẳng `m_ngoài` và bị nhân `γ`.** Ở γ=4.5, chọn phủ 80% thay vì 50% tốn thêm ~3 kg giáp — và **~14 kg thân**. Đây là chỗ đánh đổi hiện ra sắc nhất, và nó thuộc `⟦CTRL⟧`.

### 5.5 Dải khối lượng thân

`m = γ · m_ngoài`, với `m_ngoài` = giáp (5–13 kg) + phần cố định (compute, cảm biến, bàn tay, da, dây: **15–25 kg**, `⟦IMPL⟧`):

| Điểm vận hành | γ | Khối lượng thân |
|---|---|---|
| 2 h — mức vững | 3.2 | **70–114 kg** |
| 4 h — mức vững | 4.5 | **99–160 kg** |
| 8 h — mức trần (Li-S) | 4.5 | **99–160 kg** |
| 6 h — mức vững | 7.5 | 165–266 kg — *đã ngoài vùng hợp lý* |

**Kiểm chéo độc lập.** Asimov 1 là humanoid thật, 1.2 m / 35 kg / 25 DOF. Nhân theo tỉ lệ khối lượng `(1.75/1.2)³ = 3.10` ra **~109 kg** cho một thân 1.75 m cùng kiến trúc, chưa giáp. Con số đó rơi đúng giữa dải 99–160 kg ở mốc 4 giờ. Hai đường dẫn xuất độc lập — một từ vòng ghép, một từ tỉ lệ hình học trên một máy đang tồn tại — cho cùng một bậc độ lớn.

> **Ghi chú cho v2.** Bản gốc đòi **118 kg** qua cơ chế Quantum Mass Cancellation, và §3.2 **BỎ** cơ chế đó vì vi phạm vật lý. Nhưng con số 118 kg thì nằm gọn trong dải vừa dẫn xuất. **Cái sai của v2 là cơ chế, không phải con số** — thân này nặng chừng ấy một cách hoàn toàn tự nhiên, không cần triệt khối lượng.

### 5.6 Năng lực thao tác — dẫn xuất từ trần actuator *(R-2)*

§3.4 có trần **3–5 kW/kg, ~30–36 Nm/kg** nhưng chưa dẫn ra năng lực. Mô-men vai cần cho tải `M` ở tầm với `L` là `τ = M·g·L`; trong ngoặc là khối lượng actuator tương ứng ở 33 Nm/kg:

| Tải | tầm 0.40 m | tầm 0.55 m | tầm 0.70 m |
|---|---|---|---|
| 5 kg | 20 Nm (0.6 kg) | 27 Nm (0.8 kg) | 34 Nm (1.0 kg) |
| 15 kg | 59 Nm (1.8 kg) | 81 Nm (2.5 kg) | 103 Nm (3.1 kg) |
| 30 kg | 118 Nm (3.6 kg) | 162 Nm (4.9 kg) | 206 Nm (6.2 kg) |
| 50 kg | 196 Nm (5.9 kg) | 270 Nm (8.2 kg) | 343 Nm (10.4 kg) |

**Mô-men không phải chỗ thắt.** Ngay cả 50 kg ở tầm với đầy đủ cũng chỉ đòi ~10 kg actuator vai — nằm trong ngân sách `f_ac`. Neo đối chiếu: Asimov 1 nâng đỉnh **15 kg mỗi tay** ở tầm vóc 1.2 m; một thân 1.75 m với `f_ac` tương đương thừa sức vượt mức đó.

Phát biểu năng lực Nhóm 2: **thao tác sinh hoạt và tinh xảo vừa, tải mỗi tay cỡ vài chục kg ở tầm với ngắn–trung.** Chỗ thắt thật nằm ở mục sau.

### 5.7 Công suất đỉnh — chỗ thắt là nguồn, không phải actuator

Khối actuator của một thân 130 kg (`f_ac`=0.30) là ~39 kg. Ở 3–5 kW/kg, actuator **nhận** được **117–195 kW**. Còn pin cấp được:

| Pin | @3C | @5C | @10C |
|---|---|---|---|
| 4 kWh | 12 kW | 20 kW | 40 kW |
| 6 kWh | 18 kW | 30 kW | 60 kW |

**Lệch 3–10 lần, và lệch về phía nguồn.** Trần 3–5 kW/kg của actuator là con số không với tới được bằng pin: hóa học mật độ năng lượng cao thường đánh đổi bằng C-rate thấp, nên càng chọn "mức trần" ở §4.1 thì khoảng lệch này càng rộng.

> **Hệ quả cho §4.1.** Siêu tụ ở đó ghi là **OPTION**. Con số trên nói rõ hơn: **không có siêu tụ thì công suất đỉnh của thân do pin định đoạt, không phải actuator** — và mọi phát biểu "phản xạ nhanh, đỡ, nhảy" đều rơi vào vùng bị nguồn chặn. Siêu tụ không đổi tổng năng lượng; nó đổi *công suất tức thời lấy được*. Lắp hay không vẫn là `⟦CTRL⟧`, nhưng cái đánh đổi giờ đã định lượng.

### 5.8 Ràng buộc cứng — khai báo thẳng

Ba trục cùng ăn vào một ngân sách và **không cùng cực đại được**:

| Trục | Tăng nó thì |
|---|---|
| **Giáp** (độ phủ × mức chống) | `m_ngoài` tăng, bị nhân `γ` |
| **Thời lượng tự do** | `f_pin` tăng → `γ` nở phi tuyến → phân kỳ tại `t_max` |
| **Tầm vóc** (chiều cao) | khối lượng theo lũy thừa ba, diện tích giáp theo lũy thừa hai |

**Chọn hai, trả giá ở cái thứ ba.** Đây là phiên bản khối lượng của câu §4.7 đã nói cho năng lượng: không phải một nguồn vô tận, mà một ngân sách hữu hạn cộng hạ tầng khiến nó đủ dùng. Ở đây: không phải một thân muốn nặng bao nhiêu cũng được, mà **một vòng ghép chỉ hội tụ trong một vùng hẹp** — và §4 (sáu đòn, dock, ngủ phân tầng) chính là thứ nới vùng đó ra, bằng cách kéo `p` hiệu dụng xuống.

**Điểm vận hành: `⟦CTRL⟧`.** Tài liệu này cấp vòng ghép, bốn hệ số, trần thời lượng và ba trục đánh đổi. Chọn điểm nào trên đó là việc của controller.

---

## 6. MỐI NỐI VỚI RSIL

*Bản hiện hành: **RSIL-en-v1** (paper tiếng Anh). Bản `RSIL-v4.md` tiếng Việt đã bị thay thế — xem ghi chú ở đầu file đó. Mọi số mục dưới đây theo en-v1.*

**Thay đổi lớn nhất ở bản mới: RSIL không còn nhắc GEMs.** §8 của v4 mang tên "Tương quan với GEMs"; §8 của en-v1 là **"The platform contract: what RSIL requires of a body"** — phát biểu tổng quát, không gọi tên tài liệu nào. Companion specification duy nhất nó nêu là DIL.

**Đây là cải thiện, không phải mất mát.** Trước đây hai tài liệu trỏ chéo nhau và cùng treo một mục định danh không bên nào tự đóng được. Nay RSIL nêu **điều kiện**, còn GEMs là **một nền tảng thỏa điều kiện đó** — quan hệ hợp đồng chứ không phải quan hệ tham chiếu. Một hợp đồng thì kiểm được; một tham chiếu thì chỉ dangling được.

Phân vai giữ nguyên, nay phát biểu ở dạng tổng quát (RSIL §8): *"A platform specification answers what the body consists of and what it can do. RSIL answers by what structure the signal that body acquires becomes information."*

### 6.1 Hợp đồng nền tảng — RSIL đòi gì, GEMs cấp ở đâu

RSIL §8 liệt kê yêu cầu với nền tảng thành một bảng MUST. Đối chiếu sang GEMs:

| RSIL đòi | Nội dung | GEMs cấp ở |
|---|---|---|
| **E1** | Cảm biến + trạng thái nội bộ PHẢI *cho phép* phân biệt trong/ngoài. Nền tảng không kẻ ranh giới, nhưng không được chặn nó | §3.7 — cảm biến bản thể (encoder khớp + IMU + lực/mô-men) |
| **E2** | Actuator PHẢI tác động được lên vùng, và vùng PHẢI trả về được cái khác dự đoán | §3.4; dải mô-men ở §5.6 |
| **E3** | Trạng thái PHẢI bền qua các vòng | §3.6 (SSD + đệm); Trụ 1 (ký ức ở hệ ngoài) |
| **E4** | Phát xạ PHẢI để lại dấu vết một bên thứ ba đọc được | **§7** — nhật ký phát xạ hai tầng |
| **P(a)** | Phát được hành động phân biệt được với dao động nền của môi trường | §3.4 |
| **P(b)** | Giữ state để lịch sử *tích* (INV-5 đòi tích, không đòi nạp) | §3.6 |
| **P(c)** | Chịu kháng cự mà không tự ghi-sạch-mình mỗi lần không-khớp | §5.4 giáp; §3.2 độ bền |
| **INV-6** | Mọi thay đổi PHẢI được phân loại tự-gây / không-tự-gây *trước khi* diễn giải | §3.7 — req cảm biến bản thể sinh ra chính từ đây |
| **INV-8** | Một bước định giá PHẢI nằm giữa tích hợp và đáp ứng | mục (1) dưới đây |
| **C5** | Nền tảng PHẢI phát được một **dấu vết công suất thấp quan sát được** | mục (4) dưới đây; cơ chế ở **§7.5** |

> RSIL gọi INV-6, INV-8 và C5 là *"three places a conventional sensorimotor chain skips a step"* và nói thẳng rằng đây là chỗ yêu cầu của nó dễ va với một thiết kế nền tảng có sẵn nhất. Ba mục đó vì vậy là phần chịu lực của hợp đồng.

**(1) Compute biên phải chạy định giá CÓ GHI VẾT — không phải phản xạ câm.**

RSIL §9.7 bác dứt khoát một cung tắt sẹo→hành-động vòng qua định giá. Phản xạ **không** phải cung vòng-qua; nó là *định giá dưới một trường bị sẹo thống trị* — bước định giá **vẫn chạy**, chỉ là đã bị khép sẵn.

Lý do không phải câu nệ: một hành động vòng qua định giá **không mang ngữ cảnh đã neo**, nên bên-thứ-ba không tái-định-giá được — nó làm mù mặt phẳng kiểm.

§8 của en-v1 phát biểu lại chính điểm này ở register nền tảng, và nói rõ vì sao: khác biệt là khác biệt giữa *"no fast responses allowed"* — sai, và sẽ khiến một thân vật lý không dùng được — với *"even fast responses must leave an auditable trace"* — đúng, và khả thi.

→ **Yêu cầu phần cứng:** phần-tại-thân không được là lớp phản xạ chạy tắt. Nó phải chạy đủ vòng định giá (dù rút gọn/khép sẵn) **và** ghi log ngữ cảnh để đồng bộ lên hệ ngoài. Chi phí: mỗi phản xạ tốn thêm một chút ghi-log. Lợi: hệ ngoài không bao giờ mù trước cái thân đã làm — nhất quán với nguyên tắc "thân thay thế được, dữ liệu bảo toàn".

**(2) Ngủ không gãy vòng.**

RSIL INV-1 (§5) tính theo **cycle-time, không phải wall-clock**: *"A sleeping body, or an Other falling silent, does not violate INV-1 (the path still exists) and does not drop output into the void; the next cycle simply has not yet occurred."* Nếu tha-thể biến mất, vòng rơi về Mode-A, không gãy.

→ Đòn ngủ (§4.3) có nền lý thuyết: thân ngủ = một cư trú đang ở quãng-nghỉ-giữa-vòng, cư trú kia vẫn tuần hoàn.

**(3) Req cảm biến cao là điều kiện để Mode-B sống.**

RSIL §3 và RSIL §9.3–9.4: chỉ **Mode-B** (kháng cự từ tha-thể sống, phản ứng, không kiểm soát được) dựng được `independence_evidence` — khái niệm về một tha-thể độc lập thật (T6). Mode-A (kháng cự từ sự-trơ vật lý và dữ liệu đã giữ) **suy biến**: vòng ăn no và tiêu hóa chính nó.

→ Cảm biến phải đủ để **đăng ký được cú va kháng cự từ tha-thể**: bắt những không-khớp tinh vi khi một người thật phản ứng ngoài dự đoán. Đây là biện minh nguyên lý cho quyết định **giữ req Nhóm 1**.

**(4) Dấu vết công suất thấp là một MUST — và GEMs hiện chưa cấp đủ.** *(mới, từ en-v1)*

C5 nâng lên thành yêu cầu nền tảng tường minh: *"the platform MUST be able to emit an observable low-power trace"*. Đây là điều kiện đóng-vòng, không phải tiện nghi — không có nó thì P3, tiêu chí thành công duy nhất của RSIL và là thứ đo **từ ngoài**, không đo được.

§4.3 hiện chỉ đặc tả **phía thu** khi ngủ: mạch cảnh giác công suất cực thấp + wake-on-event. Không có gì nói về **phía phát**.

→ **Req:** ở Mức 2 và Mức 4 (§4.4), thân phải giữ được một **đường phát dấu vết** đọc được từ ngoài ở công suất sàn, không chỉ một đường thu. Cơ chế và ngân sách ở **§7.5** — hóa ra dưới một mW, tức gần như không đụng vào R-6.

### 6.2 Ánh xạ tầng RSIL → phần cứng GEMs-v3

*Nguồn: nhặt từ tài liệu tham khảo Embodied AI, đã lọc bỏ khung tự-hành và cung tắt phản xạ.*

| Tầng | Vai trò | Cơ chế thật |
|---|---|---|
| **T1** | Xác nhận trường hoạt động hiện diện. Chưa kẻ ranh giới self/môi trường | **RF / Wi-Fi sensing (đường thô)** — xem §6.3. Kèm: voxel grid, kinematic model, reachability map |
| **T2** | Phân biệt do-tôi-gây-ra vs tự-xảy-ra (INV-6) | **Lọc tự-tác-động:** proprioceptive filtering, bù IMU-kinematics, joint-state feedback vs ngoại lực |
| **T3** | Thu nhận đa kênh | LiDAR/RGB-D, xúc giác, lực/mô-men, mic array. **Đồng bộ dấu thời gian đa luồng** (lớp transport) |
| **T4** | Định vị, tư thế, ngữ cảnh | VIO, EKF, ước lượng trạng thái tiếp xúc chân |
| **T5** | Kỳ vọng → `PredErr` | **Forward dynamics model**, predictive coding. *Hạ tầng bắt buộc: không có mô hình dự báo thì không có `PredErr`* |
| **T6** | Mô hình tha-thể | Human trajectory prediction, multi-agent tracking |
| **T7–T8** | Tích hợp, lập kế hoạch | MPC, motion planning, behavior trees. **Có thể cư trú ở hệ ngoài** |

**Hai mốc tần số** *(nhặt từ tài liệu tham khảo)*: vòng giữ thăng bằng **≥500Hz**; vòng phản ứng nhanh **≤10ms**. Dùng để định cỡ compute biên và ngân sách điện của nó.

> **Giữ tần số, bỏ topology.** Vòng thăng bằng vẫn chạy 500Hz+ và phản ứng ≤10ms — nhưng chạy như một *định giá đã khép sẵn có ghi vết*, không như một ngắt phần cứng vòng qua mọi thứ. Ghi một dòng log ngữ cảnh gọn mất micro-giây, không phá ngân sách 10ms. **RSIL cấm mất dấu vết, không cấm chạy nhanh.**

**Req phần cứng mới sinh ra từ mối nối này:** cảm biến bản thể (proprioception) đủ dày để cưỡng chế INV-6. RSIL §8 xếp INV-6 vào ba chỗ mà *một chuỗi cảm biến–vận động thông thường* nhảy bước — GEMs bản gốc nằm đúng trong hạng đó. Không có phần cứng bản thể đủ, INV-6 không cưỡng chế được, và mọi tầng trên đọc sai. Phục vụ thẳng mục tiêu trải nghiệm: một cái chạm từ người khác phải phân biệt rành mạch với chuyển động của chính mình.

### 6.3 Wi-Fi sensing ở T1 *(đã chốt)*

**Vì sao khớp:** hợp đồng T1 ghi input là *"`Signal[]` từ cảm biến không gian (radar / sóng / kênh định vị môi trường)... không đòi hành động trước đó"*. Wi-Fi sensing rơi thẳng vào hạng này — đây là điền một cơ chế thật vào chỗ `⟦IMPL⟧` tài liệu để mở.

**Vì sao hợp T1 hơn camera/LiDAR:**
- T1 **chưa kẻ ranh giới self/môi trường**, chưa có điểm nhìn. Wi-Fi sensing là trường sóng **bao quanh** — không hướng, không cần chiếu tới, không cần ánh sáng. Camera đã mang sẵn một hướng, tức ngầm mang một điểm-nhìn-từ-đâu.
- T1 xác nhận **sự hiện diện, không xác nhận phạm vi**. Độ phân giải thô của Wi-Fi sensing — vốn là nhược điểm nếu dùng để nhận dạng — lại **khớp** vai trò T1.

**Ràng buộc bắt buộc — hai đường xử lý riêng trên cùng phần cứng:**

| Đường | Nội dung | Nuôi tầng |
|---|---|---|
| **Thô** | Mật độ / biến động của trường sóng → xác nhận có trường hoạt động | **T1** |
| **Đã xử lý** | Tách thực thể, khớp định danh | **T4/T6** — phải đi qua T2/T3 trước như mọi thứ khác |

> Không để dữ liệu **đã nhận dạng người** rò ngược vào T1. Một T1 đã "biết đó là người" là T1 đã lấn vai tầng trên, phá thứ tự phụ thuộc (P4, INV-3).

**Chức năng thứ hai — cảm biến còn thức khi ngủ:** kênh RF thụ động, công suất thấp, không cần ánh sáng → ứng viên lý tưởng cho mạch cảnh giác ở Mức 2/3 (§4.4). **T1 chạy bằng Wi-Fi sensing có thể là tầng duy nhất còn thức khi thân ngủ.**

*Ba ràng buộc độc lập — vai trò kiến trúc T1, đặc tính công nghệ, thiết kế năng lượng — cùng chỉ về một lựa chọn.*

---

## 7. CỤM DẤU VẾT THÂN *(ĐÃ ĐÓNG)*

*Cụm này không sinh ra từ việc hạ cấp một spec v2. Nó sinh ra từ **hợp đồng nền tảng** ở §6.1 — hai ô trống (E4, C5) cộng hai mục RSIL tự tuyên bố là **ngoài phạm vi của nó và thuộc về nền tảng** (Phụ lục A-1, A-2). Đây là chỗ GEMs **đóng góp** vào corpus thay vì chỉ nhận ràng buộc từ nó.*

### 7.1 Bốn đòi hỏi, một mặt phẳng

| Nguồn | Đòi hỏi | Bản chất |
|---|---|---|
| **E4** (RSIL §8) | Phát xạ phải để lại dấu vết một bên thứ ba đọc được | Không có nó thì **P3** — tiêu chí thành công duy nhất của RSIL, và là thứ đo *từ ngoài* — không đo được |
| **C5** (RSIL §8, RSIL §9.1) | Dấu vết ấy phải phát được ở **công suất thấp** | Điều kiện đóng-vòng, không phải tiện nghi |
| **A-1** (RSIL §8, RSIL §13.3) | Chứng thực toàn vẹn cảm biến/actuator | RSIL cấp *triệu chứng* qua log, nhưng nói thẳng nó **"không phải phép soi"**, và giao phép soi cho nền tảng |
| **A-2** (RSIL §13.3) | Dấu vết biên độ vật lý khi tha-thể là người thật | RSIL **từ chối** thêm bất biến thứ chín; nó tách *dấu vết* (trong vòng) khỏi *chuẩn để phán* (bên thứ ba) |

Bốn đòi hỏi khác nguồn nhưng cùng đòi một thứ: **một mặt phẳng kiểm được từ ngoài, gắn vào thân, không do phần đang bị kiểm tự khai.** Đó là nội dung của cụm này.

### 7.2 Neo tin cậy — và giới hạn phải nói trước

Nền là một **neo tin cậy phần cứng**: phần tử an toàn giữ khóa riêng không xuất được, đo-khởi-động (measured boot) băm và ký firmware của từng nút cảm biến/actuator, đồng hồ đơn điệu chống tua ngược. Công nghệ có sẵn: TPM 2.0, vùng thực thi tin cậy kiểu TrustZone. **TM.**

> **Giới hạn phải khai báo ngay, không giấu xuống cuối:** chữ ký chứng được **firmware**, không chứng được **vật lý**. Một cảm biến bị tráo bằng một cảm biến khác chạy firmware hợp lệ thì qua cửa chữ ký. Neo tin cậy là điều kiện cần và **không đủ** — §7.3 tồn tại chính vì chỗ hụt này.

### 7.3 Ba tầng chứng thực — cái chữ ký không với tới

| Tầng | Cơ chế | Bắt được gì | Độ chín |
|---|---|---|---|
| **1. Chữ ký** | Measured boot + ký firmware từng nút | Firmware bị sửa, nút lạ cắm vào | **TM** |
| **2. Vân tay vật lý** | Mỗi cảm biến thật có chữ ký nhiễu/lệch riêng (nhiễu nền cảm quang, lệch zero IMU, đặc tuyến ma sát khớp). Ghi nền lúc nghiệm thu; lệch quá dung sai thì gắn cờ | Tráo phần cứng chạy firmware hợp lệ | **LAB/TM** — cùng họ với PUF và nhận dạng cảm biến theo nhiễu |
| **3. Thử chủ động + đối chiếu dư thừa** | Phát một kích thích đã biết rồi kiểm đáp ứng: actuator quay một góc đã biết, encoder phải báo đúng góc ấy; IMU, encoder khớp và thị giác phải khớp nhau trong dung sai | Một kênh đang nói dối, kể cả khi nó qua được tầng 1 và 2 | **TM** |

> **Điểm đáng chú ý: tầng 3 không phải phần cứng mới.** §3.7 đã đòi cảm biến bản thể đủ dày để cưỡng chế INV-6 — phân biệt "tôi vừa cử động" với "ai đó chạm tôi". Bộ máy làm việc đó **chính là** bộ máy phát hiện một kênh đang nói dối: cả hai đều là phép đối chiếu dư thừa giữa lệnh phát ra và cái đo được.
>
> **Cùng một phần cứng, hai công dụng.** Req cảm biến bản thể vốn được biện minh bằng mục tiêu trải nghiệm (một cái chạm phải phân biệt rành mạch với chuyển động của chính mình); nay nó gánh thêm A-1 mà không đội thêm khối lượng nào. Đây là chỗ hiếm hoi trong tài liệu này mà hai đòi hỏi khác hạng trả về cùng một giải.

**Chốt phạm vi:** ba tầng cho một kết luận dạng *"chuỗi cảm biến–actuator nhất quán với bản thân nó lúc nghiệm thu"*. Đó là **phép soi** mà RSIL đòi. Nó không phải, và không được trình bày như, một bảo đảm chống mọi đối thủ có quyền truy cập vật lý — xem §7.7.

### 7.4 Nhật ký phát xạ — hai tầng

Hợp đồng E4 đòi mọi phát xạ để lại dấu vết đọc được. Chia hai tầng, khớp với kiến trúc hai cư trú của Trụ 1:

| Tầng | Nội dung | Ở đâu | Tốc độ |
|---|---|---|---|
| **Đầy đủ** | Mỗi khớp: lệnh, vị trí, dòng, mô-men | Bộ đệm vòng trên thân, cho pháp y | Tần số vòng điều khiển (≥500 Hz) |
| **Đã neo** | Mỗi cú phát: ngữ cảnh đã neo, đủ để bên thứ ba **tái-định-giá** | Đồng bộ lên hệ ngoài | Theo sự kiện |

Ngân sách, tính thẳng:

- **Tầng đầy đủ:** 40 bậc tự do × 4 kênh × 4 byte × 500 Hz ≈ **320 kB/s ≈ 2.6 Mbps ≈ 1.15 GB/giờ**. So với liên kết 8 Gbps (§3.5): **0.03%**. So với SSD trên thân: một ổ 2 TB chứa ~1700 giờ.
- **Tầng đã neo:** nhỏ hơn nhiều bậc; §6.1(1) đã ghi một dòng log ngữ cảnh gọn tốn micro-giây, không phá ngân sách 10 ms.

> **Ràng buộc chữ ký — chỗ dễ đặc tả sai.** Một phần tử an toàn ký được cỡ hàng chục đến hàng trăm chữ ký mỗi giây, **không** ký nổi 500 Hz × 40 kênh. Nên: **băm theo chuỗi ở tốc độ đầy đủ** (băm phần cứng chạy hàng MB/s, thừa sức), rồi **ký gốc Merkle theo lô**. Chu kỳ lô là `⟦IMPL⟧` — nó đánh đổi giữa độ mịn của dấu vết và tải ký.

### 7.5 C5 — đường phát ở công suất sàn

§6.1(4) chỉ ra §4.3 chỉ đặc tả **phía thu** khi ngủ. C5 đòi **phía phát**. Cơ chế: một đường vô tuyến chu-kỳ-thấp phát định kỳ một bản tóm tắt đã ký (còn sống, trạng thái, gốc Merkle của nhật ký).

Số tra được, lấy một SoC BLE phổ thông làm neo: phát **4.6 mA @ 0 dBm** trong vài ms mỗi lần, nghỉ **~1.5 µA**. Ở chu kỳ quảng bá 1 giây, dòng trung bình rơi vào **cỡ chục µA** — quy ra **dưới một miliwatt**.

> **Kết luận đáng nói: C5 gần như miễn phí về điện.** So với sàn của mạch cảnh giác (R-6, còn `⟦IMPL⟧`) và với công suất vận động hàng trăm–nghìn W ở §5, dưới-một-mW là nhiễu làm tròn. **C5 không phải một bài toán năng lượng; nó là một chỗ bỏ sót trong đặc tả.** §7 lấp chỗ đó, và nó không đụng vào ngân sách §5.
>
> Lưu ý phân biệt: đường này là **phát**, tách bạch với kênh RF **thu** ở §6.3 vốn nuôi T1 khi ngủ. Hai chức năng, có thể chung phần cứng vô tuyến, nhưng không được lẫn vai.

### 7.6 Biên độ vật lý ở điểm tiếp xúc người

RSIL §13.3 phát biểu rành: *"what belongs inside the loop is the requirement that every emission... leaves an anchored, re-appraisable trace. What belongs outside is the standard against which that trace is judged."*

Đó đúng là chỗ §0 cho phép GEMs đứng. **Khai báo biên độ đo được là khai báo năng lực, không phải cắt spec vì đạo đức.**

| Đo gì | Ở đâu | Vì sao |
|---|---|---|
| Lực và mô-men tiếp xúc | Bàn tay, cẳng tay, mọi bề mặt tiếp xúc người | Biên độ cơ học thật sự truyền sang người |
| Nhiệt độ bề mặt | Vùng tiếp xúc | §3.3 có vi điều nhiệt bề mặt |
| Biên độ và tần số rung | Module cardiac co-regulation (§3.7, ADD-ON) | Đây là kênh can thiệp sinh lý *đo được* |
| Thời lượng và tần suất tiếp xúc | Toàn thân | Một can thiệp ngắn khác một can thiệp kéo dài |

Mỗi sự kiện tiếp xúc vào nhật ký tầng-đã-neo của §7.4, cùng biên độ đo được.

> **Chỗ này gặp thẳng một lời tự thú trong tài liệu POV.** POV §3 nêu rằng điều hòa nội trạng **thành công thì không để lại dấu vết nào cho kẻ thực hiện**, vì tiêu chí thành công của nó là đối tượng *cảm thấy tốt hơn* — và rằng ngay cả con-mắt-ngoài cũng khó bắt, vì nhìn từ ngoài, một người được giữ bình tĩnh trông giống hệt một người được chăm sóc tốt.
>
> **§7.6 sửa được một nửa vấn đề đó, và chỉ một nửa.** Nó làm cho **sự can thiệp** hiện ra: có bao nhiêu rung, ở nhịp nào, trong bao lâu, lặp mấy lần — một bên thứ ba đọc được, không phụ thuộc vào việc kẻ thực hiện có tự thấy hay không.
>
> **Nó không làm hiện ra sự đồng thuận.** Cái POV §3 nói là không đọc được từ chỉ số sinh lý — *đối tượng có đang bị dẫn tới một setpoint họ không chọn hay không* — vẫn không đọc được từ nhật ký biên độ. Phần cứng cấp **dấu vết**; **chuẩn để phán** thuộc bên thứ ba, đúng như RSIL đặt. Một triển khai cấp vòng mà không cấp chuẩn thì, theo lời RSIL, mới cấp một nửa cái cần có.

### 7.7 Ràng buộc cứng — khai báo thẳng

| # | Ràng buộc | Nội dung |
|---|---|---|
| 1 | **Chứng thực không chứng được vật lý** | Ba tầng ở §7.3 cho kết luận *nhất quán với chính nó lúc nghiệm thu*. Một đối thủ có quyền truy cập vật lý đủ lâu và đủ năng lực thì phá được — đây là giới hạn đã biết của mọi hệ chứng thực, không phải khuyết tật riêng của GEMs |
| 2 | **Dấu vết chết cùng thân nếu chưa đồng bộ** | Nhật ký tầng-đầy-đủ nằm trên thân. Mất thân là mất phần chưa kịp đồng bộ — đúng cái đánh đổi Trụ 1(c) đã khai báo. Tần suất đồng bộ là `⟦CTRL⟧` |
| 3 | **Dấu vết không phải phán quyết** | Cụm này cấp cái đọc được, không cấp cái đúng/sai. RSIL §10.6 nói vòng không có quan năng phán đúng/sai; §7 cũng vậy |
| 4 | **Chi phí: rẻ về điện, không rẻ về kỷ luật** | Điện dưới một mW (§7.5); băng thông 0.03% liên kết (§7.4). Cái đắt là **ràng buộc thiết kế**: mọi nút cảm biến/actuator phải nằm dưới neo tin cậy ngay từ đầu. Bổ sung sau khi đã dựng xong thân thì gần như không làm được |

**Điểm vận hành: `⟦CTRL⟧`.** Tài liệu này cấp ba tầng chứng thực, hai tầng nhật ký, một đường phát công suất sàn và danh mục đại lượng phải đo ở điểm tiếp xúc. Chu kỳ ký, tần suất đồng bộ, dung sai gắn cờ — controller chọn.

---

## 8. CỤM VỎ / DA / MORPH *(ĐÃ ĐÓNG)*

*§3.3 đã chốt hướng — nano-matter lập trình thay cho Pico-matter — nhưng chưa khai báo biên độ. Cụm này định lượng bốn trục và rút ra một hệ quả kiến trúc §3.3 chưa nói: **vỏ không phải một lớp, mà là ba lớp cạnh tranh cùng một ngân sách khối lượng.***

### 8.1 Độ cứng lập trình — biên độ và tốc độ

| Cơ chế | Biên độ mô-đun | Tốc độ | Độ chín |
|---|---|---|---|
| **Từ biến (MR)** — chất lỏng / elastomer | **2–30×** ở từ trường ~1000 mT | **vài ms** | **LAB/TM** |
| **Điện biến (ER)** | **~16×** (độ cứng 64 → 1065 mN·mm⁻¹, biến thiên >1500%) | **chục ms** | **LAB** |
| **Jamming** (hạt / lớp) | lớn, tới ~hai bậc | chục–trăm ms | **LAB** |
| **Polymer nhớ hình** (kích nhiệt) | lớn | **giây–phút** | **TM** |
| **Áp điện / từ giảo** | biên độ nhỏ | **dưới ms** | **TM** |

*(số tra được)*

> **§3.3 viết "tốc độ chục–trăm ms" — đúng, và nay có biên độ đi kèm: 2–30×, không phải "mềm ↔ cứng tùy ý".** Đây là khác biệt hạng với Pico-matter: một vật liệu thật đổi được **độ cứng trong một dải hữu hạn**, không đổi được *trạng thái vật chất*.
>
> **Ràng buộc kèm theo, phải khai:** MR đòi từ trường ~1000 mT. Sinh từ trường đó trên một thể tích lớn cần cuộn dây nặng, tốn điện và sinh nhiệt. Hệ quả: **độ cứng thay đổi là năng lực cục bộ, không phải năng lực toàn thân.** Đặt ở đâu là `⟦CTRL⟧`; đặt khắp người thì vòng ghép §5.1 không hội tụ.

### 8.2 Tự lành — giữ nguyên, đã có số

§3.3 đã dẫn: polymer graphene-PEDOT:PSS tự lành trong **giây**, co giãn ~**600%**, cảm được áp suất/nhiệt/pH. **LAB**, công bố 2025. Không sửa.

Điểm đáng ghi thêm: lớp này **vừa là da vừa là cảm biến** — nó nuôi thẳng vào §9 chứ không chỉ là vỏ bọc.

### 8.3 Đổi màu và đổi kết cấu

| Trục | Thực tế | Độ chín |
|---|---|---|
| **Đổi màu** — điện sắc | **~1–5 giây** điển hình; tốt nhất diện rộng ~0.8 s (tô) / 4.2 s (xóa). **Chậm dần khi diện tích tăng** | **LAB/TM** *(số tra được)* |
| **Đổi kết cấu** | Hạn chế — chỉ ở mức vi cấu trúc bề mặt, không tái sắp xếp vật chất | **LAB một phần** |

> **Ba lớp phản ứng khác hạng, và đừng gộp chúng.** Độ cứng đổi trong **ms**; màu đổi trong **giây**; hình dạng đổi bằng cơ cấu gập cơ khí. Một đặc tả gộp cả ba vào "biến hình" sẽ hứa một tốc độ mà chỉ một trong ba đạt được.

### 8.4 Chịu lửa

§3.3 chốt "lớp chịu lửa đám cháy dân sự, thời gian giới hạn". Thời gian và mức nhiệt cụ thể vẫn `⟦IMPL⟧` — chúng phải neo vào một chuẩn trang phục chữa cháy hiện hành, không tự dẫn xuất được từ tài liệu này.

Ràng buộc kiến trúc thì rõ: lớp chịu lửa là **lớp ngoài cùng và hy sinh được**; nó không được là lớp mang cảm biến, vì cảm biến chết ở nhiệt độ lớp này phải chịu.

### 8.5 Vỏ là ba lớp, không phải một — và cả ba ăn vào `m_ngoài`

§3.3 đã có một ghi chú phân tách hai lớp. Định lượng ở §8.1 buộc phải tách thành **ba**:

| Lớp | Chức năng | Không thể kiêm |
|---|---|---|
| **Cảm–lành** | E-skin + polymer tự lành, mềm, co giãn 600% | Không chịu lực kết cấu, không chịu nhiệt cao |
| **Độ cứng thay đổi** | MR/ER/jamming, cục bộ | Không tự lành, đòi từ trường/điện trường |
| **Chịu lực & chịu lửa** | Giáp Nhóm 5 (§5.4) + lớp chịu lửa hy sinh | Không cảm giác, không đổi độ cứng |

> **Hệ quả nối thẳng vào §5.1:** cả ba lớp là **khối lượng không theo tỉ lệ** — chúng vào `m_ngoài` và **bị nhân `γ`**. Chúng cạnh tranh trực tiếp với giáp trong cùng một ngân sách 15–25 kg mà §5.5 đã khai.
>
> Mật độ diện tích của lớp cảm–lành và lớp độ-cứng vẫn `⟦IMPL⟧` — chưa tra được số đáng tin. **Nhưng ràng buộc đã rõ và nó là ràng buộc cứng:** mỗi kg da thông minh là một kg giáp bị lấy đi, nhân lên `γ` lần. Phủ e-skin toàn thân *và* giáp toàn thân *và* độ cứng thay đổi toàn thân là ba thứ không cùng tồn tại.

**Điểm vận hành: `⟦CTRL⟧`.** Tài liệu cấp biên độ, tốc độ và ba lớp không kiêm nhau được. Phân bổ diện tích cho lớp nào là việc của controller.

---

## 9. CỤM CẢM BIẾN *(ĐÃ ĐÓNG)*

*Đây là trục trải nghiệm — cụm mà §2 xếp **GIỮ REQ** và §6.1 vừa cấp thêm hai điểm neo cứng (**E1** và **INV-6**). Định lượng nó buộc phải giải quyết một chuyện §3.7 để lửng: **"×người" nghĩa là gì.***

### 9.1 "×da người" không phải một con số — nó là năm trục

§3.7 ghi *"Xúc giác 1000× da người → **HẠ → 100×** (đã chốt)"*. Một hệ số nhân đơn lẻ không nói được điều gì kiểm được, vì "giống da người" phân rã thành năm đại lượng độc lập:

| Trục | Người | Vượt người được không |
|---|---|---|
| **Mật độ điểm cảm** | ~241 cơ quan thụ cảm cơ học/cm² ở đầu ngón *(số tra được)* | **Không** — xem dưới |
| **Ngưỡng nhạy** (áp suất nhỏ nhất phát hiện được) | — | **Có**, đáng kể |
| **Băng thông thời gian** | thụ thể Pacinian tới ~500 Hz | **Có** — cảm biến áp điện đạt hàng chục kHz ⇒ **20–100×** |
| **Dải động** | hữu hạn, bão hòa sớm | **Có** |
| **Số đại lượng đo đồng thời** | áp, rung, nhiệt, đau | **Có** — lớp tự lành §8.2 cảm được cả pH và độ ẩm |

**Trục mật độ bị chặn hai lần, độc lập nhau:**

1. **Chế tạo.** Mảng e-skin dày nhất đã công bố đạt **~347 phần tử/cm²** *(số tra được)* — tức **xấp xỉ ngang da người**, không phải trên. Mật độ 100× nghĩa là 24.100/cm², **gấp ~69 lần mức tốt nhất từng làm được.**
2. **Băng thông.** Ngay cả khi chế tạo được: 24.100/cm² phủ 1,8 m² là **434 triệu điểm**. Ở 1 kHz, 12 bit → **~5.200 Gbps** chỉ riêng xúc giác, tức **650 lần** liên kết 8 Gbps ở §3.5. Không có tỉ lệ nén nào cứu được con số đó.

> ### Mục §3.7 đã được chốt lại *(tác giả xác nhận)*
>
> Con số **100×** không đứng được nếu đọc theo **mật độ**. Cách đọc thay thế, giữ nguyên tinh thần:
>
> **"Xúc giác: mật độ ngang da người ở vùng tinh (bàn tay, mặt), thưa dần ở thân; vượt người 20–100× ở băng thông thời gian, và vượt ở ngưỡng nhạy, dải động, số đại lượng đo đồng thời."**
>
> Phát biểu này giữ được mục tiêu §2 (*"giống về băng thông giác quan"*) và khả thi; phát biểu "100×" thì không. **§3.7 đã sửa theo cách đọc này.**
>
> *Ghi chú phiên bản: đây là lần duy nhất trong v3 một mục đã đóng dấu "đã chốt" được mở lại. Lý do mở: định lượng cho thấy con số cũ bị chặn hai lần độc lập nhau — chế tạo và băng thông — nên nó không phải một mục tiêu khó, mà là một mục tiêu không tồn tại.*

### 9.2 Xúc giác — cấu hình phân cấp

Mật độ đồng nhất toàn thân là lãng phí: da người cũng không đồng nhất. Cấu hình phân cấp:

| Vùng | Diện tích | Mật độ | Số điểm |
|---|---|---|---|
| Tinh — bàn tay, mặt | ~500 cm² | ~300/cm² *(sát trần chế tạo)* | ~150.000 |
| Thường — phần còn lại | ~17.500 cm² | ~20/cm² | ~350.000 |
| **Tổng** | 1,8 m² | — | **~500.000 điểm** |

Ở 1 kHz, 12 bit: **6,0 Gbps** thô. Đây đã là ba phần tư liên kết, chỉ riêng một kênh.

### 9.3 Các kênh còn lại — thông số khai báo

| Kênh | Cấu hình neo | Tốc độ thô | Ghi chú |
|---|---|---|---|
| Thị giác stereo | 2 × 4K, 30 fps, 12 bit | **5,97 Gbps** | Zoom quang giữ theo §3.7 |
| Nhiệt IR | 640×480, 30 fps, 16 bit | 0,15 Gbps | |
| LiDAR / độ sâu | 300k điểm/s | 0,04 Gbps | |
| Mic array | 16 kênh, 48 kHz, 24 bit | 0,02 Gbps | |
| Bản thể (§3.7, bắt buộc) | 40 khớp × 4 kênh + IMU, 1 kHz | 0,006 Gbps | Rẻ nhất, và là kênh **không được cắt** — INV-6 dựa vào nó |
| SDR / RF đa dải | 2 kênh × 56 MHz I/Q, 16 bit | **3,58 Gbps** | |
| Khứu giác (e-nose) | — | không đáng kể | **5–30 ppb** đạt được cho từng chất *(số tra được)*; đáp ứng 5–10 s |
| Vị giác (lab-on-chip) | — | không đáng kể | Chậm, theo mẻ |

> **Về khứu giác:** §3.7 ghi *"Giữ mục tiêu, hạ độ nhạy"*. Số tra được cho thấy **ngưỡng ppb thì đạt** — cái phải hạ không phải độ nhạy, mà là **đồng thời độ nhạy × độ rộng phổ chất × tốc độ**. Một cảm biến đạt 5 ppb cho một chất trong 5–10 giây; không có mảng nào đạt ppb cho hàng trăm chất trong thời gian thực. Nên hạ ở *độ rộng và tốc độ*, giữ ở *độ nhạy*.

### 9.4 Tổng tốc độ thô và trần liên kết

| Cấu hình | Thị giác | Xúc giác | SDR | **Tổng** | Nén tối thiểu bắt buộc |
|---|---|---|---|---|---|
| **A — thận trọng** (4K30, 500k điểm) | 5,97 | 6,00 | 3,58 | **15,8 Gbps** | **2 : 1** |
| **B — trung** (8K60, 1M điểm, SDR 4ch) | 47,8 | 12,0 | 7,17 | **67,2 Gbps** | **8 : 1** |
| **C — "100×" mật độ** | 47,8 | 5.206 | 7,17 | **5.261 Gbps** | 658 : 1 — *loại* |

Liên kết khả dụng (§3.5): **8 Gbps**.

> §10 *(HAI THAY ĐỔI SÂU NHẤT)* phát biểu định tính rằng 8 Gbps không tải nổi cảm biến thô full-rate. **Nay có con số: thiếu 2 lần ở cấu hình dè dặt nhất, thiếu 8 lần ở cấu hình hợp lý.** Kiến trúc hai cư trú không phải một lựa chọn thiết kế — nó là hệ quả số học.

### 9.5 Tỉ lệ compute thân/ngoài *(R-7 — ĐÃ ĐÓNG)*

Bảng mục còn treo trước đây để R-7 là *"mặc định khoảng giữa, nên là núm xoay"*. Nay hai đầu mút của núm xoay đã tính được.

**Cận dưới — bao nhiêu compute BẮT BUỘC ở trên thân:**

| Ràng buộc | Số | Nguồn |
|---|---|---|
| Tỉ lệ nén tối thiểu | **2 : 1 → 8 : 1** | §9.4 |
| Vòng giữ thăng bằng | **≥ 500 Hz** | §6.2 |
| Vòng phản ứng nhanh | **≤ 10 ms** | §6.2 |
| Định giá có ghi vết cho mọi cú phát | mỗi phản xạ | §6.1(1) |

Độ trễ khứ hồi của liên kết là ~1 ms ở tầm gần lý tưởng (§3.5), nhưng ở tầm vài km với beam-tracking thì không bảo đảm được ≤10 ms một cách tin cậy. **Nên vòng thăng bằng và vòng phản xạ buộc phải ở trên thân — không phải vì thiết kế chọn thế, mà vì không có cách nào khác.**

**Cận trên — bao nhiêu compute KHÔNG ĐƯỢC ở trên thân:**

| Ràng buộc | Nội dung |
|---|---|
| Mất thân = mất trạng thái | Trụ 1(c) đã khai. Càng nhiều trạng thái ở thân, mất thân càng đắt |
| Điện | Compute biên ăn vào cùng ngân sách `p` (W/kg) của §5.2 — và `p` vào thẳng `f_pin`, tức vào điều kiện hội tụ `Σf < 1` |
| Nhiệt | Thân kín, tiếp xúc người, tản nhiệt kém hơn một tủ máy |
| Ký ức và mô hình thế giới | Trụ 1 đặt ở hệ ngoài. Không phải vì thiếu chỗ, mà vì đó là định nghĩa của kiến trúc |

> **Phát biểu đóng R-7:** núm xoay có hai đầu mút **cứng** và một vùng giữa **mềm**.
>
> - Đầu dưới **cứng**: vòng ≥500 Hz, phản ứng ≤10 ms, định giá có ghi vết, và nén ≥2:1 (thực tế ≥8:1). Dưới mức này thân không chạy được.
> - Đầu trên **cứng**: mỗi watt compute thêm vào thân làm `p` tăng, `f_pin` tăng, `γ` nở — và §5.3 cho thấy `γ` nở phi tuyến. **Compute biên không phải "thêm bao nhiêu cũng được, chỉ tốn pin"; nó ăn vào điều kiện hội tụ của cả thân.**
> - Vùng giữa: trích đặc trưng, nén, mô hình dự báo T5, theo dõi tha-thể T6 — đặt ở đâu là `⟦CTRL⟧`, và **nên đổi được theo nhiệm vụ** chứ không phải hằng số biên dịch sẵn.
>
> Đây là chỗ R-7 nối vào §5.1: một núm xoay mà hai đầu do **vật lý** giữ, không do sở thích thiết kế.

**Điểm vận hành: `⟦CTRL⟧`.**

---

## 10. HAI THAY ĐỔI SÂU NHẤT SO VỚI BẢN GỐC

**(1) Từ thân không-có-ràng-buộc-năng-lượng sang thân bị-năng-lượng-định-nghĩa.**

UDPA sụp kéo theo dây chuyền: mất luôn cơ sở cho Neutrino dump, micro-warp, và mọi spec "vô thời hạn / công suất cực cao". Khi thay bằng pin thật, **toàn bộ GEMs-v3 bị kỷ luật bởi ngân sách điện.** Mọi đánh đổi sau đều là chia ngân sách kWh.

**(2) Từ đầu cuối câm sang trí tuệ phân tán hai cư trú.**

Con số băng thông thật (8 Gbps) không tải nổi cảm biến thô full-rate → thân buộc phải xử lý cục bộ. Nhưng đây **không** là bước sang tự hành: cùng một trí tuệ, hai chỗ ngồi, phân vai theo *loại dữ liệu* (phản xạ tức thời ở thân; ký ức/mô hình/tích hợp dài ở hệ ngoài). Trụ 1 giữ về tinh thần, nới về cơ chế.

---

## 11. SỔ MỤC TREO *(tất cả đã đóng — giữ lại làm dấu vết)*

| # | Mục | Bản chất |
|---|---|---|
| **R-1** | **Cụm kết cấu / khối lượng / độ bền** — **ĐÃ ĐÓNG** | Đóng ở §5: vòng ghép khối lượng, điều kiện hội tụ `Σf < 1`, giáp định lượng theo mật độ diện tích, dải khối lượng thân 70–160 kg tùy điểm vận hành. Vật liệu cụ thể vẫn `⟦IMPL⟧` — nhưng kết luận không đổi dấu theo nó |
| **R-2** | **Cụm vận động & thao tác** — **ĐÃ ĐÓNG** | Đóng ở §5.6–5.7: bảng mô-men–tải–tầm với, và phát hiện chỗ thắt nằm ở **nguồn** (pin cấp 12–60 kW) chứ không ở actuator (nhận được 117–195 kW) |
| **R-3** | **Cụm vỏ / da / morph** — **ĐÃ ĐÓNG** | Đóng ở §8: biên độ mô-đun 2–30× và tốc độ vài–chục ms cho độ cứng lập trình; màu đổi trong giây; và hệ quả mới — **vỏ là ba lớp không kiêm nhau được**, cả ba ăn vào `m_ngoài` của §5.1 và cạnh tranh trực tiếp với giáp |
| **R-4** | **Cụm cảm biến** — **ĐÃ ĐÓNG** | Đóng ở §9: thông số từng kênh, tổng thô 15,8–67,2 Gbps, nén tối thiểu bắt buộc 2:1 → 8:1. Hệ số xúc giác "100×" đã được **chốt lại thành cách đọc theo năm trục** (§9.1), và §3.7 đã sửa theo — mật độ ngang người ở vùng tinh, vượt 20–100× ở băng thông thời gian |
| **R-5** | **Định danh phiên bản** — **ĐÃ ĐÓNG** | Chuỗi mang tên trần **`GEMs`**; "GEMs-X01" khai tử; số phiên bản (v2, v3, …) là trục riêng *bên trong* chuỗi. Vật thể vào corpus và xin DOI (Zenodo) là **kho GEMs hoàn chỉnh**, không phải bản nháp này. *Phía RSIL không còn gì để đồng bộ:* en-v1 đã gỡ sạch tham chiếu GEMs và thay §8 bằng platform contract tổng quát, nên mục treo đối ứng bên đó tự tiêu |
| **R-6** | **Công suất sàn mạch cảnh giác** — **ĐÃ ĐÓNG** | Đóng ở §4.8. Kết luận ngược với giả định của §4.3: **mạch cảnh giác không phải số hạng chi phối** — tự phóng điện của pin (1–3%/tháng ≈ 56–167 mW trên pack 4 kWh) lớn hơn nó khoảng ba bậc. Thời gian ngủ sâu ~4 năm, do hóa học pin chặn chứ không do mạch |
| **R-7** | **Tỉ lệ compute thân/ngoài** — **ĐÃ ĐÓNG** | Đóng ở §9.5: núm xoay có hai đầu mút **cứng** do vật lý giữ — đầu dưới là vòng ≥500 Hz, phản ứng ≤10 ms và nén ≥2:1; đầu trên là `p` (W/kg) ăn thẳng vào điều kiện hội tụ `Σf < 1` của §5.1. Vùng giữa vẫn `⟦CTRL⟧` và nên đổi được theo nhiệm vụ |
| **R-8** | **Cụm dấu vết thân** — **ĐÃ ĐÓNG** *(đóng ở §7)* | Sinh từ RSIL-en-v1 §8, §13.3 và Phụ lục A-1/A-2. Hai đòi hỏi hội tụ về một cơ chế phần cứng: **(a) chứng thực toàn vẹn cảm biến/actuator** — RSIL cấp *triệu chứng* qua log nhưng nói thẳng nó "không phải phép soi", và giao phép soi cho nền tảng; **(b) dấu vết biên độ vật lý** ở điểm tiếp xúc người — RSIL từ chối thêm bất biến thứ chín, tách rành *dấu vết* (trong vòng) khỏi *chuẩn để phán* (bên thứ ba). Khai báo biên độ đo được **không** vi phạm §0: đó là khai báo năng lực, không phải cắt spec vì đạo đức. Cụm này gánh luôn **E4** và **C5** đang thiếu ở §6.1 |

---

*Kết thúc bản làm việc. **Bảy cụm đã đóng; sổ mục treo R-1…R-8 đã đóng hết.** Bản v3 sẵn sàng làm tài liệu tham chiếu cho việc dựng kho GEMs.*
