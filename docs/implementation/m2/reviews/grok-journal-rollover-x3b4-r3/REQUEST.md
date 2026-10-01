Grok review: X3b-4 r3, a narrow recheck of r2's RF-1 only (inventory v108 standing). Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-journal-rollover-x3b4-r3. If you build or test, use a CARGO_TARGET_DIR under that directory. Run git only read-only, and only against the worktree below.

## Scope

Your r2 review (`/tmp/opensip-implementation/reviews/grok-journal-rollover-x3b4-r2/review.json`) returned REQUIRED-FINDINGS with one finding.
- **RF-1.** The standing sentence in `repository-file-inventory.v108.json` and in `journal-rollover-x3b4-inventory-v108/successor.json` named law X3b r8. Both must name law X3b r10, with inherited rows kept by value.
- **Everything else** in r2 is unchanged: the law (X3b r10, `PROPOSAL-r10.md`, `25a60824…`), the base, the parent, the product source, and all judgment calls. The r2 request is pinned in hashes.txt for reference.

Please recheck RF-1 only, and confirm that nothing else moved.

## What changed

The only edit is in `journal-rollover-x3b4-inventory-v108/evidence/build_v108.py`. Its two standing strings now read `law X3b r10, unit X3b-4`:
- the candidate's: `PROPOSED additive grant-generation rollover layout (law X3b r10, unit X3b-4); no release, custody, profile, boot or creator qualification`;
- the successor record's: `PROPOSED additive grant-generation rollover layout (law X3b r10, unit X3b-4); independent review and lead assent required`.

v108 and successor.json were rebuilt from it on the same parent. Each grew by one byte (r8 → r10):

| file | r2 | r3 |
|---|---|---|
| repository-file-inventory.v108.json | 372606, `54f505f2…` | 372607, `000ec2ac87208bded12c94d91692530780d0ad75e32cdc6806fa89a05f692040` |
| successor.json | 20205, `3c1dc96a…` | 20206, `ce9dccd7633925b8ce0613f4527cbc6213c7fd5d79592d70b40c7c69475a445d` |
| build_v108.py | 11818, `28deee34…` | 11820, `bd011a6852d4d124b5e7ba94afb431346365052cec229dae4b9dcc9ed66ee19d` |
| subject manifest | `ce257add…` | `5fdf62b62b42ff7104cfe26c150314185c86c9f77b05f8270762db0baee85516` |

No other file under `journal-rollover-x3b4-inventory-v108/` changed. That includes the README, the verify helpers, verifier-anchor.json and the verification records; verification.stdout was regenerated with identical bytes.

## Unchanged

- **Product.** The worktree `/Users/sb/code/opensip-ai/opensip-x3b4` is still detached at f1b8321, with v112 selected; main is still f1b8321. The product diff is unchanged: sha256 `a53c78f97742497506bacdf5574c8d5c6dbd005449ed61d711cefbb7ea6aaf13`, 163034 bytes, equal to your r2 `productDiffSha256`. All nine product pins in hashes.txt equal r2's.
- **Parent.** v112: `repository-file-inventory.v112.json`, 365881 bytes, sha256 `acfc4bc9cc896bab1f916d4a06eb6adc87bab89b2a1c809696dba09b13c7473a`.
- **Inherited rows.** The builder still asserts every inherited row equal by value (789 rows) and the non-file members unchanged, and it still adds exactly the two rows.

## Checks

- `build_v108.py` (run twice) reproduces the same bytes: parent inventory112, 791 files, 2 added, 16 projection rows.
- `grep "law X3b r8"` finds nothing in v108 or successor.json.
- verify_projection against the real lock at f1b8321: PASS, 16 rows, 83 corruptions refused.
- verify_scratch (v108 appended over the real lock at f1b8321) passes: 74 inventory successors, 72 contract successors, 16 inheritance rows, v108 selected.
- No product file changed, so no workspace run was repeated. r2's checks stand: workspace 1445/0/3, clippy, fmt and `check_package_edges --lane host`.

## Decide

- Is RF-1 closed?
- Is v108 otherwise byte-for-byte r2's apart from the standing?
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": the sha256 of `journal-rollover-x3b4-inventory-v108-subject.json` (`5fdf62b6…`);
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes, sha256 of v108, parent (the v112 pin), successorRecord}.

Write REVIEW.md and review.json. Do not commit.
