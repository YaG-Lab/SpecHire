#!/usr/bin/env python3
"""
generate_jd.py — Soạn JD tự động từ thông tin đầu vào

Cách dùng:
    python generate_jd.py                    # Chế độ tương tác (hỏi từng bước)
    python generate_jd.py --input info.json  # Từ file JSON có sẵn
    python generate_jd.py --review jd.txt    # Review & cải thiện JD cũ

Yêu cầu:
    pip install anthropic
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

try:
    import anthropic
except ImportError:
    print("Thiếu thư viện. Chạy: pip install anthropic")
    sys.exit(1)

SKILL_DIR = Path(__file__).parent.parent
SKILL_MD = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
MODULE_01 = (SKILL_DIR / "references" / "01-jd-writer.md").read_text(encoding="utf-8")
SYSTEM_PROMPT = f"{SKILL_MD}\n\n{MODULE_01}"


def ask(question: str, default: str = "") -> str:
    """Hỏi người dùng, trả về input hoặc default nếu bỏ trống."""
    hint = f" [{default}]" if default else ""
    answer = input(f"{question}{hint}: ").strip()
    return answer if answer else default


def collect_info_interactive() -> dict:
    """Thu thập thông tin JD qua giao diện dòng lệnh."""
    print("\n=== Soạn JD — HR Skill ===\n")

    info = {
        "position": ask("Tên vị trí (VD: Senior Backend Engineer)"),
        "level": ask("Level", "Mid"),
        "company": ask("Tên công ty"),
        "team": ask("Team/phòng ban"),
        "report_to": ask("Báo cáo cho ai (VD: Engineering Manager)"),
        "work_type": ask("Hình thức làm việc (onsite/hybrid/remote)", "hybrid"),
        "location": ask("Địa điểm", "TP. Hồ Chí Minh"),
        "salary": ask("Mức lương (bỏ trống nếu không muốn công khai)", ""),
        "years_exp": ask("Số năm kinh nghiệm tối thiểu", "2"),
        "must_have": ask("Kỹ năng bắt buộc (cách nhau bằng dấu phẩy)"),
        "nice_have": ask("Kỹ năng là lợi thế (có thể bỏ trống)", ""),
        "main_tasks": ask("Mô tả 3-5 nhiệm vụ chính (cách nhau bằng dấu |)"),
        "benefits": ask("Quyền lợi nổi bật (cách nhau bằng dấu phẩy)", ""),
        "email": ask("Email nhận CV"),
    }
    return info


def generate_jd(client: anthropic.Anthropic, info: dict) -> str:
    """Gọi API tạo JD từ thông tin đầu vào."""
    prompt = f"""Soạn JD theo Module 01 với thông tin sau:

Vị trí: {info.get('position')} — {info.get('level')}
Công ty: {info.get('company')}
Team: {info.get('team')} | Báo cáo cho: {info.get('report_to')}
Hình thức: {info.get('work_type')} | Địa điểm: {info.get('location')}
Lương: {info.get('salary') or 'Không công khai'}
Kinh nghiệm tối thiểu: {info.get('years_exp')} năm

Kỹ năng bắt buộc: {info.get('must_have')}
Kỹ năng lợi thế: {info.get('nice_have') or 'Không có'}

Nhiệm vụ chính:
{chr(10).join('- ' + t.strip() for t in info.get('main_tasks', '').split('|') if t.strip())}

Quyền lợi: {info.get('benefits') or 'Tiêu chuẩn ngành'}
Email nhận CV: {info.get('email')}

Viết JD đầy đủ, rõ ràng, hấp dẫn. Không quá 600 từ."""

    msg = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text


def review_jd(client: anthropic.Anthropic, jd_text: str) -> str:
    """Review và cải thiện JD có sẵn."""
    prompt = f"""Review và cải thiện JD sau theo Chế độ A của Module 01.
Hiển thị đánh giá JD gốc trước, sau đó viết lại JD đã cải thiện:

JD gốc:
{jd_text}"""

    msg = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text


def save_output(content: str, prefix: str = "jd") -> Path:
    """Lưu kết quả ra file .txt với timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(f"{prefix}_{timestamp}.txt")
    output_path.write_text(content, encoding="utf-8")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Soạn / Review JD với HR Skill")
    parser.add_argument("--input", help="File JSON chứa thông tin JD")
    parser.add_argument("--review", help="File JD cũ cần review & cải thiện")
    parser.add_argument("--output", help="File output (mặc định: jd_<timestamp>.txt)")
    args = parser.parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Lỗi: Chưa set ANTHROPIC_API_KEY")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    if args.review:
        # Chế độ review JD cũ
        jd_path = Path(args.review)
        if not jd_path.exists():
            print(f"Lỗi: Không tìm thấy file: {jd_path}")
            sys.exit(1)
        print(f"Đang review JD: {jd_path.name}")
        jd_text = jd_path.read_text(encoding="utf-8")
        result = review_jd(client, jd_text)
        prefix = "jd_reviewed"

    elif args.input:
        # Chế độ từ file JSON
        info_path = Path(args.input)
        if not info_path.exists():
            print(f"Lỗi: Không tìm thấy file: {info_path}")
            sys.exit(1)
        with open(info_path, encoding="utf-8") as f:
            info = json.load(f)
        print(f"Đang tạo JD từ: {info_path.name}")
        result = generate_jd(client, info)
        prefix = "jd_generated"

    else:
        # Chế độ tương tác
        info = collect_info_interactive()
        print("\nĐang soạn JD...")
        result = generate_jd(client, info)
        prefix = "jd_generated"

    # In kết quả
    print("\n" + "=" * 60)
    print(result)
    print("=" * 60)

    # Lưu file
    output_path = Path(args.output) if args.output else save_output(result, prefix)
    output_path.write_text(result, encoding="utf-8")
    print(f"\nĐã lưu tại: {output_path}")


if __name__ == "__main__":
    main()
