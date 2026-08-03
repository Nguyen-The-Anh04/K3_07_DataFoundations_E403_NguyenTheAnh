# Báo Cáo Cá Nhân — Lab 7: Embedding & Vector Store

**Họ tên:** Nguyễn Đức Sơn  
**Mã sinh viên:** 2A202601485  
**Nhóm:** NguyenTheAnh  
**Ngày:** 03/08/2026

> Dữ liệu và 5 benchmark queries dùng chung được lấy từ `data/k3_tuition` trên nhánh `tranquochung_01683`.

**Tổng điểm phần cá nhân: 60** = Khởi động (5) + Hướng tiếp cận (10) + Hoàn thiện code (30) + Dự đoán độ tương tự (5) + Kết quả truy xuất cá nhân (10).

---

## 1. Khởi động (Warm-up) — Cá nhân (5 điểm)

### Độ tương tự Cosine

Cosine similarity cao nghĩa là hai vector embedding có hướng gần nhau. Trong xử lý văn bản, điều này thường cho thấy hai câu hoặc đoạn văn có nội dung và ngữ cảnh tương tự, ngay cả khi cách diễn đạt không giống hoàn toàn.

**Ví dụ tương đồng cao**

- Câu A: Sinh viên cần thanh toán học phí trước thời hạn.
- Câu B: Người học phải hoàn thành nghĩa vụ học phí trước ngày đến hạn.
- Hai câu cùng nói về hạn thanh toán học phí.

**Ví dụ tương đồng thấp**

- Câu A: Sinh viên cần thanh toán học phí trước thời hạn.
- Câu B: Học bổng yêu cầu ứng viên hoàn tất tối thiểu 96 tín chỉ.
- Hai câu nói về hai vấn đề khác nhau.

Cosine similarity phù hợp với text embeddings vì nó tập trung vào hướng của vector và ít phụ thuộc vào độ lớn tuyệt đối. Euclidean distance có thể bị ảnh hưởng bởi độ lớn vector dù quan hệ ngữ nghĩa tương đối giống nhau.

### Bài toán Chunking

Với tài liệu 10.000 ký tự, `chunk_size=500`, `overlap=50`:

```text
ceil((10.000 - 50) / (500 - 50))
= 23 chunks
```

Nếu tăng overlap lên 100:

```text
ceil((10.000 - 100) / (500 - 100))
= 25 chunks
```

Overlap lớn hơn giúp giữ ngữ cảnh ở ranh giới chunk nhưng làm tăng số chunk, dữ liệu trùng lặp, dung lượng lưu trữ và thời gian embedding.

---

## 2. Hướng tiếp cận của tôi (My Approach) — Cá nhân (10 điểm)

### Các hàm chunking

**`SentenceChunker.chunk`:** Tôi loại bỏ khoảng trắng thừa và dùng regex `(?<=[.!?])\s+` để tách văn bản sau dấu kết thúc câu. Các câu được nhóm theo `max_sentences_per_chunk`; đầu vào rỗng trả về `[]`.

**`RecursiveChunker.chunk` và `_split`:** Thuật toán ưu tiên tách theo đoạn, dòng, câu và từ. Nếu phần hiện tại vẫn dài hơn `chunk_size`, hàm tiếp tục đệ quy với separator kế tiếp. Khi không còn separator, văn bản được cắt cứng theo số ký tự.

### EmbeddingStore

**`add_documents`:** Mỗi `Document` được nhúng và lưu dưới dạng record gồm ID, nội dung, metadata và embedding.

**`search`:** Query được nhúng bằng cùng embedding function; hệ thống tính dot product, sắp xếp giảm dần và trả về `top_k`.

**`search_with_filter`:** Lọc metadata trước khi tính similarity. Benchmark số 1 dùng `audience=student`.

**`delete_document`:** Xóa toàn bộ chunk có cùng `doc_id`.

### KnowledgeBaseAgent

Agent truy xuất top-k chunk, ghép chúng vào `Context`, tạo prompt yêu cầu trả lời dựa trên context và gọi `llm_fn`. Khi context không đủ, agent phải từ chối suy đoán.

### Chiến lược retrieval cá nhân

Tôi sử dụng:

```python
FixedSizeChunker(chunk_size=300, overlap=50)
```

Chiến lược này kiểm soát ổn định độ dài chunk và dùng overlap để giữ một phần ngữ cảnh ở ranh giới. Điểm yếu là có thể cắt giữa câu hoặc giữa một danh sách gạch đầu dòng.

---

## 3. Hoàn thiện code (Core Implementation) — Cá nhân (30 điểm)

