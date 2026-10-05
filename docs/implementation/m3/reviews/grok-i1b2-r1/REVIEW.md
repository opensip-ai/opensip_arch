# I1-b2 r1 — ACCEPT-UNIT

Product unit for bound I1-L section 4a (`cycle-representative`), plus additive inventory v142. Acceptance is the reviewed product bytes and that inventory candidate only. There is no contract successor and no S-OP bind.

## Subject

Worktree `/Users/sb/code/opensip-ai/opensip-i1b2` is detached at product main `0cba73defd5080a2a73febdbd5ad03baab54033c`. The only dirty paths are the three subject files. `git diff --binary HEAD` is 3307724 bytes, sha256 `b5df9e42126019aa7f61ab92e0506c46981cf9df23ffe4a58b52c77c3df0bf1e`, matching `evidence/i1b2.diff`.

| Path | Bytes | SHA-256 |
|---|---:|---|
| `crates/evaluator/src/atoms.rs` | 171403 | `3bda59421913f0aa95611f7d4071370f79b50847f636c736b5b6490594893897` |
| `crates/evaluator/src/composition.rs` | 38517 | `6a26ce42a0719eaf120dfd9eb1c4481f929a1c3d581eafa912228469f872751e` |
| `crates/evaluator/tests/fixtures/cycle-representative.v1.json` | 3207736 | `070ffda1953da750a0b5a84bb3ab6f206e1efbbd3c5c67e25b167fb595736b89` |

Authority `docs/implementation/m3/preview-pack-i1/i1-l/atom-section-4a.md` is 20270 bytes, sha256 `f21e1ef7167a1ff6783c0fb4d23eb786fc70cec3a8ea2113ef32d16115b09ebf`. Items 2.1–2.9 and precisions P0–P7 were read. `UNITS.md` was not treated as law. The diff does not change policy syntax, schemas, the native owner, or the pack registry.

`composition.rs` changes one call: the scanner receives the rule as well as the subject, node, and predicate id.

## Law

The per-subject atom API still refuses this op. `admit_atom` admits only `exists`, `none`, `count-at-most`, and `all-covered`, so a direct `evaluate_atom` of `cycle-representative` returns `ATOM_OP`. The composition scanner evaluates the op only when the predicate is `p`, the node is the rule's whole `emitWhen`, relation is `imports`, rung is `resolved-target`, filters are empty, `endpoint`, `evidence`, and `n` are absent, and `subjectKind` is `file`. Any other shape returns `ATOM_CYCLE_RULE_LAW`. Existing op-law tests still pass.

The graph is built once per rule and cached by `ruleId`. Vertices are the selected file subjects `(universe, path)`; a non-file selection refuses `ATOM_KIND_INCOMPATIBLE`. Symbol placement reads every retained symbol inventory. Byte-identical `(nativeSubjectId, path)` observations count once, and one id at two paths does not place (P3). Facts whose `sourceUniverse` is outside V are ignored. Imports below `resolved-target` are not edges. A placed source outside V is not read further. An importer with no unique row is `population-unknown` on `sourceUniverse` and the target is still read (P1). External occupancy is not an edge. First-party file and symbol targets use the existing reconciliation, whose `nativeId` is the sidecar `evaluationNativeId` when that join applies. An unknown occupancy or a symbol with no unique row is `target-kind-unknown` on `targetUniverse`. A package target, and a placed first-party target outside V, are `population-unknown` on `targetUniverse`. An uncertain edge keeps every cause that applies. `imports` unresolved-edge facts are stored on the referrer's selected vertex; a referrer that maps to no selected vertex is in no witness (P4).

Components are iterative Kosaraju. A component counts when it has two or more vertices, or one vertex and a self-edge. The representative is the minimum by path bytes, then universe bytes. A member that is the representative is true. Another member of that component is false. A file in no cyclic component is false only when graph completeness is complete and no non-disclosure blocking cause remains, which is the uncertain-edge condition once cross-family disclosures are set aside. Otherwise the value is indeterminate. An indeterminate value with no blocking cause returns `Error::Law`. Composition maps that to a law fault, so the value is not emitted. Known cycles stay true or false when coverage is incomplete. File-population completeness is left to composition: the retained partial-file case keeps the graph atoms false and records `incomplete-inventory`.

Completeness runs once. No owed imports binding at all returns `missing-relation-coverage` and stops (shared prelude P2). Universes of V are then visited in UTF-8 order with no cross-universe return. A universe with no available owed binding records `selector-unbound` and continues (P2). The census uses symbol inventories of the owed imports bindings, joined by the plan's cell and program ordinals, and does not consult `required`. A partial or unavailable inventory, or no inventory, records `population-unknown` for that universe; rows of a non-complete inventory are still expected ids. A file inventory is not part of this census. Exact `imports` / `resolved-target` scopes are taken for the source universe whatever the target universe. Every such scope is cited. An unpaired scope records `scope-without-coverage`, and paired coverages are still evaluated. A universe with no such scope, or an expected id outside the scope subjects, records `uncovered-expected-source-subject`. Scope and coverage identifiers are emitted in ascending identifier order, which is section 4's selection order. Each paired coverage is passed to the existing `sufficiency_v2` owner through `run_sufficiency`. The requirement is `imports` at `resolved-target`, confidence floor 0, completeness `complete`, quantifier `universal-negative` because that rung is resolved, and both edge policies `forbid`. `imports` has no sufficiency dependency, so the extra `derivationPolicy: any` carried by the shared helper does not change this answer. Unsatisfied `DeficiencyV2` cause strings are the result's `nativeDeficiencies` (P7). Census `population-unknown` and `uncovered-expected-source-subject` carry a null `nativeCause` (P5).

