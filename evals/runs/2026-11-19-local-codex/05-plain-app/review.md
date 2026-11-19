The main upgrade is to validate model replies before saving tickets. A second is to turn the 40 labelled examples into a real classification check. I used the requested **brain-consult** skill and left the project unchanged.

Assuming the README describes an active five-person helpdesk, incorrect routing matters. The current single-call design is appropriately simple.

**Upgrade 1: Reject invalid categories before they reach SQLite.**

- **Change:** In `app/tagging.py:25`, validate the response shape and membership in `CATEGORIES` after normalization. In `app/cli.py:21`, handle failure with an actionable error before inserting anything. Keep the existing normalization and injectable client.
- **Observed:** An injected reply of `other` was accepted and stored. My in-memory reproduction printed:
  ```text
  stored: other | all open: 1 | category-filtered: 0
  ```
  The ticket remains in the unfiltered list but disappears from every supported category filter.
- **Why:** The [tool-design page](https://mishaevoma.github.io/aie-brain/concepts/tool-design.md) says deterministic code should validate model proposals, citing the [dated source note](https://mishaevoma.github.io/aie-brain/sources/2025-03-30-humanlayer-12-factor-agents.md) for [12-Factor Agents](https://github.com/humanlayer/12-factor-agents). Applying that boundary to classification is my inference.
- **Check:** Add regression cases for unknown labels, empty content and non-text responses; assert that the CLI inserts no ticket and reports a useful error. Run:
  ```sh
  python3 -B -m unittest discover -s tests -v
  ```
  I ran this command today: **5 tests passed**, but none covers these failures. The proposed regressions have not been implemented.
- **Evidence:** March 30, 2025—about 20 months old; **older, still valid** because the wiki marks this principle settled and reviewed November 17, 2026.
- **Effort and impact:** Small change; prevents tickets silently falling outside staff’s category queues.

**Upgrade 2: Measure classification quality using the existing labelled tickets.**

- **Change:** Add an evaluation runner for `data/labelled_tickets.csv`, calling the actual `tag_ticket` function and reporting accuracy, per-category errors, invalid replies and API failures. Document its command in the README and rerun it after prompt or model changes. Keep the fast mocked unit tests.
- **Observed:** All 40 examples exist, but no application or test code reads them. Both classifier tests supply the expected response themselves.
- **Why:** The [evals page](https://mishaevoma.github.io/aie-brain/concepts/evals.md), [January 9 source note](https://mishaevoma.github.io/aie-brain/sources/2026-01-09-anthropic-demystifying-evals.md), and [Anthropic’s original publication](https://www.anthropic.com/research/demystifying-evals-for-ai-agents) recommend starting with a few dozen realistic cases and deterministic grading. Although the wiki marks evaluation practice evolving, this project already has suitable starting data.
- **Check:** I ran:
  ```sh
  rg -n 'labelled_tickets|csv|tag_ticket' app tests README.md
  ```
  Only the README references the dataset. A proposed command, `python3 -B -m app.evaluate`, should evaluate all 40 rows, print mismatches and fail against an explicitly chosen quality threshold. It does not exist yet.
- **Evidence:** January 9, 2026—about 10 months old. No published benchmark score is being assumed for this classifier.
- **Effort and impact:** A few hours plus model-call costs; establishes whether routing works and whether later changes improve it.

I did not call the live model, so model availability and actual classification accuracy remain unverified.

Reply **“make upgrade 1 and run the check”** to implement the first change.  
For repeat reviews: `npx skills add mishaevoma/aie-brain --skill brain-consult`.  
Provenance: local wiki revision `fe44a47` dated November 19, 2026; consulted November 19, 2026.
