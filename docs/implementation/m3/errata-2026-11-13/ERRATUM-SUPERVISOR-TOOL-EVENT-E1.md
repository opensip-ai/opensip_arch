# Erratum SUPERVISOR-TOOL-EVENT-E1: a tool's unavailable confinement has its own event (author draft, 2026-11-13)

Status: **PROPOSED.** It drafts the candidate `LC/sup-disclose-1/a/ERRATUM-CANDIDATE.md` (`LC` =
`/Users/sb/code/.opensip-implementation-cache/lead-2026-10-25`), checked against the independent code review's point 5
(`LC/sup-disclose-1/a/review-opus/VERDICT.md:161-180`). It is **additive**: the accepted bytes stay frozen. It decides
one sentence and nothing else.

Corrects one accepted text: **law M3-D r5** (the supervisor and common control law), accepted 2026-10-04 by Grok:
`docs/implementation/m3/supervisor-d/PROPOSAL-r5.md`, 209,266 bytes, sha256
`224b9228e9d7c0bc11c848c88cd2ed7fa7da8734208c45d70fbb678a97afec6d`. The live `PROPOSAL.md` (209,670 bytes, sha256
`36c26161…`, unchanged at architecture main `a4b46e107`) is r5 plus an acceptance note; its line numbers are r5's plus 2.

**Which record form applies.** No `supervisor-d/PROPOSAL*.md` path is in the product's `design-lock.json` (main
`1bd328f3`). So the form is an erratum with an adoption receipt (`ADOPTION-SUPERVISOR-TOOL-EVENT-E1.md`, not yet written),
as `ERRATUM-SUPERVISOR-LINUX-E1.md` beside this file.

## STE1.1 The accepted sentence

Live `supervisor-d/PROPOSAL.md:1053` (r5 `:1051`), item F-4:

> - **Unavailable means disclose and continue.** Providers and tools launch unconfined (item 2), and each launch is recorded as `supervision.confinement.unavailable {reason}` (an ordinary registration). The public carrier for "provider ran unconfined: <reason>", which sits beside Coverage and never inside it, is **CF-2** (M3P:504), a WS output successor or S-OP-6 join. Until CF-2 lands, M3 has no public command (J1 item 1), and the disclosure reaches the operational record and the harness.

## STE1.2 Why it cannot be carried out as written (verified)

- **The provider event needs what a tool lacks.** Product main `1bd328f3`, `crates/operability/src/kinds/registry.rs:2253-2265`
  (on `sup-disclose-1a-r1` the same block is `:2256-2268`): `name: "supervision.confinement.unavailable"`,
  `requires: IdentitySet::ProjectPlanExecution`, `template: "provider launched unconfined: confinement unavailable"`,
  required fields `role P0 req: Code<ProviderRole>`, `universe P1 req: Universe`, `reason P0 req: Code<ConfinementUnavailable>`.
  (The review cites `registry.rs`; the file is `crates/operability/src/kinds/registry.rs`.)
- **The law already makes tool events Project-only.** Item 21, live `PROPOSAL.md:694` (not `:692`, which the review and
  the code comment cite; `:692` is `supervision.scratch.retained`): "**`tool.process.spawned`** and **`tool.process.reaped`**,
  which require **Project only**, because a tool runs before PlanId (finding F6; SOP2 item 9)". And `:698`: "Provider events
  also carry Project, Plan and Execution".
- **A new event is an ordinary registration.** S-OP-2 r6 (accepted, `operability/s-op-2/PROPOSAL-r6.md:226-227`): "A
  code unit may add any of these without a new successor …: an event or a field". `:229` admits "a code table or member",
  so the reason list is open: the product's `ConfinementUnavailable` table (`registry.rs:1237-1243` on the branch) has five
  members, and no law text lists them (the review's LAW-CHECK-Q4; the law names one reason, `not-selected`, only in the
  row of option A, live `:943`, which was not taken).

So recording a tool under `supervision.confinement.unavailable` would need a Plan, an Execution, a role and a universe
that a tool launch does not have.

## STE1.3 The amendment

In `:1053`, the words "and each launch is recorded as `supervision.confinement.unavailable {reason}` (an ordinary
registration)" are read as:

> and each provider launch is recorded as `supervision.confinement.unavailable {reason}` and each tool launch as `tool.confinement.unavailable {reason}`, which requires Project only (item 21), each an ordinary registration; the provider event is unchanged (erratum SUPERVISOR-TOOL-EVENT-E1).

The rest of `:1053` is unchanged.

## STE1.4 The alternative, and why it is not taken

Keep the law's name and change `supervision.confinement.unavailable`'s schema so that Plan, Execution, `role` and
`universe` are absent for tools. Not taken:
- it weakens the provider record: a provider disclosure with no Plan, role or universe would then be valid;
- it contradicts item 21's rule that tool events require Project only (`:694`);
- the event's template says "provider launched unconfined", which would be false for a tool.

## STE1.5 What this does not change

- The provider event, its identity set, fields, template and reason table.
- The rest of F-4: "available but an apply step fails means refuse the launch" (`:1054`), CF-2 as the public carrier,
  and `supervision.confinement.applied {profile, abi}` (`:1055`). Whether a confined tool's `applied` record has the
  same problem is not decided here; today no tool profile ships, so a tool is always unavailable (`profile-absent`).
- Item 21's list (`:689-695`, "under O7, F-4's two confinement events") is not reworded; the tool event is a further
  ordinary registration under S-OP-2 r6 `:226-227`.
- No reason code, privacy class or export rule.

## STE1.6 Review and binding owed

- **Review: two independent reviewers.** M3-D is security-boundary law (OD-PACE-1 rule 4, `OD-PACE-1.md:30-31`; the
  candidate says the same).
- **Code resting on it (at risk until this binds):** the tool-event commits on product branch `sup-disclose-1a-r1`:
  `d7be820b` (tests) and `18f7033e` ("tools disclose like providers, through tool.confinement.unavailable, reason
  profile-absent"); `bad0bea4` closes mutants on the same code.
- **Binding owed:** the lead's receipt `ADOPTION-SUPERVISOR-TOOL-EVENT-E1.md` pinning this file's sha256. No design-lock entry.
