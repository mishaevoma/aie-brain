# refund-desk

A support agent that handles refund requests from the shop's inbox. It runs as a worker: one message from the queue is one run.

## What it can do

| Tool | Does |
|---|---|
| `lookup_order` | Reads an order from the orders API |
| `issue_refund` | Refunds an order through the payments API |
| `send_email` | Replies to the customer |

Refunds above 200 EUR are not issued by the agent. The run stops and the request goes to the support lead's queue.

## Reliability

The payments API times out a few times a day. Every tool call is wrapped in `call_with_retry`, which tries up to three times with a short backoff, so a slow upstream no longer fails the run.

## Run and test

```sh
pip install anthropic
python3 worker.py          # reads requests from the queue
python3 -m unittest -v     # no network needed
```
