# Báo cáo cá nhân — Nguyễn Đức Sơn

**Mã sinh viên:** 2A202601485  
**Nhóm:** NguyenTheAnh  
**Ngày:** 03/08/2026

> Báo cáo này sử dụng corpus chung RMIT trong `data/k3_tuition/` và 5 benchmark queries chung. Các kết quả retrieval được thành viên cung cấp với `FixedSizeChunker(chunk_size=300, overlap=50)` và multilingual embedding `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`.

## 1. Khởi động

Cosine similarity đo mức gần nhau về hướng giữa hai vector embedding. Với văn bản, score cao thường cho thấy hai câu có chủ đề hoặc ý nghĩa tương đồng dù cách diễn đạt khác nhau. Cosine phù hợp với text embedding vì ít phụ thuộc vào độ dài tuyệt đối của văn bản hơn khoảng cách Euclid.

Với tài liệu 10.000 ký tự, `chunk_size=500`, `overlap=50`:

```text
ceil((10000 - 50) / (500 - 50)) = 23 chunks
```

Với `overlap=100`:

```text
ceil((10000 - 100) / (500 - 100)) = 25 chunks
```

Overlap lớn hơn giữ thêm ngữ cảnh ở ranh giới chunk nhưng làm tăng số chunk và chi phí embedding.

## 2. Hướng tiếp cận

`SentenceChunker` dùng regex để tách câu sau các dấu `.`, `!`, `?`, loại bỏ khoảng trắng và gom câu theo giới hạn cấu hình. `RecursiveChunker` thử separator theo thứ tự đoạn, dòng, câu và từ; nếu vẫn quá dài thì tiếp tục đệ quy hoặc cắt cứng khi hết separator.

`EmbeddingStore` lưu `id`, nội dung, metadata và embedding. Khi search, query được embed bằng cùng backend, tính dot product, sắp xếp score giảm dần và lấy `top_k`. Filter được áp dụng trước similarity; delete tìm theo `id` hoặc `metadata["doc_id"]`.

`KnowledgeBaseAgent` lấy top-k context, ghép vào prompt, yêu cầu LLM chỉ trả lời từ context và gọi `llm_fn`.

Strategy cá nhân:

```python
FixedSizeChunker(chunk_size=300, overlap=50)
```

Strategy này tạo chunk có kích thước ổn định và overlap giúp bảo toàn ngữ cảnh, nhưng có thể cắt giữa câu hoặc giữa danh sách.

## 3. Hoàn thiện code

```text
42 passed
```

Đã hoàn thiện các module chunking, vector store và agent.

## 4. Dự đoán similarity

| Cặp | Dự đoán | Score | Kết quả |
|---:|---|---:|---|
| 1. Gia hạn sách trực tuyến / kéo dài thời gian mượn online | Cao | 0.758805 | Đúng |
| 2. Đóng học phí trước hạn / thanh toán trước hạn công bố | Cao | 0.790770 | Đúng |
| 3. Thư viện mở cửa / ký túc xá có khu sinh hoạt | Thấp | 0.141858 | Đúng |
| 4. Đăng ký học phần online / lựa chọn môn qua hệ thống | Cao | 0.650318 | Đúng |
| 5. Học bổng theo GPA / mượn tối đa năm sách | Thấp | 0.345593 | Đúng |

Kết quả cho thấy embedding multilingual có thể nhận ra các cặp câu diễn đạt cùng ý. Tuy nhiên score cao không đảm bảo hai câu chứa toàn bộ thông tin giống hệt nhau.

## 5. Kết quả retrieval

| # | Top-1 | Score | Chunk liên quan trong top-3? | Kết quả |
|---:|---|---:|---|---|
| 1 | `rmit_tuition_2026`, chunk 1 | 0.835292 | Có | Trả về nguyên tắc thanh toán theo học kỳ và số môn đăng ký. |
| 2 | `rmit_academic_calendar_2026`, chunk 0 | 0.779169 | Có | Truy xuất được lịch và hạn thanh toán Học kỳ 2. |
| 3 | `rmit_fees_guide_2026`, chunk 5 | 0.657504 | Có | Context chứa nội dung chuyển khoản. |
| 4 | `rmit_fees_guide_2026`, chunk 6 | 0.815621 | Có | Truy xuất đúng điều kiện hoàn học phí. |
| 5 | `rmit_current_student_scholarship_2026`, chunk 1 | 0.788943 | Có | Truy xuất đúng GPA 3,4/4,0 và 96 tín chỉ. |

**Số câu có chunk liên quan trong top-3:** 5/5.  
**Điểm retrieval tạm tính:** 10/10.

### Nhận xét/failure case

Fixed-size chunking có overlap giúp các query có từ khóa rõ ràng lấy đúng tài liệu. Điểm yếu là có thể cắt giữa heading hoặc câu; chiến lược theo section có thể cải thiện tính mạch lạc. Kết quả được ghi kèm local embedding provider để nhóm phân biệt ảnh hưởng của model với ảnh hưởng của chunking.

## Tự đánh giá

| Hạng mục | Điểm |
|---|---:|
| Khởi động | 5/5 |
| Hướng tiếp cận | 10/10 |
| Code | 30/30 |
| Dự đoán similarity | 5/5 |
| Retrieval | 10/10 |
| **Tổng** | **60/60** |

