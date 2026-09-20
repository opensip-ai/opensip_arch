# Independent scoped review — frozen trust-codecs-wip-227-r7 (proof joins, typed DAG, empty-event)

Scope: root's corrected metadata joins, the typed iterative DAG, and the empty-event correction.
Not reviewed: unchanged event/time variants, core anchor (incomplete pending 229), crypto, custody,
native producers. **No cumulative, schema, protocol or readiness approval.** My earlier author
proposal is not evidence for anything here. No repo/product edit, commit or push; output only here.

## Verification and reproduction

- Archive `bc16aa0c…4dc6`, 144196 bytes: pin matched; all 165 `subject.json` members matched by
  path, sha256 and length, read from the tar before extraction; no non-regular/unsafe member;
  re-verified at the end (`claude-out/pin-verification.json`, mode `re-verified`).
- Reproduction ran in `claude-out/run/subject` (a copy of the extraction WITHOUT `proof-mutants-r2`,
  because the runner creates it with `exist_ok=False`). `check_proof_joins.py` resolves
  `T = S.parent`, so I staged the exact `canonical.py` (d47f25db…, the hash the script itself
  asserts) at the same relative path under `claude-out/run/`. **No script was edited; there is no
  redirect diff.** Nothing was run inside `inputs/` or the source trial.
- Results: 45 cases → output **byte-identical** to `proof-join-check-r4.json`; 15 variants
  rejected + baseline → regenerated `proof-mutants-r2/` **identical** to the frozen directory
  (`diff -rq` clean, including `results.json`); capsule model → **byte-identical** to
  `shape-join-model-r3.json` (60 cases).
- `shape_join_model.py` imports `canonical.py` from an absolute LIVE path with **no hash
  assertion** (unlike `check_proof_joins.py`). I checked the live file equals d47f25db… before
  running, so this run is sound; the frozen script itself would not notice drift. (L-4)

## Findings inside the claimed scope

### F-1 (medium) — the typed edge table refuses references the frozen 227 schemas contain

`EDGES` is described as "allowable direct dependency fields". Four references that exist in the
frozen r7 schemas are refused `edge-type` (`claude-out/io/adversarial-proof-joins.json`, A1–A4):

| reference in frozen r7 | table entry | result |
|---|---|---|
| `S45EpochInputV1.acceptedAuthority` (time → root) | `time: {image, closure}` | refuses |
| `S45EpochInputV1.revocationHistory` (time → history) | same | refuses |
| `TrustCapsuleV1.staged.closure` (image → closure; `StagedPayload.closure: NodeRef`) | `image: {descriptor, time, root, metadata, history, batch, event}` | refuses |
| `RoleEventV1.payloadEvidence {kind:"closure", ref}` (event → closure; EVENT-JOINS l.32) | `event: {image, operation, time, event, batch}` | refuses |

So the model cannot represent an S4.5 epoch operation, any capsule image with a staged payload,
or any payload-bearing role event — the recovery path the graph exists to order. None of the four
adds a cycle (each target is upstream, as PROOF-NODE-JOINS and TIME-INPUT-JOINS "Acyclicity" say).
The 45 cases do not notice because the only positive graph uses `time → image` and
`event → op/event/batch`. Also unplaced: `RestrictionObservationInputV1.restrictionEvidence`,
`ContinuityEventV1.targetBefore.absenceProof`, `CreationEventV1.creationInput`,
`RestoreEventV1.proof` — no node kind exists for them. **Action:** derive the table from the
schemas' NodeRef-bearing fields (one row per field, with its target kind) and add one positive
graph per operation family; a hand-written kind×kind table will keep drifting.

### F-2 (medium, test adequacy) — two new empty-event guards and five clock sub-conditions are unexercised

`shape_join_model.bad()` accepts any `Bad/ValidationError/ValueError` and never checks the reason.
For the four new negatives the ACTUAL reasons happen to be the intended ones (traced, see
`empty-event-mutation-r2.json` → `actualRefusals`). But mutation of the frozen text shows:

| guard removed / narrowed | result |
|---|---|
| `empty-event predecessor binding` (store, revision+1, `previous == digest(before)`) | **SURVIVES** |
| `empty-event head update stays retained` | **SURVIVES** |
| clock guard without `lastAccepted` / `anchor` / `recoveryEpochSerial` / `pendingRecoveryChallenge` | each **SURVIVES** |
| clock guard without the `timeEvidence` equality | **SURVIVES** |
| event-head, hidden-role, clock guard removed whole, clock guard without `evalHighWater` | killed |

The predecessor binding is the guard that makes the caller-supplied `before` trustworthy at all:
without it any convenient image satisfies the other four comparisons. It and the T/L/serial/
challenge conditions are exactly what README calls "unchanged … clock proof and recovery state",
yet nothing fails if they are deleted. (Removing `needs-before` raises `TypeError`, which is not a
semantic kill; the traced negative does hit that label.) **Action:** one negative per condition —
wrong `previous`, wrong revision, other store, P1 before-image, and one per clock field and T —
and make `bad()` assert the exact label, as `check_proof_joins.bad` already does.

### F-3 (low–medium) — closure join has no single-path/single-member rule

