# C2A-PLAN-r1 review

**Verdict: REQUIRED-FINDINGS — five required findings, two non-blocking observations.**

## Subject and verification

The 577-byte subject manifest hashes to `70a44150f3428325f0733f4692beedc126b767d509807faf860d3cc9d3c299d4`. Both members match:

| Member | Bytes | SHA-256 |
| --- | ---: | --- |
| `c2a/PLAN-r1.md` | 15707 | `de404a2f5b2c8539dbebb07cd475c58afe4fa4cb77954e88fade9dcd07d1f20d` |
| `c2b/C2B-GATING-r1.md` (context only) | 5508 | `18e18bec084b0f0fad32404c7fa024e0f50752d337786c0c10302e55c3529b9b` |

Bases are product `3d1d771ecc5a8772d57f8393ce09cc82ce5f025a` and architecture `2d169666ee5c28eedea5e43083b7968b6ba80e9f`. All seven requested product source files were compared byte-for-byte with the product base and match. The C2PM-1 successor and acceptance pins were independently checked against that base's lock; its contract is therefore relevant despite the draft wording retained inside its reviewed package.

This was a read-only plan/source review. No builds, tests, lanes, network, delegation, installation/private fixtures, key files or T2 data were used. Fixture signers are referenced only by source name. Only the two requested review artifacts were written.

## Required findings

### C2APLAN-R1-RF-1: Use the already bound C2PM-1 declaration and admission rules

Location: `c2a/PLAN-r1.md:59-63, 82-85, 122`.

Q2 is already resolved at the pinned product base. Its design-lock.json binds c2pm-1-r2/successor.json (SHA-256 f75f9cbb3561826d128ad1bbbcd7f179a31c0ef24614202eb68f27d7bd71b446) with ACCEPT-DESIGN-UNIT. That successor selects the signed top-level closureProtocolMajor, mandatory for every new C2a projection, with independent presence/analyzer-equality rechecks, exact integer copying, role-specific support and descriptor agreement. The base also contains the optional property and the shared analyzer mismatch check. Leaving the source open, suggesting compatibility as the source, and mapping all refusals generically to J1 rows 27/56 omits accepted admission and public-route duties.

Required change: Add C2PM-1 as authority/dependency. Carry its ordered projection predicates, exact role support, authenticated-source controls and origin-sensitive native route publication through the owning implementation units. Do not infer an absent declaration from compatibility.providerProtocol or treat the supporting body-reader implementation as full C2a admission.

### C2APLAN-R1-RF-2: Keep retention a prerequisite of admitted closures and native contexts

Location: `c2a/PLAN-r1.md:45-49, 64-68, 121-123`.

Separating a pure descriptor calculation from delivery is reasonable, but item 7:430 requires every admitted closure to retain its manifest and whole tree. NE:1493-1499 explicitly requires both compiler and stdlib closures retained whole and re-admits their records before digest comparisons. Q1 recommends digest-only context minting with retention deferred, contradicting that requirement and the gating memo. LD5 also calls the pre-retention operation production admission, even though its output cannot yet satisfy admission.

Required change: Define C2a-1 output before retention as an unadmitted candidate/projection that cannot authorize a context, Plan or worker. Gate successful production closure/context admission on C2a-3 or equivalent lawful complete retained inputs, including the compiler and stdlib. The fixture generator may supply synthetic bytes, but must exercise the same retention checks. Preserve the delivery-owner gate; do not count C2a-1/2 alone as unblocking successful C2b-1 context admission. Keep unavailability handling subject to item 7's X-8 and the existing durable/ephemeral routes.

### C2APLAN-R1-RF-3: Place admission completion within the pre-draw R10a/ER10a boundary

Location: `c2a/PLAN-r1.md:53, 131`.

LD1 places C2a admission after R10a and leaves its placement as a precondition. M3-C r8:71 says item 7 admission has already run no later than R10a, before any analysis-attempt ExecutionId, and row 8 adds no admission. J1:394,406-411 and M3-D item 24 put R10a before R11/R12. A new platform/protocol/field admission failure discovered after that boundary cannot silently become row-8 admission.

Required change: State that the trust reader runs first, D4 performs its excluded-form checks, and the relevant C2a admission checks finish as part of R10a/ER10a before that boundary returns and before handoff/draw. Distinguish later selection and selected-closure retention from pre-draw admission. Name the composition controls that prove ordering and unchanged reservation sets on refusal; do not move draws or reverify signatures in C2a.

### C2APLAN-R1-RF-4: Make the size controls and work accounting implementable

Location: `c2a/PLAN-r1.md:55-58, 86, 93-94`.

The unconditional control that 100,000 files admit is not achievable through the proposed full descriptor identity path. The identity canonical encoder has MAX_BYTES = 4 MiB (crates/identity/src/canonical.rs:5,279); 100,000 Blob objects alone exceed that bound. The input manifest also caps all TreeCommitment entries, including directories and symlinks, at 100,000. A 100,001-file signed manifest therefore refuses before projection. LD10 additionally leaves ledger selection and costs unspecified, although projection allocates path/Blob records, orders them, validates and canonicalizes/hashes the descriptor; the existing body reader does not require entry order.

