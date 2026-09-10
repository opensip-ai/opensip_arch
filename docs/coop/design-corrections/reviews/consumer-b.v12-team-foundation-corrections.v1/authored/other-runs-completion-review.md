# Other-runs completion review — TypeScript, Rust, syntax-data, Rust partial clones

**Verdict: `OTHER_RUNS_READY_FOR_VALIDATOR_RECHECK`**

This is not whole-consumer acceptance, not `ACCEPT-RECONSTRUCTABLE`, and not root admission. The syntax-code pilot remains a separate recheck request and was not modified. Prior whole-complete helper claims were reassessed against current kit law; evaluator-unselected plans, view-plus-inventory stage products, hardcoded complete cell rows, and unretained FACT-IDENTITY frames were reconstruction misses of existing law.

## Standing and custody

| Object | SHA-256 | Result |
|---|---|---|
| kit `consumer-input-manifest.json` | `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` | matches |
| parent frozen SHA | `a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb` | matches |
| 80 subject files | kit list | PASS 80/80 |
| `requirements.json` | `855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495` | unchanged |
| `continuation-inputs.json` | `35af7a13ff151cba8976903f4a5bca8c3342a8d84c7d8e709c0d5cf60fa3f35f` | no new peer/root files |

Write root is only `consumer-b.v12-team-corrections.v4/output`. Path correction record: `path-correction-record.v4.json` (SHA `d5446634e8f374dc2fcfbcc3ff26bd546d1bbdae895a8fccb8ec15776860e176`; rewritten 18, unchanged 15).

## Frozen this pass (byte-identical)

Syntax-code store `0a0b2c6217846264b2bff2b013410215b0941c4c50d695bd234a1d5aac14ec36` and scope-v2 `scope-correction-review.json` `554ec31f8c6dd1c2e5eb039fe8992024d935faf7f1f25621ae0771b3274d9b97` (and the other frozen scope-v2 hashes in `frozen-this-pass.v4.json`) were not rewritten.

## Preserved predecessor stores

| Run | Path | SHA-256 | Bytes |
|---|---|---|---|
| TS | `preserved-failures/ts-original/runs/ts.store.json` | `885b8e4575235fe47fbee893d83e97d650aea230f9af870b8a711f25d943075d` | 642462 |
| Rust | `preserved-failures/rust-original/runs/rust.store.json` | `67dc12f88fc19fb320385d30f6a740197c64ca9d574627b8db81cdb2f2000315` | 496105 |
| syntax-data | `preserved-failures/syntax-data-original/runs/syntax-data.store.json` | `1d07e4c8040035965a8821559a5916cf82014e19198e1e6acaf6e9b5ecdd6092` | 476183 |
| rust-partial | `preserved-failures/rust-partial-clones-original/runs/rust-partial-clones.store.json` | `b6c2b240e11fff9699aeeacdd8a68a7ee7119f241029e3de0e4c955e2b058246` | 494017 |

Those bytes were not relabeled as accepted.

## Existing-law corrections applied to all four

- Direct evaluator (and extra detector) in `plan.semanticClosures`.
- Reference stage `outputDomains: ["view"]`; inventories as `hostDerivedRefs`; `selectedRefs` exact totality.
- `derive_outcome` joined to host `CellProgramOutcomeV1` rows.
- Native coverage accounts equal the matrix pairs of the requested capabilities.
- Component-manifest stored-bytes join (v11 stock inhabitance not claimed).
- FACT-IDENTITY L0 frames retained under suffix for clones facts that mint them.
- Complete expected proof composed from exported selected inputs; fresh-process C/identity compare; logical-result tamper distinct from stale-hash C inequality.

## Per-Run results

### TypeScript (`R-RUN-TS`, `R-RUN-TS-NODE-MODULES`, `R-RUN-TS-CONFIG-DEPS`)

