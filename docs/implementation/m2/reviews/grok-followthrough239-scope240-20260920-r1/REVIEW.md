# Independent follow-through — 239 r2 F1 primary relocation and 240 source-law corrections

**Standing:** paired owner reconciliation on frozen 239 r2 bytes plus labelled assessment of four root corrections to the archived 240 proposal. **Not** cumulative protocol approval, source/runtime selection, native custody, live census, command installation, or approval of unimplemented correction code. The archived 240 report and proposal were not edited. 238 r1 review is untouched. No repo/candidate/product edit.

Python 3.12.13 `-I -B`. Historical foundation/native/workflows/security/carrier/envelope/integration suites were **not** rerun; frozen r2 receipts were read and their pin/source bindings checked against candidate bytes.

---

## Part A — frozen primary 239 r2

### Archive and pins (verified before relying on extract)

| Archive | SHA256 | Bytes | Members |
|---|---|---|---|
| `trust-operation-integration-reference-wip-239-r2` | `822e3a9f…48c3` | 7058132 | 1486 |
| nested `trust-operation-budget-wip-238-r1` | `631d5402…5f0e` | 19420 | 34 |
| nested `trust-operation-budget-wip-238-r2` | `04a73688…872e` | 20908 | 52 |
| nested `producer-integration-reference-wip-237-r1` | `dca9a702…d050` | 4784556 | 1453 |

Pin, tar bytes/SHA, tar member count, `subject.json` file count, and every extracted member hash matched for all four archives (`allMembersRehashed: true`). Nested 237/238 extracts were used only as already-pinned siblings under `grok-out/repro/`.

`frozen-candidate.json` lists **1335** files (byte-equal to the extract). Versus historical `frozen-candidate-r1.json` (also 1335 paths): **exactly 7** SHA deltas, no added/removed paths:

1. `trust_operation_reference.py` `7959bfc2…0557` → `fad1a0a0…1295`
2. `trust-operation-budget.v1.md` `05612f15…58da` → `6aa20632…4f17`
3–7. five source-pin inventories (foundation, evaluator3, native, security, workflows)

`pin-changes-r2.json` has **14** explicit pin-row updates; every `after` hash matches the live candidate file. The six original 237 producer modules plus compiled schema still match `trust-operation-source-pins.v1.json` and the nested 237 candidate. Envelope r2 `sourceBindings` include the r2 primary (`fad1a0a0…1295`) and budget prose (`6aa20632…4f17`). `frozen-candidate-r1.json` / `integration-inputs-r1.json` / r1 receipts remain on disk as historical records. r2 `baseArchiveSha256` is the 239 r1 snapshot `d16e303d…9acd`; r1’s base remains 237 `dca9a702…d050`.

### 238 F1 tightening (closed on these bytes)

238 r1 `available()` returned `CAP` (4 MiB) on a cache hit. 238 r2 and the 239 r2 primary return `len(self.raw[key])`. Unknown first captures still receive `min(CAP, remaining)`. `capture` still requires `0 < len(raw) <= cap`.

Primary algorithm body from `CAP =` is **byte-identical** to 238 r2 `operation_work.py` (`2313cc97…2f03`). Only the PRIMARY/pin-load prefix differs. 239 r1 primary body from `CAP =` is byte-identical to `operation_work-before-known-cap.py` (`d9cc5957…b8e9`, the 238 r1 current source). Budget prose now states that a previously retained hash’s callback receives the known length, including at a full retained-byte budget.

Direct presence re-read on the primary at full byte budget (the F1 follow-through): four listed-path caps were **549, 551, 539, 19** — each equal to `len(raw)`, none 4 MiB, retained bytes unchanged. Over-return still refuses `operation-capture-cap` and latches `operation-budget-closed`.

### 46 cases / 9 unsafe variants (reproduced)

Redirected `check_operation.py` with `O` swapped to the 239 r2 primary:

- **46/46** cases equal frozen 238 r2 `operation-check-r3.json` and frozen 239 r2 `operation-check-r2/report.json`
- primary `sourceSha256` `fad1a0a0…1295`
- three known-presence follow-through cases present and equal:

| case | result |
|---|---|
| `known-presence-cap-exact-length-at-full-byte-budget` | `pass` |
| `known-presence-overreturn-refuses-cap` | `refuses:operation-capture-cap` |
| `known-presence-overreturn-closes-context` | `refuses:operation-budget-closed` |

