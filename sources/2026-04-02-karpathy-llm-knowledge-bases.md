---
type: source
title: "LLM Knowledge Bases"
author: "Andrej Karpathy"
publisher: "@karpathy on X"
url: https://x.com/karpathy/status/2039805659525644595
published: 2026-04-02
ingested: 2026-11-17
kind: x-post
read: full
concepts: [compounding, llm-wiki, retrieval]
---

# LLM Knowledge Bases

**In one line:** Collect sources in a folder, let an LLM compile and maintain a markdown wiki from them, and ask questions against the wiki; at around a hundred articles this works without a vector database.

## What it says

- He now spends a large share of his tokens on manipulating knowledge stored as markdown and images, not on code.
- **Ingest.** Source documents (articles, papers, repos, datasets, images) go into a `raw/` directory. An LLM incrementally "compiles" a wiki from them: a directory of `.md` files with a summary of everything in `raw/`, backlinks, and concept articles that link to each other. He clips web articles with the Obsidian Web Clipper and saves images locally so the model can look at them.
- **Viewing.** Obsidian is the front end for the raw data, the wiki and anything derived from it. The LLM writes and maintains the wiki; he rarely edits it by hand.
- **Questions.** At roughly 100 articles and 400,000 words, an agent can research complex questions against the wiki. He expected to need retrieval-augmented generation, but the model kept its own index files and short summaries up to date and found what it needed at that scale.
- **Output.** Answers come back as markdown files, Marp slides or matplotlib charts, viewed in Obsidian. Useful answers get filed back into the wiki, so his own questions add to it.
- **Linting.** He runs LLM health checks over the wiki: find inconsistent data, fill gaps with web search, suggest connections and new articles.
- **Extra tools.** He built a small search engine over the wiki and hands it to the agent as a command-line tool for larger queries.
- **Next.** As the collection grows, synthetic data and fine-tuning could put the knowledge into model weights.
- He thinks this should be a real product, not a pile of scripts.

## What to do with it

- For a knowledge base of this size, start with files, an index the model maintains, and an agent that reads. Add search only when the index stops being enough.
- Keep raw sources separate from the compiled wiki, and let the agent own the wiki.
- File good answers back so that using the knowledge base improves it.
- Run a periodic lint pass.

## Terms

- **Compile** — his word for an LLM turning raw sources into a linked wiki.
- **raw/** — the folder of unmodified source material.

## Caveats

- One person's workflow at a stated scale of about 100 articles. He says "at this small scale" himself.
- This brain follows the pattern, with one change: it is public, so full source texts stay out of git.
- The follow-up idea file (4 Apr 2026) is the more careful version.
