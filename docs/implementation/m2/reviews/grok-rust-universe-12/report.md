# Frozen trial review: rust-universe-12

**Reviewer:** Grok. Root remains lead. Not Claude agreement.
**Kind:** Private Rust universe diagnostic on frozen11. **Not runtime selection. Not Plan/full Run/replay/compiler qualification. Not inventory v13 live install.**
**Work tree:** `/tmp/opensip-implementation/m2-grok-rust-universe-review-12/review`. Live, frozen, and history not edited. No commits.

## Subject pin

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/implementation/m2/trials/rust-universe-12/subject.json` | 44640 | `6358b3d6b740bdfe0aecf7917d1bb1849e1b2895ddb2ac55711ca48949cb6726` |
| adjacent `subject.tar.gz` / `archive-pin.json` | 1990913 | `994b132df435a0c9692d613751f156cbd27e6a05b2b6df50b9d49cdd4fac3e76` |
| adjacent `rust-universe-result.json` | 277 | `4d2b3f0aeca9190302d93e22018a29d3245868e6bdf5d2d4ab91038580e945dd` |
| export | `/tmp/opensip-implementation/m2-rust-universe-subject-12` | 247/247 member pins match; tar 247/247 match; 0 extra; 0 missing |

247 subject `files[].path` values are Python/string lexicographic sorted (unique). Integrity pins exact.

Dependency pins hash-match:

| Pin | Bytes | SHA-256 |
| --- | ---: | --- |
| frozen11 `typescript-universe-11/subject.json` | 47150 | `4bb8e1faef2dcab19461c8e2cbe9d31b42e8d6718b0c68d83c58f64d0b100304` |
| selected native `native_evidence_model.py` | 319944 | `e6784aa1a595222cfd5a3da55e2beaa3d0839c878d67d6821297682089bde2b9` |
| selected identity `identity_model.py` | 158555 | `619d6e3cf49d0cd58967688e35c1598c92eaeb32b95fd30bb67f634271c141e6` |

Identity-v3 `311c1feb…b68f` / 197480, native-v2 `e5834d37…7773` / 280357, identity crate, and `tools/identity/dependency-policy.json` are byte-identical to frozen11.

## Delta on 11 (product)

Unchanged vs typescript-universe-11: `native_context.rs`, plan/capability/unicode owners, identity sources, identity-v3, native-v2, identity dependency policy.

Frozen11 `native_universe.rs` (17803 bytes) is a byte substring of frozen12 (30120). Syntax and TypeScript binders are unchanged; this trial appends `inspect_rust_universe`.

**Product code added/changed:**

| Path | Role | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| `product/crates/evaluator/src/native_universe.rs` | Rust binder | 30120 | `67c514adac8efca808d3976b0a4b1a099b5912b3e76495ed739e0380171c7a6e` |
| `product/crates/evaluator/src/lib.rs` | export | 820 | `597e64e21262d65ac367159265f4de599be6af03aabdc76861cc69704d90842f` |
| `product/crates/host/src/native_owner_tests.rs` | boundary test | 16118 | `647e234d79f8accac36561015236fea6d7606ed93682f58db2a04792668b99dd` |
| `product/crates/host/tests/fixtures/native-context-fixtures.json` | rustUniverse packet | 43160 | `bec747fe4ecfd01269f1ece4d0c56c4951d41e20ec61fddf634de9a103eadca6` |

Layout v13 (additive `native_universe.rs` path) is a separate review. Trial12 is not live/runtime02/v3.

## Law vs selected `bind_rust_universe` (e678)

`inspect_rust_universe(inputs, digest, snapshot_id, work)` — no admission argument, no Plan id, no grants:

1. **Row dispatch.** `frame_candidate(SemanticUniverse)` against current identity-v3; require `language==rust`, `contextForm==sha256-text`, `binding.entryPoint==bind_rust_universe`. Other universe domains → `Unsupported("non-Rust universe")`.
2. **Named context rehash + owner rerun.** Walk `contextField`, frame Context, require `row.contextDomain`, then unconditional `inspect_native_context`. Carry context refusals (`missing-closure` remains `native.native-context-closure-unretained:toolClosure.closureId`). Context owner still uses closure descriptors; member blob retention is not claimed.
3. **Explicit snapshot each call.** `object(snapshot_id, Snapshot, work)` recomputes object identity/shape. Missing → `MissingObject` (unavailable). Changed descriptor under the same key → `ObjectIdentity` (invalid).
4. **Nested H-records.** `nestedIdentities` `retainedAs` + `form==sha256-text` + `domainSet==native-nested` locate frames. `frame_candidate(Nested)` rehashes; expected domains `dependency-source-set.v1` / `unified-features.rust.v1` / `prepared-output-set.v3` / `source-unit-ownership.v1`. Missing selected blob → typed `native.universe-retained-input-missing:…`. Corrupt / wrong-domain / schema → Frame/`ContextDomain` (invalid). Unrelated store blobs are not extra selected prepared/ownership records. `configProjectionSha256` has **no** `retainedAs`; bind hashes the context **record** via `H(native.cargo-config-projection.v2, configProjection)`, not `projectionSha256` file bytes, and does not require a projection frame.
5. **Field agreements.** `dependencySourceSetId` / `unifiedFeaturesId` / `preparedOutputSetId`; rustflags vs context projection; `executionCapableResolution == (preparedResolution != none)`; prepared id null iff none; cfg sets **add** to `context.baseCfg`; dependency lockfile equality; features `targetTriple`/`resolverVersion`; prepared toolchain/dependency/cfgSetId/kind (`imported-descriptor`→`imported-inert`, else `host-prepared`).
6. **Ownership.** Optional `sourceUnitOwnershipId==null` can bind (vectors `universe-sourceUnitOwnershipId-None`, `no-ownership-valid`) and grants no body/clone authority. When present: each `unitId` is closed `H(native.compilation-unit.v1, UnitIdentityV1)` over `{schemaVersion:1, markerPath, targetKind, targetName}` — `#` in markerPath is legal (`golden-hash-marker`). Marker/owned paths inventoried; selected ids declared; deferring units need a universe edition crate.
7. **Snapshot joins.** Lockfile path+digest; crate roots inventoried; context `replacedSnapshotConfigs` inventoried.
8. **No Plan/grants/execution.** `preparedResolutionGrantOperations` unused. Nested prepared bytes are inspected as inert records. No `close_run`.

