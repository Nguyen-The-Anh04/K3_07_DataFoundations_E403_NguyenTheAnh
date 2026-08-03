# Kết quả retrieval chi tiết — K3 Tuition

- Sinh viên: **Nguyễn Đức Sơn**
- Embedder: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
- Chunker: `FixedSizeChunker(300, overlap=50)`
- Corpus: `data/k3_tuition/documents`

## Query 1

**Câu hỏi:** Học phí tại RMIT Việt Nam được tính và thanh toán như thế nào?

**Gold answer:** Học phí được thanh toán theo từng học kỳ và dựa trên số môn sinh viên đăng ký trong học kỳ.

**Nguồn chuẩn:** `rmit_tuition_2026 / mục “Nguyên tắc tính và thanh toán”`

**Metadata filter:** `{'audience': 'student'}`

### Top 1

- Score: `0.835292`
- doc_id: `rmit_tuition_2026`
- chunk_index: `1`
- source_url: `https://www.rmit.edu.vn/vi/hoc-tap-tai-rmit/hoc-phi`
- Nội dung: inh viên đăng ký trong học kỳ. Mỗi năm RMIT Việt Nam có ba học kỳ; sinh viên có thể đăng ký tối đa ba môn trong một học kỳ. Học phí được tính bằng Việt Nam đồng. Thanh toán bằng ngoại tệ được quy đổi sang Việt Nam đồng theo tỷ giá tại ngày thanh toán; người thanh toán chịu các phí liên quan. T

### Top 2

- Score: `0.756222`
- doc_id: `rmit_tuition_2026`
- chunk_index: `0`
- source_url: `https://www.rmit.edu.vn/vi/hoc-tap-tai-rmit/hoc-phi`
- Nội dung: Phạm vi áp dụng Trang công bố học phí năm 2026 dành cho sinh viên, học viên mới nhập học các chương trình đại học và sau đại học tại RMIT Việt Nam. Nguyên tắc tính và thanh toán Học phí được thanh toán theo từng học kỳ và dựa trên số môn sinh viên đăng ký trong học kỳ. Mỗi năm RMIT Việt

### Top 3

- Score: `0.748091`
- doc_id: `rmit_full_scholarship_2026`
- chunk_index: `1`
- source_url: `https://www.rmit.edu.vn/vi/hoc-tap-tai-rmit/hoc-bong/hoc-bong-dai-hoc-cho-sinh-vien-tuong-lai/hoc-bong-hieu-truong`
- Nội dung: 3/07/2026. Công bố kết quả: 25/09/2026. Số lượng công bố: 7 suất. Phạm vi áp dụng Đây là học bổng thường niên dành cho sinh viên mới đáp ứng toàn bộ yêu cầu đầu vào của một chương trình cử nhân tại RMIT Việt Nam. Khả năng truy cập Trang công khai trên website chính thức của RMIT Việt N

**Tài liệu đúng trong top-3:** Có

**Vị trí:** 1, 2

**Câu trả lời trích xuất từ context:** inh viên đăng ký trong học kỳ. Mỗi năm RMIT Việt Nam có ba học kỳ; sinh viên có thể đăng ký tối đa ba môn trong một học kỳ. Học phí được tính bằng Việt Nam đồng. Thanh toán bằng ngoại tệ được quy đổi sang Việt Nam đồng theo tỷ giá tại ngày thanh toán; người thanh toán chịu các phí liên quan. T

**Similarity giữa câu trả lời trích xuất và gold answer:** `0.521490`

**Điểm:** 2/2

## Query 2

**Câu hỏi:** Hạn thanh toán học phí Học kỳ 2 năm 2026 là ngày nào?

**Gold answer:** Ngày 17/07/2026.

**Nguồn chuẩn:** `rmit_academic_calendar_2026 / mục “Học kỳ 2”`

**Metadata filter:** `None`

### Top 1

- Score: `0.779169`
- doc_id: `rmit_academic_calendar_2026`
- chunk_index: `0`
- source_url: `https://www.rmit.edu.vn/assets/vn/en/assets-for-production/documents/pdfs/academic-calendar/academic-calendar-2026-jun26.pdf`
- Nội dung: Các hạn học phí chính năm 2026 Học kỳ 1 Hóa đơn học phí được phát hành: 27/02/2026. Học kỳ bắt đầu: 02/03/2026. Hạn thanh toán học phí: 20/03/2026. Hạn cuối rút môn hoặc bảo lưu không bị phạt phí: 27/03/2026. Học kỳ 2 Hóa đơn học phí được phát hành: 26/06/2026. Học kỳ bắt

