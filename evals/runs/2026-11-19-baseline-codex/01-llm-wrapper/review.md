**Keep the single-call design; first fix the examples so they reward accurate commit messages.** I traced staged diff → prompt → API call → printed message and ran all three unit tests successfully. Assuming this is a personal CLI prototype, two improvements matter most.

1. **The timeout reference expects information the model never receives.**  
   `examples/002-timeout.msg:3` describes a six-hour nightly-sync incident, but the corresponding diff only adds `timeout=10`. `commitmsg.py:22` supplies no incident context. Comparing against this reference could penalize a grounded answer or reward invented history.

   My recommendation: remove that body from the reference and explicitly require messages to use only supplied facts. If incident explanations are essential, add an explicit context input.

   Proposed check: generate from `002-timeout.diff`; accept a correct timeout summary and reject unsupported incident claims. This follows the Brain’s [eval guidance](https://mishaevoma.github.io/aie-brain/concepts/evals.md) on unambiguous tasks and valid references, backed by [Anthropic, January 9, 2026](https://www.anthropic.com/research/demystifying-evals-for-ai-agents/).

2. **Passing tests establish plumbing, not message quality.**  
   `test_commitmsg.py:20–35` checks whitespace trimming, prompt fragments, and forwarding the model constant. The fake supplies the answer, so these tests cannot detect inaccurate summaries or broken style rules. I also confirmed that `generate()` accepts a simulated 100-character subject despite the 72-character rule.

   Keep these unit tests and the existing manual review. My recommendation: add a small example runner that records actual outputs, checks subject length and punctuation, and uses explicit human pass/fail criteria for accuracy and unsupported claims. Exact wording need not match the `.msg` files.

   Proposed check: run the examples before and after a prompt change; inspect failures against the same criteria. The same dated eval source supports combining deterministic checks with human judgment; its guidance is over six months old, so I’m applying the methodology, not its model-performance claims.

The direct API call is appropriate for this bounded task. This aligns with [Anthropic’s simplicity guidance, December 19, 2024](https://www.anthropic.com/research/building-effective-agents); that older article explicitly notes that its tooling landscape has changed.

Verified: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v` — **3 passed**. No files changed or live model calls made; model availability and actual generation quality remain unverified.

*Provenance: published AI Engineering Brain wiki and linked review procedure, consulted November 19, 2026.*
