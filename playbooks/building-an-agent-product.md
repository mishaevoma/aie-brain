---
type: playbook
title: "Building an agent product"
updated: 2026-11-17
reviewed: 2026-11-17
---

# Building an agent product

The order of decisions when turning an idea into an AI product that acts. Each step names the concept page with the detail. Stop at the first step that already solves your problem.

## 1. Decide how much autonomy the task needs

- Try one model call with retrieval and examples first. [Building effective agents, Dec 2024](../sources/2024-12-19-anthropic-building-effective-agents.md)
- If the steps are known in advance, build a workflow. If the path depends on what the model finds, build an agent. [Building effective agents, Dec 2024](../sources/2024-12-19-anthropic-building-effective-agents.md)
- Check that success can be verified and that a person can oversee it. If not, fix that before anything else. [Building effective agents, Dec 2024](../sources/2024-12-19-anthropic-building-effective-agents.md)

Detail: [agents and workflows](../concepts/agents-and-workflows.md).

## 2. Pick the model, adopt a harness

- Use an existing harness or agent SDK and configure it. Writing your own loop is rarely where the value is. [Theo, 22 Oct 2026](../sources/2026-10-22-theo-what-is-a-harness.md) · [Every, Aug 2026](../sources/2026-08-25-every-shared-company-agent.md)
- Keep your own logic in the parts that carry over: tools, instructions, skills, data access. [Theo video, 30 Oct 2026](../sources/2026-10-30-theo-my-last-video-about-ai-harnesses.md) · [Chase, Apr 2026](../sources/2026-04-04-chase-continual-learning-for-ai-agents.md)

Detail: [harness](../concepts/harness.md), [context layer](../concepts/context-layer.md).

## 3. Design the tools

- Offer a few task-shaped tools with descriptions written like a briefing, outputs the model can use, and errors that say what to do next. [Writing tools for agents, Sep 2025](../sources/2025-09-11-anthropic-writing-tools-for-agents.md)
- Reach outside systems through MCP servers or command-line tools, and watch what their definitions cost in context. [Advanced tool use, Nov 2025](../sources/2025-11-24-anthropic-advanced-tool-use.md)

Detail: [tool design](../concepts/tool-design.md), [MCP](../concepts/mcp.md).

## 4. Shape what the model sees

- Start with a minimal system prompt and add instructions only for failures you observe. [Context engineering, Sep 2025](../sources/2025-09-29-anthropic-context-engineering.md)
- Load on demand: references and search instead of everything up front, procedures as skills. [Context engineering, Sep 2025](../sources/2025-09-29-anthropic-context-engineering.md) · [Agent Skills, Oct 2025](../sources/2025-10-16-anthropic-agent-skills.md)
- If tasks run long, decide now between compaction, notes on disk and subagents, and keep the full log outside the context window. [Context engineering, Sep 2025](../sources/2025-09-29-anthropic-context-engineering.md) · [Managed Agents, Apr 2026](../sources/2026-04-08-anthropic-managed-agents.md)

Detail: [context engineering](../concepts/context-engineering.md), [retrieval](../concepts/retrieval.md), [memory](../concepts/memory.md).

## 5. Define done and let the agent check it

- Decide what evidence counts as finished before the work starts. [Osmani, 3 Nov 2026](../sources/2026-11-03-osmani-critical-thinking-when-agents-do-the-work.md)
- Give the agent a way to run the real thing and see the result. [Osmani, 17 Nov 2026](../sources/2026-11-17-osmani-claude-code-team-verification.md)
- For multi-hour work, add a separate evaluator and state kept on disk. [Harness design, Mar 2026](../sources/2026-03-24-anthropic-harness-design-long-running-apps.md) · [Long-running harnesses, Nov 2025](../sources/2025-11-26-anthropic-harnesses-long-running-agents.md)

Detail: [verification](../concepts/verification.md), [long-running agents](../concepts/long-running-agents.md).

## 6. Write the first evals

- Collect 20 to 50 tasks from real failures and grade the end state. [Demystifying evals, Jan 2026](../sources/2026-01-09-anthropic-demystifying-evals.md)
- Add a small behavioural check for each failure mode you see. [Google, Sep 2026](../sources/2026-09-09-google-anatomy-of-harness-engineering.md)
- Read transcripts before believing a score. [Demystifying evals, Jan 2026](../sources/2026-01-09-anthropic-demystifying-evals.md)

Detail: [evals](../concepts/evals.md), [trusting eval numbers](../concepts/eval-validity.md).

## 7. Contain it

- Build the boundary first: scoped filesystem, default-deny network, credentials kept outside. [Containing Claude, May 2026](../sources/2026-05-25-anthropic-how-we-contain-claude.md) · [Claude Code sandboxing, Oct 2025](../sources/2025-10-20-anthropic-claude-code-sandboxing.md)
- Add approvals or a classifier as a second layer, not as the boundary. [Auto mode, Mar 2026](../sources/2026-03-25-anthropic-claude-code-auto-mode.md)

Detail: [permissions, sandboxing and containment](../concepts/sandboxing-and-permissions.md).

## 8. Ship and watch

- Run quality checks against the production path and gate harness changes like model changes. [Anthropic postmortem, Sep 2025](../sources/2025-09-17-anthropic-postmortem-three-issues.md) · [Claude Code postmortem, Apr 2026](../sources/2026-04-23-anthropic-claude-code-quality-postmortem.md)
- Make runs resumable and deploys safe for agents that are mid-task. [Multi-agent research system, Jun 2025](../sources/2025-06-13-anthropic-multi-agent-research-system.md) · [Managed Agents, Apr 2026](../sources/2026-04-08-anthropic-managed-agents.md)

Detail: [running agents in production](../concepts/production-operations.md).

## 9. Keep it improving

- Turn every repeated correction into a check, a rule or a skill, and prune what stops earning its place. [Cherny, 15 Jul 2026](../sources/2026-07-15-cherny-automation-is-the-highest-leverage.md) · [Osmani, 17 Nov 2026](../sources/2026-11-17-osmani-claude-code-team-verification.md)
- At each model release, remove scaffolding piece by piece and keep what still carries load. [Harness design, Mar 2026](../sources/2026-03-24-anthropic-harness-design-long-running-apps.md)
- Add more agents only when the work separates cleanly and your checks can keep up. [Multi-agent research system, Jun 2025](../sources/2025-06-13-anthropic-multi-agent-research-system.md) · [C compiler, Feb 2026](../sources/2026-02-05-anthropic-building-c-compiler.md)

Detail: [compounding](../concepts/compounding.md), [multi-agent systems](../concepts/multi-agent-systems.md), [human judgment](../concepts/human-judgment.md).
