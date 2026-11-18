---
type: source
title: "Securing persistent agents like OpenClaw at OpenAI"
author: "Kevin S Lin"
publisher: OpenAI Developers
url: https://developers.openai.com/blog/securing-persistent-agents-like-openclaw-at-openai
published: 2026-11-12
ingested: 2026-11-17
kind: article
read: full
concepts: [agent-identity, sandboxing-and-permissions]
---

# Securing persistent agents like OpenClaw at OpenAI

**In one line:** OpenAI runs over 500 background agents by treating each agent, its environment and its code as untrusted: what configures the agent sits in a separate cluster, and a sandbox, a second-model review of every action, a per-agent identity and full logging surround it.

## What it says

- **Scale.** Persistent agents (running 24/7, broad in scope, acting without user input) are deployed across OpenAI, including hundreds of OpenClaw agents. Over 500 work proactively in the background.
- **Threat model.** Unlike ordinary software, a persistent agent can change its own configuration and write arbitrary code, so attacks come from inside, as misaligned actions by the agent itself.
- **Trusted and untrusted halves.** Networking, identity and sandboxing are trusted static code that behaves as configured. Agents, their environment and the code they write are untrusted. OpenAI added "remote harness execution" to open-source OpenClaw so that the OpenClaw Gateway, which configures the agent, runs in a separate container from the agent harness (at OpenAI, a separate cluster).
- **Four sandbox controls**, from the Codex harness's built-in sandbox: network (an organisation-managed allowlist plus explicit denials), workspace (writes only to the agent's working directories), process (isolation by the Codex Linux sandbox) and secrets (a credential broker hides them from the agent).
- Policy sits in two files. `requirements.toml` restricts which options exist: no `danger-full-access` mode, cached web search only (served from OpenAI's own index) and no widening of the domain allowlist by user-level configuration. `config.toml` holds the actual settings. Between them the samples block `pastebin.com`, `webhook.site` and cloud metadata endpoints, deny the SSH directory, strip GitHub tokens from command environments and disable apps by default.
- **Auto-review.** A second agent monitors and approves the primary agent's actions, and OpenAI enforces it on all of them. Reasons given: constant prompts train people to accept blindly, so a model filter keeps human attention for high-value approvals; and static controls need a defence that scales with compute as models get smarter.
- **Agent identity.** Each agent has a unique identity tied to a ChatGPT Service Account, so its actions can be told from the user's and audited. It gets its own inference credential, which operators can turn off, and teams can attach custom plugins.
- **Logging.** Every control-plane configuration change and every agent turn is logged. Turns can hold sensitive data, so only a few people in the security team can read them.
- Many of these safeguards ship in the standard codex preset of OpenClaw Enterprise (OCE), an open-source control plane still in pilot.

## What to do with it

- Put whatever configures the agent where the agent cannot reach it.
- Separate what administrators forbid from what users may configure.
- Deny metadata endpoints and paste sites explicitly, besides allowlisting.
- Give each agent its own identity and inference credential, with service accounts linked to it.

## Terms

- **Auto-review** — a second model approving or rejecting the primary agent's actions.

## Caveats

- OpenAI on its own deployment and products, with no incidents, reviewer error rates or count of how often a person is still asked.
- Not covered: what the reviewer sees, how the credential broker works, how these agents are woken and recovered, and prompt injection. The configuration is a sample.
