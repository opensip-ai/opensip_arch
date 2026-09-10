I'll stay on the same kit-only team origin, authenticate the copied S-origin pilot and the four peer reports, then remint the syntax-code positive and a structurally valid logical-result tamper from actual derivation.I'll authenticate the copied snapshot and peer reports first, then read the law-interaction findings so the remint follows those owners rather than prior grades.Peer law is jointly satisfiable: omit `rule-program` from predicate `inputRefs` and bind it only via `ruleProgramDigest`. I'll inspect the copied pilot's proof construction and the frozen-store standing next.I'll continue the same kit-only pilot authoring pass: authenticate the copied S-origin snapshot and peer reports, then remint the syntax-code proof from selected inputs rather than claimed-proof equality.Authenticating the copied snapshot, team inputs, and peer reports next, then I'll inspect the live helper paths before any remint.Hashes match. Next I’ll read the four peer reports and the live proof/checker helpers so the remint follows existing law, not claimed bytes.Peer correction is jointly satisfiable: omit `rule-program` from predicate `inputRefs`. I’ll load the builder, replay, and identity laws next, then redirect paths before any remint.Preserving the S-origin bytes, then redirecting live helper/script paths before any remint.Path redirect is done. Next I’ll apply the existing-law compose/checker fix, then remint the positive and tamper graphs.Positive remint succeeded. Next I’ll run from-scratch replay, then export the structural tamper graph.Measurements check out. I’ll write the completion reviews, freeze the other-run hashes, and record every changed versus frozen file.**Verdict: `PILOT_READY_FOR_INDEPENDENT_RECHECK`**

This is bounded authoring of the copied S-origin syntax-code pilot, not independent acceptance of these new bytes and not whole-consumer `ACCEPT`.

The P4 peer disposition is **`RESOLVED_EXISTING_LAW`**, not a demonstrated contradiction. Identity §3 requires predicate `inputRefs` ⊆ `evaluationInputRefs`. Enumeration/composition/execution-inputs require `evaluationInputRefs` = `selectedRefs` + `{execution-inputs}`, and `selectedRefs` cannot name `rule-program`. The program is bound by `proof.ruleProgramDigest` and `program-predicate.ruleProgramDigest`. `ProofInputRef.domain` still *permits* `rule-program` as shared type vocabulary; that is not a command to select it on predicates.

S-origin store `8c3b68ab…` / `proof3:0388fb97…` was shape B (subset FAIL). That is an existing-law reconstruction mistake, preserved at `preserved-failures/syntax-code-s-origin-pilot-v3/`. No absent or contradictory norm was demonstrated. No normative edit.

**Correction applied:** `compose_proof` no longer inserts `domain=rule-program` on `predicateProofs[].inputRefs`. `s3_closure` enforces the subset MUST on every predicate inputRef (the diagnostic skip is withdrawn). Complete proof/evidence/seal/Run reminted from selected inputs (`usedClaimedProofFields=[]`).

## Reminted exports

| Graph | SHA-256 | bytes | Run | Proof | Structural | Semantic |
|---|---|---:|---|---|---|---|
| Positive | `a85223b13a32c6ffcde7100dfccd526b049e7bfc848578fd5b47696e65605924` | 889218 | `run3:4b58935ae046491d0389306cbf9670e7c70a638b73e8835ac476bf08e310ff7b` | `proof3:8b21407c0b0ca62952a95201c142e66e494dd4af6524188dd1ca70202a68a521` | PASS | PASS (proof/evidence/seal/run C equal) |
| Tamper | `0d868e579f937af46006d790d0f5b7a7ea72ab8fc908d27551df0dee0c045a8f` | 893046 | `run3:8e81be4e966a29396f50b60b838b0d8257cdd213752faa903e5c26f6e8cfb49c` | `proof3:f8527d3d4b8f5543ac1c85c4b7d7c5153eeab4718dc038f5cc1c5827768b3d90` | PASS | REFUSE (expected still `proof3:8b21407c…`) |

Tamper is a whole replacement graph: selected view/facts/coverage unhidden, witness reminted, unmatched `finding3:0c895614e41c2e8a04fe8a22e04d4e7870d2d0dc38a099dddc019c1387d03cdb`, claimed `fail`/`true`, independent reconstruction still `pass`/`false`. Semantic replay **reached** because structural passed. Not a hidden-input graph labelled as a successful semantic negative. `--stale-hash` remains a separate control.

L0/L1 clone custody unchanged: file `fact2:852404c1…`, L0 `fact2:7dcdff1d…` / `sha256:72a35a8b…`, L1 `fact2:664472f8…` / `sha256:874cf4bd…`.

## From-scratch commands (measured exits)

```
/tmp/opensip-architecture-review-env/bin/python -I -B …/scripts/pilot_syntax_run.py
/tmp/opensip-architecture-review-env/bin/python -I -B …/scripts/replay_from_export.py …/runs/syntax-code.store.json
/tmp/opensip-architecture-review-env/bin/python -I -B …/scripts/replay_from_export.py --tamper …/runs/syntax-code.store.json
/tmp/opensip-architecture-review-env/bin/python -I -B …/scripts/replay_from_export.py …/runs/syntax-code.tamper.store.json
/tmp/opensip-architecture-review-env/bin/python -I -B …/scripts/replay_from_export.py --stale-hash …/runs/syntax-code.store.json
/tmp/opensip-architecture-review-env/bin/python -I -B …/probes/normative_s3_audit.py
```

Exits: reconstruct 0, replay 0, tamperExport 0, tamperStoreReplay **1**, staleHash 0, s3Audit 0.

Path redirect ran **before** execution (`path-correction-record.v7.json`).

## Frozen (byte-identical)

| Object | SHA-256 |
|---|---|
| `ts.store.json` | `885b8e4575235fe47fbee893d83e97d650aea230f9af870b8a711f25d943075d` |
| `rust.store.json` | `67dc12f88fc19fb320385d30f6a740197c64ca9d574627b8db81cdb2f2000315` |
| `syntax-data.store.json` | `1d07e4c8040035965a8821559a5916cf82014e19198e1e6acaf6e9b5ecdd6092` |
| `rust-partial-clones.store.json` | `b6c2b240e11fff9699aeeacdd8a68a7ee7119f241029e3de0e4c955e2b058246` |

Scope-v2 workflow artifacts also unchanged. Starting manifest: 241 of 280 files unchanged; prior failed bytes retained.

## Coverage and limitations

Original pilot properties executed on the new bytes: `R-RUN-SYNTAX-CODE`, `R-RUN-NO-COMPILER-UNIT`, `R-RUN-CLONES-L0-AND-NORMALIZED`, `R-REPLAY-*`, `R-HELPER-KIT-ONLY`. §3: 115/115 mapped, 0 unmapped, 0 applicable without assertion.

**notReached:** L1 tokenisation judgment; component-manifest v11 stock schema; ROOT-ADMISSION; other-four-Run remint (peer `OTHER_RUNS_REFUSED` stands on those frozen stores); positive finding emission (atom is none-of-file → false); `close_run`/query (workflow branch frozen); actual host/compiler/product qualification.

Earlier S-origin readiness, prior review grades, and a paragraph-inventory count are **not** acceptance of these exact new bytes. Scope-ready is not whole-consumer ACCEPT.
