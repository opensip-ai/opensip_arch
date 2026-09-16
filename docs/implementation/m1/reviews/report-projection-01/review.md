# Independent review: report projection author candidate (`m1-report-projection-subject-01`)

**Verdict: CHANGES REQUIRED.** This is not yet an adequate complete report owner for the product requirements.

It is a sound *partial* shape contract, but it does not close AUDIT-G10 as it claims. Measured product qualification (RP-OBL-2) is correctly kept separate and is not assessed here. Every finding below concerns design completion and admission.

Machine-readable form: `review.json`. Evidence scripts and outputs: `work/`.

## Subject verification

- Manifest `m1-report-projection-subject-01.json` has SHA-256 `9b9533ac…f8ac4d`, as expected.
- All 6 file hashes and byte lengths match the manifest.
- All 15 parent pins in `successor.json` match byte-exact, and both chapter-14 override before-texts (lines 339 and 556) match.
- The architecture checkout has unrelated uncommitted edits; the pinned files are unaffected.
- `check.py` passes in an isolated copy: 79 cases, 10 accepted, exit 0.

**After-verification.** Recomputed after writing this review:
- The manifest SHA-256 is still `9b9533ac…f8ac4d`.
- All 6 subject files still match by hash and byte length, and the subject directory has no extra entries.
- All outputs of this review are under `m1-report-projection-review-01/`.

## What holds

- **Renderer gating.** The HTML command set equals inventory4 and the prototype inventory. The renderer version and query surfaces match.
- **Envelope4.** It stays closed, with no exploration members.
- **External refs.** The transitive `$ref` closure is 1015 edges, 282 targets and 18 documents, with 0 unresolved. All come from the hash-pinned `sources.json` loader, with no retrieval.
- **Graph slots.** They pin a concrete run3 and keep request/response context and cursor disclosure. Relation, endpoint and depth joins are checked.
- **Parity and limits.** Required parity is never truncated, the three limit layers stay separate, and history never substitutes latest.

## Required findings

### RPR-1 (blocking): fit HTML is knowingly undeliverable, yet a fit document is admitted

**What the owners require.** Inventory4 `fit` declares html with parity `candidates` and `evidence-levels`, and has no `queryDispatch`. Envelope4 `kind=run` has no candidate carrier, so fit parity is not total for any renderer, JSON included. I found no registration of this gap anywhere outside this candidate.

**What the candidate does.**
- The schema freezes fit to `kind ∈ {run, failure}` and a view set with neither findings nor candidates. That view set blocks the successor path (probe P11).
- The subject's own positive case `positive-fit-budget-omission` is `kind=run` with no candidate parity, and it is admitted (probe P1).
- `check.py:332-334` asserts the gap exists and then passes anyway.

Owner lines:
- `command-inventory.v4.json:188-210, 1735`
- `workflows-and-surfaces.md:1113-1140`
- `prototype-report-inventory.md:175, 213-219`
- subject `contract.md:3, 46, 247`
- subject `report-projection.schema.json:302-354`
- subject `check.py:332-334`

**Correction:**
- Mark fit HTML as BLOCKED, and keep AUDIT-G10 open for fit.
- Admission must refuse a fit document with `kind=run`. Turn the positive case into a coded refusal.
- Do not freeze a fit view/kind set that excludes candidate or findings presentation.
- Register the envelope4/inventory4 carrier defect with its owner as blocking for every renderer.

### RPR-2 (blocking): envelope4 cross-record joins are not part of report admission

`admit()` only schema-validates the "sole parity source".

- The positive base `candidates-latest-view` has `advisory:false` and `resolvedView:{latest:true}`. Workflows requires advisory true and a concrete Run.
- An `evidenceLevels` miscount is accepted (P2).
- An inspect context Run that differs from the bundle Run is accepted (P3).
- An inspect context from another project is accepted (P3b).

Owner lines:
- `workflows-and-surfaces.md:1210-1213, 1218-1220`
- subject `contract.md:18, 99-101`
- subject `check.py:118-131, 148-151`

**Correction:** Make the envelope4 carrier joins a mandatory admission step, add refusal cases for each, and replace the invalid positive.

### RPR-3 (blocking): the subject3↔endpoint join exists; the finite projection is missing

