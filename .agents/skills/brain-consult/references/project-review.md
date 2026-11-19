# Review a project with the brain

The person should leave with at least one upgrade they can make today: what to change and where, why, how to check it, how old the evidence is, and what it costs and buys. When nothing needs upgrading, they should leave knowing that, and what it rests on.

The review is read-only. Write nothing to the project and leave its folder as you found it. If you run one of its commands, keep it from leaving files behind, for example `python3 -B` or `PYTHONDONTWRITEBYTECODE=1` for Python. Do not run project setup, live services, or anything that changes state.

## Start from the project

Read the README, the agent instructions that apply, and a short listing of tracked files. Honor a named directory, design document or question. If you cannot reach the target, ask for its path or the relevant files. The brain checkout is a target only when the person is reviewing the brain itself.

Then pick the pages. Paths are relative to the wiki root.

- **The project already calls a model.** Use `playbooks/upgrading-an-agent-app.md`. Its checks say what to look for in code. One model call in an ordinary app counts.
- **How coding agents work in this repository.** Use `playbooks/setting-up-a-repo-for-coding-agents.md`. Follow the path from opening the repository to proving a change works. This applies to a project with no AI feature too.
- **A design or a plan.** Use `playbooks/building-an-agent-product.md` and compare the stated choices. Say which claims wait on an implementation or a measurement.
- **Something already going wrong.** "When something goes wrong" in `index.md` names the page.

A project with both an AI feature and agent instructions gets both, the product first. Infer the audience, the stage and what a failure costs from the project, and name the assumption if the stage is unclear. Stage decides which checks apply: a local experiment needs the cheapest proof of its core behaviour, and a service that acts for real users needs the failure, retry, approval and evaluation paths followed.

## Scan first, then go deep

Aim to have the first upgrade written within about three minutes. Do not read the whole wiki.

1. **Scan.** Read the files on the path a request takes: the entry point, each model call, the tools, the tests and the test command. Walk every check of the playbook against them and note each candidate with its file and line. Run the documented test command if it is safe, and read what it printed.
2. **Rank.** Order candidates by what a failure costs the user, then by how little work the change is. The highest impact for the least effort goes first.
3. **Go deep on what you will report.** For each, read the concept page the playbook step names and the source note behind the advice. Confirm the problem in the code, and look for an equivalent before calling something missing: a Make target and a CI job may already do what a playbook calls a skill. Settings of your own session are not the project's.
4. **Keep what is true, backed and worth doing.** A candidate that is not true of this code, has no page of the wiki behind it, or would not be worth the maintainer's time is dropped, not reported.

Tell apart what you observed, what the project documents and what you only read. Never imply a check ran unless you ran it.

## What each upgrade must carry

Report every upgrade that passes step 4, the most valuable first. Each one is a different change. Fold a regression test into the upgrade it protects. Use this shape, one or two lines per part.

> **Upgrade 1: <the change, and what the user gets from it>.** One sentence on what you observed on the path you traced.
>
> - **Change.** The file and line, or the named section, and the smallest edit or decision that fixes it. Name a working part worth keeping.
> - **Why.** What the wiki says, linked three ways: the wiki page, the dated source note, and the original publication from that note's `url:` field.
> - **Check.** On its own line, a command that shows the problem today and what it prints. Run it when that is safe, and paste the line you ran. Then the command or exact test that passes once the change is made, with the result to expect. Say which of the two you ran.
> - **Evidence.** The date the source was published and its age. Whose models or product a figure was measured on, when a figure matters.
> - **Effort and impact.** How much work the change is, and what it prevents or enables for the user.

**Evidence age.** Advice should rest on a source published in the last 12 months. When the only source is older, either add a newer source from the same wiki page that says the same, or label it "older, still valid" and give the reason: the page that carries it has `status: settled`, or its `reviewed:` date shows it was re-read against newer sources. Never present older evidence as current. Qualify contested or evolving pages, and say which condition fits this project where sources disagree.

**Your own judgment.** When the wiki is silent on what you found, say so, and label the advice as yours. Check "What this brain does not cover yet" in `overview.md` before treating a topic as covered.

## When there is nothing to upgrade

Say so in the first sentence. Name what to keep and the check that supports it, and the limit of that conclusion. Then offer one focused question the person could ask next, in their project's terms. A clean result is a complete review.

A project with no AI feature has no agent app to upgrade. Say that first, review only how coding agents work in it, and do not stretch the product playbooks over it.

Never fill a review. A recommendation with no location in this project is not a finding. A playbook step the project has no use for is not a gap.

## Close with the next step

End with three short lines.

- The offer: the person can reply "make upgrade 1 and run the check" and you will do it. Until they do, change nothing.
- For repeat reviews, if this skill is not installed in the project: `npx skills add mishaevoma/aie-brain --skill brain-consult`.
- Provenance: the wiki revision (`git -C <wiki-root> log -1 --format='%h %cs'`, or the line in `revision.txt` of the published copy) and the date you consulted it. Add a scope limit only when it changes what the maintainer can conclude.

Use plain headings in a longer review and omit empty sections. Use the verdict words **aligned**, **gap**, **silent** and **unverified** when the person asks for verdicts. In a design-only review, give the observation that would validate the proposal.
