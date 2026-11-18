# Watchlist

Where new material for the brain comes from. The `brain-refresh` skill reads this file.

Last checked: 2026-11-18 (seed on 17 November, then research on agent platforms and durable runtimes).

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
| Simon Willison | https://simonwillison.net | Names things early (prompt injection, the lethal trifecta) and follows agent security and tooling week by week. |
| Hamel Husain | https://hamel.dev | Eval practice from consulting work: error analysis, judges, annotation. The evals FAQ written with Shreya Shankar is kept current. |
| Drew Breunig | https://www.dbreunig.com | How contexts fail and how to manage them, with pointers to the papers behind each claim. |
| Chip Huyen | https://huyenchip.com/blog | Long, structured essays from her book on AI engineering. |
| Cognition | https://cognition.com/blog | A coding-agent builder's view from outside the labs. |
| Chroma research | https://www.trychroma.com/research | Measured studies of retrieval and long-context behaviour across many models. |
| Claude articles and platform docs | https://claude.com/resources/articles, https://platform.claude.com/docs, https://code.claude.com/docs | Always-on and self-hosted agents, Managed Agents, hosting the Agent SDK. The docs are undated and change without notice. |
| OpenAI developer blog and API docs | https://developers.openai.com/blog, https://developers.openai.com/api/docs, https://openai.com/index | Agents SDK, Agents API, and how OpenAI runs its own agents. Some pages on openai.com refuse automated fetches and have to be read by hand. |
| LangChain blog and docs | https://www.langchain.com/blog, https://docs.langchain.com | Runtime design, fault tolerance, interrupts, proactive agents. |
| Durable execution vendors | https://temporal.io/blog, https://restate.dev/blog, https://www.inngest.com/blog, https://www.dbos.dev/blog, https://hatchet.run/blog | Each argues for its own design and they answer each other, so read them together. All have something to sell. |
| Jack Vanlightly | https://jack-vanlightly.com/blog | Independent analysis of durable execution and of recovery after an agent's mistake. |
| Armin Ronacher and Earendil | https://lucumr.pocoo.org, https://earendil.com/posts | Durable execution on Postgres, the Pi harness, session portability. |
| Cloudflare | https://blog.cloudflare.com, https://developers.cloudflare.com/agents, https://developers.cloudflare.com/changelog | Agents as actors. The changelog carries behaviour changes that the blog does not. |
| Vercel | https://vercel.com/blog, https://vercel.com/kb | Workflow SDK, durable harness adapters, and a guide to what the application still owns. |
| Fly.io, Rivet, E2B | https://fly.io/blog, https://rivet.dev/blog, https://docs.e2b.dev | Where harnesses and sandboxes run: durable machines, actors, snapshots. |
| MCP and A2A | https://blog.modelcontextprotocol.io, https://modelcontextprotocol.io/seps, https://a2a-protocol.org | Protocol revisions that change how state and long-running calls work. |
| Cloud agent runtimes | https://aws.amazon.com/blogs/machine-learning, https://learn.microsoft.com/en-us/azure/foundry, https://developers.googleblog.com | Limits, guarantees and pricing models of hosted runtimes, and customer cases. |
| Engineering blogs of companies that run agents | Stripe (stripe.dev/blog), Ramp (builders.ramp.com), Shopify (shopify.engineering), Spotify (engineering.atspotify.com), Dropbox (dropbox.tech), DoorDash (careersatdoordash.com/blog), Uber (uber.com/blog), Harvey (harvey.ai/blog), Sierra (sierra.ai/blog), Linear (linear.app/now), Notion (notion.com/blog), Atlassian (atlassian.com/blog), GitHub (github.blog), Meta (engineering.fb.com), Cognition (cognition.com/blog), Cursor (cursor.com/blog) | Accounts from teams that run agent platforms in production: the most useful kind of source for the runtime pages. |
| AI Engineer talks | https://ai.engineer | Talks by teams that run agent platforms. Transcripts are rough, so check figures against the slides. |
| IETF WIMSE working group | https://datatracker.ietf.org/wg/wimse/documents/ | Drafts on agent identity. Drafts expire and are replaced. |

## Open leads

Things the ingested sources cite or imply that are not in the brain yet.

