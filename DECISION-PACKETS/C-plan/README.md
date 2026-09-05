# C-plan — the record acts that remain after D-293 adopted C1–C9

Planning only. Nothing here is recorded, nothing under `docs/` was read-modified, and no value is invented.
Every claim in the nine sub-item files carries a path plus sha256 and a JSON path or a file-08 line number.

Measured at HEAD `f3456575071928022a1f0e3a77e531a87157b365` (last COORD heading `## D-294`).

| Pinned source | Path | sha256 |
|---|---|---|
| file 08 | `docs/v2/architecture/08-decision-and-readiness-register.md` | `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e` |
| COORD | `docs/coop/COORDINATOR-DECISIONS.md` | `31746810f9be78f697d66eb94d9cd50a95a51218998f97a154596363039fb9b6` |
| agreed recommendations | `DECISIONS-RECOMMENDED.md` | `42f27394746d4aac569a09a01da719c0cf318cf114086635e73097a6add97370` (= the digest D-293 **Subject** cites) |
| C1–C4 packet | `DECISION-PACKETS/C1-4-reserved-numbers-security-quality.md` | `59497fe6835c3fb3b84dfe757b63daa22b1b4cbdd103fd2d74026a0e192c376c` |
| C5–C9 packet | `DECISION-PACKETS/C5-9-reserved-encodings-owners-units.md` | `735720d9f4df7bba5717f78bb558f378edb9f825971cb60b20ed8cdf07a58e2b` |
| packet manifest | `DECISION-PACKETS/MANIFEST.sha256` | `ecdbb41dc07e4833abe787387fa39aacc5d0c4a9d98a01a25f645d32520809e0` |
| standing instructions | `HANDOFF.D-000-orchestrator-live.txt` | `b926489df28b183eccf4447e7f0b4c7f9bb56ef1c1f19747ae2f01b147804c3d` |

Note on one working file: `DECISIONS-NEEDED.md` is `7e2552a0e272b0c0ed4d5d32c33dd5f2e846604e68fed8e0e97693f656708a9b`
at this HEAD, not the `f6d49a0b1fa47b2cc493663810803c7995677c25b88a5197c8340781e7189b2e` D-293 cites — it was
edited by the hygiene commit `8bc9963` after `c10319d` (C-D293). It is a working document, not the record.

---

## 1. Remaining acts

