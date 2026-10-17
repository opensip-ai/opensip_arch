# Review request: D3B-PLAN-r1 (tree kill, cancellation, revocation and harness coexistence, M3-D items 18, 19 and 23), round 1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d3b-plan-r1/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/d3b-plan-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 380 bytes, SHA-256 `d601b12770366661eca0ea3e68e8123a9771aa7d7cb6df90798d214d599d30f4`, 1 member, `d3b/PLAN-r1.md`. Rehash it.
- **Bases:**
  - product main `5de9fd4740ea17018d0bd3fbff9496c94ddacda9` (inventory v226; D1a and D3a-0 to D3a-2 integrated);
  - architecture HEAD `dc96415fa99b2df4849dbf3920e9d45739f1ed05`.
- **Main may move while you review,** by lock-only inventory commits and by other units' integrations (C1b-1, D3a-3, D2b-3b and others). D3a-3 and D2b-3b touch `supervisor.rs`. Judge the plan against `5de9fd4`, and against the in-flight neighbours named below as context only.

## Authority

- **The law:** M3-D r5 (`docs/implementation/m3/supervisor-d/PROPOSAL-r5.md`):
  - items 18 (:579-628), 19 (:629-663) and 23 (:734-751);
  - item 14's constants (:479-508);
  - item 4's reap-last rule (:241-264);
  - item 8's platform scope (:329-347);
  - item 12's concurrent-trigger rule (:447);
  - item 22's routes (:705-733);
  - the units table's D3b row (:1244-1288).
- **The accepted neighbours:**
  - the D3a plan r4 (`supervisor-d/d3a/PLAN-r4.md`) and its review `docs/implementation/m3/reviews/codex-d3a-plan-r4/` (or `/tmp/opensip-implementation/reviews/codex-d3a-plan-r4/`);
  - the D2b plan r3 with A1 and A2 (`supervisor-d/d2b/`), especially LD-D2B-7;
  - M3-L r7 item 16 (`provider-protocol-l/PROPOSAL-r7.md`:942-1013);
  - SL S6 (`docs/v2/contracts/product-v1/security-and-lifecycle.md`:466-497);
  - S-OP-2 r6 item 23 (`operability/s-op-2/PROPOSAL-r6.md`:870-905).
- **The product on main:**
  - `crates/platform/src/process.rs` (D1a and D3a-0);
  - `crates/platform/src/clock.rs`;
  - `crates/components/src/supervisor.rs` (D3a-1 and D3a-2);
  - `crates/components/src/control_protocol.rs`.
- **In-flight context, not authority:**
  - D3a-3 r2's scope (`supervisor-d/d3a-3-r2/SCOPE.md`, `BLOCKED-TABLES.md`, `carried-obligations.json`), with its candidate in worktree `/Users/sb/code/opensip-ai/opensip-d3a3`;
  - D2b-3b's candidate in worktree `/Users/sb/code/opensip-ai/opensip-d2b3b` (`crates/components/src/provider_protocol/ts2/participant.rs`).

## What to review

The plan is the lead's draft. Judge:
1. **Coverage.** Does D3b deliver items 18, 19 and 23 exactly on this host's macOS family? Does it leave Linux to D3b-L, the G21 rows to D5, and signal delivery, the observer and routes to J1, SL S6 and J2? Does it duplicate nothing D3a or D3a-3 already provides?
2. **The split and the platform additions** (LD-D3B-1 to LD-D3B-3; Q1): within D1a's no-policy rule, with every buffer and walk bounded by item 18's own count?
3. **The descendant step** (LD-D3B-4, LD-D3B-5; Q3, Q9): item 18's macOS order exactly, its truthful `tree` report and `supervision.tree.swept`'s counts.
4. **User cancellation** (LD-D3B-6 to LD-D3B-8; Q4 to Q7): the seam, the cross-plan implementation rule, the stage-1 order, the grace's anchor, the second signal, `userInterrupted`, and the signals outside stage 1.
5. **Revocation and fail-stop** (LD-D3B-10; Q2): the ladder, the 5 s ceiling, S6's marks measured on SL's clock, and the two distinct causes.
6. **Records** (LD-D3B-9; Q8): the producers of D3a-3's registered events, and the two proposed ordinary registrations with `RevocationMark`.
7. **Item 23** (LD-D3B-12): each point dispositioned, with the structural no-cgroup control.
8. **Constants and tables** (LD-D3B-13): is every wait, bound and member cited to the law or its sources, with nothing invented?
9. **The checks and mutations** of §3: are they adequate for each sub-unit?

Answer Q1 to Q9 explicitly.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...], "rulings": {"Q1": "...", ...}}`, with ids `D3BPLAN-R1-RF-n` / `D3BPLAN-R1-NBO-n`.
