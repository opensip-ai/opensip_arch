# C3 — DR-111 / compatibility windows: what remains after D-293

Measured at HEAD `f3456575071928022a1f0e3a77e531a87157b365` (last COORD heading `## D-294`).
file 08 `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`; COORD
`31746810f9be78f697d66eb94d9cd50a95a51218998f97a154596363039fb9b6`;
`DECISIONS-RECOMMENDED.md` `42f27394746d4aac569a09a01da719c0cf318cf114086635e73097a6add97370`.

---

## 1. What D-293 already decided, and what remains

**COORD `## D-293`, Decision item 6 (verbatim, COORD lines 16243–16245):**

> `C2 and C3 as agreed (the C2 matrix/corpus,`
> `threshold-approval and G13 sequence; the C3 live-file-08`
> `remasurement with coherent evaluable windows).`

"As agreed" resolves to
`DECISION-PACKETS/C1-4-reserved-numbers-security-quality.claude-recommendation.r2.md`
`44f51a5d36eb3f03c711112a50119ea67fb01b3a07d255ccbac5d51cc0485627` (round 3 says
`- **C2, C3:** unchanged from round 2.`), C3 bullet, verbatim:

> `- **C3 DR-111:** no isolated unit choice; remasure the compatibility leftover-join against live file 08 first (or in the same reviewed cycle), then have the file-08 Versioning authority record one coherent set of evaluable windows (unit, surface coupling, the four values) — if the values are not in hand, that is choice (b) or (c) above, not a partial setting.`

Codex round 3 (`0c2550ed…`): `Retain … the agreed C3 live-file-08 remasurement plus coherent evaluable windows.`

Two limbs, with very different standing:

| Limb | Status | Remaining record act |
|---|---|---|
| **(i) remasure the compatibility leftover-join against live file 08** | **Unblocked.** The current join pins a superseded file-08 digest (§2) — a token that must change | **One act, dispatchable today** |
| **(ii) one coherent set of evaluable windows (unit, surface coupling, the four values)** | **Blocked.** D-293 states no unit, no coupling and no value; the record holds none | **No act until the Versioning authority supplies them** (owner question, §6) |

The round-2 text expressly forbids the partial move: `no isolated unit choice … not a partial setting`. So the
unit **cannot** be recorded on its own, and limb (ii) is a single later act, not a sequence of four.

---

## 2. The artifact to succeed

`docs/coop/artifacts/compatibility-leftover-join.v2.json` — sha256
`33e4299d7f65bf37c2f5d54193e004c69d542d3f5da99417e1360efc2f8b7259`; `$.version` = `2`; `$.date` = `"2026-08-21"`;
`$.status` = `"CANDIDATE-NOT-APPLIED"`; `$.registerRow` = `"DR-111"`; `$.file08StatusToken` = `"OPEN"`;
`$.head` = `"f76aa872d91e071c83bd7b03dd650402518eda64"`; `$.liveGateOwners` is **absent** (DR-111 has no gate row).

**The stale token:**

```
$.file08Pin = {"path": "docs/v2/architecture/08-decision-and-readiness-register.md",
               "sha256": "f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1"}
```

Live file 08 is `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`. The C1–C4 packet §7 measured
the history: `git log -- docs/v2/architecture/08-decision-and-readiness-register.md` — commit `892236a`
(2026-08-20, D-169) is the file-08 version whose sha256 is `f909ddff…`; the only later file-08 commit is
`fc688b1` (2026-08-23, D-236, sha256 `e503b75b…`). D-177's recording commit is `afb115d` (2026-08-21).

Recording heading: **`## D-177 — Record compatibility-leftover-join.v2 as DR-111 leftover remasurement`**
(`ADOPTED 2026-08-21`; Stage A Claude ACCEPT `a0cef800…` 0/0, Codex ACCEPT `ba6c178b…` 0/0).

`$.summary.leftoverDesign` = `["OBL-NUMERIC-WINDOWS", "OBL-LOCK-JOIN"]`. Obligation objects, verbatim:

