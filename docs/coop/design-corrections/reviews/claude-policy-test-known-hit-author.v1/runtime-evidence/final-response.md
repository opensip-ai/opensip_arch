I fixed both assigned problems in my own verified copy of frozen39. Afterwards the retained independent probe passes 50/50, and all 22 fixture-vs-composition comparisons agree. This is author correction work, not the active review's verdict; frozen39 and root's evidence are unaltered, which I re-verified at the end.

**Custody.** The frozen39 manifest sha matches (`f71a5992…569009`). All 12909 members were verified before and after copying into `work/source39`, with no faults and no unlisted files. The patch touches exactly 6 files, all modified, none added; the historical V1 files and the composition, identity and atom owners are byte-identical.

**P1: known hit under missing required evidence (confirmed).**
- **Cause:** `policy_test_model.v3.py` skipped the rule before evaluating any predicate whenever a required evidence kind was absent (frozen39 lines 214–218). Known findings were suppressed and could no longer make the verdict fail.
- **Law:** composition §5/§9.5 and `evaluator_composition_model.v3.compose` evaluate every subject. The missing evidence is a rule-level deficiency whatever the root value, but a live unwaived gating finding still makes it fail.
- **Reproduction:** a path-only rerun of the original probe on my copy failed exactly the P1 row, as root found. My comparison probe showed the fixture wrong for gating, waived, non-gating, below-threshold, two-subject and partial-Coverage cases.
- **Fix:** every subject is now evaluated.
  - Known findings (waived or live) and fail dominance are kept.
  - The rule is still listed in `indeterminateRules`, and subjects without a known finding stay unknown, so a known false result is not treated as an authoritative no-match.
  - Zero-subject cases, the optional-absent distinction and non-gating behaviour are unchanged.
- **Second defect in the same code:** the optional-absent disclosure also required complete Coverage. With partial Coverage but every native atom known, the fixture said indeterminate where composition says pass. I isolated this before correcting it and removed that condition.

**P2: universe tokens (real inconsistency).**
- **Law:** composition contract §2 closes the token map to `typescript`, `rust` and `syntax`. It refuses unknown tokens and says `typescript-v2` is not an alias. `evaluator_input_model.v3` enforces this for every rule.
- **Problem:** the policy-test route never applied it. My authored suites used `typescript-v2`, and arbitrary tokens were accepted. A typo in a fact's token silently became a no-match.
- **Fix, using existing refusal routes only:**
  - an unregistered rule token (enabled or disabled) is refused as `CONFIG.INVALID` / `POLICY.UNKNOWN_RULE`, remedy `EVALUATOR_POLICY_UNIVERSE_UNREGISTERED: <token>`;
  - an unregistered fact token is `CONFIG.INVALID`;
  - the authored fixtures now use `typescript`;
  - controls cover each registered token, facts from a different registered universe, and unknown rule, disabled-rule and fact tokens.

**Other owner changes**
- The schema's admission-precedence and representation-law text, including `ruleLaw`, which previously contradicted composition.
- Two sentences in contract §5.
- A new authored `requiredEvidenceSuite` in the fixture.
- 14 new `pt2` checks in the workflow checker.

One authored expected value changed: in case `partial-coverage-is-indeterminate-not-finding`, `runtime-hit` is no longer listed as indeterminate. Its only unknown cause is absent optional evidence, which composition §5 keeps at pass. That case's outcome, verdict and expectation outcomes are unchanged.

**Results (receipts in `receipts/`)**

| check | before | after |
|---|---|---|
| original probe (path-only rerun) | P1 failed | 50/50 |
| my comparison probe | 16 law failures (37 rows) | 37/37 |
| `check-workflow-projection.v3.py` | 838/838 | 852/852; 14 added, none removed or flipped |
| `check-composition.v3.py` | 30/30 | 30/30 |
| `check-query-projection.v3.py` | 204/204 | 204/204 |
| historical `check_workflows.v1.py` | 1816/1816 | 1816/1816; stdout byte-identical |
| `check-array-orders.py` | — | 123/123 |

Three failed attempts are kept:
- My first comparison-probe run had a harness bug: it counted a disabled rule as unknown.
- My first post-correction workflow-checker run failed only on the authored value above.
- The original probe writes to a fixed path, so its pre-correction row file was overwritten by the rerun. Its receipt stdout and root's reproduction still show the failure.

**Left unchanged:**
- `resolve_policy`, which `policy.show` also uses, still accepts any token; Run admission enforces the law. You may want `policy.show` to refuse earlier.
- An available-but-unrepresentable optional evidence atom stays blocking in the fixture; that is a representation limit, not a mismatch with production.

**Limits**
- The fixture is a bounded path-only fact view. The composition side uses check-composition-style synthesized inputs, with no full Run, native admission or provider execution; no claim depends on a full Run.
- The result record still can't say why a rule is indeterminate.
- Expected outcomes are mine; independent review is the oracle.
- The full launcher and other children were not run.

No background processes are running.

Files are in `/private/tmp/opensip-design-corrections/claude-policy-test-known-hit-author.v1`:
- review.md
- review.json
- output/correction.patch
- custody/delta-manifest.json
