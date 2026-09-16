# Independent review: report projection and fit owner candidate02 (`m1-report-projection-subject-02`)

**Verdict: CHANGES REQUIRED.** This is a substantial and mostly sound correction, but it is not yet acceptable. Six new findings remain: three blocking and three required.

- **Closed:** RPR-2, RPR-3, RPR-6, RPA-2, RPA-3 and RPA-5.
- **Partly closed:** RPR-1, RPR-4, RPR-5, RPR-7, RPR-8 and RPA-1.

Nothing here infers product, M4, browser, generator or performance qualification.

Machine-readable form: `review.json`. Evidence scripts and outputs: `work/`.

`subjectManifestSha256`: `4ebe027990867dcafc8a0f3439aa60c3bf84953e5221ce5b1d0d968243aa4551`

## Subject verification

**Before review:**
- The manifest SHA-256 matched, and all 9 files matched by hash and byte length.
- The subject directory had no extra or missing entries.

**Frozen subject fails its own checker.** `check.py` on a byte copy of the 9 frozen files exits 1 with `FileNotFoundError: build_owner.py` (`work/check-stderr.txt`). See RPR2-5.

**Augmented copy passes.** I added `build_owner.py` and `build_fixtures.py` from author-02; their SHA-256 values equal the `successor.json` pins. With them, `check.py` exits 0 (`work/augmented-check-result.json`):
- 48 pins verified, with byte-identical regeneration;
- 43 metadata-v2 cases pass through envelope5, and the historical `check_metadata.py` passes;
- 102 coverage rows rechecked;
- 126 report cases (16 accept) and 15 envelope cases.

**After review:** see the end of this file.

## Closure of prior findings

| Prior | Status | Basis |
|---|---|---|
| RPR-1 fit | Partly closed | The carrier, dispatch and host admission exist, and P1 → `J-ENV-FIT-CARRIER`. Residuals: RPR2-1. |
| RPR-2 envelope joins | Closed | P2/P3/P3b are refused with owned codes, the latest view is refused, and QueryResult equality is enforced. |
| RPR-3 subject join | Closed | Index recomputed from the governed GraphEndpoint descriptor; independently reproduced (below). |
| RPR-4 vanished features | Partly closed | Typed feature states and prose rows are refused, but F01's reason is false (RPR2-3). |
| RPR-5 provenance | Partly closed | Const provenance is visible and hiding it is refused, but verified claims are overstated (RPR2-4). |
| RPR-6 codec | Closed | Byte parse, lexical cases, chain 27 accepted and chain 28 refused. `canonical()` matches `canonical.py:67-72`, and the native gains match my path count. |
| RPR-7 budgets | Partly closed | Caps, worst cases and the shared 4 MiB envelope boundary hold, and the prefixes are deterministic and maximal. Page reduction is wrong (RPR2-2). |
| RPR-8 standing | Partly closed | "Not approval" and the conditional overrides are fine, but `contract.md:7` still says "complete finite design". |
| RPA-1 no-script parity | Partly closed | Prose and parityRule exist, but there is no owner shape or golden, and chapter-14 rows are unscoped. |
| RPA-2 / RPA-3 / RPA-5 | Closed | F03 state; P5 → `SCHEMA` plus `J-ENV-AUDIT-COMPARISON`; pins verified. |
| RPA-4 | Accepted | Root direction. |

## Required findings

### RPR2-1 (blocking): fit parity can be a truncated page, the fit request is unspecified, and the ephemeral and failure forms are inconsistent

**Truncated parity (probe Q1).** A fit envelope is accepted by both `admit_envelope` and `admit_document` with:
- `candidateList.context.truncated=true`;
- `totalItems` = listed + 500;
- a `nextCursor`.

So the fit `candidates` and `evidence-levels` parity fields can be one page. `CandidateListRecordV1.candidates` has `maxItems` 1000.

**No request.** `advisoryDispatch` fixes the surface, operation and pointers, but not the query request: no page size, cursor or view law. Two conforming hosts can emit different parity for the same Run.

**`--ephemeral` changes semantics without scope.** The inventory5 fit flag join is byte-unchanged ("cannot supply baseline/repair/verify prerequisites"). The workflows owners limit the refusal to specific cases:
- §1 lists only baseline adoption, repair, verify and authoritative replay;
- the §9 golden is scoped to "with baseline/repair prerequisite".

