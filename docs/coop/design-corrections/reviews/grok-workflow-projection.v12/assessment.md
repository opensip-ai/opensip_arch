I’ll finish the optional-unknown controls, then apply the security v6 listing-path fix on owned W files only and close the remaining v10 root targets.Optional-unknown already uses empty subjects. Next I’ll bind the listing to `.opensip/detector-compatibility.json` on the admitted closure tree, and finish the extent/candidate targets.v12 checker is **389/389 PASS**. Reports are under `grok-workflow-projection.v12/`. This is bounded W work, not source acceptance.

## What changed

**Optional-unknown (the two v11 failures).** The old fixture still had a known runtime hit, so `none` was determinate false. It now uses partial optional evidence with **no subjects**. Admitted root `p` is `indeterminate`; `rule_can_prove_absence` stays false.

**Security v6 listing conflict.** `DetectorManifestV1` is no longer treated as `closure.manifestDigest`. That digest is the DR-103 component-manifest body. The listing is the reserved regular-file Blob `.opensip/detector-compatibility.json` on the **already admitted same `closure2` tree**. A7 v7 produced no review (empty response); this follows the v6 finding plus root’s tree-path fix. No second schema, domain, or signature verifier.

**Extent / deletion.** Snapshot membership is not extraction. A path outside examinedPaths is missing-extent unless foundation `plan.scopeDigest` covers it **and** inventories are complete (deleted under a covering census → may be CODE-FIXED). A ScopeDocument wider than the foundation walk stays missing-extent.

**Candidate locators.** `evaluator_candidate_fixture.v3.py` group-bearing graphs, reminted Plan locators, stripped `candidate-producer-result` evidence joins.

## Listing law (closed)

| Case | Outcome |
|---|---|
| Path absent | no declaration |
| Present empty `compatibleClosures` | complete listing (no peers) |
| Valid listing + trio origin | `compatibleWith` filled |
| Present malformed / unrecognized / missing blob / sha256 or length mismatch | refuse (not silent none) |
| No `trustOrigin` / revoked / swapped tree without same-closure trust | no declaration |
| Caller `compatibleWith` | still refused |

Host projection carries **`componentManifestDigest`** and **`listing {path, sha256, bytes}`** separately. Signature crypto remains TCB and is not re-tested here.

## Report

- `/tmp/opensip-design-corrections/grok-workflow-projection.v12/workflow-projection-check.json` — passed true, count 389
- companions: `source-hashes.v12.md`, `declared-compatible-standing.v12.md`, `command-inventory-joins.v12.md`
- Historical v1–v11 receipts untouched

## Owned source hashes (v12)

| File | sha256 |
|---|---|
| `workflow_projection_model.v3.py` | `e08538a3fed3fe1c0c86cb550cddf6667277aaefd452c4ab265bba44e91bb5c7` |
| `check-workflow-projection.v3.py` | `c5754a4d40762e44a3de65ffe444ab54785076d90d500af7654fbf098c9356ca` |
| `workflow-projection-contract.v3.md` | `c99ce24d77e8f07c5389d35e7340e53ffa067676c30a6bf5809095ec337542b1` |
| `schemas/evaluator3/detector-manifest.schema.json` | `1cbd69c9d29b068b95c7ce8531007671e24b92433828ca30a87a6637d81dfdcd` |
| `command-inventory.v3.json` | `f3ef932a8c7f878813fbdaa11003166f3994160490c53b65a45f7cc5ec8a4b5d` |
| `command-inventory.v1.json` | `a2ca604bc7176132bbc8f6396a66bfa46cf12d7d3f369bf46aefe82f23149067` |

Full 16 hashes are in `source-hashes.v12.md`. Root still owns the normative chapter; it was not edited.
