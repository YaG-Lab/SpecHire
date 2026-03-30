#!/usr/bin/env python3
"""
export_results.py — Xuất kết quả đánh giá CV ra CSV / báo cáo

Cách dùng:
    python export_results.py --input results.json
    python export_results.py --input results.json --format csv
    python export_results.py --input results.json --format report

Yêu cầu:
    pip install tabulate  (cho report mode)
"""

import json
import csv
import sys
import argparse
from pathlib import Path
from datetime import datetime


def load_results(input_path: Path) -> list:
    with open(input_path, encoding="utf-8") as f:
        return json.load(f)


def export_csv(results: list, output_path: Path):
    """Xuất bảng xếp hạng ra CSV — mở được bằng Excel/Google Sheets."""
    fieldnames = [
        "Xếp hạng",
        "Tên ứng viên",
        "Kết luận",
        "Hard Skills",
        "Kinh nghiệm",
        "Bằng cấp",
        "Soft Skills",
        "Culture Fit",
        "Bonus",
        "Tổng điểm",
        "Tóm tắt",
    ]

    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for rank, r in enumerate(results, 1):
            scores = r.get("scores", {})
            writer.writerow(
                {
                    "Xếp hạng": rank,
                    "Tên ứng viên": r.get("name", "Unknown"),
                    "Kết luận": r.get("verdict", "?"),
                    "Hard Skills": scores.get("hard_skills", ""),
                    "Kinh nghiệm": scores.get("experience", ""),
                    "Bằng cấp": scores.get("education", ""),
                    "Soft Skills": scores.get("soft_skills", ""),
                    "Culture Fit": scores.get("culture_fit", ""),
                    "Bonus": scores.get("bonus", ""),
                    "Tổng điểm": scores.get("total", ""),
                    "Tóm tắt": r.get("summary", ""),
                }
            )

    print(f"Đã xuất CSV: {output_path}")
    print("Mở bằng Excel hoặc Google Sheets để xem bảng xếp hạng.")


def export_report(results: list, output_path: Path):
    """Xuất báo cáo text đầy đủ với bảng xếp hạng + chi tiết từng ứng viên."""
    lines = []
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")

    lines.append("=" * 64)
    lines.append("BÁO CÁO SÀNG LỌC CV")
    lines.append(f"Ngày xuất: {timestamp} | Tổng ứng viên: {len(results)}")
    lines.append("=" * 64)

    # Thống kê nhanh
    pass_count = sum(1 for r in results if r.get("verdict") == "PASS")
    maybe_count = sum(1 for r in results if r.get("verdict") == "MAYBE")
    fail_count = sum(1 for r in results if r.get("verdict") == "FAIL")

    lines.append(
        f"\nTÓM TẮT: ✅ PASS: {pass_count}  ⚠️ MAYBE: {maybe_count}  ❌ FAIL: {fail_count}"
    )

    # Bảng xếp hạng
    lines.append("\nBẢNG XẾP HẠNG")
    lines.append("-" * 64)
    lines.append(f"{'#':<4} {'Tên':<28} {'Điểm':>6}  {'Kết luận':<8}  Tóm tắt")
    lines.append("-" * 64)

    icons = {"PASS": "✅", "MAYBE": "⚠️", "FAIL": "❌"}
    for rank, r in enumerate(results, 1):
        total = r.get("scores", {}).get("total", "?")
        verdict = r.get("verdict", "?")
        icon = icons.get(verdict, "?")
        name = r.get("name", "Unknown")[:26]
        summary = r.get("summary", "")[:30]
        lines.append(
            f"{rank:<4} {name:<28} {str(total):>6}  {icon} {verdict:<6}  {summary}"
        )

    # Chi tiết từng ứng viên (chỉ PASS và MAYBE)
    lines.append("\n\nCHI TIẾT ỨNG VIÊN ĐƯỢC GỌI PHỎNG VẤN")
    lines.append("=" * 64)

    for r in results:
        if r.get("verdict") not in ("PASS", "MAYBE"):
            continue

        lines.append(f"\n{r.get('name', 'Unknown')} — {r.get('verdict')}")
        lines.append("-" * 40)

        scores = r.get("scores", {})
        lines.append(f"  Hard Skills : {scores.get('hard_skills', '?')}/35")
        lines.append(f"  Kinh nghiệm : {scores.get('experience', '?')}/25")
        lines.append(f"  Bằng cấp    : {scores.get('education', '?')}/10")
        lines.append(f"  Soft Skills : {scores.get('soft_skills', '?')}/15")
        lines.append(f"  Culture Fit : {scores.get('culture_fit', '?')}/10")
        lines.append(f"  Bonus       : {scores.get('bonus', '?')}/5")
        lines.append(f"  TỔNG        : {scores.get('total', '?')}/100")
        lines.append(f"\n  {r.get('summary', '')}")

        # Nếu có raw text, thêm phần đánh giá chi tiết
        raw = r.get("raw", "")
        if raw and len(raw) > 100:
            lines.append("\n  [Đánh giá đầy đủ]")
            for line in raw.split("\n")[:30]:  # Tối đa 30 dòng đầu
                lines.append(f"  {line}")

    lines.append("\n" + "=" * 64)
    lines.append("Hết báo cáo")

    report_text = "\n".join(lines)
    output_path.write_text(report_text, encoding="utf-8")
    print(f"Đã xuất báo cáo: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Xuất kết quả đánh giá CV")
    parser.add_argument(
        "--input", required=True, help="File results.json từ batch_screen.py"
    )
    parser.add_argument("--format", choices=["csv", "report", "both"], default="both")
    parser.add_argument("--output", help="Tên file output (không cần extension)")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Lỗi: Không tìm thấy file: {input_path}")
        sys.exit(1)

    results = load_results(input_path)
    print(f"Đã tải {len(results)} kết quả từ {input_path.name}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = args.output or f"screening_{timestamp}"

    if args.format in ("csv", "both"):
        export_csv(results, Path(f"{base_name}.csv"))

    if args.format in ("report", "both"):
        export_report(results, Path(f"{base_name}_report.txt"))


if __name__ == "__main__":
    main()