The new golden widens that law to fit. This is a request-semantics change to an accepted flag, not an additive declaration, and nothing records it. §8 also already provides a non-authoritative law (`run-id` explicitly null), which the candidate did not assess as an alternative.

**Failure form.**
- The §3.5 post-commit candidate failure (termination `runId`, no carrier) is refused as `kind=run` (`J-ENV-FIT-CARRIER`) but accepted as `kind=failure` (probes Q2a/Q2b). The contract names neither kind, and no case covers it.
- `contract.md:104` says termination is the step aggregate, but `contract.md:112` collapses every candidate-step refusal into `DELIVERY.REQUIRED_FAILED`.

Owner lines:
- `metadata-v2/command-envelope.schema.json:983-1006`
- `graph-query.schema.json:897`
- `workflows-and-surfaces.md:242-247, 1104-1106, 1125-1135, 1218, 1370-1379`
- `command-inventory.v4.json:243-246`
- subject `owner/command-inventory.v5.json:243-246, 255-268, 2208-2215`
- subject `owner/command-envelope.v5.schema.json:1124-1150`
- subject `contract.md:98, 104, 108-115`
- subject `check.py:172-181`

**Correction:**
- Specify the fit query request: view `{runId}`, `includeSuppressed` false, page size and cursor law.
- Choose one parity law and add refusal cases for it: either complete candidates only (more than 1000 is a required-delivery failure), or truncation declared as parity with its own pointers.
- For `--ephemeral`, either obtain a recorded command-owner decision with passage overrides, or use the null-parity law.
- Fix the post-commit envelope kind, with accepted and refused cases.
- Reconcile the termination statements at `contract.md:104` and `:112`.

### RPR2-2 (blocking): graph slots admit silently cut pages, and the reference projector produces them

**The contract.** §8.3 step 5 requires re-issuing the identical owner query at the smaller page size.

**What the projector does.** `check.py:453-456` instead:
- slices `response.items[:size]`;
- keeps the stale owner context;
- derives `continuation` from that stale context.

**Probe results** (`work/probes/j_reduced_slot.json`):

| Case | Items | Context | hostProjection | Result |
|---|---|---|---|---|
| Projector, worst 100-row slot | 50 of 100 | `truncated:false`, `totalItems:2`, no cursor | `complete-page-set` / `byte-budget-reduced` | admitted |
| Mutation of `audit-full` | 3 → 1 | `totalItems:3`, `truncated:false` | `complete-page-set` | accepted |

**Why admission misses it.** Admission (`check.py:309-342`) never joins item count to `truncated`, `totalItems`, `producedItems` or `nextCursor`. So R15's "visible limits" can be false in an admitted report.

**Fixture defect.** The checker's worst-slot op (`check.py:541-550`) itself builds 63/64/100 items under `totalItems:2`.

Owner lines:
- `prototype-report-inventory.md:113-117, 121-123`
- `graph-query.schema.json:897`
- subject `contract.md:163, 205, 279`
- subject `check.py:302-342, 450-477, 541-550`

**Correction:**
- Add a slot item/context count and cursor join with a stable refusal code, and cases for it.
- Model re-issue in the projector, including `nextCursor` and `not-embedded` where applicable.
- Rebuild the worst-case fixtures with consistent contexts.

### RPR2-3 (blocking): the step/attempt ledger has an owner, so a Preserve capability disappears behind a false reason

**The owner exists.** invocation:3 owns the R03 ledger:
- `InvocationRecord.stepResults` (`invocation-record.schema.json:49`);
- `StepResult.attempts[≤3]` (`:1144-1160`);
- `Attempt` (`:1039`).

**The requirements.**
- R03 is **Preserve**.
- Chapter 14 `overview-view` (line 562) must display invocation/step/attempt summaries without concealing missing child evidence.

**What the candidate does.** It marks `step-attempt-ledger` unavailable with `no-admitted-owner` for all 8 commands (for example schema line 237). The report already embeds other owner roots as panels: comparison:2, CoverageResultV3, the capability registry and AnalysisResult. The missing piece is a carrier, which is report-owner design work. RP-OBL-F01 defers exactly that as a future lane.

