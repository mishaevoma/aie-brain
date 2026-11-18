---
type: source
title: "Interrupts"
author: "LangChain"
publisher: LangChain
url: https://docs.langchain.com/oss/python/langgraph/interrupts
published: 2026-11-12
ingested: 2026-11-17
kind: docs
read: full
concepts: [side-effects]
---

# Interrupts

**In one line:** A LangGraph interrupt checkpoints the graph and waits indefinitely for an answer, but on resume the whole node runs again from its first line, so anything placed before the interrupt must be safe to repeat.

## What it says

- Calling `interrupt()` inside a node or a tool suspends the graph there. LangGraph saves the state through its checkpointer and waits, with no time limit, until the caller resumes.
- It needs a checkpointer (a persistent, database-backed one in production), a `thread_id` in the config, and a JSON-serialisable payload. The thread ID points at the saved state: reusing it resumes that checkpoint, and a new one starts an empty thread.
- The payload reaches the caller on `stream.interrupts` with event streaming, or under `__interrupt__` in the result of `invoke()`. To resume, the caller invokes the graph again with `Command(resume=...)` and the same thread ID, and that value is what the `interrupt()` call then returns.
- **What runs again.** An interrupt is a special exception caught by the runtime. On resume the node restarts from its beginning, not from the line of the call, so all code before the interrupt executes again. With a subgraph invoked as a function, both the parent node and the subgraph's node restart.
- **Side effects.** An API call made before the interrupt re-runs on every resume and can overwrite an update or create duplicate records. Remedies: idempotent operations such as an upsert, moving the effect after the interrupt, or a separate node. An effect placed after approval can still repeat if the node fails and is retried, so deduplication in the external system is still advised.
- **Several interrupts.** Within one node, resume values are matched to interrupt calls strictly by index, so the calls must occur in the same order on every execution: no conditional skipping, no loops of varying length. When parallel branches interrupt together, each pending interrupt has an ID, and one `Command(resume=...)` can carry a map from ID to resume value.
- **Pitfalls.** A bare `try/except` around `interrupt()` swallows the exception, so the pause never reaches the graph. A `while True` validation loop inside one node replays every earlier iteration on each resume; use one interrupt per node invocation and a conditional edge looping back. Functions and class instances may not serialise, so keep them out of payloads.

## What to do with it

- Keep the node that asks a person small: the interrupt first, effects after it or in the next node.
- Make every write before an interrupt idempotent, and deduplicate approved actions at the receiver too.
- Use a durable checkpointer and a stable thread ID kept outside the process.
- Call interrupts in a fixed order, and re-prompt through graph edges, not loops inside a node.

## Terms

- **Interrupt** — a dynamic pause raised from inside node code. Static breakpoints set before or after a node are meant for debugging, not for human-in-the-loop work.

## Caveats

- The page shows no publication date; the date above is the last-modified date in its metadata.
- Python documentation, and version-specific: typed validation of resume values, for instance, needs `langgraph>=1.2.12`.
- Mechanism only: nothing on timeouts, reminders, who may answer, or a paused run meeting changed graph code.
