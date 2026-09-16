# Independent design review — consolidated product **source33** (corrected record, v2)

**Verdict: ACCEPT** (source33 design bytes) — unchanged. This is the **complete corrected record** from
a second bounded review-record reconciliation. It supersedes the *record* of reconciliation v1; both
earlier reports are preserved unchanged:

| preserved report | review.json | review.md |
|---|---|---|
| `claude-independent-design.v33/` | `8004658…` | `f2f8a87…` |
| `claude-independent33-reconciliation.v1/` | `ad0457bc…` | `f4015f0e…` |

Reviewer origin `ce3dec3b-0620-44ec-86e6-129b0e25cb1b`, continuing; I have authored no source in this
lineage and am none of the six excluded acceptor origins. No consumer file, blind result, private log
or other author's diagnosis was read.

**What this pass is.** A finite record correction. Frozen source33 is immutable at **12,899** files,
manifest `1cf3db70…`; **no source34 is requested, proposed or implied**. All writes are confined to
this runtime. No suite was re-run: the only new reads are two read-only section-level comparisons of
the two changed owner files, plus re-reads of my own receipts.

Root preserved the REC-01/02/03/05 corrections, the F-row provenance work and the layer4 mapping, and
named four remaining record issues. **I assessed all four against the source and my own record: all
four are substantiated.** Scanning wider than root's phrasing then turned up **one further defective
row root did not name (FW-10)**, and **one row that root's pattern would flag but which is actually
correct (DR-007)**, which I left alone. Section 7 is the ledger.

---

## 0. Custody

Manifest and archive digests match their declared values; all **12,899** rows verified by hash and
size; **736,764,309** bytes; 0 missing, 0 hash mismatches, 0 size mismatches, 0 extras; archive
byte-equal to the manifest; declared parent exactly the source32 I graded. My independently derived
delta is **1 added, 0 removed, 17 changed — 18 touched**, agreeing with root's inventory on all 18
paths. Frozen deviations after every run in all three passes: **0**.

## 1. The changed execution law — correct, and controlled in both directions

**First-match applicability.** The five-token precedence is published as normative; my exhaustive
108-cell grid reaches every token, and the row-3-before-row-4 reachability argument holds.

**External `sourceUniverse` → binding join.** Holds for every applicability, with four refusing and
two admitting controls.

**Request vs selection vs disclosure.** The three stay distinct and each has its own control.
`optional-unsupported-cell-owes-no-required-cell-row` establishes **exactly one thing**: an OPTIONAL
matrix-unsupported cell owes **no** `requiredCellDeficiencies` row and still closes. That control has a
SELECTED enumerator at a NON-NULL universe with an admitted **synthetic** native `unknown` Coverage and
establishes **nothing** about whether a provider was executed or declined — the source says so itself
at `check-execution-inputs.v1.py:1335-1345`. Absence of SELECTION is the separate optional-unselected
control.

**Selected-U unsupported Coverage, and the required bridge.** *(corrected — R33-REC2-03)* A selected-U
unsupported cell keeps its Coverage outside the account while disclosing the matrix pair. When the cell
is **required**, it owes a `requiredCellDeficiencies` **row** and the Run closes `indeterminate`. The
row and the **cause** projected into proof are different things, and conflating them is the error my v1
MD made.

Composition §9.6 step 3 — implemented by `bridge_cause` at `check-execution-inputs.v1.py:714-721`
against `identity-schemas.v3.json#/x-opensip-evaluator-deficiency-registry/sources/execution`, an
11-member registry — resolves the cause like this:

- if the row's own `deficiency` is **registered**, the proof cause **is that deficiency**, carried
  through unchanged;
- the cause is **`required-cell-unsatisfied` only** when that deficiency is `null` — the `(null, null)`
  derived carrier for pure missing work — or `source-syntax-invalid`;
- anything else bridges to `UNREGISTERED:` and fails.

My own measured full-Run rows show exactly that split:

| retained case | verdict | cause pair carried |
|---|---|---|
| `full-run-required-unsupported-matrix-pair-bridge` | indeterminate | **`language-tier-unsupported` / `capability-missing`** (the MATRIX pair) |
| `full-run-empty-returned-partitions-bridge-required-cell-unsatisfied` | indeterminate | `required-cell-unsatisfied` / null |
| `full-run-census-missing-subjects-bridge-keeps-originating-coverage` | indeterminate | `required-cell-unsatisfied` / null |
| `full-run-mixed-accounts-first-typed-pair` | indeterminate | **both**: `budget-exhausted` and `required-cell-unsatisfied` in one Run |

