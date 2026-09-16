# Blind20 disagreement diagnosis — consumer20 ACCEPT-RECONSTRUCTABLE vs frozen33 REFUSE

**Standing.** READ-ONLY diagnosis by the actual Claude **source-author origin**
`823bf66b-e92a-4789-ab81-63a1a9dc371d`. I am **not** the independent reviewer and **not** the blind
consumer. **No acceptance** of the design, of consumer20, or of the final application is given or
implied. Nothing outside this runtime was written. The consumer Run was never reminted and no
consumer code was executed. I did not open independent33 or its reconciliation runtime, and did not
contact or modify the blind origin.

I did **not** assume either model correct because it labels itself PASS. Each discrepancy is
classified against a named published selector, and where the published text does not settle it I
say so.

---

## 0. Byte custody

| | |
|---|---|
| Manifest | `reviews/candidate-subject.v33.json` SHA `1cf3db70d4b73b0c42f1393331e6a874ee26f7ddf67aa05c6ac15a5753069299` — **matches** the declared value |
| Tree | **12 899 / 12 899 manifest rows verified byte-exact**, 736 764 309 bytes, 0 mismatched, 0 missing |
| Untracked | one `foundation/__pycache__/canonical.cpython-**314**.pyc`. Not a manifest row. My interpreter is 3.12.13 run with `-B`, which writes no bytecode, so it is not mine. |

