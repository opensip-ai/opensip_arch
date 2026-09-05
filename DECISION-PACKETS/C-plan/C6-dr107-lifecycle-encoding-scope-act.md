# C6 — DR-107 / lifecycle encodings: what remains after D-293

Measured at HEAD `f3456575071928022a1f0e3a77e531a87157b365` (last COORD heading `## D-294`).
file 08 `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`; COORD
`31746810f9be78f697d66eb94d9cd50a95a51218998f97a154596363039fb9b6`;
`DECISION-PACKETS/C5-9-reserved-encodings-owners-units.md` `735720d9f4df7bba5717f78bb558f378edb9f825971cb60b20ed8cdf07a58e2b`.

---

## 1. What D-293 already decided, and what remains

**COORD `## D-293`, Decision item 7, C5/C6 sentence (verbatim, COORD lines 16249–16253):**

> `7. **C5–C9.** C5/C6: reviewed architecture-scope acts classify the`
> `   reserved encodings; no concrete encoding becomes post-Condition-5`
> `   work without an express scope/eligibility successor and a`
> `   successor-join remeasurement; live file 04's "same-filesystem`
> `   atomic rename or a reviewed equivalent" rule stands.`

The adopted C6 detail (`DECISIONS-RECOMMENDED.md` `42f27394…` §C5–C9, Claude round 2, verbatim):

> `- **C6 DR-107:** the same architecture-scope/eligibility sequence for the on-disk formats, lock grammar, lease, solver, layout. **No new atomic-rename-equivalent admissibility policy** — live file 04 already permits "same-filesystem atomic rename or a reviewed equivalent" and any successor must prove the recorded properties regardless of mechanism (my round-1 addition withdrawn).`

Codex round 2 (AGREE), verbatim: `preserve the live atomic-rename-or-reviewed-equivalent rule.`

| Limb | Remaining record act |
|---|---|
| **(a) a reviewed DR-107 architecture-scope act classifying the reserved mechanisms as implementation encodings** | **One act.** Content supplied by D-293; nothing needed from the owner |
| **(b) express scope/eligibility successor + successor-join remeasurement** | **Conditional, not now** (same as C5) |
| **(c) no new atomic-rename-equivalent admissibility policy** | **A prohibition on the act**, not an act. The successor must **not** decide which equivalents are admissible on the D-002 platforms — the orchestrator's round-1 proposal to do so was **withdrawn** |
| **(d) `OBL-ENCODING-RESERVED` stays leftoverDesign true** | **No act.** It already is |

---

## 2. Current artifacts

### 2.1 File 08 row (line 289, verbatim)

> `| DR-107 | Project/operation lock and multi-version generation semantics | Lifecycle + versioning | [Operations](04-lifecycle-delivery-and-operations.md) | DR-G18 crash-point harness; concurrent conflicting locks; immutable installs; leases/refcounts; reference-safe GC/removal; atomic dependency/state closure and migration | PROPOSED-CLOSED-FOR-REVIEW | Still hard blocker until reviewed successor and DR-G18 harness acceptance |`

Owner cell: `Lifecycle + versioning`. Status cell: `PROPOSED-CLOSED-FOR-REVIEW` — file 08's own legend
(`## How to use the register`): `` `PROPOSED-CLOSED-FOR-REVIEW` — V2 prose now addresses the review finding, but
no binding successor or qualification is implied. `` HANDOFF line 25: `DR-107 remains
`PROPOSED-CLOSED-FOR-REVIEW`. Do not flatten to OPEN.`
Gate row **DR-G18** (line 354), owner cell: `Lifecycle + storage + versioning`; status `OPEN`.

### 2.2 The contract carrying the reservation

