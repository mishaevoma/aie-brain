#!/usr/bin/env python3
"""Run the release-notes crew: planner, researcher, writer, critic."""
import json
import sys

MODEL = "claude-sonnet-5-5"

PLANNER = "You are the Planner. Given this week's merged pull requests, list the steps the crew should take to write release notes."
RESEARCHER = "You are the Researcher. Summarise the merged pull requests for the Writer in a few sentences."
WRITER = "You are the Writer. Write customer-facing release notes from the research summary."
CRITIC = "You are the Critic. Review the release notes. Reply APPROVED if they are ready, otherwise say what to fix."


def ask(role_prompt: str, content: str, client) -> str:
    reply = client.messages.create(
        model=MODEL, max_tokens=1500, system=role_prompt, messages=[{"role": "user", "content": content}]
    )
    return reply.content[0].text


def run(prs: list[dict], client=None) -> str:
    if client is None:
        import anthropic

        client = anthropic.Anthropic()
    transcript = []

    plan = ask(PLANNER, json.dumps(prs), client)
    transcript.append(f"Planner: {plan}")

    research = ask(RESEARCHER, "\n".join(transcript) + "\n\nPull requests:\n" + json.dumps(prs), client)
    transcript.append(f"Researcher: {research}")

    notes = ask(WRITER, research, client)
    transcript.append(f"Writer: {notes}")

    while True:
        verdict = ask(CRITIC, notes, client)
        transcript.append(f"Critic: {verdict}")
        if "APPROVED" in verdict:
            return notes
        notes = ask(WRITER, "\n".join(transcript) + "\n\nRewrite the notes to address the Critic.", client)
        transcript.append(f"Writer: {notes}")


if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as handle:
        print(run(json.load(handle)))
