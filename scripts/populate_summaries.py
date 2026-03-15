import json
from pathlib import Path
from datetime import date

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def build_short_summary(subject: str, chapter_title: str) -> str:
    return f"This chapter introduces the main ideas of {chapter_title} in {subject}."


def build_detailed_summary(subject: str, chapter_title: str, class_num: int) -> str:
    return (
        f"This chapter for Class {class_num} {subject} explains the core concepts of "
        f"{chapter_title}. It is intended as a structured study summary for CBSE learners."
    )


def build_key_concepts(chapter_title: str) -> list[dict]:
    return [
        {
            "title": f"Introduction to {chapter_title}",
            "explanation": f"This concept introduces the basic idea of {chapter_title}."
        },
        {
            "title": f"Core ideas in {chapter_title}",
            "explanation": f"This concept covers the main principles and important points in {chapter_title}."
        },
        {
            "title": f"Applications of {chapter_title}",
            "explanation": f"This concept explains common uses, examples, or relevance of {chapter_title}."
        }
    ]



def update_file(json_path: Path) -> None:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    subject = data.get("subject", "")
    chapter_title = data.get("chapter_title", "")
    class_num = data.get("class", "")

    if "summary" not in data or not isinstance(data["summary"], dict):
        data["summary"] = {
            "short_summary": "",
            "detailed_summary": "",
            "key_concepts": []
        }

    data["summary"]["short_summary"] = build_short_summary(subject, chapter_title)
    data["summary"]["detailed_summary"] = build_detailed_summary(subject, chapter_title, class_num)
    data["summary"]["key_concepts"] = build_key_concepts(chapter_title)

    if "metadata" not in data or not isinstance(data["metadata"], dict):
        data["metadata"] = {}

    data["metadata"]["last_updated"] = str(date.today())

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main() -> None:
    json_files = sorted(DATA_DIR.rglob("*.json"))

    for json_file in json_files:
        update_file(json_file)

    print(f"Updated summaries for {len(json_files)} chapter files.")


if __name__ == "__main__":
    main()
