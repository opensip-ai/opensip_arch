# Capture of explicit stage returns, two-cell attribution, and matrix relation wording (frozen41)

**Author:** bounded AUTHOR f5617310-c7c7-4d85-acdd-31370f220944 (the same author as the v40 attribution proposal). This is an architecture, design and reference assessment only. It is **a proposal, not acceptance**. Nothing was written to LIVE, frozen41, the root successor or an older runtime.

**Base.** `candidate-subject.v41`, manifest sha256 `eb7a4c48d86c844914ffc0ef70743752655a411e453bbaa066cfaee572312236`. All 12912 members were verified before the work (`receipts/frozen41-verify.json`) and again after it (`receipts/frozen41-verify-final.json`): 737732367 bytes read, 0 missing, 0 mismatched, 0 extra. Frozen41's contract, model, fixture and checker are byte-identical to my v1 patched tree. The schema is unchanged since v40.

**Standing of the evidence.**
- *Admission* columns come from `admit_execution_inputs`. They show reference self-consistency, because the builder reuses the model.
- *Closed-run* columns come from a maintained Run driver:
  - for file-fixture worlds, `check-execution-inputs.v1.full_run`;
  - for TypeScript semantic worlds, the `check-semantic-replay.v3.close_positive` sequence (`seed_seal → open_run_closure → R.derive → seal_derived → R.replay → close_run`).
- `exactManifest` means the proof's `executionInputsDigest` equals `raw_digest` of the very manifest the admission column admitted.
- A *host-authored* manifest is labelled as such, and is never presented as builder output.
- Replay cannot certify a malicious host omission (§1 `:24`), and nothing here claims it can.
- Two different `hostCapture` observations are two different inputs. No finding here rests on that.

## Disposition: **CORRECTION_REQUIRED** (with one bundled clarification)

1. **Builder.** The maintained host-capture builder does not construct the capture from the explicit stage returns it is given. It captures only the attributed subset. §8 documents exactly that, so the implementation is faithful to §8's own row. But that row contradicts §1 (capture is an observation of stage returns) and the new §3 sentence ("a captured view attributed to no row stays lawful and stays on `selectedRefs`"). It also contradicts the incorporated wiring, which names this builder as the host adapter's capture step (§7 `:263`, `:280`). The same graph's Run then cannot close.
2. **Model.** The model does not enforce §1's exact stage-produced totality for attributed views. A manifest whose `selectedRefs` and row name a view that appears on no complete receipt admits, and closes a Run.
3. **Clarification.** §3's `S.relation ∈ …/relations` is literally unsatisfiable, because the matrix entries are `[relation, resolution]` pairs. Relation-column and pair membership give different Run-admissible encodings (P1). The model uses relation-column membership, so the text is pinned to that. Behaviour is unchanged.
4. **Schema.** No change is required.

## 1. Published selectors

**Contract (`execution-inputs-contract.v1.md`)**

| Selector | Text |
|---|---|
| `:12` (§1) | "The record is a **host TCB observation of stage returns**." |
| `:14-19` (§1) | "`selectedRefs` is **exact totality**": stage-produced = "union of **complete** receipt `outputRefs`"; coverage = the `coverageIds` "of those captured returned views". |
| `:24` (§1) | Replay "**cannot** certify a malicious host omission"; "Physical object/blob censuses are **not** fields of this record … Ambient unselected store contents must not change `C(ExecutionInputs)`." |
| `:53` (§3, integrated from v1) | "The candidate views are the captured returned views: `view` refs on `selectedRefs` and `view` `outputRefs` of complete receipts"; "`S.relation` ∈ `native-capability-matrix.v2.json#/capabilities[capabilityId]/relations`"; "A captured view attributed to no row stays lawful and stays on `selectedRefs` (§1)." |
| `:263` (§7) | "Fixtures call `attach_host_capture` before seed seal." |
| `:280` (§7) | Step 5, actor **host adapter**: "`attach_host_capture` then `close_run`". |
| `:294` (§8) | "`execution_inputs_fixture.v3.py` is the reusable builder." |
| `:298` (§8) | `normalize_graph` accepts "`viewIds`/`viewId` … existing `evaluationInputRefs`". |
| `:299` (§8) | `build_manifest`: "`selectedRefs` = attributed views + their coverage + …"; "Does **not** hash retained object/blob censuses." |
| `:301`, `:303` (§8) | `attach_host_capture` sets `evaluationInputRefs = selectedRefs + execution-inputs ref`; ambient objects and blobs must not change the manifest. |

**Other owners**

