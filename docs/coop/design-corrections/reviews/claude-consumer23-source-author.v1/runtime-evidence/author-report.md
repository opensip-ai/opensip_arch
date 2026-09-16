# Author report: consumer23 source clarifications (V23-S1, V23-S2, V23-S3)

**Standing: authorship only.** Origin `823bf66b-e92a-4789-ab81-63a1a9dc371d`. This is not independent acceptance, blind B, successor, final-application or readiness agreement, or product qualification. Nothing was committed or pushed.

**What I touched.** I wrote only to:
- the assembly `/tmp/opensip-design-corrections/consumer23-source-clarifications.v1/source`;
- this runtime.

**What I left alone.** I did not edit:
- frozen36 or the live repository;
- previous evidence, pin ledgers or generated reports;
- planning layers or freezes.

I did not touch the other reviewer's runtime or the blind consumer.

**How commands ran.** Every command used `/tmp/opensip-architecture-review-env/bin/python -I -B`. Each one's argv, cwd, stdout, stderr, exit code and SHA-256 digests are kept under `probes/receipts/`, including failed runs. `author-report.json` is built by `build-author-report.py` from those receipts and the manifests.

## 1. Custody and changed files

**Custody check.** `after-manifest.json` compares the whole assembly against frozen36 hash by hash:
- both trees have 12,899 files, with none added or removed;
- exactly **6** files differ from frozen36;
- nothing changed outside the target list.

The frozen36 manifest file (`a729406b…4235`) is not readable from here, so the tree comparison stands in for it.

**Where the images are.** Before-images are in `before/`, after-images in `after/`, and full diffs in `diffs/`.

| Owner file | frozen36 sha256 | after sha256 | diff |
|---|---|---|---|
| `workflows/query-projection-contract.v3.md` | `69b2298d…` | `6a409247…` | +8/−6 |
| `workflows/query_projection_model.v3.py` | `4c9c9121…` | `0c7150b9…` | +17/−5 |
| `workflows/check-query-projection.v3.py` | `f90f1001…` | `2beb8a7d…` | +43/−0 |
| `v2/contracts/product-v1/native-evidence.md` | `1cfc8fcc…` | `b74c0741…` | +46/−4 |
| `native/native_evidence_model.v2.py` | `bf25f8bf…` | `2ea98af4…` | +81/−9 |
| `native/native-cases.v2.json` | `58b2d77d…` | `1194d905…` | +82/−0 |

**Schema file reverted.** `native/native-evidence.schemas.v2.json` was edited, then put back to exact frozen36 bytes (`3e37c7b7…`); see §3.

## 2. V23-S1: package endpoint without a coordinate

**The finding holds.** Section 2 sent a package endpoint with no `packageManifestPath` to `QUERY.ENDPOINT_AMBIGUOUS`. But `GraphEndpoint` requires that coordinate, and section 8 step 1 checks the request against the schema first. So the public wrapper already returned `QUERY.PARAMS_MALFORMED`. The ambiguous branch in `parse_endpoint_syntax` could not be reached through `execute_graph_query`.

**Fix: the schema check comes first.**
- Anything `GraphEndpoint` rejects is `QUERY.PARAMS_MALFORMED`, including a package endpoint without a non-empty coordinate.
- That refusal happens before any Run, view, availability observation or vertex is looked at.
- `QUERY.ENDPOINT_AMBIGUOUS` is kept only for a well-formed, complete tuple that matches more than one admitted vertex.

**Where the fix lands.**
- **Contract:** section 2 precedence, and the section 7 rows for malformed input and for ambiguity.
- **Model:** the helper branch and its docstrings.
- **Public behaviour:** unchanged.

**Why not the consumer's suggested fixes.**
- *Reclassify when the coordinate is the only schema fault.* That needs a second admission with a placeholder coordinate, and it would call an incomplete request "ambiguous".
- *Loosen the schema.* That weakens strict public admission and lets through a tuple that can never resolve.

**Limit.** `inventory_vertices` keys vertices by the full tuple, so the reference public wrapper can never return `ENDPOINT_AMBIGUOUS`. Only a helper-level control covers that code.

## 3. V23-S2: native deficiencies must follow the existing D9 codes

