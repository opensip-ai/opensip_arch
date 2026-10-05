Codex review: **X9 r17 round 3, §RW**. Grok leads as of 2026-10-04. You are the single reviewer. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**. No cargo and no lane lock.

Write only `REVIEW.md` and `review.json` under `/tmp/opensip-implementation/reviews/codex-crash-matrix-x9-r17-rw/`. No repository edits, commits, pushes, or delegation. Git is read-only. Never touch `~/Library/Application Support/OpenSIP` and never read the private 413 UUID fixture.

## Subject

- **Live file:** `docs/implementation/m2/crash-matrix-x9/PROPOSAL.md`, 332138 bytes, sha256 `118a9a9835933da722691d1477a3f574e7ffd9deca73f7c21af7c6217c581aff`. That sha256 is `subjectSha256`.
- **Diff base:** `PROPOSAL-r17-S12.md`, 278697 bytes, sha256 `6b208ccf7d1b0ce5c18ec0329724fbc103de8b18d9abae0b02a6ac0856f397f3`. Round 2's accepted bytes.
- **Against that base the diff is exactly three hunks:**
  1. Round 2's acceptance note already at the top of the live file (two lines). It is not this round's change.
  2. One citation in §S12's `arrivalPhases` bullet (NBO-1). The expected spelling stays `A` to `E`, and `O`. A–E stay SOP2:871. O is J1 r6:588, J1's registration. No expected value moves.
  3. The reserved `### §RW` heading replaced by round 3's section (J-RW item 10, successor RW-S6, units J4a to J4e). It is marked not accepted.
- No other section's rows change. Under LD-17-1, judge §RW and the NBO-1 citation only.

## Law this section transcribes

- **J-RW r4, accepted:** `docs/implementation/m3/resume-repair-jrw/PROPOSAL-r4.md`, 118261 bytes, sha256 `9c53bce7185399511340b3313d55379395cd7029d375cb7006a514f859ab617f`. Item 10 is §RW's content. The live `PROPOSAL.md` adds only the acceptance note.
- Pins are in `hashes.txt`.

## Decide

- Does §RW carry RW-F00, RW-D1, RW-K1 to RW-K10, RW-N1 to RW-N12 and RW-B as J-RW r4 item 10 states them, with no new outcome?
- Are the six RW-F00 re-transcriptions the cells J4a moves, old and new, and nothing else?
- Is the NBO-1 citation a record correction only?
- Are lead decisions LD-RW-1 to LD-RW-11 acceptable? A disagreement with one is a finding.
- Does any other r17 section's row change?

`review.json` needs `verdict`, `requiredFindings`, and `subjectSha256` as a single string. Do not commit.
