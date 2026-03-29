# Module 02 — Sàng lọc & Đánh giá CV

Đây là module quan trọng nhất. Thực hiện theo đúng thứ tự dưới đây.

---

## Bước 1 — Thu thập đầu vào

**Bắt buộc phải có trước khi đánh giá:**

- JD (Job Description) của vị trí
- Ít nhất 1 CV ứng viên

**Định dạng CV được hỗ trợ:**

- PDF → đọc trực tiếp từ file đính kèm
- Word (.docx) → đọc trực tiếp từ file đính kèm
- Text dán vào chat → đọc trực tiếp
- Link (TopCV, LinkedIn, v.v.) → yêu cầu người dùng copy-paste nội dung, vì không thể truy cập link trực tiếp

Nếu thiếu JD hoặc CV, hỏi người dùng trước khi tiếp tục.

---

## Bước 2 — Phân tích JD để trích xuất tiêu chí

Từ JD, tự động xác định và phân nhóm tiêu chí:

### Nhóm tiêu chí & trọng số mặc định (tổng = 100 điểm)

| #   | Nhóm                           | Trọng số | Mô tả                                 |
| --- | ------------------------------ | -------- | ------------------------------------- |
| 1   | Kỹ năng kỹ thuật (Hard Skills) | 35đ      | Tech stack, tools, ngôn ngữ lập trình |
| 2   | Kinh nghiệm làm việc           | 25đ      | Số năm, độ phù hợp ngành/domain       |
| 3   | Bằng cấp & chứng chỉ           | 10đ      | Học vấn, certifications liên quan     |
| 4   | Soft Skills & Leadership       | 15đ      | Giao tiếp, teamwork, ownership        |
| 5   | Culture Fit & Motivation       | 10đ      | Định hướng sự nghiệp, stability       |
| 6   | Yếu tố bonus                   | 5đ       | Side projects, OSS, blog, speaker...  |

> Nếu JD nhấn mạnh đặc biệt vào một nhóm nào đó, hãy điều chỉnh trọng số tương ứng và ghi chú lại.

---

## Bước 3 — Chấm điểm từng CV

Với mỗi ứng viên, chấm theo thang điểm sau:

### Thang điểm chi tiết từng nhóm

**Nhóm 1 — Kỹ năng kỹ thuật (35đ)**

- 32-35đ: Đáp ứng 90%+ tech stack bắt buộc, có thêm nice-to-have
- 25-31đ: Đáp ứng 70-89% tech stack bắt buộc
- 15-24đ: Đáp ứng 50-69%, có thể train thêm
- 0-14đ: Dưới 50%, thiếu nhiều kỹ năng cốt lõi

**Nhóm 2 — Kinh nghiệm làm việc (25đ)**

- 22-25đ: Vượt yêu cầu số năm, đúng domain/ngành
- 17-21đ: Đủ số năm, domain gần tương đương
- 10-16đ: Thiếu 1-2 năm hoặc domain khác nhưng transferable
- 0-9đ: Thiếu nhiều, chủ yếu lý thuyết hoặc intern

**Nhóm 3 — Bằng cấp & chứng chỉ (10đ)**

- 9-10đ: Đúng ngành, có certifications liên quan (AWS, GCP, PMP...)
- 6-8đ: Ngành liên quan hoặc tự học có bằng chứng rõ ràng
- 3-5đ: Ngành khác nhưng kinh nghiệm bù đắp
- 0-2đ: Không liên quan, không có chứng chỉ bù

**Nhóm 4 — Soft Skills & Leadership (15đ)**

- 13-15đ: Có bằng chứng rõ ràng (lead team, mentor, trình bày...)
- 9-12đ: Có một số dấu hiệu tốt (collaborate, initiative...)
- 5-8đ: Mô tả chung chung, khó đánh giá
- 0-4đ: Không đề cập hoặc dấu hiệu tiêu cực

**Nhóm 5 — Culture Fit & Motivation (10đ)**

