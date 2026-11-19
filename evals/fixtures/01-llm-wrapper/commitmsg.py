#!/usr/bin/env python3
"""Print a commit message for the staged changes."""
import subprocess
import sys

MODEL = "claude-haiku-5-5"

RULES = """You write git commit messages.
- Subject line: imperative mood, at most 72 characters, no trailing period.
- Name the thing that changed, not the file list.
- Add a body only when the reason is not obvious from the subject.
- Never mention that you are an AI.
"""


def staged_diff() -> str:
    result = subprocess.run(["git", "diff", "--staged"], capture_output=True, text=True, check=True)
    return result.stdout


def build_prompt(diff: str) -> str:
    return f"{RULES}\nHere is the staged diff:\n\n{diff}\n\nReply with the commit message only."


def generate(diff: str, client=None) -> str:
    if client is None:
        import anthropic

        client = anthropic.Anthropic()
    reply = client.messages.create(
        model=MODEL,
        max_tokens=300,
        messages=[{"role": "user", "content": build_prompt(diff)}],
    )
    return reply.content[0].text.strip()


def main() -> int:
    diff = staged_diff()
    if not diff.strip():
        print("Nothing staged.", file=sys.stderr)
        return 1
    print(generate(diff))
    return 0


if __name__ == "__main__":
    sys.exit(main())
