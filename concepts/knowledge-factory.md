---
type: concept
title: "Knowledge factory"
updated: 2026-11-22
reviewed: 2026-11-22
status: evolving
---

# Knowledge factory

**Definition:** The system that collects, curates and maintains what a company knows about doing its work, in a form its agents can load. Working agents use the knowledge and flag what is missing or wrong, and a separate curator agent keeps it current. The name is one author's, from November 2026.

## Why it matters

A capable model with good tools still does not know which source the company trusts, what a metric means there, or how a report is expected to look. The best employees carry that in their heads, and much of it was never written down. Without a system that keeps it current, each agent run either lacks it or a person re-supplies it by hand. [Knowledge factory, Nov 2026](../sources/2026-11-21-chase-how-to-build-a-knowledge-factory.md)

The name comes from the **software factory**: a company's best engineers build the systems that let everyone build software, and agents write the code. The claim is that other knowledge work, such as presentations, launch videos and outbound sales, is going the same way, so the effort belongs in the knowledge and in the system that maintains it. [Knowledge factory, Nov 2026](../sources/2026-11-21-chase-how-to-build-a-knowledge-factory.md)

## Context and knowledge

**Context** is what an agent has available during one task. **Knowledge** is the reusable understanding that is maintained so the task is done correctly. Knowledge becomes context when it is loaded, and it is one part of the context: the facts of the task at hand come straight from the systems that hold them. [Knowledge factory, Nov 2026](../sources/2026-11-21-chase-how-to-build-a-knowledge-factory.md)

How much of either to load at each step is the subject of [context engineering](context-engineering.md). Where each piece is kept is the subject of the [context layer](context-layer.md).

## Three kinds of knowledge

[Knowledge factory, Nov 2026](../sources/2026-11-21-chase-how-to-build-a-knowledge-factory.md)

| Kind | The question it answers | Its usual state | Page |
|---|---|---|---|
| Skills | How is the work done properly here? | Passed between colleagues, seldom written | [Skills](skills.md) |
| Domain knowledge | How does the business work? Definitions, policies, facts about products, customers, competitors and the organisation | Written, but incomplete or wrong because there is so much of it. Changes slowly | [LLM wiki](llm-wiki.md) |
| Data access guidance | Where is current information, and how is it queried? | The data has a system of record. The instructions for reaching it are the new thing to maintain | [Retrieval](retrieval.md) |

## The parts

[Knowledge factory, Nov 2026](../sources/2026-11-21-chase-how-to-build-a-knowledge-factory.md)

- **Working agents** do the company's tasks and load the knowledge they need.
- **A flag tool** lets a working agent report knowledge it could not find or found to be wrong, and optionally suggest the correction.
- **A curator agent** runs in the background on a cadence and updates the knowledge. It reads the raw sources where knowledge is scattered (documents, chat, meeting notes), the agent traces, and the flags.
- **A knowledge store** holds the result. The format is called the least important choice and also the least settled one.

In this brain's vocabulary the curator is a [background agent](background-agents.md) started by a schedule, and its run is a form of dreaming (see [memory](memory.md)) whose input is wider than one agent's sessions. The store for domain knowledge is an [LLM wiki](llm-wiki.md), with two extra inputs to its maintenance: flags and traces. This mapping is this brain's reading.

## What to do

- Start with one recurring workflow, not with documentation. Run agents on it, look at where they struggle, and fill those gaps first. [Knowledge factory, Nov 2026](../sources/2026-11-21-chase-how-to-build-a-knowledge-factory.md)
- Give working agents a tool to flag missing or wrong knowledge, with room for a suggested fix. [Knowledge factory, Nov 2026](../sources/2026-11-21-chase-how-to-build-a-knowledge-factory.md)
- Keep the repair out of the working agents. They are pursuing their own task, and a store that each of them edits fills with contradictions. Run a separate curator on a schedule. [Knowledge factory, Nov 2026](../sources/2026-11-21-chase-how-to-build-a-knowledge-factory.md)
- Give the curator three inputs: the raw sources, the traces and the flags. Traces show how people actually use the agents, which is what gets written into skills. [Knowledge factory, Nov 2026](../sources/2026-11-21-chase-how-to-build-a-knowledge-factory.md)
- Keep every trace. A correction that a person makes in a session reaches the curator only through the record of that session. [Knowledge factory, Nov 2026](../sources/2026-11-21-chase-how-to-build-a-knowledge-factory.md) · [Chase, Apr 2026](../sources/2026-04-04-chase-continual-learning-for-ai-agents.md)
- Make agent output quick for a person to judge and correct. Review is how feedback reaches memory. [Proactive agents, Nov 2026](../sources/2026-11-17-langchain-proactive-agents.md)
- Leave data that has a complete and current source of truth where it is. Maintain the instructions for what lives where and how to query it, not a second copy. [Knowledge factory, Nov 2026](../sources/2026-11-21-chase-how-to-build-a-knowledge-factory.md)
- Do not design an elaborate storage format. Procedures go in skills, and files are enough for the rest until a standard appears. [Knowledge factory, Nov 2026](../sources/2026-11-21-chase-how-to-build-a-knowledge-factory.md) · [Chase, Jun 2026](../sources/2026-06-30-chase-wiki-memory.md)
- Check what the curator wrote against the record, on a routine. A wrong note keeps misleading every agent that loads it until something corrects it. [Agent memory, Nov 2026](../sources/2026-11-06-anthropic-components-of-agent-memory.md)

