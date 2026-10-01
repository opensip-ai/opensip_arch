Grok re-review: law X3b r3 after Grok's r2 findings. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-journal-x3b-r3. Law review; no product cargo.

Subject: docs/implementation/m2/journal-x3b/PROPOSAL.md r3 (pin in hashes.txt). `diff` it against PROPOSAL-r2.md. Earlier findings are in `reviews/grok-journal-x3b-r1/` and `-r2/`.

## Changes

- **RF-1.** A new step 3 classifies by format before any floor decision:
  - a complete format-1 or format-2 carrier always takes F46;
  - a format-3 footprint that is not a lawful prefix takes `MIGRATION.CORRUPT`;
  - the digest must equal `SHA-256(N)`, or it takes the binding row.

  `floorLost` applies only to a complete format-3 carrier, or to a witness without its floor.
- **RF-2.** The step 4 table is rewritten:
  - the no-carrier quarantine is qualified;
  - `reconcile_witness` is a read-only decision, and any quarantine leaves the floor untouched;
  - INIT requires floor generation 1 at `lastSeq 0`;
  - the floor is compared and copied forward only after OK, REVERT or ADVANCE;
  - the full INIT `CarrierFloor` is spelled out.

  The crash list gains the format-1/2 row and the qualified `floorLost`.

## Decide

Are RF-1 and RF-2 closed? Is the state table now complete and consistent with the crash list? Is anything new wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