The last row is the clearest single demonstration that the fallback is **conditional, not general**:
the typed account projects its own registered deficiency while the untyped one falls back. My v1 MD
said a required cell "bridges to an indeterminate Run through `required-cell-unsatisfied`", dropping
the null-deficiency precondition; that is **corrected**. The v1 JSON was already right — it said §9.6
"maps a **null** deficiency to proof cause `required-cell-unsatisfied`" and recorded the matrix pair —
so this was an MD-only defect, and no control needed re-running to find or fix it.

**`(null, null)` for pure missing work.** Pure missing work carries the derived `(null, null)` carrier,
and four controls refuse any attempt to claim `provider-unavailable` instead.

**Mixed typed and untyped sources — two distinct ordering levels.** The **whole-cell cross-source**
order is `SOURCE_ORDER` (contract §4, `execution_inputs_model.v1.py:494-505`): binding/enumerator at
index 0; then inventories in this row's `inventoryDigests` canonical-set order; then candidate; then
coverage/account per owed matrix pair in the **authored `relations` ARRAY order** — explicitly not
lexical. **Inside one account**, partitions follow the §5 order (returned partitions in canonical H
order, then named-but-not-returned Coverage), and `_outcome_from_items` takes the pair WHOLE from the
first source that actually carries a typed pair.

**Per-universe attribution.** The clause is deliberately narrow: it constrains only views reached
**through** a selected binding's account derivation and forbids exactly one thing. Its evidence,
`rec("owner-graph-two-universes", admit(two))` at line 886, is **admission-only** — not a measured Run.

**The two-owner contradiction, corrected together.** Composition's previously prescribed
`provider-unavailable` fallback was a genuine contradiction between two normative owners, corrected
together with execution-inputs and recorded on the contract's own face.

**Control set and the full-Run column.** 75 cases, 0 mismatches, 41 admitting, 34 refusing, five
full-Run rows with real `run3:` ids. The full-Run digest binding is `check-execution-inputs.v1.py:751`
— `if admission_digest != proof["executionInputsDigest"]` inside `full_run_case`, `controlStanding:
"closed-run"`. The `digest0` form at 1177-1187 belongs to a `helper-unit` control.

## 2. Bounded scopes

**Candidate envelope: schema admission only.** Not a retained join, not a full Run, and not a
retroactive success for the original author q2 command.

**Optional candidate carrier reachability — measured.** The root-authored control (digest `e32d15f0…`
verified before execution) reached
`run3:a6a17e18de4555538b55defc75925113ff96946403316e322eeeb5a3c1de189a`: structural ADMIT, semantic
ADMIT, verdict pass, `executionDeficiencies: []`, candidate cell `required: false` at a non-null
universe with `enumeratorStatus: selected`, `candidateResultDigest: null`, `deficiency: null`,
`nativeCause: null`; frozen33 drift 0 before and after. A **root-authored control independently
executed, not a new independent consumer implementation**. It says nothing about REQUIRED candidate
cells, which still refuse `EXECUTION_INPUTS_CANDIDATE_REQUIRED` without an envelope.
`extra-candidate-ref-no-outcome` returns **both** `EXECUTION_INPUTS_CANDIDATE_REQUIRED` and
`EXECUTION_INPUTS_REF_INVALID_BYTES`, so the first refusal masks the second condition — recorded as a
limit, with no control built to raise a count.

## 3. Suites and planning

Six changed-input suites run on frozen33, all exit 0: `check-execution-inputs.v1.py`,
`check-replay.v3.py`, `check-enumeration.v1.py`, `check-identity.py` (1596/1596),
`check_native_evidence.v2.py`, `check-integration.py`. Planning **layer4** carries 29 pins, all
resolving against frozen33, differing from layer3 by exactly one repin (`native-evidence.md`), nothing
added or removed; layer3, layer2 and the original layer are preserved. Populations unchanged: 198
paths, 20 packages, 320 coverage mappings, M0–M6, **54 recovery cases, 0 executed**.

## 4. Author package — verified on source33

Package10 verifies: artifact manifest matches the root-named digest `88c38b16…`, **305/305** members
hash-verified, source-manifest byte-equal to the frozen33 manifest, all 13 Run/control cases replay as
expected through **both** boundaries with my own decoder, `verify-package.py` rc 0 over 12,899 source
files and 305 package files with 7/7 query checks.

*(corrected — R33-REC2-02)* The **current** evidence pointer now binds that measurement (receipts
p12/p13, root input `98548046…` at `READY_FOR_INDEPENDENT_REVIEW`). The earlier p11 record — status
`INCOMPLETE` against the **pending** root input `5ac4a3ec…` — is retained and explicitly labelled
**historical**: it ran before the root-owned input named any package10. A single record cannot carry
both as current, and previously mine did.

