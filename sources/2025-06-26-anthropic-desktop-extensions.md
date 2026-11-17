---
type: source
title: "Desktop Extensions: One-click MCP server installation for Claude Desktop"
author: "Anthropic"
publisher: Anthropic
url: https://www.anthropic.com/research/desktop-extensions
published: 2025-06-26
ingested: 2026-11-17
kind: article
read: full
concepts: [mcp]
---

# Desktop Extensions: One-click MCP server installation for Claude Desktop

**In one line:** package a local MCP server, its dependencies and a manifest into one archive, so non-developers can install it with a double-click instead of editing JSON config and installing runtimes.

## What it says

- Installing a local MCP server used to mean installing runtimes, editing JSON config by hand, managing dependencies and updating manually, which kept non-developers out.
- A Desktop Extension is a ZIP archive with the `.mcpb` (MCP Bundle) extension, originally `.dxt`. It holds the server code, bundled dependencies and a `manifest.json`. Only the manifest is required.
- The manifest declares metadata, the server `type` (`node`, `python` or `binary`), the entry point and the launch command. Variables such as `${__dirname}`, `${HOME}`, `${TEMP}` and `${user_config.<key>}` are filled in at install time. Optional fields declare tools and prompts, compatibility (app version, platforms, runtime versions) and per-platform overrides.
- `user_config` describes the settings a user must supply: strings, numbers with min and max, directories, and fields marked `sensitive`. Claude Desktop builds a settings form from it, validates the input, keeps secrets in the OS keychain, and will not enable the extension until required values are filled in.
- Claude Desktop ships its own Node.js runtime, so Node-based extensions need nothing extra. Extensions update automatically.
- Tooling: `npx @anthropic-ai/mcpb init` generates a manifest interactively, and `npx @anthropic-ai/mcpb pack` validates it and builds the archive. Dragging the file into Settings installs it.
- A curated extension directory inside Claude Desktop accepts submissions, which Anthropic reviews for quality and security after they are tested on Windows and macOS.
- Enterprises can manage extensions through Group Policy (Windows) and MDM (macOS): pre-install approved extensions, blocklist extensions or publishers, turn off the public directory, or run a private one.
- The spec (version 0.1), tooling and schemas are open source, so other desktop apps can adopt the format.

## What to do with it

- If non-developers need your local MCP server, ship it as an `.mcpb` bundle rather than install instructions.
- Declare every secret and setting in `user_config` with `sensitive` set where needed, rather than asking users to edit environment variables.
- Bundle dependencies and declare platform compatibility so the extension runs on install.
- In enterprise rollouts, use the allowlist and blocklist controls and a private directory to govern which extensions run.

## Terms

- **Desktop Extension / MCP Bundle (`.mcpb`)** — a single-file package of a local MCP server plus a manifest, installable with one click.
- **`user_config`** — manifest section that declares the settings a user must supply, from which the host app builds a form.

## Caveats

- A banner dated Sep 11, 2025 records the rename from `.dxt` to `.mcpb`. Older `.dxt` files still work. Later articles in this batch (2025-09-11 tools article) still call the format "DXT".
- The page links developer docs to the `anthropics/dxt` repo but also points to an `anthropics/mcpb` repo. Check which one is current.
- Spec version 0.1 is early, and field names may have changed.
- This is a product announcement for Anthropic's own desktop app. No author is named on the page.
