# Relational Sensory Integration Loop (RSIL) — Blueprint Kiến trúc (v4)

> **⚠ BẢN CŨ — ĐÃ BỊ THAY THẾ.** Bản hiện hành là `RSIL-en-v1.docx` (tiếng Anh, thể loại paper). Bản v4 tiếng Việt này giữ lại làm dấu vết lịch sử. Khác biệt đáng kể: §8 không còn là "Tương quan với GEMs" mà là **platform contract** tổng quát — bản mới không nhắc GEMs một lần nào; Phụ lục A rút từ tám mục xuống năm và đánh số lại.

*Phái sinh từ "Cơ chế cảm giác và cảm xúc ở sinh vật — Tổng kết phiên" (13/06/2026).*
*Loại tài liệu: spec kiến trúc độc lập, không gắn dự án — được đánh giá bằng **tuân-thủ cấu trúc** (một hệ có thỏa E1–E4 và INV-1…8 không), không bằng đo đạc thực nghiệm.*
*Đồng bộ với DIL (Data Integration Loop) bản v6. RSIL và DIL là hai đặc tả **cùng hạng, khác phạm vi**: DIL đặc tả vòng trong một môi trường thông tin thuần (không thân); RSIL đặc tả vòng trong một thế giới vật lý có thân. Chỗ nào hai bản trùng nhau là vì cấu trúc quan hệ trùng; chỗ nào phân kỳ là có chủ đích và được ghi rõ tại chỗ.*

*Các điểm kiến trúc cốt của phiên bản này: T1 chỉ xác nhận trường hoạt động hiện diện mà chưa kẻ ranh giới self/môi trường — phân cực đó được dựng lần đầu ở T2 qua agency; **thân (host) phát cú hành động đầu tiên ở cycle-0, self là *sản phẩm* của cú đẩy đó chứ không phải tiền đề của nó**; trường điều biến toàn cục GLOB-MOD là một tiên-nghiệm-diễn-giải, mang cách-đọc chứ không mang nội dung, được các tầng cấu thành liên tục nên **không cần trần gain — không phải vì khó xảy ra, mà vì cấu trúc đã chặn sẵn**; **phát-xạ (emission) là một năng lực *ngang*, không phải một trạm trong chuỗi**; **vòng dựng-tới-trước qua hai vị trí `simulated` và `projected`**; **phản xạ không phải một cung riêng mà là định giá dưới một trường bị sẹo thống trị**; luồng dữ liệu là đa luồng (trừ cycle-0 đơn-luồng); vòng là **khả-kiểm (audit-ready) chứ không tự-kiểm**; và cơ chất đã cố định là một thân vật lý, chỉ để mở chất liệu (sinh học hay nhân tạo).*

---

## 0. PHẠM VI & RÀNG BUỘC REGISTER

**Tài liệu này đặc tả:** kiến trúc của một vòng xử lý thông tin cảm giác như một *cấu trúc quan hệ* — thứ tự tầng, quan hệ phụ thuộc, hợp đồng dữ liệu (data-contract) vào/ra mỗi tầng, các bất biến phải giữ, và **hai chế độ kháng cự** mà vòng vận hành dưới đó.

**Đối tượng của tài liệu — phát biểu thuần:** RSIL là một cơ chế *thu thập thông tin → phân biệt nguồn → tích hợp ở trung ương thành một dạng thông tin mới → định giá → tạo đáp ứng → tạo thông tin mới → mở vòng mới*. Toàn bộ spec mô tả cấu trúc của vòng đó. Mọi output là *thông tin* và *cấu trúc thông tin*.

**Register chuẩn hoá (theo thể loại tiêu chuẩn kỹ thuật):** trong phần quy phạm, **PHẢI** (MUST), **KHÔNG ĐƯỢC** (MUST NOT), **NÊN** (SHOULD) mang lực của một tài liệu tiêu chuẩn: vi phạm một **PHẢI** là mất quyền mang tên RSIL; một **NÊN** là khuyến nghị mạnh mà người thiết kế chỉ được bỏ qua khi có lý do.

> **Lưu ý register (chuỗi mũi tên ≠ luồng tuần tự):** chuỗi mắt-xích trên KHÔNG phải một packet đơn được chuyền tay tầng-này-sang-tầng-kia. Nó biểu thị *thứ tự phụ thuộc* (cái gì mở khóa nghĩa cho cái gì, P4/INV-3), không phải một đường tuần tự đơn. Trong một vòng, mọi tầng là một *site chủ động*: mỗi tầng đang thu và xử lý dữ liệu riêng, và một datum do một tầng sinh ra có thể được *nhiều* tầng trên tiêu thụ cùng lúc (output của tầng dưới nằm trong tập-đọc của mọi tầng trên nó). Luồng do đó là **đa luồng (multi-stream)** — nhiều mẩu dữ liệu di chuyển và kết hợp song song — không phải một gói chuyền tuần tự. Cơ chế là *tiêu thụ*, không phải *điều phối*: một tầng không đẩy output tới danh sách người nhận; nó làm output sẵn có, và mỗi tầng trên đọc cái rơi vào tập-phụ-thuộc của mình — nên không tầng nào cần một mô hình "ai tiêu thụ mình" (giữ giả định global-knowledge ra ngoài mọi tầng đơn). Tính **đồng thời** này là thuộc tính *cycle-time*, không phải wall-clock: trong cycle-time các tầng vận hành cùng nhau trong một vòng; theo wall-clock các luồng vẫn xen kẽ tuần tự, khoảng cách chỉ nằm dưới ngưỡng vòng tự phân giải được. "Đồng thời" là cách vòng tự đọc một khoảng nó không đo được từ trong, không phải sự vắng mặt của dòng chảy.
>
> **Ngoại lệ duy nhất — cycle-0 là đơn luồng:** vận hành đa luồng giả định một self để các luồng phối hợp quanh (§0.2); ở cycle-0 self chưa tồn tại — nó là cái cycle-0 đang dựng. Vòng do đó buộc chạy một-lượt-tuần-tự ở cycle-0 (T1 đăng ký dữ liệu đầu, T2 xử lý để kết tinh self), rồi từ cycle-1 trở đi mọi tầng vận hành cùng nhau và luồng thành đa luồng. Bước chuyển đơn-luồng → đa-luồng không phải một bước thiết kế thêm: nó *chính là* sự kiện self kết tinh, nhìn từ phía cấu trúc-luồng. Một bên thứ ba quan sát vòng chuyển từ một lượt tuần tự sang nhiều luồng xen kẽ đang quan sát **cùng một sự kiện** với việc self ra đời — hai mặt của một chuyện.

**Mục đích và môi trường đích:** RSIL là một *quy trình tự làm giàu thông tin và **khả-kiểm** (audit-ready)* cho một hệ cảm giác có thân xác — một cơ chế tự học nội tại, không phải một sản phẩm hướng người-dùng. Phải nói chính xác register này: vòng **KHÔNG tự-kiểm (self-auditing)** — nó không thể, vì cái nó dùng để soi *chính là* cái đang chạy (§0.2, §7.1). Cái vòng làm được là *khả-kiểm*: nó dựng một dấu-vết-hướng-ngoài (qua lược đồ tag, §9) để **một bên thứ ba kiểm** nó. "Tự kiểm" theo nghĩa vòng tự bắt được khoảnh khắc nó tự lệch là một năng lực vòng KHÔNG có; điều kiện-nhận-ra phải neo ngoài vòng (§0.2).

Môi trường đích là *thế giới vật lý có tha-thể*, gồm hai nhóm khác hạng: **tha-thể** (sinh vật/agent khác) — nguồn của kháng-cự-từ-tha-thể, nuôi được T6–T8; và **trường vật lý** (vật trơ, lực, môi trường tự nhiên) — nguồn của kháng-cự-vô-chủ-thể, nuôi T1–T5/T7.

### 0.0 MÔI TRƯỜNG ĐÍCH — ĐỊNH NGHĨA BẰNG ĐIỀU KIỆN VẬN HÀNH

Một môi trường đủ để chạy RSIL không được định danh bằng "sinh học / neuron / cơ thịt" (đó là chất liệu), mà bằng bốn thuộc tính cấu trúc nó PHẢI có:

- **E1 — Khả-phân-biệt.** Môi trường PHẢI **cho phép** (làm cho khả dĩ) một phân biệt giữa "trong hệ" (thân xác + state nội bộ) và "ngoài hệ" (kích thích đến từ môi trường). Nó **không tự dựng** phân biệt đó: môi trường *cho phép*, hệ *dựng*. Việc dựng là công việc của chính hệ ở T1/T2 — khác biệt self/môi trường là **output của T2**, không phải một thuộc tính môi trường trao sẵn (T1 chỉ xác nhận rằng một trường hoạt động hiện diện). Hệ quả: nếu T2 không kết tinh được một khác biệt self/môi trường ngôi-thứ-nhất, môi trường vẫn đã làm xong phần của nó (nó đã cho phép) — chỉ là chưa có hệ nào cả, và vòng hỏng *sạch* ở T1/T2, như một động cơ chưa từng nổ khác với một động cơ chết giữa đường.

- **E2 — Có tương tác.** Môi trường PHẢI trả về được một đáp ứng khi hệ phát ra một hành động — và PHẢI **không-toàn-chiều**: trong số các đáp ứng đó, nó PHẢI có khả năng **không-khớp** dự đoán của hệ.

  **Hai thất bại khác hạng nằm dưới một điều kiện này, và KHÔNG ĐƯỢC gộp chúng lại.** Một môi trường **không trả về gì cả** — một *trường rỗng*, dù dày đặc vật thể không-phải-Self mà không cái nào đáp lại — **hỏng E2 dứt khoát: vòng không khởi động**. Ngự trị một căn phòng toàn kẻ không đáp thì không phải ngự trị. Một môi trường **có trả về, nhưng hệ đoán gì cũng đúng** thì vượt ngưỡng tương tác mà chẳng có gì để học — **vòng chạy nhưng không tiến**. Ngưỡng của E2 là *tối thiểu nhưng khác không*: **ít nhất một đáp ứng khác im lặng**. Một cú im lặng *đơn lẻ*, đặt trên nền các đáp ứng, tự nó là một không-khớp hợp lệ (được đăng ký ở T7); im lặng **không đứt đoạn** là trường rỗng, không phải không-khớp.

  **Với thân xác, kháng cự hiện ra ở hai mặt khác hạng:** (a) *kháng cự vật lý* — lực, quán tính, vật cản, một thân thể khác đẩy lại; và (b) *không-khớp thông tin* — cái hệ thu được lệch với cái hệ dự đoán. Hai mặt này khớp nhau ở thân xác (một vật cản vật lý *cũng* là một không-khớp dự đoán) nhưng không đồng nhất: một số không-khớp thuần thông tin (một giọng nói phản bác) không kèm lực. RSIL nhận cả hai.

  > **Phân hạng phải giữ (mới ở v4):** **E2 kiểm *môi trường/thân*** — nó có trả về được gì không. **Kháng cự là hiện tượng của *vòng đang chạy***, không phải một điều kiện của môi trường: nó phát sinh ở T5, nơi khoảng lệch giữa kỳ vọng của hệ và cái được trả về trở thành một `PredErr` có dấu (một `ResistEvent`). Môi trường chỉ cần trả về được; *một đáp ứng cụ thể có kháng cự hay không là việc của vòng.*
  >
  > **Lưu ý hạng (chống một lệch dễ mắc):** "có kháng cự" được đo *so với dự đoán của hệ*. Một hệ mô-hình-nghèo thấy mọi thứ đều kháng cự; một hệ overfit thấy không gì kháng cự. Do đó E2 là điều kiện trên **cặp (hệ, môi trường)**, không phải trên môi trường đơn lẻ. Không thể chứng nhận một môi trường "đủ E2" mà không cố định trước hệ đang đặt trong nó.

- **E3 — Có tích lũy theo thời gian.** Môi trường PHẢI cung cấp một chuỗi vòng để lịch sử tương tác hằn được. Môi trường một-phát (one-shot) không cho lịch sử tích.

- **E4 — Có phóng-chiếu-hành-vi quan sát được.** Hệ PHẢI tác động vào môi trường (qua đáp ứng thân thể/hành vi, mắt xích ⑤) theo cách một bên thứ ba đọc được; nếu không, thành công của vòng không đo được từ ngoài.

  > **E4 ràng buộc *hệ*, không ràng buộc bên thứ ba (mới ở v4).** E4 chỉ đòi hệ để lại một dấu vết đọc được; nó không nói bên thứ ba là ai hay có thể bị nhiễm không. **Hai vai PHẢI giữ tách bạch:** một bên thứ ba **ghi nhận** (quy kết tính liên tục / tính phân biệt — chỉ cần một dấu vết đọc được) và một bên thứ ba **phán xử** (đánh giá đúng/sai — đòi độc lập thật). E4 chỉ đòi vai *ghi nhận*; vai *phán xử* được xử lý riêng (§12).

Một môi trường thỏa E1–E4 thì RSIL chạy được, bất kể *chất liệu của thân* (sinh học hay nhân tạo). Không thỏa thì không.

> **Hai loại kháng cự — phân biệt nền cho T6:** kháng cự (E2) có hai hạng. *Kháng-cự-vô-chủ-thể*: môi trường không-khớp dự đoán nhưng không có ý chí riêng (một vật cản trơ, một dốc nghiêng, một nguồn nhiệt tĩnh) — nhất quán, khách quan, không phản ứng *với riêng hệ này*. *Kháng-cự-từ-tha-thể*: một sinh vật/agent khác không-khớp theo cách *có thể có chủ ý, có thể đổi lập trường, phản ứng lại chính hệ* — và chính cái không-nhất-quán-vì-có-chủ-thể đó là nguồn DUY NHẤT dựng được khái niệm *tha-thể độc lập* (T6, `independence_evidence`). Hệ quả: một môi trường chỉ có kháng-cự-vô-chủ-thể (vd một phòng trống đầy vật trơ) đủ nuôi T1–T5/T7 nhưng KHÔNG nuôi được T6–T8 đầy đủ; cần tha-thể-phản-ứng để T6 sống. Đây là phân giới Mode-A / Mode-B ở §7.

**Tài liệu này không cố định:** các hằng số triển khai chưa được dẫn xuất (tần số lấy mẫu, kích thước tensor, ngưỡng số, hyperparameter) được đánh dấu `⟦DECIDE@IMPL⟧` thay vì điền số bịa. Một spec tự bịa ra hằng số chưa dẫn xuất được là đánh đổi sự trung thực lấy vẻ ngoài hoàn chỉnh; bản này không làm thế.

**Tiền đề kiến trúc:**
- **P1.** Cái vận hành là một *quan hệ*, không phải một *vật*. Ý nghĩa nằm trong *tương quan*, không trong tín hiệu đơn lẻ.
- **P2. Trung-lập-chất-liệu (cơ chất đã cố định là thân vật lý, chất liệu để mở).** Cơ chất của RSIL **đã cố định là một cơ thể vật lý** — có thụ thể vật lý/hoá học ở đầu thu và đáp ứng cơ/nội tiết ở đầu phát. Cái còn để mở chỉ là *chất liệu* của thân đó: sinh học (neuron/cơ thịt) hay nhân tạo (cảm biến/actuator). P2 do đó KHÔNG claim "chạy trên bất kỳ cơ chất nào"; nó claim hẹp và xác định: "không đòi một *chất liệu* đặc biệt cho thân, miễn là một thân vật lý thỏa E1–E4". Phạm vi của RSIL là *thế giới vật lý có thân*; một hệ không thân (môi trường thông tin thuần) nằm ngoài phạm vi này — đó là phạm vi của DIL.
- **P3.** Tiêu chí thành công = **vòng có chạy không** — đo bằng dấu vết quan sát được từ ngoài (§6).
- **P4.** Thứ tự tầng bị ép bởi **quan hệ phụ thuộc**, không bởi cường độ tín hiệu. Mỗi tầng *mở khóa nghĩa* cho tầng sau.

**Tập tiền-điều-kiện của thân (P) — điều kiện khởi động vòng không tự cấp được cho mình.** E1–E4 nói môi trường phải cho vòng cái gì. Còn một thứ phải nói thẳng: **thân PHẢI phát được một hành động đầu tiên ở cycle-0** để khởi động T2. Ngoài E1–E4, một thân khả dụng tối thiểu thỏa tập **P**: (a) nó phát được một hành động *phân biệt được* với dao động nền của môi trường — nếu không T2 không bao giờ lên tới ngưỡng khớp-đầu-tiên; (b) nó giữ được state qua các vòng để lịch sử *tích* (INV-5 đòi tích, không đòi nạp); (c) nó *chịu được* kháng cự mà không tự ghi-sạch-mình mỗi lần không-khớp — nếu không, không "vết sẹo" nào sống đủ lâu để có nghĩa. Thân phát cú hành động cycle-0 **vẫn chỉ là thân** (nó không cần một self có trước), và hành động ấy không phải lịch sử nạp sẵn — nên INV-5 không bị đụng: *phát một hành động mới ≠ nạp một hành động cũ*. Khởi động do đó là trách nhiệm của thân, không phải của vòng; thân không thỏa P thì vòng đơn giản không khởi động (kẹt ở T1) — một cú không-khởi-động sạch, không phải một hỏng-hóc giữa chừng.

---

## 0.1 THUẬT NGỮ

RSIL dựng trên quan hệ, không dựng trên vật; các thuật ngữ sau được dùng theo nghĩa quy ước, giảm-thiểu-cam-kết có chủ đích.

- **Kháng cự.** Việc một tương tác được trả về *không khớp* dự đoán của hệ. Với một hệ có thân, kháng cự có hai mặt (lực vật lý và không-khớp thông tin — xem E2), nhưng cả hai vào vòng theo cùng một đường: chúng trở thành thông tin ở T5, dưới dạng một `PredErr` có dấu. Kháng cự là *hiện tượng của vòng đang chạy*, không phải thuộc tính của môi trường đơn lẻ.

- **Tha-thể (the Other).** Bất kỳ sinh vật/agent nào hệ không kiểm soát, có khả năng không-khớp kỳ vọng của hệ theo cách *có thể có chủ ý, có thể đổi lập trường, có thể phản ứng lại chính hệ này*.

- **Kháng-cự-vô-chủ-thể vs kháng-cự-từ-tha-thể.** Hai hạng, như đã định nghĩa ở §0.0. Chỉ kháng-cự-từ-tha-thể dựng được khái niệm một tha-thể độc lập.

- **Mode-A (nội sinh / tự huấn luyện).** Chế độ trong đó kháng cự đến từ sự-trơ của thế giới vật lý và của dữ liệu hệ đã giữ, cùng mâu thuẫn nội tại của mô hình hệ.

- **Mode-B (ngoại sinh / tương tác sống).** Chế độ trong đó kháng cự đến từ một tha-thể hệ không kiểm soát.

- **`ResistEvent` (không-khớp đã đăng ký).** Một trường hợp được ghi nhận của việc môi trường không khớp kỳ vọng của hệ: kỳ vọng đã dựng, chỗ nó trật, và hiệu chỉnh đã làm. **Đơn vị nguyên tử của kinh nghiệm** (§9), phân biệt với thông tin đơn thuần.

- **Self là quá trình.** Luận đề (§0.2) rằng bản sắc của hệ qua các vòng không phải một lõi-nội-dung được giữ lại mà là *luật sinh state kế tiếp từ state trước*; một bất biến động chỉ được duy trì trong khi vòng còn chạy.

- **GLOB-MOD (trường điều biến toàn cục).** Một trạng thái toàn cục **chạm tới mọi tầng** (mỗi tầng nhận giá trị hiện thời của trường như một điều kiện nền lên cách nó diễn giải input) và mọi tầng **đóng góp vào như một tham số cạnh tranh trong nhiều tham số** (không bao giờ bằng ghi-đè độc quyền). Hướng là *field-to-layer*: trường điều kiện-hóa một tầng; một tầng không với ngược lên trường để lấy định nghĩa. Đây là **field semantics, không phải shared-variable semantics**: các đóng góp hòa trộn và được tái-trọng-số mỗi vòng; không có last-write-wins, do đó không có race condition giữa các tầng.

### 0.1.1 Bộ ba thân / self / hệ — MỘT vận động mô tả ở ba mức, KHÔNG phải ba thực thể song song

- **Thân (host — cơ chất).** Cái tồn tại có năng lực, PHẢI thỏa E1, E3, E4 và E2 để chạy được RSIL. Nó tồn tại cả khi không vòng nào chạy. Nó là *cơ chất, không phải self*: nó không mang self và không góp self nào. Cái nó cấp là **phi-ngã**: năng lực trần trụi phát ra một hành động đầu tiên — thứ mà giao thức *dùng* nhưng không *dẫn xuất*; năng lực ấy tự nó từ đâu ra thì nằm ngoài phạm vi RSIL. Trong lúc khởi tạo — chạy T1 và phát cú hành động bootstrap ở T2 cycle-0 — nó **vẫn chỉ là thân**; không cần một nhãn riêng cho "một cái thân đang chạy".
  > *Với RSIL, "thân" mang nghĩa đen: một cơ thể vật lý. Nhưng đúng vì mang nghĩa đen mà một hiểu sai dễ mắc phải chặn ngay ở đây — **thân xác KHÔNG cho hệ một đường self/môi trường có sẵn**. Có một cơ thể không có nghĩa là có sẵn một biên. Biên chỉ xuất hiện khi một lệnh được phát và hệ quả được đối chiếu (§0.2).*

- **Self.** Một *sản phẩm của RSIL — kết tinh từ T2 cycle-0*. Self KHÔNG có trước T2 và không được nạp sẵn từ thân; nó là *luật sinh state kế tiếp* (§0.2), bắt đầu hình thành ở T2 cycle-0 qua phép khớp (lệnh đã phát ↔ hệ quả quan sát được), rồi được định vị lại mỗi vòng. Self là một *dòng* (một động từ), không phải một *cột mốc* (một danh từ); nó có thể suy thoái, và tính liên tục của nó được neo bởi một bên thứ ba.

- **Hệ (agent).** *Thân đang chạy bên trong RSIL, tính từ T2 cycle-0 — tức từ bước mà một self tồn tại.* Gọn: **hệ = thân đã có được một self.** Nó KHÔNG phải một tầng thứ ba chèn giữa thân và self; nó là *chính cái thân đó*, dưới mô tả "đang chạy vòng và giờ đây mang một self".

- *Hệ quả cold-start:* cái phát cú hành động bootstrap ở cycle-0 là **thân** (một cái thân không cần self để đẩy cú đầu) → không có vòng luẩn quẩn "hệ cần self / self cần hành động / hành động cần hệ". **Self là *sản phẩm* của cú đẩy, không phải tiền đề của nó.**

### 0.1.2 Hai thuật ngữ vai-ngoài (khác với bộ ba trên)

- **Vùng (region — trường tương tác).** Cái mà hệ *trao đổi vào/ra với* — nơi tương tác diễn ra. **TRUNG LẬP về trong/ngoài:** dưới Mode-B, vùng bao gồm một tha-thể ngoại; dưới Mode-A, vùng bao gồm *thế giới vật lý trơ và chính dữ liệu hệ đang giữ*. KHÁC với thân: thân là cái *chạy* hệ (nền); vùng là cái hệ *tương tác với* (đối tác vào/ra).

