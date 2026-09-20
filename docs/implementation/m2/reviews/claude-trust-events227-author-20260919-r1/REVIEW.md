# Author assistance — draft operation/event shell codec (for root's review; not approval, not a decoder)

Author: Claude. Date 2026-09-19. **Draft only. Nothing here is selected, accepted or authority; root must review it as it would any proposal. No product/candidate/repo edit, commit or push; work confined to this directory.**

## Inputs (verified before reading; every member hashed from the tar)
| Frozen input | SHA-256 | bytes / members |
|---|---|---|
| `trust-audit-wip-226-r3` | `cbc909dca77af8d71dc9b996f09447a5a5b1d7cf57e522bfa00f8c37985f86c9` | 77,812 / 69 |
| `trust-time-wip-225-r2` | `84e48e36301532b11659c4f4863a39207bd1197b56b204ab33e4a440bd96c413` | 198,108 / 84 |
| `trust-codecs-wip-227-r2` | `ee7ba31b43537aa8b4fee905d67e1de6879a4a5b604bf71066b8e77bd143db8e` | 87,012 / 15 |
All equal the request and their archive pins (`claude-out/pin-verification.json`; end pass re-verified). I did **not** use working 215 r15 / 222 r7 / 203 prose. I did not reuse 227 r1's withdrawn same-S generation claim; the notes state the corrected law.

## Deliverables (`proposed/`)
- `trust-event-shells.v1.json` — closed JSON-Schema fragment, 38 `$defs`: **21 copied verbatim from 227 r2** (Timestamp, Hex64, integers, Anchor, RequestId, ExecutionId, StateSchema, BlobRef/NodeRef/EventRef/DocRef, RootBinding, RoleToken, StateToken, AcceptedStanding, RoleRecordV1, StoreId, StoreBinding, PublicationRef, NativeBefore) and **17 new**: `StepId`, `InvocationBinding`, `OperationInputV1` (13 closed action/input pairings, no details member), `V14Event` and `V14Refusal` (read from the pinned v14 JSON: 9 and 13 tokens), `ClockInputV1`, `PayloadEvidenceV1`, the nine event variants and `TrustEventV1`. Built by `claude-out/probes/build_event_shapes.py`.
- `JOIN-NOTES.md` — per-variant semantic joins, original vs new marked, the cycle rule, the `staged.by` rule with justification, and the list of input nodes still owed.
- `shape-check.json` — **46 cases** run with the exact-integer validator from the frozen reference-201 `canonical.py` copy (`d47f25db…b442`, hash asserted): every action's valid node; one valid instance per event variant (incl. accepted-stay, refused, pre-genesis ABORT with typed time-not-required, forward continuity, both restore variants); 20 rejections (wrong action/input pairing, `details` member, `stepId` 64 / boolean / float, invented action or `EV-*`, refusalReason pairing both ways, untyped not-required reason, embedded AFTER, `payloadDigests`, reset/termination/abort reaching TRUSTED, annotation carrying a role image, continuity naming an AFTER image, recovery without proof); and the `staged.by` rule on a three-role group plus two violations. Clock and authentication values in fixtures are **asserted toy inputs, not measured or verified**.

## Choices root should look at first
1. **`clock` on role-events is a reference, not a copy:** `{kind:"clock-write", by:EventRef}` to the same operation's earlier clock-write event, or the single typed `not-required` reason. This keeps v14's "clockObservation" information (one hop away, hash-bound) without duplicating observation data per role, and makes "which S4 decision authorised this dispatch" explicit. If root prefers an inline observation, the typed exemption still stands.
2. **`payloadEvidence` replaces `payloadDigests` by one bounded NodeRef** to the closure that retains them — per 222's instruction to "preserve the complete information via a bounded immutable descriptor, never silently truncate".
3. **`staged.by` = first canonical staging event** (notes §C) — no stage role, no tenth event kind, begun binding untouched because `staged` changes only with `staged.closure`.
4. **`batch-termination.cause` includes `COMMITTED`** — my addition, flagged; 215 does not say a COMMIT publishes one. Delete if not wanted.
5. **Continuity shape forbids any AFTER/carrier member**, making the cross-store acyclicity rule structural rather than conventional.
6. **`abort-termination-annotation.to`** excludes `ST-TRUSTED` and `ST-RECOVERY` by shape; equality with the ABORT event's `to` is a semantic join.

## What this is not
Not the complete event/capsule decoder; the input node kinds in notes §D are named prerequisites only. JSON Schema cannot express: same-descriptor/earlier-than ordering, equality joins (`before`, `batch`, `to`), sortedness of `writes`, role/state applicability, or acyclicity — all listed as joins. No model of these joins was written here; 226's conditional model still rejects null-`roleChange` entries (my r2 O-1), so the annotation/batch-termination/continuity joins remain unexercised anywhere. This is my own draft: it has had no independent review.
