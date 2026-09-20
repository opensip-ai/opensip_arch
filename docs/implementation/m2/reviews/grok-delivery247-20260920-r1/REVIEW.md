# Independent review — prepared trust delivery binding 247 r1

**Standing:** bounded code review of frozen `trust-delivery-binding-wip-247-r1` over pinned 245 r1, 246 r1, 243 r1, 244 r2, and 242 r2. **Not** cumulative approval, native/current-effect authorization, durable delivery, mutating transport, source selection, or product qualification. Archived 246/245/244 reports were not edited.

Python 3.12.13 `-I -B`. Sibling names reconstructed from verified archives. Frozen variant output directories were not overwritten.

---

## Verification

Frozen `trust-delivery-binding-wip-247-r1`: **6440 B, 14 members, SHA256 `2747c1f55d2322932f846287f8bd200235f8e342ffd077507cda4f333816c38b`**. Pin, tar, member count, and every `subject.json` hash matched before extract; extract rehashed 14/14. Standing on the subject: Incomplete WIP, not approval or source selection.

`delivery_reference.py` SHA256 `deb8ff34c21b03ce35230a5b92795cfa2e4fc8a8af119055388de80ad2fb466f`.

`inputs.json` pins match reconstructed siblings:

| Pin | SHA256 |
|---|---|
| 245 r1 archive | `6c7b70fc…3647` (`request_reference.py` `bee8e447…8982`) |
| 246 r1 archive | `8421fc04…2614` (`context_reference.py` `6758c5ac…6675`, `render_reference.py` `0ee8e0b0…5ee5`, envelope `d5ec3aad…bf33`) |
| 243 r1 (via 246) | `d207de6c…d18f` |
| 244 r2 helper | **unchanged** `de40f007…30ce` |
| 242 r2 module | `3ff84c3f…bc62` |

Work copy sibling names: `m2-trust-command-request-draft-245`, `m2-trust-command-context-draft-246`, `m2-trust-delivery-binding-247` (frozen `delivery-variants-r1` excluded), plus 243/244/242/241/239 from prior verified extracts.

Archived 246 review SHA256 `bb4dd564acb7773879e7a5fd5d2cbc12723ea457607aaf92ec9008fcbba33256` — unchanged.

---

## What 247 adds

Prepared request/invocation/attempt/outcome **delivery joins only**. `prepare` requires an actual 243 `Operation` and stays on that ledger.

Pipeline in `delivery_reference.py`:

1. 245 `decode_body` → command from closed `{action}`.
2. 242 `parse_invocation` + `bind_step(current, retained, scope, command, 0, store=selected_store)` — original installation scope, immutable invocation, mutation step 0, `retryPolicy: none`.
3. Host `InvocationBinding` attempt: `requestId` equals current, `stepId == 0`.
4. Exact built-in two-step expansion: `len(orderedSteps)==2` and canonical steps equal 245 `prepare_invocation` expected steps (format and mode taken from **current**).
5. Load D (`PublicationRef` + `previousCapsule`) and `TrustCommandOutcomeV1`; `outcome.scope` equals retained scope; receipt `requestId`/`stepId`/`executionId` equal the attempt.
6. Same-Operation 246 `R.prepare` + selected renderer.

Standing is `prepared-delivery-only` with **7** pending owners (246’s five plus `native-retained-invocation-and-attempt-custody` and `actual-delivery-and-final-invocation-result`). Matching caller-supplied current/retained/attempt bytes are **not** native custody. Termination/exit remain asserted inputs; 246’s required-effect success rule still fires through `R.prepare`. Original receipts only (`replayed` const `false` on 243 `TrustCommandOutcomeV1`). Render format is not mutating agent-serve.

244 `prepare_projection` is unchanged. 247 does not call `current_agent_request`.

---

## Reproduction

| Corpus | Result |
|---|---|
| `check_delivery.py` | **38/38** equal frozen `delivery-check-r1.json` (source `deb8ff34…466f`) |
| Shared positive fixture | objects **9**, edges **17**, bytes **6723** |
| `check_variants.py` | **4/4** core fields equal frozen `delivery-variants-r1/results.json` |

38 cases: five 246 fixture actions × three formats (human/json/agent); exact shared budget; short objects/edges/bytes; host-attempt `requestId`/`stepId`/`executionId` plus fail-stop close; selected-store S/G/K; wrong request; body `store` injection; current≠retained params; coherent extra-mutation-param / optional-mutation / missing-render / renderer-dependency; coherent fresh requestId cannot borrow old outcome; wrong publication locator; caller-echo-does-not-become-custody.

Omission controls (baseline refuses, mutant admits `prepared-delivery-only`):