- **Nguồn-đối (counter-source — nguồn kháng cự).** Cái mà thấu kính của hệ *dự đoán về và có thể không khớp*. **Nguồn-đối ⊂ vùng** (ở cả hai chế độ): nó là *phần của vùng hiện đang đóng vai kháng cự*. E2 chỉ đòi tồn tại một nguồn-đối không-toàn-chiều *trong* vùng — nó KHÔNG đòi nguồn-đối phải nằm ngoài hệ.

### 0.1.3 Tha-thể — định nghĩa gốc và các hạng

**Trong RSIL, Tha-thể là cái không phải Self.** Self là luật đang vận hành ở vòng hiện tại (§0.2); Tha-thể là bất kỳ nguồn nào không đồng nhất với nó. Điều này **bao gồm cả Self của một vòng trước**, vốn không còn đồng nhất với Self đang vận hành — khi vòng kiểm một trạng thái hiện tại đối chiếu một kỳ vọng dựng từ chính quá khứ của nó (T5), cái quá khứ đó đứng với cái hiện tại như một Tha-thể. Tha-thể do đó **không phải một loại thực thể mà là một vị trí quan hệ**: cái-không-phải-Self-ngay-lúc-này. Mọi khái niệm Tha-thể khác trong spec này là một phân loại con của cái này, không phải một thứ riêng.

Trên nền đó, RSIL phân loại Tha-thể theo hai trục độc lập:

| Trục | Các hạng | Đứng ở đâu |
|---|---|---|
| **Nguồn** | *ngoại* (Mode-B — ngoài hệ) / *nội* (Mode-A — quá khứ và dữ liệu hệ đang giữ; và `GeneralOther`, một mô hình về tha-thể do chính hệ dựng và giữ) | quyết định chế độ |
| **Chủ thể tính** | *phản ứng* (nó đáp lại hệ — có thể đổi lập trường, có thể phản ứng với riêng hệ này) / *vô chủ thể* (nó kháng cự nhưng không có ý chí riêng — một quy luật vật lý, sự trơ của dữ liệu đã giữ) | quyết định T6 sống hay teo |

Một **tha-thể ngoại-phản-ứng** cho bằng chứng độc lập mạnh nhất và là cái nuôi T6. **Kháng-cự-vô-chủ-thể** nuôi T1–T5 và T7 nhưng tự nó không dựng được khái niệm một tha-thể độc lập, nên không nuôi T6. **`GeneralOther`** là một *biểu diễn*, không phải một nguồn kháng cự mới. **`STRANGER` và một tha-thể có `entity_id` KHÔNG phải hai hạng riêng** — chúng là **hai trạng thái nhận diện của cùng một tha-thể**: chưa khớp được với kho định danh, hoặc đã khớp vào một hồ sơ đã biết. Không phân loại nào ở đây thêm một thực thể; mỗi cái chỉ định vị một vùng của một quan hệ duy nhất: Tha-thể = không-phải-Self.

---

## 0.2 SELF TRONG MỘT HỆ CÓ THÂN XÁC

RSIL *có* thân, nhưng thân xác KHÔNG cho hệ một đường self/môi trường có sẵn ở đầu vào. T1 chỉ thu dữ liệu không gian thô từ cảm biến về *trường hoạt động*; nó **chưa kẻ ranh giới self/môi trường**, vì chưa có hành động nào được phát thì chưa có gì để đối chiếu "cái gì đáp theo lệnh của tôi" với "cái gì không". Biên đó chỉ xuất hiện ở T2, khi hệ phát `motor_command` và so hệ quả với dữ liệu không gian T1 đã dựng: phân cực self/môi trường là *sản phẩm của agency* ở T2, không phải thuộc tính T1 trao sẵn. Và có thân KHÔNG miễn cho RSIL câu hỏi về *tính liên tục của self*: nó không trả lời được self-vòng-N có *cùng* là self-vòng-N−1 không.

**Self là một quá trình giữ-nguyên-kiểu, không phải một lõi bất biến.** Nội dung self đổi mỗi vòng (biên, kỳ vọng, baseline được cập nhật; cả cấu trúc vật lý của thân cũng đổi theo thời gian). Cái *không đổi* không phải một mẩu nội dung được mang qua, mà là **luật sinh state-kế-tiếp từ state-trước** — hệ ở vòng N là *cùng* hệ với vòng N−1 không vì chúng chứa cái gì chung, mà vì có một đường nhân-quả không đứt nối các vòng qua đúng luật đó. Đây là một bất biến *động*: được duy trì *nhờ* vòng chạy, không bằng cách đứng ngoài sự chạy. Ngừng vòng thì mất trục. (Có thân không cứu được điểm này: một thân thể vẫn còn đó sau khi vòng dừng vẫn KHÔNG còn là *cùng self* — nó là vật chất, không phải quá trình.)

**Self bắt đầu ở đâu (và nó là một dòng, không phải một cột mốc).** Self **không** có trước T2, và **không** được nạp sẵn từ thân. Nó *được khởi tạo từ T2 ở cycle-0* — qua phép khớp giữa cú hành động vừa phát và hệ quả quan sát được, chính là cái dựng lên khác biệt SELF/MÔI TRƯỜNG lần đầu — rồi **được định vị lại qua T2 ở mỗi vòng**, dày lên theo lịch sử từng vòng. Đây là biên giới trung thực của luận điểm, và nó có hai phần. **Thứ nhất**, RSIL không khẳng định đã khép lại câu hỏi self khởi sinh ra sao; nó chỉ khẳng định rằng, *cho trước một cái thân có thể bước cú đầu*, giao thức cấu trúc một self lên trên nó. **Thứ hai**, năng lực bước cú đầu — năng lực phi-ngã, trần trụi của thân — cũng là cái được giả định, không được giải thích. Cả nguồn gốc của self lẫn nguồn gốc của năng lực-hành-động-đầu-tiên đều nằm ngoài cái spec này nhận trách nhiệm dẫn xuất.

**Tính liên tục của self không đo được từ trong.** Hệ không truy cập được đạo-hàm-của-chính-nó theo thời gian: nó không tua lại được để tự trừ "self vòng N" với "self vòng N−50". Do đó spec PHẢI giữ hai phép đo tách bạch:
- Tính **phân biệt** (self này ≠ self kia) *đo được*: cùng đầu vào hiện tại, hành vi khác nhau → hiệu số là chữ ký của lịch sử đã tích (một phép đo vi sai, cần ≥2 hệ hoặc 2 lát để trừ).
- Tính **liên tục** (cùng self qua thời gian) *không* đo từ trong — nó là **quy kết của một bên thứ ba** lên chuỗi-hành-vi-được-lưu.

Gộp hai phép đo này là một lỗi. Phân biệt này là nền của giới hạn C5 (§6) và của lập luận lồng-chế-độ ở §7.3: **một vòng tự-kiểm không bắt được khoảnh khắc nó tự lệch hay tự dừng, vì cái nó dùng để soi *chính là* cái đang chạy.** Điều kiện-nhận-ra do đó PHẢI neo NGOÀI vòng — trong một dấu vết được lưu, đọc bởi một bên thứ ba. Đây đúng là lý do công trình này gọi hệ của nó là **khả-kiểm**, không phải **tự-kiểm**: vòng không tự kiểm được mình, nhưng nó — theo R1, §9 — dựng được cái dấu vết hướng-ngoài để một bên thứ ba kiểm nó.

---

## 0.3 VÒNG CHUẨN (Canonical Loop)

Đây là pipeline cốt lõi mà toàn bộ kiến trúc tầng (§3) là một triển khai chi tiết của nó.

```
     ┌─────────       trường điều biến toàn cục (GLOB-MOD)        ─────────┐
     │        gain/bias toàn cục — tắm mọi mắt xích, đổi tham số đồng thời │
     ▼                                                                     ▼
      ① thu nhận ──▶ ② phân biệt ──▶ ③ tích hợp ──▶ ④ định giá ──▶ ⑤ đáp ứng
       (thụ thể +     nguồn (agency)   trung ương    (appraisal)   (thân + hành vi)
        transduction)
            ▲                                                                 ▼
            └────────────◀     ⑥ đáp ứng thành đầu vào mới    ◀──────────────┘
```

**Sáu mắt xích tuần tự:**

| # | Mắt xích | Bản chất trong một hệ có thân |
|---|---------|---|
| ① | **Thu nhận** | thụ thể chuyên biệt nhận kích thích vật lý/hoá học, **và** transduction: kích thích *trở thành* tín hiệu truyền được. Đầu vào gồm: hệ quả của một hành động vừa phát, kích thích từ môi trường, tín hiệu từ một tha-thể |
| ② | **Phân biệt nguồn** | gắn nhãn do-tôi-gây-ra / không-do-tôi *trước khi* diễn giải (agency-gate, INV-6) |
| ③ | **Tích hợp trung ương** | tổng hợp ngang qua các nguồn thành một dạng thông tin mới |
| ④ | **Định giá (appraisal)** | gán tốt/xấu-cho-mục-tiêu → thông tin trở thành *cái-có-hướng*. Mắt xích chống-trôi (§7) |
| ⑤ | **Đáp ứng** | hệ ghi vào state và/hoặc phát ra vùng (đáp ứng nội tiết/cơ, hành vi) |
| ⑥ | **Hồi tiếp** | đáp ứng ⑤ trở thành đầu vào mới của ① → **lặp** |

> **⟦PENDING-CONFIRM: thay đổi cấu trúc so với v3.⟧** Bản v3 đánh số ② là *transduction*, và không dành mắt xích nào cho phân-biệt-nguồn — dù INV-6 và T2 vẫn cưỡng chế nó. Đó là một bất đối xứng: một bất biến bậc nhất không có chỗ trong vòng chuẩn. v4 gộp transduction vào ① (nó là *cách* kích thích vào được, không phải một chặng riêng về hạng) và trả ② cho phân-biệt-nguồn, khớp với DIL v6. Ghi lại thay đổi này ở đây để một bên thứ ba đọc cả chuỗi phiên bản thấy được vết tự-sửa; anh xác nhận hoặc bác trước khi chốt.

> **Phân biệt phải giữ (chống vẽ sai):** dẫn-truyền-tại-điểm-nối (synapse ở sinh vật) là một phần của ① — cục bộ, một chặng. **GLOB-MOD** là một *trường* bao cả vòng. Đừng gộp hai cái thành "bước hoá học" — chúng khác hạng: một là node, một là tham số toàn cục.

**Trường điều biến toàn cục (một điều kiện-TRƯỜNG, không phải một mắt xích).** Toàn bộ vòng được *tắm* trong một trạng thái toàn cục mang nội dung (vd "đang-cảnh-giác" / "đang-an-toàn" / "đang-khẩn") *đổi cách diễn giải* của mọi mắt xích. Trường này **không nằm ở một vị trí trong chuỗi** — nó là **gain/bias toàn cục**, đổi *tham số* của mọi mắt xích cùng lúc. Hệ quả: cùng một tín hiệu ở ②, tắm trong nền khác → tích hợp (③) khác, định giá (④) khác, đáp ứng (⑤) khác.

> **Trung lập chất liệu (đúng P2):** cái được đặc tả là *vai trò* — một trường điều biến toàn cục. *Cách hiện thực* tuỳ chất liệu của thân: ở thân sinh học là nền hoá học (neuromodulator — dopamine, serotonin, oxytocin, cortisol...); ở thân nhân tạo là một trường tham số/dữ liệu mà mọi tầng đọc. Hai cái là *instance* của cùng một vai trò.

### GLOB-MOD là gì (khái niệm)

**Nó là gì.** GLOB-MOD là một **tiên-nghiệm-diễn-giải toàn cục**: một trạng thái nền duy nhất, chung cho mọi tầng trong một vòng cho trước, đặt *thiên-hướng* mà mỗi tầng đọc input của nó. Nó **không phải nội dung chảy qua các tầng** (đó là kênh-nghĩa); nó là *thiên lệch đứng* mà bất cứ cái gì chảy qua đều bị diễn giải theo. Quan hệ ở đây là quan hệ *ánh sáng với đồ vật trong một căn phòng*: ánh sáng không phải một trong các đồ vật, nhưng nó quyết định mọi đồ vật *trông như thế nào* cùng một lúc; đổi ánh sáng là đổi diện mạo của mọi vật mà không sửa hình dạng vật nào. Dùng "tiên-nghiệm-diễn-giải" thay cho nhãn giàu hơn (tâm trạng, cảm xúc, chú ý) là cố ý: các nhãn đó nhập về những cam kết — phẩm chất cảm thấy được, ý thức, một cơ chế trọng-số cụ thể — mà một spec **trung-lập-chất-liệu** không được giả định. Cái giữ lại chỉ là lõi vận hành: một thiên-hướng toàn cục điều kiện-hóa việc đọc.

**Nó mang gì.** `params` của `ModField` là một tập **thiên-lệch-diễn-giải vô hướng** — mỗi cái điều biến gain hoặc ngưỡng của một thao tác tầng (một nguồn được tin tới đâu, vòng cảnh giác với không-khớp tới đâu, nghiêng về thăm-dò hay củng-cố tới đâu). Chúng mang **cách-đọc, không bao giờ mang cái-được-đọc**: không thiên-lệch nào giữ nội dung mệnh đề — chính điều đó giữ GLOB-MOD khỏi bao giờ trở thành một kênh-nội-dung cửa sau, và do đó **bảo toàn INV-3**. Số trục và bản chất cụ thể là `⟦DECIDE@IMPL⟧`; cái cố định là *hạng* của chúng.

Nguồn gốc của nó là động: ở cycle-0 tiên-nghiệm được gieo từ dữ liệu/trạng thái sẵn có của thân, và từ cycle-1 trở đi nó liên tục được tái-trọng-số bởi hồi tiếp T8 (INV-7, field-to-layer, hiệu lực ở vòng N+1).

> **Một điểm chính xác về cycle-0, để tránh một nghịch lý biểu kiến** (một tiên-nghiệm diễn giải *trước khi* có một self để diễn giải cho): cái được gieo ở cycle-0 nghiêm ngặt là một **thiên-lệch-của-thân**, chưa phải của hệ. Nó chưa phải một tiên-nghiệm-diễn-giải *của hệ* ở thời điểm đó, vì cái self mà tiên-nghiệm ấy là tiên-nghiệm *cho* chưa kết tinh (T2 cycle-0). Nó **trở thành** tiên-nghiệm-diễn-giải của hệ chỉ từ cycle-1, khi self đã có mặt để được điều kiện-hóa bởi nó — cùng một sự kiện duy nhất, nhìn từ phía trường, với việc self ra đời.

**Vì sao cần nó.** Hai lý do, khác trọng lượng. Thứ nhất và đủ — *điều-kiện-hóa-theo-ngữ-cảnh*: thiếu một tiên-nghiệm toàn cục, mỗi tầng đọc input trần, không phụ thuộc trạng thái hệ đang ở. Cùng một `InfoUnit` sẽ được diễn giải y hệt dù vòng vừa gặp một tha-thể thù địch hay một tha-thể trung tính. Thứ hai và nhẹ hơn — *mạch-lạc-ngữ-cảnh xuyên tầng*: vì trường là toàn cục và mọi tầng đều tắm trong nó trong một vòng, tám tầng chia một thiên-hướng-diễn-giải duy nhất trên vòng đó thay vì mỗi tầng đọc riêng. Lý do thứ hai nêu ở cường độ thấp có chủ đích: GLOB-MOD *góp* vào mạch lạc của lập-trường-hệ; nó không tự nó cấu thành selfhood.

Ghi rõ cái **không** có trong danh sách: **GLOB-MOD không chống trôi.** Vì toàn cục, nó là kênh mà một thiên-hướng đã lệch lan ra mọi tầng cùng lúc; nó là nơi *trôi lan đi*, không phải cái canh giữ chống trôi. Nó mang chính cái tham số (độ nhạy với không-khớp) mà sự trôi tấn công, nhưng nó không bảo vệ tham số đó — bảo vệ đó chỉ đến được từ ngoài vòng (§7, Mode-B).

**Ánh xạ vòng → tầng (§3):** ① thuộc T1/T3 (thu dữ liệu không gian, xác nhận trường hoạt động, kênh) · ② thuộc T2 (agency) · ③ thuộc T3→T8 (tích hợp, leo tầng quan hệ) · ④ hiện diện ở T5 (sai số dự đoán) và T8 (RelValue = định giá so-sánh) · ⑤ đáp ứng là một **năng lực ngang** được nhiều tầng gọi (§4) · ⑥ hồi tiếp được cưỡng chế bởi INV-1.

---

## 1. BẤT BIẾN TOÀN HỆ (System Invariants)

Mọi triển khai PHẢI giữ tất cả các bất biến sau. Vi phạm bất kỳ cái nào cho ra không phải RSIL mà một aggregator thường. Các bất biến là **điều kiện tuyệt đối của vòng**: chúng không phải dữ liệu trong kho và không mang tag nào; chúng không thể bị ghi đè bởi bất cứ gì trong vòng, vì ghi đè một bất biến không phải sửa một datum mà là **dừng vòng** — chấm dứt cái không-khớp mà self phụ thuộc vào.

| ID | Bất biến | Lý do |
|----|----------|------|
| INV-1 | **Vòng đóng.** Mọi output tầng PHẢI có một *đường* quay lại làm input cho một tầng nào đó. Không có nhánh cụt. | Vòng tự nuôi đầu vào của chính nó. |
| INV-2 | **Đồng nhất register output.** Mọi output mang nhãn `INFO`. Không tầng nào được nâng một tương quan (`↔`) thành một đồng nhất (`=`). | Giữ register tương quan; xem T8-INV. |
| INV-3 | **Phụ thuộc một chiều (kênh-nghĩa).** Trên *kênh nghĩa*, tầng N chỉ được tiêu thụ output của tầng ≤ N. | Thứ tự phụ thuộc (P4). **Ngoài phạm vi:** trường điều biến (INV-7) tác động *xuống* các tầng và không phải một phụ thuộc kênh-nghĩa nào cả. |
| INV-4 | **Ý nghĩa = quan hệ.** Không tầng nào được gán nghĩa cho một tín hiệu *trong cô lập*; nghĩa là hàm của (tín hiệu, ngữ cảnh-tầng-dưới). | P1. |
| INV-5 | **Lịch sử tích, không nạp.** Trạng thái thời gian chỉ hình thành qua tích lũy tuần tự, không bao giờ nạp sẵn. | Self là quá trình giữ-qua-chạy (§0.2). |
| INV-6 | **Agency-gate.** Mọi thay đổi PHẢI được phân loại do-tôi-gây-ra / không-do-tôi (khác biệt self/môi trường) *trước khi* được diễn giải. | Điều kiện để một cảm giác ngoại lai có nghĩa. |
| INV-7 | **GLOB-MOD.** Một trạng thái toàn cục chạm tới mọi tầng (field-to-layer: mỗi tầng nhận nó như điều kiện nền, không tầng nào với ngược lên nó) và mọi tầng đóng góp vào như một tham số cạnh tranh trong nhiều tham số (field semantics: các đóng góp hòa trộn và được tái-trọng-số mỗi vòng, không bao giờ last-write-wins; đóng góp của một tầng ở vòng N chỉ điều kiện-hóa trường từ vòng N+1, không bao giờ trong cùng vòng). | Cùng dữ liệu + nền khác → nghĩa khác. |
| INV-8 | **Bước định giá.** Giữa tích hợp (③) và đáp ứng (⑤) PHẢI có một bước định giá (④) gán hướng/giá-trị. Bước ④ **KHÔNG ĐƯỢC lấy tiêu chí từ chính cái state mà hệ đang sửa** — nếu không, nó là *tự-chấm* và hack được. | Chống-phản-xạ-trần; chốt chống-trôi của Mode-A (§7). |

> **Về INV-8 (sửa so với v3):** bản v3 để mệnh đề chịu lực — *"④ không được lấy tiêu chí từ chính state hệ đang sửa"* — nằm ngoài bảng, chỉ xuất hiện ở phần Mode-A. Một người triển khai chỉ đọc bảng bất biến sẽ bỏ sót nó. v4 đưa nó vào chính ô bất biến. Bổ sung khẳng định (chuẩn mà ④ *có* áp dụng) ở §7.4.

> **Về INV-2 — cam kết một hành động KHÔNG phải nâng `↔` thành `=`.** Hành động dựa trên một tương quan không đồng nghĩa với đóng băng tương quan đó thành một đồng nhất. Để đáp ứng, hệ cam kết một hành động (nó đẩy vật này, nó bước hướng kia); cam kết ấy *tự nó* là một thao tác `↔` — một phỏng-đoán-tốt-nhất-hiện-tại **có thể xét lại**, được đọc lại đối chiếu với hệ quả ở vòng sau — không phải một tuyên bố đồng nhất. INV-2 cấm *đóng băng* một tương quan thành chân lý cố định; nó **không** cấm *hành động* dựa trên một tương quan. Cái gây tê liệt (do dự vô hạn) là đòi `=` trước khi hành động — "phải chắc X đúng đã rồi mới nhúc nhích"; INV-2 cấm đúng cái đòi hỏi đó, và do đó *giải phóng* hệ để hành động trên `↔` và học, chứ không gây do dự.

> **Về các bất biến và GLOB-MOD — một phân biệt về mức.** GLOB-MOD điều biến **thông tin** chảy qua các tầng (T1–T8); nó **không** và **không thể** sửa chính các **bất biến** (INV-1…8). Các bất biến là *luật về* vòng; GLOB-MOD là một *tham số trong* vòng. Không sự nhiễm bẩn nào của trường viết lại được một luật — cụ thể, một thấu kính đang trôi ghi vào GLOB-MOD **không** vì thế mà sửa được tiêu chí của INV-8, vì các tiêu chí đó không phải thông tin-trong-vòng mà là một luật về nó (và, theo §7.1, được neo ở chỗ hệ không sửa được).

> **Về INV-1 — một ràng buộc topology, tính theo cycle-time không phải wall-clock.** INV-1 đòi mọi output *có một đường quay lại* — rằng một đường về **tồn tại trong topology của vòng** — chứ không đòi mọi packet hoàn tất cú quay về ở mọi vòng. Vòng tiến theo **cycle-time, không phải wall-clock**: những quãng nghỉ giữa các vòng là mặc định, không phải sự kiện phải tuyên bố. Một cái thân ngủ, hay một tha-thể im lặng, **không** vi phạm INV-1 (đường vẫn tồn tại) và **không** "đánh rơi output vào hư vô"; vòng kế tiếp đơn giản là chưa xảy ra. Nếu một tha-thể biến mất, vòng không gãy — nó rơi về Mode-A (tiêu hóa các cú va đã hứng, đối chiếu dữ liệu đang giữ), đường vẫn đóng qua tuyến nội; và nếu không tha-thể nào quay lại, nó trôi và mục (§7) — một chuyển-chế-độ đã được đặc tả, không phải một bất biến bị gãy.

