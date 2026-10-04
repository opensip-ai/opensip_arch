GROK2 re-review: **S18 r2**, the final-output-section contract successor of the host pipeline law M3-J1, after your r1 finding. This is a **design unit** (a `verify_design` contract successor). Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-DESIGN-UNIT** with `subjectManifestSha256`, or **REQUIRED-FINDINGS**.

Write only under `/tmp/opensip-implementation/reviews/codex2-s18-r2`.

(Lead note: the directory keeps the name `codex2-s18-*` because the unit's builder emits that review path. You reviewed r1 in `codex2-s18-r1/`. Your r1 review is copied there, and its status is REQUIRED-FINDINGS. Judge whether RF-1 is resolved. Don't run cargo.)

**Rules:**
- **Read-only.** No repository edits, commits, pushes or delegation. Run git only read-only.
- **No builds or tests.** Run no cargo, no tests, no generator and no crash-matrix binary or checker.
- **Scripts.** If you run anything, use only the evidence scripts below and read-only commands, at `nice -n 19`, with any scratch files under your review directory.
- **`verify_design`.** Run it only through `evidence/verify_scratch.py`, which writes nothing and holds a synthetic review and assent in memory. Never edit the product or its lock.
- **Never touch the real home.** `~/Library/Application Support/OpenSIP` stays absent; do not read or create it.
- **Never read the private 413 UUID fixture.**

## Subject

The pins are in `hashes.txt`. The S18 files are still untracked in arch until acceptance.
- **The subject manifest** is `docs/implementation/m3/host-pipeline-j/s18-subject.json`. Its sha256 is `subjectManifestSha256`.
- **Its 8 members** are the same paths as r1.
- **Not part of the subject:** `s18-unit.json`, the lead's DRAFT-PENDING-REVIEW record. It now carries the r2 pins and the review path `docs/implementation/m3/reviews/codex2-s18-r2/review.json`.

**Product.** Main is `392499e` (`392499e3a42ab9f45d517b8c267a83031abf3863`), read-only. It binds CRC-1, so its lock has 83 contract successors.
- **Lock pin:** `design-lock.json@392499e` (335,667 bytes, `d1b2a5d1…`), read with `git show`, not the live file.
- **r1's base** was `cd5958b` (82). Between the two commits only `design-lock.json` changed. `verify_design.py`, INV5, ENV7, `bootstrap.rs` and `delivery.rs` are byte-identical, so every product citation stands.
- **CRC-1's selectors** are WS:308 and WSE:312. They are not S18's.

**Law.** M3-J1 r4 (`host-pipeline-j/PROPOSAL-r4.md`, `c18c0d3c…`, your r4 acceptance), with CODEX2's J1 r3 observations NB-01 and NB-02.

## What r2 changes

The diff base is the r1 subject, `9d184011…`, which you reviewed. Its exact bytes are in this directory's `r1-members/`: the r1 subject manifest and the seven r1 members r2 changes, each verified against the r1 pins. The eighth member, `s18/operability/PLAN.md`, is unchanged (74,185 bytes, `69af0f1b…`).

| Member | r1 | r2 | Change |
|---|---|---|---|
| `s18/successor.json` | 13062, `5407ce51…` | 15617, `e83430ad…` | **RF-1:** four new line overrides: WS:227, WS:228, WSE:229 and WSE:230. **One changed `after`:** WS:231 and WSE:235, the settlement sentence. Also the `standing` (ten overrides; the after-settle lines named) and the candidate pins. The parents, the six r1 selectors and their `before`s, and the other four r1 `after`s are byte-identical. |
| `s18/PASSAGES.md` | 16287, `1de15a0d…` | 18079, `89925827…` | regenerated: the ten overrides; the header names the base `392499e` |
| `s18/evidence/copies-report.json` | 11638, `15f2f1ed…` | 12920, `aa1ecade…` | regenerated: `productRev` `392499e`, the four new roles, and the bound entries on WS and WSE now including CRC-1's |
| `s18/evidence/build_s18.py` | 26386, `2759405d…` | 29436, `ca07d88b…` | the after-settle overrides, built per parent as one insertion each and asserted to read correctly across both lines; base `392499e`; review path `codex2-s18-r2`; the unit draft's assessment |
| `s18/evidence/check_s18.py` | 15896, `9a5729ba…` | 17351, `218d3333…` | default `--rev 392499e`; ten overrides; the shared pairs; each after-settle line a single insertion; the parenthetical read across both lines on both parents; the settlement-point sentence |
| `s18/evidence/verify_scratch.py` | 6938, `53a51f41…` | 6952, `bda2da4e…` | ten overrides; the docstring's example base |
| `s18/README.md` | 28082, `3e15ea0a…` | 34581, `9fa4203e…` | The new **r2 changes** table, plus updates for the reviewer (GROK2), the base, LD-2, LD-4, LD-5 and LD-9, cross-law items 1d, 1g, 2 (NBO-2) and 4 (NBO-1), the review points, binding and the evidence runs |