Nine unsafe variants were rerun in a **fresh** 238 r2 work tree (frozen `operation-variants-r3/` was not overwritten). Core fields `variant` / `baseline` / `mutant` / `mutation` are equal to frozen r3; all nine **unsafe-admit** while baseline refuses. `sourceSha256` differs because the harness rewrites `PRIMARY` to the local 237 path (same harness-only delta as the 238 r1 review).

### Seven current root receipts (read, not rerun)

| Lane | Frozen r2 receipt |
|---|---|
| foundation | `PASS` 231/231 |
| native | `cases.total` 477, `passed` 477, `failed` 0; pins verified |
| workflows | 2193/2193, `failed: []` |
| security | `counts` 580/580, `sourcePinsValid: true` |
| carrier | 479/479 |
| integration | 1787/1787, `failed: []` |
| envelope | explicit 168, composition/drift 147, recorded differential 1803, actual replay crypto 55, fuzz 6000; `passed: true` |

All frozen r2 reports record `productQualification: false` (or equivalent standing). This follow-through does **not** treat those owner receipts as independent cryptographic or native qualification.

### Part A remaining (still open)

- 238 **F-2**: 237 default `Work()` is a separate unintegrated ledger; native still must construct one `Operation` and pass `input_work`.
- 238 **F-3** / 237: FULL graph, pending role effects, opaque metadata authentication, S4.5/safe-ABORT skip lists are not this module.
- Native capture allocation, live publication census, semantic/current trust/whole-image effects, and command/transport/outcome integration remain incomplete. 239 r2 does not add or relax a command/replay schema.

F1’s native remainder is now “callback gets known length, still must not over-allocate”; it is not a ledger double-count.

---

## Part B — four root corrections to the 240 proposal

Archived 240 `REVIEW.md` `69a15bf0…e030` and `proposed/INSTALLATION-MUTATION-SCOPE.v1.md` `4668c231…94e6` still match that directory’s `hashes.txt`. `review-origin.json` in that directory was rewritten in the original 240 session ~140s after `hashes.txt` (standing text only); this follow-through did not edit it. Probe bytes `2ef5a3d4…4951` are unchanged.

This section is **source-law vs new decision**, not approval of unimplemented records.

### 1. MutationReceiptV1 is not project-exclusive — **confirm**; correct 240’s project-only wording

**Source-law (confirmed on 239 r2 candidate schemas):**

- `MutationReceiptV1` has **no** `projectId` property. `additionalProperties: false`. Required: `schemaFamily`, `schemaMajor`, `receiptId`, `requestId`, `stepId`, `executionId`, `operation`, `idempotencyKey`, `effectOutcome`, `commitClass`, `replayed`.
- Identity is `receipt2:` + `H('workflow.mutation-receipt', this object without receiptId)` — the **complete** remaining object. `check_workflows.v1.py` computes exactly that set-difference, not a five-field subset.
- `operation` refs `MutationOperation`, whose enum **already** includes `trust-import`, `trust-refresh`, `trust-recovery-challenge`, `trust-recovery-import`, `install`, `update`, `core-*`, and `store-*`.
- `workflow.mutation-receipt` is the owning **mutation** receipt domain (`workflows-and-surfaces.md` §1), not a project-ledger type.

240’s wording that `MutationReceiptV1` is “the project mutation-receipt domain” and the speculative shortened preimage `{requestId,stepId,idempotencyKey,operation,effectOutcome}` are **too tight**. A shortened preimage is a **different** digest than the full recipe (probe: `d068dc77…ef46` vs `ab7bfbca…85b1`).

**New decision (not yet bytes):** embed the **original full** receipt in a typed `TrustCommandOutcomeV1` dependency prepared before D; that composition is not a project-ledger write. Agree this does not by itself write 228’s project evidence ledger.

**Four new enum entries:** `ceremony-begin` / `ceremony-commit` / `ceremony-abort` / `acknowledge-restore` (and the `trust-*` spellings) are **absent** from the current `MutationOperation` enum. Adding them needs an explicit current-owner successor of the closed enum, maps, and inventory. Existing receipt identities for already-enumerated operations do not change because those receipts’ bodies do not carry the new tokens.

**Counterexample if ignored:** minting `H('workflow.mutation-receipt', five-field sketch)` would not equal any lawful `receiptId` under the current recipe.

### 2. `replayed:false` original; do not mint INDETERMINATE after uncertain write — **confirm**, with one wording nuance

**Source-law:**

