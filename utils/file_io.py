import json
from pathlib import Path

# Central output directory
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


def read_text_file(filename: str) -> str:
    path = OUTPUT_DIR / filename
    return path.read_text(encoding="utf-8")


def write_text_file(filename: str, content: str) -> None:
    path = OUTPUT_DIR / filename
    path.write_text(content, encoding="utf-8")


def read_json_file(filename: str) -> dict:
    path = OUTPUT_DIR / filename
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json_file(filename: str, data: dict | list) -> None:
    path = OUTPUT_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
