# SM-ORIGINAL-RUSTFLAGS-CONTROLS-r1

Supporting review of the frozen first-party original build and target rustflags controls. The subject is `subject.json`, 674931 bytes, SHA-256 `72855567ce5367e5a08f06a4c827ec95fc64c75d061bb2a72cc8a4bcb599f87e`, schemaVersion 1, unit `SM-ORIGINAL-RUSTFLAGS-CONTROLS-r1`. It has 3315 unique members, does not include itself, and rehashes with 0 missing and 0 mismatched digests, 101355597 member bytes.

`source.json` is 1185672 bytes, SHA-256 `df74cd8b13cc032faf73e3b092aba588025a1f81abc24404f5734cecf6f6e46f`, standing `FROZEN FIRSTPARTY ORIGINAL BUILD/TARGET RUSTFLAGS AND EXACT INFO QUERY VECTORS`. `draft-source.json` is 1185551 bytes, SHA-256 `5fadfdbde14bdbb202fd3f39e31857e8a7099e9be1359ef5bd2207fcf50e5417`. The draft body matches the frozen record aside from the standing text and the frozen product and architecture bases. Those bases are product `95279fa8ae086f98bd221cd827f6c0efc156c0c5` and architecture `e785e11e990d51b2fcf47b030c23f4fd1fbf7154`.

## Source census

The frozen producer tree is 3130 files and matches `finalSourcePins` byte for byte. The closed original-config parent pins name the same 3130 paths. Exactly one file differs:

`src/cargo/util/context/experimental_command_data.rs` is 53737 bytes, SHA-256 `8d61b30498a779f2dc1de4de065f9ec94f83fce1cbf3686030d6587174369ea3`. The closed parent copy is 46108 bytes, SHA-256 `f3cc36e7fb562ab09b69c229bcc1d068aea54838ad5e1e1cb2b332589cfb3556`.

`crates/cargo-util/src/process_builder.rs` has the same pin in both censuses. The closed producer tree still matches every closed pin, 0 missing and 0 mismatched. The closed Cargo image is 78464328 bytes, SHA-256 `8ea3dee89071e417e24c24100c2dd0ecb67aa115e237ff5f65822dea74fe4ad3`. The frozen image `compiled-image/cargo-lib-tests` is 78538872 bytes, SHA-256 `9e6bd79607690fcbdc895d53a70fcd38abfc2d2021d6bbd4551838c77ede2809`. The pinned rustc image is 412504 bytes, SHA-256 `b829b733131d4e1673eeebd1f34d06ae1e9ff4977b051313cf42e2a9e79ecf1c`, and the live image matches that pin.

The closed reference `subject.json` is 658982 bytes, SHA-256 `f22242bc93b82d411f8ba69eaa8bd891c8f3fc9ebd547eb21c5cfb8c1d3658fa`. Its `source.json` is 1186821 bytes, SHA-256 `fb8c282605a7487749a36eeb27984b01a10057da46ca0249692265902c26ab1a`, unit `SM-LARGE-ORIGINAL-CONTEXT-CONTROLS-r1`, 14 controls. Its `REVIEW.md` is 11277 bytes, SHA-256 `5ed79af95f73c7e957c94d812565e76d0a1ae08a7e68d156806016a4456b9149`, and its `review.json` is 1512 bytes, SHA-256 `a5176e0ac6f0efb7ea934c55428d4a777a28de0d874397f77ecfde32efbc941d`. Those files match the accepted large-context review and frozen record. This review leaves that unit closed. Architecture HEAD `e785e11e990d51b2fcf47b030c23f4fd1fbf7154` records that publication.

`authoring-r1.json` is 518 bytes, SHA-256 `2dc40f2874003c150a431cad721091004278eeee62286824df9f326da5c85801`. It pins the closed collector digest and an intermediate after-digest `af84d1888d09e2883570912e6755d9eeb20e27a951a1d961f0e8b3ad7770b913`, standing unreviewed. The frozen census file above is the authority.

