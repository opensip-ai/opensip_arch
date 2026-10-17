# Review request: D3A-PLAN-r1 (the supervisor plan, M3-D items 12-17 and 20-22), round 1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d3a-plan-r1/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/d3a-plan-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 380 bytes, SHA-256 `83a1581edd2c28975e4c36fec72350c5c49ffc48fa08edf89d76e34d68f955af`, 1 member, `d3a/PLAN-r1.md`. Rehash it.
- **Bases:** product main `a9a84a6fd369e7ca10689d6ab432bead3ad7eef2` (D1a and D2a integrated); architecture HEAD `1649a041df87555d682b4a5c30aeda67b16c6d97` (the D2b plan r3 published).
- **Main may move while you review,** by lock-only inventory commits and by C1a3's or D2b-1's integration (host, security, identity and components files). None changes D1a's `process.rs` or D2a's `control_protocol.rs`.

## Authority

- **The law:** M3-D r5 (`docs/implementation/m3/supervisor-d/PROPOSAL-r5.md`), section C, items 12 to 17 and 20 to 22, with the units table row for D3a and its controls (D3-T*), and the items D3a's interfaces touch (1, 10, 11, 18, 19, 23).
- **The accepted neighbours:** D1a (`crates/platform/src/process.rs` on main), D2a (`crates/components/src/control_protocol.rs` on main), and the D2b plan r3 (`d2b/PLAN-r3.md`, especially LD-D2B-6's `ProcessEvent` and LD-D2B-15).
- **S-OP-2 and O1's registry** (`crates/operability/` on main), and the sources the plan cites.

## What to review

The plan is the lead's draft. Judge:
1. **Coverage:** does D3a deliver items 12 to 17 and 20 to 22 exactly, with nothing of D3b's (items 18, 19, 23) or D4's taken, and nothing owed left out?
2. **The split and the interim ladder** (LD-D3A-2, LD-D3A-6; Q1).
3. **The seams:** the `Participant` (LD-D3A-3) against items 10 and 11, `ProcessEvent` ahead of D2b-3 and D2b-4 (Q2), and the control channel's bounded acquisition (LD-D3A-4), which D2a's review left to D3a (D2A-R1-NBO-2).
4. **Settlement** (LD-D3A-5): is a second settlement unrepresentable, and does every path reach `Settled`?
5. **Constants** (LD-D3A-7, LD-D3A-8, LD-D3A-12): is every wait, ceiling and bound cited to the law or its sources, with nothing invented?
6. **Fixtures** (LD-D3A-9; Q3), **records** (LD-D3A-10; Q4) and **the outcome join** (LD-D3A-11; Q5).
7. **The platform additions** (the sampler and the bounded scratch walk): within D1a's no-policy rule?
8. **The checks and mutations** of §3: adequate for each sub-unit?

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `D3APLAN-R1-RF-n` / `D3APLAN-R1-NBO-n`.