| Sub-item | Remaining record acts | Stage-A subject(s) | Blocked on | File |
|---|---|---|---|---|
| **C1** DR-112 | **1** — record OD-112-3 as the final fail-closed policy. (OD-112-1/2/4 authority: **no further act**; D-293 restates the live state) | `signed-index-trust-contract.v9.json`; `harness.DR-G08.trust-recovery.install-surfaces.v4.json`; `signed-index-leftover-join.v5.json` | — (unblocked) | `C1-dr112-od-112-3-fail-closed.md` |
| **C2** DR-118 | **0 — no further act.** No artifact carries a token D-293 changes; the adopted C2 content is a sequence whose first step waits on DR-125 | — | DR-125 closure or express disposition (**not decided by D-293**) | `C2-dr118-thresholds-matrix-g13.md` |
| **C3** DR-111 | **1 now + 1 later** — (i) `compatibility-leftover-join.v3` remasured to live file 08; (ii) one coherent set of evaluable windows | (i) `compatibility-leftover-join.v3.json`; (ii) `compatibility-matrices-contract.v6.json` + `compatibility-leftover-join.v4.json` | (i) — ; (ii) owner **Q3** | `C3-dr111-live-file08-remasurement.md` |
| **C4** DR-126 | **3** — owner assignment → application-grade TCB successor making the grammar governing → complete profile population. (The "G22 qualification evidence = candidate standing only" limb: **no further act**) | (b) COORD-only (optionally `platform-tcb-leftover-join.v10.json`); (c) `platform-tcb-contract.v46.json` + `platform-tcb-leftover-join.v11.json`; (d) the population packet + `harness.DR-G22.platform-abi-loader.v3.json` + a further join | (b) owner **Q4**; (c) after (b); (d) after (c) + owner **Q5** | `C4-dr126-tcb-owner-grammar-profiles.md` |
| **C5** DR-121 | **1** — reviewed architecture-scope act classifying the six `reservedForBlueprint` members as implementation encodings | COORD-only (the `## D-294` shape); optionally `monorepo-leftover-join.v5.json` | — (unblocked); **Q6**/**Q7** are named, not answered, by the act | `C5-dr121-ci-encoding-scope-act.md` |
| **C6** DR-107 | **1** — the same scope act for the seven reserved lifecycle mechanisms; **no new atomic-rename admissibility policy** | COORD-only; optionally `lifecycle-leftover-join.v5.json` | — (unblocked); the lock limb additionally waits on **C3(ii)** | `C6-dr107-lifecycle-encoding-scope-act.md` |
| **C7** DR-103 | **1 (or 2 if split)** — OD-1 owner assigned to DR-115 `Product + release engineering`; OD-2 final do-not-fold (the only **unblocked** leftoverDesign flip in the C set). Caps: **no act**, numeric limb stays open. MF-6 naming OD-2 with OD-1: **later, separate** | `component-manifest-leftover-join.v10.json` (optionally `component-manifest-schemas.v12.json`, which drags a corpus act) | — for the owner assignment and the do-not-fold; caps blocked on owner **Q8** | `C7-dr103-od1-owner-od2-do-not-fold.md` |
| **C8** DR-101 | **2** — OD-101-1 core implementation language; OD-101-2 core code-signing + OS notarization, owned separately from DR-112 | (a) `distribution-core-inventory-contract.v17.json` and/or `distribution-core-leftover-join.v10.json`; (b) a DR-101 ceremony successor + a further join | owner **Q11**/**Q12** and **Q13** — D-293 supplies the route, not the content | `C8-dr101-od-101-1-language-od-101-2-ceremony.md` |
| **C9** D-006 / DR-115 | **4** (or 2 bundled) — three occupancy successors + one join successor carrying the D-293 unit. **`OBL-2` does not close**; G02 accounting stays open | `harness.DR-G01.core-download.v10.json`; `harness.DR-G02.core-installed.v5.json`; `harness.DR-G04.core-memory.v5.json`; `distribution-core-leftover-join.v10.json` | — (unblocked); **Q14**/**Q15** are named by the acts | `C9-d006-mb-unit-1e6.md` |

**Totals: 12–14 acts**, of which **8–10 are unblocked today** and **5 wait on owner sentences D-293 does not
contain**.

Later measurement at HEAD `8787d6ded31776a645b0a45f9f7a79b6c42513e2` (last COORD heading
`## D-341`, 2026-08-31): C1-a through C9 unblocked acts and A3 are recorded
(D-303 through D-313). C4-b is recorded (D-341). C4-c is unrecorded
(`platform-tcb-contract.v46` Stage A dual ACCEPT 0/0 with a grade split).
C10–C12 evidence packet authorized by D-314 item 20 (Q16):
`DECISION-PACKETS/C10-12-g07-fcc1-grant-al.md`. Planning only; no COORD
append.

### No further act (the owner's entry is itself the disposition, and no artifact token must change)

- **C2 in full** — every reserving token in `language-quality-leftover-join.v5`,
  `language-quality-matrix-contract.v13` and file 08 line 300 already states the standing D-293 adopts.
- **C1's OD-112-1 / OD-112-2 authority limb** — file 08 line 294 already reads `Security + operations`.
- **C1's OD-112-4 authority limb** — `signed-index-trust-contract.v8` `$.namedOpenDecisions[3].standing`
  already reads `RESERVED to product/release…`, and `$.auditAndWaiver.waiverExpiry` already routes the duration
  to product/release.
- **C4's "candidate standing only" limb** — `platform-tcb-leftover-join.v9` `$.obligations[5]` already records
  `leftoverDesign: true`, `existingGate: "none"`, `executionObligationOwnerToday: "none"`,
  `rideStanding: "not-capable-of-riding"`; `platform-tcb-contract.v45` is `CANDIDATE-NOT-APPLIED` / `binds`
  `NOTHING`.
- **C5/C6's "OBL-…-RESERVED stays leftoverDesign true" limb** — it already is.
- **C7's "name OD-2 with OD-1 at the next MF-6" limb** — rides a later MF-6, already anticipated by
  `component-manifest-leftover-join.v9` `$.proposedLaterWork[0]`.

---

## 2. Suggested order — cheapest and unblocked first

| # | Act | Why here |
|---|---|---|
| 1 | **C3-a** `compatibility-leftover-join.v3` | One subject; the diff is a file-08 pin, a version and custody prose. No new content anywhere. |
| 2 | **C7-a(ii)** OD-2 final do-not-fold (run split from the OD-1 limb) | Fully determined by D-293; one subject; but it is the **first RESERVED-value obligation ever to leave a leftoverDesign partition** (§ below), so run it early while attention is on it. |
| 3 | **C9-a / C9-b / C9-c / C9-d** the three occupancies then the join | Fully determined; four short cycles of the D-231…D-235 class. Run **before C8**, which needs the D-006 envelope unambiguous, and before any further `distribution-core-leftover-join` edit. |
| 4 | **C1-a** OD-112-3 | Determined; three subjects, so a longer Stage A. |
| 5 | **C5-a**, then **C6-a** | COORD-only decision entries of the `## D-294` shape. Determined content, but `## D-294` itself needed three turns and drew two MUST-FIXes; budget accordingly. |
| 6 | **C7-a(i)** OD-1 owner assignment | Determined, but inherits D-102's CONTESTED history (`D-094/D-098/D-099/D-101` were CONTESTED attempts at a scoped D-006 successor before D-102 landed). Run after the cheap wins. |
| 7 | **C4-b → C4-c → C4-d** | Blocked on **Q4**, then strictly sequenced by D-293's own "then … then". |
| 8 | **C8-a → C8-b** | Blocked on **Q11**/**Q13**; ordered after C9. |
| — | **C2** | Nothing to run. Its first step is a DR-125 disposition, which is not a C-item at all. |