- Required `replayed` is boolean. Description: true when an equal idempotencyKey already had a COMPLETED receipt and no second effect was performed.
- `workflows-and-surfaces.md` §1: the original receipt is immutable; a replay delivery produces a **separately identified** receipt with the new request/attempt binding and `replayed=true`. Repair-apply checks keep the same `idempotencyKey` and `r2['replayed'] is True`.
- Capsule persistence / 222 restore: report success only after the file/parent barrier. Visibility/durability uncertainty **stops further effects** and is diagnosed by the ordinary capsule owner; it is not success, rollback, or permission to retry blindly. A repeat `acknowledge-restore` after uncertain visibility is a **new** declaration, not orphan replay.
- S4 write-ahead is a separate earlier capsule revision that **survives** later commit/import refusal. Clock-write, an orphan D, or an outcome node that was never published as the authorized final capsule cannot assert main-command COMPLETED.
- Pre-dispatch parse/custody/shape/time refusals retain the owner’s **no-write** result (`trust-state-continuity.v1.md` audit dispatch boundary).

**Nuance vs 240/root wording:** “projects true without rewriting original receipt/body/id” is right that the **original** bytes/id stay. The delivery artifact in current mutation-receipt law is a **new** receipt with `replayed=true`, not a field flip on the original. Do not collapse those.

**New decision applying that law:** a trust retained outcome may be COMPLETED or FAILED only when an ordinary **final outcome publication** is actually authorized. INDETERMINATE on `MutationReceiptV1` is a **schema-legal observation value**, not a license to publish an extra capsule/record/receipt merely to record uncertainty. Before-dispatch refusal may have **no** persisted command outcome.

240 tests 6–7 (“S4 write-ahead + refused ⇒ FAILED/INDETERMINATE receipt”; “uncertain replacement ⇒ mint INDETERMINATE”) over-publish. Replace them with: S4-ahead + later refusal is not COMPLETED; uncertain replacement is diagnosed without a new outcome publication; a later authorized attempt is a new requestId where 222 says so.

**Counterexample if ignored:** writing an INDETERMINATE `MutationReceiptV1` after an uncertain capsule replace would be a second retained publication “to record uncertainty,” which 222/persistence explicitly refuse (stop; diagnose; no automatic rollback; no success claim).

### 3. Same `workflow.mutation-intent` domain is lawful for a new closed shape; do not silently narrow the historical schema — **confirm** as identity fact; constructor change is still unimplemented

**Source-law:**

- Historical `MutationReplayScopeV1` is closed `{schemaVersion, requestId, stepId, projectId, operation}`, `additionalProperties: false`. Key = `H('workflow.mutation-intent', this complete record)`. Canonical identity is `opensip.product.v1 \0 domain \0 len(raw) \0 canonical(value)`.
- `mutation_replay_scope` / `mutation_replay_key` always validate that historical schema. `None` projectId ⇒ `CONFIG.INVALID` (still true for the four trust operations).
- Historical five-field `trust-import` **with** a syntactically valid ProjectId still **schema-admits** and the current constructor still **mints distinct keys** for two ProjectIds (probe keys `2dbc32c5…96b2` vs `a7e86df5…3386`). That is today’s gap, unchanged by 239.

**Identity fact (not a requirement to reuse the domain):** a proposed closed `{schemaVersion:1, kind:'installation', requestId, stepId, operation, store}` has a **different canonical preimage** than the five-field project record (probe lengths 230 vs 193 bytes; keys `f6ebec8f…5d2a` vs `2dbc32c5…96b2`). A hybrid with both `kind`/`store` and `projectId` is a third digest and **refuses** historical `MutationReplayScopeV1` (`CONFIG.INVALID`). An installation record against the historical schema also refuses. So a new H domain is **not required merely for record shape**. 240’s default `workflow.installation-mutation-intent` was a conservative labelled speculation, not a collision proof.

**New decisions:**

- Introduce `InstallationMutationReplayScopeV1` as an explicit new closed record.
- Reuse `H('workflow.mutation-intent', completeRecord)` **if and only if** current-command scope selection is explicit (host picks the constructor by command owner, never a caller flag). Historical validators stay on the five-field schema.
- **CURRENT** constructor/admission must refuse installation commands with a ProjectId. That change is **not present** on these bytes.
- Do **not** add `not: enum [trust-import, …]` (or otherwise drop those tokens) on historical `MutationReplayScopeV1.operation` and claim compatibility unchanged. `admissibleGenericFieldDomain` currently lists those four trust operations among 24. Narrowing that enum is a historical schema change.

