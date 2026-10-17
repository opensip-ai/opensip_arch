# C2a implementation plan r1: closure admission and the core role closures (M3-C r8 items 7, 8 and 9)

**Lead plan, 2026-10-17. Proposed; it needs Codex review.** It is the second unblocking unit that `../c2b/C2B-GATING-r1.md` names. C2b-1, the TypeScript context, waits for C2a, because the context names manifest-admitted `toolchain` and `stdlib` closures (`PROPOSAL.md`:434, :571; NE:1501-1519).

**Bases:**
- product main `3d1d771` (the v221 lock);
- the current architecture head, and the files the subject manifest names.

**Authority:**
- **The law:** M3-C r8:
  - item 7 (`PROPOSAL.md`:409-453), the one admission path, the `role → kind` table (:417-427), retention (:430), the no-trust-view case (:431-437), and controls C2-T1 to C2-T5 and C2-T18;
  - item 8 (:455-469), the synthetic signed closures, with controls C2-T6 to C2-T8;
  - item 9 (:471-557), the core role closures, with controls C2-T9 to C2-T13a;
  - the Units table, C2a (:1183, "closure admission and the core role closures").
- **The contracts:**
  - SL:21-60 (`docs/v2/contracts/product-v1/security-and-lifecycle.md`). The envelope is `opensip-signature-envelope.2`, with subject `kind=manifest`, domain `opensip.metadata.manifest.1`, and `storedSha256` equal to `closure.manifestDigest`. The catalog is `opensip-catalog.1` `releases[]` `{manifestDigest, manifestPreimageSha256, envelopeDigest, artifacts[{platform, archiveProfileId, archiveDigest, sha256}]}`, signed TR-INDEX. The projection maps each `type=file` TreeCommitment entry to one `Blob {path, sha256, bytes}`. `dir` and `symlink` rows are not Blob members and are never followed.
  - IE:272-285 (`identity-and-evidence.md`): `manifestDigest` is the raw SHA-256 of the body, envelope excluded, and a manifest for another tree, platform or component refuses.
  - The identity schema's `closure` (`opensip/schemas/sources/identity-v3.schema.json`:253): `schemaVersion` 2, `kind` from a closed eight-value enum, `tree` at most 100,000 Blobs ordered by `path`, `semanticVersion` and `platform` strings of 1 to 4,096 characters, `protocolMajor` an integer.
- **The successors bound for it:** CR-1, the role vocabulary and command-tree gating (`cr-1/`, bound at `3fe7eb5`); CRC-1 and CRC-2, the core role closures (`crc-1/`, `crc-2/`).
- **The units it composes with:**
  - J1's R10a and ER10a, D4's pre-draw component admission (`host-pipeline-j/PROPOSAL.md`:394, :406-411; M3-D item 24). Item 16's row 8 selects only among R10a-admitted manifests (S19; `PROPOSAL.md`:71).
  - X4T's ordinary trust reader. `trust_ordinary_metadata.rs`:57-160 already joins each validated manifest to its catalog release (`MissingRelease`), its verified envelope and its preimage.

## 1. What C2a delivers, and what exists

**What exists on main:**
- **CR-1's table:** `component_manifest.rs`:39-49 (`closure_kind`) maps an admitted role to its kind. Its comment states that "Signature, tree capture, closure identity and field-use admission are separate owners".
- **The trust join:** `trust_ordinary_metadata.rs`:90-160. A validated manifest is joined to its catalog release by `{stableId, publisher, sourceClass, version}`; the release's `manifestDigest` equals the raw SHA-256 of the body (`BodyDigest`); the verified envelope's preimage equals `manifestPreimageSha256` (`Preimage`).
- **Item 9's projections:** `core_inventory.rs`:384-421. The core descriptor's `tree` holds the platform row's regular files `{path, sha256, bytes}`, and `closure_id` is `closure2:` + H("closure", D) (:435-440). The evaluator, detector, provider and adapter closures are the role descriptors, exposed by `initial_core.rs`:238-254.
- **The detector join** in the evaluator: `composition.rs`:125, :163, :765-774.
- **The fixture signing precedents,** all under the joint predicate `cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))` (`core_authentication.rs`:5, :241):
  - `component_body`, `component_release` and the catalog builder (`core_authentication.rs`:563-600, :696-713) build a TR-COMPONENT-signed component manifest and a TR-INDEX-signed catalog, with the public test-only signers `INDEX_SIGNER` and `COMPONENT_SIGNER` (quorum62 seeds, :563-565);
  - `sign_synthetic_profile` (`native_census.rs`:648-651), whose comment reads "Public deterministic fixture keys … never operational keys".