| Variant | Baseline refusal |
|---|---|
| scope | `request-outcome-original-scope-binding` |
| attempt | `host-attempt-receipt-binding` |
| expansion | `builtin-command-expansion` |
| budget | `operation-object-budget` (246 `R.prepare` on a **new** `Operation`) |

Repro `sourceSha256` on generated variant files differs because the harness rewrites `S=Path(...)` to the local work path. Frozen `delivery-variants-r1/` was not overwritten.

---

## Independent probes

| Probe | Result |
|---|---|
| `replayed: true` on original outcome | `shape:TrustCommandOutcomeV1` |
| BEGIN FAILED + `termination.class: success` | `CONFIG.INVALID` (246 required-effect rule) |
| COMPLETED + `operational-failed` / exit 4 | `prepared-delivery-only` |
| begin request + commit descriptor | `request-outcome-original-scope-binding` |
| `format=agent` | prepares; `delivery_reference.py` does not call `current_agent_request` |
| coherent mutation `retryPolicy: idempotent-retry` | `CONFIG.INVALID` |
| attempt `executionId` ≠ receipt | `host-attempt-receipt-binding` |
| tampered `receiptId`, attempt triple unchanged | `receipt-identity` (via 246 → 244 helper) |
| restore-recovery descriptor + public `{action: acknowledge-restore}` | **admitted** (see joins below) |
| format rewritten only on current+retained render step | result `format` follows current; request body has no format field |
| pending owners | 7, standing `prepared-delivery-only` |

No native exploit is claimed by the four omission controls.

---

## Joins inside prepared scope, and what 247 does not stringify-equal

Claimed joins hold on this candidate: request→245 command, 242 original scope/`bind_step`, exact 245 two-step expansion, host attempt vs current `requestId`+step 0, D locator, outcome scope vs retained scope, receipt vs attempt triple, same-Operation 246 context, selected renderer. Receipt identity is still checked because 246 calls the unchanged 244 helper.

**Not a 247 string-equality of public `{action}` to `trustContext.action`.** Those vocabularies differ by design:

- 245 body enum is `begin|commit|abort|acknowledge-restore`. 246 `trustContext.action` is 241 `OperationInput.action` (`ceremony-begin`, …, `restore-recovery`).
- 242 `trustActions` maps both `acknowledge-restore` and `restore-recovery` onto command `trust-acknowledge-restore`. The 247 corpus **passes** restore-recovery fixtures using public body `acknowledge-restore`. Probe: admitted, `request.action=acknowledge-restore`, `trustContext.action=restore-recovery`, `replayScope.operation=trust-acknowledge-restore`.
- Cross-command confusion (begin request vs commit descriptor) **is** refused, because installation `operation` in the original scope differs.

That is consistent with 245’s closed body, not a missed 247 command/scope join. 247 still does not add a prepared-scope check that the public action token equals the retained OperationInput action. Do not treat restore-recovery as a fifth public request leaf.

**Other prepared-scope facts, not defects against the README:**

- Render `format` is recovered from current step 1 params, then fed back into 245 `prepare_invocation`. It is not a 245 body field.
- `selected_store` (StoreBinding) and publication byte `store` are different parameters. Selected store is joined to outcome scope through 242 `bind_step` + canonical scope equality, not by comparing the in-memory dict.
- Termination/exit are still asserted; pairing with `effectOutcome` remains the 246 schema rule.
- Equal caller-supplied current/retained/attempt records remain a TCB premise (`caller-echo-does-not-become-custody`).

Replay delivery (new receipt, `replayed: true`) is not implemented here.

---

## Remaining (do not count closed)

Native retained-invocation/attempt custody, actual delivery and final invocation result, metadata authentication/current effects, publication census/durability, fence/barrier, mutating API/MCP, GC sweep owner, two evidence commands, 51-command integration, M3–M6. 244 generic helper is not a product dispatcher. 247 is not native command installation.

---

## Verdict

- [x] Archive/pins/members verified. **38 / 4** reproduced. Variant path SHA differs only from local `S=Path` rewrite.
- [x] Prepared pipeline joins 245 request decode, 242 original scope and built-in expansion, host attempt, 243 original outcome scope/execution, and same-Operation 246 context/render. Standing `prepared-delivery-only` with seven pending owners.
- [x] Independent probes refuse replayed original receipts, FAILED+success, cross-command descriptor borrow, execution mismatch, coherent retry rewrite, and receipt-identity tamper. Agent format does not call mutating transport. COMPLETED+failed delivery remains legal.
- [x] Public request action is not string-equal to 246 `trustContext.action`; restore-recovery remains a shared 245 command, as in the frozen 38-case corpus.
- [ ] **Not** native/current-effect authority, durable delivery, or command installation.