**Genuine absences, correctly disclosed:**

| Feature | Evidence |
|---|---|
| F04 | Policy `Rule` has no description (`policy-document.v2.schema.json:423`) |
| F05 | `ReleaseCapabilityDeclarationV1` is `{capabilityId, languageModes}` (`native-evidence.schemas.v2.json:795`) |
| F07, F08 | `RecipeRef` holds references only (`evaluator3/repair.schema.json:284`) |
| F09 | No metric definition found in the pinned schemas |

**Imprecise reason.** For F11, `FrameworkRecognitionV1.entryPoints` exists (`native-evidence.schemas.v2.json:3857-3901`), so the gap is retention, not ownership (A5).

**Design decisions labelled as lanes.** F03 (multi-run selection) and S01 (graph slot selection, on whose plan order the byte law depends) are design decisions, not implementation lanes.

**Correction:**
- Author a bounded ledger carrier over InvocationRecord, StepResult and Attempt, with joins to `requestId`/`runId`, missing-child disclosure and a byte-law position. Alternatively, obtain a recorded root deferral with a truthful reason code.
- Classify F01, F03 and S01 as design blockers that keep AUDIT-G10 open.
- Keep B01, B02, H01, M01, G01 and E01 as implementation or qualification lanes.

### RPR2-4 (required): provenance overclaims

These probes show `verifiedInDocument` claims that admission does not actually verify, and host decisions that are not disclosed:

| Claim or gap | Probe | Result |
|---|---|---|
| graph `rows-match-request-parameters` | Q5: row `unresolved` under `minResolution:resolved` | accepted (only relation and endpoint are checked, `check.py:322-328`) |
| graph `rows-match-request-parameters` | Q13: path row node on no edge, violating the owner simple-path law | accepted; the endpoint enters the subject index |
| graph item/context counts | RPR2-2 | accepted |
| `item-counts-consistent` covers budget causes | Q3: `byte-budget` omission of 3000 on a 22,300 B document | accepted |
| `item-counts-consistent` covers budget causes | Q4: `byte-budget-reduced` page on the same document | accepted |
| report `command` | Q6: audit envelope labelled `analyze` | accepted; the envelope has no command member |
| capabilities `registry-sha256-recomputed` | — | integrity only, not source evidence (A9) |

Owner lines:
- `graph-query.schema.json:158-171, 837`
- `prototype-report-inventory.md:35-37`
- subject `contract.md:225-236`
- subject `check.py:238-243, 316, 322-336`

**Correction:**
- Verify each claim, or move it to `hostAsserted`.
- Disclose the omission cause and the report command as host decisions.
- Add the Q3–Q6 and Q13 cases.

### RPR2-5 (required): the frozen subject is not self-checking, and pins are incomplete

**Missing files.** `check.py:622-623` needs `build_owner.py` and `build_fixtures.py`. Both are pinned in `successor.json:298-307` and listed in `contract.md:30-35` (as is `seal.py`), but the manifest omits them. The "byte-identical regeneration" claim therefore cannot be verified from the frozen bytes.

**Unpinned module.** Every `J-ENV-QUERY_SURFACE_*` code comes from `query_surface_projection.v3.py`, which loads `discovery-defaults.py` at import (`:274`). That file is unpinned and is uncommitted-modified in the architecture checkout. `contract.md:372` acknowledges unpinned imports but does not name this one.

**Correction:**
- Freeze every file the checker executes.
- Pin and assert the full transitive load closure.

### RPR2-6 (required): passage scope is incomplete

The overrides cover only chapter-14 lines 339 and 556. The candidate also changes meaning in these passages:

| Passage | Change not scoped |
|---|---|
| workflows §1 (`:242-247`) and §9 (`:1379`) | ephemeral scope (RPR2-1) |
| inventory5 fit flag join | ephemeral scope (RPR2-1) |
| chapter 14 `:459` (html_renderer) | static human-parity section and failure notice |
| chapter 14 `:564` (report-data: "incompatible data produces a display error") | static failure fallback |
| chapter 14 `:463` (projection.rs) | envelope5 host admission and byte law |
| E01 targets (`metadata-unit.v1.json`, `docs/implementation/README.md`) | pinned parents with no selectors |

