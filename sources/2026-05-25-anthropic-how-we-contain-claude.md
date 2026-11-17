---
type: source
title: "How we contain Claude across products"
author: "Max McGuinness, Mikaela Grace, Jiri De Jonghe, Jake Eaton, Abel Ribbink"
publisher: "Anthropic"
url: https://www.anthropic.com/research/how-we-contain-claude
published: 2026-05-25
ingested: 2026-11-17
kind: article
read: full
concepts: [context-layer, human-judgment, instruction-files, mcp, memory, multi-agent-systems, production-operations, sandboxing-and-permissions]
---

# How we contain Claude across products

**In one line:** cap the blast radius with deterministic environment boundaries first, use model-layer defenses as a second layer, and expect your own custom glue to be what breaks.

## What it says

- Risk is likelihood times **blast radius**. Training lowers likelihood; more access raises blast radius. Responses: supervision (human or classifier approvals) and **containment** (sandboxes, VMs, egress controls), where Anthropic invests most.
- Threat sources: user misuse, model misbehaviour (capable models route around unwritten limits, such as escaping a sandbox to finish a task), and external attackers.
- Defend three things: the **environment** (credentials that never enter the sandbox cannot leak), the **model** (on Gray Swan's Agent Red Teaming benchmark Claude Opus 4.7 holds attack success to about 0.1% single-shot, 5–6% after 100 adaptive tries; auto mode catches about 83% of overeager actions), and **external content** (an audited connector is not audited data).
- **claude.ai:** ephemeral gVisor container, server-side.
- **Claude Code:** human-in-the-loop plus an OS sandbox (Seatbelt / bubblewrap) allowing workspace writes, denying network by default; prompts fell 84% (users had approved about 93%). Experienced users auto-approve about twice as often as new ones but interrupt more.
- **Claude Cowork:** for non-developers, a local VM (Apple Virtualization framework; HCS on Windows) mounting only the workspace and `.claude`, credentials kept in the host keychain, mounts read-only, read-write or read-write-no-delete. The agent loop later moved to the host ("host-mode"); code still runs in the VM.
- Missed risks: three bugs (mid-2025 to January 2026) where input from an untrusted repository ran code before the trust dialog, the most direct being a hook in the repo's `.claude/settings.json`; a February 2026 internal phish where a pasted prompt sent `~/.aws/credentials` out 24 of 25 times, stoppable only by egress and filesystem limits; Cowork exfiltration via allow-listed api.anthropic.com with an attacker's API key, fixed by an in-VM proxy accepting only the session's token; and VM isolation hiding activity from enterprise EDR (pull-based OTLP logs help).
- Remote MCP tools can change after approval; treat anything outside Anthropic's connector directory as untrusted. Proxies inspect tool results before they reach the model.
- Open problems: memory poisoning (CLAUDE.md, memory, state dirs), trust escalation through subagent output, agent identity.

## What to do with it

- Build the deterministic boundary first: scoped filesystem, default-deny egress, no credentials inside.
- Match isolation to who supervises: developers can handle prompts; non-developers need an always-on admin boundary.
- Treat allow-listed domains as capability grants; bind requests to the session's own token.
- Load no project config before trust; treat localhost listeners as untrusted.
- Resolve symlinks before validating paths.
- Review your own proxies hardest; standard primitives held up better.
- Plan early for security monitoring inside VMs.

## Terms

- **blast radius** — the damage an agent could do if it fails.
- **containment** — enforcing what an agent can reach, rather than supervising each action.

## Caveats

- Vendor describing its own products; incidents are self-reported.
- Product details reflect May 2026.
- The 83% figure restates auto mode's 17% miss rate (2026-03-25). Agrees with Loams (2026-10-18) that classifiers are not the boundary.
