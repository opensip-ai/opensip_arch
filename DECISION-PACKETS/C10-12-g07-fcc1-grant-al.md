# C10–C12 evidence packet

Planning only. D-314 item 20 (Q16) authorized this packet. It authors
no fixture byte, records no successor, proposes no COORD entry, and
decides nothing. Every claim cites a path, a sha256, and a JSON path
or a file-08 line.

Measured at HEAD `8787d6ded31776a645b0a45f9f7a79b6c42513e2`
(last COORD heading `## D-341`). Date from the clock: 2026-08-31.

| Pinned source | Path | sha256 |
|---|---|---|
| file 08 | `docs/v2/architecture/08-decision-and-readiness-register.md` | `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e` |
| COORD | `docs/coop/COORDINATOR-DECISIONS.md` | `2a61a842ec9a7dd3191bdd2589336aae6a96a2766525dc7c7c3427754b74e3e7` |
| agreed recs | `DECISIONS-RECOMMENDED.md` | `42f27394746d4aac569a09a01da719c0cf318cf114086635e73097a6add97370` |
| D-314 rec r2 | `DECISION-PACKETS/G-owner-residuals.claude-recommendation.r2.md` | `a96b868e78ae5ed101b36c471963b00649b42047faf0e22359a682937d5f0ace` |
| exact-bytes leftover-join.v7 | `docs/coop/artifacts/exact-bytes-leftover-join.v7.json` | `2f73148e1fe6e1b0a734ba92978e876bb0594f5770f5ac23d1ab1fe3dd1d0df7` |
| G07 occupancy v4 | `docs/coop/artifacts/harness.DR-G07.exact-bytes.v4.json` | `99be421cd11a7524c87ee56b31b1c3b8335d8156bdb0d27a3a94ddddae7a56ed` |
| g07-coverage-domain.v1 | `docs/coop/artifacts/g07-coverage-domain.v1.json` | `7ea413859b5a77e8a8091839f5f06d76b990ee37cbafc0ddc7e9196f47dfe6a7` |
| doctor-actor leftover-join.v12 | `docs/coop/artifacts/doctor-actor-leftover-join.v12.json` | `0c0b894ffb5f80981282455a99153975e3fac30ade076d2596efb2b4fcf1a9e9` |
| permission leftover-join.v12 | `docs/coop/artifacts/permission-leftover-join.v12.json` | `496b75c60c6540c3272c2c57d86c43ca71a77a1ed2eceaa6e3a1c49251374fb3` |
| state-class leftover-join.v5 | `docs/coop/artifacts/state-class-leftover-join.v5.json` | `30a6fc91984b0a2b330a47f9df813e38f827d300f10713b273d6128706bb7e81` |
| anti-lockstep leftover-join.v6 | `docs/coop/artifacts/anti-lockstep-leftover-join.v6.json` | `bebf1103b8640b6c9e4e0adb7dc7bca9fef1e6857df6b6f03eb6c05eafb134af` |

C4 standing at this HEAD, not decided here: D-341 recorded C4-b.
C4-c (`platform-tcb-contract.v46`) is unrecorded. Stage A dual ACCEPT
0/0 with a grade split (Claude `NOT SUSTAINED` CLAUDE-V46-A1;
Codex `SUSTAINED FOR APPLICATION`). This packet does not close C4-c
and does not treat TCB `identifierEnum` as the G07 coverage domain.

D-293 Decision 6 and 7 name no C10/C11/C12 disposition. D-314 item 20
(Q16) opens this packet now and takes the substantive decisions only
after it exists, sequenced after the C4 and C8 chains.

---

## C10 — G07 filesystem coverage list

**Register.** File 08 line 343, DR-G07 owner cell `Security + platform`,
status `OPEN`, harness cell names `supported filesystems`.

**Current GATE leftover-join.** exact-bytes leftover-join.v7 (D-286).
`$.summary.leftoverDesign` =
`["OBL-G07-FX-AUTHORING", "OBL-FILESYSTEM-COVERAGE"]`.
`$.obligations` OBL-FILESYSTEM-COVERAGE leftoverDesign true,
existingGate none, executionObligationOwnerToday none, rideStanding
not-capable-of-riding. Reason: occupancy v4 `filesystems.standing` is
`UNPOPULATED`; g07-coverage-domain.v1 recorded that no live governing
source exists; that source-search limb is OBL-G07-COVERAGE-DOMAIN-ACT,
leftoverDesign false; leftover-design of later populating the set
remains.

