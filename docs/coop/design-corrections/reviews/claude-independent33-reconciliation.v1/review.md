# Independent design review — consolidated product **source33** (corrected record)

**Verdict: ACCEPT** (source33 design bytes) — unchanged from my source33 review. This document is the
**complete corrected record** produced by a bounded review-record and measured-scope reconciliation.
It supersedes the *record* of that review; the original report is preserved unchanged at
`claude-independent-design.v33/` (`review.json` `8004658…`, `review.md` `f2f8a87…`).

Reviewer origin `ce3dec3b-0620-44ec-86e6-129b0e25cb1b`, continuing. I have authored no source in this
lineage and I am none of the six excluded acceptor origins. No consumer output, runtime, report or
root blind replay file was opened.

**What this pass is.** A record correction plus **one** newly measured scope. It is **not** source
authoring and **not** a new source freeze: frozen source33 remains immutable at **12,899** files,
manifest `1cf3db70d4b73b0c42f1393331e6a874ee26f7ddf67aa05c6ac15a5753069299`. All writes are confined to
this runtime. No unchanged suite was re-run merely because prose changed. The substantive ACCEPT and
its basis are preserved, not re-derived.

Root withheld design assent pending five record corrections (R33-REC-01…05). I assessed each against
the source rather than accepting it on authority. **All five are substantiated; I found
counter-evidence against none of them.** Section 7 is the ledger, with exact JSON selectors.

---

## 0. Custody

Manifest and archive digests match their declared values; all **12,899** rows verified by hash and
size; **736,764,309** bytes measured against the same declared total; 0 missing, 0 hash mismatches, 0
size mismatches, 0 extras; the archive is byte-equal to the manifest across every member; the declared
parent is exactly the source32 I graded.

My independently derived delta is **1 added, 0 removed, 17 changed — 18 touched**, agreeing with
root's inventory on all 18 paths. Frozen deviations after every run in both passes: **0**.

## 1. The changed execution law — correct, and controlled in both directions

**First-match applicability.** The five-token precedence is published as normative. My exhaustive
108-cell grid reaches every token, and the row-3-before-row-4 reachability argument holds.

**External `sourceUniverse` → binding join.** Holds for every applicability, with four refusing and
two admitting controls.

**Request vs selection vs disclosure.** *(corrected — R33-REC-01)* The three stay distinct and each
has its own control. A capability REQUEST can be UNSUPPORTED-TYPED and still requestable; ENUMERATOR
selection is separately unselected or selected-at-null-U; optional retained DISCLOSURE is a third
thing, controlled by `optional-unselected-account-retained-typed-disclosure`.

`optional-unsupported-cell-owes-no-required-cell-row` establishes **exactly one thing**: an OPTIONAL
matrix-unsupported cell owes **no** `requiredCellDeficiencies` row and still closes. That control has
a SELECTED enumerator at a NON-NULL universe with an admitted **synthetic** native `unknown` Coverage,
and it establishes **nothing** about whether a provider was executed or declined — no synthetic
reference fixture executes or declines a real provider. Absence of SELECTION is the separate
optional-unselected control. The source says so itself at `check-execution-inputs.v1.py:1335-1345` and
repeats it in the control's own note. My source33 record said this control shows such a cell "is not
forced to execute a provider to close"; that resurrected an overclaim the source had already
qualified, and it is **withdrawn**.

**Selected-U unsupported Coverage, and the required bridge.** A selected-U unsupported cell keeps its
Coverage outside the account while disclosing the matrix pair, and when the cell is required it
bridges to an indeterminate Run through `required-cell-unsatisfied`.

**`(null, null)` for pure missing work.** Pure missing work carries the derived `(null, null)` carrier,
and four controls refuse any attempt to claim `provider-unavailable` instead.

**Mixed typed and untyped sources — two distinct ordering levels.** *(corrected — R33-REC-03)*
The **whole-cell cross-source** order is `SOURCE_ORDER`, contract §4, documented at
`execution_inputs_model.v1.py:494-505`:

1. the `enumerator`/`binding` carrier, inserted at index 0 so it precedes the same cell's inventories;
2. `inventory`, one per non-complete inventory, in this row's `inventoryDigests` order, whose schema
   order is `canonical-set`;
3. `candidate`, at most one, for a candidate-only capability;
4. `coverage`/`account` per owed matrix pair, in the **authored `relations` ARRAY order** in
   `native-capability-matrix.v2.json` — explicitly **not** lexical, since `syntax` is authored
   `declares, literal, control-flow`.

No host array order and no lexical guess is read anywhere in it. **Inside one account**, the
partitions follow the §5 order — returned partitions in canonical H order, then any
named-but-not-returned Coverage — and `_outcome_from_items` takes the pair WHOLE from the first source
that actually carries a typed pair, which is what stops an untyped source from masking a typed one.
My source33 record gave only the per-account partition order and presented it as the ordering for the
cell. The two levels are now stated separately.

