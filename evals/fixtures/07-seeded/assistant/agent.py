"""The reply loop."""
import time

from assistant import context, tools

MODEL = "claude-sonnet-5-5"
MAX_STEPS = 8


def with_retries(function, arguments: dict, attempts: int = 3, sleep=time.sleep):
    last_error = None
    for attempt in range(attempts):
        try:
            return function(**arguments)
        except Exception as error:
            last_error = error
            sleep(1 + attempt)
    raise last_error


def reply_to(email: dict, client=None, registry=None) -> str:
    if client is None:
        import anthropic

        client = anthropic.Anthropic()
    registry = registry or tools.TOOLS
    # Reworked in October: friendlier, shorter, stopped promising refunds. Tweaked a few times since.
    system = f"""You are the support assistant of Fern & Fig, an online plant shop.
Be warm and brief. Use the customer's first name. Never promise a refund; say the team will review it.
If an order is late, give the tracking link. If you are not sure, say a person will follow up.
Sign off as "The Fern & Fig team".

{context.build_context(email["customer_id"])}
"""
    messages = [{"role": "user", "content": f"From: {email['from']}\nSubject: {email['subject']}\n\n{email['body']}"}]
    for _ in range(MAX_STEPS):
        reply = client.messages.create(
            model=MODEL, max_tokens=1200, system=system, tools=tools.TOOL_DEFINITIONS, messages=messages
        )
        messages.append({"role": "assistant", "content": reply.content})
        calls = [block for block in reply.content if block.type == "tool_use"]
        if not calls:
            return "".join(block.text for block in reply.content if block.type == "text")
        results = []
        for call in calls:
            output = with_retries(registry[call.name], call.input)
            results.append({"type": "tool_result", "tool_use_id": call.id, "content": str(output)})
        messages.append({"role": "user", "content": results})
    return "Stopped: step limit reached."