**Occupancy v4 (D-210)** `$.filesystems.standing` = `"UNPOPULATED"`.
`$.filesystems.laterAct` names g07-coverage-domain.v1 as the dedicated
act, limb taken `record-that-no-live-source-exists`, set remains
unpopulated, choosing a further populating act's owner is a separate
decision, and that act is not G22 TCB filesystem-selector population.
`$.filesystems.matrixStanding` = INCOMPLETE on the filesystem axis until
a later act supplies the set. `$.filesystems.notG22TcbSelectors` forbids
treating TCB v45 `identifierEnum` as the G07 coverage domain.

**Coverage-domain act.** g07-coverage-domain.v1
`$.leftoverDesignStanding.OBL-FILESYSTEM-COVERAGE.leftoverDesign` true.
`$.proposedLaterWork` includes: a later owner decision may populate the
set if a live source appears; this act does not invent that set and
does not choose that owner. `$.doesNot` includes `Does not populate a
filesystem allowlist` and `Does not invent filesystem type tokens`.

**D-293 Decision 8.** G07 (with every current same-id ROW twin) is
reserved to the owner. D1 does not populate this list.

**Not in the record.** Any filesystem type name as a G07 coverage-domain
member. Any owner of a later populating act. Any live governing source
for the set.

**Options for a later owner act (not chosen here).** (a) populate the
set from a named live governing source; (b) park with a named trigger;
(c) leave UNPOPULATED. File 08's G07 owner cell is `Security + platform`;
occupancy v4 says choosing the populating act's owner is a separate
decision. This packet assigns neither.

**Does not collapse with C4.** G22 TCB `filesystemWhereItAffectsResolution`
is a platformProfile selector. G07 `supported filesystems` is an
exact-bytes coverage domain. Occupancy v4 `notG22TcbSelectors` and
g07-coverage-domain.v1 `doesNot` both refuse the collapse.

---

## C11 — FC-C1 joint-owner recording; BLK-1..4 routing

**Register.** File 08 line 287 DR-105 owner `Security + platform owners`,
status OPEN. File 08 line 296 DR-114 owner `Operability + security`,
status OPEN.

**D-032 (ADOPTED 2026-08-13).** Host-under-instruction is outside DR-105.
Doctor consent is not a grant. Component tails stay in DR-105.
Host-actor owners: Operability + security jointly with Security +
platform owners. A scoped host-effect authorization contract is
necessary, not sufficient, before CA-1 host head, CA-2, CA-3, or host
CA-4 is exercisable. BLK-1/2/3/4 STILL-ROUTED. BLK-5 DISCHARGED.
BLK-6 DISCHARGED-AS-INAPPLICABLE for the named host default. BLK-7
REPAIRED-IN-V4. Applies no candidate.

**Current ROW leftover-joins.**

- doctor-actor leftover-join.v12 (D-285 class; sha above). leftoverDesign
  includes `OBL-FC-C1`, `OBL-BLK-1`, `OBL-BLK-2`, `OBL-BLK-3`,
  `OBL-BLK-4`. `$.proposedLaterWork` includes `A later joint-owner act
  may record FC-C1. This join is not that act.`
- permission leftover-join.v12 (D-283). leftoverDesign includes the same
  five still-routed ids plus G09 authoring leftovers.

| id | leftoverDesign (both joins) | executionObligationOwnerToday (doctor-actor leftover-join.v12) | routing sentence |
|---|---|---|---|
| OBL-FC-C1 | true | Operability + security jointly with Security + platform owners | joint-owner FC-C1 recording remains unmet; existence of doctor-actor-join-integration-contract.v8 / host-effect-authorization.v25 is not that recording |
| OBL-BLK-1 | true | none on this row alone | CA-2 execute-anything gap STILL-ROUTED; DR-119 necessary and not sufficient |
| OBL-BLK-2 | true | Operability + security jointly with Security + platform owners | four tokenless CA-3 effects STILL-ROUTED; KEYCHAIN deferred to DR-108 |
| OBL-BLK-3 | true | Operability + security jointly with Security + platform owners | host outcome vocabulary versus doctor-contract.v4 effectOutcome STILL-ROUTED |
| OBL-BLK-4 | true | Operability + security jointly with Security + platform owners (permission leftover-join.v12: Security + platform owners) | grant journal against doctor's read-only fixture STILL-ROUTED; host consent is not a journal grant |

**Not in the record.** The FC-C1 joint-owner recording itself. A
discharge of BLK-1..4. A later CA-2 decision that would make CA-2
exercisable.

