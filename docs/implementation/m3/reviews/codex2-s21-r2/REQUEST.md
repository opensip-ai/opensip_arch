Grok re-review: **S21 r2**, the commit-outcome exception to WS's before-settle rule, a contract successor of the host pipeline law M3-J1 r5 (LD-r5-2), after your r1 finding. This is a **design unit** (a `verify_design` contract successor). Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-DESIGN-UNIT** with `subjectManifestSha256`, or **REQUIRED-FINDINGS**.

Write only under `/tmp/opensip-implementation/reviews/codex2-s21-r2`.

(Lead note: the directory keeps the name `codex2-s21-*` because the unit's builder emits that review path. You reviewed r1 in `codex2-s21-r1/`. Your r1 review is copied there, and its status is REQUIRED-FINDINGS. Judge whether RF-1 is resolved. Don't run cargo.)

**Rules:**
- **Read-only.** No repository edits, commits, pushes or delegation. Run git only read-only.
- **No builds or tests.** Run no cargo, no tests, no generator and no crash-matrix binary or checker.
- **Scripts.** If you run anything, use only the evidence scripts below and read-only commands, at `nice -n 19`, with any scratch files under your review directory.
- **`verify_design`.** Run it only through `evidence/verify_scratch.py`, which writes nothing and holds a synthetic review and assent in memory. Never edit the product or its lock.
- **Never touch the real home.** `~/Library/Application Support/OpenSIP` stays absent; do not read or create it.
- **Never read the private 413 UUID fixture.**

## Subject

The pins are in `hashes.txt`. The S21 files are still untracked in arch until acceptance.
- **The subject manifest** is `docs/implementation/m3/host-pipeline-j/s21-subject.json`. Its sha256 is `subjectManifestSha256`.
- **Its 7 members** are the same paths as r1.
- **Not part of the subject:** `s21-unit.json`, the lead's DRAFT-PENDING-REVIEW record. It now carries the r2 pins and the review path `docs/implementation/m3/reviews/codex2-s21-r2/review.json`.

**Product.** Main is `6190e66` (`6190e66cdc6e6de5816cefc2887661ab08d47515`), read-only. It binds SYN-NS, so its lock has 92 contract successors.
- **Lock pin:** `design-lock.json@6190e66` (505,663 bytes, `8b32ede7…`), read with `git show`, not the live file.
- **r1's base** was `218465f` (91). `verify_design.py` and INV5 are byte-identical at both commits.
- **SYN-NS** touches neither WS nor WSE.
- **S18** still binds WS 225, 227, 228, 231 and 1393, and WSE 225, 229, 230, 235 and 1466.

