# Independent adjudication r2 — storage D3–D6 owner decisions

Reviewer: Claude (actual independent reviewer; Codex owns the design). 2026-09-18.
Standing: **design adjudication of unselected decisions**, against my D3–D6 r1 findings A-1 to A-5.
Not approval of any text, schema, model or code; not cumulative acceptance. My r1 review and evidence
are unchanged. No frozen, selected or product byte edited; no commit, push or delegation.

## 1. Exact bytes reviewed

`storage-D3-D6-owner-decisions-r2-20260918.md`, 7,758 bytes, SHA-256
`8aada2b0a1fb4431f1611ca9d7b5619b798e8339a1a3d548c4f0350af2f9ee5a`
(copy: `claude-out/decisions-r2-as-reviewed.md`).

Owners: the eight files I read for r1, taken this time from my verified scratch copy of frozen **118**;
each hashes identical to the 111 copy (`claude-out/owners-read.txt`), so the owner's statement "same
owner bytes as 111 for this scope" is confirmed, not assumed. Additional schema facts read for this
round: `retryPolicy` enum `{idempotent-retry, none}` with mutation excluded from retry;
`dependencyGate` enum `{completed, terminal}`; `terminationEmitted` is a bare boolean; envelope,
`StepResult` and `InvocationRecord` are all `additionalProperties: false`; `CommandEnvelope.invocation`
is optional.

## 2. Verdict

**r2 resolves A-1, A-2, A-3 and most of A-5, and A-4's three conditions are adopted verbatim. The
parity projection and the closed one-step form are coherent with each other and with the owners.**
Three things should change before normative authoring (B-1 to B-3); the rest are small.

| r1 | r2 | Assessment |
|---|---|---|
| **A-1** durable home of the step rejection; exit-4 golden | item 1: disclosure **not guaranteed durable** on aggregate failure; no new store; three-part golden; step never relabelled | **Resolved, honestly.** I found no owner this conflicts with: workflows §1 retains the *RequestId* for refusals, identity l.1573 and the `output-serialization` fault cause already say complete-or-fail, and nothing promises a standalone step record. Declining my "skip later purge steps" option is right — it would have changed step semantics to fix a size problem. See B-1 for the one consequence r2 does not yet face. |
| **A-2** wrong availability; missing parity carriers | item 2: claim retracted; closed `PurgeRefusalProjection`; published pointers for all five parity fields; capability collection absent from the direct form, still owed by composites that selected analysis | **Resolved**, with B-2. Pointers into `termination` rather than `errors[0]` are the right choice since the two are byte-equal by rule. |
| **A-3** three closure rules + optional members | item 3: no `result`; one Attempt with exactly `executionId`/`outcome`; `retryPolicy=none`; every optional member I listed excluded; "a cancellation or other owed field changes the form and obeys complete-or-fail — do not discard owed data" | **Resolved.** That last sentence is the important one: the closed form is a *guarantee about one shape*, not a licence to drop data to reach it. `terminationEmitted` as the actual delivery fact is correct. |
| **A-4** no pagination, three conditions | item 6: all three adopted; import/restore refuse **before durable publication**, atomically; doctor reports count and bytes, "unavailable" rather than invented | **Resolved.** |
| **A-5** detail code; shrinking replacement; batch; human bound | items 5 and 7: new registered `evidence.pin-limit`; strictly size-reducing changes permitted while over budget; all-or-nothing batch; validated spool, no invented ceiling | **Mostly resolved**, with B-3 and the notes. |

## 3. Required before authoring

### B-1 — an envelope that *attaches* the invocation carries four copies, and fails at half the budget
The closed direct form excludes `invocation`, so it is safe. But `CommandEnvelope.invocation` is an
optional member any other failure envelope may carry, and with it the disclosure appears in
`termination`, `errors[0]`, `invocation.termination` and the step. Measured from the owner's own
samples with the r2 members applied (`probes/reserve-r2.json`): fixed overhead 28,375 B, so the largest
disclosure that fits is **1,041,482 B — 0.499 of the budget, and smaller than the contract's own
4,096-ASCII-pin inventory (1,220,808 B)**. So "a one-step purge invoked through any path that attaches
the invocation" is *not* covered by the guarantee, and r2 item 1's golden would fire for an inventory
D3 admitted.

