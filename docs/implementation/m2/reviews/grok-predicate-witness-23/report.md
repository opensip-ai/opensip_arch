# Frozen trial review: predicate-witness-23

**Reviewer:** Grok. Root remains lead. Not Claude agreement.
**Kind:** Scoped source review of private `inspect_predicate_witnesses`. **Not runtime selection. Not v10 re-acceptance. Not policy compilation, atom evaluation/truth, full Run, or replay.**
**Work tree:** `/tmp/opensip-implementation/m2-grok-predicate-witness-review-23/review`. Live, frozen, and history not edited. No commits.

The candidate `design-lock.json` is the **historical 18/22** product lock inherited from frozen-22. Current live is **18/24 / runtime v10** after a separate formal review and private activation. That live install is **not** this source’s acceptance; live still has **no** `proofs.rs`.

## Subject pin

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/implementation/m2/trials/predicate-witness-23/subject.json` | 51407 | `62771186f2d4656d860a8ba1f15ff1788a87a21cf955cf2848418d3185abc486` |
| adjacent `subject.tar.gz` / `archive-pin.json` | 2527988 | `16e6e4ad5bcff36e49e2c05ef503b0795fec62774698dc3df42a118602815bde` |
| adjacent `predicates-result.json` | 318 | `4110ee86cba49b5e3963887ac2c186e1d0f94d9058ee378730a7247c25694538` |
| adjacent `host-case-account.json` | 1659 | `a6b0da419f30ed5925d2e4fff6f6410d07c2b7bc81035f9f31d384d982e9e769` |
| export | `/tmp/opensip-implementation/m2-predicate-witness-subject-23` | **287/287** members; tar 287; 0 extra; 0 missing |

287 `files[].path` values are unique and string-sorted.

Dependency pins hash-match: policy-admission-22 `4ba8978d…6d89`; runtime-v10 unit `2160836f…9346`; reference-v2 unit `5e3b1b9a…57b1`; selected I `7f840b9a…989e` / 158607; selected `workflows_model.v1.py` `1d5212d5…9874`.

Live lock independently **18 inventory / 24 contract** (`f8e47e7a…2c71` / 54390). Last inventory candidate remains v20; last contract is runtime **v10**. Live `policy.rs` matches this trial’s frozen-22 body; live `lib.rs` has **no** `proofs` module.

## Source delta vs frozen 22

**239** prior product files byte-identical, including identity `closure.rs`, identity-policy, `Cargo.lock`, `policy.rs`, `atom-registry.json`, and prior runtime bodies. External TCB unchanged.

Changed: `lib.rs` export; host tests; fixture. **New:** planned `proofs.rs`.

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `product/crates/evaluator/src/proofs.rs` | 10578 | `fd3711743f043dc968dd4669ce9cd42afc83d3c5c91917d9e1e1621fc83248a0` |
| host fixture | 3360663 | `b49c7f79bd13511bcd0ebf963157761d63bc020a01fae2eb072b2ae9b26cd979` (< 4 MiB) |

## Law vs selected reference-v2 I 1829–1852

`inspect_predicate_witnesses` takes retained inputs and **Run id** only. It derives evaluation-seal → proof-bundle, admits the compiled program with `current_record_shape` (`RuleProgramV2`), and walks cited **view** input refs. No caller proof sets.

Joins, in order: `HIDDEN_PREDICATE_INPUT`; `PREDICATE_SCOPE_ROOTS`; `WITNESS_FACT_ROOTS` / `WITNESS_COVERAGE_ROOTS`; `PROGRAM_PREDICATE_PROGRAM_JOIN`; `PROGRAM_PREDICATE_ADDRESS_JOIN`; `PROGRAM_PREDICATE_OPERATION_JOIN`; `PROGRAM_PREDICATE_RULE_UNKNOWN`; ASCII shortest-decimal `predicate_node_at` (`PREDICATE_ADDRESS`, **LEAF before RANGE**); `PROGRAM_PREDICATE_NODE_OPERATION`; node digest; `WITNESS_CHILD_ADDRESS_JOIN`; `WITNESS_CHILD_NOT_PROVEN` (same rule **and** subject); `WITNESS_COUNT_LIMIT_JOIN`.

Five actual retained helpers (`get`, `blob`, `canonical_bytes`, `payload`, `foreign_payload`) plus two address helpers (`predicate_node_at`, `predicate_child_addresses`). Local `payload` walk is an explicit **NOOP**; identity-record shape and full workflow program schema still run. Per-node `admit_program_predicate_node` is covered by whole-program `RuleProgramV2` (`emitWhen` → `#/$defs/Predicate`). Private `predicate_count` is not proof/truth/Run authority: empty proofs and claimed `false`/`indeterminate` can pass these joins.

Unicode decimal aliases (`٠`, `０`, `²`, …) refuse `PREDICATE_ADDRESS`. Oversized ordinal on a leaf is `PREDICATE_ADDRESS_LEAF`; the same ordinal on an `and`/`or` is `PREDICATE_ADDRESS_RANGE`.

History preserved: initial-five and first-136 corpora. First-136 used obsolete `fact3:`/`coverage3:` prefixes (shape `invalid`); final-136 uses `fact2:`/`coverage2:` and reaches `WITNESS_FACT_ROOTS` / `WITNESS_COVERAGE_ROOTS`. Named root refusals are the final expected causes.

## Reproduction (independent, rustc 1.95.0, `--locked --offline`)

- Frozen actual vs expected: **136/136**, **19 checked**, **0 mismatch** (84 refused / 17 invalid / 15 unavailable / 1 Limit).
- Independent extract of selected-v2 1829–1852 + 5 helpers + 2 address helpers, walk NOOP: **0 mismatch** vs frozen expected (rust `zero-steps` Limit is the local budget; Python AST has none).
- Host 60 fixture controls including LEAF-before-RANGE, child other-subject/rule, opaque extra blob, empty proof, claimed false/indeterminate. `cargo test --locked --offline -p opensip-host predicate_witnesses --lib` ok (each case also `steps==0` → Limit).
- Identity policy independently passed: `sourceFilesVerified: 110`. Frozen workspace sums to **107**. Independent `cargo clippy --locked --offline --workspace --all-targets -- -D warnings` Finished.

Did not rebuild the harness and re-pipe 2.6 MiB `predicates-requests.ndjson`. Did not re-exec Unicode-15 or 07–12 corpora.

## requiredFindings

None.

## Limits (not required findings)

- Local checked/predicate counts are not ADMIT, atom truth, proof census, `close_run`, or ReplayedRun.
- Policy compilation, walk/native census, stages, and view-joins remain other owners.
- Whole-program `RuleProgramV2` stands in for per-node `admit_program_predicate_node`; this slice does not re-run policy-22.
- Python AST replay has no `work` budget; rust `Limit` on `steps==0` is the local implementation bound.
- Candidate lock is historical 18/22; live 18/24 runtime v10 is a **separate** install and does not include these `proofs.rs` bytes.
- Did not re-pipe 2.6 MiB requests through a rebuilt harness.

## Verdict

No required findings. Private `inspect_predicate_witnesses` matches selected reference-v2 I 1829–1852 with explicit payload-walk NOOP, LEAF-before-RANGE, same-rule-subject child keys, and no caller proof sets. Not a live/runtime selection.
