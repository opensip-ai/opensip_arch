# Provider-return end-to-end — negotiated FactBatchV3 occupancy companion

**Standing.** Actual Grok DESIGN COAUTHOR. COMPLETE58 is retained and not accepted. This turn does not accept, seal pins, implement product, commit, or freeze. Provider58 source `/tmp/opensip-design-corrections/target-provider-return-successor.v1` was kept immutable (read-only). Fresh peer of provider58 is independent; its verdict is not assumed. COMPLETE58 outputs in `grok-target-provider-return-author.v1/output` are historical and preserved.

**This task output.** `/tmp/opensip-design-corrections/grok-target-provider-return-e2e-author.v1/output/`
Proposed full files: `output/proposed/<repo-relative-path>`
Patch: `provider58-to-e2e.patch`

Python: `/tmp/opensip-architecture-review-env/bin/python -I -B`.

---

## 1. Why COMPLETE58 “no wire extension” was not delivery

The worker-to-host product is a closed `FactBatch` of closed `FactCandidateV1`. The candidate already carries opaque encoded `resolvedTarget`. `planId` / `sourceFactId` / `producerClosure` do not exist until the host mints fact2. COMPLETE58 §9.6 placed a language wrapper **after** mint, building `ProviderTargetAttributionReturnV2` from a compiler-native table that is not on the wire. `admit_provider_attribution_return` consumed an already-created envelope. That is not provider invocation.

There is no unnamed table, shared memory, or host re-parse that can recover occupancy without extending the worker return. Wire correction is required and is made here.

## 2. Bounded wire correction (not a silent FactBatchV2 field)

| Item | Decision |
|---|---|
| Protocol major | Unchanged: rust-semantic 3, typescript-semantic 2 |
| Frame | Unchanged name `FactBatch` (P3-23). No new frame. |
| Historical payload | `FactBatchV2` + closed `FactCandidateV1` when token absent |
| New payload | `FactBatchV3` (`native/fact-batch.schema.v3.json`) iff Hello/HelloAck includes `target-attribution-v2` |
| Candidate schema | `FactCandidateV1` unchanged (`additionalProperties: false`; no occupancy member) |
| Companion | `OccupancyCompanionV1` parallel array, associated only by `candidateOrdinal` **before fact2 exists** |
| Hello limits | No new `ProtocolLimitsV3` member. Companions bounded by existing 4096 and `len(candidates)` |
| Identity tokens | Unchanged four identity tokens. Attribution token is optional-negotiated, not required to spawn |

Mismatch: V3 payload without the token, or V2 payload with the token → `PROVIDER.PROTOCOL_VIOLATION`.

**Where the wrapper runs.** Inside the worker, before FactBatch emit, while compiler-native resolution is still in memory. It writes opaque `SubjectIdV1` into the candidate payload **and** `OccupancyCompanionV1` into the same batch. It does not run after host mint.

Companion MUST NOT carry `planId`, `sourceFactId`, or `producerClosure`.

## 3. Owning host entry (not caller-scalar admission)

`bind_worker_occupancy` is the complete host-adapter entry.

**Trusted host observations / preconditions:** negotiated Hello tokens; retained Plan locator; execution-plan stage row + stage spec `producerClosure`; closure kind map; selected views; mint map `candidateOrdinal → fact2` verified against this batch’s candidates; inventories; enumeration plan.

**Provider claims (rederived):** companion occupancy fields; candidate relation/resolution/universes/payload `targetNativeId`.

**Host-filled mechanical projection** onto `TargetAttributionV2`: `planId` from retained Plan; `sourceFactId` from the mint of that ordinal; `producerClosure` from the stage spec of `batch.stageOrdinal`; `targetUniverse` from the minted fact; occupancy fields copied from the companion. The fact MUST be a member of a selected view of that producer. `kind=provider` is rederived from retained closures.

Caller equality of envelope fields to scalar args is **not** complete admission (`PROVIDER_RETURN_OWNERS_REQUIRED` / `PROVIDER_RETURN_UNBOUND_ENVELOPE`).

## 4. Origin boundary (measured probe)

COMPLETE58 `admit_provider_attribution_return(envelope, origin=provider-return|host-internal)` admitted the same valid envelope both times and captured the same digest. That authorized host-authored bytes as provider attestation.

**Reconciled meaning.** `origin` is the evaluator-fault observation field recorded **after** a refusal. It is not an admit parameter that blesses identical bytes.

| Call | Result |
|---|---|
| `origin=host-internal` + caller envelope | `PROVIDER_RETURN_HOST_AUTHORED`; **no capture** |
| `origin=provider-return` + caller envelope, no worker batch | `PROVIDER_RETURN_UNBOUND_ENVELOPE`; **no capture** |
| Worker `FactBatchV3` companions + retained owners | project + capture as provider attestation |

