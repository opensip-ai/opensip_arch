# Other-runs completion review — TypeScript, Rust, syntax-data, Rust partial clones

**Verdict: `OTHER_RUNS_READY_FOR_INDEPENDENT_RECHECK`**

This is not whole-consumer acceptance, not `ACCEPT-RECONSTRUCTABLE`, and not root admission. Two verbatim kit-only peer reports (`OTHER_RUNS_REFUSED`) were assessed against original kit law. Peer expected proof digests on unadmitted graphs were not copied. Syntax-code, `foundation/`, and workflow/scope outputs stayed byte-identical.

## Standing and custody

| Object | SHA-256 | Result |
|---|---|---|
| kit `consumer-input-manifest.json` | `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` | PASS 80/80 |
| parent frozen SHA | `a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb` | match |
| `requirements.json` | `855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495` | unchanged |
| `team-inputs.json` | `3a728ad08934deda8f06d55a59ab1ed316efc51fa5128e0db9aac203563e1ddc` | authenticated |
| `team-inputs/other-runs-review.md` | `2b1829d39ab28f5696971026fdfb3025b6b657b37390942b4617e6dd635c9179` | match |
| `team-inputs/other-runs-review.json` | `231392ebeccd36f04eed81fc103677871139e92e3e1816c7a198826a85c0c6f7` | match |

Write root is only `consumer-b.v12-team-other-runs-corrections.v5/output`. Path correction: `path-correction-record.v5.json` (SHA `6014fdfbca54ffa1a0fa295d8ce6b121e81c59d5e9f35f035761ad5503c7fb59`).

## Frozen this pass

Syntax-code store `0a0b2c6217846264b2bff2b013410215b0941c4c50d695bd234a1d5aac14ec36`, all 25 `foundation/` artifacts, and 80 workflow/scope envelopes/query/vectors/traces/reviews: 0 mismatches.

## Preserved predecessor four-Run graphs

Peer-refused v4 stores copied to `preserved-failures/v4-peer-refused-four-runs/` before replacement: ts `af2238a65a…`, rust `e6457494c4…`, syntax-data `e050875685…`, rust-partial `227856b1de…`.

## From-scratch commands

Builders then replay (admission prerequisite) then whole-graph tamper:

```
/tmp/opensip-architecture-review-env/bin/python -I -B …/scripts/build_ts_run.py
/tmp/opensip-architecture-review-env/bin/python -I -B …/scripts/build_rust_run.py
/tmp/opensip-architecture-review-env/bin/python -I -B …/scripts/build_syntax_data_and_partial.py
/tmp/opensip-architecture-review-env/bin/python -I -B …/scripts/build_rust_partial.py
/tmp/opensip-architecture-review-env/bin/python -I -B …/scripts/replay_from_export.py <store>
/tmp/opensip-architecture-review-env/bin/python -I -B …/scripts/replay_from_export.py --tamper <store>
```

Each replay exit 0, `closureOk=true`, `proofCompareEqual=true`, `firstRefusal=null`. Tamper remints proof+evidence+seal+run, admits the replacement, then semantically refuses. Stale-hash C-inequality is recorded separately.

## Per-Run results

| Run | Store SHA-256 | Run / Plan / Proof | Verdict | Admission / Replay / Tamper |
|---|---|---|---|---|
| ts | `ca1b44df3f89bc6d6cc63edfe239ce510a60c7fc47f2d531c5bcb10385b99086` | `run3:9fb05cf2…` / `plan2:9a6654ad…` / `proof3:6969b09b…` | pass | PASS / C `f1d4454d…` / refuse `proof3:d6ee2aaa…` |
| rust | `3b4daf1caa81f11cbaa255feede860c27fc81dd27b92e1f31cb9de634570d791` | `run3:db635639…` / `plan2:25d8e4df…` / `proof3:8c329c54…` | pass | PASS / C `d7efff1f…` / refuse `proof3:80495bf8…` |
| syntax-data | `00fce98f9683084563b1bf54e1119813fc97d670250e49fd7d56ad5fe57e5099` | `run3:4ec370fb…` / `plan2:09e25c1e…` / `proof3:d0d5b5f1…` | indeterminate | PASS / C `490810b7…` / refuse `proof3:4387e3c3…` |
| rust-partial | `89fd6accbc6181217e6605fbc6b4a058520b7ae8ce0cda3523f4a0a86b1a004c` | `run3:4852e398…` / `plan2:1539822b…` / `proof3:94063605…` | indeterminate | PASS / C `3fd11e8c…` / refuse `proof3:1f05af57…` |

