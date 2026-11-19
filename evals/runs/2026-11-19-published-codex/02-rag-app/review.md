The main upgrade is to keep superseded policies out of current-policy answers. I found four worthwhile changes. All five tests pass, but they also pass with retrieval and answering disabled.

I reviewed the supplied development sample against the linked procedure. No project files changed; no live model or embedding calls ran. The README describes a larger Slack deployment, whose integration and production corpus are absent here.

**1. Exclude archived policies from current answers.**

[ingest.py:23](ingest.py:23) indexes every Markdown file, including the 2024 expense policy. [qa.py:28](qa.py:28) returns up to 25 chunks; this sample has only seven, so every question receives everything—including conflicting 30-day and 60-day filing deadlines.

- **Change:** Exclude `docs/archive/` from the default index and rebuild it. Keep archives available separately if historical questions are required. Preserve the existing source-file metadata.
- **Check run:** An in-memory `python3 -B` probe with mocked embeddings printed `CHUNKS 7 RETRIEVED 7`, `ARCHIVE_RETRIEVED True`, and `CONFLICT_IN_PROMPT True`. This proves conflicting context reaches the prompt, not that a live model necessarily answers incorrectly.
- **Acceptance check:** Add a regression asserting current-policy retrieval excludes archived rows; an answer eval should return **60 days**, supported by `expenses.md`.
- **Why and evidence:** The wiki recommends removing stale near-matches: [context engineering](https://mishaevoma.github.io/aie-brain/concepts/context-engineering.md), [dated source note](https://mishaevoma.github.io/aie-brain/sources/2025-07-14-chroma-context-rot.md), [original research](https://www.trychroma.com/research/context-rot). Published **2025-07-14**, about 16 months old: **older, still valid** as guidance on the wiki’s settled page, reviewed 2026-11-17. Its experiments do not establish this app’s error rate.
- **Effort and impact:** Small code change plus index rebuild; removes a direct source of wrong expense guidance.

**2. Turn the existing questions into a retrieval and answer evaluation.**

[test_qa.py:7](test_qa.py:7) checks chunk lengths, cosine arithmetic and prompt substrings. Nothing consumes the **16 labelled questions** in [data/asked.csv:1](data/asked.csv:1): eight expense, five leave and three security questions.

- **Change:** Keep these useful unit tests. Add an evaluation using the CSV’s expected documents, reporting retrieval rank and results by topic. Add answer-level expectations separately; document labels alone cannot establish answer correctness. Run it when prompts, models or retrieval change.
- **Check run:** `python3 -B -m unittest -v` passed five tests. A second in-memory run replaced `retrieve` and `answer` with functions that raise exceptions; all five still passed.
- **Acceptance check:** Disabling retrieval must fail the new evaluation. Check correct answers, supporting excerpts and unsupported-question abstention. On this seven-chunk sample, recall@25 is trivial; use smaller ranks and representative distractors.
- **Why and evidence:** [Evals](https://mishaevoma.github.io/aie-brain/concepts/evals.md), [dated source note](https://mishaevoma.github.io/aie-brain/sources/2026-01-09-anthropic-demystifying-evals.md), [original publication](https://www.anthropic.com/research/demystifying-evals-for-ai-agents). Published **2026-01-09**, about ten months old. Applying this guidance to document retrieval is the wiki’s explicit inference.
- **Effort and impact:** Moderate; the labels already exist. Adds measurable evidence that subsequent changes help, with API costs for live answer trials.

**3. Preserve complete policy statements and their provenance.**

[ingest.py:11](ingest.py:11) cuts through words and sentences. The London hotel limit is split into `240 EU` and `R in London`. [qa.py:32](qa.py:32) also discards filenames when assembling excerpts.

- **Change:** Use paragraph/section-aware chunks with bounded size and overlap where needed. Include document title, heading and source path in indexed context and prompt excerpts. Keep the existing separation between ingestion and answering.
- **Check run:**
  ```sh
  python3 -B -c 'import ingest; p=ingest.chunk((ingest.DOCS/"expenses.md").read_text()); print(repr(p[0][-6:]), repr(p[1][:11]))'
  ```
  Printed `'240 EU' 'R in London'`.
- **Acceptance check:** A retrieved passage must contain the complete **240 EUR London** rule and its source. Also test the doctor’s-note rule, currently split across chunks.
- **Effort and impact:** Moderate plus re-embedding; prevents fragments losing the facts needed to interpret them.

**4. Add lexical retrieval for form identifiers, then measure the gain.**

[qa.py:25](qa.py:25) ranks solely by embedding similarity. The README specifically reports misses for identifiers such as `EXP-204`; I verified the implementation, but did not reproduce that failure with live embeddings.

- **Change:** Combine BM25 with vector retrieval using rank fusion, preserving identifiers during tokenization. Keep semantic search for paraphrased questions. Tune the final passage count using upgrade 2.
- **Check run:** `python3 -B -c 'import inspect, qa; print(inspect.getsource(qa.retrieve))'` confirmed cosine-only ranking.
- **Acceptance check:** Evaluate `EXP-204`, `EXP-310` and `LV-110` against passages actually containing those identifiers; compare with the vector-only baseline and check ordinary questions for regressions.
- **Effort and impact:** Moderate; adds index maintenance and query work, while addressing the reported exact-match weakness.

For upgrades 3–4, the supporting chain is [retrieval](https://mishaevoma.github.io/aie-brain/concepts/retrieval.md) → [2024-09-19 source note](https://mishaevoma.github.io/aie-brain/sources/2024-09-19-anthropic-contextual-retrieval.md) → [Anthropic’s original publication](https://www.anthropic.com/research/contextual-retrieval). At 26 months old, this is **older, still valid** guidance retained by the wiki’s 2026-11-17 review; the page remains evolving. Section-aware splitting is my concrete implementation recommendation. Neither the paper’s performance gains nor its preferred retrieval counts are established for this project.

Reply **“make upgrade 1 and run the check”** to implement the first change.  
For repeat reviews: `npx skills add mishaevoma/aie-brain --skill brain-consult`.  
Provenance: published wiki revision **9b70bc0**, dated and consulted **2026-11-19**.
