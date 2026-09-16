# Independent design review — consolidated product **source32** (complete successor record)

Same reviewer origin `ce3dec3b-0620-44ec-86e6-129b0e25cb1b`. This is a **bounded review-record
reconciliation on UNCHANGED frozen source32** — not a new source version, not a fresh origin, and
not a patch. It is a complete successor record. My source32 report is **preserved unchanged** at
`claude-independent-design.v32/` (sha `90abddbb…e044fe`, which matches the digest root quoted).

**Verdict: ACCEPT — unchanged.** Manifest `3897e8d1…0bf2`. Zero new MUST, zero new SHOULD, two
advisories. **No new normative source defect was demonstrated by root, and none by me.** All four
record defects are citation, wording and bookkeeping errors in my own report; **no disposition
changed and no obligation moved.**

Design review only: no application grade, activation, blind acceptance or implementation
authorization. No source edits, no repository changes, no commit or push.

---

## 1. RR32-01 … RR32-04, independently assessed

I recomputed everything myself rather than accepting root's audit — which matters, because root
discloses that its own v1 mechanical audit misread `currentOwnerSelectors` and emitted 30 false
missing-owner findings before a v2 corrected the field access. I never saw those findings and
neither adopt nor dispute them; my conclusions come from my own measurement against frozen32
membership.

**All four are substantiated. I agree with each.**

### RR32-01 — DR-007 cited a file that does not exist ✅ confirmed

My row cited `foundation/evaluator-fault-contract.v1.md`. Measured: that path is **absent** from
frozen32, and the only such file present is **`evaluator-fault-contract.v3.md`**. Across all 107
rows this was the *only* owner path absent from the snapshot.

I read the actual owner freshly this pass (8,678 bytes, sha `5731b41d…`, manifest-verified). It
publishes the closed condition/public-meaning table, states that an internal refusal is not itself a
public D9 code and that origin is never inferred from a filename or error text, and names the **24**
allowed condition/origin pairs. Decisively for this row, it says in its own words:

> "the mandatory LIVE D9 successor-artifact obligation is not discharged by this design reference or
> by a passing route-control suite."

So **the disposition was already right** — the D9 successor remains an assigned implementation
obligation. This was a citation defect, not a wrong judgement. Corrected in DR-007 and DR-011-R08.

### RR32-02 — one surviving inverse-ordering clause ✅ confirmed

`F-04.limits` still read "a boundary that **precedes** structural custody" — the exact inverse my own
RR31-05 correction had already retired elsewhere in the same document. Scanning every precedence
sentence found two: this stale one, and the RR31-05 entry stating the corrected order. Now fixed to
state the traced order — `open_run_closure → derive → admit_enumeration → compare_complete_replay` —
and to repeat that join-only controls remain adequate, with **no whole-Run controls demanded**.

### RR32-03 — an asserted reading session that never existed ✅ confirmed

`RES-EP13-13` said the changed file "was read fresh in **that session**", meaning the 27→28 window.
**My lineage contains no source28 review**: source26, source27, source31, source32, plus a bounded
prospective-bytes review. The truthful history, taken from the original receipts:

- the FILE last changed in the 27→28 window;
- I first reviewed and executed the post-28 bytes in my **source31** review, which assessed the whole
  27→31 delta including the source28 ordering work — `claude-independent-design.v31/receipts/p06-replayorder.json`, frozen run rc=0;
- I executed them again as a changed-input run in **source32** — `claude-independent-design.v32/receipts/p06-changedchecks.json`, rc=0;
- **in this pass I freshly READ the current bytes** (17,179 bytes, sha `8405862f…`, manifest-verified)
  and confirmed the deep-copy fixture isolation the row disposes is present throughout. I did not
  re-execute it here and claim no new execution.

### RR32-04 — four false booleans, and a worse problem underneath ✅ confirmed

`DR-011-R02/R04/R05/R08` reported `ownerPathsResolveInFrozen32=false` while every path they *stored*
resolved. I found the cause in my own v32 build code: it **stored the filtered list but computed the
boolean against the unfiltered one**. So a nonexistent path was *silently dropped from the row* and
simultaneously made the boolean false.

That makes this the most substantive of the four — not merely a wrong flag but **four rows missing an
owner I intended to cite**:

| Row | Silently dropped | Actual owner, now restored |
|---|---|---|
| DR-011-R02 | `foundation/fact-identity-policy.v2.json` | `docs/coop/artifacts/fact-identity-policy.v2.json` |
| DR-011-R04 | `native/native-protocol.v3.md` | `native/protocol3-transitions.v1.json` |
| DR-011-R05 | `native/native-protocol.v3.md` | `native/protocol3-transitions.v1.json` |
| DR-011-R08 | `foundation/evaluator-fault-contract.v1.md` | `foundation/evaluator-fault-contract.v3.md` |

`native-protocol.v3.md` does not exist anywhere in frozen32; the real protocol owner is
`protocol3-transitions.v1.json`, and I verified it carries **`phases: 22`** and **`ruleCount: 34`
with 34 rules** — exactly the 22-phase state machine and 34-row transition table DR-011-R05
describes, with standing "NORMATIVE and CLOSED".

**Every owner-resolution boolean across all 107 rows is now derived from actual frozen32
membership.** Result: 107 rows checked, **0 unresolved owner paths**, all 16 DR-011-R booleans true
and matching measurement.

## 2. Bounded probe limits — accepted and applied in place

Root's two notes are accurate against my own receipts, and I have qualified both rather than leaving
the stronger reading standing:

- **p05** used hand-built rows with pseudo identities (`coverage2:aaa` / `coverage2:bbb`). It
  establishes that `record_coordinates()` emits **distinct string coordinates**; it does **not**
  establish two lawfully admitted native records. The ownership, unavailability, unselected-exclusion,
  extent-distinctness, absence-folding and gate results are likewise unit-level over constructed
  views. Full-Run weight belongs to the *source's own* asymmetric control, which I did not construct.
- **p12c** never admitted a real EnumerationPlan: its lookup failed with `KeyError: 'properties'` and
  it recorded `cellsOrderAnnotation: None`. What it showed is that the ExactValidator enforces
  `x-opensip-order {by:[…]}` on an **isolated** schema. My cellOrdinal conclusion is therefore a
  **bounded inference** from three parts — that generic behaviour, the static annotation I *did* read
  directly in p12, and enumeration-contract §8 naming the ExactValidator as the plan validator. Still
  **no finding**, but on inference rather than executed plan admission.

## 3. What is preserved

All **107** individual dispositions with the same row ids (14 F, 30 evaluation residual, 16 AR, 15
FW, 27 inherited, 5 scoped owner); the **ACCEPT** verdict; both advisories; every executed-evidence
citation at its **original** v31/v32 receipt location, never relabelled as work done here.

**TCB-SCOPE-01** assessed once with its **13** dependent rows and the joint-reopening consequence
intact: rejecting that one assumption reopens all thirteen together, never thirteen independent
successes. All **28** condition-2 obligations retained; **32** qualification gates unperformed and
**condition 5 NOT MET**; **54** recovery cases unexecuted; the D9 published successor remains an
**assigned** implementation obligation on DR-007 / DR-011-R08; all **30** residual proposals remain
author **PENDING**, not grades. Every row keeps `appliedByThisReview=false` and
`finalApplicationOutcomeGranted=false`. No consumer-b runtime, output or report was read.

Root's assent remains withheld pending an accurate record — which this successor supplies — plus the
separate blind and application prerequisites, which this pass does not touch.

## 4. Consistency check

35 structural and semantic checks over the complete successor record, **0 failures**: maps and row
ids preserved, verdict and manifest binding intact, all four corrections applied, every owner path
resolving, obligations and grants unchanged, superseded record byte-identical at its original
location.

Two checks failed on first run and were my checker's fault, not the record's: they flat-matched the
whole document and so flagged the **intentional quotations** inside `recordCorrection` and
`rootFinding` fields, which exist precisely to document what was wrong. Reclassified by JSON path
(`r05-locate.json`): **7 occurrences, all intentional, 0 genuine stale clauses.** Both probes are
preserved.

---

*The complete machine-readable record is `review.json` in this runtime, with
`correctionsToMyOwnV32Record` carrying evidence for each item. Receipts for this pass are in
`receipts/` (`r00`–`r05`); all inherited executed evidence is cited at its original v31/v32 location.*
