# O1-a whole product code unit r1

ACCEPT-UNIT. This accepts the proposed M3 O1-a code only. `productQualification` stays false, `inventoryAuthored` stays false, and `fullO1aCodeAccepted` is true. No inventory successor, lock bind, product qualification, or push is authorized by this review.

Subject `/tmp/opensip-implementation/reviews/grok-o1a-whole-unit-r1/subject.json` is 14846 bytes, SHA-256 `17f1dbe4842bc5177bb3ceade3101d4d9059baf6f2722ce9720ba878b563edc5`. It pins 80 sorted unique product files. Every pin matches `/tmp/opensip-implementation/o1a-whole-unit-candidate-r1/product`. Nine files differ from product `bf9561a4c280a141ba4cf14d7acf535e6dbb5bd0`; seventy-one are additions. None are under `crates/platform`, `crates/security`, `crates/storage`, `schemas`, `crates/contracts/src/generated`, or `apps/report/src/generated`. Architecture `262ebe04113e71d4026ef89e5f18997f0a50682a` is the accepted tooling-record HEAD. The product lock at that base is schemaVersion 4 with 137 contract successors and inventory tail v167.

## Delta

`Cargo.lock` adds one package, `opensip-operability` 0.1.0, depending only on `opensip-platform`, and adds that package to `opensip-host`. No other package name or version changes. The workspace member list gains `crates/operability`. The operability manifest depends only on `opensip-platform`, has no build script, and leaves `operability-dev-sinks` and `test-mints` off by default. The CLI does not depend on operability; its `operability-dev-sinks` feature forwards through the host and is not default. The host forwards that same feature and never enables it from the dependency table.

Host and CLI edits are the capability hold, the optional unavailable result, and the freeze backstops. `MetadataHost::begin` allocates the request identity and then calls `start`. Allocation failure returns before `start` and before `finalize`, and the CLI writes `HOST.IO_FAILURE` and exits 4. A failed `start` stores `LoggingUnavailable` and freezes nothing. A second `start` returns `None`. Metadata success, required-delivery failure, projection backstop, stdout failure, and the successful deliver path all call `finalize_invocation`. A second call finds the phase already frozen and returns. Doctor still observes through its existing macOS ingress, then freezes, then builds the response. An invalid correlation returns `MetadataError::Projection` before that freeze, and the CLI backstop freezes on the way out. Non-macOS doctor remains the existing rejected metadata path. The host holds `CapabilitySet` and calls no mint and no event emit.

`tools/README.md` records the operability checker as an enforcement aid and states that the check does not qualify a product.

## Law the code implements

Selected O1 r2 (`PROPOSAL-r2.md`, 80638 bytes, `987153221b913fc1c4cc729ecfabad397670502c8dc95a4bb292ebe0506bbbf0`), the S-OP-2 r6 recording, bound O1-D1 r2, and bound O1-PKG r1 are the authorities. Definition gaps are the bound O1-D1 profile.

The crate forbids unsafe code. Release builds with `operability-dev-sinks` or `test-mints` fail `compile_error` with the item 10 and item 7 sentences. `BuildProfile` is only `debug-assertions-on` / `debug-assertions-off` via `cfg!(debug_assertions)`. Platform is the four named targets. `IoErrorKind` is permission-denied, no-space, io-error, and other, captured with the same error's errno. The registry events are `log.stream.opened` (info, request identity, export false) and `log.loss.counted` (warn, sink plus the 8×5 loss map, optional sink error and errno together, export false). Sink members are file and stderr. Harness is not a member: read-back drops the literal `harness` as an unknown sink value. `ComponentRole` and `RustDetailCode` are not registered. K8 `LossCell` is the nonempty 40-cell map. The empty `code_table!` arm is reduction-only and cannot emit a K1 member. Credential matching uses the three families, the named whitespace scalars, the folds U+017F→s and U+212A→k, and the `***` replacement in the guard tests. Guard admission requires one final LF and no interior LF. Line, field, and depth bounds are the O1-D1 caps (4096, 32 fields, depth at most 2).

The catalog is the fifteen-member source list and `MEMBER_SHA256` `d1e2924bfce2dad6dc4adc1e541857b49f5822dc500f0e2ad97227b7211b88b7`, with the two O1-D1 source receipts. There is no mint-list file. `exceptions.json` has 113 source rows and 176 mint-audit rows. The refreshed census matches those counts, adds no rows, and states that the lexical census authorizes no call. Public test mint functions exist only under `cfg(test)` or `test-mints`. Production host code does not call them. `CapabilitySet` retains the owner mint methods for a later wiring unit and is not used to emit.

