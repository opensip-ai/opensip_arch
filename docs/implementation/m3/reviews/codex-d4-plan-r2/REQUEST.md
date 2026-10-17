# Review request: D4-PLAN-r2 (manifest admission, request predicates and the session factory, M3-D items 24-26), round 2

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d4-plan-r2/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, private test keys, held trees, held-out entries, any T2 store or overlay, or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/d4-plan-r2-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 588 bytes, SHA-256 `17674885db05827e292504141ab68ec7372554523633687c7d966fca36902c6d`. It has 2 members: `d4/PLAN-r2.md` (the subject) and `d4/PLAN-r1.md` (history, unchanged since round 1). Rehash them.
- **Bases:** product main `d704ed4` (D3a-3 integrated; inventory v227; contract successor 177); architecture `9415426c053c8e2b287022f5db4dd380024d120a`. Read product files at that commit with `git show d704ed4:<path>` if main moves.
- **Round 1:** `/tmp/opensip-implementation/reviews/codex-d4-plan-r1/REVIEW.md` and `review.json` (REQUIRED-FINDINGS: RF-1 and RF-2; Q1 to Q9 ruled).
- **Companion, reviewed separately:** CI-A3 r1 (`docs/implementation/m3/component-install/CI-A3-r1.md`, request `codex-ci-a3-r1`), the amendment D4-4 waits on. Do not review CI-A3 here. Check only that PLAN-r2's X-D4P-2 list matches what CI-A3 is said to define.

## Round 1 disposition (to verify)

| Round 1 item | r2's answer | Where in PLAN-r2 |
| --- | --- | --- |
| D4PLAN-R1-RF-1 (ordering and membership pricing) | `admit`'s algorithm specified and priced: two `u32` index buffers and a charged merge sort (CI-A1-b), a duplicate pass refusing `DuplicateDigest`, count and fill passes in sorted order, sorted borrowed policy slices probed by charged binary search (CI-A2-c's price), the explicit-trust probe, a static pinned provider-relation table, and the reserved slice view priced; complexity restated; independent accounting controls with one-unit-short checks per site | LD-D4-2, LD-D4-8, LD-D4-10, LD-D4-13; §3; §5 D4-1 |
| D4PLAN-R1-RF-2 (budget and observation failures across the seam) | `RecheckFailure {Budget, Io, Corrupt(cause)}` and `FactoryRefusal`, each on its existing route per CI r5 item 8 (MISSING for `Absent`); the recheck-I/O matrix row carried as a J2 gate (X-D4P-5); controls through the factory for one unit short, I/O and each mismatch, with no spawn and zero snapshot bytes | LD-D4-11; X-D4P-5; §5 D4-4 |
| Q1 (EE-1 from the authenticated association) | provenance read from the catalog release row the reader joined; the lend is constructible only from `AuthenticatedComponent`; the empty M3 list is an explicit policy choice | LD-D4-3, LD-D4-12 |
| Q2 (EE-3b backstop) | pinned matrix projection; no authority claimed outside CMS; `fact` and `candidate-only` members excluded in controls | LD-D4-4 |
| Q3 (the nested closed-world pin) | covers top-level and nested `$defs` property sets and the nested claim types | LD-D4-5 |
| Q4, Q5 | unchanged, as ruled | LD-D4-6, LD-D4-7 |
| Q6 (SD-9) | lead decision LD-D4-SD9: the lead owns SD-9 with the J1 and D4 admission owners; owed; gates production R10a/ER10a, C2a-4, J3d and J2c, and no pure D4 sub-unit | LD-D4-SD9; X-D4P-1 |
| Q7 (CI-A3 before D4-4) | D4-4 waits for CI-A3's acceptance; the list of what CI-A3 must define; the pin held through spawn by the operation's capability | LD-D4-11; X-D4P-2 |
| Q8, Q9 | `Cleared` carries the sorted digests for the wiring's comparison; J-C10b's path-owed cases listed | LD-D4-8; §1; §7 |
| Review notes (D4-4's comparison sources; the reader's reserved set) | independent authorities per compared value; the reader's set moved into `Evidence` and borrowed | LD-D4-11; LD-D4-13 |

## What to review

1. Is each round-1 finding resolved, and is each Q condition applied?
2. Is D4-1's priced model now complete: every allocation, comparison and probe charged before its work, with the stated complexity?
3. Is RF-2's refusal sum faithful to CI r5 item 8 and J1 r7's rows 2, 11 and 28, with no code invented and nothing collapsed?
4. Is the D4-2 ordering after CI-2/CI-3 (§6) and D4-4's gating on CI-A3, D2b-3b, D2b-4, CI-3 and C4a stated correctly?
5. Answer Q1 to Q5 of PLAN-r2 §8 with explicit rulings.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...], "rulings": {"Q1": "...", ...}}`, with ids `D4PLAN-R2-RF-n` / `D4PLAN-R2-NBO-n`.
