# Frozen trial review: policy-admission-22

**Reviewer:** Grok. Root remains lead. Not Claude agreement.
**Kind:** Scoped source review of private retained policy/program admission (`inspect_policy_program`) plus neutral `current_record_shape`. **Not runtime selection. Not predicate-matching reference-v2 acceptance. Not glob-21 re-acceptance. Not full Run, stages, predicate addressing, import admission, or replay.**
**Work tree:** `/tmp/opensip-implementation/m2-grok-policy-admission-review-22/review`. Live, frozen, and history not edited. No commits.

## Subject pin

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/implementation/m2/trials/policy-admission-22/subject.json` | 52321 | `4ba8978dcbe6225a28356e1bcc8e8e8a3f4ff207ed0d30526cfd7a54ef606d89` |
| adjacent `subject.tar.gz` / `archive-pin.json` | 3402401 | `f3fb7241912ffceada456095b0e3ae500c365ecb0f0457adc6dc96ce24a864d7` |
| adjacent `policy-result.json` | 387 | `b5b79442b8bc68b57f40365ad1833eb943b8da5a1809ae32bdd185c8fce2f89a` |
| adjacent `oracle-scope-account.json` | 1882 | `c3234dd51217ab8e0271a587f3a9d64cbb76de7aa0781f4ccf3ef9bfa80a3e74` |
| export | `/tmp/opensip-implementation/m2-policy-admission-subject-22` | **293/293** members; tar 293; 0 extra; 0 missing |

293 `files[].path` values are unique and string-sorted.

Dependency pins hash-match: glob-21 subject `f478f097…9fd4`; archived glob-21 `report.json` `e76fbe39…01a0` / 6588; inventory-20 unit; runtime-v9 unit; selected I `619d6e3c…41e6`; W v3 `60f28dc9…6123`; atom_model `4477285c…9ade`; evaluator-projection-registry `65f163cc…5abb` / 60005; pending reference-v2 subject `83c90070…6033`.

Live lock independently **18 inventory / 22 contract** (`c4bc31ef…a73a` / 52530). Last inventory **candidate** is v20; last contract is runtime **v9**. Live tree has **no** evaluator `policy.rs` / `atom-registry.json`. Reference-v2 is **not** selected. Glob-21 and this source are **not** installed.

## Source delta vs frozen glob-21

**235** prior product files byte-identical, including `portable_glob_match` **function text**, glob unit tests, `run_links.rs`, prior runtime bodies, `Cargo.lock`, and identity methods other than the new helper. No new crate dependency. External TCB unchanged (sha2-const-stable 0.1.0 / tinyvec 1.13.3 / unicode-normalization 0.1.24).

Changed: `lib.rs` export; `policy.rs` admission; host tests/fixture; `closure.rs`; identity-policy pin. **New:** `atom-registry.json`.

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `product/crates/evaluator/src/policy.rs` | 16386 | `57637018141542b5303552a4250d5d37e8a3a0f686f47838b36c8280795d19b9` |
| `product/crates/identity/src/closure.rs` | 51535 | `65e30f540120e319a40ce0701715a02449f91a773571afed3210bcd5e8dac75f` |
| `product/crates/evaluator/src/atom-registry.json` | 21633 | `b1ae0b4a91db887edbbf2b69735f474b4889fcd7f999bf1dd21821689bdaeb68` |
| host fixture | 2185913 | `8e9673f1…ef5f` (< 4 MiB `MAX_BYTES`) |

Removing `current_record_shape` from `closure.rs` yields **byte-identical** glob-21 identity methods. Identity-policy JSON equals glob-21 except the local `src/closure.rs` pin **51535** / `65e30f54…c75f`.

## Law vs selected I 1757–1784 (619d) and actual W v3

`inspect_policy_program` takes retained inputs and **Run id** only. It rehashes Run → Plan → evaluation-seal → proof-bundle. Then `current_record_shape` admits policy (`PolicyDocumentV2`), waiver (`WaiverSetV1`, shape only), and compiled program (`RuleProgramV2`) using **already-bound** embedded RegisteredSchemas. It does **not** require an extra retained schema blob (`registered_record_shape` still does, unchanged). `foreign_payload` on workflows documents does not walk; no walk shim.

Then `RULE_PROGRAM_POLICY_JOIN` and exact compilation: canonical `{schemaVersion:2, policyDigest, rules:[{ruleId,ruleProgramRef,emitWhen}]}` digest vs `proof.ruleProgramDigest`. **Every** policy rule, including disabled, runs `rule_law` (evidenceUse uniqueness; 64 nodes / depth 8; atom relation/rung/endpoint/kind/evidence/field/comparator/enum; undeclared evidence `IMPORT.ABSENT_FOR_PREDICATE`). Program atoms use `walk_atoms` + `atom_law(..., kind=None)` — actual W v3 **first-kind fallback** retained (`export`→`symbol`). Internal atom helpers run only after full registered shapes. Private `rule_count` is not a closed Run.

Closed `atom-registry.json` is an exact extract of selected projection-registry **17 relations**, `comparatorTable`, and portable universes (typescript/rust/syntax v2), named by selected inventory v20. Policy `$defs/FieldFilter` equals registry `FieldFilterSuccessorV1` after removing only `x-opensip-order` annotations.

History preserved: initial compiler `ok_or` / Clippy collapsible-if; initial 5- and 927-row corpora; 930 adds actual NUL prefix and disabled valid/bad-rung/undeclared.

## Reproduction (independent, rustc 1.95.0, `--locked --offline`)

- Frozen actual vs expected: **930/930**, **369 checked**, **0 mismatch** (468 refused / 89 invalid / 3 unavailable / 1 Limit).
- Independent extract of 619d `get`/`blob`/`canonical_bytes`/`foreign_payload` plus 1757–1784, executed with actual W v3: **929/930** equal frozen expected. The only difference is labeled `zero-steps`: Python AST has no local work budget (`checked`); Rust returns `Limit`. That is the typed local budget, not an admission-law mismatch.
- Host 47 cases include disabled-still-admitted, disabled-bad-rung, depth 8/9, first-kind `calls-kind-export`, `file-kind-symbol` refuse, compilation/policy joins, opaque extra blob still checked, NUL/backslash glob refuse. `cargo test --locked --offline -p opensip-host policy_program --lib` ok (each case also `steps==0` → Limit). Glob unit test still ok.
- Identity policy independently passed: `sourceFilesVerified: 110`. Frozen workspace sums to **106**. Independent `cargo clippy --locked --offline --workspace --all-targets -- -D warnings` Finished.

Did not rebuild the harness and re-pipe 13 MiB `policy-requests.ndjson`. Did not re-exec Unicode-15 or 07–12 corpora.

Predicate-matching-reference-selection-v2 (`83c90070…6033`) is **not** accepted here. Original 04bf missed current 311c description; 01b8 named unaccepted source-v2 as parent and failed private activation; v2 uses accepted source-v3 parent with the **same** helper bytes (`1d5212d5…9874`). Future runtime-10 is after both this source and that reference are independently accepted.

## requiredFindings

None.

## Limits (not required findings)

- Local checked/rule counts are not ADMIT, predicate evaluation, `close_run`, or ReplayedRun.
- Waiver is registered shape only; stages / predicate addressing / imports remain later owners.
- Walk/native census remain earlier owners.
- `current_record_shape` is inert shape, not producer/owner/Plan selection.
- Proposed reference-v2 is unselected; this review does not accept it.
- Python AST replay has no `work` budget; rust `Limit` on `steps==0` is the local implementation bound.
- Live 18/22 runtime v9 does not install these bytes.
- Did not re-pipe 13 MiB requests through a rebuilt harness.

## Verdict

No required findings. Private `inspect_policy_program` matches selected I 1757–1784 with actual W v3/atom owner, keeps first-kind fallback, uses embedded schema without inventing a schema-blob requirement, and does not mint a Run. Glob-21 body is unchanged. Not a live/runtime/reference selection.
