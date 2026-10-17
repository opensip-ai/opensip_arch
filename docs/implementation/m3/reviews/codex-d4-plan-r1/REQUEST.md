# Review request: D4-PLAN-r1 (manifest admission, request predicates and the session factory, M3-D items 24-26), round 1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d4-plan-r1/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, private test keys, held trees, held-out entries, any T2 store or overlay, or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/d4-plan-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 378 bytes, SHA-256 `a21f8a6dd188fe9da06a4e911763db9acb6634525d226642d68b235a9e7b4424`, 1 member, `d4/PLAN-r1.md`. Rehash it.
- **Bases:** product main `5de9fd4740ea17018d0bd3fbff9496c94ddacda9` (C2a-2 integrated, inventory v226 bound); architecture `dc96415fa99b2df4849dbf3920e9d45739f1ed05`.
- **Main and the architecture HEAD may move while you review,** by other units' integrations and lock-only inventory commits (C1b-1, C2b-0, CI-2/CI-3, D2b-3b, D3a-3). The plan's citations are to the base commits; read product files at `5de9fd4` with `git show 5de9fd4:<path>` where main has moved.

## Authority

- **The law:** M3-D r5 (`docs/implementation/m3/supervisor-d/PROPOSAL-r5.md`), items 24 to 26 (:752-878), with D4-T1 to D4-T4, the r4 and r5 changes tables, items 2, 12 and 22 where the plan cites them, item 30's cross-law records, and the units table row for D4 (:1262).
- **J1 r7** (`docs/implementation/m3/host-pipeline-j/PROPOSAL-r7.md`): R1, R10a, ER10a, rows 56 and 57, S20, J-C10b, J-C20.
- **The neighbours:** C2a plan r4 (`snapshot-plan-c/c2a/PLAN-r4.md`, the Q5 ruling and LD-C2A-1, LD-C2A-10); the component installation law r5 (`component-install/PROPOSAL-r5.md`, items 6 and 7); the D2b plan r3 with A1 and A2; SD-2, SD-5, SD-7 and CR-1 as bound.
- **The sources the plan cites:** PPBS v10, AQ §5, DR103, CMS (and the product's pinned `tools/security/inputs/manifest-schema.json`), the native capability matrix (`crates/host/src/native_capability_matrix.v2.json`), QG's DR-G29 entry, and the product files at `5de9fd4` (`component_manifest.rs`, `trust_ordinary_metadata.rs`, `trust_admitted_components.rs`, `trust/verified_envelopes.rs`, `trust/native_read_session.rs`, `platform/src/process.rs`, `platform/src/work_ledger.rs`, `components/src/supervisor.rs`, `components/src/control_protocol.rs`, `components/src/provider_protocol/ts2.rs`, `host/src/invocation.rs`). The CR-1 materialization is product commit `d579140`; its accepted record is E033 in `docs/implementation/m3/status/2026-10-17-r108/accepted-work.json`.

## What to review

The plan is the lead's draft. Judge:
1. **Coverage:** does D4 deliver items 24 to 26 exactly, with nothing of C2a's, J1's (J2a, J3d, J2c), D3's or D5's taken, and nothing owed left out? Is the standing of D4-T1 (interface-complete, path-owed) and of D4-T2 (unrepresentable at M3) honest?
2. **The split** (LD-D4-1) and its dependencies, especially D4-4's on D2b-3b, D2b-4, CI-3 and X-D4P-2.
3. **The projection** (LD-D4-2): no second parser in components, with the host building claims from security's validated value and the authenticated catalog.
4. **Each class's arm against its sources:** EE-1 (LD-D4-3, Q1), EE-3b (LD-D4-4, Q2), EE-4 (LD-D4-5, Q3), EE-5a in the post-materialization phase (LD-D4-6, Q4), and item 25 (LD-D4-7, Q5). Is anything invented: a member, a list, a constant or a code?
5. **The refusal order and the projection boundary** (LD-D4-8, LD-D4-9; Q8): SD-5's subject rule, every form kept, and records and envelopes left to J1.
6. **The prices** (LD-D4-10, §3): charged before each use, no unpriced allocation, and no profile selected.
7. **The cross-law items:** X-D4P-1, R10a's work profile (Q6); X-D4P-2, the launch recheck through CI-3 (LD-D4-11, Q7); X-D4P-3 and X-D4P-4.
8. **The controls and mutations of §5:** adequate for each sub-unit, with each mutation caught by a test rather than by a compile failure, except where the plan names a compile-time pin.

Answer Q1 to Q9 with explicit rulings.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...], "rulings": {"Q1": "...", ...}}`, with ids `D4PLAN-R1-RF-n` / `D4PLAN-R1-NBO-n`.