| Field | Value |
|---|---|
| Store | `af2238a65afb0b7d82c5dd5ab1278436d55c4bc3087631d407563346593eb4ca` (678780 bytes, 115 blobs) |
| Run | `run3:97651646098ed5ff74bbafa5546898d9a96e77fa352beb209c622bd321276adc` |
| Plan | `plan2:2d723a9a8f88e00bbd81af2ee4a262bcf24c73e9cca9514facf24060cd3514dc` |
| Proof | `proof3:ab7796b647e93608b36dbae713977d088f41882682bff889dfaed39a6f86e0c7` |
| Fresh replay | exit 0; `closureOk` true; `proofCompareEqual` true; derived verdict `pass`; atom `false`; proof C `afc54dc5d0cd73208c9de95363cf2590c3c7b1c854d9dc73e103a6c092820f36` |
| Tamper | semantic refuse true; stale-hash control true; `proof3:0925ffba1773128a227920a24b4bc514e2970b50467251477fdece4756a2a0e1` |
| Properties | `node_modules/left-pad` retained; bare specifier `left-pad`; `TypeScriptConfigGraphV1` and `ResolvedNodeModulesLayoutV1` stock-ok; import `import2:1bdd740b…0eaa` |

### Rust (`R-RUN-RUST` and original ownership/edition properties)

| Field | Value |
|---|---|
| Store | `e6457494c46b2c8cefc7f6c0779da08de820b26890bc250defe1361b6e29fd4a` (536279 bytes, 100 blobs) |
| Run | `run3:02f31e575e6841316fe34f4f9a95fcb572c528b66f9793aad948078ec59a7949` |
| Plan | `plan2:12445233b2b92fdd2df79c7189f5a7b4a13a1402331d6bb8e075c25620575380` |
| Proof | `proof3:026843f105a1bdc931091b8224eec091fb5cd2aa0961efef1efa1dd2c5e4e86c` |
| Fresh replay | exit 0; `closureOk` true; `proofCompareEqual` true; derived verdict `pass`; proof C `00d293ea4e699c61d66058598a58c8bd69cb6be96fe44122b385b6b6bd54b2ce` |
| Tamper | semantic refuse true; `proof3:55a7ae5ffed5b37360d993a5e77d841dc98be053d5e9cd97c1e0e8420197668b` |
| Mixed editions | 2015, 2018, 2021, 2024 on the edition map |
| Target ≠ package default | package `a` 2018; `bin.tool` 2021 |
| Same file two editions | `#/a/src/lib.rs` owned by lib and bin units; L0 2018 `sha256:321e22ac…4d1b` ≠ L0 2021 `sha256:4cfa4328…7fa8` |
| Hash marker | inventoried `#/Cargo.toml` |
| Stable body on ownership-only change | lib-only selection identity equals 2018 L0; pair in `runs/rust.body-identity-pair.json` |
| Large edition map | 17 entries; languageVersion from admitted rustc context + body dialect |

### syntax-data (`R-RUN-SYNTAX-DATA`, `R-RUN-UNAVAILABLE-SEMANTIC`)

| Field | Value |
|---|---|
| Store | `e050875685a7a4f706c98982baeafbce3b15f9c6c4c2ff97c2800a820645ec87` (490576 bytes, 65 blobs) |
| Run | `run3:a803341435a3a360d96c535261d3e45a32942a5db4c445764d102d1810ffccbc` |
| Plan | `plan2:09e25c1ec3e3267c252402623391071321a6dc0d2551200dd504c23aabb61cd9` |
| Proof | `proof3:22e08d2fa0618444910aff48ea7bc8d862cde7c837cc6473024f095681ff6337` |
| Fresh replay | exit 0; `closureOk` true; `proofCompareEqual` true; derived verdict `pass`; proof C `7d791f7c7eeb94a0519bcb9fe3426f9cd331badf1a4fc67a8c5572de4028950f` |
| Tamper | semantic refuse true; `proof3:c09833ece4b29e9bbf5a6bc11e99fb264f8a4e3f2910fded9d9454b670bf8580` |
| Unsupported clones | Coverage `unknown` + `language-tier-unsupported` / `capability-missing`; native account `unsupported-typed`; not complete-empty concealment. Inventory present. Membership is syntax-only with `unitOrdinal` null (no invented unit). |

