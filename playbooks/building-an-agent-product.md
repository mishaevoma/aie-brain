---
type: playbook
title: "Building an agent product"
updated: 2026-11-18
reviewed: 2026-11-17
---

# Building an agent product

The order of decisions when turning an idea into an AI product that acts. Each step names the concept page with the detail. Stop at the first step that already solves your problem.

## 1. Decide how much autonomy the task needs

- Try one model call with retrieval and examples first. [Building effective agents, Dec 2024](../sources/2024-12-19-anthropic-building-effective-agents.md)
- If the steps are known in advance, build a workflow. If the path depends on what the model finds, build an agent. [Building effective agents, Dec 2024](../sources/2024-12-19-anthropic-building-effective-agents.md)
- Check that success can be verified and that a person can oversee it. If not, fix that before anything else. [Building effective agents, Dec 2024](../sources/2024-12-19-anthropic-building-effective-agents.md)
- Count the steps the task needs. Errors multiply: at 95% accuracy per step, 10 steps succeed 60% of the time. [Huyen, Jan 2025](../sources/2025-01-07-huyen-agents.md)

Detail: [agents and workflows](../concepts/agents-and-workflows.md).

## 2. Pick the model, adopt a harness

- Use an existing harness or agent SDK and configure it. Writing your own loop is rarely where the value is. [Theo, 22 Oct 2026](../sources/2026-10-22-theo-what-is-a-harness.md) · [Every, Aug 2026](../sources/2026-08-25-every-shared-company-agent.md)
- Keep your own logic in the parts that carry over: tools, instructions, skills, data access. [Theo video, 30 Oct 2026](../sources/2026-10-30-theo-my-last-video-about-ai-harnesses.md) · [Chase, Apr 2026](../sources/2026-04-04-chase-continual-learning-for-ai-agents.md)
- One builder argues for an exception: a customer-facing feature where you must control the exact prompt and pause before each action. There, own the loop. [12-Factor Agents, Mar 2025](../sources/2025-03-30-humanlayer-12-factor-agents.md)

Detail: [harness](../concepts/harness.md), [context layer](../concepts/context-layer.md).

## 3. Design the tools

- Offer a few task-shaped tools with descriptions written like a briefing, outputs the model can use, and errors that say what to do next. [Writing tools for agents, Sep 2025](../sources/2025-09-11-anthropic-writing-tools-for-agents.md)
- Reach outside systems through MCP servers or command-line tools, and watch what their definitions cost in context. [Advanced tool use, Nov 2025](../sources/2025-11-24-anthropic-advanced-tool-use.md)

Detail: [tool design](../concepts/tool-design.md), [MCP](../concepts/mcp.md).

## 4. Shape what the model sees

- Start with a minimal system prompt and add instructions only for failures you observe. [Context engineering, Sep 2025](../sources/2025-09-29-anthropic-context-engineering.md)
- Load on demand: references and search instead of everything up front, procedures as skills. [Context engineering, Sep 2025](../sources/2025-09-29-anthropic-context-engineering.md) · [Agent Skills, Oct 2025](../sources/2025-10-16-anthropic-agent-skills.md)
- Send the relevant parts, not everything that fits. In one test every model did worse with a full history than with the relevant extract from it. [Context rot, Jul 2025](../sources/2025-07-14-chroma-context-rot.md)
- If tasks run long, decide now between compaction, notes on disk and subagents, and keep the full log outside the context window. [Context engineering, Sep 2025](../sources/2025-09-29-anthropic-context-engineering.md) · [Managed Agents, Apr 2026](../sources/2026-04-08-anthropic-managed-agents.md)

Detail: [context engineering](../concepts/context-engineering.md), [retrieval](../concepts/retrieval.md), [memory](../concepts/memory.md).

## 5. Define done and let the agent check it

- Decide what evidence counts as finished before the work starts. [Osmani, 3 Nov 2026](../sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md)
- Give the agent a way to run the real thing and see the result. [Osmani, 17 Nov 2026](../sources/2026-11-17-osmani-claude-code-team-verification.md)
- For multi-hour work, add a separate evaluator and state kept on disk. [Harness design, Mar 2026](../sources/2026-03-24-anthropic-harness-design-long-running-apps.md) · [Long-running harnesses, Nov 2025](../sources/2025-11-26-anthropic-harnesses-long-running-agents.md)

Detail: [verification](../concepts/verification.md), [long-running agents](../concepts/long-running-agents.md).

## 6. Write the first evals

- Read real interactions first. Note each failure, group and count the failures, and let the largest groups decide the first tests. With no users yet, generate the inputs. [Husain field guide, Mar 2025](../sources/2025-03-24-husain-field-guide-improving-ai-products.md)
- Collect 20 to 50 tasks from real failures and grade the end state. [Demystifying evals, Jan 2026](../sources/2026-01-09-anthropic-demystifying-evals.md)
- Add a small behavioural check for each failure mode you see. [Google, Sep 2026](../sources/2026-09-09-google-anatomy-of-harness-engineering.md)
- Read transcripts before believing a score. [Demystifying evals, Jan 2026](../sources/2026-01-09-anthropic-demystifying-evals.md)

Detail: [evals](../concepts/evals.md), [trusting eval numbers](../concepts/eval-validity.md).

## 7. Contain it

