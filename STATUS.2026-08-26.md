# OpenSIP V2 architecture — status at 2026-08-27 (Claude orchestrator; started after D-281, now after D-292)

Live HEAD `4abb961` = D-292 (last COORD heading; 277 headings). D-282..D-284 recorded 2026-08-26; D-285 (`791187b`, adoption date corrected by `9d04151 D-285 hygiene`) and D-286..D-292 on 2026-08-27 — eleven acts by Claude as orchestrator, each at independent dual ACCEPT 0/0 (Stage A) and dual CONSENT 0/0 (Stage B). File 08 digest `e503b75b…`. Git ahead of origin; not pushed.
Every number below was measured from file 08 / COORD bytes by independent readers and re-counted by an adversarial verifier.

## 1. Where the five readiness conditions stand (file 08, the only definition of "complete" — D-001)

| # | Condition | Standing | What the number really means |
|---|---|---|---|
| 1 | DR-001–011 SATISFIED or explicitly disposed | **MET (preview scope only)** | 1 of 11 SATISFIED (DR-001); 9 HARD-BLOCKED + 1 PARTIAL carry owner-recorded *preview* dispositions (D-058…D-083). Nothing blocked is settled; it is scoped around. |
| 2 | Every slice-affecting V2 row SATISFIED | **NOT MET — 5 of 32** | SATISFIED: DR-102 (Class A), DR-104, DR-115, DR-119, DR-123 (Class B). 3 rows deferred by disposition (DR-128/129/130). **24 slice-affecting rows remain** (22 OPEN, DR-118 DECIDED-V1-NOT-INTEGRATED, DR-107/122 PROPOSED-CLOSED-FOR-REVIEW). |
| 3 | DR-201–205 re-reviews ACCEPTED | **MET** | 5 of 5. |
| 4 | Gates named + owned; no unevidenced QUALIFIED | **MET (naming half)** | 28 of 28 required-now gates named; 32 of 32 owners; 0 QUALIFIED claims. Execution half is qualification work, not architecture. |
| 5 | Authorities authorize `docs/v2/implementation/` | **NOT MET — structurally last** | Directory absent; this is a separate PREFERENCE-LADEN act reserved to you (D-001). |

The handoff's own five-item completion bar (from your D-132 grant: DR-131, DR-133, DR-117 SATISFIED; Condition 2 MET; identity cited via D-077/D-078): **all five NOT MET** (identity citation exists only at candidate grade).

## 2. Why the 24 remaining rows cannot simply be marked SATISFIED

D-056 allows SATISFIED only when five eligibility gates hold. Two things block almost every remaining row:

1. **Gate 1 Class A is unopened.** DR-117, DR-131, DR-133 each have an independently accepted *candidate* contract, but every recording carries an express reservation ("CANDIDATE-NOT-APPLIED; Class A not opened"). COORD says the only venue for a lift is "a reviewed coordinator act, not an artifact" — a D-000 cycle recording *application-grade, no-express-reservation* (T2-02) acceptance. The file-08 owners of those rows are **Product owner** (DR-117), **Product + CLI/output** (DR-131), **Semantic/component architecture** (DR-133). D-001 classes DR-117 as a route-C PREFERENCE-LADEN product decision. **This is your decision, not a reviewer's.**
2. **Leftover-design remains on every other row** (71 obligations measured across the 38 current leftover-joins). D-056 clause 5: authoring fixtures is design work, so a row with unauthored fixtures is ineligible.

## 3. The remaining work, by who can do it

### A. Mechanical remasurement queue — AI does this, no decisions needed — **COMPLETE as of D-287 (2026-08-27)**
Occupancy-stale leftover-joins (they cite a superseded harness occupancy as the specification). Each act = author successor → dual Stage A ACCEPT 0/0 → COORD draft → dual Stage B CONSENT → COORD-only commit (~30–45 min per act when reviews pass first time).
1. component-manifest v6 → v9 — **DONE, recorded as D-282** (`4881022`; v7 and v8 were rejected on wording only; v9 dual ACCEPT 0/0, D-282 dual CONSENT at turn 2)
2. permission v9 → v12 (G09 occupancy v3→v4) — **DONE, recorded as D-283** (`9eb56dc`; v10 Split / v11 Dual REJECT on wording; v12 dual ACCEPT; COORD draft consented at turn 3 of 3)
3. state-class v3 → v4 (G19 v1→v2) — **DONE, recorded as D-284** (`b8bc52a`; Stage A dual ACCEPT 0/0; COORD draft needed three Stage B turns, all wording: object-shape gloss at turn 1, single-prior-turn plural at turn 2; turn 3 dual CONSENT 0/0)
4. doctor-actor v11 → v12 (G12 v4→v6, G21 v3→v4, G32 v1→v3) — **DONE, recorded as D-285** (`791187b`; Stage A dual ACCEPT 0/0; Stage B dual CONSENT 0/0 at turn 1)
5. exact-bytes v5 → v7 (G07 v3→v4; DR-103 join currency → v9) — **DONE, recorded as D-286** (`81c7657`; v6 dual ACCEPT 0/0 but withdrawn unrecorded because its `date` predated its pinned HEAD; v7 dual ACCEPT 0/0; Stage B dual CONSENT 0/0 at turn 1)
6. distribution-core v7 → v8 (G01–G05 v1→v9/v4/v5/v4/v4) — not in Grok's handoff list but the same class; **DONE, recorded as D-287** (`8e3db61`; v8 Split at Stage A — Codex ACCEPT 0/0, Claude REJECT 0/2 on two custody-wording defects — and unrecorded; v9 lands both, dual ACCEPT 0/0; Stage B dual CONSENT 0/0 at turn 1)
7. identity-namespace v6 (G31 v2→v5) — **row already SATISFIED (D-236)**; remasuring has zero readiness effect — NOT done; your call (DECISIONS-NEEDED A3)
Not candidates: lifecycle/monorepo/signed-index/DR-117 joins only cite a superseded *GATE* join; COORD (D-276/D-278/D-281) explicitly keeps those current.

