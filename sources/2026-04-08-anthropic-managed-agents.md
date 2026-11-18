---
type: source
title: "Scaling Managed Agents: Decoupling the brain from the hands"
author: "Lance Martin, Gabe Cemaj, Michael Cohen"
publisher: Anthropic
url: https://www.anthropic.com/research/managed-agents
published: 2026-04-08
ingested: 2026-11-17
kind: article
read: full
concepts: [agent-platforms, context-engineering, durable-execution, harness, long-running-agents, mcp, memory, production-operations, sandboxing-and-permissions]
---

# Scaling Managed Agents: Decoupling the brain from the hands

**In one line:** Split an agent system into three replaceable parts: a durable session log, a stateless harness (the "brain"), and sandboxes or tools (the "hands"), each behind a narrow interface. Then any part can crash, scale or be swapped as models change.

## What it says

- Harness assumptions go stale: context resets built for Sonnet 4.5's **context anxiety** were dead weight on Opus 4.5. So Managed Agents, Anthropic's hosted agent service, fixes interfaces rather than a harness, as operating systems keep `read()` stable across hardware.
- Three components: the **session** (append-only log of everything that happened), the **harness** (loop that calls Claude and routes tool calls) and the **sandbox** (where code runs and files change).
- First design: all three in one container, which became a "pet". If it died, the session was lost. Debugging meant a shell next to user data, and customer VPCs needed network peering.
- Decoupled design:
  - Sandboxes are called like any tool via `execute(name, input) → string` and created with `provision({resources})`. A dead container becomes a tool error Claude can retry around ("cattle").
  - The harness is stateless. After a crash, `wake(sessionId)` and `getSession(id)` reload the log and resume. Events are written with `emitEvent(id, event)`.
  - Credentials never enter the sandbox. Git tokens are used at setup and wired into the remote. MCP calls go through a proxy that fetches OAuth tokens from a vault, so neither sandbox nor harness sees secrets. Narrow token scoping alone was judged too weak against prompt injection.
- **The session is not the context window.** Compaction, the memory tool and trimming discard information irreversibly. With the full log outside the model, the harness fetches slices via `getEvents()` (resume, rewind, reread) and can transform them before inference, e.g. for prompt-cache hits.
- Lazy container provisioning let inference start sooner: p50 time-to-first-token fell about 60%, p95 over 90%.
- "Many hands": one brain can drive several environments (containers, MCP servers, even a phone) through the same interface.
- Managed Agents is described as a **meta-harness**: it can host Claude Code or task-specific harnesses and has opinions only about the interfaces.

## What to do with it

- Keep agent state in a durable event log, outside both context and sandbox, and make the loop stateless and resumable from it.
- Treat sandboxes as disposable, lazily created tools behind one call signature.
- Keep credentials structurally out of reach of generated code (setup-time injection, vault-backed proxies).
- Decide what enters the context window at read time, not by destroying history.

## Terms

- **Brain / hands** — model plus harness vs the sandboxes and tools it acts through.
- **Meta-harness** — infrastructure that fixes interfaces but not the agent loop.

## Caveats

- Describes Anthropic's own commercial product; latency numbers are self-reported, and interface names may change.
- Its critique of irreversible compaction pushes against the compaction-based harnesses in [earlier posts](2026-03-24-anthropic-harness-design-long-running-apps.md).
- The product's documentation, read in November 2026, adds the limits this article leaves out, such as how long a sandbox is kept and what a stream carries: see the [Managed Agents docs note](2026-11-17-anthropic-managed-agents-overview.md).