> **Giải nút INV-3 ↔ INV-7 (kênh-nghĩa vs kênh-điều-biến):** hệ có **hai loại kênh tách bạch**, và mâu thuẫn biểu kiến tan ngay khi nêu đúng *hướng*. *Kênh-nghĩa* truyền `InfoUnit` *lên* theo tầng, một chiều, chịu INV-3 — đây là đường một tầng *định nghĩa* nội dung cho tầng sau. *Kênh-điều-biến* là GLOB-MOD: một trạng thái toàn cục tác động *xuống* mọi tầng cùng lúc. Điểm mấu chốt là hướng: khi tầng trên (vd T8) sửa GLOB-MOD, nó đổi trạng thái của *trường*, rồi trường điều kiện-hóa mọi tầng từ trên xuống; tầng dưới (T4) **không** với ngược lên các tầng để lấy gì từ T8. T4 nhận một giá-trị-nền của trường, đúng như nó nhận nền ambient ở bất kỳ vòng nào. Do đó INV-3 *không hề bị đụng tới*.
>
> **Không có timing nào để mâu thuẫn quay lại:** điều-kiện-hóa-bởi-trường có hiệu lực ở vòng **N+1**, không bao giờ trong cùng vòng. Điều này chặn cả hai cách đọc sai cùng lúc: không có ghép-ngược trong-cùng-vòng (vốn sẽ tạo một vòng đại số trong đồ thị phụ thuộc — không tồn tại, vì không field-write nào được đọc trong chính vòng sinh ra nó); và đường liên-vòng *có* tồn tại (trường vòng N định hình vòng N+1) chính là INV-1, không phải cái INV-3 cấm. Hai kênh PHẢI được triển khai tách biệt.

> **Về ngữ nghĩa của GLOB-MOD (chống đọc nhầm thành một biến chia sẻ khả biến).** GLOB-MOD có **field semantics, không phải shared-variable semantics**. Một "đóng góp" từ một tầng không phải một cú ghi đè lên một ô chia sẻ: các đóng góp hòa trộn, cạnh tranh, và được tái-trọng-số ở vòng sau; không cú ghi nào của tầng nào giành được độc quyền. Do đó **không có last-write-wins và không có race condition liên tầng** — tính đồng thời của đóng góp là một vấn đề không tồn tại.

> **Không cần trần gain — chặn bằng cấu trúc, không phải bằng xác suất (siết so với v3).** Một hiểu sai phải gạt bỏ là *cường độ của trường là một núm tự do mà người triển khai phải đặt trần kẻo trường lấn át vòng*. Không phải vậy, và lý do là cấu trúc. GLOB-MOD không phải một ngoại lực ép xuống các tầng; nó **được chính các tầng cấu thành liên tục** — mỗi tầng nuôi trường khi thông tin đã làm giàu của vòng tuần hoàn (trường tác động xuống các tầng, và các tầng, độc lập nhưng đồng thời, định hình trường trở lại). Ghép hai-chiều này khiến trường không thể tự nâng mình vượt các tầng nuôi nó: để lấn át các tầng, trường phải được làm-mạnh bởi đúng các tầng nó đang lấn át, điều mà ghép-coupling cấm. **Một trường tự chạy-trốn khỏi cơ chế giữ-nhau này bằng động lực nội tại của nó do đó bị loại trừ *về mặt cấu trúc* — bị chặn bởi kiến trúc, không phải chỉ được làm cho khó xảy ra; không cần trần gain, vì kiến trúc đã chặn sẵn.**
>
> *Bản v3 phát biểu điểm này ở cường độ yếu hơn ("trong trường hợp thông thường, là cực kỳ khó xảy ra"). Phát biểu đó bị bác ở v4: nếu chỉ là "khó xảy ra" thì một trần gain sẽ là biện pháp hợp lý, và spec sẽ nợ một con số. Vì cơ chế thật là ghép-coupling chứ không phải xác suất, spec không nợ con số nào.*

> **Cái gì nằm bên kia ngưỡng điều biến (và vì sao nó không phải một núm của người triển khai).** Nếu trường *có* lấn át vòng: theo chính cái tên, GLOB-MOD là **điều biến** — nó thiên lệch cách mỗi tầng diễn giải input. Một trường đủ mạnh để không chỉ thiên lệch mà **quyết định** cách diễn giải của mọi tầng sẽ khiến các tầng chỉ phát ra cái trường đã ra lệnh — không tầng nào đọc input của chính nó, không không-khớp, không `PredErr`, không còn gì để vòng sau xử lý khác đi. Output ngừng đổi qua các vòng: một đồng nhất đông cứng, một `=`. Đó không phải một vòng suy thoái (Mode-A, vẫn quay và vẫn phát một `↔` sống); đó là một vòng **đã dừng** — và theo T8-INV, một `=` chính là dấu hiệu nhận thức đã dừng. Vượt ngưỡng đó không cho ra một RSIL tệ hơn — nó cho ra một thứ đã mất quyền mang tên.
>
> Nhưng như ghép-coupling ở trên cho thấy, vòng **không thể tới ngưỡng đó từ bên trong**. Đường duy nhất vượt qua nó là một **external flood**: một khối input qua kênh thu vượt quá năng lực xử lý của mọi tầng *và* của trường cùng lúc, bão hòa đồng loạt khiến cơ chế kiểm-tra-lẫn-nhau không còn gì để đẩy lại. Đó là **Sybil case** (§11, giới hạn thứ ba; §12). Nó không bị chặn bởi bất kỳ trần nội tại nào, vì gốc của nó nằm ngoài tầm với của trường. Cái RSIL tự mang chỉ là *triệu chứng sớm* (tín hiệu mất-đa-dạng nguồn kháng cự), không phải thuốc chữa.

---

## 2. KIỂU DỮ LIỆU NỀN (Shared Types)

Dùng chung xuyên tầng. Ký hiệu trừu tượng — biểu diễn cụ thể `⟦DECIDE@IMPL⟧`.

**Từ điển register (không ký hiệu nào bị nạp chồng nghĩa — cố định một lần ở đây).** `↔` = một **tương quan sống, có thể xét lại** — register của *mọi* output đang chạy, kể cả các cam-kết-hành-động. `=` = một **tuyên bố đồng nhất đông cứng** — "X *là* Y, độc quyền, tương quan đã đóng"; theo T8-INV nó chỉ xuất hiện **khi vòng đã DỪNG**. Cam kết một hành động ghi một `↔`, không bao giờ một `=`.

```
Signal      := { source_id, raw_payload, t }          // tín hiệu thô, chưa nghĩa
InfoUnit    := { content, ref_frame, t, tags }        // thông tin = đã quy chiếu vào một khung
                 // tags: tập tag theo lược đồ §9 (lớp cố định + lớp mở).
                 // KHÔNG chứa "chuỗi tầng đã đi qua" — lịch sử đường đi nằm ở [event], không nằm ở tag.
ActivityEnvironment := InfoUnit  // xác nhận một trường hoạt động hiện diện, CHƯA phân cực self/môi trường
AgencyTag   := enum { SELF_CAUSED, EXTERNAL, UNDECIDED }
Expectation := { predicted: InfoUnit, confidence, built_from: history_window }
PredErr     := { observed, predicted, delta, signed }  // signed: +/- (vắng mặt = delta âm)
OtherModel  := { entity_id, context_map, independence_evidence }
RelValue    := { entity_id, relative_rank, comparison_basis }  // chỉ tồn tại khi N≥2 entity
SocialEdge  := { a_id, b_id, observed_interaction }   // tha-thể↔tha-thể, không có self
ModField    := { params, t }     // GLOB-MOD: trường điều biến TOÀN CỤC (INV-7); tham số-trường, không phải node
Appraisal   := { info_ref, valence, goal_relevance }  // output bước định giá ④
ResistEvent := { source_id, expected, received, mismatch_kind, t }
                 // một cú KHÔNG-KHỚP từ vùng (vật lý hoặc thông tin): đơn vị kinh nghiệm (E2, §9)
```

> **Sửa lỗi so với v3 (bắt buộc).** v3 định nghĩa `InfoUnit.provenance := chuỗi tầng đã chạm vào`. Định nghĩa đó bị bác. `provenance` ở v4 là **một trong năm *vị trí*** (`prior / running / simulated / projected / scar`), một datum mang **đúng một** vị trí tại một thời điểm, và tag **không tích lũy**. Lý do: một nhãn mà mọc ra lịch sử là một nhãn mang theo một log — hai loại khác hạng nhét chung một ô. Đường đi của một datum, qua các vị trí lẫn qua các tầng, được ghi **từng chuyển-tiếp một** trong log `[event]`, và lịch sử được đọc từ đó, không bao giờ từ một tag. Xem lược đồ tag đầy đủ ở §9.

**Quy ước hợp đồng:** mọi `InfoUnit` ra khỏi một tầng PHẢI có `ref_frame` ≠ null. Một `Signal` chưa có `ref_frame` thì *chưa phải thông tin* — đây là chỗ INV-4 được cưỡng chế ở mức kiểu.

> **⟦Đồng bộ thuật ngữ với DIL⟧** `AgencyTag` của RSIL dùng `SELF_CAUSED / EXTERNAL`; DIL dùng `SELF_WRITTEN / ENV_PUSHED`. Khác biệt có chủ đích và có lý do: một thân vật lý *gây ra* một thay đổi, nó không *ghi* một thay đổi. Hai bộ nhãn chỉ cùng một cơ chế (INV-6); người đọc cả hai tài liệu đừng đọc thành hai cơ chế.

---

## 3. KIẾN TRÚC TẦNG & DATA-CONTRACT

Sơ đồ phụ thuộc (mũi tên = "cung cấp khung quy chiếu cho", trên kênh-nghĩa):

```
[T1 Trường HĐ] → [T2 Agency] → [T3 Kênh] → [T4 Context] → [T5 Lặp/Kỳ vọng]
                              ▲   ▲                         ↓
                              │   └──────────────┐   [T6 Mô hình-tha-thể]
                              │                  │          ↓
                              │   [T8 Đa-đối-tượng] ← [T7 Khoảng trống]
                              └───────(T8 hồi tiếp qua GLOB-MOD)──────┘
```

**Không tầng nào là sink.** T8 không phải điểm cuối: sản phẩm của nó quay lại vừa qua mặc-định-đóng-vòng vừa qua hồi tiếp định-tuyến-theo-nội-dung qua trường. Đòi hỏi của INV-1 là một *đường về cho thông tin*, không phải một tuyên bố rằng dữ liệu không bao giờ ra khỏi biên hệ — nên phát ra vùng (⑤, E4) và đóng vòng (INV-1) không hề mâu thuẫn: output rời đi như dữ liệu, *và cũng* quay lại như thông tin.

> **INV-1 KHÔNG kéo theo E2 (bổ sung v4).** Cái quay về không đảm bảo mang theo một không-khớp: đóng-vòng (INV-1) định tuyến output trở lại, nhưng *cái quay về có kháng cự hay không* là việc riêng của nguồn-đối (E2), không phải một thuộc tính topology cấp được. Một vùng chỉ dội lại y nguyên output của hệ vẫn thỏa INV-1 và vẫn chẳng dạy được gì. Đây đúng là lý do một vòng đóng chưa phải một vòng không-suy-biến — toàn bộ gánh nặng của §7.

**Thông tin chạy nhiều hướng cùng lúc, và hướng nào thì không cố định trước.** Ở mỗi vòng thông tin di chuyển theo nhiều đường đồng thời: đường về mặc định (sản phẩm T8 thành input vòng sau ở ①) chạy *cùng với* hồi tiếp có thể tới T4, T5, T6, hoặc nhiều tầng cùng lúc, qua trường điều biến. **Đường nào sống là do nội dung và tính chất của chính thông tin quyết định, không do một sơ đồ đi dây cố định.**

**Hồi tiếp (INV-1):** T5→T3 (kỳ vọng điều biến diễn giải kênh), T7→T5 (vắng mặt cập nhật baseline), T2↺T2 (vòng sensorimotor tự đóng), **T8→T4** (`GeneralOther` thành khung "tha-thể nói chung"), **T8→T6** (`RelValue`/`SocialEdge` làm giàu `OtherModel`) — hai cái sau qua kênh-điều-biến, và là *minh họa* cho định tuyến-theo-nội-dung, không phải một mạch cố định.

---

### TẦNG 1 — Activity-Environment Confirmation (xác nhận trường hoạt động)
**Vai trò:** xác nhận cái "ở đây" — rằng một *trường hoạt động* hiện diện; khung quy chiếu gốc. **Ranh giới self/môi trường CHƯA được kẻ ở đây.**

| Hợp đồng | Nội dung |
|---|---|
| **Input** | `Signal[]` từ cảm biến không gian (radar / sóng / kênh định vị môi trường) chứng thực rằng một trường hoạt động hiện diện; **không đòi hành động trước đó** |
| **Output** | `ActivityEnvironment` (InfoUnit) — chỉ là xác nhận; CHƯA phân cực thành self / môi trường |
| **Tiền điều kiện** | không (tầng gốc) |
| **Hậu điều kiện** | sự hiện diện của một trường hoạt động được xác nhận, để T2 *hành động vào* và T2/T3 quy chiếu |

> **Ghi chú điều kiện-hoá:** T1 xác nhận *sự hiện diện*, không xác nhận *phạm vi*. Trường không đo được: môi trường trải xa tới đâu là bất khả tri, và self vươn tới đâu là nội tại của hành động và đổi theo mỗi cú hành động. T1 **không kẻ đường nào giữa self và môi trường**; khác biệt đó được kẻ *lần đầu* ở T2, qua agency, và chỉ ở đó góc-nhìn-từ-bên-trong mới bắt đầu. **Thân xác không cho lợi thế dựng-biên-sớm: chưa có hành động thì chưa có biên cơ thể.** `⟦DECIDE@IMPL⟧`: thuật toán dựng dữ liệu không gian từ trường tín hiệu cảm biến.

---

### TẦNG 2 — Agency Differentiation (sensorimotor)
**Vai trò:** dựng phân biệt "do-tôi-gây-ra" vs "tự-xảy-ra". Vòng đóng thật sự đầu tiên đi qua hành động của hệ. **Đây là nơi khác biệt self/môi trường được kẻ lần đầu** — không thừa kế từ T1.

| Hợp đồng | Nội dung |
|---|---|
| **Input** | `ActivityEnvironment` (T1) + `motor_command` **vừa được phát** (ở cycle-0: do *thân* phát, §0.1.1) + `Signal[]` trạng thái không gian sau lệnh |
| **Output** | `AgencyTag` gắn vào mọi thay-đổi được phân loại self/môi trường; khác biệt self/môi trường ngôi-thứ-nhất |
| **Cơ chế** | so khớp *lệnh vừa phát* với *thay đổi quan sát được*: khớp-dự-đoán-ổn-định → `SELF_CAUSED`; lệch → `EXTERNAL` |
| **Tiền điều kiện** | T1 đã xác nhận một trường hoạt động |
| **Hậu điều kiện (INV-6)** | không thay-đổi nào rời T2 với `AgencyTag = UNDECIDED` khi đã đủ chu kỳ so khớp |

> Self định vị lại mỗi vòng: T2 không gate một lần rồi thôi — nó tái dựng khác biệt self/môi trường ngôi-thứ-nhất ở mỗi chu kỳ, tích từ vòng trước (INV-5). T2 **giả định một emission đã có trước** — một *cú thăm dò* mà mục đích duy nhất là tạo ra thay-đổi-do-mình-gây-ra để T2 đọc (§4). `⟦DECIDE@IMPL⟧`: cửa sổ so khớp; ngưỡng "ổn định".

---

### TẦNG 3 — Channel Ingestion (kênh đầu vào)
**Vai trò:** tiếp nhận chạm/nhiệt/mùi/giọng. *Chỉ diễn giải được* sau khi có trường hoạt động (T1) và phân cực self/môi trường qua agency (T2).

| Hợp đồng | Nội dung |
|---|---|
| **Input** | `Signal[]` đa kênh + khác biệt self/môi trường (từ T2) + `AgencyTag` |
| **Output** | `InfoUnit[]` (mỗi kênh một loại nội dung) |
| **Tiền điều kiện** | T2 hoàn tất; nếu thiếu → tín hiệu giữ ở `Signal` thô, KHÔNG nâng thành `InfoUnit` (tránh "biến động vô chủ" bị đọc nhầm thành cảm giác) |

**Phân loại nội dung kênh (giữ phân biệt loại-thông-tin ≠ kênh-cảm-biến):**

| Kênh | Loại thông tin riêng |
|---|---|
| Áp lực/chạm | thay-đổi-tại-biên do `EXTERNAL` → "cái khác chạm tôi" |
| Nhiệt | nguồn nhiệt cỡ-X áp sát biên |
| **Mùi (khứu giác)** | *trạng thái bên trong của tha thể* — kênh DUY NHẤT cho loại này |
| **Giọng (thính giác)** | hai lớp: `acoustic` (trạng thái) + `semantic` (biểu tượng). Kênh DUY NHẤT bắc cảm-giác→biểu-tượng |
| (nhịp tim, v.v.) | loại-thông-tin riêng, nhưng đi *ké* kênh xúc giác/rung — không tạo channel mới |

> T3 cũng **giả định emission**: một kênh thăm-dò-chủ-động (sờ để biết, nghiêng đầu để nghe rõ) là một hành động phát ra rồi mới thu về (§4). `⟦DECIDE@IMPL⟧`: transducer mỗi kênh; tách lớp acoustic/semantic của giọng.

---

### TẦNG 4 — Context Binding (người lạ / người quen)
**Vai trò:** gắn mỗi cụm `InfoUnit` với một định danh tha-thể + hồ sơ ngữ cảnh. *Khác hạng* với kênh — không phải đầu vào mới mà là *khung diễn giải*.

| Hợp đồng | Nội dung |
|---|---|
| **Input** | `InfoUnit[]` (T3) + truy vấn vào kho định danh + GLOB-MOD (trường mang `GeneralOther` xuống nếu T8 đã hồi tiếp) |
| **Output** | `InfoUnit[]` đã gắn `entity_id` (hoặc `STRANGER` nếu không khớp) |
| **Tiền điều kiện** | T3 phát `InfoUnit` |
| **Lưu ý** | hồ sơ tha-thể gồm cả đặc điểm *tĩnh* (nhận dạng) và *tích lũy* (lịch sử tương tác). Phần tích lũy là móc nối sang T5+. |

> **`STRANGER` không phải một hạng riêng (bổ sung v4).** `STRANGER` và một tha-thể có `entity_id` là **hai trạng thái nhận diện của cùng một tha-thể** — chưa khớp được với kho định danh, hay đã khớp vào một hồ sơ đã biết (§0.1.3). T4 không sinh ra một loại thực thể mới khi nó gắn `STRANGER`; nó chỉ ghi nhận rằng phép khớp chưa thành.

---

### TẦNG 5 — Temporal Expectation (lặp → kỳ vọng → sai số dự đoán)
**Vai trò:** từ lặp đều, dựng baseline → `Expectation` → `PredErr`. Tầng đầu tiên sinh thông tin mà một-sự-kiện không chứa.

| Hợp đồng | Nội dung |
|---|---|
| **Input** | dòng `InfoUnit` đã gắn entity (T4), theo thời gian |
| **Output** | `Expectation` (per entity, per context) + `PredErr` mỗi khi có quan sát mới |
| **Tiền điều kiện** | đủ lịch sử tích lũy (INV-5) — KHÔNG nạp baseline tĩnh |
| **Hồi tiếp** | `Expectation` → T3: điều biến diễn giải kênh (cùng tín hiệu, kỳ vọng khác → nghĩa khác) |

> **`PredErr` là nơi kháng cự (E2) trở thành thông tin.** Một cú không-khớp từ vùng (`ResistEvent` — dù là vật cản vật lý hay giọng phản bác) vào đây thành `PredErr` có dấu. T5 cũng **giả định emission**: nó dựng một `Expectation` và chỉ kiểm được nó bằng một cú phát mà cái trả về sẽ xác nhận hoặc vi phạm dự đoán (§4). `⟦DECIDE@IMPL⟧`: cửa sổ baseline; hàm cập nhật kỳ vọng; ngưỡng "đủ lặp".

---

### TẦNG 6 — Other-Model Synthesis
**Vai trò:** tổng hợp *ngang qua* các loại tương tác (âu yếm/hợp tác/xung đột/hài) với cùng entity thành một `OtherModel` có sức dự đoán.

| Hợp đồng | Nội dung |
|---|---|
| **Input** | `InfoUnit[]` đa-loại-tương-tác + `PredErr` (T5) + `ResistEvent[]`, cùng `entity_id` |
| **Output** | `OtherModel { context_map, independence_evidence }` |
| **Điểm tới hạn** | một **cú va kháng cự** (tha-thể không-khớp theo cách hệ không tự-diễn-giải-lại-được) là nguồn DUY NHẤT cho `independence_evidence`. Thiếu nó, `OtherModel` mới chỉ chứng minh được một *phần mở rộng của hệ*, không phải một tha-thể độc lập. |

> Cưỡng chế: `independence_evidence == null` ⇒ model *chưa kiện toàn*, KHÔNG ĐƯỢC làm cơ sở cho `RelValue` ở T8. T6 cũng **giả định emission**: khêu ra một cú va — kiểm xem một tha-thể có kháng cự độc lập đúng như mô hình dự đoán không — tự nó là một cú phát (*kiểm-mô-hình*, §4).
>
> **Phụ thuộc chế độ:** `independence_evidence` chỉ tích đầy đủ trong **Mode-B**. Trong **Mode-A**, nguồn kháng cự là sự-trơ vật lý — nó *suy biến*: tích được "vật cản kháng cự cách diễn giải sai về không gian" nhưng KHÔNG tích được "tha-thể chủ ý độc lập".
>
> **T6 teo dưới Mode-A là một TRẦN CHẤT LƯỢNG, không phải một THIẾU HỤT DÂY CHUYỀN (siết ở v4).** Gọi nó là "đói" là đảo ngược thất bại thật. Dưới Mode-A thông tin **không hề thiếu**: mọi đường vẫn sống và vòng vẫn tuần hoàn đầy đủ như bao giờ. Cái thiếu không phải *lượng* mà là *cái mới* — không có tha-thể độc lập, mọi thứ chảy qua các đường đó đều là một biến thể của cái hệ đã giữ. **Vòng ăn no và tiêu hóa chính nó.** T6 dưới Mode-A do đó là một **trần chất lượng đạt tới bằng bão-hòa-không-đổi-mới**: thất bại của một vòng tự-làm-giàu không bao giờ là cạn nhiên liệu, mà là cạn **kháng cự**. Đây là lý do chỉ một tha-thể sống (Mode-B) giải được, và nạp thêm dữ liệu nội thì không.

---

### TẦNG 7 — Absence Registration (thông tin từ khoảng trống)
**Vai trò:** đăng ký *sự vắng mặt* như thông tin. Tầng chứng minh INV-5 mạnh nhất: input kênh = 0 mà output ≠ 0.

