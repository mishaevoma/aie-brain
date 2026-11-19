# AI Engineering Brain

A dated, cited wiki of AI engineering practice, compiled into high-signal knowledge your agent can load. It is a compounding, agent-maintained wiki in the Karpathy LLM-wiki pattern: immutable dated sources, cited playbooks, and a freshness linter that flags stale or unbacked claims. Your agent reviews a project against that evidence and returns findings you can verify. A green test run that tested nothing is the kind of miss it catches.

## Get your first review

Open your coding agent **in the project you want reviewed**. With access to your checkout and public Markdown, it can run the review without an install. Paste this into chat.

```text
Review this project using
https://mishaevoma.github.io/aie-brain/review.md
```

The review is read-only. The result appears in the same chat, under your agent’s usual data settings and model usage.

### What comes back

![Three upgrades in twelve seconds, each named by the part of the stack it improves. Harness: start simple, a workflow before an agent. Tools: an action that changes the world needs a plan for running twice. Memory: keep what is always loaded small, and correct notes against evidence. Under each, the file and line, a check and a dated source.](.github/review-demo.gif)

Each scene names the part of [the stack](overview.md#the-stack) and the practice, then shows evidence from a real review of a sample project: [the harness](evals/runs/2026-11-19-published-codex/04-multi-agent/review.md), [the tools](evals/runs/2026-11-19-published-codex/03-tool-agent/review.md) and [the memory](evals/runs/2026-11-19-showcase-memory-codex/08-memory-agent/review.md).

On a small support agent that issues refunds, the review led with this upgrade. Here it is, shortened.

> **1. Prevent duplicate payments after a timeout.** `agent.py:16` retries every exception from every tool. `tools.py:42` sends writes without an idempotency key. A payment can commit before its response is lost, and the retry can then pay again.
>
> **Change.** Keep bounded retries for reads. For refunds and emails, require the receiver to deduplicate on a stable operation identifier that survives retries and queue redelivery.
>
> **Check.** The simulation prints `retry: error 3`: three simulated commits, then an error. Add a commit-then-timeout test and a redelivery test. Both must produce exactly one external effect.
>
> **Why and evidence.** [Side effects](concepts/side-effects.md), [Temporal source note](sources/2026-11-04-temporal-deciding-what-survives-failure.md), [original publication](https://temporal.io/blog/durable-execution-means-deciding-what-survives-failure), 4 November 2026, 15 days old.
>
> **Effort and impact.** Small immediate retry-policy change, moderate work for durable deduplication. Prevents duplicate refunds and messages.

Every upgrade carries those five parts, and a source older than 12 months is labelled as older. You can inspect the evidence, narrow the review (“follow one customer email through a retry”), or reply “make upgrade 1 and run the check.” When nothing needs upgrading, the review says so.

The review is tested on a set of sample projects. One has planted issues and one has no AI at all. [See the latest scorecard](evals/scorecard.md)

Some agents cannot read the review URL with their web tool: Codex fails to open the site, and Claude Code gets a summary in place of the file. Both then fetch it with `curl`, so allow that command when your agent asks. If your agent can reach GitHub but not the site, use the same prompt with [the skill on GitHub](https://github.com/mishaevoma/aie-brain/blob/main/.agents/skills/brain-consult/SKILL.md). An agent with no network access at all cannot load the review, and should tell you so.

## Keep it in your agent

For repeat reviews, install the skill from your project directory with Node.js and npm. On first use it can download the wiki to `~/.aie-brain` using Git and a POSIX shell. A web-enabled agent can also consult the public copy.

```sh
npx skills add mishaevoma/aie-brain --skill brain-consult
```

Select your agent, start a new session in the same project, and say **“Use brain-consult to review this project.”** You can also point it at a design document or ask a focused question such as “Do we need a second agent for this step?”

<details>
<summary>Global install, updates, and existing wiki checkouts</summary>

Add `-g` to the install command to use the skill across projects. Update a project install with `npx skills update brain-consult -p`. Set `AIE_BRAIN` to the path of a wiki checkout you already maintain.

For an agent that reads project instructions, clone the wiki once.

```sh
git clone https://github.com/mishaevoma/aie-brain ~/.aie-brain
```

Add this line to the project's `AGENTS.md` or the instruction file your agent reads.

```markdown
For an AI engineering question or project review, follow ~/.aie-brain/.agents/skills/brain-consult/SKILL.md.
```

For a team using a wiki submodule, substitute its project-relative path.

</details>

## Read the wiki

Start with a decision such as “How do I know the agent did the right thing?” The index takes you to a playbook or concept, then to a dated source note and the original publication. Agents maintain the summaries. Check the original when a number or assumption matters to your design. The overview records disagreements and gaps in coverage.

[Browse the wiki](https://mishaevoma.github.io/aie-brain/) · [Index by decision](index.md#by-decision) · [Overview](overview.md) · [Glossary](glossary.md) · [Markdown index for agents](https://mishaevoma.github.io/aie-brain/llms.txt)

## Work on the wiki

In a wiki checkout, ask your agent to **ingest a source** by URL, **refresh** the watchlist, or **lint** the wiki. To cite a review later, keep the wiki revision that the agent reports. [Repository guide](AGENTS.md) · [Watchlist](watchlist.md) · [Sources considered](considered.md) · [Change log](log.md)

Run `python3 tools/lint.py` to check citations and links. Use `--ages` to inspect the age of the evidence. For a wiki edit, `--sync --log "edit | Title"` regenerates the index and backlinks and records the change. For changes to the review skill or its public URL, run `python3 site/test_review_publication.py`, then rerun the review on the sample projects as [the eval runbook](evals/README.md) describes. All of it uses the Python standard library.

## Licence

The repository's own text and code use the [MIT licence](LICENSE). The original articles, posts and videos remain their authors’ work.
