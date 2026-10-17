# C2a implementation plan r3: closure admission and the core role closures (M3-C r8 items 7, 8 and 9)

**Lead plan, 2026-10-17. Proposed; it needs Codex review.** Round 3 answers Codex `codex-c2a-plan-r2` (REQUIRED-FINDINGS: RF-1, NBO-1, NBO-2, rulings on Q5 and Q6). Round 2 answered `codex-c2a-plan-r1`. r1 and r2 are history, and their changes tables below are kept as history, superseded where r3 says so. The cross-law item it raised, X-C2A-1, is written up in `X-C2A-1-r1.md` (this directory) as the input to the component-delivery law.

## r3 changes

| Finding | Change | Where |
| --- | --- | --- |
| **R2-RF-1** (the size and cost derivation) | **The size formula is corrected and verified against the real encoder.** A Blob has **96 fixed bytes** (its keys, separators, braces and the quoted 64-character digest), plus the decimal digits of `bytes`, plus the encoded payload of `path`. The whole descriptor is **175 fixed bytes**, plus the encoded payloads of `kind`, `platform` and `semanticVersion`, plus the digits of `protocolMajor`, plus the Blobs and their `n − 1` separators. Here an *encoded payload* is a string's canonical JSON encoding without its quotes: raw UTF-8, with `"`, `\`, the five short escapes and `\u00XX` for other controls below U+0020 (`canonical.rs`:286-312). **Verified** by a scratch program against the real `opensip_identity::canonical_bytes` at the plan's base (`evidence/size-check-r3/`, its source and log pinned in the subject). A Blob with `bytes` 0 and path `p` encodes in 98 bytes. Four descriptors, including non-ASCII, escaped and control-character paths, predict exactly (201, 336, 538 and 436 bytes). A real tree of 34,662 unique 20-byte paths encodes in 4,194,299 bytes, and one more row refuses `ByteLimit`. **Every owned representation and buffer has a published `WorkCost` price**, derived from compile-time `size_of` and the encoder's growth rule. The trust evidence is borrowed and is not charged again (LD-C2A-10, rewritten). New predicted-versus-encoded vectors cover non-ASCII and escapable paths, a feasible byte boundary and aggregate exhaustion. The 4 MiB cap and the isolated count predicate are unchanged. | LD-C2A-3; LD-C2A-10; §4 |
| **R2-NBO-1** (scope of "no new admission") | Row 8 adds **no new component-manifest admission and never re-verifies a signature**. The existing context and Run-closure checks (`native_context.rs`:189-223, NE:1493-1499, item 10's shared admission functions at :562) and the typed retention and I/O failures stay at their owning boundaries. A new control: a promised retained object failing **after the draw** keeps its actual cause, and becomes neither not-installed nor a second R10a refusal. | LD-C2A-1; §4 |
| **R2-NBO-2** (the core branch) | **`AdmittedClosure` is a sum type**, `Component(..)` or `Core(..)`. `Component` is constructed only by C2a-3's verifier. `Core` is constructed only from the authenticated `InitialCore` receipt's role projections (`initial_core.rs`:238-254; `core_inventory.rs`:417-421), with no manifest, catalog, delivery law or fixture root. In the no-trust-view case, core roles stay available and no component closure is admitted. | LD-C2A-7; LD-C2A-12 (rewritten) |
| **Q5 ruling** | D4's and J1's **production work-profile selection** (the profile, its caps, its aggregate cost model and its `Budget` projection) is a **named dependency gate of C2a-4**, beside the delivery law. C2a-1's helper takes a borrowed `WorkScope`, and is checked only with explicitly identified test scopes. Those checks are not evidence for a production profile. No snapshot or discovery profile is inferred from a caller's name, no scope is unbounded, and no scope is reset per component. | §2; LD-C2A-10; §7 |
| **Q6 ruling** | **Staged.** C2a-1, C2a-2 and an optional **pure verification kernel** (C2a-3k) land early as internal library work with no production authority. The kernel takes concrete, bounded inputs: the candidate's Blob list and an in-memory map of retained byte slices, with every comparison charged. It confers no claim of delivered custody, and exposes no operational custody interface. **C2a-3's production `Component` constructor and C2a-4 wait** for the delivery law's interface and Q5's profile. Early synthetic tests go through the same kernel and the ordinary trust path, with no fixture-only admission bypass. | §2; §7 |

## r2 changes (round 2, answering `codex-c2a-plan-r1`)

| Finding | Change | Where |
| --- | --- | --- |
| **RF-1** (C2PM-1 is bound) | **C2PM-1 is authority and a dependency.** It is bound in the design lock (`c2pm-1-r2/successor.json`, ACCEPT-DESIGN-UNIT). Its body-validation half is in the product (`c2pm-body-r1`): the optional root `closureProtocolMajor`, the shared analyzer equality with `Error::ClosureProtocolMismatch` (`component_manifest.rs`:19, :513, :659), the four route rows (`native-v2.schema.json`:544-602) and the typed keys (`outcomes.rs`:811-818). C2a-1 carries the rest of its contract: mandatory authenticated presence for every new projection; the ordered guard set *missing declaration, analyzer inequality, descriptor mismatch, unsupported major*; the role support table (`toolchain`, `stdlib`, `rust-dev-llvm` and `grammar` support major 1; `analyzer` only under its selected subprotocol); the exact integer copied into `protocolMajor`; and origin-sensitive routes, where an external release declaration is `request-rejected` / `REQUEST.PRECONDITION_FAILED` with detail `native.closure-protocol-invalid`, and a host bug is `HOST.INVARIANT_VIOLATED`. Nothing is inferred from `compatibility.providerProtocol`. Q2 is withdrawn. | LD-C2A-4 (rewritten); LD-C2A-11 (new); §4; §5 |
| **RF-2** (retention gates admission) | **C2a-1's output before retention is an unadmitted `ClosureCandidate`.** It authorizes no context, Plan, worker or selection. **Admission succeeds only with C2a-3's whole retention**, which is the manifest body and every tree file, verified. For the compiler and the stdlib this is what NE:1493-1499 requires before any digest comparison. The fixture generator supplies synthetic tree bytes but goes through the **same** retention checks. C2a-1 and C2a-2 alone do not unblock successful C2b-1 context admission. Unavailability keeps item 7's routes and X-8. Q1's digest-only recommendation is withdrawn. | §2; LD-C2A-5 (rewritten); LD-C2A-12 (new) |
| **RF-3** (placement) | **Admission completes inside R10a and ER10a, before they return** and before R11's handoff and R12's draw. The trust reader runs first, then D4's excluded-form checks, then C2a's admission checks: projection, C2PM-1's guards, platform, role, kind support and the retained-tree verification. Row 8's later selection adds no admission, and retaining a selected closure for the Run is distinguished from that pre-draw admission. Composition controls prove the ordering and that the reservation set is unchanged on every C2a refusal (J-C10b; D4-T1). | LD-C2A-1 (rewritten); §4 |
| **RF-4** (size and work) | The schema's 100,000 count is a predicate, tested only on constructed input and labelled so. The manifest already caps a TreeCommitment's entries, directories and symlinks included, at 100,000, so a 100,001-entry signed manifest refuses upstream, before projection. **The feasible bound** is the canonical encoder's 4 MiB descriptor (`canonical.rs`:5, :278-283) together with the caller's ledger. Both are tested at their own typed refusals with a feasible positive boundary. The **ledger and costs** are specified: the projection charges the R10a scope it runs in, with published pre-allocation costs for path copies, Blob records, ordering, the descriptor encoding buffer and the identity hash, and with exhaustion and aggregate calls tested. No larger cap is introduced. | LD-C2A-3; LD-C2A-10 (rewritten); §4 |
| **RF-5** (the owner matrix) | **The complete item-9 field-use matrix** (LD-C2A-8, rewritten). It covers every admitted and refused use by field and owner: C3 for import admission; E3, with E3-T13 and E3-T14, for syntax production; C4a for Plan, stage, binding and `semanticClosures`; H for views, facts, scopes and host inventory; E's item 14a for candidate results; L item 3 for cache keys, with no `cache2` minted at M3; and X12d for the same-core detector join. CRC-2's mirror rule, the symbol-inventory exclusion and the candidate-result exclusion are kept. Each is a named owed control, and C2a claims none. | LD-C2A-8 |
| **NBO-1** (the platform join) | The selected-platform join is closed. The selected manifest row's `{os, arch}` is associated with the **same release's** catalog artifact whose `platform` is the token `os + "-" + arch`, one of the four the catalog admits (`recovery_catalog.rs`:67-79). A missing or mismatched artifact refuses `Platform`. Core-inventory platform spellings are never used. | LD-C2A-3 |
| **NBO-2** (the existing vector) | C2-T9 is already covered by `crc1_vector_core_role_closures` and `crc1_all_accepted_inventory_cases_preserve_members_and_distinct_ids` (`core_inventory.rs`:665-737). C2a names them and adds nothing. The shared fixture module is narrow (Q4 ruling). | LD-C2A-8; LD-C2A-6 |
| **Q1 to Q4 rulings** | **Q1:** retention before successful context admission (RF-2). **Q2:** C2PM-1 (RF-1). **Q3:** fail closed within the existing route's limits. A durable required-closure absence may use the not-installed disclosure; X-8 is not resolved by it; no ephemeral `domainDetail`; corruption of a promised retained tree keeps its own cause. **Q4:** a shared security fixture module under exactly `cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))`, with no new key, root or feature, and existing bytes preserved. | LD-C2A-5; LD-C2A-6 |

**Bases:**
- product main and the architecture head, as the subject manifest names;
- of the files this plan cites, none changed between round 1's `3d1d771` and `b753854` (D2b-0b's generation and its lock only).