- Build the boundary first: scoped filesystem, default-deny network, credentials kept outside. [Containing Claude, May 2026](../sources/2026-05-25-anthropic-how-we-contain-claude.md) · [Claude Code sandboxing, Oct 2025](../sources/2025-10-20-anthropic-claude-code-sandboxing.md)
- Add approvals or a classifier as a second layer, not as the boundary. [Auto mode, Mar 2026](../sources/2026-03-25-anthropic-claude-code-auto-mode.md)
- Check each agent, and each set of tools connected to it, for the lethal trifecta: private data, untrusted content and a way to send data out. Remove one of the three. [Lethal trifecta, Jun 2025](../sources/2025-06-16-willison-lethal-trifecta.md)

Detail: [permissions, sandboxing and containment](../concepts/sandboxing-and-permissions.md).

## 8. Decide where it runs

- Skip this step while the agent is an interactive session on one machine; that is this brain's reading. Once it must run unattended, wait for people or serve several users, it needs what one vendor lists as a production runtime: durable execution, interrupt and resume, sandboxes, multi-tenancy. [Deep Agents runtime, Apr 2026](../sources/2026-04-20-langchain-runtime-behind-deep-agents.md)
- Keep the session record outside every process and sandbox, run the loop outside the sandbox, and make workers and sandboxes disposable. [Shopify, May 2026](../sources/2026-05-28-shopify-under-the-river.md) · [Managed Agents, Apr 2026](../sources/2026-04-08-anthropic-managed-agents.md)
- Choose how a run survives a crash (recorded steps, checkpoints or a session log), then decide for each tool whether it may run twice. [Determinism, Nov 2025](../sources/2025-11-24-vanlightly-determinism-in-durable-execution.md) · [Building LangGraph, Sep 2025](../sources/2025-09-04-langchain-building-langgraph.md) · [Managed Agents, Apr 2026](../sources/2026-04-08-anthropic-managed-agents.md) · [Durable harness, Oct 2026](../sources/2026-10-19-vercel-making-every-harness-durable.md)
- Decide whose authority the agent acts under, and keep credentials out of the sandbox. [Uber, May 2026](../sources/2026-05-21-uber-solving-identity-crisis-for-ai-agents.md) · [Notion, Feb 2026](../sources/2026-02-27-notion-security-in-custom-agents.md) · [Managed Agents, Apr 2026](../sources/2026-04-08-anthropic-managed-agents.md)
- Rent when one lab's models are enough and the session may sit on its servers, or rent from a cloud and attach the runtime to your own network. Build when you need to switch model providers, change the platform at your product's pace, read every trace, or keep code and customer data away from any third party. Either way keep your own copy of the session log. This is this brain's reading of the positions in these sources. [Plumbing wars, Apr 2026](../sources/2026-04-28-proctor-plumbing-wars.md) · [Laminar, Oct 2026](../sources/2026-10-20-ramp-building-laminar.md) · [DoorDash, Aug 2026](../sources/2026-08-11-doordash-cloud-based-agents.md) · [Sierra, Jul 2026](../sources/2026-07-29-sierra-agency-sandboxes-for-agents.md) · [Axonius, Aug 2026](../sources/2026-08-18-aws-axonius-multi-tenant-agents.md) · [Session portability, Jul 2026](../sources/2026-07-30-earendil-session-you-cannot-take-with-you.md)

Detail: [agent platforms](../concepts/agent-platforms.md), [durable execution](../concepts/durable-execution.md), [side effects and approvals](../concepts/side-effects.md), [managed agent runtimes](../concepts/managed-agent-runtimes.md), [agent identity and tenancy](../concepts/agent-identity.md), [background agents](../concepts/background-agents.md).

## 9. Ship and watch

- Run quality checks against the production path and gate harness changes like model changes. [Anthropic postmortem, Sep 2025](../sources/2025-09-17-anthropic-postmortem-three-issues.md) · [Claude Code postmortem, Apr 2026](../sources/2026-04-23-anthropic-claude-code-quality-postmortem.md)
- Make runs resumable and deploys safe for agents that are mid-task. [Multi-agent research system, Jun 2025](../sources/2025-06-13-anthropic-multi-agent-research-system.md) · [Managed Agents, Apr 2026](../sources/2026-04-08-anthropic-managed-agents.md)
- Let a run pause for a person and resume: store it as a thread of events, and make asking a person an output the model can choose. [12-Factor Agents, Mar 2025](../sources/2025-03-30-humanlayer-12-factor-agents.md)
- Pin running agents to the release they started on, and put a queue with limits in front of unattended work. [Updating agents safely, Mar 2026](../sources/2026-03-11-restate-updating-agents-safely.md) · [Harvey talk, Nov 2026](../sources/2026-11-11-harvey-harness-has-to-finish-the-job.md)

Detail: [running agents in production](../concepts/production-operations.md).

## 10. Keep it improving

- Turn every repeated correction into a check, a rule or a skill, and prune what stops earning its place. [Cherny, 15 Jul 2026](../sources/2026-07-15-cherny-automation-is-the-highest-leverage.md) · [Osmani, 17 Nov 2026](../sources/2026-11-17-osmani-claude-code-team-verification.md)
- At each model release, remove scaffolding piece by piece and keep what still carries load. [Harness design, Mar 2026](../sources/2026-03-24-anthropic-harness-design-long-running-apps.md)
- Add more agents only when the work separates cleanly and your checks can keep up. [Multi-agent research system, Jun 2025](../sources/2025-06-13-anthropic-multi-agent-research-system.md) · [C compiler, Feb 2026](../sources/2026-02-05-anthropic-building-c-compiler.md) · [Cognition, Jun 2025](../sources/2025-06-12-cognition-dont-build-multi-agents.md)

Detail: [compounding](../concepts/compounding.md), [multi-agent systems](../concepts/multi-agent-systems.md), [human judgment](../concepts/human-judgment.md).
