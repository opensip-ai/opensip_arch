ACCEPT for SM-CARGO-LINT-SPELLING-CONTROLS-r1 as supporting-only experimental evidence. `review.json` records `supportingOnly` true, `controlsPassed` 4, `compilerChildren` 3, and `compilerInformationQueries` 6. `newGraphExecutor`, `capturedManifestLintSpellingsPreserved`, `nativeRustflagsProjectionUnchanged`, and `acceptedParentsUnchanged` are true. `newCargoSource`, `newRustWrapper`, `controlsRerun`, `actualCorpusUse`, `applicationExecuted`, `completeRuntimeCommand`, `fullCargoProfileEnvironment`, `completeStatisticalSet`, `physicalPeakScratchMeasured`, `sourceAuthentication`, `nativeAdmission`, `firstUsePermissionGranted`, `productChange`, `SMComplete`, `effectiveL`, `productQualification`, and `entirePlanComplete` stay false. `requiredFindings` is empty.

The subject manifest is 15802 bytes, SHA-256 `96ea3deb2d4370e3cbfaa460bc9b4a113cdd63f16a4beacdafda4fceebc10018`, schemaVersion 1, unit `SM-CARGO-LINT-SPELLING-CONTROLS-r1`, 82 unique members, 676390 member bytes. Every member rehashed in place, with zero missing and zero bad. The frozen source standing is “FROZEN OUTSIDE-PRODUCT CARGO MANIFEST HYPHENATED LINT SPELLING CONTROLS”. The draft sibling keeps the same counters and its pre-review standing sentence. The retained control report keeps its pre-review standing sentence as well.

## Closed parents

The new executor is the closed lint-command executor plus one header comment and a hyphen in two DATA character classes. That parent executor is 13715 bytes, SHA-256 `d74f03e951fe88fd38ad0576bcac61f86976062b84d733ad8c8b001ac50afba3`, and the live file matches. SM-LINT-COMMAND-PROFILE-CONTROLS-r1 stays closed. Its published subject is 25907 bytes, SHA-256 `6d64f40a2dc9ae59c53168e173a27180e3180539d180aa519da4944980f3e642`. Its review is 1003 bytes, SHA-256 `509bcad4e16e12113c637652546f79fd6f8ee9bc72e440349b5dd5239b032240`. The packet’s closed-parent copies match those bytes. That publication is architecture `bf75300569d361dc4f2a8d0112b13077938b709a`.

SM-COMMAND-PROFILE-CONTROLS-r1 stays closed at architecture `5480e20e5668e4278d2071fc1ef1611789892b35`. Its subject is 15954 bytes, SHA-256 `310efe8ce130ac6ac3d162fc867474811365974a13a70ff0ed4bdbe96dd06fe2`. Its review is 892 bytes, SHA-256 `1d31c052fba141ae8512defc42e064b738ad375690ba3ad98dc6709884f7d42f`, with `verifyDesignPassed` true. SM-COMMAND-DATA-CONTROLS-r1 stays closed at architecture `2d3df4e7668eb9192a4248cf03a6357c7a343e68`. Its subject is 26822 bytes, SHA-256 `5c5e99f6e6c74b40136803ff311ab010d619bdf071883e053c5cb6e25963e096`. Its review is 991 bytes, SHA-256 `80a92f51c85279e6d30644c71112d044709464b30750cc6da38e298ad1a9b85f`, with `verifyDesignPassed` true. Those published files match the source record. Their controls stay closed.

The new executor is 13846 bytes, SHA-256 `4dc32ce85bc5af5db6561a8a46be60150786d791ea1d5ad7334e459ca6bafd67`, and the live file matches the stage copy. The Cargo image is 78269832 bytes, SHA-256 `e3d15902981ae680ca05b7a4355866450750914df1ace29e24aade2408fa7b06`. The wrapper image is 180840 bytes, SHA-256 `c8cde6df1bb5f0608244d320537c31d34bb2d7658664152a16183294372c2adb`. Both live files match. `newCargoSource` and `newRustWrapper` stay false.

## Parser and bound grammar

The parent source contains `'[a-z0-9_:]+'` in exactly two places: the separated `--warn`, `--deny`, `--allow`, and `--forbid` value, and the joined `--warn=`, `--deny=`, `--allow=`, and `--forbid=` suffix. Replacing those two classes with `'[a-z0-9_:-]+'` and prefixing the header comment reproduces this executor exactly. No other line differs. Captured arguments are appended as the same strings. This parser does not rewrite a hyphen to an underscore or split a joined argument.

Section 3.3 of the bound native evidence names `RustflagsProjectionV1` lint syntax `[a-z0-9_:]+` for `-A`/`-W`/`-D`/`-F`, the attached short spellings, and the long forms, and limits `--cap-lints` to `allow`, `warn`, `deny`, and `forbid`. The packet’s law reference is 329013 bytes, SHA-256 `83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0`, byte-identical to `docs/v2/contracts/product-v1/native-evidence.md`. Line 1772 still states lint name syntax `[a-z0-9_:]+`. The experimental class adds a hyphen only inside this outside-product DATA check. The bound projection grammar stays the published class.

