# Review request: C2B0-PLAN-r2 (the C2b-0 implementation plan: the `node_modules` layout; M3-C r8 items 3 and 10), round 2

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-c2b0-plan-r2/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries.

## Subject

- **Manifest:** `docs/implementation/m3/snapshot-plan-c/c2b0-plan-r2-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 767 bytes, SHA-256 `69965663f63834ffd4a1c69a2fd8308596b800175a9e90576bd77054bbd2f7b7`, 3 members:
  - `c2b/PLAN-r2.md` (the subject);
  - `c2b/PLAN-r1.md` (history);
  - `c2b/C2B-GATING-r1.md` (the prior gating record, context).

  Rehash all three.
- **Bases:** as the manifest names. Product is `b753854`; since round 1's `3d1d771` it moved only by D2b-0b's generation and its lock, which touch no file the plan cites.
- **Your round 1:** `codex-c2b0-plan-r1` (REQUIRED-FINDINGS: RF-1 to RF-4, NBO-1, NBO-2, Q1 to Q5 rulings), at `/tmp/opensip-implementation/reviews/codex-c2b0-plan-r1/`.
- **Related, in review separately:** the C1c plan r4 (`snapshot-plan-c/c1c/PLAN-r4.md`). This plan depends on its C1c-0 interface and is revised if that review changes it.

## Authority

As in round 1. In addition:
- the C1a plan r6 (`c1a/PLAN-r6.md`:119, :194) and the r9 law record (`c1a-r9/RECORD-r9.md`:138, :195), which **amendment A-C2B0-1** changes for C2's layout reads only;
- item 1's C1-T24 (`PROPOSAL.md`:230);
- the C1c plan r4's LD-C1C-2, -5, -6, -9, -12 and -13;
- Node's documented `NODE_MODULES_PATHS`, cited as the traversal's source.

**This round proposes amendment A-C2B0-1 for acceptance with the plan** (LD-C2B0-11). It changes four statements: C1a plan r6:119 and :194, and the r9 record's §3 Q2 and its outside-r9 list. It moves C2's layout captures to the snapshot ledger and orders the layout after the walk. The r9 caps are unchanged. Accepting the plan accepts the amendment. A REQUIRED-FINDINGS verdict against the amendment rejects both.

## What to review

`PLAN-r2.md` opens with an r2 changes table. Judge:
1. **RF-1** (LD-C2B0-1): are the search directories, `NODE_MODULES_PATHS` of each `realPath` restricted to the project, complete for npm, nested-npm, pnpm (the virtual-store parent and `.pnpm/node_modules`) and workspace-link layouts, with no wholesale `.pnpm` scan? Check the fixtures' visited-set assertions.
2. **RF-2** (LD-C2B0-13): the worklist, the `searched` and `real_seen` sets and the row map; reuse, `Inconsistent` and aliases; a symlink chain refused while a dependency cycle terminates; the controls for shared targets, the diamond and the A→B→A cycle.
3. **RF-3** (LD-C2B0-6, LD-C2B0-14): the two interfaces C2b-0 owns, `reach_directory` and `excluded_path`. Does `excluded_path` classify first-party targets separately from `read_set_path`'s dependency-tree eligibility, with every exclusion kept and no-open/no-read controls? Is ordering the layout after the walk, which gives `WalkEvidence` and the walk's captures, right (Q6)?
4. **RF-4** (LD-C2B0-7): joining only before a freeze, otherwise owning a new interval, cumulative tracking, and receipt-specific deltas (both receipts change).
5. **NBO-1** (LD-C2B0-5): the named `canonical::parse` profile and the typed `Profile(variant)` refusal, with one case per variant.
6. **NBO-2** (LD-C2B0-8): the count predicate tested alone, and the 4 MiB encoder bound. Is the largest admitting record of 26,715 rows right by the stated row arithmetic? Check `Encoding`.
7. **Q4 and Q5:** the refused layout's capture set and the composition obligation (LD-C2B0-12); the ledger and the A-C2B0-1 reconciliation (LD-C2B0-7, LD-C2B0-11).
8. **The empty and absent policy** (LD-C2B0-10), and the parse handoff (LD-C2B0-5, Q7).
9. **No regression** from round 1.
10. **Rule on Q6 and Q7.**

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `C2B0PLAN-R2-RF-n` / `C2B0PLAN-R2-NBO-n`.
