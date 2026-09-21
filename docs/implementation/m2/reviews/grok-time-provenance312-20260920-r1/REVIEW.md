# Independent review — successor original-core codec 312

**Standing:** bounded source review of frozen `time-provenance-successor-312`. Unselected successor codec and conditional context/embedded-byte joins. Not native runtime, complete proof admission, publication, or product installation. Installed product remains `fa72e50`. Keys/signatures in 229 fixtures are **synthetic zeros**, not crypto/TCB positives. Prior 309–311 reports were not edited (311 fully read; 310 ADDENDUM fully read, including withdrawal of the two §3 joins). Claude312 at 18:43 PDT was quota-blocked and produced no substantive review.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Review-local copies only. Frozen check/control logs were not overwritten.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **2354140 B, 559 members, SHA256 `f04b5b4284ac49d4acd51c6392bc268619b9e4db9c139834ff6ec41ae4396e5b`**. Standing: unselected312 successor codec and conditional context/embedded-byte joins; not full proof authentication or runtime integration. Extract rehashed **559/559**. Nested parent 311 pin `5c8d692e…b87d` (live tar match, 8953260 B / 957). Nested 229 r3 pin `edde8b4f…6b4e` (live tar match, 92716 B / 88). Nested 265 shapes `1328ba16…4208`. `kernel201.py` `df45c9c5…2299`. `canonical.py` `d47f25db…b442`. Original `trust_record_reference.py` `00ad3a34…e6df` **byte-identical** to frozen 309/310/311 full125; `trust_record_reference.before.py` equals it. Successor schema `private-trust-state.successor312.json` SHA256 `a0431300…7928` (packet root equals security copy).

Packet `review-inputs/` REVIEW/FOLLOWTHROUGH/ADDENDUM are byte-identical to independent grok 310 reports. ROOT-CHALLENGE.md SHA256 `b1ef9d0f…6a91`.

Preserved unchanged: 309 REVIEW `6a47037d…eb67`; 310 REVIEW `fb443e04…5b33`, FOLLOWTHROUGH `1c8c2ace…456b`, ADDENDUM `6d7c499d…45a9`; 311 REVIEW `02e8228a…d1f1`.

---

## Explicit versioning

`S4EvaluationInputV1` in the successor bundle is **byte-identical** to frozen 125 (`legacyS4Unchanged: true`). Two definitions added (`S4EvaluationInput`, `S4EvaluationInputV2`); two enclosing unions changed (`TimeInputV1`, `TimeEvidenceV1` now `$ref` the union); **123** other `$defs` unchanged; **0** removed. 125 → 127.

V2 is closed: `inputSchema` const **2**, `kind` still `s4-evaluation`, the existing eight members, plus **required** `authority: NodeRef`. `additionalProperties: false`. Versioning is the `inputSchema` const, not a new kind. Optional-on-V1 is not used.

Internal union `S4EvaluationInput` is `oneOf` V1|V2. Typed registry 134 → 136: two new V2-owned sites (`authority` → `RootAdmissionNodeV1` records; `beforeImage` → `TrustCapsuleV1` records). Exactly two `ClockWriteEventV1` target mappings change (`evaluation` and s4 `timeEvidence.proof`) from `S4EvaluationInputV1` to the union. S4.5 / challenge / restriction defs are unchanged.

**Legacy:** a reader can still `extract('S4EvaluationInputV1', …)`. Decoding V1 does not establish original-core provenance. P0/P1 V1 bind refuses `legacy-original-core-unavailable`. P2 V1 can **structurally derive** authority from exact `beforeImage.heads.root.admission` (hash and length), subject to all remaining historical admission. V1-plus-`authority`, unknown `inputSchema` 3, missing V2 `authority`, and extra members refuse `record-shape`. No re-encoding of historical V1 into V2 is offered. No installation migration is selected.

This is the honest closed-wire path named in 310 ADDENDUM §3.

---

## Original evaluating core

`bind_context` is literal joins only (`standing: literal-context-binding-only`).

