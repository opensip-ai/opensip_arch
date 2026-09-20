# Independent review — installation output 244 r1 and 242 r2 GC fail-closed

**Standing:** bounded code review of frozen 244 r1 plus 242 r2 follow-through. **Not** cumulative approval, product output/command issuer integration, native custody, lookup, durability, or a finished GC implementation. Archived 242 r1 / 243 reports were not edited.

Python 3.12.13 `-I -B`. Sibling trees reconstructed from verified 239 r2 (`822e3a9f…48c3`) and 241 r1 (`393a4999…b447`). Copied variant dirs were renamed/omitted so frozen artifacts were not overwritten.

---

## Verification

| Archive | SHA256 | Bytes | Members |
|---|---|---|---|
| `installation-output-wip-244-r1` | `0dabe53d…828e` | 13040 | 22 |
| `current-mutation-scope-wip-242-r2` | `4b649237…6188` | 34468 | 53 |

Pin, tar, member count, and every `subject.json` hash matched before extract; both extracts rehashed in full.

244 `inputs.json` pins 242 r2 module/map/schemas (`mutation_scope_reference.py` `3ff84c3f…bc62`, map `af719206…c48e`) and historical envelope `37498354…3027f`. Those hashes match the reconstructed siblings.

242 r2 `before-r1/` is byte-identical to frozen 242 r1 for `mutation_scope_reference.py` and `current-command-scope-map.json`. Current invocation/repair/installation-scope schemas are **unchanged** vs r1.

---

## Part A — 242 r2 GC fail-closed

Map is **24 routes = 15 installation + 8 project + 1 unowned-sweep**. `store-gc` is `{operation: store-gc, scope: unowned-sweep}` with an explicit `unownedCommands` note: no one-ProjectId key, no lock-class inference, no cross-namespace atomicity.

Both `scope_for_command` and standalone `current_key` refuse unless `scope` is `installation` or `project` (`mutation-scope-owner-unavailable`). Historical `MutationReplayScopeV1` still **admits** a five-field `store-gc` project record under the old URI. No historical schema/`not` list/token/key preimage was narrowed.

### Reproduction

| Corpus | Result |
|---|---|
| `check_scope.py` | **120/120** equal frozen `scope-check-r3.json` |
| `check_composition.py` | **15/15** equal frozen `composition-r3.json` |
| `check_variants.py` | **5/5** core fields equal frozen `scope-variants-r2` |

New vs r1: three GC issuance refusals + historical GC readability; schema-valid appended `StepResult`/`termination` golden (immutable request preserved, standing still join-only); malformed appended result refuses. Variant `sourceSha256` differs (harness path rewrite).

### Independent GC probes

| Probe | Result |
|---|---|
| `scope_for_command(..., project_id)` | `mutation-scope-owner-unavailable` |
| `scope_for_command(..., store=S/G/K)` | `mutation-scope-owner-unavailable` |
| `current_key('store-gc', historical project scope)` | `mutation-scope-owner-unavailable` |
| `current_key('store-gc', installation-shaped record)` | `mutation-scope-owner-unavailable` (owner check before URI validate) |
| Historical URI five-field `store-gc` | still admitted |
| `parse_invocation` of a `store-gc` builtin invocation | admitted (name remains in the 49-name list) |
| `bind_step` of that invocation | `mutation-scope-owner-unavailable` |

Imported/current invocation bytes **cannot** mint a current key. Parse of a named `store-gc` request is still possible; issuance is fail-closed. That is a visible incomplete command, not finished GC.

**Law (unchanged from 242 r1 review, now encoded):** S7 iterates registered namespaces with nonblocking EXCLUSIVE under the install fence, busy skip/retain. A future owner must record **partial/pass** per namespace. Completed writes may remain if a later namespace is busy/fails. Scope kind must not select lock class. No SC-TRUST capsule or transition journal.

---

## Part B — 244 r1 installation output profile

Historical `CommandEnvelope` `kind=mutation` still requires `projectId`. Installation-only output cannot lawfully emit on that URI without a fake project. 244 uses a **distinct** URI `urn:opensip:proposal244:command-envelope` that `$ref`s 242 current repair/invocation/installation-scope resources.