## Seven controls

`original-rustflags-checks-r2.json` is 1013 bytes, SHA-256 `767fa30fde63e96dc922fb8dccbee9490df6269a6262d2f89e1fc19f6ced38ed`, `allPassed` true, exit 0. The log is 1854 bytes, SHA-256 `4dc1b90059ff09377aa06fafd30ef6ce2e4d9e6c500dadbabc4efa1c190e5ca8`: 7 passed, 0 failed, 218 filtered out. The seven tests are build-flag definition preservation, operational-override refusal, wrong-type refusal, the actual build-flag graph, the cfg fixed-point graph, the explicit-target plus cfg graph, and the stable-compiler nightly-flag refusal.

The preserve-original mode now allows `build.rustflags` beside `target-dir`. A `build.rustflags` value must be a list of strings. A string that names a codegen backend, a sysroot, or an extern is refused, as is a non-list value. The definition test compares the projected Cargo config value with `ConfigValue::from_toml` for `['-C','force-frame-pointers=yes','-A','unknown_lints']`.

`original_flag_lists` reads Cargo’s resolved explicit `target.aarch64-apple-darwin` rustflags, `build.rustflags`, and `target_cfgs` rows. Cargo’s cfg-table load sorts those keys. The function refuses more than three cfg rows, then enumerates every subset in that order, at most eight masks. Each subset starts from the explicit triple list; an empty combination is replaced by the build list. Duplicate lists are dropped. That population is a private experimental allowlist. It is not a native constant.

Those exact vectors are assembled with `-vV` and the host print probe, then installed by replacing `experimental_rustc`, before environment registration and before `Workspace::new`. `configure` and the flag-list reader do not launch rustc. The argument lists contain no wildcard. No runtime bootstrap is added. The closed process-builder checks for program, cwd, wrappers, empty stdin, and the executable byte pin remain, because that file is unchanged. These four fixtures have no `[env]` table, so each retained environment record is 8 bytes and decodes to a count of zero.

`graph` still calls `create_bcx` and `capture_experimental_command_data`. That capture path is `BuildRunner::new`, `prepare_units`, `prepare`, and `prepare_rustc`. `compile`, `dry_run`, and `JobQueue::new` stay outside it.

## Four graphs and 24 information queries

Each project is the first-party package `original-rustflags` 1.0.0, edition 2024. Every `src/lib.rs` is 51 bytes, SHA-256 `cdd8ec672b0a4c3382da78a7c71461e10adb79e4bdcf106e79dd6899f6ca0a6a`, and contains `compile_error!`. Each config pin matches the retained config bytes. `project/target` is absent. The three successful static commands use `--out-dir` `observation/target/aarch64-apple-darwin/debug/deps`, `compilerLaunched` false, and `HOME` absent. Their target trees have no rmeta or rlib output.

| Control | Queries | Result | Config pin |
| --- | --- | --- | --- |
| Nightly flag | 4 | rustc exit 1 | `1a5dd1fe84d66859377fa1d90e5d75d66d6594d3348e0cac67a16890a4f5e069` |
| Build flags | 6 | graph success | `811835987b185b0d4487af038ae6defcb1383c1d0d8ebaab5dc7dc275d78857e` |
| Cfg fixed point | 7 | graph success | `8e6224a6c820b28c4d8616ba5cc781bda514f7c67fa888ff8065ca1337950863` |
| Explicit target plus cfg | 7 | graph success | `a29dd9fdb1f7230a3bf9da235ab4637f584657eae503cdae7a7cf75bf9b6a48d` |

4 + 6 + 7 + 7 = 24. Every query retains arguments, an environment record, status, stdout, and stderr.

The nightly config is `[target.'cfg(all())']` with `rustflags=['-Zshare-generics=y']`. Three information probes exit 0. The fourth probe’s arguments include `-Zshare-generics=y` and its status is exit 1. The retained compiler text says the option `Z` is only accepted on the nightly compiler. `control.json` is 1388 bytes, SHA-256 `71f99d9b4dbedb5cce1424a1020a875dd86b07946fcabe5a00e15203d8d38e76`, `graphSuccess` false. No unit graph and no unit-command record are present. The refusal stays a real incomplete compiler result.

