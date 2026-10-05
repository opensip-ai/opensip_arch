Codex review: **X9 r17 round 3, §RW, correction of X9-RW-RF-01**. Grok leads as of 2026-10-04. You are the single reviewer. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**. No cargo and no lane lock.

Write only `REVIEW.md` and `review.json` under `/tmp/opensip-implementation/reviews/codex-crash-matrix-x9-r17-rw-r2/`. Do not write into `/tmp/opensip-implementation/reviews/codex-crash-matrix-x9-r17-rw/` (that is round 3 r1 and stays REQUIRED-FINDINGS). No repository edits, commits, pushes, or delegation. Git is read-only. Never touch `~/Library/Application Support/OpenSIP` and never read the private 413 UUID fixture.

## Subject

- **Live file:** `docs/implementation/m2/crash-matrix-x9/PROPOSAL.md`, 332508 bytes, sha256 `312f4de06b968d5a788672bf139f192748eca6dde819d3f4b27a856dd8ae553e`. That sha256 is `subjectSha256`.
- **Previous subject:** round 3 r1, 332138 bytes, sha256 `118a9a9835933da722691d1477a3f574e7ffd9deca73f7c21af7c6217c581aff`. A byte copy is `PROPOSAL-r1-subject.md` beside this request. Its review is `/tmp/opensip-implementation/reviews/codex-crash-matrix-x9-r17-rw/review.json`, verdict REQUIRED-FINDINGS, one finding X9-RW-RF-01.
- **Diff base:** `PROPOSAL-r17-S12.md`, 278697 bytes, sha256 `6b208ccf7d1b0ce5c18ec0329724fbc103de8b18d9abae0b02a6ac0856f397f3`. Round 2's accepted bytes.
- **Against that base the diff is still exactly three hunks:**
  1. Round 2's acceptance note already at the top of the live file (two lines). It is not this round's change.
  2. One citation in §S12's `arrivalPhases` bullet (NBO-1). The expected spelling stays `A` to `E`, and `O`. A–E stay SOP2:871. O is J1 r6:588, J1's registration. No expected value moves.
  3. The reserved `### §RW` heading replaced by round 3's section. It is marked not accepted.
- Against the r1 subject, the diff is three sentences inside §RW and nothing else:
  1. The round heading records that this is X9-RW-RF-01's correction.
  2. RW.3's prediction now says J4a's two repair start states add four census point names, each occurring twice (eight durability events), and eight kill-set points. The eight RW-K rows stay as RW.5 lists them. J4b, J4c and J4d add only the names their own censuses contribute.
  3. RW.7's J4e census gate repeats that four-name delta. Every other sub-part contributes only the `.repair` names its own census adds.
- No RW-K row, expected object, scope name or lead decision changes. X9-RW-NB-01 and X9-RW-NB-02 are unchanged.

## The finding this round answers

X9-RW-RF-01 (P2): state that J4a's two repair start states contribute four new census point names, each occurring twice, hence eight physical durability events and eight kill-set points. Keep the eight RW-K rows unchanged. Use the four-name census delta in every related prediction and gate. Other units' contributions remain derived from their own censuses.

Census points are names. At the pinned product `43ea32a`, `Census::from_exit` groups occurrences by name. `n = 2` puts both occurrences of a name in the kill set.

## Law this section transcribes

- **J-RW r4, accepted:** `docs/implementation/m3/resume-repair-jrw/PROPOSAL-r4.md`, 118261 bytes, sha256 `9c53bce7185399511340b3313d55379395cd7029d375cb7006a514f859ab617f`. Item 10 is §RW's content. The live `PROPOSAL.md` of J-RW adds only the acceptance note.
- Pins are in `hashes.txt`.

## Decide

- Does the corrected census sentence close X9-RW-RF-01, and does RW.7's J4e gate use that same four-name delta?
- Did this correction change any row, expected object, scope name or lead decision?
- Do the two unchanged non-blocking observations stay non-blocking? An unchanged note is not a new required finding unless this correction made it false.
- Does any other r17 section's row change?

`review.json` needs `verdict`, `requiredFindings`, and `subjectSha256` as a single string (`312f4de06b968d5a788672bf139f192748eca6dde819d3f4b27a856dd8ae553e`). Do not commit.