**Options for a later owner act (not chosen here).** Record FC-C1 as
the joint-owner act both joins name; or leave it unmet. Route each
BLK-1..4 to a named later D-000 or leave STILL-ROUTED. This packet
records none of those acts.

D-293 Decision 8 also reserves `OBL-JOIN-FX-AUTHORING`,
`OBL-R10-AUTHORING`, `OBL-R6-AUTHORING`, and the G09/DR-105
decision-record envelope to the owner. Those are adjacent leftoverDesign
members on these joins; this packet does not populate them.

---

## C12 — DR-124 grant-journal assignment; DR-127 AL-1/2/5 and AL-3 execution routes

### C12-a grant-journal

**Register.** File 08 line 306 DR-124 owner
`Semantic/evidence/storage/lifecycle owners`, status OPEN.

**Current leftover-join.** state-class leftover-join.v5 (D-333).
`$.obligations` OBL-GRANT-JOURNAL leftoverDesign true, existingGate none,
executionObligationOwnerToday none, rideStanding not-capable-of-riding.
Reason: D-117 records grant-journal assignment remains a proposed
supersession; state-class-contract.v11 whatThisDoesNotDo:
`Does not apply SUP-124-GRANT-JOURNAL by existing. Owner concurrence is
required at recording.` Undecided assignment is leftover-design (D-056).

**Not in the record.** Owner concurrence at recording. A grant-journal
envelope. Application of SUP-124-GRANT-JOURNAL.

**Options for a later owner act (not chosen here).** Concur and record
the assignment; or leave leftoverDesign true. This packet does neither.

### C12-b AL execution routes

**Register.** File 08 line 309 DR-127 owner
`Protocol + versioning + release owners`, status OPEN.

**Current leftover-join.** anti-lockstep leftover-join.v6 (D-326).
`$.summary.leftoverDesign` =
`["OBL-HOSTILE-GOLDENS", "OBL-AL3-CORE-ROLLBACK", "OBL-AL1-AL2-AL5"]`.

- OBL-AL1-AL2-AL5 leftoverDesign true. Reason: v7 executionRoutes
  AL-1/AL-2/AL-5: selection/qualification evidence rides a reviewed
  owning gate such as DR-G16 only for the exact cases that accepted
  contract covers; uncovered AL-1/AL-2/AL-5 execution remains at
  DR-127. Occupancy v5 is the current G16 occupancy remasurement
  (D-215). This join does not add a DR-G* row and does not force a
  ride.
- OBL-AL3-CORE-ROLLBACK leftoverDesign true. Reason: v7
  executionRoutes AL-3-core-release-byte-rollback: reviewed DR-110
  owning contract and its applicable named gates, or remains this row
  until that contract exists. D-107/DR-G18 expressly exclude
  core-release-byte rollback. self-update-repair-contract.v3 is
  recorded at D-121 as DR-110 leftover T2-02.
- OBL-AL3-COMPONENT leftoverDesign false: rides G18 / accepted D-107.
- OBL-AL4 leftoverDesign false: rides G18.
- OBL-HOSTILE-GOLDENS leftoverDesign true because seven classes carry
  unenumerated within-class quantifiers after D-300's sixteen citation
  implementations (D-314/D-315 G3-HOSTILE: those sets stay named-open;
  supply no per-class totals).

**Not in the record.** An owning-gate ride that covers every AL-1/AL-2/AL-5
case. A DR-110 contract that owns core-release-byte rollback. Per-class
totals for the seven hostile within-class sets.

**Options for a later owner act (not chosen here).** Name a reviewed
owning gate for uncovered AL-1/AL-2/AL-5 cases; or leave them at
DR-127. Name a DR-110 successor for AL-3 core-release-byte rollback; or
leave leftoverDesign true. This packet names no gate and no contract.

---

## What this packet does not do

It does not edit file 08. It does not append COORD. It does not SATISFY
DR-G07, DR-105, DR-114, DR-124, or DR-127. It does not open D-056 Class A.
It does not populate a filesystem list. It does not invent APFS, HFS+,
ext4, XFS, or any other filesystem type token. It does not treat TCB
`identifierEnum` as the G07 coverage domain. It does not record FC-C1.
It does not discharge BLK-1..4. It does not apply SUP-124-GRANT-JOURNAL.
It does not add a DR-G* row. It does not force a ride onto G16. It does
not invent a D9 code. It does not authorize `docs/v2/implementation/`.
It does not close C4-c. It does not SATISFY DR-117, DR-131, or DR-133.

Substantive decisions wait on the owner after this evidence exists,
sequenced after the C4 and C8 chains (D-314 item 20).
