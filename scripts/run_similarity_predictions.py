from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src import LocalEmbedder, compute_similarity


# Lab không quy định ngưỡng cao/thấp cụ thể.
# Quy tắc thực nghiệm:
# score >= 0.50 là "cao", score < 0.50 là "thấp".
HIGH_THRESHOLD = 0.50


PAIRS = [
    {
        "id": 1,
        "a": "Sinh viên có thể gia hạn sách trực tuyến.",
        "b": "Người học được phép kéo dài thời gian mượn tài liệu online.",
        "prediction": "cao",
    },
    {
        "id": 2,
        "a": "Sinh viên phải đóng học phí trước ngày 15.",
        "b": "Học phí cần được thanh toán trước thời hạn quy định.",
        "prediction": "cao",
    },
    {
        "id": 3,
        "a": "Thư viện mở cửa từ thứ Hai đến thứ Sáu.",
        "b": "Ký túc xá có khu vực sinh hoạt chung.",
        "prediction": "thấp",
    },
    {
        "id": 4,
        "a": "Sinh viên cần đăng ký môn học trên cổng thông tin.",
        "b": "Người học lựa chọn học phần qua hệ thống trực tuyến.",
        "prediction": "cao",
    },
    {
        "id": 5,
        "a": "Điều kiện nhận học bổng là GPA từ 3.5.",
        "b": "Sinh viên có thể mượn tối đa năm cuốn sách.",
        "prediction": "thấp",
    },
]


def classify(score: float) -> str:
    """Phân loại cosine similarity theo ngưỡng thực nghiệm."""
    return "cao" if score >= HIGH_THRESHOLD else "thấp"


def main() -> None:
    print("Đang tải local multilingual embedding...")
    embedder = LocalEmbedder()

    print(f"Backend: {embedder._backend_name}")
    print(f"Ngưỡng phân loại cao/thấp: {HIGH_THRESHOLD:.2f}")
    print()

    output = [
        "# Kết quả dự đoán độ tương tự",
        "",
        f"- Backend: `{embedder._backend_name}`",
        f"- Quy tắc: score >= {HIGH_THRESHOLD:.2f} là **cao**.",
        "",
        "| Cặp | Dự đoán | Điểm thực tế | Phân loại thực tế | Đúng? |",
        "|---:|---|---:|---|---|",
    ]

    for item in PAIRS:
        vector_a = embedder(item["a"])
        vector_b = embedder(item["b"])

        score = compute_similarity(vector_a, vector_b)
        actual = classify(score)
        correct = "Có" if actual == item["prediction"] else "Không"

        print("=" * 80)
        print(f"Cặp {item['id']}")
        print(f"Câu A: {item['a']}")
        print(f"Câu B: {item['b']}")
        print(f"Dự đoán: {item['prediction']}")
        print(f"Điểm thực tế: {score:.6f}")
        print(f"Phân loại: {actual}")
        print(f"Đúng: {correct}")

        output.append(
            f"| {item['id']} | {item['prediction']} | "
            f"{score:.6f} | {actual} | {correct} |"
        )

    output_path = PROJECT_ROOT / "report" / "similarity_results.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(
        "\n".join(output) + "\n",
        encoding="utf-8",
    )

    print()
    print(f"Đã lưu kết quả tại: {output_path}")


if __name__ == "__main__":
    main()