Lệnh kiểm thử:

```powershell
python -m pytest tests -v
```

Kết quả:

```text
42 passed
```

**Số lượng bài test vượt qua:** 42/42.

---

## 4. Dự đoán độ tương tự (Similarity Predictions) — Cá nhân (5 điểm)

- Embedder: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
- Quy tắc thực nghiệm: score từ `0.50` trở lên là **Cao**.

| Cặp | Câu A | Câu B | Dự đoán | Điểm thực tế | Phân loại | Kết luận |
|---:|---|---|---|---:|---|---|
| 1 | Sinh viên có thể gia hạn sách trực tuyến. | Người học được phép kéo dài thời gian mượn tài liệu online. | Cao | 0.758805 | Cao | Đúng |
| 2 | Sinh viên phải đóng học phí trước thời hạn quy định. | Học phí cần được thanh toán trước hạn được nhà trường công bố. | Cao | 0.790770 | Cao | Đúng |
| 3 | Thư viện mở cửa từ thứ Hai đến thứ Sáu. | Ký túc xá có khu vực sinh hoạt chung. | Thấp | 0.141858 | Thấp | Đúng |
| 4 | Sinh viên cần đăng ký học phần trên cổng thông tin. | Người học lựa chọn môn học qua hệ thống trực tuyến. | Cao | 0.650318 | Cao | Đúng |
| 5 | Điều kiện xét học bổng liên quan đến GPA của sinh viên. | Sinh viên có thể mượn tối đa năm cuốn sách. | Thấp | 0.345593 | Thấp | Đúng |

**Số dự đoán đúng:** 5/5.

**Nhận xét**

Cặp 1 là kết quả đáng chú ý nhất với score `0.758805`. Kết quả cho thấy embedding không chỉ so khớp từ khóa mà còn biểu diễn chủ đề và quan hệ ngữ nghĩa tổng quát. Tuy nhiên, cosine similarity cao không có nghĩa hai câu hoàn toàn tương đương về mặt thông tin.

---

## 5. Kết quả truy xuất của tôi (Competition Results) — Cá nhân (10 điểm)

### Dữ liệu và cấu hình

- Corpus gồm 7 tài liệu công khai về học phí, phương thức thanh toán, lịch học phí và học bổng RMIT Việt Nam.
- Benchmark được đọc trực tiếp từ `data/k3_tuition/benchmark_queries.csv`.
- Embedder: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
- Chunker: `FixedSizeChunker(chunk_size=300, overlap=50)`
- Query số 1 dùng `metadata_filter={"audience": "student"}`.

