# PA-1 addendum: the analysis-envelope producers are a deferred edge of J3d-TS

2026-11-12. Written by the lead (Claude Fable 5.2, route R3) under owner decision OD-TS1-RUN-1, decision 4
(`docs/implementation/OD-TS1-RUN-1.md`). Status: **PROPOSED, r2.** r2 applies the cross-vendor review
(`LC/j3d-ts/review-codex-delivery/VERDICT.md`, RF-1 and point 2): A2 is now an explicit, reviewed staging exception
to R-TS1.3 for this one deferred edge, not a claim of compliance with it; A4 claims a derived projection only from a
successful derivation that matched the reference. It needs the cross-vendor review that reviews
J3D-DELIVERY (`README.md` in this directory), then adoption by the lead. It edits no byte of the
adopted plan amendment PA-1 (`PLAN-AMENDMENT-TS1-r3.md`, sha256
`ff2d9569639b1279a11510a1a380c884041b71f9dfae4fa7bcb67beeda21297e`) and no contract, schema, registry or lock; it adds
one deferred edge (A1) and one named exception to R-TS1.3 (A2).

Short names: PA1 = the adopted amendment; MJ = the host pipeline law (`host-pipeline-j/PROPOSAL.md`, r7); WS and CINV
as J3D-DELIVERY's short names; D1, D3 = J3D-DELIVERY's clauses.

## Why it is needed

J3D-DELIVERY D3 establishes from the texts that a lawful `kind: run` envelope needs four total projections
(`findings`, `required-coverage`, `capability-availability`, and `comparison-counts` for the durable `analyze`
command) and that none has a producer in the product. PA1 §1.5 gives J3d-TS "the durable pipeline R0 to settlement,
read back from storage", and R-TS1.1 says of a staged unit's scope "Nothing else is removed" beyond the deferred edges
PA1 names. PA1 §1.7 names none for delivery. Without this addendum a J3d-TS that ends its Run without a delivered
envelope would be dropping accepted scope silently. The owner decided (OD-TS1-RUN-1, decision 4) that the milestone
Run may end that way and that the producers are the immediate follow-up.

## What is added

**A1. One more deferred edge for J3d-TS (adds to PA1 §1.5 and the J3d-TS row of §1.7).**

| Staged unit | Deferred edge added | Where it lands |
|---|---|---|
| J3d-TS | the producers of the analysis envelope's required members: `findings` (the finding-surface projection), `required-coverage` (per rule and Run level), `capability-availability`, and `comparison-counts` for `analyze`; with them, delivery of a `kind: run` envelope for a committed Run | a named follow-up sub-unit, **J3d-ENV**, started immediately after the M3-M-TS1 record; in any case no later than J3d-RS, which may not complete without it |

J3d-TS keeps everything else PA1 §1.5 gives it: the pipeline R0 to settlement, the commit, the read-back by execution
id, and the derivation of the outcome projection inside `finalize` (D1).

**A2. How a TS1 Run ends meanwhile: a staging exception to R-TS1.3 for this deferred edge only.** R-TS1.3 requires
an input whose processing needs a deferred edge to be "refused before any effect that could be read as its analysis"
(PA1:67-70). The Run A1 keeps is such an effect: its analysis commit is durable, and the absence of an envelope does
not undo it. This addendum therefore **supersedes R-TS1.3 for the delivery-producer deferral named in A1 and for
nothing else**, under OD-TS1-RUN-1 decision 4 ("Such a Run ends on the delivery-failure row with its run id"): the
Run commits, and then a committed Run whose envelope cannot be projected ends on MJ's outcome row 43: operational-failed, exit 4,
`DELIVERY.REQUIRED_FAILED` with detail `DELIVERY.RENDERER_FAILED_AFTER_COMMIT`, carrying the runId (MJ:815;
WS:1128-1134: "A missing field or projection exception is a required-delivery operational fault … If a Run was
already committed, the termination retains its RunId and the after-commit detail"). No `run` member is emitted and
nothing is manufactured in its place. A phase-D signal on such a Run also ends on row 43 with the runId, not on row
47 (D3). For every other deferred edge of J3d-TS and of every other TS1 sub-unit, R-TS1.3 stands unchanged: refusal
before any effect that could be read as analysis, with a code accepted law already has. The exception uses WS's
existing row (WS:1130-1138); no new code, cause, row or successor is added (R-TS1.6). OD-TS1-RUN-1 does not by itself
supersede R-TS1.3; this exception takes effect only on the lead's adoption of this addendum after its review.

**A3. Disclosure (R-TS1.4).** Every J3d-TS record and the M3-M-TS1 record carry, in the deferred list of the
R-TS1.4 line, `analysis-envelope producers (findings, required-coverage, capability-availability,
comparison-counts); kind: run delivery`. The M3-M-TS1 record states in its own text that the Run ended exit 4
`DELIVERY.REQUIRED_FAILED` with its runId and that this is the staged limit, not a product fault found by the Run.

**A4. What the M3-M-TS1 record may claim (narrows PA1 §1.6's "a J3d-TS Run … read back").** The commit; the
read-back by execution id; the outcome projection derived by the product and checked by the harness against the
reference. The last claim needs an actual successful derivation (D1's carried value is `Ok(Derived)`) whose
comparison with the reference matched: a committed Run whose derivation was refused (`Err(Refusal)`) still ends on
row 43 under A2, but it cannot satisfy that claim and is not a Run the M3-M-TS1 record may be made from
(OD-TS1-RUN-1 decision 4 requires the projection derived). It may not claim a delivered envelope, a verdict shown to
a user, or any parity field.

## What is not decided here

- The open owner points of J3D-DELIVERY (the deficiency pair of a pass or fail Run and the Run-level
  required-coverage rule; an owning text for `comparison-counts`; the reading of `run.authority`; where synthetic
  Runs are refused on authoritative surfaces). They belong to J3d-ENV and are put to the owner with it.
- J3D-DELIVERY's O5 (a refused projection is reported with a renderer-failure detail). A2 uses the existing detail
  under the reading recorded there.
- J3d-ENV's scope, size and controls: its own unit plan.

## Control for this addendum

PA-E1: J3d-TS's unit plan and its review requests cite A2's row and carry A3's line; a J3d-TS test shows a committed
Run ending on row 43 with its runId and no `run` member (J3D-DELIVERY's C7 control). J3d-RS's plan lists J3d-ENV as a
predecessor.
