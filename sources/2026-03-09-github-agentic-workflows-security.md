---
type: source
title: "Under the hood: Security architecture of GitHub Agentic Workflows"
author: "Landon Cox, Jiaxiao Zhou"
publisher: The GitHub Blog
url: https://github.blog/ai-and-ml/generative-ai/under-the-hood-security-architecture-of-github-agentic-workflows/
published: 2026-03-09
ingested: 2026-11-17
kind: article
read: full
concepts: [side-effects]
---

# Under the hood: Security architecture of GitHub Agentic Workflows

**In one line:** GitHub runs an untrusted agent as a compiled GitHub Action in which the agent's container holds no secrets, reads GitHub through a read-only server, and can only stage writes, which deterministic checks vet after it exits.

## What it says

- GitHub Agentic Workflows run agents as an extension of CI/CD, not as a separate runtime: each workflow is compiled into a GitHub Action whose permissions, outputs, audit trail and network access are constrained explicitly.
- **Threat model.** An autonomous agent reading untrusted input is not trusted, and GitHub Actions by default runs everything in one trust domain, which gives it a large blast radius. It is assumed to try to read and write state it should not, use unintended channels and abuse legitimate ones. Strict mode is the default.
- **Three layers**, each limiting failures above it: a substrate (runner VM and trusted containers, with kernel-enforced boundaries), configuration (which components load, which tokens go into which container) and planning (the staged workflow).
- **No secrets for the agent.** In an ordinary action every process on the VM can read the environment variables and configuration files that hold MCP server API keys and the agent's own authentication tokens, so a prompt-injected agent with a shell can leak them. Here the agent has its own container on a private network behind a firewall. Model tokens sit in a separate API proxy that carries the agent's model traffic. An MCP gateway in another trusted container launches the MCP servers and alone holds their credentials.
- The agent runs in a chroot jail over the host file system, mounted read-only at `/host`, so host tools stay usable.
- **Staged writes.** While it runs, the agent reads GitHub state through the read-only GitHub MCP server and can stage updates only through the safe outputs MCP server, which buffers them. After the agent exits, deterministic analyses decide what is passed on: only operations the workflow author allowed, a cap on their number (for example at most three pull requests per run), and content sanitisation such as removing URLs or secrets.
- **Logging at each trust boundary.** The firewall records network destinations, the API proxy records model request and response metadata, and the MCP gateway and servers record tool calls. Instrumentation in the agent container audits sensitive actions such as reading environment variables. Every observation point is also a possible control point.

## What to do with it

- Assume the agent is compromised, and design for what it could then reach.
- Keep model and tool credentials in proxies outside the agent's container.
- Give the agent read access and a staging tool, and apply its writes after it exits, through deterministic checks on type, count and content.
- Log at every boundary the agent's traffic crosses.

## Terms

- **Safe outputs** — the subsystem that buffers the agent's intended GitHub writes and vets them after the run.
- **Zero-secret agent** — an agent whose container holds no authentication material.

## Caveats

- A vendor's design description from March 2026 with no measurements: nothing on attacks stopped or missed, or on overhead.
- Vetting writes after exit suits batch automation, not an interactive agent whose writes must land during the run.