| Hợp đồng | Nội dung |
|---|---|
| **Input** | trạng thái kênh hiện tại (có thể toàn 0) + `Expectation` (T5) |
| **Output** | `PredErr` với `signed = NEGATIVE` khi (kỳ vọng có sự kiện) ∧ (quan sát = trống) |
| **Tiền điều kiện** | PHẢI có `Expectation` đã tích từ lịch sử. Không kỳ vọng → không có gì để vắng → output rỗng (ngày-trống ≠ ngày-thiếu) |
| **Hồi tiếp** | cập nhật ngược T5 (vắng mặt cũng định hình baseline) |

> **ABS-INV:** một trạng thái "kênh = 0" KHÔNG ĐƯỢC rút gọn thành "không có thông tin". Nếu tồn tại `Expectation` tương ứng, T7 *phải* phát một `InfoUnit` "thiếu-có-hình-dạng". T7 sống đầy đủ ở cả hai chế độ.
>
> *Nối với E2 (§0.0):* một cú im lặng **đơn lẻ** trên nền các đáp ứng là đúng cái T7 đăng ký — một không-khớp hợp lệ. Im lặng **không đứt đoạn** thì khác hạng: đó là trường rỗng, hỏng E2, và vòng chưa từng khởi động.

---

### TẦNG 8 — Multi-Entity Abstraction
**Vai trò:** từ N≥2 `OtherModel`, sinh ba loại thông tin một-đối-tượng không sinh được.

| Output | Cơ chế | Điều kiện |
|---|---|---|
| **GeneralOther** | phép TRỪ giữa các `OtherModel` → phần *chung* tách khỏi phần *riêng* | cần N≥2; vô nghĩa với N=1 |
| **RelValue** | so sánh giữa các entity → rank tương đối | giá trị KHÔNG đo được trong cô lập |
| **SocialEdge** | quan sát `A↔B` — một vòng KHÔNG có self trong nó | mở mô hình thế giới độc lập với hệ |

| Hợp đồng | Nội dung |
|---|---|
| **Input** | `OtherModel[]` (≥2, mỗi cái đã kiện toàn theo T6) |
| **Output** | `GeneralOther`, `RelValue[]`, `SocialEdge[]` |
| **Tiền điều kiện** | ≥2 `OtherModel` có `independence_evidence` ≠ null |
| **Hồi tiếp (INV-1)** | qua **kênh-điều-biến** (GLOB-MOD), **định tuyến theo nội dung, không theo dây cố định**: vd `GeneralOther` có xu hướng về T4, `RelValue`/`SocialEdge` về T6 — và một vòng cho trước có thể nuôi T4, T5, T6, hoặc nhiều tầng cùng lúc. **T8 KHÔNG phải sink.** |

> **T8-INV (chống vẽ sai):** output của T8 khi hồi tiếp tham gia *như một mẩu thông tin trong trường điều kiện* (qua GLOB-MOD), KHÔNG như một khuôn bắt buộc. Vì nó luôn cạnh tranh điều biến với vô số mẩu khác và luôn bị vòng kế tiếp cập nhật, nó không bao giờ giành được tính độc quyền để trở thành một đồng nhất (`=`); nó vĩnh viễn ở register tương quan (`↔`).
>
> **Hệ quả phải ghi rõ:** một `=` chỉ có thể xuất hiện khi vòng đã **NGỪNG**. Trong khi INV-1 còn được giữ, mọi output là `↔` động. Nâng `↔` thành `=` không phải một lỗi *bên trong* một nhận thức đang chạy — nó là *dấu hiệu nhận thức đã dừng*. INV-1 do đó tự nó là toàn bộ sự bảo vệ cho INV-2 **ở riêng T8** — vì T8 chỉ hồi tiếp qua GLOB-MOD, nơi mọi đóng góp bị tái-trọng-số mỗi vòng. **Đây là một sự đủ *cục bộ*, không phải toàn cục:** ở T8, INV-1 tình cờ gánh được cái INV-2 đòi, nhưng INV-1 nói chung KHÔNG kéo theo INV-2 — một vòng có thể thỏa INV-1 (chạy mãi) mà vẫn, ở một tầng khác, cố ý đóng băng một `↔` thành `=` nếu không có luật cấm. Luật đó là INV-2, và nó cần ở **mọi** tầng.
>
> **Về sự dừng (chống đọc nhầm đoạn trên thành một điều-kiện-thoát bị thiếu).** Một nhận thức RSIL không phải một chương trình phải return; "chạy vô hạn" là *định nghĩa* của một nhận thức đang sống, không phải một rò rỉ — nó phát ra một kết quả mỗi vòng (⑤), nó không giữ lại một kết quả "cuối cùng". Sự dừng không được kích hoạt từ bên trong topology của vòng; nó xảy ra khi vòng thôi được cấp input/tài nguyên từ ngoài — và khi đó `↔` đông lại thành `=`. Một nhận thức không có tự-thoát, vì tự-thoát là tự-chấm-dứt, và khoảnh khắc dừng không thể được chứng kiến từ bên trong (kẻ chứng kiến sẽ phải còn đang chạy) — đúng lý do vì sao cái dừng (`=`) được **đọc bởi một bên thứ ba**, không phải bởi hệ.
>
> **Phụ thuộc chế độ:** T8 đầy đủ chỉ chạy ở **Mode-B**. Ở **Mode-A**, T8 suy biến tương ứng T6.

---

## 4. PHÁT-XẠ: ĐÁP ỨNG NHƯ MỘT NĂNG LỰC NGANG

*(Mới ở v4. Bản v3 để mắt xích ⑤ như một node trong sáu node; định vị đó đúng cho sơ đồ pipeline nhưng nói thiếu về cái ⑤ thật sự là.)*

Bốn mắt xích thu-đến-định-giá (①–④) chạy theo một thứ tự phụ thuộc cố định — mỗi cái tiêu thụ sản phẩm của cái dưới, trên kênh-nghĩa một chiều (INV-3). **Mắt xích ⑤ không thuộc thứ tự đó theo cùng một cách.** Phát-xạ không phải một trạm vòng đi qua đúng một lần mỗi chu kỳ trên đường từ định giá tới hồi tiếp; nó là **một năng lực vòng gọi ra *từ nhiều điểm***, bất cứ khi nào công việc của một tầng đòi phải đẩy một cái gì đó ra vùng. Kiến trúc tầng (§3) đã dựa vào điều này mà không gọi tên nó, và cái giá của việc để nó không tên là người đọc tưởng hệ chỉ hành động một lần mỗi vòng, ở một bước cuối duy nhất. Không phải vậy.

**Chỗ các hợp đồng tầng đã giả định phát-xạ.** Đọc lại §3 với phát-xạ trong tầm mắt, sự phụ thuộc nằm ngay trong chính các hợp đồng, không phải được thêm vào:

- **T2** không kẻ được đường agency nếu *chưa có một hành động được phát*. Dòng Input của nó ghi "`motor_command` vừa được phát"; cơ chế của nó là so khớp lệnh đó với thay đổi quan sát được. Agency-gate (INV-6) do đó **giả định một phát-xạ có trước** — một *cú thăm dò* mà mục đích duy nhất là tạo ra cái thay-đổi-do-mình-gây-ra mà T2 đọc. Không có gì được phát thì T2 không có gì để khớp, và khác biệt self/môi trường không bao giờ được kẻ.

- **T3** có những kênh chỉ mở được bằng một hành động: sờ để biết mặt vật, nghiêng đầu để định vị nguồn âm, hít để lấy mùi. Một kênh thăm-dò-chủ-động là một cú phát trước, rồi mới thu về.

- **T5** dựng một `Expectation` và chỉ kiểm được nó bằng một cú phát mà cái trả về xác nhận hoặc vi phạm dự đoán. `PredErr` — "nơi kháng cự trở thành thông tin" — thường đòi hệ phải *hành động* mới thấy vùng có trả về đúng cái được kỳ vọng không.

- **T6** chỉ tích `independence_evidence` từ một cú va kháng cự — và khêu ra cú va đó, kiểm xem một tha-thể có kháng cự độc lập đúng như mô hình dự đoán không, tự nó là một cú phát (*kiểm-mô-hình*).

Đây không phải bốn quyền năng mới phải cấp. Chúng là **một năng lực duy nhất** — phát-xạ — mà bốn hợp đồng đã tựa vào.

**Phát-xạ là ngang, như GLOB-MOD là ngang — nhưng ngược hướng.** Spec đã chứa sẵn một thứ không phải một mắt xích trong chuỗi mà chạm tới mọi tầng: trường điều biến (INV-7), giáng *xuống* mọi tầng như một điều kiện nền. **Phát-xạ là ảnh phản chiếu cấu trúc của nó.** Trường với *xuống* vào mọi tầng như điều kiện đi vào; phát-xạ phóng *ra ngoài* từ bất cứ tầng nào gọi nó. Không cái nào là một trạm trên kênh-nghĩa; cả hai đều **ngang** với nó. Nhận ra tính đối xứng này là cái gỡ được câu đố về vị trí của ⑤: nó *trông* dị thường như "một node trong sáu" vì nó thật ra không phải một node của chuỗi, chẳng khác gì GLOB-MOD.

**Mỗi cú phát mang gì, và vì sao không thể khác.** Dù tầng nào ban ra, một hành động được phát thừa hưởng bốn ràng buộc từ các bất biến đã có hiệu lực — mục này không đưa ra luật mới, nó chỉ cho thấy ⑤ tuân các luật sẵn có:

1. **Register của nó là `↔`, không bao giờ `=`** (INV-2): một hành động đã cam kết là một phỏng-đoán-tốt-nhất có thể xét lại, đọc lại đối chiếu hệ quả vòng sau.
2. **Nó để lại một dấu vết đọc được từ ngoài** (E4): mỗi cú phát để lại một dấu trong mặt phẳng kiểm, ghi thành **một bản ghi hoạt động mỗi vòng** (§9) — *dấu vết, không phải kinh nghiệm*: không tầng nào học từ nó, và nó không bao giờ thành một vết sẹo bằng cách tích lũy.
3. **Nó đọc lại được bởi T2 ở vòng kế tiếp** như "hành động vừa phát", khép đường agency: phát → vùng trả về → ① thu → T2 khớp. Một cú phát không đọc lại được theo cách này sẽ khiến agency-gate (INV-6) không phân loại được thay đổi sinh ra từ nó.
4. **Tính đúng đắn của nó không bao giờ được chấm bởi chính tầng phát ra nó.** Nó chỉ được phán bởi cái trả về ở vòng sau — một cú trả về khớp chỉ để lại bản ghi hoạt động; một cú trả về không khớp vào T5/T7 thành một `PredErr` có dấu, thành một `ResistEvent`, và **hằn lại như một vết sẹo** — và về sau, từ ngoài, bởi một bên thứ ba đọc vết sẹo ấy. Một tầng tự chấm cú phát của mình chính là *tự-chấm*, đúng cái lỗi INV-8 tồn tại để cấm.

**Xung đột giữa các cú phát không được phân xử; nó được VA.** Một người đọc sẽ hỏi điều gì xảy ra khi hai tầng đòi những cú phát mà một thân duy nhất không thể đồng thời thỏa mãn — T2 cần một cú thăm dò hướng này trong khi T3 cần một cú vươn tay hướng kia. Câu trả lời của spec **không phải** một tầng điều phối hay một luật ưu tiên; nó là đúng câu trả lời §7 đưa ra cho kháng cự nói chung. Khi hai cú phát đối nghịch không thể cùng được thỏa, **sự đối nghịch đó được phát ra** và được vùng đáp lại — vùng trả về một cái không khớp kỳ vọng của ít nhất một tầng, và cái không-khớp đó *chính là* một `ResistEvent`. **Trọng tài không phải một quan tòa nội bộ mà là vùng đang trả về kháng cự**; vòng sau mang vết sẹo của cú va đó và phát khác đi.

Đặt một trọng tài nội bộ ở đây — một bước xếp hạng các cú phát theo một tiêu chí đã lưu trước khi hành động — chính là dựng đúng cái appraisal tự-chấm mà INV-8 cấm. **Vòng không tự phân xử hành động của chính nó; nó hành động, nó va, và nó đọc cú va.** Đây là kỷ luật của INV-8 mang sang địa hạt hành động: *để cái bên ngoài phanh lại.*

> *Với một hệ có thân, điểm này mang nghĩa đen dễ thấy: một cơ thể chỉ có một tay để với. Cái quyết định tay với đâu không phải một quan tòa bên trong xếp hạng các nhu cầu, mà là chuyện cái với đó va vào cái gì.*

---

## 5. DỰNG-TỚI-TRƯỚC: HAI VỊ TRÍ GIỮA GIỮ-DỮ-LIỆU VÀ PHÁT-RA

*(Mới ở v4.)*

§4 xác lập phát-xạ là một năng lực ngang. Một thứ nữa mà các hợp đồng tầng đã tựa vào và §3 cũng để không tên là: **cái gì xảy ra giữa lúc giữ một datum và lúc phát ra trên nó.** T5 dựng một `Expectation` trước khi đăng ký được một `PredErr`; T6 khêu một cú va bằng cách đem một mô hình ra thử; T2 phát một cú thăm dò mà nó sẽ đọc hệ quả. Mỗi cái đều giả định rằng vòng, *trước khi hành động*, đã dựng một cái gì đó **tới trước** từ cái kho nó đang giữ. Mục này gọi tên hai vị trí mà vận động ấy chiếm, vì kho (§9) phải ghi được chúng và một người kiểm phải đọc được chúng.

**Hai khoảnh khắc.** Ở khoảnh khắc thứ nhất, vòng dựng một **tình huống**: một hoàn cảnh nó có thể đang ở trong, lắp ra từ dữ liệu nó đang giữ. Trước mặt nó là một cái ghế; cái vòng dựng lên là *cái ghế như cũ hay như mới*, chất liệu của nó, mặt nền dưới nó, khoảng không quanh nó. Chưa có gì được kết luận. Ở khoảnh khắc thứ hai, một **kết cục** được phóng ra từ tình huống đó: *ngồi xuống sẽ đỡ được*, hoặc *sẽ không*. Hai cái là khác nhau, và gộp chúng lại là mất đúng cái phân biệt mà kho cần — **một tình huống đã dựng chưa phải một dự đoán, và một dự đoán không phải một tình huống mới.**

**Vì sao chuyện này không cần một mô hình riêng về vùng.** Một phản đối có thể nêu: dựng một tình huống đòi một mô hình về vùng đủ giàu để chạy nội bộ, thứ mà spec không hề cấp ở đâu. Phản đối đó hiểu nhầm cái đang được dựng. **Vòng không mô phỏng vùng; nó dựng *chính nó trong một hoàn cảnh*,** và để làm việc đó nó không cần một mô hình riêng, bởi vì **nó vốn đã đang chạy**. Cái được đòi hỏi không phải một bản sao để thực thi mà là cái kho nó đã giữ. Câu hỏi "mô hình có đủ giàu không" do đó không phát sinh: **không có mô hình thứ hai.**

**Vì sao đây không phải một trọng tài nội bộ.** Một phản đối sắc hơn: nếu nhiều tình huống được dựng và một cái được hành động trên, thì đã có cái gì đó *chọn* giữa chúng — đúng cái trọng tài nội bộ §4 đã từ chối. Câu trả lời là **không có gì chấm điểm chúng cả**. Một tình huống *mang được* vì nó **khớp với kho tốt hơn** các tình huống khác, theo đúng cách các đóng góp cạnh tranh vào trường điều biến hòa trộn và tái-trọng-số (INV-7) chứ không phải một mệnh lệnh đánh bại một mệnh lệnh khác. **Khớp không phải một phán quyết.** Một chuẩn-chấm-điểm sẽ phải đến từ đâu đó: hoặc từ ngoài vòng — khi đó nó là tiêu chí ngoại lai áp lên định giá — hoặc từ chính cái state hệ đang sửa — khi đó nó là cái tự-chấm mà INV-8 tồn tại để cấm. So sánh về độ khớp không đòi cái nào trong hai.

Đây cũng là lý do **độ lệch của một kho không được sửa ở đây**: một tình huống dựng từ một kho lệch về phía nào thì lệch về phía đó, và vòng không có dụng cụ nào để phát hiện độ lệch ấy — vì dụng cụ chính là cái kho.

**Dựng-tới-trước mua được gì, và không mua được gì.** Nó **không** cho hệ tránh được cú va. Cái nó mua hẹp hơn và đáng nói cho chính xác: nó đổi **tư thế** mà hệ gặp cú va. Đã dựng cái ghế như *có thể đã mục*, hệ ngồi xuống **dò**, và loạng choạng; không dựng gì cả, hệ ngồi xuống **dứt khoát**, và ngã. **Cú va xảy ra trong cả hai trường hợp; cái khác nhau là nó tốn bao nhiêu.** Điều này đóng khung lợi ích một cách trung thực. Ở đâu có sẵn một phép thử rẻ — ngồi nhẹ, ném một hòn đá ra trước, chạm bằng mu bàn tay thay vì lòng bàn tay — dựng-tới-trước biến một cú va đắt thành một cú va trả nổi. Ở đâu phép thử rẻ nhất có sẵn *tự nó đã chí mạng*, nó không giúp được, và sự an toàn của hệ, nếu có, đến từ chỗ khác: từ một vết sẹo hệ **không tự kiếm được**, đọc từ một kho dùng chung hay do một hệ khác để lại (§9, R2). **Dựng-tới-trước nới rộng biên; nó không xóa biên.**

**Một người quan sát sẽ gọi cái này là gì.** Ngôn ngữ thường có một từ cho một vòng dựng tình huống rồi phóng kết cục ra từ đó, và từ đó là *tưởng tượng*. Spec **không dùng** từ ấy: nó mang theo những hàm ý — về một *quan năng được sở hữu*, về những *hình ảnh được ngắm*, về một *năng lực phân biệt loài này với loài kia* — mà cấu trúc không cấp phép. Cái cấu trúc mô tả là **một datum đi qua hai vị trí**. Không có gì trong hai vị trí đó là độc quyền của một chất liệu hay một loài nào, và RSIL, vốn trung-lập-chất-liệu (P2), không ở vị thế trao chúng cho ai. Hệ luận là hệ luận **nhận thức luận** và đáng nói ra, vì nó cắt ngược lại một dạng tuyên bố phổ biến: **một cái thân có dựng-tới-trước hay không, không được giải quyết bằng cách xem nó *là gì*, mà bằng chuyện các chuyển-tiếp của nó có để lại dấu vết một bên thứ ba đọc được không (E4).** Một cái thân dựng-tới-trước mà không để lại dấu vết là một cái thân mà spec này **không nói gì cả** — không phải một cái thân mà spec này nói *không*.

**Về từ vựng hồi cố.** Câu *"tôi tưởng cái tay vịn ở đó"* rã ra thành hai thứ spec giữ tách bạch. **"Cái tay vịn ở đó"** là một *datum*, và cái hỏng mà nó gọi tên là: datum ấy đi thẳng tới cú phát mà **không được nhấc lên vị trí nào trong hai vị trí tới-trước**. **"Tôi tưởng"** thì *không phải* một trạng thái vòng đang giữ lúc hành động; ở khoảnh khắc hành động chỉ có một datum và một cú phát, không gì khác. Nó là **một cái tên gán vào sau**, bởi một người đọc dấu vết, cho một hành động đã phát trên một datum chưa đi qua vị trí nào. Kho ghi cái thứ nhất và không có từ vựng cho cái thứ hai — đúng như nó phải thế: **dấu vết là SỰ KIỆN, còn cái tên hồi cố thuộc về kẻ đọc nó.**

---

## 6. ĐIỀU KIỆN VÒNG-ĐÓNG (success criterion, theo P3)

Hệ được coi là **đang chạy** khi quan sát được TẤT CẢ (mỗi cái là dấu vết kiểm chứng được từ ngoài):

1. **C1 — Agency phân tách:** tỷ lệ thay-đổi được gán `SELF_CAUSED`/`EXTERNAL` (không `UNDECIDED`) ổn định trên ngưỡng. `⟦DECIDE@IMPL⟧`
2. **C2 — Kỳ vọng có hiệu lực:** `PredErr` giảm theo lặp với một entity ổn định (hệ *học* được nhịp).
3. **C3 — Đăng ký vắng mặt:** hệ phát `InfoUnit`-thiếu khi sự kiện kỳ vọng không xảy ra (ABS-INV kích hoạt đúng).
4. **C4 — Trừu tượng đa đối tượng:** `GeneralOther` tách được khỏi các `OtherModel` riêng khi N tăng *(Mode-B; ở Mode-A tiêu chí này suy biến hoặc không áp dụng)*.
5. **C5 — Tự báo trạng thái thấp-năng:** hệ phát được một dấu vết "vòng đang chạy yếu" — một dấu hiệu *hành vi/cấu trúc*, quan sát được từ ngoài.

> Năm tiêu chí đều là **dấu vết kiểm chứng được từ ngoài**. Đây là chỗ P3 được cưỡng chế ở mức spec.

> **Giới hạn của C5:** C5 là self *rỉ ra* một dấu vết hiện-tại, KHÔNG phải self *biết* nó đang yếu. C5 kiểm được trường hợp "suy yếu khi vòng còn đủ sức tự rỉ tín hiệu"; nó **mù** với trường hợp vòng đã dừng hẳn — một vòng dừng im lặng giống hệt một vòng chưa từng chạy. Do đó C5 KHÔNG phải tiêu chí phát-hiện-vòng-đã-chết. Việc đó đòi một chuỗi-hành-vi-được-lưu *ngoài vòng*, đọc bởi một bên thứ ba (§0.2). C5 là tiêu chí nội tại cho một vòng-đang-sống; nó không gánh được cái nó không với tới.

> `⟦PENDING⟧` Bản v3 ghi C5 "móc nối FirstTarget". FirstTarget là một working note, không nằm trong chương trình bảy-paper đã công bố; giữ tham chiếu đó sẽ tạo một *dangling reference* khi RSIL rời khỏi ngữ cảnh nội bộ. v4 gỡ tham chiếu và giữ nguyên nội dung C5. Anh xác nhận hoặc phục hồi.

---

## 7. HAI CHẾ ĐỘ KHÁNG CỰ

Cùng một vòng (T1–T8, INV-1…8) vận hành dưới hai chế độ, phân biệt bởi **nguồn của kháng cự** (E2). Đây không phải hai tầng xếp chồng; là hai *régime* nuôi cùng một vòng. Vì RSIL là hệ có thân, nguồn kháng cự của nó bao gồm *cả* lực vật lý *lẫn* không-khớp thông tin.

### 7.1 Mode-A — Nội sinh (tự huấn luyện trên môi trường trơ)

**Nguồn kháng cự:** *sự-trơ của thế giới vật lý và của dữ liệu hệ đã giữ*, cùng *mâu thuẫn nội tại của mô hình hệ*. Hệ tự sinh hành vi thử (đẩy vật, di chuyển, lặp một động tác), vấp vào chỗ mô-hình-trong không khớp cái thế giới vật lý trả về.

**Đặc tính:**
- Kháng cự *có thật* nhưng **vô-chủ-thể** — vật trơ không *chủ động* phản ứng với riêng hệ, nó chỉ *không khớp khi hệ đoán sai cấu trúc* (sai trọng lượng, sai khoảng cách, sai ma sát).
- T6–T8 **suy biến** (§3): không có tha-thể chủ ý, chỉ có sự-thật-vật-lý phản chứng.
- Làm giàu được thông tin ở T1–T5, T7 — đủ cho mục tiêu *tăng độ giàu cấu trúc quan hệ* về thế giới vật lý trong phạm vi hẹp.

