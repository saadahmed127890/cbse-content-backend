from fastapi import FastAPI, HTTPException
from pathlib import Path
import json

app = FastAPI(title="CBSE Content API", version="1.0")

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def load_json_file(file_path: Path):
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Content not found")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON file")


def get_class_dir(class_num: int) -> Path:
    class_dir = DATA_DIR / f"class_{class_num}"
    if not class_dir.exists():
        raise HTTPException(status_code=404, detail="Class not found")
    return class_dir


def list_available_classes():
    if not DATA_DIR.exists():
        return []

    classes = []
    for item in DATA_DIR.iterdir():
        if item.is_dir() and item.name.startswith("class_"):
            try:
                classes.append(int(item.name.replace("class_", "")))
            except ValueError:
                continue
    return sorted(classes)


def list_subjects_for_class(class_num: int):
    class_dir = get_class_dir(class_num)

    subjects = []
    for item in class_dir.iterdir():
        if item.is_dir() and not item.name.startswith("stream_"):
            subjects.append(item.name)

    return sorted(subjects)


def list_streams_for_class(class_num: int):
    class_dir = get_class_dir(class_num)

    streams = []
    for item in class_dir.iterdir():
        if item.is_dir():
            streams.append(item.name)

    return sorted(streams)



def list_subjects_for_stream(class_num: int, stream: str):
    stream_dir = get_class_dir(class_num) / stream
    if not stream_dir.exists():
        raise HTTPException(status_code=404, detail="Stream not found")

    subjects = [item.name for item in stream_dir.iterdir() if item.is_dir()]
    return sorted(subjects)



def get_chapter_file_no_stream(class_num: int, subject: str, chapter_slug: str) -> Path:
    return get_class_dir(class_num) / subject / f"{chapter_slug}.json"


def get_chapter_file_with_stream(class_num: int, stream: str, subject: str, chapter_slug: str) -> Path:
    return get_class_dir(class_num) / stream / subject / f"{chapter_slug}.json"

@app.get("/health")
def health_check():
    total_files = len(list(DATA_DIR.rglob("*.json")))
    return {
        "status": "ok",
        "total_chapter_files": total_files
    }



@app.get("/")
def root():
    return {"message": "CBSE Content API is running"}


@app.get("/classes")
def get_classes():
    return {"classes": list_available_classes()}


@app.get("/classes/{class_num}/subjects")
def get_subjects(class_num: int):
    return {
        "class": class_num,
        "subjects": list_subjects_for_class(class_num)
    }


@app.get("/classes/{class_num}/streams")
def get_streams(class_num: int):
    return {
        "class": class_num,
        "streams": list_streams_for_class(class_num)
    }


@app.get("/classes/{class_num}/streams/{stream}/subjects")
def get_stream_subjects(class_num: int, stream: str):
    return {
        "class": class_num,
        "stream": stream,
        "subjects": list_subjects_for_stream(class_num, stream)
    }


@app.get("/content/{class_num}/{subject}/{chapter_slug}")
def get_full_content_no_stream(class_num: int, subject: str, chapter_slug: str):
    file_path = get_chapter_file_no_stream(class_num, subject, chapter_slug)
    return load_json_file(file_path)


@app.get("/content/{class_num}/{subject}/{chapter_slug}/summary")
def get_summary_no_stream(class_num: int, subject: str, chapter_slug: str):
    file_path = get_chapter_file_no_stream(class_num, subject, chapter_slug)
    content = load_json_file(file_path)
    return {
        "id": content["id"],
        "class": content["class"],
        "stream": content["stream"],
        "subject": content["subject"],
        "chapter_number": content["chapter_number"],
        "chapter_title": content["chapter_title"],
        "summary": content["summary"]
    }


@app.get("/content/{class_num}/{subject}/{chapter_slug}/questions")
def get_questions_no_stream(class_num: int, subject: str, chapter_slug: str):
    file_path = get_chapter_file_no_stream(class_num, subject, chapter_slug)
    content = load_json_file(file_path)
    return {
        "id": content["id"],
        "class": content["class"],
        "stream": content["stream"],
        "subject": content["subject"],
        "chapter_number": content["chapter_number"],
        "chapter_title": content["chapter_title"],
        "practice_questions": content["practice_questions"]
    }


