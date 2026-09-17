# Advisory: private atom kernel (50)

**Reviewer:** Grok. Root remains lead. Not Claude agreement.  
**Kind:** Bounded review of two pinned private files. **Not public API. Not global atom admission. Not target-sidecar or incoming-search validation. Not native scanning. Not replay, custody, SOURCE48/runtime24 re-acceptance, or M2.**  
**Work tree:** `/tmp/opensip-implementation/m2-grok-atom-kernel-50-advisory/review`. Copied sources, trial product, frozen48, live repositories, and the pinned snapshot were not edited. Tests used a disposable overlay copy plus the native-case15 reference interpreter loading actual selected modules. Root native-completeness 4896 comparisons are outside this pin and were not re-run.

## Verdict

**PRIVATE-KERNEL-MATCHES-SELECTED-ATOM; NO-REQUIRED-FINDINGS.**

Pinned `atoms.rs` plus `atom-registry.json` match selected `atom_model.v1.py` (**97581** / `4477285c…`) on the imported runtime/test/history scanner and inventory/result helpers, and match selected `native_evidence_model.v2.py` `sufficiency_v2` (**319944** / `e6784aa1…`) on coverage normalization, conservative first-wins fold, dependency recursion, and deficiency precedence. Registry source projections match the selected foundation registry, native ladders, and N helper tables. A disposable overlay plus the reference interpreter loading those actual modules reproduced **1197 / 1464 / 3638 / 540 / 3199** cases. Error comparison is the typed key only.

Global atom admission, target-sidecar joins, incoming-search validation, native scanning, public API, and replay are not implemented and are not claimed. No caller-provided truth or flags enter this kernel; reconstructed retained inputs remain required. Local `tick` work is a private `Limit`, not Plan aggregate CPU qualification.

## Pins

| File | Bytes | sha256 |
| --- | ---: | --- |
| `atoms.rs` | 43651 | `41eb30d20fac25f3f3b668debee32b2576f1fe77949f3c25473048a29ee2d9d9` |
| `atom-registry.json` | 30466 | `8f37ed0096df5ae1d1077bb3be467d01917b933d1810e5faf70b354a3048dd13` |

Both pins match `source-pins.json` byte-for-byte. The crate-private module has no public export. Trial `native-sufficiency-check` `atoms.rs` is this pin plus its probe. The live trial `product/crates/evaluator/src/atoms.rs` (**59418**) starts with this pin and then adds out-of-scope native-scanning draft; that draft is **not** this unit.

## Selected references

| File | Bytes | sha256 |
| --- | ---: | --- |
| `atom_model.v1.py` | 97581 | `4477285c547d6697e8faefea15ed0d05e0f6f0b144e0e5e8706b532451089ade` |
| `native_evidence_model.v2.py` (N) | 319944 | `e6784aa1a595222cfd5a3da55e2beaa3d0839c878d67d6821297682089bde2b9` |
| `evaluator-projection-registry.v1.json` | 60005 | `65f163cc194d50fdbe430bd76eb68d25634ef2b6258e9f34269ecb1e49125abb` |
| `identity-schemas.v3.json` | 197480 | `311c1feb09ff8cd0b207233d2ec0d7440bb1c72fc0470de277ee1891c24bb68f` |
| live `policy-document.v2.schema.json` | 27863 | `c8b0a907a7b8019be4c6ed5b1d217ac7689bbbba2873679c42b86499280a3595` |

`atom-registry.json` `source` and `scannerNativeModel` / `scannerIdentitySchema` pins equal the reconstruction-48 copies. `fieldFilterSchema` equals the live selected policy-document, not the nested reconstruction-48 workflows copy (**26534** / `b221b5ed…`). `FieldFilterSuccessorV1` is exact after removing only `x-opensip-order` annotations. Relation ladders equal both the projection registry and native `relation-payload-schemas.v2.json` `x-opensip-relation-registry`. `scanner.dependsOn`, `sufficiencyPrecedence`, and `rungCause` equal N `DEPENDS_ON` / `PRECEDENCE_V2` / `RUNG_CAUSE`. `comparatorTable`, `engineFamilies`, `resolvedRungs`, `AtomCauseCodeV1`, and `NativeCause` enums match.

## Semantics vs selected atom model and N helper

