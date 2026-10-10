# SM-CONTROLLED-RESOLVER-r1

ACCEPT. Subject manifest SHA-256 `bad612b8973ed5cbe764733c4fbba12f12a4efd2b31fd4a6a3473b7e8e22062f` (23361 bytes, 131 sorted unique members, one trailing newline). This is supporting evidence for three final first-party resolver and Check-graph fixture controls. `supportingOnly` and `fixtureOnly` are true. `controlsPassed` is 3. `actualChildInvocations` is 12, all rustc information queries. Product code, the inventory, and the design lock stay unchanged. `corpusResolutionRun`, `nativeAdmission`, `firstUsePermissionGranted`, `SMComplete`, `effectiveL`, `productQualification`, and `entirePlanComplete` remain false.

The closed Cargo information branch stays closed. Its ACCEPT review is pinned at 498 bytes, SHA-256 `e5f5176d5f146da0904cb3769e78a64dc4e956e28c948d4961d0750bf65db446`, subject `9be077c1250d9ed946554aee2acd32ab167009d7bf62eeb3fc640fd947d07fd0`. That branch was not re-audited. `src/cargo/util/rustc.rs` 17269 / `b1698e9bc9cfa7ac863b931ddaabc5352f9e45c2c155b7d1d6866f7afd47ad44` and `crates/cargo-util/src/process_builder.rs` 34441 / `3c6e09b15176547b1629057f1a4814dc99a8dd46bb98f8ffd722298f6bbcb912` are byte-identical to that closed producer. `src/cargo/util/context/mod.rs` grows from 107318 / `218187d8d22820c675ef74b1a76159d0c8f698232cf02ba82c354acac5df4683` to 107368 / `71209e715baf6d3f0291b7e8207c5e00aec7205f5d948733f0ac8a185194f3e3` by the test-module line `mod experimental_resolver_controls;` only. The new control is `experimental_resolver_controls.rs`, 8081 bytes, SHA-256 `ed6db740d2621757ca6119a754f6957060589afbad9a26111b62944d54711905`.

## Pins

Product HEAD is clean at `95279fa8ae086f98bd221cd827f6c0efc156c0c5`. Committed `design-lock.json` remains 630770 bytes, SHA-256 `6f041cb13f35f04092268c6906008bb060658fbfadb470b3fd03f2ea8b53c409`. Architecture HEAD is `cf1b6e33baaeae32b61f076dd6107fadbc0c29e2`, message “Record reviewed explicit experimental Cargo information branch and controls.” Architecture porcelain is only the untracked `docs/implementation/m3/syntax-e/e2s/` tree, which stays outside this unit.

`Cargo.lock`, both Cargo manifests, `build_config.rs`, `unit_graph.rs`, `features.rs`, and `cargo_compile/mod.rs` match the closed producer byte for byte. The separate authoring image is 76451816 bytes, SHA-256 `0364c61ad871079247692b3c1512ab4cf33457f16d72248f8c99ec984c39bf5c`. The closed parent image remains 76253464 bytes, SHA-256 `7b96247ff80fc273e1ebdd08d019f8817f5a42dee0fce707fa215c51d9baca8a`. Member hashes, graph identities, and query digests were recomputed from the frozen copies. The control process, rustc, and Cargo stayed as archived.

## What the three controls run

Each control writes a fresh five-member workspace and calls the closed experimental context with an empty config map, an empty environment map, no jobserver, and the pinned compiler. `configure` sets offline true, with frozen and locked false. `Workspace::new` then sees no lock and writes one. `CompileOptions` uses `UserIntent::Check`, `Packages::Default`, and requested kind `aarch64-apple-darwin` with JSON-target support false. The control calls `create_bcx` and `emit_serialized_unit_graph`. It does not construct `BuildRunner` or call `compile`.

The workspace manifest lists members `app`, `dep`, `macro_pkg`, `build_helper`, and `linux_only`, with `default-members` `app` and resolver 2. The generated `Cargo.lock` is version 4, 418 bytes, SHA-256 `2bec3635511568ee4b9a61eee1edd6a8537dc1736a73220cb80bc5767253e0aa`, and the same bytes in all three roots. It names those five packages and carries no registry source and no checksum. Feature selection is in the unit graph, not in that shared lock text.

