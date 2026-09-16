# Independent Grok advisory: typescript-universe-11

**Reviewer:** Grok (explicitly authorized). Root remains lead. Not Claude agreement.
**Kind:** Frozen-trial advisory. **Not runtime selection. Not ACCEPT-DESIGN-UNIT. Not inventory-12. Not runtime-02. Not M2 complete. Not Plan/full closure/member-blob/compiler/replay.**
**Work tree:** `/tmp/opensip-implementation/m2-grok-typescript-universe-review-11/review`. Live product, frozen history, and commits were not edited.

**Prior:** syntax-universe-10 `70dc7cba…af16`. Universe-binding-boundary-01 `d114bb0e…1626`. Selected native `e678` / identity `619d`. Archived 09 advisory required none. Live lock is **10/15**; this frozen copy still carries **9/15** like 09/10 and does not install.

## Standing

Private TypeScript universe binder on frozen10's `inspect_syntax_universe` in the same evaluator owner. `inspect_typescript_universe` takes a named universe H-frame, an explicit snapshot id, and retained inputs. It rehashes/shape-admits the universe, resolves `nativeContextId` (`sha256-text`) to a TypeScript context H-frame, reruns `inspect_native_context`, rehashes the caller-named snapshot object, and binds only nested canonical records selected by the immutable registry row (`configGraph` from the universe, `nodeModulesLayout` from the context). No caller ADMIT. No decoded map as proof. Snapshot/member retention beyond this local diagnostic is out of scope.

## Custody

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `subject.json` | 47150 | `4bb8e1faef2dcab19461c8e2cbe9d31b42e8d6718b0c68d83c58f64d0b100304` |
| `subject.tar.gz` | 2119671 | `9cbfb143229203daaf321d9b799a0794591dd0c80b64116e0c0cb9e98464595e` |
| Files | 263 | 0 missing / 0 mismatch |
| `native_universe.rs` | 17803 | `df76bf556bd4519e3da9ad5aa443484743d5d1dcd7ce07314fceb8dfea411acb` |
| `native-context-registry.json` | 9783 | `8601618ad47b9a2d37af916b4db42aa1e108ea78c4071898c9bfbeef72d38611` |
| `native_context.rs` / `unicode_case.rs` / identity `closure.rs` / `Cargo.lock` | — | **byte-identical to 09** |

Export `/tmp/opensip-implementation/m2-typescript-universe-subject-11` matches. Copied excluding targets.

## TypeScript binder

Delta vs 10 (`native_universe.rs` 4606 `4f5c8d48…`): 10 exported only `inspect_syntax_universe`. 11 adds `inspect_typescript_universe` and re-exports it from `lib.rs` (771 `33427d56…`). Syntax arm still Unsupported for non-syntax domains; a TypeScript universe digest passed to the syntax owner is `Unsupported` (host test + independent probe).

Registry row coupling (current identity-v3 `311c1feb…`, same as 09):

- `contextField: ["nativeContextId"]`, `contextForm: sha256-text`, `entryPoint: bind_typescript_universe`
- universe `nestedRecords`: path `["tsconfigGraphHash"]`, `retainedAs: configGraph`, `form: canonical-record`, selector `#/$defs/TypeScriptConfigGraphV1`
- context `nestedRecords`: path `["nodeModulesLayoutDigest"]`, `retainedAs: nodeModulesLayout`, `form: canonical-record`

Only those selected keys are eligible. Missing selected record → `native.universe-retained-input-missing:…`. Corrupt blob → `Frame(Input(BlobDigest))` (invalid), not missing. Unrelated extra blobs do not change refusals/digest. Graph digest is **raw SHA-256 of canonical JSON** (`{"entryConfigPath"…`); universe/context frames are **H-preimages** (`opensip.product.v1\0…`). Snapshot id is caller-named; object identity/shape rehashed each call; empty inventory is a diagnostic refusal, not Plan selection.

Kind table `configNodeKindLaw` in the embedded registry is **object-equal** to current product `native-v2.schema.json` `e5834d37…` `#/x-opensip-config-node-kind-law`: exact case-sensitive basenames `tsconfig.json`/`jsconfig.json`, otherwise `other`. Iterative DFS preserves `extendsResolved` **sequence** (repeats legal), cycle cause `native.config-graph-cycle:{path}`, unreachable `native.config-graph-node-unreachable-from-entry:{path}`. `configOrigin` from the **entry** node only (`jsconfig`/`tsconfig`/`synthesized`).

## Initial fixture/compile account (preserved)

`check.stderr`: first compile used `TraversalBudget { max_nodes, max_depth }`; real fields are `steps`/`depth`. Corrected before harness build. NestedRecords `path` (not a different field name) corrected before first comparison.

`synth-fixture.stderr` / `expanded-oracle.stderr`: synthesized positive fixture used tsconfig honored defaults and **string** `synthesizerVersion: "1.0.0"` instead of exact `SynthesizedCompilerOptionsV1` keys and const integer `1`. Assertion failed **before** expanded corpus. Logs retained. `oracle.stdout` 153-case result is historical; final is 394 (`corrected-oracle.stdout` / `typescript-universe-result.json`). No product semantic patch hidden as a pass.

Manifest inventories sort by explicit string `path`.

## Independent reproduction

Trusted rustc/cargo **1.95.0**, `--offline`. Did not rerun 07/09 giant corpora; identity/context/case sources unchanged.

| Check | Result |
| --- | --- |
| 263-file pin + archive | match |
| `cargo test --workspace --all-targets` | **95** |
| evaluator compile-fail doctest | **1** → **96** |
| Clippy `--workspace --all-targets -D warnings` | 0 |
| harness replay | **394** lines, 323 checked, 296 native-refused, 68 invalid, 3 unavailable, **0 mismatch**, 240 graph topologies, identical to prior actual |
| kind law vs e583 | object-equal |
| independent negatives | **ALL_PASS** |

## Independent negatives

- TypeScript universe → syntax owner `Unsupported`
- Golden empty refusals with one packet of selected blobs
- Unrelated extra blob is not a semantic argument
- Missing `configGraph` → typed missing; corrupt graph bytes → `BlobDigest` invalid
- `work=0` Limit; missing named snapshot `MissingObject`
- Config graph digest is raw SHA; universe frame is H-preimage

## Findings

**Required:** none relative to the trial’s stated private-candidate standing.

**Should-fix:** none new for this freeze.

**Not findings**

- `native_universe.rs` is **not** in accepted inventory-12; an additive inventory successor is required before install. This is not runtime-02.
- Context diagnostics without member blobs / Plan / compiler execution / replay are the stated subset.
- Root continues the Rust binder separately.
- Historical 153-case oracle and failed synthesized fixture are retained evidence, not hidden product bugs.

## Limits

- Advisory only. Not acceptance of 11, 10, runtime-02, native ADMIT, M2, or release.
- Did not execute `close_run`, universe Plan joins, body identity, compiler execution, or complete replay.
- Snapshot/member-record retention beyond local diagnostic remains out of scope.
- Did not rerun 07 CVE1 / 09 case15 corpora.
- Additive inventory for `native_universe.rs` is still required; root remains lead.

## Conclusion

11 adds a TypeScript universe binder beside the 10 syntax binder: named context rerun, selected nested canonical records (raw SHA vs H-frames), explicit snapshot rehash, exact basename kind law from current e583, iterative DFS cycle/unreachable causes. 394 vectors and 96 tests/Clippy reproduce. Inventory-12 does not yet list this file.

**Verdict: NOT ACCEPTANCE.** Prototype matches its standing.