**A cross-cutting finding worth stating in every entry that closes an obligation.** A sweep of every
`*leftover-join*.json` in `docs/coop/artifacts/`, comparing `summary.leftoverDesign` across consecutive versions,
finds **no case in which a RESERVED/UNDECIDED-value obligation has left the partition**. Every recorded shrink is
an authoring or execution obligation closed by authored bytes or by a recorded specification —
`OBL-G15-HARNESS-SPEC` (`component-manifest-leftover-join.v2` at `## D-161` → `.v6` at `## D-174`),
`OBL-G09-HARNESS-SPEC` (permission v2→v3), `OBL-JOIN-FX-EXECUTION` (doctor-actor v8→v9),
`OBL-NT-11-EXECUTION` (identity-namespace v4→v5), and `OBL-G23-FX-AUTHORING` → `[]`
(`g23-leftover-join.v8.json` `498324e5e456562317c7681b44cdac9138ca1e947aa363dad5a331caa3eef812` at `## D-240`,
after the D-237/D-239 fixture recordings). The C7 OD-2 flip, and later the C4 and C8 flips, will each be first
of their class. Say so in the entry; do not let a reviewer find the gap first.

**And a wording discipline the verdict files justify.** Every recent leftover-join REJECT in these lineages was a
custody or self-description defect, never a substantive one: `CLAUDE-PTLJ-V8-SF1` / `CODEX-PTLJ-V8-SF1` /
`CMLJ-V8-SF1` / `CLAUDE-CMLJ-V8-SF1` (a `This v7` speaker label surviving into a v8);
`CMLJ-V8-SF2` and `CLAUDE-DCLJ-V8-SF2` (self-description the diff contradicts);
`CLAUDE-DCLJ-V8-SF1` (a landing-custody claim the frozen predecessor bytes contradict);
`CLAUDE-LQLJ-V4-SF1` / `CODEX-LQLJ-V4-SF1` (landing provenance attributed to the wrong artifact, with an empty
`landedAt`). `component-manifest-leftover-join.v7` and `.v8` were both burned this way.

