REVIEWER re-review, three laws: X5 r2, X6 r2, and the X2 r6 amendment. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/REVIEWDIR. Law review; no product cargo.

Pins are in hashes.txt. The r1 findings are in `reviews/grok-replay-join-x5-r1/` and `reviews/grok-carrier-recovery-x6-r1/`.

## X5 r2 (diff against `replay-join-x5/PROPOSAL-r1.md`)

`Input(MissingObject)` and `Input(MissingBlob)` take `HOST.IO_FAILURE` / `host-io` / `evidence.missing`, with the key or digest. Schema, identity and decode failures stay `EVALUATION.INPUT_REFUSED`. The match is exhaustive over `RetainedInputError`.

## X6 r2 (diff against `carrier-recovery-x6/PROPOSAL-r1.md`)

- **RF-1.** Item 3 cites X2 r6 for the fence-free `readers.lease`.
- **RF-2.** Item 8 gives both projections of `committed-availability-degraded`:
  - history is success;
  - a selected operation needing an unavailable object is operational-failed, `HOST.IO_FAILURE`, `host-io`, with `evidence.missing`, `corrupt`, `purged` or `expired`. It is never success.

## X2 r6 (diff against `project-root-x2/PROPOSAL-r5.md`, which equals the accepted r5)

Item 7 adds one exception (lead decision), citing identity §5 and owner §5:
- the read-only recovery selector takes `readers.lease` `LOCK_SH|LOCK_NB`, without the fence and without waiting;
- it never takes `writer.lease`, and the lease is never upgraded;
- nothing else takes a lease without the fence.

The forbidden-substitutes list names the exception. The rejected alternatives are taking the fence for recovery, and a general fence-free shared-read lease.

## Decide

Are the findings closed in each law? Is the X2 exception narrow and lawful? Is anything new wrong?

Write one REVIEW.md, and three verdict files: `x5/review.json`, `x6/review.json` and `x2/review.json`. Each must contain "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Do not commit.
