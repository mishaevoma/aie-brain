# Considered, not ingested

Sources that were looked at and left out. `brain-ingest` and `brain-refresh` check this list before proposing anything, so the same item is not weighed twice.

Rules:

- One row per source, with the date it was considered, a link, the outcome and a one-line reason.
- Outcomes: `no material` (it adds nothing the brain can use) or `owner passed` (the owner turned it down).
- This repository is public. Give a reason about fit, such as "repeats the note on X", "announcement with no practice" or "outside the brain's scope". Never a judgement of the author.
- If a source here is ingested later, remove its row in the same change. The lint fails when a link is both here and in `sources/`.

| Date | Source | Outcome | Reason |
|---|---|---|---|
| 2026-11-17 | [Minions: Stripe’s one-shot, end-to-end coding agents](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents) | no material | Part 1 of a series; repeats the note on part 2, which covers the same system in more depth. |
| 2026-11-17 | [Who needs workflows when you have agents?](https://temporal.io/blog/who-needs-workflows-when-you-have-agents) | no material | Repeats the notes on mixing fixed steps and agent steps (Stripe, Dropbox, DoorDash). |
| 2026-11-17 | [How a durable workflow engine works: you might not need a queue](https://www.inngest.com/blog/how-durable-workflow-engines-work) | no material | General explainer; repeats the notes on durable execution. |
| 2026-11-17 | [The thread is the Workflow](https://temporal.io/blog/manetu-the-thread-is-the-workflow) | no material | Repeats the note on running the Pi harness on Temporal. |
| 2026-11-17 | [Durable Task extension for Microsoft Agent Framework](https://learn.microsoft.com/en-us/azure/durable-task/sdks/durable-agents-microsoft-agent-framework) | no material | Setup guide with no practice beyond the notes on durable execution. |
| 2026-11-17 | [What's This Golem Cloud Thing About?](https://golem.cloud/blog/whats-this-golem-cloud-thing-about/) | no material | Product description with no production practice to act on. |
| 2026-11-17 | [What's New in Dapr 1.19](https://www.diagrid.io/blog/dapr-1-19-release-highlights) | no material | Release notes. |
| 2026-11-17 | [Agents That Survive a Crash Without Paying for the Same Tokens Twice](https://www.union.ai/blog-post/agents-that-survive-a-crash-without-paying-for-the-same-tokens-twice) | no material | Short tip; repeats the notes on recording model calls. |
| 2026-11-17 | [A platform engineer's guide to workflow orchestration](https://vercel.com/i/workflow-orchestration) | no material | General explainer. |
| 2026-11-17 | [Lambda durable functions: Real implementation notes](https://depot.dev/blog/lambda-durable-implementation) | no material | Not about agents. |
| 2026-11-17 | [Decomposed Durability for Data Workflows](https://www.prefect.io/blog/decomposed-durability-a-different-approach-to-durable-execution) | no material | About data workflows, outside the brain's scope. |
| 2026-11-17 | [Bringing more agent harnesses and frameworks to Cloudflare, starting with Flue](https://blog.cloudflare.com/agents-platform-flue-sdk) | no material | Its practice is covered by the notes on Cloudflare's agent documentation. |
| 2026-11-17 | [Why managed agents are the next big thing in agent building](https://www.langchain.com/blog/why-managed-agents-are-the-next-big-thing-in-agent-building) | no material | An argument with no practice or figures; other notes cover the build-or-rent positions. |
| 2026-11-17 | [Introducing eve 1.0](https://vercel.com/blog/eve-is-now-generally-available) | no material | Launch announcement. |
| 2026-11-17 | [A new programming model for durable execution](https://vercel.com/blog/a-new-programming-model-for-durable-execution) | no material | Superseded by the note on Workflow SDK 5. |
| 2026-11-17 | [How Fluid compute pricing compares to EC2, Fargate, and EKS](https://vercel.com/kb/guide/fluid-compute-vs-cloud-cost) | no material | Price comparison that is not about agents. |
| 2026-11-17 | [Vercel Sandbox: Persistence](https://vercel.com/docs/sandbox/concepts/persistent-sandboxes) | no material | Repeats, for another vendor, the note on sandbox persistence. |
| 2026-11-17 | [Introducing Dynamic Workflows](https://blog.cloudflare.com/dynamic-workflows) | no material | Launch announcement. |
| 2026-11-17 | [Introducing: Cloudflare Agents](https://blog.cloudflare.com/agents-on-cloudflare) | no material | Launch announcement. |
| 2026-11-17 | [We rebuilt LangSmith around the agent](https://www.langchain.com/blog/we-rebuilt-langsmith-around-the-agent) | no material | Product announcement about registry and governance. |
| 2026-11-17 | [Letta Agents SDK: An SDK for stateful agents](https://www.letta.com/blog/introducing-the-letta-agent-sdk/) | no material | Announcement with no practice to act on. |
| 2026-11-17 | [Sandbox snapshots: hibernate and resume agents fast](https://blaxel.ai/blog/sandbox-snapshot-hibernate-resume-ai-agents) | no material | Repeats the note on sandbox persistence. |
| 2026-11-17 | [VMs (Pause & Fork)](https://www.daytona.io/dotfiles/vms-pause-and-fork) | no material | Announcement. |
| 2026-11-17 | [Modal becomes a gVisor maintainer](https://modal.com/blog/modal-gvisor-maintainer) | no material | Announcement. |
| 2026-11-17 | [Turn And Face The Strange](https://fly.io/blog/kurt-scott-money-sprites/) | no material | Announcement. |
| 2026-11-17 | [What's new in Gemini Enterprise Agent Platform](https://cloud.google.com/blog/products/ai-machine-learning/whats-new-in-gemini-enterprise-agent-platform) | no material | Availability announcement. |
| 2026-11-17 | [Scaling AI Agent Infrastructure with the MCP Stateless updates](https://developers.googleblog.com/scaling-ai-agent-infrastructure-with-the-mcp-stateless-updates/) | no material | Secondary account of the specification release, which has its own note. |
| 2026-11-17 | [The 2026-07-28 MCP Specification Release Candidate](https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/) | no material | Superseded by the note on the final release. |
| 2026-11-17 | [Durable agent approval workflows on Vercel](https://vercel.com/kb/guide/agent-approval-workflow-stack-guide) | no material | Repeats the note on running durable agents on Vercel. |
| 2026-11-17 | [Identity-Chained Authorization with Auth0 Token Vault](https://auth0.com/blog/identity-chained-authorization-auth0-token-vault/) | no material | A demonstration project with no production practice. |
| 2026-11-17 | [Creating a Multi-Tenant AI Agent Platform Handling 7K+ Sessions Without Cross-Team Interference](https://engineering.salesforce.com/building-a-multi-tenant-ai-agent-platform-handling-7k-sessions-without-cross-team-interference/) | no material | Names the problem without describing the mechanism. |
| 2026-11-17 | [See what's happening. Control what happens next.](https://temporal.io/blog/production-controls) | no material | Product announcement. |
| 2026-11-17 | [What Is an Agent Runtime?](https://restate.dev/what-is-an-agent-runtime) | no material | Repeats the vocabulary in the note on frameworks, runtimes and harnesses. |
| 2026-11-17 | [Your Agent Architecture Has a Half-Life. Your Execution Layer Shouldn't.](https://www.inngest.com/blog/your-agent-architecture-has-a-half-life) | no material | Repeats the argument in the note on checkpointing. |
| 2026-11-17 | [The importance of Agent Harness in 2026](https://www.philschmid.de/agent-harness-2026) | no material | Definitions that the harness page already covers. |
| 2026-11-17 | [The anatomy of an agent harness](https://www.langchain.com/blog/the-anatomy-of-an-agent-harness) | no material | Definitions that the harness page already covers. |
| 2026-11-17 | [Amazon's vibe-coding tool Kiro reportedly vibed too hard](https://www.theregister.com/2026/02/20/amazon_denies_kiro_agentic_ai_behind_outage/) | no material | Second-hand report of an incident that the company disputes. |
| 2026-11-17 | [How We Built Secure, Scalable Agent Sandbox Infrastructure](https://browser-use.com/posts/two-ways-to-sandbox-agents) | no material | Repeats the sandbox design in the note on Sierra's Agency. |
| 2026-11-17 | [The self-driving codebase: Building Horizon at WorkOS](https://workos.com/blog/project-horizon) | no material | Repeats the notes on Harvey's and Shopify's platforms at smaller scale. |
| 2026-11-17 | [How we built a background agent to cover 30% of our backlog](https://docs.litellm.ai/blog/lap-internal-agent-30-percent) | no material | Three weeks of use at the time of writing; too early for practice. |
| 2026-11-17 | [Ready for your busiest day: how we scale](https://www.intercom.com/blog/ready-for-your-busiest-day-how-we-scale) | no material | One section on the agent, with no runtime detail. |
| 2026-11-17 | [Replit’s Architecture Behind Secure Agent Work](https://replit.com/blog/architecture-behind-secure-agent-work) | no material | Overview without mechanism. |
| 2026-11-17 | [Block rolls out Builderbot](https://block.xyz/inside/block-rolls-out-builderbot-a-new-suite-of-ai-native-tools-that-changes-the-way-we-ship) | no material | Announcement. |
| 2026-11-17 | [Agentic automation in practice: putting standard engineering work on autopilot](https://www.atlassian.com/blog/development/agentic-automation-in-practice-putting-standard-engineering-work-on-autopilot) | no material | Little runtime detail beyond the note on Rovo's harness. |
| 2026-11-17 | [Scaling Engineering with Agentic Workflows](https://blog.duolingo.com/agentic-workflows/) | no material | Little runtime detail. |
| 2026-11-17 | [The Agent Stack](https://vercel.com/blog/agent-stack) | no material | Launch announcement. |
| 2026-11-17 | [Codex as a platform](https://developers.openai.com/blog/codex-as-a-platform) | no material | Positioning with no practice to act on. |
| 2026-11-17 | [Horizon](https://sierra.ai/blog/horizon) | no material | Launch announcement. |
| 2026-11-17 | [Missions](https://decagon.ai/blog/missions) | no material | Launch announcement. |