`docs/coop/artifacts/lifecycle-generation-contract.v2.json` — sha256
`a5f9d6a35f83d64687cdd2a00ec3106251ae407e54a5538727c086dd8f9ab77b`; `$.status` = `"CANDIDATE-NOT-APPLIED"`,
`$.reviewStatus` = `"AWAITING-INDEPENDENT-REVIEW"`, `$.binds` = `"NOTHING"`; recorded at **`## D-107`**
(`Concrete journal/lock/lease encoding remains reserved. Generation-rollback remains distinct from DR-110
self-update rollback. No lock is producible.`).

Verbatim, the reserving JSON paths:

```
$.mechanismReservation.file04Verbatim = "The concrete lock/journal/lease mechanism is open, but a successor that cannot\nprove every property fails DR-107."
$.mechanismReservation.reserved = ["on-disk journal format", "lock file grammar beyond DR-103 lockSchema", "lease implementation (fcntl, sqlite, custom)", "solver algorithm", "filesystem layout"]
$.mechanismReservation.failureRule = "A later implementation successor that cannot prove P-1..P-8 fails DR-107, regardless of mechanism choice."
$.crashSafety.doesNotChoose = "The reviewed equivalent of atomic rename is reserved. Fail-closed quarantine is required; the on-disk quarantine format is reserved."
$.crashSafety.rules[1] = "Publication requires durable staged files/directories/journal, same-filesystem atomic rename or a reviewed equivalent, and recovery at each write/fsync/rename/pointer transition."
```

**So the reserved set is seven members:** the five in `$.mechanismReservation.reserved`, plus (i) the reviewed
equivalent of atomic rename and (ii) the on-disk quarantine format from `$.crashSafety.doesNotChoose`.

### 2.3 The current DR-107 leftover-join and the obligation

`docs/coop/artifacts/lifecycle-leftover-join.v4.json` — sha256
`bcc76ee3d99c88c258496dcc5591682d4ad655e06049b802a383ba03d3f1ddfb`; `$.version` = `4`; `$.date` = `"2026-08-24"`;
`$.status` = `"CANDIDATE-NOT-APPLIED"`; `$.registerRow` = `"DR-107"`;
`$.file08StatusToken` = `"PROPOSED-CLOSED-FOR-REVIEW"`; `$.head` = `"ebb7889d29f0cc6b9e6a1292a72db804f11307fd"`;
`$.file08Pin.sha256` = `e503b75b…` (**live**).
Recording heading: **`## D-275 — Record lifecycle leftover-join.v4 as DR-107 leftover remasurement`**
(`ADOPTED 2026-08-24`; Stage A dual ACCEPT 0/0; Stage B dual CONSENT 0/0).

`$.summary` (verbatim, in part): `"leftoverDesign": ["OBL-G18-FX-AUTHORING", "OBL-ENCODING-RESERVED"]`,
`"deferredOrRidesElsewhere": ["OBL-DR110-BOUNDARY"]`, `"requiredNowUnchanged": 28`, `"journalInvented": false`,
`"classAOpened": false`.

The obligation to remeasure, verbatim (`$.obligations[5]`):

```
{
 "id": "OBL-ENCODING-RESERVED",
 "leftoverDesign": true,
 "existingGate": "none",
 "executionObligationOwnerToday": "none",
 "rideStanding": "not-capable-of-riding",
 "reason": "Contract v2 reserves the reviewed equivalent of atomic rename and the on-disk quarantine format. G18 occupancy names crash-injection sites and does not choose an on-disk journal format, lock-file grammar, lease API, solver, filesystem layout, or reviewed-equivalent of atomic rename. Those mechanisms remain reserved. This join does not invent them. g18 leftover-join.v5 does not steal OBL-ENCODING-RESERVED. This join does not close it."
}
```

`$.proposedLaterWork[2]` = `A later implementation successor may choose a journal/lock/lease mechanism. That
successor must still prove the live file 04 properties. This join chooses none.`
`$.proposedLaterWork[3]` = `A later DR-110 disposition must draw the generation-rollback versus
self-update-rollback boundary. This join does not record that disposition.`

---

## 3. Precedent

Identical to C5 §3, and read the same way:

