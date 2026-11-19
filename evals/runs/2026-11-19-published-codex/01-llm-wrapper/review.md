The single-call design fits this tool. **Two worthwhile upgrades:** make quality checks repeatable, and enforce the output rules already promised by the prompt.

I treated this as a local developer utility. All three tests passed; no project files changed. Live model availability and response quality remain unverified.

**Upgrade 1: Turn the examples into a repeatable quality check.**

- **Observed:** [test_commitmsg.py](test_commitmsg.py:20) checks canned responses and prompt substrings. All three tests still passed when I replaced `build_prompt` in memory with a constant that discarded the actual diff.
- **Change:** Keep the fast unit tests, but add an evaluation command over `examples/`, recording model, output, and pass/fail criteria: describes the actual change, follows formatting, and invents no rationale. Fix [002-timeout.msg](examples/002-timeout.msg:3): its six-hour outage is absent from the input diff. Remove that body or supply supporting context.
- **Why:** The wiki recommends repeatable outcome checks and reference answers supported by their inputs. Its evaluation guidance is evolving; my recommendation for this small project is to start with the three existing examples and expand from observed failures. [Wiki](https://mishaevoma.github.io/aie-brain/concepts/evals.md) · [Source note, January 9, 2026](https://mishaevoma.github.io/aie-brain/sources/2026-01-09-anthropic-demystifying-evals.md) · [Original publication](https://www.anthropic.com/research/demystifying-evals-for-ai-agents). Evidence age: about ten months.
- **Check run:** `python3 -B -m unittest -v` → **3 passed**. An additional in-memory mutation probe printed `Tests pass with real diff discarded: True`.
- **Acceptance check:** A regression test using two distinct diffs must fail when the prompt discards either input. The new evaluation must flag unsupported outage claims and report per-example results; exact wording should not be required.
- **Effort and impact:** A few hours, plus model-call costs when evaluating. Makes prompt and model changes reviewable.

**Upgrade 2: Validate messages before printing them as successful output.**

- **Observed:** [commitmsg.py](commitmsg.py:35) only strips whitespace. Offline probes confirmed that empty text, a 73-character subject, and `Fix parsing.` are all accepted.
- **Change:** Validate nonempty output, subject length, and trailing punctuation before [main](commitmsg.py:43) prints it. On failure, return a nonzero exit status with a useful stderr message. Keep the existing single-call flow.
- **Why:** The wiki supports cheap output sanity checks; applying them at this CLI’s output boundary is my engineering inference. [Wiki](https://mishaevoma.github.io/aie-brain/concepts/production-operations.md) · [Source note, September 17, 2025](https://mishaevoma.github.io/aie-brain/sources/2025-09-17-anthropic-postmortem-three-issues.md) · [Original publication](https://www.anthropic.com/research/a-postmortem-of-three-recent-issues). Evidence is **older, still valid**: about fourteen months old, retained by the wiki’s November 17, 2026 review.
- **Check run:**
  ```sh
  python3 -B -c 'import commitmsg; from test_commitmsg import FakeClient; print(repr(commitmsg.generate("diff", FakeClient(" "))))'
  ```
  Output: `''`.
- **Acceptance check:** Add tests rejecting those three invalid replies, accepting a valid subject with an optional body, and confirming CLI failure produces no stdout.
- **Effort and impact:** Under an hour. Prevents obvious formatting failures from reaching the documented commit command.

Reply **“make upgrade 1 and run the check”** to implement it.
For repeat reviews: `npx skills add mishaevoma/aie-brain --skill brain-consult`.
Provenance: published wiki revision **9b70bc0 (2026-11-19)**, consulted **2026-11-19**; review procedure read from raw GitHub.
