---
type: source
title: "The \"think\" tool: Enabling Claude to stop and think in complex tool use situations"
author: "Anthropic"
publisher: Anthropic
url: https://www.anthropic.com/research/claude-think-tool
published: 2025-03-20
ingested: 2026-11-17
kind: article
read: full
concepts: [evals, tool-design]
---

# The "think" tool: Enabling Claude to stop and think in complex tool use situations

**In one line:** a no-op tool named `think` gives the model a sanctioned place to reason between tool calls, which helped in policy-heavy, multi-step agent work. As of December 2025, Anthropic recommends extended thinking instead in most cases.

## What it says

- The tool has a single required string parameter, `thought`, and does nothing except record the reasoning. The model uses it mid-response to check whether it has what it needs and whether the next step complies with the rules.
- Unlike extended thinking, which happens before the response, it reasons mid-stream about new information such as tool results.
- Tested with Claude 3.7 Sonnet on τ-bench (customer service with simulated users, policies and database tools), scored by pass^k.
- Airline domain: according to the text, the think tool plus an optimized prompt reached 0.570 pass^1 against a 0.370 baseline, a 54% relative gain. The optimized prompt tells the model to list the applicable rules, confirm it has the required information, check policy compliance and verify tool results, with two worked examples. With that prompt, the think tool beat extended thinking. Without it, the think tool performed about as well as extended thinking.
- Retail domain: the think tool alone, with no special prompt, scored 0.812 against a 0.783 baseline. The gains held out to k=5.
- SWE-bench: adding the tool improved Claude 3.7 Sonnet by 1.6% on average and contributed to a 0.623 score.
- It helps most with analysing tool output, following detailed policies, and long sequential decisions where mistakes are costly. It helps little for single or parallel tool calls and for simple instructions. It costs extra prompt and output tokens.

## What to do with it

- For current models, use extended or interleaved thinking first. Reach for a think-style tool only if your evals show a gain.
- In policy-heavy agents, put domain-specific reasoning examples (what to check before acting) in the system prompt rather than in the tool description.
- Measure consistency with pass^k, not only pass@k, when an agent must follow rules every time.

## Terms

- **think tool** — a tool with no side effects whose only input is free-text reasoning, giving the model a structured pause between steps.
- **pass^k** — the probability that all k independent trials of a task succeed.

## Caveats

- The editor's note on the page (Dec 15, 2025) says improved extended thinking should be preferred over a dedicated think tool in most cases. That largely supersedes the article's main advice.
- Results are for Claude 3.7 Sonnet. A footnote says Claude 3.5 Sonnet (New) also improved.
- The body text and the results table disagree on airline pass^1. The text gives 0.570 vs 0.370, but the table seems to show about 0.584 vs 0.332. The text's figures are used above.
- In retail, extended thinking scored below baseline, unexplained. The SWE-bench comparison used n=30 runs with the tool vs n=144 without. No author is named.
