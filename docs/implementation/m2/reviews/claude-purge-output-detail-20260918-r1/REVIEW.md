# Independent adjudication — purge131 output-detail gap (D3 aggregate-overflow fallback)

Reviewer: Claude (independent; Codex remains decision owner). 2026-09-18. Owner question:
`purge131-output-detail-20260918.md` (SHA-256 `d275092a…338a`, 1,713 B). Owner bytes read from **my verified
extraction of frozen 127** (hashes of all seven files in `claude-out/cases.json`): public-detail registry,
`common.schema.json`, `command-envelope.schema.json`, D9 v1.14, workflow-projection contract v3, and D3–D6 owner
decisions r3 (`b6296a77…`). Earlier decisions are preserved; this answers one question. No schema, code or
frozen/selected edit; no commit, push or delegation; no approval of any schema or code follows from it.

## 1. The gap is real (executable, `claude-out/cases.py`)
- `OUTPUT.SERIALIZATION_FAILED` is a `D9ErrorCode`; it is **not** a `DomainDetailCode` and has no registry record
  (case 1: the proposed detail is schema-invalid today).
- `kind=failure` requires `errors`, `minItems: 1`, items `DomainDetail` — so the agreed fallback
  (operational-failed / output-serialization / `OUTPUT.SERIALIZATION_FAILED` / exit 4) **cannot be emitted** without
  some registered detail.
- It cannot keep `evidence.pinned`: that code *requires* `purgeDisclosure` (case 5), which is exactly what did not
  fit. And no other code may carry `purgeDisclosure` (case 4) — the schema already enforces the owner's "never
  includes purgeDisclosure".

## 2. Is there an already-owned detail that honestly names this? — No

| Candidate | Schema-valid today | Why it is not honest |
|---|---|---|
| `OUTPUT.RENDERER_QUOTA_EXCEEDED` | yes (case 2) | The code occurs in exactly three frozen files — two schema enums and the registry — and in **no prose anywhere**. It has a name but no owned meaning. The name says *renderer* (SARIF/HTML/agent projections) and *quota* (a policy allowance); the failing thing here is the JSON envelope itself, which the envelope schema calls "the parity reference", hitting a structural bound. Borrowing it would *define* an undefined code by accident. |
| `DELIVERY.REQUIRED_PROJECTION_FAILED` | yes | Owned by the delivery-required route (query/workflow projection checkers bind it there). It would contradict the agreed `faultCause=output-serialization`. |
| `EVALUATION.OUTPUT_BOUND_EXCEEDED` | yes (case 3) | **Same D9 triple**, and the closest precedent — but owned by identity/evaluator-fault and scoped by name and selector to evaluator emission ("array/C-byte bound"). A purge refusal is not an evaluation. |
| `HOST.IO_FAILURE` / `CONFIG.INVALID` (the two existing dual codes) | yes | Wrong cause; the first is the very thing the projection contract says this must *never* be. |

So I agree a fourth row is needed, and that it adds no D9 class, error code or exit.

## 3. On the proposed spelling — lawful, but I recommend a different one
Registering the D9 error code a second time as a detail has precedent (`CONFIG.INVALID`, `HOST.IO_FAILURE` are in
both enums), so the proposal is **admissible**. My objection is to what it says, not whether it may exist:

1. **It carries no information.** `termination.errorCode` already says `OUTPUT.SERIALIZATION_FAILED`. The registry's
   own rationale for adding details is that a code must "name its remedy". A detail equal to the error code names
   nothing the envelope did not already say.
2. **It merges two causes with opposite remedies.** "Serialization failed" covers (a) a *complete, well-formed*
   document that exceeds the output bound — deterministic, the user's remedy is to narrow scope or release pins —
   and (b) an encoder fault (unrepresentable value, invariant breach) — a defect, the remedy is to report it. The
   owner's own wording is (a) only ("complete bounded product-document encoding failures … not policy failure").
   A generic dual code will attract (b) the first time someone needs a detail for it, and consumers keyed on the code
   can then no longer offer the right remedy.
3. **The frozen precedent for this exact triple chose the specific name.** `EVALUATION.OUTPUT_BOUND_EXCEEDED` →
   `OUTPUT.SERIALIZATION_FAILED`/operational-failed/output-serialization. The honest sibling is the same idea one
   level up: a workflow-owned **`OUTPUT.*` "document bound exceeded"** detail (spelling is the owner's; I am naming
   the *meaning*, not selecting vocabulary). It is not purge-specific — any command's envelope can exceed the
   bound — which is why it belongs under `OUTPUT.` with owner `workflows`, as proposed.

If the owner nevertheless prefers zero new spellings and takes the dual registration, I would not block it, **provided**
the registry record states the narrowing in its selector: *whole-document bound overflow only; encoder faults carry
no domain detail or a separate one*.

## 4. Conditions that apply to either spelling
- **C-1 binding.** The detail is lawful only with class `operational-failed`, `faultCause=output-serialization`,
  `errorCode=OUTPUT.SERIALIZATION_FAILED`, exit 4 — and that triple with `kind=failure` should require *a* bound
  detail. State it where `CONFIG.INVALID`'s "not an arbitrary DomainDetail" sentence lives; one positive and one
  negative checker case each way.
- **C-2 the fallback must be unable to overflow.** `errors` has exactly one item; `subject = requestId`; `remedy` is a
  **fixed** string (≤ 1,024 by `BoundedText`); no `invocation`, no `purgeDisclosure`, no echo of user paths beyond
  the header's bounded fields. Then its size is a constant that can be asserted against the bound in a checker case —
  otherwise the fallback needs a fallback.
- **C-3 no false claims (carried from D3 r3 B-1).** The remedy text must not say the full record *was* retained; say
  how to retrieve it *if* retained (by RequestId), and that evidence and pins are unchanged. "No purge mutation on
  this path" needs an ordering case: the overflow is detected before any deletion effect, not after.
- **C-4 parity.** The non-JSON renderings of this failure carry the same code and no disclosure; a renderer that
  cannot fit is the *separate* delivery/renderer route and must not loop back here.
- **C-5 registry closure.** `DomainDetailCode == registry records` holds today (316 = 316); the new row must be added
  to both common schemas (workflows and `evaluator3/`) and the registry together, or the closure sweep fails — which is
  the desired guard.

## 5. Answer
**No existing detail honestly names this case; a fourth workflow-owned detail row is justified and adds nothing to D9.
I agree with the owner's route, subject, remedy content and the no-disclosure rule. I recommend the row name the
*bound overflow* (sibling of `EVALUATION.OUTPUT_BOUND_EXCEEDED`) rather than duplicate the error code, because the
duplicate is uninformative and merges overflow with encoder defects; the dual registration is admissible with the
narrowing written into its record. C-1..C-5 apply either way.** No schema, vocabulary, code or cumulative approval
is implied.

Evidence: `claude-out/cases.py`, `claude-out/cases.json` (owner-byte hashes, facts, five executable cases).
