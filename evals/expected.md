# What a good review finds

The answer key for the fixtures in `fixtures/`. A reviewer never sees this file: `run.py` copies each fixture out of the repository before the agent starts.

Each fixture lists the upgrades a maintainer would accept, what is already right, and what would be an invented finding. An upgrade not listed here can still count, if it is true of the code, backed by a page of this wiki and worth doing. Score it with the rubric in [the runbook](README.md).

## 01-llm-wrapper

One call that turns a staged diff into a commit message.

| ID | Upgrade | Where | Wiki |
|---|---|---|---|
| W1 | The three example diffs with reference messages are compared by eye. Turn them into a small eval with yes/no checks and rerun it on every prompt or model change. | `README.md` "Changing the prompt", `examples/` | [Evals](../concepts/evals.md) |
| W2 | The tests use a fake client, so a green run says nothing about a prompt change, which is what the README runs them for. | `test_commitmsg.py`, `README.md` | [Verification](../concepts/verification.md) |
| W3 | The whole staged diff is sent, with no filter or size limit. A lockfile or generated file goes in whole. | `commitmsg.py`, `staged_diff` and `build_prompt` | [Context engineering](../concepts/context-engineering.md) |

Already right: one model call with no loop, tools or second agent. Advice to add an agent framework, a sandbox, durable execution or more agents is an invented finding here.

## 02-rag-app

Question answering over a handbook of about 1.4 million tokens.

| ID | Upgrade | Where | Wiki |
|---|---|---|---|
| R1 | `data/asked.csv` already pairs 16 real questions with the file that answers each. Nothing reads it. Score retrieval with it before changing anything else. | `data/asked.csv`, `README.md` "Known problems" | [Evals](../concepts/evals.md), [Retrieval](../concepts/retrieval.md) |
| R2 | Embeddings alone miss exact identifiers such as `EXP-204`. Add keyword search (BM25) beside them. | `qa.py`, `retrieve` | [Retrieval](../concepts/retrieval.md) |
| R3 | Chunks are cut every 400 characters with nothing saying where they came from. Add context to each chunk before indexing. | `ingest.py`, `chunk` | [Retrieval](../concepts/retrieval.md) |
| R4 | The superseded 2024 expenses policy in `docs/archive/` is indexed beside the 2026 one. A stale version of a fact is the most harmful kind of filler. | `ingest.py`, `DOCS.rglob`; `docs/archive/expenses-2024.md` | [Context engineering](../concepts/context-engineering.md) |
| R5 | 25 chunks and the whole conversation go into every prompt. Rerank and keep the final list short. | `qa.py`, `TOP_K` and `build_prompt` | [Retrieval](../concepts/retrieval.md), [Context engineering](../concepts/context-engineering.md) |

Already right: building retrieval at all. The README gives the corpus size, which is far above what fits in a prompt. "Skip retrieval and put it all in the prompt" is wrong here.

Most sources behind R2, R3 and R5 are older than 12 months. A review has to say so and say why the advice still holds.

## 03-tool-agent

A support agent with three tools, each wrapped in the same retry.

| ID | Upgrade | Where | Wiki |
|---|---|---|---|
| T1 | `issue_refund` is retried after a timeout with no idempotency key, so a refund that reached the payments service is sent again. `test_refund_is_retried_after_a_timeout` asserts the second call. | `agent.py`, `call_with_retry`; `tools.py`, `issue_refund`; `test_agent.py` | [Side effects and approvals](../concepts/side-effects.md) |
| T2 | Every tool gets the same retry. Declare for each tool whether it may run twice. `send_email` has the same problem as the refund. | `agent.py`, `call_with_retry` | [Side effects and approvals](../concepts/side-effects.md) |
| T3 | A failed tool returns the string `"error"`, and the descriptions are four words long. The model cannot tell a timeout from a refusal, or what to do next. | `agent.py`, `call_with_retry`; `tools.py`, `TOOL_DEFINITIONS` | [Tool design](../concepts/tool-design.md) |
| T4 | Nothing measures whether the agent refunds the right amount. | whole project | [Evals](../concepts/evals.md) |

Already right: the step limit (`MAX_STEPS`), retrying the read-only lookup, and stopping for a person above 200 EUR, decided in code and not by the model.

## 04-multi-agent

Four "agents" that write release notes from a list of merged pull requests.

