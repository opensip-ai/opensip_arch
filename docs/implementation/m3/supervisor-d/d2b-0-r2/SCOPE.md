# D2b-0 r2: the successor schemas, admission-only (D2b plan r3, sub-unit D2b-0, as LD-D2B0-A re-sequences it)

**Lead scope record, 2026-10-16. Unreviewed candidate, round 2. This unit proposes one narrow D2b plan amendment, LD-D2B0-A, for acceptance with it: a deferral that re-sequences D2b-0's generator work into a new sub-unit, D2b-0b. It changes no requirement.** Accepting the unit accepts the amendment. Until it is accepted, D2b plan r3's text stands as written.

It implements D2b-0 of the D2b plan, r3 (accepted, `codex-d2b-plan-r3`): FA-2's and RUST3-LIM's two new schema documents are materialized at their product paths, rebased on RCA-1's product handshake (LD-D2B-13). Under LD-D2B0-A they are **admission-only in D2b-0**:
- they enter the admission registry, its architecture copy, the admission source map, the identity crate's compiled `SOURCE_PINS`, and the host's and storage's embeddings;
- they enter **no generator table**, so no generated carrier changes here. The generator rows, the generator profile extension, the regenerated carriers and the blind refresh are D2b-0b's (LD-D2B0-A).