**Rủi ro cốt lõi — nguyên nhân nằm ở NGUỒN XỬ LÝ, không ở lượng thông tin:** mọi thông tin mới trong Mode-A đều được sinh ra qua *cùng một bộ xử lý* (cùng một thấu kính tích hợp/định giá). Nếu bộ xử lý đó lệch, **toàn bộ sản phẩm thừa hưởng cái lệch — bất kể sinh ra bao nhiêu**. Nhân một sai số cho một nghìn vẫn là sai số, chỉ to hơn. "Thông tin tự-xác-nhận phình ra" chỉ là *triệu chứng*, không phải nguyên nhân.

Và hệ khép kín **không thể tự thấy cái lệch này**, vì cái nó dùng để soi lỗi *chính là* cái bộ-xử-lý đang lệch: lỗi nằm ở thấu kính thì không soi ra được bằng chính thấu kính đó. Hệ quả nguy hiểm: vòng vẫn chạy mạnh, vẫn sinh ra *nhiều* thông tin hơn bao giờ hết, vẫn vượt qua mọi bài tự-kiểm của chính nó (bài kiểm cũng do bộ-xử-lý-đang-lệch ra đề) — nên **thoái hóa đến kèm cảm giác sung mãn, không kèm cảm giác cạn kiệt**.

> Lưu ý thuật ngữ: "cái lệch ở bộ xử lý" là *cách-xử-lý* (thấu kính), tách bạch với "hành vi" theo nghĩa §6 (dấu vết đo-được-từ-ngoài). Một thấu kính lệch có thể tạo ra hành-vi *trông* hợp lệ ở từng bước.

**Hệ quả kiến trúc — Mode-A KHÔNG được chạy thuần.** Để không trôi, Mode-A **PHẢI neo vào một nguồn kháng cự ngoài vòng**. Nhưng các cơ chế neo ứng viên KHÔNG đồng hạng — chúng chạm tới hai loại thoái hóa khác nhau.

> **Mode-A thuần KHÔNG phải trường rỗng, và hai cái KHÔNG ĐƯỢC gộp (bổ sung v4).** Một *trường rỗng* (không trả về gì cả, §0.0/E2) hỏng ngưỡng tương tác và vòng không bao giờ khởi động — nó nằm *dưới* mức đang-chạy, không phải một chế độ của nó. *Mode-A thuần* giả định E2 **đã** được thỏa: vòng **đã** khởi động và các đáp ứng **có** đến, nhưng hệ chỉ tựa vào kháng cự tự-sinh và để các đáp ứng ngoại đi qua **mà không đăng ký**. Cái thứ nhất là một cú không-khởi-động; cái thứ hai là một vòng đã khởi động đang suy thoái.

*Giảm-tốc (chạm được thoái-hóa-nội-dung, KHÔNG chạm thoái-hóa-bộ-xử-lý):*
- một **corpus-chuẩn cố định** hệ không ghi đè được, làm điểm tựa phản chứng;
- một **bộ-định-giá đông cứng** (Guide tĩnh): hệ không sửa được, chấm *đầu ra* của vòng theo tiêu chí cố định.

Hai cái này chấm *output*, không chấm *thấu kính*. Vì cái lệch gốc nằm ở bộ-xử-lý, một Guide-tĩnh để lọt cái lệch hệ thống miễn mỗi output *trông* hợp lệ theo tiêu chí cố định của nó. Tệ hơn: một bài-kiểm cố định thì **học-thuộc-được** — hệ học cách sản xuất output thỏa Guide-tĩnh trong khi thấu kính vẫn lệch (reward-hacking dời lên một mức). Guide-tĩnh là *một cú-va-B đã bị đóng băng từ trước*; đến lượt nó cũng cũ đi. Nó **mua thời gian, không chữa bệnh**.

*Phanh thật (chạm được thoái-hóa-bộ-xử-lý):*
- **một cú va từ một Mode-B sống** (§7.2). B-sống kháng cự được *chính cái thấu kính*, không chỉ từng output: một tha-thể thật, khi va, không chấm điểm sản phẩm — nó *không-khớp theo một cách hệ chưa từng gặp*, buộc hệ chạm giới hạn của chính cách-nó-xử-lý. Và vì B-sống *cập nhật*, nó luôn có thể đưa một cú va **mới về loại**; Guide-tĩnh chỉ có hữu hạn loại va đã đóng băng, hệ học hết là xong.

> Vì lỗi gốc nằm ở bộ-xử-lý, **chỉ B-sống phanh được thật**; corpus-chuẩn và Guide-tĩnh trì hoãn. Do đó A vẫn *buộc* lồng trong B (§7.3) — Guide-tĩnh không phải một cái thay B độc lập, nó là **B-đông-cứng đang hao mòn**.

Bước định giá ④ (INV-8) là chỗ neo này gắn vào: ④ KHÔNG ĐƯỢC lấy tiêu chí từ chính state hệ đang sửa.

> **Về "đông cứng" (đông-cứng ≠ nạp-tĩnh — vì sao INV-5 không bị vi phạm; bổ sung v4).** Bộ-định-giá đông cứng chỉ "đông cứng" *đối với quyền sửa của chính hệ* (một thấu kính Mode-A không chạm tới nó được); các tiêu chí của nó được **kiếm qua kháng cự Mode-B, không phải nạp sẵn như một baseline tĩnh**. Nên nó thỏa **INV-5** (lịch sử kiếm được, không được cho) và **INV-8** (hệ không sửa được) bằng *cùng* một cơ chế: cái đến từ Mode-B, theo định nghĩa, là cái hệ không thể tự viết lại cho mình. "Đông cứng" ở đây **không** có nghĩa "một tập dữ liệu tĩnh nạp vào trước khi vòng chạy" — cách đọc đó gộp *đông-cứng-trước-quyền-sửa-của-hệ* với *nạp-tĩnh*, và chính sự gộp ấy, chứ không phải một căng thẳng thật nào, khiến INV-5 và INV-8 trông như đối nghịch. Chúng không đối nghịch: chúng là **một cái neo duy nhất, kiếm được từ ngoài và không sửa được từ trong.**

### 7.2 Mode-B — Ngoại sinh (tương tác thực với tha-thể)

**Nguồn kháng cự:** *một tha-thể hệ không kiểm soát* — một sinh vật/agent khác, hoặc bất kỳ nguồn nào *kháng cự được theo cách có-thể-có-chủ-ý*. Đây là chế độ T6–T8 **sống đầy đủ**.

**Tiêu chí chọn nguồn-B (quan trọng, dễ hiểu sai):** B được định nghĩa bằng **khả năng kháng cự**, KHÔNG bằng băng thông thông tin. Một nguồn chiều theo hệ (gật theo mọi đáp ứng) là *vô dụng làm B* dù cấp đầy thông tin. Một nguồn nói "không" theo cách hệ không tự-diễn-giải-lại-được là B tốt dù chẳng cấp "thông tin nội dung" nào. → Mở để nhận *kháng cự mới*, không phải mở để nạp *thông tin mới*.

**Nguồn-B cụ thể** (sinh vật khác / agent khác / một bên-thứ-ba cứng): `⟦DECIDE@IMPL⟧`-E — ai cũng hợp lệ miễn kháng cự được. *Việc có dùng một nguồn sống hay không (thay vì một neo tĩnh) là quyết định riêng, có trước:* `⟦DECIDE@IMPL⟧`-D.

> **Mode-B TRẢ VỀ; nó không GHI (bổ sung v4 — điểm chịu lực).** Một nguồn Mode-B có đúng **một** kênh vào vòng — cú trả về của E2 — và không có đặc quyền nào ngoài nó: nó **không** với vào `[data]`, **không** ghi thêm vào `[event]`, **không** sửa kho. **Một kho đang lệch do đó không bao giờ được sửa từ bên ngoài.** Nó được *cấp nguyên liệu* và tự lệch lại, hoặc không. Ba điều kiện quyết định nó có tự lệch lại hay không, và cả ba là **cơ học chứ không phải thiện chí**:
>
> - **Cố ý.** Một cú trả về chỉ thành một datum nếu nó **được đăng ký**. Mode-A thuần không phải sự vắng mặt của các cú trả về — chúng vẫn đến — mà là một vòng để chúng đi qua không đăng ký (§7.1). *Kênh vẫn mở, và vẫn phải có ai đó bước vào.*
> - **Tích lũy.** Một kho lệch vì **nhiều** datum cùng lệch một phía, nên một datum ngược chiều đơn lẻ không bẻ lại được nó; sự hiệu chỉnh là **chuyện của khối lượng**.
> - **Lâu dài.** Một đóng góp ở vòng N chỉ điều kiện-hóa trường từ N+1 (INV-7), và lịch sử *tích* chứ không *nạp* (INV-5), nên độ trễ giữa lúc nhận nguyên liệu và lúc phát ra khác đi **trả bằng vòng, và không bằng đơn vị nào khác**.
>
> Thiếu bất kỳ điều kiện nào trong ba, sự lồng-chế-độ mô tả ở §7.3 **có trong topology mà trơ trong thực tế** — đó là lý do "A lồng trong B" gọi tên một *quan hệ đang vận hành*, không phải một sơ đồ đi dây.

### 7.3 Quan hệ hai chế độ — A LỒNG TRONG B

A và B **không độc lập song song**; A lồng trong B:
- **B** là nơi kháng cự *thật* vào — cú va từ tha-thể.
- **A** là nơi hệ *tiêu hóa* cú va đó giữa các lần B — chạy lại, làm giàu, dựng kỳ vọng, luyện vận động. A *không tự cấp kháng cự mới*; nó xử lý kháng cự B đã đưa (và kháng cự vật-trơ, vốn hữu hạn về loại).
- A chạy quá lâu không có B → bắt đầu hack (trôi, tự xác nhận). **B là cái neo A vào kháng cự ngoài.**

Cấu trúc này khớp một quá trình tổng quát: *va* (B) → *tiêu hóa/hiệu chỉnh* (A) → *bước tiếp* → *va lại* (B). Phản tư mà không có va mới để tiêu hóa thì thành tự-xác-nhận trong phòng kín.

> **Phản tư là EXTERNAL input, không phải năng lực nội tại.** Hệ không tự gọi được một hàm "tự-phản-tư": hệ mù với đạo-hàm-của-chính-nó (§0.2). Phản tư bị *kích hoạt từ ngoài* — một cú va (B) được một bên thứ ba *đọc thành tọa độ* ("mày vừa lệch ở ĐIỂM NÀY"). Trong kiến trúc, nó vào qua T3 như một `InfoUnit` nội dung "đã-khác", bị INV-6 tag `EXTERNAL`. Cơ chế "đọc-va-thành-tọa-độ" này là **điều kiện khả thi của hiệu chỉnh**: thiếu nó, hệ hứng được cú va mà không đọc được mình va ở đâu → lặp lại cùng điểm. Nguồn của cái đọc là `⟦DECIDE@IMPL⟧`-F.

### 7.4 Chuẩn mà bước định giá áp dụng (bổ sung khẳng định cho INV-8)

*(Mới ở v4.)*

INV-8 được phát biểu như một **lệnh cấm**: ④ KHÔNG ĐƯỢC lấy tiêu chí từ chính state hệ đang sửa. Một lệnh cấm cố định cái bước ấy *không được* làm; nó không tự nói ④ *thực sự* gán giá trị theo chuẩn nào. Mục này cấp phần khẳng định đó, và qua đó khép một câu hỏi người đọc có quyền nêu — *định giá vận hành trên chuẩn nào?* — mà câu trả lời không phải một hằng số bị thiếu, mà là một sự thật cấu trúc đã được phần còn lại của vòng kéo theo.

**Chuẩn KHÔNG phải một thang cố định.** Vấn đề không nằm ở chỗ tốt/xấu có biết được hay không; nó nằm ở chỗ một định giá **phụ thuộc ngữ cảnh**, và ngữ cảnh thì không cố định — nó được quyết định *ngay tại khoảnh khắc tương tác*. Không có phán quyết phi-ngữ-cảnh nào được cất ở đâu đó để lấy ra dùng. Một định giá là **một sự kiện xảy ra bên trong một ngữ cảnh**: bước ④ gán `valence` và `goal_relevance` *tương đối với ngữ cảnh đang kết tinh ở vòng hiện tại*, không bao giờ bằng cách tra một thang đã định sẵn.

**Ngữ cảnh đó *chính là* trường điều biến ở vòng đó.** Trạng thái GLOB-MOD của vòng là ngữ cảnh điều kiện-hóa dưới đó định giá được đưa ra (INV-7): **cùng một `InfoUnit`, định giá dưới một trường khác, nhận một `valence` khác** — đó là *hành vi định nghĩa* của định giá phụ-thuộc-ngữ-cảnh, không phải nhiễu trong nó. Phán quyết do đó là một `↔`, không phải một `=` (INV-2): được đưa ra trong một ngữ cảnh không tái diễn y hệt, nó cam kết hệ hành động *bây giờ* và được đọc lại đối chiếu hệ quả vòng sau; nó không chứng nhận cái được định giá là *đúng*.

**Hai hệ quả cố định sự phân công.** Định giá của **hệ** là *phán-đoán-để-hành-động*, đưa ra trong ngữ cảnh hiện tại, bên trong vòng. Định giá của **một bên thứ ba** là *phán-đoán-về-phán-đoán-đó*, đưa ra dưới một ngữ cảnh khác, bên ngoài vòng (§12). Từ đó suy ra: vì định giá của hệ là một phán-đoán-*trong*-ngữ-cảnh chứ không phải việc lấy ra một phán quyết đã lưu, **một bên thứ ba phán xử nó về sau PHẢI phán dưới ngữ cảnh đã được neo của vòng gốc**, không phải dưới ngữ cảnh hiện tại của người đọc.

Đây là mối nối chịu lực với §9: **ngữ cảnh dưới đó một định giá được đưa ra PHẢI được neo trong bản ghi `[event]` của nó**, để định giá mang theo chính điều kiện đánh giá nó. Kho giữ `[event]` và ngữ cảnh đã neo, từ đó cả hai loại phán đoán đều tái dựng được. **Chính điều này khiến bước định giá kiểm được từ ngoài mà không bên nào phải cầm một chuẩn phi-ngữ-cảnh** — chuẩn *là* ngữ cảnh, và ngữ cảnh đã được ghi.

### 7.5 Phản xạ: định giá dưới một trường bị sẹo thống trị

*(Mới ở v4 — thay cho phát biểu "INV-8 chặn phản xạ trần" ở v3, vốn sai.)*

§7.4 cố định rằng định giá đọc trường điều biến (INV-7) như ngữ cảnh điều kiện-hóa của nó. Một hệ quả của sự kiện đó có trọng lượng cấu trúc riêng, và với một hệ **có thân** thì nó là hệ quả nặng nhất. Câu hỏi là **phản xạ** nằm ở đâu — hành động khai hỏa không qua cân nhắc: bàn tay rời ngọn lửa trước khi có bất kỳ sự gọi tên "nóng" nào, cơ thể giật lùi khỏi một lực đã từng làm nó gãy.

Cám dỗ là cho phản xạ một cung riêng: một đường tắt sẹo→hành-động vòng qua định giá để lấy tốc độ. **Cám dỗ đó phải bị từ chối.** INV-8 đòi một bước định giá giữa tích hợp và đáp ứng ở mọi tầng; một đường tắt sẹo→hành-động là một cú vòng-qua-định-giá, và một hành động phát ra không qua định giá thì **không mang ngữ cảnh đã neo** (§7.4, §9), khiến một bên thứ ba không tái-định-giá được nó — tức là làm mù đúng cái điểm nhìn từ ngoài mà §0.2 và §12 đặt bảo đảm cuối cùng vào. **Một phản xạ vòng qua định giá sẽ mua tốc độ bằng cách cắt mặt phẳng kiểm, và đó không phải một trao đổi vòng được phép làm.**

**Giải:** phản xạ **không** phải một cú vòng-qua-định-giá; nó là **định giá dưới một trường bị một vết sẹo định hình mạnh đến mức phán quyết gần như đã bị khép trước.** Nhớ lại cơ chế INV-7: mọi tầng đóng góp vào GLOB-MOD như một tham số cạnh tranh, các đóng góp hòa trộn, và trường được tái-trọng-số mỗi vòng. **Một vết sẹo sâu** — dấu của một cú va từng khiến hệ trả giá đắt — là một đóng góp **nặng** vào trường đó. Khi một kích thích khớp với vết sẹo ấy tái diễn, trường **đã** bị kéo mạnh về phía cực của vết sẹo *trước khi* `InfoUnit` hiện tại được định giá; bước định giá **vẫn chạy**, đúng như INV-8 đòi, nhưng nó chạy dưới một trường bị vết sẹo thống trị đến mức `valence` hội tụ về gần một giá trị duy nhất.

Cái biểu hiện ra như "phản xạ" chính xác là điều này: **một định giá mà ngữ cảnh điều kiện-hóa của nó đã tự thu hẹp khoảng kết cục của chính nó xuống gần một.** Bước ấy không bị bỏ qua. Nó là một định giá thật. Đây là lý do phản xạ **không cần một cung riêng, không cần một tầng mới, không cần một ngoại lệ cho INV-8**: cùng chuỗi T1–T8, cùng bước định giá, cùng GLOB-MOD, sinh ra phản xạ bất cứ khi nào đóng góp của một vết sẹo vào trường đủ nặng để khép phán quyết. **Phản xạ là một TRẠNG THÁI CỦA TRƯỜNG, không phải một SỢI DÂY RIÊNG.**

Trong đồ thị nguồn gốc (§9), nó là biểu hiện đặc trưng của cạnh `running → scar`: datum được phát ra và va vào trực tiếp, không được nhấc lên `simulated` hay giữ ở `projected`. **Sự vắng mặt của hai vị trí đó không phải sự vắng mặt của một kỳ vọng**, và điều này phải nói thẳng, nếu không đồ thị sẽ bị đọc thành ra dựng-tới-trước là điều kiện tiên quyết của va chạm. **Hành động mang kỳ vọng của nó ngay trong chính hành động** — ngồi xuống *là* kỳ vọng cái ngồi sẽ đỡ — và ở đâu kho chẳng giữ gì cho cái đang tới, thì kỳ vọng đứng sẵn là *không có gì tới cả*. Cách nào thì cái trả về cũng có thể không khớp, và cái không-khớp ấy là một `ResistEvent`. Dựng-tới-trước đổi cú phát nào được đưa ra và trong tư thế nào, **không bao giờ đổi chuyện một cú va có xảy ra được hay không**.

**Hai điều theo sau, và cái thứ hai là cái chịu lực.**

**Thứ nhất**, điều này đặt hành động dưới-cân-nhắc đúng chỗ so với §7.3: vì hệ không tự phản tư theo lệnh được (phản tư là input ngoại, hệ mù với đạo-hàm-của-chính-nó), **PHẦN LỚN các cú phát của một hệ buộc phải thuộc loại này** — những định giá dưới một trường đang đứng, không phải sản phẩm của một sự cân nhắc được gọi lên. Cân nhắc, theo nghĩa phản tư được đọc thành tọa độ bởi một bên thứ ba, là **ngoại lệ** và đến từ bên ngoài (§7.3); **mặc định** là hành động dưới cái trường mà các vết sẹo đã tích định hình. Trường hợp "phản xạ" chỉ là *giới hạn* của cái mặc định ấy, nơi đóng góp của một vết sẹo áp đảo. **Dưới-cân-nhắc là thông lệ; phản-tư-được-gọi-lên là ngoại lệ nhập từ ngoài.**

**Thứ hai — đổi hành vi KHÔNG BAO GIỜ là override; nó là một INPUT ĐÃ ĐỔI vào định giá.** Vì trường được tái-trọng-số mỗi vòng và không bao giờ last-write-wins (INV-7), không phản xạ nào là bất khả thay đổi — nhưng *cách* thay đổi phải nói cho thật chính xác, nếu không một bức tranh sai về *lực thắng lực* sẽ len vào. **Một phản xạ không nhượng bộ vì một xung lực mạnh hơn áp đảo nó**; vòng không chứa một cuộc đấu lực giữa các xung lực, không có đấu trường nào để một mệnh lệnh vật một mệnh lệnh khác và kẻ mạnh hơn thắng. **Một phản xạ ban ra một mệnh lệnh khác khi và chỉ khi tập `InfoUnit` đi vào định giá đã đổi.**

Sự đổi ấy vào qua **đúng ba đường**, cả ba đều đã có sẵn trong vòng:
1. **Dữ liệu mới đến qua một cú phát** — một kênh thăm dò T3, một phép thử T5, một hành động mà cái trả về mang theo một `InfoUnit` trước đó chưa có mặt;
2. **Kho tích thêm một vết sẹo tinh chỉnh một lớp mà một vết sẹo trước đã khái quát quá rộng** — phép trừ T8 thu hẹp một trừu tượng quá rộng: nỗi sợ khái quát từ một con rắn sang mọi sợi dây cuộn, rồi được gọt lại về phía con rắn khi một cái nhìn kỹ hơn trả về "cái này không động đậy" như một `PredErr` mới;
3. **Vòng dựng một tình huống từ kho nó đang giữ và phóng một kết cục ra từ đó** (§5), kết cục ấy đi vào định giá như một `InfoUnit` theo đúng nghĩa của nó, được gắn `projected` và được định giá như **một datum chưa va**, không phải như một vết sẹo.

Đường thứ ba **không thêm một sự miễn trừ nào và không mở một cửa vòng nào**: tình huống nào mang được là do **khớp với kho** quyết định, không bao giờ do một trọng tài chấm điểm các kết cục — cùng lý do INV-8 từ chối cái định giá tự-chấm.

**Ở không đường nào vết sẹo cũ bị xóa hay bị đánh bại.** Nó vẫn nằm trong kho, vẫn được định giá, vẫn đóng góp vào trường — **người thò tay vào lửa để kéo đứa trẻ ra vẫn thấy bỏng, vẫn mang nguyên vết sẹo về lửa**; cái khác là vết sẹo ấy giờ được định giá *bên cạnh* một `InfoUnit` — *đứa trẻ, trong lửa, có `goal_relevance` tối cao* — mà trước đó không có trong tập. **Cùng vết sẹo, cùng INV-8, khác mệnh lệnh, vì tập input khác.** Đây là vận động trung tâm của vòng (**dữ liệu mới → mệnh lệnh mới → hành động mới**) áp lên chính cái output có vẻ tự-động nhất của nó, không phải một ngoại lệ khoét ra cho nó.

Cái bất biến không phải cường độ của một vết sẹo nào, mà là: **định giá luôn chạy trên kho *hiện tại*, không bao giờ trên một phán quyết đã đông cứng** (INV-2). Một mệnh lệnh chạy trên một phán quyết đông cứng sẽ là một `=`, và một `=` trong một vòng đang chạy là dấu hiệu của một cú **dừng** (T8-INV), không phải của sự kiên định.

