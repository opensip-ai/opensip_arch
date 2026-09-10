I’ll peer-review P5’s PILOT_FULL_ADMITS claim from the authorized snapshot and two raw stores only: first verify hashes and isolate a copy of the checker, then measure actual producing-law joins against the kit.Custody of the snapshot and both stores matches. Next I’ll read P5’s PILOT_FULL_ADMITS claim and the producing-law inventory without treating those reports as expected results.I’ll verify every snapshot file, then inspect the checker’s real call graph and operands rather than P5’s checklist counts.I’ll isolate a path-redirected copy of the checker, then trace `admit` → `producing_law` → `replay` for actual operands instead of inventory counts.I’ll isolate a path-only copy of the checker, run it as a fresh measurement, and independently reconstruct producing joins and proof C from the kit and the two stores.The incomplete verdict may be from probe reconstruction, not a store defect. I’ll compare reconstructed `selectedRefs` and atom values against the actual admitted operands.**Verdict: `PILOT_FULL_ADMITS`** for the original two-store syntax-code pilot. This is not whole-consumer ACCEPT and not product qualification. The prior FILE/PACKAGE import-target gap remains preserved and is outside this `file@enumerated` source-endpoint scope.

Delivered only under `/tmp/opensip-design-corrections/consumer-b.v12-kit-pilot-checker-peer-review.v1/output`:

- `pilot-checker-peer-review.md` `3e3dfb26c946694e383b200773a7feb50e8026a5dd067ec1666ca3cbffb2b0ed`
- `pilot-checker-peer-review.json` `47acfcc01640b8a459c960cdcee052c6ade6faa52557c899c72413eee3716fdf`

Peer code ran only from an isolated redirected copy (`output/isolated/checker`). Exact source is preserved; the path-only diff retargets kit/exports/output paths. Exports were not reminted. P5’s claimed output was not used as an expected value.

**Call graph, not checklist counts.** `Admit` finishes structural phases, then `Replay.run` calls `ProducingLaw.execute` before `_evaluate`. Execute reconstructs enum-plan joins, membership/extents, inventory totality, stage receipts, `selectedRefs`, native coverage accounts, cell outcomes, then evaluation-input refs. Native context admission actually runs at frame retain (`_admit_native_context`), not as the later `L-NATIVE-ADMIT` mark_pass.

**Fresh measurement on the two raw stores**

| Graph | Structural | Producing | Semantic | First refusal |
|---|---|---|---|---|
| syntax-code | ADMIT | 60 pass / 0 fail | REPLAY_MATCH | none |
| syntax-code.tamper | ADMIT | 60 pass / 0 fail | REPLAY_REFUSE | `REPLAY_PROOF_MISMATCH` after structural admit |

Independently: snapshot `{hello.rs}` membership cover; file `rows[].path` equals derived extent `{hello.rs}` (field-specific, not schema `state` membership); reconstructed `selectedRefs` C-equals claimed; all 14 required proof fields present; atom `none` of `file@enumerated` with known `hello.rs` fact is false; emitWhen false; derived proof C `eb2a3bd6…ae71` equals the positive retained proof and enclosing H. Tamper producing inputs match the positive; claimed proof C `2d2df6df…c9da` / verdict `fail` / finding `0c895614…3cdb` disagree after those joins.

**Prior claim.** P5’s `PILOT_FULL_ADMITS` (after withdrawing the earlier self-authenticating-inputs grade) is confirmed for this pilot scope.

**Checker limitations that did not hide a defect here:** extra inventory locators are not refused (extra was empty); `evaluationInputRefs` is filled from claimed `selectedRefs` after C-equality (equivalent here); `discover_units` is kit-bounded notReached; `none=true` sufficiency is unimplemented but not taken; `_waived_ids` always returns `[]` on an empty waiver join.
