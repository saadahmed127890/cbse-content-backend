import json
from pathlib import Path

from jsonschema import Draft202012Validator


BASE_DIR = Path(__file__).resolve().parent.parent
SCHEMA_PATH = BASE_DIR / "schema" / "chapter.schema.json"
DATA_DIR = BASE_DIR / "data"


def load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    schema = load_json(SCHEMA_PATH)
    validator = Draft202012Validator(schema)

    json_files = list(DATA_DIR.rglob("*.json"))
    if not json_files:
        print("No JSON files found in data directory.")
        return

    error_count = 0

    for json_file in json_files:
        data = load_json(json_file)
        errors = sorted(validator.iter_errors(data), key=lambda e: e.path)

        if errors:
            error_count += 1
            print(f"\nValidation failed: {json_file}")
            for error in errors:
                path = " -> ".join(str(x) for x in error.path)
                print(f"  - {path if path else 'root'}: {error.message}")

    if error_count == 0:
        print("All JSON files are valid.")
    else:
        print(f"\nValidation completed with {error_count} invalid file(s).")


if __name__ == "__main__":
    main()
