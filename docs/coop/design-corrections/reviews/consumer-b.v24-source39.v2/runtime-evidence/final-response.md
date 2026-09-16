Final-chain status so far:
- Run-termination: 28 Runs, 9 candidate checks and 30 compositions, 0 failures.
- Phase 8 envelopes: 0 failures.
- Graph query: 53 vectors, 0 failures.
- Phase 8 compare: 0 failures.
- From-scratch: all 27 claimed positives admit through owner graph admission, the independent retained closure and fresh-process replay, with reachable-set equality. The designed negative `syntax-mixed-falsecomplete` still refuses at owner admission.

Still running are the admission log, replay export and the final run-termination pass. Everything left depends on those finishing:
- the negatives rerun with the fixed remint;
- the v1→v2 provenance diff;
- notes 09, 10 and 11;
- checkpoints 4–11;
- `blind-review.md`/`.json`.

I'll pick up as soon as the chain reports completion.