```
$.obligations[1] = {"id": "OBL-NUMERIC-WINDOWS", "leftoverDesign": true, "existingGate": "none",
 "executionObligationOwnerToday": "none", "rideStanding": "not-capable-of-riding",
 "reason": "v5 numericWindows is RESERVED: 'This artifact does not mint how long a reader is supported. Product/versioning sets numbers later. Alias-window numbers are D-012's, not this row's.' Undecided numbers are leftover-design (D-056). This join does not invent those numbers."}

$.obligations[4] = {"id": "OBL-LOCK-JOIN", "leftoverDesign": true, "existingGate": "none on DR-111. Consumed later on DR-103.",
 "executionObligationOwnerToday": "none on this row alone", "rideStanding": "not-capable-of-riding",
 "reason": "v5 lockJoin PROPOSES that no lock of any form is producible until this row closes with evaluable windows, and that a later DR-103 successor would consume those windows. Evaluable windows wait on OBL-NUMERIC-WINDOWS. This join does not invent window numbers, does not emit a lock, and does not retarget DR-103."}
```

`$.numericWindowsVerbatim` = `"RESERVED. This artifact does not mint how long a reader is supported. Product/versioning sets numbers later. Alias-window numbers are D-012's, not this row's."`
`$.proposedLaterWork[0]` = `"A later product/versioning act may set numeric reader-support windows. This join does not invent those numbers."`

**Originating contract:** `docs/coop/artifacts/compatibility-matrices-contract.v5.json` — sha256
`d0386cee26d8aafd3d07b46f21352cc3d9d03cdc8f406de0adf571f8c81f7f41`; `$.status` = `"CANDIDATE-NOT-APPLIED"`,
`$.binds` = `"NOTHING"`; recorded **`## D-103`** (`Numeric windows remain RESERVED. S-EVIDENCE remains deferred
with DR-113. No lock is producible.`). Reserving fields: `$.numericWindows` (same string as above) and the four
surfaces whose skeleton carries a window reservation — `S-CORE` (`current writer = signed distribution core
major as published; numeric windows RESERVED`), `S-SCHEMA` (`current writer = DR-103 schema majors; windows
RESERVED`), `S-CTRL` (`consumes control-protocol-contract.v2 row skeleton; window SEMANTICS reserved here`),
`S-TS1` (`current writer = applied delivery major 1; windows RESERVED`).

**File 08 row (line 293, verbatim):**

> `| DR-111 | Separate compatibility windows for core/index/control, each provider major, component API, state schema, and evidence formats | Versioning authority | [Operations](04-lifecycle-delivery-and-operations.md) | Per-surface matrices and cross-version conformance; no shared same-version assumption | OPEN | Hard blocker |`

Owner / decision-authority cell: `Versioning authority`.

---

## 3. Precedent

### 3.1 The recording form for this lineage

**`## D-177`**, Decision (verbatim): `Record v2 as DR-111 leftover remasurement after D-176. The candidate binds
NOTHING. DR-111 stays `OPEN`. leftover-design of OBL-NUMERIC-WINDOWS and OBL-LOCK-JOIN remains. D-056
Eligibility gates 2 and 3 do not hold for DR-111. Gate 1 Class A is not opened. Not eligible in kind. Not
SATISFIED. Required-now stays 28. Condition-4 effect is zero. Frozen v1 remains a historical measurement as of
HEAD `5d5d778` / required-now 26. v1 stays frozen; do not record it as current. Does not invent numeric windows.
Does not produce a lock. Does not edit file 08. Does not invent a D9 code. Does not authorize
`docs/v2/implementation/`.`

### 3.2 A file-08-pin advance as the warrant for a successor

The closest recorded class is the **occupancy-stale** remasurement family D-282–D-287: a join is succeeded
because a cited input moved, and the leftoverDesign partition does **not** change. `## D-282` (component-manifest
v9) is the template: `Record leftover-join.v9 as DR-103 leftover remasurement after D-281. … leftover-design of
OBL-WINDOWS-PATH, OBL-ENVELOPE-MISMATCH, OBL-UNICODE-NORM, OBL-OD-1, and OBL-OD-2 remains on leftover-join.v9.`

