CODEX2 review: **I1-P**, the pack contract successor for `opensip.preview.typescript.pack:1`. It executes item 5 of the law M3-I1 r2 you accepted, which is X12c. This is a **design unit** (a `verify_design` contract successor) that depends on I1-L (`codex2-i1-l-r1`), so it is best reviewed after I1-L. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-DESIGN-UNIT** or **REQUIRED-FINDINGS**.

Write only under `/tmp/opensip-implementation/reviews/codex2-i1-p-r1`.

**Rules:**
- **Read-only.** No repository edits, commits, pushes or delegation. Run git only read-only.
- **No builds or tests.** A timing-sensitive crash-matrix lead set may be using this machine. Run no cargo, no tests and no crash-matrix binary or checker.
- **Scripts.** If you run anything, use only the evidence script below and read-only commands, at `nice -n 19`, with any scratch files under your review directory.
- **Never touch the real home.** `~/Library/Application Support/OpenSIP` stays absent; do not read or create it.
- **Never read the private 413 UUID fixture.**

## Subject

The pins are in `hashes.txt`. Every file is untracked in arch until acceptance.
- **The subject manifest** is `docs/implementation/m3/preview-pack-i1/i1-p-subject.json`. Its sha256 is `subjectManifestSha256`.
- **Its 8 members** are:
  - `i1-p/successor.json`;
  - `README.md`;
  - `pack-contract.json`, the record of the row, the digests and S1 to S10;
  - `materialization-map.json`;
  - `product/crates/evaluator/src/preview-typescript-pack.v1.policy.json`, the 5.2 document;
  - `product/crates/evaluator/src/pack-registry.json`, I1-c's whole new registry file;
  - `evidence/build_i1p.py`;
  - `evidence/digests.json`.
- **Not part of the subject:** `i1-p-unit.json`, the lead's DRAFT-PENDING-REVIEW record.

**Parents.** These are accepted once I1-L is bound ahead of I1-P:
- the law snapshot `PROPOSAL-r2.md`, an I1-L member;
- I1-L's design policy-document copy;
- I1-L's product policy-document copy.

If I1-L changes in review, I1-P is rebuilt on it and re-reviewed.

**Product.** Main is `e093e90` (F8b on top of `3e64266`; F8b changed no file this unit pins), read-only. I1-P changes no product byte. Unit I1-c ships the two data files, after I1-a and I1-b1.

## What it does

- **The document.** Its bytes are taken from the law's 5.2 block, not retyped: 574 B, `96675a5e…`, no trailing newline, its own canonical bytes.
- **The digests of 5.3**, recomputed with the design encoder `docs/coop/design-corrections/foundation/canonical.py` (IE:134). The exact-schema profile's encoder (`exact-schema-profile-selection-v1/reference/canonical.py`) gives the same bytes. All three equal the law's provisional values:
  - `programDigest`: `8e8936af…`;
  - `policySha256`: `96675a5e…`;
  - `ruleProgramDigest`: `e796f817…`, 457 B.
- **The row of 5.4**, exactly as the law prints it. It is placed in a full `pack-registry.json` whose `standing` names the law and states "one row" (LD-P1).
- **Schema admission,** checked with the exact-schema profile:
  - the document (`PolicyDocumentV2`) and its compiled `RuleProgramV2` are admitted under both of I1-L's policy-document copies;
  - both parents refuse it at `emitWhen`;
  - all four of I1-L's copies pass the Draft 2020-12 meta-schema;
  - I1-L's model admits the rule under the op law (2.2).
- **The self-checks S1 to S10**, recorded with the law's wording. S5 names this record's values, and S10 names I1-L's oracle (`cases-report.json`, cases `corpus-*`).
- **S6's pins at `3e64266`:** `policy_pack_tests.rs:638` asserts 7 `include_bytes!(`, and `&RELEASE_PACKS` appears twice.

## Decide

1. **Bytes and digests.**
   - Are the document bytes exactly law item 5.2?
   - Do the three digests follow 5.3's recipes?
   - Does the compiled RuleProgramV2 in `digests.json` match the shape `compile_program` builds (`policy.rs:584-606`)?
   - Recompute independently if you like.
2. **Row and registry.**
   - Is the row exactly 5.4, with the key set `policy.rs:953-965` enforces?
   - Is the registry file well-formed for `PackRegistry::rows` (`policy.rs:930-1023`)? Is its `standing` right?
   - Rule on LD-P1 (I1-P fixes the whole file).
3. **Admission.** Is the schema evidence sound? Are the X12 item 6 steps it does not cover (6.2's imperative classifier and the product rule law) correctly left to I1-c's S3?
4. **Self-checks.** Are S1 to S10 complete and exact for I1-c and, for S10, I1-b2? Is S5's binding to this record's values unambiguous?
5. **Structure.** Rule on LD-P2 to LD-P5:
   - the record layout;
   - the encoder choice;
   - the parents and binding order;
   - S10's oracle.

   Is the successor well-formed for selection after I1-L? Is anything else wrong?

## Running the evidence (optional)

Use `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`.

1. **Dependencies.** Install `jsonschema` offline into your review directory: `python3.14 -m pip install --no-index --no-cache-dir --find-links ~/opensip-deps/wheels --target /tmp/opensip-implementation/reviews/codex2-i1-p-r1/deps jsonschema==4.25.1`.
2. **Build check.** `docs/implementation/m3/preview-pack-i1/i1-p/evidence/build_i1p.py --product /Users/sb/code/opensip-ai/opensip --deps <that dir> --check` recomputes everything, re-validates, and compares the result with the files on disk. It reads the product lock and one base blob read-only.

The lead ran it twice, with byte-identical results.

## Output

Write REVIEW.md and review.json. review.json must contain:
- `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`: each with id, location, problem, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectManifestSha256"`: a single string, the sha256 of `i1-p-subject.json`. The lead's value is `f051269c6c7fa4856ed58040efd56a3508eca9846135d91dae7a2841f6293791`.
- `"successor"`: `{path, bytes, sha256}` of `i1-p/successor.json`. The lead's value is 2598 bytes, `3cb6d4855d1523376ae9e3eb8941f1905f73a2d74639663db58296533f85f9ac`.

This is a contract successor, so it has no `inventoryCandidateAssessment`. If you would change bytes, give the exact replacement. Do not commit.
