# Báo Cáo Nhóm — Lab 7: Embedding & Vector Store

**Nhóm:** NguyenTheAnh  
**Thành viên:** Trần Quốc Hùng, Nguyễn Đức Sơn, Nguyễn Thế Anh  
**Ngày:** 03/08/2026

> Nhóm sử dụng chung corpus RMIT trong `data/k3_tuition/` và cùng 5 benchmark queries trong `data/k3_tuition/benchmark_queries.csv`. Mỗi thành viên thử một strategy riêng. Kết quả của Nguyễn Thế Anh trong báo cáo cá nhân được thực hiện trên corpus/query HUST cũ, vì vậy chưa được dùng để chấm so sánh RMIT và cần chạy lại trước khi nộp bản cuối.

**Tổng điểm phần nhóm: 40** = Lựa chọn tài liệu (10) + Thiết kế chiến lược (15) + Chất lượng truy xuất (10) + Thuyết trình (5).

---

## 1. Lựa chọn tài liệu (Document Set Quality) — Nhóm (10 điểm)

### Phạm vi bộ tài liệu (Scope)

Nhóm tập trung vào các quy định học phí dành cho sinh viên RMIT Việt Nam, gồm cách tính học phí, mức phí tham khảo, phương thức và thời hạn thanh toán, hoàn trả học phí, chính sách chiết khấu và học bổng hỗ trợ học phí.

### Danh sách tài liệu (Data Inventory)

Corpus gồm 7 tài liệu công khai từ website chính thức của RMIT Việt Nam.

