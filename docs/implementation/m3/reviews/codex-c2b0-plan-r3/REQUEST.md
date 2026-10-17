# Review request: C2B0-PLAN-r3 (the C2b-0 implementation plan: the `node_modules` layout; M3-C r8 items 3 and 10), round 3

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-c2b0-plan-r3/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries.

## Subject

- **Manifest:** `docs/implementation/m3/snapshot-plan-c/c2b0-plan-r3-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 956 bytes, SHA-256 `9fa287f4c070d3c6415597c582feb6a2ba247a4968ecb33850f70ce82c094a5d`, 4 members:
  - `c2b/PLAN-r3.md` (the subject);
  - `c2b/PLAN-r2.md` and `c2b/PLAN-r1.md` (history);
  - `c2b/C2B-GATING-r1.md` (context).

  Rehash all four.
- **Bases:** as the manifest names (product `b753854`, unchanged from round 2).
- **Your round 2:** `codex-c2b0-plan-r2` (REQUIRED-FINDINGS: R2-RF-1, R2-NBO-1 to R2-NBO-3, Q6 and Q7 rulings), at `/tmp/opensip-implementation/reviews/codex-c2b0-plan-r2/`.

## Authority

As in round 2, including the amendment **A-C2B0-1**, proposed for acceptance with the plan. Your round 2 found its substance coherent and its required finding unrelated to it. Accepting the plan accepts the amendment, and a REQUIRED-FINDINGS verdict against the amendment rejects both. In addition: `opensip/crates/evaluator/src/native_universe.rs` (:142-147, :235-252, :296-309) and `crates/evaluator/src/lib.rs` (its exports).

## What to review

`PLAN-r3.md` opens with an r3 changes table. Judge:
1. **R2-RF-1** (LD-C2B0-9, LD-C2B0-14): the one shared, bounded evaluator helper `layout_real_path_faults`, exported, which the existing `inspect_typescript_universe` consumer and C2b-0 both call, after schema and order admission. Check:
   - that its step bound and typed `LayoutBound` fit the evaluator's step-budget convention;
   - the byte-identical fault strings and set semantics at the consumer;
   - the regression controls over the existing native-context fixtures;
   - that no context, universe or native identity is fabricated and no second predicate exists;
   - that the retained-context, digest and Plan-selection checks stay with C2b-1 and later units.

   Also check the census claim: no census or model tool pins an evaluator file, so there is no receipt delta, with the companion-receipt caveat.
2. **R2-NBO-1** (LD-C2B0-8): is 26,715 now stated as a conservative, unattainable ceiling in encoded payload bytes, with the boundary controls on real unique layouts?
3. **R2-NBO-2:** the nine parser-variant controls.
4. **R2-NBO-3** (LD-C2B0-5, LD-C2B0-11, LD-C2B0-13): the charged file `fstatat` through the held parent with a complete-observation comparison, for first-party reuse and for alias meetings; the read-set reach control as C1c-1's, carried in C2b-0's lane once available; and no cached-byte or directory-metadata substitute.
5. **The Q6 and Q7 rulings,** applied as stated.
6. **No regression** from rounds 1 and 2.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `C2B0PLAN-R3-RF-n` / `C2B0PLAN-R3-NBO-n`.
