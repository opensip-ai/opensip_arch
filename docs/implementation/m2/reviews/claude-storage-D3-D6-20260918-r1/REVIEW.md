# Independent adjudication — storage D3–D6 purge-disclosure representation proposal

Reviewer: Claude (actual independent reviewer; Codex owns the design). 2026-09-18.
Standing: **design adjudication of an unselected proposal.** Not approval of reference 111, Rust 114,
any storage code, or any normative text. No frozen, selected or product byte was edited; no commit,
push or delegation. Owners were read from my verified scratch copy of frozen reference 111
(archive `050104a2…9a55`), whose workflow/common/envelope/invocation files are unchanged from 108.

## 1. Exact bytes reviewed

| Item | Bytes | SHA-256 |
|---|---|---|
| `storage-D3-D6-owner-proposal-20260918.md` | 8,189 | `e0289fc3c41502c73c98829e1d4066e4f30994fb0b42004bfd3808faf9ca7fe2` |
| `storage-D3-D6-measurements-20260918.md` | 1,619 | `9c791a751a5170c5af598bb6598cd6726e1d2907b6f7b0d27ca45588844f9ec9` |
| owner `result.json` / `sample-direct.json` / `sample-invocation.json` (copied to `claude-out/owner-*.json`) | — | `2fe7def5…9afe` / `4044957a…500b` / `53e8571f…0fea` |

Owner inputs read and hashed in `claude-out/owners-read.txt`: `workflows-and-surfaces.md` (§1, §9,
renderers/parity law l.1108–1130, capability availability l.1302–1345, `evidence.pinned` l.1597–1627),
`identity-and-evidence.md` (serialization fault route l.1573–1576), `command-inventory.v3.json`,
`check_workflows.v1.py` (purge refusal section l.1335–1368), the evaluator3 `command-envelope`,
`invocation-record` and `common` schemas, `foundation/canonical.py`.

## 2. Verdict

**The central choice — guarantee the direct refusal and its single-step record, and fail the aggregate
explicitly rather than shrink, summarize or page — is sound and is supported by existing owners.**
**Not yet ready for normative authoring: item 2 rests on a misidentified field (A-2), the two-copy
claim for the single-step record needs three closure rules the proposal does not state (A-3), and
three consequences need an owner sentence (A-1, A-5).**

## 3. Answers to the five questions

### A-1 — Q1: no owner requires durable full `InvocationRecord` admission for every admitted workflow
I searched the two contracts that could own it. What exists:
- workflows §1: "`RequestId` [is] minted before admission and **retained for refusal as well as
  success**" — retention of the request *identity*, not admission of a complete record;
- identity l.1573: "Output size overflow follows the serialization fault route with its measured bound;
  it never truncates or mints an empty successful Run";
- workflows §9: `output-serialization` and `delivery-required` are existing `faultCause` values of
  `operational-failed`.

So complete-or-fail for an oversized aggregate is the *existing* law applied, not a new exception, and
I found no conflicting owner. (Limit: I searched the contracts in the 111 tree, not every historical
completion document.) Two consequences need a sentence each:
1. **Where the per-step rejection lives when the aggregate cannot be serialized.** "Cannot
   retroactively change the observed per-step rejection" is only meaningful if that rejection, with its
   complete disclosure, has a durable home other than the record that failed to serialize. Name it
   (or say the disclosure is *not* durable in that case and only the mutation-free fact is).
2. **The visible class changes.** A refused purge inside a composed invocation is `request-rejected`
   / exit 2 at the step and `operational-failed` / exit 4 at the envelope. That is coherent, but it is
   a D9 golden and should be listed as one.

An option worth weighing, not a requirement: a refused *required* step ends the invocation, so more
than one `evidence.pinned` detail needs optional purge steps. A rule "after one `evidence.pinned`
refusal, later purge steps of the same invocation are skipped" would bound composed invocations to two
copies as well and make the 79.8 MB case unreachable. It changes step semantics, so it is an owner
call; the explicit-failure path is needed either way for other large aggregates.

### A-2 — Q2: the mandatory `availability` for purge is **not** `CommandEnvelope.availability`
The proposal requires the explicit empty `CapabilityAvailabilityV1` collection "mandatory even when
empty" and tells me not to repeat my earlier recommendation to omit it. The owners say otherwise:
- `command-envelope.schema.json`: `availability` is **optional**; `required` is
  `schemaFamily, schemaMajor, kind, requestId, termination, exitCode` (+ `errors` for failures).
- workflows l.1325–1332: `capability-availability` is a declared — and therefore required — parity
  field "of **every `requestClass: analysis` command** — `default`, `analyze`, `fit`, `audit` and
  `repair-verify`". The inventory agrees: 5 of 45 commands declare it, all `analysis`.
- `purge` is `requestClass: mutation` and declares `run-id, receipt-id, availability,
  termination-class, purge-disclosure`. Its `availability` is the **Run's evidence availability**, and
  the selected checker projects the refusal as
  `{'run-id': RUN1, 'receipt-id': None, 'availability': 'retained', 'termination-class':
  'request-rejected', 'purge-disclosure': …}` (`check_workflows.v1.py:1363`).

Two fields share a word. My earlier recommendation concerned the capability collection and stands:
it is not owed by a purge. Including the empty collection is harmless in bytes (the owner's 13,760
already contains it) but the closed form should not *require* it on a ground that does not exist.
What D4 actually has to answer is the opposite gap: parity totality (l.1128) requires `run-id`,
`receipt-id` (explicit null) and `availability: retained` to reach every renderer, "`CommandEnvelope`
major 3 is the parity reference", and the closed form forbids `run` and `mutation`. For `query` the
contract publishes envelope pointers for each parity field (l.1228–1233); for `purge` none is
published. Decide where those three values live — a few dozen bytes, but membership, not size, is
what the closed form fixes.

