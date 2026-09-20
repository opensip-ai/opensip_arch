# Author fixture assistance — 232 reference-reader coverage (V-1)

**AUTHOR assistance for root; NOT independent approval, not a review of the corrected reader.** I
wrote fixtures and a harness only; I did not modify the reader, the schema or the 230 model. No
repo/candidate/earlier-review edit, no commit or push. A fresh review is owed later and must not be
mine-approving-mine.

## What was pinned

Live root files copied at the start into `pinned/` and used for every run (paths adjusted only by an
output-local directory layout; `pinned/m2-trust-layout-reference-201` is a symlink to my verified
reference-201 extraction, whose `canonical.py` the reader hash-asserts):

| live file | sha256 at pin |
|---|---|
| `m2-trust-reference-reader-draft-232/reference_reader.py` | 6f2a7497029e4a942209f38e513cb0bbea5acdcfb6e451e4c305ca9c9894cfea |
| `m2-trust-codec-integration-draft-231/private-trust-state.schemas.v1.json` (122 defs) | a3a0b4f468f0a43c2befa0e3157c6796b09128084a9a68c70b4fd04b43bd8520 (as root stated; the reader asserts it too) |
| `m2-trust-inputs-draft-230/trust_inputs_model.py` | 544a95e1eb7936b4e1795763dc9376d86b3f8b8e2bc1cf95fa61581232dfb375 |
| `m2-trust-inputs-draft-230/check_trust_inputs.py` | 2269dc397492cc9b4a312290f21488d53a121b7b2d715f9bd8f59d9abf7f3b08 |

At the end of the task all four live files were still byte-equal to the pins. The 230 model/check
were pinned and read for shapes only; they are not executed by this harness. The reader needs the
schema beside it, so the pinned schema is also copied into the pinned 232 directory (same bytes).
The pinned reader's registry has **132** rows (dump: `claude-out/io/registry-as-pinned.json`).

## Deliverables (`proposed/`)

| file | content |
|---|---|
| `build_coverage_fixtures.py` | fixture PRODUCER. Imports nothing from the reader. Prints JSON. sha256 dd42a15e…9f00 |
| `coverage-fixtures.json` | **71 literal fixtures**: `{name, root, value, expected}`; portable, no code needed to consume. sha256 e0a7be99…ee76 |
| `coverage_harness.py` | standalone: `coverage_harness.py READER.py FIXTURES.json`; prints a report; exit 1 on any mismatch, refusal, error or uncovered registry row. sha256 18587758…99d6 |
| `coverage-report-r1.json` | the run against the pinned reader |

**Result against the pinned reader:** 71/71 fixtures match their hand-written maps exactly (476
pointer→[type, target, collection] assertions); registry rows hit **132 of 132**; uncovered: none.

## Fixture coverage (all synthetic, shape-valid only)

- **Capsule:** maximal P2 (accepted heads ×3 with raw document pairs; all SIX roles with all six
  reference slots — `accepted.rootAdmission`, `accepted.by`, `revokedBy`, `quorumLostBy`, `reset.by`,
  `ceremony.batch/begin`, plus the INDEX catalog pair; staged payload; live batch with six members;
  history; source fence; event head; publication) and a P1 capsule with every nullable slot null.
- **Descriptor:** operation, two publication events (one with a full before/after `roleChange`, one
  null), and a maximal `afterProjection` (hits the separate `CapsuleAfterProjection` rows).
- **BeginBatch** (six `beginEvents`, six `beforeRoles`), **history** list-with-prior and merge,
  **closures** ordinary and recovery each with a present repair member, **roots** ordinary /
  recovery / 229 core anchor (six raw edges), **metadata admission**.
- **Time inputs:** S4 with source ordinary / recovery / none, S4.5 epoch, S4.5 challenge,
  restriction observation; S4 and epoch also through the `TimeEvidenceV1` root; both non-P0
  `ClockPhase` branches.
- **Operation shell:** all 14 actions (13 with a typed input edge, challenge with none).
- **Events:** role accepted + clock-write + payload closure; role REFUSED + observed-context; role
  accepted + not-required; clock-write s4 new-T, s4 kept-T, s4.5-apply, s4.5-challenge; creation;
  continuity forward-absent and ancestor-capsule; restore declared and recovery; standing-reset;
  private ceremony termination; abort annotation; batch termination with two closing events; a first
  event with null `previous`. Role, clock-write, standing-reset and continuity events are run through
  BOTH `TrustEventV1` and their own new root.
