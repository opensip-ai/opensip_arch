Grok review 466 r1: the P0 trust publication producer and inventory66. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-initial-publication466-r1. You own the serial native lane until your report is written. Rust is /opt/homebrew/Cellar/rust/1.95.0/bin. Use cargo --locked --offline in /Users/sb/code/opensip-ai/opensip. Do not read or print the private 413 UUID fixture.

Product HEAD 4e0cb7b. Pins of the four paths are in hashes.txt beside this request; `git status` must show exactly those (three modified, one new). Owner text: /Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/initial-root-binding-owner-selection-v1/owner.md §2 (the initial complete tree and the budget).

## The unit

- New crates/security/src/trust/initial_publication.rs, included in root_payload.rs as a sibling of trust_input_bindings. `build(inputs, work)` checks input lengths before any charge, charges a fixed build cost, then builds with the canonical encoder and the closed shape for each record: the 72-byte store marker record, CreationInputV1, the creation OperationInputV1, CreationEventV1, the initial PublicationDescriptorV1 (afterProjection is the capsule without `publication`; one event with roleChange null; nativeBefore and previousCapsule null) and the P0 TrustCapsuleV1 (revision 1, unevaluated clock, all six roles ST-UNBOOTSTRAPPED, publication pinning the descriptor bytes). It then runs `trust_input_bindings::creation`, `capsule_consistency` (no predecessor) and `publication_events::bind_events` (blank roles, null head) through `Budget::borrowed(work)` over an in-memory store of exactly the built records and event. Paths come from the trust locator (`locator_components`, a new pub(super) accessor on the existing `Locator` in native_record_capture.rs) and, for state.v1, from `current_parents` and `CURRENT_LEAF` now shared with native_current.rs's own reader.
- Inputs (S, K, core closure, platform, staging nonce, observation anchor, request/step/execution ids) are supplied by the caller. Their producers (InitialCore, InitialPlatform, the stage, ingress) are later units; nothing here mints them. Nothing is read from or written to disk. Nothing outside security can call this yet.
- Inventory66 (docs/implementation/m2/initial-publication-inventory-v66/, repository-file-inventory.v66.json, subject manifest initial-publication-inventory-v66-subject.json) adds exactly that file at index 281, role builder. The projection helper is byte-identical to v64/v65 and passed with 28 corruptions refused.

## Decide

1. Do the records match the selected shapes and the existing verifiers' P0 rules exactly? The test reproduces the inputs275 row-0 marker, creation input, operation and event hashes byte for byte from the same inputs.
2. Is the internal verification real (not vacuous)? A test swaps in another build's capsule or descriptor and expects refusal.
3. Is any allocation made before its reservation? Are the verifiers' charges on the same ledger?
4. Are the paths exactly the reader-side locators?
5. Does anything read as creation permission or as producing the missing inputs?

## Lead results

rustfmt check clean; `cargo clippy --workspace --all-targets -- -D warnings` clean; `cargo test -p opensip-security --lib` 439 passed, 2 ignored; filter `initial_publication` 6 passed. Replay at least rustfmt, the `initial_publication`, `native_current`, `native_record_capture` and `trust_input_bindings` filters, clippy, and the inventory66 projection helper from the architecture repository.

review.json must contain top-level "verdict" ("ACCEPT-UNIT" or "REQUIRED-FINDINGS"), "requiredFindings", "subjectManifestSha256" (SHA-256 of initial-publication-inventory-v66-subject.json), and "inventoryCandidateAssessment": {"verdict", "requiredFindings", "path", "bytes", "sha256" of repository-file-inventory.v66.json, "parent": {path, bytes, sha256 of v65}, "successorRecord": {path, bytes, sha256 of initial-publication-inventory-v66/successor.json}}. Paths are relative to the architecture repository. Write REVIEW.md and review.json. Do not commit.
