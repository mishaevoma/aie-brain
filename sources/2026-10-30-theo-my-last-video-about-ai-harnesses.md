---
type: source
title: "My last video about ai harnesses"
author: "Theo Browne"
publisher: "Theo - t3.gg on YouTube"
url: https://www.youtube.com/watch?v=ebILGCoN4UU
published: 2026-10-30
ingested: 2026-11-17
kind: video
read: full
concepts: [context-layer, harness, mcp, multi-agent-systems, skills]
---

# My last video about ai harnesses

**In one line:** A harness is what lets a model act, but which harness you pick now matters about as much as which editor you use, because labs train each model on its own harness and the measurable gap between harnesses is a few percent.

## What it says

- What engineers need to care about keeps moving up: instruction sets, then languages, then frameworks, then architecture. Each new abstraction makes the layer below a detail. Engineers tend to stay attached to the layer that was current when they started.
- A model only produces text. The harness tells it a syntax it can answer in, and then does the thing: read a file, edit a file, run a command. His picture is a chef in an empty kitchen, who can describe a meal but cannot cook until there are tools.
- People use **interfaces**. Models use **harnesses**. The Claude Agent SDK is a harness. The Claude Code CLI is an interface that bundles a harness.
- An **agent** is a harness plus a model.
- The **tool plane** is what a harness exposes to the model. Some harnesses ship almost nothing (Pi is roughly just bash), others ship many tools (Claude Code: subagents, file read and edit, skills, bash and more). Plugins add tools. Adding tools does not make something a harness.
- The **data plane** is how the agent reaches things that live outside the harness, mostly through MCP. A tool is code shipped into a specific harness. An MCP server is a contract: the harness asks something else to do the work. That is why T3 Code exposes its features through an MCP server and can broker work between different harnesses.
- His stack: model, then harness, then interface, then the product you are building.
- Why harnesses barely matter now:
  - Users no longer notice them. T3 Code's model picker is really a harness picker, and people are surprised when skills set up for one harness are missing in another.
  - Models are increasingly trained on data from their lab's own harness, so a lab's model tends to behave best in that lab's harness. Choose the capability and price you want; the harness comes with it.
  - For the same model, he puts the gap between harnesses at roughly 3 to 5 percent, and treats anything larger as a model-layer problem that will get fixed.
  - Six months earlier he would have argued about harnesses. Now he compares harness loyalty, and loyalty to one model family, to arguing about editors.
- He calls T3 Code an agentic development environment (ADE), not a harness, and expects ADEs to stop mattering too as people start prompting from tools like Slack.

## What to do with it

- Use the words precisely: harness, interface, agent, tool, MCP server are different things at different layers.
- Do not spend effort picking or building a harness for small benchmark wins. Pick the model, use the harness built for it.
- Put effort into what carries across harnesses: instructions, skills and data access through MCP.
- If you build something that sits above several harnesses, expect to supply what users assume every harness has (skills, configuration), because they will not know which layer is missing it.

## Terms

- **Harness** — the runtime that gives a model tools and executes its tool calls.
- **Interface** — what a person uses. It may bundle a harness.
- **Agent** — a harness plus a model.
- **Tool plane / data plane** — tools that live inside the harness, versus access to outside systems through MCP.
- **ADE** — agentic development environment, his name for tools like T3 Code.

## Caveats

- Based on the auto-generated transcript, so product names may be misheard. Long tangents and a sponsor segment (Vercel's Eve agent framework) are left out.
- The author builds T3 Code, which benefits if harnesses are interchangeable. The 3 to 5 percent figure is his estimate, with no data shown.
- Disputed in replies to his 9 Nov post, and at odds with sources that treat harness design as the main lever for long-running work.
