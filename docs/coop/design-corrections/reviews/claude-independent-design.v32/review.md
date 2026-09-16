# Independent design review — consolidated product **source32**

Same reviewer origin `ce3dec3b-0620-44ec-86e6-129b0e25cb1b`. I have authored no source in this
lineage and am not a coauthor. My source31 ACCEPT and the later bounded glob/repair review are
historical and unchanged; **neither accepts these integrated bytes**, which are assessed here on
their own evidence.

**Verdict: ACCEPT.** Zero new MUST, zero new SHOULD, two advisories each stating why it is not a
SHOULD.

**Design review only.** No application grade, no activation, no blind acceptance, no implementation
authorization, no commit or push. I am none of the five forbidden source-author origins; author
SID `919c766d…` is a coauthor of these bytes and is not an independent acceptor.

---

## 0. Verification

| Binding | Expected | Measured |
|---|---|---|
| `candidate-subject.v32.json` | `3897e8d1…0bf2` | ✅ |
| `candidate-source.v32.tar.gz` | `acbc2beb…5d96` | ✅ |
| Snapshot | 12,898 files / 736,666,114 B | ✅ every row's hash **and** size; 0 missing, 0 mismatched, **0 extras** |
| Archive ↔ manifest | — | ✅ **all 12,898 members** compared byte-for-byte; 0 mismatches, none extra, none absent |
| Ancestry | parent = my v31 | ✅ `ca713db5…` is exactly the frozen31 I graded |
| Package 8 | `116a0f30…cab4` | ✅ **277/277** members; `source-manifest.json` byte-equal to the frozen32 manifest |

Frozen32 re-measured **unchanged** after every run (0 deviations). Report writers ran only in a
disposable copy of 1,356 files verified byte-equal to the manifest first.

`consumer-b*` runtimes were excluded by name from every inventory and never opened.

**My delta: 3 added, 0 removed, 23 changed (26 touched), +129,607 bytes**, derived from the two
frozen manifests before consulting anything else. `root-delta31-to32.json` names the **same 26
paths** with the same 0 removals — full agreement. (My first probe searched the reviews tree and
`/tmp` and reported it unlocatable; it was in my own runtime root. Corrected here, probe preserved.)
Root's listing is an inventory, not approval.

## 1. The new repair closed-world selection owner — substantively correct

`workflows/repair_closed_world_selection.v1.py` (new, 622 lines) with the law published as
`workflows-and-surfaces.md` **§6**. I executed the module across ten property groups rather than
reading it for agreement:

| Property | Result |
|---|---|
| Ownership from the retained **EnumerationPlan**, not scopes | symbol-extent owner `uB` **is returned** — the RRS-A1 gap my bounded review confirmed is closed |
| `candidateSourcePaths` counts as ownership | ✅ reported with its own extent kind |
| Selected **unavailable** binding (`universe=null`) | ✅ typed unresolved carrying its deficiency — and an available *closed* owner of the same path does **not** discharge it |
| **Unselected** programs | ✅ contribute to neither bucket; never inferred |
| file / package / symbol extents | ✅ stay distinct per binding; an unrelated path is in no census, so all snapshot files are **not** every compiler's `programRootFiles` |
| source-path scopes | ✅ demoted to an **additional witness**, unioned, never a completeness certificate |
| Coverage selection | ✅ on `sourceUniverse` alone, **independent of `evidenceRequirements`** — a recipe cannot narrow the evidence |
| Conjunction | ✅ non-vacuous; uncovered universe, unowned path and unresolved owner each report `REPAIR.CLOSED_WORLD_NOT_ESTABLISHED` |
| Display reduction | ✅ absence folds in and flips the boolean, so the summary cannot read closed while eligibility is refused; the sentinel has exactly **two** `unknown` members and is never "all-unknown" |
| Remedies | ✅ name all six ordering members including the retained `coverage2` identity — two records differing only in `targetUniverse`, `subjectScopeCommitment` and identity now yield **distinct** coordinates |

Chapter 6 publishes all eight of those law claims; both repair schemas carry annotations naming the
selection owner and the non-authoritative display with its least-closed sentinel; `native-evidence.md`
links workflows §6 as the consuming owner; and `workflows_model.v3` exposes the seam while recording
that the historical major-1 profile keeps its own behaviour.

