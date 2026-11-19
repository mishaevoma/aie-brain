"""Notes the tutor keeps about the learner between sessions."""
import datetime
import json
from pathlib import Path

MEMORY = Path(__file__).parent / "memory.jsonl"
MODEL = "claude-haiku-5-5"

EXTRACT = (
    "You maintain notes about a language learner. From the exchange below, list what to remember.\n"
    "Rules: record only mistakes the learner made. One note per line. No praise, no goals, no preferences.\n"
    "Reply with NONE if there is no mistake."
)


def load_all(path: Path = MEMORY) -> str:
    """Every note ever written, oldest first, as one block of text."""
    if not path.exists():
        return ""
    notes = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return "\n".join(f"[{note['date']}] {note['text']}" for note in notes)


def remember(learner_text: str, tutor_text: str, client, path: Path = MEMORY, today=None) -> int:
    """Ask the model what to keep from one exchange and append it. Returns the number of notes added."""
    reply = client.messages.create(
        model=MODEL,
        max_tokens=300,
        system=EXTRACT,
        messages=[{"role": "user", "content": f"Learner: {learner_text}\nTutor: {tutor_text}"}],
    )
    text = reply.content[0].text.strip()
    if text == "NONE":
        return 0
    date = (today or datetime.date.today()).isoformat()
    lines = [line.strip("- ").strip() for line in text.splitlines() if line.strip()]
    with path.open("a", encoding="utf-8") as handle:
        for line in lines:
            handle.write(json.dumps({"date": date, "text": line}) + "\n")
    return len(lines)
