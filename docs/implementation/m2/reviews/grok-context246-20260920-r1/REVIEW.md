# Independent review — trust command context and parity 246 r1

**Standing:** bounded code review of frozen 246 r1 over pinned 243 r1 and 244 r2 (and 239/241/242 r2). **Not** cumulative approval, native/current-effect authority, 245 request-pipeline integration, 51-command completion, or authenticated completion. Archived 245/244 r2 reports were not edited.

Python 3.12.13 `-I -B`. Sibling names reconstructed from verified archives. Frozen variant output directories were not overwritten.

---

## Verification

Frozen `trust-command-context-wip-246-r1`: **16748 B, 49 members, SHA256 `8421fc04…2614`**. Pin, tar, member count, and every `subject.json` hash matched before extract; extract rehashed 49/49.

`inputs.json` pins match reconstructed siblings: 243 primary `d207de6c…d18f` (`trust_operation_reference.py` `bf92db33…fb3b`), 244 r2 `ce13548b…996a` (envelope `e0566ab5…7777`, `output_reference.py` **unchanged** `de40f007…30ce`).

New schema URI: `urn:opensip:proposal246:command-envelope`.

---

## What 246 adds

Closed `TrustCommandContextV1` is **required only** for the four 245 commands (`trust-ceremony-begin|commit|abort`, `trust-acknowledge-restore`). Other operations **must not** carry `trustContext`. Context fields are raw retained-byte SHA-256 projections (action, OperationInput digest, payload-body digest, authorization-body digest, BeginBatch digest) — not new H identities. Public `batch-id` maps to `batchDigest`.

`prepare` requires an actual 243 `Operation`, validates `PublicationRef` + `previousCapsule` locator, then loads D/outcome/operation through current `InputWork` (243 joins). BEGIN COMPLETED requires the created batch descriptor and binds closure/payload/authorization to the original OperationInput closure. BEGIN FAILED: `batchDigest` null means **none created bound here**, not “no live batch.” COMMIT/ABORT load the **input** batch even if after-image clears it. Ack/restore-recovery: three ceremony digests **null** means not a ceremony request / not bound here, not absence from restored history. Body **and** envelope bytes are captured under the **same** budget; envelope presence cannot be skipped (`doc_digest`). No signature/current-effect/durability proof.

**Required-effect success rule (four commands only):** 245’s mutation step is REQUIRED, so `FAILED` or `INDETERMINATE` cannot pair with `termination.class: success`. Encoded on the 246 wire schema (`allOf` last rule) and therefore on raw validate/render. COMPLETED + later failed delivery remains legal. 244’s generic `prepare_projection` is **unchanged**; purge FAILED+success still formats there. No full historical/project/optional matrix is inferred. EffectOutcome is still asserted, not proven.

Renderers (json / agent with empty `agentHints` / human) share the five 245 parity fields; human prints null as `not bound by this command result`. Action-command and 244 exit joins are checked. Source envelope bytes are not mutated. Formats do not grant mutating agent-serve access.

---

## Reproduction

| Corpus | Result |
|---|---|
| `check_context.py` | **33/33** equal frozen `context-check-r4.json` (source `6758c5ac…6675`) |
| `check_render.py` | **32/32** equal frozen `render-check-r4.json` (5 actions × COMPLETED/FAILED × 3 formats + action/exit refusals) |
| `check_variants.py` | **4/4** batch / presence / locator / budget omission controls |
| `check_effect_schema_variant.py` | **1** rule omission × **2** effects (FAILED and INDETERMINATE + success admit after removing the rule) |

**Beforeimages:** r3 `context-check-r3.stderr` is `AssertionError: ('admitted', 'required-failed-effect-cannot-report-success')` — unmatched-brace builder left the old schema, so the new test correctly failed. `build_schema-before-matrix-syntax.py` / `build_schema-before-required-effect.py`, `context_reference-before-locator.py`, `render_reference-before-typed.py` retained. r4 passes after the corrected builder; tests were not weakened.

Synthetic fixture bodies/envelopes are **intentionally unauthenticated**; roles may remain unbootstrapped. Success standing is `prepared-trust-output-only` with five pending owners (244’s three plus metadata-auth/effects and renderer/native-dispatch).

---

## Independent probes

| Probe | Result |
|---|---|
| Old D without `commandOutcome` | `command-outcome-missing` |
| Coherent batch payload ≠ closure manifest | `batch-payload-authorization-binding` |
| Missing authorization envelope bytes | `operation-capture-cap` |
| Wrong `previousCapsule` locator | `publication-reference-binding` |
| BEGIN COMPLETED shared counters | objects 9 = `len(budget.raw)`; bytes match sum of captured raw |
| Fail-stop after missing body | `operation-budget-closed` |
| Four-command FAILED + `success` | `CONFIG.INVALID` |
| Project `purge` envelope on 246 schema (no `trustContext`) | admitted |
| 244 helper FAILED receipt + `success` for `purge` | still `prepared-output-only` (helper unchanged) |
| 245 `request_reference` / `prepare_invocation` imported? | no |

---

## Required-effect rule: fit and remaining joins

**Source grounding is sound and scoped.** 245 makes the mutation step required for these four commands, so reporting overall `success` with FAILED/INDETERMINATE effect would contradict that step’s requiredness. Putting the rule on the **246 current URI** (not historical envelope, not 244 Python helper) matches “no full matrix for historical/project/optional workflows.” COMPLETED + `operational-failed` delivery remains the 244 selected delivery-failure case.

**Not a truth claim:** the rule constrains **reported pairing**, not whether the effect happened.

**Missing joins still outside this slice:** wiring 245 retained invocation/native effect into 246; replay/delivery context; public refusal mapping; authenticated metadata/current state. Do not extend this four-command rule by silently changing 244’s generic formatter.

---

## Remaining (do not count closed)

245 request/retained-invocation pipeline is **not** composed here. Native/current-effect, fence/barrier, lookup/census/durability, mutating transport, GC sweep owner, two evidence commands, 51-command integration, M3–M6 remain pending. Context projects original receipts only; separately identified replay context is owed.

---

## Verdict

- [x] Archive/pins/members verified. **33 / 32 / 4 / 1×2** reproduced. r3 builder failure retained; r4 not weakened.
- [x] Context digests are captured body/envelope bytes under one 243 Operation. Null batch/ceremony digests mean “not bound here,” not historical absence.
- [x] Four-command required-effect success rule is schema-encoded and renderer-visible. COMPLETED+failed delivery remains. 244 helper and project outputs are unaffected.
- [x] Independent coherent rewrite / missing ref / locator / fail-stop probes refuse. 245 is not integrated.
- [ ] **Not** native/current-effect authority, request-pipeline completion, or command installation.