**A caution the record itself records.** `DECISIONS-NEEDED.md`
(`7e2552a0e272b0c0ed4d5d32c33dd5f2e846604e68fed8e0e97693f656708a9b` at this HEAD; D-293 pinned the pre-hygiene
`f6d49a0b…`), item A3, second arrow, verbatim:

> `Four pre-D-236 joins (anti-lockstep v3, compatibility v2, sarif v4, identity-namespace v6) pin the pre-D-236 file 08 digest — the class the 2026-08-26 hunt judged not stale under the strict rule; unchanged.`

So the orchestrator's own hunt did **not** treat this pin as stale. **The warrant for the v3 successor is
D-293's adoption of the C3 recommendation, not a staleness rule** — and the successor must say so, or a
reviewer will ask what it remeasures. D-294 does not supply a warrant either: its three successor triggers are
`(a)` a superseded consumed occupancy, `(b)` a sibling successor changing a projected value, `(c)` the join's own
lineage superseded — a file-08 pin is none of the three.

### 3.3 What reviewers attacked in successors of this era

Read verbatim from the verdict files: `component-manifest-leftover-join.v8.review-independent.codex.json`
(**REJECT**, `CMLJ-V8-SF1`: `"The v8 subject's predecessorV6 role still says 'This v7 remasures occupancy v7
stale after occupancy v9 (D-214).' … deictic 'This v7' names the wrong speaker"`, and `CMLJ-V8-SF2`:
`"The purpose calls the cumulative lands record unchanged while v8 extends it"`);
`platform-tcb-leftover-join.v8.review-independent.claude2.json` / `.codex.json` (**REJECT** on the identical
deictic class, `CLAUDE-PTLJ-V8-SF1` / `CODEX-PTLJ-V8-SF1`);
`distribution-core-leftover-join.v8.review-independent.claude2.json` (**REJECT** 0/2, `CLAUDE-DCLJ-V8-SF1`
charging a custody claim `"that the frozen leftover-join.v3 bytes contradict"`, `CLAUDE-DCLJ-V8-SF2` charging
`"carries the former basedOn object unchanged"` against the actual diff).

---

## 4. The successor's minimal diff — `compatibility-leftover-join.v3.json`

**Changes:**

- `$.file08Pin.sha256` — `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1`
  → `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`, with a note naming the one intervening
  file-08 commit (`fc688b1`, D-236) and stating that D-236 changed the DR-104 row, not DR-111.
- `$.version` → `3`; `$.date`; `$.head` → this act's HEAD; `$.basedOn` — predecessor custody for v2 with its
  D-177 recording pinned (the house rule the record charges as `G25LJ-V4-CL-SF1`: `predecessor recording must be
  pinned`), and the speaker labelled **this v3** at every site (the `CLAUDE-PTLJ-V8-SF1` / `CMLJ-V8-SF1` defect).
- `$.purpose` — must describe the **actual** v2→v3 diff, not claim anything carried "unchanged" that is not
  (`CLAUDE-DCLJ-V8-SF2`).

**Byte-identical, and this is the point of the act:**

- `$.summary.leftoverDesign` stays `["OBL-NUMERIC-WINDOWS", "OBL-LOCK-JOIN"]`.
- `$.obligations[1]` and `$.obligations[4]` — `leftoverDesign: true`, `existingGate`, `executionObligationOwnerToday`,
  `rideStanding` all unchanged. **No window value exists to remeasure against.**
- `$.numericWindowsVerbatim`, `$.file08StatusToken` (`"OPEN"`), `$.registerRow`, the contract v5 pin.

**Cross-lineage citations (D-294 Decision 3):** refresh any sibling-lineage citation to the version current at
dispatch and label the superseded one not current. `compatibility-leftover-join.v2` is **not** among the eight
citing joins D-294 measured, so this is a discipline for whatever citations the successor adds, not a repair of
existing ones.