## Fixture and four controls

The owned fixture manifest quotes four lint names:

```toml
[lints.rust]
'unused-variables'='deny'
'rust-2018-idioms'='warn'
'unsafe-code'='forbid'
'unused-imports'='allow'
```

The captured command and all three launched argv lists retain, in this order, `--deny=unused-variables`, `--allow=unused-imports`, `--forbid=unsafe-code`, and `--warn=rust-2018-idioms`. The same rows also retain `--check-cfg` `cfg(docsrs,test)` and `--check-cfg` `cfg(feature, values())`. `HOME` is absent. `completeRuntimeCommand` and `fullCargoProfileEnvironment` are false on each launched record. The original `src/lib.rs` remains exactly `compile_error!("original fixture must not compile");` followed by a newline. Each synthetic map is `OPSMRUST1` with one entry, and its payload is the control program. None of those payloads contains `compile_error`.

The graph is one check-mode library unit, `lint_command`, edition 2024, and that unit is the only root. The collector outcome records success, `unitGraphOnly` true, `fixtureOrCorpusCodeExecuted` false, `experimentalLockCreation` true, and `originalBytePinsReobserved` true. Six information queries all exit 0 with empty stderr and 8-byte big-endian length prefixes: queries 0, 3, 4, and 5 are `rustc -vV`; queries 1 and 2 are `--print=file-names`. Query stdout stays in the packet.

| Control | Launch | Result |
| --- | --- | --- |
| `actual-four-lint-family-success` | 1 child | exit 0, `after_analysis`, metadata 2408 bytes, SHA-256 `47fc24ead74134f0da9c33db1555f224fdde83485c83b7e0ec5ebe312858e0ea`, empty stderr, standing `analysis-and-metadata-completed` |
| `actual-deny-unused-variable` | 1 child | exit 101, `after_analysis`, no metadata file, standing `incomplete`; stderr reports unused variable `unused` requested with `-D unused-variables` |
| `actual-forbid-unsafe` | 1 child | exit 101, `after_analysis`, no metadata file, standing `incomplete`; stderr reports an `unsafe` function requested with `-F unsafe-code` |
| `invalid-lint-data-prelaunch` | 0 children | `--deny=invalid lint spelling` raises `outside explicit joined lint argument DATA shape` before the output root exists |

The two failures still record `after_expansion` and `after_analysis` and then exit 101, which is the lint-denial shape. Their standings stay `incomplete`, and neither directory contains an rmeta. The success metadata file matches the recorded hash. Each graph result records `procMacroBuildScriptOrApplicationExecuted` false. The malformed context is the captured command with only that deny value replaced, and the packet contains no output directory for that refusal. Four controls and three compiler analysis children follow.

## Standing limits

O7 is ADOPTED-EXISTING-PROPOSAL. D3 and D13 are SIGNED-OFF. Those three rows carry `currentlyBlocks` false. The decisions file remains 9065 bytes, SHA-256 `db75be37dd896d7883437aece2e6bce72b8410e86d7a52908a041defa0344bdf`. Product HEAD is clean at `95279fa8ae086f98bd221cd827f6c0efc156c0c5`. `design-lock.json` remains 630770 bytes, SHA-256 `6f041cb13f35f04092268c6906008bb060658fbfadb470b3fd03f2ea8b53c409`. The r59 status files remain byte-identical to that accepted board, including checks 4291 bytes SHA-256 `ace005230081261e2f3637074f5e7742cc0d82f403e83fe413824c251a7b978a` with `scopedRecords` 148, accepted-work 355043 bytes SHA-256 `6b76e302ce4bb70793d1b9ef7c7aa4fee6fd7ddacf858cbf45961273e78bb43c`, and the front door 104990 bytes SHA-256 `57e65a4ecdb6e6c1795e872556f089b220f7ec4843f0c315039c2d2a50fa7e26`. Inventory 187 and contract successors 161 stay the figures recorded there. Architecture HEAD is `a73e16ad33430d059e001fff41f6740a5bff45dc`, parent `bf75300569d361dc4f2a8d0112b13077938b709a`, message “Record reviewed remaining context pilots and nine exploratory sample series.” The untracked `docs/implementation/m3/syntax-e/e2s/` tree stays outside this unit. This unit is absent from both repository heads.

The earlier nine-entry attempt, including its refusals and analysis children, stays outside this packet. Corpus use, application execution, build scripts, and proc macros stay unrecorded here. A complete runtime command, a full Cargo profile environment, source authentication, native admission, physical peak scratch, a complete statistical set, full S-M, effective L, and product qualification stay open. Effective L remains ML5.

This review used read-only hashes, JSON, and git. `verify_design`, Cargo, the control runner, and the closed controls stayed unrun. Own root substantive assent and design-plus-implementation verification of this support snapshot remain due before an architecture-only evidence publication and before experimental use. That publication, when made, publishes this evidence only. Review acceptance grants no dependent gate. Nothing is pushed, and no law, lock, code, or native permission follows from this acceptance.
