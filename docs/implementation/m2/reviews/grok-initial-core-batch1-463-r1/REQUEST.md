Grok review 463 batch 1 (463e, 463f-1, 463f-2) and inventory69, r1. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-initial-core-batch1-463-r1. You own the serial native lane until your report is written. Host macOS 27.0. Rust is /opt/homebrew/Cellar/rust/1.95.0/bin. Use cargo --locked --offline. Do not read or print the private 413 UUID fixture.

Law: docs/implementation/m2/initial-core-launch-463/PROPOSAL.md, r3 through r8 (all accepted). Product HEAD 0786537. The uncommitted files are pinned in hashes.txt.

## Code

- **463e**, new crates/security/src/trust/core_release_embedding.rs (included in root_payload.rs):
  - `EmbeddedRootBinding` and `EmbeddedCoreRelease`, with const-fn constructors whose `assert!` helpers follow reporting/assets.rs `CompiledBuildSelection`;
  - `EMBEDDED_CORE_RELEASE = new(None, None, None)` and `COMPILED_PLATFORM` from cfg!;
  - `admit()`, whose absences are checked in order `EmbeddingAbsent::{Root, Entrypoint, Bootstrap}`;
  - path rules: at most 4096 bytes, at most 32 components of 1 to 255 bytes, `[A-Za-z0-9._-]`, no leading dot; the two paths differ, neither is a prefix of the other, and neither begins with `inventory.json` or `inventory.sig.json`.
- **463f-1**, platform macos_image.rs: `RunningImageObservation::leaf_name_matches_accounted(work) -> bool`, the exact on-disk spelling of the retained leaf, charged.
- **463f-2**:
  - core_inventory.rs: `ProjectionV3::into_parts`.
  - core_anchor.rs: `capture_with(.., InventorySchema)`, which is `pub(super)` because core_authentication is a sibling; `capture` stays V2. `CapturedCore::release()` gives `ReleaseMembers { state_writer, required_flags }` for the anchor platform's row, V3 only.
  - core_authentication.rs: `authenticate` stays V2, the private `authenticate_with` is added, and `authenticate_embedded_release` is now V3 only (law item 6). The synthetic builder now emits V3, and the positive tests assert `release() == (2, CS_VALID)`. A V2 release is refused by the embedded path, and a V3 one by the V2 path.

## Inventory69

docs/implementation/m2/initial-core-inventory-v69/ (subject pin in subjects.txt) is v68 plus three planned rows:
- core_release_embedding.rs (configuration)
- initial_core.rs (validator)
- initial_core_tests.rs (test)

That makes 721 rows. The projection helper is byte-identical; its run gave PASS with 5 rows and 28 corruptions refused. initial_core.rs and initial_core_tests.rs do not exist yet; they are planned rows for 463f-3 and 463g.

## Lead's replay

security lib 468/0; platform lib 171/0; clippy `-D warnings` and fmt pass. A scratch verify_design with v69 selected passed.

## Decide

Does the code implement items 1, 2, 3, 6 and the embedded-values part of r3 exactly? Are the compile-time checks sufficient, with no runtime path, env!, or caller input? Is V2 behaviour unchanged everywhere, and is the V3 selection in capture_with correct for the anchor platform's row? Is the leaf check honest? Is v69 exactly v68 plus three rows with a correct projection?

**Output format (the verifier needs this exact shape):** review.json must contain:
- "verdict": ACCEPT-UNIT or REQUIRED-FINDINGS;
- "requiredFindings";
- "subjectManifestSha256": a single string, the sha256 of docs/implementation/m2/initial-core-inventory-v69-subject.json;
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes and sha256 of repository-file-inventory.v69.json, parent {path, bytes, sha256 of v68}, successorRecord {path, bytes, sha256 of initial-core-inventory-v69/successor.json}}.

Replay the security and platform libs, workspace clippy and fmt. Write REVIEW.md and review.json. Do not commit.
