# Báo Cáo Cá Nhân — Lab 7: Embedding & Vector Store

**Họ tên:** Trần Quốc Hùng
**Nhóm:** NguyenTheAnh
**Ngày:** 03/08/2026

> Phần retrieval trong báo cáo này dùng corpus chung RMIT về quy định học phí. Kết quả benchmark hiện tại được chạy bằng mock embedding vì local multilingual embedder chưa khởi tạo xong trong môi trường; mock chỉ dùng để kiểm tra pipeline, không dùng làm kết luận cuối cùng về chất lượng ngữ nghĩa.

**Tổng điểm phần cá nhân: 60** = Khởi động (5) + Hướng tiếp cận (10) + Hoàn thiện code (30) + Dự đoán độ tương tự (5) + Kết quả truy xuất (10).

---

## 1. Khởi động (Warm-up) — Cá nhân (5 điểm)

### Độ tương tự Cosine

Độ tương tự cosine cao nghĩa là hai vector embedding có hướng gần nhau; với text embedding, điều này thường cho thấy hai đoạn văn có nội dung hoặc ý nghĩa gần nhau. Giá trị thấp hoặc âm cho thấy hai vector ít liên quan hoặc có hướng ngược nhau.

**Ví dụ có độ tương tự cao:**

- Câu A: `Sinh viên thanh toán học phí theo từng học kỳ.`
- Câu B: `Học phí được trả vào mỗi học kỳ.`
- Tại sao tương đồng: Hai câu diễn đạt cùng một ý dù dùng từ khác nhau.

**Ví dụ có độ tương tự thấp:**

- Câu A: `Sinh viên cần thanh toán học phí trước hạn.`
- Câu B: `Thư viện mở cửa vào buổi tối.`
- Tại sao khác: Hai câu nói về hai chủ đề khác nhau là tài chính và thư viện.

Cosine similarity thường phù hợp với text embeddings vì nó tập trung vào hướng biểu diễn, ít phụ thuộc vào độ lớn tuyệt đối của vector. Hai văn bản dài/ngắn khác nhau vẫn có thể được xem là tương đồng nếu embedding của chúng có hướng gần nhau.

### Bài toán tính toán Chunking

Với `length=10,000`, `chunk_size=500`, `overlap=50`:

```text
step = 500 - 50 = 450
number_of_chunks = ceil((10,000 - 50) / 450)
                  = ceil(9,950 / 450)
                  = 23 chunks
```

Nếu `overlap=100`:

```text
step = 500 - 100 = 400
number_of_chunks = ceil((10,000 - 100) / 400)
                  = ceil(9,900 / 400)
                  = 25 chunks
```

Overlap lớn hơn giúp giữ ngữ cảnh ở ranh giới giữa hai chunk, nhưng làm tăng số lượng chunk, chi phí embedding và khả năng trùng lặp dữ liệu.

---

## 2. Hướng tiếp cận của tôi (My Approach) — Cá nhân (10 điểm)

### Các hàm chia nhỏ (Chunking Functions)

Tôi chọn `RecursiveChunker(chunk_size=500)` làm strategy cá nhân. `SentenceChunker` dùng regex để giữ các câu kết thúc bằng `.`, `!` hoặc `?`, sau đó gom tối đa số câu được cấu hình vào một chunk. Trường hợp text rỗng trả về danh sách rỗng và khoảng trắng dư được loại bỏ.

`RecursiveChunker` thử các separator theo thứ tự ưu tiên, gồm đoạn văn, dòng mới, dấu chấm và khoảng trắng. Nếu một mảnh vẫn lớn hơn giới hạn, thuật toán tiếp tục đệ quy với separator thấp hơn; base case là mảnh đã nhỏ hơn `chunk_size` hoặc không còn separator phù hợp, khi đó fallback sang cắt theo ký tự.

### Lớp EmbeddingStore

`add_documents` tạo embedding cho từng `Document` và lưu một record gồm `id`, `content`, `metadata` và `embedding`. `search` tạo embedding cho query, tính dot product với các vector đã lưu, sắp xếp score giảm dần và trả về tối đa `top_k` kết quả.

`search_with_filter` lọc record theo metadata trước rồi mới tính similarity trên tập ứng viên đã lọc. `delete_document` xóa record có `id` bằng `doc_id` hoặc có `metadata["doc_id"]` tương ứng, nên có thể xóa cả document đơn lẻ và toàn bộ chunks của một tài liệu.

### Tác tử KnowledgeBaseAgent

`answer` trước hết truy xuất top-k chunks từ `EmbeddingStore`. Các chunks được nối thành phần `Context` trong prompt, cùng với câu hỏi và hướng dẫn chỉ trả lời dựa trên context. Sau đó prompt được truyền cho hàm `llm_fn`; nếu không có context, agent được yêu cầu nói rõ rằng không đủ thông tin.

---

## 3. Hoàn thiện code (Core Implementation) — Cá nhân (30 điểm)

