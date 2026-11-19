The main upgrade is to make memory reflect the learner’s **current state**. The code confirms the README’s complaints, although this checkout contains 12 notes rather than the reported 1,900. I treated it as a personal terminal tutor and left all files unchanged.

**1. Replace append-only recall with a small, maintained learner profile.**

- **Change:** [memory.py:16](< / >) loads every note, while `remember()` only appends. At [buddy.py:20](buddy.py), those notes enter every session. Deduplicate recurring mistakes, support resolved/superseded notes, and load a bounded selection of current goals and practice needs. Keep the simple JSONL storage. For future corrections, attach supporting exchange excerpts to new notes; existing notes cannot be checked against discarded conversations.
- **Why:** The wiki recommends correcting memories against evidence and keeping injected context small: [memory guidance](https://mishaevoma.github.io/aie-brain/concepts/memory.md), [dated source note](https://mishaevoma.github.io/aie-brain/sources/2026-11-06-anthropic-components-of-agent-memory.md), [original publication](https://www.anthropic.com/research/components-of-agent-memory).
- **Check:** I ran a read-only Python probe using `memory.load_all()`: **12 notes loaded, the same wann/wenn note appeared three times, and the March exam plan remained present**. Add a regression scenario that records “I passed B1,” restarts the tutor, and checks that exam preparation is no longer active; repeat a mistake and verify only one active entry. These proposed checks have not run.
- **Evidence:** Published November 6, 2026—13 days old. The wiki labels this area evolving; its Anthropic experiments do not establish the ideal memory policy for this tutor.
- **Effort and impact:** Moderate. Prevents obsolete drills and bounds memory-related prompt growth.

**2. Let the extractor remember goals, preferences, and demonstrated progress.**

- **Change:** [memory.py:9](memory.py) explicitly requires “only mistakes” and “No praise, no goals, no preferences.” Replace that restriction with the purpose of memory: personalize future German lessons using supported facts about progress, current needs, and preferences. Keep the `NONE` option for exchanges with nothing useful to retain.
- **Why:** The [memory page](https://mishaevoma.github.io/aie-brain/concepts/memory.md) and its [November 6 source note](https://mishaevoma.github.io/aie-brain/sources/2026-11-06-anthropic-components-of-agent-memory.md) describe poorer results under failure-only recording rules. [Original publication](https://www.anthropic.com/research/components-of-agent-memory).
- **Check:** The read-only probe confirmed the exclusion is present. After changing it, evaluate exchanges expressing a practice preference, passing an exam, and demonstrating mastery. Expect supported facts to survive into a fresh session, without inventing achievements. Model behavior was not tested here.
- **Evidence:** 13 days old; the reported experiments concern Anthropic models and tasks, not this extractor’s teaching quality.
- **Effort and impact:** Small prompt change, plus evaluation. Directly addresses the README’s third complaint.

**3. Test cross-session learning, beyond successful file writes.**

- **Change:** [test_memory.py:10](test_memory.py) supplies canned model responses, and its accumulation test rewards repeated notes. Preserve the storage tests, but add isolated cross-session scenarios covering the failures above and a small model-backed evaluation set.
- **Why:** Grade the resulting behavior and stored state using [eval guidance](https://mishaevoma.github.io/aie-brain/concepts/evals.md), its [dated source note](https://mishaevoma.github.io/aie-brain/sources/2026-01-09-anthropic-demystifying-evals.md), and [original publication](https://www.anthropic.com/research/demystifying-evals-for-ai-agents).
- **Check run:** `python3 -B -m unittest -v` — **3 tests passed**. This proves storage mechanics with fake responses. Proposed acceptance checks: a fresh session honors a saved practice preference, excludes a completed goal, and avoids redundant active memories. Run live extraction trials separately and inspect their outputs.
- **Evidence:** Published January 9, 2026—about 10 months old. The guidance is applicable; no benchmark improvement is assumed.
- **Effort and impact:** Small deterministic suite; additional API cost for live trials. Makes future prompt changes assessable.

Reply **“make upgrade 1 and run the check”** to implement the first change.
For repeat reviews: `npx skills add mishaevoma/aie-brain --skill brain-consult`.
Provenance: published wiki revision **a046fde, 2026-11-19**, consulted **2026-11-19**. No live model calls or latency measurements were performed.