**Authority:**
- **The law:** M3-C r8 items 7 to 9 (`PROPOSAL.md`:409-557), row 8's narrowing (:71), and the Units table (:1183).
- **The contracts:**
  - SL:21-60: the envelope, the catalog `releases[]` and `artifacts[]`, and the regular-file projection;
  - IE:272-285;
  - NE:1493-1499: the stdlib and compiler closures are retained whole and re-admitted before digest comparisons;
  - the identity schema's `closure` (`opensip/schemas/sources/identity-v3.schema.json`:253).
- **The bound successors:**
  - CR-1 (`cr-1/`);
  - **C2PM-1** (`c2pm-1-r2/`: CONTRACT.md, `closure-protocol-routes.json`, `materialization-map.json`), with its body-validation materialization integrated (`c2pm-body-r1/`);
  - CRC-1 and CRC-2 (`crc-1/`, `crc-2/`).
- **The composition owners:**
  - J1's R10a and ER10a (`host-pipeline-j/PROPOSAL.md`:394, :406-412), with J-C10b;
  - M3-D item 24 and D4-T1 (`supervisor-d/PROPOSAL.md`; D4-T1 samples the reservation registry at the refusal's return);
  - J1's `ExecutionIdReservations` (`host-pipeline-j/PROPOSAL.md`:250).
- **The trust owner's evidence:** `trust_ordinary_metadata.rs`:57-160, the ordinary reader's validated component joined to its release, envelope and preimage.

## 1. What C2a delivers, and what exists

**What exists on main:**
- CR-1's `closure_kind` (`component_manifest.rs`:39-49);
- C2PM-1's body half: the root property, `ClosureProtocolMismatch` in both validation paths, the four route rows and the typed `ClosureProtocolKey` (`outcomes.rs`:811-818);
- the ordinary reader's component join (`trust_ordinary_metadata.rs`:90-160);
- item 9's projections (`core_inventory.rs`:384-440) and their vectors (:665-737);
- the evaluator's detector-join checks (`composition.rs`:125, :163, :765-774);
- the fixture signers `INDEX_SIGNER` and `COMPONENT_SIGNER` and their builders (`core_authentication.rs`:563-600, :696-713), under the joint predicate (:5, :241);
- `sign_synthetic_profile` (`native_census.rs`:648-651).

**What is missing:**
- a narrow bridge from the trust implementation's evidence to a sibling closure module. Today the ordinary reader's `Component` and `Evidence` are `pub(super)` inside the trust implementation;
- the projection, the C2PM-1 projection guards and the platform join;
- the retained-tree verification;
- the shared fixture module;
- the R10a and ER10a wiring;
- the controls.

## 2. The split

| Sub-unit | Delivers | Depends on |
| --- | --- | --- |
| **C2a-1** | **The candidate.** A trust-owned bridge, `trust::admitted_components`, returns, for each component the ordinary reader verified, its authenticated body bytes, its validated manifest, its catalog release row and its envelope provenance, read-only. A new module `crates/security/src/component_closure.rs` computes, from one such component and the selected platform, a **`ClosureCandidate`**: the C2PM-1 guards in their order (LD-C2A-11), the platform join (LD-C2A-3), CR-1's kind (LD-C2A-2), the regular-file projection, the descriptor admitted against identity-v3's `$defs/closure`, and the candidate id `closure2:` + H("closure", D) (`core_inventory.rs`:435). **A candidate authorizes nothing**: no context, Plan, worker or selection accepts it (LD-C2A-12). | CR-1, C2PM-1 (bound); the ordinary reader (integrated) |
| **C2a-2** | **The shared fixture module** (Q4 ruling) under exactly `cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))`. It generalizes `core_authentication.rs`'s builders to role-valid manifests of every role, each with C2PM-1's declaration, and supplied tree bytes. Signing uses only `INDEX_SIGNER`, `COMPONENT_SIGNER` and the existing synthetic root. Existing fixture bytes are unchanged, and `core_authentication.rs`'s tests use the module and keep their outputs. Every artifact carries `LABEL = "synthetic"` (`scenario.rs`:66). No root, key source or feature is new. | C2a-1 |
| **C2a-3k** (r3, Q6) | **The pure verification kernel:** `verify_retained_tree(candidate, blobs: &BTreeMap<&str, &[u8]>, body: &[u8], work)`. For each Blob it checks that the slice is present, that its length equals `bytes` (`BLOB_LENGTH`), and that its SHA-256 equals `sha256`. It also checks that the body's raw SHA-256 equals `manifestDigest`. Each comparison and digest is charged first (LD-C2A-10). It returns typed `Retention(Missing \| Length \| Digest)`. It reads no file, holds no custody and constructs nothing admitted. | C2a-1 |
| **C2a-3** | **Retention and admission.** It obtains the retained bytes from delivered custody through the delivery law's interface, runs C2a-3k over them, and only then constructs **`AdmittedClosure::Component`** (LD-C2A-12). The fixture module's synthetic trees go through the same kernel (RF-2). **Gated on X-C2A-1**, the component-delivery and tree-custody law (`X-C2A-1-r1.md`). | C2a-3k; X-C2A-1 |
| **C2a-4** | **The R10a and ER10a wiring** (LD-C2A-1). After D4's excluded-form checks, R10a runs C2a-1 and C2a-3 for every component the trust view admits and the analysis step can select, before it returns. Any refusal takes its route, and no ExecutionId is drawn or reserved. | C2a-3; D4 (M3-D item 24) |

**Order (r3, Q6):** C2a-1, C2a-2 and C2a-3k land first, as internal library work with no production authority. C2a-3, the production constructor, waits for X-C2A-1. **C2a-4 waits for X-C2A-1 and for D4's and J1's production work-profile selection (Q5 ruling), and for D4 itself.**
- **C2b-1's successful context admission needs C2a-3** (Q1 ruling).
- C2b-1's code may be **authored** against `AdmittedClosure` with synthetic retained inputs from C2a-2 and C2a-3's verifier. Its production dependency is met only when C2a-3 is.

## 3. Lead decisions

- **LD-C2A-1. Admission completes inside R10a and ER10a (r2, RF-3).**
  - **The order within R10a:**
    1. R10's trust read (the ordinary reader verifies body, envelope, catalog and preimage);
    2. D4's excluded-form checks (EE-1, EE-3b, EE-4's manifest part, EE-5a; M3-D item 24);
    3. **C2a's admission:** the candidate (C2a-1), the C2PM-1 guards, the platform, role and kind support, and the retained-tree verification (C2a-3), for every component the trust view admits and the analysis step can select.

    R10a returns the admitted set only after step 3. R11's handoff and R12's ExecutionId draw follow (`host-pipeline-j/PROPOSAL.md`:394, :406).
  - **ER10a** runs the same steps under the read session's fence. With no trust view it admits nothing (LD-C2A-7).
  - **After the draw (r3, R2-NBO-1):** row 8 selects among R10a's admitted set. It adds **no new component-manifest admission** and **never re-verifies a signature** (`PROPOSAL.md`:71).
    - The existing context and Run-closure checks stay at their owning boundaries: NE:1493-1499's re-admission of the retained compiler and stdlib records, and item 10's shared admission functions (:562; `native_context.rs`:189-223, missing, malformed, wrong-identity and wrong-kind retained objects).
    - The typed retention and I/O failures of copying or pinning bytes into the Run's retention also stay where they arise.
    - A promised retained object that fails after the draw keeps its actual cause. It is neither relabelled as not installed nor turned into a second R10a refusal.
  - **No signature is re-verified in C2a, and no draw is moved.**
  - **The controls:** J-C10b and D4-T1 extended to C2a's refusals. The reservation registry, sampled when R10a returns a C2a refusal, is unchanged, and no analysis-attempt ExecutionId exists.
