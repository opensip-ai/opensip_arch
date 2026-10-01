REVIEWER re-review: law X3b r2 after Grok's r1 findings. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/REVIEWDIR. Law review; no product cargo. Product HEAD is f7acb6d.

Subject: docs/implementation/m2/journal-x3b/PROPOSAL.md r2 (pin in hashes.txt). `diff` it against PROPOSAL-r1.md. The r1 findings are in `reviews/grok-journal-x3b-r1/`.

## Changes

- **RF-1 (lead decision).** A floor step runs under the fence before X2d's lease:
  - it probes `writer.lease` with a nonblocking attempt and releases it immediately;
  - if busy, it skips; otherwise it writes the floor with no project lock held;
  - the end step mirrors this after retaking the fence;
  - the floor never moves down.
- **RF-2 (lead decision).** `projectKeyDigest` = `SHA-256(N)`, where N is the canonical lowercase UUID text of the ACTIVE row's `namespaceId`, taken from `ProjectOperation`'s R0 or R2. The product's existing `project_key` comparison works unchanged.
- **RF-3.**
  - No quarantine row or marker is ever written; every open re-detects.
  - `MIGRATION.CORRUPT` covers only a non-prefix format-3 footprint or a violated generation boundary.
  - A complete format-1 or format-2 carrier is F46: `HOST.IO_FAILURE`, `host-io`.
- **RF-4 (lead decision).** Creation is floor first: `{lastSeq 0}`, then the carrier and witness under the lease. "Floor absent" with no carrier or witness means INIT; otherwise it is a new quarantine, `floorLost`. All crash states are listed.
- **Alignment.** Two X3b steps sit inside X2 r4's single fence hold; X2 must record that order in its next revision. The checkpoint aligns with X4 r2 and `JournalAppendLock`. X4T r1 item 7's "floor records the trust epoch" is corrected here: the floor shape is closed, and X4T must compare against SC-TRUST's own floors.

## Decide

- Are RF-1 to RF-4 closed?
- Is the floor step's lease probe sound against S7's lock order and lease semantics?
- Is the RF-2 preimage right?
- Are the crash-state tables complete?
- Are the cross-law corrections right?
- Is anything new wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
