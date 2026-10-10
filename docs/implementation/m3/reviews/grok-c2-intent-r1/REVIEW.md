# C2-INTENT-PREIMAGE-SUPPORT-R1

ACCEPT-UNIT. The candidate adds one bounded byte-preimage helper on three existing identity-crate paths. The helper implements the C2 `opensip.plan-intent.v1` NFC domain-tag recipe. Closed PlanIntent schema admission, whole C2a, a native worker, whole S-M, effective L, and product qualification stay open.

Subject manifest `docs/implementation/m3/snapshot-plan-c/c2-intent-preimage-r1-subject.json` is 7766 bytes, SHA-256 `2d56b94c75287bf1a47f15240d6e4e43790f10245ace45a7f5a2d40fea48fa16`, with one trailing newline. Its 23 members are unique, sorted, and byte-identical to the archive. The archive contains those 23 files and no others.

## Bases

Product HEAD and the candidate worktree are `0eb17be7afb7adca554ecd589abe4410e32e5480`. The product tree is clean. The worktree differs only in `crates/identity/src/digests.rs`, `crates/identity/src/canonical_tests.rs`, and `crates/identity/src/lib.rs`. The live `git diff` of those three paths is byte-identical to the staged `product.diff` (5486 bytes, SHA-256 `5dd0eefb30f56c03953a4cbc3600f5dc32fc0d1dd13e9f2fee4b2f7533dfe719`).

The subject architecture base is `fe1fe12fff54f42c3a2f2c2e6548268124a4706b`. Live architecture HEAD is `7bd8b7daf6b0ca357602022b3a2183e1074a0119`, whose sole parent is that base. The one intervening commit records the already accepted architecture-only Plan-equivalent support. Its subject is 7452 bytes, SHA-256 `e7fb2359475cfbb7733eeb31e99398c9edbcc7c4027f8f3a403e2663539a240a`, and all 24 accepted members match that manifest. The archived `review.json` is the accepted review (813 bytes, SHA-256 `8ab624a35af2e52e9d2fc5b965e3bccab0e0af80c0e78189f15a8e46d3c6489d`). Product HEAD, `design-lock.json`, and the three authority bytes are unchanged across that commit. The only untracked architecture path remains `docs/implementation/m3/syntax-e/e2s/`, outside this unit.

Authority bytes match the subject pins at the architecture base, at live HEAD, and on disk:

- `docs/coop/artifacts/c2-plan-stage-schema.v3.json`, 112128 bytes, SHA-256 `3c488ff66a1ec9ab746e99e0701d59460aff3e1d66cd072d9d564a1382b9d285`
- `docs/coop/artifacts/check-c2.py`, 77952 bytes, SHA-256 `4f31d57cd1cd252d47eeb520aa31b5fe8c4fd3b0f067a6840b008b1fe176f3`
- `docs/implementation/m3/snapshot-plan-c/PROPOSAL-r8.md`, 183744 bytes, SHA-256 `578c186ec9fc239f42d88713b8c31ec7085ab507251691f6cbba01e49b6607e1`

`design-lock.json` is 619916 bytes, SHA-256 `2c1d9096fd6fd525c20b975d51436194133693599ff8d13ef0218c456392e05e`, equal to the product base. It records 141 inventory successors and 157 contract successors. The selected inventory candidate remains `docs/implementation/m2/repository-file-inventory.v181.json`, 651614 bytes, SHA-256 `5b89dd41b65e23f2407d28d8fefb2929bac06c9b881602e0f08426937e1276dd`.

## Three product files

Before pins match the blobs at `0eb17be7afb7adca554ecd589abe4410e32e5480`. Candidate bytes match the worktree.

| Path | Before | Candidate |
| --- | --- | --- |
| `crates/identity/src/digests.rs` | 3830 bytes, `a19ede27c26e9ba977c8827a7e6fb975c8db1dcf386f62a41daa4218c830b0ef` | 5643 bytes, `8de86abcdf1f2ffd1e5880efc26f18e3d45306e11d55889ab44af6354d786422` |
| `crates/identity/src/canonical_tests.rs` | 15088 bytes, `86ada1b44633c074ea72114a750ccf99dccd57d2d210a690896f8ae5106246ed` | 17378 bytes, `837d51493698ecc4e87472e78150818057a36ad465350ed4e829b42c5812daa7` |
| `crates/identity/src/lib.rs` | 3357 bytes, `2e00f0ed23c5ba4af52cdd9051d7a30e2adddf191208b3540e9f454c6f76f01a` | 3379 bytes, `5979defdcd22dac2ea6097fe5758f00b165410e5408397b2ad62ec9bdb2a980a` |

`lib.rs` adds `plan_intent_preimage` to the existing digests export. `crates/identity/src/canonical.rs` (11878 bytes, SHA-256 `e524652830590943dfb33c917b95ae0e87255588df66fcad114ffccad9c3fcb1`), `crates/identity/Cargo.toml`, and `Cargo.lock` match the product base. `unicode-normalization` 0.1.24 is the dependency already locked there.

## Preimage

