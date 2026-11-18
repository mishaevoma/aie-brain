---
type: source
title: "Hosting the Agent SDK"
author: "Anthropic"
publisher: Anthropic
url: https://code.claude.com/docs/en/agent-sdk/hosting
published: 2026-11-17
ingested: 2026-11-17
kind: docs
read: full
concepts: [managed-agent-runtimes]
---

# Hosting the Agent SDK

**In one line:** One Agent SDK session is one `claude` CLI subprocess whose transcript, memory files and working directory sit on local disk; hosting means choosing how long containers live relative to sessions and mirroring transcripts to a best-effort store that copies nothing else.

## What it says

- Covers the hosting page and three sub-pages: "Work with sessions", "Persist sessions to external storage" and "Securely deploying AI agents".
- **One session, one subprocess.** A `query()` call spawns a `claude` CLI process owning a shell, a working directory and a JSONL transcript (the prompt and every tool call, result and response). Transcripts, `CLAUDE.md` memory files and working-directory artefacts are on local disk; none outlives a container restart, a scale-down or a change of node.
- **Four session patterns.** Ephemeral: one container per one-off task, destroyed afterwards. Long-running: persistent containers holding many sessions, for agents that act autonomously, serve content or handle heavy message streams. Hybrid: ephemeral containers that load from a `SessionStore` and write back, for sessions with idle gaps; the store is mandatory. Multi-agent: several subprocesses in one container, for agents that collaborate closely.
- **Resume** starts a new subprocess from a stored transcript, restoring the conversation but not the filesystem. Session files are local to one machine; across hosts, use a session store, move the file, or pass saved results into a fresh session (called often more robust).
- **`SessionStore`** (required methods `append` and `load`) is a mirror: the subprocess writes local disk first and the SDK forwards each batch.
  - Transcripts only: not memory files or working-directory artefacts.
  - Best-effort: after at most three attempts at `append`, the batch is dropped, a `mirror_error` message is emitted and the query continues.
  - A run that resumes from the store removes its local transcript when it ends, so the store holds the only durable copy.
  - Its key encodes the working directory, so resume needs a matching `cwd`.
- **Sizing.** Start at 1 CPU, 1 GiB RAM and 5 GiB disk for each agent, as a floor: memory grows with session length. Token cost typically exceeds container cost (roughly $0.05 per hour) by an order of magnitude or more.
- **Secure deployment.** The agent runs inside the isolation boundary and credentials stay outside it.
  - Isolation, in rising order of overhead: sandbox-runtime, Docker containers, gVisor, VMs such as Firecracker. The first two share the host kernel.
  - Network: no direct egress; a proxy enforces a domain allowlist and logs requests. Data can still leave to any allowed domain.
  - Credentials: the proxy injects them, so the agent never sees them. `ANTHROPIC_BASE_URL` covers model calls only; other HTTPS services need a tool calling out of the boundary, or a TLS-terminating proxy.

## What to do with it

- Choose the session pattern first: it decides whether a store is required.
- Alert on `mirror_error`, and deduplicate in `append` by `entry.uuid`.
- Bound sessions with `maxTurns`; they have no timeout of their own.

## Terms

- **Session** — the conversation history that a later call can continue, resume or fork.

## Caveats

- Undated documentation, read on 17 November 2026; the date above is the day it was read.
- Vendor documentation for one SDK, with rule-of-thumb figures and nothing on triggers, schedules or queues.
