# Review a project with the brain

The person should leave knowing what already works, what to change first, and how to tell if the change helped.

## Establish the scope from the project

Read the project brief or README, applicable agent instructions, and a short listing of tracked files. Honor a named directory, design document or question. If you have no access to the target, ask for the project path or the relevant files. The brain checkout is a valid target only when the user is reviewing the brain itself.

Choose the playbook from “By decision” in the wiki index.

- **How coding agents work here.** Use `playbooks/setting-up-a-repo-for-coding-agents.md`. Follow the path a contributor takes from opening the repo to proving a change works. This applies even if the project itself has no AI features.
- **What the AI feature does for a user.** Use `playbooks/building-an-agent-product.md`. Trace a representative request from the entry point through the model and tools to the user-visible result. Include the repo setup when the user asks for both or when it materially affects the product finding.
- **A proposed design.** Use the playbook that fits the proposal. Compare its stated choices and trade-offs. Identify which claims rely on future implementation or a measurement.

Infer audience, deployment stage and consequences from the project. Name the assumption if stage is unclear. For a local experiment, look for the cheapest way to prove its core behavior. For a service handling real users or external actions, follow the relevant permissions, failure, retry, evaluation and recovery paths. Deployment context and impact determine which playbook steps apply.

## Compare actual behavior with the sources

1. Walk the relevant playbook steps. For each material claim, inspect the artifact that would prove it. Follow a README command to its script and CI invocation, or a tool call to its permission check and failure handling. Distinguish the behavior you observed, documented intent, and checks you only read. Never imply a check ran unless you ran it. Avoid running project setup, live services or actions that change state during a review.
2. Check for an equivalent before calling something missing. A Make target and CI job may already provide the verification a playbook describes as a skill. Look for contrary evidence. Session permissions describe the current agent session. Look for repo-owned configuration before crediting the project with those controls. If settings live elsewhere, identify what would settle the question.
3. Read the relevant concept page and its supporting source note for each reported comparison. Link a precise project location (file and line or named section), the wiki page and a dated source supporting the specific recommendation. Use the source's publication date. Qualify contested or evolving guidance, evidence older than about six months, and vendor-specific results when they affect the decision. Where practices disagree, explain which condition makes one fit here. Label your own design suggestions as judgment.
4. Use **aligned** for supported agreement and **gap** for a demonstrable discrepancy with a relevant practice. Reserve **silent** for a decision the wiki does not cover. Use **unverified** for missing project evidence. For a design-only review, explicitly label alignment as proposed. Omit genuinely inapplicable steps or briefly explain their exclusion if the reader would expect them.
5. Prioritize discrepancies by their consequence on the traced path, the evidence and the effort to fix them. Prefer an existing working mechanism when it meets the goal. Group closely related issues under the change that would resolve them.

## Return a review someone can act on

Lead with the project's purpose, the path you reviewed and the single most useful decision. Write for the person maintaining it. Use familiar project names and explain what a failure looks like for a contributor or user.

Present the highest-impact findings first. For each, connect the project evidence to the dated advice, explain why it matters here, recommend the smallest effective change, and give an observable acceptance check. A verification suggestion should include the expected outcome and use real project commands or clearly label a proposed test. Highlight a working choice worth preserving when the evidence supports one.

Keep the first response proportional. A few well-supported findings usually suffice. Summarize only remaining decisions and unknowns that could change the advice, including how to resolve them. If everything inspected aligns, say what establishes that and where your inspection ended. End with the first action a maintainer can take. Include the wiki revision for reproducibility when available (`git -C <wiki-root> log -1 --format='%h %cs'`), or identify the published copy and date consulted.
