# NATIVE-COMMON-MATERIALIZATION-R1

Verdict: ACCEPT-DESIGN-UNIT. The isolated product-code assessment is ACCEPT-UNIT. requiredFindings is empty.

This accepts the exact merged native and common materialization and the private failure projection. Consumer admission, full C2a, full C3a, authenticated provenance, whole S-M, effective L, and product qualification remain open. Review acceptance grants no dependent gate.

## Subject

The subject manifest is 14160 bytes, SHA-256 `b417533976ccdf2d9fb24c42f93be0094910a3131b7429f68c932872a4b7a507`. It lists 57 unique sorted members, and every staged member matches its recorded length and SHA-256. The review copy matches the staged subject.

Product main is clean at `12e0ad13f4443bb525470d4922ec4c8b897ce6aa`. Architecture HEAD is `929ec858b48a74b240678a8895da7a969125a3b6`. The isolated tree `opensip-native-public` is detached at the product base and modifies exactly the 15 paths in the materialization map. Each isolated file matches the candidate pin and the staged copy. The same paths on main match the map's before pins. The untracked architecture path `docs/implementation/m3/syntax-e/e2s/` is outside this unit.

## Merged sources

`common-v1`, `common-v3`, and `common-v4` append `native.closure-protocol-invalid` and `native.input-import-invalid` to `DomainDetailCode`. Every previous enum value stays in order. Those codes and their remedies are the accepted C2PM-1 and NIJ-1 public details, and the host-invariant remedy remains the accepted host-bug text.

`native-v2` adds the nine accepted route objects. The previous 18 routes are unchanged. `acquisitionSourcePath` now uses the accepted NIJ-1 `oneOf`: the previous string bounds, minimum 1 and maximum 4096, or null. Both `DependencySourceManifestV3` and `DependencySourceSealV3` `manifestSha256` properties equal the accepted DT-MD1 objects, including the deterministic-CBOR entries-array annotation.

## Pins, aliases, and generation

The source map's 40 rows keep their owners, implementation paths, and identities. The four changed architecture pins name this unit's source copies and match the product bytes.

The admission map's 48 rows keep their identities. Its registry pin and the four changed source pins match the admission registry and the product files. All 48 admission source rows match the product files. All 15 aliases keep logical document, schema id, and source path, and each alias digest equals its source row. The updated alias digests are native evidence v2 and common v1.

`registry.json` keeps one recipe and the same eight output paths. Its source hash list is the sorted set of the 40 source rows, with the four previous document hashes replaced by the four merged hashes. `generatorClosureSha256` is the new closure file. The compiled identity source registry updates those same four full-document pins, including the 32-byte digests.

`generator-closure.json` keeps 349 paths, the same profile, and the same Node, generator, and Python toolchain pins. Six rows change by length and SHA-256: `schemas/source-map.json`, the four schemas, and `tools/contracts/pipeline.py`. The selected Node, generator, and Python renderer images match those unchanged pins. `pipeline.py` removes the child `HOME` override and keeps the deny-default profile together with `PATH`, `LANG`, `LC_ALL`, and `TZ`. The closure's ignored Node and Python package inputs are regular files and match their pins. Generation recorded the same eight outputs. `report.ts` and `evidence.rs` changed to the candidate hashes. The other six outputs match the product base byte for byte. The generation record claims no source approval, confinement qualification, or product qualification.

## Private projection

The new private enums cover the 23 selected registry pairs: four closure-protocol keys at the three registered origins, four native-import keys at externally supplied spec and host-generated internal layer, and `native.input-import-configured` at external configuration, externally supplied spec, and host-generated internal layer. External configuration is expressible on configured-import. The closure-protocol and other native-import keys have no external-configuration variant.

`native_input_failure_projection` is crate-visible. It takes this host's `RequestContext` and a private refusal. The envelope request id is the id this host allocated for that context. A context from another host returns `Projection`. An older `ReleaseDeclaration` refusal returns `Projection`. The envelope is schema family `opensip.product.envelope`, major 7, kind failure. Exit is 2 for request-rejected and 4 for operational-failed. Fault cause is present where the selected boundary names `host-invariant`. `domainDetail` is omitted where that boundary is null, and where the boundary names a detail it is the single `errors` object. That object uses the registry envelope detail as its code, the accepted remedy, and the raw guard bounded to 1024 code points. The envelope has no plan or run identity. The owning authenticated boundary and the retained Run rechecks remain unimplemented.

## Retained checks

These records were read and were not re-run. r1 failed to compile on a moved `envelope_schema` test handle. r2's outcome filter selected zero tests, with 279 filtered out, and is excluded from the counted validation. r3 ran 17 outcome tests and six failed with `SourceBytes` while the compiled pins were stale. r4 passed those 17 tests, including the 23-origin envelope test and the foreign-context and old-route refusal. Host Clippy `--all-targets -D warnings` exited 0. rustfmt edition 2024 on the touched Rust sources exited 0. r5 passed 7 host schema tests. Its identity `schema_registry` filter selected zero tests, with 68 filtered out, and is excluded from the count. r6 passed all 68 identity library tests, with zero filtered out. The records use the ordinary lane and a private mode 0700 temporary directory. `tools/operability/exceptions.json` is unchanged at 83200 bytes, SHA-256 `b5cc19ba3b1f29c14c534deb5d20eb6ab69408c710e8cb35d4c85f94226f3cb0`, with 113 source rows. The operability source record also reports 113 rows.

## Before a lock commit

The source preflight records 40 generator sources, 48 admission sources, and 15 aliases for the prospective selection. Its standing is consistency of that selection, and it claims no acceptance. `verify_design.py` was not run. Full `verify_design` under this review and real assent is required before the lock commit. The live design-lock is 618900 bytes, SHA-256 `9253e9245e4b800ce3bb3583c2fe436db28da84b2705afa702f5f87e7be2297c`, with 156 contract successors and selected inventory v181. `inventoryUnchanged` is 181. `contractSuccessorsAfter` is 157 when this proposed successor binds, unless another contract binds first. The subject has no inventory successor and no acceptance or scratch pin. The code commit and the design-lock commit stay separate. Nothing is pushed.