### A-3 — Q3: every occurrence, and what "two copies" is conditional on
`probes/positions.py` walks the complete schema closure and lists every position that can hold a
`DomainDetail`, with the multiplicity the schema permits:

| Document | Position | Max |
|---|---|---|
| `InvocationRecord` | `/termination/domainDetail` | 1 |
| | `/stepResults[]/termination/domainDetail` | 64 |
| | `/stepResults[]/result/unmetPreconditions[]`, `…/defects[]`, `…/remedy` | 4,096 / 16,384 / 64 |
| `CommandEnvelope` | `/termination/domainDetail`, `/errors[]` | 1 / 64 |
| | `/invocation/…` (as above), `/doctor/defects[]`, `/queryRecord/…`, `/queryResponse/termination/domainDetail` | — |

`Attempt` has **no** `DomainDetail` position, and neither has `CommandEnvelope.mutation`
(`MutationReceiptProjection`); with `receipt-id: null` in the owner's own refusal projection, a refused
purge has no receipt to budget. `errors` is already closed in prose — workflows l.1340: where the
termination's `domainDetail` is present "`errors` is exactly that detail" — so D4's errors rule adds
schema/host enforcement to an existing sentence; good.

The single-step record is two copies **only if** the successor also states:
1. **a refused purge `StepResult` carries no `result`.** `result` is required only for `completed`,
   and the schema does not bind the result variant to the step kind, so a rejected purge step may
   schema-validly carry a variant with `unmetPreconditions[]` — the natural place for a precondition
   failure, and a third copy (2B + B > 4 MiB at budget);
2. **exactly one attempt** (the owner's "no automatic mutation retry"): pin `retryPolicy` for purge and
   forbid `retried`;
3. **which optional members are excluded or reserved**: the owner's admitted sample omits
   `retentionDisclosure`, `cancellation`, and the attempt members `derivation`, `faultCause`,
   `installationJournalRefs`, `installationRecoveryStartRef`, `retried`.

Reserve: I re-measured the owner's two samples with the frozen-111 canonicalizer and obtain the same
**13,760** (direct) and **14,384** (single-step) bytes; worst canonical cost is 6 B per scalar (C0),
U+2028 is 3 B, emoji 4 B. At exact budget that leaves **2,624 / 2,000 bytes** spare — enough for the
A-2 parity values, not for an unreserved `retentionDisclosure`. `2·2,088,960 + 16,384 = 4,194,304`
exactly, so the reserve has no slack of its own.

### A-4 — Q4: no pagination is acceptable for a first version, on three conditions
Non-destructive failure with `DELIVERY.REQUIRED_PROJECTION_FAILED` is right, and I would not invent a
cursor surface for a state D3 admission is designed to make unreachable. But "ordinary authorized
release of explicitly named pins" helps only someone who already knows the names, so the state is
unrecoverable by design for anyone else. That is tolerable only if: (i) D3 admission lands no later
than pin persistence; (ii) **import and restore run the same complete-inventory admission and refuse**
— "not silently grandfathered" does not yet say what happens; (iii) doctor reports count and canonical
byte size against the budget, explicitly not an inventory. If any of the three cannot be promised, the
bounded listing becomes a first-version requirement.

### A-5 — Q5: what is still missing
- **The refusal's detail code.** "Refuse under existing retention-precondition semantics" needs a
  registered public detail. The registry and the generated enums are closed and checked (my
  reference 60 B-1); if the existing count/name-bound code is reused, say which; if a new one is
  minted it must go through the registry, the generator and all five inventories.
- A replacement that **shrinks** an over-budget inventory but leaves it over budget: treat like
  release (permitted). The proposal covers release, no-op and size-increasing replacement only.
- Batch: all-or-nothing on the complete *resulting* set, including a batch that both adds and releases.
- D3's counter is over `PinnedPurgeDisclosure(R)` and therefore a pure function of the pin set and the
  fixed-length RunId — this satisfies my earlier F3-5; keep remedy text and request ids out of it.
- D6 needs either a number or a mechanism: "pre-render into a checked bounded output buffer" has no
  bound for the human form. Per-pin framing (label, indentation, newline) × 4,096 is outside the
  canonical 4 MiB, and human escapes differ from canonical ones (examples in `probes/reserve.json`).
  Either publish the human renderer's per-pin framing constant and derive its maximum, or specify the
  fully validated spool with no fixed bound. Partial physical output with no success marker is the
  right terminal semantics.

## 4. Agreement, for the record
D3 single aggregate budget owned by foundation and imported by workflows; admission inside the
protected transaction over the complete resulting inventory (this is my F3-4); equality admits;
checked early-refusing counter; release permitted while over budget; D5 no deletion, no rename, no
incomplete `evidence.pinned`; D6 complete-or-fail with no destructive fallback. The owner's statement
that schema-valid examples do not establish host-semantic validity is correct and I rely on it too: my
position table is schema reachability, not host behaviour.

## 5. Probes and limits
`probes/positions.{py,json}` (three failed harness versions preserved with a note), `probes/reserve.{py,json}`,
`probes/optional-members.json`. One schema id (`native:evidence-schemas:v2`) was not resolvable from
the workflow closure and is listed in the output; it is not on a path to `DomainDetail` that I could
see from the referring side. I did not construct a complete schema-valid 64-step record myself; the
79,798,436-byte figure is the owner's.

## 6. Bounded verdict
**D3–D6 proposal: direction accepted as sound; CHANGES REQUIRED before normative authoring — A-2
(the availability ground and the missing parity carriers), A-3 (three closure rules and the optional
members), A-1 (durable home of the step rejection; the exit-4 golden), A-5 (detail code; human bound).**
This approves no text, schema, model or code.