Does not take a caller ADMIT.

## Reproduction (independent, rustc 1.95.0, `--locked --offline`)

- `cargo test --locked --offline -p opensip-host rust_universe --lib`: **ok** (features recheck + file-digest vs record-H).
- Harness replay of frozen `rust-universe-requests.ndjson`: **194/194**, 0 mismatches vs expected. 54 `checked`, 46 native-refused, 3 unavailable (missing universe/context/snapshot), remainder invalid (corrupt/wrong-domain/shape). Independent replay bytes equal frozen actual `ba1e65a1…a5f8`. Three preparation modes (`None`, `imported-descriptor`, `authorized-execution`) covered.
- Frozen `workspace.stdout` sums to **97** passing tests (0 failed); `clippy.stderr` finishes `-D warnings` with no diagnostics.
- Static bypass checklist: no admission parameter, reruns context owner, named snapshot, nested H + expected domains, record-H projection, optional ownership skip, cfg subset, no grant strings, no memo.

Did not replay Unicode 15 million-scalar corpus or the 394 TS / 47 syntax differentials. Did not re-exec the Python oracle (review unidata is 16.0.0). Comparison used frozen expected rows.

## requiredFindings

None.

## Limits (not required findings)

- Layout v13 is a separate unit; this trial is not live-installed.
- Local bind is not Plan selection, member-byte closure, compiler execution, or evaluator replay. Root’s next native frame retention is out of scope.
- Extra unselected prepared/ownership **dict keys** in the Python helper are not a native store concept; native ignores unrelated blobs, matching the trial README.

## Verdict

No required findings. Private diagnostic matches the selected Rust bind: named context owner rerun, explicit snapshot identity/shape, nested H-records on immutable selectors/domains, typed missing vs invalid corrupt/wrong-domain, record-H config projection, optional ownership without body authority, closed unitId including `#` marker paths, snapshot joins, no caller ADMIT, no Plan/grants. Not a live/runtime02/v3 selection.
