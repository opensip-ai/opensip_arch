Grok review: law X9 r9, which answers your X9 r8 RF-1. Claude Opus 5.5 leads. You are the single reviewer.

**Rules:**
- No repository edits, commits, pushes or delegation.
- Write only under /tmp/opensip-implementation/reviews/grok-crash-matrix-x9-r9.
- This is a law review with no product cargo. Run git only read-only, against product `a2c5e8b`.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.

## What changed

Pins are in hashes.txt. `crash-matrix-x9/PROPOSAL-r8.md` holds the r8 bytes you reviewed: 93125 bytes, `44317b51…`. Diff PROPOSAL.md against it.

r8 was not accepted, so r9 corrects its text in place. There are only these changes:
- **Title:** r8 becomes r9.
- **r8 header note:** an r9 note is inserted after "r7 bytes are preserved in PROPOSAL-r7.md.". It names RF-1, the fix and the row.
- **The r8 header's X4T dependency sentence is replaced:**
  - `create.after` leaves the leaf empty, and `write.before` leaves it torn.
  - Either way the leaf sits before the pointer. The next fenced read doesn't name it (X4T r9 item 2). The next publication writes a determined, content-addressed list, and `write_dependency` creates a leaf only when it is absent, admits equal bytes and refuses unequal bytes.
  - So each census occurrence has exactly one R2:
    - if the next publication writes that name, R2 is `CONFIG.CUSTODY_REFUSED`, subject `installation-incomplete` (X4T r9 item 10);
    - if it doesn't, R2 is Committed.
- **How the per-occurrence value is obtained:** one deterministic, unarmed reference run before any kill run, under the run set's epoch, on two fresh synthetic installations:
  - (A) an unarmed commit at ordinal 1, the killed child's ordinal;
  - (B) an unarmed commit at ordinal 2, R2's ordinal. A kill before the draw has no R1, so R2 follows the killed child directly.
  - In (A), the `trust/` entries the publication created are numbered in creation order by APFS birth time. A barrier separates each creation. All entries count toward `dependency/create#k`, and files alone count toward `dependency/write#j`, which is the census's own numbering.
  - A file occurrence whose relative path (B) also writes takes the refusal. Any other occurrence takes Committed.
  - No directory occurrence is in X9-2's kill set at this census. A later census that adds one transcribes it by the same reference.
  - The value is never read back from a run under test.
- **The F00 cell's r8 clause and L11** now use `CONFIG.CUSTODY_REFUSED` with subject `installation-incomplete` and the per-occurrence rule. No `INSTALLATION.INCOMPLETE` token remains.

The rest of r8 is byte-identical: the registration window, X3c custody, the X3b floor directory, the WAL gap, R4, F07, L11's other states and the four promoted choices. The `marker/write.before` "empty" wording you noted, which is really a torn marker, was not a finding. It is left as written, because the request was for RF-1 only.

## Decide

- Does r9 resolve RF-1 exactly?
- Is the reference-run derivation a lawful way to fix each occurrence's R2 before any kill? That means unarmed, fixed by the script and the product, and never read back.
- Does r9 change nothing else in r8?
- Is anything else wrong?

Write REVIEW.md and review.json under the output directory. review.json needs:
- "verdict";
- "requiredFindings";
- "noAcceptedOutcomeChanged";
- "subjectSha256";
- "subject" (path, bytes, sha256);
- "preservedSnapshot": the accepted r7, `PROPOSAL-r7.md`, 85255 bytes, `913523…`.

Do not commit.