**What is missing:**
- the step from an admitted, trust-verified component to an item-7 `closure2`: the TreeCommitment projection, the descriptor and its identity;
- the closure's retention;
- item 8's generator as a reusable fixture producing complete signed closures;
- the controls C2-T1 to C2-T8 and C2-T18.

## 2. The split

| Sub-unit | Delivers | Controls | Depends on |
| --- | --- | --- | --- |
| **C2a-1** | **Item 7's identity** (security, a new module `crates/security/src/component_closure.rs`): from a component that X4T's ordinary reader returned (a validated manifest joined to its release, envelope and preimage) and the selected platform, mint the `closure2` descriptor `{schemaVersion: 2, kind, manifestDigest, tree, semanticVersion, protocolMajor, platform}` and its id, by the same `closure_id` rule as the core (`core_inventory.rs`:435). The kind comes from CR-1's `closure_kind` (LD-C2A-2). The tree is the projection of the selected platform's TreeCommitment onto `type=file` rows (SL:41-48; LD-C2A-3). A manifest without the selected platform refuses. The descriptor is admitted against identity-v3's `$defs/closure`. Then the field check: a closure whose kind is not the one its selecting field requires refuses (`PROPOSAL.md`:429; IDS `closureKinds.byField`). | C2-T1 (another platform; a TreeCommitment mismatch); C2-T2 (role and kind per field); C2-T3 (a bad envelope signature, through the trust reader); C2-T4 (a symlink row never followed and never a Blob); C2-T5 (a changed version gives a new `closure2`); C2-T18's admission half (no trust view: nothing admitted) | CR-1 (bound); X4T's ordinary reader (integrated) |
| **C2a-2** | **Item 8's generator** (security fixture module, on the joint predicate). It takes a supplied tree (path, mode, bytes), writes a real component-manifest body with its TreeCommitment, signs its envelope under TR-COMPONENT and its catalog row under TR-INDEX with the public fixture signers, and returns the signed bytes and the tree bytes. The precedent is `core_authentication.rs`:563-600 and :696-713, generalized from that fixed body to any role and tree, and moved behind the predicate unchanged. Admission then runs the **production** path of C2a-1 (C2-T6). Every artifact carries the `synthetic` label (`scenario.rs`:66, `LABEL = "synthetic"`; the law's `scenario.rs:51` is r8's line). | C2-T6 (synthetic closures admit through production admission); C2-T7 (a release build has no synthetic root: a source pin, as X8 item 4f); C2-T8 (a synthetic-labelled Run refused by any authoritative surface, at C2a's boundary: the label is carried, and its refusal leg belongs to J2's authoritative surfaces) | C2a-1 |
| **C2a-3** | **Retention of the whole tree** (`PROPOSAL.md`:430): the closure's manifest body and every tree file's bytes, retained by raw SHA-256 with `BLOB_LENGTH` checked against each Blob (SL:41-48). **Gated** (LD-C2A-5). | the retained bytes equal the Blobs; a length or digest mismatch refuses; no symlink is followed into the tree | C2a-1; an owner of installed component trees (LD-C2A-5) |

**Order:** C2a-1, then C2a-2, then C2a-3 once its gate is met. **C2b-1 needs C2a-1 and C2a-2** for its context's closure names and its tests. Whether it also needs C2a-3 (retained stdlib bytes for the `libSelection` membership rule) is Q1.

