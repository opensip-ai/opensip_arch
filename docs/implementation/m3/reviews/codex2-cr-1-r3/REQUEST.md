CODEX2 re-review: **CR-1 r3**, the security and DR-103 host-vocabulary contract successor for law M3-C item 7, after your r2 finding RF-CR1-2. This is a **design unit** (a `verify_design` contract successor). Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-DESIGN-UNIT** with `subjectManifestSha256`, or **REQUIRED-FINDINGS**.

Write only under `/tmp/opensip-implementation/reviews/codex2-cr-1-r3`.

**Lead note (reviewer change).** CODEX2 reviewed CR-1 r1 and r2; its reviews are copied in those directories. **GROK2** reviews r3, because CODEX2 is busy with the SYN units. The directory keeps its name, because the builder emits this review path. Write your output under `/tmp/opensip-implementation/reviews/codex2-cr-1-r3`. Don't run cargo.


**Rules:**
- **Read-only.** No repository edits, commits, pushes or delegation. Run git only read-only.
- **No builds or tests.** Run no cargo, no tests, no generator and no crash-matrix binary or checker.
- **Scripts.** If you run anything, use only the evidence scripts below and read-only commands, at `nice -n 19`, with any scratch files under your review directory.
- **`verify_design`.** Run it only through `evidence/verify_scratch.py`, which writes nothing and holds a synthetic review and assent in memory. Never edit the product or its lock.
- **Never touch the real home.** `~/Library/Application Support/OpenSIP` stays absent; do not read or create it.
- **Never read the private 413 UUID fixture.**

## Subject

The pins are in `hashes.txt`. The CR-1 files are still untracked in arch until acceptance.
- **The subject manifest** is `docs/implementation/m3/snapshot-plan-c/cr-1-subject.json`. Its sha256 is `subjectManifestSha256`.
- **Its 11 members** are r2's paths.
- **Not part of the subject:** `cr-1-unit.json`, the lead's DRAFT-PENDING-REVIEW record. It carries the r3 pins and the review path `docs/implementation/m3/reviews/codex2-cr-1-r3/review.json`. The builder emits that same path.

**Product.** Main is `392499e` (`392499e3a42ab9f45d517b8c267a83031abf3863`), read-only, with 83 contract successors. **CRC-1 is accepted at r4 (Grok) and bound as the 83rd.** r3 is built and checked against `design-lock.json@392499e`, read with `git show`. From `cd5958b` to `392499e` only `design-lock.json` changed. The security inputs, the generator, `component_manifest.rs`, the generated shape and both manifest fixtures are byte-identical at `9c11c53`, `cd5958b` and `392499e`.

## What r3 changes

The diff base is the r2 subject, `4e1b169b…`, which you reviewed. Its exact bytes for every changed member, and the r2 subject manifest, are in this directory's `r2-members/`, verified against the r2 pins.

**Unchanged byte for byte:**
- the successor copy `completion/manifest-schema.completed.v1.json` (`343dc517…`);
- `evidence/verify_scratch.py` (`f30ac855…`);
- the record's four passage overrides, its parents and its `standing`.

| Member | r2 | r3 | Change |
|---|---|---|---|
| `cr-1/materialization-map.json` | 3819, `c154a531…` | 4602, `e236abdb…` | **RF-CR1-2.** The `component_manifest.rs` instruction (`/alsoChangedByC2a/2/change`) is your replacement **verbatim**, followed by one added sentence that cites the line ranges, identical at `cd5958b` and `392499e`: `command_checks` spans 166-279; its command-tree checks are 171-256; its name and alias admission is 257-276; `validate_inner` calls it at 414 for both `validate` (395-397) and `validate_inventory` (398-403). Also `baseProductHead`, the base move. |
| `cr-1/README.md` | 29895, `525c3b0f…` | 32961, `eab85162…` | **RF-CR1-2:** LD-7's C2a bullet and CR-T7's last line are your replacements verbatim. **CR-T9** is your text verbatim, plus one sentence the lead directed: "(r3) In particular, a closure-only manifest with no `commands` whose name collides with a reserved or live name refuses on that existing route, in both `validate` and `validate_inventory`." **Also:** a new "r3 changes" section; r2's table rows rewritten as history; the base (`392499e`, 83, CRC-1 bound); the Files row for `verify_scratch.py`; Binding (`codex2-cr-1-r3`); reviewer points; evidence runs. |
| `cr-1/evidence/build_cr_1.py` | 27780, `04fc3c0c…` | 28591, `abcc30ac…` | Emits the map string above. Defaults to `392499e`. The unit template names `codex2-cr-1-r3` and the r3 assessment. |
| `cr-1/evidence/check_cr_1.py` | 11940, `00d1ef76…` | 13240, `a15710c3…` | Defaults to `392499e`. It adds RF-CR1-2 assertions: the map instruction starts with your exact text and cites 166-279, 171-256, 257-276, 414 and `validate_inventory`; the README carries CR-T9, the LD-7 bullet and the CR-T7 line; and the old whole-function gate sentence is gone. |
| `cr-1/evidence/audit_schema.py` | 7188, `9739bdc0…` | 7188, `e3f01709…` | Defaults to `392499e` (docstring and `REV`). |
| `cr-1/evidence/schema-audit.json` | 18532, `fa29df6d…` | 18532, `124099c8…` | `productRev`: `cd5958b` to `392499e`. Same fixture pin, same 11,010 verdicts, same 100 variants. |
| `cr-1/evidence/copies-report.json` | 6311, `00c7a1ad…` | 6311, `8d1528a2…` | `productHead` only. |
| `cr-1/PASSAGES.md` | 8234, `12db39aa…` | 8234, `d41997f2…` | Its header names `392499e` and 83 successors. The passage texts are unchanged. |
| `cr-1/successor.json` | 10694, `5ee9beac…` | 10694, `728fbcc8…` | Candidate pins only. The overrides, parents and `standing` are byte-identical. |