This matters more than an ordinary size limit because of what is lost: on aggregate failure the user
gets exit 4 and **no pin names at all**, and item 1 has just (correctly) said the disclosure is not
durable either. The refusal's whole purpose is to show the pins. Decide one of:
(a) a failure envelope whose termination carries `evidence.pinned` never attaches `invocation`
(the record, if any, is reachable by RequestId) — this keeps every such envelope at two copies and is
an omission of an *optional attachment*, not of owed detail; or
(b) state explicitly that the guarantee is for the direct command only and list the four-copy
threshold as a disclosed limit. I recommend (a).

### B-2 — `availability: "retained"` should be the observed value, not a constant
The purge parity field is the Run's evidence availability. A pinned Run whose evidence is already
corrupt, expired or partially unavailable is still refused by its pins (identity l.1755 lists "purged,
expired, corrupt or unavailable" as distinct current-availability states; workflows l.319 and l.689
speak of partial availability). A constant would then assert something false in exactly the situation
where the user is deciding whether the evidence is worth keeping. Make it the observed value from a
closed vocabulary — and name that vocabulary's owner, because I could not find a schema enum that
contains `retained`; today it exists in prose and in the checker's literal. Size is unaffected
(longest token +3 B). `receiptId: null` as a constant is right: no mutation ran.

### B-3 — `evidence.pin-limit` hides which limit, and the over-budget exception must not admit fresh invalid names
- One code for count, name-length and aggregate-bytes with `subject = RunId` leaves the cause only in
  free-text `remedy`. A caller, and a test, cannot tell them apart, and the remedy differs (release
  pins / shorten this name / shorten or release). `DomainDetail` is closed to `code, remedy, subject,
  purgeDisclosure`, so either mint three codes or publish a subject grammar that carries the limit.
  Either way it goes through the registry, generator, both common schemas and all five inventories
  atomically, as r2 says; also replace the contract sentence that currently sends these refusals to
  "the existing retention precondition rule", and add the golden.
- "Permit … strictly size-reducing replacements even if still over budget" must be scoped to the
  **aggregate-bytes** ceiling. A rename or create inside such a batch must still satisfy the per-name
  256-scalar bound on its own; shrinking a 400-scalar legacy name to 300 is a release-worthy
  improvement only if you say so deliberately, and I would not. State the rule per ceiling.

## 4. Smaller points
- **Budget (item 4).** r2 expects the change to reduce direct cost. Measured, it *rises* slightly:
  direct 13,760 → **13,837**, single-step record 14,384 → **14,524** (the 124-byte projection outweighs
  the removed empty collection). Spare at exact budget is **2,547 / 1,860 B** — still inside 16 KiB.
  These are my constructions from the r1 samples and are **not schema-validated**: `purgeRefusal` is a
  proposed member and the current schemas refuse it. Re-measure on the successor schemas, as r2 says.
- **Schema enforcement.** Envelope, `StepResult` and record are `additionalProperties: false`, so both
  new members need schema edits plus `if/then` conditions for "required here, forbidden elsewhere";
  the RunId four-way equality (request target, `subject`, disclosure, projection) and the
  `errors[0] == termination.domainDetail` equality are host validation. `dependencyGate = completed`
  with no dependencies is schema-valid and vacuous; fine.
- **Doctor (item 6).** "Exact canonical byte size" of an over-budget inventory must come from the same
  streaming, non-allocating counter as admission, not from building the document that could not be
  built; say so, or allow "exceeds budget by at least N".
- **Spool (item 7).** Agreed. Add: private file mode, removed on every path including failure, never a
  second durable copy of pin names — the same hygiene the publication review required.
- **Item 1 wording.** "existing durable attempts/records … survive": add that the *aggregate* failure
  envelope's own `errors` carry the small `output-serialization` detail, never an `evidence.pinned`
  detail without its disclosure.

## 5. Probes
`probes/reserve_r2.py` → `reserve-r2.json` (sizes via the frozen-118 foundation canonicalizer);
`owners-read.txt` (118 vs 111 owner hashes). r1's position enumeration still applies unchanged because
the schemas are byte-identical.

## 6. Bounded verdict
**D3–D6 r2: coherent, and A-1 to A-4 resolved. CHANGES REQUIRED before normative authoring: B-1
(four-copy attached-invocation envelopes — recommend never attaching `invocation` to an
`evidence.pinned` failure), B-2 (observed availability from an owned closed vocabulary), B-3
(distinguishable pin-limit causes; per-ceiling scope of the reduction exception).** Approves no text,
schema, model or code.