Owner model ADMITS (B2, B3, B5, B6): one signed path bound to two different digests across slots;
a metadata member whose path equals the direct `catalog` path with a different digest; an artifact
path equal to a metadata member path; and a recovery authorization BODY that is the same member as
`rootChain[1]`. A directory holds one file per path, so such a manifest cannot byte-verify at the
original import — but this join is also the HISTORICAL re-verification, and it rehashes by digest,
never by path, so it cannot see the contradiction. 215 r14 l.32 requires the authorization body
and envelope to "identify distinct admitted members"; the model checks only that the two PATHS of
the pair differ. **Action:** one global guard — every `(path)` across rootChain, catalog,
revocation, all slots, artifacts, repair and authorization is distinct, and each direct document
is a distinct member — with a negative per collision class. Cheap, and removes a class of
"two readings of one payload".

## Low observations

- **L-1 envelope pairing is by set membership.** Cross-swapping two LISTED envelopes between direct
  documents admits (B1). README/PROOF-NODE-JOINS state that envelope subject/raw-body joins are
  owed real admission, so this is inside an acknowledged boundary; I record it only because the
  case label `direct-envelope-must-be-listed` could be read as pairing. A listed outer envelope
  (B4) admits too but is unreachable with real bytes (a true hash cycle).
- **L-2 empty-event reachability is narrower than the prose suggests.** The guard freezes L and T.
  A shared-head update that accepts any document issued after L must advance L and write a new T
  (225), which is a clock-write event — so an empty-event head publication is lawful only when
  every newly accepted document's issue time ≤ L and S4's write-ahead F landed in an earlier
  revision. That is consistent, but it is unstated; worth one sentence so nobody widens the guard
  to "fix" a legitimate L-advancing import. Related question for the 226 owner, not a defect here:
  such a publication changes accepted heads with no entry in the event chain; the descriptor's
  operation node is then the only audit record of the change.
- **L-3 `topo(nodes, [])` returns an empty order** (A6). A caller that derives `starts` wrongly
  gets a vacuous pass; require a non-empty start set or return the visited count for the caller to
  compare with the required graph.
- **L-4 unpinned live import** in `shape_join_model.py` (above). Add the same hash assertion.
- **L-5 six clock-record fields are outside the guard by design** (`rootVersion`,
  `indexSnapshotVersion`, `revocationVersion` and the three accepted-document times may change in a
  head update). Correct, but their equality to the new heads is owed and currently nowhere checked;
  README says so ("Full shared guards still owed").

## Confirmed as claimed

- Raw-byte joins: manifest body is parsed from its retained bytes, must be canonical, and selects
  payload1/payload2 by closure scope; a recovery scope cannot ride payload1, payload2 cannot choose
  ordinary scope, legacy recovery-kind payload1 stays on the ordinary route (B8) — matches prose.
- Full metadata retention on both routes; exact repair typed-absence vs member; authorization pair
  and exactly-once envelope membership; artifact inventory/order/length; every retained blob
  re-hashed and length-checked under 4 MiB and the aggregate budget, charged before use.
- The traversal is genuinely iterative and correct: I reasoned through duplicate pushes (a stale
  copy of a node is always popped after that node finishes, so no false `cycle`), and the 2000-deep
  chain, diamond, self-cycle, successor-history cycle and precharge cases behave as labelled.
  Same-operation root→root and BEGIN/event ordering are admitted, as root's correction requires.
- The 15 mutants each die on the exact intended assertion; `typed-edges` correctly documents that
  it may meet the cycle guard first.
- Scope statements are honest: no case claims crypto, custody, publication proof or accepted
  standing; fixture ids are not hash claims; artifact captures are asserted inputs.

## Limitations of this review

Probes import the owner model unmodified and use its own toy fixtures; "ADMITS" means the toy
model admits, not that a real importer would. F-1 is judged against the frozen r7 schemas and
join notes only. I did not re-run or re-read the 67 event and 35 time checks, 215/222/225/226
owners, or the core-anchor material. My first probe run had two harness errors (a `pass`
replacement with wrong indentation, and a `TypeError` variant), both reported as
`ERROR-not-a-kill`, never as kills; the indentation one is corrected in `…_r2.py` and both outputs
are kept.

## Pins

`check_proof_joins.py` 5b423d24abf587e0cd6483c26c89c2488e60f11e31faaec818069cc907055fc4 ·
`shape_join_model.py` 9e2511c9c5bc21aefd0d10b72cd30e69314356d6403563aa63e4d90306066d27 ·
`trust-proof-nodes.v1.json` 64a52354278cce51d373de222304817b4c3e3c3beb665d6c36fc6316213a00a3 ·
`PROOF-NODE-JOINS.md` e44ed2b3e2b2d62221d0e6edc735b8715abe37b7f366fa1de4dc317e06767649 ·
`trust-event-shells.v1.json` 37d714fb96782e70c78fb03f620cb3334a639a6279becfc7df012715ec87c220 ·
`trust-time-inputs.v1.json` d308f4dd8c005bd0f30d7009f7ffd2b6ef522ad692532ad8c5739abd2ff568b5 ·
`canonical.py` d47f25db0fb09ceb84282a89fdf74055cb81ccb9de26f85a5a70b032b9a6b442