@app.get("/content/{class_num}/{subject}/{chapter_slug}/mcqs")
def get_mcqs_no_stream(class_num: int, subject: str, chapter_slug: str):
    file_path = get_chapter_file_no_stream(class_num, subject, chapter_slug)
    content = load_json_file(file_path)
    return {
        "id": content["id"],
        "class": content["class"],
        "stream": content["stream"],
        "subject": content["subject"],
        "chapter_number": content["chapter_number"],
        "chapter_title": content["chapter_title"],
        "mcqs": content["mcqs"]
    }


@app.get("/content/{class_num}/{stream}/{subject}/{chapter_slug}")
def get_full_content_with_stream(class_num: int, stream: str, subject: str, chapter_slug: str):
    file_path = get_chapter_file_with_stream(class_num, stream, subject, chapter_slug)
    return load_json_file(file_path)


@app.get("/content/{class_num}/{stream}/{subject}/{chapter_slug}/summary")
def get_summary_with_stream(class_num: int, stream: str, subject: str, chapter_slug: str):
    file_path = get_chapter_file_with_stream(class_num, stream, subject, chapter_slug)
    content = load_json_file(file_path)
    return {
        "id": content["id"],
        "class": content["class"],
        "stream": content["stream"],
        "subject": content["subject"],
        "chapter_number": content["chapter_number"],
        "chapter_title": content["chapter_title"],
        "summary": content["summary"]
    }


@app.get("/content/{class_num}/{stream}/{subject}/{chapter_slug}/questions")
def get_questions_with_stream(class_num: int, stream: str, subject: str, chapter_slug: str):
    file_path = get_chapter_file_with_stream(class_num, stream, subject, chapter_slug)
    content = load_json_file(file_path)
    return {
        "id": content["id"],
        "class": content["class"],
        "stream": content["stream"],
        "subject": content["subject"],
        "chapter_number": content["chapter_number"],
        "chapter_title": content["chapter_title"],
        "practice_questions": content["practice_questions"]
    }


@app.get("/content/{class_num}/{stream}/{subject}/{chapter_slug}/mcqs")
def get_mcqs_with_stream(class_num: int, stream: str, subject: str, chapter_slug: str):
    file_path = get_chapter_file_with_stream(class_num, stream, subject, chapter_slug)
    content = load_json_file(file_path)
    return {
        "id": content["id"],
        "class": content["class"],
        "stream": content["stream"],
        "subject": content["subject"],
        "chapter_number": content["chapter_number"],
        "chapter_title": content["chapter_title"],
        "mcqs": content["mcqs"]
    }


@app.get("/classes/{class_num}/{subject}/chapters")
def list_chapters_no_stream(class_num: int, subject: str):
    subject_dir = get_class_dir(class_num) / subject

    if not subject_dir.exists():
        raise HTTPException(status_code=404, detail="Subject not found")

    chapters = []

    for file in sorted(subject_dir.glob("*.json")):
        data = load_json_file(file)

        chapters.append({
            "chapter_number": data["chapter_number"],
            "chapter_slug": file.stem,
            "chapter_title": data["chapter_title"]
        })

    return {
        "class": class_num,
        "subject": subject,
        "chapters": chapters
    }


@app.get("/classes/{class_num}/{stream}/{subject}/chapters")
def list_chapters_with_stream(class_num: int, stream: str, subject: str):
    subject_dir = get_class_dir(class_num) / stream / subject


    if not subject_dir.exists():
        raise HTTPException(status_code=404, detail="Subject not found")

    chapters = []

    for file in sorted(subject_dir.glob("*.json")):
        data = load_json_file(file)

        chapters.append({
            "chapter_number": data["chapter_number"],
            "chapter_slug": file.stem,
            "chapter_title": data["chapter_title"]
        })

    return {
        "class": class_num,
        "stream": stream,
        "subject": subject,
        "chapters": chapters
    }

@app.get("/search")
def search_content(q: str):
    results = []

    for file in DATA_DIR.rglob("*.json"):
        data = load_json_file(file)

        title = data.get("chapter_title", "").lower()

        if q.lower() in title:
            parts = file.parts

            class_num = parts[-4].replace("class_", "")
            subject = parts[-2]
            chapter_slug = file.stem

            results.append({
                "class": class_num,
                "subject": subject,
                "chapter_slug": chapter_slug,
                "chapter_title": data.get("chapter_title")
            })

    return {
        "query": q,
        "results": results
    }
