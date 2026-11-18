---
type: source
title: "Context Rot: How Increasing Input Tokens Impacts LLM Performance"
author: "Kelly Hong, Anton Troynikov, Jeff Huber"
publisher: "Chroma"
url: https://www.trychroma.com/research/context-rot
published: 2025-07-14
ingested: 2026-11-17
kind: paper
read: full
concepts: [context-engineering, eval-validity, memory, multi-agent-systems, retrieval, tool-design]
---

# Context Rot: How Increasing Input Tokens Impacts LLM Performance

**In one line:** 18 models from four vendors all got less reliable as input grew, even on trivial fixed-difficulty tasks, so the answer being in the window is not enough: what surrounds it, and how, matters more.

## What it says

- **Setup.** 18 models: Anthropic's Claude Opus 4, Sonnet 4, Sonnet 3.7, Sonnet 3.5, Haiku 3.5; OpenAI's o3, GPT-4.1, GPT-4.1 mini, GPT-4.1 nano, GPT-4o, GPT-4 Turbo, GPT-3.5 Turbo; Google's Gemini 2.5 Pro, 2.5 Flash, 2.0 Flash; Alibaba's Qwen3-235B-A22B, Qwen3-32B, Qwen3-8B. Not all ran every experiment. Tasks keep difficulty fixed and vary only length. Scores are only in charts; directions follow.
- **Needle-question similarity.** Models nearly ace standard Needle in a Haystack (NIAH), a word-for-word lookup. When the question resembles its answer less, by embedding cosine similarity, accuracy falls faster with length. Short inputs did well even at low similarity, so the authors blame length. Needle position barely mattered.
- **Distractors (NIAH):** on-topic passages that do not answer the question. One lowered accuracy against a needle-only baseline, four lowered it further, some more than others, and the effect grew with length. In failures Claude models hallucinated least, Opus 4 and Sonnet 4 tending to abstain, and GPT models most, confidently.
- **Needle-haystack similarity and haystack structure (NIAH).** Among Paul Graham essays, off-topic needles were found markedly more often than blended-in ones (there the strongest models held steady); among arXiv papers the difference was minimal. Across all 18 models, shuffling the haystack's sentences beat the original coherent text.
- **LongMemEval.** 306 chat-memory questions, asked over the full history (about 113k tokens) or only its relevant parts (about 300 tokens). Every model tested scored markedly higher on the focused version. Claude models had the widest gap, mostly from abstaining, and Opus 4 and Sonnet 4 fell below older Claude models on full prompts. Thinking modes raised both scores but left a gap.
- **Repeated Words.** Models copy 25 to 10,000 words, all identical but one, so output grows with input. Fidelity fell with length in every model scored. Models stopped short or ran to the output limit, misplaced the odd word, emitted random text (Gemini models typically from 500-750 words) or refused (Claude Opus 4 2.89% of attempts, GPT-4.1 2.55%).
- The authors give no mechanism, expect larger losses on real multi-step tasks, and call context engineering essential.

## What to do with it

- Send the relevant passages, not the whole history or corpus, even when it all fits.
- Cut near-misses first: stale versions of a fact and look-alike records hurt more than neutral filler.
- Evaluate at production input length: passing a short prompt or NIAH does not carry over.
- Count wrong answers, abstentions and refusals separately.
- Do not have a model copy long text exactly; move it in code or by reference.

## Terms

- **Context rot** — the title's name for output becoming less reliable as input tokens increase. The body never defines it.
- **Distractor** — content on the needle's topic that does not answer the question. **Irrelevant content** is unrelated to both.

## Caveats

- July 2025: later models are untested. The code is published for re-running.
- Chroma sells a retrieval database, and the result favours retrieval. No retriever was tested: focused prompts were hand-built from the dataset's labels, so the gap is an upper bound.
- No scores, error bars or significance tests in the prose, and the capture used here showed no charts.
- NIAH rests on two questions with 8 hand-written needles each. Every task is one call: no agent loop, no tool output.
- GPT-4.1 was both judge and test subject, tuned on about 500 (NIAH) and 600 (LongMemEval) hand-labelled outputs to over 0.99 agreement.
- [Contextual Retrieval](2024-09-19-anthropic-contextual-retrieval.md) advised sending a knowledge base under about 200,000 tokens whole. Here about 113k tokens of history lost to selection.