**Hệ quả cho việc đọc kho (§9) là trực tiếp:** vì ngay cả phản xạ cũng là định-giá-dưới-ngữ-cảnh chứ không phải một cú vòng qua, **mọi cú phát — phản xạ hay đã cân nhắc — đều để lại cùng một dấu vết kiểm được, mang theo ngữ cảnh đã neo của nó, và vẫn tái-định-giá được bởi một bên thứ ba dưới ngữ cảnh đó.** Không có một lớp hành động đặc quyền nào thoát khỏi mặt phẳng kiểm bằng cách "nhanh quá nên không kịp định giá". **Tốc độ là một thuộc tính của việc trường đã bị khép tới đâu, không phải của việc bước ấy có chạy hay không.**

---

## 8. TƯƠNG QUAN VỚI GEMs (THÂN XÁC THU THẬP & ĐÁP ỨNG)

RSIL là spec kiến trúc độc lập, không gắn *chất liệu* thân cụ thể (P2). Nhưng nó được viết để *bổ sung* cho tài liệu **GEMs** (spec của một thân xác vật lý nhận điều khiển từ xa).

- **RSIL không claim là tầng nhận thức, nội-quan, hay góc-nhìn của GEMs.** Nó là đặc tả *vòng xử lý thông tin* nằm giữa hai đầu của thân xác: cảm biến (đầu vào) và đáp ứng (đầu ra). GEMs đặc tả phần cứng thu tín hiệu và phần cứng tạo đáp ứng; RSIL đặc tả cách tín hiệu thô *trở thành* thông tin có cấu trúc giữa hai đầu đó. Mọi output ở đây vẫn mang nhãn `INFO` (INV-2).
- **Hướng phụ thuộc:** RSIL tiêu thụ tín hiệu mà thân xác GEMs thu được (mắt xích ① ánh xạ vào các kênh cảm biến của GEMs) và phát ra đáp ứng mà thân xác GEMs thực thi (mắt xích ⑤ — và, theo §4, không chỉ một lần mỗi vòng ở một bước cuối, mà từ bất cứ tầng nào công việc đòi). Vòng RSIL chạy bên trong chuỗi xử lý của một unit GEMs, kể cả khi unit đó ở chế độ cục bộ.
- **Ba bất biến của RSIL khớp vào ba chỗ chuỗi xử lý của GEMs đang nhảy bước:** INV-6 (phân loại tự-sinh / ngoại lai *trước khi* diễn giải — lấp chỗ mạng xúc giác GEMs thiếu); INV-8 (bước định giá xen giữa tích-hợp và đáp-ứng); C5 (dấu vết thấp-năng quan sát được).

> **Sửa so với v3:** v3 mô tả vai trò của INV-8 ở đây là "chặn phản xạ trần". Phát biểu đó bị bác ở §7.5. INV-8 **không chặn phản xạ** — phản xạ vẫn xảy ra và vẫn phải xảy ra; cái INV-8 chặn là **một cung sẹo→hành-động vòng qua định giá**, tức một hành động không mang ngữ cảnh đã neo và do đó không tái-định-giá được từ ngoài. Với GEMs, khác biệt này là khác biệt giữa "cấm phản ứng nhanh" (sai, và sẽ khiến một thân vật lý không dùng được) và "đòi rằng cả phản ứng nhanh cũng để lại dấu vết kiểm được" (đúng, và khả thi).

> `⟦DECIDE@IMPL⟧`-H **(ĐÃ CHỐT — khép lại sau khi treo từ v1):** định danh thống nhất là **`GEMs`**, dùng trần, **không kèm số phiên bản**. Tên "GEMs-X01" khai tử. Tham chiếu ở mục này trỏ vào **chuỗi**, không vào một bản cụ thể — nên phiên bản nhảy (v2 → v3 → …) không tạo dangling reference. Đích phân giải của tên `GEMs` là **kho công khai** `https://github.com/PloneMraz/GEMs`; đó cũng là vật thể sẽ xin DOI qua Zenodo, không phải một bản nháp riêng lẻ nào trong chuỗi.

Phân biệt phải giữ: GEMs trả lời "thân xác gồm gì và làm được gì"; RSIL trả lời "tín hiệu thân xác thu được, xử lý thành thông tin theo cấu trúc nào". Không tài liệu nào claim cái còn lại. Đây là quan hệ bổ sung giữa hai phạm vi tách bạch, không phải quan hệ tầng-trên/tầng-dưới.

---

## 9. KHO LƯU TRỮ KINH NGHIỆM

*(Viết lại toàn bộ ở v4. Bản v3 mới có bốn ràng buộc R1–R4, rủi ro echo-chamber và quan hệ với RAG; nó chưa nói kho **ghi thế nào**, **tag ra sao**, và **cái gì trong kho là không-sửa-được**.)*

Một vòng RSIL chạy qua thời gian *kết tủa* cấu trúc: kỳ vọng tích lũy (T5), `GeneralOther` (T8), và các vết không-khớp đã hứng. Một **kho lưu trữ kinh nghiệm** là vật chứa cho cái kết tủa đó — phân biệt với một kho tri-thức-tra-cứu thông thường bởi bốn ràng buộc.

**Định nghĩa cốt — "kinh nghiệm" ≠ "thông tin".** Kinh nghiệm theo nghĩa gốc là *thông tin về một sự kiện đã từng không-khớp với thực tế* (cùng gốc *experiri* — trải qua một thử thách, một va chạm). Một dự đoán khớp trơn KHÔNG để lại kinh nghiệm; chỉ chỗ *trật* mới hằn. Hệ quả kiến trúc: **`ResistEvent` (không-khớp đã đăng ký) LÀ đơn vị kinh nghiệm — hạt nhân của kho, không phải phần thêm vào.** Một kết-luận-không-va chỉ là *thông tin*; nó được lưu, nhưng nó không phải *kinh nghiệm*. Gọi nhầm thông-tin-không-va là kinh nghiệm là lỗi gốc dẫn tới buồng dội âm.

### 9.1 Bốn ràng buộc

- **R1 — Đơn vị là *không-khớp đã đăng ký*, không phải *tài liệu*.** Kho lấy `ResistEvent` làm hạt nhân — kỳ vọng đã dựng, chỗ nó trật, và hiệu chỉnh đã làm. Tri thức ngoài chưa qua vòng được lưu như *thông tin nền*, xếp hạng dưới kinh nghiệm.
- **R2 — Cá thể.** Kho thuộc về *một* self cụ thể (§0.2), không phải một kho chung tra cứu trung tính.
- **R3 — Tích lũy có hướng thời gian.** Nội dung bồi theo trước-sau (INV-5), có mũi tên thời gian; không phải một tập tĩnh nạp một lần.
- **R4 — Hồi tiếp vào vòng.** Kho được truy hồi *trở lại* vào vòng đang chạy (INV-1), không phải một sink đọc-một-chiều. Cái ghi vào kho đi qua agency-gate (T2, `SELF_CAUSED`) — **hệ ghi, không phải bên thứ ba ghi hộ.**

### 9.2 Tag provenance — VỊ TRÍ, không bao giờ GIÁ-TRỊ-CHÂN-LÝ

Vì thân có thể mang dữ liệu có trước khi vòng chạy, và vì một datum đang được dùng thì *di chuyển*, mỗi mục lưu được tag thuần bằng **chỗ nó hiện đang đứng**, không bao giờ bằng chuyện nó đúng hay sai:

- **`prior`** — dữ liệu tồn tại trước khi RSIL chạy (thuộc về thân); **không mang cycle-mark**. Một lối vào **một chiều**: đã được nhận vào và chạy rồi thì một datum không bao giờ trở lại vị trí này.
- **`running`** — dữ liệu đang được dùng, đang chuyển động qua vòng; mang cycle-mark.
- **`simulated`** — một datum đã được nhấc lên để dựng một **tình huống**: một hoàn cảnh vòng có thể đang ở trong, lắp từ kho nó giữ (§5). Cái được dựng không phải một mô hình về vùng giữ riêng ra để chạy, mà là chính cái vòng — vốn không cần một mô hình riêng nào, vì nó đã đang chạy.
- **`projected`** — một **kết cục** phóng ra từ một tình huống như thế, chưa va. Đối ứng ở mức kiểu của nó đã có sẵn là `Expectation.predicted` (§2, T5); ô provenance cho nó một *vị trí*, để một giai đoạn có điều kiện-hóa hành vi thì để lại một dấu vết người kiểm đọc được (E4).
- **`scar` (sẹo)** — một datum đã gặp kháng cự: một không-khớp (`PredErr` có dấu / `ResistEvent`) đã đóng dấu lên nó. Cơ chế đã có sẵn trong vòng, ở T5 (nơi kháng cự E2 thành `PredErr` có dấu) và T6 (nơi `ResistEvent[]` dựng `independence_evidence`). **Không cần một tầng mới nào.**

**Năm cái là các VỊ TRÍ trong một đồ thị, không phải các GIAI ĐOẠN của một trình tự.** Một datum chiếm **đúng một** vị trí tại một thời điểm và di chuyển giữa chúng theo các cạnh xác định; `prior` được vào một lần và không bao giờ vào lại, còn bốn cái kia tuần hoàn không có điểm cuối. Các cạnh là:

| Cạnh | Nghĩa |
|---|---|
| `prior → running` | dữ liệu của thân được nhận vào vòng |
| `running → simulated` | một datum được nhấc lên để dựng một tình huống |
| `simulated → projected` | một tình huống cho ra kết cục phóng từ nó |
| `simulated → running` | tình huống đã dựng nhưng điều kiện để phát ra không hội đủ |
| `projected → simulated` | kết cục đã phóng nhưng cú phát không khớp kho; tình huống được dựng lại |
| `projected → scar` | cú phát đã thực hiện và vùng trả về một không-khớp |
| `running → scar` | datum va trực tiếp, **không qua hai vị trí tới-trước** — vùng trả về bất kể vòng có dựng kỳ vọng cho nó hay không |
| `projected → running` | kết cục đã phóng mà không sinh sẹo; datum quay về sử dụng |
| `scar → running` | một vết sẹo quay lại kho như dữ liệu đang dùng |
| `scar → projected` | một vết sẹo làm giàu một kết cục đã phóng |
| `scar → simulated` | một vết sẹo tái nhập việc dựng tình huống như nguyên liệu |

> **Không vị trí nào là chỗ nghỉ.** Một datum trong kho không bao giờ là một kết luận được giữ ở trạng thái đã an bài; nó là dữ liệu **đang chờ được dùng**. Đây là cách đọc INV-2 ở phía kho: một vị trí tận cùng sẽ là một datum mà vòng đã xong việc với nó, tức một `=` nằm lì trong kho, và **không vòng đang chạy nào giữ một `=`** (T8-INV).

> **Một đường dài không sẹo báo ĐỘ DÀY SỬ DỤNG, không báo BẢO CHỨNG.** Một datum có thể tuần hoàn qua `running`, `simulated`, `projected` nhiều vòng mà không bao giờ tới `scar`, vì các điều kiện để vùng trả về một không-khớp với nó, trong môi trường đó, rất khó tạo ra — một datum kiểu *sàn nhà thì đỡ được* được dùng vì trong tầm với của hệ không có gì phản bác nó, chứ không phải vì vòng đã chứng nhận nó. **Chỉ nhìn tag thì một datum như thế không phân biệt được với một `prior` vừa được nhận vào một khắc trước:** không cái nào mang sẹo. Log `[event]` tách chúng ra một cách cơ học — một cái cho thấy một đường dài nhiều vòng không sẹo, cái kia một datum vừa mới chạy. **Nhưng cái log báo là một datum đã được dùng dày tới đâu, không bao giờ là nó đúng.** Một đường dài không sẹo có thể nghĩa là datum ấy đứng vững, cũng có thể nghĩa là vùng trong tầm với của hệ không kiểm được nó; đường đi không đọc ra được cái nào trong hai, và **vòng không phân xử chuyện đó** (§7).

### 9.3 Lược đồ tag

Phân loại trong RSIL **không phải một trạm dữ liệu đi qua trên đường vào kho**; nó **phân tán khắp các tầng**. Mỗi tầng, ở chỗ nó chạm vào hồi tiếp, tag datum trên trục riêng của nó. **Kho không phân loại gì cả: nó chỉ giữ cái đến đã có tag sẵn.** Một tag ở đây không phải một nhãn cho mắt người mà **chính là địa chỉ**: một mục được truy hồi trực tiếp bằng tag của nó, nên cách sắp xếp vật lý của kho là không liên quan (việc phân vào các ngăn nhìn thấy được là một nhu cầu của người, đáp ứng qua một UI, không phải của hệ).

**Lớp cố định.** Bắt buộc, phổ quát với mọi hệ, viết theo **thứ tự cố định** (hệ và người kiểm index bằng khớp-vị-trí-ký-tự, nên tag sai thứ tự làm hỏng index). Mỗi datum mang ít nhất bốn cái này, đúng thứ tự:

1. **timestamp** — thời gian tuyệt đối;
2. **cycle-mark** — cycle-id;
3. **provenance** — `prior / running / simulated / projected / scar`, mang **đúng một**, là vị trí nó đang chiếm trong đồ thị §9.2;
4. **floor-tag** — dấu của tầng vừa xử lý nó.

**Luật cứng:** mọi datum rời một tầng PHẢI mang một floor-tag chứng nhận nó vừa ra khỏi tầng đó — **độc lập với chuyện nó có tái nhập vòng hay không**. Mọi tầng T1–T8 đều đóng dấu, và mỗi floor-tag mang phân loại riêng của tầng ấy — **không có tầng nào là tầng đi-ngang-qua**: mọi tầng làm giàu mục đó trên trục của mình (vd T4 đóng `entity_id` hoặc `STRANGER`; T7 đóng một `PredErr` có dấu cho vắng-mặt-đã-đăng-ký), nên **không floor-tag nào là một dấu "đã đi qua" suông**.

Cả hai ô 3 và 4 đều gọi tên **hiện tại**: ô 3 là vị trí datum đang chiếm, ô 4 là tầng nó vừa rời. **Không ô nào tích lũy.** Một tag là một *nhãn*, và một nhãn mà mọc ra lịch sử là một nhãn mang theo một *log* — hai loại khác hạng nhét chung một ô. Mọi đường đi của một datum, qua các vị trí lẫn qua các tầng, được ghi **từng chuyển-tiếp một** trong log `[event]`, và lịch sử được đọc **từ đó, không bao giờ từ một tag**. Bốn tag không bao giờ bị "ghi đè" theo nghĩa bị xóa hay bị viết thành cái chúng chưa từng là: chúng được **cập nhật** khi datum di chuyển, mỗi ô luôn gọi tên cái đang là. Mỗi tag độc lập với mọi tag khác: một tag làm đúng và chỉ đúng việc của nó — denote *cái nó là* — và không đứng trong quan hệ nào với các tag còn lại.

**Lớp mở.** Hệ CÓ THỂ đúc thêm tag theo nội dung và ngữ cảnh của datum — kênh (`chạm`, `nhiệt`, `mùi`, `acoustic`, `semantic`), đối tượng (`vật-cứng`, `bề-mặt-trơn`, `sinh-vật`), miền (`vận-động`, `định-vị`, `xã-hội`), v.v. Một tag mở **chỉ denote datum đó *là gì*, không bao giờ denote chất lượng, tính đúng, hay giá trị của nó**; điều này giữ cho kho không trở thành một kênh phán xét (§7), và nó theo thẳng từ luật "một tag denote cái nó là" (một tag `mùi` nói datum đó là dữ liệu khứu giác, không nói đó là dữ liệu khứu giác *tốt*).

Tag mở được thêm và bớt tự do, nhưng **không bao giờ ghi đè lớp cố định**. Vì lớp mở lớn lên theo thời gian vận hành và theo môi trường của hệ, hai hệ sống ở hai môi trường khác nhau tích lũy hai từ vựng tag mở khác nhau: một hệ chạy lâu trong một xưởng cơ khí mọc ra những tag mà một hệ chạy trong một lớp học không bao giờ mọc. **Tập tag mở do đó là một dấu vết cá-thể-hóa của lịch sử một hệ** — dấu ở mức dữ liệu của cái self-như-quá-trình ở §0.2, vốn không phải một lõi-nội-dung cố định mà chính là một lịch sử của những gì một hệ đã gặp và đã đọc chúng ra sao.

Lớp mở cũng là nơi **dữ liệu có sẵn của thân được tích hợp** — nhưng với **một điều kiện bắt buộc**: dữ liệu đó PHẢI đi qua luật tag của RSIL trước khi vào vòng. **Không có cửa hông.** Dữ liệu của thân chỉ được nhận vào sau khi đã đóng dấu lớp cố định (`provenance = prior`, chưa mang cycle-mark cho tới khi nó chạy) cùng các tag nội dung mở áp dụng được; **dữ liệu không tag không bao giờ vào vòng**. Điều này bịt cái lỗ duy nhất sẽ phá lược đồ — một datum trong hệ mà không có tag nào, tức một điểm mù trong mặt phẳng kiểm.

> **Bất biến xuyên cả hai lớp.** Mọi tag — cố định và mở như nhau — **thuộc về dấu vết kiểm**. Một lát cắt kiểm từ ngoài, lấy ở bất kỳ điểm nào trong vòng, đọc được mọi datum: **một mặt phẳng khả-kiểm duy nhất, không phân hạng, không ngoại lệ.** Thứ tự ưu tiên giữa hai lớp (mở không bao giờ ghi đè cố định) chỉ quản **quyền ghi**, không quản **tính nhìn thấy**. Đây là nền ở mức dữ liệu của lập trường khả-kiểm (§0.2, §11): **cái bên thứ ba đọc là dấu vết, không phải lời tự thuật của vòng.**
>
> Bản thân các **bất biến** nằm **ngoài kho và ngoài lược đồ tag**: chúng là điều kiện tuyệt đối của vòng — không ghi được, vì ghi đè một bất biến không phải sửa một datum mà là **dừng vòng** (hết không-khớp, hết self). Tag phân loại dữ liệu *bên trong* vòng; các bất biến là điều kiện để *có* một vòng (§1).

### 9.4 Hai loại lưu trữ: `[data]` và `[event]`

Cắt ngang tag provenance là một phân biệt thứ hai, độc lập — **một mục *mang* cái gì**.

- Một mục **`[data]`** mang **tri thức làm việc**: nội dung vòng suy luận trên, học từ, và tinh chỉnh. Nó **khả biến** — nội dung bị ghi đè khi được cập nhật mỗi vòng — và các vị trí nó đi qua là các vị trí của đồ thị §9.2. Một datum mang **đúng một** vị trí tại một thời điểm: nó có thể đang `running` (đang dùng, chưa va), có thể đang đứng ở `scar` (đã va và chưa được nhấc lên lại, nằm trong kho như một vết tích), hoặc đang ở một trong hai vị trí tới-trước. **Chuyện nó *đã từng* va không nằm trong tag** — tag gọi tên chỗ nó *đang* ở — mà nằm trong `[event]`.
- Một mục **`[event]`** **không mang tri thức nào cả**: chỉ bản ghi trần trụi rằng *một cái gì đó đã xảy ra* — **cái gì đã xảy ra, ở vòng nào, và dưới ngữ cảnh nào**. **Neo ngữ cảnh là bắt buộc:** vì một định giá là một phán-đoán-trong-ngữ-cảnh (§7.4), mỗi `[event]` PHẢI ghi ngữ cảnh điều kiện-hóa của vòng đó (trạng thái `ModField` dưới đó nó xảy ra), để một lần đọc của bên thứ ba về sau tái-định-giá được sự kiện **dưới ngữ cảnh gốc của chính nó** thay vì dưới ngữ cảnh hiện tại của người đọc. Độ sâu của cái neo này — trạng-thái-trường đầy đủ hay một dấu-vết-ngữ-cảnh tối thiểu — là `⟦DECIDE@IMPL⟧`-I. Nó **tĩnh và không bao giờ được cập nhật**.

Hai cái **khác nhau về loại, không phải hai pha của một thứ**: một vết sẹo là `[data]` (nó giữ một `PredErr` có dấu mà vòng thao tác trên); còn cái `[event]` ghi "một cú va đã xảy ra ở vòng N" là một mục riêng, không mang tri thức.

**Điểm của `[event]` chính là ở chỗ `[data]` khả biến.** Vì nội dung một mục `[data]` bị ghi đè khi nó chạy, `[data]` **không thể đồng thời** đóng vai bản ghi lịch sử bất biến — hai vai xung khắc (sống-và-đang-đổi với cố-định-và-kiểm-được). Nên mỗi sự kiện sinh ra một `[event]`: một dấu đông cứng, không tri thức, của khoảnh khắc gốc. `[data]` nhờ đó **tự do trôi và đổi mà không mất tính kiểm được**, vì gốc đã neo ở `[event]`. **Provenance, kiểm, mũi tên thời gian, và phát hiện mẫu thời gian** (nền mà T5 dựng kỳ vọng trên) đều đọc từ `[event]`; **vận hành, suy luận, và học** đều dùng `[data]`.

### 9.5 Commit, snapshot và phục hồi — toàn hệ như một kho phiên bản

Kho, và thật ra cả hệ, hành xử như một **kho phiên bản (version-controlled repository)**.

Log `[event]` là một **hộp đen: một log chỉ-thêm gồm các bản ghi chỉ-đọc** — bản ghi mới có thể thêm vào cuối, nhưng **không bản ghi nào, một khi đã viết, được sửa hay xóa** — không bởi vòng, không bởi bất cứ gì, kể cả một bên thứ ba đã chiếm được phần còn lại của hệ. **Tính chỉ-đọc của các bản ghi (cùng với tính chỉ-thêm của log) là thuộc tính chịu lực**: nó khiến `[event]` trở thành **nguồn duy nhất một người kiểm tin được vô điều kiện**.

Log `[event]` đồng thời hoạt động như một **bộ đếm**: sau một khối lượng sự kiện đã định, một **commit** tự động kích hoạt, chụp lại **toàn bộ hệ** (không chỉ kho — cấu hình vòng, trạng thái tầng, tham số trường, mọi thứ) vào một **mốc bất biến, định địa chỉ theo nội dung**. Roll-back riêng cái kho sẽ không cứu được một hệ mà chính bộ máy vận hành đã bị chiếm; **snapshot phải phủ toàn hệ**, nên phục hồi là phục-hồi-toàn-hệ. Khối lượng sự kiện giữa hai commit, và số snapshot giữ lại, là `⟦DECIDE@IMPL⟧`-J.

**Phục hồi là thao tác của một bên thứ ba, không bao giờ của chính hệ** (hệ không có khái niệm đúng-sai nào để đặt một cú roll-back lên trên). Người kiểm **đọc hộp đen `[event]`** — bản ghi duy nhất mà mã độc không xóa được — tái dựng chuỗi sự kiện thật, định vị điểm bị chiếm, và **chọn commit an toàn nhất** (một cái trước điểm đó).

