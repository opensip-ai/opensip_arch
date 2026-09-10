I’ll do a bounded read-only peer review of the six SHOULD findings against the current fault files, run the required checker, and write only `review.md`/`review.json` in this output folder.I’ll hash the current fault sources, run the 38-control checker, and probe each of the six SHOULD items against the live files.Six original SHOULDs are closed against the live files. I’ll write only `review.md` and `review.json` in the recheck folder, with hashes and the remaining residuals.Six original SHOULD findings are **closed**. Recheck is in `/tmp/opensip-design-corrections/grok-fault-recheck.v1/review.md` and `review.json`. Checker: **38/38** with `/tmp/opensip-architecture-review-env/bin/python -I -B`.

**Closed (measured):**
1. Illegal pairs fail `C.validate` (`anyOf` 24 = `x-opensip-routes` 24).
2. `owner_observation` equals identity `EvidenceUnavailable` / `RegenerationMismatch` on the full termination, including remedy and subject.
3. Native origin map is published; map values ⊆ native `possibleOrigins`; evaluator-only origins stay unmapped.
4. Both replay origins require a nonempty `reference`.
5. Pointer omission uses registered `EVALUATION.REQUIRED_OUTPUT_OMITTED` (DomainDetail, not a new D9 code).
6. Output-bound carries `{field, observed, maximum}`; routed subject is `proof.predicates:100001>100000`.

**MUST:** none.

**Remaining (residuals, not reopenings):**
- `observed == maximum` is still schema-valid; only `route()` raises `EVALUATOR_FAULT_NOT_OVER_LIMIT`.
- Origin map is annotation; `route()` does not call `public_termination_for`.
- Checker does not assert `anyOf` == routes.

Workflow Run-on-failure and code-list prose were left to that owner. Atom files were not edited. LIVE D9 artifact was not treated as a design blocker. Not whole-source acceptance.