- GBrain's own documentation. The post gives no detail, and the figures in the seeding brief are unverified.
- Every's article on Headway's internal agent, linked from the Every post.
- The study on auto-generated context files cited by Red Hat (arXiv 2602.11988).
- The Meta-Harness paper cited by Harrison Chase.
- Anthropic's post on how code review works there, cited by Addy Osmani.
- The Agent Skills specification (agentskills.io) and the `AGENTS.md` specification.
- Current Claude Code documentation on instruction files and skills, which changes faster than blog posts.
- Cloudflare's "Code Mode" write-up, cited in the code execution article.
- The work behind the terms in Addy Osmani's essay: cognitive surrender (Shaw and Nave), and Anthropic's research on the paradox of supervision.
- Drew Breunig's earlier post "How Long Contexts Fail", where the four context failure modes are argued.
- The two papers behind the tool-count figures, "RAG MCP" and "Less is More", cited by Drew Breunig.
- The paper of six design patterns against prompt injection and Google DeepMind's CaMeL, both cited by Simon Willison.
- The rest of Hamel Husain and Shreya Shankar's evals FAQ. Only its entry on error analysis is in the brain.
- Hamel Husain's longer pieces on judges, "Creating a LLM-as-a-Judge That Drives Business Results" and "Your AI Product Needs Evals", and the paper behind criteria drift, "Who Validates the Validators?" by Shankar and others.
- A re-run of Chroma's context rot tests on models released after July 2025. The code is public.

Found during the research on agent platforms and durable runtimes (18 November 2026) and not read in full:

- OpenAI, "Unlocking the Codex harness: how we built the App Server" and "Inside OpenAI's in-house data agent". The site refused automated fetches.
- Coinbase's post on its agent platform, Mux. The site refused automated fetches.
- AI Engineer CODE 2026 talks: "Agentic SDLC at Uber", Warp on its Oz cloud agent platform, and Ramp on its internal agent.
- Spotify's series on its background coding agent, parts 2 and 4. Parts 1 and 3 are ingested.
- Follow-up posts that Ramp and DoorDash may publish on their platforms.
- Talks from Temporal's Replay 2026 by companies that run agents on it. No transcripts were found.
- Trigger.dev's documentation on its AI Agents SDK, which freezes an idle run instead of replaying it. A fifth mechanism for [durable execution](concepts/durable-execution.md), if it holds up.
- Vercel, "The best workflow engine is a programming language" (August 2026).
- Cloudflare: "Your agent needs a computer, not a container" (August 2026), "Building durable agents with Durable Objects", and the Agents documentation on durable execution.
- AWS, "Building ambient agents with Amazon Bedrock AgentCore" (October 2026), and its general guidance on multi-tenant agents beyond the one customer case ingested.
- Google's documentation for its agent runtime and sessions.
- Restate's customer story on Replit. Undated when checked, so not ingested.
- First-hand incident accounts: Alexey Grigorev, "How I Dropped Our Production Database and Now Pay 10% More for AWS" (March 2026), and Lan Tian, "AI Agent Bankrupted Their Operator While Trying to Scan DN42".
- Birgitta Böckeler, "Harness engineering for coding agent users" (martinfowler.com, April 2026): the builder's harness against the user's. For the [harness](concepts/harness.md) page.
- arXiv 2609.00006, "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents", a source-code study. Check its date before ingesting.
- Armin Ronacher, "Agent design is still hard" (November 2025). Not about the runtime: for the harness and context pages.
- Steve Yegge's write-ups of Gas Town: disposable agents with durable work state.
- LangChain's 2025 writing on ambient agents, the background to its November 2026 article on proactive agents.
- MCP: enterprise-managed authorization, and the roadmap after the 2026-07-28 revision.
- OpenTelemetry's GenAI semantic conventions for agents, and anything on tracing a run across pauses and resumes.
- The IETF drafts that Uber says it tracks for agent authentication.

## Gaps to fill

From the end of [overview.md](overview.md): guidance from labs other than Anthropic, fine-tuning, voice and multimodal products, cost, and product design for AI features.

Added after a design review on 17 November 2026. For each, look first for a primary source from a team that runs it in production:

- Serving many customers: the brain has one production case of keeping tenants apart. Still missing: data residency, noisy neighbours, and limits per customer beyond a spend cap.
- Model gateways: routing, fallback to another model, and evals that cover the fallback.
- Agents that operate an application's interface: browser and computer use, and tools a page declares for the agent.
- Figures for the same practices measured on models from other labs.

Added after the research on agent platforms and durable runtimes on 18 November 2026:

- Failure rates and cost per run of background agents. Companies publish adoption figures.
- How reliably a model resolves a tool call whose outcome is unknown after a crash.
- Approvals that go stale while they wait.
- Tracing and debugging a run across pauses, resumes and machines.
- Calls between agents (A2A) as run by a team in production, beyond passing identity.
- Failure and throughput figures for durable agent runs from a team that does not sell an engine.
