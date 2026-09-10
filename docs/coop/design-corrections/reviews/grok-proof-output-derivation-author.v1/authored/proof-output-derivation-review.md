# Proof-output derivation review and authored correction

**Standing.** Same actual Grok coauthor origin as `grok-proof-output-contract-audit.v1` session `01a084ff-a43d-7562-8dfc-ab2fbd910b1c`. Not blind. Not independent final acceptance. Frozen `candidate-subject.v24` was not modified. No source application, freeze, or readiness.

**Prior audit retained as history.** `history/grok-proof-output-contract-audit.v1/` (the COMPLETE25 395-line audit, JSON companion, and the consulted-only patch that Codex rejected).

**This turn.** Reconcile Codex's five findings against the actual emission bridge, then author a precise normative correction in `proposed/` using frozen24 as beforeimage.

---

## 1. Verdict after reconciliation

A precise field-derivation table **is** required for unique complete proof bytes. That table must **publish the current intended bridge**, not switch to consulted-only `predicateProof.inputRefs`, not drop ExecutionInputsV1 refs, and not re-label required-execution `source=execution` as native.

The alleged reference cause-enum bugs are **withdrawn as proof-output bugs**. Internal `requiredCellDeficiencies.cause` tokens `native-work-incomplete` / `unsupported-typed` are not emitted as `proof.cause`. Every native `DeficiencyV2` member is in both the execution and native cause registries.

No reference-code patch is proposed. No incompatible-input control produced invalid **output** through the published bridge.

Until this correction is three-way integrated, the published kit remains underspecified for those fields. This authored text is the proposed unique mapping, not an applied freeze.

---

## 2. Codex findings — agreed / rejected / revised

| # | Codex finding | Grade after tracing actual output | Disposition |
|---|---|---|---|
| 1 | Internal admission rows ≠ schema evaluation-deficiency; bridge reads `row.deficiency`, maps null/`source-syntax-invalid` to `required-cell-unsatisfied`; `native-work-incomplete`/`unsupported-typed` are not proof causes; all DeficiencyV2 members sit in both registries | **Revised.** Prior “reference cause-enum bug” treated an internal vocabulary as proof output. Actual emitted `proof.cause` is a DeficiencyV2 member or `required-cell-unsatisfied`. Control: `D2 − execution = ∅`, `D2 − native = ∅`. Execution extras vs D2 are only `required-cell-unsatisfied` and `work-budget-exhausted`. Native extras vs D2 are evaluator diagnostics, not DeficiencyV2 carriers. | Withdraw proof-schema-bug claim. Publish the bridge in composition §9.6. |
| 2 | `source=execution` is the required-execution assessment layer; original DeficiencyV2/nativeCause and originating refs remain plus manifest context | **Agreed.** Prior always-native account `source` was an unsupported alternative that changes intended semantics. No output contradiction: claimed `source=native` on syntax-data is a graph/convention dispute, not a kit requirement to change the layer. Absent table = **underspecified mapping**. | Keep `source=execution`. Publish the layer. |
| 3 | Whole admitted selection on every atomic `predicateProof.inputRefs`; exact projection sentence because witness has no `inputRefs`; boolean union; consulted `scopeIds` / witness `coverageIds` may be narrower; do not switch scanner semantics | **Agreed.** Prior consulted-only switch is an **unsupported alternative**. Redundancy with `evaluationInputRefs` is not inconsistency. “Actually read” is a poor new discriminator without a separate abstract-read algorithm. Atom internal consumed refs ≠ profile output refs. | Retain Run-wide selection. Add the projection sentence. |
| 4 | Proof execution-deficiency `inputRefs` = `Cset({ExecutionInputsV1 ref} ∪ row.inputRefs)`; distinguish inventory vs native-account originating refs; keep siblings; explain internal vs proof uniqueness | **Agreed.** Prior removal of the ExecutionInputs ref was an **unsupported alternative**. Two unsupported-typed relations with identical bridged records collapse at proof grain; cell/relation coordinates remain on hashed ExecutionInputsV1. No operand shown where existing law still requires two identical proof items. | Keep XI plus originating refs. Explain uniqueness. Do not add proof fields. |
| 5 | `semantic-evidence.importIds` “evaluated subset” is stale | **Agreed** as a precise description correction, not a broad ownership contradiction. | Fix the annotation. Distinguish Plan import selection, whole-selection proof refs, and witness observation addresses. |
| — | Pilot symbol census | **Agreed** (unchanged). Existing-law checker omission (execution-inputs §5 includes `symbol`). Not missing design. | No kit field added. |

