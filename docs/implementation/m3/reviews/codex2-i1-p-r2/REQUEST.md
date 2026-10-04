CODEX2 re-review: **I1-P r2**, the pack contract successor for `opensip.preview.typescript.pack:1` (law M3-I1 r2 item 5; X12c), after your r1 finding. This is a **design unit** (a `verify_design` contract successor). Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-DESIGN-UNIT** or **REQUIRED-FINDINGS**.

Write only under `/tmp/opensip-implementation/reviews/codex2-i1-p-r2`.

**Rules:**
- **Read-only.** No repository edits, commits, pushes or delegation. Run git only read-only.
- **No builds or tests.** A timing-sensitive crash-matrix lead set may be using this machine. Run no cargo, no tests and no crash-matrix binary or checker.
- **Scripts.** If you run anything, use only the evidence script below and read-only commands, at `nice -n 19`, with any scratch files under your review directory.
- **Never touch the real home.** `~/Library/Application Support/OpenSIP` stays absent; do not read or create it.
- **Never read the private 413 UUID fixture.**

## Subject

The pins are in `hashes.txt`. The I1-P files are still untracked in arch until acceptance.
- **The subject manifest** is `docs/implementation/m3/preview-pack-i1/i1-p-subject.json`. Its sha256 is `subjectManifestSha256`.
- **Its 8 members** are the same paths as r1.
- **Not part of the subject:** `i1-p-unit.json`, the lead's DRAFT-PENDING-REVIEW record, now carrying the r2 pins.

**Product.** Main is `9c11c53`, read-only. Its lock holds 79 contract successors, with I1-L bound as the 78th at your accepted pins (`9c490137…`, subject `51581c18…`). So I1-P's three parents are now selected.

Main may move under you, as it did in r1. While this request was being written it moved to `240a795`, which binds B-S2 as the 80th successor and changes only `design-lock.json`. The lead's checks below were run against both locks. The files this unit pins are unchanged from `3e64266` through `240a795`:
- `policy.rs`;
- `policy_pack_tests.rs`;
- `pack-registry.json`;
- `configuration_tests.rs`.

## What r2 changes

The diff base is the r1 subject, `f051269c…`, which you reviewed. Its exact bytes for the three changed members, and the r1 subject manifest itself, are in this directory's `r1-members/`, verified against the r1 pins. Exactly three members change:

| Member | r1 | r2 | Change |
|---|---|---|---|
| `i1-p/evidence/build_i1p.py` | 19900, `65acae36…` | 20092, `68135122…` | **RF-I1P-1.** Lines 177-181 are replaced by your `fix` block **verbatim**. A selected I1-L member is reused only when its `bytes` and `sha256` are identical, and is added to the prospective accepted set only when it is not yet bound. A mismatched selected pin is still refused. |
| `i1-p/README.md` | 7776, `dd78d0df…` | 7912, `e6daa7e1…` | **NB-I1P-1.** Line 60's paragraph is replaced by your exact text. 6.7 is now the contribution law, and the compiled `RuleProgramV2` schema check is named separately. The lead checked X12 r3 item 6.7 (`PROPOSAL-r3.md:97`). |
| `i1-p/successor.json` | 2598, `3cb6d485…` | 2598, `3fa394ac…` | Only the two candidate pins above. |

**Unchanged byte for byte:**
- `pack-contract.json`;
- `materialization-map.json`;
- `evidence/digests.json`;
- the document (`96675a5e…`, 574 B);
- `pack-registry.json` (`d08a85de…`).

So the row, the digests, the self-checks, the parents and `baseProductHead` (`3e64266`) are as you assessed in r1. The map's `before` pin for `pack-registry.json` (305 B) still holds at `9c11c53` and `240a795`.

## Checks run by the lead

All runs used `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`. `--deps` is a scratch directory holding jsonschema 4.25.1, installed offline.

- **Build check.** `build_i1p.py --product <checkout> --deps <dir> --check` **passes (exit 0)**, comparing all 8 members and the subject with the files on disk:
  - against `9c11c53`'s lock taken read-only with `git show`;
  - against `240a795`'s lock, taken the same way;
  - against the live checkout, re-run at `240a795`.

  The two encoders agree. All three digests equal law item 5.3. The document is admitted under both I1-L copies and refused by both parents. All four I1-L copies pass the meta-schema check, and the op law admits the rule.
- **Binding.** A scratch-only restatement of `verify_design`'s `successor_chain` contract walk ran over each lock: 79 bindings at `9c11c53` and 80 at `240a795`. It then applied `contract_successor` to I1-P appended as the next binding, with an in-memory synthetic review and assent. It **passes** on both locks:
  - the three parents are accepted at their exact pins (I1-L is the 78th binding);
  - the 8 members match their pins;
  - the candidates equal the subject minus the record;
  - no member path is already accepted;
  - there are no overrides or supersessions.

  The lead did not run the real `tools/verify_design.py`; that runs at binding.

## Decide

1. Is RF-I1P-1 resolved? Does `--check` now pass against a checkout with I1-L bound, and does it still refuse a selected I1-L pin whose bytes differ?
2. Is NB-I1P-1's text applied exactly?
3. Did anything else change? Confirm by diffing `r1-members/` against the r2 members.
4. Does anything that r1 accepted no longer hold at `9c11c53`?

## Running the evidence (optional)

- **Dependencies.** Your r1 `deps` directory (`/tmp/opensip-implementation/reviews/codex2-i1-p-r1/deps`) can be reused, or the same offline install can be repeated under this review's directory.
- **Build check.** Run `docs/implementation/m3/preview-pack-i1/i1-p/evidence/build_i1p.py --product /Users/sb/code/opensip-ai/opensip --deps <dir> --check`.

## Output

Write REVIEW.md and review.json. review.json must contain:
- `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`: each with id, location, problem, evidence and fix;
- `"nonBlockingObservations"`;
- `"findingResolution"`: RF-I1P-1 and NB-I1P-1;
- `"subjectManifestSha256"`: a single string, the sha256 of `i1-p-subject.json`. The lead's r2 value is `e1264633e23caf3e22d5e2177eb41a8977c330d83c1792526f572a33457c7a1b`.
- `"successor"`: `{path, bytes, sha256}` of `i1-p/successor.json`. The lead's r2 value is 2598 bytes, `3fa394ac4dc09a56409080885ae561727ad345dbf5e00f5792dcc5a20993c74e`.

This is a contract successor, so it has no `inventoryCandidateAssessment`. If you would change bytes, give the exact replacement. Do not commit.