**Per-universe attribution.** *(corrected — R33-REC-03)* The clause is deliberately narrow and says
so: it constrains only views reached **through** a selected binding's account derivation, forbids
exactly one thing — one view carrying two universes' Coverage then attributed to a binding fixed at
one — and does not ban multi-universe Runs, cross-universe targets or incoming targets. Its evidence
is `rec("owner-graph-two-universes", admit(two))` at `check-execution-inputs.v1.py:886`, which is
**admission-only**: it shows a two-universe manifest admits. It is not a measured complete Run, and I
no longer describe it as showing the multi-universe Run stays lawful end to end.

**The two-owner contradiction, corrected together.** The parent composition contract's previously
prescribed `provider-unavailable` fallback was a genuine contradiction between two normative owners.
It is corrected together with execution-inputs and recorded honestly on the record.

**Control set and the full-Run column.** 75 cases, 0 mismatches, 41 admitting and 34 refusing,
including five full-Run rows with real `run3:` ids. *(corrected — R33-REC-03)* The full-Run column's
digest binding is `check-execution-inputs.v1.py:751` —
`if admission_digest != proof["executionInputsDigest"]` inside `full_run_case`, where
`admission_digest` is `M.raw_digest(admission_inputs["execution_inputs"])` from line 742, and the case
records `controlStanding: "closed-run"`. My source33 record instead quoted
`attached["graph"]["inputs"]["executionInputsDigest"] == digest0`, which lives at lines 1177-1187 under
`controlStanding: "helper-unit"`. The substance — the full-Run column binds an exact ExecutionInputs
digest — survives; the selector was wrong and is corrected.

## 2. Bounded scopes

**Candidate envelope: schema admission only.** Not a retained join, not a full Run, and not a
retroactive success for the original author q2 command, whose invalid `execution2` prefix and refusal
stand.

**Optional candidate carrier reachability — claim withdrawn, then measured.** *(R33-REC-02)* My p09
reasoning combined two different fixtures: `optional-candidate-absent-envelope-derives-null-pair` is
**admission-only** and carries `fullRunId` null, while the only full-Run case in that probe is
`full-run-optional-unselected-and-optional-unsupported` (`run3:87d2fa33…`), a different
optional-unselected + unsupported fixture. Together they did **not** establish full-Run reachability
for a SELECTED optional cell with a missing candidate. Withdrawn.

I then measured the exact path. The control is **root-authored**; I read it in full, verified its
digest `e32d15f0…` against the declared one before executing it, and ran it against frozen33 with
`-I -B`. **This is a root-authored control independently executed, NOT a new independent consumer
implementation.** Result:

