---
type: source
title: "Why We Built Our Own Background Agent"
author: "Zach Bruggeman, Jason Quense, Rahul Sengottuvelu"
publisher: Ramp
url: https://builders.ramp.com/post/why-we-built-our-background-agent
published: 2026-01-12
ingested: 2026-11-17
kind: article
read: full
concepts: [agent-identity, agent-platforms, background-agents, multi-agent-systems]
---

# Why We Built Our Own Background Agent

**In one line:** A background coding agent is three parts you can build yourself: a sandbox per session started from a snapshot, a state store per session that every client syncs with, and clients where people already work.

## What it says

- Inspect is Ramp's internal background coding agent. About 30% of the pull requests merged to its frontend and backend repositories are written by it, a level reached within a couple of months and without a mandate. The post doubles as a build specification.
- **Sandbox.** Each session runs in a sandboxed VM on Modal with a full development environment and the integrations an engineer has (Sentry, Datadog, LaunchDarkly, GitHub, Slack, Buildkite and others), so the agent can verify its own work.
  - An image per repository is rebuilt every 30 minutes: clone, install, build, even run the app and tests once to fill caches. A session starts from the latest snapshot and has at most 30 minutes of changes to sync.
  - When the agent finishes, another snapshot is taken. If the sandbox has exited and the user sends a follow-up, the session is restored from it.
  - For speed: start warming a sandbox when the user begins to type, keep a warm pool for busy repositories, and let the agent read at once while blocking edits until the sync completes.
- **Agent.** OpenCode, chosen because it is a server with clients on top, has a typed SDK and plugins, and its source can be read by an agent.
- **State and API.** One Cloudflare Durable Object per session, each with its own SQLite database, so that hundreds of sessions streaming tokens do not affect one another. Hibernating WebSockets keep idle connections free.
- Follow-up prompts sent during a run are queued, not injected. A way to stop a run midway is required.
- The agent has a tool to start further sessions and one to read their status.
- **Multiplayer.** A session is not tied to one author, and each prompt carries its author.
- **Identity.** The sandbox pushes the branch. The API then opens the pull request with the requesting user's GitHub token, not as the app, so that nobody can approve their own change.
- **Clients.** Slack (a fast model classifies which repository a message is about), a web app with a hosted editor and a streamed desktop, a Chrome extension, and pull request comments. The metric to track is the share of sessions that end in a merged pull request.

## What to do with it

- Do the slow setup in a scheduled image build, not at session start.
- Snapshot the sandbox at the end of a turn, so that a later follow-up resumes the same machine state.
- Keep session state in a store separate from the sandbox, one per session.
- Act on the code host with the requesting user's identity.
- Measure merged outcomes per session.

## Terms

- **Background agent** — a coding agent that runs in a hosted sandbox, without the user's machine, and reports back with a pull request.

## Caveats

- Self-reported in January 2026 by a team that has since offered Inspect to other companies. No cost, failure or review figures.
- The claim that models will not start too many sessions is an opinion, not a measurement.