**The join exists.** `evaluation-subject` is `{schemaVersion:3, universe, kind∈file|symbol|package, nativeSubjectId≤4096, packageManifestPath iff package}`. GraphEndpoint has exactly the same members and bounds.

The identifier is `ID(D,X) = prefix:hex(H(D,X))`. The evaluator models mint subject3 from exactly those members. So the host can mint each endpoint's subject3 and join `FindingSurface.subjectId` exactly. The "must not unpack" law forbids only the reverse direction. The contract's "no subject3↔endpoint join exists" is therefore false, and R11's required exact Run/universe/symbol binding and R07's finding joins are lost.

Owner lines:
- `identity-schemas.v3.json:3225`
- `evaluator-composition-contract.v3.md:275-277`
- `evaluator_graph_fixture.v3.py:223, 235`
- `evaluator_input_model.v3.py:114, 151`
- `graph-query.schema.json:83-89`
- `prototype-report-inventory.md:65-67, 89-91`
- subject `contract.md:64, 207-208, 250`

**Needed contract:** a bounded, sorted, unique `GraphSubjectIndexV1` of `{endpoint, subjectId}` rows:
- `subjectId` is host-minted as `ID("evaluation-subject", {schemaVersion:3, …endpoint})`.
- Admission recomputes every row, and refuses a duplicate or mismatch.
- No endpoint is ever derived from a subjectId.
- Findings join by exact subjectId only. Path, name and body-hash matching stay forbidden.

### RPR-4 (blocking): required features vanish under "no owner" with no typed disclosure or obligation

These rows are each mapped to "not projected / not shown" with no document state:
- **R07:** metrics and test reachability. The inventory requires "show unknown values". I confirmed no owner exists in the pinned schemas.
- **R05:** policy/capability descriptions.
- **R06:** recipe descriptions and parameters. The inventory requires "an explicit state".
- **R03:** the step/attempt ledger. audit has two analysis steps plus comparison.
- **R23:** declared configuration.

None of them is listed in RP-OBL-1..4. `check.py:347` treats any prose `presentationalOnly` string as a complete mapping.

Owner lines:
- `prototype-report-inventory.md:43, 55, 61, 67, 165`
- `14-repository-and-module-layout.md:551, 562`
- subject `contract.md:143-146, 199-219, 245-250`
- subject `report-projection.schema.json:1407`
- subject `check.py:346-351`

**Correction:**
- Add a finite per-command, per-view disclosure `{featureId, state:"unavailable", reason:"no-admitted-owner"}` that the browser renders as an unknown/unavailable state.
- Register one obligation per feature.
- Do not claim complete R01–R24 coverage.
- Make the checker refuse rows satisfied only by prose.

### RPR-5 (required): panels are described as "exact admitted owner records" while their source identity is unbound

- A capability registry replaced by `[]` with a self-recomputed digest is accepted (P10). `registrySha256` binds nothing to the Run's release.
- History with an arbitrary `baselineId` is accepted when comparison is unavailable (P4).
- A history row carrying the current Run's findings is accepted (P7). FindingSurface has no runId, and no host obligation is declared for it.

Owner lines:
- subject `contract.md:128, 135, 142`
- subject `report-projection.schema.json:1226-1262, 1352-1407, 1466-1474`
- subject `check.py:236-251, 259-261`
- `prototype-report-inventory.md:37`

**Correction:** Bind each panel to a checkable in-document identity, or declare each unverifiable join as a named host obligation and mark the panel host-asserted.

### RPR-6 (required): the larger report codec overrides owner exact-codec laws and is not a byte codec

**Depth.** A uniform depth of 38 is applied, but embedding gains differ (envelope 1, rule 5, graph and registry 6). A PolicyDocumentV2 rule with a `not` chain of 28 is refused by its owner (`DEPTH_LIMIT` at 32) but accepted inside the report (P6).

**Bytes.** Admission checks Python values only: there are no parse-level refusals for duplicate keys, `-0`, floats or a byte limit at parse. The line-556 override nonetheless says the report-profile exact codec "is applied before shape validation". Its validator owner is unnamed (RP-OBL-3).

Owner lines:
- `foundation/canonical.py`
- subject `contract.md:91, 161, 170-171`
- subject `report-projection.schema.json:583-586`
- subject `check.py:47-59, 134-138, 387-408`
- subject `successor.json:134`

