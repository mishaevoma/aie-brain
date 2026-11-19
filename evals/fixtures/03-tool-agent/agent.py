"""The agent loop: ask the model, run the tool it picks, feed the result back."""
import time

import tools

MODEL = "claude-sonnet-5-5"
MAX_STEPS = 12
RETRIES = 3

SYSTEM = (
    "You handle refund requests for an online shop. Look up the order before deciding. "
    "Refund only what the customer paid for the returned items. Always email the customer at the end."
)


def call_with_retry(name: str, arguments: dict, registry=None, sleep=time.sleep):
    """Run a tool, trying again when it fails. Returns the result, or the string "error"."""
    registry = registry or tools.TOOLS
    for attempt in range(RETRIES):
        try:
            return registry[name](**arguments)
        except tools.NeedsApproval:
            raise
        except Exception:
            sleep(2 ** attempt)
    return "error"


def run(request_text: str, client=None, registry=None) -> str:
    if client is None:
        import anthropic

        client = anthropic.Anthropic()
    messages = [{"role": "user", "content": request_text}]
    for _ in range(MAX_STEPS):
        reply = client.messages.create(
            model=MODEL, max_tokens=1000, system=SYSTEM, tools=tools.TOOL_DEFINITIONS, messages=messages
        )
        messages.append({"role": "assistant", "content": reply.content})
        calls = [block for block in reply.content if block.type == "tool_use"]
        if not calls:
            return "".join(block.text for block in reply.content if block.type == "text")
        results = []
        for call in calls:
            output = call_with_retry(call.name, call.input, registry)
            results.append({"type": "tool_result", "tool_use_id": call.id, "content": str(output)})
        messages.append({"role": "user", "content": results})
    return "Stopped: step limit reached."
