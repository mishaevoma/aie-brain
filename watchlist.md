# Watchlist

Where new material for the brain comes from. The `brain-refresh` skill reads this file.

Last checked: 2026-11-17 (seed).

## Feeds

| Source | Where | Why it is here |
|---|---|---|
| Anthropic engineering blog | https://www.anthropic.com/engineering | All 29 articles ingested at seed. New ones appear a few times a quarter. |
| Addy Osmani | https://x.com/addyosmani | Writes long pieces on verification and review from inside the Claude Code team. |
| Boris Cherny | https://x.com/bcherny | Leads Claude Code. Posts on features and working practice. |
| Theo Browne | https://x.com/theo, https://t3.gg/blog, YouTube "Theo - t3.gg" | Harness and interface vocabulary, and the view from above several harnesses. |
| Dan Shipper and Every Frontier | https://x.com/danshipper, https://frontier.every.to | Experiments with skills and shared company agents. |
| Harrison Chase | https://x.com/hwchase17 | Framing articles on memory and agent architecture. |
| Andrej Karpathy | https://x.com/karpathy | Source of the LLM wiki pattern. Quiet on these topics since July 2026. |
| Google Developers Blog | https://developers.googleblog.com | Harness engineering and behavioural evals. |
| Red Hat Developer | https://developers.redhat.com | A series on `AGENTS.md` and Agent Skills. Part one ingested; later parts cover skill writing and trigger testing. |
| Loams | https://www.loams.dev/blog | Detailed harness teardowns. |
| kepano | https://x.com/kepano | Obsidian as the reading side of agent-written wikis. |
| Garry Tan | https://x.com/garrytan | GBrain, a large personal knowledge system. |
| Tobi Lütke | https://x.com/tobi | How a large engineering organisation standardises agent configuration. |

## Open leads

Things the ingested sources cite or imply that are not in the brain yet.

- GBrain's own documentation. The post gives no detail, and the figures in the seeding brief are unverified.
- Every's article on Headway's internal agent, linked from the Every post.
- The study on auto-generated context files cited by Red Hat (arXiv 2602.11988).
- The Meta-Harness paper cited by Harrison Chase.
- Anthropic's post on how code review works there, cited by Addy Osmani.
- The Agent Skills specification (agentskills.io) and the `AGENTS.md` specification.
- Current Claude Code documentation on instruction files and skills, which changes faster than blog posts.
- Simon Willison on the lethal trifecta, cited by Loams.
- The context rot research cited in Anthropic's context engineering article.
- Cloudflare's "Code Mode" write-up, cited in the code execution article.
- The work behind the terms in Addy Osmani's essay: cognitive surrender (Shaw and Nave), and Anthropic's research on the paradox of supervision.

## Gaps to fill

From the end of [overview.md](overview.md): guidance from labs other than Anthropic, fine-tuning, voice and multimodal products, cost, and product design for AI features.

Added after a design review on 17 November 2026. For each, look first for a primary source from a team that runs it in production:

- Durable execution for agent tasks: workflow engines, retries, writes that are safe to repeat, approvals that wait for days.
- Serving many customers: keeping tenants apart, data residency, limits per customer.
- Model gateways: routing, fallback to another model, and evals that cover the fallback.
- Agents that operate an application's interface: browser and computer use, and tools a page declares for the agent.
- Figures for the same practices measured on models from other labs.
