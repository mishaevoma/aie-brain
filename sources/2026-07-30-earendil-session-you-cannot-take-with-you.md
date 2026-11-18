---
type: source
title: "The Session You Cannot Take With You"
author: "Earendil Engineering"
publisher: Earendil
url: https://earendil.com/posts/session-portability/
published: 2026-07-30
ingested: 2026-11-17
kind: article
read: full
concepts: [managed-agent-runtimes, memory]
---

# The Session You Cannot Take With You

**In one line:** Once a model API keeps or seals part of a session, the transcript you hold is only a partial view; to stay portable, keep the local log canonical and let no opaque item be the sole carrier of meaning.

## What it says

- **The argument.** Keeping an API's inputs and outputs once meant owning the conversation. APIs now mix text with state only the provider can read or resolve, so the local transcript is a partial view. Portable means another model can continue from the exported transcript after the old provider's credentials are revoked.
- **Five ownership tests:** inspection (what the model saw, its tool calls, the messages between agents), export (self-contained), replay (another implementation can rebuild an equivalent context), audit (a person can explain an action afterwards), deletion (every server-side copy can be found and removed).
- **Stored state.** OpenAI's Responses API stores responses by default, for at least 30 days per its documentation. Gemini's Interactions API defaults to `store: true`: 55 days on the paid tier, one day on the free tier. A response id becomes a foreign key into someone else's database; file, vector-store, container and cache references resolve nowhere else either.
- **Sealed reasoning.** With `store: false` OpenAI returns `encrypted_content` for the client to keep and replay. Anthropic returns the full thinking encrypted in a `signature` field, shows only a summary written by another model, and says to strip thinking blocks when switching models.
- **Hosted search.** OpenAI, Google and Anthropic return search actions, citations and optionally source URLs, not the text the model read.
- **Compaction.** OpenAI's server-side compaction emits an encrypted item. Anthropic's returns a readable summary and accepts custom instructions, so sealing is not technically necessary.
- **Subagents.** OpenAI's hosted Responses Multi-agent beta encrypts the task given to a subagent and the messages between agents, turns on server-side compaction for every agent and injects instructions the developer cannot edit. Since a June 2026 commit, the open-source Codex client's readable history omits the task too.
- **Seven rules** for providers and agent builders: the client's event log is canonical; storage is explicit, with `store: false` preferably the default; nothing opaque is the only carrier of meaning; hosted tools keep full-fidelity logs; subagent communication is auditable; compaction is inspectable; artifacts are exportable.

## What to do with it

- Keep your own event log as the record, never just a response id, and turn provider storage off.
- Prefer client-side search and compaction, which let you record the queries, passages and summaries.
- Keep a readable equivalent beside every sealed item, including each subagent's task and messages.

## Terms

- **Provider-sealed state** — content the client holds but only the provider can decrypt.

## Caveats

- July 2026, from the makers of the Pi harness, who gain when sessions can move. Retention periods and API details are as the article reports them, and will date.
- It concedes that few people switch models mid-session, and that sealing can help privacy and same-model quality.
- Its closing case for distillation is not covered here.
- It carries [Your harness, your memory](2026-04-11-chase-your-harness-your-memory.md) down to the model API, but calls Anthropic's server-side compaction readable and portable where that note lists it as provider-held state.