`start` draws one ephemeral key from platform entropy, wipes the temporary copy, and publishes one runtime. `finalize` takes one `Instant` deadline, 200 ms normal or 100 ms cancel, closes admission, waits without holding the slot lock, then derives and stores one frozen summary. It does not join a writer. Already settled work records the deadline and does not sleep. Post-freeze producer calls increment only the post-freeze gauges. Reservation of queue bytes and a record precedes encoding. Error and warn may use the full queue; other levels stop at the 256 KiB / 512-record headroom. The development FIFO test fills the debug budget, still reserves an error record, freezes on the cancel deadline, and only then releases the blocked reader. The frozen snapshot does not change when the late worker publishes. Writer I/O keeps one sticky captured error pair, stops further syscalls after that error, and exchanges the snapshot once. Marker completion is a compare-exchange from the attempted state; freeze records skipped or unconfirmed only when it wins that exchange. File capability stays off (`FILE_SINK_ADMITTED` is false). Ring loss is not a loss-matrix cell.

The accepted package checker, already on the product base, reports `passed: true`, `productQualification: false`, and an empty stderr. The only operability edges are `opensip-host` → `opensip-operability` and `opensip-operability` → `opensip-platform`. Storage and components do not declare the permitted edge in this unit. `verify-design` on this candidate passed and stayed unqualified.

## Controls

| Control | Evidence |
| --- | --- |
| Library tests | Default 82 passed in 6.79s. Development 85 passed in 7.85s, including the FIFO headroom test. |
| Fresh process | Two runtime tests passed on each build, including a fresh process key. |
| Refusal | 25 external cases and the structural probe function passed inside 3 tests (7.11s). The structural function is 10 non-field refusals plus 13 bound mutations (7 event bounds, 3 literal-token refusals, 3 member/empty-counter refusals). Four self-test files must fail. |
| Checker and census | 17 checker tests, source check `rows: 113`, `findings: []`, lock check `found: []`. Census 113 / 176, `inventoryAuthored: false`. Catalog 5 tests. |
| Clippy | `cargo clippy --locked --offline -p opensip-host -p opensip-cli --all-targets -- -D warnings` and the same command with `--features operability-dev-sinks` both exited 0. Neither passes `--no-deps`. Both logs show `Checking opensip-operability`. |
| Release | Both forbidden release features exit 101 with the exact `compile_error` text. Featureless `opensip` is 6357808 bytes, SHA-256 `0761f2d584833181dfb66937c739d7187ff997c5f1b67eb68e6265a9eb148f2b`. Release-absence found neither dev-sink nor harness-sink marker. Help exited 0. `cargo package --list` exited 0. |
| Metadata | 27 deterministic rows: help, version, and rejected, across accepted-main, featureless, and development, and across fixed, logging-env, and closed-stderr. Each case has one normalized envelope hash. Help and version exit 0. Rejected exits 2. Stderr is empty. Three no-reader output-failure rows exit 4 with 62 stderr bytes, the `OUTPUT.SERIALIZATION_FAILED` line. Only the fresh request id is normalized. |
| Termination | Eight fresh children, default and development, for metadata, rejected, delivery, and projection-backstop. The frozen carrier is unchanged after repeated normal and cancel finalize. |
| Start failure | The child with `RLIMIT_NOFILE` 64 allocates a request, fails logging start, holds no capability set, and has no frozen summary before or after finalize. Parent descriptors stay unchanged. |
| Host logging | One `logging_tests` test passed on each build. |

Doctor and request-allocation failure are source-order and shared-freezer facts. This review did not execute doctor, read a home installation, or read a private 413. The earlier closed-stderr init-failure hypothesis is not evidence. Strict timing is not qualified; the authored 200/100 deadlines and raw overshoot remain M3 observations, and M6 still owns timing qualification. No tolerance is added.

`final-controls.json` is preparatory. Its `fullO1aAccepted: false` is the pre-review standing, not this verdict.

## Still outside this acceptance

S-OP-6 summary rendering, S-OP-7 K6 writer and source census, S-OP-2-P then S-OP-2-R then S-OP-2b, O1-b harness and phase RequestId wiring, O1-c generated and termination events, O1-S, and the closed O1-p platform change stay deferred. After this code is what main contains, a new additive inventory, v168 unless another inventory binds first, needs its own review and a separate lock commit. Checkpoint reviews r1–r3 stay historical.