- **No recorded sub-row scope-classification act exists.** The two deferral shapes on record (`## D-010`
  DR-130 row-level; `## D-006` clause 5 / DR-G05 number-level) both wrote into file 08.
- **The COORD-only decision template is `## D-294`** (subject = its own turn-3 draft
  `9be8f7db1dc9b6c1137c899ccfffbbd9d769ff3c25869526721cb40022fd5f05`; `RULE-GOVERNED`; three turns to CONSENT;
  turn-1 Codex raised two MUST-FIXes, `CODEX-D294-MF1`, `CODEX-D294-MF2`).
- **The lineage recording form is `## D-275`**, Decision (verbatim, in part): `Record leftover-join.v4 as DR-107
  leftover remasurement after D-274. The candidate binds NOTHING. DR-107 stays `PROPOSED-CLOSED-FOR-REVIEW`.
  leftover-design of OBL-G18-FX-AUTHORING and OBL-ENCODING-RESERVED remains on leftover-join.v4. … Does not
  invent a journal. … Does not steal OBL-G18-FX-AUTHORING as a GATE closure. … Does not SATISFY DR-107. Does not
  flatten DR-107 `PROPOSED-CLOSED-FOR-REVIEW` to `OPEN`.`
  Its Stage A and Stage B Claude reviews returned three unlabeled `observationsNotFindings` strings each and no
  identifiers; Codex returned empty lists both stages — D-275 records this precisely and adds
  `This entry recites those Claude observations as strings. It does not invent a Claude identifier.`
- **What reviewers attack in successors of this era:** the deictic-speaker class
  (`CLAUDE-PTLJ-V8-SF1` / `CODEX-PTLJ-V8-SF1` / `CMLJ-V8-SF1`), false landing provenance
  (`CODEX-LQLJ-V4-SF1`: `"Both historical repairs are attributed to the wrong landing artifact"`), and
  self-description that the diff contradicts (`CLAUDE-DCLJ-V8-SF2`; `CMLJ-V8-SF2`).

---

## 4. The successor's minimal diff

### 4.1 The COORD entry (the act's substance)

