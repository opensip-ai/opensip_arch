# Decisions needed from you (running list — Claude orchestrator, started 2026-08-26)

> **Historical handoff, superseded for current work.** D-367 delegated the remaining design decisions; D-368 replaced the review/recording workflow; D-369 completed the preview design under independent review. The owner-blocking and dual-review instructions below describe their dates. Use [file 08](docs/v2/architecture/08-decision-and-readiness-register.md) and the [accepted reference architecture](docs/coop/completion/reference-architecture.v2.md) for current scope, decisions and next steps.

> **DECIDED 2026-08-28.** You adopted every agreed recommendation ("record it, i agree. commit everything and then push to remote main"); recorded as user-made entry **D-293** in `docs/coop/COORDINATOR-DECISIONS.md`, committed at `c10319d` and pushed to `origin/main`. The items below are kept as the historical list; the authorized follow-on acts run under D-000 in the order D-293 states.

> **Read `DECISIONS-RECOMMENDED.md` first:** it carries, for every item below, the recommendation Claude and Codex reached by independent adversarial review (up to three rounds; AGREED or SPLIT), with pointers into the evidence packets.

> **Decision packets:** for every item below a byte-cited packet (evidence, options, consequences, pre-drafted D-000 cycle) is being written to `DECISION-PACKETS/` (repo root, tracked since `c10319d`) and adversarially verified; read the packet before answering an item.

> **State when you read this (2026-08-27, end of day):** both mechanical queues are finished — D-282..D-287 (occupancy-stale remasurements) and D-288..D-292 (GATE cross-citation refreshes per precedent) recorded at dual ACCEPT/CONSENT 0/0, HEAD `4abb961`, COORD 277 headings, file 08 untouched (`e503b75b…`), Condition 2 still 5 of 32. Nothing mechanical remains; every item below needs you. Nothing below was decided on your behalf; every item is yours. Cheapest path: rule A first (minutes), then B (the three Class A openings unblock the most), then C/D.


Each item names the decision, the register anchor, and what an answer unblocks. Answer in one sitting; I will
turn each answer into a D-000 cycle (dual adversarial review) and record it.

## A. Process rulings (cheap)
A1. **D-272 ruling.** Both reviewers found the fourth-turn dispatch a D-000 clause-2 breach; D-273 recorded the same
    subject as a new cycle. Options: (a) confirm D-273 stands and D-272 stays CONTESTED-parked as history; (b) direct a
    COORD note acknowledging the breach; (c) something else.
A2. **Superseded CONTESTED entries** (D-017/019–024, D-051/052/053, D-059, D-067, D-094, D-095, D-098, D-099, D-101):
    each was later resolved by an ADOPTED successor. Confirm they stay parked as history (no action), or name any you
    want reopened.
A3. **identity-namespace leftover-join.v6** (DR-104, already SATISFIED at D-236) cites G31 occupancy v2 while v5 is
    current. Remasure it (harmless, no-cell-edit) or leave it? Default if you say nothing: remasure it last.
    → Status: not done (zero readiness effect; DR-104 is already SATISFIED). Say "do it" and it is one more mechanical act; say "skip" and it stays as is. My recommendation: skip.
    → Re-swept from bytes after D-292: this is the ONLY occupancy-stale join left in the record (G31 spec v2 cited; occupancy v5 recorded at D-208); every other current join names its current occupancy. Four pre-D-236 joins (anti-lockstep v3, compatibility v2, sarif v4, identity-namespace v6) pin the pre-D-236 file 08 digest — the class the 2026-08-26 hunt judged not stale under the strict rule; unchanged.

