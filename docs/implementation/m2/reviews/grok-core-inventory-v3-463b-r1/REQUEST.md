Grok review unit 463b, r1: `CoreInventoryV3` code and contract successor. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-core-inventory-v3-463b-r1. You own the serial native lane until your report is written. Host macOS 27.0. Rust is /opt/homebrew/Cellar/rust/1.95.0/bin. Use cargo --locked --offline. Do not read or print the private 413 UUID fixture.

Law: docs/implementation/m2/initial-core-launch-463/PROPOSAL.md, r3 plus the r5 amendment item 6 (accepted).

## Subjects

1. **Product code**: seven uncommitted files on 4c43c70, pinned in hashes.txt:
   - the trust-record schema, which adds `CoreInventoryV3` and `CorePlatformV3`, appended after `WalkRecord`;
   - sources.json and reference-registry.json (schema sha);
   - record_shapes.py and record_visits.py (asserted schema sha);
   - the regenerated trust_record_shape_nodes.rs;
   - core_inventory.rs: opt-in `project_v3`, `state_writer()`, `required_code_signing_flags()`, the `CODE_SIGNING_FLAGS` table, and tests.

   V2 `project` is unchanged. Neither reader accepts the other schema.
2. **Contract successor** docs/implementation/m2/core-inventory-v3-selection-v1/ (subject pin in subjects.txt). Read its README for the decisions and the flag table, which is sourced from the macOS 27.0 SDK Kernel.framework kern/cs_blobs.h.

**Parents question.** None of the seven files was ever selected by a contract unit, and verify_design needs a nonempty parent list. The helper named two accepted, unchanged law documents as parents: security-and-lifecycle.md and security_lifecycle_model_v1.py, with no passage overrides. Is that an acceptable parent choice? If not, what should the parents be?

## Lead's replay

The security lib passed 455/0 while the 458b files were also present; 458b is now committed at 4c43c70. The helper reports that the 318 corpus still passes (125 cases, 53 positive), that the record270 corpora are unchanged, and that generate_security_tables.py --check passes. In a scratch pair with a provisional review and assent appended at contractSuccessors index 67, verify_design --implementation passed with 68 contract units.

## Decide

Does the code implement item 6 exactly? Check:
- `stateWriter` in {1, 2} and required;
- the flags are a closed, sorted, unique set that must contain CS_VALID;
- the bit values are correct;
- there is no default K or flags;
- V2 is unchanged and its corpora keep their results;
- the appended node numbering leaves 0–554 and the visitor file unchanged.

Are the schema pins complete? Are the successor, its README and its parents right?

**Output format (the verifier needs this exact shape):** review.json must contain top-level "verdict" (`ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`), "requiredFindings", and "subjectManifestSha256" as a single string: the sha256 of docs/implementation/m2/core-inventory-v3-selection-v1-subject.json. Replay the security lib, generate_security_tables.py --check, workspace clippy and fmt. Write REVIEW.md and review.json. Do not commit.