| | |
|---|---|
| structural admission | **ADMIT** |
| semantic admission | **ADMIT** |
| runId | `run3:a6a17e18de4555538b55defc75925113ff96946403316e322eeeb5a3c1de189a` |
| verdict | **pass**, `executionDeficiencies: []` |
| candidate cell | `required: false`, non-null universe, `enumeratorStatus: selected`, `candidateResultDigest: null`, `state: unavailable`, `deficiency: null`, `nativeCause: null` |
| frozen33 drift | **0 before, 0 after** (my own check, plus the control's own empty `sourceDrift`) |

So the full-Run path is reachable for a selected optional cell with no retained candidate envelope and
no candidate reference, and **no carrier was manufactured** for the missing optional candidate. It
remains a synthetic reference-fixture transformation: no provider, compiler, OS or host qualification,
no blind reconstruction, and nothing about REQUIRED candidate cells, which still refuse
`EXECUTION_INPUTS_CANDIDATE_REQUIRED` without an envelope.

**A recorded limit.** `extra-candidate-ref-no-outcome` returns **both**
`EXECUTION_INPUTS_CANDIDATE_REQUIRED` and `EXECUTION_INPUTS_REF_INVALID_BYTES`, so it does not isolate
a missing matching outcome or envelope under otherwise valid joins — the first refusal masks the
second condition. That observed masking is the limit. I built no further control; no test is written
merely to raise a count.

## 3. Suites and planning

Six changed-input suites run on frozen33, all exit 0: `check-execution-inputs.v1.py`,
`check-replay.v3.py`, `check-enumeration.v1.py`, `check-identity.py` (1596/1596),
`check_native_evidence.v2.py`, `check-integration.py`. 1357 disposable files copied and verified.

Planning **layer4** carries 29 pins, all resolving against frozen33, differing from layer3 by exactly
one repin — `docs/v2/contracts/product-v1/native-evidence.md` — with nothing added or removed. Layer3,
layer2 and the original layer remain in the source as preserved history. Populations are unchanged:
198 paths, 20 packages, 320 coverage mappings, M0–M6, **54 recovery cases, 0 executed**.

## 4. Author package — verified on source33

Package10 verifies: artifact manifest matches the root-named digest `88c38b16…`, **305/305** members
hash-verified, source-manifest byte-equal to the frozen33 manifest, all 13 Run/control cases replay as
expected through **both** `open_run_closure` and `close_run` with my own decoder, and
`verify-package.py` exits 0 over 12,899 source files with 7/7 query checks.

**Mixed provenance, stated exactly** *(R33-REC-05, and F-10)*. From package10's own
`source-binding.v33.json`: the three TypeScript-derived groups — `checkpoint3`, `binding-controls`,
`semantic-controls1` — are **new source33 constructions** from the corrected bundled author helper
(`helperChanged: ["author-helpers/evaluator.py"]`, `exportsChangedDetail` naming exactly those three);
`normalized-examples6` (4) and `rust-selection-examples1` (2) are the **exact source30 construction
bytes**, re-verified rather than rebuilt. The file records
`constructionSourceVersion {typescriptDerivedGroups: 33, normalizedAndRustGroups: 30}`. I did not
re-run the constructors.

Package9 remains known stale and was **not** re-run; its failure is assessed from preserved receipts.
Verifying package evidence is not accepting the package as a product artifact and grants no
application outcome.

## 5. Advisories

**A-9** — the repair selection law is reference-level only; no product surface emits it. Carried with
its limits intact: the repair owners are not in my 32→33 delta.

**A-10** — two-binding and combinator coverage remain unexercised. *(corrected — R33-REC-05)* The
**limits** are unchanged on 33: exists/none only, and/or/not unexercised, count-at-most and
all-covered unimplemented in the partial helper, two-binding construction still incomplete with a
single-explicit control. But the **constructed evidence** those limits describe **did** change: the
`binding-controls` group and `author-helpers/evaluator.py` are among the new source33 constructions.
My blanket "nothing in my derived 32→33 delta touches this advisory's subject" was too broad — the
source delta indeed does not, but the package rebuild does — and it is withdrawn. The limits still
hold, now measured on the new construction.

**A-11** — resolved during the source33 review, when the root input named package10 and I verified it.

## 6. Dispositions and standing

All **107** individual maps are carried complete and unchanged in count: **14** F rows, **30**
evaluation residuals, **16** AR, **15** FW, **27** inherited residuals, **5** scoped review owners.
Every row still carries `appliedByThisReview: false` and `finalApplicationOutcomeGranted: false`.

Every **current** field now states current source33 truth only, and every row carries an explicit
pointer that its source32 reasoning is preserved verbatim in the prior field **as history, not as
current evidence**. No prior field was edited and no blanket 32→33 substitution was made — see §7.

Carried forward unchanged: **28** condition-2 obligations retained; **32** product qualification gates
with **0** performed and condition 5 **NOT MET**; **54** recovery cases unexecuted; the published D9
successor carrying host-invariant remains an **assigned** implementation obligation on **DR-007** and
**DR-011-R08**, carried forward and not closed. TCB-SCOPE-01 is assessed once over its **13**
dependent rows, and reopening it reopens all 13 jointly. All **30** author residual proposals remain
**PENDING** independent grading; I grade none of them here.

This grants nothing: no grade, no architecture-ready, no activation, no implementation authorization,
no blind acceptance, no package acceptance, no final application outcome, no commit or push. Still
required: the final application review and activation, a successful original blind reconstruction, and
product qualification of the 32 gates and 54 recovery cases.

## 7. Correction ledger — R33-REC-01…05

| Item | Disposition | Evidence | Principal selectors |
|---|---|---|---|
| **R33-REC-01** optional-unsupported control overclaim | **Accepted and corrected** | `check-execution-inputs.v1.py:1335-1345` states in the source that the control "establishes NOTHING about whether a provider was executed"; the control note repeats it. The provider-execution reading was in my `review.json`; my `review.md` did not carry that phrase. | `$.sourceChangeAssessment.executionInputsLaw.requestVersusSelectionVersusDisclosure.assessment` · `.exactQualification` · `…selectedUnsupportedCoverageRetention.optionalNotForced` · md §1 |
| **R33-REC-02** p09 combined two fixtures | **Accepted; claim withdrawn, exact path measured** | My own p09 receipt: the optional-candidate case has `fullRunId` null; the full-Run case is a different fixture. Root-authored control (`e32d15f0…`, digest verified first) independently executed on frozen33 → `run3:a6a17e18…`, ADMIT/ADMIT, verdict pass, `executionDeficiencies: []`, `candidateResultDigest: null`, drift 0/0. `extra-candidate-ref-no-outcome` dual refusal recorded as a masking limit. | `$.sourceChangeAssessment.boundedScopes.optionalCandidateCarrierReachability` · `.newMeasuredScope` · `$.evidenceReceipts.newFullRunCandidateControl` · md §2 |
| **R33-REC-03** full-Run selector, two-universes standing, ordering level | **Accepted on all three parts** | Line 751 is `admission_digest != proof["executionInputsDigest"]` inside `full_run_case` (`closed-run`); 1177-1187 carry `digest0` under `helper-unit`; 886 is `admit(two)` with no Run; `execution_inputs_model.v1.py:494-505` documents the four-step cross-source `SOURCE_ORDER` whose account step follows the authored `relations` array. | `…fullRunColumn.digestBindingExactSelector` · `…perUniverseAttribution.evidenceStandingCorrectedR33REC03` · `…mixedTypedAndUntypedSources.wholeCellCrossSourceOrder` · `.perAccountPartitionOrder` · `$.fwDispositions.FW-06.currentStatusOn33` · md §1 |
| **R33-REC-04** stale prose in current fields | **Accepted; all 107 current fields rewritten** | The mechanical cause: on **96** of 107 rows the current field was the current prefix followed by the prior field **verbatim**, which reproduced every example root named (F-03 "executed it against frozen32", F-05 "snapshot32", F-13 "binds the frozen32 manifest", RES-EP13-05 "12,898 rows", DR-204 "frozen32 / 12,898 / inputs.v3", F-01 "277 members"). Auditing F-09's false unchanged-claim across the F rows — which have no owner arrays and so escaped the mechanical pass — found the same defect on **F-04** (`enumeration-contract.v1.md` is in the delta) and imprecision on F-07/F-13/F-14, whose subjects are rebuilt package artifacts. | `$.fDispositions.*.currentBasisOn33` · `$.{evaluationResidual,ar,fw,inheritedResidual,scopedReviewOwner}Dispositions.*.currentStatusOn33` · `$.*.*.currentFieldStandingOn33` · `$.scopedReviewOwnerDispositions.DR-204.currentOwnerFiles` / `.ownerFilesChangedIn32to33` / `.ownerFilesUnchangedIn32to33` · `$.currentFieldAudit` |
| **R33-REC-05** A-9/A-10 blanket unchanged claim | **Accepted and qualified** | `source-binding.v33.json` records `exportsChanged: true`, `exportsChangedDetail: "checkpoint3, binding-controls and semantic-controls1 only"`, `helperChanged: ["author-helpers/evaluator.py"]`. A-10's limits are unchanged but its constructed evidence changed. A-9's source owners really are absent from the delta, so only the over-broad phrasing was tightened. | `$.advisories[?(@.id=="A-10")].statusOn33` / `.selectors` / `.whyStillNotAShould` · `$.advisories[?(@.id=="A-9")].statusOn33` · `$.fDispositions.F-10.currentBasisOn33` |

**How R33-REC-04 was fixed.** The appended prior suffix was removed from those 96 fields — the text
remains verbatim in the prior field — **16** rows received bespoke current text measured on 33, and
every current field gained an explicit HISTORY pointer. DR-204's current owner array now names
`implementation-normative-inputs.v4.json` (the one added file in the 18-file delta) alongside the
preserved v3; both resolve in the frozen33 manifest. All current facts used came from records already
measured in this session or the source33 pass — package10 305/305, 12,899 files, layer4 pins, suite
exit codes, the residual assessment binding — so no unchanged suite was re-run to restate them.

**Preserved errors.** The original source33 report and all previously recorded probe errors stay
exactly as they were, including the document-wide table-order index, the metric that read False
because a clean PASS row has no refs, the keyword scan that mistook a lawful `provider-unavailable`
carrier for the forbidden one, the invented envelope record shape, and the initial misreading of a
negative group's `passed` field. The p09 reasoning withdrawn under R33-REC-02 is added to that list;
its receipt is preserved unchanged. This record qualifies that history — it does not rewrite it.

## 8. Remaining blocker — stated plainly

There is **one**, and it is not mine to close: the five R33-REC items were the stated condition on
root's design assent, and whether these corrections satisfy it is root's call, not something I can
assert for root. Everything I can resolve within this bounded scope is resolved — five of five
accepted on measured evidence, one withdrawn claim replaced by a real measurement, all 107 current
fields rewritten, no source defect found or introduced.

Beyond that, nothing here changes what was already outstanding and unowned by this review: the 30
author residual proposals are still PENDING independent grading, 32 qualification gates and 54
recovery cases are still unperformed, the D9 successor obligation on DR-007 / DR-011-R08 is still
assigned and open, and the original blind reconstruction and the final application review remain
separate work I have not touched and must not.
