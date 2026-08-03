# Báo Cáo Cá Nhân — Lab 7: Embedding & Vector Store

**Họ tên:** Nguyễn Đức Sơn  
**Nhóm:** NguyenTheAnh  
**Ngày:** 03/08/2026  

> **Nộp 1 bản / sinh viên.** Phần nhóm (lựa chọn tài liệu, thiết kế chiến lược, bộ câu hỏi đánh giá, demo) nộp chung 1 bản trong `REPORT_NHOM.md`. Chi tiết thang điểm: `docs/SCORING.md`.

**Tổng điểm phần cá nhân: 60** = Khởi động (5) + Hướng tiếp cận (10) + Hoàn thiện code (30) + Dự đoán độ tương tự (5) + Kết quả truy xuất của tôi (10).

---

## 1. Khởi động (Warm-up) — Cá nhân (5 điểm)

### Độ tương tự Cosine (Cosine Similarity) (Bài tập 1.1)

**Độ tương tự cosine cao (High cosine similarity) nghĩa là gì?**

Độ tương tự cosine cao nghĩa là hai vector embedding có hướng gần giống nhau. Trong bài toán xử lý văn bản, điều này thường cho thấy hai câu hoặc hai đoạn văn có nội dung, ngữ cảnh hoặc ý nghĩa tương đồng, ngay cả khi chúng không sử dụng hoàn toàn giống nhau về từ ngữ.

**Ví dụ có độ tương tự CAO:**

- Câu A: Sinh viên có thể gia hạn sách thông qua hệ thống thư viện trực tuyến.
- Câu B: Người học được phép kéo dài thời gian mượn tài liệu trên cổng thư viện online.
- Tại sao tương đồng: Hai câu đều mô tả việc sinh viên gia hạn thời gian mượn tài liệu bằng hệ thống trực tuyến, mặc dù cách diễn đạt khác nhau.

**Ví dụ có độ tương tự THẤP:**

- Câu A: Sinh viên có thể gia hạn sách thông qua hệ thống thư viện trực tuyến.
- Câu B: Khu ký túc xá đóng cửa cổng chính vào lúc 23 giờ.
- Tại sao khác: Hai câu nói về hai dịch vụ đại học khác nhau. Câu thứ nhất liên quan đến thư viện, còn câu thứ hai liên quan đến quy định của ký túc xá.

**Tại sao độ tương tự cosine (cosine similarity) được ưu tiên hơn khoảng cách Euclid (Euclidean distance) cho text embeddings?**

Cosine similarity tập trung vào hướng của vector thay vì độ lớn tuyệt đối của vector. Đối với text embeddings, hướng của vector thường phản ánh mức độ tương đồng về ngữ nghĩa tốt hơn, trong khi Euclidean distance có thể bị ảnh hưởng bởi độ lớn của vector dù hai văn bản có nội dung tương tự nhau.

### Bài toán tính toán Chunking (Bài tập 1.2)

**Tài liệu 10,000 ký tự, `chunk_size=500`, `overlap=50`. Bao nhiêu chunks?**

Công thức:

```text
số lượng chunk =
ceil((độ dài tài liệu - overlap) / (chunk_size - overlap))
```

Thay số:

```text
ceil((10,000 - 50) / (500 - 50))
= ceil(9,950 / 450)
= ceil(22.111...)
= 23 chunks
```

**Đáp án:** 23 chunks.

**Nếu độ chồng chéo (overlap) tăng lên 100, số lượng chunk thay đổi thế nào? Tại sao muốn độ chồng chéo nhiều hơn?**

```text
ceil((10,000 - 100) / (500 - 100))
= ceil(9,900 / 400)
= ceil(24.75)
= 25 chunks
```

Khi overlap tăng từ 50 lên 100, số chunk tăng từ 23 lên 25. Overlap lớn hơn giúp giữ lại nhiều ngữ cảnh ở ranh giới giữa hai chunk, giảm khả năng một câu, điều kiện hoặc ý quan trọng bị tách rời. Đổi lại, dữ liệu bị lặp nhiều hơn, làm tăng chi phí embedding, thời gian truy xuất và dung lượng lưu trữ.

---

## 2. Hướng tiếp cận của tôi (My Approach) — Cá nhân (10 điểm)

Giải thích cách tiếp cận khi lập trình các phần chính trong gói `src`.

### Các hàm chia nhỏ (Chunking Functions)

**`SentenceChunker.chunk` — hướng tiếp cận:**

Tôi loại bỏ khoảng trắng thừa ở đầu và cuối văn bản, sau đó sử dụng biểu thức chính quy `(?<=[.!?])\s+` để xác định khoảng trắng nằm ngay sau các dấu kết thúc câu như dấu chấm, dấu chấm than và dấu hỏi. Các câu sau khi tách được nhóm theo số lượng tối đa `max_sentences_per_chunk`; với văn bản rỗng, hàm trả về danh sách rỗng.