| # | Tên tài liệu | Nguồn | Ngày lấy / Phiên bản | Số ký tự | Metadata |
|---:|---|---|---|---:|---|
| 1 | Học phí RMIT Việt Nam năm 2026 | [RMIT tuition](https://www.rmit.edu.vn/vi/hoc-tap-tai-rmit/hoc-phi) | 03/08/2026; năm 2026 | 1.926 | student, tuition_schedule, vi |
| 2 | Hướng dẫn học phí và phí phụ thu 2026 | [RMIT fees guide](https://www.rmit.edu.vn/assets/vn/en/assets-for-production/documents/pdfs/study-at-rmit/tuition-fees/student-fees-and-charges-guide-06-2026.pdf) | 03/08/2026; cập nhật 17/06/2026 | 2.494 | student, tuition_policy, vi |
| 3 | Phương thức thanh toán học phí | [RMIT payment methods](https://www.rmit.edu.vn/vi/hoc-tap-tai-rmit/hoc-phi/phuong-thuc-thanh-toan-hoc-phi) | 03/08/2026; ngày ban hành không xác định | 1.722 | student, payment_instructions, vi |
| 4 | Academic Calendar 2026 – Vietnam Campus | [RMIT academic calendar](https://www.rmit.edu.vn/assets/vn/en/assets-for-production/documents/pdfs/academic-calendar/academic-calendar-2026-jun26.pdf) | 03/08/2026; approved 29/06/2026 | 1.316 | student, payment_deadlines, vi |
| 5 | Chính sách học phí đặc biệt | [RMIT tuition assistance](https://www.rmit.edu.vn/vi/hoc-tap-tai-rmit/hoc-phi/chinh-sach-hoc-phi-dac-biet) | 03/08/2026; áp dụng kỳ 2026/2027 | 1.729 | student, tuition_discount, vi |
| 6 | Học bổng thành tích cho sinh viên hiện đang học | [RMIT current-student scholarship](https://www.rmit.edu.vn/vi/hoc-tap-tai-rmit/hoc-bong/hoc-bong-thanh-tich-hoc-tap-xuat-sac-cho-sinh-vien-hien-dang-hoc-tai-rmit) | 03/08/2026; chương trình 2026 | 1.150 | student, scholarship, vi |
| 7 | Học bổng toàn phần RMIT Việt Nam | [RMIT full scholarship](https://www.rmit.edu.vn/vi/hoc-tap-tai-rmit/hoc-bong/hoc-bong-dai-hoc-cho-sinh-vien-tuong-lai/hoc-bong-hieu-truong) | 03/08/2026; đợt 2026 | 991 | student, scholarship, vi |

**Quản trị dữ liệu:**

- [x] Có 7 tài liệu, nằm trong yêu cầu 5–10 tài liệu.
- [x] Tất cả là nguồn công khai trên tên miền chính thức của RMIT Việt Nam.
- [x] Không đưa thông tin cá nhân, tài khoản đăng nhập hoặc tài liệu nội bộ vào corpus.
- [x] Mỗi tài liệu có `source_url`, `retrieved_at` và `document_version` trong front matter.
- [x] `sources.csv` khớp với 7 tài liệu.
- [ ] Nhóm cần kiểm tra lần cuối việc sử dụng nội dung theo điều khoản bản quyền của từng nguồn; hiện corpus ghi rõ chưa xác định giấy phép tái sử dụng riêng.

### Cấu trúc Metadata (Metadata Schema)

| Trường | Kiểu | Ví dụ | Tác dụng |
|---|---|---|---|
| `doc_id` | string | `rmit_fees_guide_2026` | Định danh ổn định và xóa theo tài liệu |
| `audience` | string | `student` | Lọc đúng đối tượng; dùng trong benchmark query 1 |
| `department` | string | `RMIT Việt Nam` | Phân biệt đơn vị/phạm vi ban hành |
| `category` | string | `payment_instructions` | Lọc theo loại nội dung học phí |
| `language` | string | `vi` | Hỗ trợ truy xuất theo ngôn ngữ |
| `source_url` | string | URL RMIT | Truy vết nguồn câu trả lời |
| `retrieved_at` | date | `2026-08-03` | Theo dõi thời điểm thu thập |
| `document_version` | string | `2026` | Phân biệt phiên bản/chương trình áp dụng |

---

## 2. Thiết kế chiến lược (Strategy Design) — Nhóm (15 điểm)

### Phân tích đường cơ sở (Baseline Analysis)

Kết quả dưới đây chạy bằng `ChunkingStrategyComparator().compare(..., chunk_size=300)` trên ba tài liệu đại diện.

| Tài liệu | Strategy | Số chunk | Độ dài trung bình | Nhận xét |
|---|---|---:|---:|---|
| Học phí 2026 | Fixed size | 7 | 275.1 | Độ dài ổn định nhưng có thể cắt giữa câu/metadata |
| Học phí 2026 | By sentences | 5 | 383.4 | Giữ câu tốt hơn nhưng một số chunk dài |
| Học phí 2026 | Recursive | 11 | 173.5 | Giữ heading/list tốt nhưng tạo nhiều chunk nhỏ |
| Fees guide 2026 | Fixed size | 9 | 277.1 | Kích thước đều, dễ kiểm soát |
| Fees guide 2026 | By sentences | 6 | 414.0 | Giữ ý tương đối đầy đủ, ít chunk hơn |
| Fees guide 2026 | Recursive | 13 | 190.3 | Tách rõ các mục “Hạn thanh toán” và “Hoàn trả” |
| Payment methods | Fixed size | 6 | 287.0 | Phù hợp độ dài cố định, có nguy cơ cắt danh sách |
| Payment methods | By sentences | 8 | 213.6 | Giữ câu nhưng có thể tách danh sách thành nhiều phần |
| Payment methods | Recursive | 10 | 170.5 | Bảo toàn heading và các nhóm phương thức thanh toán |

### Chiến lược của từng thành viên

**Trần Quốc Hùng**

- **Loại strategy:** `RecursiveChunker(chunk_size=500)`.
- **Lý do:** Tài liệu học phí có nhiều heading, danh sách và mục chính sách; recursive chunking ưu tiên giữ các đoạn và mục có ý nghĩa.
- **Điểm mạnh:** Giữ được cấu trúc section, đặc biệt với mục hoàn trả học phí.
- **Điểm yếu:** Độ dài chunk không đồng đều; mock embedding khiến retrieval chưa ổn định.

**Nguyễn Đức Sơn**

- **Loại strategy:** `FixedSizeChunker(chunk_size=300, overlap=50)`.
- **Lý do:** Kiểm soát được kích thước chunk và overlap giúp giữ ngữ cảnh tại ranh giới.
- **Điểm mạnh:** Kích thước đều, dễ triển khai và đạt kết quả benchmark tốt khi dùng local multilingual embedder.
- **Điểm yếu:** Có thể cắt giữa câu hoặc giữa danh sách gạch đầu dòng.

**Nguyễn Thế Anh**

- **Loại strategy trong báo cáo cá nhân:** `RecursiveChunker(chunk_size=300)`.
- **Lý do:** Giữ cấu trúc heading/đoạn và giảm cắt giữa ý.
- **Trạng thái:** Báo cáo cá nhân hiện chạy trên corpus HUST cũ và các query thư viện/ký túc xá, không phải corpus RMIT chung. Cần chạy lại đúng 5 query RMIT trước khi dùng kết quả để so sánh.

### So sánh giữa các thành viên

| Thành viên | Strategy | Kết quả hiện có | Điểm mạnh | Hạn chế |
|---|---|---:|---|---|
| Trần Quốc Hùng | Recursive 500 | 2/5 top-3 với mock | Giữ cấu trúc section | Mock embedding không phản ánh ngữ nghĩa |
| Nguyễn Đức Sơn | Fixed 300, overlap 50 | 5/5, tự đánh giá 10/10 | Kết quả local multilingual tốt, chunk đều | Có thể cắt giữa câu |
| Nguyễn Thế Anh | Recursive 300 | Chưa thể so sánh | Giữ cấu trúc tài liệu | Đã dùng corpus/query HUST khác; cần rerun |

Kết quả hiện tại gợi ý `FixedSizeChunker(300, overlap=50)` có triển vọng tốt trên corpus này, nhưng chưa thể kết luận chắc chắn vì Hùng dùng mock còn Sơn dùng local multilingual embedding. Để so sánh công bằng, cả ba thành viên cần chạy lại cùng embedding provider và cùng version corpus.

---

## 3. Câu hỏi đánh giá & Chất lượng truy xuất (Retrieval Quality) — Nhóm (10 điểm)

### 5 benchmark queries và gold answers

| # | Query | Gold answer | Tài liệu chứa thông tin |
|---:|---|---|---|
| 1 | Học phí tại RMIT Việt Nam được tính và thanh toán như thế nào? | Học phí thanh toán theo từng học kỳ và dựa trên số môn đăng ký trong học kỳ. | `rmit_tuition_2026`, mục Nguyên tắc tính và thanh toán; filter `audience=student` |
| 2 | Hạn thanh toán học phí Học kỳ 2 năm 2026 là ngày nào? | Ngày 17/07/2026. | `rmit_academic_calendar_2026`, mục Học kỳ 2 |
| 3 | Khi chuyển khoản học phí, nội dung chuyển khoản cần có những thông tin gì? | Họ tên, mã số sinh viên hoặc ngày sinh nếu chưa có mã số, và nội dung khoản thanh toán. | `rmit_payment_methods`, mục Nội dung chuyển khoản |
| 4 | Sinh viên học kỳ thứ hai trở đi phải rút môn trước thời điểm nào để được hoàn toàn bộ học phí? | Trước khi kết thúc ngày làm việc Thứ Sáu của tuần thứ tư trong học kỳ. | `rmit_fees_guide_2026`, mục Hoàn trả học phí |
| 5 | Điều kiện GPA tối thiểu của học bổng thành tích dành cho sinh viên hiện đang học năm 2026 là bao nhiêu? | GPA tích lũy từ 3,4/4,0 trở lên và hoàn tất ít nhất 96 tín chỉ. | `rmit_current_student_scholarship_2026`, mục Điều kiện chính |

### Tổng hợp chất lượng truy xuất hiện có

| # | Strategy tốt nhất hiện có | Chunk liên quan trong top-3? | Ghi chú |
|---:|---|---|---|
| 1 | Fixed 300, overlap 50 | Có | Sơn truy xuất đúng tài liệu; Hùng mock chưa lấy đúng chunk |
| 2 | Fixed 300, overlap 50 | Có | Sơn lấy đúng academic calendar; Hùng mock thất bại |
| 3 | Fixed 300, overlap 50 | Có | Sơn lấy đúng payment methods; Hùng mock lấy đúng tài liệu ở top-1 |
| 4 | Fixed 300, overlap 50 / Recursive | Có | Cả kết quả Sơn và Hùng đều lấy được fees guide |
| 5 | Fixed 300, overlap 50 | Có | Sơn lấy đúng scholarship document; Hùng mock chưa lấy đúng |

Kết quả tổng hợp chính thức cần chốt lại sau khi tất cả thành viên chạy cùng local embedding. Số liệu hiện tại chỉ dùng làm bản nháp vì embedding provider khác nhau.

**Metadata filtering:** Query 1 dùng `metadata_filter={"audience": "student"}`. Filter giúp giới hạn kết quả đúng đối tượng, nhưng vì toàn bộ 7 tài liệu hiện đều có `audience=student`, tác dụng phân biệt chưa lớn. Trong lần cải thiện tiếp theo, nhóm nên gán audience đa dạng hơn hoặc kết hợp thêm `category`, ví dụ `payment_instructions` và `scholarship`.

---

## 4. Thuyết trình (Demo) & Bài học nhóm — Nhóm (5 điểm)

### Insights chính

1. Chunking và embedding ảnh hưởng đồng thời đến retrieval: cùng corpus nhưng mock embedding có thể xếp hạng sai dù chunk chứa đúng thông tin.
2. Fixed-size chunking với overlap cho độ dài ổn định và kết quả tốt trong thử nghiệm của Nguyễn Đức Sơn; recursive chunking giữ heading và section tốt hơn về mặt cấu trúc.
3. Metadata có giá trị truy vết nguồn và lọc đối tượng, nhưng filter `audience=student` chưa tạo khác biệt lớn vì các tài liệu hiện tại đều dành cho sinh viên.

### Failure case

Trong kết quả của Trần Quốc Hùng bằng mock embedding, query về hạn thanh toán Học kỳ 2 không đưa `rmit_academic_calendar_2026` vào top-3, dù tài liệu chứa chính xác ngày 17/07/2026. Nguyên nhân chính là mock embedding không biểu diễn ngữ nghĩa; không nên kết luận recursive chunking thất bại chỉ từ trường hợp này. Cách cải thiện là dùng local multilingual embedding và giữ riêng các mục lịch học kỳ trong chunk.

### Bài học nhóm

Cùng một corpus là điều kiện bắt buộc để so sánh strategy công bằng. Kết quả của Nguyễn Thế Anh trên corpus HUST cũ không thể dùng chung với benchmark RMIT; thành viên đó cần chạy lại đúng corpus và 5 queries RMIT. Nhóm cũng cần cố định embedding provider, chunker parameters và cách chấm trước khi so sánh.

### Nếu làm lại

Nhóm sẽ dùng local multilingual embedding ngay từ đầu, lưu kết quả top-3 của từng query vào một bảng chung và thêm metadata `category` vào filter. Nhóm cũng sẽ tạo chunk theo heading/section cho tài liệu chính sách để giữ trọn các điều kiện, ngoại lệ và thời hạn.

---

## Tự Đánh Giá (Phần Nhóm)

| Tiêu chí | Điểm tự đánh giá |
|---|---:|
| Lựa chọn tài liệu | 10 / 10 |
| Thiết kế chiến lược | 12 / 15 — chờ rerun cùng embedding provider |
| Chất lượng truy xuất | 8 / 10 — cần chốt lại kết quả cùng provider |
| Thuyết trình | 4 / 5 — cần bổ sung demo cuối |
| **Tổng** | **34 / 40 tạm tính** |

