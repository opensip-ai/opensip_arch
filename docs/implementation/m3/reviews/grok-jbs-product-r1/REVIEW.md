# J-BS product schema and regeneration r1

Verdict: ACCEPT-UNIT.

This is the implementation leg required by the accepted J-BS/S13 design. That design review remains ACCEPT-DESIGN-UNIT: `review.json` is 159 bytes, sha256 `bbbe00df12e466f456536926f482b4914f55f779bff15bc9e5fcbab6bbfc43cf`, and its subject manifest is 1448 bytes, sha256 `238093ec4bb5f266f2ecc32f8af12453e120ec43b276da630cb6fcf9d4a365c5`. This review leaves that record unchanged.

Product HEAD is `2146910cca62e2dce492e7b637e4c2d11390c419` and its porcelain is empty. Architecture HEAD is `23bfb5d1dab2acc079d1ab9e34b7156807839ce1` with no tracked changes. The candidate snapshot is `/tmp/opensip-implementation/jbs-product-authoring/product`. Neither repository has a commit for this unit. Across every tracked product path, the candidate differs in exactly eight files. The snapshot's gitignored `tools/contracts/node_modules` and `tools/contracts/python-packages` copies match the product worktree. The OpenSIP support directory is absent.

## Schema

`schemas/sources/invocation-v5.schema.json` is 71837 bytes, sha256 `63f97dfcb77d3065c4a5f4af3194fbe0e874cc89a8b9e2533728da2a4af28ec0`, byte-identical to the accepted design candidate. `$id` remains `urn:opensip:product-v1:workflows:evaluator3:invocation:5` and `schemaMajor` remains the integer 5. `RetentionDisclosure.required` remains `policy`, `provenance`, `firstUse`, and `storageRoot`. `backupStatus` admits exactly `backed-up`, `not-backed-up`, and `unknown`. The single `allOf` branch requires `backupStatus` when `firstUse` is true and forbids it otherwise. Compared with the product schema at HEAD, that property and that branch are the whole schema delta.

`schemas/sources/command-envelope-v7.schema.json` is byte-identical to HEAD. Its `retentionDisclosure` reference remains `urn:opensip:product-v1:workflows:evaluator3:invocation:5#/$defs/RetentionDisclosure`. The empty-errors interrupted branch still forbids `retentionDisclosure` through `not.anyOf`.

## Joins and regeneration

The 349-member generator closure keeps the same `schemaVersion`, `profile`, and `toolchain`. Node, the Rust generator, and Python stay on their existing pins. Exactly three closure rows change: `schemas/source-map.json` (28565/76409db5… to 28561/43e34d45…), `schemas/sources/invocation-v5.schema.json` (71161/28aa0c42… to 71837/63f97dfc…), and `tools/contracts/confinement-profile.json` (sha256 only, ca125726… to 3f9da49d…, still 809 bytes).

`dependency-policy.json` stays 5199 bytes. `dependencies`, feature profiles, features, owner, standing, and package are unchanged. The only local source pin that moves is `src/generated/invocation.rs`, from 407313/774dffc9… to 409358/a44964c7….

`registry.json` stays 20211 bytes. `recipes[0].generatorClosureSha256` becomes `2d6ece9eb8ab35444e9b0b1ed700472e988f0ec753440db2b9ba0ef92343fa94`. The sorted `sourceSha256s` list replaces `28aa0c42…` with `63f97dfc…`, which shifts indexes 8 through 15 and no other digest. `sources[25]` remains invocation 5, declared major 5, implementation path `schemas/sources/invocation-v5.schema.json`, and semantic owner `crates/host/src/invocation.rs`, with `sourceSha256` `63f97dfc…`.

`source-map.json` changes only `sources[28].architectureSource`. The implementation path, schema id, declared major 5, and semantic owner stay put. The architecture source is now `docs/implementation/m3/host-pipeline-j/j-bs-r1/schemas/invocation-v5.schema.json`, 71837 bytes, sha256 `63f97dfc…`. That path is the accepted design candidate and is not yet in the architecture repository, which matches the required design-then-product bind order.

Regeneration recorded 40 sources, 857 entry points, and eight outputs. `invocation.rs` and `report.ts` take the new pins. `evidence.rs`, `identity.rs`, `mod.rs`, `output.rs`, `protocol.rs`, and `providers/typescript/src/generated/protocol.ts` match the unchanged pins in both the product HEAD and the candidate. The authoring script passed the candidate closure and explicit registry and closure provenance into the existing development pipeline and wrote the candidate tree. It records `sourceApproved`, `confinementQualified`, and `productModified` false. The recorded input snapshot, 68206 bytes, sha256 `4a43f141a4cda1476a8ab37f126ced971f9e00cec346d518338176f9225f9bb2`, is the pipeline's selected-files document, distinct from the 68280-byte closure document.