**Second queue (opened by the first): cross-citation refresh of GATE joins, per precedent D-269/D-276/D-278/D-281 — COMPLETE as of D-292** — each GATE join that names a ROW join superseded by D-282..D-287 "as the current … leftover-join" gets a successor with the citation refreshed (occupancy unchanged; zero readiness effect). Measured 2026-08-27 from bytes; all five have byte-identical leftoverDesign partitions between the cited and current ROW versions:
8. g09 v11 → v12 (permission v9→v12, doctor-actor v11→v12) — **DONE, recorded as D-288** (`8d0cf09`; Stage A dual ACCEPT 0/0; Stage B dual CONSENT 0/0 at turn 1)
9. g12 v4 → v5 (doctor-actor v11→v12) — **DONE, recorded as D-289** (`63d1387`; Stage A dual ACCEPT 0/0; Stage B dual CONSENT 0/0 at turn 1)
10. g15 v5 → v6 (component-manifest v6→v9) — **DONE, recorded as D-290** (`20e6d2d`; Stage A dual ACCEPT 0/0; Stage B dual CONSENT 0/0 at turn 1)
11. g19 v4 → v5 (state-class v3→v4) — **DONE, recorded as D-291** (`cb8bd16`; Stage A dual ACCEPT 0/0; Stage B dual CONSENT 0/0 at turn 1)
12. g21 v12 → v13 (doctor-actor v11→v12) — **DONE, recorded as D-292** (`4abb961`; Stage A dual ACCEPT 0/0; Stage B turn 1 Claude OBJECT 0/2 on two wording defects, turn 2 dual CONSENT 0/0)
Left current by precedent: the ROW joins that now name a superseded GATE join (component-manifest v9, doctor-actor v12, permission v12, state-class v4, plus lifecycle/monorepo/signed-index v4 from before) and the two ROW→ROW citations (packaging v4 → component-manifest v6, permission v12 → doctor-actor v11). Re-swept from bytes after D-292: **no GATE join names a superseded ROW join** — the cascade is closed. The systemic alternative (content-based citation reading) is DECISIONS-NEEDED A4 / `PROPOSAL.cross-citation-convention.md`.

### B. Leftover-design an AI cycle could author *if the bytes were uniquely determined by closed types* — 39 obligations
Fixture authoring for ~20 gates (G07, G08, G09 ×14 FX classes, G12 ×12 FC, G14, G15/AT ×8, G16, G18, G19, G20, G21, G22, G24–G30, DR-114 JOIN ×13, DR-122 SARIF, DR-127 hostile goldens, DR-105 R-6/R-10) plus two schema successors (DR-103 unicode-norm, OD-2 fold).
Grok's standing judgment (handoff): "uniquely determined leftover-design of fixture bytes from closed types is exhausted — do not invent." I.e. **what is left requires choices** (envelope shapes, byte-sets, corpus contents) that the register does not determine. Closing these means either (a) you decide the shapes/inputs, or (b) you explicitly authorize the orchestrator to choose on your behalf under D-000 adversarial review, accepting the CONTESTED risk.

