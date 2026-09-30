Grok review: law 458c r6, an amendment after r5 acceptance. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-read-premise458c-r6. Law review; no product cargo. Product HEAD is 417d443.

Subject: docs/implementation/m2/read-premise-458c/PROPOSAL.md r6 (pin in hashes.txt). `diff` it against PROPOSAL-r5.md.

## Why

Starting 458c-c found two problems:
- The product has no doctor report assembler: nothing builds `DoctorResult`, only the generated `Invocation5DoctorResult` exists.
- There is no existing doctor defect classification for the session's structural findings (`IncompleteRefusal::{Missing(Entry), Pair, Marker, Store, Node, Chain}`). The only doctor rows are `DOCTOR.DEFECTS_FOUND`, `DOCTOR.REPORT_NOT_PRODUCIBLE` and `INSTALLATION.DURABILITY_NOT_CHECKED`. `doctor-cases.json` uses stand-in codes.

Item 12 said "under the existing doctor defect classifications", which do not exist, and the owner allows no new code.

## Changes

- **Item 12.** Each structural finding is one actual defect entry with the existing detail `CONFIG.CUSTODY_REFUSED`, the same detail as 468's incomplete row, and a finding subject:
  - `installation-incomplete:missing:<path>`;
  - `:pair`, `:marker`, `:store`, `:node` and `:chain`.

  Each has a fixed remedy per kind, reviewed with 458c-c. `subject` is the existing optional `BoundedText` of `DomainDetail`, so there is no schema, registry or code change.
- **Item 10.** 458c-c builds the first doctor report assembler as a library, following owner §5 and the reference `DoctorSession.assemble`, and is tested against `doctor-cases.json`. The CLI human label is not claimed.

## Decide

- Is the per-finding subject on `CONFIG.CUSTODY_REFUSED` a faithful existing-vocabulary classification, under owner §5 ("actual structural defects", "preserving all existing defect classifications", no new code) and 468 item 6?
- Is building the assembler in 458c-c in scope?
- Is anything else wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