- Installation operations (the same 15): envelope **forbids** `projectId`/`projectRoot`; `MutationReceiptProjection.replayScope` is required and is `CurrentInstallationMutationReplayScopeV1` (original S/G/K).
- Project operations: **require** `projectId`, **forbid** `replayScope`.
- Historical registry unshadowed. Existing **8** project-route outputs validate the original envelope schema; installation outputs refuse that old URI.

`prepare_projection` checks full current `MutationReceiptV1`, complete `receipt2:` identity, command/scope/key and request/step joins, then the five projection fields plus owner context. `validate` now also enforces the fixed termination/exit table (r1 omission).

### Reproduction and beforeimages

| Corpus | Result |
|---|---|
| `check_output.py` | **79/79** equal frozen `output-check-r3.json` (source `de40f007…30ce`) |
| `check_variants.py` | **4/4** identity/key/request/exit omission controls |

- **r1:** `output_reference-before-exit-join.py` has no exit join; `output-check-r1.stderr` is `AssertionError: ('admitted', 'termination-exit-mismatch')`. Current `validate` requires the table. Schema was not relaxed.
- **r2:** `check_output-before-failure-detail.py` used `errors: []`; `output-check-r2.stderr` is jsonschema `minItems` on `errors`. Current fixture has a real `CONFIG.INVALID` detail. Schema was not relaxed to accept the empty array.

### Independent output probes

| Probe | Result |
|---|---|
| New token `trust-ceremony-begin` projection | `prepared-output-only`, has `replayScope`, no `projectId` |
| Same envelope on historical URI | `CONFIG.INVALID` |
| Fake `project_id` on installation prepare | `installation-project-context-forbidden` (in 79) |
| Coherent receipt/store/operation rewrites | refuse identity/scope/join (in 79) |
| Flip `replayed` keeping original `receiptId` | `receipt-identity` |
| Separately identified replay (`new ExecutionId`, `replayed=true`, new id) | formats; pending still 3; **not** replay authority |
| COMPLETED effect + `operational-failed` / exit 4 | formats; effect stays COMPLETED |
| Pre-dispatch failure envelope, no receipt | validates |
| `prepare_projection('store-gc', ...)` | `mutation-scope-owner-unavailable` |

Standing is `prepared-output-only` with pending `receipt-and-effect-authority`, `original-scope-custody-and-lookup`, `publication-and-delivery-authority`. Asserted COMPLETED is not success proof.

---

## Missing literal binding / compatibility (fix before integration)

1. **Envelope schema does not fail-closed on `store-gc`.** Installation/project `if` enums are the 15 installation operations only. A mutation envelope with `operation: store-gc` and `projectId` **validates** (`schema-store-gc-falls-to-project-branch` admitted). Constructor/`current_key` refuse issuance, but raw `validate()` of a project-shaped GC envelope is not fail-closed. Before integration, the current envelope should refuse `store-gc` (or any `unowned-sweep` token) rather than treating it as a project mutation output. Do **not** add historical schema `not`.
2. **Installation operation lists are copied** into 244 envelope `allOf` and `MutationReceiptProjection`. They currently match 242’s 15. They will drift if the map changes; the map should be the single owner.
3. **`INDETERMINATE` remains on `MutationReceiptProjection.effectOutcome`.** This fixture’s `prepare_projection` of an INDETERMINATE receipt refused `CONFIG.INVALID`. That is not permission to persist an uncertainty receipt. Keep it as observation-only; do not treat the enum as a write license.

Declared pending (not closed): current output registry/renderer parity; native issuers and 242 admission wiring; 51-command contracts; lookup/census/publication; separately owned replay delivery; GC sweep owner.

---

## Verdict

- [x] Both archives/pins/members verified. 242 r2: 120/15/5 reproduced. GC current key issuance refuses on constructor **and** standalone `current_key`; historical token/data untouched. Partial/pass sweep law is explicit; not atomic; not SC-TRUST/transition journal.
- [x] 244: 79/4 reproduced. Distinct URI; installation forbids fake project; project still requires ProjectId; complete `receipt2:` recipe and exit join present. r1/r2 test defects were fixture/join omissions, not schema weakening.
- [x] Fail-closed GC is not bypassable via imported current key. Envelope **schema** still admits a project-shaped `store-gc` mutation document — fix before integration.
- [ ] **Not** product output/command issuer integration, GC implementation, or native/current/durable/replay proof.