| Selector | Text or content |
|---|---|
| `identity-model.v3.py:1797-1799` | `set(evidence['viewIds']) != view roots of proof.evaluationInputRefs` → `EVALUATION_VIEW_ROOTS`. |
| `evaluator_graph_fixture.v3.py:384-388` | The seal attaches host capture, then commits `semantic-evidence.viewIds = graph['viewIds']`. |
| `evaluator_semantic_fixture.v3.py:208-209, 224` | The same wiring. |
| `evaluator_graph_fixture.v3.py:293-296` | Comment: views bound to no cell outcome make "the host capture drops them from selectedRefs, which is EVALUATION_VIEW_ROOTS rather than a real Run" (fixtures are shaped around the drop). |
| Builder (frozen41) | `execution_inputs_fixture.v3.py:204-209`: `view_ids` = `viewIds` ∪ view refs on `evaluationInputRefs` present in `objects`. `:341`: `view_hexes` = the union of rows' `viewDigests` (attributed only). `:346-389`: `selectedRefs` and receipt `outputRefs` are built from `view_hexes`. |
| Model (frozen41) | `execution_inputs_model.v1.py:1671-1672`: expected stage-produced views = attributed views ∪ receipt views. |
| Schema | `execution-inputs.schema.v1.json:621`: `viewDigests` "Must equal captured receipt views attributed to this cell/program/U/producer." |
| Matrix | `native-capability-matrix.v2.json` `capabilities[]` is an array with `id`, and `relations` holds `[relation, resolution]` pairs (`references`: `[["references","resolved-binding"]]`). |
| Native ladder | `references` has `syntactic-name-match` and `resolved-binding`. |
| `relation-payload-schemas.v2.json:834-839` | `SubjectIdV1` pattern `^[a-z][a-z0-9-]*:…`. |
| `relation-payload-schemas.v2.json:639-668` | `DeclaresPayloadV1` requires `SubjectIdV1` for `container` and `declared`. |

## 2. Builder capture: the same explicit returns (probe A, `receipts/probe-A-capture.json`)

The base world is the maintained file fixture (`unsupported_cell="required"`, `multiple_universes=True`). The probe adds a `references@resolved-binding` view at U1 with owner-admitted Coverage. No references binding exists at U1, so no cell owns it.

| World | Where the view is present in the builder input | Frozen41 builder manifest | Admission | Closed Run |
|---|---|---|---|---|
| A0 | unmutated control | 5 of 5 views captured | ADMIT | `indeterminate`, exactManifest |
| **A1** | `graph['viewIds']` **and** `evaluationInputRefs` | **not on the receipt, not on `selectedRefs`**; `attach_host_capture` overwrites the refs without it | ADMIT | **`EVALUATION_VIEW_ROOTS`** (evidence names 6 views, selection 5) |
| **A2** | `viewIds` only | not captured | ADMIT | **`EVALUATION_VIEW_ROOTS`** |
| A3 | `evaluationInputRefs` only | not captured | ADMIT | closes (evidence never named it) |
| A4 | store census only (`objects`) | not captured; digest **equal** to A0 | ADMIT | closes |
| A5 (failed attempt, kept) | an extra owned `file` partition | captured | ADMIT | `COVERAGE_INVENTORY_TOTALITY_OMITS_PATH` from the probe's own partition, not from attribution |

**The distinction the question asks for.**
- **Store census:** the builder correctly ignores it (A4, §1 `:24`, §8 `:303`).
- **Explicit returned views:** `viewIds`/`viewId` and view refs on existing `evaluationInputRefs` are builder *inputs* (§8 `:298`). The builder already unions them into `view_ids` for attribution (`:204-209`).
- **The gap:** it then captures only the attributed subset (`:341`). An explicitly returned, lawful, unowned view is therefore discarded. The Run's evidence keeps it, because the seal commits `graph['viewIds']`, so that same graph cannot close.

Constructing the capture from the same explicit stage returns is **specified** (§1, §3) but **not faithfully implemented**. §8's row describes the defect rather than an intended limit: §7 designates `attach_host_capture` as the incorporated capture step, and the graph fixture's own comment treats the drop as a hazard to design around.

Sweep receipts: `receipts/sweep-builder-base.json` and `sweep-candidate-base.json`. Across 18 maintained file and semantic graph constructors and the candidate fixture, no explicit view is dropped, and no selected or attributed view is off-receipt. The defect is invisible to maintained graphs only because they were shaped around it.

## 3. Receipts vs `selectedRefs` (probe A, S1/S2)

These are host-authored manifests over A0.

