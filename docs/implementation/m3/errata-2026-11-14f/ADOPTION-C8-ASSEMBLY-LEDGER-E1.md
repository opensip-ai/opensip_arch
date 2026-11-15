# C8-ASSEMBLY-LEDGER-E1: adopted at r5 (lead, 2026-11-14 UTC)

`LC/stack-fix-1/u4/ERRATUM-C8-ASSEMBLY-LEDGER-E1-r5.md`, sha256
`efdd03d0d5228e9793cfac35d78c2f8a8512ac478f90c56562f671ad2c908c19` (42,560 bytes), is adopted as an erratum to M3-C
r8/r9 item 2 "Ledger" and to the J3d-TS composition's builder (seam 3.26): what pays for the Run's assembly between
Plan admission and the mint. It was written under the lead's Decision A and the rulings added after the erratum draft
(E-1 to E-8, E-9, E-10), all in `LC/stack-fix-1/LEAD-DECISIONS.md`.

What it amends (the files are not edited):
- M3-C (`ARCH/docs/implementation/m3/snapshot-plan-c/PROPOSAL.md`, = **M3C**; r8 with the r9 note, M3C:5), item 2
  "Ledger" (M3C:251-261), which names only the walk. This adds the producer's work, the reread and the seeding to the
  same ledger.
- M3C:261's census obligation is **deferred, not removed**, as statement 6 says; its gate is LD-DEC-5 item 8 (before
  analysis is wired to the command line).
- MJ row 36 (`host-pipeline-j/PROPOSAL.md`:808) and X5 item 5's structural row (X5 `PROPOSAL.md`:79) are also taken
  by statement 2's host pre-check, which is not a replay refusal.
- The J3d-TS composition's interim Q67 arrangement ("C8 opens its own snapshot-profile ledger for `produce`",
  `LC/j3d-ts/QUESTIONS.md`:1193), which is withdrawn.

Accepted by both reviewers at these bytes, each by that digest: Codex `stack-review/packets/codex-U4E/VERDICT-r5.md`
(sha256 81578386aa48513fa193478246dcaac9f82da9ed8a9783a58fbde52a140781b9), Claude
`stack-review/packets/claude-U4E/VERDICT-r5.md` (sha256
c4ad52a0f6286e2e4d5b32904a8ac3ed2feb8b769ac671c9546868bbe6838ccf). History: r1 (the drafter); r2 (the drafter, from the
lead's rulings E-1 to E-8), reviewed by both with required findings (Claude RF-1 to RF-8; Codex U4E-R1 to U4E-R4); r3
(the drafter, every required finding upheld); r4 (the lead, three edits), reviewed with one required finding from Claude
(RF-R4-1) and two from Codex (U4E-r4-R1 and U4E-r4-R2); r5 (the lead), accepted by both (ACCEPT).

What it binds (the text governs; this is a summary): capture, the inventory-inputs producer and custody assembly share
the invocation's one snapshot ledger, with its cumulative usage and failure latch, and no ledger is opened for the
reread or the seeding; a size pre-check is made once before the producer runs; the avoidable work is removed first; the
census is owed and the controls the implementing unit delivers are stated. The numbered statements of the text, not
this summary, are the requirements.

Recorded with the adoption:
- Open item (one), for the owner's post-M3 list: the structural row names the provider for a host sizing limit.
- Left to the implementing unit as stop-and-report checks, before the join's limit is set: the cap on the planned-program
  count P, taken from the first of three bases the unit can show at an enforcing line; whether the returns of a TS2
  session that breached its response bound are excluded before fact admission; and where the number of TS2 sessions is
  capped. If none can be shown, the unit stops and reports and does not set the limit.
- Claude's r5 advisory (A-R5-1, not a change to the text): basis (3) says "per accepted program", but P counts distinct
  planned programs while the native vectors have one entry per retained program, duplicates included; the unit should
  say whether its minimum charge per program bounds the distinct count or the raw count (if it uses the up-front
  `reserved(n)` charge, the bound is on the raw count n, and n is at least P, so it bounds both).
- The census of the snapshot ledger is owed. A lawful repository that ends on row 21 is a host defect under LD-DEC-5
  items 1, 4 and 8, and the census gates the wiring of analysis to the command line.
- Recorded as owed elsewhere: one owner of the source blobs (R-1); the participants' sealed reads (R-2).

It accepts requirements only: no implementation, price, census, integration or Run gate.
