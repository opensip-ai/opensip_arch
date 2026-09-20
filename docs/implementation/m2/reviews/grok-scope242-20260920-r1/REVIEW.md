# Independent review — current mutation scope and immutable joins 242 r1

**Standing:** bounded code review of frozen 242 r1 over pinned 239 r2 and 241 r1. **Not** cumulative approval, live host-issuer integration, 51-command completion, native custody, lookup, or durable effect. 241 reviewed bytes and the archived 239/240 follow-through were not edited.

Python 3.12.13 `-I -B`. Siblings reconstructed as `m2-trust-operation-integration-reference-239/candidate` (239 r2 `822e3a9f…48c3`) and `m2-installation-trust-outcome-draft-241` (241 r1 `393a4999…b447`).

---

## Verification

Frozen `current-mutation-scope-wip-242-r1`: **32404 B, 29 members, SHA256 `d43edfdd…f658`**. Pin, tar, member count, and every `subject.json` hash matched before extract; extract rehashed 29/29.

`inputs.json` 239 schema/canonical pins all match the sibling candidate (`canonical.py` `d47f25db…b442`). 241 `private-trust-state.schemas.v1.json` `1328ba16…4208` and `command-actions.json` `c43fb596…1fb4` match both the 242 pin and the archived 241 extract.

`mutation_scope_reference.py` imports only stdlib + `referencing` / `jsonschema` and loads `foundation/canonical.py` by file. No security-module or `workflows_model` import (no cycle). Composition tests load 241 separately.

---

## What this adapter is

Closed **24-route** current command map (`current-command-scope-map.json`): **15 installation** (exact original StoreBinding S/G/K, no ProjectId) and **9 project** (historical five-field `MutationReplayScopeV1`, no store). Callers do not choose a scope kind. `current_key` validates the **owner-specific** shape and operation, then `H('workflow.mutation-intent', complete scope)`.

Prospective schemas use **new URIs** (`urn:opensip:proposal242:{invocation,repair,command-names,installation-scope}`). Historical `MutationReplayScopeV1.operation` still `$ref`s `urn:opensip:product-v1:workflows:evaluator3:repair:2#/$defs/MutationOperation`. Current name list is **49** (historical 45 + four ceremony/restore tokens). That is not 49 inventory rows or 51-command completion. Current repair enum is **28** (24 historical MutationOperation + 4 new).

`bind_step` is a **join**: current vs retained invocation parse, immutable projection equality, builtin command/request/step/params/key vs original scope and host context. Success standing `immutable-scope-binding-only` with four pending owners (transport/authorization, DAG/operation-input, original-evidence lookup, effect/durable outcome). No replay token.

---

## Reproduction

| Corpus | Result |
|---|---|
| `check_scope.py` | **116/116** byte-equal to frozen `scope-check-r2.json` (r1 file hash identical; r2 is the same 116) |
| `check_composition.py` | **15/15** equal frozen `composition-r2.json` (10 trust command/action receipts + historical registry/domain/map controls) |
| `check_variants.py` | **5/5** guard-deletion controls; core fields equal frozen r1. `sourceSha256` differs (harness rewrites `S=Path(...)`) |

Variants admit incorrect bindings where baseline refuses: immutable projection, command name, installation `projectId`, original-store rebind, params/key join.

`check_scope-before-main-guard.py` still prints at import; `composition-r1.stdout` retains that extra report. r2 composition uses `check_scope.py`'s `__main__` guard only. No behavioral test was relaxed.

---

## Independent probes

| Probe | Result |
|---|---|
| `current_key('trust-import', five-field project scope)` | `CONFIG.INVALID` — standalone current key admission, not merely a constructor wrapper |
| Historical URI still admits that five-field trust-import scope | admitted (old data readable) |
| Current installation scope + key for `trust-ceremony-begin` | admitted |
| Historical URI + `operation: trust-ceremony-begin` | `CONFIG.INVALID` (domain did not grow) |
| New `$id`s vs historical invocation `$id` | five distinct URIs; historical registry resources unshadowed |
| Same request after selected-store S/G/K change | `original-scope-binding` |
| Wrong host command `analyze` | `command-without-generic-mutation-owner` |
| Wrong project context on `purge` | `original-scope-binding` |
| Extra param `force=True` even on both current and retained | `CONFIG.INVALID` |
| Caller echo (`retained_raw is current_raw`) | structurally binds — **not custody** |
| Ill-typed appended `stepResults` | `CONFIG.INVALID` at parse (valid append is claimed via `immutable()`; the 116 do not include a golden StepResult append) |
| `install` current installation scope | admitted; **not** a 241 trust action |

Historical project keys for the 11 old installation operation tokens remain schema-readable under the old URI; current issuer selection still refuses them as current keys (`no-project-key-issuer-*` in the 116).

---

## Map / schema consistency

