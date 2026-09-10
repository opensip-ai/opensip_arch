I'll continue as kit-only author correction of the syntax-code pilot and its tamper replacement graph, using only this copy, the same kit, own history, and the authenticated peer reports.I’ll read the authenticated peer reports, this copy’s standing, and the current pilot/tamper artifacts next so the correction can target the actual withdrawn acceptance.Peer reports treat the tamper graph as structurally inconsistent (claimed `none=true` vs retained witness matches). I’ll read composition §§3–7 and the current tamper/proof helpers against those owning laws before reminting.Peer classification matches composition §§3–4: the tamper proof is internally inconsistent (claimed `none=true` vs nonempty witness matches, and `emitWhen` true with no `finding3`). I’ll redirect copied write paths, then remint a structurally consistent tamper graph so semantic replay can actually run.I’ll preserve the structurally inconsistent tamper store, then remint a replacement graph whose claimed value, witness matches, and `finding3` emission are internally consistent.**Verdict: `PILOT_READY_FOR_INDEPENDENT_RECHECK`.** This is author correction, not independent acceptance of these bytes, and not whole-consumer `ACCEPT`.

Peer classifications were assessed against composition §§3–4–7 and `R-REPLAY-TAMPER` and **agreed**. The v1 tamper graph (`c9c1be48…`) failed structural claimed-output joins: `none=true` while witness `matchingFactIds` still listed `fact2:852404c1…`, and `emitWhen` true with empty `findingIds`. Semantic C-unequal was not a reached replay boundary. That store is preserved and not relabeled accepted.

**Helper conflict:** v1 treated `witnessDigest` as an input citation. Witness is a claimed output. Input citations to preserve are `evaluationInputRefs` / plan / snapshot / views / facts / coverage / inventories.

**Correction:** remint witness `matchingFactIds=[]`, value `true`, emit unmatched `finding3:0c895614…`, join `evidence.findingIds`, remint proof/evidence/seal/Run. Did not keep nonempty matches while claiming `none=true`.

| Exhibit | Store | Structural | Semantic |
|---|---|---|---|
| Positive | `8c3b68ab…` `run3:d7b78def…` `proof3:0388fb97…` | PASS | PASS (expected C of proof/evidence/seal/run equal; `usedClaimedProofFields=[]`) |
| NEW tamper | `f6e79d73…` `run3:c624c90f…` `proof3:023f6c04…` | PASS | **REACHED REFUSE** (expected still `proof3:0388fb97…` / pass / false) |
| Preserved v1 tamper | `c9c1be48…` | REFUSE (`claimed-predicate-value-agrees-with-retained-witness-matches-0`) | notReached |

From-scratch builder reproduced the **same** positive store bytes. Tamper-store replay **exit 1**. `--stale-hash` remains a separate control (Run unchanged). Other four Run stores and scope-v2 outputs stayed byte-frozen. Paths redirected in `path-correction-record.v5.json` before execution.

Delivered: `pilot-completion-review.md` / `json` under `/tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v2/output`. Independent recheck and `ROOT-ADMISSION` of these new tamper bytes are still required.