The build-flag graph’s static command contains `force-frame-pointers=yes`, `force-unwind-tables=yes`, `unknown_lints`, and `mismatched_lifetime_syntaxes`. Its command record is 5989 bytes, SHA-256 `b1c1ce4e2e85c12696d05c03e2d26f5276854ee8e07c60171d1082ab60489058`. One information probe carries that same flag list.

The cfg graph’s config is `[target.'cfg(all())']` with `--cfg tokio_unstable` and `-A clippy::all`. The static command contains both `tokio_unstable` and `clippy::all`. Its command record is 5877 bytes, SHA-256 `9b9b4cd57d391a5c3c6764f28ce3d232a0a6b56223a9536609b80b0ff66bc9b1`. The probes include the plain target vector and the cfg-flag vector.

The combined graph’s config has explicit `target.aarch64-apple-darwin` flags `force-frame-pointers=yes` and a `cfg(all())` row `--cfg tokio_unstable`. Separate probes carry the explicit list alone and the explicit list plus `tokio_unstable`. The static command contains both `force-frame-pointers=yes` and `tokio_unstable`, which is the combination Cargo selected. Its command record is 5890 bytes, SHA-256 `de8f770b4af364b9c0e06d63dd73a13de5de5e0e09350028d6223bbf4e8ca0c7`. Each successful command record has `BuildRunnerConstructedForStaticData` true and `BuildRunnerCompileOrDryRunCalled` false. The recorded dev profile fields remain static command data; full profile completeness stays open.

## Initial build failure

The first build failed before any control ran. `FAILURE.md` is 198 bytes, SHA-256 `f55714068c03528acac6997d0926f307973a424f4b6e3c2f1e3c2f11ca9d0249`. The log is 1950 bytes, SHA-256 `7cff41ce0b26af87485dca77b097bab39a65f2a83fa0e55c5a6fbd6345ecd032`, and reports `E0599`: `StringList` has no method `into_vec`. The check receipt exit code is 101, `allPassed` false. The retained historical collector is 53719 bytes, SHA-256 `74340dd8712732f7ce803f3f8bb32ef3e3f718c5b0b8340656a091324fdc278c`, and contains two `into_vec` calls. The frozen collector contains `as_slice().to_vec()` and no `into_vec`. The historical runner equals `runners/run_sm_original_rustflags_checks_r1.py`, 2476 bytes, SHA-256 `cd33ffac6887399778d34f59340a2fa14590e76f59b077ee660051d33b2f00eb`. The r2 runner is 2476 bytes, SHA-256 `7f57746996d4fdd6c51231f1cff86a656c965221a2f44cd359c7e1487c339096`. No historical runtime query child is retained. The fresh seven controls are a separate run. Closed parent controls were not replayed.

## Open gates

Product HEAD is clean at `95279fa8ae086f98bd221cd827f6c0efc156c0c5`. `design-lock.json` is 630770 bytes, SHA-256 `6f041cb13f35f04092268c6906008bb060658fbfadb470b3fd03f2ea8b53c409`, with inventory successor v187 and 161 contract successors. O7 is `ADOPTED-EXISTING-PROPOSAL`, and D3 and D13 are `SIGNED-OFF`, each with `currentlyBlocks` false. The untracked `docs/implementation/m3/syntax-e/e2s/` tree is outside this unit.

No corpus source, Sui workload, alias, build script, proc-macro, or application was executed. Source authentication, native admission, a complete runtime command, full Cargo profile completeness, physical peak scratch, a complete statistical set, full S-M, effective L, product qualification, and the entire plan stay open. Native production admission is not an extra gate for this outside-product control.

This review’s own exact substantive assent, and a fresh design-and-implementation verification, remain due before an architecture-only publication of this support record. Publication stays unpushed.
