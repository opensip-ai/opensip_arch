# Installation mutation replay/outcome owner gap — diagnosis and labelled proposal

**Standing:** independent diagnosis plus explicitly labelled proposal assistance. Root remains
implementation owner. **Not** unimplemented-design approval, not a runtime vulnerability claim,
not command installation. 238 review untouched. No repo/candidate/product edit.

Probe reproduced 17/17 against the already-reviewed 237 candidate (`dca9a702…d050`). Frozen 240
archive `45ea1070…1c31` (6176 B, 5 members) verified before extract. README/probe/owners were
read **before** `ROOT-DIRECTION.md`.

---

## 1. Source-grounded diagnosis (confirmed owner gap)

This is an **owner/contract gap**, not a missed existing installation-scope persistence owner and
not a product-host exploit.

### What the sources actually require

- `InvocationRecord` (evaluator3) **does not require** `projectId`. The four trust commands
  therefore have shape-valid projectless invocations. Probe: four `shape-valid-only` rows.
- `MutationReplayScopeV1` (both invocation-record schemas) **requires**
  `{schemaVersion, requestId, stepId, projectId, operation}`. `workflows_model.v1.py`
  `mutation_replay_scope` / `mutation_replay_key` validate that closed record. v3 **inherits**
  those functions unchanged. `None` ⇒ `Refusal` `CONFIG.INVALID` for all 11 probed operations.
- Omitting `projectId` from an otherwise complete scope also refuses. Two syntactically valid
  `ProjectId`s for the same request/step/`trust-import` mint **distinct**
  `H("workflow.mutation-intent", …)` keys. That is the current namespace, not admitted custody.
- `command-inventory.v3.json` places `trust-import|refresh|recovery-challenge|recovery-import`,
  `install`, `update`, and the five S9.2 executors on generic `mutation` (+ `render`) steps.
- `repair.schema.json` `byCommandGenericMutationStep` maps those commands onto
  `MutationReplayScopeV1.operation` with `mintedByStepKind: mutation`.
- `workflows-and-surfaces.md` §1: generic mutation idempotence is exactly that five-field
  scope; a COMPLETED receipt permits delivery replay with no second effect; a key grants no
  authority.
- Security S7 lease table: `install`/`update` and the four SC-TRUST writes are **fence-only,
  no project lock**. “Trust recovery deliberately takes no project lease: it mutates SC-TRUST
  only.” S9.2 disposition row: those four trust commands never recover/retire the transition
  slot, never change the registry, never touch project stores.
- `trust-command-restore.v1.md` (unselected): ceremony begin/commit/abort and
  `acknowledge-restore` share that SC-TRUST fence-only law. Acknowledge-restore is **one**
  capsule publication, no second marker transaction; a repeat after uncertain visibility is a
  **new declaration** (222), not orphan replay. S4.5 keeps the existing
  `trust-recovery-challenge` / `trust-recovery-import` spellings.

### Search for a missed owner

Searched 237 for `InstallationReplayScope`, `InstallationScope`, installation-scoped
`mutation_replay_*`, and a trust-command receipt other than generic `MutationReceiptV1`.
**None.** SC-TRUST is a physical class. S7 fence is a lock. `InstallationTransitionJournalV1`
owns the **five executor** protocol (Phase A/B/C), not trust-import replay and not a
ProjectId substitute. 228’s guarded ledger is for **project** evidence export/restore.
Capsule `PublicationDescriptorV1` + `OperationInput.action` + role events record **private
publication**, not public-command completion (S4 write-ahead can persist on refusal; D may
be orphaned; successor forks/uncertain replacement are 222 law).

Filling `ProjectId` with a fake project, cwd, or a project created only to validate the
workflow schema would contradict S7 and would be a new product restriction (especially
before first project registration and during recovery). Nullable `projectId` on
`MutationReplayScopeV1` would change historical `workflow.mutation-intent` preimages for
**project** mutations — forbidden.

