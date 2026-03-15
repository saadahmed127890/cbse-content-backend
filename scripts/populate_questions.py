import json
from pathlib import Path
from datetime import date

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def build_practice_questions(class_num: int, subject: str, chapter_title: str, chapter_id: str) -> list[dict]:
    base_id = chapter_id.replace("cbse-", "").replace("-", "_")

    return [
        {
            "question_id": f"{base_id}_pq_001",
            "type": "very_short_answer",
            "difficulty": "easy",
            "question": f"What is the main idea introduced in the chapter '{chapter_title}'?",
            "answer": f"The chapter '{chapter_title}' introduces foundational concepts in {subject} for Class {class_num}."
        },
        {
            "question_id": f"{base_id}_pq_002",
            "type": "short_answer",
            "difficulty": "medium",
            "question": f"Explain one important concept from the chapter '{chapter_title}'.",
            "answer": f"One important concept from '{chapter_title}' is understanding its core ideas and how they apply within {subject}."
        },
        {
            "question_id": f"{base_id}_pq_003",
            "type": "application_based",
            "difficulty": "hard",
            "question": f"How can the ideas from '{chapter_title}' be applied in a practical learning context?",
            "answer": f"The ideas from '{chapter_title}' can be applied by solving examples, analyzing situations, and connecting concepts to real learning problems in {subject}."
        }
    ]


def update_file(json_path: Path) -> None:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    class_num = data.get("class", "")
    subject = data.get("subject", "")
    chapter_title = data.get("chapter_title", "")
    chapter_id = data.get("id", json_path.stem)

    data["practice_questions"] = build_practice_questions(
        class_num=class_num,
        subject=subject,
        chapter_title=chapter_title,
        chapter_id=chapter_id
    )

    if "metadata" not in data or not isinstance(data["metadata"], dict):
        data["metadata"] = {}

    data["metadata"]["last_updated"] = str(date.today())

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main() -> None:
    json_files = sorted(DATA_DIR.rglob("*.json"))

    for json_file in json_files:
        update_file(json_file)

    print(f"Updated practice questions for {len(json_files)} chapter files.")


if __name__ == "__main__":
    main()