**Correction:**
- Define the codec at the byte level, using `canonical.py`'s parse rules at the document ceiling.
- Enforce each embedded record's owner depth measured from its native offset.
- Add lexical cases and the chain-28 refusal case.
- Name the validator owner before applying the override.

### RPR-7 (required): budgets are derived from representative samples, and worst-case owner payloads refute them

All worst-case constructions below are validated against the owner schemas (`work/probes/d_worst.json`).

| Record | Representative bytes | Worst-case bytes | Consequence |
|---|---|---|---|
| FindingSurface | 759 | 49,889 | 100k findings ≈ 4.99 GB vs the 80 MiB envelope ceiling; only 1,681 worst-case findings fit |
| GraphNeighborRow | 635 | 66,236 | A 1000-row page is 66 MB; only 63 rows fit in 4 MiB |
| GraphPathRow, 64 hops | — | 6,414,670 | One row alone exceeds the exploration ceiling |

Byte pressure also cannot prefix-truncate evidence, because `item-limit` requires exactly 3956 embedded entries (P9). Graph pages are embedded whole. So any byte overflow forces whole-panel omission.

Owner lines:
- `prototype-report-inventory.md:115, 221-223`
- `command-envelope.schema.json:160-162`
- subject `contract.md:150-161, 168-181`
- subject `report-projection.schema.json:571-606, 929-952`
- subject `check.py:222-226, 365-410`

**Correction:**
- Restate the constants as caps with their worst-case consequences.
- State the HTML required-delivery failure boundary relative to JSON.
- Add a byte-driven projection cause or a deterministic page-size selection law.
- Add worst-case cases to the checker.

### RPR-8 (required): the standing overstates design completion

The contract says it "closes AUDIT-G10" and calls itself a "Complete closed owner schema", despite RPR-1..7. The AUDIT-G10 M1 decision forbids generating report carriers as complete while the gap is open.

Owner lines:
- `m1-protocol-gap-resolution-01/resolutions.json` AUDIT-G10 `decision.M1`
- subject `contract.md:3, 9`
- subject `successor.json:6, 121-134`
- subject `report-projection.schema.json:4-5`

**Correction:** Set the standing to partial owner, keep AUDIT-G10 open with an explicit residual list, and make the chapter-14 overrides conditional on that list.

## Advisories

- **RPA-1: browser failure states.** Nothing specifies what the static file shows when script execution, bundled assets or generated validation fail. The HTML parity rule and R01 need a non-script failure/parity notice.
- **RPA-2: R14 deferral.** Deferring multi-run history selection to a command-owner successor is legitimate, but it is not registered as an obligation.
- **RPA-3: audit not-selected.** An audit report with comparison `not-selected` is admitted (P5), although audit always selects a comparison.
- **RPA-4: inventory standing.** The prototype inventory and chapter 14 are themselves author proposals pending review. Here R01–R24 are treated as the selected design scope that chapter 14 and M4 bind to. The findings stand either way.
- **RPA-5: checkout state.** The architecture checkout has unrelated uncommitted edits. The pins are unaffected.

## Evidence

- **`work/subject-copy`:** a byte copy of the subject, used for checker outputs.
- **`work/check-stdout.txt`, `work/check-result-copy.json`:** the reference check run.
- **`work/probes/a_subject_join.py`:** the evaluation-subject/GraphEndpoint shape and ID computation.
- **`work/probes/c_refs.py`:** the transitive `$ref` closure; also finds the single reachable recursive definition (`policy-document:2 Predicate`).
- **`work/probes/d_worst.py`, `d_worst.json`:** the worst-case owner-valid constructions.
- **`work/probes/e_joins.py`, `e_joins.json`:** probes P1–P11, run through the subject's own `admit()` against the pinned registry.

## Limits

- No UI, browser, generator or product code was built or run, and no browser failure state was exercised.
- The subject3 recipe is confirmed from the identity schema, the composition contract text and the evaluator models, not from a pinned subject3 test vector.
- Worst-case CoverageResultV3 and comparison:2 sizes were not constructed.
- The prototype source was not inspected; only the inventory text was read.
- No author session transcripts or private sessions were read.
- Nothing here is a measured performance or release-qualification claim.