**Counterexamples:**

1. Schema `not` on the four trust tokens would make today’s still-valid five-field `trust-import` scope fail historical validators. That is the silent-narrowing 240 recommended and root now rejects.
2. Constructor-only refusal leaves a leftover issuance hole: `validate_import_record(..., MutationReplayScopeV1, five-field-trust-import)` still admits. Acceptable only if every issuer is the constructor. If any other mint path exists, the hole remains.
3. A reader that hashes an unvalidated dict can still compute an installation key in this domain; it cannot **parse** it as `MutationReplayScopeV1`. Explicit selection is what prevents coercion, not the hash function.

### 4. Trust-only first; StoreBinding is exact S/G/K; lookup still unowned — **confirm**

**Source-law:** `StoreBinding` is closed `{storeInstanceId, storeGeneration, stateSchema}`. S7: the four SC-TRUST writes and `install`/`update` are fence-only, no project lock. S9.2: those four trust commands never recover/retire the transition slot. `InstallationTransitionJournalV1` owns the five executor protocol only. 228 guarded ledger is project evidence. 224 reserved-S / first creation is a separate owner. 222 `trust-command-restore.v1.md` is still unselected proposal for ceremony/acknowledge-restore commands.

**New decisions (agree, not implemented):**

- Initial trust-only correction must not claim executors / component install-update / first creation done.
- The admitted selected S/G/K is the binding in the installation key. Later store selection does **not** rebind an old request. Lookup by “current S only” is forbidden.
- Same-scope delivery requires the original binding **and** the original publication evidence under an explicit allowed lookup; otherwise **unavailable**, not a retry grant.

**Still unowned (do not invent public codes as a substitute):**

- Outcome lookup / retained-graph census for installation keys (no current index owner).
- Native one-`Operation` producer wiring (238 F-2).
- Ceremony/acknowledge-restore command inventory + transport (222 still unselected).
- Transition journal, component generation/selection, and 224 creation outcome owners (follow-through families).

**Counterexample if ignored:** after store-migrate, delivering a COMPLETED trust replay because “the installation’s current S” has some later capsule would ignore the StoreBinding that the proposed key includes and would treat a different physical store as the same effect.

---

## What 240 should change on the next frozen correction (not done here)

| 240 text | Correction |
|---|---|
| `MutationReceiptV1` is project-exclusive; shortened five-field receipt H | Full existing receipt body/recipe; no `projectId`; embed original receipt if a typed outcome is added |
| Default new H domain because historical records lack a discriminator | Disjoint canonical preimages are enough for collision; reuse is an identity-owner choice; new domain still allowed, not required |
| Exclude trust ops from historical `MutationReplayScopeV1.operation` via `not` | Keep historical schema; current constructor/admission refuses installation commands with ProjectId |
| Tests 6–7 persist FAILED/INDETERMINATE after S4-ahead refusal / uncertain replace | No extra outcome publication to record uncertainty; COMPLETED/FAILED only after authorized final publication |
| Lookup in “current store’s retained graph” | Exact original S/G/K + original publication evidence; else unavailable |

Do not invent top-level public error tokens. Reuse existing `CONFIG.INVALID` / `MUTATION_REPLAY_SCOPE_JOIN` until a registry owner lands a detail.

---

## Verdict

- [x] 239 r2 archive/pins/1335-file candidate/7 r1 deltas verified. Primary body from `CAP =` equals 238 r2. F1 cache-hit cap is `len(raw)`, demonstrated at full byte budget.
- [x] 46 cases and 9 unsafe variants reproduced against the primary. Three known-presence follow-through cases match frozen r2/r3.
- [x] Seven frozen r2 root receipts read as PASS with published counts; pin/source bindings for the r2 primary hold. Historical suites not rerun.
- [x] Root’s four 240 corrections are source-grounded as labelled above. 240’s project-only receipt wording and shortened identity sketch are withdrawn. Same-domain H is collision-free for the closed shapes. Historical schema must not be silently narrowed. INDETERMINATE must not be minted to paper over uncertain writes.
- [ ] Current constructor still admits `mutation_replay_scope(req, 0, syntheticProject, 'trust-import')`. That is the remaining 240 gap on **these** bytes.
- [ ] Not implementation approval of `InstallationMutationReplayScopeV1` / `TrustCommandOutcomeV1` / constructor refusal — those are the next frozen correction.
- [ ] Native/semantic/command/census limits remain open. This is not 238 F-2/F-3 closure and not 51-command integration.