`cross-family-edge-not-owed` is the shared prelude's non-blocking disclosure. Unavailable bindings whose registry family is not `tsjs` receive it with no universe. `tsjs` is the engine family of `native.semantic-universe.typescript.v2`, the domain of the bundled rule's `typescript` universe. The cause does not make completeness fail and does not flip a known cycle. The oracle case `extra-foreign-family-unavailable-is-disclosure` matches that treatment.

Witnesses are `native-atom`. The representative receives the facts of every edge inside its component. Another member receives the facts of edges leaving that member. Uncertain facts leaving a subject, and unresolved imports placed on it, are kept even when the value is known. Unplaced uncertain facts are copied only onto indeterminate subjects. Every subject carries the shared coverage ids, scope ids, native deficiencies, and causes. Fact lists are canonical sets. Composition maps `knownFactIds` to `matchingFactIds` and maps causes through the existing deficiency join. Findings stay on the existing `declarative-subject-v1` profile. The retained self-cycle proof fails with one finding whose subject path is `a.ts`. The member-path presentation in item 2.7 and P6 is specified for M4 rendering; this unit does not add a renderer.

The work counter is the existing step budget: one projection of facts and inventory rows, one SCC pass, and one completeness pass, cached per rule. Item 2.8's witness-array ceiling remains the existing predicate-witness schema (`matchingFactIds` maxItems 100000) and the existing preflight refusal `EVALUATION.OUTPUT_BOUND_EXCEEDED`. This unit does not truncate. A component larger than that ceiling was not executed.

The fixture holds 45 `cases` (41 accepted I1-L oracle cases plus the four precision cases) and 4 `retainedCases`. The 45 exercise the private graph and census against the fixture's expected values, witnesses, scopes, coverages, deficiencies, and causes. The four retained cases go through public `derive_evaluation`, sealed `replay_run`, and a second replay from owned evidence: self-cycle fail at `a.ts`, acyclic pass, partial file population indeterminate with false graph atoms and `incomplete-inventory`, and optional partial symbol census indeterminate with `population-unknown`. Schemas and source bytes are retained. This is synthetic evidence. The generator scripts were not run.

## Checks

Under the lane lock, at 2026-10-05T16:43:44Z, on this worktree, with `cargo --offline --locked`, nice -n 10, `CARGO_HOME=/Users/sb/.cargo`, and a private 0700 `TMPDIR`:

- `cargo test -p opensip-evaluator --lib`: 44 passed, 0 failed, 9.04s. That includes `cycle_graph_and_census_match_all_accepted_oracle_cases` and `cycle_retained_evaluation_and_replay_match_known_and_partial_results`.
- `cargo test -p opensip-evaluator --doc`: 3 compile-fail tests passed.
- `cargo clippy -p opensip-evaluator --all-targets -- -D warnings`: exit 0.
- `cargo fmt -p opensip-evaluator -- --check`: exit 0.

`~/Library/Application Support/OpenSIP` was absent before and after. The lead's earlier host sealed-replay log (`i1b2-suite.log`) records 1 passed and 186 filtered, 115.32s, from before the census-index stamp. That host suite was not re-run. The stamp adds `_cellOrdinal` and `_programOrdinal` on the internal imports-binding clone; the evaluator library tests that share `owed_source_bindings` passed after it.

## Inventory v142

Staged outside both repositories. Parent v141 in the architecture tree matches the pin (585083 bytes, sha256 `6f9cddbc0531ff3128e783d8446d05462281b227a116ec84456ba28af642e750`).

Candidate `docs/implementation/m2/repository-file-inventory.v142.json` is 585522 bytes, sha256 `2745e424f78185a4cda1da3dc573e753356a43a5985059d847dc5c5f44299acc`. Successor record is 307651 bytes, sha256 `fa6b5274a05c6551e18390b78662c9b515d5ecb78e7fab251deb1e65e7f283aa`. Subject manifest is 643 bytes, sha256 `a895e8609ba2c1e166836e3b8dcf962982445810b6aaebaefa65a79fd94756d1`. Its three members hash to the staged README, successor, and candidate.

The candidate has the parent's keys. `packages` and `pendingDecisions` are equal. `standing` is the v142 sentence for this unit, which the additive profile allows. `files` grows from 1015 to 1016, stays sorted and unique, and adds only `crates/evaluator/tests/fixtures/cycle-representative.v1.json` (role `fixture`, package `opensip-evaluator`, `generated` false). Every inherited row is equal by value, including `atoms.rs` and `composition.rs`, which the record lists as planned rows. The 103 description projections resolve to those paths in v141 and v142. Their before/after text matches the selected v141 inheritance exactly. The new file sorts at index 99, so 100 selectors move and 3 stay.

Inventory verdict: ACCEPT. No required findings.
