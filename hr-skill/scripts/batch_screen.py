#!/usr/bin/env python3
"""
batch_screen.py — Sàng lọc hàng loạt CV qua Anthropic API

Cách dùng:
    python batch_screen.py --jd jd.txt --cv-dir ./cvs/ --output results.json

Yêu cầu:
    pip install anthropic pdfplumber python-docx

Biến môi trường:
    ANTHROPIC_API_KEY=sk-ant-...
"""

import os
import sys
import json
import argparse
import time
from pathlib import Path

try:
    import anthropic
    import pdfplumber
    from docx import Document
except ImportError:
    print("Thiếu thư viện. Chạy: pip install anthropic pdfplumber python-docx")
    sys.exit(1)

SKILL_DIR = Path(__file__).parent.parent
SKILL_MD = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
MODULE_02 = (SKILL_DIR / "references" / "02-cv-screening.md").read_text(
    encoding="utf-8"
)
SYSTEM_PROMPT = f"{SKILL_MD}\n\n{MODULE_02}"


def extract_text(filepath: Path) -> str:
    """Trích xuất text từ PDF, DOCX, hoặc TXT."""
    suffix = filepath.suffix.lower()

    if suffix == ".pdf":
        with pdfplumber.open(filepath) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)

    elif suffix in (".docx", ".doc"):
        doc = Document(filepath)
        return "\n".join(p.text for p in doc.paragraphs)

    elif suffix == ".txt":
        return filepath.read_text(encoding="utf-8")

    else:
        print(f"  [!] Bỏ qua file không hỗ trợ: {filepath.name}")
        return ""


def screen_cv(
    client: anthropic.Anthropic, jd_text: str, cv_text: str, cv_name: str
) -> dict:
    """Gọi API đánh giá 1 CV, trả về dict kết quả."""
    prompt = f"""JD:
{jd_text}

CV ứng viên ({cv_name}):
{cv_text}

Đánh giá CV này theo đúng format Module 02. 
Sau phần đánh giá text, hãy thêm một block JSON như sau (để dễ parse):

```json
{{
  "name": "Tên ứng viên",
  "scores": {{
    "hard_skills": 0,
    "experience": 0,
    "education": 0,
    "soft_skills": 0,
    "culture_fit": 0,
    "bonus": 0,
    "total": 0
  }},
  "verdict": "PASS|MAYBE|FAIL",
  "summary": "1 câu tóm tắt lý do"
}}
```"""

    msg = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )

    full_text = msg.content[0].text

    # Parse JSON block nếu có
    result = {
        "name": cv_name,
        "raw": full_text,
        "scores": {},
        "verdict": "UNKNOWN",
        "summary": "",
    }
    try:
        import re

        json_match = re.search(r"```json\s*(\{.*?\})\s*```", full_text, re.DOTALL)
        if json_match:
            parsed = json.loads(json_match.group(1))
            result.update(parsed)
    except Exception:
        pass  # Giữ raw text nếu parse lỗi

    return result


def main():
    parser = argparse.ArgumentParser(description="Batch CV Screening với HR Skill")
    parser.add_argument("--jd", required=True, help="File JD (.txt/.pdf/.docx)")
    parser.add_argument("--cv-dir", required=True, help="Thư mục chứa các file CV")
    parser.add_argument("--output", default="results.json", help="File output JSON")
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Giây chờ giữa mỗi CV (tránh rate limit)",
    )
    args = parser.parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Lỗi: Chưa set ANTHROPIC_API_KEY")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    # Đọc JD
    jd_path = Path(args.jd)
    if not jd_path.exists():
        print(f"Lỗi: Không tìm thấy file JD: {jd_path}")
        sys.exit(1)
    jd_text = extract_text(jd_path)
    print(f"JD: {jd_path.name} ({len(jd_text)} ký tự)")

    # Tìm tất cả CV
    cv_dir = Path(args.cv_dir)
    cv_files = sorted(
        [
            f
            for f in cv_dir.iterdir()
            if f.suffix.lower() in (".pdf", ".docx", ".doc", ".txt")
        ]
    )
    print(f"Tìm thấy {len(cv_files)} CV\n")

    results = []
    for i, cv_path in enumerate(cv_files, 1):
        print(f"[{i}/{len(cv_files)}] Đang đánh giá: {cv_path.name}")
        cv_text = extract_text(cv_path)
        if not cv_text.strip():
            print("  [!] Bỏ qua — không đọc được nội dung")
            continue

        result = screen_cv(client, jd_text, cv_text, cv_path.stem)
        results.append(result)

        verdict = result.get("verdict", "?")
        total = result.get("scores", {}).get("total", "?")
        print(f"  → {verdict} | {total}/100 | {result.get('summary', '')}")

        if i < len(cv_files):
            time.sleep(args.delay)

    # Sắp xếp theo tổng điểm giảm dần
    results.sort(key=lambda r: r.get("scores", {}).get("total", 0), reverse=True)

    # Lưu kết quả
    output_path = Path(args.output)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # In bảng xếp hạng
    print(f"\n{'='*60}")
    print(f"BẢNG XẾP HẠNG — {len(results)} ứng viên")
    print(f"{'='*60}")
    for rank, r in enumerate(results, 1):
        total = r.get("scores", {}).get("total", "?")
        verdict = r.get("verdict", "?")
        name = r.get("name", "Unknown")
        icon = "✅" if verdict == "PASS" else "⚠️" if verdict == "MAYBE" else "❌"
        print(f"  {rank}. {icon} {name:<30} {total}/100")

    print(f"\nKết quả đầy đủ đã lưu tại: {output_path}")


if __name__ == "__main__":
    main()
