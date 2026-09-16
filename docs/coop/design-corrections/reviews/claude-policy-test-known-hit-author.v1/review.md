# Policy-test known-hit and universe-token correction (bounded author work over frozen39)

Coauthor origin 823bf66b-e92a-4789-ab81-63a1a9dc371d. Runtime `R=/private/tmp/opensip-design-corrections/claude-policy-test-known-hit-author.v1`.

**Standing.** This is a bounded AUTHOR reference/design correction, made in my own disposable capture of verified frozen39.
- **Not an assessment:** not independent acceptance, and not the active independent review's verdict.
- **Nothing else altered:** no frozen, LIVE or other-review artifact.
- **No successor claimed:** no source40.
- **No side effects:** no product work, commits, pushes, planning, pins or report regeneration.

`R/review.json` is built by `R/build_review.py`, which recomputes every claim below and refuses on mismatch.

## 1. Custody

**Frozen39 manifest.**
- Path: `/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v39.json`
- sha256: `f71a59928d1b6aa84eed81b8cb49fd1fba91c65dd6599c58f99efcdc42569009`, matching the expected value.

**Member verification.** All 12909 members under `/tmp/opensip-design-corrections/candidate-subject.v39` (737605070 bytes) were verified before and after the copy:
- no digest or size fault;
- no unlisted file and no `__pycache__`;
- no copy fault.

**Capture.** `R/work/source39` holds fresh regular files; the record is `R/custody/frozen39-capture.json`.

**End of work.** `R/custody/end-of-work-recheck.json` shows:
- All members were re-verified at the snapshot root: frozen39 is unaltered.
- Root's counterexample files still match their recorded probe hashes.

**Evidence read.** Root's `assessment.json`, `claude-original-probe.py`, `rerun-probe.py`, `path-only-adaptation.diff`, `stdout.json`, `stderr.txt` (empty), `command.json` and `receipts/probes/policy-test.json`.

**Delta.** Exactly 6 modified files, no additions.
- Patch: `R/output/correction.patch`, sha256 `8fe83cd122eefeec384f4d48aebc2c2eaa505a5c1a1bac5958c6fe74672a9f28`, 790 lines.
- Manifest: `R/custody/delta-manifest.json`, with base and after hashes per file.
- **Byte-identical owners:**
  - historical `PolicyTestSuiteV1` schema, `workflows_model.v1.py`, `workflow-cases.v1.json` and `check_workflows.v1.py`;
  - the composition model and contract;
  - `identity-schemas.v3.json`, the atom owner and the public detail registry.

## 2. Owning law read

**`foundation/evaluator_composition_model.v3.py`, `compose`, rule loop.**
- Every selected subject is evaluated.
- `unknown` includes `requiredEvidenceDeficiencies` regardless of the root.
- Outcome: `fail` if gating and a live unwaived finding exists; else `indeterminate` if gating and unknown; else `pass`.
- `blocks()`: native, enumeration and execution causes, plus imports of a required kind.

**`foundation/evaluator-composition-contract.v3.md`.**
- **§2 (line 26):** "The closed policy universe token map is typescript→…, rust→…, syntax→…. Unknown tokens refuse admission; historical illustrative tokens such as typescript-v2 are not additional implicit aliases."
- **§3:** Kleene logic; known matches are preserved; optional imported evidence never acquires gating authority.
- **§5 (line 56):**
  - a required-import deficiency makes a gating rule indeterminate "whatever its root value", unless a live unwaived finding makes it fail;
  - an optional-only root unknown stays pass;
  - an advisory rule stays pass.
- **§9.5:** required-import deficiency rows apply to enabled rules only.

**`foundation/check-composition.v3.py` A9 controls**, including `a9-known-live-failure-dominates-missing-required-import`.

**`foundation/identity-schemas.v3.json`:** `x-opensip-evaluator-profile.policyUniverseMap` = `{typescript, rust, syntax}`.

**`foundation/evaluator_input_model.v3.py`:** `EVALUATOR_POLICY_UNIVERSE_UNREGISTERED` for every rule, and token → portable domain.

**Current policy-test owners:** `policy_test_model.v3.py`, the `workflows_model.v3.py` policy section, the evaluator3 policy-test schema, the authored cases, and the checker's `pt2` block.

**`workflows-and-surfaces.md`:**
- §5 DSL and authoring test;
- lines 1575–1580: "Missing required evidence and incomplete coverage follow the same rule; neither can silently become an authoritative no-match."

## 3. Diagnosis

### P1 (confirmed, reproduced before correction)

`policy_test_model.v3.evaluate` hit `if required - available: …; continue` (frozen39 lines 214–218) before evaluating any predicate. As a result, a known true root emitted no finding and could not make the verdict fail.

**Reproduction.** A path-only rerun of the retained probe against my capture (`R/probes/original-probe.path-only.py` with its diff) gave 50 rows, with the only failure being P1 `known-native-hit-under-missing-required-evidence-agrees-with-composition`. That matches root.