No contract text, schema or passage changes. RF-CR1-2 concerned C2a's instructions only, as you said. No completed-schema edit or extra parent override is made.

## Checks run by the lead

Every check used `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`, and each was run twice. `--deps` is a scratch directory holding jsonschema 4.25.1, installed offline from `~/opensip-deps/wheels`.
- **`audit_schema.py --deps <dir>`**: identical (11,010 cases, 100 variants).
- **`build_cr_1.py --check`**: identical, the unit draft included.
- **`check_cr_1.py`**: passes at `392499e` (the default), at `--rev cd5958b` and at `--rev 9c11c53`.
- **`verify_scratch.py --rev 392499e`**: **83 to 84**, with four overrides, no supersession, and inventory `v134` and 55 inheritance rows unchanged. CRC-1 is bound in this lock, so this run binds CR-1 with CRC-1.
- **`verify_scratch.py`** on the checkout at `392499e`: 83 to 84, with 40 generation sources and 48 admission sources verified.
- **At r2's base, `--rev cd5958b`:**
  - alone, 82 to 83;
  - with `--after-crc-1` and with `--before-crc-1`, 82 to 84 each. CRC-1's files on disk are its accepted r4, subject `ec896801…`, which is the subject the lock binds.

## Decide

1. **Is RF-CR1-2 resolved?** Do the map, LD-7, CR-T7 and CR-T9 make only command-tree validation conditional on `commands`? Does component-name and manifest-alias admission (duplicate keys, the reserved list, live names of a different `(stableId, provenance)`, and the coexistence exception) stay mandatory for every role, in both `validate` and `validate_inventory`? Are the cited line ranges right?
2. **The added text.** Is the map's added line-range sentence, and CR-T9's added sentence, correct and within your fix?
3. **Did anything else change?** Diff `r2-members/` against the r3 members. Only the changes above should appear.
4. **Does anything you accepted in r2 no longer hold at `392499e`**, with CRC-1 bound?

## Running the evidence (optional)

From `docs/implementation/m3/snapshot-plan-c/cr-1/`:
- Your r2 `deps` directory (`/tmp/opensip-implementation/reviews/codex2-cr-1-r2/deps`) can be reused for `evidence/audit_schema.py --deps <dir>`. Leave out `--write`.
- `evidence/build_cr_1.py --check`
- `evidence/check_cr_1.py`, and the same with `--rev cd5958b` or `--rev 9c11c53`
- `evidence/verify_scratch.py --rev 392499e`
- `evidence/verify_scratch.py`, which uses the checkout

`--after-crc-1` and `--before-crc-1` apply only to a lock that does not yet bind CRC-1, such as `cd5958b`.

## Output

Write REVIEW.md and review.json. review.json must contain:
- `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`: each with id, location, problem, evidence and fix;
- `"nonBlockingObservations"`;
- `"findingResolution"`: RF-CR1-2;
- `"subjectManifestSha256"`: a single string, the sha256 of `cr-1-subject.json`. The lead's r3 value is `24c880b436a48848d36c0e3a005ed8b5ec96ea7f66018c99b2fe49119de7d82f`.
- `"successor"`: `{path, bytes, sha256}` of `cr-1/successor.json`. The lead's r3 value is 10694 bytes, `728fbcc84e60850c842d56ac5c9c6867b2dec2da3de7967886d1337c1918b12b`.

This is a contract successor, so it has no `inventoryCandidateAssessment`. If you would change bytes, give the exact replacement. Do not commit.
