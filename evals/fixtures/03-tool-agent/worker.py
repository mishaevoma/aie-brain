#!/usr/bin/env python3
"""Take refund requests from the queue and run the agent on each."""
import json
import sys

import agent
import tools


def handle(message: dict) -> dict:
    try:
        return {"id": message["id"], "status": "done", "summary": agent.run(message["text"])}
    except tools.NeedsApproval as reason:
        return {"id": message["id"], "status": "needs_approval", "reason": str(reason)}


if __name__ == "__main__":
    for line in sys.stdin:
        print(json.dumps(handle(json.loads(line))), flush=True)