**Prior COMPLETE25 grades that stand:** kit does not yet uniquely determine complete proof bytes (underspecification, now proposed to close); schema-only is never unique; P7 full-C of a self-derived expected proof is not kit-unique reconstructability; rust FULL_ADMIT withdrawn; TS `IMPORT_PRODUCER_KIND` first refusal / producing `notReached`; rust-partial first refusal membership/extent; original selected-field `proofCompare` withdrawn; `FOUR_RUNS_REFUSED`.

**Prior COMPLETE25 grades that are revised:** “reference bug” on `native-work-incomplete`/`unsupported-typed` as proof causes; “true contradiction” of original-cause vs always-execution **output** (it was a missing bridge table, not an emitted invalid cause); consulted-only `inputRefs` as the recommended semantics; removal of ExecutionInputs refs; always-native account source.

---

## 3. Trace of actual emitted fields (point 1)

Site: `evaluator_input_model.v3.py` `execution_input_account` lines 47–56.

For each internal `requiredCellDeficiencies` row:

1. `d = row.deficiency` — **not** `row.cause`.
2. If `d` ∈ execution cause registry → proof `cause = d`.
3. Else if `d` in `{None, source-syntax-invalid}` → proof `cause = required-cell-unsatisfied`.
4. Else refuse `EVALUATOR_EXECUTION_CAUSE_UNREGISTERED`.
5. Emit `{source:execution, cause, subjectId:null, predicateId:null, inputRefs:Cset([XI]+row.inputRefs), evidenceKind:null, nativeCause:row.nativeCause, universe:binding.universe}`.

Internal row.cause `native-work-incomplete` / `unsupported-typed` (`execution_inputs_model.v1.py` append sites at unsupported-typed, native-account, inventory/candidate/binding) never become `proof.cause`.

DeficiencyV2 (9): `budget-exhausted`, `confidence-floor-unmet`, `derivation-policy-unmet`, `external-consumers-unknown`, `input-closure-incomplete`, `language-tier-unsupported`, `provider-unavailable`, `required-relation-missing`, `resolution-incomplete`. All nine are in both registries.

---

## 4. Authored correction (frozen24 beforeimage)

Proposed files (relative to this output). Another coauthor owns active target schema/model edits; root three-way integrates nonoverlapping prose/schema descriptions after both handoffs.

| Proposed path | Frozen relative path | bytes | sha256 |
|---|---|---|---|
| `proposed/docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md` | same | 44542 | `634d4bd243b9323f0850396a916b604ce718c7cd4aa761fc3e6699c47a2f9d67` |
| `proposed/docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md` | same | 16372 | `db80e6c7cdcee71ec05b3c4b154932afa7ecd85c10bfbbd79ba3fd3118680cd1` |
| `proposed/docs/coop/design-corrections/foundation/identity-schemas.v3.json` | same | 186386 | `0de21c6d2109208c0a6c0cd57b6ba992561e01dabe0f71dbfeb76db101ae966f` |
| `proposed/docs/v2/contracts/product-v1/identity-and-evidence.md` | same | 119277 | `25423ef98266e1d85ad4182712e8d94954aee9994de28163708f58b3f121d082` |
| `proposed/frozen24.patch` | unified diff of the four | 41802 | `1727cfbc55559a9857161316706254a1f7cf875e2438c1b4c287d2fc24608a47` |
| `proposed/MANIFEST.json` | hashes | — | — |
| `proposed/_section9.md` | extract of new composition §9 | — | — |

Exact patch: `proposed/frozen24.patch` (`diff -u` labels `a/<frozen-relative>` / `b/<frozen-relative>`).

**What the patch does (intended semantics retained):**

- Composition: projection sentence; finding `evidenceRefs` spelled to current emission; §8 points at §9; **new §9** is the complete field recipe.
- Execution-inputs §4/§5: internal vs proof records; bridge; inventory vs Coverage vs candidate originating refs; internal vs proof uniqueness.
- Identity-and-evidence §4: witnesses have no `inputRefs`; whole selection projects onto atomic `predicateProofs[].inputRefs`.
- Identity-schemas: descriptions only (no required-key or enum change) for `evaluationInputRefs`, `predicateProofs[].inputRefs`/`scopeIds`, `executionDeficiencies`, `semantic-evidence.importIds`, `finding.evidenceRefs`, `evaluation-deficiency`, `predicate-witness`.

**What it does not do:** change Kleene, gates, budget formula, native extraction, source inventory, H recipes, scanner code, or add proof coordinates.