**Diagnosis:** generic mutation replay/receipt law is project-namespaced; several
installation-fence commands are registered as generic mutation steps anyway. Replay
namespace and durable outcome owner are both unnamed for those commands. Gap confirmed.

---

## 2. Assessment of root’s tentative direction

Root direction (not selected) is **mostly the right shape**. It should not be blessed as-is.

| Direction | Assessment |
|---|---|
| Keep generic `mutation` steps; split project vs installation **scope records** | Agree. Inventory already uses `mutation`+`render`. A dedicated `installation-mutation` step is a valid alternative but a larger grammar/result/registry change for the same one-invocation model. Mitigate host error by **excluding** installation operations from `MutationReplayScopeV1.operation`, so a synthetic ProjectId cannot mint a trust key. |
| Installation scope = discriminator + requestId + stepId + operation + StoreBinding(S,G,K); no ProjectId/path | Agree. `StoreBinding` already exists. After store-migrate, new invocations bind the new S; old keys stay on the old binding. |
| Same `workflow.mutation-intent` domain only if identity owner confirms | **Do not default to reuse.** Historical five-field records have no discriminator. Safer **speculative** default: new domain `workflow.installation-mutation-intent`. Reuse remains an identity-owner decision. |
| Capsule publication as sole atomic effect for the eight trust writes; outcome node referenced by D; receipt identity **before** D | Agree this avoids a hash cycle and a second transaction. D/action/role-events **alone** still must not imply COMPLETED (S4-ahead, refused roles, interrupted batch, uncertain replacement). |
| Embedding “original MutationReceiptV1 body” | **Too tight.** That type is the project mutation-receipt domain (`receipt2:` + `H(workflow.mutation-receipt, …)`). Prefer a **typed private** `TrustCommandOutcomeV1` in `records/H`, cited from D. Whether render parity still needs a `receipt2:` is unresolved — do not silently look it up in the project ledger. |
| Closed action↔command map; exclude bootstrap/creation/continuity/host-trust-admission | Agree; must be a closed table, not name-matching. |
| Transitions / install / update as mandatory follow-through, not capsule-owned | Agree. Trust capsule must not claim executable/store selection. |
| 228 project evidence stays project-scoped | Agree. |
| Reject if it creates an unowned lookup/census | Binding: outcome lookup is **in the admitted store’s retained graph under the fence**, not a new global index. |

---

## 3. Recommended correction (trust-only first)

**Keep generic mutation steps. Add a typed installation replay scope. Add a typed
trust-command outcome node whose publication is the capsule. Exclude installation
operations from the project scope schema.**

Concrete records, maps, crash/replay, and locks: `proposed/INSTALLATION-MUTATION-SCOPE.v1.md`
(proposal, not law).

### Dependency order (do not invent a blanket all-installation guarantee)

1. **Trust-only slice (this correction):** four existing SC-TRUST writes + three proposed
   ceremony leaves + `acknowledge-restore`. Schema/scope/outcome/map/tests below.
2. **Five S9.2 executors:** installation scope for **replay namespace**, but durable
   outcome remains intent+journal (Phase B vs Phase C). Separate PR. No trust-capsule claim.
3. **Component `install`/`update`:** generation/selection owner defines the terminal
   artifact. Separate PR.
4. **First creation / reserved S (224):** mint installation scope **after** S exists.
   Creation owner, not this trust slice.

Clock recovery commands stay in the trust-only slice with their existing S4.5 owners; they
are **not** ceremony.

---

## 4. Exact files/owners to change (trust-only)