| World | Manifest | Admission | Closed Run |
|---|---|---|---|
| **S1** | an attributed view is on `selectedRefs` and on its row, but **on no complete receipt** | **ADMIT** | closes `indeterminate`, **exactManifest** |
| S2 | the view is on a receipt and a row, but not on `selectedRefs` | REFUSE `SELECTED_COVER` | `EVALUATION_VIEW_ROOTS` |

S1 is one manifest that is internally inconsistent with §1's exact stage-produced totality. It is not a pair of differing observations, and it is not an undetectable omission. The model's expected set adds attributed views to the receipt union (`:1671-1672`), so the contradiction is silently accepted. The v1 §3 candidate-set sentence ("`view` refs on `selectedRefs` and `view` `outputRefs`") mirrored that permissive union.

## 4. Two capability cells on one program/U (probe B, `receipts/probe-B-twocell-base.json`)

**Choice of world.**
- **File-fixture symbol worlds** can't close even unmutated (`receipts/symbol-baseline.json`):
  - with the checker's `nativeSubjectId: "x"`, `PAYLOAD_RECORD:#/$defs/DeclaresPayloadV1`, since `"x"` is not a `SubjectIdV1`;
  - with the lawful `symbol:x`, `POLICY_RULE_NOT_ADMISSIBLE:policy:file-observed:POLICY.UNKNOWN_RULE`.
  - This is a helper baseline defect. The control doesn't need that helper, so I didn't correct it.
- **The maintained TypeScript semantic fixture** with a `declares` atom is a lawful two-cell world. It has `inventory` and `syntax` at `ts-tsconfig`, one binding each at `u1`, `SubjectIdV1` symbol ids, and owner-admitted file, package, declares, literal and control-flow Coverage. Unmutated, its builder manifest closes (`receipts/semantic-declares-baseline.json`: verdict `fail`, exactManifest).

| World | Manifest | Rows | Admission | Closed Run (semantic driver) |
|---|---|---|---|---|
| B0 | builder, unmutated | inventory 2 views, syntax 3 | ADMIT | `fail`, exactManifest |
| **B1** | builder; one view holds `file` (facts) and `declares` (facts) partitions | shared view on **both** `inventory#0` and `syntax#0` | ADMIT | `fail`, **exactManifest** |
| B1x | host: syntax row omits the shared view | — | REFUSE `VIEW_TOTALITY` | refused `VIEW_TOTALITY` |
| **B2** | builder; B1 plus a returned `references@resolved-binding` view at `u1` (owner-admitted Coverage, subject `symbol:foo`), which matches neither cell | the extra view is **dropped** | ADMIT | **`EVALUATION_VIEW_ROOTS`** |
| B2h | host: builder output plus that view captured exactly | extra view captured, on no row | ADMIT | `fail`, exactManifest |
| B2y | host: B2h plus the extra view named on the inventory row | — | REFUSE `VIEW_TOTALITY` | refused `VIEW_TOTALITY` |

Current law and model already decide every two-cell attribution question: a shared view is on both rows, and a view matching neither cell is on no row. The maintained suite simply had no control for it. Only the capture defect in §2 stops the builder from producing a closable manifest for B2.

## 5. Matrix relation wording (probe B, P1)

The base world is the unsupported `references@syntax-only` row. The probe adds a view whose scope is `references@syntactic-name-match`, which is on the relation's ladder but is not the matrix pair's rung.

| World | Encoding | Admission | Closed Run |
|---|---|---|---|
| P1 | builder: **relation-column** reading (the view is on `references#0`) | ADMIT | `indeterminate`, exactManifest |
| P1y | host: **pair** reading (the row omits it) | REFUSE `VIEW_TOTALITY` | refused |

The two readings produce distinct identities and outcomes, and the published text supports neither literally. The model's reading is pinned (see §6).

**Schema description.** `CellProgramOutcomeV1.viewDigests.description` says "captured receipt views attributed to this cell/program/U/producer". After the correction, that matches §3 exactly (candidate views = complete receipt views). The contract paragraph names `CellProgramOutcomeV1.viewDigests` as its subject, so an owner link exists from the owning side. `NativeCoverageAccountV1` publishes `x-opensip-external-joins`, but `viewDigests` has no comparable annotation, and adding one would change registered bytes and force a repin for a cosmetic gain. **No schema change is required.**

## 6. Proposed correction (exact delta)

`correction.patch` has sha256 `92aa515f52b439792fb63930e4237a5ee5352d57f053213868c2a3be4ba9017e` (25650 bytes). `delta-manifest.json` lists each file below; every base file is byte-identical to frozen41.

