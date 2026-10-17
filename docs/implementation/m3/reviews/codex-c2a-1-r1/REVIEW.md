# C2A-1-r1 review

**Verdict: ACCEPT-UNIT.** No required findings or non-blocking observations.

This accepts the unadmitted candidate library unit. It does not accept component delivery, retained-tree admission, production work-profile selection, R10a/ER10a wiring, public routing or product qualification.

## Subject and verification

Subject manifest: `docs/implementation/m3/snapshot-plan-c/c2a-1-r1-subject.json`, 13,147 bytes, SHA-256 `cc9916f71c928a85ddb3bcf901d226f141180f3fb06e55d803e2f365a86ae0b7`.

Rehashed all 56 members successfully. All six product-map candidate/archive pins, three existing-file parent pins, source.json authority pins and the product-lock pin match. The candidate is detached at `813d559efccbfc30b81b7530833c8427bb4f7dfd`; its changed/untracked paths exactly match the six map rows. Security lib.rs begins with the exact base bytes, including C1c-0's prior append. The three new paths have no planned inventory rows; no planned path is realized. Their additive inventory successor remains a separate integration obligation, numbered from the then-current bound inventory.

Read the scope, source and tests, relevant trust-reader/body-validation/platform-catalog implementations, C2a plan r4 and its review, C2PM-1, M3-C r8 items 7–8, and the archived lane runner/results. Independently ran only the permitted operability source check: passed, 114 rows, no findings. No compiler, build, test or lane was run for this review.

## Implementation assessment

**Trust bridge.** AuthenticatedComponent has private borrowed fields and a constructor restricted to crate::trust. Evidence::admitted_components maps each validated component to its own retained body/envelope pair and release row, without copying or re-verifying evidence. The full ordinary reader already validates bodies with the real host context and checks the signed/catalog associations. The cfg(test)-only TestComponent runs the actual full body validator; its stand-in envelope/release do not claim signed-path admission. The extended ordinary-reader reference test separately checks real evidence associations and the absent-declaration refusal for all eight bridged M2 bodies.

**Platform, kind and projection.** The selected manifest row joins one of the catalog's four exact tokens to an artifact in that same component release. No core spelling is substituted. Kind comes from Validated::closure_kind, CR-1's closed table. Only regular-file entries become borrowed BlobRefs, with exact path, digest and length; directory and symlink entries are skipped. The count and projection visits are each charged by entry count, and the Blob vector is reserved after its charge for exactly the regular-file count.

**Ordering and funding.** The bottom-up merge owns only the two charged u32 buffers. Each comparison follows a fallible edge charge, so Budget precedes an unfunded comparison. The n·ceil(log2 n) reference bound is conservative, with zero comparisons for n<2. Adjacent duplicates have a separate n.saturating_sub(1) charge and Tree refusal. Tests distinguish success with the sufficient old estimate from refusal with actual-comparisons-minus-one funding, implementing plan NBO-2 correctly. Descriptor/object/id funding controls and second-component exhaustion preserve cumulative use of the caller's scope.

**C2PM-1.** Presence and analyzer consistency are rechecked against authenticated declarations. The exact declaration is copied into protocolMajor; providerProtocol never supplies a missing value. After identity admission, the descriptor copy is checked before role support. A host-generated descriptor mismatch carries HostGeneratedInternalLayer, while declaration failures carry AuthenticatedReleaseDeclaration. Resource-role support remains independently keyed to major 1; analyzer support requires its opaque selected-subprotocol seam. There is no numeric support union or cross-role equivalence. No production constructor selects that seam. Public termination/envelope composition remains C2a-4's.

**Descriptor and prices.** The size calculation includes fixed syntax, escaped UTF-8 payloads, integer widths and commas, using saturating arithmetic. It rejects a descriptor over 4 MiB before its buffer charge/allocation. One Vec is then reserved at the predicted size; the hand encoder uses canonical key order, canonical escapes, stack decimal digits and stack hex. Production checks length/capacity; canonical equality is a test oracle, implementing plan NBO-1 without adding a second encoding. IdentityCandidate::from_json stays inside the accepted descriptor/schema-budget exception. The separately copied identifier is charged first. The published constants/const functions cover the projection, visits, sort storage/comparisons, duplicate pass, body digest, descriptor and id. The candidate's private fields and lack of Clone/Default/serialization confer no admission authority.

## Open-question dispositions

Each question is **not a finding**:

1. **Q-C2A1-1 — Encoding/Field between guards 2 and 3:** accepted. These failures belong to constructing/admitting the descriptor that guard 3 must inspect. They do not reorder the four projection guards or replace the earlier owning parse/shape/body/field-use prerequisites. Comparing a pre-encoding copy instead would not check the host's actual admitted descriptor.
2. **Q-C2A1-2 — Two projection visits:** accepted. Charging one edge per entry on both passes accurately prices counting and projection while avoiding reservation for non-file entries.
3. **Q-C2A1-3 — Analyzer seam:** accepted for this staged unit. Without an applicable selected subprotocol, analyzer projection remains Unsupported. The test-only constructor demonstrates the equality rule and supplies no production authority; selection remains with its owner.
4. **Q-C2A1-4 — Count and size legs:** sufficient with their labels. Even 100,000 minimal Blobs exceed 4 MiB, so the schema maxItems edge cannot be reached through this encoder. The constructed count checks and oversized upstream body refusal do not claim production admission. Separate tests exercise actual identity admission at the largest fitting unique-tree count and exactly 4,194,304 descriptor bytes, plus Encoding refusal one byte/row over before descriptor charge. Production-profile feasibility remains C2a-4's gate.
5. **Q-C2A1-5 — Full ordinary reader:** accepted. InventoryBody explicitly lacks full host admission and cannot be converted to Validated without those checks. Borrowing full-reader evidence is the lawful seam. C2a-4 must arrange full validation for the current R10a path while preserving its authenticated associations, ordering and work-profile obligations; this unit does not claim that wiring exists.

## Lane and rules

Raw archived logs agree with the comparison record: security 1,198 to 1,212 passes with the same 14 failures; host 412 to 412 passes with the same 8 failures. The focused suite passes all 15 tests, including the extended ordinary-reader reference test. Archived warning-denied all-targets Clippy, workspace all-targets check, both security feature checks, release build, environment checks, operability and verify_design pass. New/base-clean Rust files are formatted; the base-dirty lib.rs is append-only. The earlier surviving guard-order mutation is history; the revised controls catch it in this packaged run.

All 26 mutation logs show failing tests, match controls.json's failure lists and contain no compilation failure substituting for detection. The mutation changes target the specified semantic, provenance, ordering, encoding and allocation rules. These archived results were inspected, not rerun.

All 19 current census-closure pins match and none intersects the six candidate paths. The operability exception file is unchanged, with 439 mint-audit rows; no mint authority or mint-census call is added. Inspection found no new runtime environment read or let-discard, signing operation, key/private-test-key read, key/root/role/feature, public API or production caller. The compile-time CARGO_MANIFEST_DIR lookup belongs to the test schema registry.

## Remaining scope and boundaries

C2a-2's signed fixtures, C2a-3k's kernel, C2a-3's custody-backed retention/admission, the admitted sum type and composition pin, and C2a-4's R10a/ER10a/profile/public-route controls remain with their named owners. This review does not substitute the test holder or identity calculation for that complete chain.

No repository, worktree or control file was edited. The lane lock was not taken. No network, private 413 fixture, installation, signing/private test key, held tree, T2 store or cache was accessed. No other pane or delegation was used. Only REVIEW.md and review.json were written in the requested directory.
