---
type: source
title: "It’s safe to close your laptop now: Hosting coding agents on Amazon Bedrock AgentCore"
author: "Evandro Franco, Eashan Kaushik, Kosti Vasilakakis, Mark Roy, Abhimanyu Siwach, Shreyas Subramanian"
publisher: AWS Artificial Intelligence Blog
url: https://aws.amazon.com/blogs/machine-learning/its-safe-to-close-your-laptop-now-hosting-coding-agents-on-amazon-bedrock-agentcore/
published: 2026-06-08
ingested: 2026-11-17
kind: article
read: full
concepts: [agent-platforms, managed-agent-runtimes]
---

# It’s safe to close your laptop now: Hosting coding agents on Amazon Bedrock AgentCore

**In one line:** AgentCore Runtime gives each coding-agent session its own microVM and a workspace that outlives it, plus identity, an MCP tool gateway and tracing; the harness, the model route and the network rules for shell traffic stay with the builder.

## What it says

- **Bring the harness.** Any coding harness (Claude Code, Codex, Kiro, your own) ships as a container or a zipped Python or Node.js project. The runtime is model agnostic: Amazon Bedrock, a provider's API or your own gateway.
- **Isolation unit.** One Firecracker microVM per session, with its own kernel and filesystem, so parallel agents never share a host.
- **Lifecycle.** A microVM runs for up to 8 hours. A session idle past `idleRuntimeSessionTimeout` (15 minutes by default, configurable) has its compute shut down; `StopRuntimeSession` ends it at once. Invoking the same session ID starts a fresh microVM.
- **State.** Managed session storage (public preview) is a per-session directory mounted at, say, `/mnt/workspace`. It survives stop and resume and is held for 14 days of inactivity. Shared data comes from Amazon S3 Files or Amazon EFS access points; up to five mounts per runtime.
- **Other ways in.** `agentcore exec --it` opens a reattachable shell in the running microVM, and `InvokeAgentRuntimeCommand` runs a command there without the model, for deterministic steps.
- **Tools and credentials.** AgentCore Gateway exposes registered tools as one MCP endpoint. AgentCore Identity holds the credentials (AWS Secrets Manager, a Token Vault), attached per call outside the agent. Three patterns: a bot token, on-behalf-of and a broker.
- **Two gaps it names.** The GitHub MCP server cannot clone, so the session needs one read-only credential, fetched through Identity at start and used once. Shell traffic (`pip install`, `git push`) bypasses Gateway; in VPC mode, private DNS, security groups and a firewall allowlist decide what the microVM reaches.
- **Billing.** No size is chosen up front: charges follow actual CPU consumption (I/O wait adds none) plus the rolling peak of memory used so far. No prices are listed.
- **Audit.** Invocations go to AWS CloudTrail and OpenTelemetry traces to Amazon CloudWatch.

## What to do with it

- Persist the session ID: it resumes the workspace on new compute.
- Keep whatever must survive under the session-storage mount.
- Attach credentials at a gateway outside the agent, preferring on-behalf-of tokens.
- Restrict installs and git remotes at the network layer, and run deterministic steps as direct commands.

## Terms

- **On-behalf-of** — the developer signs in through the IdP, and Identity exchanges a workload access token for a GitHub-scoped one (OAuth 2.0 Token Exchange, RFC 8693), so pull requests are attributed to the person.
- **Broker pattern** — a Lambda behind the Gateway that mints a credential per call and never returns it to the agent.

## Caveats

- Product promotion by six AWS staff with customer testimonials; the promised harness comparison on latency, cost and tests gives no numbers in its text.
- Not stated: what happens to processes and to files outside the mount, the idle timeout's range, request and streaming limits, storage size, sessions longer than 8 hours, other causes of a wiped workspace.
- Page metadata shows a modification on 25 June 2026.
