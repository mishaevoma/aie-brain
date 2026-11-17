---
type: source
title: "Beyond permission prompts: making Claude Code more secure and autonomous"
author: "David Dworken, Oliver Weller-Davies"
publisher: "Anthropic"
url: https://www.anthropic.com/research/claude-code-sandboxing
published: 2025-10-20
ingested: 2026-11-17
kind: article
read: full
concepts: [sandboxing-and-permissions]
---

# Beyond permission prompts: making Claude Code more secure and autonomous

**In one line:** replace per-action approval prompts with an OS-enforced boundary on both filesystem and network, so the agent works freely inside it and a prompt injection has nowhere to go.

## What it says

- Claude Code starts read-only and asks before edits or commands, auto-allowing only safe ones like `echo` and `cat`. Frequent asking causes **approval fatigue**: people stop reading what they approve.
- Sandboxing sets the boundary once and asks only when the agent tries to cross it. Internally it cut permission prompts by **84%**.
- Both boundaries are required. Without network isolation, a hijacked agent can send out SSH keys; without filesystem isolation, it can tamper its way out and regain network access.
- **Sandboxed bash tool:** a new sandbox runtime (beta, open-source research preview) enforces limits with **bubblewrap** on Linux and **seatbelt** on macOS, covering every subprocess a command spawns. It can also wrap other processes, agents and MCP servers without containers.
- Defaults: read and write only in the current working directory. Network goes via a Unix domain socket to a proxy outside the sandbox that enforces a domain allow-list, asks about new domains, and can apply custom egress rules. Enable with `/sandbox`.
- **Claude Code on the web:** each session runs in an isolated cloud sandbox with no git credentials or signing keys inside. A git proxy accepts a scoped credential, checks the operation (for example, pushes only to the configured branch), then attaches the real GitHub token.

## What to do with it

- Read a high approval rate as a sign prompts are not working; move the decision into a boundary.
- Isolate filesystem and network together, at OS level so child processes inherit limits.
- Send all egress through a proxy with a domain allow-list.
- Keep real credentials outside the sandbox; give it a scoped stand-in and let a proxy swap in the real token after checking the request.

## Terms

- **approval fatigue** — users rubber-stamp frequent prompts and stop checking them.
- **sandbox runtime** — Anthropic's open-source process sandbox behind the sandboxed bash tool.

## Caveats

- Vendor writing about its own product; the 84% figure is internal, method not given.
- Late-2025 research preview. The Loams teardown (2026-10-18) adds that this sandbox covers shell commands only (not file tools, MCP servers or hooks) and does not run on native Windows.
- Followed by auto mode (2026-03-25) for actions needing network or host access, and by "How we contain Claude" (2026-05-25), which reports a missed risk: content from an untrusted repository, such as a project hook, ran before the trust dialog.