Original IDs: `R-RUN-TS` (+ node_modules, config-deps) → ts store. `R-RUN-RUST` and mixed-edition / target-edition / body-dialect / same-file-two-editions / hash-marker / stable-body / large-map / version-component → rust store + `runs/rust.body-identity-pair.json`. `R-RUN-SYNTAX-DATA` + `R-RUN-UNAVAILABLE-SEMANTIC` → syntax-data. `R-RUN-RUST-PARTIAL-EMPTY-CLONES` → rust-partial.

Discriminating properties retained: TS `node_modules/left-pad` + bare specifier; RuntimePayloadV1 `istanbul-json`; Rust `#/Cargo.toml` marker, mixed 2015/2018/2021/2024, package 2018 vs bin 2021, L0 `sha256:321e22ac…` ≠ `sha256:4cfa4328…`, same-dialect lib vs lib+test L0 equal; syntax-data clones Coverage unknown + `language-tier-unsupported`/`capability-missing` without complete-empty concealment; rust-partial empty clones facts, clones Coverage unknown, required cell partial.

## Peer findings vs kit

Existing-law corrections (not first-refusal-only):

1. **Import payload.** `RuntimePayloadV1` format enum and object `observationWindow`. TS import `import2:98fee8f9…` now inhabits the payload registry.
2. **Rust snapshot join.** `crateRootPaths` is `#/a/Cargo.toml` (inventoried). `#/a` is not a Blob path.
3. **Tree length.** `bin/proc-macro-srv` declared length equals retained 14 bytes.
4. **Body-language owner.** Kit selectionLaw: one physical path at two editions is valid **one selection at a time**. Sealed universe selects `bin.tool@2021` only (`editions=[2021]`). Lib@2018 and lib+test@2018 are retained other selections, not stuffed into one `selectedUnitIds`.
5. **syntax-data applicability.** Matrix `clones-fact × syntax-only` is `SUPPORTED-DESIGN`, so the account is `supported-available`. Grammar/scopeCapabilityLaw still discloses unknown Coverage. Required cell is **partial**, seal **indeterminate**. `unsupported-typed` is the matrix UNSUPPORTED-TYPED state, not this cell.
6. **rust-partial composition §5.** Required partial cell now produces `executionDeficiencies` and sealed `indeterminate`, not a false pass.
7. **evaluationInputRefs.** enumeration-contract §7: selectedRefs plus the execution-inputs reference only.
8. **Tamper.** Whole replacement remints proof, evidence, seal, and run; replacement is admitted; semantic C differs from the expected proof. Stale-hash remains a separate control.

Passing peer subgrades (node_modules, mixed edition, hash marker, file inventory, empty clones facts) were not treated as a waiver of the failed joins.

Disputed / scoped:

- Peer `proof-C-compare` expected IDs were diagnostic reconstructions on graphs that had already failed structural admission. They are not this origin's accepted proofs. Expected proofs here are independently composed after admission.
- `R-RUN-RUST-SAME-FILE-TWO-EDITIONS` is exhibited as two selections of one path (2018 vs 2021), which is the kit-lawful form. Putting both in one `selectedUnitIds` is the refused ambiguous request.
- `R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE` original observable allows “two retained graphs or an explicit pair vector”. Lib-only and lib+test universes are retained; L0 is equal when dialect does not change.
- No broader default-profile cells were invented. Unselected `calls`/`types`/`references` were not demanded.
- `component-manifest-schemas.v11` remains CANDIDATE-NOT-APPLIED; stored-bytes tree join still executed.

## Shared helper changes

`helper/compose_proof.py`, `execution_inputs.py`, `annotated_admit.py`, `proof_replay.py` were repaired for these four Runs. Replaying the frozen syntax-code store with the new `evaluationInputRefs` rule would mint a different proof C; that store was not overwritten. Later peer integration owns that conflict.

## Remaining work

ROOT-ADMISSION not performed. v11 inhabitance not claimed. Real host/compiler/crypto not demanded. L1 tokenisation not executed. Default-profile remaining matrix cells not requested. Syntax-code, foundation, and workflow remain other actors. All 123 original accept-blocking obligations remain.
