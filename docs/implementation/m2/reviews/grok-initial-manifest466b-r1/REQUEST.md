Grok review 466b (P0 manifest producers) and inventory72, r1. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-initial-manifest466b-r1. You own the serial native lane until your report is written. Host macOS 27.0. Rust is /opt/homebrew/Cellar/rust/1.95.0/bin. Use cargo --locked --offline. Do not read or print the private 413 UUID fixture.

Law: docs/implementation/m2/initial-publication-467/PROPOSAL.md, "The P0 tree" and item 5 (accepted). Product HEAD d9d2779. The uncommitted files are pinned in hashes.txt:
- new: crates/security/src/custody/initial_manifest.rs;
- initial_publication.rs: `pub(crate)` items, `verify_files`, `Error::Path`;
- root_payload.rs: a re-export and `#[allow(private_interfaces)]`, as for initial_core and initial_platform;
- trust.rs and custody.rs: module wiring;
- installation_fence.rs: `CARRIER` becomes `pub(super)`, so the fence name has one source.

## Summary

- **`initial_manifest::build`** wraps 466's `build`. It charges `MANIFEST_COST` and encodes the registry v2, node and pair canonically. Every new file is decoded with its existing decoder. The fence must be empty. The tree must be closed and parents first. It yields exactly 14 directories and 11 files, in law order with the pair last. Exact bytes:
  - registry: `{"entries":[],"schemaVersion":2}`
  - marker: `{"schemaVersion":1,"storeInstanceId":"S"}`
  - node: `{"predecessor":null,"schemaVersion":1,"selectedByIntentDigest":null,"stateSchema":K,"storeGeneration":0,"storeInstanceId":"S"}`
  - pair: `{"coreClosure":"C","selectionSchema":1,"stateSchema":K,"storeGeneration":0,"storeInstanceId":"S"}`
- **`initial_publication::verify_files`** re-runs the 466 verifiers over reread trust bytes. Each path must equal the locator computed from its bytes, and the count and a 32 KiB bound are checked before any charge.
- **`cross_joins`** checks every join in law item 5: marker, staging name, closure, the S/0/K agreement, the node path, the platform, the invocation, and stepId 0.

## Deviations for your judgement

1. **Lineage path.** The inventory permits lifecycle→security and not security→lifecycle, so `node_path` spells `lineage::relative_path`'s format itself, from identity's `LineageKey`. The test checks it against a literal. The two spellings could drift. The alternative is to move the spelling into identity, as a follow-up.
2. **Test vector.** The inputs275 vector has four real hashes. The descriptor (ae8dda9f…) and capsule (6fd82e12…) are pinned as this build's regression values.
3. **Row role.** The v72 row role is `service`; `builder` may fit better.
4. **Build versus joins.** `build` accepts a non-zero stepId, as 466 did; only `cross_joins` refuses it.

## Inventory72

v71 plus crates/security/src/custody/initial_manifest.rs, for 727 rows. The helper is byte-identical and gives PASS. Scratch verify_design with v72 passed.

## Lead's replay

The security lib is 514/0. The workspace is 1039/0. One run hit a known pre-existing shared-temp-directory race in `installation_observation::native_descendant_earlier_ancestor_changes_during_capture_and_consumption_refuse` (ChangedDuringRead); it passed on rerun and is logged for the same isolation fix. Clippy and fmt pass.

## Decide

Are the bytes, order and tree exactly the law's? Does every file round-trip through its decoder? Are `verify_files` and `cross_joins` complete for item 5? Is every charge made before its work? Are the deviations acceptable? Is v72 exactly v71 plus one row?

**Output format:** review.json must contain:
- "verdict": ACCEPT-UNIT or REQUIRED-FINDINGS;
- "requiredFindings";
- "subjectManifestSha256": a single string, from subjects.txt;
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes and sha256 of repository-file-inventory.v72.json, parent (v71 pin), successorRecord (the pin of initial-manifest-inventory-v72/successor.json)}.

Write REVIEW.md and review.json. Do not commit.