- **P0/P1:** `authority` must be `RootAdmissionNodeV1` with `kind: anchor` (CoreAnchor). CoreAnchor has **no** `OriginalContext.time`. Index zero is the **authentication start** plus retained inventory/bootstrap-manifest/index-0 six blobs. It is **not** the final evaluating/recovery root. Final head is computed by 229 `conditional_embedded_head` over the **complete** embedded `rootChain` (ordered, time-free, no prefix). That head is still not accepted store/role standing.
- **P2:** `authority` (V2) or caller-supplied raw (V1) must equal `beforeImage.heads.root.admission` in hash and length; document/binding and `rootVersion` must agree with the before-head and clock record. Literal equality is not accepted standing.
- **No creator pin.** P0/P1 bind accepts a different original CoreAnchor than the 229 fixture’s first core (`P0/P1-own-original-evaluating-core-context`). `coreClosure == CreationInput.deliveringCore` is not a 312 join.
- **No AFTER-root cycle.** P0/P1 ordinary `RootAdmission` (required `context.time`) is refused `preaccepted-anchor-kind`. Downstream ordinary admission may cite the completed evaluation **after** S4; S4 must not depend on that future node.

This matches 229 G1/C.1/C.5 as corrected by 310 ADDENDUM. The S4 field locates the CoreAnchor of the core **relied on for that evaluation**, not the store creator and not the final embedded head.

---

## Complete embedded-chain addressing and envelope retention

`embedded_bytes` loads the CoreAnchor on the **same** `Operation.Budget`, reuses 229 `verify_anchor_bindings` (six blobs, index-0 body/envelope membership, bootstrap tree lengths), then `Operation.index` over the retained bootstrap-manifest body.

**Addresses (encoded, no new S4 field):**

- CoreAnchor already holds inventory body+envelope, bootstrap manifest body+envelope, index-0 root body+envelope. Those six blobs stay.
- Complete chain list lives in the retained bootstrap-manifest `members.rootChain`, not on V2 and not on current `source.closure`.
- Later root **bodies** are captured from inventory tree `sha256`+`length` at the manifest path. Index-zero selected pair must equal `node.root`.
- C.5 “ordinary edge” is specified here as **raw old/new chain authentication before S4** over those retained pairs. It is **not** a pre-S4 ordinary `RootAdmissionNodeV1`. The prototype **does not** run old/new quorum or revocation; `conditional_embedded_head` is selection law assuming that upstream work. Synthetic 229 signatures remain zeros.

**Envelope retention (enough and minimal for pairing uniqueness):**

- Read **every listed** `members.envelopes` row in bounded UTF-8 path order (inherited 234 index). Unlisted files are not read.
- Apply existing exact subject/domain/body-preimage pairing. Each selected root needs exactly one matching declared envelope.
- Missing an unrelated-looking listed candidate is **unavailable** (`operation-capture-cap`); uniqueness is not established without its bytes. Two distinct ROOT-matching candidates refuse `envelope-ambiguous`.
- Unused embedded catalog/list **bodies**, executables, and artifacts are **not** newly required by this resolver (`core-cache-and-unused-bodies-absent` keeps only the nine loaded objects). When those bodies are used as time evidence they keep existing payload-closure obligations.
- No `source.closure` substitute. No store-wide records scan.

That retention rule is the existing listed-envelope uniqueness law, not a new expansion. It is **enough** to address every embedded root and to refuse skip/ambiguity. It is **minimal** relative to 234: it does not pull unused catalog/list bodies. It is **not** enough as authentication, TCB, or a publication gate: `bind_context` and `embedded_bytes` are separate helpers; nothing in this packet requires both before a clock write is published.

Budget: first resolve **9 objects / 17 edges / 22691 B**; repeat same objects, **34** edges, same bytes. Exact-fit admits; object/edge/size−1 refuse; failure latches `operation-budget-closed`. `replace-shared-budget` (fresh inner `Operation()`) is caught as `operation-capture-cap`.

---

## Reproduction