It is a contract successor (the admission registry's architecture copy is new), like RCA-1's materialization. Its subject is the successor record and its candidates.

**Base:** product main as the subject manifest names (C1a3 integrated; 173 contract successors).

## Round 2

Round 1 (`codex-d2b-0-r1`, subject `8b5f799c…`) returned REQUIRED-FINDINGS. The product code was assessed **ACCEPT-UNIT**, and LD-D2B0-A was **REJECT**ed under one finding.

- **D2B0-R1-RF-1: the hand-written carrier branch exceeds a plan amendment. Accepted.** Round 1's LD-D2B0-A let D2b-3 and D2b-4 decode the successor payloads into hand-written typed carriers that are never generated. That contradicts two authorities:
  - M3-D item 10 (`supervisor-d/PROPOSAL-r5.md`:381): "The decoded tree is converted by hand-written, schema-checked code into the generated carrier types";
  - both accepted materialization maps' standing passages, which require the implementing units to add the source-map rows, re-pin the registries and regenerate carriers.

  **The lead's resolution: LD-D2B0-A becomes a deferral only.**
  - It permits no hand-written carrier for either successor payload.
  - M3-D item 10 and both materialization maps' generated-carrier requirements stay in force, **unamended**.
  - The amendment only re-sequences them. D2b-0 is admission-only now, and the new sub-unit **D2b-0b** owes:
    - the generator's pattern-profile extension (the `SubjectIdV1` translation and `pattern-profile.json`, as a reviewed generator-input change);
    - the source-map, generation-registry and options rows, re-making LD-D2B0-1 to LD-D2B0-4 there, including the Root and root-law-annotation question;
    - the regenerated carriers;
    - the reviewed blind refresh.
  - D2b-0b is integrated before D2b-3 or D2b-4 consumes either successor payload.

  The revised text is below.

**Unchanged from round 1:** the product candidate (the nine paths, byte for byte), the package's other decisions (LD-D2B0-5 to LD-D2B0-8), lane attempt 3 (the lane of record), and the post-rebase check on the package base. No lane was run for this round.

**One correction to round 1's record,** noted by the review: the lane's `focused-identity-schema-registry` step's filter matches no test. Identity's coverage comes from its full 72-test suite (base and candidate equal, and re-run on the package base), and from the host and storage embedding tests. The checks list below says so.

**The admission registry's architecture copy** stays at `d2b-0-r1/admission-registry.json`, where the unchanged product admission source map points. It is a candidate of this round's successor record. Round 1's files are otherwise frozen history.

## LD-D2B0-A. The amendment: a deferral, with D2b-0b owing the generator work

**Why.** The generator cannot generate FA-2's census schema without a change to its own reviewed runtime profile:

1. **The pattern profile.** `symbol-census-v1.schema.json`'s `$defs/SubjectIdV1` (line 79) has the pattern `^[a-z][a-z0-9-]*:[^\u0000-\u001f\u007f-\u009f]+(?![\s\S])`. It is not in the generator's selected TypeScript pattern table, `tools/contracts/runtime/patterns.ts`, which is generated from a reviewed M1 pattern profile and is unchanged since `436d615`. The pipeline's `validate` step refuses it ("pattern outside selected profile"). The census's request, row and payload types all reach `SubjectIdV1`.
2. **The precedents.** The same pattern is in three schemas that are **admission-only, never generator sources**:
   - `relation-payload-v2.schema.json`:838;
   - `subject-inventory-v1.schema.json`:296;
   - `target-attribution-v2.schema.json`:356.

   Each is in the admission registry and the identity crate's pins, and absent from `schemas/source-map.json`, `schemas/registry.json` and `tools/contracts/options.json`.
3. **The root law annotations.** Each new schema's root carries one law keyword outside the generator runtime's closed annotation set (`tools/contracts/runtime/schema.ts`:17): `x-opensip-symbol-census-law` and `x-opensip-subject-scope-law`. `prepare.py` refuses converting either root.

   Every other keyword in the two schemas is in the selected set. This was checked by walking every schema node.

Generating these schemas therefore needs a reviewed extension of the generator's pattern profile and annotation set: a change to a reviewed generator input, and to the TypeScript runtime text embedded in `apps/report/src/generated/report.ts` and `providers/typescript/src/generated/protocol.ts`. That extension, and the generation it allows, are D2b-0b's, under its own review. They are owed, not waived.

**What it does not amend.** These stay in force exactly as written, and LD-D2B0-A only re-sequences them:
- **M3-D item 10** (`supervisor-d/PROPOSAL-r5.md`:381): "The decoded tree is converted by hand-written, schema-checked code into the generated carrier types. **Serde never deserializes wire bytes** …";
- **FA-2's materialization map** (`native-successors-fa/fa-2/materialization-map.json`, its `standing`): "Those units also add the census schema's source-map and admission rows, re-pin the registries and regenerate carriers …";
- **RUST3-LIM's materialization map** (`rust3-lim/materialization-map.json`, its `standing`): "Those units also add the new schema's source-map and admission rows, re-pin the registries and regenerate carriers …".

D2b-0 does their admission part. D2b-0b does the rest: the source-map rows, the generation-registry re-pin and the regenerated carriers. Neither D2b-3 nor D2b-4 may use a hand-written carrier for a successor payload.

**The D2b plan r3 text it replaces** (`supervisor-d/d2b/PLAN-r3.md`):

- **§1's table, the D2b-0 row** (:81).
  - Current: "| **D2b-0** | The successor schema materialization, FA-2's and RUST3-LIM's schemas, rebased on RCA-1's product handshake; then **a reviewed blind refresh** | the materialization's own checks; the refreshed receipt | — |".
  - Replacement, two rows:
    - "| **D2b-0** | The successor schema materialization, FA-2's and RUST3-LIM's schemas, rebased on RCA-1's product handshake, **admission-only** (LD-D2B0-A): the admission registry and its source map, the identity pins and the host and storage embeddings; no generator input changes, so the blind receipt stays current | the materialization's own checks; the census `--check` against the unchanged receipt | — |"
    - "| **D2b-0b** | The successor schemas' generation: the generator's pattern-profile extension (`SubjectIdV1`'s pattern, with `pattern-profile.json`, a reviewed generator-input change) and the root law annotations; the source-map, generation-registry and options rows; the regenerated carriers (M3-D item 10; both materialization maps); then **a reviewed blind refresh** | the generation checks; the refreshed receipt | D2b-0 |"
- **§1's table, the D2b-3 and D2b-4 rows' dependencies** (:82-83).
  - Current: "D2b-1, D2b-2, D2b-0" (each row's last cell).
  - Replacement: "D2b-1, D2b-2, D2b-0, D2b-0b" (each row's last cell).
- **§1, the order** (:85).
  - Current: "**Order:** D2b-1, then D2b-2, then D2b-0 with its blind refresh, then D2b-3 and D2b-4."
  - Replacement: "**Order:** D2b-1, then D2b-2, then D2b-0, then D2b-0b with its blind refresh, then D2b-3 and D2b-4. D2b-0b is integrated before D2b-3 or D2b-4 consumes either successor payload."
- **§1, the two bullets after the order** (:86-87).
  - Current: "**D2b-0 comes after the two mechanics units.** Its regenerated carriers change `tools/contracts/generator-closure.json`, a file the discovery census binds as reference-loading code. That makes the B2-b4c blind held-out receipt stale, and the census `--check` then fails on main." and "**So D2b-0 is followed at once by the reviewed blind refresh,** before any other lane needs the census: a pre-run Codex review of the blind mode, the lead's mechanical blind run (the owner's standing answer), and a post-run review. This is B2-b4c3's sequence."
  - Replacement: "**D2b-0 and D2b-0b come after the two mechanics units.** D2b-0 changes no generator input (LD-D2B0-A). D2b-0b's regenerated carriers change `tools/contracts/generator-closure.json`, a file the discovery census binds as reference-loading code. That makes the B2-b4c blind held-out receipt stale, and the census `--check` then fails on main." and "**So D2b-0b is followed at once by the reviewed blind refresh,** before any other lane needs the census: a pre-run Codex review of the blind mode, the lead's mechanical blind run (the owner's standing answer), and a post-run review. This is B2-b4c3's sequence. **No hand-written carrier** stands in for a successor payload's generated carrier in D2b-3 or D2b-4 (M3-D item 10)."
- **LD-D2B-13** (:135).
  - Current: "… and its review judges each, with the registry, source-map and admission updates and every regenerated carrier."
  - Replacement: "… and its review judges each, with the admission updates; D2b-0b's review judges the registry and source-map updates and every regenerated carrier."
- **§4, the repository checks** (:211).
  - Current: "For D2b-0, also its generation checks and the census `--check` after the blind refresh."
  - Replacement: "For D2b-0, also the admission-only assertions (no generator input or output changes) and the census `--check` against the unchanged receipt. For D2b-0b, also its generation checks and the census `--check` after the blind refresh."

§0's codec requirement (:54, "each payload decoded by hand-written, schema-checked code into the generated carriers") is **not** replaced, unlike in round 1.

LD-D2B-2's depth bound (computed in D2b-3 and D2b-4 over the complete successor-aware closure, "after D2b-0's materialization") is unchanged. The successor schemas are in the admitted registry from D2b-0 on, and D2b-3 and D2b-4 follow D2b-0b.

## What it changes

| File | Change |
| --- | --- |
| `schemas/sources/symbol-census-v1.schema.json` (new) | FA-2's accepted bytes (`95d84054…`, 19,045 bytes; `$id` `opensip.product.symbol-census.1`, 20 `$defs`). |
| `schemas/sources/rust-subject-scope-v1.schema.json` (new) | RUST3-LIM's accepted bytes (`17f9b5bc…`, 8,672 bytes; `$id` `opensip.product.rust-subject-scope.1`, 5 `$defs`). |
| `schemas/admission-registry.json` | Two source rows `{schemaId, sourcePath, bytes, sha256}`, in schema-ID order (50 to 52). No alias: the successors' design documents (`design/native/symbol-census.schemas.v1.json`, `rust-subject-scope.schemas.v1.json`) are published like the handshake's and startup's (`design/native/provider-handshake.schemas.v1.json`, `provider-startup.schemas.v1.json`), which have no alias row either. |
| `schemas/admission-source-map.json` | Two rows `{schemaId, implementationPath, architectureSource}`, pinned to the FA-2 and RUST3-LIM candidates (accepted contract successors); `registryArchitectureSource` re-pointed to this unit's copy, `d2b-0-r1/admission-registry.json`. |
| `crates/identity/src/schema.rs` | The schema compiler's annotation set gains `x-opensip-subject-scope-law` and `x-opensip-symbol-census-law` (LD-D2B0-7). |
| `crates/identity/src/schema_registry.rs` | Two `SourcePin` rows in `SOURCE_PINS`, in its schema-ID order (50 to 52). |
| `crates/host/src/schema_sources.rs` | The two `include_bytes!` sources, in pin order; and `successor_source_tests` (2 tests, below). |
| `crates/host/tests/admission_tests.rs` | `the_candidate_registry_is_storages_selected_registry`'s pinned source count, and two doc comments, from 50 to 52. |
| `crates/storage/src/schema_sources.rs` | The two `include_bytes!` sources, in pin order (X3d-2's copy of the same set). |
| `d2b-0-r1/admission-registry.json` (architecture) | The exact admission registry, the accepted copy the admission source map selects. |

**Unchanged** (asserted by the lane's design preflight):
- `schemas/source-map.json`, `schemas/registry.json`, `tools/contracts/options.json` and `tools/contracts/generator-closure.json`;
- every generator closure input that is tracked, and every generated output;
- `schemas/wire/native-carriers-v1.json`;
- the Cargo manifests and lock;
- the blind receipt and the census tool.

## Lead decisions

- **LD-D2B0-A** (above): D2b-0 is admission-only, and D2b-0b owes the generator work. It is a deferral only: M3-D item 10 and both maps are not amended.
- **Deferred with the generated carriers.** These are LD-D2B0-1 to LD-D2B0-4 of the generator route, which no longer applies here. They pass to D2b-0b, which makes them again and has them judged there:
  1. the type namespaces `SymbolCensus1` and `RustSubjectScope1`, module `protocol`;
  2. the source mappings (`declaredMajor` 1, profile `opensip-exact-schema-reference-1`, semantic owner `crates/components/src/provider_protocol.rs`, the shared standing text);
  3. the entry points: every `$def`, `typeName` = namespace + definition name. **No Root:** each root is a `$defs`-only container whose law annotation is outside the selected set, as common-v4's and graph-query-v4's roots have no Root entry point. The rule "Root plus every `$def`" has those two exceptions, and native-v2 leaves out its three denied definitions;
  4. no `providerEntryPoints` until the TypeScript codec needs them.
- **LD-D2B0-5. Placement (a lead placement decision).** Each new row goes before the first row whose key is greater. The keys are the schema ID, or the source path for the generation registry the unit no longer touches. The admission registry and the identity pins are fully sorted by schema ID, and stay so: `verify_design` requires it of the registry. The admission source map's sorted prefix (its two `urn:opensip:p…-configuration` rows are appended at the end) takes the rows at the same sorted position. The host and storage embeddings follow `SOURCE_PINS` exactly, which `from_sources` requires.
- **LD-D2B0-7. The identity compiler's annotation set (a lead placement decision).** The identity crate's schema compiler (`crates/identity/src/schema.rs`, `fn annotation`) refuses any keyword outside its closed set. Without the two new root law keywords, the embedded registry does not compile, and every registry consumer fails: lane attempt 1 was void with 139 host failures, all `Schema(Schema)`. The set already holds each admitted schema's own law keyword (`x-opensip-join-law` for target-attribution-v2, `x-opensip-law` for incoming-search-v1, `x-opensip-file-membership-extent-law` for enumeration-plan-v1, `x-opensip-derived-carrier-law` for execution-inputs-v1, and so on). The two keywords are added at the end, after `x-opensip-join-law`, as annotations: no evaluation changes. The prepare derives them from the two accepted documents, and asserts that they are the only `-law` keywords.
- **LD-D2B0-8. The lane base (a lead decision).** The package is built on lane attempt 3, base `3e70bbf`. The package base, the v218 lock commit, differs from it by D2b-1's code commit `d70af81` (the components' provider protocol files, the components' `Cargo.toml` and `lib.rs`, and identity's `lib.rs`, which gains `is_nfc` and `NFC_UNICODE_VERSION` additively) and the v218 lock commit. Both are disjoint from this unit's paths. The post-rebase focused check (see *Checks*) stands in for a full lane rerun.
- **LD-D2B0-6. The successor record.** The record names three parents, each already accepted: the previous admission-registry copy (`config-discovery-b/s10-tsc/admission-registry.json`), and FA-2's and RUST3-LIM's successor records. Its candidates are this package. The binding adds contract successor 174 and leaves the inventory unchanged.

## LD-D2B-13: the handshake

The re-derivation is recorded in `evidence/preparation.json`. RUST3-LIM's handshake candidate (`a08cc59e…`, which contains FA-2's edits) was merged three ways onto the current product handshake (`1fc57cbc…`, RCA-1's `5b53e5e`), against the maps' common before-image (`9090e2ad…`, product `436d615`), with `git merge-file`.
- It exits 0, and the result **equals the current product bytes**: RCA-1's materialization already carries both successors' handshake edits.
- **The differences from the maps' recorded after-hashes:** the maps' after-image is 35,746 bytes (`a08cc59e…`); the current bytes are 38,182 (`1fc57cbc…`). The difference is RCA-1's accepted materialization (`rust-commit-alignment-r2`, bound as product `5b53e5e`), applied after the maps were recorded, not a successor's edit; the merge shows the successors' edits are all present in it.
- D2b-0 changes nothing in the handshake.

## The tests

**`successor_source_tests`** (host, 2 tests):
- **every successor definition is selected under its document pin:** each of the 20 and 5 `$defs` resolves in the embedded registry, and its handle's document digest is the source's pin;
- **the shapes admit and refuse as published:**
  - `RustSubjectScopeV1` admits `subjectCount` 1 and 200,000, and refuses 0, 200,001 and an extra member;
  - the census's `Sha256Text` admits a lowercase `sha256:` digest, and refuses uppercase hex and a missing prefix.

  Shape is not semantic admission.

The existing registry controls cover the rest: a missing, extra, reordered or changed source refuses (host `missing_extra_reordered_changed_and_truncated_sources_refuse`), and storage's embedding is the pinned set (`the_embedded_sources_are_the_pinned_registry`).

## Checks

Lane r1, attempt 3, `evidence/d2b0-checks-r1/` (the lane of record), on product `3e70bbf` (the v217 lock commit, C1a3 integrated). allPassed. The runner and its detectors are in `evidence/`.

**Void history.** Two attempts were killed and are kept:
- **Attempt 1** (`evidence/d2b0-checks-r1-void-attempt1/`) was killed during the host comparison. The embedded registry did not compile, so 139 host tests failed with `Schema(Schema)`; LD-D2B0-7 fixed it.
- **Attempt 2** (`…-void-attempt2/`) was killed after the host comparison showed one new failure: `the_candidate_registry_is_storages_selected_registry` pins the source count at 50. Its count and comments are now 52, a direct consequence of the two new embedded schemas.

The checks:
- **The suites,** at base and candidate, with equal failure sets and no differing or flaky test:

  | Suite | Base: failed / passed | Candidate: failed / passed | New passing tests |
  | --- | --- | --- | --- |
  | identity | 0 / 72 | 0 / 72 | 0 |
  | host | 8 / 407 | 8 / 409 | 2 |
  | storage | 33 / 137 | 33 / 137 | 0 |
  | evaluator | 0 / 47 | 0 / 47 | 0 |

  Every failure is pre-existing on the base.
- **rustfmt** on the five edited Rust files (each base-clean, each candidate-clean), and warning-denied all-targets Clippy on identity, host and storage.
- **The focused tests:** host's `schema_sources` (29) and storage's `schema_sources` (1). The `focused-identity-schema-registry` step's filter matches no test, as round 1's review noted. Identity's coverage is its full 72-test suite and the embedding tests.
- **The design preflight** (`check_d2b0_preflight.py`):
  - verify_design on the candidate refuses for exactly one reason, "admission source is not selected by accepted design" (the unbound copy);
  - with only the copy accepted, it passes, with generation sources unchanged and admission sources 50 to 52 (aliases 15);
  - 99 tracked generator inputs and outputs, the Cargo manifests, the census tool and the blind receipt are the base's bytes. The 268 ignored pinned inputs (`node_modules`, `python-packages`) are absent from the worktree;
  - the changed paths are exactly the nine listed above.
- **The census `--check`** over the lead-readable cache passes: the receipt is current and no refresh is needed. Also FW-01, the environment exceptions, the operability source census (114 rows, no findings) and the census-closure check (no closure file changed).
- **Six mutations,** each caught by its named detector:
  - the host embedding omits the census (host);
  - the storage embedding omits the scope (storage);
  - a pin byte is changed (host);
  - the identity annotation set omits the census law (host);
  - the admission map omits the census (preflight);
  - the admission registry omits the scope (preflight).

**The base difference (LD-D2B0-8).** The package base is the v218 lock commit. It differs from the lane base by D2b-1's code commit `d70af81` and the v218 lock commit. D2b-1 touches the identity crate only in `lib.rs`, additively (`is_nfc`, `NFC_UNICODE_VERSION`), and is disjoint from this unit's nine paths. A post-rebase focused check on the package base, with the candidate applied, is recorded in `evidence/d2b0-postrebase-check/`. It runs the identity suite, host's `admission_tests` and `schema_sources`, and storage's `schema_sources`, each under the lane lock, each compared with attempt 3's result for the same tests: **all equal**, with the candidate's nine paths byte-identical to attempt 3's edited set:

| Tests | On the package base: passed / failed | Attempt 3: passed / failed |
| --- | --- | --- |
| identity suite | 72 / 0 | 72 / 0 |
| host `admission_tests` | 10 / 8 | 10 / 8 |
| host `schema_sources` | 29 / 0 | 29 / 0 |
| storage `schema_sources` | 1 / 0 | 1 / 0 |

The same 8 `admission_tests` failures are the base's pre-existing ones.

## Inventory and binding

- **Two new product paths** (the two schema sources): an inventory successor follows acceptance.
- **Contract successor 174** binds the record, the subject, the review and the root assent (LD-D2B0-6).

## Not delivered

- **The generator extension, the generator rows, the regenerated carriers for the successor payloads and the blind refresh:** D2b-0b, under LD-D2B0-A, before D2b-3 or D2b-4 consumes either successor payload.
- **The codecs:** D2b-3 and D2b-4.
- **The depth bound:** D2b-3 and D2b-4 (LD-D2B-2).

## Not claimed

- No codec, no semantic admission of a successor payload, no caller.
- No qualification; D2b's completion is not claimed.
