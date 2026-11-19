**Fix policy selection and chunk boundaries first so staff receive complete, current handbook rules.** I traced ingestion → retrieval → answer prompt: an offline check with mocked embeddings selected all seven sample chunks, including both the 30-day archived deadline and the current 60-day deadline.

1. **Archived policies compete with current rules.** [ingest.py:23](ingest.py:23) indexes `docs/archive/` indiscriminately; [qa.py:32](qa.py:32) discards the stored filename when constructing excerpts. The sample retains policy titles, but later chunks lack that context. My recommendation: exclude archived documents from default answers, preserve document/section identifiers in prompts, and expose historical policies only when requested.

   **Proposed check:** A current expense-deadline query excludes archived evidence and answers **60 days**, citing `expenses.md`; a historical query explicitly identifies its policy year.

2. **Chunking breaks facts needed to answer questions.** [ingest.py:11](ingest.py:11) cuts every 400 characters. I confirmed the London hotel allowance splits between `240 EU` and `R in London`, and the sick-note requirement splits inside “fourth.” Retrieval can select either fragment independently. Use paragraph/section boundaries, retain headings, and keep supporting sentences together.

   **Proposed check:** Retrieved evidence independently supports **240 EUR per night in London** and **a note from the fourth consecutive day**.

   Preserving chunk context follows the Brain’s [retrieval guidance](https://mishaevoma.github.io/aie-brain/concepts/retrieval.md) and [Anthropic, September 19, 2024](https://mishaevoma.github.io/aie-brain/sources/2024-09-19-anthropic-contextual-retrieval.md). Archive filtering is my project-specific judgment.

3. **Existing tests cannot detect the reported answer failures.** All five tests in [test_qa.py:7](test_qa.py:7) pass, but they check string slicing, cosine arithmetic, and prompt inclusion. None uses the **16 real questions** in [data/asked.csv:1](data/asked.csv:1). Turn those into a baseline before tuning retrieval: measure supporting-passage recall separately from answer correctness, grouped by expenses, leave, and identifiers. File labels alone are insufficient—the right file can contribute the wrong passage.

   **Proposed check:** Record retrieved passages and answers for all 16 questions, with People-team-approved answer criteria. Include unsupported questions to check abstention. This follows [Brain eval guidance](https://mishaevoma.github.io/aie-brain/concepts/evals.md) and [Anthropic, January 9, 2026](https://mishaevoma.github.io/aie-brain/sources/2026-01-09-anthropic-demystifying-evals.md).

4. **Identifier search needs a measured lexical baseline.** [qa.py:25](qa.py:25) uses embeddings alone despite the documented `EXP-204` complaints. Trial BM25 or exact-identifier matching alongside vector retrieval, then merge rankings. Treat reranking and candidate counts as experiments after establishing the baseline.

   **Proposed check:** Compare supporting-passage recall for `EXP-204`, `EXP-310`, and paraphrased questions on the full corpus. The seven-chunk sample cannot meaningfully test recall@25 because every chunk is returned. Hybrid retrieval is supported by the September 2024 source above; its older, vendor-specific measurements do not predict gains here.

Keep the simple retrieval-plus-one-call architecture. The documented 1.4-million-token corpus justifies evaluating retrieval against the full handbook rather than drawing conclusions from this tiny sample.

Verified: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v` passed; offline chunk/prompt checks ran. No files changed or live model calls made. Slack integration and production answer quality remain unverified.

*Provenance: published AI Engineering Brain and linked review procedure, consulted November 19, 2026. Both supporting source studies are over six months old.*
