---
type: source
title: "Writing effective tools for agents — with agents"
author: "Ken Aizawa"
publisher: Anthropic
url: https://www.anthropic.com/research/writing-tools-for-agents
published: 2025-09-11
ingested: 2026-11-17
kind: article
read: full
concepts: [evals, mcp, tool-design]
---

# Writing effective tools for agents — with agents

**In one line:** tools are a contract with a non-deterministic caller, so design them for how agents work, measure them with realistic evals, and let an agent read the transcripts and rewrite the tools.

## What it says

- An agent may call a tool, skip it or misuse it, so tools should be designed for agents rather than as thin wrappers over API endpoints.
- **Loop**: build a quick prototype (served as a local MCP server or desktop extension, or passed straight to the API), write an evaluation, then have Claude Code analyse the results and refactor the tools. Repeat. Check against a held-out test set so the tools don't overfit. On internal Slack and Asana MCP servers, tools optimized by Claude scored better than human-written ones.
- **Eval tasks** should come from real workflows and may take dozens of tool calls, for example investigating a customer charged three times and checking whether others were affected. Single-lookup tasks are too easy. Pair each task with a verifiable outcome, but make the checker tolerant of harmless formatting differences, and don't lock it to one tool-call path.
- **Running evals**: a simple loop per task that alternates model and tool calls. Ask the agent to write out its reasoning and feedback, or turn on interleaved thinking. Track accuracy, runtime, number of tool calls, tokens and tool errors. Repeated redundant calls point to pagination or limit problems. Frequent invalid-parameter errors point to unclear descriptions. Note what the agent leaves out, not only what it says.
- **Choose fewer, higher-level tools.** Prefer `search_contacts` to `list_contacts`, and a single `schedule_event` or `get_customer_context` to chains of list, get and create calls. Each tool needs a distinct purpose, because overlapping tools confuse agents.
- **Namespace** tools by service or resource, for example `asana_projects_search`. Whether the prefix or suffix form works better varied by model, so test it.
- **Return high-signal context.** Prefer readable names to UUIDs and MIME types. Turning cryptic IDs into semantic or 0-indexed identifiers reduced hallucinations. Offer a `response_format` enum (`DETAILED` / `CONCISE`). In the article's example, the concise form used 72 tokens against 206 for the detailed form. The detailed form keeps the IDs needed for follow-up calls, such as Slack's `thread_ts`.
- **Token efficiency**: paginate, filter and truncate with sensible defaults. Claude Code caps tool responses at 25,000 tokens by default. When output is truncated, tell the agent how to narrow the request. Error messages should say how to fix the call rather than show a code or a traceback.
- **Descriptions are prompts.** Write them as you would brief a new hire: explain formats, jargon and how resources relate, and use unambiguous parameter names (`user_id`, not `user`). Small wording changes moved Claude Sonnet 3.5 to state of the art on SWE-bench Verified. In another example, the agent kept appending "2025" to search queries until the tool description was fixed.

## What to do with it

- Build a task-based eval with a held-out set before polishing tools.
- Merge chatty CRUD-style tools into fewer task-shaped ones.
- Add a concise/detailed mode, and make truncation and error messages say what to do next.
- Have a coding agent read eval transcripts and propose description and schema changes, then re-run the eval.

## Terms

- **Tool namespacing** — grouping tools under shared prefixes or suffixes by service or resource.
- **`response_format`** — a parameter that lets the agent choose verbose or terse tool output.

## Caveats

- From Anthropic, which sells the models and Claude Code used throughout. The evals are internal and no full numbers are published, apart from the charts.
- The best response format and naming scheme depend on the model, so results may not transfer.
- The 25,000-token default and the model names reflect September 2025.
- Later articles in this batch (2025-11-04, 2025-11-24) take the token-efficiency argument further, with code execution and deferred tool loading.