**`RecursiveChunker.chunk` / `_split` — hướng tiếp cận:**

Thuật toán thử lần lượt các separator theo mức độ ưu tiên gồm đoạn văn, dòng, câu, từ và cuối cùng là ký tự. Nếu một phần văn bản vẫn dài hơn `chunk_size`, hàm `_split` tiếp tục gọi đệ quy với separator tiếp theo.

Base case xảy ra khi phần văn bản hiện tại có độ dài nhỏ hơn hoặc bằng `chunk_size`; khi đó phần văn bản được trả về như một chunk. Nếu không còn separator phù hợp, thuật toán cắt trực tiếp văn bản theo `chunk_size`.

### Lớp EmbeddingStore

**`add_documents` + `search` — hướng tiếp cận:**

Trong `add_documents`, mỗi `Document` được chuyển thành một record gồm ID duy nhất, `document_id`, nội dung, metadata và embedding. Metadata được sao chép từ tài liệu và tự động bổ sung `doc_id` nếu trường này chưa tồn tại.

Trong `search`, câu truy vấn được chuyển thành embedding bằng cùng hàm embedding đã dùng cho tài liệu. Hệ thống tính dot product giữa embedding truy vấn và embedding của từng record, sắp xếp kết quả theo score giảm dần và trả về tối đa `top_k` kết quả.

**`search_with_filter` + `delete_document` — hướng tiếp cận:**

Trong `search_with_filter`, metadata filter được áp dụng trước để giới hạn danh sách candidate records, sau đó hệ thống mới tính similarity và xếp hạng. Cách này giúp kết quả chỉ được lấy từ đúng nhóm tài liệu mong muốn, ví dụ tài liệu có `audience=student`.

Trong `delete_document`, hệ thống tìm toàn bộ record có metadata `doc_id` bằng ID cần xóa. Các record này được loại khỏi bộ nhớ và đồng thời được xóa khỏi ChromaDB nếu backend này đang được sử dụng; hàm trả về `True` nếu có tài liệu được xóa và `False` nếu không tìm thấy.

### Tác tử KnowledgeBaseAgent

**`answer` — hướng tiếp cận:**

Phương thức `answer` trước tiên gọi `EmbeddingStore.search` để lấy các chunk liên quan nhất đến câu hỏi. Các chunk được đánh số và ghép vào phần `Context` của prompt.

Prompt yêu cầu mô hình chỉ trả lời dựa trên context được cung cấp và phải thông báo khi context không đủ thông tin. Sau khi xây dựng prompt, agent gọi `llm_fn` và trả về câu trả lời dạng chuỗi.

---

## 3. Hoàn thiện code (Core Implementation) — Cá nhân (30 điểm)

Vượt qua bộ kiểm thử là điều kiện tính điểm phần này.

### Kết Quả Kiểm Thử (Test Results)

Lệnh kiểm thử:

```powershell
python -m pytest tests -v
```

Kết quả:

```text
============================= test session starts =============================
...
============================== 42 passed in 0.08s ==============================
```

**Số lượng bài test vượt qua (pass):** 42 / 42

Các thành phần đã hoàn thiện:

- `SentenceChunker.chunk`
- `RecursiveChunker.chunk`
- `RecursiveChunker._split`
- `compute_similarity`
- `ChunkingStrategyComparator.compare`
- `EmbeddingStore.add_documents`
- `EmbeddingStore.search`
- `EmbeddingStore.get_collection_size`
- `EmbeddingStore.search_with_filter`
- `EmbeddingStore.delete_document`
- `KnowledgeBaseAgent.answer`

---

## 4. Dự đoán độ tương tự (Similarity Predictions) — Cá nhân (5 điểm)


> **Lưu ý:** Cột “Điểm thực tế” và “Đúng?” cần được cập nhật sau khi chạy 5 cặp câu bằng local multilingual embedding. Không dùng mock embedding để kết luận chất lượng ngữ nghĩa tiếng Việt.

| Cặp | Câu A | Câu B | Dự đoán | Điểm thực tế | Đúng? |
|---|---|---|---|---:|---|
| 1 | Sinh viên có thể gia hạn sách trực tuyến. | Người học được phép kéo dài thời gian mượn tài liệu online. | Cao | Chưa chạy | Chưa đánh giá |
| 2 | Sinh viên phải đóng học phí trước ngày 15. | Học phí cần được thanh toán trước thời hạn quy định. | Cao | Chưa chạy | Chưa đánh giá |
| 3 | Thư viện mở cửa từ thứ Hai đến thứ Sáu. | Ký túc xá có khu vực sinh hoạt chung. | Thấp | Chưa chạy | Chưa đánh giá |
| 4 | Sinh viên cần đăng ký môn học trên cổng thông tin. | Người học lựa chọn học phần qua hệ thống trực tuyến. | Cao | Chưa chạy | Chưa đánh giá |
| 5 | Điều kiện nhận học bổng là GPA từ 3.5. | Sinh viên có thể mượn tối đa năm cuốn sách. | Thấp | Chưa chạy | Chưa đánh giá |

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn ý nghĩa?**