- **LD-C2A-2. The kind comes only from CR-1's table** (`component_manifest.rs`:39-49). `evaluator`, `detector` and `adapter` are never manifest roles (`PROPOSAL.md`:427). No caller-asserted or path-inferred kind is accepted.
- **LD-C2A-3. The platform join and the projection (r2, NBO-1, RF-4).**
  - **The join:** the selected platform is a `{os, arch}` row of the manifest's `platforms[]`. Its token `os + "-" + arch` must be one of the four the catalog admits (`recovery_catalog.rs`:67-79), and must equal the `platform` of an artifact in the **same release row**. No such row or artifact refuses `Platform`. The closure's `platform` is that token. Core-inventory spellings are never used.
  - **The projection:** each `type=file` entry of the selected row's `tree.entries` becomes `Blob {path, sha256: entry.sha256, bytes: entry.length}`, with the same path. `dir` and `symlink` rows are not Blob members (SL:41-48).
    - Blobs are sorted by `path` bytes, which the schema's `x-opensip-order` requires and the body reader does not guarantee.
    - Duplicate paths refuse `Tree`.
  - **The bounds:**
    - **Upstream:** the manifest caps a TreeCommitment's entries at 100,000, directories and symlinks included, and the reader refuses beyond that.
    - **The descriptor (r3, R2-RF-1):** the closure descriptor's canonical encoding must fit 4 MiB (`canonical.rs`:5, :278-283), or it refuses `Encoding`. Writing e(x) for a string's encoded payload (its canonical encoding without the two quotes) and d(n) for an integer's decimal digits:
      - **a Blob** `{"bytes":N,"path":"P","sha256":"<64 hex>"}` is **96 + d(N) + e(P)** bytes;
      - **the descriptor** `{"kind":..,"manifestDigest":..,"platform":..,"protocolMajor":..,"schemaVersion":2,"semanticVersion":..,"tree":[..]}`, with keys in byte order, is **175 + e(kind) + e(platform) + d(protocolMajor) + e(semanticVersion) + Σ(96 + d(Nᵢ) + e(Pᵢ)) + max(n − 1, 0)** bytes;
      - e(·) counts raw UTF-8 bytes, 2 for each `"` and `\`, 2 for each of `\b \f \n \r \t`, and 6 for any other control below U+0020 (`canonical.rs`:286-312). DEL and non-ASCII are raw UTF-8.

      C2a computes this predicted length D exactly, **before** encoding, and refuses `Encoding` if D exceeds 4,194,304 without allocating the buffer. So a feasible tree has far fewer than 100,000 files, and the boundary is tested at the real encoder's edge.
    - **The ledger:** LD-C2A-10.

    The schema's `tree` `maxItems` of 100,000 is a predicate tested only on constructed input, labelled so, and never claimed as production admission.
- **LD-C2A-4. The descriptor (r2, RF-1).**
  - `manifestDigest` is the raw SHA-256 of the authenticated body (IE:272-276).
  - `semanticVersion` is the manifest's `version`.
  - `platform` comes from LD-C2A-3.
  - **`protocolMajor` is the authenticated top-level `closureProtocolMajor`, copied exactly** (C2PM-1 CONTRACT.md). It is never normalized, inferred, defaulted, or copied from `compatibility.providerProtocol` when absent.
  - `schemaVersion` is 2, and the kind comes from LD-C2A-2.
- **LD-C2A-5. Retention gates admission (r2, RF-2; Q3 ruling).**
  - Item 7 retains the manifest and the whole tree of every admitted closure (`PROPOSAL.md`:430). NE requires the compiler and stdlib retained whole and re-admitted before digest comparisons (NE:1493-1499). So **admission is C2a-3's**, and C2a-1's candidate is not an admitted closure.
  - **The tree's bytes** come from delivered component custody, which no accepted law or code provides yet (X-C2A-1, `X-C2A-1-r1.md`). Until it exists, production admission of a component closure is not possible. The gated identity calculation is never presented as item-7 admission.
  - **The interim, failing closed (Q3 ruling):**
    - a durable required closure that has no delivered tree is disclosed as not installed (`COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED`, durable only, `PROPOSAL.md`:435). This does not resolve X-8's required-cell binding gap (:436), invents no binding, and adds no ephemeral `domainDetail`;
    - a **promised** retained tree whose bytes disagree with its Blobs (digest, length or identity) keeps its own failure cause, `Retention(Digest | Length | Missing)`, and is never relabelled as not installed.
- **LD-C2A-6. The shared fixture module (Q4 ruling; NBO-2).**
  - It lives in security, under exactly `cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))`.
  - It reuses `INDEX_SIGNER`, `COMPONENT_SIGNER` and the existing synthetic root (`core_authentication.rs`:563-565).
  - It preserves the existing fixture bytes and the release-build source pin (C2-T7).
  - It introduces no root, key source or feature.
  - It builds role-valid, role-scoped manifests with C2PM-1's declaration.
  - It cannot bypass production verification or retention: its outputs enter through the ordinary reader and C2a-3's verifier like any other.
  - C2-T6 exercises that whole lawful chain.
- **LD-C2A-7. No trust view.** ER10a with no admitted trust view (I positively absent, or F absent under the read session) admits nothing. C2a represents this as an empty admitted set, and never as an ordinary-reader `Evidence` with an absent catalog. Item 9's core role closures are unaffected. C2-T18's cells, bindings and public result are C4a's and J2c's (`PROPOSAL.md`:453), and are not inferred from a signature test.
- **LD-C2A-8. Item 9: the complete field-use matrix (r2, RF-5; NBO-2).**
  - **Already in the product:** the four core role projections (`core_inventory.rs`:417-421) and C2-T9's vectors (`crc1_vector_core_role_closures`, `crc1_all_accepted_inventory_cases_preserve_members_and_distinct_ids`, :665-737). C2a adds nothing for item 9's identity.
  - **The fields, each a named owed control at its owner** (`PROPOSAL.md`:488-557; CRC-1; CRC-2):

    | Field or rule | Admitted closure | Refused | Owner and control |
    | --- | --- | --- | --- |
    | `import.producerClosure` of a `dependency` or `prepared` import | core provider (use 1) | any other kind or role | **C3**'s import admission (items 12 to 14) |
    | `import.adapterClosure` of such an import | core adapter | any other field for the adapter, `semanticClosures` included | **C3** (C2-T12's import leg); **C4a** for its non-membership |
    | syntax-universe `subject-scope.enumeratorClosure`, `view.producerClosure` and `fact.producerClosure`, `stage-spec.producerClosure`, and enumeration `enumerator.closureId` | core provider (use 2) | the TypeScript or Rust provider's closure | **E3** (E3-T13, E3-T14; `syntax-e/PROPOSAL.md`:710-711) for production; **C4a** for stage and binding selection; **H** for view, fact and scope admission |
    | `CandidateProducerResultV1.producerClosure` | core provider, in a syntax universe only | use 3; any non-syntax universe | **E**'s item 14a (the candidate-only result) |
    | host-inventory `enumerator.closureId`, `stage-spec.producerClosure`, `view`/`fact.producerClosure` and `subject-scope.enumeratorClosure` (use 3) | core provider, for the three `inventory` relations' host-derived records only | a provider-returned record, any other relation, and a binding that owes a symbol inventory | **H** (item 18; H's host inventory stage) and **C4a** (stage and binding) |
    | CRC-2's mirror rule | none | any language provider closure as producer or enumerator of an `inventory` record | **H** |
    | `cache-key.producerClosure` | none at M3 | every closure (CRC-1 LD-4) | **L** item 3; no `cache2` is minted at M3 |
    | `plan.semanticClosures` membership of the core provider | exactly when a syntax universe is selected or an `inventory` cell is requested | otherwise; its absence then | **C4a** (C2-T13) |
    | an emission row's `detectorClosure` | the seal's core detector | the evaluator closure; another core's detector | **X12d** (item 19; C2-T10, C2-T11): the same-core join, beyond the evaluator's existing kind and membership checks (`composition.rs`:765-774) |

    C2a implements none of these consumers, and claims none of their controls.
- **LD-C2A-9. Refusals are typed.**
  - `ClosureRefusal {Platform, Tree, Kind, Field, Encoding, Protocol(key), Retention(Digest | Length | Missing)}`.
  - The trust reader's refusals pass through unchanged.
  - `Protocol(key)` is C2PM-1's four internal keys, routed by LD-C2A-11.
  - Other public projections are J1's (rows 27 and 56).
  - Work exhaustion stays the ledger's `Budget` failure.
- **LD-C2A-10. The ledger and the costs (r2, RF-4; r3, R2-RF-1, Q5).**
  - **The scope.** C2a-1, C2a-3k and C2a-3 take a **borrowed `WorkScope`**, the caller's. In production that is R10a's, and **its profile is D4's and J1's production work-profile selection, a named gate of C2a-4** (Q5 ruling). C2a selects no profile, infers none from a caller's name, uses no unbounded scope, and never resets a scope per component. Before that selection, the bounded helpers are checked only with explicitly identified test scopes, which are not evidence for a production profile.
  - **Borrowed evidence is not charged again.** The ordinary reader's validated manifest, body bytes, release row and envelope provenance are borrowed by reference (`trust_ordinary_metadata.rs`:29-56). C2a allocates only what follows.
  - **The published prices.** Each is a `const fn` beside its use, from compile-time `size_of`, as D3a-0's `descend_cost` is. Every allocation is charged before it is made:
    - **per regular-file entry,** the Blob as a `JsonValue::Object` of three members:
      - objects 6: the map's node, the three key strings, the path copy and the digest string;
      - bytes `11 × size_of::<(String, JsonValue)>()`, a conservative B-tree leaf of std's capacity of 11, plus `5 + 4 + 6` for the keys, plus e_raw(P) (the path's UTF-8 length) plus 64 for the two strings;
      - edges 1;
    - **the tree array,** `Vec<JsonValue>` reserved exactly for `n` entries: objects 1, bytes `n × size_of::<JsonValue>()`;
    - **the ordering,** an in-place `sort_unstable_by` on path bytes, which allocates nothing. Its comparisons are charged as edges, `n × ⌈log₂(n + 1)⌉`. Duplicate paths are found by one adjacent pass (n edges);
    - **the descriptor's other members:** objects 1 for the map's node plus 7 for the key strings plus 4 for the string values (`kind`, `manifestDigest`, `platform`, `semanticVersion`); bytes `11 × size_of::<(String, JsonValue)>()` plus 71 for the keys plus the four values' UTF-8 lengths;
    - **the encoding buffer,** the canonical encoder growing a `Vec` from empty to the predicted D (`canonical.rs`:267-283). It is charged at the amortized-doubling bound of std's growth (doubling from a minimum capacity of 8): objects ⌈log₂(D / 8)⌉ + 1, and bytes 4·D for all its reallocations. D is computed first, by the formula, so no encoding starts unfunded;
    - **admission and identity,** `IdentityCandidate::from_json(registry, IdentityDomain::Closure, &bytes, SCHEMA_BUDGET)`, as C1a3's sealing admits `snapshot2` (`snapshot_seal.rs`:390-394). Its own work is bounded by the 4 MiB descriptor and the 64 MiB schema budget, the accepted precedent of LD-C1A3-4. The id string it returns is charged as an owned record of `"closure2:".len() + 64` bytes;
    - **C2a-3k,** per Blob one SHA-256 over its slice (edges ⌈len / 64⌉ + 1, its block count) and one length comparison (one edge). One SHA-256 over the body. No copy of any slice;
    - **across components,** the prices add up in one scope. Exhaustion is `Budget` partway through any component, never truncation.
  - **The feasible positive boundary** is the smaller of the scope's limits under the selected profile and the 4 MiB descriptor, at the encoder's real edge.
- **LD-C2A-11. C2PM-1's projection guards (r2, RF-1).** After the trust, parse, shape, body-semantic, tree, platform, role and field prerequisites succeed, in their owning order, the guards run in C2PM-1's deterministic order. The first failure mints nothing.
  1. **missing declaration**, `native.closure-protocol-declaration-missing`. The body validated, since absence is lawful for M2 body validation, but every new projection requires the declaration;
  2. **analyzer inequality**, `native.closure-protocol-analyzer-mismatch`. This independently rechecks the shared body rule;
  3. **descriptor mismatch**, `native.closure-protocol-descriptor-mismatch`. An input or recomputed descriptor's `protocolMajor` differs from the authenticated declaration;
  4. **unsupported major**, `native.closure-protocol-unsupported`. The role support table: `toolchain`, `stdlib`, `rust-dev-llvm` and `grammar` support major 1, and `analyzer` only under its already-selected named subprotocol. No numeric union and no cross-role equivalence is applied.

  **Origin is carried, never asserted by a caller:**
  - an authenticated release declaration, or a retained or supplied descriptor of known external origin, routes `request-rejected` / `REQUEST.PRECONDITION_FAILED` / exit 2, with public detail `native.closure-protocol-invalid` and its code-keyed remedy;
  - a host bug in the host's own descriptor routes `operational-failed` / `SYSTEM.OUTCOME.ILLEGAL_STATE` / `HOST.INVARIANT_VIOLATED` / exit 4;
  - an unknown origin is refused by the derivation;
  - the termination's `domainDetail` is absent. The failure envelope carries exactly one `errors` DomainDetail, with the internal key as its bounded subject (C2PM-1 CONTRACT.md, "Refusal predicates, origins and real public carriers").
- **LD-C2A-12. The types (r3, R2-NBO-2).**
  - `ClosureCandidate` is C2a-1's output: unadmitted, with no public constructor outside security, and accepted by nothing but C2a-3, through C2a-3k.
  - **`AdmittedClosure` is a sum type**, the only closure type a native context, the Plan or row 8's selection accepts:
    - **`Component(..)`** is constructed only by C2a-3, after whole retention;
    - **`Core(..)`** is constructed only from the authenticated `InitialCore` receipt's role projections (`initial_core.rs`:238-254; `core_inventory.rs`:417-421). It needs no manifest, catalog, delivery law or fixture root.

  So no component closure is admitted without its retained tree. Core roles are unaffected, including the no-trust-view case (LD-C2A-7).

## 4. Controls

- **C2-T1:**
  - a manifest without the selected `{os, arch}` row refuses;
  - a release with no artifact of the joined token refuses `Platform`;
  - a TreeCommitment whose retained bytes disagree refuses `Retention(Digest)`, keeping its cause.
- **C2-T2:** a role/kind mismatch per field refuses (`PROPOSAL.md`:429).
- **C2-T3:** a bad envelope signature refuses in the trust reader, and C2a never sees it.
- **C2-T4:** a `symlink` or `dir` row is never a Blob and never followed.
- **C2-T5:** the same tree under a changed version, a new `closure2`.
- **C2-T6:** synthetic role-valid closures of every role, with C2PM-1 declarations, admit through the ordinary reader, C2a-1 and C2a-3's verifier.
- **C2-T7:** a release build has no synthetic root (the source pin over the predicate).
- **C2-T8's label half:** the `synthetic` label is carried. The authoritative-surface refusal is J2's and is not claimed here.
- **C2-T9:** the existing `core_inventory.rs`:665-737 vectors, named.
- **C2-T18's admission half:** no trust view gives an empty admitted set, with the core roles intact.
- **C2PM-1 (RF-1):**
  - each guard in order;
  - combined failures pick the first;
  - an unsupported major on a mismatched descriptor yields descriptor-mismatch;
  - an absent declaration on a body that validated refuses at projection;
  - an analyzer major equal to its subprotocol admits;
  - the external and host-bug origins route as LD-C2A-11 says, with the full failure envelope (one `errors` detail, absent termination `domainDetail`) and the code-keyed remedy;
  - no inference from `compatibility.providerProtocol`.
- **Retention (RF-2):**
  - a missing tree file refuses `Retention(Missing)`, and a short file `Retention(Length)`;
  - a `ClosureCandidate` handed to a context or selection API does not compile, which is a type-level pin;
  - the fixture's synthetic tree goes through the same verifier.
- **Placement (RF-3):**
  - each C2a refusal returned from R10a, and from ER10a, leaves the `ExecutionIdReservations` sample unchanged and no analysis-attempt ExecutionId drawn (J-C10b and D4-T1, extended);
  - a successful R10a returns only `AdmittedClosure`s;
  - row 8 performs no admission check.
- **Size and cost (r3, R2-RF-1):** predicted-versus-encoded vectors through the real `canonical_bytes`:
  - a Blob with `bytes` 0 and path `p` is 98 bytes;
  - descriptors with an empty tree, one Blob, a non-ASCII path (`日本/語.wasm`), and an escapable path (with `"`, `\`, `\n` and U+001F) each predict their exact encoded length;
  - a feasible boundary admits a real unique tree at the largest row count that fits, and refuses `Encoding` one row over, with the refusal raised before any buffer is allocated;
  - aggregate exhaustion partway through the second of two components is `Budget`;
  - the charge equals the published prices summed over the recorded allocations.