The origin probe is not a full Run and does not claim a malicious host TCB can be proven honest.

Public routes stay existing: provider schema/join → `EVALUATION.INPUT_REFUSED`; host-authored → `HOST.INVARIANT_VIOLATED`. No new D9 codes. LIVE D9 not discharged.

## 5. Controls (not a full-suite Run)

`check-provider-attribution-return.v2.py` **21/21 pass**, failed 0, `fullRun: false`.

Honest first failure of this turn’s development: schema `x-opensip-order: {by: candidateOrdinal}` cannot utf-8-encode integers; order moved to admission. Final suite first failure: **none**.

Executed: worker→mint→bind→capture positive file first-party; unnegotiated omit; unnegotiated V3 refuse; empty companions; unknown ordinal; payload native-id mismatch; fact not in view; stage not in execution-plan; evaluator closure; C15 from worker companion; malformed companion; host-internal no capture; unbound envelope; origin probe both refuse; scalar args without owners; public routes; internal keys not DomainDetailCode; LIVE D9; partial omit; refused batch captures nothing.

Launcher: proposed `run-evaluator3-checks.py` adds job `provider-attribution-return`. Pinning an unused checker is not the proposal.

Query-projection / full evaluator3 suite / native-cases corpus were **not** re-run this turn (proposed overlay only). No fake qualification.

## 6. Historical COMPLETE58

Preserved at `/tmp/opensip-design-corrections/grok-target-provider-return-author.v1/output/provider-return-correction.md` (and `.json`). Statements that “no wire extension is necessary” and that origin is an admit blessing are historical and incorrect as delivery. C15 identity-conflict guard in `atom_model` remains selected.

## 7. Proposed paths and hashes

Isolated proposed root: `.../output/proposed/`.

### New

| Path | bytes | sha256 |
|---|---|---|
| `docs/coop/design-corrections/native/occupancy-companion.schema.v1.json` | 5580 | `ac54a081669c6059899e18c4adc2fc4fa1a36f1b6f66d8d9c0500884961e31ca` |
| `docs/coop/design-corrections/native/fact-batch.schema.v3.json` | 5382 | `3b762589a7e2f8466d039d433a7baf00d1a4ea5fb7524e650652f81ae2b58f7c` |

### Changed (selected)

| Path | bytes | sha256 |
|---|---|---|
| `docs/coop/design-corrections/foundation/provider_attribution_return_model.v2.py` | 13269 | `02aaff6dc8fab83f722b0f53dd1ecf3dae2af545e4adb5cfacd7c392f2826fdd` |
| `docs/coop/design-corrections/foundation/check-provider-attribution-return.v2.py` | 17522 | `693b385ea181b06bba52d0302f75f2b32cf484c45924d8d784abf1e1d976ccb4` |
| `docs/coop/design-corrections/foundation/provider-target-attribution-return.schema.v2.json` | 18551 | `2cc28d5125c224d5fe630fe75121a9653ec9f95306291172ee141465e48d32ad` |
| `docs/coop/design-corrections/foundation/run-evaluator3-checks.py` | 3435 | `c68a9ce9605d777bd2a0066ac14aa2da4e6e471ddb65d5bf98ce03035f5ef60c` |
| `docs/v2/contracts/product-v1/native-evidence.md` | 269728 | `66b3304fa22829e2760317ba95edb609ff111992354e39dd487dbf0c09d4790f` |
| `docs/coop/design-corrections/native/native-evidence.schemas.v2.json` | 230207 | `d8e9a1fcaa980ef397eb9f3c6b294a546783c4155fd924d0a1290eef1de71728` |
| `docs/coop/design-corrections/native/native_evidence_model.v2.py` | 286442 | `2b57bfc34af43fc40c611a19910f1da457913c1567805559ef4ea4b2ca6bcbf1` |

Full inventory: `proposed-hashes.json`. Patch: `provider58-to-e2e.patch`.

## 8. Remaining issues (not discharged)

- LIVE D9 successor-artifact.
- Source-pin / check-array-orders / whole-suite receipts after merge.
- Native-cases corpus does not yet drive live FactBatchV3 CBOR frames through `protocol3_run` payload validation (payload validation remains prose-owned beside the 34 rows, as §9.2 already states). Reference bind uses JSON-vector `canonicalRelationPayloadHex` as fact-plane already allows.
- P7 closure-kind patch still separate.
- Frozen24 not rewritten.
- No product implementation.

## 9. What this is not

Not acceptance. Not readiness. Not a sealed pin set. Not a full-suite Run. Not a protocol major bump. Not a new DomainDetailCode or D9 code. Not a silent FactCandidateV1/FactBatchV2 field.
