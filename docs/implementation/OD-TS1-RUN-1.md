# OD-TS1-RUN-1: four decisions for the first TS1 Run

Status: accepted owner decision; effective 2026-11-12 UTC.
Scope: how the lead brings milestone M3-M-TS1 to its first Run. It changes no
product law. Where a design record or plan amendment must follow, that is said
below and remains subject to its own reviews.

## Owner instruction

The lead put four questions, each with a recommendation. The owner answered:

> yes to all 4, go with your recommendations

The four questions, as the lead put them:

1. "May I install Python 3.12 on the Mac? Without it, the outcome projection
   can't be checked against the design's goldens."
2. "Run constructs before body-parser? I recommend yes."
3. "May test-only batches integrate on a Claude review alone? I'm holding the
   flake fix for Codex meanwhile."
4. "What should the milestone Run deliver, given nothing produces the
   envelope's required members? I recommend the milestone without a delivered
   envelope, with the producers as the follow-up."

The details below are the lead's. They are not further quotations from the owner.

## What is decided

1. **Python 3.12.** The lead may install Python 3.12 on the owner's Mac
   (Homebrew `python@3.12`). Its purpose is the design-side reference builders
   that require Unicode data 15.0.0. Nothing else is installed under this
   decision.
2. **Fixture order.** The first TS1 Run is made on `ts-small-constructs`, then
   on `js-small-body-parser`. This reverses the order of LD-Q-25. The reason:
   body-parser is a JavaScript package that needs the synthesized-profile unit
   (JS-SYNTH-PROFILE-1), which is not yet written; constructs has a `tsconfig`
   and does not. The milestone still requires both fixtures.
3. **Test-only batches.** A batch that changes only tests, test fixtures, test
   scratch or the lane's own tooling, and no production code, may be integrated
   and pushed after one accepted independent Claude review and green lanes
   (macOS strict lane and Linux lane), without waiting for a Codex review. This
   is OD-REVIEW-1's same-vendor strategy applied to that class. It does not
   extend to production code, security-boundary code, signing, durable formats
   or qualification, which keep their existing review rules. Each such
   integration is reported to the owner with its basis. Codex may still review
   such a batch afterwards.
4. **What the milestone Run delivers.** The M3-M-TS1 record may be made from a
   Run that commits, is read back by its execution id, and has its outcome
   projection derived, while the analysis envelope is NOT delivered: the
   envelope's required members (`findings`, `required-coverage`,
   `capability-availability`, and `comparison-counts` for the durable `analyze`
   command) have no producer yet. Such a Run ends on the delivery-failure row
   with its run id. The record claims the commit, the read-back and the derived
   projection, and nothing about a delivered envelope. The envelope producers
   are the immediate follow-up after the milestone.

## What is still owed

- For decision 4, the TS1 plan amendment must name the envelope producers as a
  deferred edge of J3d-TS and carry that in its disclosure line; the design
  record J3D-DELIVERY (proposed, under review) states how a Run without a
  delivered envelope ends. Neither is adopted by this decision.
- The other points the J3D-DELIVERY record marks for the owner (the deficiency
  pair for pass and fail Runs and the Run-level required-coverage rule; the
  reading of the envelope's `run.authority`; where synthetic Runs are refused
  on authoritative surfaces) are not decided here. They concern the envelope
  producers and are put to the owner with that follow-up.

## What is not changed

- Signing: OD-SIGN-1c and OD-SIGN-RS1 stand.
- Pushing: the standing permission (push after each green, reviewed
  integration; report each push) stands, with decision 3 defining "reviewed"
  for test-only batches.
- Review of production code: unchanged.
