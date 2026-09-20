# Independent review — installation scope and prepared trust outcome 241 r1

**Standing:** bounded code review of frozen 241 r1 over pinned 239 r2. **Not** cumulative protocol approval, source/runtime selection, native custody, live census, command installation, or 51-command admission. The archived 239/240 follow-through and 240 proposal were not edited. No repo/candidate/product edit.

Python 3.12.13 `-I -B`. Sibling `m2-trust-operation-integration-reference-239/candidate` reconstructed from already-verified 239 r2 `822e3a9f…48c3` (primary `trust_operation_reference.py` still `fad1a0a0…1295`).

---

## Verification

Frozen `installation-trust-outcome-wip-241-r1` pin, tar, and every `subject.json` member matched **before** extract: **30244 B, 26 members, SHA256 `393a4999…b447`**. Extract rehashed 26/26.

`inputs.json` eight 239 pins all match the sibling candidate (schema `a3a0b4f4…8520`, record `f149dc4a…fd02`, graph `9dba2150…0954`, operation `fad1a0a0…1295`, evaluator3 repair/common, workflows v1/v3).

Local graph relocation: `graph_reader.py` algorithm from `class Refusal` is **byte-identical** to 239 `trust_graph_reference.py`. Only the reader path/PIN prefix changes (`record_reader.py` `0cf23615…062c`).

Compiled local schema: **125 `$defs`** (121 inherited JSON-equal, `PublicationDescriptorV1` gains optional `commandOutcome` NodeRef not in `required`, three new defs). Reader **134** registry sites (132 previous + `PublicationDescriptorV1.commandOutcome` → `TrustCommandOutcomeV1` and `TrustCommandOutcomeV1.operation` → `OperationInputV1`). `TrustCommandOutcomeV1` is a new `ROOTS` member.

---

## What this slice actually is

`outcome_reference.py` is a **prepared-data constructor**. `effect_outcome` is an asserted owner decision. Successful `bind_outcome` / `bind_descriptor` return `standing: prepared-bindings-only` plus three pending owners:

- `requested-effect-semantics`
- `final-publication-census-and-durability`
- `current-admission-and-original-scope-lookup`

They never return a replay-permission token. That matches ROOT-DISPOSITION and the 239/240 replay nuance: this slice prepares **originals only** (`replayed` const `false`); a later delivery replay must mint a **separately identified** receipt with `replayed=true` and a new attempt binding.

Installation keys reuse `H('workflow.mutation-intent', complete scope)`. Closed shape `{schemaVersion:1, kind:'installation', requestId, stepId, operation, store}` excludes ProjectId and ExecutionId. Historical `MutationReplayScopeV1` bytes/schema are untouched.

---

## Reproduction

| Corpus | Result |
|---|---|
| `check_outcome.py` | **84/84** byte-equal to frozen `outcome-check-r3.json`; source SHA `77a74d3f…b2fb` |
| `check_variants.py` | **5/5** guard-deletion controls; core fields equal frozen r1. `sourceSha256` differs because the harness rewrites `S=Path(...)` to the local work path |

The five controls admit incorrect bindings where baseline refuses: project-scope bypass, outcome-store, receipt-identity, receipt-executionId, descriptor-outcome bytes. They are binding controls, not effect authority.

r1=80 / r2=82 / r3=84 retained on disk; this review reproduced r3 only.

---

## Prepared-only boundary (honest)

Concrete counterexamples, all on these bytes:

1. **Asserted COMPLETED ≠ standing.** `prepare_outcome(..., 'COMPLETED')` then `bind_descriptor` against a descriptor whose `afterProjection` roles are still `ST-UNBOOTSTRAPPED` and clock `unevaluated` returns `prepared-bindings-only`, the three pending owners, and no replay permission.
2. **`bind_outcome` is not a graph/census.** The same ordinary-import outcome binds while the payload `input.ref` bytes are absent. A structural `graph.walk` of that outcome refuses `missing-object`.
3. **`bind_descriptor` does not load events.** Fixture `EventRef`s are dangling (`sha256='c'*64`). `bind_descriptor` still succeeds. Walking that publication refuses `missing-object`.
4. **Graph does not call `bind_outcome`.** Walking a `kind:none` clock-recovery-challenge outcome visits `TrustCommandOutcomeV1` then `OperationInputV1` (2 objects / 2 edges) with standing `structural-full-dependencies-only`.
5. **`bind_params` is class/key join only.** Extra field `garbage=True` still returns `scope-key-binding-only`. Public `MutationParams` (`additionalProperties: false`) would refuse.
6. **INDETERMINATE cannot be prepared.** `prepare_outcome(..., 'INDETERMINATE')` refuses `shape:TrustCommandOutcomeV1`. Original `replayed=true` likewise refuses. No extra publication is introduced to record uncertainty.
7. **Orphan D is not completion.** `bind_descriptor` without `commandOutcome` refuses `command-outcome-missing`. Old descriptors remain structurally valid because `commandOutcome` is optional.

Do **not** count those pending owners as closed.

---

## Independent probes (cross-rewrite, historical wrapper, enum)