**A concern I raised and resolved myself.** The module derives `cellOrdinal` with `enumerate()`, but
the enumeration contract says `cellOrdinal` is the index *after* the published sort and is not stored.
`identity-model.ordered()` has no named `cells` branch — so I tested the validator directly: on an
isolated schema the declared `{by:[…]}` order **admits** and a shuffled or duplicated order
**refuses**. The plan schema declares that order on `cells` and §8 names the ExactValidator as the
plan validator, so `enumerate()` yields the normative ordinal. **No finding.**

## 2. RRS-A3 evidence scope — honestly scoped, no correction needed

The asymmetric control is a **fully admitted Run** (fixture → `admit_coverage_result_v3` →
`close_run` complete semantic replay), and the source's own comments state the limits I would
otherwise have to raise:

- the empty-target derivation "isolates path ownership only… **not a lawful repair request (targets
  requires minItems=1)**";
- the sole matched finding belongs to the symbol universe, so a legal target already reaches it under
  the earlier target-occurrence join — and therefore "**this control does not prove a lawful
  old-preview bypass**";
- the projection control now uses **actual nonempty targets**, with a check asserting they are nonempty;
- `_cw_preview`'s own docstring: the adapter is historical fixture data not derived from the Run, the
  inherited constructor emits a major-1 descriptor, and it "demonstrates **gate integration only**,
  not current descriptor admission or snapshot joins";
- UNIT controls are labelled in their ids, and the unavailable/candidate-only controls state that the
  frozen fixture builds no such binding.

**My assessment: the bounded design/reference evidence is sufficient for what it claims.** I do not
report the invalid adapter input as a product bypass, because it is not one — an empty-target
derivation and a major-1 synthetic descriptor are invalid or historical inputs, not a lawful path
through current law. I also do not demand a product repair implementation as a design acceptance
prerequisite. **No narrow reference correction is needed**: the limit is stated in three separate
places and the one control that could have been misread now runs with real targets.

## 3. Glob, planning, suites

**Glob** now has one coherent normative reading across **all six** owners — the four earlier ones, the
projection contract, and the **new main-chapter link** ("the single portable glob contract"). The
matcher implementation is unchanged; my bounded review's 5,927,922-pair differential result is
inherited here under exact-byte verification of the contract, and I restate that it was **not** a
blind prose-only origin — I had author and reference code in hand.

**Planning** is consistent: the work is carried by **existing** `crates/evaluator/src/policy.rs`
(portable glob predicate) and `crates/host/src/repair.rs` (retained program/Coverage selection); no
new package or planned filename; 198 paths / 20 packages / 320 mappings / M0–M6 / 54 planned
recovery cases, 0 executed. `implementation-normative-inputs.v3` binds **29** inputs that all resolve
against frozen32, with layer2 and the original layer1 preserved. All five pin ledgers carry both new
owners — and layer3 contains the glob **contract** but **zero `.py` files at all**, so the reference
module is correctly pin-only and not a normative input.

**Suites I ran** (each justified by changed inputs, not repeated for its own sake): six
changed-input checkers all exit 0, including `check-workflow-projection.v3.py` (92.5 s) and
`check_workflows.v1.py` (1803/1803); the pinned evaluator3 launcher with **1,244 pins valid, 0
changed or missing, 16/16 children**; and both planning groups (198 unique paths; 320 mappings, 54
planned cases). Root's six suite results were treated as evidence to assess — my conclusions rest on
my own execution.

**Package 8**: 277/277 verified, `verify-package.py` rc=0 over 12,898 source files, and my own decoder
replayed all 13 through **both** boundaries — 7 positives ADMIT/ADMIT, 3 controls ADMIT then REFUSE
`EVALUATOR_COMPLETE_PROOF_REPLAY`, invalid-default ADMIT then REFUSE
`ENUMERATION_BINDING_PROGRAM_ENTRY` — plus the 7 automatic query checks. Exports were originally built
on source30 and preserved through 31/32; **I did not re-run the from-scratch construction and do not
relabel those historical commands as source32 work**.

## 4. Corrections to my own source31 record

All five root findings are correct — I verified each against my actual v31 `review.json` before
accepting it — and I add one of my own. The source31 report is left unchanged.

- **RR31-01** — all 16 `DR-011-R01..R16` rows had `currentOwnerFiles=[]` while RR27-03 claimed every
  row names actual paths. **Confirmed (16/16 empty).** Every one now carries real current owner paths
  resolved against frozen32, with changed/unchanged accounting from my delta.
