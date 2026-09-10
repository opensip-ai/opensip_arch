# Provider-return COMPLETE56 — coauthor peer (v4)

**Standing.** Same independent Grok coauthor peer as COMPLETE30. Focused correction review of author COMPLETE56. Not fresh blind. Not final-whole-design acceptance. Not pin seal. Not product compiler. Not LIVE D9. Query/proof/closure out of scope.

**Verdict: `ACCEPT_SCOPED`.**

COMPLETE30’s four MUSTs and the occupancy-relevant SHOULDs are closed on these bytes. 42 helper rows are **not** native/compiler proof. Remaining residuals are documentation drift and a non-required receipt `outputDomains` compare.

Source-manifest SHA256 `7e9211aefba919147f17efb5818fc3de36da58db704700ea35efc7ca7bc2ded1` matches. **1323/1323** files match. **22/22** proposed hashes match. Model `78eac275f4c638c515695dd511126fb7f742a2fcb372e56f1c1f06ba62ce41c8`. Source and historical peer outputs were not modified.

---

## COMPLETE30 findings vs these bytes

| COMPLETE30 | Result | Evidence |
|---|---|---|
| MUST-1 stage correlation | **Closed.** `FactBatchV3.stageId` is C-2 **text**. `DispatchBindingV1` separates `analyzeRequestOrdinal` from `retainedStageOrdinal`. Integer `stageId` refuses schema. Subset Analyze (request 0, retained 5, text `s-imports`) admits the Plan producer, not Plan ordinal 0. TS `StageRequestV1.stageId` text + `stageOrdinal` contiguous; Rust `StageRequestV2.stageOrdinal` + nested `planStage` C-2 bytes. §9.6 matches those owners. No fictional compiler access; worker echo is request `stageId` text. | `P-STAGEID-TEXT-SUBSET` |
| MUST-2 trusted inputs same set | **Closed.** Dispatch is required (`PROVIDER_RETURN_DISPATCH`). Capture requires receipts (`PROVIDER_RETURN_RECEIPT`). Buffer during ANALYZING does **not** require receipts/views (`status=buffered`, no refs). Batch `analysisOrdinal=77` cannot bypass dispatch (`PROVIDER_RETURN_ANALYSIS_ORDINAL`). | `P-DISPATCH-RECEIPT-TIMING` |
| MUST-3 prior-batch facts | **Closed.** Distinct compatible prior V2 admits with **current-only** mint map. Combined occupancy-conflict uses sidecars (`_admit_provider_occupancy_conflicts` does not use facts). | `P-PRIOR-AND-ANCHORS` |
| MUST-4 schemas without mutation | **Closed.** Published `occupancyCompanions.items` `$ref` `opensip.product.occupancy-companion.1`; return `records.items` `$ref` `opensip.product.target-attribution.2`. No import-time `items =` assignment. Independent Registry admission: first-party null `evaluationNativeId` **refuses**; external/unknown/package allOf branches behave. `candidateOrdinal` vocabulary is published on the companion schema. | `P-SCHEMA-NO-MUTATION`, `P-COMPANION-BRANCHES` |
| SHOULD-1 mint anchors | **Closed.** Different path, same length → `PROVIDER_RETURN_MINT_MISJOIN` `anchors`. Correspondence is `(path, blobDigest/contentSha256, startByte, endByte)`. | `P-PRIOR-AND-ANCHORS` |
| SHOULD-2 receipt closed fields | **Occupancy-relevant join closed; residual not required.** Capture requires receipt + selected view digest on `outputRefs` (`PROVIDER_RETURN_VIEW_NOT_ON_RECEIPT` on owner path). Bind still does not compare receipt `outputDomains`/`state` to the stage row (`P-RECEIPT-OUTPUTDOMAINS` admits a `coverage` vs `view` mismatch). That is unused by this binder given view-on-receipt. Not a remaining MUST. | owner-positive negative; `P-RECEIPT-OUTPUTDOMAINS` |

No blanket `producerClosure == enumerator.closureId`. Enumerator may differ (`P-ENUMERATOR-HOST-INTERNAL`).

---

## Owner-admitted semantic fixture (not 42-as-proof)

`test_owner_admitted_semantic_fixture_positive` **passed** in the independently re-run 42-case checker.

**Preadmitted TCB observations (helper does not re-mint as FACT-ID-V1 proof):** fixture fact2 payload/anchors, view, inventories, enumeration plan, execution-plan/stage-spec, `attach_host_capture` receipts, `DispatchBindingV1` assembled from that stage (`expectedStageId` set to `"s-imports"` in lockstep with the transcribed batch, not read from a C-2 field on the execution-plan row).

**Runtime verification on the same graph:** `open_run_closure` → `derive` → `replay` → `close_run`. Captured sidecar digest equals the fixture sidecar digest. Malformed receipt `outputRefs=[]` through that path refuses `PROVIDER_RETURN_VIEW_NOT_ON_RECEIPT`.

**Not claimed:** compiler TCB authenticity, FACT-ID-V1, live protocol3 FactBatch CBOR, OS qualification.

Handmade helper facts remain TCB assumptions for narrow join comparison (including digest `1c5df32c…` on that path).

---

## Controls (first failures)

| Check | Result | First failure | Class |
|---|---|---|---|
| `check-provider-attribution-return.v2.py` | **42/42**, `fullRun: false` | none | Helper + one owner-fixture/M3 path. Not compiler proof. |
| `check-array-orders.py` | **121/121** | none | Helper. |
| Independent probes | 10 ran; 8 author-claims hold | none required; advisory `P-STALE-PRODUCERSUPPLY` | This peer. |
| Full launcher | **not run** | pins stale | No pin bypass. |
| `protocol3_run` live FactBatchV3 | **not run** | author remaining | Not a new blocking requirement. |

Author first-run overlay `delivery.v4.json` missing and owner-positive universe mismatch are **harness/fixture** history, not present on this overlay re-run.

---

## Residual (not required)

1. **Advisory.** `provider-target-attribution-return.schema.v2.json` `producerSupply.modes` still says “After fact2 mint, emit one V2 record…”. Title/invocation already withdraw COMPLETE58 as delivery. Occupancy companion is the current channel. Minimal correction: replace that sentence with in-worker companion emit. Not a wire bypass.

2. **Optional SHOULD remainder.** Receipt `outputDomains`/`state` unused by occupancy bind. View-on-`outputRefs` is the selected-view join this correction required.

---

## Read coverage

Normative: `provider_attribution_return_model.v2.py`; `dispatch-binding.schema.v1.json`; `fact-batch.schema.v3.json`; `occupancy-companion.schema.v1.json`; `provider-target-attribution-return.schema.v2.json`; `canonical.py` `validate(..., registry=)`; `check-provider-attribution-return.v2.py`; native-evidence §9.1/§9.4/§9.6; TS `delivery.v2` `StageRequestV1`/`FactBatchV1.stageId`; rust `StageRequestV2`; `StageReceiptV1`; author COMPLETE56 MD/JSON/proposed-hashes.

---

## Limitations

- Did not read other root/source/reviews, web, or subagents. Own peer v2/v3 history used.
- Did not run source-pinned full launcher.
- Did not run live compiler/`protocol3_run` FactBatchV3.
- Native live compiler/OS/D9 remain later qualification.
- No self-authored source fixes.

No pin seal. No freeze. No commit. No whole-design acceptance.