### C. Decisions only you (product/release/architecture authority) can make — 25 obligations + 10 parked contests
Reserved numbers and lists (each row stays OPEN until set):
- DR-112 quorum / clock-skew / emergency / waiver numbers (OD-112-1..4)
- DR-118 per-row language-quality thresholds + matrix corpus acceptance; G13 reserved gate
- DR-111 numeric reader-support windows
- DR-126 per-OS TCB allowlist tables / selectors
- DR-121 CI encodings (provider, YAML, path filters, caches, commands)
- DR-107 lifecycle encodings (atomic-rename equivalent, quarantine/journal format, lock grammar)
- DR-103 OD-1 owner assignment + size caps; DR-101 OD-101-1 core language (Rust-as-core not minted) / OD-101-2 signing ceremony; DR-115 D-006 unit & tree accounting; G07 filesystem coverage
- DR-105/DR-114 FC-C1 joint-owner recording and BLK-1..4 routing (D-032); DR-124 grant-journal assignment; DR-127 AL-1/2/5 & AL-3 execution routes
- DR-120 adapter implementations, DR-125 SDK APIs, DR-107/121 encodings are reserved to *after Condition 5* — implementation, not design
Parked CONTESTED entries batched to you (D-000 clause 2): D-017/019–024, D-051/052/053, D-059, D-067, D-094, D-095, D-098, D-099, D-101 (most were superseded by later ADOPTED successors — you need only confirm), and **D-272** (both reviewers found the orchestrator's fourth-turn dispatch a clause-2 breach; D-273 recorded the same subject in a new cycle — a ruling is needed).
Then: **Class A lifts for DR-117 / DR-131 / DR-133**, and finally **Condition 5**.

## 4. Honest bottom line
- The register is internally consistent and heavily cross-verified; the naming/ownership scaffolding (Condition 4) is done.
- Architecture completion is now **decision-bound, not effort-bound**: the mechanical remasurement queue is exhausted (D-282..D-287); no further row can move without a product/architecture decision from you (numbers, lists, envelope shapes, Class A opening). Condition 2 is unchanged at 5 of 32 — these acts corrected stale custody, they did not and could not SATISFY anything.
- Risk notes: (a) ~~several artifacts cited by recorded joins are untracked in git~~ — resolved by your backlog commit `078b3d6`; re-measured 2026-08-27: all 695 artifact files cited by COORD are tracked; (b) Codex capacity is fine (weekly limit 99% left, resets 3 Sep) but its long-running session context is 14% from full — the next review should run in a fresh `codex --yolo` pane; (c) HEAD is 7 commits ahead of origin and unpushed (D-282..D-287 + the D-285 hygiene commit).

## 5. Suggested next decisions from you (cheapest first)
1. ~~Confirm the mechanical queue order~~ — done through D-287; only say whether you want identity-namespace v7 (zero readiness effect).
2. Rule on D-272 and confirm the superseded CONTESTED entries.
3. Decide whether to open Class A for DR-131 / DR-133 / DR-117 (or state what you need to see first).
4. Pick which reserved numbers/lists you will set now vs. defer. Correction (2026-08-27, Codex review of packet C1–C4): a number-level deferral disposition records the reservation but has no Condition-2 or D-056-eligibility effect; only a row-level deferral under the D-002/D-010 limb (a scoped D-002 successor) removes a row from the SATISFIED-requiring set.
5. State whether the orchestrator may choose fixture shapes/byte-sets on your behalf (D-000 review) or whether you want to specify them.

## 6. Recommendation phase (2026-08-27/28) — what to read now
- Every item in `DECISIONS-NEEDED.md` (A1–A4, B1–B3, C1–C9, D1, E2, F1) now has a **reconciled Claude + Codex recommendation** in
  `DECISIONS-RECOMMENDED.md` (repo root), each on a byte-cited, adversarially verified packet under `DECISION-PACKETS/` (round files
  `*.claude-recommendation[.rN].md` / `*.codex-recommendation[.rN].json`; verifier records under `DECISION-PACKETS/.verify/`).
  Protocol: `DECISION-PACKETS/RECOMMENDATION-PROTOCOL.md` (≤3 rounds; nothing is decided — every item is yours).
- Outcome: A–E items AGREED; F1 reconciled through the full three rounds (its final status is the one shown in `DECISIONS-RECOMMENDED.md`). Codex's refutations changed the recommendations materially in A1, A3, A4, B1–B3, C1–C9, D1, and F1
  (F1: the sealing/archive integrity model was rebuilt around four commits — measured `<P>`, measurement-record `<R>`, seal `<S>`,
  pure move `<M>` — after Codex showed the first draft's in-tree manifest and self-cited seal commit were circular).
- A4's convention proposal is regenerated as `PROPOSAL.cross-citation-convention.md` (draft D-294 — D-293 records your decisions; not recorded, not dispatched).
- F1's packet `DECISION-PACKETS/F-docs-rewrite.md` carries the proposed `docs/` tree, per-doc templates, the D-SEAL draft, the
  `git mv` procedure, sizing (128 pages baseline), ten owner options with positions, and 23 open questions. Nothing under `docs/`
  was touched. Your decisions were recorded 2026-08-28 as user-made entry D-293 (`c10319d`) and pushed to `origin/main` (E2 done).
- Correction to §5 item 5 / E4: 729 of 760 `_dispatch.*.txt` files are tracked; only the 31 for D-282..D-292 are untracked.