---

## 3. Open questions only the owner can answer

Each is followed by the sentence that shows the answer is not in the record.

**Q0 — Does D-293's adoption reach the round-2 recommendation files, or only the round-3 text carried in
`DECISIONS-RECOMMENDED.md`?** This governs C2's, C3's and C4's content.
*Not stated:* `DECISIONS-RECOMMENDED.md` §C1–C4 carries only the round-3 text, which says
`All three amendments adopted on top of round 2` and `- **C2, C3:** unchanged from round 2.` — the round-2 text
itself lives in `DECISION-PACKETS/C1-4-reserved-numbers-security-quality.claude-recommendation.r2.md`
(`44f51a5d36eb3f03c711112a50119ea67fb01b3a07d255ccbac5d51cc0485627`, listed in `MANIFEST.sha256`), which D-293
reaches only through its Subject's pointer to `the complete file list with digests`. D-293's own words never
quote it.

**Q1 — OD-112-3: what wording replaces the reservation?** Does "final fail-closed" drop the word `preview`?
Does OD-112-3 stay in `namedOpenDecisions` with a DECIDED standing, or leave it?
*Not stated:* D-293 says only `OD-112-3 is the final fail-closed policy`; the live sentence it supersedes is
`signed-index-trust-contract.v8` `$.offlineRunningPolicy.totalDecision[4].alreadyRunning` =
`"refuse unless OD-112-3 is later numbered; preview refuse"`.

**Q2 — OD-112-1, OD-112-2, OD-112-4 values.**
*Not stated:* the C1–C4 packet §1.4 measured `**None in the record.**`; D-293 adds none, saying only that they
`stay under DR-112's `Security + operations` authority` and `under product/release`.

**Q3 — DR-111: the window unit, whether the four reserved surfaces share one window, and each value.**
*Not stated:* D-293 says only `the C3 live-file-08 remasurement with coherent evaluable windows`; the adopted
round-2 text says `if the values are not in hand, that is choice (b) or (c) above, not a partial setting`; the
C1–C4 packet §3.5: `Unit of a "window" (majors? releases? days?) is **not in the record**`.

**Q4 — DR-126: who owns the population packet?**
*Not stated:* D-293 says `owner assignment, then an application-grade TCB successor …` and names no authority.
The record says three times that this is a separate decision — `platform-tcb-contract.v45`
`$.platformProfile.populationPacket`: `Choosing its owner is a separate decision.`;
`harness.DR-G22.platform-abi-loader.v2` `$.filesystems.laterAct`: same sentence;
`platform-tcb-leftover-join.v9` `$.proposedLaterWork[2]`: `… and does not choose that packet's owner.`
(The round-2 recommendation names `Security + release + platform owners` — see **Q0**.)

**Q5 — DR-126: the four filesystem selectors, the four version/build selectors, and the per-OS member tables.**
*Not stated:* C1–C4 packet §4.4: `**None in the record** for any per-OS table row, filesystem selector value, or
version/build selector value.`

**Q6 — Do the C5/C6 architecture-scope classifications get a file-08 echo?** The two deferral precedents both
wrote into file 08 (DR-G05's `caps deferred by explicit disposition (D-006)`; DR-130's in-row disposition).
*Not stated:* D-293's item 7 says only `reviewed architecture-scope acts classify the reserved encodings`, names
no register site, and its Decision closes `It does not edit file 08.`

**Q7 — Can an obligation classified as implementation-scope but still `leftoverDesign: true` ever satisfy D-056
gate 2?**
*Not stated:* C5–C9 packet, open question 1: `No COORD entry or artifact rules on a sub-row deferral; the only
deferral limb D-056 names is the D-002/D-010 row-level limb.` D-293 answers half — no eligibility effect
`without a separate reviewed act and a successor join` — and leaves open whether such an act can succeed.

