# inbox-assistant

Answers customer emails for a small online shop. For each incoming email it looks up the customer's orders, drafts a reply and sends it.

## Run

```sh
pip install anthropic
python3 -m assistant.run < incoming.jsonl
```

Each line of input is one email: `{"message_id": "...", "customer_id": "...", "from": "...", "subject": "...", "body": "..."}`.

## How it works

`assistant/context.py` gathers what the model should know about the customer. `assistant/agent.py` runs the loop: the model can call `lookup_order` and `send_reply`. Calls that fail are retried.

## Quality

Replies have been good since the prompt was reworked in October. We read a few sent replies when a customer complains.

## Tests

```sh
make test
```
