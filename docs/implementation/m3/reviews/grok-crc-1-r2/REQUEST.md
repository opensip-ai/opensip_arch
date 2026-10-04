GROK2 re-review: **CRC-1 r2**, the identity contract successor for law M3-C item 9 (the core detector, provider and adapter closures), after your r1 finding. This is a **design unit** (a `verify_design` contract successor). Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-DESIGN-UNIT** with `subjectManifestSha256`, or **REQUIRED-FINDINGS**.

Write only under `/tmp/opensip-implementation/reviews/grok-crc-1-r2`.

(Lead note: GROK2 reviewed r1. Grok reviews r2, because GROK2 is busy with M3-PLAN r7. GROK2's r1 review is in `grok2-crc-1-r1/`; judge whether its RF-1 is resolved. Don't run cargo.)


**Rules:**
- **Read-only.** No repository edits, commits, pushes or delegation. Run git only read-only.
- **No builds or tests.** Run no cargo, no tests and no crash-matrix binary or checker. P0's lanes may be using the machine.
- **Scripts.** If you run anything, use only the evidence scripts below and read-only commands, at `nice -n 19`, with any scratch files under your review directory.
- **`verify_design`.** Run it only through `evidence/verify_scratch.py`, which writes nothing and holds a synthetic review and assent in memory. Never edit the product or its lock.
- **Never touch the real home.** `~/Library/Application Support/OpenSIP` stays absent; do not read or create it.
- **Never read the private 413 UUID fixture.**

## Subject

The pins are in `hashes.txt`. The CRC-1 files are still untracked in arch until acceptance.
- **The subject manifest** is `docs/implementation/m3/snapshot-plan-c/crc-1-subject.json`. Its sha256 is `subjectManifestSha256`.
- **Its 7 members** are the same paths as r1.
- **Not part of the subject:** `crc-1-unit.json`, the lead's DRAFT-PENDING-REVIEW record. It now carries the r2 pins and the review path `docs/implementation/m3/reviews/grok-crc-1-r2/review.json` (NBO-2).

**Product.** Main is `cd5958b` (`cd5958b3608f44a0035566c9d4500e5005c62e91`), read-only. Its lock has 82 contract successors. r2 is built and checked against `design-lock.json@cd5958b`, read with `git show`, not the live file. r1's base was `9c11c53` (79). The parents, the fixture and the nine selectors are the same at both commits, and none of B-S2, B-S9 and I1-P touches a CRC-1 key.

**Law.** M3-C r7 item 9 (`snapshot-plan-c/PROPOSAL-r7.md`, `a1ee9386…`), with r6's X-C1 (`PROPOSAL-r6.md`, `8274bca1…`).

## What r2 changes

The diff base is the r1 subject, `adfa0d97…`, which you reviewed. Its exact bytes are in this directory's `r1-members/`: the r1 subject manifest and all seven r1 members, verified against the r1 pins. All seven members change:

| Member | r1 | r2 | Change |
|---|---|---|---|
| `crc-1/evidence/build_crc_1.py` | 22232, `95f0ef65…` | 22343, `92829935…` | **RF-1:** `SELECTION_ADD` ends "…and is never selected otherwise, not even explicitly; the core adapter closure is never a member.", your replacement verbatim. **The drift check:** IE:285's provider bullet reads "and is never selected otherwise, not even explicitly" instead of "and never otherwise". The default `--rev` is `cd5958b`. **NBO-2:** the unit template emits the `grok-crc-1-r2` review path. |
| `crc-1/successor.json` | 21459, `55b43151…` | 21493, `910d9ae6…` | Exactly two `after` strings change: the `selectionLaw` string ("explicitly included" becomes "not even explicitly") and IE:285 (the clause above). Also the candidate pins. The parents, selectors, `before`s, the seven other `after`s and `standing` are byte-identical. |
| `crc-1/PASSAGES.md` | 16395, `9fc07ef4…` | 16428, `60769b71…` | regenerated: the same two texts, and the header names `cd5958b` with 82 successors |
| `crc-1/evidence/check_crc_1.py` | 9866, `c38552fe…` | 10779, `b07ecbb6…` | Your fix: after the IE:285 needle loop it asserts that all three membership statements (IE:285, IE:1377 and `selectionLaw`) contain "exactly when the Plan selects" and "is never selected otherwise, not even explicitly" and state the adapter's non-membership, and that no `after` contains "explicitly included". Run against r1's record, these assertions refuse it. The default `--rev` is `cd5958b`. |
| `crc-1/evidence/verify_scratch.py` | 6493, `4526bf5e…` | 7113, `ab4e492c…` | Adds `--with-cr-1`, which binds CR-1 first and CRC-1 after it, and asserts the count. |
| `crc-1/evidence/vector.json` | 16122, `4ca132f6…` | 16122, `288045ff…` | Only `source.product`, `9c11c53` to `cd5958b`. The fixture pin (`2d42bb5d…`) and every id and digest are unchanged. |
| `crc-1/README.md` | 27465, `202fc5c2…` | 30439, `99aa8335…` | The new **r2 changes** table, plus updates for the reviewer (GROK2), the base (`cd5958b`), cross-law item 1 (NBO-1), binding and the evidence runs. |