**Q8 — OD-1: the four cap values, and what "measured caps" measures.** The caps are **not derivable from bytes**:
`component-manifest-schemas.v11` `$.namedOpenDecisions[0].standing` = `NO caps are stated in these schemas, and
that absence is a NAMED OPEN DECISION, not a default.`; same object's `candidateOwners` = `… a cap is a product
threshold …`; `## D-006` Decision type = `Numbers are not derivable from any rule`; and
`component-manifest-leftover-join.v9` `$.obligations[9].existingGate` = `"none"`, so no gate measures these four
quantities.
*Not stated:* D-293 says `with measured caps before oversized-input fixtures` and does not say what is measured,
by whom, at which gate, or against which corpus.

**Q9 — For OD-1 assigned to DR-115: MF-6 note on the already-`SATISFIED` DR-115 row, or a successor cited from
the schemas/occupancies?**
*Not stated:* C5–C9 packet, open question 2: `The record shows both mechanisms in use (D-089 MF-6 for the label;
D-102 successor without label change) and does not say which applies to added thresholds.`

**Q10 — Which `summary` bucket does `OBL-OD-2` move to once do-not-fold is final?** The lineage offers
`specifiedNotLeftover` (the `OBL-G15-HARNESS-SPEC` precedent) and `dischargedOrDeferred` (`OBL-SIG-CEREMONY`,
`OBL-LOCK`).
*Not stated:* D-293 says only `OD-2 is a final do-not-fold disposition`.

**Q11 — OD-101-1: which language, and against which candidate set?**
*Not stated:* D-293 says `OD-101-1 is resolved before the core-implementation blueprint under `Architecture +
release engineering` (a dedicated D-000 successor, or the owner's direct statement)` and names neither a
language nor a candidate list. C5–C9 packet §C8: `OD-101-1: **none in the record** as a decision.`
HANDOFF forbids inventing the list: `Do not invent … reserved lists …`, and the guard
`does not mint Rust-as-core` recurs across `## D-231`, `## D-232`, `## D-287` and four artifacts.

**Q12 — Is OD-101-1 route C (preference) or rule-governed?** It sets the overturn cost under D-000 clause 5.
*Not stated:* `## D-001` classes DR-101 as `Rule-governed architecture authoring with review`, while
`distribution-core-inventory-contract.v16` `$.namedOpenDecisions[0].owner` says `A later Route-C or rule-governed
successor, not this extraction.` D-293 does not resolve the disjunction.

**Q13 — OD-101-2: the core code-signing ceremony and OS notarization content.**
*Not stated:* C5–C9 packet §C8: `OD-101-2: **none in the record.** Signing ROLES exist … no ceremony, threshold,
or notarization procedure is named.` D-293 supplies only the routing (`its own DR-101 successor owned separately
from DR-112`).

**Q14 — May the C9 occupancy successors write the derived byte constants** (25000000, 80000000, 40000000,
50000000, 60000000, 100000000)?
*Not stated:* D-293 states a rule — `MB means 1e6 bytes for the D-006 G01/G02/G04 quantities` — not constants;
none of the six appears anywhere in the record, and the occupancies' current `doesNot` entries refuse the
binary analogues by name (`Does not invent a D-006 unit or authorize 26214400 as the bound.` /
`… 83886080 …` / `… a binary-MB byte constant.`).

**Q15 — Who are "the named authorities" for the G02 installed-tree accounting rule?**
*Not stated:* D-293 says `G02 installed-tree accounting stays open until the named authorities record a complete
rule` and names none in that sentence. The adopted round-2 text names two — `Product + release engineering` and
`Architecture + release` — the DR-115 and DR-G02 owner cells (file 08 lines 297 and 338). See **Q0**.

### Outside this plan, but in the same DECISIONS-NEEDED section

`DECISIONS-NEEDED.md` also lists **C10** (G07 filesystem coverage list), **C11** (DR-105/DR-114 FC-C1
joint-owner recording; BLK-1..4 routing) and **C12** (DR-124 grant-journal assignment; DR-127 AL-1/2/5 and AL-3
execution routes). `DECISIONS-RECOMMENDED.md`'s Summary table covers `C1–C4` and `C5–C9` only, and D-293's
Decision items 6 and 7 name no C10/C11/C12 disposition. **They remain undecided and unplanned.**
