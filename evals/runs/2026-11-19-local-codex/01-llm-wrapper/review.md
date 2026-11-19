The main upgrade is **a repeatable quality check for generated messages**. The single-call design fits this small CLI; keep it. I treated the project as a local developer utility and left all files unchanged.

All three tests pass with `python3 -B -m unittest -v`. They verify request construction and canned-response handling, but don’t establish that the model produces useful commit messages. No live model call was run, so model availability and actual output quality remain unverified.

**Upgrade 1: Turn the existing examples into a small regression eval.**

- **Change:** Add an eval runner around `commitmsg.py:25` and document it in README’s “Changing the prompt” section. Start with the three existing diffs. Check subject length and punctuation automatically; use explicit yes/no criteria for meaning and unsupported claims. Keep the fast unit tests.
- **Correct the reference first:** `examples/002-timeout.msg` mentions a six-hour nightly-sync incident absent from its input diff. Remove that body or supply the incident context explicitly. Otherwise, the reference rewards information the model cannot know.
- **Why:** The wiki’s [eval guidance](https://mishaevoma.github.io/aie-brain/concepts/evals.md), its [dated source note](https://mishaevoma.github.io/aie-brain/sources/2026-01-09-anthropic-demystifying-evals.md), and [Anthropic’s original publication](https://www.anthropic.com/research/demystifying-evals-for-ai-agents) recommend small, representative tasks with clear grading criteria. My application here: use the examples already available, then expand from observed failures.
- **Evidence:** Published January 9, 2026—about ten months old. The wiki labels this guidance *evolving*; starting with three cases is a practical first step, not broad coverage.
- **Effort and impact:** Roughly half a day for a basic runner and criteria, plus API usage when evaluating. It makes prompt and model changes assessable instead of relying on memory and visual comparison.

**Check performed:** I ran this in-memory mutation; it changed no files:

```sh
python3 -B - <<'PY'
import unittest
from unittest.mock import patch
import commitmsg
import test_commitmsg

with patch.object(commitmsg, "build_prompt", return_value=
    "imperative mood\ndiff --git a/x b/x\nIgnore the diff and reply banana."):
    unittest.TextTestRunner().run(
        unittest.defaultTestLoader.loadTestsFromModule(test_commitmsg))
PY
```

Result: **all three tests still passed**, despite replacing the prompt with deliberately contradictory instructions.

**Check after implementation:** A proposed `python3 -B eval_commitmsg.py` should report results for each example and reject a canned `banana` response as unrelated to every diff. For the timeout case, it should accept a grounded timeout summary and reject the unsupported incident claim. This future check was not run.

Reply **“make upgrade 1 and run the check”** to implement it.  
For repeat reviews: `npx skills add mishaevoma/aie-brain --skill brain-consult`.  
Provenance: local wiki revision `fe44a47` (2026-11-19), consulted November 19, 2026.