A4. **Cross-lineage citation convention (systemic; my recommendation attached).** D-282..D-287 superseded six ROW
    leftover-joins, so five GATE joins (g09, g12, g15, g19, g21) now name a superseded ROW join as "the current …
    leftover-join". Precedent (D-269, D-276, D-278, D-281) remasures GATE citers in exactly this case and tolerates the
    reverse direction; I followed that precedent (D-288..D-292, no readiness effect) and re-swept: no GATE join now names a
    superseded ROW join, so the cascade is closed for this round. The alternative is a
    content-based reading — a citation is custody at recording and only a changed leftoverDesign partition triggers a
    successor — which ends the cascade for good; in all eleven current cases the partitions are byte-identical.
    Full byte-measured draft: `PROPOSAL.cross-citation-convention.md` (repo root, tracked since `c10319d`). Say "adopt" and I run it
    through the dual-CONSENT cycle as D-28x; say "keep precedent" and the proposal is discarded. Recommendation: adopt.

## B. Class A openings (product/architecture authority — file-08 owners: Product owner; Product + CLI/output; Semantic/component architecture)
B1. **DR-131** preview non-authoritative `analyze` — candidate `preview-analyze-contract.v2` (D-138). Open Class A
    (application-grade acceptance, no express reservation) → then a SATISFIED-GRADE cycle? Or what must change first?