| Probe | Result |
|---|---|
| Coherent store rewrite (new S/G, recomputed key+receiptId, original operation bytes) | `outcome-store-binding` |
| Coherent executionId rewrite (recomputed receiptId) | `receipt-invocation-binding` |
| Coherent operation rewrite to `trust-refresh` keeping import bytes | `command-action-binding` |
| Same rewrite plus retargeted outcome.operation ref vs import bytes | `outcome-operation-bytes` |
| Wrong action (`refresh` as `trust-import`) | `command-action-binding` |
| Canonical prepare round-trip | `C.canonical(parse(out)) == out` |
| Extra outcome field `command` | `shape:TrustCommandOutcomeV1` |
| Shortened five-field receipt | already in 84: `shape:TrustCommandOutcomeV1` |
| Historical `W.mutation_replay_scope(req, 0, syntheticProject, 'trust-import')` | **still admits** (key `48863ea4…527d`) |
| `current_project_scope` for the same | `installation-scope-required` |
| `current_project_scope` for `baseline-adopt` | byte-equal to historical project scope/key (in 84) |
| `installation_scope(..., 'install', ...)` | `shape:InstallationMutationReplayScopeV1` (enum is the eight trust commands only) |
| Ceremony receipt as public `MutationReceiptV1` | `CONFIG.INVALID` (`trust-ceremony-begin` not in `MutationOperation`) |
| Ceremony params as public `MutationParams` | `CONFIG.INVALID` |
| Four new tokens in `MutationOperation` | **absent** |

`current_project_scope` denies the documented **15** operations (eight trust commands + `install`/`update` + five executors). It is **not** wired into `W.mutation_replay_scope`. A constructor wrapper alone is not current-command admission. Declared remaining; confirmed.

---

## Missing literal binding / confusing ownership (fix before integration)

These are not silent ledger holes in the prepared API. They **will** be misread as admission if the next owner skips the pending list.

1. **Issuer wiring.** Historical project constructor still mints `trust-import` keys with a synthetic ProjectId. `current_project_scope` refuses, but nothing in 239 workflows calls it. Integration must select installation vs project scope at **every** current issuer, including imported invocation admission.
2. **Public enum successor.** `TrustMutationReceiptV1.operation` / installation-scope enum include `trust-ceremony-begin|commit|abort` and `trust-acknowledge-restore`. Those tokens are not in `MutationOperation` / `MutationParams.mutationClass` / public `MutationReceiptV1`. `prepare_outcome` can mint them; public receipt/params validation cannot. Do not ship those four commands until the workflow/inventory successor lands. Existing four trust receipts **do** validate as public `MutationReceiptV1` (all eleven required fields, complete-body `receipt2:` identity, `replayed=false`).
3. **Fifteen-deny vs eight-enum.** `INSTALLATION_OPERATIONS` is a project-constructor deny list of 15 names. `InstallationMutationReplayScopeV1.operation` is only the eight trust commands. `install`/`update`/executors are correctly left without a trust outcome, but the name “installation operations” can be read as “these fifteen have installation keys.” They do not.
4. **`bind_*` vs graph.** Do not compose `bind_outcome`/`bind_descriptor` success with `graph.walk` as one admission. The former does not load payload/event bytes; the latter does not call bind and does not interpret `effectOutcome`.
5. **Standalone graph `Work()`.** Traversal uses the 236-style local ledger, not 238 `Operation`. Native one-context wiring remains F-2.
6. **`store-gc`.** Not in the 15-deny list. `current_project_scope(..., 'store-gc')` still admits a project-scoped key (`a9e8682f…9730`). S7’s fence-only row lists install/update/trust, not `store-gc` (exclusive-lease / install-fence namespace sweep). Not a trust-slice regression; still a leftover project-constructor path for a lifecycle command. Do not silently add it to the historical schema `not` list.

No new public top-level/detail codes are introduced here. Do not invent them as shortcuts.

---

## Source-law vs new decision

| Item | Label |
|---|---|
| Full 11-field receipt identity `receipt2:` + H(complete body without receiptId) | source-law (preserved) |
| `workflow.mutation-receipt` not project-exclusive | source-law |
| Historical five-field `MutationReplayScopeV1` unchanged | source-law |
| Disjoint installation preimages may reuse `workflow.mutation-intent` | identity fact (confirmed) |
| Original `replayed=false`; replay delivery is a **new** receipt | source-law (241 prepares originals only) |
| INDETERMINATE / uncertain write is not a new outcome publication | source-law applied |
| S4 write-ahead / orphan D / outcome node alone ≠ command COMPLETED | source-law; 241 does not claim otherwise |
| Exact original S/G/K in the scope; no current-S rebind | new decision, encoded |
| `TrustCommandOutcomeV1` + optional `commandOutcome` | new proposal (unselected) |
| `current_project_scope` wrapper | new decision, **unintegrated** |
| Four new operation tokens | new proposal; public successor owed |
| Trust-only first; executors/install/update/creation separate | source-law / 240 order, unchanged |

---

## Remaining (do not count closed)

Current scope selection across issuers; immutable StepSpec/intent binding; 51-command inventory and transports; public result/receipt projection; separately identified replay delivery; original-scope lookup/census; requested-effect semantics; final publication durability; native host actor and one shared 238 `Operation`. Component install/update, five transition executors, first creation, and `store-gc` need their own outcome owners.

---

## Verdict

- [x] Archive/pins/125 defs/134 sites/graph algorithm verified. 84 checks and 5 guard-deletion controls reproduced.
- [x] Prepared-only boundary is honest: asserted `effectOutcome`, join-only `bind_params`, orphan D is not completion, graph is structural and does not call `bind_outcome`, no issuer wiring, no durability/lookup proof.
- [x] Cross-store / execution / operation / receipt rewriting is refused when the original operation bytes are held fixed. Historical project schema/keys remain. Four new tokens are not public `MutationOperation`.
- [x] Confusing ownership to fix **before integration**: wire `current_project_scope` into every issuer; land the public enum successor before ceremony/acknowledge-restore commands; do not treat `bind_*` success as census or completion; keep the 15-deny list distinct from the eight-command trust enum.
- [ ] **Not** implementation approval, source selection, or command installation. Fresh review is required on the next frozen issuer/inventory/lookup bytes.
