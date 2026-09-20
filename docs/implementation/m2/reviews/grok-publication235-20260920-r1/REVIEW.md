# Independent bounded review — publication-event bindings 235 r1

ROOT follow-through on the 230 C2 / R9 / R10 remainder. **Not cumulative protocol approval, not
226/v14 semantic closure, not native custody or live census.** Prior completed reports in
`/tmp/opensip-implementation/reviews/grok-trust230r3-20260920-r1/` and
`/tmp/opensip-implementation/reviews/grok-reader232r4-index234-20260920-r1/` are untouched. No repo,
product, or candidate edit.

`bind_events` is a trusted reference helper over an owner-supplied logical role/head base and a
shared 230 `Work` reader. It is not a public security API and does not grant tokens. Accepted role
effects are returned as `pendingAuthenticatedRoleEffects` with standing `structural-bindings-only`.

## Verification and reproduction

- Frozen `publication-events-wip-235-r1` `112dc6a0…5468` (25584 B, 26 members): pin and every
  `subject.json` member verified from the tar before extraction; extracted copy re-verified after
  the runs.
- Sibling layout in the output tree only: already-verified 201 (canonical `d47f25db…b442`) and the
  already-verified 230 r3 model `45982508…42f8` plus its pinned `inputs/`. Schema 122 defs
  `a3a0b4f4…8520`. Python 3.12.13 `-I -B`. No live unpinned import, no third-party fetch.
- Regenerated `event-check-r3.json` **byte-identical** (41 cases). Regenerated
  `event-variants-r1/results.json` **byte-identical** (9/9). Regenerated
  `restore-bridge-check-r2.json` **byte-identical** (valid/nested-valid pass; link/witness/nested-bad
  refuse `event-store-operation`).
- `restore-function-230-before.py` is byte-equal to `admit_restore_proof` sliced from the pinned 230
  r3 model (`aa4b6e5c…f93c`). `restore_event_bridge.py`'s function is that body with only: `W.`
  qualification of `require/shape/node/reconstruct/descriptor_operation`, `bindings=[]`, **two**
  `B.bind_events` calls (every link, every terminal), and a structural result. Round-trip stripping
  those hooks restores the original function. Nothing else changed.
- Initial restore-bridge fixture used invented action `restore-declaration` (closed
  `OperationInputV1` shape-refuses it). Current fixture uses existing `acknowledge-restore`; the
  input kind remains `restore-declaration-input`. No new owner vocabulary. Fixture-alias beforeimage:
  `roleChange.before` is now a deepcopy so a later mutation cannot alias the descriptor row.

## Claimed literal bindings — hold

Every `TrustEventV1` union member is classified: six `NULL_KINDS`
(creation / clock-write / batch-termination / restore / continuity / abort-termination-annotation)
and three `ROLE_KINDS` (role-event / standing-reset / private-ceremony-termination). No union kind
is omitted.

On the unmodified helper:

- Event bytes go through 230 `Work.load` (rehash / cap / canonical / `TrustEventV1` shape).
- Locator: `event.store/sequence` equals the `EventRef`.
- `event.store` equals the descriptor store **and** `event.operation` equals `descriptor.operation`.
- Unique event sha256; previous/sequence chain from the supplied logical head.
- Null kinds forbid `roleChange`; empty `events` must keep the supplied head and all roles.
- Role rows bind `role/from/to/before`; `current[role]` must equal that before (ordered replay);
  `afterProjection.roles` and `eventHead` must equal the replay.
- Standing-reset: exact applicability and exact after-record (only `state`/`reset` change).
- Private termination: batch/begin binding, REVOKED BEGIN restriction preserved, cannot also reset.
- ABORT annotation must name an earlier **accepted** `EV-RECOVER-ABORT` in **this** descriptor and
  match role/from/to/batch.
- Accepted role-events append to `pendingAuthenticatedRoleEffects` and do not grant standing
  (probe: after `EV-QUORUM-OBSERVE`, role remains `ST-UNBOOTSTRAPPED`, pending length 1).

Shared `Work` is the same object through nested restore-proof traversal: exact nested budget admits;
one object short on that ledger refuses `work-objects`.

## C2 / R9 / R10 against the recorded 230 remainder

230 `descriptor_operation` is **unchanged**. The original helper still returns on same-store without
looking at events. Independent probes:

| probe | 230 `descriptor_operation` / `admit_restore_proof` | 235 `bind_events` / restore bridge |
|---|---|---|
| Same-store shell whose event.operation is a different NodeRef (C2 / X4) | **ADMITS** | `event-store-operation` |
| Extra chained event of a **different** operation (R9) | n/a (230 counts target-side continuity only) | `event-store-operation` |
| Extra chained event of the **same** operation | n/a | ADMITS (literal extra row of this D, not a foreign extra) |
| Synthetic restore link/witness/nested-link with `event.operation` ≠ descriptor.operation (R10-class) | **ADMITS all five shells** | refuses the three mismatched shells; valid direct (2 bindings) and nested (4) pass |

So the recorded gap is closed **at the 235 layer** when `bind_events` is actually invoked (the
restore bridge does so on every link and every terminal). 230 alone still admits the toy shells;
that is the demonstration, not a 235 regression.

## Remaining findings

#### F-1 (stated remainder, demonstrated) — roles/head only, not the rest of `afterProjection`

`bind_events` checks `afterProjection.{store,revision,previous,roles,eventHead}`. A shape-valid
`clock` drift with honest roles/head **ADMITS**. Whole-image clock/heads/history/staged/batch/sourceFence
joins remain the owed 226/215 owners named in README. Do not read a structural pass as complete
projection admission.

#### F-2 (stated) — 230 same-store helper is not replaced

Callers that only run 230 `descriptor_operation` still have C2. 235 is an additional bind, not a
patch of that function. Continuity/cross-store operation admission remains 230; this module is not a
blanket event-store waiver.

#### F-3 (stated) — pending list is an incomplete obligation

Accepted role effects are not authorized by event tokens. Clock/creation/batch/restore/continuity
input and effect owners, reset-cause authorization, BeginBatch / accepted-standing / root / time /
role guards, native collections, live census, proven-image admission, and v14 dispatch are all still
owed. Logical base is an upstream premise.

No omitted join was found **inside** the claimed locator/store/op/chain/role-replay/reset/term/ABORT
surface. `bind_events` compares operation NodeRefs and does not load the operation body; the restore
bridge still goes through 230 `descriptor_operation`, which does. Isolated `bind_events` assumes an
already-admitted descriptor, matching the "upstream inputs" contract.

## Verdict

- [x] Literal bindings hold on the claimed event-chain / role-replay / reset / termination / ABORT
  surface, using the real 9-kind `TrustEventV1` union rather than 226 toy action strings.
- [x] Restore bridge is the 230 r3 iterator plus two bind hooks and shared `Work`; original function
  retained.
- [x] Recorded 230 C2/R9/R10 mismatched-event admissions are refused once 235 is applied.
- [ ] **Not 226 semantic closure, not a grant, not cumulative approval.**

No harness failure. Empty r1 reports are retained failed/empty runs, not counted passing.