Consumer exports (root's captures, re-hashed here): `syntax-code 01415c13…`, `typescript
98aaa233…`, `rust 133d0f38…`, `rust-partial 223cda4d…`, `syntax-data 59662816…`. All other input
hashes are in `diagnosis.json → inputHashes`.

**Missing evidence, flagged:** `consumer-b.v20/final-public-artifact-manifest.json`, named in my
task as the exact public retention, **does not exist at that path**. I read
`consumer-b.v20/output/**` directly and hashed every file I used. I treated no substitute as an
authoritative manifest.

## 1. Where the disagreement now lives, and what it hides

Transport and structural admission are **ADMIT on all five**. `executionDeficiencies`,
`evaluationInputRefs` and `executionInputsDigest` are **equal on all five** — the execution-inputs
and host-account layer that dominated blind19 is now clean. Predicate-proof **counts** agree on all
five (6/6, 18/18, 19/19, 7/7, 12/12), so subject enumeration and predicate structure agree too.

**First refusal:** `EVALUATOR_COMPLETE_PROOF_REPLAY`, raised by
`evaluator_composition_model.v3.py compare_complete_replay`, called at
`evaluator_replay_model.v3.py:59`.

**What it masks.** That call precedes the `proofBundleId` identity check (`:60`),
`EVALUATOR_EVIDENCE_REPLAY` (`:66`), `EVALUATOR_SEAL_REPLAY` (`:71`) and `EVALUATOR_RUN_REPLAY`
(`:75`). Those four joins are **unestablished for all five Runs** — neither confirmed nor refuted.
No one should read this diagnosis as saying they hold.

## 2. Method, and one correction to how the differences should be counted

Root's `root-blind20-proof-differences33.v1/diagnose.py` is sound: exact consumer bytes → transport
decode → `open_run_closure` → `R.derive` using the **consumer's own** `evaluationInputRefs` →
structural diff. No remint. I re-ran that derivation to recover what a path-level diff cannot show:
witness **preimages**, coverage payloads, atom inputs and enumeration bindings.

**Index-aligned diffs over canonical sets overstate the disagreement.** rust-partial's reported 36
deficiency field differences are, at set level, **one substitution of 4 records** plus re-sorting —
8 of its 12 members are shared verbatim. I compare at set level wherever the field is a `Cset`.

**The 33 `witnessDigest` differences reduce to two fields.** Comparing preimages,
`coverageIds` and `deficiencies` are the *only* witness fields that ever differ.
`programPredicateDigest`, `matchingFactIds`, `uncertainFactIds`, `matchingImportRows`,
`uncertainImportRows`, `countLimit`, `childPredicateIds`, `kind` and `schemaVersion` always agree.

## 3. Root causes

### RC-1 — the sufficiency view omits the published recursive `DEPENDS_ON` — *consumer violated explicit law*

syntax-data, atom `{op:none, relation:clones, minResolution:normalized-body-hash}`:

* consumer cites **1** partition: `coverage2:1298b6be…` (relation `clones`)
* reference cites **2**: that one **plus** `coverage2:e007ce53…` (relation **`declares@syntactic`**,
  `coverage: unknown`, `language-tier-unsupported`/`capability-missing`)
* consumer causes `{language-tier-unsupported}`; reference `{coverage-unknown,
  language-tier-unsupported}`

**Published law:** `foundation/atom-evaluation-contract.v1.md` line 88 — *"`sufficiency_v2` view
includes **actual** recursive native `DEPENDS_ON` (reachability→`calls@resolved-callee`;
**clones→`declares@syntactic`**) of the same (S, T) … Unrelated S→V coverage cannot heal a missing
S→U dependency. All `su.causes` are retained."* The registry is
`native/native_evidence_model.v2.py:670-671`; the reference path is
`atom_model.v1._build_sufficiency_view` → `_depends_chain` → `run_suff`, which emits
`coverage-unknown` at `:1463` when the view is unsatisfied.

Consequence: the consumer's syntax-data deficiency set is a **strict subset** (12 of 24). It loses
disclosure; it does not over-disclose. **No source change.**

### RC-2 — outgoing scope pairing finds nothing where the reference finds a scope — *consumer deviation*

19 spurious `uncovered-expected-source-subject` records across four Runs, where the reference finds
containing scopes and proceeds (syntax-code `rule.no-duplicate-body`: consumer 2, reference **0**).

**Published law:** line 74 — *"Outgoing: only scopes/coverages at exact rung whose associated scope
**contains the current source subject**. Pairing is native `subject_scope_commitment` of the actual
subject-scope2 descriptor … **or** explicit owner-derived `coverageScopes` mapping. **No
one-scope/one-coverage fallback.**"* Reference: `_coverages_for_current_source`; empty → `:1479`.

**The consumer had every input.** In all three Runs checked, every scope descriptor the atom inputs
reference is present in the **consumer's own export**, the `coverageScopes` mapping is present and
full-size (5/5, 5/5, 6/6), and commitments compute without error. *Probe limitation:* my own
commitment-recomputation column returned 0 matches because I serialised
`subject_scope_commitment`'s return shape wrongly — that column is an artifact and proves nothing;
RC-2 rests on the other columns. **No source change.**

### RC-3 — binding availability — *consumer deviation, factually settled*

Consumer emits `missing-relation-coverage` + `required-relation-missing` where the reference emits
`selector-unbound`. The reference reserves `missing-relation-coverage` for **no bindings at all**
(`:1437`) and `selector-unbound` for bindings that exclude the subject's universe (`:1472`).

**Settled on the consumer's own retained plan:** `syntax-code`/`unresolved-edge` → capability
`unresolved-edge`, **1 binding** (unavailable, universe null); `rust`/`clones` → `clones-fact`, **2
available**; `typescript` → **1 available**. Bindings exist in every case, so
`missing-relation-coverage` is factually wrong regardless of any publication question.

*Narrow clarity observation (not the cause):* the outgoing predicate is published explicitly only
for the **incoming** direction (line 76) and implied for outgoing (line 74). Root may wish to state
it for outgoing. **No source change is required by this disagreement.**

### RC-4 — composite `scopeIds` are not the union of children — *consumer violated explicit law*

typescript, 6 composite nodes (`and`/`not`): consumer scopeIds **empty on all 6**; the reference's
value equals **the union of the consumer's own children's scopeIds on all 6**. The two sides agree
on every leaf; only the propagation is absent.

**Published law:** `evaluator-composition-contract.v3.md` line 121 — *"`scopeIds` on
**predicateProof** … Boolean: `Cset` of **union of children's `scopeIds`**"*. Reference:
`evaluator_composition_model.v3.py:135`. **No source change.**

### RC-5 — rust `count-at-most`: 4 findings suppressed — *downstream of RC-2/RC-3*

Consumer 3 findings, reference 7; `rule.c-at-most-one-body` goes 0 findings/14 deficiencies
(consumer) vs 4 findings/5 deficiencies (reference). Four `count-at-most` predicates are
`indeterminate` for the consumer and `true` for the reference.

**Every value difference coincides with a witness difference**, and the consumer's extra blocking
causes force `UNK` at `atom_model.v1.py:1619`. Four other `count-at-most` predicates are
indeterminate on **both** sides, so the consumer is not uniformly wrong about the operator.

This is the only family where the consumer's output is materially weaker than disclosure loss — it
**suppresses findings**. *Uncertainty:* the linkage is established by coincidence of witness
differences, not by counterfactual execution; repairing RC-2/RC-3 should be **re-measured**, not
assumed to fix it.

### RC-6 — `matchingImportCount` under-reported — *independent consumer deviation*

typescript: 4 findings on each side, but 2 differ. The **only** differing field is
`parameters.matchingImportCount` — consumer **0**, reference **1**. Subject, `messageCode`,
severity and citations all agree, and both sides emit the finding, so the import atom was true on
both. An atom true on an observed hit cannot have zero matching import rows.
(`evaluator-composition-contract.v3.md` line 119; `evaluator_composition_model.v3.py:172`.)
Not downstream of RC-1..RC-5. **No source change.**

## 4. Surface claims

### S-1 — protocol capability tokens: the blind19 finding **persists in final20** — *consumer violated explicit law*

Root's control ran on consumer**19**. My task says not to infer it carries over, so I repeated it on
final20's own bytes.

`consumer-b.v20/output/lib/phase3_traces.py` (`c64bf986…`) line 131:
`HELLO_ACK_FULL = {'capabilities': ['snapshot2','plan2','fact2','coverage2','scope2','view2']}`.
No owning-token literal appears anywhere in the file. The owning four —
`source-identity-snapshot2`, `plan-identity-plan2`, `fact-identity-fact2`, `coverage-v3` — are
published in `docs/v2/contracts/product-v1/native-evidence.md` lines 2607-2615.

Running the **frozen** `native_evidence_model.v2.protocol3_run` on final20's own event literals:

| | finalPhase | terminalKind | identityNegotiated | sourceBytesSent | stagesCompleted |
|---|---|---|---|---|---|
| as final20 wrote it | **FAULT** | null | false | false | 0 |
| owning tokens only changed | DONE | complete | true | true | 1 |
| final20's own claim | DONE | complete | true | true | 1 |

First rule-trace divergence at **index 2**: reference `P3-34`, consumer `P3-03`. The frame sequence
matches final20's own claim, and the token list is the only thing changed in the control.

**Masking:** the FAULT lands at `OpenUniverse` **with no source disclosure**; every later phase is
`FAULT-absorb`, so final20's DONE/complete/stagesCompleted claim and all later frame semantics are
**unestablished**. **No source change** — changing only the token list completes the trace.

### S-2 — mutation replay-scope ids — *violated in the old vector; corrected in the new probe; the two retained artifacts disagree*

Published: `RequestId` `^req1_[0-9a-f]{32}`, `StepId` **integer** 0-63.

| artifact | entry | requestId / stepId | `MutationReplayScopeV1` |
|---|---|---|---|
| `vectors/mutation-keys.json` | genericMutation | `req-7f3a1c` / `step-2` | **REFUSE** |
| `vectors/mutation-keys.json` | importStep | `req-7f3a1c` / `step-2` | **REFUSE** |
| `vectors/mutation-keys.json` | nativePreparationStep | `req-7f3a1c` / `step-2` | **REFUSE** |
| `vectors/indep-mutation-surface.json` | mutationReplayScope | `req1_7b31d0c4…` / `2` | **ADMIT** |

The fair characterisation is narrower than "still `req-7f3a1c`": the consumer **did** correct the
surface in its new probe, but left the old vector (and `repair-descriptor.json`) in the final public
retention. Both are retained and they publish **different** generic mutation-intent keys —
`20cbbcc1…` (old, inadmissible preimage) vs `f0ccf0a6…` (new, admissible). Only the newer rests on
a preimage the owning schema can admit. **No source change.**

### S-3 — multistep availability / aggregate termination — *undischarged, not a defect on either side*

`phase7-standing-rules.json` carries a **single-step** availability rule
(`hasMultistepAvailability: false`), and **no** retained artifact contains an `aggregateTermination`
record. I can neither confirm nor refute a multistep availability or indeterminate-aggregation claim
from the retained bytes. This is an evidence gap, not a demonstrated error.

### S-4 — envelope schema results are shape only — *scope statement*

Root's 20 records / 18 ADMIT / 2 expected REFUSE establishes **shape** against the frozen owning
schema. It does not establish response/projection joins, host conformance, or that any envelope is
answerable by an admitted Run. **Count checks and fragment-only laws do not discharge the charter**;
the whole charter (123+8+3) remains required.

### S-5 — complete query execution — *blocked*

Query execution through the public reference needs an admitted Run. All five consumer Runs refuse
semantic replay, so the query surface cannot be exercised on consumer20's own evidence. I did not
remint their Run; a reminted Run would not be their acceptance. **No claim either way.**

## 5. Does frozen source33 need a design change?

**No design change is demonstrated as required by anything in this diagnosis.** Every substantive
discrepancy resolves to a consumer deviation from a published law with a named selector (RC-1 line
88; RC-4 line 121; RC-2 line 74; S-1 native-evidence 2607-2615; S-2 common/invocation-record
schemas), or is downstream of one (RC-5), or is an undischarged evidence area (S-3, S-5).

One **clarity** candidate, explicitly not a defect and not the cause of any disagreement here:
`atom-evaluation-contract.v1.md` could state the `selector-unbound` vs `missing-relation-coverage`
predicate for the **outgoing** direction as explicitly as line 76 states owed programs for incoming.
RC-3 is already settled on the consumer's own retained plan without it.

**I make no blanket stage-count or suite-count conformance claim.**

## 6. Limitations and missing evidence

1. **I am the source-author origin.** Diagnosis only; no acceptance of anything.
2. **I did not read consumer20's atom or composition implementation.** Every consumer
   classification is established from **outputs** against published law, not from its code. Where
   that leaves the causing line unidentified, each root cause says so.
3. **Four replay joins are unestablished** for all five Runs (§1).
4. **No remint, no consumer execution.** Query execution stays blocked.
5. **The charter was not read in full.** I assessed the five proof disagreements and the surface
   claims named in my task. No full-charter claim is made.
6. **Root's blind19 controls are diagnosis, not authority.** I re-measured the protocol-token claim
   on final20's own bytes (S-1) rather than inheriting it. I did **not** independently re-measure
   `surface-parity`, `termination-joins`, `mutation-fields` or `query-record-assessment`; those
   remain **unconfirmed for final20** and should not be assumed to hold.
7. **`consumer-b.v20/final-public-artifact-manifest.json` does not exist** at the path my task
   named. I used `output/**` directly and hashed everything I read.
8. **My p8 commitment column is a probe artifact** and supports nothing (see RC-2).
9. Three receipts exit non-zero (`p3`, `p5`, `p8`) — probe coding errors, corrected and re-run under
   `b` labels. Both runs are retained.