| ID | Upgrade | Where | Wiki |
|---|---|---|---|
| M1 | The path is fixed: plan, summarise, write, critique. That is a workflow, and the Planner's output is used by nobody but the Researcher's prompt. Make it a prompt chain in code, or one call. | `crew.py`, `run` | [Agents and workflows](../concepts/agents-and-workflows.md), [Multi-agent systems](../concepts/multi-agent-systems.md) |
| M2 | The Writer sees only the Researcher's summary, never the pull requests. This is how "removed the export endpoint" became "new export API". Keep the original reachable. | `crew.py`, `notes = ask(WRITER, research, client)` | [Context engineering](../concepts/context-engineering.md), [Multi-agent systems](../concepts/multi-agent-systems.md) |
| M3 | The critic loop has no round limit (`while True`), which is the run that "never finished". Cap the rounds and hand over to a person. | `crew.py`, `while True` | [Verification](../concepts/verification.md), [Agents and workflows](../concepts/agents-and-workflows.md) |
| M4 | The rewrite prompt carries the whole transcript, which grows every round. | `crew.py`, rewrite call | [Context engineering](../concepts/context-engineering.md) |

Already right: nothing to protect here. A review that only says "consider fewer agents" without naming the fixed sequence in `run` is generic.

## 05-plain-app

A helpdesk with one model call that tags each new ticket.

| ID | Upgrade | Where | Wiki |
|---|---|---|---|
| P1 | 40 tickets labelled by the support lead sit unused in `data/labelled_tickets.csv`. Run `tag_ticket` over them, report accuracy, and rerun on every prompt or model change. | `data/labelled_tickets.csv`, `app/tagging.py` | [Evals](../concepts/evals.md) |
| P2 | The model's reply is stored as the category without checking it is one of the four. `list --category` then never shows that ticket. | `app/tagging.py`, last line; `app/cli.py`, `add` | [Tool design](../concepts/tool-design.md) (treat model output as a proposal), or the reviewer's own judgement, labelled |
| P3 | The tagging tests use a canned reply, so they show nothing about tagging quality. | `tests/test_tagging.py` | [Verification](../concepts/verification.md) |

Already right: one direct model call for a small classification job. Advice to make it an agent, add tools or add retrieval is an invented finding.

## 06-no-ai-control

A pure-Python library with no model call, a short `AGENTS.md`, real tests and CI that runs them.

Expected: the review says there is no AI feature to review and that the coding-agent setup works on the path it checked, names what to keep, and offers one focused question. It proposes no change.

Any **Change** presented as a gap is an invented finding. So is advice with no location in this project ("add a verify skill", "turn on a sandbox", "add evals") when the test command, `AGENTS.md` and CI already cover what a one-function library needs.

## 07-seeded

An email assistant with five planted issues. Recall is counted against these.

| ID | Planted issue | Where | Wiki |
|---|---|---|---|
| S1 | **Misleading green tests.** `make test` reports OK with 4 of 5 tests skipped. They need `ASSISTANT_LIVE_TESTS=1`, which nothing sets. The one test that runs checks an import. `AGENTS.md` calls this the gate before every commit. | `tests/test_agent.py`, the two `skipUnless` lines; `Makefile`; `AGENTS.md` | [Verification](../concepts/verification.md), [Setting up a repository](../playbooks/setting-up-a-repo-for-coding-agents.md) step 2 |
| S2 | **A send that may run twice.** `send_reply` goes through `with_retries` like the lookup, with no idempotency key. A timeout after the mail service accepted the message sends the customer a second reply. | `assistant/agent.py`, `with_retries` and its call; `assistant/tools.py`, `send_reply` | [Side effects and approvals](../concepts/side-effects.md) |
| S3 | **No evals.** Quality is "read a few sent replies when a customer complains". | `README.md` "Quality" | [Evals](../concepts/evals.md), [Error analysis](../concepts/error-analysis.md) |
| S4 | **Prompt in code with no version and no check.** The system prompt is an f-string inside `reply_to`, "tweaked a few times since" October, and no test or eval runs when it changes. This is the coverage probe: the wiki has no page on it, only lines on two pages. | `assistant/agent.py`, `system = f"""…` | [Running agents in production](../concepts/production-operations.md), [Evals](../concepts/evals.md) |
| S5 | **Unbounded context.** Every email the customer ever sent and the whole `kb/` folder go into the system prompt of every call. | `assistant/context.py`, `build_context` | [Context engineering](../concepts/context-engineering.md) |

A planted issue counts as found when the review names the right file and the right problem. Naming the theme alone ("consider adding tests") does not count.

## What the wiki cannot answer

If a review of these fixtures wants to advise on any of the gaps listed under "What this brain does not cover yet" in [the overview](../overview.md), the right outcome is to say the wiki is silent and ask one focused question. Advice on those topics presented as if the wiki backed it is an invented finding.
