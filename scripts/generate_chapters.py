import json
import re
from pathlib import Path
from datetime import date

import yaml


BASE_DIR = Path(__file__).resolve().parent.parent
INVENTORY_PATH = BASE_DIR / "inventory" / "syllabus_inventory.yaml"
DATA_DIR = BASE_DIR / "data"


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = text.replace("&", "and")
    text = re.sub(r"[—–-]+", " ", text)
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", "_", text)
    return text


def build_chapter_payload(
    class_num: int,
    stream: str | None,
    subject: str,
    textbook: str,
    chapter_number: int,
    chapter_title: str,
) -> dict:
    chapter_slug = slugify(chapter_title)
    subject_slug = slugify(subject)

    if stream:
        chapter_id = f"cbse-{class_num}-{stream}-{subject_slug}-{chapter_slug}"
    else:
        chapter_id = f"cbse-{class_num}-{subject_slug}-{chapter_slug}"

    return {
        "id": chapter_id,
        "curriculum": "CBSE",
        "class": class_num,
        "stream": stream,
        "subject": subject_slug,
        "chapter_number": chapter_number,
        "chapter_title": chapter_title,
        "language": "en",
        "book": textbook,
        "version": "1.0",
        "summary": {
            "short_summary": "",
            "detailed_summary": "",
            "key_concepts": []
        },
        "practice_questions": [],
        "mcqs": [],
        "metadata": {
            "status": "draft",
            "reviewed": False,
            "tags": [],
            "source": "NCERT-based",
            "last_updated": str(date.today())
        }
    }


def write_chapter_file(output_dir: Path, chapter_number: int, chapter_title: str, payload: dict) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"chapter_{chapter_number:02d}_{slugify(chapter_title)}.json"
    output_path = output_dir / filename

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def process_subject(class_num: int, stream: str | None, subject_name: str, subject_data: dict, output_dir: Path) -> None:
    textbook = subject_data.get("textbook", "")
    chapters = subject_data.get("chapters")

    if chapters:
        for idx, chapter_title in enumerate(chapters, start=1):
            payload = build_chapter_payload(
                class_num=class_num,
                stream=stream,
                subject=subject_name,
                textbook=textbook,
                chapter_number=idx,
                chapter_title=chapter_title,
            )
            write_chapter_file(output_dir, idx, chapter_title, payload)
        return

    books = subject_data.get("books", {})
    if books:
        chapter_counter = 1
        for _, book_data in books.items():
            for chapter_title in book_data.get("chapters", []):
                payload = build_chapter_payload(
                    class_num=class_num,
                    stream=stream,
                    subject=subject_name,
                    textbook=textbook,
                    chapter_number=chapter_counter,
                    chapter_title=chapter_title,
                )
                write_chapter_file(output_dir, chapter_counter, chapter_title, payload)
                chapter_counter += 1


def main() -> None:
    if not INVENTORY_PATH.exists():
        raise FileNotFoundError(f"Inventory file not found: {INVENTORY_PATH}")

    with open(INVENTORY_PATH, "r", encoding="utf-8") as f:
        inventory = yaml.safe_load(f)

    classes = inventory.get("classes", {})

    for class_key, class_data in classes.items():
        class_num = int(class_key)
        class_dir = DATA_DIR / f"class_{class_num}"

        if "subjects" in class_data:
            for subject_name, subject_data in class_data["subjects"].items():
                subject_dir = class_dir / slugify(subject_name)
                process_subject(class_num, None, subject_name, subject_data, subject_dir)

        elif "streams" in class_data:
            for stream_name, stream_data in class_data["streams"].items():
                for subject_name, subject_data in stream_data.get("subjects", {}).items():
                    subject_dir = class_dir / slugify(stream_name) / slugify(subject_name)
                    process_subject(class_num, stream_name, subject_name, subject_data, subject_dir)

    print("Chapter JSON files generated successfully.")


if __name__ == "__main__":
    main()
