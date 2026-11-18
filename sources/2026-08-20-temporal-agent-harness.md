---
type: source
title: "Temporal Agent Harness: An early look at durable agent infrastructure"
author: "Cornelia Davis"
publisher: Temporal
url: https://temporal.io/blog/temporal-agent-harness-durable-agent-infrastructure
published: 2026-08-20
ingested: 2026-11-17
kind: article
read: full
concepts: [agent-platforms, durable-execution, harness, production-operations]
---

# Temporal Agent Harness: An early look at durable agent infrastructure

**In one line:** Keep the agent SDK you already use as an *inner harness*, and wrap it in an *outer harness* that makes every turn, tool call and wait durable and gives your business rules a place to be enforced in code.

## What it says

- The problem framed: giving an agent capabilities is easy, giving it responsibility is hard, because responsibility needs control. An agent that acts for a business, not for one person, raises questions about data access, when a refund needs review, and what happens when infrastructure fails mid-request. Those are the business logic of the agent.
- Two unsatisfying choices today. Full harnesses (Claude Code, Codex) do a lot but leave little room to own those controls. Agent SDKs (OpenAI Agents SDK, PydanticAI, LangGraph, AWS Strands, Google ADK), which the post calls inner harnesses and commoditized, give control but leave a lot of infrastructure to build.
- An instruction such as "only access this customer's data" is not a control. Rules are only dependable when the harness applies them.
- The proposal is an outer harness around the inner one:
  - **Durable execution.** Every agent is a Temporal Workflow. It survives worker crashes and deploys, waits minutes or days, retries model and tool calls by policy, and resumes without re-running finished work.
  - **A seam at tool calls.** A policy layer sits at the point where the model has chosen a tool and the tool has not yet run. Approval is the first use: read an order freely, require a person before refunding one. Policies can be layered, changed at run time and scoped to tools or sessions.
  - **Turns, not only loops.** A turn invokes the inner harness once. A long interaction is many turns, started by a message, an approval, a timer or an outside event, with context carried between them.
  - **Typed agents.** Named operations with typed inputs and outputs, so agents can be called by programs and composed with other agents.
  - **Code mode under the same rules.** Model-written programs that call tools stay durable, observable and subject to the approval policies.
  - **Callback tools.** A tool that must run elsewhere (a user's laptop, a private network) is a typed request the agent durably waits on.
- All of it rests on one stream of structured agent events (turns, model calls, tool calls, approvals, hand-offs), grounded in the workflow's event history. Frontends, approval services, analytics and audit consume the stream without living inside the loop, and a past run can be played back from events instead of reconstructed by a model.
- Status: very early, before public preview. Integrations with Gemini, the OpenAI Agents SDK and PydanticAI.

## What to do with it

- Put approvals and business invariants at the point where a tool call is about to execute, in code.
- Model a long interaction as turns triggered by different events, not as one loop.
- Expose the run as an event stream that other services subscribe to.

## Terms

- **Inner harness / outer harness** — the agent SDK that runs the loop, and the layer around it that supplies durability and control points.
- **Turn** — one invocation of the inner harness within a longer interaction.

## Caveats

- A vendor's early announcement from August 2026, with APIs expected to change and no production evidence.
- It uses "harness" for agent SDKs, which this brain would call frameworks.