**My bounded comparison probe** (`R/probes/known_hit_universe_probe.py`, pre-correction v2) runs 22 fixture-vs-composition scenarios. The fixture diverged in 7:
- known true, required absent: gating unwaived, waived (finding dropped), non-gating and below-threshold (findings dropped), and two subjects (one true, one false; wrong verdict and dropped finding);
- the same under partial Coverage;
- plus one adjacent defect: optional-only disclosure under partial Coverage (below).

The other 15 agreed, among them:
- known-false AND under missing required evidence;
- the optional-absent-only unknown root;
- `not`-unknown;
- both zero-subject cases;
- native unknown under partial Coverage;
- the disabled rule.

### Adjacent defect in the same rule-accounting code (discriminated before correction)

The optional-evidence-absent disclosure also required `complete` Coverage. With partial Coverage but every native atom known, `and(known true, optional-absent)` was fixture `indeterminate` vs composition `pass`. Composition blocks only on native causes or required-import causes.

My first pre-correction run did not isolate this. It is kept as a failed attempt, together with a harness bug: I derived rule-unknown for a disabled rule. Pre-correction run v2 isolates it.

### P2 (actual inconsistency)

- **Unapplied law:** composition §2 closes the token map, and the evaluator input admission refuses any other token for every rule. The policy.test route never applied that law.
- **Wrong token in the fixtures:** both authored suites used `typescript-v2`.
- **Arbitrary tokens accepted:** arbitrary rule and fact tokens were admitted. A fact-token typo silently became a no-match: before correction, a fact with `typescript-v2` against a `typescript` rule gave `exists` false with no finding.
- **Why this is not just labelling:** a candidate accepted this way could never be enforced.

## 4. Correction (smallest coherent delta)

### `workflows/policy_test_model.v3.py`
- **Evaluate every subject.** Every enumerated subject is evaluated regardless of evidence.
- **Missing required kind** is a blocking rule-level deficiency:
  - the rule is listed in `indeterminateRules` and is gating-unknown;
  - known findings, waived or live, are kept, and fail dominance is preserved;
  - subjects without a known finding stay unknown, so a known false root is not an authoritative no-match;
  - with zero subjects, the rule is still listed.
- **Unknown roots** block unless their only causes are absent optional evidence. The `complete` precondition is removed; Coverage and uncertain-match causes remain blocking.
- **Universe tokens:** `POLICY_UNIVERSES` is read from the evaluator profile, not re-declared. A fixture fact with an unregistered token is a fixture fault. A new `unregistered_universes(policy)` helper lists rule tokens outside the map.

### `workflows/workflows_model.v3.py` (policy section only)
After the current resolver, an unregistered rule universe (enabled or not) is a resolver refusal:
- route: `CONFIG.INVALID` / `POLICY.UNKNOWN_RULE`;
- remedy: `EVALUATOR_POLICY_UNIVERSE_UNREGISTERED: <token>`;
- subject: the rule id.

This reuses an existing route, with no new error code, detail, golden or registry row.

### Normative text
- **`schemas/evaluator3/policy-test.schema.json`:** admission precedence steps 4 and 5; representation law `subject`, `factUniverse` and `ruleLaw`, restated to the composition law. The previous `ruleLaw` sentence contradicted composition.
- **`workflows-and-surfaces.md` §5:** fixture fact token fault; the universe resolver refusal; required evidence never suppresses a known finding.

### `workflows/policy-test-cases.v3.json`
- **Tokens:** 12 `typescript-v2` selectors become `typescript`, as explicit new construction.
- **New suite:** an authored `requiredEvidenceSuite` with 4 rules and 5 cases, plus expected outcomes, covering:
  - a known gating hit and an advisory hit under missing required evidence;
  - a known false root;
  - a waived hit;
  - required evidence present;
  - no selected subjects;
  - optional-only unknown under partial Coverage.
- **One authored expected value changed.** In `currentSuite` case `partial-coverage-is-indeterminate-not-finding`, `indeterminateRules` no longer lists `runtime-hit`: its only unknown cause is absent optional runtime evidence, and composition §5 keeps that rule at pass. The case outcome, verdict and all expectation outcomes are unchanged. This expected value surfaced as the single failure of the first post-correction checker run, which is retained.

### `workflows/check-workflow-projection.v3.py`
14 new `pt2` checks:
- **Required-evidence behaviour:**
  - suite admission and outcomes;
  - a known gating hit survives and fails;
  - a known false root is not an authoritative no-match;
  - a waived hit keeps the unknown;
  - no selected subjects stay indeterminate;
  - optional-only disclosure under partial Coverage.
- **Universe tokens:**
  - authored suites use closed tokens;
  - each registered token gives the same outcomes;
  - facts of another registered universe never occupy (a discriminating valid control);
  - `typescript-v2`, arbitrary and disabled-rule tokens are resolver refusals;
  - an unregistered fact token is `CONFIG.INVALID`.