| File | Base sha256 | After sha256 |
|---|---|---|
| `foundation/execution_inputs_fixture.v3.py` | `a94c971462c4e449d81eee5b1bd7a51c60b8b8b3c2e1b5cb88e32a7b2e13c8fa` | `d8c48fb5147887d04d875547ea450510a63106f1361de2711a48aa22d1070073` |
| `foundation/execution_inputs_model.v1.py` | `5ea205090c1450a65fb14c29c2e02da7ef91be04baf67cb299fe67fd7bc96157` | `66a15adddc7fed3d9209740da5ea0e2271e3b6c69236b73d4371f33aa6ab9ea1` |
| `foundation/execution-inputs-contract.v1.md` | `64438ff18364eefc736e877fbce43b0d89e94eca17c41cacb79a08d25b8e7d70` | `8521f36217fb1499b93895789c392a6afd1a369db136afb8cd2c286d0735a2e1` |
| `foundation/check-execution-inputs.v1.py` | `b1b5d4be7d0c9e240b258ec9345f4b36eda2d62197994b0e3be6adfda9629d1c` | `e169fecb74e8000174f1cb4d88830d409c7d9c249d1ec080214c18415cde4e2d` |

The schema (`604bd941…`) is deliberately unchanged.

**Builder.** `view_hexes` becomes the explicit returned views: `view_ids` present in `objects` whose `producerClosure` is a view stage's producer. It is no longer the attributed subset. Receipts and `selectedRefs` are built from those views exactly as before, and rows keep §3 attribution. The census is still never walked.

**Model.** The expected stage-produced views are exactly the complete-receipt view `outputRefs`. An attributed or selected view that appears on no receipt refuses the existing `EXECUTION_INPUTS_SELECTED_COVER`. There is no new code and no attribution change.

**Contract.**
- §3 candidate set: "the `view` `outputRefs` of complete receipts, which §1 makes exactly the `view` members of `selectedRefs` (a `view` on `selectedRefs` but on no complete receipt refuses `EXECUTION_INPUTS_SELECTED_COVER`)".
- §3 relation: "`S.relation` is the relation member (first element) of some `[relation, resolution]` pair in the `relations` array of the … `capabilities[]` entry whose `id` is the row's `capabilityId`. This is relation-column membership: the pair's resolution plays no part, so a scope at another rung of that relation's ladder is attributed too."
- §8 `build_manifest` row: receipts capture the **explicit** returned views (`viewIds`/`viewId` plus existing `evaluationInputRefs` view refs, never the census) on the view stage whose producer each carries. `selectedRefs` = those views + their coverage + …, and rows are the §3-attributed subset.

**Checker.**
- New and extended helpers:
  - `semantic_full_run`, which mirrors `check-semantic-replay.v3.close_positive`;
  - a `graph_factory` parameter on `view_attribution_world`, plus scope `subjects`;
  - `manifest_edit` and `runner` parameters on `view_attribution_case`, and `executionInputsDigest`, `capturedViews` and `selectedViews` fields in its result.
- 9 new cases (6 closed-run) with oracles:
  - `capture-builder-keeps-returned-view-that-no-cell-owns` (closed-run): the view is captured, selected and on no row, and the Run closes on the **builder** manifest.
  - `capture-builder-ignores-store-census-only-view` and `capture-control-same-world-without-census-view`: the census-only view is not captured, and the digests are equal.
  - `capture-selected-attributed-view-on-no-receipt-refuses` (closed-run): `SELECTED_COVER` at admission and in the Run.
  - `two-cell-shared-view-and-captured-view-matching-neither-cell-close` (closed-run, semantic driver, builder manifest): the shared view is on both rows, the neither-cell view is captured and on no row, verdict `fail`, sameManifest.
  - `two-cell-syntax-row-omitting-shared-view-refuses` and `two-cell-row-naming-view-matching-neither-cell-refuses` (closed-run): `VIEW_TOTALITY`.
  - `relation-column-membership-attributes-non-matrix-rung-view` (closed-run) and `relation-column-membership-pair-reading-encoding-refuses`: `VIEW_TOTALITY`.

## 7. Focused receipts

**Owning checker runs** (runtime copies: `receipts/copy-base-tree.json`, 1346 files, 0 mismatches)

| Run | Tree | Cases | Mismatches | Receipt sha256 |
|---|---|---|---|---|
| base | frozen41 byte copy | 86 | 0 (exit 0) | `6206a7f6c5189c1f948aa5a8cebfa65cb1e6282cf261a93a6d01bd4cc94ac7a5` |
| patched | + the 4-file delta | 95 | 0 (exit 0) | `426d0d2091c11676d353268d701cba1a99208f68c1000bce66c312b4123f775b` |
| controls-only | base + the patched checker only | 95 | 4 (exit 1) | `2685cfa2785a77605dcd24798daf6ed365e77f9a56a915e1eb38d4e23106ccf4` |

