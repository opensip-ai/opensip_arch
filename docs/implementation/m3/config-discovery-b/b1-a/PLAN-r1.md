# B1-a implementation plan r1 (M3-B unit B1-a: the configuration resolver)

**Lead plan record, 2026-10-14. Not law, not code.** M3-L is in effect from 2026-10-14 (L r7), so B1-a, the first unit of M3-PLAN r10's host chain, may start. Its dependencies are met: P0 (integrated), L (in effect) and B-S9 (bound at `8adfe0c`). This plan fixes how B1-a is built, before any code is written, and names one design prerequisite found while reading the product. Codex reviews it.

**Authority.**
- M3-B r4 (`config-discovery-b/PROPOSAL.md`, cited as MB):
  - items 1, 2 (B1-a's half), 4 to 8, 10 and 11;
  - the B1-a row of "Units after the law" (MB:875);
  - B-S9 (`b-s9/README.md`).
- AQ §1 and §1.1 (`admission-and-qualification.md:8-187`).
- PCS (`foundation/product-configuration.schema.v2.json`, `591a66e5…`, 10,262 bytes) and PCM (`product-configuration-model.py`, `055ab34c…`) with its checker (`check-product-configuration.py`). All three are in the accepted approval source manifest (`candidate-subject.v45.json`).
- HFC §3 (`completion/host-foundation-completion.v2.md`, the preview carrier, for item 11).

## 1. What B1-a delivers (MB:875)

These all go in `crates/host/src/configuration.rs` and its tests, and the work is pure, with no I/O:
- **The pipeline** (MB item 4), in its order:
  1. lexical admission;
  2. schema;
  3. per-layer allowlist;
  4. merge;
  5. logical paths;
  6. registry admission;
  7. defaults completeness;
  8. partition;
  9. normalize;
  10. semantic validation;
  11. digest.
- **`ResolvedConfigurationV1`** (item 5): the semantic record, the operational record and per-leaf provenance.
- **`resolvedConfigDigest`** (item 6): lowercase hex SHA-256 of the canonical bytes of the normalized semantic record. It is not an H-identity.
- **The operational partition** and its rules O-1 to O-6 (item 7), with an invariance-control template for S-OP-5.
- **The FW-13 registries** (item 8) that B1-a consumes: the PCS pinned source and its registry row, the generated classification table, and the capability-ID enum. The recognizer and shared-flag enums are listed in item 8, but discovery (B2) and the CLI (M4) consume them. B1-a generates the shared-flag enum because the resolver must type layer 6. It reuses the existing generated recognizer enum, and adds no consumer.
- **The X12 order** (item 10): `resolve` returns the resolved `policy.packIds`, and `admit_policy_selection` runs on them immediately after resolution. It runs once, with no other step in between.
- **Schema-one carriers** (item 11): admission through the exact preview carrier schema, then in-memory projection with `sourceSchemaVersion: 1`.
- **B-S9's remedy string** at `REMEDY_CONFIG_INVALID`: 706 ASCII bytes, SHA-256 `7ba6e8e5…`. `doctor_ingress.rs` reuses it, and the pin test in `configuration_tests.rs` is repinned.

**B1-b, not B1-a, owns:** the carriers and their custody capture (X2 r9 item 3a), `I/host/settings.json` access, the computation of `InvocationModeV1` from terminals, and the item 9 environment structural check. B1-a consumes those as **typed inputs**. Its entry point is pure over captured bytes and typed observations:

```
resolve(ResolverInputV1 {
  defaults: CompiledDefaultsV1,            // typed, host-built
  release: &ReleaseDeclarationRegistryV1,  // profiles, capability availability
  global: Option<CapturedCarrierV1>,       // bytes + carrier path + sha256
  project: Option<CapturedCarrierV1>,
  local: Option<CapturedCarrierV1>,        // never read when mode.interactive is false
  flags: FlagLayerV1,                      // typed: workspaceRoots only at M3
  mode: InvocationModeV1,
}) -> Result<ResolvedConfigurationV1, ConfigurationRefusal>
```

Layer 5, the environment, is a typed constant: empty. It is not a parameter.

## 2. Design prerequisite: the configuration schemas' admission successor (B-S10, proposed)

**The finding.** Runtime schema validation in the product goes through `opensip_identity::RegisteredSchemas`. That registry is pinned by `SOURCE_PINS` (`crates/identity/src/schema_registry.rs:33`), and its source set is exactly the **admission** registry's (48 sources). It is not `schemas/registry.json`'s (40). `verify_design` requires `schemas/admission-registry.json` to be byte-equal to an accepted architecture registry, currently `docs/implementation/m3/native-publication/rust3-identity-materialization-r1/admission-registry.json` (`a85500ef…`).

So PCS cannot be validated at runtime by the shared mechanism unless an accepted admission-registry copy lists it. The schema-one preview carrier (`completion/preview-configuration.schema.v1.json`) is in the same position. MB item 8 names only a `schemas/registry.json` row and "the existing schema-pin checks", and did not foresee this.

**Lead decision: a small design unit, B-S10, before B1-a's product commit.** It takes the precedent's form (the rust3 identity materialization):
- a new accepted copy of the admission registry with two added rows, `urn:opensip:product-configuration:2` (PCS) and the preview v1 carrier;
- `$id` values exactly as the schemas declare;
- sorted by schema ID, as `verify_design` requires.

It is reviewed by Codex as ACCEPT-DESIGN-UNIT and bound in `design-lock.json` as a contract successor. B1-a then adds:
- `schemas/sources/product-configuration-v2.schema.json` and `preview-configuration-v1.schema.json`, byte copies;
- their rows in `registry.json`, `source-map.json`, `admission-source-map.json` and `admission-registry.json`;
- `SOURCE_PINS` and host `SOURCES` entries;
- the generator closure for any generated carrier.

**Rejected.**
- **A hand-written PCS validator in `configuration.rs`.** It duplicates the schema, and MB item 8 forbids hand-maintained vocabularies in the resolver.
- **Exporting `opensip_identity`'s private `Program` for a standalone compile.** It widens the identity crate's public API for one consumer and bypasses the pinned registry.

## 3. The generated registries (MB item 8)

- **Classification table.** A reviewed mapping file, `crates/host/src/configuration_classes.json`, assigns every PCS leaf exactly one of DRC's two classes (DRC:588-589):
  - `host.analysis.semantic`: analysis, components, discovery, policy, evidence;
  - `host.operability.nonsemantic`: `retention.*`, `ui.color`.

  A test walks the pinned PCS bytes. Every leaf must have exactly one row, and no row may name a non-leaf. The table is the resolver's only partition source.
- **Capability IDs.** A tool, `tools/host/generate_configuration_tables.py`, reads NCM (a lock input, `native-capability-matrix.v2.json`) at its pinned bytes and writes `configuration_tables.rs`: the capability enum, the per-mode `NOT-SELECTED` cells and CINV's seven shared flags with their classes. It records each source's SHA-256 in the generated file, and the tool's `--check` mode is the drift check. The tool reads and writes no product authority beyond that file.
- **Recognizers.** The existing generated `Native2FrameworkRecognitionResultV1RecognizerId` is the registry. B1-a adds no copy.
- **Waivers.** These are an empty registry at M3, so any waiver ID refuses `CONFIG.INVALID`.
- **Profiles and capability availability.** These come from the authenticated release declaration registry, an admitted input whose type is NE's `ReleaseCapabilityRegistryV1`. Tests use a `cfg(test)` synthetic registry. B1-a does not authenticate it; its signature check belongs to the release unit that supplies it (MB item 8, row "Capability availability").

## 4. Refusals (MB item 4, "no new code")

Every refusal maps to an existing generated code, in X12's termination shape:
- **External input.** Lexical, schema, allowlist, path, an unknown registry ID, components and the schema-one mapping give request-rejected, exit 2, `CONFIG.INVALID`, with B-S9's remedy and a subject naming the layer and JSON pointer. AQ:334's `CONFIG_PROFILE_MISSING` and `CONFIG_PROFILE_UNREGISTERED` are reference-model refusal names, not generated codes. No `CONFIG.PROFILE_*` detail exists, so both use detail `CONFIG.INVALID`, with subjects `profile:missing` and `profile:<id>`, and the mapping is pinned in a test.
- **Host invariant.** An invalid compiled-defaults document, `CONFIG_DEFAULTS_INCOMPLETE`, and an invalid semantic record after resolution give the host-invariant row, as X12 row 4 shapes it.
- **Custody.** `CONFIG.CUSTODY_REFUSED` is B1-b's, at capture time. B1-a never sees an unjudged carrier.

An exhaustive `match` without a wildcard arm keeps every refusal on exactly one row.

## 5. Byte vectors (MB item 4 controls)

`tools/host/configuration_vectors.py` runs PCM, the accepted reference, over a fixture set:
- every case in `check-product-configuration.py`;
- each layer's win and loss at every adjacent pair;
- the permutation, invariance and sensitivity cases of item 6;
- a schema-one projection case.

It writes `crates/host/src/configuration_vectors.json`, with each fixture's layers, registry and expected `resolvedConfigDigest` or refusal class. The product test pins those digests. The tool runs only on arch bytes, which it checks against their accepted SHA-256s. A fixture PCM cannot express, such as item 2's layer allowlist, which PCM does not model, is tested in Rust only and is labelled as having no PCM vector.

## 6. Tests (MB controls; AQ:183-187)

- **Per-step controls.** One negative test per pipeline step and per registry. A swapped-order mutation, for example sorting before duplicate detection or validating after the merge, must fail its test.
- **Layers.** The adjacent-pair win/loss matrix for every layer, and the per-layer allowlist matrix over every PCS leaf and layer.
- **CI mode.** A hostile `local` has no effect when `mode.interactive` is false, and the local carrier is never parsed.
- **Digest invariance and sensitivity.** The digest is unchanged by provenance-only moves, operational fields, flag-only selections and permutations, except `allowedScopes`. It changes for every semantic leaf. All five sections are always present.
- **Schema-one.** A round trip of each mapped field; an unmapped field refuses; the input bytes are unchanged.
- **X12 order.** A refused project-layer pack ID refuses at admission, with nothing else run.
- **Remedy.** The repinned length and SHA-256, and `doctor_ingress` reuse.
- **The O-4 invariance template** for S-OP-5.

Verification uses the standard lane:
- `cargo test --locked --offline -p opensip-host` and the full workspace suite;
- all-targets Clippy with warnings denied;
- `tools/verify_design.py`.

## 7. Sequence

1. **This plan,** reviewed by Codex.
2. **B-S10** (design unit; arch only): the admission-registry copy. It is Codex-reviewed and bound, as a contract successor, by its own product lock commit.
3. **B1-a code:** the stage, checks, Codex review, product commit, then the inventory successor (v188) and its bind. These are separate commits, and nothing is pushed.
4. **Status rounds** after each publication.

## 8. Not claimed

This plan writes no code and binds nothing. It changes no law. It chooses no S-OP-5 field, no release registry content and no B1-b carrier mechanics. It neither authenticates the release registry nor claims product qualification.