| # | Câu hỏi | Top-1 chunk | Score | Tài liệu đúng trong top-3? | Câu trả lời trích xuất từ context | Điểm |
|---:|---|---|---:|---|---|---:|
| 1 | Học phí tại RMIT Việt Nam được tính và thanh toán như thế nào? | rmit tuition 2026 — chunk 1: inh viên đăng ký trong học kỳ. Mỗi năm RMIT Việt Nam có ba học kỳ; sinh viên có thể đăng ký tối đa ba môn trong một học kỳ. Học phí được tính bằng Việt Nam đồng. Thanh toán bằng ngoại tệ đượ… | 0.835292 | Có | inh viên đăng ký trong học kỳ. Mỗi năm RMIT Việt Nam có ba học kỳ; sinh viên có thể đăng ký tối đa ba môn trong một học kỳ. Học phí được tính bằng Việt Nam đồng. Thanh toán bằng ngoại tệ được quy đổi sang Việt Nam đồng theo tỷ giá tại ngày thanh toán; người thanh toán chịu các phí liên quan. T | 2/2 |
| 2 | Hạn thanh toán học phí Học kỳ 2 năm 2026 là ngày nào? | rmit academic calendar 2026 — chunk 0: Các hạn học phí chính năm 2026 Học kỳ 1 Hóa đơn học phí được phát hành: 27/02/2026. Học kỳ bắt đầu: 02/03/2026. Hạn thanh toán học phí: 20/03/2026. Hạn cuối rút môn hoặc bảo lưu không bị phạ… | 0.779169 | Có | Các hạn học phí chính năm 2026 Học kỳ 1 Hóa đơn học phí được phát hành: 27/02/2026. Học kỳ bắt đầu: 02/03/2026. Hạn thanh toán học phí: 20/03/2026. Hạn cuối rút môn hoặc bảo lưu không bị phạt phí: 27/03/2026. Học kỳ 2 Hóa đơn học phí được phát hành: 26/06/2026. Học kỳ bắt | 2/2 |
| 3 | Khi chuyển khoản học phí, nội dung chuyển khoản cần có những thông tin gì? | rmit fees guide 2026 — chunk 5: ý môn còn phải nộp giấy tờ thay đổi đăng ký, bảo lưu, thôi học hoặc đề nghị xem xét nghĩa vụ tài chính, tùy trường hợp. Có thể hoàn toàn bộ học phí khi trường rút thư mời hoặc không thể cung… | 0.657504 | Có | Nội dung chuyển khoản Nội dung chuyển khoản cần có: Họ tên sinh viên. Mã số sinh viên; nếu chưa có mã số thì dùng ngày tháng năm sinh theo hướng dẫn. Nội dung khoản thanh toán, ví dụ học phí của học kỳ cụ thể. Lưu ý tại quầy Quầy Thu ngân của trường thông thường chỉ nhận thẻ ngân hàng. | 2/2 |
| 4 | Sinh viên học kỳ thứ hai trở đi phải rút môn trước thời điểm nào để có thể được hoàn toàn bộ học phí trả trước của học kỳ? | rmit fees guide 2026 — chunk 6: ến thông tin sai do người học cung cấp. Sinh viên học kỳ thứ hai trở đi rút môn hoặc chương trình trước khi kết thúc ngày làm việc Thứ Sáu tuần thứ tư của học kỳ có thể được hoàn toàn bộ phầ… | 0.815621 | Có | ến thông tin sai do người học cung cấp. Sinh viên học kỳ thứ hai trở đi rút môn hoặc chương trình trước khi kết thúc ngày làm việc Thứ Sáu tuần thứ tư của học kỳ có thể được hoàn toàn bộ phần học phí đã trả trước cho học kỳ đó. Tài liệu phân biệt hoàn toàn bộ, hoàn một phần, không hoàn và hoàn/b | 2/2 |
| 5 | Điều kiện GPA tối thiểu của học bổng thành tích dành cho sinh viên hiện đang học tại RMIT năm 2026 là bao nhiêu? | rmit current student scholarship 2026 — chunk 1: chính Ứng viên phải: Là sinh viên hiện đang học chương trình cử nhân tại RMIT Việt Nam. Đã hoàn tất ít nhất 96 tín chỉ. Có GPA tích lũy từ 3,4/4,0 trở lên. Số lượng và phân bổ học bổng được… | 0.788943 | Có | chính Ứng viên phải: Là sinh viên hiện đang học chương trình cử nhân tại RMIT Việt Nam. Đã hoàn tất ít nhất 96 tín chỉ. Có GPA tích lũy từ 3,4/4,0 trở lên. Số lượng và phân bổ học bổng được công bố theo từng khoa và từng học kỳ. Trường bảo lưu quyền thay đổi giá trị hoặc phân bổ khi cần thi | 2/2 |

**Số câu có tài liệu đúng trong top-3:** 5/5.  
**Điểm retrieval tự đánh giá:** 10/10.

### Nhận xét về metadata filter

Query số 1 sử dụng `audience=student` theo yêu cầu của biến thể K3. Vì các tài liệu trong corpus hiện đều hướng đến sinh viên, filter này chủ yếu xác nhận đúng phạm vi đối tượng hơn là giảm mạnh số candidate. Có thể tăng giá trị của metadata filtering bằng cách kết hợp thêm `category`, ví dụ `tuition_schedule`, `payment_instructions` hoặc `scholarship`.

### Bài học rút ra

Fixed-size chunking dễ kiểm soát và có overlap giúp hạn chế mất ngữ cảnh. Tuy nhiên, với các tài liệu có heading và danh sách gạch đầu dòng, SentenceChunker hoặc chiến lược chia theo section có thể giữ cấu trúc ý nghĩa tốt hơn. Kết quả chi tiết được lưu tại `report/retrieval_results_k3_tuition.md`.

---

## Tự đánh giá

| Tiêu chí | Điểm |
|---|---:|
| Khởi động | 5/5 |
| Hướng tiếp cận | 10/10 |
| Hoàn thiện code | 30/30 |
| Dự đoán độ tương tự | 5/5 |
| Kết quả truy xuất | 10/10 |
| **Tổng** | **60/60** |

> Điểm Phần 5 được script tính theo rubric: 2 điểm nếu tài liệu đúng nằm trong top-3 và câu trả lời trích xuất đủ gần gold answer; 1 điểm nếu tài liệu đúng có trong top-3 nhưng câu trả lời còn thiếu; 0 điểm nếu tài liệu đúng không có trong top-3.