**NBO-1, recorded but not applied here.** The live SYN-1F copy (`syntax-e/syn-1f/design/foundation/identity-schemas.v3.json`, 200,510 bytes, `69438966…`, unbound) has absorbed CRC-1's strings, and its `selectionLaw` still has r1's "explicitly included". It is another drafter's file. README cross-law item 1 says that it must take r2's sentence if SYN-1F keeps carrying CRC-1 in place. The lead tells SYN-1F's drafter.

## Checks run by the lead

Every check used `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`, and each was run twice.
- **`build_crc_1.py --check`**: identical, the unit draft included.
- **`check_crc_1.py`**: passes at `cd5958b` (the default) and at `--rev 9c11c53`.
- **`verify_scratch.py --rev cd5958b`**: 82 to 83, nine overrides, no supersession, inventory `v134` and 55 inheritance rows unchanged. The second-override probe refuses.
- **`verify_scratch.py`** on the checkout at `cd5958b`: 82 to 83, with 40 generation sources and 48 admission sources verified.
- **Together with CR-1:**
  - `verify_scratch.py --rev cd5958b --with-cr-1` binds CR-1 then CRC-1, 82 to 84;
  - CR-1's `evidence/verify_scratch.py --rev cd5958b --after-crc-1` binds CRC-1 then CR-1, 82 to 84.

  CR-1 is unchanged and still in CODEX2's review.
- **`verify_scratch.py --rev 9c11c53`**: 79 to 80, as before.

## Decide

1. **Is RF-1 resolved?** Is the `selectionLaw` `after` exactly your replacement? Do IE:285, IE:1377 and `selectionLaw` now state one rule?
2. **The drift check.** Is IE:285's alignment right and meaning-preserving? Did the lead miss any other CRC-1 string that drifts from IE:1377, or from MC r7:443 and C2-T13 (r7:470)?
3. **Did anything else change?** Diff `r1-members/` against the r2 members. Only the changes in the table should appear.
4. **The base move.** Does anything you accepted in r1 no longer hold at `cd5958b`?

## Running the evidence (optional)

From `docs/implementation/m3/snapshot-plan-c/crc-1/`:
- `evidence/build_crc_1.py --check`
- `evidence/check_crc_1.py`, and the same with `--rev 9c11c53`
- `evidence/verify_scratch.py --rev cd5958b`, and the same with `--with-cr-1`
- `evidence/verify_scratch.py`, which uses the checkout

## Output

Write REVIEW.md and review.json. review.json must contain:
- `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`: each with id, location, problem, evidence and fix;
- `"nonBlockingObservations"`;
- `"findingResolution"`: RF-1, NBO-1 and NBO-2;
- `"subjectManifestSha256"`: a single string, the sha256 of `crc-1-subject.json`. The lead's r2 value is `e71ee47d2bd438b90bd87f1ee9168012e08eabe21791fffa60d9116f3f7a8d6f`.
- `"successor"`: `{path, bytes, sha256}` of `crc-1/successor.json`. The lead's r2 value is 21493 bytes, `910d9ae634663a43c67aa3d0dd9029034b8b4e4cd92e812c47833ceb25e4fc5b`.

This is a contract successor, so it has no `inventoryCandidateAssessment`. If you would change bytes, give the exact replacement. Do not commit.
