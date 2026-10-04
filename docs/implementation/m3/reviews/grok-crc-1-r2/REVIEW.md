# CRC-1 r2

Verdict: **REQUIRED-FINDINGS**.

Subject `crc-1-subject.json` is 1434 bytes, sha256 `e71ee47d2bd438b90bd87f1ee9168012e08eabe21791fffa60d9116f3f7a8d6f`. Successor `docs/implementation/m3/snapshot-plan-c/crc-1/successor.json` is 21493 bytes, sha256 `910d9ae634663a43c67aa3d0dd9029034b8b4e4cd92e812c47833ceb25e4fc5b`. Product main `cd5958b` has 82 contract successors. No inventory candidate.

## r1 RF-1 is resolved

The `selectionLaw` after is GROK2's replacement verbatim. It keeps the parent's grant that extra admissible retained closures may be selected explicitly, then withdraws that grant for the core role closures: the core provider closure is a direct member exactly when the Plan selects a `native.semantic-universe.syntax.v2` universe, and is never selected otherwise, not even explicitly; the core adapter closure is never a member.

IE:285, IE:1377, and `selectionLaw` state that one rule. IE:285 says "a syntax universe". IE:1377 and `selectionLaw` name `native.semantic-universe.syntax.v2`. M3-C r7:436 defines that identity, and r7:443 uses "a syntax universe" for the same referent. The adapter is never a `plan.semanticClosures` member in IE:285, never a `semanticClosures` member in IE:1377, and never a member in `selectionLaw`. C2-T13 (r7:470) refuses the provider closure in `semanticClosures` when no syntax universe is selected, and refuses its absence when one is selected.

`check_crc_1.py` asserts the shared clause on all three statements and refuses any after that contains "explicitly included". It passes at `cd5958b` (`boundAtRev` 82) and at `9c11c53` (`boundAtRev` 79). The five closure ids are the same at both commits, and the vector still has 53 fixture cases.

No other after states membership or contains "explicitly included". The standing summary keeps r7:443's shorter positive half, "a plan.semanticClosures member exactly when a syntax universe is selected", and does not reopen explicit selection.

## The base move holds

`verify_scratch.py` at `cd5958b` goes from 82 to 83 successors: nine overrides, zero supersessions, six candidates, inventory v134, 55 inheritance rows, and the second-override probe refuses. Checkout mode at `cd5958b` is the same 82 to 83, with 40 generation sources and 48 admission sources (15 aliases). `--with-cr-1` and CR-1's `--after-crc-1` both go from 82 to 84. At `9c11c53` the count is still 79 to 80. Parents, the fixture pin, and the nine selectors are unchanged.

## RF-1

The r2 member diff matches the review-request table except the review path. `build_crc_1.py:340` emits `docs/implementation/m3/reviews/grok2-crc-1-r2/review.json`. The unit record emits `docs/implementation/m3/reviews/grok-crc-1-r2/review.json`. `build_crc_1.py --check` exits 1 and differs only on `crc-1-unit.json`. That file is canonical JSON, and the path is its only disagreement with the template.

README.md:3 says the draft needs GROK2's `ACCEPT-DESIGN-UNIT`. README.md:13 points r1's member bytes at `reviews/grok2-crc-1-r2/r1-members/`, which is absent; the bytes are in `reviews/grok-crc-1-r2/r1-members/`. README.md:22 and binding step 1 (line 196) name the grok2-crc-1-r2 review path and say `--check` covers the unit draft. README.md:206 says `--check` reported identical bytes for every generated file, the unit draft included.

Replace the builder path and those README strings with `grok-crc-1-r2`, leave the unit record's path in place, and leave the shared rootAssessment sentence that names GROK2's r2 review unchanged. Regenerate so the candidate pins follow the edited README and builder. The nine passage overrides stay as they are. `--check` must then exit 0.

## Non-blocking

The live SYN-1F identity schema is 200510 bytes, sha256 `73645b7633d95f5d7b8e5183d789b8aab028148be0dd158e0b503a4cc3e2bd19`. The README and `hashes.txt` still pin `69438966…` at that size. Its three CRC-1 identity strings already equal r2's afters, and "explicitly included" does not occur. README.md:173 still calls the `selectionLaw` string r1's. If SYN-1F binds first, CRC-1's befores still have to be re-checked, because they equal I1-L and the live copy already carries the afters.

The builder and the unit record both say the lead completes the draft after GROK2's r2 review. Align that sentence in both files together.