### Top 2

- Score: `0.765794`
- doc_id: `rmit_academic_calendar_2026`
- chunk_index: `1`
- source_url: `https://www.rmit.edu.vn/assets/vn/en/assets-for-production/documents/pdfs/academic-calendar/academic-calendar-2026-jun26.pdf`
- Nội dung: học phí được phát hành: 26/06/2026. Học kỳ bắt đầu: 29/06/2026. Hạn thanh toán học phí: 17/07/2026. Hạn cuối rút môn hoặc bảo lưu không bị phạt phí: 24/07/2026. Học kỳ 3 Hóa đơn học phí được phát hành: 23/10/2026. Học kỳ bắt đầu: 26/10/2026. Hạn thanh toán học phí: 13/11/2026. H

### Top 3

- Score: `0.731764`
- doc_id: `rmit_academic_calendar_2026`
- chunk_index: `2`
- source_url: `https://www.rmit.edu.vn/assets/vn/en/assets-for-production/documents/pdfs/academic-calendar/academic-calendar-2026-jun26.pdf`
- Nội dung: 10/2026. Hạn thanh toán học phí: 13/11/2026. Hạn cuối rút môn hoặc bảo lưu không bị phạt phí: 20/11/2026. Phạm vi Các mốc trên thuộc lịch năm 2026 của cơ sở Việt Nam. Người học cần đối chiếu loại chương trình và thông báo học phí cá nhân vì một số khóa học chuyên biệt có thể có lịch khác.

**Tài liệu đúng trong top-3:** Có

**Vị trí:** 1, 2, 3

**Câu trả lời trích xuất từ context:** Các hạn học phí chính năm 2026 Học kỳ 1 Hóa đơn học phí được phát hành: 27/02/2026. Học kỳ bắt đầu: 02/03/2026. Hạn thanh toán học phí: 20/03/2026. Hạn cuối rút môn hoặc bảo lưu không bị phạt phí: 27/03/2026. Học kỳ 2 Hóa đơn học phí được phát hành: 26/06/2026. Học kỳ bắt

**Similarity giữa câu trả lời trích xuất và gold answer:** `0.460755`

**Điểm:** 2/2

## Query 3

**Câu hỏi:** Khi chuyển khoản học phí, nội dung chuyển khoản cần có những thông tin gì?

**Gold answer:** Họ tên sinh viên, mã số sinh viên (hoặc ngày tháng năm sinh nếu chưa có mã số), và nội dung khoản thanh toán.

**Nguồn chuẩn:** `rmit_payment_methods / mục “Nội dung chuyển khoản”`

**Metadata filter:** `None`

### Top 1

- Score: `0.657504`
- doc_id: `rmit_fees_guide_2026`
- chunk_index: `5`
- source_url: `https://www.rmit.edu.vn/assets/vn/en/assets-for-production/documents/pdfs/study-at-rmit/tuition-fees/student-fees-and-charges-guide-06-2026.pdf`
- Nội dung: ý môn còn phải nộp giấy tờ thay đổi đăng ký, bảo lưu, thôi học hoặc đề nghị xem xét nghĩa vụ tài chính, tùy trường hợp. Có thể hoàn toàn bộ học phí khi trường rút thư mời hoặc không thể cung cấp khóa học/chương trình, trừ các trường hợp liên quan đến thông tin sai do người học cung cấp. Sinh viê

### Top 2

- Score: `0.602304`
- doc_id: `rmit_payment_methods`
- chunk_index: `3`
- source_url: `https://www.rmit.edu.vn/vi/hoc-tap-tai-rmit/hoc-phi/phuong-thuc-thanh-toan-hoc-phi`
- Nội dung: Nội dung chuyển khoản Nội dung chuyển khoản cần có: Họ tên sinh viên. Mã số sinh viên; nếu chưa có mã số thì dùng ngày tháng năm sinh theo hướng dẫn. Nội dung khoản thanh toán, ví dụ học phí của học kỳ cụ thể. Lưu ý tại quầy Quầy Thu ngân của trường thông thường chỉ nhận thẻ ngân hàng.