`app` depends on path package `dep` under the extern name `renamed` with `default-features` false. Feature `picked` forwards `renamed/chosen`. Feature `with-macro` selects optional `macro_pkg`. A `cfg(target_os = "linux")` dependency names `linux_only`. `app/src/lib.rs` contains `compile_error!`, and `app/build.rs` contains `panic!`. Dependency libraries contain `compile_error!` as well. Each retained project has those sources and no `target` directory. Each control record sets `fixtureSourcesExecuted` false, `unitGraphOnly` true, and `generatedExperimentalLock` true.

Each private home contains a 57344-byte `.global-cache`, SHA-256 `882ac79220cd9683530756836d479da6e9272f1e5da5d63277339df055a1965a`, identical across the three roots, and a zero-byte `.package-cache`. The cache bytes include the schema text `CREATE TABLE registry_src` and contain no `crates.io` text and no `http` URL. No `.rustc_info.json` is present. That home file is not a registry resolution or a public download.

## Indexed graphs

The serialized graphs are Cargo version 1. Every dependency index falls inside the unit array. Identity of package, target name, kind, mode, platform, feature list, and dev profile is unique inside each graph. Every unit uses profile `dev`. The Check root index is 0 in each graph, and the only root package is `app`. `linux_only` appears in none of the three graphs.

Default features off, macro off, `unit-graph.json` 4261 bytes, SHA-256 `dbe8ed63cbf7a4b2e6c138e98e83aa92d165487787808b2a6232faa669cd5f19`, five units:

- 0, `app` lib, mode `check`, platform `aarch64-apple-darwin`, features empty, edges to 1 as `build_script_build` and 4 as `renamed`.
- 1, `app` custom-build, mode `run-custom-build`, same platform, edge to 2 as `build_script_build`.
- 2, `app` custom-build, mode `build`, host platform, edge to 3 as `build_helper`.
- 3, `build_helper` lib, mode `build`, features empty.
- 4, `dep` lib, mode `check`, platform `aarch64-apple-darwin`, features empty.

Default features on, macro off, 4323 bytes, SHA-256 `a800bb11e391f8a43dcb6ffe38873283f377bf9209d2cbefbdc2270b34ad7af4`, the same five units. `app` features are `default` and `picked`. `dep` features are `chosen` only. The `renamed` edge remains.

Default features on, macro on, 5217 bytes, SHA-256 `47e0441f49a0bfe115df444c7931b02acbe995d0a1611e455aba2be2b6e6d357`, six units. `app` features add `with-macro`, and unit 0 gains an edge to 5 as `macro_pkg`. Unit 5 is `macro_pkg`, kind `proc-macro`, mode `build`, features empty. `dep` still has `chosen` and not `ambient`.

So `default-features = false` keeps the real `dep` edge while leaving `ambient` off. `picked` is what adds `chosen`. Disabling default app features removes `chosen` and keeps the edge. The requested Apple target excludes the linux-only dependency. The proc-macro unit and both custom-build units are graph entries. Their source was not compiled and the build script was not run: the only rustc outputs are the information queries below, and a fixture compile would have failed on `compile_error!` or `panic!`.

A readonly walk of each retained graph starts with every `custom-build` and `proc-macro` unit, then adds every unit that depends on an unavailable unit. It blocks indices 0, 1, and 2 in both five-unit graphs, and 0, 1, 2, and 5 in the six-unit graph. The other units are 3 and 4 each time: `build_helper` and `dep`. Root 0 is blocked in every graph because the `app` check unit depends on `run-custom-build`. These counts match `fixture-graph-observations.json`, 1664 bytes, SHA-256 `3acedcbfec78adfdc02204a3bcb2c089f2ee9caa4a6a9a3169da510ae5f0f8af`. The blocked root is unavailable expansion input. It is not a successful fixture typecheck and it supplies no per-subject cost, timing, native RSS, or peak-scratch sample.