**Records, and only this:** that the seven reserved members of `lifecycle-generation-contract.v2` (`a5f9d6a3…`)
— `on-disk journal format`, `lock file grammar beyond DR-103 lockSchema`,
`lease implementation (fcntl, sqlite, custom)`, `solver algorithm`, `filesystem layout`, the reviewed equivalent
of atomic rename, and the on-disk quarantine format — are **implementation encodings**; that
`$.mechanismReservation.failureRule` remains the acceptance bar regardless of mechanism; that
**live file 04's rule stands** (`same-filesystem atomic rename or a reviewed equivalent`); and that the
classification has **no Condition-2 or D-056 eligibility effect** without a separate reviewed act and a
successor join (D-293's cross-cutting clause).

**Must NOT record:**
- Any concrete mechanism. The C5–C9 packet §C6 measured: `**None in the record.** The contract names example
  lease implementations only as a parenthetical enumeration — "(fcntl, sqlite, custom)" — inside the *reserved*
  member; that is not a candidate. No journal format, quarantine format, or atomic-rename equivalent is named
  anywhere.` The seven members remain **explicit named open decisions**.
- **Any admissibility policy for atomic-rename equivalents.** D-293: `live file 04's "same-filesystem atomic
  rename or a reviewed equivalent" rule stands.` The round-1 proposal to settle admissibility was withdrawn in
  round 2 (`my round-1 addition withdrawn`), and round 2 is what D-293 adopted.
- Any flattening of `PROPOSED-CLOSED-FOR-REVIEW`.

### 4.2 Optional `lifecycle-leftover-join.v5.json`

- `$.obligations[5].reason` extended to cite the classification act; `leftoverDesign` **stays `true`** with
  `existingGate`, `executionObligationOwnerToday`, `rideStanding` byte-identical.
  `$.summary.leftoverDesign` stays `["OBL-G18-FX-AUTHORING", "OBL-ENCODING-RESERVED"]`.
- `$.file08StatusToken` stays `"PROPOSED-CLOSED-FOR-REVIEW"` — **not** `OPEN`.
- **Cross-lineage citation refresh (D-294 Decision 3):** the current G18 GATE leftover-join is
  `g18-leftover-join.v6` (recorded **`## D-276`**), not `g18 leftover-join.v5` as `$.obligations[5].reason`
  says. Custody at recording under D-294 Decision 1; refreshed if a successor issues for another reason.

---

## 5. Prohibitions

From **D-293**: `This entry marks nothing `SATISFIED`. It does not edit file 08. It does not open D-056 Class A.
It does not amend D-000 or D-056.` and, for this item specifically,
`live file 04's "same-filesystem atomic rename or a reviewed equivalent" rule stands.`

From **D-275** (verbatim): `Does not pin QUALIFIED. Does not invent fixture bytes. Does not invent a journal.
Does not invent a D9 code. Does not invent a section 7.1 recipe. Does not steal OBL-G18-FX-AUTHORING as a GATE
closure. Does not occupy the identifier. Does not SATISFY DR-107. Does not flatten DR-107
`PROPOSED-CLOSED-FOR-REVIEW` to `OPEN`. Does not flatten DR-118 `DECIDED-V1-NOT-INTEGRATED` to `OPEN`. Does not
reopen DR-119 SATISFIED. … Gate 1 Class A is not opened. Not SATISFIED. Required-now stays 28. Condition-4
effect is zero. … Does not execute G18. Does not rewrite occupancy v4. Does not edit file 08. Does not authorize
`docs/v2/implementation/`.`

From **D-107**: `Concrete journal/lock/lease encoding remains reserved. Generation-rollback remains distinct from
DR-110 self-update rollback. No lock is producible.`
From **D-106**: `Locks remain deferred to DR-111.` — and `component-manifest-schemas.v11` `$.lockSchema.purpose`:
`NO lock is producible until DR-111 closes` (so C6 also waits on **C3(ii)** for anything lock-shaped).

From **D-056**'s pinned subject (`dfb0c2af…`), gate 2 (quoted in full in the C5 file).

From HANDOFF: line 25 `DR-107 remains `PROPOSED-CLOSED-FOR-REVIEW`. Do not flatten to OPEN.`;
`Do not invent … a journal …`; `Do not steal … OBL-ENCODING-RESERVED …`;
`No file-08 cell edit for leftover/occupancy remasurements.`

---

## 6. Dependencies and ordering

- **Unblocked** for the classification act itself.
- **The lock limb is not.** `lock file grammar beyond DR-103 lockSchema` cannot be settled while
  `NO lock is producible until DR-111 closes` — i.e. it waits on **C3(ii)**, which waits on the owner. The
  classification act can still classify it as implementation scope; it cannot decide it.
- **Second bar on this row.** File 08's blueprint-impact cell: `Still hard blocker until reviewed successor and
  DR-G18 harness acceptance` — a bar the classification act does not touch.
- Same open questions as C5: **Q6** (file-08 echo or COORD-only — D-293 does not say) and **Q7** (whether a
  scope-classified but still-`leftoverDesign` obligation can ever satisfy D-056 gate 2 — no COORD entry or
  artifact rules on it).

---

## 7. Act shape

**Act C6-a — "DR-107: architecture-scope classification of the reserved lifecycle mechanisms"** (unblocked).

- **Stage A**: none required (COORD-only, the `## D-294` shape); optionally
  `docs/coop/artifacts/lifecycle-leftover-join.v5.json`.
- **Stage B**: `coordinator-decisions.D-NNN.draft.md` — dual CONSENT 0/0, up to three turns.
  Decision type: `RULE-GOVERNED` recording of the owner's D-293 disposition.
- **Then**: COORD-only append; commit `C-DNNN`.

**Estimated acts: 1** (2 if reviewers require the join successor as a separate recording).
