# Frozen trial review: plan-native-14

**Reviewer:** Grok. Root remains lead. Not Claude agreement.
**Kind:** Scoped source review of private Plan-native diagnostics over an explicit census. **Not runtime selection. Not full Run/replay/release/product qualification. Inventory v14 layout is accepted; this code is not live-installed.**
**Work tree:** `/tmp/opensip-implementation/m2-grok-plan-native-review-14/review`. Live, frozen, and history not edited. No commits.

Prior native-retention-13 and plan-native-boundary-14 reviews are **advisories**, not acceptance and not a fresh-blind claim.

## Subject pin

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/implementation/m2/trials/plan-native-14/subject.json` | 49004 | `a08387ba1c17447f4e1d93b107b2abe57205868136a5f873e6519fa98f7457e5` |
| adjacent `subject.tar.gz` / `archive-pin.json` | 3005893 | `d0975c0965c4cfc0293dc2c6642418c255590cac14fc1ef6165f12f87ad7ff49` |
| adjacent `plan-native-result.json` | 331 | `bb0e31dd28a5eac2c8a07e0508016d745be92bf038ddb570e129d9e67d1159c1` |
| adjacent `final-replay-result.json` | 332 | `01a6386261e9cdd37f15fc3ff5af773f3ffa87d12a8531deaff1226b9716e966` |
| adjacent `oracle-scope-account.json` | 2240 | `090a493b53642b82affbd6f57e3c9e077b4b8522b0b1206160456765b761912c` |
| export | `/tmp/opensip-implementation/m2-plan-native-subject-14` | 274/274 member pins match; tar 274/274; 0 extra; 0 missing |

274 `files[].path` values are unique and both string-sorted and pathlib-component-sorted.

Dependency pins hash-match: retention-13 subject `72230f77…e2a6`; grok retention-13 advisory `ff100415…ad6b`; grok plan-native-boundary-14 advisory `f59acf0a…3038`; selected native e678 `e6784aa1…e2b9`; selected identity 619d `619d6e3c…41e6`; inventory-v14 unit `d38a7d01…0c1f`.

Live lock independently observed **12 inventory / 16 contract** (last inventory candidate v14; last contract native-runtime v3). Live tree has no `plan_native.rs` / `native_retention.rs` / `native_universe.rs`.

## Source delta vs retention-13

Identity `lib.rs` and identity `Cargo.toml` are byte-identical to 13. External dependency TCB unchanged (`dependencies`, `unsafeAccounting`, `unicodeVersion`, crate deps `sha2-const-stable=0.1.0` + `unicode-normalization=0.1.24` default-features=false). Identity source policy **110** files: only local `src/closure.rs` pin updated `47631/a6dc8b89…` → `48663/4ea092d6…`.

| Path | Role | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| `product/crates/evaluator/src/native_retention.rs` | extracted public retain + crate-private frame-only | 15908 | `48bf211eb3b4aff45bfd60a5cf3adcb6a459dd10f379f09ff6df7727b53f272d` |
| `product/crates/evaluator/src/plan_native.rs` | Plan-native census owner | 13170 | `786134549d6b7b8ae5f2942b87810a34544d06c6de4919987fda9a1ccd3cd276` |
| `product/crates/evaluator/src/native-plan-registry.json` | kebab closed vocabulary | 1784 | `36f4a4f51fbb023dcaf357dcbbf54eaff506c8992ef827df0e10b0126d89b21d` |
| `product/crates/evaluator/src/native_universe.rs` | binders remain; helpers `pub(crate)` | 30164 | `fb802b9d33117ab6fa8806b348cab4029b1d9c480e1e935d9f4c992868baaac8` |
| `product/crates/evaluator/src/lib.rs` | export `inspect_plan_native` / `inspect_native_retention` | 1039 | `ce6d34a4b9c17f369021c72327248a5b2f0eeac2588b33c211d04601a9e73a1b` |
| `product/crates/identity/src/closure.rs` | `identity_record_shape` | 48663 | `4ea092d611fcc29bf113266feb5f9fa91a9224c29177b4447819ff3e4f4b3fd1` |

`inspect_native_frame_inputs` is `pub(crate)` and is **not** re-exported. Public `inspect_native_retention` still follows universe `contextField` and runs the actual syntax/TS/Rust binders. Frozen public retention outputs are byte-identical extraction vs final: **304** rows, SHA-256 `591d2c50…5404`.

## Law vs selected I native-block (619d 1689–1749) + N owners (e678)

`inspect_plan_native(inputs, plan_id, observed_contexts, observed_universes, budget)` — no admission argument:

1. **Budget.** `steps==0` or `depth==0` or census length `> steps` → `Limit`. `steps` bounds census size and **each** retention walk independently (`TraversalBudget` is `Copy`); not a Run/CPU envelope. `descriptor_work` bounds each schema op.
2. **Plan/snapshot identity** via `object(Plan)` / `object(Snapshot)`.
3. **`identity_record_shape`** on `analysisSpecDigest` / `semanticGrantDigest`: rehash canonical record, admit identity-v3 `/$defs/{kind}`, collection order; returns inert `JsonValue`. No `Walker`, no payload reference traversal, no grant/execution.
4. **Crate-private retain** of the explicit census (`inspect_native_frame_inputs`): contexts as `Context` (mandatory `inspect_native_context`), universes as `SemanticUniverse` **without** context follow or binder — so Plan language/selection gates precede binding. Duplicates collapse; universe first-observed order is kept.
5. **`NATIVE_CONTEXT_SET_JOIN`** before per-universe gates.
6. **Vocabulary.** Foundation languageMode map (syntax-only → `syntax`, not null); N capability ids/modes; `NOT-SELECTED` cells `clones-cross-tsjs`×{rust-cargo, rust-cargo-prepared, syntax-only}; ownership tuple `(capabilityId, languageMode, workspaceRoot)` unique (`required` is not part of the name).
7. **Per selected universe, in order:** requested language; prepared mode (`rust-cargo-prepared` for rust `preparedResolution != none`); `UNIVERSE_CONTEXT_NOT_SELECTED` **before** loading the named context (also if `contextForm != sha256-text`); context domain; `contextAgreementFields`; **actual** `inspect_*_universe` (empty refusals, digest identity); then grant `preparedResolutionGrantOperations` (`read-import` for imported-inert). Host + vector `prepared-bind-before-grant` keeps bind-before-grant (`NATIVE_UNIVERSE_BINDING:…cfgSets.primary`).
8. **Pruned-tree** uses **selected** TS `nodeModulesLayout` install/real paths only. Nested `node_modules`, VCS, and Cargo `target` under a marker remain unread.

No caller ADMIT. `PlanNativeChecks` is `{context_count, universe_count}` only — not a Run token. Oracle AST stops before `UNIVERSE_FRAME_UNRETAINED`.

## Reproduction (independent, rustc 1.95.0, `--locked --offline`)

- `cargo test --locked --offline -p opensip-host plan_native --lib`: **ok** (five selection/preparation cases + census `steps:1` Limit).
- Harness replay of frozen `plan-native-requests.ndjson`: **383/383**, 0 mismatches vs expected. 209 checked, 62 refused, 56 unavailable, 56 invalid. Independent replay bytes equal frozen actual `340d3bdd…4fcb`.
- Frozen public retention 304-row pair is byte-identical (`591d2c50…5404`). Did not re-run 07–12 corpora.
- Frozen `workspace.stdout` sums to **99** passing tests; `clippy.stderr` `-D warnings` clean; identity policy stdout `sourceFilesVerified: 110`, `passed: true`.

Did not re-exec the Unicode-15 Python oracle. Comparison used frozen expected rows (AST of selected I native-block + N owners).

## requiredFindings

None.

## Limits (not required findings)

- Explicit census is not graph completeness, fact/scope universe retention, or `UNIVERSE_FRAME_UNRETAINED`.
- Not earlier full grant/project/capability-manifest joins, native execution, metadata security, `close_run`, or ReplayedRun.
- Private frame-only retain cannot be used as a universe admission token; public retain remains stronger.
- Inventory v14 names these files; live product still lacks them.
- Root writes native Plan next; other Grok advised retention separately.

## Verdict

No required findings. Private source matches the selected native block: crate-private frame-only universe retain, mandatory context owner, actual binders after selection, vocabulary/NOT-SELECTED/tuple uniqueness, prepared-mode and grant order, selected-TS pruned-tree, inert `identity_record_shape`, typed Limit, no caller ADMIT. Not a live/runtime/full-Run selection.
