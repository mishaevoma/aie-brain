"""The three tools the agent may call."""
import json
import urllib.request

ORDERS_API = "https://orders.internal.example.com"
PAYMENTS_API = "https://payments.internal.example.com"
MAIL_API = "https://mail.internal.example.com"
TIMEOUT_SECONDS = 5
APPROVAL_LIMIT_CENTS = 20_000

TOOL_DEFINITIONS = [
    {
        "name": "lookup_order",
        "description": "Look up an order.",
        "input_schema": {"type": "object", "properties": {"order_id": {"type": "string"}}, "required": ["order_id"]},
    },
    {
        "name": "issue_refund",
        "description": "Refund an order.",
        "input_schema": {
            "type": "object",
            "properties": {"order_id": {"type": "string"}, "amount_cents": {"type": "integer"}},
            "required": ["order_id", "amount_cents"],
        },
    },
    {
        "name": "send_email",
        "description": "Send an email.",
        "input_schema": {
            "type": "object",
            "properties": {"to": {"type": "string"}, "subject": {"type": "string"}, "body": {"type": "string"}},
            "required": ["to", "subject", "body"],
        },
    },
]


class NeedsApproval(Exception):
    """Raised when a person has to decide. The worker moves the request to the lead's queue."""


def _post(url: str, payload: dict) -> dict:
    request = urllib.request.Request(
        url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}, method="POST"
    )
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        return json.load(response)


def lookup_order(order_id: str) -> dict:
    with urllib.request.urlopen(f"{ORDERS_API}/orders/{order_id}", timeout=TIMEOUT_SECONDS) as response:
        return json.load(response)


def issue_refund(order_id: str, amount_cents: int) -> dict:
    if amount_cents > APPROVAL_LIMIT_CENTS:
        raise NeedsApproval(f"refund of {amount_cents} cents on {order_id}")
    return _post(f"{PAYMENTS_API}/refunds", {"order_id": order_id, "amount_cents": amount_cents})


def send_email(to: str, subject: str, body: str) -> dict:
    return _post(f"{MAIL_API}/send", {"to": to, "subject": subject, "body": body})


TOOLS = {"lookup_order": lookup_order, "issue_refund": issue_refund, "send_email": send_email}