**What must stay an explicit named open decision in the successor:** the window unit, whether the four reserved
surfaces share one window, and each surface's value. The C1–C4 packet §3.5 measured the gap: `Unit of a "window"
(majors? releases? days?) is **not in the record**; the contract's own phrase is `how long a reader is supported`.`
The only nearby decided number belongs to another row — `## D-012` Decision item 5
(`a rename keeps the old name as a deprecated alias for AT LEAST one minor release cycle AND no fewer than 90
days from the deprecating release, whichever is longer`) — and the contract says
`Alias-window numbers are D-012's, not this row's.`

---

## 5. Prohibitions

From **D-293**: `This entry marks nothing `SATISFIED`. It does not edit file 08. It does not open D-056 Class A.`
and `It does not record any artifact successor, fixture byte, or successor join; every such act follows under
D-000 as the adopted recommendation states.`

From **D-177** (verbatim, and the successor must carry the equivalents): `Does not invent numeric windows. Does
not produce a lock. Does not edit file 08. Does not invent a D9 code. Does not authorize
`docs/v2/implementation/`.` plus `D-056 Eligibility gates 2 and 3 do not hold for DR-111.`

From **D-103**: `Numeric windows remain RESERVED. S-EVIDENCE remains deferred with DR-113. No lock is producible.`

From **D-106** (quoted in the C5–C9 packet): `Locks remain deferred to DR-111.` — and
`component-manifest-schemas.v11` `$.lockSchema.purpose`: `NO lock is producible until DR-111 closes`.

From HANDOFF: `No file-08 cell edit for leftover/occupancy remasurements.`;
`Do not invent … UNDECIDED numbers …`; `Do not SATISFY DR-117 / DR-131 / DR-133 (Class A unopened).`

---

## 6. Dependencies and ordering

- **Act (i) is unblocked and cheap.** It needs nothing from the owner. It is the single cheapest C act in this
  plan.
- **Act (ii) is blocked on the owner.** D-293 states **no** unit, **no** surface coupling and **no** value.
  The sentence that shows it is not in the record: D-293 Decision item 6 says only
  `the C3 live-file-08 remasurement with coherent evaluable windows` — it names the *shape* of the later act and
  supplies none of its content; and the round-2 text it adopts says
  `if the values are not in hand, that is choice (b) or (c) above, not a partial setting.` **Owner question Q3
  (§ README):** unit, coupling, and the four values, from the `Versioning authority`.
- **Downstream.** `OBL-LOCK-JOIN` and DR-103's lock rule stay blocked until act (ii): the join's own reason says
  `no lock of any form is producible until this row closes with evaluable windows, and … a later DR-103
  successor would consume those windows.` So C3(ii) gates a DR-103 successor (owner cell `Delivery + security`,
  file 08 line 285) — an ordering fact that also touches C7.
- **Bundling option the record allows:** the round-2 text says `remasure the compatibility leftover-join against
  live file 08 **first (or in the same reviewed cycle)**`. If the owner supplies values, acts (i) and (ii) may be
  one cycle; otherwise (i) stands alone.

---

## 7. Act shape

**Act C3-a — "DR-111: compatibility leftover-join.v3, live file-08 remasurement"** (unblocked).

- **Stage A**: `docs/coop/artifacts/compatibility-leftover-join.v3.json` — independent dual adversarial review,
  ACCEPT only at 0/0.
- **Stage B**: `coordinator-decisions.D-NNN.draft.md` — dual CONSENT 0/0, up to three turns.
  Decision type: `RULE-GOVERNED`, same no-cell-edit branch as D-170 through D-235 and D-237 through D-294
  (D-272 excluded — CONTESTED).
- **Then**: COORD-only append; commit `C-DNNN`.

**Act C3-b — "DR-111: evaluable windows"** (blocked on the owner; not schedulable).

- **Stage A**: `compatibility-matrices-contract.v6.json` (windows filled) + `compatibility-leftover-join.v4.json`
  (remeasuring `OBL-NUMERIC-WINDOWS` and then `OBL-LOCK-JOIN`).
- **Stage B**: COORD draft, `PREFERENCE-LADEN` (D-000 clause 5 — the numbers turn on the owner's preference).

**Estimated acts: 1 now, 1 later (blocked).**