## 3. Lead decisions

- **LD-C2A-1. Admission composes after the trust reader and R10a.** C2a-1 takes only a component the ordinary trust reader has already verified. It never parses an envelope or a catalog itself, and never verifies a signature (item 7: "both verified by the M2 trust owner", `PROPOSAL.md`:412). D4's R10a excluded-form check (EE-1, EE-3b, EE-4's manifest part, EE-5a) runs before it, and row 8 selects among R10a's set (S19). That this is R10a's admitted set is a **composition precondition** owned by J1's ordering and D4, not something C2a-1's type proves.
- **LD-C2A-2. The kind comes only from CR-1's table.** `closure_kind` (`component_manifest.rs`:39-49) is the one source. `evaluator`, `detector` and `adapter` are never manifest roles (`PROPOSAL.md`:427). A caller-asserted kind, or one inferred from a path, is never accepted (:440).
- **LD-C2A-3. The projection is SL's exactly.**
  - Each `type=file` entry of the selected platform's `tree.entries` maps to `Blob {path, sha256: entry.sha256, bytes: entry.length}`, with the same path string. `dir` and `symlink` rows are not Blob members (SL:41-48).
  - Blobs are ordered by `path` bytes, as the schema's `x-opensip-order` requires.
  - More than 100,000 files refuses (the schema's `maxItems`, `identity-v3.schema.json`:253), never truncating.
- **LD-C2A-4. The descriptor's other members, from the admitted bytes only.**
  - `manifestDigest` is the raw SHA-256 of the body (IE:272-276), which the trust reader has already checked equal to the release's.
  - `semanticVersion` is the manifest's `version`.
  - `platform` is the selected platform's catalog `artifacts[].platform` string (SL:35-38), so the closure's platform spelling is the signed catalog's own and no new spelling is invented.
  - `protocolMajor`: no source names the manifest member it comes from. The candidate is the manifest's `compatibility` object (for example `providerProtocol` in the fixture body, `core_authentication.rs`:568). This is Q2, and C2a-1 does not guess.
- **LD-C2A-5. Tree retention is gated on an owner of installed component trees.**
  - Item 7 retains the whole tree (`PROPOSAL.md`:430), so the tree's file bytes must come from somewhere. The signed catalog names each platform's release `artifacts[{platform, archiveProfileId, archiveDigest, sha256}]` (SL:35-38).
  - **No accepted M2 or M3 law, and no product code, installs or extracts a component's tree** from those artifacts into custody. X4B carries the catalog and component manifests (`m2/trust-bootstrap-x4b/PROPOSAL.md`:100-137), and 463h retains the catalog and component-manifest pairs (:199). Neither carries tree bytes.
  - So C2a-3 waits for the law and owner of component delivery (DR-103, per SL:30-31). That is the lead's cross-law item **X-C2A-1**.
  - Until then, production admission can mint identities (C2a-1), and the synthetic generator supplies tree bytes for tests (C2a-2). **No production context names a closure whose tree is not retained:** C2b-1's consumers fail closed on an unretained tree, and C2a-3's absence makes the durable path's required-closure case the existing `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED` disclosure (`PROPOSAL.md`:435-436). That reading is Q3.
- **LD-C2A-6. The synthetic generator uses only public fixture signers.**
  - It reuses `INDEX_SIGNER` and `COMPONENT_SIGNER` and the synthetic root that `core_authentication.rs` already uses (:563-565). These are public, deterministic, test-only seeds, under the joint fixture predicate.
  - It reads no operational key, and no private test key outside that existing public fixture set.
  - A release build carries no synthetic root (C2-T7, X8 item 4f). It is a source pin over the predicate's absence in a non-test build.
  - No new signing key, root or role is introduced.
- **LD-C2A-7. The no-trust-view case** (`PROPOSAL.md`:431-437). With no admitted trust view (I positively absent, or F absent under the read session), the trust reader returns no components, so C2a-1 admits nothing. Item 9's core role closures are unaffected. C2-T18's Plan and result legs are C4a's and J2c's, as the law assigns them (:453).
- **LD-C2A-8. Item 9's remaining legs.**
  - The four core role projections and their identities exist (`core_inventory.rs`:417-421).
  - C2a's own item-9 deliverable is **the C2-T9 vector check**: D″ equals D′ except `kind`, the ids differ, and `manifestDigest` is the body's SHA-256. It is confirmed against CRC-1's bound vector (`crc-1/`), or added if no product test asserts it.
  - The field-use restrictions are enforced where each field is admitted, not by C2a:
    - C2-T10 and C2-T11 at the emission-row join (X12d, item 19; the evaluator's join at `composition.rs`:765-774 already checks `semanticClosures` membership and `kind: detector`);
    - C2-T12, C2-T13 and C2-T13a at the Plan and view owners (C4a and H; the law gives C4a C2-T13's Plan leg, `PROPOSAL.md`:549).
  - C2a lists each against its owner, and claims none.
- **LD-C2A-9. Refusals are typed.**
  - `ClosureRefusal {Platform, Tree, Kind, Field, Bound, Identity}`.
  - The trust reader's own refusals (`Manifest`, `MissingRelease`, `BodyDigest`, `Preimage`, `MissingProof`) pass through unchanged.
  - The public projection is J1's and J2's (rows 27 and 56).
- **LD-C2A-10. Work bounds.** C2a-1's projection is linear in the manifest's tree entries, at most 100,000. It is charged to the caller's ledger, the discovery or trust read's, with each entry charged before it is projected. No new cap is introduced.

## 4. Controls

C2-T1 to C2-T8, C2-T9 (LD-C2A-8) and C2-T18's admission half, as §2 maps them. Also:
- a manifest whose release digest disagrees is refused by the trust reader before C2a-1 (`BodyDigest`);
- a `dir` or `symlink` row is never a Blob;
- 100,000 files admit, and 100,001 refuse `Bound`;
- the descriptor is admitted by identity-v3's `$defs/closure`, and its id recomputes independently;
- a synthetic closure and a hand-built one over the same bytes are the same `closure2` (deterministic generator).

## 5. Mutations

Each must fail the controls:
- a symlink row projected as a Blob;
- a `dir` row projected;
- the kind taken from the manifest's own `role` string, bypassing `closure_kind`;
- `manifestDigest` over the envelope;
- the platform taken from the host's spelling rather than the catalog's;
- a missing platform admitted;
- the Blob order unsorted;
- the generator signing with a non-fixture key path;
- the synthetic root reachable without the predicate.

## 6. Checks

The lane covers:
- the security and host suites at base and candidate;
- warning-denied all-targets Clippy, rustfmt, and the focused tests;
- the release-build source pin;
- the environment exceptions, the operability source census with its mint audit, the census-closure check and verify_design;
- the mutations.

## 7. Open questions

- **Q1.** Does C2b-1 need C2a-3 before it can mint a TypeScript context, that is, retained stdlib bytes for `libSelection` membership (NE:1501-1519)? Or can it join by the admitted tree's Blob digests, with retention a later owner's? **Recommendation:** C2b-1 joins by Blob digest at mint. A replayable Run still needs C2a-3.
- **Q2.** Which manifest member is a component closure's `protocolMajor` (LD-C2A-4)? No source names it. **Recommendation:** ask the owner of component-manifest schemas v11 (DR-103) rather than choose.
- **Q3.** Is it right that, until C2a-3, a durable required closure is disclosed as not installed (LD-C2A-5), rather than admitted with an unretained tree?
- **Q4.** Should the generator live in `core_authentication.rs`'s test module (extended), or in a new fixture module that both use (recommended, without changing the existing tests' bytes)?

## 8. Not delivered

- Component delivery and installation (X-C2A-1).
- C2b-1 and C2c.
- Item 9's field-use enforcement at the Plan, view and emission owners (LD-C2A-8).
- Any production caller beyond R10a's composition.

## 9. Not claimed

- No trust-owner change, no new key, role or root, and no qualification.