- **After the draw (r3, R2-NBO-1):** a promised retained object, corrupted after R10a's admission, fails at its context or Run-closure owner with its own cause. It is neither not-installed nor a second R10a refusal.
- **The core branch (r3, R2-NBO-2):** with no trust view, `AdmittedClosure::Core` values exist and no `Component` does. A `Core` value is unconstructible from a component candidate.
- **Size and work (RF-4):**
  - the count predicate at 100,000 and 100,001, on constructed input, labelled;
  - the upstream 100,001-entry signed manifest refuses in the reader before projection;
  - the 4 MiB descriptor boundary admits at its edge and refuses `Encoding` one byte over;
  - `Budget` at exhaustion, including partway through the second component;
  - the charge equals the recorded calls' price.
- **The platform join (NBO-1):** a mismatched artifact token refuses, and a core-inventory spelling is never accepted.
- **Composition:** a context or selection receiving a `ClosureCandidate` is unconstructible.

## 5. Mutations

Each must fail the controls:
- a symlink or `dir` row projected;
- the kind taken from the role string;
- `manifestDigest` over the envelope;
- the platform from the host's spelling, or from another release;
- the Blob order unsorted;
- **a C2PM-1 guard reordered, or skipped;**
- **`protocolMajor` copied from `compatibility.providerProtocol`;**
- **a host-bug origin routed as external, or the reverse;**
- **retention bypassed (a candidate accepted as admitted);**
- **a retention digest or length check removed;**
- **a corrupted retained tree relabelled as not installed;**
- **a C2a refusal returned after R10a's boundary, or a draw before it;**
- the generator signing with a non-fixture key path;
- the synthetic root reachable without the predicate.

## 6. Checks

The lane covers:
- the security and host suites at base and candidate;
- warning-denied all-targets Clippy, rustfmt, and the focused tests;
- the release-build source pin;
- the generated route and public-detail tables reproduced, as C2PM-1's materialization map requires;
- the environment exceptions, the operability source census with its mint audit, the census-closure check and verify_design;
- the mutations.

## 7. Open questions

- **Q5 (ruled in r3):** D4's and J1's production work-profile selection is a named gate of C2a-4 (LD-C2A-10).
- **Q6 (ruled in r3):** staged. C2a-1, C2a-2 and C2a-3k land early, while C2a-3's production constructor and C2a-4 wait (§2).

## 8. Not delivered

- Component delivery and tree custody (X-C2A-1; `X-C2A-1-r1.md`).
- C2b-1 and C2c.
- Item 9's field-use enforcement at its owners (LD-C2A-8).
- D4's own checks.

## 9. Not claimed

- No trust-owner change, and no new key, root, role or feature.
- No production context, and no qualification.