- **Unknown vs false.** Kleene filter `and`: null projected field is `unknown`, not `nomatch`. `exists` with a known match is `true` even when causes such as `wrapper-partial` or `observation-window-insufficient` remain. `exists` with no known match is `false` only when covering is complete, uncertain addresses are empty, and no incompleteness cause is present; otherwise `indeterminate`. `none` / `count-at-most` with a dominating known match is `false` even if incomplete. Uncertain addresses are retained when a known value dominates.
- **Source identity dedup.** Inventory lookup keeps distinct payloads of one native id (JSON value equality) and does not collapse them to a single identity key. Package path is part of occupancy when supplied. Symbol path+qualifiedName lookup first-wins per `nativeSubjectId`. Two different symbol ids sharing path+qn yield occupancy `unknown`, not `nomatch` (corpus occupancy-unknown case: `sym:a` / `sym:b` on `src/a.ts` `f`).
- **First-wins Coverage fold.** `conservative_entry` uses the first carrier; later rows overwrite only when strictly worse (`complete < partial < unknown`, RC `complete`/`not-applicable` < `partial` < `incomplete` < `not-attempted`, lower confidence, `closed < open < unknown` for `exportsClosed`). Ties keep the first object. Deficiency/nativeCause take the first non-empty deficiency. `derivationKinds` is first-order union. All **450** fold cases already supply ascending Coverage ids. The kernel does not sort; native scanning that would run `_unique_pairs` is not this unit.
- **Dependency and deficiency precedence.** `sufficiency_v2` walks every step with no existential one-rung shortcut (confidence floor still runs). Missing/unindexed relation is `required-relation-missing`. `DEPENDS_ON` is `reachability→calls@resolved-callee` and `clones→declares@syntactic`, depth `< 4`, inheriting quantifier and edge/consumer policies. Closed-world `target_exported` / unresolved `target_affected` apply only on `universal-negative`. Deficiency is the `PRECEDENCE_V2` minimum; an unregistered cause is `Law`, never a new rank. Empty/null coverage deficiency falls back through `rungCause`.
- **Imported scanner.** Owed wrappers are selected ids whose kind matches and whose reconstructed import scope contains the logical path (no path ⇒ still owed). Missing wrapper `ATOM_IMPORT_WRAPPER_MISSING`; extra adapter keys `ATOM_IMPORT_FLAG_ADAPTER`; missing flags typed unstated keys. Runtime row occupancy then observability then filters; more than one matched row `ATOM_RUNTIME_ROW_AMBIGUOUS`. History collection-scope miss is `history-outside-collection-scope` and incomplete, not a silent false. Test process result is error ≻ failed ≻ passed. Local `tick` is private `Limit`.
- **Result helpers.** Cause uniqueness is `json.dumps(sort_keys=True, separators=(',',':'))` order (ASCII-escaped JSON, not general C canonical). Observation addresses unique by `(importId, selector, ordinal)` with null ordinal first. `imported-atom` result keeps native fact/coverage/scope/deficiency arrays empty.

## Independent overlay

Disposable copy: `/tmp/opensip-implementation/m2-grok-atom-kernel-50-advisory/review/copy` (native-sufficiency trial product without `target/`, pinned sources overlaid, five probes appended). `CARGO_TARGET_DIR` under this review tree. rustc/cargo **1.95.0**, `--offline --locked -p opensip-evaluator --lib -- atoms::`.

Selected-module comparison uses `/tmp/opensip-implementation/native-case15-reference-env/bin/python -I -B -X int_max_str_digits=0` (CPython **3.12.13**, UCD **15.0.0**, jsonschema **4.25.1**). `selected-module-replay.py` imports reconstruction-48 `atom_model.v1.py` and its loaded N `sufficiency_v2`; jsonschema is not stubbed and helpers are not inlined. Result `selected-module-replay.json` **998** / `47d8cf79…`.

The earlier host-3.14.6 `python-replay.py` is an **extra inlined/AST-isolated control only**. It is not the selected-module comparison.

| Check | Overlay rust | Selected modules (3.12.13) | Extra inlined control |
| --- | ---: | ---: | ---: |
| helpers (scope/string/int/completeness/process/filters) | **1197** | **1197** | 1197 |
| inventory (lookup/occupancy) | **1464** | **1464** | 1464 |
| results (causes/addresses/imported_result) | **3638** | **3638** | 3638 |
| imported scanner (typed error key only) | **540** | **540** | 540 |
| native sufficiency (entry/fold/sufficiency_v2) | **3199** | **3199** | 3199 |

Rust: 5 passed / 0 failed / 18 filtered, 1.70s.

Imported values in the 540: **180** true / **99** false / **201** indeterminate; refused keys `ATOM_IMPORT_WRAPPER_MISSING` 24, `ATOM_IMPORT_CONSUMABLE_UNSTATED` 24, `ATOM_RUNTIME_ROW_AMBIGUOUS` 6, `ATOM_FILTER_FIELD_FORBIDDEN` 6. **29** `exists` cases stay indeterminate when covering is incomplete and no known match exists; known matches still dominate to true while retaining causes.

## requiredFindings

None.

## Limits

Private kernel only. Not global `admit_atom_inputs`, target-sidecar, incoming-search, native scanning, public API, or replay. No caller truth/flags callback. Fixed reconstructed retained inputs remain required (`importScopes` and `importFlagsAdapter` are present on every imported case; the selected `importScopeAdapter` fallback is unused here). Local `tick`/`glob` `Limit` is not Plan `BudgetExceeded`. `conservative_entry` requires callers to supply ascending Coverage ids. Trailing-slash workspace roots would diverge from `N._under_unit` `rstrip("/")`; **0** helper cases use them. Nested reconstruction-48 `policy-document.v2.schema.json` is not the registry field-filter pin. Root native-completeness **4896** comparisons are outside this pin. SOURCE48 and runtime24 were not re-reviewed. Not custody or M2.
