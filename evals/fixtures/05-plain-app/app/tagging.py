"""Pick a category for a new ticket."""

MODEL = "claude-haiku-5-5"
CATEGORIES = ["billing", "bug", "how-to", "account"]


def tag_ticket(text: str, client=None) -> str:
    if client is None:
        import anthropic

        client = anthropic.Anthropic()
    reply = client.messages.create(
        model=MODEL,
        max_tokens=20,
        messages=[
            {
                "role": "user",
                "content": (
                    "Classify this support ticket as one of: billing, bug, how-to, account. "
                    "Reply with the category only.\n\n" + text
                ),
            }
        ],
    )
    return reply.content[0].text.strip().lower()
