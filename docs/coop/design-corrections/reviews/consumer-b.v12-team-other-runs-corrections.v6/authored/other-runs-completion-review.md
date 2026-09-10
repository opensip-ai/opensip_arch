# Other-runs completion (v6 peer-law correction)

**Verdict: `OTHER_RUNS_READY_FOR_INDEPENDENT_RECHECK`**

Same original B12 kit-only author origin. Previous query-run-corrections.v1 is complete. This pass corrects the four existing non-pilot Runs (query-prepared TypeScript, Rust, syntax-data, rust-partial) against completed independent peer findings, plus the bounded foundation trace issue (separate review). Not independent acceptance, not whole-consumer ACCEPT, not a new Run kind.

`R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR` remains unexecuted.

## Custody

team-inputs.json `20337e19afd19c9bf0a85ed8c4d3a583e1a8a1f0c77d88f83782ca98c8fcfedc` match. Ten peer reports PASS. Kit 80/80. Charter `57df2ed62c…`. native-selfaudit precedes law-disposition. Law-disposition withdraws the diagnostic exception and the syntax-data ADMIT. Raw-export is structural-only on old exact inputs. None is a blanket oracle.

## Peer first refusals vs this origin’s current operands

| Run | Peer first refusal (old bytes) | This correction |
|---|---|---|
| ts | `compilerPackageDigest` not a toolchain tree member (peer also saw old `ca1b44df`; current predecessor was query-prepared `59b7d384`) | digest is a tree member of `toolClosure.closureId`; `compilerVersion` equals closure `semanticVersion` |
| rust / rust-partial | `rustcVersion` `1.80.0` ≠ closure `semanticVersion` `1.0.0` | `rustcVersion` produced from admitted closure `semanticVersion` |
| syntax-data | predicate `inputRefs` `domain=rule-program` (law-disposition; not a diagnostic) | `compose_proof` no longer inserts that citation; program bound by `proof.ruleProgramDigest` |
| all four | identity §3 subset MUST | predicate domains are `view`+`coverage` ⊆ evaluationInputRefs; `rule-program` not added to selectedRefs |

Do not reinstate the withdrawn diagnostic. Do not add forbidden selected roots.

## From-scratch commands (exit 0)

Second produce hash-identical. Structural admission precedes semantic replay on every graph. Tamper remints proof/evidence/seal/run then semantically refuses.

```bash
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-team-other-runs-corrections.v6/output/scripts/build_ts_run.py
# likewise build_rust_run.py, build_syntax_data_and_partial.py, build_rust_partial.py
/tmp/opensip-architecture-review-env/bin/python -I -B \
  .../scripts/replay_from_export.py <store>
/tmp/opensip-architecture-review-env/bin/python -I -B \
  .../scripts/replay_from_export.py --tamper <store>
```

| Store | SHA-256 | runId | structural | semantic | tamper | verdict |
|---|---|---|---|---|---|---|
| ts | `bac8d383…10b6` 709874 | `run3:26dd4376…0164` | pass | C equal | refused | pass |
| rust | `44989322…ab82` 548285 | `run3:9032d3b0…5436` | pass | C equal | refused | pass |
| syntax-data | `2c4f1950…cc7e` 490800 | `run3:ab1d6fc4…ae7f` | pass | C equal | refused | indeterminate |
| rust-partial | `ddd72876…9920` 508684 | `run3:0f06d053…8c5b` | pass | C equal | refused | indeterminate |

Predecessor bytes: `preserved-failures/v6-pre-peer-four-runs-and-traces/`.

## Frozen

`syntax-code.store.json` `0a0b2c62…ec36` 889618, workflow/scope/query/envelopes/vectors/checkpoints/output-traces, and foundation artifacts other than traces: freeze `frozen-this-pass.other-runs.v6.json`, **0 mismatches**. The frozen pilot was not rebuilt under the corrected `compose_proof`.

## Query input properties (support, not execution)

TS still carries node_modules, bare specifier `left-pad`, import payload, and the two-hop attributed `imports@resolved-target` chain plus one stored unattributed import. SubjectId namespaces were not stripped. occupancy=external remains the jointly satisfiable TargetAttributionV1 reading (payload SubjectIdV1 vs file-inventory LogicalPath). That is not a kit contradiction that cannot be jointly satisfied.

Required query operations and complete output parity still await final workflow integration.

## Clone quantifier

Charter at-least-one complete file-fact Run across TS|Rust|syntax-code, not per-language L1. L0 clones remain on the complete TS and Rust graphs. syntax-code is frozen pending integration.

## Limitations

- Query cases not executed.
- syntax-code not reminted.
- Raw-export review did not measure these new store hashes.