## Twelve rustc information children

Each fixture retains query 0 through query 3, all `exit status: 0`, with empty stderr. Query 0 and query 3 are `['-vV']`, stdout 192 bytes, SHA-256 `e61cba8ded8c60e985f759f74a221c4773649021477d00b44c7af411eb8c218c`. Query 1 is the 21-argument empty-flag host vector, stdout 1114 bytes, SHA-256 `2b195f138dac5b59ca958a0aff88549e608c0dccbac2c45e55739b2d6fd6d0b3`. Query 2 is that vector plus `--target aarch64-apple-darwin`, the same stdout digest. The three roots repeat those four outputs. That is twelve children. The second version file is a new ordinal with the same bytes, so the call is fresh rather than a reused collector. No argument vector contains a linker flag. These are the closed branch's registered version, host, and requested-target vectors. This review does not reopen that branch.

## Final record and the earlier summary pass

`resolver-controls-r2.log`, 1296 bytes, SHA-256 `84591d699d9833b7b07d70ed6f9914be9c6dc6126151d8f01bc494547f838550`, records `running 3 tests` and `test result: ok. 3 passed; 0 failed; 0 ignored; 0 measured; 180 filtered out`, finished in 0.25s. The three tests are `no_default_features_keeps_real_dependency_without_feature`, `default_member_features_target_and_renamed_path_dependency`, and `selected_macro_and_custom_build_remain_graph_units_without_execution`. `resolver-checks-r2.json`, 656 bytes, SHA-256 `5756d5781d9afaf00b56894c69fa0404d4669ce1bcea65a5565c2ea728228986`, records exit 0, niceness 10, an owned ordinary checks lane, and HOME unchanged. The invocation is `cargo test --locked --offline` for filter `experimental_resolver_controls`, after `rustfmt --edition 2024` on the closed process and rustc files, `mod.rs`, and the new control. No failed resolver run is in the packet.

The earlier three passes remain under `history-r1-summary-graphs`. Their log, 1297 bytes, SHA-256 `7bd389a8c65986eb665c48b6ed2edd9e93060179461e16f9d8eece5dc81f0561`, also records 3 passed, and it names three earlier roots. Their checks file is exit 0. `NOTE.md`, 489 bytes, SHA-256 `878dbef15e5544d88045ed70e3e575550ab4466d4d872aac33e7c12776770aa0`, states that those passes kept package-level assertion summaries. The historical control, 7391 bytes, SHA-256 `16bdf35b1cef1f8c438d3af73aeb3c078e1f1bf113fda5ebc480f5c31f1825d8`, differs from the final control only by the `emit_serialized_unit_graph` retention and the assertion that the serialized unit count equals the in-memory graph. The r1 and r2 runners differ by those output names. The final graphs are the retention pass. The earlier pass does not establish it.

## Open work

These limits stay explicit. The acceptance covers three first-party fixtures, their offline path lock, the indexed Check graphs, the expansion-unavailable reading, and twelve borrowed information queries. Corpus locks, registry resolution, public acquisition, original config and definition provenance, rustflag provenance, the two T2 serde and serde-json workspaces, and named overlay links remain open. Runtime closure, source, profile, owner, and worker admission remain open. Full query populations, read and resource accounting, confinement, and peak bounds remain open. `⟨SM-4⟩`, `⟨SM-11⟩`, `⟨SM-12⟩`, `⟨SM-13⟩`, `⟨SM-14⟩`, F, T, full S-M, effective L, and qualification remain open. The older collectors stay untouched. This packet authorizes no corpus collector.

Production native admission stays a separate gate. This fixture support adds no production-admission prerequisite to throwaway S-M. Later corpus-input, config, and dependency preparation still owes its own controls.

Own substantive assent and actual design and implementation verification precede an architecture-only archive of this exact support. The design verifier remains unrun for that archive. The archive leaves law, product code, the inventory, and the lock unchanged, and it pushes nothing. Review acceptance alone grants no dependent gate. Effective L remains at ML5.
