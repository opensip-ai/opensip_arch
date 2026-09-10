I’ll author the one-pilot correction from the measured `evaluationInputRefs` equality failure, using only the kit, my prior review, and this copied snapshot.I’ll locate remaining hardcoded paths and the exact `evaluationInputRefs` plus tamper code that need correction.I’ll redirect hardcoded paths first, preserve the refused store, then correct `evaluationInputRefs` and the tamper replacement graph.**Verdict: `PILOT_READY_FOR_INDEPENDENT_RECHECK`.** This is not whole-consumer acceptance and not self-issued independent acceptance of these new bytes.

The existing-law failure was extra `evaluationInputRefs`. Kit law is `selectedRefs` plus the one execution-inputs manifest. The builder and fresh-process replay now construct and check that equality. The refused store was preserved, not relabeled accepted.

**New positive export** (`runs/syntax-code.store.json` SHA-256 `8c3b68ab…`, 889354 bytes):

| Record | Identity |
|---|---|
| Run | `run3:d7b78def…c6fd` |
| Plan | `plan2:61407daf…` (unchanged selected input) |
| Snapshot | `snapshot2:f50135a2…` (unchanged) |
| Proof | `proof3:0388fb97…` |
| Proof C | `8764a0ac…` |
| `evaluationInputRefs` | **12** (was 14) |

That proof identity is the kit-law expected identity measured on the previous graph. It was produced by reminting proof/evidence/seal/Run, not by editing store metadata.

**Fresh replay:** exit 0, `proofCompareEqual` true, `closureOk` true, verdict `pass`, atom `false`.

**Logical-result tamper** is now a structurally valid replacement graph (`runs/syntax-code.tamper.store.json`, `run3:5d2ee675…`, `proof3:94c13996…`): same selected inputs and citations; reminted proof/evidence/seal/Run; structural admission passes; fresh derivation remains `pass`/`false`; claimed verdict is `fail`. Replay of that store **exits 1**. `--stale-hash` is a separate labeled control (Run identity unchanged).

Other four Run stores and workflow outputs are byte-identical. Path literals were redirected before execution (`path-correction-record.v4.json`). Failed stores remain under `preserved-failures/`. Remaining obligations: later independent/root recheck, `ROOT-ADMISSION`, L1 token-stream, v11 candidate-not-applied, and the other Runs/workflows.