B2. **DR-133** provider-only TypeScript output — candidate `provider-only-output-contract.v3` (D-136). Same question.
B3. **DR-117** product-boundary successor — candidate `preview-product-boundary-successor.v8` (D-207). Same question.
    (Grok's standing instruction was "do not SATISFY DR-117/131/133"; I will not open Class A without your word.)

## C. Reserved numbers / lists / owners (each keeps a row OPEN until decided)
C1. DR-112 signed-index: quorum/threshold cardinality, clock-skew & last-known-revocation freshness, emergency, waiver
    (OD-112-1..4). Decide now, or defer with an explicit disposition?
C2. DR-118 language-quality: per-row numeric thresholds; matrix corpus acceptance; G13 gate reserved.
C3. DR-111 compatibility: numeric reader-support windows.
C4. DR-126 platform TCB: per-OS allowlist tables / filesystem & version selectors.
C5. DR-121 monorepo CI encodings (provider, YAML, path filters, caches, commands) — or explicitly post-Condition-5.
C6. DR-107 lifecycle encodings (atomic-rename equivalent, quarantine/journal format, lock grammar) — or post-Condition-5.
C7. DR-103 OD-1: assign owner (DR-115 vs DR-120) and set size caps; OD-2 fold (schema shape) — may be delegated to me.
C8. DR-101: OD-101-1 core implementation language (Rust-as-core not minted); OD-101-2 signing ceremony.
C9. DR-115/D-006: unit and tree-accounting for the size threshold (G01/G02 cannot compare without it).
C10. G07 filesystem coverage list (DR-G07 `filesystems.standing` UNPOPULATED).
C11. DR-105/DR-114: FC-C1 joint-owner recording; BLK-1..4 routing (D-032 "still-routed").
C12. DR-124 grant-journal assignment (owner concurrence); DR-127 AL-1/2/5 and AL-3 execution routes.

## D. Delegation scope for fixture authoring (39 obligations)
D1. May I choose fixture shapes / byte-sets / envelope formats on your behalf under D-000 adversarial review where the
    register does not determine them (accepting CONTESTED risk), or do you want to specify them? If delegated, name any
    classes you want to reserve for yourself (e.g. security-sensitive: G08 trust recovery, G09 permissions).

## F. Documentation rewrite after sealing (you agreed in principle on 2026-08-27)
F1. **Restructure:** after the five conditions are met and a final "sealed at HEAD X" COORD entry closes the record, `git mv docs docs-old`
    (history preserved; archive README states the sealing commit and path mapping) and build a new `docs/` that carries only the design:
    accepted contracts (final versions), gate harness specs + corpora (final occupancy versions), the final register, ADR-style condensed
    decisions linking their archival D-NNN, glossary. Condition 5 names `docs/v2/implementation/` literally — the new register must carry
    that path decision explicitly. Every new sentence cites its archival source; each doc gets dual adversarial review for fidelity.
    → Decision-support packet built and byte-verified: `DECISION-PACKETS/F-docs-rewrite.md` (content inventory: design vs process-only, which
    contract/harness versions are final; proposed tree; per-doc templates; derivation/review process; sizing; ten owner options; 23 open
    questions), from the four inventories `DECISION-PACKETS/F-inventory-*.md`. Claude/Codex reconciled recommendation: `DECISIONS-RECOMMENDED.md` §F1.
    Nothing is moved or edited until you approve the structure and the sealing entry exists.

## E. Housekeeping
E1. ~~Untracked cited artifacts~~ — RESOLVED by your commit `078b3d6` (2,518 files). Note: that commit landed while
    component-manifest v9 was under Stage A review; no pinned input moved, so I proceeded (recorded in the D-282 draft).
    Going forward, if you commit mid-act, tell me so I can re-pin before dispatch.
E2. ~~HEAD is 12 commits ahead of origin — push?~~ DONE 2026-08-28: pushed with D-293 (`078b3d6..c10319d`, non-force, fast-forward checked).
E3. ~~Codex shows one usage-limit reset left~~ — re-checked 2026-08-27: weekly limit 99% left (resets 3 Sep). New note: the Codex session at `wC:p1` has only 14% context left; I will run any further review in a fresh `codex --yolo` pane rather than reuse it (no decision needed, FYI).
E4. `STATUS.2026-08-26.md` (modified) and this file (untracked) are your working documents — commit or discard as you prefer; the 31 untracked `_dispatch.*.txt` files are dispatch texts for D-282..D-292 (correction 2026-08-28, from the F packet review: 729 earlier dispatch texts *are* tracked, so "never-committed" was wrong — the F1 recommendation asks you to decide once, before any seal, whether these 31 are committed or deleted).

## G. Round 2 — decisions needed after D-293/D-294 (added 2026-08-28 by the Claude orchestrator at handoff)
The execution phase surfaced questions only you can answer. Each is byte-cited in the plan files named.
G1. **Class A opening entries (owner-controlled, D-293 Decision 5).** DR-117: once D-295 (recording `preview-product-boundary-successor.v10`, dual ACCEPT 0/0 at Stage A with both grade rulings SUSTAINED FOR APPLICATION) is adopted, your entry lifting D-137's reservation and restating the v10/contract.v8 relationship is the next step; it also unblocks G29/G30 fixture authoring. DR-131 and DR-133 (B1/B2 programmes): their openings gate the G24–G28 preview-gate fixtures (`DECISION-PACKETS/D1-plan/README.md`, "sequencing only").
G2. **C-plan owner questions Q0–Q16** (`DECISION-PACKETS/C-plan/README.md` §3): Q0 whether D-293 adopts the round-2 recommendation files or only the round-3 text (governs C2/C3/C4 content); Q1–Q2 OD-112 wording and values; Q3 DR-111 window unit/values; Q4 DR-126 population-packet owner; Q5 DR-126 selectors/tables; Q6–Q7 C5/C6 file-08 echo and gate-2 standing; Q8–Q9 OD-1 caps and MF-6 note; Q10 OBL-OD-2's summary bucket; Q11–Q13 DR-101 language candidates, route, and signing ceremony; Q14 whether C9 successors may write derived byte constants; Q15 G02 accounting authorities; Q16 C10–C12 are outside D-293.
G3. **D1 byte blockers** (`DECISION-PACKETS/D1-plan/`): G15 (adapter, OBL-ADAPTER-IMPL), G16 (unenumerated comparison-basis component axis), G18 (quarantine on-disk format reserved) cannot be authored without values the record lacks; OBL-HOSTILE-GOLDENS per-class counts are unenumerable (author witnesses only, or state counts); DR-122 `FC-OUTFAIL.committed-run-preserved` waits on the §7.1 RunId park.
G4. **Reviewer capacity.** The Claude reviewer/subagent weekly limit was hit at ~14:30 PT 2026-08-28 (resets 5 pm PT); D-295 turn 2 is frozen and dispatched to Codex only — the Claude dispatch is pending the reset (see `HANDOFF.D-000-orchestrator-live.txt`).