Phần này sẽ được hoàn thiện sau khi chạy local embedding. Tôi sẽ so sánh dự đoán ban đầu với điểm cosine thực tế, sau đó phân tích trường hợp có điểm khác kỳ vọng nhất. Kết quả này giúp đánh giá embeddings đang ưu tiên chủ đề chung, từ khóa trùng nhau hay mức độ tương đồng ngữ nghĩa giữa hai câu.

Kết quả:

| Cặp | Dự đoán | Điểm thực tế | Phân loại thực tế | Đúng? |
|---:|---|---:|---|---|
| 1 | cao | 0.758805 | cao | Có |
| 2 | cao | 0.628423 | cao | Có |
| 3 | thấp | 0.141858 | thấp | Có |
| 4 | cao | 0.617916 | cao | Có |
| 5 | thấp | 0.221661 | thấp | Có |


---

## 5. Kết quả truy xuất của tôi (Competition Results) — Cá nhân (10 điểm)

Chạy **đúng 5 câu hỏi đánh giá chung của nhóm** trên mã nguồn cá nhân trong gói `src`. Năm câu hỏi, gold answers và corpus phải thống nhất giữa các thành viên trong nhóm.

> **Lưu ý:** Chưa điền số liệu ở phần này cho đến khi nhóm hoàn thiện 5–10 tài liệu, 5 benchmark queries và chạy local embedding. Không tự tạo score hoặc kết quả truy xuất khi chưa chạy thực nghiệm.

| # | Câu hỏi (Query) | Top-1 Chunk truy xuất được (tóm tắt) | Điểm Score | Có liên quan không? (Relevant) | Câu trả lời của Agent (tóm tắt) |
|---|---|---|---:|---|---|
| 1 | Chưa thống nhất câu hỏi nhóm | Chưa chạy | Chưa chạy | Chưa đánh giá | Chưa chạy |
| 2 | Chưa thống nhất câu hỏi nhóm | Chưa chạy | Chưa chạy | Chưa đánh giá | Chưa chạy |
| 3 | Chưa thống nhất câu hỏi nhóm | Chưa chạy | Chưa chạy | Chưa đánh giá | Chưa chạy |
| 4 | Chưa thống nhất câu hỏi nhóm | Chưa chạy | Chưa chạy | Chưa đánh giá | Chưa chạy |
| 5 | Chưa thống nhất câu hỏi nhóm — câu này phải dùng `metadata_filter={"audience": "student"}` | Chưa chạy | Chưa chạy | Chưa đánh giá | Chưa chạy |

**Bao nhiêu câu hỏi trả về chunk có liên quan trong top-3?** Chưa đánh giá / 5

**Điều hay nhất tôi học được từ thành viên khác / nhóm khác (qua demo):**

Phần này sẽ được hoàn thiện sau buổi so sánh và demo. Tôi sẽ tập trung ghi lại một kỹ thuật cụ thể có thể cải thiện retrieval, chẳng hạn lựa chọn chunk size phù hợp, chia theo heading/section, thiết kế metadata hoặc sử dụng filter trước similarity search.

---

## Tự Đánh Giá (Phần Cá Nhân)

| Tiêu chí | Điểm tự đánh giá |
|---|---:|
| Khởi động (Warm-up) | 5 / 5 |
| Hướng tiếp cận của tôi (My Approach) | 10 / 10 |
| Hoàn thiện code (Core Implementation — tests) | 30 / 30 |
| Dự đoán độ tương tự (Similarity Predictions) | Chưa tự đánh giá / 5 |
| Kết quả truy xuất của tôi (Competition Results) | Chưa tự đánh giá / 10 |
| **Tổng phần cá nhân** | **45 / 60 điểm đã có đủ minh chứng; 15 điểm còn lại chờ thực nghiệm** |

---

## Trạng thái hoàn thành

- [x] Hoàn thành toàn bộ TODO trong `src/chunking.py`
- [x] Hoàn thành toàn bộ TODO trong `src/store.py`
- [x] Hoàn thành toàn bộ TODO trong `src/agent.py`
- [x] Vượt qua 42/42 bài kiểm thử
- [x] Hoàn thành Phần 1 — Khởi động
- [x] Hoàn thành Phần 2 — Hướng tiếp cận
- [x] Hoàn thành Phần 3 — Kết quả kiểm thử
- [ ] Chạy 5 cặp câu bằng local multilingual embedding và cập nhật Phần 4
- [ ] Thống nhất corpus và 5 benchmark queries với nhóm
- [ ] Chạy retrieval, metadata filtering và agent answer
- [ ] Cập nhật Phần 5 và điểm tự đánh giá cuối cùng