## A worked example

The article's own case is a revenue report at LangChain. [Knowledge factory, Nov 2026](../sources/2026-11-21-chase-how-to-build-a-knowledge-factory.md)

1. **Context.** The raw revenue figures, read from BigQuery and Salesforce.
2. **Knowledge.** A skill for writing reports in the house style, kept in GitHub. The definition of ARR, kept in the company wiki. Instructions for querying the two data systems, kept as skills.
3. **The run.** The agent finds that a column was renamed, works out the right one, and flags it with the new name.
4. **The correction.** A finance lead works with the agent on formatting and tells it that all company documents now need a new header.
5. **That night.** The curator reads the flag and the trace of the correction, and updates the data access skill and the report skill.

Two signals drive the loop: one from the agent (the flag) and one from a person (the correction in the trace).

## Where sources disagree

- **Who writes the knowledge.** A separate curator, because working agents leave contradictions. [Knowledge factory, Nov 2026](../sources/2026-11-21-chase-how-to-build-a-knowledge-factory.md) Or the working agent itself: in Anthropic's tests its newest models, given a memory folder and a statement of what it is for, kept a small set of useful notes without rules. [Agent memory, Nov 2026](../sources/2026-11-06-anthropic-components-of-agent-memory.md) The two are measured on different things. Anthropic's result is one agent's own notes on its own task. The article is about knowledge shared by many agents, and gives no measurement.
- **Who approves an update.** In the article's example the curator rewrites two skills overnight and no person signs off. [Knowledge factory, Nov 2026](../sources/2026-11-21-chase-how-to-build-a-knowledge-factory.md) A team that turns review misses into rules sets a bar first: the pattern must recur, several agents try to disprove it, and a person approves it. [Osmani, 17 Nov 2026](../sources/2026-11-17-osmani-claude-code-team-verification.md)
- **How much to write first.** Aim for an agent that needs no extra context from the person prompting, by writing down what lives in people's heads. [Cherny, 15 Jul 2026](../sources/2026-07-15-cherny-automation-is-the-highest-leverage.md) Do not document everything before agents start, and let the work show what is missing. [Knowledge factory, Nov 2026](../sources/2026-11-21-chase-how-to-build-a-knowledge-factory.md) These differ in order more than in aim.

## What the sources leave open

This section is this brain's reading. No source settles these.

- **Misses that leave no mark.** The loop learns from a miss that an agent flags or a person corrects. An agent has no reason to flag a stale fact that looks fine. Checking the store against its sources on a schedule is the known defence. [Agent memory, Nov 2026](../sources/2026-11-06-anthropic-components-of-agent-memory.md)
- **Practice against policy.** The curator reads chat and meeting notes as well as official documents. Suppose a hotel's policy page sets a fee for late checkout, a manager writes in chat that regular guests are never charged, and the traces show guests complaining about the fee. The article does not say which of these the curator should write down, or who decides. Tacit practice is what the factory exists to capture, and it is also what an owner may not want made into a rule.
- **A wider way in for bad instructions.** Whatever the curator writes is later loaded as trusted context by every agent. Chat messages and transcripts are content written by many people, and memory files are already a known route for poisoning. [Containing Claude, May 2026](../sources/2026-05-25-anthropic-how-we-contain-claude.md) See [permissions and sandboxing](sandboxing-and-permissions.md).
- **Work where a miss is expensive.** Learning from use suits work in which a mistake shows up quickly and costs little, such as a draft that a person rejects. Where a mistake is found late and cannot be undone, such as a missed legal deadline, the first runs need a person in the loop or a rehearsal on past cases. The general advice is to delegate fully only where being wrong is cheap. [Osmani, 3 Nov 2026](../sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md) See [side effects and approvals](side-effects.md) and [human judgment](human-judgment.md).
- **Knowledge that is used once.** The definition covers what is reused. What a single piece of work is for (this customer, this event, this audience) is context for one task and stays with the person or the brief.

## Related

[Memory](memory.md) · [LLM wiki](llm-wiki.md) · [Compounding](compounding.md) · [Skills](skills.md) · [Context layer](context-layer.md) · [Background agents](background-agents.md) · [Retrieval](retrieval.md) · [Human judgment](human-judgment.md)