| Owner | File | Change |
|---|---|---|
| workflows schema | `workflows/schemas/invocation-record.schema.json` and `evaluator3/` copy | Add `InstallationMutationReplayScopeV1`. `not` the eight trust operations on `MutationReplayScopeV1.operation`. |
| workflows schema | `workflows/schemas/repair.schema.json` and evaluator3 copy | Split `byCommandGenericMutationStep` trust rows to installation-scope recipe; publish the new key domain; keep project rows byte-stable. |
| workflows model | `workflows_model.v1.py` (v3 inherits) | `installation_mutation_replay_scope` / `_key` / join; refuse trust operations on the project builder. |
| workflows tests | `check_workflows.v1.py` | Existing “generic rows == mutation-step commands” controls must distinguish project vs installation scopes. |
| workflows inventory | `command-inventory.v3.json` | Ceremony + acknowledge-restore rows when those commands land; trust rows already `mutation`+`render`. |
| product contract | `workflows-and-surfaces.md` §1 | Installation-scope recipe beside the project one. |
| product contract | `security-and-lifecycle.md` S7/S9.2 | Cite installation scope; no project receipt. |
| security schema | `private-trust-state.schemas.v1.json` | `TrustCommandOutcomeV1`; optional `commandOutcome` on `PublicationDescriptorV1`. |
| security prose | `trust-command-restore.v1.md`, `trust-capsule-persistence.v1.md` | Bind outcome-before-D; uncertain ≠ COMPLETED; ack-restore = new declaration. |
| 232/236 | record reader / graph | Treat `commandOutcome` as a `NodeRef` edge when the descriptor schema successor lands. |
| CLI/API/MCP/locks | inventory + transports | No new lock class for trust (fence only). |
| public-detail registry | only if a new **detail** is added | No new top-level public error token. |

Do **not** rewrite project generic mutation, 228 evidence, or S4.5 domains.

### Bounded tests (trust-only)

1. `mutation_replay_scope(..., None, 'trust-import')` still refuses; **also** refuses with a
   synthetic ProjectId (new).
2. `installation_mutation_replay_scope` admits `{req, step, trust-import, StoreBinding}`;
   two StoreBindings ⇒ distinct keys; missing store refuses.
3. Project `baseline-adopt` scope bytes/key **unchanged** vs 237.
4. Outcome node canonicalizes without a descriptor digest; D may reference it; including D
   digest in the outcome must fail the closed schema.
5. COMPLETED delivery replay: same scope + same input + confirmed capsule ⇒ `replayed=true`,
   no second publication.
6. S4 write-ahead present + command refused ⇒ FAILED/INDETERMINATE, never COMPLETED.
7. Uncertain capsule replacement ⇒ INDETERMINATE; second `acknowledge-restore` is a new
   requestId.
8. `ordinary-import` D without outcome node does not authorize command COMPLETED.
9. `bootstrap`/`creation`/`continuity`/`host-trust-admission` rejected by the public-command map.
10. Fence-only: no project lease assertion in the trust-command lock test (existing S7 table).

---

## 5. Speculative vs existing law vs blockers

**Existing law:** optional invocation `projectId`; required project field on
`MutationReplayScopeV1`; fence-only SC-TRUST; COMPLETED delivery replay meaning; 222
new-declaration acknowledge-restore; S4-ahead ≠ command success; 228 project evidence
separation.

**Speculative (proposal):** new H domain; `TrustCommandOutcomeV1` shape; optional
`commandOutcome` on D; whether `MutationResult.receiptId` remains `receipt2:` for trust
steps.

**Unresolved blockers (do not fake):**

- Identity-owner decision on H domain reuse.
- Workflows vs security agreement on receipt2 vs outcome NodeRef for render `receipt-id`.
- 224 reserved-S for first creation (out of trust-only slice).
- Transition/component outcome artifacts (follow-through PRs).
- Native one-`Operation` context (238) is host wiring, not this scope key.

---

## Verdict

- [x] Gap is real; no overlooked installation replay/outcome owner in 237.
- [x] Root direction is a sound starting point if project scope bytes stay intact, installation
  operations are excluded from that schema, outcome identity is before D, and transitions are
  not stuffed into the trust capsule.
- [x] Trust-only correction is the safe first slice; remaining installation families are
  ordered, not promised.
- [ ] **Not implementation approval.** Fresh review is required on frozen correction bytes.