- **RR31-02** — `RES-EP13-13`'s standing said "byte-equal" while the row noted the file had changed.
  **Confirmed.** That row now separates the **unchanged normative law** (fixture isolation, no
  sandboxing claim) from the **changed file** (last changed 27→28 for the ruleResults work, and not in
  my 31→32 delta), and no generic inherited label is applied to newly attached historical artifacts.
- **RR31-03** — A-7 said the native schema file was not in the 27→31 delta; **it was**. Corrected: the
  **pointer** is what is unchanged, and its v2 definitions are byte-identical to v3. No source defect
  was demonstrated and I select no cosmetic repoint or digest churn.
- **RR31-04** — A-8's evidence is now supplied and **I inspected it**: the source29 and source30
  `native-cases.v2.json` have the same byte count and differ in **exactly one leaf**,
  `$/fixtures/coverageView/schemaDigests/0`, `673a9bf8…` → `3e37c7b7…`, both 64-hex, both bound by the
  bundled manifests; and the failed source29 receipt is preserved **as a failure** (`passed: false`
  with `sourcePinsValid: true`, `checksExecuted: true`). This is **new custody supplied to me now, not
  retro-authentication** of the original transition. A-8 was an honest reviewer-input limit and is
  discharged.
- **RR31-05** — my report said the enumeration join precedes structural custody. **Wrong, and proven
  so by execution**: tracing a real fixture replay gives `open_run_closure → derive →
  admit_enumeration → compare_complete_replay`. Structural custody runs **first**. Root's further
  point is also right: a structural-ADMIT-then-semantic-REFUSE construction is therefore not
  inherently impossible, so I do not claim it is, and the join-only controls remain adequate for
  their claimed scope — I demand no whole-Run replacements.
- **Wording limit** — accepted: finite hash controls show distinct identities for finitely changed
  inputs, never global SHA-256 injectivity.
- **RR31-07, mine** — my bounded review's remedy-ambiguity demonstration used pseudo IDs with an
  unequal source/target universe on a `same-only` file relation, so those two rows would not both be
  lawfully admitted records. **That construction did not demonstrate two lawfully admitted records.**
  What survives is the structural finding root accepted — the old remedy could not name the actual
  retained record — and source32 fixes exactly that.

## 5. Residuals and TCB-SCOPE-01

All 30 rows bind cleanly to frozen32: ids identical, **0** unresolved evidence paths, **0** sha
mismatches, **0** cited evidence files changed in this window, all `PENDING`, none applied. The
proposal itself is unchanged 31→32 and all 30 remain **author proposals, not grades**.

**TCB-SCOPE-01 is assessed once**, with **13** dependent rows. As design it is coherent, disclosed and
consistently applied, and stated explicitly rather than left implicit. I do not grade it. **Rejecting
or changing this one assumption reopens all thirteen accounts together — never thirteen independent
successes — and would neither repair the historical attacks nor establish containment.**

## 6. Advisories (no MUST, no SHOULD)

- **A-9** — the repair selection law is reference-level only; no product surface emits it, and the
  only projection is a synthetic adapter the source itself labels as gate integration. Not a SHOULD:
  this is the expected state of a design-and-reference layer, the source says so rather than
  overstating it, and demanding a product implementation would make implementation a design
  acceptance prerequisite.
- **A-10** — two-binding and combinator coverage remain unexercised in the author package. Not a
  SHOULD: carried unchanged from source31 where I already assessed it as an evidence limit rather
  than a demonstrated owner defect, and nothing in this delta changes it.

## 7. Standing

Every F, evaluation-residual, AR, FW, inherited and scoped-owner row carries
`appliedByThisReview=false` and `finalApplicationOutcomeGranted=false`. **All 28** condition-2
obligations retained; **all 32** qualification gates unperformed and **condition 5 NOT MET**; **all
54** recovery cases unexecuted. **DR-007 / DR-011-R08**: the published D9 successor carrying
host-invariant remains an **assigned implementation obligation**. The original blind 123/8/3
reconstruction is a separate requirement — I read no consumer runtime, output or report. Final
application review and activation are separate.

---

*All 107 dispositions with current owner paths, evidence and limits are in `review.json`; probe
sources are in `probes/` and receipts in `receipts/`. Six probes failed on my own errors and are
preserved and labelled: a syntax error in my own comprehension; a definition-vs-call-site comparison
plus a behaviour-altering monkey patch; an incomplete fixture construction that refused
`EVALUATOR_COMPLETE_PROOF_REPLAY`; a duplicated keyword argument; a fixture option called without its
required guard arguments; and an out-of-enum synthetic that made one order test inconclusive rather
than negative.*
