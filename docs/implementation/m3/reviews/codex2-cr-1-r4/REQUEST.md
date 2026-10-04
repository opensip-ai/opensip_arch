GROK2 re-review: **CR-1 r4**, the security and DR-103 host-vocabulary contract successor for law M3-C item 7, after your r3 finding RF-CR1-3. This is a **design unit** (a `verify_design` contract successor). Claude Opus 5.5 leads, and you are the single reviewer. The directory keeps the `codex2-` prefix, as r3's did. Verdict wanted: **ACCEPT-DESIGN-UNIT** with `subjectManifestSha256`, or **REQUIRED-FINDINGS**.

Write only under `/tmp/opensip-implementation/reviews/codex2-cr-1-r4`.

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
- **Its 11 members** are r3's paths.
- **Not part of the subject:** `cr-1-unit.json`, the lead's DRAFT-PENDING-REVIEW record. It carries the r4 pins and the review path `docs/implementation/m3/reviews/codex2-cr-1-r4/review.json`. The builder emits that same path.

**Product.** Main is `5e25d04` (`5e25d04b3bfa85a244f5d958fe089e9626fd33fa`, P0's integration), read-only, with 87 contract successors. CRC-1 has been bound since `392499e`. r4 is built and checked against `design-lock.json@5e25d04`, read with `git show`, not the live file.

From `392499e` to `5e25d04`, none of these changed: the security inputs, the generator, `crates/security/src/component_manifest.rs`, the generated shape, both manifest fixtures and `tools/verify_design.py`. The line numbers you cited (`268-276`, `395-414`) hold at `5e25d04`.

## What r4 changes

The diff base is the r3 subject, `24c880b4…`, which you reviewed. Its exact bytes for every changed member, and the r3 subject manifest, are in this directory's `r3-members/`, verified against the r3 pins.

**Unchanged byte for byte:**
- the successor copy `completion/manifest-schema.completed.v1.json` (`343dc517…`);
- `evidence/verify_scratch.py` (`f30ac855…`);
- the record's four passage overrides, its parents and its `standing`;
- the map's `component_manifest.rs` instruction, including its line-range sentence, which is left as you asked.

| Member | r3 | r4 | Change |
|---|---|---|---|
| `cr-1/README.md` | 32961, `eab85162…` | 35706, `1898c3a2…` | **RF-CR1-3.** CR-T9's added sentence is replaced by your text **verbatim**. CODEX2's CR-T9 paragraph before it is unchanged. **The entry-point audit:** every other sentence naming `validate` or `validate_inventory` was re-read against `component_manifest.rs:395-414` and is unchanged, because it already holds. These are the map's line-range sentence and r3's table row, both of which say `validate_inner` calls `command_checks` at 414 for both entry points. LD-7's bullet and CR-T7 name no entry point. **README audit:** a new "r4 changes" section; r3's rows rewritten as history, with a note that r4 corrects CR-T9's sentence; the status (Draft r4, GROK2); the base (`5e25d04`, 87); the parents' and the lock's base; Binding (`codex2-cr-1-r4`); reviewer points; evidence runs. |
| `cr-1/evidence/check_cr_1.py` | 13240, `a15710c3…` | 14024, `58d710fe…` | Asserts your corrected sentence exactly, and that r3's "reserved or live name … in both" sentence is gone. Defaults to `5e25d04`. |
| `cr-1/evidence/build_cr_1.py` | 28591, `abcc30ac…` | 28589, `a6ee94b3…` | Defaults to `5e25d04`. The unit template names `codex2-cr-1-r4` and the r4 assessment. |
| `cr-1/evidence/audit_schema.py` | 7188, `e3f01709…` | 7188, `6af97ebb…` | Defaults to `5e25d04` (docstring and `REV`). |
| `cr-1/evidence/schema-audit.json` | 18532, `124099c8…` | 18532, `d80196b3…` | `productRev` only. The verdicts are unchanged: 11,010 cases, 100 variants. |
| `cr-1/evidence/copies-report.json` | 6311, `8d1528a2…` | 6311, `36c488db…` | `productHead` only. |
| `cr-1/materialization-map.json` | 4602, `e236abdb…` | 4602, `1e4c31cf…` | `baseProductHead` only. |
| `cr-1/PASSAGES.md` | 8234, `d41997f2…` | 8234, `e68e1ec2…` | Its header names `5e25d04` and 87 successors. |
| `cr-1/successor.json` | 10694, `728fbcc8…` | 10694, `0f1e187b…` | Candidate pins only. |

## Checks run by the lead

Every check used `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`, and each was run twice. `--deps` is a scratch directory holding jsonschema 4.25.1, installed offline from `~/opensip-deps/wheels`.
- **`audit_schema.py --deps <dir>`**: identical (11,010 cases, 100 variants).
- **`build_cr_1.py --check`**: identical, the unit draft included.
- **`check_cr_1.py`**: passes at `5e25d04` (the default), and at `--rev 392499e`, `--rev cd5958b` and `--rev 9c11c53`.
- **`verify_scratch.py --rev 5e25d04`**: **87 to 88**, with four overrides and no supersession. The selected inventory (`repository-file-inventory.v135.json`) and the inheritance projection (100 rows) are unchanged.
- **`verify_scratch.py`** on the checkout at `5e25d04`: 87 to 88, with 40 generation sources and 48 admission sources (15 aliases) verified.
- **Earlier bases:**
  - `--rev 392499e`: 83 to 84;
  - `--rev cd5958b`: 82 to 83 alone, and with `--after-crc-1` or `--before-crc-1`, 82 to 84 each.

## Decide

1. **Is RF-CR1-3 resolved?** Is CR-T9's sentence exactly your replacement? Does it now match `component_manifest.rs:268-276` and `:395-414`: a reserved-name collision refuses in both entry points, and a live-name collision of a different `(stableId, provenance)` refuses in `validate` only and stays inventory-valid in `validate_inventory`?
2. **The entry-point audit.** Does every other sentence that names `validate` or `validate_inventory` match the product?
3. **Did anything else change?** Diff `r3-members/` against the r4 members. Only the changes above should appear.
4. **Does anything you checked in r3 no longer hold at `5e25d04`?**

## Running the evidence (optional)

From `docs/implementation/m3/snapshot-plan-c/cr-1/`:
- **Dependencies:** `python3.14 -m pip install --no-index --no-cache-dir --find-links ~/opensip-deps/wheels --target /tmp/opensip-implementation/reviews/codex2-cr-1-r4/deps jsonschema==4.25.1`, then `evidence/audit_schema.py --deps <that dir>`. Leave out `--write`.
- `evidence/build_cr_1.py --check`
- `evidence/check_cr_1.py`, and the same with `--rev 392499e`
- `evidence/verify_scratch.py --rev 5e25d04`
- `evidence/verify_scratch.py`, which uses the checkout

## Output

Write REVIEW.md and review.json. review.json must contain:
- `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`: each with id, location, problem, evidence and fix;
- `"nonBlockingObservations"`;
- `"findingResolution"`: RF-CR1-3;
- `"subjectManifestSha256"`: a single string, the sha256 of `cr-1-subject.json`. The lead's r4 value is `e9e1a406dcf9e75d2359b609087e80327ab1f47554eb094425b2e3ae8ef781ba`.
- `"successor"`: `{path, bytes, sha256}` of `cr-1/successor.json`. The lead's r4 value is 10694 bytes, `0f1e187b0af676bb3face09a5d0055a75a77a0d898071763a2952d487a3ce9f8`.

This is a contract successor, so it has no `inventoryCandidateAssessment`. If you would change bytes, give the exact replacement. Do not commit.
