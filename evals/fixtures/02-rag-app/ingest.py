#!/usr/bin/env python3
"""Build index.json: one embedding per 400-character chunk of every handbook file."""
import json
from pathlib import Path

DOCS = Path(__file__).parent / "docs"
INDEX = Path(__file__).parent / "index.json"
CHUNK_CHARS = 400


def chunk(text: str, size: int = CHUNK_CHARS) -> list[str]:
    return [text[start:start + size] for start in range(0, len(text), size)]


def embed(texts: list[str]) -> list[list[float]]:
    import voyageai

    return voyageai.Client().embed(texts, model="voyage-4", input_type="document").embeddings


def build() -> list[dict]:
    rows = []
    for path in sorted(DOCS.rglob("*.md")):
        for piece in chunk(path.read_text(encoding="utf-8")):
            rows.append({"file": path.relative_to(DOCS).as_posix(), "text": piece})
    for row, vector in zip(rows, embed([row["text"] for row in rows])):
        row["vector"] = vector
    return rows


if __name__ == "__main__":
    INDEX.write_text(json.dumps(build()))
    print(f"indexed {len(json.loads(INDEX.read_text()))} chunks")