Required change: Separate the schema count predicate from feasible whole-record admission. Retain existing upstream/canonical limits and test their typed refusals, with a feasible positive boundary. Specify the production ledger/profile and pre-allocation costs for descriptor/path ownership, ordering and identity work, including exhaustion and aggregate calls. If an isolated count test uses constructed input beyond manifest admission, label it as such rather than claiming production admission. Do not promise unconditional schema-max admission or introduce an unreviewed larger cap.

### C2APLAN-R1-RF-5: Complete the item-9 field-use owner matrix

Location: `c2a/PLAN-r1.md:75-81, 130`.

Assigning C2-T12/13/13a collectively to C4a and H covers Plan/view legs but does not enumerate all fields and restrictions in item 9 and bound CRC-1/CRC-2. These include dependency/prepared import producer and adapter admission; syntax stage/scope/binding and CandidateProducerResultV1 provenance; host inventory origin/relation/binding restrictions; and the all-role cache-key prohibition. E3 has explicit E3-T13/T14 legs (syntax-e/PROPOSAL.md:710-711), while import admission has its own owner. A generic Plan/view assignment leaves these duties untracked.

Required change: Add a field/control-to-owner matrix covering all admitted and refused uses, including import admission (C3), syntax production (E3), Plan/stage/binding selection (C4a), view/fact/scope admission (H), candidate-result admission and cache-key admission at their actual owners. Explicitly retain CRC-2's mirror rule and the symbol-inventory and candidate-result exclusions. Keep these as named dependencies/owed controls rather than claiming C2a implements every consumer. X12d must still prove the same-core detector join, beyond the evaluator's existing kind/membership checks.

## Rulings on Q1–Q4

- **Q1: Retention is required before successful context admission.** Reject the digest-only recommendation. NE's retained-tree rule covers both compiler and stdlib, before digest comparisons. Developing the context code with lawful synthetic retained inputs is possible; claiming the production dependency is met by C2a-1/2 alone is not. See RF-2.
- **Q2: Use the already bound C2PM-1 source.** The signed top-level `closureProtocolMajor` is the source, with its specified guards, support rules and routes. No new owner guess is needed. See RF-1.
- **Q3: Fail closed, with the existing route's limits.** Deferring successful production admission while tree delivery/custody is unavailable is sound. X4B and the cited retained-pair path supply metadata, not an installed component tree. A verified catalog is not tree custody. The durable required-closure absence may use the existing not-installed disclosure; this does not itself resolve X-8's required-cell binding gap, authorize an invented binding, or permit an ephemeral domainDetail. A digest/length/identity corruption of a promised retained tree must retain its actual failure cause rather than automatically becoming “not installed.” The gated identity calculation must not be presented as completed item-7 admission.
- **Q4: Prefer a shared security fixture module.** Reuse `INDEX_SIGNER`, `COMPONENT_SIGNER` and the existing synthetic root under exactly `cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))`. Preserve existing fixture bytes, introduce no root/feature/key source, and retain the release-build source pin. The cited X4B/463 builders and `sign_synthetic_profile` support this approach. Public fixture-signing helpers do not permit bypassing production verification or retention.

## Other requested assessments

The closed CR-1 role-to-kind table, exact regular-file projection, envelope-excluded body digest, schema validation, deterministic identity and unchanged trust-owner verification are correct directions. The ordinary reader checks body, preimage, envelope and compatibility association; C2a should consume that evidence through a narrow trusted interface, rather than reopen raw signature/catalog admission. Its current component/evidence visibility is confined to the trust implementation and needs deliberate bridging for a sibling component_closure module.

C2-T1–T5 are appropriately named, subject to the platform association, retention and bounds corrections above. C2-T6 must exercise the full lawful admission chain with role-valid signed fixtures. C2-T7's source pin and the label/refusal split for C2-T8 are appropriate; carrying the label alone does not discharge authoritative-surface refusal. C2-T18's empty component set, preserved core roles, unavailable-cell bindings and public result remain split across C2a, C4a and J2c; they must not be inferred from a signature test. The no-trust-view case should be represented without inventing a successful ordinary-reader Evidence containing an absent catalog.

The mutation list is useful but must gain C2PM-1 guard/route mutations, retention bypass/digest/length failures, and the pre-draw placement controls. Existing item-9 projections are implemented; consumer enforcement remains owed as RF-5 describes. No acceptance of code, delivery, a production context or qualification is implied by this plan review.

## Non-blocking observations

### C2APLAN-R1-NBO-1: Make the selected-platform join explicit

Location: `c2a/PLAN-r1.md:62`.

The catalog is a valid authenticated source for the platform spelling: recovery_catalog.rs:68-79 admits the four component platform tokens. State the closed association between the selected manifest os/arch row and its same-release artifact token, with a mismatch/missing-artifact control. Merely copying a signed token does not join it to the selected tree. Core inventory platform spellings are a different vocabulary and must not be copied here.

### C2APLAN-R1-NBO-2: Record the existing vector and preserve a narrow fixture seam

Location: `c2a/PLAN-r1.md:46,69-77`.

core_inventory.rs already has crc1_vector_core_role_closures and crc1_all_accepted_inventory_cases_preserve_members_and_distinct_ids (665-737), covering pinned role ids, raw-body digest, only-kind projection and distinctness. Name them instead of leaving their existence uncertain. A shared fixture module is reasonable, preserving existing bytes and the exact joint predicate; it must build valid role-scoped manifests, including the C2PM-1 declaration for new projections, and must retain the existing synthetic label and release source pin.