**Correction:** Add conditional overrides for these passages, or remove the changes.

## Advisories

- **A1: subject-index bound.** The derivation 12006 = 6×(2×1000+1) is wrong: slots are capped at 100 rows, and path rows carry up to 65 nodes. The cap is reachable only with owner-invalid path rows. At about 333 B per extra endpoint, roughly 12,007 endpoints fit in about 4.0 MiB; owner-consistent paths cost about 630 B per endpoint.
- **A2: endpoint discovery.** `check.py:207-220` finds endpoints by structural key-set walk, not governed per-operation pointers.
- **A3: depth refusal code.** It depends on parser recursion: nesting 39 gives `CODEC-DEPTH`, but nesting 200000 gives `CODEC-LEXICAL`. Specify iterative depth detection during parse.
- **A4: native-offset gains.** They are hard-coded (`check.py:857-859`), not derived from the schema.
- **A5: reason vocabulary.** Feature-state reasons need to distinguish no-owner, not-retained, no-redaction-owner and no-carrier.
- **A6: S01.** Graph slot selection is design, not an M4 lane.
- **A7: coverage overlay.** It leaves the 24 reportFeatures rows and 13 workflows contractSections rows untouched. No F-obligation or schema rows are added.
- **A8: generator implications are untested.**
  - The documents use object/array consts and allOf-`$ref` narrowing. The m1 adapter projects consts through `prepare.py:167-168`, and `render-types.cjs:34` throws on unprojected consts.
  - No generator run was performed.
  - The AUDIT-G10 M1 decision still applies until acceptance.
- **A9: registry digest.** Label `registry-sha256-recomputed` as integrity-only.
- **A10: static-section oracle.** Add per-base expected static-section content so RP-OBL-B01 tests against a fixed oracle.
- **A11: dirty checkout.** Pins bind uncommitted working-tree bytes, including a modified `canonical.py` that matches its pin. Retain those bytes with the acceptance record.

## Independent evidence

**Positive:**
- **Additive diffs.** My JSON diffs confirm envelope5, inventory schema5 and inventory5 change only the declared members, and restoration checks pass.
- **subject3.** A stdlib-only implementation (`h_subject3_independent.json`) reproduces:
  - 3/3 goldens;
  - 5/5 index rows, in strict order.

  The path-lookalike finding (`src/legacy.js`) is not joined.
- **Codec.** `canonical()` uses the same parameters as `canonical.py`, and the depth gains match a schema path count.
- **Document ceiling.** Root overhead is 2,339 B, well inside the 65,536 B allowance.
- **Byte law.**
  - With the cap lowered on a context copy, the evidence prefix is 560 of 2000, deterministic and maximal. Later panels are omitted per `J-BUDGET-ORDER`, and the result admits under the real cap.
  - A worst 100-row slot reduces to page 50.
- **Fit termination.** Q2c: an indeterminate fit with carrier and `runId` is admitted.

**Negative:** Q1, Q2a/Q2b, Q3, Q4, Q5, Q6, Q7b, Q13, the S2 reduced slot, the items-cut mutation, the frozen-copy checker failure, and the invocation:3 ledger owner. Details are in the findings above.

## Untested limits

- No generator, UI, browser, HTML, human renderer or product code was built or run. The no-script section was not exercised.
- Nothing here is measured performance or release qualification; worst-case sizes are constructions only.
- The workflows reference model was not rerun for the fit golden.
- The transitive load closure of the other pinned models was not enumerated.
- No worst-case CoverageResultV3, comparison or owner-valid 12006-row index was constructed. A1 is an arithmetic estimate.
- The subject3 goldens are computed, not published vectors.
- The augmented copy uses two out-of-manifest files whose hashes match the pins.
- The evidence prefix test lowered the cap on a context copy, so it tests the law, not the constant.
- Owner-absence searches covered definition names and properties in design-corrections JSON only.
- The author response, final response and session logs were not read or used.

## After-verification

Recomputed after writing `review.json` and `review.md`:
- The manifest SHA-256 is still `4ebe0279…aa4551`.
- All 9 files still match by hash and byte length, and the subject directory has no extra or missing entries.
- `review.json` parses.
- All outputs of this review are under `m1-report-projection-review-02/` (`review.json`, `review.md`, `work/`).
