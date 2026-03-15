import json
from pathlib import Path
from datetime import date

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def build_mcqs(class_num: int, subject: str, chapter_title: str, chapter_id: str) -> list[dict]:
    base_id = chapter_id.replace("cbse-", "").replace("-", "_")

    return [
        {
            "mcq_id": f"{base_id}_mcq_001",
            "difficulty": "easy",
            "question": f"What is the main focus of the chapter '{chapter_title}'?",
            "options": {
                "A": f"Understanding the core concepts of {chapter_title}",
                "B": "Learning only historical facts",
                "C": "Ignoring practical applications",
                "D": "Memorizing unrelated topics"
            },
            "correct_answer": "A",
            "explanation": f"The chapter '{chapter_title}' mainly focuses on understanding its core concepts in {subject} for Class {class_num}."
        },
        {
            "mcq_id": f"{base_id}_mcq_002",
            "difficulty": "medium",
            "question": f"Which of the following best describes a useful way to study '{chapter_title}'?",
            "options": {
                "A": "Avoiding all examples",
                "B": "Reviewing concepts and practicing questions",
                "C": "Skipping the summary section",
                "D": "Reading unrelated chapters only"
            },
            "correct_answer": "B",
            "explanation": f"A useful way to study '{chapter_title}' is by reviewing the concepts carefully and practicing relevant questions."
        },
        {
            "mcq_id": f"{base_id}_mcq_003",
            "difficulty": "hard",
            "question": f"Why is '{chapter_title}' important in the study of {subject}?",
            "options": {
                "A": "Because it replaces all other chapters",
                "B": "Because it has no connection to the subject",
                "C": f"Because it builds understanding of important ideas within {subject}",
                "D": "Because it is only useful for memorization"
            },
            "correct_answer": "C",
            "explanation": f"'{chapter_title}' is important because it helps build understanding of major ideas and their relevance within {subject}."
        }
    ]


def update_file(json_path: Path) -> None:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    class_num = data.get("class", "")
    subject = data.get("subject", "")
    chapter_title = data.get("chapter_title", "")
    chapter_id = data.get("id", json_path.stem)

    data["mcqs"] = build_mcqs(
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

    print(f"Updated MCQs for {len(json_files)} chapter files.")


if __name__ == "__main__":
    main()
