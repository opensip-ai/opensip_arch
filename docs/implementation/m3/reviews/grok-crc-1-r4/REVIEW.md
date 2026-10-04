# CRC-1 r4

Verdict: **ACCEPT-DESIGN-UNIT**.

Subject `crc-1-subject.json` is 1434 bytes, sha256 `ec89680137ed0ad29af1d2b3b955eff763a184c5314387f2fa83b67da14433bc`. Successor `docs/implementation/m3/snapshot-plan-c/crc-1/successor.json` is 21493 bytes, sha256 `29df5f5e2b145daf3c9b8e231ccac1d08c5b36d2eb006fbdc3bba543d7084166`. Product main `cd5958b` has 82 contract successors. The lock at that commit is 334799 bytes, sha256 `67a5bb929ccc27821878c31cb75f39c37237e0d089f970c66843e5828e4650c2`.

## r3 RF-1 is resolved

README.md:3 says **Draft r4, PROPOSED, not accepted** and asks for an independent `ACCEPT-DESIGN-UNIT`, with Grok reviewing r4. README.md:26 keeps r1's members in `reviews/grok-crc-1-r2/r1-members/`. That directory is present and holds the eight r1 member files. Binding step 1 (README.md:209) copies the accepting round's review to `docs/implementation/m3/reviews/grok-crc-1-r<N>/review.json`, where the builder's emitted path names N. `build_crc_1.py:340` and `crc-1-unit.json` both emit `docs/implementation/m3/reviews/grok-crc-1-r4/review.json`. `build_crc_1.py --rev cd5958b --check` exits 0 and reports identical, with an empty differs list. `reviews/grok2-crc-1-r2` is absent.

The rootAssessment in the builder and in the unit draft both say the lead completes the draft after Grok's r4 review. The unit status remains `DRAFT-PENDING-REVIEW`.

## The diff matches the stated pass

Against `reviews/grok-crc-1-r4/r3-members/`:

- `README.md` updates the status line, adds the r4 changes section, corrects the r3 candidate-pin sentence, cites `reviews/grok-crc-1-r2/r1-members/`, points the NBO-2 row at `grok-crc-1-r4`, rewrites the SYN-1F note, and rewrites binding step 1.
- `evidence/build_crc_1.py` changes the review path and the draft assessment text.
- `successor.json` changes the candidate pins of those two files. The `passageOverrides` region is byte-identical to r3 (17872 bytes), as are the parents, the standing, and the other four candidates. The two changed pins match the files on disk.

`crc-1-subject.json` updates the pins of `README.md`, `build_crc_1.py`, and `successor.json`. `crc-1-unit.json` updates the review path, the assessment, and those subject and successor pins. `PASSAGES.md`, `check_crc_1.py`, `vector.json`, and `verify_scratch.py` keep their r3 hashes.

## Two README lines are still stale

README.md:34, in the r2 changes table, still says the live SYN-1F copy absorbed r1's `selectionLaw` sentence and must take r2's. README.md:186 says that sentence is already r2's. The live `identity-schemas.v3.json` is 200510 bytes, sha256 `73645b7633d95f5d7b8e5183d789b8aab028148be0dd158e0b503a4cc3e2bd19`. Its three CRC-1 strings equal the afters, and "explicitly included" does not occur. The table row is NBO-1.

README.md:186 also says that only SYN-1F's parent pin on this record moves. The nine overrides, including every parent pin, compare byte-identical to r3. The three IDS parents are still I1-L (`c9214f0304b8b4023e1e4fba0179211fa2460814b03cfbd87301334e4822613d`, 198725 bytes), and the befores still equal that file. The conditional rebase if SYN-1F binds first is the previous bullet. The parent-pin clause is NBO-2.

## Nothing else blocks

`check_crc_1.py` passes at `cd5958b`: nine overrides, six parents, 82 successors already bound, and 53 fixture cases. GROK2's r1 wording stays in force. `verify_scratch.py --rev cd5958b` goes from 82 to 83 successors, selects this successor, keeps nine overrides and zero supersessions, keeps inventory v134 and 55 inheritance rows, and the second-override probe returns `REFUSED: conflicting contract passage overrides`.