Review-local copy only. Frozen `controls-r1/`, `check-report.json`, `registry-report.json`, `fixtures.json` were not overwritten.

| Kind | Result |
|---|---|
| 312 pins before extract | match |
| Nested 311 / 229 r3 live tars | SHA match |
| V1 def vs frozen 125 | byte-identical |
| Live `check_registry312.py` | 134 → 136; report SHA `512081d0…05a0` frozen-equal |
| Live `check_provenance312.py` | **68/68**; baseline 9/17/22691; repeat 9/34/22691; report SHA `68a1eeb8…bd03` frozen-equal |
| Live `check_controls312.py` | 9/9 caught; report SHA `442d6ac1…81bb` frozen-equal; all nine patches SHA-equal |

Nine syntax-valid controls: **7** AssertionError kills (`accept-legacy-core-from-caller`, `ignore-before-authority`, `allow-future-ordinary-authority`, `ignore-phase-history`, `ignore-head-document-binding`, `ignore-head-counter`, `use-index-zero-as-final`); **2** earlier refusals (`truncate-embedded-chain` → `complete-embedded-chain`; `replace-shared-budget` → `operation-capture-cap`). Matcher uniqueness 1 for all nine replace-targets. Three initial harness errors remain in `TEST-CORRECTIONS.md` / `check-r2` / `check-r3` (outer capture-unavailable vs innermost `operation-capture-cap`; size−1 `embedded-tree-length-cap`; missing `metadata238.Refusal` in the exception tuple). Producer unchanged for those; later head/history/counter joins are additional checks, not inferred from the first 60-case pass.

---

## Findings

### 1. Successor V2 vs 310 ADDENDUM — hold

Required `authority` on a new closed version, V1 preserved, P0/P1 CoreAnchor locator, complete-head as algorithm not a forward ordinary admission, no creator pin: these are the ADDENDUM corrections, not a reopening of the withdrawn joins.

### 2. Retention/typed resolution — hold, with a remaining producer join

Listed-envelope uniqueness plus manifest-keyed bodies is the right encoded address for C.5/G1. It is not a substitute for old/new quorum, launch TCB, or 222 durability. Publication still owes a join that a V2 record is not emitted unless `embedded_bytes` succeeds on that authority. That join is **not** in this packet (OWNER: separate successor reader/helper, not full workflow).

### 3. No authority-cycle / format / legacy / ambiguous-pairing flaw in this freeze

P0/P1 ordinary-with-`context.time` is refused. V1 remains interpretable in its limited scope; P0/P1 V1 cannot be migrated by inventing a locator. Ambiguous ROOT pairing uses the inherited index rule. Clock-event edges now name the union, so a V1 evaluation still type-checks; mixed old-producer / new-consumer pipelines are **not** selected.

**Actionable defects in this freeze:** none that make the successor codec self-contradictory with frozen 227/229/234/310 ADDENDUM.

---

## Remaining (do not count closed)

Actual original-authority authentication, retained∪incoming revocation, OLD/R populations, per-root signatures, proven clock publication, scoped old-T exceptions, accepted standing, 222 durability, fences/custody/census/capacity, qualified final age, native schema/visitor/producer integration, fused publish-time retention check, P2 parent-walk from before-head to CoreAnchor, payload `rootChain` 64-cap vs lifetime ancestry, and M2–M6 remain open. 311 Keep/NewRequired still emit V1 until a later native candidate. 305 1 s is still unqualified. Typed `TimeEvidence` is not proof a floor was established.

---

## Verdicts

- [x] **312 as unselected successor codec:** archive verified; V1 bytes preserved; explicit V2 `inputSchema` 2 with required CoreAnchor/before-head `authority`; complete embedded-chain addressing from retained inventory+manifest; every listed envelope retained for uniqueness; no creator pin; no forward ordinary-admission cycle; 68 cases and 9 controls frozen-equal.
- [ ] **Not** complete or durable provenance, TCB/signature admission, publication, native integration, OS qualification, or product installation.