### Identity effects
- **Changed:** the authored `currentSuite` `suiteDigest` and `policyTestResultId`, because the selector bytes changed (value in `review.json`).
- **Unchanged:**
  - the pinned historical workflow1 id;
  - `PolicyTestResultV1` / `CaseResult` shape, which needed no change;
  - schema majors, goldens and detail registry.

## 5. Results (`R/receipts/`)

| receipt | exit | result |
|---|---|---|
| pre-correction-original-probe | 0 | 50 rows; failed exactly P1 known-hit (reproduced) |
| pre-correction-known-hit-universe-probe | 0 | retained failed attempt (35 rows; disabled-rule harness bug, partial scenario not discriminating) |
| pre-correction-known-hit-universe-probe.2 | 0 | 37 rows, 16 law failures (7 K, 3 E, 6 U) |
| baseline-check-workflow-projection-v3 / composition / query / workflows-v1 | 0 | 838/838, 30/30, 204/204, 1816/1816 |
| post-correction-known-hit-universe-probe (.2 final) | 0 | 37/37 law rows; all 22 composition comparisons agree |
| post-correction-original-probe (.2 final) | 0 | 50/50; P1 agrees with composition |
| post-correction-check-workflow-projection-v3 | 1 | retained: only `pt2-admitted-current-suite-reaches-the-authored-outcomes` (the authored value above) |
| post-correction-check-workflow-projection-v3.2 | 0 | **852/852**: 14 added `pt2-*`, none removed or flipped |
| post-correction-check-composition-v3 / query-projection-v3 | 0 | 30/30, 204/204 |
| post-correction-check-workflows-v1.2 | 0 | 1816/1816; stdout byte-identical; report differs only in its source hash table |
| post-correction-check-array-orders | 0 | 123/123 |
| make-delta | 0 | manifest and patch above |

**Fixture vs composition after correction:**

| scenario | fixture verdict / findings / listed | composition verdict / findings / unknown |
|---|---|---|
| or(true, test) required absent, gating | fail / a / listed | fail / a / unknown |
| and(false, test) required absent | indeterminate / — / listed | indeterminate / — / unknown |
| or(true, test) optional absent | fail / a / — | fail / a / — |
| waived true, required absent | indeterminate / a (waived) / listed | indeterminate / a (waived) / unknown |
| non-gating true, required absent | advisory / a / listed | pass / a / unknown |
| no selected subjects, required absent | indeterminate / — / listed | indeterminate / — / unknown |
| and(true, optional absent), partial Coverage, natives known | pass / — / — | pass / — / — |
| two subjects (true, false), required absent | fail / a / listed | fail / a / unknown |

**Universe after correction.**
- **Admitted:** `typescript`, `rust` and `syntax`.
- **`POLICY.UNKNOWN_RULE`:** `typescript-v2`, arbitrary and disabled-rule tokens.
- **`CONFIG.INVALID` at fixture admission** (which precedes the resolver): an unregistered fact token, and rule plus facts both unknown.

**Expectation law after correction:**
- a known hit under missing required evidence is a met finding (fail);
- a known false root gives `indeterminate` for no-finding;
- mixed subjects give `met` / `indeterminate` / `unmet`;
- zero subjects give `met`;
- a waived hit gives `met` with verdict `indeterminate`;
- optional-only absence gives no-finding `met`.

No background process is running.

## 6. Observations (not changed; outside the assigned boundary)

- **`policy.show` still accepts any universe token.** `workflows_model.v3.resolve_policy`, which `policy.show` also uses, does not apply the token law. Run admission enforces it in `evaluator_input_model.v3`. Root may decide whether `policy.show` should refuse earlier.
- **An optional-kind atom whose evidence is available but unrepresentable stays blocking in the fixture.** Production could evaluate that observation as true, so this is a fixture representation limit. It is not the production optional-unknown law, and it is not compared with composition.

## 7. Limits

- **Bounded harness.** The fixture is a finite path-only fact view. The composition side uses check-composition-style synthesized population, Plan and closure locators with scanner values. There is no full retained Run, native admission or provider execution, and no claim here depends on a full Run.
- **Comparison mapping.** Fixture `advisory` maps to composition `pass`. Composition rule-unknown is derived from required-evidence rows, or from an indeterminate root whose witness carries a §5 blocking cause.
- **Result shape.** `PolicyTestResultV1` / `CaseResult` carry no per-rule unknown cause, and the optional-absent disclosure stays internal to the model.
- **Overwritten pre-correction rows.** The retained original probe writes a fixed output path, so its pre-correction detail file was overwritten by the rerun. The pre-correction receipt stdout and root's retained reproduction remain.
- **Oracle.** Authored expected outcomes are author expectations aligned to the owning laws; independent review is the oracle.
- **Checks run.** Only the workflow projection, query, composition, historical workflow1 and array-order checkers were run, not the full launcher. The independent review's final verdict may contain more findings.
