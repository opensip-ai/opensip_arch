Codex review, round 2: the **M3-O1 law r2**. Claude Opus 5.5 leads, and you are the single reviewer. One verdict is wanted, **ACCEPT** or **REQUIRED-FINDINGS**, on the law only. The two S-OP-2 recording units are already accepted (your r1 review), so they are not in this round.

Write only under `/tmp/opensip-implementation/reviews/codex-o1-law-r2/`.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation. Run git read-only.
- **No cargo.** Don't run any build, test or lead set: timing-sensitive lanes may be using this machine. Because you run no cargo, the shared lane lock does not apply to you.
- You may run `evidence/recount.py` (this directory). It is Python only and runs `git grep` on product commit `b7b87b7`; it writes nothing.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.

## The subject

Paths are under `/Users/sb/code/opensip-ai/opensip_arch/`. Every pin is in `hashes.txt`. Apart from the subject, this request pins snapshots only: accepted bytes, your r1 review, and the overnight log at an arch commit.

| Role | Path | sha256 | Bytes |
|---|---|---|---|
| **Subject: M3-O1 r2** | `docs/implementation/m3/operability/o1/PROPOSAL.md` (untracked; read the working tree and check the pin) | `98715322…` | 80,638 |
| **Diff base: M3-O1 r1** | `docs/implementation/m3/operability/o1/PROPOSAL-r1.md`, the bytes you reviewed (committed at arch `99de7516b`) | `ac3f12fa…` | 73,886 |

`evidence/r1-to-r2.diff` is the unified diff from the base to the subject, for convenience; check it against the two pinned files.

**Product base.** r2 keeps `b7b87b7`, the commit you checked r1 against. Product main has since moved to `43ea32a` (I1-b1 at `083ad5c`, then X3c-3). r2 says so in its "r2 changes" table and re-pins nothing.

## What r2 changes

r2 answers your r1 review (`reviews/codex-o1-law-r1/review.json` and `REVIEW.md`) and, by its own account, changes nothing else of substance. The lead's decision for RF-01 is recorded in the overnight log, pinned as `docs/implementation/OVERNIGHT-2026-10-03.md@99de7516b` (lines 876-880).

| Finding | Where in r2 | Change |
|---|---|---|
| **M3-O1-RF-01** (P2) | item 2's "Why one leg"; item 20; item 21; O1-C11; item 23's O1-p and O1-S rows and its edge bullet; X-O3 | **Lead decision: operability's re-export of `dispose` moves to O1-S,** which already depends on O1-a (the crate) and O1-p (the helper). O1-p is platform-only: `clock.rs` CPU time, the descriptor admission, `disposition.rs` and the `lib.rs` lines. It depends on J3a only, not on O1-a and not on the held J4a. **Rejected:** an O1-a edge on O1-p; the re-export in O1-b. **For M3P r11:** O1-p's only edge is J3a, and O1-S carries the re-export. |
| **M3-O1-NB-02** | item 13; the Q1 answer | 4 production `debug_assert!` sites, not 9, each named; O1-b re-audits the measured artifact's sites at launch. |
| **M3-O1-NB-03** | Problem; item 19; item 20 | 143 production `let _ =` lines, not 140 (security 73, not 70); so 129 in platform and security, and 163 in test-only files. r1 had also dropped `installation_read_fixture.rs`'s 3 lines, which the stated path rule does not exclude; the count now follows the rule, with no extra exclusion. |
| **M3-O1-NB-01** | this request | Refreshed. r1's `hashes.txt` pinned `REQUEST.md` before the lead added answers Q1 and Q2. This request is a new directory; its own `REQUEST.md` pin is the last line written to `hashes.txt`, after this file was final. |
| Open questions | "Open questions: answered in r1's review" | Q1 and Q2 are recorded as the lead's answers, which you found sound; Q3 to Q8 as your review's answers. No new question. |

Also recorded, as record text only: the two S-OP-2 units' acceptance (Standings, header, item 22, Short names), and new Short-names rows for r1's snapshot and the overnight log.

`evidence/recount.py` and its output, `evidence/recount.json`, reproduce the corrected figures at `b7b87b7`: 306 lines in 150 files; 143 production (platform 56, security 73, storage 10, cli 3, lifecycle 1); 163 test-only; 129 in platform and security; the 3 `installation_read_fixture.rs` lines; and the 4 `debug_assert!` macro sites, with the 5 other text matches listed.

## Decide

1. **RF-01.** Does r2 close it? Can O1-p now start after J3a with every target file in existence, and is every unit that touches `crates/operability` gated on O1-a? Is the lead's ruling that O1-p need not wait for J4a preserved?
2. **The rejected alternatives.** Are they right?
3. **NB-02 and NB-03.** Are the corrected figures right, and is every place r1 used the old figures corrected (r1 lines 56, 331, 449, 477 and 634)?
4. **The answered questions.** Does the new table state your r1 answers to Q3 to Q8 faithfully?
5. **Only declared changes.** Does the subject differ from the diff base only in the regions above?
6. **Anything else wrong.**

## Output

Under `/tmp/opensip-implementation/reviews/codex-o1-law-r2/`. Do not commit, and run no cargo. `REVIEW.md` and `review.json`, with:
- `"verdict"`: `ACCEPT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`: a list, empty if you accept; each finding with an id, a location, the problem, the evidence and the fix;
- `"findingResolution"`: one entry each for M3-O1-RF-01 and NB-01 to NB-03, with a status and your assessment;
- `"nonBlockingObservations"`;
- `"diffAssessment"`: whether only declared changes were made;
- `"subjectSha256"`: `987153221b913fc1c4cc729ecfabad397670502c8dc95a4bb292ebe0506bbbf0`, with the subject's path and bytes (80,638).

This is a law review, not a design unit or an inventory unit, so no `subjectManifestSha256`, `supersededPassages` or `inventoryCandidateAssessment` is wanted.
