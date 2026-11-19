The first upgrade is to exclude superseded policies from current-policy answers. The sample currently puts conflicting expense rules into the prompt. Three further upgrades would make retrieval measurable and address the reported failures.

I used the requested brain-consult skill and local wiki. This was read-only; all five unit tests passed. The README describes a staff-facing Slack service, but this checkout contains only the CLI and sample documents. Live model quality and the full handbook remain unverified.

**Upgrade 1: Keep obsolete policies out of current answers.**

- **Observed:** `ingest.py:23` includes `docs/archive/expenses-2024.md`. With seven sample chunks and `TOP_K=25`, retrieval includes everything: both the old **30-day** and current **60-day** expense rules.
- **Change:** Exclude archived documents from the default index, rebuild it, and retain source paths in `qa.py:32` when constructing context. Keep the existing file metadata. Historical questions can use an explicit historical-policy path if needed.
- **Why and evidence:** The wiki’s [context engineering guidance](https://mishaevoma.github.io/aie-brain/concepts/context-engineering.md), [dated source note](https://mishaevoma.github.io/aie-brain/sources/2025-07-14-chroma-context-rot.md), and [Chroma publication](https://www.trychroma.com/research/context-rot) support removing distracting context. Published **14 July 2025**, about **16 months old**: older, still valid as a principle on the wiki’s settled page, reviewed 17 November 2026. Applying it to policy versions is my inference; this does not prove which answer the live model gives.
- **Effort and impact:** A small change that removes a direct source of incorrect staff guidance.

**Upgrade 2: Turn the existing questions into a retrieval and answer evaluation.**

- **Observed:** `data/asked.csv` contains 16 labelled questions—eight expenses, five leave, three security—but `test_qa.py` never uses them. Its five checks exercise chunk lengths, cosine arithmetic and prompt assembly.
- **Change:** Add a runner over those questions, reporting retrieval ranking and answer correctness separately, broken down by topic. Extend labels with expected facts and supporting passages; keep the cheap unit tests. File-level recall alone is misleading here because the sample retrieves every file.
- **Check run:** `python3 -B -m unittest -v` → **Ran 5 tests … OK**. This establishes utility behavior, not answer quality.
- **Acceptance check:** The new evaluation must flag a 30-day expense answer, a missing EXP-204 passage, and an unsupported answer to the business-class question. Run it before and after retrieval changes; it does not exist yet.
- **Why and evidence:** [Evals guidance](https://mishaevoma.github.io/aie-brain/concepts/evals.md) → [source note](https://mishaevoma.github.io/aie-brain/sources/2026-01-09-anthropic-demystifying-evals.md) → [Anthropic publication](https://www.anthropic.com/research/demystifying-evals-for-ai-agents), **9 January 2026**, about **10 months old**. Its recommendation is to start with real failures and explicit success criteria.
- **Effort and impact:** Roughly a day for an initial runner and labels, plus model-call costs; provides evidence that subsequent changes help.

**Upgrade 3: Preserve complete policy statements and their context.**

- **Observed:** `ingest.py:11` splits the London hotel allowance into `240 EU` and `R in London…`. The second chunk also loses the policy title and effective-date context.
- **Change:** Split along Markdown sections and paragraph boundaries, with a size fallback that preserves sentences. Include title, section and policy version with each chunk before embedding and in the prompt. Keep source-file tracking.
- **Acceptance check:** Assert that one expense chunk contains `240 EUR in London` and its policy/section metadata. This fails today; the replacement check has not been implemented.
- **Effort and impact:** A few hours plus reindexing; prevents retrieval from separating amounts from their conditions.

**Upgrade 4: Add lexical retrieval for form identifiers.**

- **Observed:** `qa.py:25` ranks exclusively by embedding similarity. A controlled test returns `unrelated` over an exact `EXP-204` match when the supplied vectors favor the unrelated passage. This demonstrates the missing lexical signal, not measured Voyage performance.
- **Change:** Combine BM25 candidates with embedding candidates using rank fusion. Preserve semantic retrieval for paraphrased questions; tune the final context size against upgrade 2.
- **Acceptance check:** Test EXP-204, EXP-310 and LV-110 against competing passages, then compare identifier retrieval and overall answer quality with the baseline.
- **Effort and impact:** Approximately half a day to a day plus index work; targets the identifier failures documented in the README.

For upgrades 3–4, the evidence is [retrieval guidance](https://mishaevoma.github.io/aie-brain/concepts/retrieval.md) → [source note](https://mishaevoma.github.io/aie-brain/sources/2024-09-19-anthropic-contextual-retrieval.md) → [Anthropic’s Contextual Retrieval publication](https://www.anthropic.com/research/contextual-retrieval), **19 September 2024**, about **26 months old**. **Older, still valid as an experiment:** the evolving wiki page retained it after review on 17 November 2026. Heading-aware splitting is my implementation choice; the publication supports contextualized chunks and hybrid search, without guaranteeing gains here.

The read-only diagnostic for upgrades 1, 3 and 4 was:

```sh
python3 -B - <<'PY'
from unittest.mock import patch
import ingest, qa
with patch.object(ingest, 'embed', side_effect=lambda ts: [[1.0] for _ in ts]):
    rows = ingest.build()
print('archived files:', sorted({r['file'] for r in rows if r['file'].startswith('archive/')}))
print('intact London limit:', any('240 EUR in London' in r['text'] for r in rows))
with patch.object(qa, 'embed_query', return_value=[1.0, 0.0]):
    hits = qa.retrieve('EXP-204', [
        {'text': 'unrelated', 'vector': [1.0, 0.0]},
        {'text': 'EXP-204', 'vector': [0.0, 1.0]},
    ], top_k=1)
print('identifier winner:', hits[0]['text'])
PY
```

It printed `['archive/expenses-2024.md']`, `False`, and `unrelated`, respectively. Embeddings were mocked; no external model calls ran.

Reply **“make upgrade 1 and run the check”** to implement the first change.
For repeat reviews: `npx skills add mishaevoma/aie-brain --skill brain-consult`.
Provenance: local wiki revision **fe44a47 (2026-11-19)**, consulted **19 November 2026**.