**Law.** M3-J1 r5 (`host-pipeline-j/PROPOSAL-r5.md`, `4ccb2320…`, Codex's acceptance):
- 8.3, J1:588-592;
- LD-r5-2, J1:600-627;
- the S21 row, J1:868.

## What r2 changes

The diff base is the r1 subject, `090de59f…`, which you reviewed. Its exact bytes are in this directory's `r1-members/`: the r1 subject manifest and all seven r1 members, each verified against the r1 pins. All seven change:

| Member | r1 | r2 | Change |
|---|---|---|---|
| `s21/successor.json` | 5538, `3e8ad15d…` | 6768, `df5ab70a…` | **RF-1:** two new line overrides, WS:229 and WSE:233. The `standing` names them, and the candidate pins are renewed. The two line-226 overrides (their `before` and `after` included) and the parents are byte-identical to r1. |
| `s21/PASSAGES.md` | 6286, `7d87e79d…` | 6969, `953e9457…` | regenerated: four overrides, the base `6190e66`, and both paragraphs reading "Per kind: an analysis attempt that the signal aborts leaves no Run; an import discards its staged bytes;" |
| `s21/evidence/reading-report.json` | 20221, `d3e1e21e…` | 20341, `1a029013…` | regenerated: `productRev` `6190e66`, 92 successors, the per-kind line owned by S21 |
| `s21/evidence/build_s21.py` | 12937, `fefe6bbf…` | 14728, `c0efc511…` | The per-kind override is built from your text. It asserts that each line is free and outside S18, that the next line still begins "staged bytes;", and that the effective paragraph no longer contains the unqualified sentence. Also the base `6190e66`, the review path `codex2-s21-r2` and the unit draft. |
| `s21/evidence/check_s21.py` | 12763, `14a0316b…` | 14252, `0f44220b…` | Checks: <br>- four overrides; <br>- the per-kind pair is identical, and its `after` is your text verbatim and a single replacement inside the line; <br>- no bound entry on any of the four lines; <br>- the per-kind line reads into the next line on both parents; <br>- no code, exit or class in it; <br>- the WS:229, WSE:233 and SL:553 citations. <br>The default `--rev` is `6190e66`. |
| `s21/evidence/verify_scratch.py` | 7078, `9bca5434…` | 7082, `6c66187c…` | four overrides; the docstring's example base |
| `s21/README.md` | 18070, `d3aff5cc…` | 22312, `5548ad43…` | The new **r2 changes** table, plus updates for: <br>- the reviewer (Grok) and the base; <br>- LD-1, LD-2 and LD-6 (amended; your rejection recorded, WS:1393 kept per your R5); <br>- the J1 row table and "Why this form"; <br>- cross-law items 1 (item 13's row) and 6 (withdrawn); <br>- the review points, binding and the evidence runs. |

**RF-1, the fix.** Your replacement text, verbatim, on WS:229 and WSE:233:
- before: "Per kind: an analysis attempt aborts and leaves no Run; an import discards its"
- after: "Per kind: an analysis attempt that the signal aborts leaves no Run; an import discards its"

Both lines are free at `6190e66`. WSE:229 stays with S18. Each line still ends "an import discards its", so WS:230 and WSE:234 ("staged bytes; …") still join. WS:1393 is unchanged, as your R5 ruled.

## Checks run by the lead

Every check used `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`.
- **`build_s21.py`**, twice; the second run's `--check` reported identical bytes, the unit draft included.
- **`check_s21.py --rev 6190e66`**: 85 checks pass, no failures. 18 unbound records were scanned, and none touches an S21 selector.
- **`verify_scratch.py --rev 6190e66`**, design-only, passes. It takes the lock from 92 to 93 successors, with four overrides and no supersession. The inventory (`v135`) and the 100 inheritance rows are unchanged, and a later conflicting override of WS:226 is refused.
- **The r1-to-r2 record diff:** the r1 overrides and parents are unchanged, and two selectors are new, WS:229 and WSE:233.

## Decide

1. **Is RF-1 resolved?**
   - Are WS:229 and WSE:233 overridden with your text, with exact `before`s?
   - Do the lines still join "staged bytes;"?
   - Is WSE:229 left with S18?
   - Does the assembled paragraph now say nothing that contradicts the two exceptions?
2. **Nothing else changed.** Use `r1-members/` for the comparison. Is anything in r2 beyond RF-1, the base move and the records?
3. **Selection at `6190e66`.** Is the record well-formed under `verify_design`'s `contract_successor` and `successor_chain` rules, after S18 and SYN-NS? Is anything else wrong?

## Output

Write REVIEW.md and review.json. review.json must contain:
- `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`: each with id, location, problem, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectManifestSha256"`: a single string, the sha256 of `s21-subject.json`. The lead's value is `5aec0838da6794866bd22a57252b0300c638810d00e9f10db399ce1537ef2515`.
- `"successor"`: `{path, bytes, sha256}` of `s21/successor.json`. The lead's value is 6768 bytes, `df5ab70ac30b86783bf81e8b96ad1c1b4d7c8cd85d3acbc3ebc94f1496e46241`.

This is a contract successor, so it has no `inventoryCandidateAssessment`. One review maps exactly one subject. If you would change bytes, give the exact replacement text. Do not commit.