**What the controls-only run shows.** Its 4 failures are exactly the capture defects:
- the builder drop, in both the file control and the two-cell control (`EVALUATION_VIEW_ROOTS`);
- S1, where the Run closes.

The two-cell refusal controls and the rung controls pass on base too. They are the missing maintained discriminators for law that already decides those cases; they are not evidence for the correction.

**Comparison** (`receipts/compare-base-patched-controls.json`).
- The 86 shared cases are **field-identical** between base and patched: results, refusals, deficiency rows, derived states, coverage records and full-run records. All full-run `runId`s are identical.
- All 18 sweep manifest digests are identical between base and patched (`sweep-builder-patched.json`).

**Probe receipts**

| Probe | Base (frozen41) | Patched |
|---|---|---|
| A (capture) | `probe-A-capture.json` `70e672ae…` | `probe-A-capture-patched.json` `85072901…` |
| B (two-cell and rung) | `probe-B-twocell-base.json` `032fd335…` | `probe-B-twocell-patched.json` `6888ca09…` |

On the patched tree:
- A1/A2 are captured and close exactManifest;
- A4 is unchanged;
- S1 refuses `SELECTED_COVER` at admission and in the Run;
- B2 is captured and closes `fail` exactManifest;
- B1, B1x, B2y, P1 and P1y are unchanged.

## 8. Identity and behaviour consequences

- **Maintained graphs:** no change to any `ExecutionInputsV1` digest, admission row or Run id (the sweep, plus 86 identical cases).
- **Graphs that declare an unowned returned view:** the builder manifest now captures and selects it. The digest changes and the Run closes where it previously could not (A1, A2, B2).
- **A view named only in `evaluationInputRefs` (A3):** it is now captured, just as the base builder already did for such a view when attributed. A graph whose evidence `viewIds` omits it now fails `EVALUATION_VIEW_ROOTS` instead of silently losing the ref. No maintained graph has refs-only views.
  - Root decision point: restricting capture to `viewIds` alone would keep A3's old outcome, but would make the builder treat its two documented inputs inconsistently.
- **Host manifests** naming a view on `selectedRefs` (and a row) but on no complete receipt now refuse `EXECUTION_INPUTS_SELECTED_COVER`. There is no new refusal code.
- **Attribution semantics** are unchanged: same-scope, relation-column membership, candidate-only by U alone. The contract text now states the column reading the model already implemented.
- **The schema** is unchanged, with no repin. The owned hashes of 4 files change.

## 9. Limitations

- Admission columns are reference self-consistency. Closed-run columns use reference drivers, not an independent reconstruction, and no consumer input or output was used.
- The semantic closed-run driver is the `close_positive` sequence, reproduced in the probe and added to the checker as `semantic_full_run`; I did not import it from `check-semantic-replay.v3.py`.
- Other `attach_host_capture` callers were **not run**. The sweep covers their base constructors (file, semantic, package and candidate fixtures), but not graphs they mutate internally. Root integration must run them:
  - `security/check-analysis-seal-adapter.v1.py`
  - `check-native-consumer24-corrections.v1.py`
  - `check-provider-attribution-return.v2.py`
  - `evaluator_candidate_fixture.v3.py`
  - `check-execution-replay.v3.py`
  - `evaluator_semantic_fixture.v3.py`
- Pins, text sweeps, planning and global reports, and the full suite were not run.
- The file-fixture symbol-row baseline defects (§4) are reported, not corrected.
- The A5 probe partition failed Coverage inventory totality. That is a probe construction issue, and it is preserved.
- **Not assessed:** producer or `planId` filter provenance, target-attribution and incoming-search capture, unavailable receipts, and multi-stage plans with several view producers. The builder change handles several producers by construction, but no maintained multi-producer graph exists to exercise it.
- Nothing under `reviews/` was read; only the formal manifest file was used. The one broad glob printed file *paths* only.

## 10. Preserved failed attempts

1. **A5:** an extra owned file partition, admitted, whose Run refused `COVERAGE_INVENTORY_TOTALITY_OMITS_PATH`. Kept in both probe-A receipts.
2. **Symbol-row closure attempts** (`receipts/symbol-baseline.json`): `PAYLOAD_RECORD` with `"x"`, and `POLICY_RULE_NOT_ADMISSIBLE` with `symbol:x`.
3. **Frozen41 builder, B2 and A1/A2:** `EVALUATION_VIEW_ROOTS`. These are the defect's own evidence, kept in the base receipts.
