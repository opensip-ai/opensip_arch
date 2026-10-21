# CODEX2 Review — CLI doctor guard repair r1

## Verdict

**REQUIRED-FINDINGS**

## Required findings

### DOCTOR-GUARD-R1-RF-1 — Bind the accepted feature graph by resolution, activation, and lawful use

`metadata_declared_features_are_closed` proves only that five package objects have the expected names, canonical manifest paths, and textual `features` maps. It never examines Cargo metadata's dependency declarations or resolve graph. Its own positive synthetic document omits both `dependencies` and `resolve` and is still accepted. Consequently, the guard would continue to pass if the `opensip-host` alias used by the CLI were retargeted to another package while the expected host package row remained elsewhere in metadata. It would also pass if an ordinary dependency declaration directly enabled `operability-dev-sinks` or `harness-instrumentation`, because that changes `dependencies[*].features` without changing the package's declared feature map.

Those are material gaps in the property this test claims. Accepted O1 r2 requires the CLI and host to forward the development sink only to the intended package and says it is reached only through an explicit `--features`; O1/S-OP-2b also prohibit enabling the harness sink from a `[dependencies]` table. X10 r4 permits the later features only while no bridge reaches the binary, doctor ingress, default build, or release build. A forwarding string such as `opensip-host/harness-instrumentation` does not establish either the target package identity or the activation path.

The production-source side has the corresponding lawful-use gap. `no_home_profile_or_release_selector_reaches_the_binary_or_the_ingress` rejects only the literal substring `cfg(feature`. A new `#[cfg(any(feature = "harness-instrumentation"))]`, `cfg_attr`, or token-separated `cfg ( feature = ... )` selector in an unpinned CLI, ingress, or request production region passes that check while reusing an allowed feature name for a purpose the accepted law did not grant. The exact `KNOWN_LOGGING_PREFIX` pins the current accepted feature-gated logging sites before the mid-file block in `outcomes.rs`, but it does not protect the other scanned production regions or later outcomes code.

A successor should use the locked offline metadata to bind every guarded forwarding alias through the selected resolve node to the intended canonical package (including the operability and platform targets), and reject direct ordinary-dependency activation of the guarded features. It should also constrain production feature gates to the exact accepted logging/release-guard uses, using an actual syntax-aware check or an equivalently complete token/exact-site fence. Add pure controls for a same-spelling alias retarget, direct dependency feature activation, and alternate `cfg` forms, plus compiled runtime mutations showing the new resolution/activation and lawful-use conditions are observed.

## Authority ruling

No further design selection is needed. X10 r4 establishes the no-doctor-bridge and no-selector boundary. Accepted O1 r2 and S-OP-2b establish the two opt-in logging/harness feature names, their intended forwarding path, their non-default status, and the prohibition on ordinary dependency activation. The required work is to make the test enforce those already selected meanings and identities.

## Frozen subject and evidence

The requested `subject.json` SHA-256 is exact: `7d81b8a0d12c925283afc2090a17930e8e6649865853875835a05e62f110fd15`. All 102 declared members are present and unique, every byte count and SHA-256 matches, and there are no undeclared frozen-subject members. The sole candidate path is byte-identical to the named worktree file; the worktree is at parent `82be07e21dedefb2bd928339ce22c88e97db21ff` with only that existing test path modified. Product main is at the same parent and architecture is at `0e29831a50d66eebdbc415692f391d16fbe7688c`. The frozen parent and all pinned product-authority files equal their corresponding Git bytes.

The source-projection repair is sound within its stated scope. `KNOWN_LOGGING_PREFIX` is the exact 15,825-byte prefix of the pinned `outcomes.rs`; `KNOWN_LOGGING_TESTS` is the exact unique 1,954-byte block immediately after it; and the three known tails exactly match the respective EOF test modules in `outcomes.rs`, `doctor_ingress.rs`, and `request.rs`. The outcomes-path, prefix, uniqueness, and exact-suffix conditions preserve production on both sides and leave changed, duplicate, nested, foreign-path, and post-tail forms visible. The three existing doctor command test bodies remain parent-exact.

Owning r3 records all six doctor tests and all-target CLI Clippy passing. All six mutations compiled, failed at their stated runtime witnesses, restored the exact candidate hash, and were followed by a fresh six-test positive. Those controls cover projection erasure, path and prefix weakening, blind tail truncation, widening the declared feature map, and hiding an unknown test shape. They do not exercise dependency alias resolution, direct dependency feature activation, or alternate feature-gate syntax, so they do not close DOCTOR-GUARD-R1-RF-1.

The preserved r1 stale-feature failure and r2 driver precondition failure are accurately distinguished from the complete r3 lane. The unrelated Rust3/source-count and platform FD3 repairs remain outside this subject. This verdict grants no integration, inventory/status reconciliation, release qualification, or product qualification.

## Non-blocking observations

None.
