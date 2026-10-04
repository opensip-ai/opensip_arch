# S21 r1 — REQUIRED-FINDINGS

Design-unit review of the WS:226 / WSE:226 contract successor of law M3-J1 r5 (LD-r5-2). Reviewer: Grok. The review directory keeps the name `codex2-s21-r1` because the builder emits that path.

**Verdict:** REQUIRED-FINDINGS. One finding, RF-1. No non-blocking observations.

**Subject.** `docs/implementation/m3/host-pipeline-j/s21-subject.json`, 1422 bytes, sha256 `090de59ff7c4281f65d3f0ba2a63b9444d0583c820dc3f01a5c294d47eb72097`. Successor `docs/implementation/m3/host-pipeline-j/s21/successor.json`, 5538 bytes, sha256 `3e8ad15dec56bc8a1e4f8d63a6a47654f483d68ba26662f6118f0c76f11c7294`. The other five subject members match the manifest pins. Parents match WS `1ee203e3ce626d88a53d0247881cd3ffb0d52b421821ac798b9f0b57346ff6ed` (133335 bytes) and WSE `4478ce1a69369cd0b430fd5d3fc695e8372219629b05a08ae6642a845cab794d` (139497 bytes). Product base `218465f`, read only.

## Evidence

Under a private home, with hooks off:

- `build_s21.py --check` reported identical bytes.
- `check_s21.py --rev 218465f` passed 74 checks. The new text names only `DURABILITY.COMMIT_FAILED` and `DELIVERY.REQUIRED_FAILED`, fault causes `durability-commit` and `delivery-required`, and exits 4 and 130.
- `verify_scratch.py --rev 218465f` takes the lock from 91 to 92 contract successors, selects S21, keeps two overrides and no supersession, leaves inventory `repository-file-inventory.v135.json` and 100 inheritance rows, and refuses a later conflicting override of WS:226 (`conflicting contract passage overrides`).

## Rulings

**R1, exactness.** Each `before` is the parent line 226, and the two overrides are byte-identical. The `after` keeps the line's first word `` `cancelled` `` and its last words "a Run committed by an earlier". S18's WS:225 and WSE:225 end "remaining steps are". S18's WS:227, and the raw WSE:227, begin "step is named in the termination's `runId`." The before-settle sentence runs from S18's 225 through S21's 226 into that 227 on both parents.

**R2, the line-226 text against J1.** The override carries J1:868 and 8.3 rules 1 and 2 (J1:588-605): the aggregate stays `interrupted` (130) unless one of the two commit outcomes governs; each of those is operational-failed 4; the returned outcome is matched first. It adds no class, code, exit, or fault cause. Rules 3 and 4 stay on the interrupted branch that continues into S18's line 227. Open question 7 (J1:938) is the same exception. The sibling per-kind sentence is RF-1.

**R3, LD-3, accepted.** The scope is a required analysis or verify step's commit. IE:1680-1681 and SL:551-554 are commit-protocol rows. WS:82 lets analysis and verify steps seal or link a `run3`. WS:233-235 take the aggregate over required steps only, and an optional step's rejection or failure never changes the aggregate. The pre-existing tension between that optional-step sentence and IE:1680 stays cross-law item 5. "The attempt's ExecutionId" is the attempt whose commit was undetermined.

**R4, LD-4 and LD-5, accepted.** The returned outcome decides, never the gate's latch state alone (J1:588; X3D:170). A latch after admission followed by an undetermined evidence `COMMIT` is rule 1. Rule 1 names IE:96's `DURABILITY.COMMIT_FAILED`, X3D:283's row (operational-failed 4, `durability-commit`, ExecutionId, no RunId), WS:1360's fault cause, and IE:1680-1681's `durability-undetermined` disclosure. Rule 2 names SL:552-554 for state 3: the commit stays committed, the RunId stays observable, and required delivery is reported through `DELIVERY.REQUIRED_FAILED`, the selected law. S21's "latched after admission" is that state-3 row (J1 rule 2, X3D:170). The detail `DELIVERY.RENDERER_FAILED_AFTER_COMMIT` stays on X7:100, where F39 takes the F16 row and starts no delivery phase. WS:1376 is the golden for a renderer that failed after commit.

**R5, what is left.**

- WS:1393 stays. S18 binds it. The golden remains the ordinary SIGINT row, interrupted 130 / settled class. CINV `interrupted-before-settle` remedies an attempt that had not committed. Goldens for the two exception outcomes stay with the M4 CLI unit (cross-law item 3).
- WS:229 and WSE:233 must be overridden in this unit. See RF-1. LD-6 is rejected for those two lines.
- LD-7 is accepted. INV5's `Cancellation.phase` description still says a before-settle aggregate is interrupted (130). No M3 envelope carries the invocation record. The restatement stays with the invocation-record owner (cross-law item 2).

**R6, selection.** The record is well-formed under `verify_design`'s `contract_successor` and `successor_chain` rules at `218465f`, after S18, with no selector clash. Line 226 is unbound on both parents. S21 selects none of S18's lines. LD-1, LD-2, and LD-8 are accepted: one override on each free line 226, the same text on WSE, binding-only after S18.

## RF-1

Add a passage override of WS:229 and a passage override of WSE:233, with the same before and after:

```text
Per kind: an analysis attempt aborts and leaves no Run; an import discards its
```

```text
Per kind: an analysis attempt that the signal aborts leaves no Run; an import discards its
```

Leave WSE:229 with S18. The line still ends "an import discards its", so the next line's "staged bytes;" still joins. Regenerate the successor, the passages, the subject manifest, and the evidence that currently requires exactly the two line-226 overrides.
