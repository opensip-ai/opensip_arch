# CRC-1 r3

Verdict: **REQUIRED-FINDINGS**.

Subject `crc-1-subject.json` is 1434 bytes, sha256 `e030a1cf5031c7ece420b54663415cae69a7db1a55937130be91281408437728`. Successor `docs/implementation/m3/snapshot-plan-c/crc-1/successor.json` is 21493 bytes, sha256 `01a995b90ee9486eca2130b2cefb270b730696a5130c1721e438174e65b71d45`. Product main `cd5958b` has 82 contract successors. The lock at that commit is 334799 bytes, sha256 `67a5bb929ccc27821878c31cb75f39c37237e0d089f970c66843e5828e4650c2`.

## r2 RF-1 is partly resolved

The builder and the unit draft now name the same review. `build_crc_1.py:340` emits `docs/implementation/m3/reviews/grok-crc-1-r3/review.json`. `crc-1-unit.json` records that path, with status `DRAFT-PENDING-REVIEW`. `build_crc_1.py --rev cd5958b --check` exits 0 and reports identical, with an empty differs list. The NBO-2 row at README.md:31 cites that path. The rootAssessment in the builder and in the unit draft both say the lead completes the draft after Grok's r3 review.

Three README cites from r2 RF-1 are still the r2 text:

- README.md:3 still says **Draft r2** and that the draft needs GROK2's `ACCEPT-DESIGN-UNIT`.
- README.md:22 still keeps r1's members in `reviews/grok2-crc-1-r2/r1-members/`. That directory is absent. The eight r1 member files are in `reviews/grok-crc-1-r2/r1-members/`.
- Binding step 1 at README.md:205 still copies the review to `docs/implementation/m3/reviews/grok2-crc-1-r2/review.json`. `reviews/grok2-crc-1-r2` is absent. The unit draft's `independentReview.path` is `docs/implementation/m3/reviews/grok-crc-1-r3/review.json`.

That remainder is this review's RF-1. Line 14's account of the r2 builder bug is history, and it matches the r2 template.

## The diff is the three listed changes

Against `reviews/grok-crc-1-r3/r2-members/`:

- `evidence/build_crc_1.py` changes the review path and the draft assessment text.
- `README.md` adds the r3 changes section, replaces the NBO-2 row, and updates the SYN-1F digest sentence in cross-law item 1.
- `successor.json` changes the candidate pins of those two files. The nine `passageOverrides`, the parents, the standing, and the other four candidates compare equal to r2. The two changed pins match the files on disk.

`crc-1-subject.json` updates the pins of `README.md`, `build_crc_1.py`, and `successor.json`. `crc-1-unit.json` updates the review path, the assessment, and those subject and successor pins. `PASSAGES.md`, `check_crc_1.py`, `vector.json`, and `verify_scratch.py` keep their r2 hashes. README.md:18 says the passages and every candidate are byte-identical to r2. The nine passage overrides are. The two edited candidates are not. That sentence is NBO-2.

## The assigned checks pass

`check_crc_1.py` passes at `cd5958b`: nine overrides, six parents, 82 successors already bound, and 53 fixture cases. GROK2's r1 `selectionLaw` wording stays in force. The check still requires "not even explicitly" on IE:285, IE:1377, and `selectionLaw`, and it refuses an after that contains "explicitly included".

`verify_scratch.py --rev cd5958b` goes from 82 to 83 successors, selects this successor, keeps nine overrides and zero supersessions, keeps inventory v134 and 55 inheritance rows, and the second-override probe returns `REFUSED: conflicting contract passage overrides`.

## RF-1

In README.md:3, replace the draft label with **Draft r3** and name Grok's `ACCEPT-DESIGN-UNIT`. In README.md:22, cite `reviews/grok-crc-1-r2/r1-members/`. In README.md:205, copy the review to `docs/implementation/m3/reviews/grok-crc-1-r3/review.json`, the path the builder and the unit draft already emit. Leave the builder path as it is. Regenerate so the README pin, the subject manifest, and the unit draft follow the edited README. The nine passage overrides stay. `--check` must still exit 0.

## Non-blocking

The live SYN-1F identity schema is 200510 bytes, sha256 `73645b7633d95f5d7b8e5183d789b8aab028148be0dd158e0b503a4cc3e2bd19`. The `73645b76` prefix in README.md:182 matches it. Its three CRC-1 strings equal the afters, and "explicitly included" does not occur. `selectionLaw` is the corrected sentence. README.md:30 and README.md:182 still say that string is r1's and that the copy must take r2's sentence. The three befores still equal I1-L (`c9214f0304b8b4023e1e4fba0179211fa2460814b03cfbd87301334e4822613d`, 198725 bytes), so a rebase remains if SYN-1F binds first.

README.md:18 says every candidate is byte-identical to r2. The README and `build_crc_1.py` pins differ from r2 and match the files on disk.