`plan_intent_preimage` takes the supplied bytes and parses them with the existing product JSON parser. That parser keeps the current bounds: 4 MiB, depth 32, exact integers from `-(2^63)` through `2^64-1`, lexical duplicate rejection, and refusal of floats, negative zero, and ill-formed Unicode. The helper then NFC-normalizes every string and object key, returns `DuplicateKey` when two keys become equal, and leaves array order and multiplicity unchanged. `canonical::encode` emits the body: objects in ascending Unicode scalar order, compact separators, lowercase shortest required escapes, an unescaped solidus, and raw UTF-8. The preimage is the UTF-8 domain tag `opensip.plan-intent.v1`, one NUL, and that body. The caller hashes it with the existing raw SHA-256 helper.

The C2 authority spells the same preimage. `canonicalCommitment` requires domain tag `opensip.plan-intent.v1`, digest SHA-256, and encoding `opensip-canonical-json-v1`. `canonical_plan_intent` NFC-normalizes, refuses keys that collide after NFC, and serializes with `ensure_ascii` false, sorted keys, separators comma and colon, and `allow_nan` false. The existing `frame` function still builds the product H preimage (`opensip.product.v1`, domain, NUL, big-endian length, canonical body). The new helper leaves `frame` in place and does not call it.

The in-crate golden `{"z":["e\\u0301",3,1,3],"e\\u0301":{"s":"\\/\\n"},"a":null}` recomputes to the 67-byte preimage whose body is `{"a":null,"z":["é",3,1,3],"é":{"s":"/\\n"}}`. That is the literal the passing test asserts. The same test keeps the combining sequence in the ordinary canonical encoding of the parsed value, so the existing product canonical profile still preserves raw Unicode. Collision inputs `{"a":1,"a":2}`, `{"é":1,"e\\u0301":2}`, and the nested pair return `DuplicateKey`. `[3,1,3]` stays `[3,1,3]`. The scalar vector keeps `true`, `false`, `null`, and `-9223372036854775808`. Floats, `NaN`, a lone surrogate, negative zero, invalid UTF-8, the byte ceiling, and depth 33 stay refusals of the existing parser.

The function accepts only the raw bytes. It mints no lifecycle identifier and admits no PlanIntent schema. Closed schema admission remains the separate owner named by the encoding closure rule.

## Frozen intent and three vectors

The already frozen admitted harness intent is 4063 bytes, SHA-256 `99974a06700a316e865471fdb3ce746229236c2ba7b85ff9a97114eb711b41b7`. It is ASCII, has no lexical duplicate keys, no floats, and ten integers, all inside the product integer range. Independent `plan_intent_commitment` over that value is `sha256:4b6211d5fcc6b58e803013e7a90cecba6a937ada6aa21e46daa325831e25d5ea` on a 2918-byte preimage. That equals the retained reference-product record.

The three retained vector files are 44, 38, and 34 bytes. Parsed values match the NFC, escape, supplementary-character, and scalar literals. Their preimages are 59, 58, and 55 bytes, with SHA-256:

- `c0b25ba453581d34647e92dfed761b003a97b4106d638e8d327183174890c5b5`
- `8e3409edc07683bafdb03d4ab0cda9ad59c4b1bdea76f16994c260b572b5ae82`
- `dfe98b3ebd8a394f0fe5edd60a08542dc3f94da8aa6a3e9ab42fdf8f38d0bb10`

Those digests equal `evidence/c2-intent-checks-r1/reference-product.json` (742 bytes, SHA-256 `cb061614ab75740a77e34504c64d1194af1127b9f55f1b88ffd04d38fe82c2d8`). The retained bridge source calls `plan_intent_preimage` and the existing raw SHA-256 hex helper. This review recomputed the reference side and compared it with that retained product record. Cargo, rustc, the bridge, and the stage runners were not executed again.

## Retained checks

`identity-tests.log` (6980 bytes, SHA-256 `0e1b0e095fbdfac35c33634986667b9b70e32664bfe9dd53afed9cd7a90c211b`) records 72 passed, 0 failed, including the four new `plan_intent_preimage` tests. Clippy `--all-targets` with warnings denied exited 0; the log has no warning line. Both rustfmt invocations exited 0 with empty logs. The identity library build exited 0. The retained operability source record has an empty finding list, `passed` true, and 113 rows. `tools/operability/exceptions.json` is unchanged at 83200 bytes, SHA-256 `b5cc19ba3b1f29c14c534deb5d20eb6ab69408c710e8cb35d4c85f94226f3cb0`, and its `rows` array has length 113. The retained lock-mint record has an empty `found` list and `passed` true. The check records report niceness 10, a private mode `0700` directory, lane ownership by that process, and an absent installation. No archive member contains private-key material.

## Scope that remains open

`closedPlanIntentAdmissionImplemented`, `fullC2a`, `actualNativeWorker`, `SMComplete`, `effectiveL`, and `productQualification` are false. `productFiles` is 3. `inventoryUnchanged` is 181. `contractSuccessorsUnchanged` is 157. `verify_design.py` was not run. Under the standing ML5 rule, this acceptance grants no dependent gate. A later product-code archive and architecture-support archive of this unit still follow exact acceptance, root assent, and the current design check. This review changes no lock, inventory, law, or status board.

Required findings: none.
