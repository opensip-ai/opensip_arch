Final run done, plus three things that turned up while reconciling the bytes.

**Final command** — `/tmp/opensip-architecture-review-env/bin/python -I -B .../output/lib/verify_all.py`, fresh process, after the last edit:

| | |
|---|---|
| verdict | **ACCEPT-RECONSTRUCTABLE** |
| stages | 48 declared / 48 recorded / 0 failed |
| kit | 102 / 102 rows verified, manifest `5f53b88a…`, parent `1cf3db70…` |
| measured delta | 97 unchanged / 5 changed / 0 added / 0 withdrawn (inventory verified, 0 disagreements) |
| requirements | executed 131, futureQualification 3; MUST 0 / SHOULD 0 / advisory 1 |
| helper rows | 36, **0 open** |
| positives | syntax-code 877, typescript 1062, rust 1157, rust-partial 747, syntax-data 804 closure checks |
| query / mutation surfaces | 20 ops, 110 checks, 8 controls refused / 29 checks, 7 controls refused |
| history | CONFINED-WITH-DISCLOSED-HISTORICAL-DAMAGE (generation-16 overwrite still OPEN); NO HISTORICAL LABEL DRIFT |
| md sha256 | `b083e634338b012e796b28f4b60f6cde7b107408b5c9952d43920f648de6928c` |
| json sha256 | `98820890378980acfd882f3a3d12e9b6aef437316c4a229292d7bc2e1ba33412` |

**Reconciliation to the exact final bytes, re-measured out of band.** All 102 rows of `retainedArtifactDigests` recompute to the bytes on disk (0 mismatches, 0 missing). The digests the reports quote that are *not* file hashes are framed identities and measured keys, and each one is literally present in the artifact that carries it: 5×5 run/seal/proof/plan/snapshot ids across export+closure+replay, and the four per-step-kind idempotency keys in the mutation artifact. The `48 / 47` pair in the review is ordering, not a discrepancy — the reconciliation stage records 47 because it is itself stage 48.

**Byte reproducibility, now disclosed in the report.** Three consecutive commands with no source edit between them produced a **byte-identical** `blind-review.md`; `blind-review.json` differed in exactly nine leaves, all clock readings — seven stage `seconds`, `firstWriteOfThisSessionUtc`, and the digest of the one artifact carrying that timestamp. No substantive leaf changed and none was added or dropped. Measured with `diagnostics/json_variance.py`, deliberately outside `output/` so taking the measurement doesn't perturb the tree.

**One new defect found and fixed: V20-D6**, the complement of V18-D6. Because the rebind rewrites path form only — correctly — four hand-written *current* self-declarations kept an older label: `helper-corrections.json` declared `consumerId` `consumer-b.v18`, `vectors/repair-descriptor.json` declared `v19`, `standing.kitOnly` still listed the generation-17 review and generation-18 response as this generation's disclosed prior inputs while the custody artifact it cites named the generation-19 ones, and one sentence said "generation 19 wrote into none of them" about this session's own measurement. Path confinement was never affected (census CLEAN, all writes under 20); the reports simply misnamed their own author and inputs. The two ids are now v20 with in-code notes separating them from the row `generation` fields (v14–v19 provenance untouched), and the input list is now read verbatim from `notes/v20-input-custody.json` rather than restated. `diagnostics/current_declaration_audit.py` reports **0** current-declaration fields naming another generation, and the label-provenance check still says NO HISTORICAL LABEL DRIFT, so nothing historical was rewritten in the repair.

Standing unchanged: no root verdict is known to me, no product or host is qualified, synthetic TCB observations remain assumptions.
