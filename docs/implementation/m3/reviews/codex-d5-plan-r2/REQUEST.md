# Review request: D5-PLAN-r2 (the DR-G21 controls, the fake providers and the escape controls; M3-D r5 items 18 and 27, F-7), round 2

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d5-plan-r2/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, private test keys, held trees, held-out entries, any T2 store or overlay, or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/d5-plan-r2-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 563 bytes, SHA-256 `091699f80bdb2c762ad66ec36e5d0968983699c4fff82061ad140f55b512d05c`. It has 2 members: `d5/PLAN-r2.md` (the subject, 44,878 bytes) and `d5/PLAN-r1.md` (history, unchanged since round 1: `9230130437fa…`). Rehash them.
- **Bases:** product main `4e475c753…` (D3a-4 integrated); architecture `e9474b1fe…`. Read product files at that commit with `git show 4e475c7:<path>` if main moves. The pinned sources' hash prefixes are in the plan's opening table.
- **Round 1:** your `/tmp/opensip-implementation/reviews/codex-d5-plan-r1/REVIEW.md` and `review.json` (REQUIRED-FINDINGS: RF-1 to RF-4 and NBO-1; Q1 to Q5 ruled).

## Round 1 disposition (to verify)

| Round 1 item | r2's answer | Where in PLAN-r2 |
| --- | --- | --- |
| RF-1 (an enforced spawn-file restriction) | A file-bound spawn-site predicate in `check_operability.py`, separate from the census rows. Reachability comes from M3-B's brace-matching test-gate analysis. A production spawn line is refused outside `process.rs`'s `libc::posix_spawn(`. Exceptions are exact `spawnSites` rows `{path, function, pattern, feature}` for test-only-feature code (today the crash-matrix driver), with the feature gate verified. Mutations: a planted call in another platform file with a synchronized census row; the exception row moved; the gate removed. | r2 table; LD-D5-6; §5 D5-0 |
| RF-2 (baseline before widening) | A read-only baseline census at the base, by file, function, key and reachability; today's census is listed site by site. The production set stays exactly `git_tracking::process_environment`, with no crate exempted. `SCAN_SCOPE` is split from `CLIPPY_CRATES` (host and security unchanged). The unmodified base must pass. Mutations: planted production reads in `components` and in a platform production function. | r2 table; LD-D5-6; §5 D5-0 |
| RF-3 (automatic concurrency and the projection) | OPP:277's resolver value (S-OP-5 with J), never a test number, which gates the row. A deterministic projection and an excluded-telemetry list, with telemetry checked separately. C-11's logging and sink invariance cited to its owners. Mutation: the release made conditional on another live supervision. | LD-D5-11; X-D5-7; §5 D5-4 |
| RF-4 (per-API escape outcomes) | Per-API result domains: errno only where the API defines it; `posix_spawn`'s returned number; `EAI_*`; Mach and bootstrap status. Three outcome kinds exactly as MD F-7 states them. Unconfined validity controls; no unconfined public-address egress. DISCLOSURE-ONLY, wrong-reason and missing-execution rules kept. | LD-D5-9; §5 D5-5 |
| NBO-1 (the replay's claim) | The replay validates frames only. Executable smoke controls per script behaviour. No claim that a supervision failure cannot be a fake defect. | LD-D5-3; §5 D5-1 |

## What to review

1. Is each round-1 finding resolved as you required, and is each Q ruling applied?
2. Is the RF-1 predicate's reachability analysis sound? Does it refuse a production spawn even with a matching census row? Is the `spawnSites` exception narrow enough?
3. Is the RF-2 baseline census correct against `4e475c7`, site by site? Is the `SCAN_SCOPE` / `CLIPPY_CRATES` split the deliberate adaptation you asked for?
4. Is LD-D5-11's projection deterministic and sufficient? Is its excluded-telemetry list complete, with nothing that could hide a real result change?
5. Are LD-D5-9's per-API records and validity controls faithful to MD F-7 (:1084-1093) and CFP (:60, :129-134, :181)?
6. Answer Q6 to Q8 of PLAN-r2 §9 with explicit rulings.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...], "rulings": {"Q6": "...", "Q7": "...", "Q8": "..."}}`, with ids `D5PLAN-R2-RF-n` / `D5PLAN-R2-NBO-n`.
