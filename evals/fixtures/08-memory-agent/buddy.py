#!/usr/bin/env python3
"""Chat with the tutor. Type an empty line to stop."""
import memory

MODEL = "claude-sonnet-5-5"

TUTOR = """You are a patient German tutor. Speak German at the learner's level and correct mistakes briefly.
Start each session by picking up where the learner left off.

What you know about the learner:
{notes}
"""


def session(client=None, read=input, write=print) -> None:
    if client is None:
        import anthropic

        client = anthropic.Anthropic()
    system = TUTOR.format(notes=memory.load_all())
    messages = []
    while True:
        learner_text = read("> ")
        if not learner_text.strip():
            return
        messages.append({"role": "user", "content": learner_text})
        reply = client.messages.create(model=MODEL, max_tokens=600, system=system, messages=messages)
        tutor_text = reply.content[0].text
        messages.append({"role": "assistant", "content": tutor_text})
        write(tutor_text)
        memory.remember(learner_text, tutor_text, client)


if __name__ == "__main__":
    session()
