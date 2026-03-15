# CBSE Content Backend

A structured **CBSE educational dataset and FastAPI backend** designed for an AI-powered learning platform.

This project provides a validated **chapter-level academic dataset** and a **read-only API** for serving structured study material such as summaries, practice questions, and MCQs. The backend reads structured JSON files and dynamically delivers the content through API endpoints.

The system is designed to support learning applications, revision platforms, question practice systems, and future AI-powered educational tools.

---

# Project Goal

The goal of this project is to build a **complete backend content foundation for a CBSE learning platform**.

The system automatically delivers educational content based on:

- class
- subject
- stream
- chapter

The backend reads structured JSON chapter files and serves the data dynamically through API endpoints.

This architecture allows the platform to support:

- revision tools
- study platforms
- MCQ practice systems
- question banks
- AI tutoring tools
- smart content retrieval
- automated content generation pipelines

---

# Dataset Scope

The dataset follows the **CBSE / NCERT syllabus structure**.

## Included Classes

6
7
8
10
11
12




## Excluded Class

9




## Subject Coverage

### Classes 6–8 and 10

All relevant **core CBSE subjects** are included.

### Classes 11–12

All major streams are supported:

Science
Commerce
Humanities

c

Each stream contains its respective subjects.

---

# Dataset Structure

Each chapter is stored as a **structured JSON file** containing:

- chapter metadata
- summaries
- key concepts
- practice questions
- MCQs

Example JSON structure:

```json
{
  "id": "cbse-6-mathematics-patterns_in_mathematics",
  "curriculum": "CBSE",
  "class": 6,
  "stream": null,
  "subject": "mathematics",
  "chapter_number": 1,
  "chapter_title": "Patterns in Mathematics",
  "language": "en",
  "book": "Ganita Prakash (Grade 6)",
  "version": "1.0",
  "summary": {
    "short_summary": "...",
    "detailed_summary": "...",
    "key_concepts": [
      {
        "title": "...",
        "explanation": "..."
      }
    ]
  },
  "practice_questions": [],
  "mcqs": [],
  "metadata": {}
}
All JSON files strictly follow the schema defined in:



schema/chapter.schema.json
Architecture Overview
The project follows a data-first backend architecture.



Syllabus Inventory
        ↓
JSON Schema
        ↓
Chapter File Generation
        ↓
Content Population
        ↓
JSON Validation
        ↓
FastAPI Backend
        ↓
API Content Delivery
This approach ensures:

consistent data structure

schema validation

scalable dataset generation

reliable backend content delivery

Project Structure


cbse_content/
│
├── app.py
├── README.md
├── requirements.txt
│
├── data/
│   └── class_x/... (chapter JSON files)
│
├── inventory/
│   └── syllabus_inventory.yaml
│
├── schema/
│   └── chapter.schema.json
│
├── scripts/
│   ├── generate_chapters.py
│   ├── validate_json.py
│   ├── populate_summaries.py
│   ├── populate_questions.py
│   └── populate_mcqs.py
│
└── venv/
Setup Instructions
Always run commands from the project root.

Activate the project environment:



cd ~/Downloads/cbse_content
source venv/bin/activate
Install dependencies:



pip install -r requirements.txt
JSON Validation
To validate all chapter files against the schema:



python3 scripts/validate_json.py
Output:



All JSON files are valid.
Content Population Scripts
These scripts populate structured content into the generated chapter files.

Populate summaries:



python3 scripts/populate_summaries.py
python3 scripts/validate_json.py
Populate practice questions:



python3 scripts/populate_questions.py
python3 scripts/validate_json.py
Populate MCQs:



python3 scripts/populate_mcqs.py
python3 scripts/validate_json.py
Running the Backend
Start the FastAPI server:



uvicorn app:app --reload
Server runs at:

cpp

http://127.0.0.1:8000
Interactive API documentation:

arduino

http://127.0.0.1:8000/docs
API Endpoints
General
sql

/
health
docs
search?q=...
classes
Class Discovery
Get subjects for a class:



/classes/{class_num}/subjects
Get streams (Class 11–12):



/classes/{class_num}/streams
Get subjects in a stream:



/classes/{class_num}/streams/{stream}/subjects
Chapter Discovery
Non-stream classes:



/classes/{class_num}/{subject}/chapters
Stream classes:



/classes/{class_num}/{stream}/{subject}/chapters
Content Retrieval
Get full chapter content:



/content/{class_num}/{subject}/{chapter_slug}
Get summary:



/content/{class_num}/{subject}/{chapter_slug}/summary
Get practice questions:



/content/{class_num}/{subject}/{chapter_slug}/questions
Get MCQs:



/content/{class_num}/{subject}/{chapter_slug}/mcqs
Stream Content Retrieval


/content/{class_num}/{stream}/{subject}/{chapter_slug}
Example:



/content/11/science/physics/chapter_01_units_and_measurements
Dataset Status
Current dataset statistics:



247 chapter JSON files generated
Summaries populated
Practice questions populated
MCQs populated
All JSON files validated
The dataset is schema-compliant and ready for programmatic use.

Design Principles
This project follows several important backend engineering principles:

inventory is the source of truth

schema defines the contract

dataset validation is mandatory

backend reads validated data only

APIs are read-only for safety

scripts are idempotent and repeatable

Project Deliverables
This project provides the following deliverables:

Structured JSON dataset for all included CBSE classes and chapters

JSON schema defining the chapter content structure

Master syllabus inventory for classes, subjects, and chapters

FastAPI backend serving summaries, questions, and MCQs

JSON validation system to ensure schema consistency

Documentation explaining project structure, workflow, and API usage