- Routes = historical `byCommandGenericMutationStep` keys plus four new trust commands (24).
- Installation enum on `CurrentInstallationMutationReplayScopeV1` = the 15 installation route operations (eight trust + `install`/`update` + five executors). That is **wider than 241’s eight-command** `InstallationMutationReplayScopeV1`. 242 may mint installation keys for `install`/`update`/executors; 241 still cannot prepare `TrustCommandOutcomeV1` for them. Declared remaining: those families keep distinct outcome owners. Do not compose a 242 `install` key as a 241 trust outcome.
- `store-gc` is the only lifecycle `mutation`+`render` inventory command left on **project** in this map (see below).
- Current `MutationParams.mutationClass` points at the new repair URI; copied `MutationReplayScopeV1` still points at the **old** repair URI. Byte-equal to historical scope JSON.

---

## store-gc — against the per-namespace sweep owner, not lifecycle class

242 currently maps `store-gc` → `{operation: store-gc, scope: project}` and admits a five-field project key (`9721cafe…473e`). Installation store context is refused (`project-store-context-forbidden`). README/request treat this as **pending**, not settled.

**Existing law used (not requestClass, not “installation ⇒ fence-only”):**

- Inventory: `owner: security`, `authorizationClass: exclusive-lease`, `writesTrackedIntent: false`, steps `mutation`+`render`. `requestClass: lifecycle` is a surface class only.
- **S7 lease table:** `store gc` is **EXCLUSIVE (one namespace), per namespace, busy = retain**. It is **not** in the fence-only / no-project-lock row (that row is install/update/trust/doctor/store-status). It is **not** in the core-transition lock set (five executors).
- **S7 GC law:** “GC iterates registered namespaces and treats a busy namespace as retain, never as refusal.” Namespaces are the host registry `ProjectId ↔ namespace locator`.
- **S9.2:** `store-gc` is a nonexecuting-mutator, not an intent-writing transition executor.
- **commit-recovery-readonly.v3.md §4** (authorized settlement sweep, selected prospective expansion of `store-gc`): install fence at level 0, then `EXCLUSIVE` `LOCK_EX|LOCK_NB` on the **affected project namespace**; busy → skip and retain; if no write, **continue to the next namespace**; writes `committed`/`refused` on that namespace’s attempt-custody row only; no reuse of dead-attempt authority.
- **carrier-migration.v1.md:** same custody sentence for an additional per-namespace maintenance step under this command.

**Definite (not a 242 implementation bug, a mapping that cannot be law yet):**

1. `store-gc` is **not** fence-only SC-TRUST and must not ride `TrustCommandOutcomeV1`.
2. `store-gc` is **not** an S9.2 executor and must not ride `InstallationTransitionJournalV1`.
3. A **single** `MutationReplayScopeV1` ProjectId cannot be the replay namespace for a command whose specified effect is **iterate registered namespaces, skip/retain busy, continue**. One-project COMPLETED would mean the wrong thing.
4. `requestClass: lifecycle` does not choose project vs installation vs a third owner.

**Missing explicit law:** whether the **public builtin** is one installation-wide invocation that performs that loop, or a host-scheduled per-namespace invocation. Inventory (one command, one `receipt-id` parity field) plus “GC iterates” / “next namespace” lean toward one invocation; they do not publish a sweep journal or a per-namespace child receipt recipe.

**Labelled proposal (not selected):** keep 242’s project mapping only as an explicit **unsettled placeholder**. Do **not** add `not: store-gc` to historical `MutationReplayScopeV1`. Do **not** move `store-gc` onto 241 trust outcomes or onto the 15-name installation enum as if that made it fence-only. Give it a **distinct sweep/outcome owner**: installation-fence command whose atomic public effect is a per-namespace EXCLUSIVE skip/retain pass over the registered set at the admitted store binding, with an explicit namespace journal (swept / skipped-busy / not-written). Replay identity for that owner is not one ProjectId and not SC-TRUST capsule completion.

---

## Remaining (do not count closed)

No actual current host issuer calls `bind_step` / `current_key`. Original retained bytes/scope remain trusted inputs; caller echo still structurally binds. `bind_step` is not DAG admission, operation-input capture, authorization, lookup, or publication. 241 receipt/outcome/descriptor binding is a separate compose. Components, five executors, first creation, and `store-gc` still need their own final outcome owners. Two evidence commands remain unowned (`evidence-restore` refuses `command-without-generic-mutation-owner`). Native one-`Operation` wiring remains 238 F-2.

---

## Verdict

- [x] Archive/pins/new-URI isolation verified. 116 scope checks, 15 composition cases, 5 guard-deletion variants reproduced.
- [x] Standalone `current_key` rejects project-based trust scopes (`CONFIG.INVALID`). Historical tokens/domain unchanged; four new tokens admitted only on current URIs/installation scope.
- [x] Immutable join refuses coherent command/project/store/params rewrites; extra fields refuse; bool `stepId` refuses. Success is join-only.
- [x] `store-gc`: existing sweep/GC law is per-namespace EXCLUSIVE under the install fence with busy skip/retain. 242’s project mapping is an incomplete placeholder, not a definite correct choice and not a silent historical-schema `not`. Distinct owner recommended, labelled proposal.
- [ ] **Not** host-issuer integration, 51-command completion, or outcome/publication approval.