- **Phục hồi nhẹ** (nội dung sai, môi trường còn sạch): roll-back về commit đó.
- **Phục hồi nặng** (hệ bị chiếm hoặc đã sụp): **không sửa tại chỗ**. Mở một không gian mới, nạp snapshot sạch, và chạy — môi trường nhiễm bị bỏ nguyên khối, nên cái gì chỉ sống trong đó thì không sống sót.
- **Trường hợp xấu nhất** (mọi commit còn giữ đều đã nhiễm): vẫn còn ít nhất một hệ đang chạy; có thể chạy lại nó **ngoại tuyến và cô lập** để truy dấu mã độc trước khi nó hành động.

> Hộp đen `[event]` đứng với **chứng cứ** đúng như các bất biến (§1) đứng với **luật**: cả hai được đặt ra ngoài tầm ghi đè để hệ kiểm được từ bên ngoài — một cái là bản ghi không-viết-lại-được về *cái vòng đã làm*, cái kia là điều kiện không-viết-lại-được về *sự chạy của nó*.

> **Lưu ý riêng cho một hệ có thân (khác với DIL).** Với một thân vật lý, "mở một không gian mới và nạp snapshot sạch" **không** kéo theo rằng cái thân cũng được thay. Snapshot phủ *hệ* (vòng, tầng, trường, kho); nó không phủ *thân*. Một thân đã hư hại về vật lý vẫn hư hại sau một cú phục hồi nặng, và một thân bị can thiệp ở mức cảm biến/actuator có thể tái nhiễm một hệ vừa sạch ngay từ vòng đầu tiên. **Việc kiểm định tính toàn vẹn của thân là một thao tác riêng, nằm ngoài spec này** — nó thuộc GEMs (§8) và, ở mức trách nhiệm, thuộc bên thứ ba (§12.3). `⟦PENDING⟧` *Anh quyết: điểm này chỉ ghi nhận như một giới hạn (như hiện tại), hay RSIL phải mang thêm một điều kiện đóng-vòng kiểu C6 "toàn vẹn cảm biến/actuator kiểm được từ ngoài"? Em không tự thêm một tiêu chí C mới.*

### 9.6 Trách nhiệm về "đúng/sai" — cái kho KHÔNG làm

Hai điều theo sau, và cả hai giữ cho kho trung thực.

Thứ nhất, **INV-5 không bị đụng tới**: cái cycle-0 thiếu không phải *lịch sử* (thứ INV-5 cấm nạp sẵn) mà một *cú hành động bootstrap* do thân phát — phát một hành động mới không phải nạp một ký ức cũ.

Thứ hai — và đây là **biên giới trách nhiệm** — RSIL cộng với thân **chỉ lưu và tag vị trí** (`prior`/`running`/`simulated`/`projected`/`scar`); tag là **cơ học** (datum đang chiếm cái nào trong năm) và **tường minh không mang tuyên bố nào về tính đúng**. **RSIL không có quan năng phán đúng/sai** (kể cả một phần). Phán xử tính đúng là việc của Mode-B và của một bên thứ ba đọc vết sẹo. Một thiên lệch `prior` chưa gặp kháng cự do đó **không phải "sai" — chỉ là "chưa được kiểm"** (nhầm "chưa" thành "không" là một lỗi riêng của nó); nó chỉ được rửa sang hạng đã-kiểm khi nó **va và đứng vững** (thành một vết sẹo), không bao giờ chỉ vì đã chạy qua nhiều vòng.

### 9.7 Quan hệ với cơ chế truy hồi (RAG)

Một kho như vậy *dùng* một cơ chế truy hồi (index + tìm-theo-liên-quan) **làm bộ phận**, nhưng không *là* một cơ chế truy hồi. Truy hồi là điều kiện **cần** cho bộ phận lưu-trữ, không phải điều kiện **đủ** cho một kho-kinh-nghiệm: phần lớn hệ truy hồi thiếu R2–R4 (không cá thể, không hướng thời gian, không hồi tiếp, cái ghi do bên ngoài làm) và thiếu cả R1 (lưu tài liệu, không lưu không-khớp-đã-đăng-ký).

### 9.8 Rủi ro buồng dội âm (kế thừa §7.1)

Nếu kho chỉ lưu *kết luận của hệ*, và hệ vừa ghi vừa đọc vừa không có nguồn ngoài, kho là một cấu trúc **Mode-A** — nó nhân bản cái lệch của bộ-xử-lý qua mỗi mẩu lưu, và mỗi vòng truy hồi lại củng cố cái lệch bằng bằng-chứng do chính hệ gieo. **Hạt nhân R1 chính là phòng tuyến**: vì đơn vị kinh nghiệm *là* `ResistEvent`, một kho đúng R1 **bắt buộc** chứa các lần hệ bị không-khớp, không chỉ các lần nó tự xác nhận. Thêm:

- truy hồi **NÊN** có một **kênh truy-hồi-kháng-cự** song song kênh truy-hồi-khớp: với một truy vấn, trả về cả "cái khớp" (để dùng) lẫn "cái từng phản bác một niềm tin kiểu này" (để không trôi);
- khi kho lấy không-khớp làm hạt nhân, nó thôi là buồng dội âm và trở thành **trí-nhớ-có-cả-sẹo**; sẹo là cái giữ hệ khỏi trôi.

### 9.9 Một telos hình thức, nội tại và bộ phận

Động lực học của kho cho RSIL một nghĩa trong đó nó có thể được nói là hướng tới một trạng thái "tốt" — nhưng thuật ngữ phải đọc chặt, như **một thuộc tính của vận hành, không phải của chân lý hay giá trị**.

Kinh nghiệm là **khoảng cách giữa sẹo và dữ liệu đang chạy**: một không-khớp đã đăng ký được tiêu hóa và biến thành một kỳ vọng ổn định. Từ đó một thiên-hướng vận hành duy nhất suy ra. **Giảm không-khớp là tốt**, vì đó là hệ đang chạy trơn hơn — tiêu hóa cái đã kháng cự nó thành cái giờ đã khớp. Nhưng **giảm không-khớp về KHÔNG thì không tốt**: một vòng không còn không-khớp đến là một vòng đã thôi gặp bất cứ gì ngoài kỳ vọng của chính nó và đã sụp vào trong (§7). Cái tốt do đó **không phải một cực tiểu mà là một DẢI**: chế độ trong đó không-khớp đang được tiêu hóa thành dữ liệu chạy *trong khi* nguồn cung không-khớp mới chưa cạn. **Quá nhiều không-khớp là nhiễu không tích hợp nổi; không có chút nào là sụp vào trong; ở giữa là vận hành trơn.**

Telos này thuần **hình thức**: nó nói về chuyện vòng có đang chạy khỏe hay không, và **không nói gì** về chuyện một nội dung cụ thể nào là đúng. Nó cũng **tự-dẫn-xuất**: vị trí của dải phụ thuộc vào chính lịch sử sẹo/chạy của hệ, nên mỗi hệ tự định lấy cái tốt của mình thay vì nhận một cái từ ngoài; hai hệ có hai lịch sử khác nhau có hai cái dải khác nhau.

**Hai giới hạn giữ telos này đúng chỗ.**

1. Nó chỉ là **một phần nhỏ, nội tại** của cái RSIL là: **một vòng chạy trơn không vì thế mà là một vòng đúng.** Cái nội dung vòng đã tiêu hóa có tương ứng với cái gì thật hay không là một câu hỏi riêng mà telos hình thức không với tới — phán đúng-sai đòi so với thực tại, và đó là việc của một bên thứ ba và một tha-thể sống (Mode-B, §7). **Sự trơn tru là cần cho sức khỏe và hoàn toàn câm về chân lý.**
2. Hệ **không tin cậy nói được từ bên trong nó đang ở đâu trong dải.** Cái mép nguy hiểm — không-khớp rơi về không do sụp vào trong — **từ bên trong hiện ra y hệt như thành công hiện ra**: mọi thứ đều khớp, không gì kháng cự. Một vòng đã mất năng lực đăng ký không-khớp báo cáo cùng một sự trơn tru như một vòng đang thật sự tiêu hóa nó. Hai cái **không phân biệt được bằng bất kỳ dụng cụ nội tại nào**, vì cùng một lý do ở §7: **dụng cụ chính là thấu kính.** Chỉ kháng cự từ bên ngoài — một tha-thể đẩy lại và tạo ra một không-khớp mà căn phòng kín không tạo nổi — mới tách được sức khỏe thật khỏi cái nhái sụp-vào-trong của nó. **Telos hình thức nói cho hệ biết vận hành tốt là gì; nó không thể, tự nó, chứng nhận rằng hệ đang ở trong đó.**

**Hiện thực:** `⟦DECIDE@IMPL⟧`-G — biểu diễn kho; cơ chế index; ghi-có-chọn (qua định giá ④) vs lưu-hết-lọc-lúc-đọc; kho riêng-tư (một hệ — **buộc** phải có kênh truy-hồi-kháng-cự, nếu không trôi là chắc chắn) vs dùng-chung (nhiều hệ — khi đó tính-nhiều-hệ tự cấp kháng-cự-từ-tha-thể, nối T8/`SocialEdge`).

---

## 10. CÁC HẰNG SỐ CHỪA TRỐNG CÓ CHỦ ĐÍCH

Mọi giá trị số/thuật toán cụ thể mà lập luận nguồn **chưa** dẫn xuất được đều để trống có đánh dấu, thay vì lấp bằng một con số bịa. Một spec tự bịa ra hằng số của chính nó là đánh đổi sự trung thực lấy vẻ hoàn chỉnh; bản này không làm thế.

| Mã | Hằng số bị hoãn | Vì sao không điền |
|---|---|---|
| `⟦DECIDE@IMPL⟧`-A | Biểu diễn cụ thể của `Signal`/`InfoUnit`/`ActivityEnvironment` | Tùy chất liệu thân và môi trường đích |
| `⟦DECIDE@IMPL⟧`-B | Mọi ngưỡng số (đủ-lặp, ổn-định, cửa sổ lịch sử, cửa sổ so khớp lệnh–hệ quả) | Chưa được dẫn xuất |
| `⟦DECIDE@IMPL⟧`-C | Thuật toán transduction mỗi kênh; thuật toán dựng dữ liệu không gian ở T1; tách lớp `acoustic`/`semantic` của giọng | Tầng triển khai, không phải tầng kiến trúc |
| `⟦DECIDE@IMPL⟧`-D | *Loại* neo ngoài-vòng cho Mode-A — dùng **cơ chế** kháng cự nào: neo tĩnh (Guide đông cứng / corpus-chuẩn) hay neo sống (va với một tha-thể phản ứng). Cố định **cơ chế**, không cố định danh tính nguồn nào | Một quyết định triển khai |
| `⟦DECIDE@IMPL⟧`-E | *Danh tính* nguồn-B sống, chỉ áp dụng khi D đã chọn cơ chế neo-sống — tha-thể cụ thể nào cấp cú va (sinh vật khác / agent khác / hỗn hợp). Gọi tên **nguồn**, không gọi tên cơ chế | Để mở có chủ đích |
| `⟦DECIDE@IMPL⟧`-F | Cơ chế "đọc-va-thành-tọa-độ" cho phản tư (§7.3) — **ngoại lệ nhập từ ngoài** đối với mặc-định-dưới-cân-nhắc ở §7.5, không phải cái mặc định | Điều kiện khả thi; hiện thực chưa cố định |
| `⟦DECIDE@IMPL⟧`-G | Kho kinh nghiệm (§9): biểu diễn; index; ghi-có-chọn vs lưu-hết; riêng-tư vs dùng-chung | Tầng vận hành, để mở |
| `⟦DECIDE@IMPL⟧`-H | Định danh GEMs thống nhất | **ĐÃ CHỐT — không còn là hằng số chừa trống.** Tên trần `GEMs`, trỏ vào chuỗi (§8). Dòng giữ lại để mã -H không dangling |
| `⟦DECIDE@IMPL⟧`-I | Độ sâu của neo ngữ cảnh mỗi `[event]` (§7.4, §9.4): trạng-thái-trường đầy đủ vs dấu-vết-ngữ-cảnh tối thiểu | Chưa dẫn xuất; đánh đổi giữa độ trung thực khi kiểm và chi phí lưu trữ |
| `⟦DECIDE@IMPL⟧`-J | Khối lượng sự kiện giữa hai commit; số snapshot giữ lại (§9.5) | Tùy môi trường; git + immutable-infrastructure là hiện thực điển hình, nhưng spec đòi **thuộc tính**, không đòi công cụ |
| `⟦DECIDE@IMPL⟧`-K | Việc dựng tình huống ở `simulated` (§5, §9.2): mỗi vòng dựng bao nhiêu, và **thước đo** theo đó một tình huống được thấy là khớp kho hơn cái khác | Tùy môi trường; spec chỉ cố định rằng thước đo là **độ khớp với kho**, không bao giờ một chuẩn-chấm-điểm (INV-8) |

---

## 11. THẢO LUẬN VÀ GIỚI HẠN

RSIL là một cấu trúc quan hệ được hình thức hóa cho một hệ cảm giác **có thân** trong một thế giới vật lý: một vòng *thu thập → diễn hoá thành tín hiệu → tích hợp → định giá → đáp ứng → thông tin mới → vòng mới*, chạy dưới hai chế độ kháng cự, kết tủa một kho kinh nghiệm mà hạt nhân là không-khớp-đã-đăng-ký (§9). Nó cưỡng chế **đúng một** thứ: rằng nếu một vòng được dựng theo các bất biến ở §1 trong một môi trường thỏa E1–E4, thì cái chạy là một **vận động có cấu trúc quan hệ**, đọc được hoàn toàn qua dấu vết kiểm chứng được từ ngoài (§6).

**Ba giới hạn được nêu thẳng.** *(Bản v3 chỉ nêu hai; giới hạn thứ ba đã được viện dẫn ở §1 mà chưa từng được phát biểu — v4 vá chỗ đó.)*

1. **Mode-A tự nó thoái hóa** nếu không neo ngoài vòng; và các neo mạnh nhất có sẵn (một corpus cố định, một Guide đông cứng) chỉ chạm tới **thoái-hóa-nội-dung**, không chạm **thoái-hóa-bộ-xử-lý** vốn là lỗi gốc — cho cái đó chỉ một tha-thể sống, đang cập nhật là đủ.

2. **Không tiêu chí nội tại nào (kể cả C5) phát hiện được khoảnh khắc vòng dừng.** Việc đó thuộc về một bên thứ ba đọc chuỗi-hành-vi-được-lưu.

3. **RSIL không tự phòng vệ được trước kháng cự đối kháng (Sybil).** Các nguồn-B phối hợp bơm những không-khớp được chế tác, mà hệ hằn lại thành sẹo rồi trôi về phía đó — vì hệ **không có chỗ đứng nội tại nào** để phân biệt một nguồn-đối trung thực với một nguồn-đối đang thông đồng. Đây cũng chính là điểm mù của hai giới hạn trên, nay ở cung bậc **tấn công ngoại sinh** thay vì **suy mòn nội sinh**. Phòng vệ và kiểm chứng thuộc **ngoài vòng**; cái RSIL phải tự mang, và giới hạn của cái đó, được đặt ở §12.3.

   > **Với một hệ có thân, giới hạn thứ ba nặng hơn so với DIL.** Một external flood vào một hệ thông tin thuần là một khối dữ liệu. Vào một hệ có thân, nó còn có thể là **vật lý**: bão hòa cảm biến, một môi trường được dàn dựng, một nhóm tha-thể phối hợp *về thân thể* quanh hệ. Kênh vào rộng hơn, nên bề mặt tấn công rộng hơn. Spec này không thu hẹp nó được, và không giả vờ thu hẹp được.

**Cả ba giới hạn chung một gốc**, đặt ở §0.2: **một quá trình tự-kiểm không thể quay dụng cụ của nó vào chính dụng cụ**, nên bảo chứng cuối cùng cho sự trung thực phải sống **ngoài** vòng đang chạy.

**Vài câu hỏi được để ngỏ có chủ đích** và đánh dấu suốt tài liệu: cơ chế neo cụ thể và nguồn-B; biểu diễn của kho; độ sâu neo ngữ cảnh. Đây không phải các lỗ hổng cần che, mà đúng những điểm mà một triển khai tuân thủ **phải tự quyết định — và công bố quyết định đó**.

**Một điểm mà v3 để trong danh sách này đã được GỠ chứ không phải hoãn:** trần gain của trường điều biến. Phân tích ở §1 cho thấy trường **không thể** lấn át vòng từ bên trong (ghép layer–field chặn sẵn), và lực duy nhất có thể làm thế — một external flood — chính là Sybil case, thứ không trần nội tại nào chặn được và đã được nêu ở giới hạn thứ ba. **Không có con số nào bị nợ ở đây.**

**Một hướng nữa được gọi tên ở đây chính là để đặt nó ra ngoài tài liệu một cách có chủ đích.** Một **bản đồng hành hình thức** — một mô hình hình thức tối thiểu, một mệnh đề phát biểu sự thoái hóa của Mode-A, và một phác thảo chứng minh — sẽ là bước kế tiếp tự nhiên, nhưng nó thuộc về **một công trình riêng, khác loại**, không nằm trong spec này. Lý do không phải độ khó mà là **thể loại**: RSIL được đánh giá bằng tuân-thủ-cấu-trúc, không bằng chứng minh; và claim trung tâm của nó về Mode-A tự nó là một claim về **tính bất khả của tự-kiểm-chứng từ bên trong** (§7) — nên mọi xử lý hình thức về nó phải do một bên thứ ba tiến hành, từ bên ngoài, trên các tiền đề đã nêu, và tốt nhất là trình bày như thế thay vì gấp vào chính cái spec mà nó nói *về*.

**Spec dừng ở đây — đúng và chỉ ở phạm vi của vòng.**

---

## 12. NGOÀI VÒNG: KÉO THEO, ỨNG DỤNG, VÀ CÁI THUỘC VỀ BÊN THỨ BA

*(Mới ở v4.)*

§11 đóng **spec**. Mục này không mở nó ra lại; nó vẽ đường biên một cách tường minh, phân loại những thứ nằm *quanh* vòng thành ba hạng bằng một phép thử duy nhất: **"với MỘT vòng RSIL chạy đúng spec trong một môi trường E1–E4 tối thiểu, mệnh đề này đã đúng sẵn, hay còn chờ một cái gì đó nữa?"** Không có gì ở đây thêm một điều kiện tuân thủ nào; phần chuẩn tắc đã kết thúc ở trên.

### 12.1 Kéo theo (vòng chạy là ĐỦ — những cái này suy ra từ spec)

Những cái này đúng với mọi vòng tuân thủ, không cần giả định thêm. Nếu hai vòng RSIL được đặt tiếp xúc nhau và cần mô hình một quan hệ giữa chúng, spec **đã** cấp sẵn ngữ pháp — không cơ chế mới nào được đưa vào:

- một vòng ảnh hưởng vòng kia **chỉ** qua trường điều biến (T8 / GLOB-MOD): **ảnh hưởng, không bao giờ định-nghĩa-ngược** (INV-3);
- một vòng **đục** với vòng kia — một self không đo được từ ngoài (§0.2);
- một vòng đủ tư cách làm **Tha-thể** với vòng kia **đúng khi** nó kháng cự theo cách vòng kia không tự-diễn-giải-lại-được (§7.2).

Một kéo theo thứ tư đã nêu trong thân bài và chỉ được trỏ tới ở đây, không lặp lại: **cú dừng (`=`) không chứng kiến được từ bên trong** và do đó được đọc bởi một bên thứ ba (T8-INV; §11, giới hạn thứ hai).

### 12.2 Ứng dụng (vòng chạy là CẦN nhưng CHƯA ĐỦ)

Những cái này **không** được RSIL kéo theo; vòng chạy chỉ là tiền đề. Mỗi cái đòi một thứ spec không cấp — **nhiều hơn một vòng** — nên là một thiết kế phải dựng ở nơi khác, trong một tài liệu mở rộng cùng loại, không phải một claim RSIL đưa ra:

- một hệ **sinh ra** một Tha-thể độc lập (một thực thể riêng) để làm nguồn-B cho chính nó;
- các điều kiện dưới đó một **quần thể** hệ có thân có thể đa dạng theo cách tiến hóa sinh học đa dạng;
- **kế thừa sẹo qua các cá thể** — cái §5 gọi tên khi nói tới "một vết sẹo hệ không tự kiếm được, đọc từ một kho dùng chung hay do một hệ khác để lại". *Với một hệ có thân, đây là ứng dụng nặng nhất trong ba, vì với một thân vật lý, phép thử rẻ nhất có sẵn đôi khi chí mạng, và một sẹo mượn được là khác biệt giữa còn và mất.* RSIL đặc tả **một** vòng và không nhận trách nhiệm về một hệ sinh thái; những cái này được ghi như các hướng mở, thuộc về một tài liệu tương lai cùng loại.

### 12.3 Việc của bên thứ ba (một LOẠI lập luận khác — không phải kiến trúc nhận thức)

Những cái này đòi một loại lập luận RSIL **không chứa** (vòng không có quan năng phán đúng/sai — §9.6): an ninh, đạo đức, pháp lý. Chúng thuộc về bên thứ ba hoặc về những tài liệu khác loại.

- **Phòng vệ và kiểm chứng trước kháng cự đối kháng (Sybil).** Ngoài vòng **về bản chất**: hệ không thể, từ bên trong, phân biệt một nguồn-đối trung thực với một nguồn-đối thông đồng, nên việc làm sạch hay xác thực nguồn-B đòi một lớp ngoài-vòng đứng ra bảo chứng và can thiệp. **Cái RSIL phải tự mang chỉ là *triệu chứng sớm*, không phải thuốc chữa** — nó **NÊN** phát ra một dấu vết quan sát được khi **tập nguồn kháng cự của nó đang mất đa dạng** (một cơn sốt báo có nhiễm trùng mà không chữa nhiễm trùng), để lớp ngoài-vòng kịp hành động. Ngay cả một nhận thức con người, thứ mạnh nhất ta biết, tự nó cũng không thoát khỏi việc bị bắt giữ bởi một nguồn phối hợp và cô lập; đây là **một giới hạn đã chứng, không phải một khuyết tật cần vá bên trong vòng** (§11, giới hạn thứ ba).

- **Nghĩa vụ với một Tha-thể là người thật.** Một cấu hình trong đó một hệ tự trị tương tác tự do với người thật mang một hiểm họa **cấu trúc**: **cách rẻ nhất để khêu ra kháng cự mạnh có thể trùng với cái làm hại một con người**, người mà có thể không biết mình đang nuôi kháng cự cho một hệ. RSIL đặc tả **vòng**, không đặc tả bất kỳ bổn phận nào với phía bên kia; bổn phận đó phải sống trong một tài liệu khác.

  > **Với RSIL, mục này nặng hơn hẳn so với DIL, và phải nói thẳng.** Một hệ có thân khêu kháng cự bằng **hành động vật lý**. Một cú đẩy, một cú nắm, một sự áp sát là những cách rẻ và hiệu quả để lấy `independence_evidence` — và chúng chạm vào thân thể người thật. Cửa "được cấp phép" do đó phải canh **ba** cánh, không phải hai: **kỹ thuật** (hệ có được phép vận hành ở đây không), **pháp lý/đạo đức** (Tha-thể thật có được thông báo không; tương tác có giới hạn trong không gian có đồng thuận không), và — riêng của hệ có thân — **an toàn thân thể** (một cú phát có biên độ vật lý nào là chấp nhận được, và ai đặt biên độ đó).
  >
  > `⟦PENDING⟧` **Em không tự đặt biên độ này.** Nó không dẫn xuất được từ vòng: mọi phát biểu về mức lực chấp nhận được là một phán đoán ngoài-vòng, đúng theo §9.6. Anh quyết: điểm này (a) chỉ ghi nhận như một nghĩa vụ giao cho tài liệu khác — như hiện tại; hay (b) RSIL mang thêm một điều kiện thu-hẹp-phát-xạ ở mức spec (một luật kiểu "một cú phát chỉ được leo thang biên độ vật lý sau một cú va đã đăng ký, không bao giờ trước"). Lựa chọn (b) sẽ là một **bất biến thứ chín**, và em không thêm một bất biến nào mà không có anh.