Đã triển khai các phần còn thiếu trong `src/chunking.py`, `src/store.py` và `src/agent.py`.

Kết quả kiểm thử:

```text
42 passed in 0.13s
```

**Số lượng bài test vượt qua:** 42 / 42

---

## 4. Dự đoán độ tương tự (Similarity Predictions) — Cá nhân (5 điểm)

Các điểm dưới đây được tính bằng `_mock_embed`, vì local multilingual embedder chưa hoàn tất khởi tạo.

| Cặp | Câu A | Câu B | Dự đoán | Điểm thực tế | Đúng? |
|------|-----------|-----------|---------|--------------|-------|
| 1 | Học phí được thanh toán theo từng học kỳ. | Sinh viên trả học phí theo mỗi học kỳ. | cao | 0.0390 | Không phản ánh đúng dự đoán |
| 2 | Học phí được thanh toán theo từng học kỳ. | Thư viện mở cửa đến 21 giờ. | thấp | 0.0438 | Không phản ánh rõ |
| 3 | Rút môn đúng hạn có thể được hoàn học phí. | Có thể yêu cầu hoàn trả học phí khi rút môn đúng thời hạn. | cao | -0.0204 | Không |
| 4 | GPA tối thiểu là 3,4 trên 4,0. | Mức GPA yêu cầu là 3,4/4,0. | cao | -0.2104 | Không |
| 5 | RMIT có chính sách học bổng. | Hạn thanh toán học phí là ngày 17/07/2026. | thấp | 0.0450 | Không phản ánh rõ |

Kết quả khá bất ngờ: các cặp câu có nghĩa gần nhau không nhận được điểm cao. Điều này cho thấy mock embedding được tạo gần như ngẫu nhiên theo chuỗi, nên không biểu diễn tốt ngữ nghĩa tiếng Việt. Vì vậy không nên dùng các điểm mock này để kết luận strategy retrieval nào tốt hơn.

---

## 5. Kết quả truy xuất của tôi (Competition Results) — Cá nhân (10 điểm)

**Strategy:** `RecursiveChunker(chunk_size=500)`  
**Embedding:** mock fallback, chỉ dùng để kiểm tra pipeline; cần thay bằng local embedder cho kết quả chính thức.

| # | Câu hỏi | Top-1 chunk truy xuất được | Score | Liên quan? | Câu trả lời/nhận xét |
|---|---|---|---:|---|---|
| 1 | Học phí tại RMIT Việt Nam được tính và thanh toán như thế nào? | `rmit_tuition_2026`, chunk 4 | 0.1306 | Chưa đủ | Top-1 nói về phí phụ thu, chưa chứa nguyên tắc tính học phí đầy đủ. |
| 2 | Hạn thanh toán học phí Học kỳ 2 năm 2026 là ngày nào? | `rmit_fees_guide_2026`, chunk 6 | 0.1740 | Không | Top-3 chưa lấy được chunk lịch học kỳ chứa ngày 17/07/2026. |
| 3 | Khi chuyển khoản học phí, nội dung chuyển khoản cần có những thông tin gì? | `rmit_payment_methods`, chunk 2 | 0.2190 | Có | Chunk chứa họ tên, mã số sinh viên/ngày sinh và nội dung khoản thanh toán. |
| 4 | Sinh viên học kỳ thứ hai trở đi phải rút môn trước thời điểm nào để được hoàn học phí? | `rmit_fees_guide_2026`, chunk 4 | 0.3239 | Có | Top-1 chứa đúng mục hoàn trả học phí và điều kiện rút môn. |
| 5 | Điều kiện GPA tối thiểu của học bổng thành tích năm 2026 là bao nhiêu? | `rmit_tuition_assistance_2026`, chunk 0 | 0.2455 | Không | Top-3 chưa lấy được tài liệu học bổng dành cho sinh viên hiện đang học. |

**Số câu hỏi trả về chunk liên quan trong top-3:** 2 / 5 với mock embedding.

Kết quả này chỉ là baseline kỹ thuật. Mock embedding làm điểm similarity gần như ngẫu nhiên; cần chạy lại bằng `EMBEDDING_PROVIDER=local` trước khi dùng bảng này để so sánh chính thức giữa các thành viên.

**Điều học được:** Chunking theo separator giúp giữ nguyên các mục như “Hoàn trả học phí”, nên query 4 được truy xuất tốt. Ngược lại, chunk size và embedding không phù hợp có thể làm query ngày tháng hoặc học bổng bị xếp hạng sai.

---

## Tự Đánh Giá (Phần Cá Nhân)

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Khởi động (Warm-up) | 5 / 5 |
| Hướng tiếp cận của tôi (My Approach) | 10 / 10 |
| Hoàn thiện code (Core Implementation — tests) | 30 / 30 |
| Dự đoán độ tương tự (Similarity Predictions) | 5 / 5 |
| Kết quả truy xuất của tôi (Competition Results) | Chờ chạy lại bằng local / 10 |
| **Tổng phần cá nhân** | **50 + retrieval local / 60** |