- **230 inputs:** creation input (→ `StoreMarkerV1`), store marker (no edges), target absence,
  restore declaration (two orphans), restore proof (two links + witness + two images), restriction
  evidence revocation-with-begin / quorum-with-begin-and-history / quorum-null-slots, three trust
  admission purposes (no edges), transition-intent alias (no edges).

Golden maps distinguish fixed EventRef targets from the generic union: `clock.by` → ClockWrite;
`reset.by` → StandingReset; `sourceFence.by` → Continuity; `accepted.by`, `revokedBy`,
`quorumLostBy`, `ceremony.begin`, `staged.by`, `beginEvents.*`, termination `begin`, annotation
`abort` → RoleEvent; `previous`, `eventHead`, `sourceEventHead`, publication `event`, batch `closing`,
live-batch `members.*.by` → generic `TrustEventV1`.

## Negative controls (the harness can fail) — `claude-out/io/control-*`

1. One expected target changed (`reset.by` → generic): exit 1, reports exactly that pointer as `different`.
2. Continuity fixtures removed: exit 1, lists the six uncovered `ContinuityEventV1` rows.
3. Same fixtures against the FROZEN 232 r2 reader: exit 1 — 34 match, 19 refused (new root types /
   pending codecs), 18 mismatch (its generic EventRef targets). So the maps do bind the V-2 fix.

## Independence — stated honestly

The `expected` maps are written by hand in the producer from owner prose (227 EVENT-JOINS,
PROOF-NODE-JOINS, TIME-INPUT-JOINS; 230 joins) and root's request text; no expectation is computed
by, or copied from, the reader's output. BUT: I had dumped the pinned registry (owner, schema path,
target) to know which 132 rows needed covering BEFORE writing the maps, and the role/heads/staged/
batch maps are produced by small hand-written helper functions reused across fixtures. So this is
not a blind second implementation: agreement on 476 assertions shows the reader matches my reading of
the owners, and a shared misreading would not be caught. One first-run failure was MINE (an invented
refusal token, fixed to a v14 vocabulary member); `claude-out/io/harness-try1.json` is preserved.

## Ambiguities and observations for root

1. **A time input carries the OLD T as an edge.** `S4EvaluationInputV1.beforeClock` and
   `RestrictionObservationInputV1.beforeClock` embed the before `ClockPhase`, so
   `/beforeClock/timeEvidence` is extracted as a `TimeEvidenceV1` NodeRef. That is a true reference in
   the bytes, but a graph walker that follows it eagerly re-creates the "missing old T blocks
   S4.5 / safe ABORT / restrictive observation" problem one hop later. Scope-sensitive traversal
   must treat this pointer like the capsule's own `clock.timeEvidence`.
2. **Role records inside events and descriptors are full reference carriers.** A role event's
   `before`, a `roleChange` before/after and `BeginBatch.beforeRoles` each contribute up to nine
   edges per role. Correct, but it means historical images multiply edges; the 131072 per-record
   edge limit is per record, not per graph.
3. **Generic EventRefs that could be narrowed with an owner decision:** `LiveBatch.members.*.by`
   (BEGIN, or the interrupting REVOKE/QUORUM role event — both RoleEvent? or may a private termination
   appear?), `BatchTermination.closing[]` (mixed by design), `sourceEventHead`/`eventHead`/`previous`
   (any kind). I kept them generic exactly as root stated; only the first looks narrowable.
4. **Coverage is per registry row `(owner definition, schema path)`, not per embedding.** A
   `RoleRecordV1` row counts as hit whether reached through a capsule, a descriptor or an event. The
   fixtures do reach it through all of those, but `hits == registry` alone would not demand it.
5. `not-required` forces `before.accepted == null`, so that fixture cannot carry the accepted slots;
   they are covered by the other role fixtures.
6. `StoreMarkerV1` and the three `TrustAdmissionInputV1` purposes, `TransitionIntentInputV1` and the
   challenge operation have NO reference edges; their fixtures assert an empty map (no phantom edge).

## Not claimed

No native, crypto, custody, publication, accepted-standing or lifecycle-reachability meaning. Values
are not reachable states (e.g. every role in RECOVERY with every slot set). Digests are hashes of
readable tags; no referenced object exists. `decode_edge` (target re-hash, forged-row refusal,
locator binding) is NOT exercised by this harness — it is root's corrected code and needs its own
cases. Root's own check corpus was not run as a claim.

## Reuse

`python coverage_harness.py <reader> coverage-fixtures.json` from any layout where the reader finds
its schema and reference-201 sibling. To extend: add a `fixture(...)` call in the producer with a
hand-written map, regenerate the JSON, re-run; a new registry row without a fixture fails the run.
