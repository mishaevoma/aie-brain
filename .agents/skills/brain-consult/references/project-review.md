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
3. Read the relevant concept page and its supporting source note for each reported comparison. Note the exact project location, the source's publication date and which recommendation it supports. Qualify disputed or evolving guidance, older evidence (roughly six months or more), and vendor-specific results when they affect the decision. Where practices disagree, explain which condition fits here. Label your own design suggestions as judgment.
4. Distinguish supported agreement (**aligned**), a demonstrated discrepancy (**gap**), a question the wiki does not cover (**silent**), and missing project evidence (**unverified**). Keep these distinctions in plain language. Use the labels when a user requests verdicts. In a design review, identify proposed behavior as such.
5. Prioritize discrepancies by their consequence on the traced path, the evidence and the effort to fix them. Prefer an existing working mechanism when it meets the goal. Group closely related issues under the change that would resolve them.

## Write the review for the maintainer

Give the person a first action they could take directly from chat. Open with a short bold sentence naming the decision and its user-visible outcome in their project's terms. In the next sentence, pin it to the path you traced and what you observed. Name the conditions of the observation when they matter, such as a simulated retry.

Keep the handoff together.

- **Change.** Point to the exact file and line or named section, explain the cause, and give the smallest edit or decision that addresses it. Mention a working part when it helps the maintainer keep the change small.
- **Check.** Put the command they can run, or a clearly proposed test, on its own line with the expected observable result. Say what you verified yourself. When the choice depends on an unknown, make checking that condition the first action.
- Attach the project location to the observation and a dated source to the advice it supports. Use short link text such as an author's name and publication date. Link the concept when its synthesis or a trade-off matters. Cite shared evidence once for related points.

Use one compact finding for one problem. Fold its regression test into the same finding. Add a second finding when it leads to a different consequential action, and lead with the most important. Use plain headings for longer reviews and omit empty sections. When the inspected path already works and you find no material discrepancy, say what to keep, which check supports it and the boundary of that conclusion. A clean result is a complete review. In a design-only review, give the observation that would validate the proposal.

Close with a short provenance line giving the wiki revision (`git -C <wiki-root> log -1 --format='%h %cs'`) or published copy and date consulted. Include a scope limit only when it changes what the maintainer can conclude.
