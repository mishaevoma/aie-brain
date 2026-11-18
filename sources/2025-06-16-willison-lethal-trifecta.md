---
type: source
title: "The lethal trifecta for AI agents: private data, untrusted content, and external communication"
author: "Simon Willison"
publisher: "Simon Willison's Weblog"
url: https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/
published: 2025-06-16
ingested: 2026-11-17
kind: article
read: full
concepts: [mcp, sandboxing-and-permissions]
---

# The lethal trifecta for AI agents: private data, untrusted content, and external communication

**In one line:** An agent that can read private data, sees content an attacker controls, and can send data out can be tricked into stealing that data, and the only dependable defence is never to combine all three.

## What it says

- The **lethal trifecta** is three capabilities in one agent: access to private data, exposure to untrusted content, and a way to communicate externally. With all three, an attacker can have the agent read the private data and send it to them.
- The cause is that a model follows instructions wherever they appear. It cannot reliably tell its operator's instructions from text in a web page, an email, a document or an image.
- This is found in production all the time. The post lists 3 cases from the weeks before it (Microsoft 365 Copilot, GitHub's official MCP server, GitLab's Duo Chatbot) and 14 more going back to April 2023.
- Vendors fixed almost all of them, usually by closing the route out. That does not protect people who combine tools themselves, which MCP encourages. One MCP server can even hold all three: the GitHub server could read public issues that anyone may file, read private repositories, and open pull requests.
- Routes out are close to unlimited: any HTTP request, an image that loads, a link shown to the user. A tool that reads email is a ready source of untrusted content.
- **Guardrail** products do not solve it. No method prevents the attack every time, and a filter said to catch 95% of attacks fails by the standard of application security.
- For developers the post points to a paper of six design patterns, built on the rule that an agent which has taken in untrusted input must be unable to trigger consequential actions, and to Google DeepMind's CaMeL.
- On terms: **prompt injection** is the mixing of trusted and untrusted content in one context, a name this author coined after SQL injection. **Jailbreaking**, tricking a model directly into misbehaving, is a different problem.

## What to do with it

- For every agent, and every set of tools connected to it, list which of the three capabilities it has. Remove one before shipping.
- Count every tool that makes a network request, renders an image or shows a link as a way out.
- Treat anything the agent reads from outside as able to carry instructions.
- Do not rely on a prompt or a detection product to stop injected instructions.

## Terms

- **Lethal trifecta** — private data, untrusted content and external communication in one agent.
- **Exfiltration** — sending stolen data out to an attacker.

## Caveats

- June 2025. The list of incidents stops there.
- Written for people who combine tools themselves. For what a product team can build, see [How we contain Claude](2026-05-25-anthropic-how-we-contain-claude.md), which caps the damage with boundaries on the environment.