### Rust partial/empty clones (`R-RUN-RUST-PARTIAL-EMPTY-CLONES`)

| Field | Value |
|---|---|
| Store | `227856b1dec3c4d051677e156b9b3883613a90dee7e1c8db46670bb95a4e1141` (501289 bytes, 77 blobs) |
| Run | `run3:679b3d194b062fa3b113a453b9c45c01da530fa0d553570f8d98d44a50832737` |
| Plan | `plan2:a98f5aab0dfe84694a41f36aa5aa33bc2a152e46f33fe6e02c577d74d45fd8c5` |
| Proof | `proof3:607fbbdb8b74c939ac42e6506c8b0c3f09dfc4c186b7c458f3eb3f8f8cc9ba5a` |
| Fresh replay | exit 0; `closureOk` true; `proofCompareEqual` true; file-present derived verdict `pass`; proof C `3ecd8de773be3907f46e698d5d4a10ddf9c70b091249f4be699bdf2835aa8ca4` |
| Tamper | semantic refuse true; `proof3:a1c0fcc48b9410c89848b8d1677edd04044b877a46cecad80b703424403b786b` |
| Partial clones | ownership `enumeration=partial`; no clone facts; clones Coverage `unknown` + `input-closure-incomplete` / `body-language-owner-unenumerated`; clones-fact cell **derived partial** (not rewritten complete). File-present still evaluates from the complete inventory cell. |

Replay command (each store):

```bash
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-team-corrections.v4/output/scripts/replay_from_export.py \
  /tmp/opensip-design-corrections/consumer-b.v12-team-corrections.v4/output/runs/<stem>.store.json
# --tamper for logical-result tamper
```

## Applicable-law inventory (this pass)

| Law | TS | Rust | syntax-data | rust-partial |
|---|---|---|---|---|
| evaluator in `plan.semanticClosures` | PASS | PASS | PASS | PASS |
| selectedRefs totality / view-only stage | PASS | PASS | PASS | PASS |
| derive_outcome join | complete×4 | complete×3 | complete×2 (clones-fact via unsupported-typed) | clones-fact **partial**, inventory complete |
| native coverage totality for requested cells | PASS | PASS | PASS | PASS |
| annotated digest/order/membership on graph records | PASS (fresh process) | PASS | PASS | PASS |
| complete expected proof C compare | PASS | PASS | PASS | PASS |
| logical-result tamper | PASS | PASS | PASS | PASS |
| TS config-graph + node_modules nested records | PASS | N/A | N/A | N/A |
| Rust ownership/edition/body dialect | N/A | PASS | N/A | partial ownership exhibited |
| syntax grammar tree | N/A | N/A | PASS | N/A |
| TypeScript/Rust compiler execution | not demanded | not demanded | N/A | not demanded |
| ROOT-ADMISSION | not performed | not performed | not performed | not performed |
| v11 component-manifest stock inhabitance | not claimed | not claimed | not claimed | not claimed |

Requested capabilities are explicit analysis-spec rows, not the full default-profile product. Default-profile remaining cells (TS/Rust `calls`/`types`/`references`/…; syntax-only UNSUPPORTED-TYPED extras beyond clones-fact) are not cells of these Plans.

## Remaining obligations

1. Independent validator recheck of these NEW graphs. This walk is not root admission.
2. `ROOT-ADMISSION` was not performed.
3. `component-manifest-schemas.v11` remains `CANDIDATE-NOT-APPLIED`; signature envelopes are not verified.
4. L1 token-stream tokenization was not executed where L1 facts are absent.
5. Default-profile remaining matrix cells are not requested here.
6. Syntax-code pilot and scope-v2 outputs stay frozen for other reviews.
7. Original requirements outside these four Runs remain visible and unverified by this pass.
8. Whole-consumer `ACCEPT-RECONSTRUCTABLE` is not issued.

Python: `/tmp/opensip-architecture-review-env/bin/python -I -B`.