**RF-1, the fix.** The *after-settle* parenthetical spans two lines on each parent. Both lines are overridden, so that after-settle is defined by the settlement point, as the lead directed. Each `after` is its own `before` with one insertion:

| Line | Insertion |
|---|---|
| WS:227, WSE:229 | "*after-settle* (every required step" becomes "*after-settle* (after the settlement point: every required step" |
| WS:228, WSE:230 | "already terminal):" becomes "already terminal and, where the final output section below applies, the required output returned):" |

Read across both lines, each parent now says: "*after-settle* (after the settlement point: every required step already terminal and, where the final output section below applies, the required output returned): the aggregate is **not reclassified**; the settled class stands."
- WSE:229 begins "status affects gating, not commit identity.", and WSE:230 ends "Settled aggregates retain the required-step D9". Those words are kept.
- In the paragraph, "The invocation settles when the output returns and not earlier, so *after-settle* begins only then" now reads "…and not earlier: that return is its settlement point, so *after-settle* begins only then".
- The plan copy's row E already says the same: "Every required step terminal and the required output returned".

This differs from RF-1's suggested text in two ways:
- the opening line is overridden too, to name the settlement point;
- the conjunct reads "the required output returned" rather than "only once that section's required output has returned".

The meaning is the same. README LD-4 records the choice.

**NBO-1 and NBO-2, recorded, not applied.**
- **NBO-1** is README cross-law item 4. When the invocation-record owner restates INV5's after-settle description, it takes RF-1's conjunct. INV5 is not changed, because LD-5 keeps phase O out of that record.
- **NBO-2** is README cross-law item 2. O1 carries row O's qualifier: S-OP-2 r6:653's "100 ms on cancellation" means a decided `interrupted` envelope. The copy's row O already says this, so the copy is unchanged.

## Checks run by the lead

Every check used `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`.
- **`build_s18.py`**, twice; the second run's `--check` reported identical bytes, the unit draft included.
- **`check_s18.py --rev 392499e`**: 133 checks pass, no failures. They cover:
  - the pins;
  - no lock entry on any of the ten selectors;
  - no unbound record touching them;
  - the copy's alignment;
  - the content;
  - every citation.
- **`verify_scratch.py --rev 392499e`**, design-only, passes. It takes the lock from 83 to 84 successors, with ten overrides and no supersession. The inventory (`v134`) and the 55 inheritance rows are unchanged, and a later conflicting override of WS:231 is refused.
- **The r1-to-r2 record diff:**
  - the six r1 selectors are kept, with the same parents and `before`s;
  - only the WS:231 and WSE:235 `after`s change;
  - four selectors are new.

## Decide

1. **Is RF-1 resolved?**
   - Do WS:227-228 and WSE:229-230 now define *after-settle* by the settlement point, with every required step terminal and, where the final output section applies, the required output returned?
   - Is each of the four `before`s the exact parent line, and each `after` that line with only the stated insertion?
   - Does the paragraph's settlement sentence agree?
2. **The partition.** Where the section applies, are *before-settle* (WS:225, unchanged), *final-output* (the paragraph) and *after-settle* (WS:227-228) now disjoint and exhaustive, an interrupted invocation included? Elsewhere, does every reading stay as before?
3. **The observations.** Are NBO-1 and NBO-2 recorded where they belong?
4. **Nothing else changed.** Use `r1-members/` for the comparison. Is anything in r2 beyond RF-1, the settlement sentence, the base move and the records?
5. **Selection at `392499e`.** Is the record well-formed under `verify_design`'s `contract_successor` and `successor_chain` rules, after CRC-1? Is anything else wrong?

## Output

Write REVIEW.md and review.json. review.json must contain:
- `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`: each with id, location, problem, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectManifestSha256"`: a single string, the sha256 of `s18-subject.json`. The lead's value is `d22282a3e91728256ba509e0976f9bf4f1fa2b0fb58bb2fc3318a5a236ffc403`.
- `"successor"`: `{path, bytes, sha256}` of `s18/successor.json`. The lead's value is 15617 bytes, `e83430adfb20730566721274e9ef5e6688adca6b743039d16a5baf881f0e1503`.

This is a contract successor, so it has no `inventoryCandidateAssessment`. One review maps exactly one subject. If you would change bytes, give the exact replacement text. Do not commit.