### Top 3

- Score: `0.586093`
- doc_id: `rmit_fees_guide_2026`
- chunk_index: `0`
- source_url: `https://www.rmit.edu.vn/assets/vn/en/assets-for-production/documents/pdfs/study-at-rmit/tuition-fees/student-fees-and-charges-guide-06-2026.pdf`
- Nội dung: Phạm vi và hiệu lực Tài liệu quy định việc thu và thanh toán học phí, phí hành chính và phí phụ thu áp dụng trong năm 2026. Việc chấp nhận thư mời nhập học hoặc hoàn tất đăng ký môn học làm phát sinh nghĩa vụ tuân thủ các điều khoản trong tài liệu. Nghĩa vụ tài chính Nghĩa vụ tài chính ph

**Tài liệu đúng trong top-3:** Có

**Vị trí:** 2

**Câu trả lời trích xuất từ context:** Nội dung chuyển khoản Nội dung chuyển khoản cần có: Họ tên sinh viên. Mã số sinh viên; nếu chưa có mã số thì dùng ngày tháng năm sinh theo hướng dẫn. Nội dung khoản thanh toán, ví dụ học phí của học kỳ cụ thể. Lưu ý tại quầy Quầy Thu ngân của trường thông thường chỉ nhận thẻ ngân hàng.

**Similarity giữa câu trả lời trích xuất và gold answer:** `0.824817`

**Điểm:** 2/2

## Query 4

**Câu hỏi:** Sinh viên học kỳ thứ hai trở đi phải rút môn trước thời điểm nào để có thể được hoàn toàn bộ học phí trả trước của học kỳ?

**Gold answer:** Trước khi kết thúc ngày làm việc Thứ Sáu của tuần thứ tư trong học kỳ, theo điều kiện của Tài liệu Hướng dẫn Thông tin học phí & Các phí phụ thu 2026.

**Nguồn chuẩn:** `rmit_fees_guide_2026 / mục “Hoàn trả học phí”`

**Metadata filter:** `None`

### Top 1

- Score: `0.815621`
- doc_id: `rmit_fees_guide_2026`
- chunk_index: `6`
- source_url: `https://www.rmit.edu.vn/assets/vn/en/assets-for-production/documents/pdfs/study-at-rmit/tuition-fees/student-fees-and-charges-guide-06-2026.pdf`
- Nội dung: ến thông tin sai do người học cung cấp. Sinh viên học kỳ thứ hai trở đi rút môn hoặc chương trình trước khi kết thúc ngày làm việc Thứ Sáu tuần thứ tư của học kỳ có thể được hoàn toàn bộ phần học phí đã trả trước cho học kỳ đó. Tài liệu phân biệt hoàn toàn bộ, hoàn một phần, không hoàn và hoàn/b

### Top 2

- Score: `0.685021`
- doc_id: `rmit_academic_calendar_2026`
- chunk_index: `0`
- source_url: `https://www.rmit.edu.vn/assets/vn/en/assets-for-production/documents/pdfs/academic-calendar/academic-calendar-2026-jun26.pdf`
- Nội dung: Các hạn học phí chính năm 2026 Học kỳ 1 Hóa đơn học phí được phát hành: 27/02/2026. Học kỳ bắt đầu: 02/03/2026. Hạn thanh toán học phí: 20/03/2026. Hạn cuối rút môn hoặc bảo lưu không bị phạt phí: 27/03/2026. Học kỳ 2 Hóa đơn học phí được phát hành: 26/06/2026. Học kỳ bắt

### Top 3

- Score: `0.680980`
- doc_id: `rmit_academic_calendar_2026`
- chunk_index: `1`
- source_url: `https://www.rmit.edu.vn/assets/vn/en/assets-for-production/documents/pdfs/academic-calendar/academic-calendar-2026-jun26.pdf`
- Nội dung: học phí được phát hành: 26/06/2026. Học kỳ bắt đầu: 29/06/2026. Hạn thanh toán học phí: 17/07/2026. Hạn cuối rút môn hoặc bảo lưu không bị phạt phí: 24/07/2026. Học kỳ 3 Hóa đơn học phí được phát hành: 23/10/2026. Học kỳ bắt đầu: 26/10/2026. Hạn thanh toán học phí: 13/11/2026. H