**Reference patch:** none. No newly demonstrated invalid output.

---

## 5. Complete field mapping (consumer recipe)

Normative owner: proposed composition **§9**. Summary:

| Output field | Mapping |
|---|---|
| `proof.evaluationInputRefs` (`EI`) | `Cset(selectedRefs ∪ {XI})` |
| Atomic `predicateProofs[].inputRefs` | **equals `EI`** (whole admitted selection) |
| Boolean `predicateProofs[].inputRefs` | `Cset` union of immediate children (= `EI` under this profile) |
| Witness `inputRefs` | **absent** |
| `predicateProofs[].scopeIds`, witness `coverageIds` / match arrays | consulted; may be narrower |
| Enumeration / required-import / atom / correspondence deficiencies | composition §9.5 tables (enumeration inventory refs; required-import empty refs + `evidenceKind`; atom causes copy `EI` except Coverage-entry items which name that Coverage) |
| `proof.executionDeficiencies` | composition §9.6 bridge: `source=execution`; cause from `row.deficiency`; `inputRefs=Cset({XI}∪row.inputRefs)`; null addresses; `nativeCause` from row; universe from binding |
| Inventory vs native-account originating refs | inventory digest vs Coverage digest (table in §9.6) |
| Finding `evidenceRefs` | root witness + descendant facts + consulted Coverage + observation importIds + every `EI` import member |
| Evidence3 `importIds` | exact Plan `importIds` (not evaluated subset, not `EI`) |
| Seal/Run/policy-derivation | existing identity recipes |

`Cset` = unique by `C.canonical`, ordered by those bytes (`x-opensip-order: canonical-set`). Predicate-proof array order = UTF-8 `(ruleId, subjectId, predicateId)`.

---

## 6. Discriminating controls and honest boundaries

| Control | Distinguishes |
|---|---|
| Same-count different-ref proofs disagree on `C(proof)` | selected-field compare vs complete replay (still law) |
| `D2 ⊆ execution registry` and `D2 ⊆ native registry` | internal tokens vs proof causes |
| Feed a requiredCellDeficiencies row with `cause=native-work-incomplete` and `deficiency=provider-unavailable` | emitted proof `cause` must be `provider-unavailable`, not the internal token |
| Atomic `inputRefs` vs witness `coverageIds` | whole-selection vs consulted evidence |
| Evidence3 `importIds` vs witness observation addresses vs atomic `inputRefs` import members | Plan selection vs matched/uncertain rows vs whole-selection copy |
| Two Coverage records with different digests | two proof execution-deficiency items after adding `XI` |
| Two unsupported-typed relations, same DeficiencyV2, same nativeCause, same universe, empty originating refs | **one** proof item; both accounts remain on ExecutionInputsV1 |

**Boundaries.** This session did not re-admit the syntax-data export graph. P7 inventory-convention vs root Coverage+XI remains a graph/convention dispute; the **kit mapping** after this correction is XI plus originating refs, with originating class from independently admitted inventories/accounts. Schema-only validators still cannot certify unique complete proof without implementing composition §9. No whole-kit ACCEPT.

**Uniqueness operand (not a mapping change).** Two required unsupported-typed matrix cells (or two relations on one cell) with identical `deficiency`, `nativeCause`, `universe`, and empty `row.inputRefs` bridge to identical evaluation-deficiency records and `Cset`-collapse. Existing law keeps those coordinates on hashed ExecutionInputsV1. Verdict only needs nonempty execution deficiencies. No proof field added.

---

## 7. Consumer-grade implications (unchanged except syntax-data uniqueness)

- COMPLETE49 original rust FULL_ADMIT: stay withdrawn.
- COMPLETE49 original syntax-data FULL_ADMIT basis: stay withdrawn.
- P7 rust producing `ENUMERATION_MEMBERSHIP_SNAPSHOT_COVER`: first refusal stands.
- P7 TS `IMPORT_PRODUCER_KIND`: first refusal; producing `notReached`.
- P7 rust-partial: first refusal membership/extent; ruleResults mismatch diagnostic.
- P7 syntax-data successor FULL_ADMIT: still **not** accepted here as kit-unique reconstructability on the frozen kit; after integration of this correction, uniqueness is the published §9 bridge (whole-selection + XI∪originating refs), not P7’s inventory-only convention and not consulted-only.
- Pilot symbol census: existing-law omission.

No implementation authorization. No freeze. Root integrates with the other coauthor’s target-identity successor using these nonoverlapping prose/schema descriptions.