`Invocation5RetentionDisclosure.backup_status` is `FieldPresence<Option<Invocation5RetentionDisclosureBackupStatus>>`, with serde default and `skip_serializing_if = FieldPresence::is_missing`. The unchanged `FieldPresence` carrier in `evidence.rs` keeps an omitted field missing and a present null present. The enum renames are exactly the three schema spellings. `first_use` stays a required bool. The added Rust has no cross-field conditional. The host, creator, notice, and emitter sources are outside the eight-file diff, so actual M3 classification and J-C18/J-C19 remain with J3d.

`report.ts` changes its registry and closure provenance lines to `223d4154…` and `2d6ece9e…`. `Invocation5RetentionDisclosure` gains optional `backupStatus` and the generator's `allOf` intersection. The existing shape checker already applies `allOf`, `not`, and `if`/`then`/`else`. Of the 40 embedded schema strings, only invocation 5 changes, and the new string decodes to the candidate schema file.

## Runtime pin

The development profile remains `macos-seatbelt-development-1` with timeout 300. Of the four runtime pins, only `/System/Library/CoreServices/SystemVersion.plist` changes, from 600/49533878… to 604/`bd61e19dd67dd97ce9a27c79a2148d42cc9685a71c6f17ff27d62b819f39f983`. The live plist matches that pin: ProductVersion 27.0.1, ProductBuildVersion 26A434, ProductName macOS. Live `dyld-support.sb`, `system.sb`, and `/usr/bin/sandbox-exec` match the unchanged pins. No helper, policy, tool, or source version moves.

## Supplied execution evidence

This review did not run Cargo, the generator, the confinement probe, or the authoring scripts. The supplied logs are the executed checks.

The shape script loads the candidate `report.ts` through the candidate TypeScript and checks the invocation 5 retention definition and command envelope 7. Its arithmetic is 72 presence cases (3 policies, 3 provenances, both `firstUse` values, and four backup states), 22 malformed cases, and 9 interrupted cases. `shape.stdout` matches `shape-checks.json`: passed, those counts, `emitterRan` false, and `productQualification` false. `shape.stderr` is empty.

Contracts `cargo test --locked --offline -p opensip-contracts --lib` finished in the candidate tree and ran 0 tests, with 0 passed and 0 failed. `cargo clippy --locked --offline -p opensip-contracts --lib -- -D warnings` finished with no warning line. `cargo check --locked --offline --workspace` finished the dev profile. `build-checks.json` records exit 0, an owned lane, `nice` 10, and a private `0700` temporary directory for each command, with `productQualification` false. The checker sets `CARGO_HOME` and does not assign `HOME`.

Seven confinement records match their captured output. The confined Node probe exited 0 with outside-canary, shell, loopback, and listen denials, and both listeners stayed unseen. The unconfined control exited 0, read the owned synthetic canary, ran the shell, sent loopback UDP, accepted loopback TCP, and observed both listeners. Confined generation exited 0 and printed `generated six Rust files`. The outside-read and outside-write generations exited 101 with `PermissionDenied`. The unconfined generator control exited 0 with the same success line. Undeclared `/bin/sh` exited 71 with `sandbox-exec: execvp() of '/bin/sh' failed: Operation not permitted`. The probe script is the existing native-repin reprobe, 3930 bytes, sha256 `b63117cbca47fbbbec2c96678814a7f95675098dfbaaa309eb19463e26cb1dee`. The canary text remained `synthetic outside canary\n`. The evidence records the support directory absent. These runs are development runtime-pin controls. They grant no release, portable, O7, or provider qualification.

## Successor and inventory

Subject manifest sha256 `8d44699c63fe127427b1b2b0689d13f5171f2217e3248bdf3682f10b82feff0c` (10708 bytes). All 47 members match their pins. Successor `docs/implementation/m3/host-pipeline-j/j-bs-product-r1/successor.json` is 11386 bytes, sha256 `ab350b38550dd9cde288ce791a1f24cade05bca29dfd7cb86b9781674b9b32a3`. Its standing is the proposed J-BS product schema and regeneration record with one macOS development metadata pin update. `passageOverrides` is empty and `passageSupersessions` is absent. Its candidates are the other subject members. The three parents match the architecture copies and the product-before pins: confinement profile `ca125726…`, dependency policy `f283f3a1…`, and generator closure `22fcd1f8…`.

Bound inventory v166 is 614780 bytes, sha256 `d1d5e69aeacbef99d33fcfd4f4881c72e8671cda04e036156f1412c17c30926d`. All eight product paths already have rows. Those rows carry path, package, role, description, generated, and standing, and they do not pin content hashes, so this leg leaves inventory v166 unchanged.

After acceptance, the strict public `generate_contracts` drift check, with genuine review and lead assent in temporary architecture and lock staging, is still required before repository integration. It may only corroborate these frozen bytes. Design successor binding comes before product successor binding. The code commit and the design-lock commit stay separate. Nothing is pushed. Full M3, J3d emission, and product qualification remain open.

No required findings.
