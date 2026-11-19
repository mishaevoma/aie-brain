"""Read emails as JSON lines on stdin and answer each one."""
import json
import sys

from assistant import agent

if __name__ == "__main__":
    for line in sys.stdin:
        email = json.loads(line)
        print(json.dumps({"message_id": email["message_id"], "result": agent.reply_to(email)}), flush=True)