**Mixed provenance.** From package10's own `source-binding.v33.json`: `checkpoint3`,
`binding-controls` and `semantic-controls1` are **new source33 constructions** from the corrected
bundled helper (`helperChanged: ["author-helpers/evaluator.py"]`); `normalized-examples6` (4) and
`rust-selection-examples1` (2) are the **exact source30 bytes**, re-verified. Package9 remains known
stale and was not re-run. Verifying package evidence is not accepting the package as a product
artifact.

## 5. Advisories

**A-9** — repair selection law is reference-level only; limits intact, repair owners not in the delta.

**A-10** — limits unchanged (exists/none only; and/or/not unexercised; count-at-most and all-covered
unimplemented; two-binding construction incomplete), but the **constructed evidence** those limits
describe changed on 33: `binding-controls` and `author-helpers/evaluator.py` are among the new source33
constructions. The limits still hold, measured on the new construction.

**A-11** — resolved during the source33 review.

## 6. Dispositions, owner scope and inheritance

All **107** maps are carried complete and unchanged in count: **14** F, **30** evaluation residuals,
**16** AR, **15** FW, **27** inherited residuals, **5** scoped review owners. Every row carries
`appliedByThisReview: false` and `finalApplicationOutcomeGranted: false`.

*(corrected — R33-REC2-01 and R33-REC2-04)* Each row's current field now belongs to one of three
honestly-labelled classes:

