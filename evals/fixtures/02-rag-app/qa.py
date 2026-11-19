#!/usr/bin/env python3
"""Answer one question from the indexed handbook."""
import json
import math
import sys
from pathlib import Path

INDEX = Path(__file__).parent / "index.json"
MODEL = "claude-sonnet-5-5"
TOP_K = 25


def cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm = math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b))
    return dot / norm if norm else 0.0


def embed_query(text: str) -> list[float]:
    import voyageai

    return voyageai.Client().embed([text], model="voyage-4", input_type="query").embeddings[0]


def retrieve(question: str, index: list[dict], top_k: int = TOP_K) -> list[dict]:
    query = embed_query(question)
    ranked = sorted(index, key=lambda row: cosine(query, row["vector"]), reverse=True)
    return ranked[:top_k]


def build_prompt(question: str, chunks: list[dict], history: list[dict]) -> str:
    context = "\n\n".join(row["text"] for row in chunks)
    past = "\n".join(f"{turn['role']}: {turn['text']}" for turn in history)
    return (
        "Answer the question using the handbook excerpts.\n\n"
        f"Excerpts:\n{context}\n\n"
        f"Conversation so far:\n{past}\n\n"
        f"Question: {question}"
    )


def answer(question: str, history: list[dict] | None = None) -> str:
    import anthropic

    index = json.loads(INDEX.read_text())
    prompt = build_prompt(question, retrieve(question, index), history or [])
    reply = anthropic.Anthropic().messages.create(
        model=MODEL, max_tokens=600, messages=[{"role": "user", "content": prompt}]
    )
    return reply.content[0].text


if __name__ == "__main__":
    print(answer(" ".join(sys.argv[1:])))