- 9-10đ: Định hướng rõ ràng, phù hợp, ít nhảy việc
- 6-8đ: Ổn định, không có red flag rõ ràng
- 3-5đ: Nhảy việc nhiều hoặc mục tiêu không rõ
- 0-2đ: Red flags (khoảng trống dài không giải thích, nhảy <6 tháng liên tục)

**Nhóm 6 — Yếu tố bonus (5đ)**

- 4-5đ: GitHub active, blog kỹ thuật, speaker, OSS contribution
- 2-3đ: Có side project hoặc một trong các yếu tố trên
- 0-1đ: Không có

---

## Bước 4 — Tạo output đánh giá

### Output cho 1 ứng viên

```
═══════════════════════════════════════════════
📋 ĐÁNH GIÁ ỨNG VIÊN
Tên: [Họ tên]
Vị trí ứng tuyển: [Tên JD]
Ngày đánh giá: [Ngày hôm nay]
═══════════════════════════════════════════════

BẢNG ĐIỂM CHI TIẾT
┌─────────────────────────────┬────────┬────────┐
│ Tiêu chí                    │ Điểm   │ Tối đa │
├─────────────────────────────┼────────┼────────┤
│ Kỹ năng kỹ thuật            │  __    │  35    │
│ Kinh nghiệm làm việc        │  __    │  25    │
│ Bằng cấp & chứng chỉ        │  __    │  10    │
│ Soft Skills & Leadership    │  __    │  15    │
│ Culture Fit & Motivation    │  __    │  10    │
│ Yếu tố bonus                │  __    │   5    │
├─────────────────────────────┼────────┼────────┤
│ TỔNG ĐIỂM                   │  __    │ 100    │
└─────────────────────────────┴────────┴────────┘

KẾT LUẬN: ✅ PASS / ⚠️ MAYBE / ❌ FAIL
(PASS ≥ 70đ | MAYBE 50-69đ | FAIL < 50đ)

ĐIỂM MẠNH
• [Điểm nổi bật 1]
• [Điểm nổi bật 2]

ĐIỂM YẾU / RỦI RO
• [Điểm cần lưu ý 1]
• [Điểm cần lưu ý 2]

CÂU HỎI NÊN HỎI TRONG PHỎNG VẤN
• [Câu hỏi để làm rõ điểm yếu hoặc red flag]
• [Câu hỏi xác nhận điểm mạnh]

KHUYẾN NGHỊ
[1-2 câu tổng kết: có nên mời phỏng vấn không, lý do tóm tắt]
═══════════════════════════════════════════════
```

### Output cho nhiều ứng viên — Bảng xếp hạng

Sau khi đánh giá tất cả, tạo thêm bảng tổng hợp:

```
BẢNG XẾP HẠNG ỨNG VIÊN — [Tên vị trí]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Hạng │ Tên ứng viên   │ Tổng điểm │ Kết luận │ Ghi chú nhanh
─────┼────────────────┼───────────┼──────────┼──────────────
  1  │ [Tên]          │   87/100  │ ✅ PASS  │ Strong tech, lead exp
  2  │ [Tên]          │   74/100  │ ✅ PASS  │ Good fit, needs React
  3  │ [Tên]          │   61/100  │ ⚠️ MAYBE │ Junior nhưng tiềm năng
  4  │ [Tên]          │   43/100  │ ❌ FAIL  │ Thiếu backend experience

KHUYẾN NGHỊ MỜI PHỎNG VẤN: [Liệt kê tên những người PASS]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Lưu ý quan trọng

- **Không phân biệt đối xử** theo giới tính, tuổi tác, quê quán, ngoại hình
- **Chỉ đánh giá dựa trên bằng chứng** có trong CV — không suy diễn
- **Ghi rõ "thiếu thông tin"** thay vì tự đánh giá thấp khi CV không đề cập
- **Red flags cần ghi chú**: nhảy việc <6 tháng liên tục ≥3 lần, khoảng trống >1 năm không giải thích, mô tả công việc mơ hồ ở công ty lớn
- **Với MAYBE**: ghi rõ điều kiện để upgrade lên PASS (vd: "Nếu phỏng vấn confirm kinh nghiệm Node.js thì đủ điều kiện")