**The finding holds, and the problem went beyond the table.**
- **Section 10 table.** It gave `VERDICT.INDETERMINATE` for `language-tier-unsupported`, `confidence-floor-unmet` and `required-relation-missing`. D9 v1.14 (`codeMaps.deficiencyToReasonCode`) ends those Runs with the matching `COVERAGE.*` codes.
- **`run_termination`: successful stage.** It only special-cased `provider-unavailable`, so it also returned `VERDICT.INDETERMINATE` for `budget-exhausted` (root's observation, confirmed).
- **`run_termination`: `BudgetExhausted`/`Unavailable` stage.** It kept the stage's code even when an entry carried a higher-precedence deficiency. The code and the typed detail could then name different deficiencies, and `nativeCauses` was always `[]` there.

The consumer suggested calling the section 10 columns the per-requirement route. I did not take that: it contradicts the D9 owner. The per-requirement code is `REPAIR.EVIDENCE_RUN_UNAVAILABLE`.

**The rule now written in section 10.**
- **What the columns are.** They are the whole-Run termination code for the Run's primary deficiency, and D9 owns them.
- **How native maps into D9.** The five `DeficiencyV2` members that also exist in `D9Deficiency` map to themselves. The other four map to `verdict-indeterminate`, which gives `VERDICT.INDETERMINATE`.
- **How the primary deficiency is chosen.** Section 10 precedence picks it from the entry deficiencies plus the deficiency a clean typed stage terminal implies.
- **Faulted or cancelled stages** keep their own termination.
- **Per-requirement codes are separate.** The `DeficiencyV2` outcome and the `REPAIR.EVIDENCE_RUN_UNAVAILABLE` rule are unchanged, and no D9 class, code or exit changed.
- **Model changes.**
  - New `native_deficiency_d9`: total over the nine members, and it refuses anything else.
  - New `d9_route_drift`: checks the mapping against `DeficiencyV2` and the D9 contract's own map.
  - `run_termination` now uses the new mapping.
  - `D9_MAP` is left alone: it is keyed by detail code, and `check-integration` requires those keys to be registered details.
- **Also updated:** the fault-law sentence and the section 13 H-3 list of codes in use.

**Scope of the helper.** `run_termination` returns **one** primary code. The ordered `reasonCodes` list with `secondaryDeficiencies` in D9's cause model is built by the host, not by this helper.

**What changed, frozen36 vs assembly** (`p2-discrimination.2`, 24 stage × entry rows, 11 changed):

| Stage | Entries | frozen36 | assembly |
|---|---|---|---|
| success | budget / tier / floor / missing relation | `VERDICT.INDETERMINATE` | the matching D9 `COVERAGE.*` code |
| success | resolution-incomplete + budget | `VERDICT.INDETERMINATE` | `COVERAGE.BUDGET_EXHAUSTED` |
| budget-exhausted | tier / provider | `COVERAGE.BUDGET_EXHAUSTED` | `COVERAGE.LANGUAGE_TIER_UNSUPPORTED` / `COVERAGE.PROVIDER_UNAVAILABLE` |
| budget-exhausted | input-closure | `COVERAGE.BUDGET_EXHAUSTED` | `VERDICT.INDETERMINATE` (input-closure outranks budget; less specific public code, by section 10 precedence) |
| unavailable | tier | `COVERAGE.PROVIDER_UNAVAILABLE` | `COVERAGE.LANGUAGE_TIER_UNSUPPORTED` |
| unavailable | provider / input-closure | code unchanged | `nativeCauses` `[]` → the entries' causes |

In the budget-exhausted rows that changed code, `nativeCauses` also now carries the entries' causes.

**Schema annotation: left for root.** I edited the `publicD9Termination` annotation in `native-evidence.schemas.v2.json`. That broke `check-identity` `v20-native-view-fixture-declares-current-registered-schemas`: the document's raw SHA-256 is a registered `payloadSchemaDigest`, which is part of every `coverage2` id. I restored the exact frozen36 bytes. The annotation already defers to "the section 10 table columns", which are now correct; only its example list is incomplete. The exact current and proposed text is in `author-report.json#/decisions/V23-S2/schemaAnnotationNotChanged`. It should be applied only together with a deliberate schema re-registration.

## 4. V23-S3: availability states on graph queries

**The finding holds, as a gap in the published text.** The model already refused `unavailable` with `evidence.missing` (`AVAIL_REFUSE`), but section 7 only said `evidence.*`.

**Now written in section 7** (one paragraph and two table rows):

| availability.state | Class / code / exit | Detail |
|---|---|---|
| `purged` | operational-failed / `HOST.IO_FAILURE` / 4 | `evidence.purged` |
| `expired` | operational-failed / `HOST.IO_FAILURE` / 4 | `evidence.expired` |
| `corrupt` | operational-failed / `HOST.IO_FAILURE` / 4 | `evidence.corrupt` |
| `unavailable` | operational-failed / `HOST.IO_FAILURE` / 4 | `evidence.missing`, the identity owner's `EvidenceUnavailable` carrier |
| `retained`, `partial`, or no observation | no refusal on its own | no Run authority either; `close_run` decides on missing or corrupt bytes |

- **No new vocabulary:** no enum or detail was added.
- **Unchanged:** `finding.show` exit 2 and the other seventeen operations.
- **Model:** only a comment changed.

## 5. Advisories

- **V16-A3: kept as an advisory, no change.**
  - graph-query `TraversalCoverage` already says "Not native CoverageResult".
  - The two obligations are separate required fields.
  - The consumer's note says the phrase appears "in both places", but the native schema does not mention traversal at all.
  - Renaming a public field would be a major version change made only for wording.
- **V23-A1: kept as an advisory, no change.**
  - workflows-and-surfaces §1 Cancellation already fixes the outcome: interrupted (130), remaining steps cancelled, and an aborted analysis leaves no Run.
  - The command-inventory golden `interrupted-before-settle` fixes class `interrupted` and exit 130.
  - Every parity field is identical under either lawful envelope kind.

## 6. Controls

Final assembly results come from the `.3` receipts, run after the self-review fix in §7.

| Check | frozen36 | assembly |
|---|---|---|
| `check-query-projection.v3.py` (report written to this runtime) | 123, 0 failed | **138, 0 failed** |
| `native-cases.v2.json` via `run_case` | 375/375 | **377/377** |
| `foundation/check-identity.py` (report written to this runtime) | 1596 passed / 0 failed | **1596 passed / 0 failed** |
| `check-integration.py` (report written to this runtime) | 412 passed / 0 failed | **412 passed / 0 failed** |

**15 new query controls.**
- **S3 (8):**
  - `corrupt` and `unavailable` are refused through the public wrapper;
  - each of the four refusing states gives an operational-failed envelope, exit 4 and the exact detail;
  - `partial` neither refuses nor grants;
  - `partial` still cannot admit missing bytes.
- **S1 (7):**
  - a missing or an empty coordinate is malformed;
  - so is a path target without a coordinate;
  - the malformed refusal comes before both the Run/view join and a purged observation;
  - the helper agrees;
  - a well-formed package tuple outside the domain is `ENDPOINT_UNKNOWN`;
  - a helper-level control reserves ambiguity for complete tuples.
- **Against frozen36 (P2):** only `endpoint-helper-agrees-package-without-manifest-path-is-malformed` fails there. The other 14 lock in wrapper behaviour frozen36 already had but never published.

**2 new native cases.**
- **`native-deficiency-whole-run-route-is-total-and-d9-owned`** covers the nine rows, the refusal of unknown inputs, and the drift check.
- **`run-termination-code-is-the-primary-deficiency-route`** covers the stage and precedence boundaries.
- **Against frozen36 (P3):** both fail under the frozen36 model. The second fails on real results: it gets `VERDICT.INDETERMINATE` where budget, tier, floor, missing relation and precedence expect `COVERAGE.*` codes, the stage-precedence code is wrong, and `nativeCauses` is `[]`.

**No existing expectation was changed.** Every original control and case still passes.

## 7. Failed attempts and self-review fix

**Failed attempts, kept as receipts.**
- `identity-assembly`: 1595 passed, 1 failed, caused by the schema annotation edit. Rerun passed after the revert.
- `p2-discrimination`: exit 1 from the same digest mismatch. Rerun as `p2-discrimination.2`.

**Fix found in my own diff review.** The new native-evidence.md fault-law sentence cited `native-deficiency-whole-run-route-is-total-and-d9-owned` for stage-terminal precedence. That behaviour is held by `run-termination-code-is-the-primary-deficiency-route`. I corrected the citation. I then reran native cases, query, identity and integration (the `.3` receipts, 0 failures) and regenerated the after-images (`snapshot-after.2`).

## 8. For root

- **Stale pin rows.** 30 rows hold frozen36 hashes of the six changed files: 6 each in `foundation/evaluator3-source-pins.v1.json`, `foundation/source-pins.v1.json`, `native/source-pins.v2.json`, `security/source-pins.v1.json` and `workflows/source-pins.v1.json`. No new pins are needed.
- **Other files holding frozen36 hashes of the changed files** (not edited by me):
  - `docs/v2/architecture/implementation-normative-inputs.v4.json`, `implementation-planning-sources.v1.json` and `implementation-coverage.v1.json`;
  - `workflows/workflows-report.v1.json`;
  - historical review evidence, which stays as history.

  Exact counts are in `author-report.json#/forRoot`.
- **Generated report:** `native/native-evidence-report.v2.json` records 375 cases; the assembly now has 377.
- **Schema annotation:** decide on it together with a schema re-registration.
- **Remaining steps:**
  - run all six groups and planning;
  - freeze;
  - get independent successor review;
  - get blind reconstruction;
  - get a fresh final application review.

## 9. Limits and carried state

- **S2 evidence** comes from calling helpers directly: no Coverage admission of `run_termination` inputs, no complete Run, and no closed enumeration.
- **`QUERY.ENDPOINT_AMBIGUOUS`** cannot be reached through the reference wrapper.
- **Not run by me:** the native checker's `main()` (it verifies pins and writes a report into the tree), the six integrated groups, the planning checks, and pin validation.
- **Carried unchanged:**
  - one TCB-SCOPE-01 assumption with 13 dependent residual accounts;
  - 32 product gates and 54 planned recovery cases, none performed.
- **Standing:** source acceptance stays reopened, and this report grants nothing.
