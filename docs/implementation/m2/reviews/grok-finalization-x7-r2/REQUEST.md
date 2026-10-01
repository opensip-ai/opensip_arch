Grok review: law X7 r2, finalization. It answers your X7 r1 RF-1 (the rolled-generation refusal row) and RF-2 (the rollover's admission, fence, lease and ledger). Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-finalization-x7-r2. Law review; no product cargo.

Subject: docs/implementation/m2/finalization-x7/PROPOSAL.md r2 (pin in hashes.txt). r1 bytes are preserved in PROPOSAL-r1.md (pinned too). Your r1 review is under docs/implementation/m2/reviews/grok-finalization-x7-r1.

What changed:
- **Item 6 (RF-2).** The rollover runs inside X3b r6 item 4's end step:
  - after `finish` releases the operation lease;
  - on this invocation's one gate admission, under the fence that end step holds;
  - with no `admit_ordinary_writer`, no second `DurableWriteGate` and no fence of finalization's own.

  Under that fence, X3b r7's rollover takes `EXCLUSIVE` (as `carrier-format.v3.md` §7 step 1 closes a generation). It then appends `TERMINAL` (`grantGenerationClosure`) through X3b item 5's one-append protocol and opens g+1. A busy namespace skips the rollover. The X3b r7 dependency is explicit, and X7a works without it.
- **Item 6a (RF-1, lead decision).** The attempt reports the existing busy row, `LEDGER.BUSY_TIMEOUT` / `ledger-busy` / `PROJECT.BUSY`, with S7's subject and remedy unchanged. The precedent is the §8.1 `unavailable-busy` row for a lawful migration prefix, and S12's read-only recovery busy row. The rejected alternatives are recorded.
- **Items 7, 10 and 11.** The rollover is charged to the existing gate ledger; the integration test expects that fence and that lease; and X7b's dependencies are corrected.
- **Other updates.** The item 3 table row and Forbidden substitutes are updated to match.

Context: the accepted laws X1 r1 (item 7), X2 r6, X3b r6, X3c r7, X3d r3, X4 r7; the drafts X5 and X6; the security contract's S7 and S12; `design-corrections/security/carrier-format.v3.md` §7 and §8.1; the build plan's F32 and its end-path paragraph.

## Decide

Do RF-1 and RF-2 close? Is the busy row a lawful fit for an exhausted or rolled generation under S12, with its subject and remedy unchanged? Does the rollover now respect one gate per process, the end step's fence, and the operation-lease append protocol? Is anything else wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
