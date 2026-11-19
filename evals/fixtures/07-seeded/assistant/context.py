"""Collect what the model is shown about a customer."""
import json
import urllib.request
from pathlib import Path

SHOP_API = "https://shop.internal.example.com"
KB = Path(__file__).parent.parent / "kb"


def past_emails(customer_id: str) -> list[dict]:
    with urllib.request.urlopen(f"{SHOP_API}/customers/{customer_id}/emails", timeout=10) as response:
        return json.load(response)


def knowledge_base() -> str:
    return "\n\n".join(path.read_text(encoding="utf-8") for path in sorted(KB.glob("*.md")))


def build_context(customer_id: str) -> str:
    emails = past_emails(customer_id)
    history = "\n\n".join(f"[{mail['date']}] {mail['subject']}\n{mail['body']}" for mail in emails)
    return f"Shop policies and product notes:\n{knowledge_base()}\n\nEvery email this customer has sent us:\n{history}"