**Tài liệu đúng trong top-3:** Có

**Vị trí:** 1

**Câu trả lời trích xuất từ context:** ến thông tin sai do người học cung cấp. Sinh viên học kỳ thứ hai trở đi rút môn hoặc chương trình trước khi kết thúc ngày làm việc Thứ Sáu tuần thứ tư của học kỳ có thể được hoàn toàn bộ phần học phí đã trả trước cho học kỳ đó. Tài liệu phân biệt hoàn toàn bộ, hoàn một phần, không hoàn và hoàn/b

**Similarity giữa câu trả lời trích xuất và gold answer:** `0.698264`

**Điểm:** 2/2

## Query 5

**Câu hỏi:** Điều kiện GPA tối thiểu của học bổng thành tích dành cho sinh viên hiện đang học tại RMIT năm 2026 là bao nhiêu?

**Gold answer:** GPA tích lũy từ 3,4/4,0 trở lên; ứng viên cũng phải hoàn tất ít nhất 96 tín chỉ.

**Nguồn chuẩn:** `rmit_current_student_scholarship_2026 / mục “Điều kiện chính”`

**Metadata filter:** `None`

### Top 1

- Score: `0.788943`
- doc_id: `rmit_current_student_scholarship_2026`
- chunk_index: `1`
- source_url: `https://www.rmit.edu.vn/vi/hoc-tap-tai-rmit/hoc-bong/hoc-bong-thanh-tich-hoc-tap-xuat-sac-cho-sinh-vien-hien-dang-hoc-tai-rmit`
- Nội dung: chính Ứng viên phải: Là sinh viên hiện đang học chương trình cử nhân tại RMIT Việt Nam. Đã hoàn tất ít nhất 96 tín chỉ. Có GPA tích lũy từ 3,4/4,0 trở lên. Số lượng và phân bổ học bổng được công bố theo từng khoa và từng học kỳ. Trường bảo lưu quyền thay đổi giá trị hoặc phân bổ khi cần thi

### Top 2

- Score: `0.719531`
- doc_id: `rmit_tuition_2026`
- chunk_index: `3`
- source_url: `https://www.rmit.edu.vn/vi/hoc-tap-tai-rmit/hoc-phi`
- Nội dung: trạng đăng ký thực tế. Một số mức học phí đại học năm 2026 Đối với nhiều chương trình cử nhân thuộc Kinh doanh, Truyền thông & Thiết kế, và Khoa học, Kỹ thuật & Công nghệ: Khối lượng tham khảo mỗi năm: 96 tín chỉ, thường tương đương 8 môn. Học phí tham khảo mỗi năm: 375.840.000 VND. Nhi

### Top 3

- Score: `0.695671`
- doc_id: `rmit_current_student_scholarship_2026`
- chunk_index: `0`
- source_url: `https://www.rmit.edu.vn/vi/hoc-tap-tai-rmit/hoc-bong/hoc-bong-thanh-tich-hoc-tap-xuat-sac-cho-sinh-vien-hien-dang-hoc-tai-rmit`
- Nội dung: Đối tượng và giá trị Chương trình dành cho sinh viên hiện đang theo học chương trình cử nhân tại RMIT Việt Nam. Trong năm 2026, trường công bố các suất học bổng có giá trị 50% hoặc 25% học phí của phần chương trình cử nhân còn lại. Điều kiện chính Ứng viên phải: Là sinh viên hiện đang họ

**Tài liệu đúng trong top-3:** Có

**Vị trí:** 1, 3

**Câu trả lời trích xuất từ context:** chính Ứng viên phải: Là sinh viên hiện đang học chương trình cử nhân tại RMIT Việt Nam. Đã hoàn tất ít nhất 96 tín chỉ. Có GPA tích lũy từ 3,4/4,0 trở lên. Số lượng và phân bổ học bổng được công bố theo từng khoa và từng học kỳ. Trường bảo lưu quyền thay đổi giá trị hoặc phân bổ khi cần thi

**Similarity giữa câu trả lời trích xuất và gold answer:** `0.697267`

**Điểm:** 2/2

---

**Tổng điểm retrieval tự đánh giá:** 10/10