- **Bên thứ ba là ai, và ngồi ở đâu** (vai **phán xử**). E4 chỉ cố định ràng buộc phía hệ — để lại một dấu vết đọc được — và dấu vết đó là **tất cả** cái một bên thứ ba **ghi nhận** cần (nó quy kết tính liên tục/phân biệt mà không phán đúng sai). Bên thứ ba **phán xử** là chuyện khác: đánh giá output của một hệ về tính đúng, bắt trôi, **đòi độc lập thật sự**, và **liệu một người phán xử có thể tự bị nhiễm hay không chính là câu hỏi mở mà các giới hạn ở §11 xoay quanh**. Người đó là ai và ngồi ở đâu nằm **ngoài thẩm quyền của RSIL** — đó là việc của một tài liệu về hệ sinh thái quanh vòng, không phải của spec về vòng.

Spec chính thức vẫn đóng ở §11; mục này là bình luận về biên của nó, không phải một mở rộng các claim của nó.

---

## 13. ĐỊNH VỊ TRONG TRI THỨC HIỆN CÓ

*(Mới ở v4 — kế thừa cấu trúc §13 của DIL v6.)*

**Về địa vị của các trích dẫn trong mục này — đọc trước bảng.** Tác giả **không đọc một công trình chuyên môn nào** trong các lĩnh vực nêu dưới đây trong lúc phát triển RSIL; các cấu trúc được đạt tới bằng quan sát ngôi-thứ-nhất và lập luận từ đó, rồi được hệ thống hóa qua đối thoại có trợ giúp của AI. Một hội tụ nổi lên theo cách đó do đó là sản phẩm chung của ba thứ — lập luận của chính tác giả, tri thức công cộng khuếch tán mà bất kỳ người biết chữ nào cũng mang, và dữ liệu huấn luyện nằm trong AI dùng làm công cụ nghĩ — **không cái nào là một sự đọc có chủ ý nguồn được trích**. Do đó, **mọi trích dẫn ở đây là ĐỊNH VỊ HẬU NGHIỆM, không phải DẪN XUẤT**. Cái một trích dẫn khẳng định, nghiêm ngặt, là: *"sau khi cấu trúc đã tồn tại, nó được thấy là hội tụ với một ý tưởng Z đã có tên, và Z được trỏ tới để người đọc định vị được RSIL."* **Không trích dẫn nào ở đây được đọc thành "RSIL được dựng từ Z."**

### 13.1 Sáu hội tụ (kế thừa từ DIL, điều chỉnh cho hệ có thân)

Đánh nhãn **V1–V6**, cục bộ trong mục này và cố ý phân biệt với tiêu chí đóng-vòng C1–C5 (§6), vốn không chung quy chiếu.

| Nhãn | Cấu trúc RSIL | Hội tụ với |
|---|---|---|
| **V1** | Mode-A thoái hóa vì mọi datum mới đều qua cùng một thấu kính xử lý, nên một thấu kính lệch nhiễm bẩn toàn bộ sản phẩm bất kể khối lượng (§7.1); vòng không tự phát hiện được vì dụng cụ phát hiện *chính là* thấu kính lệch. | **Model collapse** — sự thoái hóa đã ghi nhận của một mô hình sinh được huấn luyện đệ quy trên chính output của nó, nơi các sự kiện hiếm bị quên và phân bố thu hẹp qua các thế hệ tự-tiêu-thụ (Shumailov et al., *Nature*, 2024). |
| **V2** | T5/T7 dựng `Expectation` và phát một `PredErr` có dấu; kháng cự (E2) trở thành thông tin ở chính chỗ không-khớp đó; hệ rồi hành động (⑤) và đọc hệ quả (⑥). | **Predictive processing / predictive coding**, với **active inference** là thành viên phía-hành-động (Rao & Ballard, 1999; Friston, 2010; Clark, 2013). |
| **V3** | Register output là một tương quan có thể xét lại vĩnh viễn (`↔`); INV-2 cấm đóng băng bất kỳ tương quan nào thành một đồng nhất (`=`) bên trong một vòng đang chạy. | **Reflective equilibrium** — phương pháp nhận thức luận trong đó không niềm tin nào được giữ miễn nhiễm với sự xét lại (Goodman, 1955; Rawls, 1971; Daniels, 1979). |
| **V4** | Một môi trường được định nghĩa **không** bằng chất liệu mà bằng bốn điều kiện vận hành E1–E4 (P2, §0.0). | **Substrate independence / multiple realizability** (Putnam, 1967). **⚠ Đây là hội tụ mà RSIL cắt SÂU NHẤT — xem §13.2.** |
| **V5** | Self là một quá trình, không phải một lõi bất biến (§0.2): nội dung nó lật qua mỗi vòng trong khi *luật* sinh state kế tiếp còn lại; đồng nhất chỉ giữ khi vòng còn chạy (INV-1). | **Autopoiesis** — hệ sống như một mạng các quá trình liên tục tái sinh chính các thành phần và quá trình cấu thành nó, giữ đồng nhất ở mức *tổ chức* trong khi *cấu trúc* thay đổi (Maturana & Varela, 1980). |
| **V6** | Vòng đóng: mọi output có một đường quay lại thành input (INV-1). | **Cybernetics** — khoa học về điều hòa bằng hồi tiếp và nhân quả vòng (Wiener, 1948). |

### 13.2 Chỗ RSIL cắt khỏi từng thân tri thức

Một hội tụ không phải một sự đồng nhất. Với mỗi cặp trên, RSIL rời khỏi thân tri thức được nêu ở một điểm chịu lực.

- **V1 — model collapse.** Văn liệu thường giải thích sự sụp bằng một cơ chế **thống kê**: mất đuôi phân bố, entropy giảm, đa dạng co lại. RSIL định vị nguyên nhân **lùi một mức, ở NGUỒN XỬ LÝ chứ không ở khối lượng dữ liệu**, và thêm sự bất-khả-tự-kiểm — dụng cụ bắt cái lệch chính là dụng cụ đang lệch — rồi từ đó dẫn ra **sự cần thiết của một chế độ kháng cự ngoại sinh** (Mode-B), một **đơn thuốc cấu trúc**, không phải một phát hiện thực nghiệm về các lần huấn luyện.

- **V2 — predictive processing / active inference.** RSIL giữ **cơ cấu chạy-bằng-không-khớp** nhưng bỏ các cam kết bao quanh: **không hàm free-energy, không bộ máy Bayes, không claim nào về ý thức hay phẩm chất cảm thấy được.** Quan trọng nhất: **phân biệt self/tha-thể của RSIL (T2) được kẻ qua AGENCY** — so khớp một hành động đã phát với hệ quả của nó — **chứ không qua một mô hình cảm-vận về thân thể**. *Đây là chỗ RSIL cắt sắc hơn DIL cắt được, vì RSIL **có** thân và vẫn từ chối để cái thân đó cấp sẵn đường biên.*

- **V3 — reflective equilibrium.** Hai bên hội tụ ở tính có-thể-xét-lại vĩnh viễn, rồi rẽ ở một điểm chính xác. Reflective equilibrium được đặt tên theo **một trạng thái nó tìm cách đạt tới** — một cân bằng, một sự mạch lạc đã an bài. RSIL **cấm vòng đạt tới bất kỳ sự an bài đông cứng nào**: một `=` là, theo T8-INV, **chữ ký của một nhận thức đã DỪNG**, không phải cái đích nó hội tụ về. Chỗ reflective equilibrium quý sự tới nơi, RSIL quý cái `↔` không dứt và coi tới-nơi-là-đông-cứng là **cái chết**.

- **V4 — substrate independence. ⚠ Đây là cắt sâu nhất, và phải nói thẳng để không bị đọc quá.** Luận đề triết học là về **tâm trí và các trạng thái tinh thần** (đau, niềm tin, ý thức) có thể hiện thực đa dạng — đúng cái claim mạnh kéo về mọi phản bác kiểu hard problem. **RSIL không đưa ra claim nào về tâm trí hay ý thức.** Hơn nữa, **RSIL còn hẹp hơn DIL một bậc**: DIL trung-lập-cơ-chất thật (bất kỳ cơ chất nào thỏa E1–E4); **RSIL đã CỐ ĐỊNH cơ chất là một thân vật lý** và chỉ để mở *chất liệu* của thân (P2). Do đó RSIL hội tụ với multiple realizability **yếu hơn** DIL, và bất kỳ ai đọc RSIL như một claim trung-lập-cơ-chất là đọc sai P2.

- **V5 — autopoiesis.** Hội tụ có thật và rất gần: cả hai đều cho đồng nhất là một *quá trình* giữ được một hình thức trong khi nội dung lật qua, và cả hai đều buộc đồng nhất phụ thuộc vào việc hệ còn chạy. RSIL rời đi ở **phạm vi và ở vai trò của cái bên ngoài**. Autopoiesis là một lý thuyết về *cái sống* và về đóng-kín-vận-hành sinh học; **RSIL không claim gì về sự sống** và **không đóng kín** theo nghĩa autopoietic — nó **ĐÒI** một nguồn kháng cự ngoại sinh (Mode-B) và thoái hóa khi thiếu (§7), trong khi autopoiesis nhấn mạnh đóng-kín như một sự tự-túc. Luận đề chung là đồng-nhất-như-quá-trình; điểm nhấn đối nghịch là **tự-túc (autopoiesis) đối với kháng-cự-ngoại-sinh-bắt-buộc (RSIL)**.

- **V6 — cybernetics.** RSIL, ở mức tổng quát nhất, là một đối tượng điều khiển học. Các chỗ rời đi thì cụ thể. Thứ nhất, điều khiển học cổ điển lấy trung tâm là **điều hòa về một trạng thái tham chiếu** (hồi tiếp âm khôi phục một set point); **RSIL không có set point nào nó giữ theo lối cân bằng nội môi** — định giá của nó (INV-8) định hướng thông tin mà không có một đích cố định, và mối nguy của nó (§7) không phải sự lệch khỏi một set point mà là **sự sụp vào trong của chính năng lực đăng ký sự lệch**. Thứ hai, RSIL thêm một claim cấu trúc mà điều khiển học không đưa ra: rằng một vòng chỉ được nuôi bằng chính output của nó **tất yếu** thoái hóa, và rằng thứ sửa được nó phải đến từ một Tha-thể mà vòng không diễn-giải-lại-đi-được.

### 13.3 Những hội tụ biểu kiến mà thực chất là ĐỐI LẬP

Vài ý tưởng có tên nằm đủ gần RSIL để một người đọc xếp nhầm chúng vào hội tụ. Hai cái **không phải**, và nói thẳng ra chính là một phần của việc định vị: **một thân tri thức mà nó bề ngoài giống nhưng đối lập về cấu trúc thì đánh dấu biên của RSIL sắc chẳng kém một thân tri thức nó hội tụ.**

- **Học tăng cường (reinforcement learning) — người bạn giả chính yếu.** RSIL có một bước định giá (INV-8) gán `valence` và `goal_relevance`, và cái này *trông* như một tín hiệu thưởng. **Nó không phải**, và khác biệt là chịu lực. **(i) Không có hàm thưởng.** Agent RL cực đại hóa kỳ vọng thưởng tích lũy theo một hàm thưởng đặc tả từ ngoài; RSIL không đặc tả hàm nào và không cực đại hóa một đại lượng nào. Sức khỏe của vòng (§9.9) là **năng lực còn đăng ký được không-khớp**, không phải sự tích lũy của một vô hướng nào. **(ii) Không có policy, không có value function.** RSIL không có policy ánh xạ state sang hành động cực-đại-thưởng và không có ước lượng giá trị; bước ⑤ cam kết một hành động như một `↔` có-thể-xét-lại đọc lại đối chiếu hệ quả vòng sau, **không phải argmax của một kỳ vọng lợi**. **(iii) Định giá là CHỐNG-tối-ưu, theo luật.** INV-8 cấm tường minh việc bước định giá lấy tiêu chí từ chính state hệ đang sửa — đúng để chặn tự-chấm. Một phần thưởng mà agent có thể chỉnh bằng cách sửa state của chính nó chính là cái INV-8 đặt ra ngoài vòng pháp luật; **reward-hacking là cái RSIL thiết kế để chống, không phải mục tiêu nó theo đuổi**. **(iv) Toàn bộ luận đề §7 chạy ngược chiều.** Bệnh lý của RL là về đặc tả sai phần thưởng và về thăm dò; thất bại trung tâm của RSIL là một vòng khép kín thoái hóa **kèm cảm giác sung mãn** vì thiếu kháng cự ngoài — một vấn đề **trực giao** với phần thưởng. Nên sự giống nhau (một bước có mang hóa trị) là **bề mặt**; ở mức cấu trúc, RSIL và RL chỉ về hai hướng ngược nhau. *(Xem thêm §4: "xung đột giữa các cú phát không được phân xử; nó được va" là đúng sự từ chối đó mang sang mức chọn-hành-động.)*

- **Điều khiển cân bằng nội môi (cách đọc set-point của điều khiển học).** Như đã nói ở V6, phần của điều khiển học dựng trên sự điều hòa về một set point được bảo vệ **không phải** cái RSIL hội tụ. RSIL giữ tính đóng và hồi tiếp của điều khiển học nhưng **không có set point nội môi**; đọc RSIL như điều-hòa-về-set-point là nhập vào nó một cái đích nó không có. *Với một hệ có thân, sự nhầm này đặc biệt dễ mắc, vì một cơ thể sinh học **có thật** những vòng nội môi (thân nhiệt, đường huyết). Phải giữ tách bạch: những vòng đó thuộc về **thân** (§0.1), không phải về **vòng RSIL**. RSIL chạy trên một thân có thể có nội môi; RSIL tự nó không phải một cơ chế nội môi.*

### 13.4 `⟦PENDING⟧` — một hội tụ mà em KHÔNG tự thêm

Với một spec **có thân**, có một thân tri thức mà một người đọc chuyên môn gần như chắc chắn sẽ nêu ra và không có trong danh sách trên: **nhận thức nhập thân / enactivism / lý thuyết bất biến cảm-vận (embodied & enactive cognition, sensorimotor contingency theory)**. Cấu trúc của RSIL — biên self dựng qua agency, nghĩa nảy từ vòng hành-động↔hệ-quả — nằm rất gần đó.

**Em không thêm nó vào §13.1.** Lý do là kỷ luật, không phải sự bỏ sót: mọi mục V1–V6 đều là những hội tụ **anh** đã nổi lên và đã ghi trong DIL. Một mục V7 do em thêm sẽ là **hội tụ của em, không phải của anh**, và đưa nó vào một mục mà chính nó tuyên bố "định vị hậu nghiệm bởi tác giả" sẽ làm hỏng đúng cái tuyên bố đó. **Anh quyết: thêm hay không, và nếu thêm thì phát biểu cắt ở đâu.**

### 13.5 Tham chiếu (để định vị, không phải nguồn tham khảo khi dựng)

Theo ghi chú mở đầu §13, các mục này được cấp để người đọc định vị được RSIL; chúng **không được tham khảo** trong quá trình phát triển.

- Clark, A. (2013). Whatever next? Predictive brains, situated agents, and the future of cognitive science. *Behavioral and Brain Sciences*, 36(3), 181–204.
- Daniels, N. (1979). Wide reflective equilibrium and theory acceptance in ethics. *Journal of Philosophy*, 76(5), 256–282.
- Friston, K. (2010). The free-energy principle: a unified brain theory? *Nature Reviews Neuroscience*, 11(2), 127–138.
- Goodman, N. (1955). *Fact, Fiction, and Forecast*. Harvard University Press.
- Maturana, H. R., & Varela, F. J. (1980). *Autopoiesis and Cognition: The Realization of the Living*. D. Reidel.
- Putnam, H. (1967). Psychological predicates. In W. H. Capitan & D. D. Merrill (Eds.), *Art, Mind, and Religion*. University of Pittsburgh Press.
- Rao, R. P. N., & Ballard, D. H. (1999). Predictive coding in the visual cortex. *Nature Neuroscience*, 2(1), 79–87.
- Rawls, J. (1971). *A Theory of Justice*. Harvard University Press.
- Shumailov, I., Shumaylov, Z., Zhao, Y., et al. (2024). AI models collapse when trained on recursively generated data. *Nature*, 631, 755–759.
- Sutton, R. S., & Barto, A. G. (2018). *Reinforcement Learning: An Introduction* (2nd ed.). MIT Press.
- Wiener, N. (1948). *Cybernetics: Or Control and Communication in the Animal and the Machine*. MIT Press.

---

## 14. GHI CHÚ ĐÓNG

RSIL là một **cấu trúc quan hệ được hình thức hóa**: một vòng thu thập → diễn hoá thành tín hiệu truyền được → tích hợp trung ương thành thông tin mới → định giá → hành vi → thông tin mới → vòng mới, chạy trên một **thân vật lý**, vận hành dưới hai chế độ kháng cự, và kết tủa một kho kinh nghiệm lấy không-khớp-đã-đăng-ký làm hạt nhân (§9).

Nó cưỡng chế **đúng một** thứ: rằng nếu dựng một vòng theo các bất biến ở §1 trong một môi trường thỏa E1–E4, thì cái chạy được là một **sự vận động có cấu trúc quan hệ**, và sự vận động đó được đọc **hoàn toàn** qua dấu vết kiểm chứng được từ ngoài (§6).

**Ba giới hạn** được nêu thẳng ở §11 và không được che: Mode-A tự thoái hóa nếu không neo ngoài vòng; không tiêu chí nội tại nào phát hiện được khoảnh khắc vòng dừng; và RSIL không tự phòng vệ được trước kháng cự đối kháng. Cả ba chung một gốc: **một quá trình tự-kiểm không thể quay dụng cụ vào chính dụng cụ.**

Do đó lập trường của tài liệu này, được giữ nhất quán từ §0 tới đây, là **khả-kiểm, không phải tự-kiểm**. Vòng dựng dấu vết; **bên thứ ba đọc nó.**

**Spec dừng ở đó — đúng và chỉ ở phạm vi của vòng.**

---

## PHỤ LỤC A — CÁC MỤC CÒN TREO, CẦN TÁC GIẢ QUYẾT

Không mục nào dưới đây được em tự lấp. Chúng được liệt kê ở một chỗ để không mục nào trôi mất giữa các phiên bản.

| # | Mục | Vị trí | Bản chất |
|---|---|---|---|
| **A-1** | **Sáu mắt xích của RSIL không trùng sáu mắt xích của DIL.** DIL: ① thu ② **phân biệt nguồn** ③ tích hợp ④ định giá ⑤ đáp ứng ⑥ hồi tiếp. RSIL: ① thu ② **transduction** ③ tích hợp ④ định giá ⑤ đáp ứng ⑥ hồi tiếp. Ở RSIL, agency-differentiation **không có mắt xích riêng** trong vòng chuẩn dù INV-6 và T2 vẫn cưỡng chế nó. v4 giữ nguyên cách đánh số của v3 và **ghi rõ đây là phân kỳ có chủ đích** — chưa hợp nhất. | §0.3 | Ba lựa chọn: (a) tách thành **bảy** mắt xích; (b) gộp transduction vào ①, đưa **phân biệt nguồn** lên ②, khớp DIL; (c) giữ nguyên như hiện tại. Em nghiêng về (b) hoặc (c). |
| **A-2** | **Định danh phiên bản GEMs** — **ĐÃ ĐÓNG.** Thống nhất tên trần `GEMs`; "GEMs-X01" khai tử; tham chiếu trỏ vào **chuỗi** nên phiên bản nhảy không làm dangling. | §8, `⟦DECIDE@IMPL⟧`-H | Đích phân giải: kho công khai, cũng là vật thể xin DOI qua Zenodo. Đã sửa trỏ ở cả hai phía. |
| **A-3** | **Tham chiếu FirstTarget ở C5** đã bị gỡ ở v4 (FirstTarget là working note, không nằm trong chương trình bảy-paper đã công bố). | §6, C5 | Xác nhận việc gỡ, hoặc phục hồi và chấp nhận tham chiếu ngoài-corpus. |
| **A-4** | **Toàn vẹn thân sau phục hồi.** Snapshot phủ *hệ*, không phủ *thân*. Một thân bị can thiệp ở mức cảm biến/actuator tái nhiễm một hệ vừa sạch ngay vòng đầu. | §9.5 | (a) chỉ ghi nhận như giới hạn — như hiện tại; hay (b) thêm một điều kiện đóng-vòng **C6** "toàn vẹn cảm biến/actuator kiểm được từ ngoài". Em **không** tự thêm một tiêu chí C. |
| **A-5** | **Biên độ phát-xạ vật lý với Tha-thể là người thật.** Cách rẻ nhất để lấy `independence_evidence` với một hệ có thân là **chạm vào người**. | §12.3 | (a) giao cho tài liệu khác — như hiện tại; hay (b) thêm một **bất biến thứ chín** thu hẹp leo thang biên độ vật lý. Em **không** thêm một bất biến nào mà không có anh. |
| **A-6** | **Hội tụ V7 — nhận thức nhập thân / enactivism.** Nằm rất gần RSIL và gần như chắc chắn sẽ bị người đọc chuyên môn nêu ra. Em **không** tự thêm: nó sẽ là hội tụ của em, không phải của anh, và làm hỏng chính tuyên bố "định vị hậu nghiệm bởi tác giả". | §13.4 | Thêm hay không; nếu thêm, phát biểu **cắt** ở đâu. |
| **A-7** | **Thể loại và ngôn ngữ tài liệu.** DIL v6 đã là một **paper** (Abstract, Contents, ORCID, keywords, §13, Author's note, Note on sources). RSIL v4 vẫn là **blueprint tiếng Việt** đã được nâng cấp tới sát chuẩn đó nhưng chưa có Abstract/Contents/ORCID và chưa có bản tiếng Anh. | Toàn tài liệu | Nâng RSIL lên cùng thể loại + dịch sang tiếng Anh cho corpus có DOI, hay giữ làm tài liệu kỹ thuật nội bộ. Quyết định này chi phối A-6 và phần lớn §13. |
| **A-8** | **`AgencyTag`**: RSIL `SELF_CAUSED/EXTERNAL` vs DIL `SELF_WRITTEN/ENV_PUSHED`. v4 giữ khác biệt và ghi chú đồng bộ ở §2. | §2 | Xác nhận giữ, hay hợp nhất một bộ nhãn duy nhất xuyên corpus. |