- **21 rows whose owner bytes changed.** Eleven now carry substantive current text written here (the
  eight corrected under R33-REC2-01 plus the three residuals under R33-REC2-04); the other ten already
  did. For each corrected row I measured the change at section level, read-only on both sides, and
  state what changed, why this row's specific law is nonetheless unchanged, and the current
  implication. The record carries its own audit of this class at `$.changedOwnerRowAudit`: **12** rows
  name the changed owner path, **9** describe the change in prose without repeating the path (for
  example AR-12 "the native chapter now agrees with execution-inputs §5", DR-011-R01 "the execution law
  now states explicitly…"), and **0** deny or stay silent about their own change. The nine are accurate
  as written, so I left them alone rather than cosmetically rewriting them to repeat a filename.
- **72 rows whose owner bytes are verified unchanged** and whose owner paths resolve in frozen33. These
  are marked **INHERITED**: the prior substantive reasoning is *expressly adopted as current on that
  byte verification*, and explicitly labelled as inherited evidence rather than a fresh re-derivation.
  My v1 wording disclaimed it as "not current evidence", which understated rows that legitimately carry
  forward.
- **14 F rows** with no owner array, which already hold bespoke current text measured on 33.

**The two changed owners, measured.** `native-evidence.md`: 61 sections on each side, **none added,
none removed, exactly one changed** — *"Admission and event routes (existing; unchanged rows)"* — with
**zero deleted lines**, i.e. a pure addition. The added paragraph says where an answered native
`unknown` Coverage is accounted for: it stays in its returned view, the stage capture and
`selectedRefs`, while the account names **no** `coverageIds`; a required such cell holds the Run at
`indeterminate` through the required-execution bridge; an execution outcome of `complete` means that
cell's account was **answered**, never that the capability became supported.
`evaluator-composition-contract.v3.md`: 19 sections on each side, none added or removed, exactly one
changed — *"§9.6 `proof.executionDeficiencies` — required-execution bridge"*.

Carried forward unchanged: **28** condition-2 obligations retained; **32** product qualification gates,
**0** performed, condition 5 **NOT MET**; **54** recovery cases unexecuted; the D9 successor carrying
host-invariant remains an **assigned, open** implementation obligation on **DR-007** and
**DR-011-R08**. TCB-SCOPE-01 is assessed once over its **13** dependent rows and is **not** closed
here; reopening it reopens all 13 jointly. All **30** author residual proposals remain **PENDING**
independent grading.

This grants nothing: no grade, no architecture-ready, no activation, no implementation authorization,
no blind acceptance, no package acceptance, no final application outcome, no commit or push.

## 7. Correction ledger — R33-REC2-01…04

| Item | Disposition | Evidence | Principal selectors |
|---|---|---|---|
| **R33-REC2-01** seven unchanged-assertions contradicting their own changed-owner arrays | **Accepted and corrected — plus one more row found** | I re-derived the set rather than taking the list: root's exact phrase across all 107 rows returns precisely their seven. Widening to *any* denial across all **21** changed-owner rows returns **nine** — the seven, plus **FW-10** (a genuine eighth: it named only five unchanged owners and silently omitted `native-evidence.md`, which is in its own changed array) and **DR-007** (a **false positive**: it already says the owning fault contract is not in the delta and the native chapter is — correct, so unchanged). Section-level measurement then scoped each change to exactly one section per file. | `$.arDispositions.AR-13` · `$.fwDispositions.{FW-01,FW-02,FW-04,FW-10}` · `$.inheritedResidualDispositions.{DR-011-R03,DR-011-R05,DR-011-R08}` `.currentStatusOn33` · `$.*.*.ownerChangeScopeMeasuredOn33` |
| **R33-REC2-02** current package receipt still `INCOMPLETE` | **Accepted and corrected** | `evidenceReceipts.authorPackage` read `{"status": "INCOMPLETE", "rootInputSha256": "5ac4a3ec…"}` — the **pending** input digest — while `authorPackageReview.status` read COMPLETE and p12/p13 recorded 305/305, manifest `88c38b16…`, source-manifest equal to frozen33, rc 0, 7/7 queries. The current pointer now binds p12/p13; p11 is kept as `historicalP11`. | `$.evidenceReceipts.authorPackage` · `.currentMeasurement` · `.historicalP11` |
| **R33-REC2-03** MD conflated the required-cell **row** with the cause fallback | **Accepted — MD corrected, exact rule added** | `bridge_cause` (checker 714-721) returns the deficiency itself when registered, and `required-cell-unsatisfied` only for `null`/`source-syntax-invalid`; the registry lists 11 execution deficiencies including `language-tier-unsupported`. The retained control at 1412-1414 expects `["language-tier-unsupported"]`; 1406-1411 expect `["required-cell-unsatisfied"]`; my own `fullRunRows` receipt records the matching pairs. **The defect was MD-only — the v1 JSON already carried the null-deficiency precondition.** | review.md §1 · `…requiredCellBridgeAndUniqueness.exactCauseRule` · `.measuredCauseSplit` · `…selectedUnsupportedCoverageRetention.causeIsTheMatrixPairNotTheFallback` |
| **R33-REC2-04** three residuals had provenance notes but no current substance | **Accepted and corrected** | The three carried only "owner bytes CHANGED … re-read this session" plus a pointer disclaiming the prior reasoning — which cannot support a carried disposition. Scoped by measurement: the composition change is confined to §9.6; none of RES-EP13-01's or RES-EP13-15's subject terms occurs in the added text, while RES-EP13-07's subject is exactly what §9.6 tightens; their other owner `identity-and-evidence.md` is byte-unchanged, with package10 recording the same digest before and after. RES-EP13-07's controls sit in `semantic-controls1`, newly constructed on 33 and replayed in my package10 verification. All three remain PENDING and ungraded. | `$.evaluationResidualDispositions.{RES-EP13-01,RES-EP13-07,RES-EP13-15}.currentStatusOn33` |

**A new defect of my own, stated plainly.** FW-10 is mine, not root's: root named seven rows and my
wider scan found an eighth. It is a **record-accuracy defect only** — no source defect, no disposition
change, no verdict change — and it is fixed here. I report it because a reviewer who only fixes the
list they were handed has not audited anything.

**On the invariant tests themselves.** 47 invariants pass, and they are claims that could have been
false: current assertions against each row's own changed-owner array, current-versus-historical package
receipt consistency, and the required-cell bridge cause checked against **both** the retained
measurement and the frozen `bridge_cause` rule. Two checks failed on first run and I triaged rather
than reran them into green. One was a genuine check defect — it forbade the withdrawn sentence
outright, so quoting it *as withdrawn* tripped it; it now requires every occurrence to sit in a
correction context. The other was my own overreach: it demanded that every changed-owner row repeat the
owner's filename, which six accurate rows do not do. The defect class root identified is **denial or
silence**, not phrasing, so the invariant now fails on denial or silence and the naming split is
censused in the record instead. Neither refinement weakens the test that caught the eight rows: run
against the v1 record, it still fails on all eight.

**Preserved errors.** The source33 report, reconciliation v1, and every previously recorded probe error
stay exactly as they were — the document-wide table-order index, the metric that read False because a
clean PASS row has no refs, the keyword scan that mistook a lawful `provider-unavailable` carrier for
the forbidden one, the invented envelope record shape, the misread negative-group `passed` field, and
the p09 reasoning withdrawn under R33-REC-02. This record qualifies that history; it does not rewrite
it.

## 8. Remaining blocker — stated plainly

**One, and it is not mine to close:** whether these corrections satisfy the condition on root's design
assent is root's call. Everything inside this bounded scope is resolved — four of four accepted on
measured evidence, one further defect found and fixed on my own initiative, one root-pattern match
examined and correctly left alone.

**No new source defect.** Nothing in this pass found a defect in frozen source33, and no source34 is
requested or implied.

Unchanged and still open beyond this scope: 30 residual proposals PENDING independent grading, 32
qualification gates and 54 recovery cases unperformed with condition 5 NOT MET, TCB-SCOPE-01 open over
its 13 dependent rows, the D9 successor obligation on DR-007 / DR-011-R08 assigned and open, and the
original blind reconstruction and final application review untouched — separate work I have not done
and must not do.
