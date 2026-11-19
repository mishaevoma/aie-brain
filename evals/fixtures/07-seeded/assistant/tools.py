"""Tools the model may call."""
import json
import urllib.request

SHOP_API = "https://shop.internal.example.com"
MAIL_API = "https://mail.internal.example.com"

TOOL_DEFINITIONS = [
    {
        "name": "lookup_order",
        "description": "Get one order by its id, with items, status and tracking link.",
        "input_schema": {"type": "object", "properties": {"order_id": {"type": "string"}}, "required": ["order_id"]},
    },
    {
        "name": "send_reply",
        "description": "Send the reply to the customer. Call this once, when the reply is final.",
        "input_schema": {
            "type": "object",
            "properties": {"to": {"type": "string"}, "subject": {"type": "string"}, "body": {"type": "string"}},
            "required": ["to", "subject", "body"],
        },
    },
]


def lookup_order(order_id: str) -> dict:
    with urllib.request.urlopen(f"{SHOP_API}/orders/{order_id}", timeout=10) as response:
        return json.load(response)


def send_reply(to: str, subject: str, body: str) -> dict:
    payload = json.dumps({"to": to, "subject": subject, "body": body}).encode()
    request = urllib.request.Request(
        f"{MAIL_API}/send", data=payload, headers={"Content-Type": "application/json"}, method="POST"
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        return json.load(response)


TOOLS = {"lookup_order": lookup_order, "send_reply": send_reply}
