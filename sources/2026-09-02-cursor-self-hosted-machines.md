---
type: source
title: "Run cloud agents on machines you manage"
author: "Jack Pertschuk"
publisher: Cursor
url: https://cursor.com/blog/self-hosted-machines
published: 2026-09-02
ingested: 2026-11-17
kind: article
read: full
concepts: [managed-agent-runtimes]
---

# Run cloud agents on machines you manage

**In one line:** Cursor's self-hosted option moves only tool execution to the customer's machines: the agent loop, inference and planning stay in Cursor's cloud, and a worker on each machine dials out over a long-lived HTTPS connection to receive tool calls.

## What it says

- Cursor-hosted remains the default: a dedicated VM per session in the Cursor cloud. By Cursor's count, more than 60% of the pull requests it merges internally now come from cloud agents.
- **What moves.** With Self-Hosted Machines the repository's working copy, the file edits and the commands live on a machine in the customer's environment. The agent loop, inference and planning stay with Cursor.
- **Connection.** Running `agent worker start` from the Cursor CLI registers the machine and opens an outbound HTTPS connection that stays open. Cursor's harness sends tool calls to a worker dedicated to the session, which sends results back for the following inference round. No connection is ever opened from Cursor into the customer's network.
- **Still through the vendor.** Tool outputs, which may contain code, go back to Cursor for inference, and Cursor may process and store agent transcripts.
- **When teams choose it:** tools must run inside their network, the work needs special hardware (GPUs, Macs), or the operating system or build pipeline does not package easily as a Cloud Agent build.
- **Pools.** My Machines connects one laptop or VM to an account; a pool puts workers behind a named queue for a team or enterprise. A request names only the pool, so one pool serves many repositories. A free worker claims it; otherwise it waits while a controller watching the queue runs a team-supplied spawn script to start machines.
- **Idle machines.** Each worker connection has an idle timeout, after which the machine can reset and rejoin the pool or keep its workspace. With hibernation an idle machine is snapshotted and stopped; a follow-up inside the reconnect window restores it under the same worker ID, and a later one can go to a new machine. The alternatives: pay for an idle machine, or wait several minutes while a workspace is rebuilt.
- Workers can be started on AWS Lambda, Cloudflare, Coder, Daytona, E2B, Modal, Namespace or Vercel.

## What to do with it

- To keep execution in your network, split the agent at the tool boundary and check what still crosses it: here, tool outputs and transcripts.
- Have the execution side dial out, so no inbound connection is needed.
- Address work to a pool, and scale it from the queue with a start script you own.
- Snapshot idle workspaces, with a window for follow-ups to return to the same one.

## Terms

- **Worker** — the process on a customer machine that holds the connection to Cursor and executes tool calls.

## Caveats

- A product announcement from September 2026 with partner testimonials. The 60% figure is Cursor's own count for its own repositories.
- No values for the idle timeout, reconnect window or restore time, and nothing on worker authentication, where the controller runs or isolation between sessions. The linked docs were not read.
