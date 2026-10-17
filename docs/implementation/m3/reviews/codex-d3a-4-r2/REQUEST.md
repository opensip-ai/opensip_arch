# Review request: D3A-4-r2 (the four record events S-OP-2c unblocks; M3-D r5 item 21 with S-OP-2c item 23a), round 2

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d3a-4-r2/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries; in the candidate worktree, `python3 -I -B tools/check_operability.py source --repository .`.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/d3a-4-r2-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 21,571 bytes, SHA-256 `454d5eeb6a96260ed56f7dd208ae96f0fec56f6e86db18146acc79719229b1fa`, 91 members. Rehash every member.
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-d3a4`, detached at product main `7a4be0b0402341481ae388c0cd46877f328de6c2` (S-OP-2c bound as contract successor 177 at `d704ed4`), holding the exact bytes `product-map.json` lists: 16 files, no new path.
- **Round 1:** `d3a-4-r1/` and `d3a-4-r1-subject.json` (`27819282…`) stay as you reviewed them. Your review is copied to `docs/implementation/m3/reviews/codex-d3a-4-r1/`, and `source.json`'s `priorRounds` pins it.

## What to review

1. **SCOPE's round-1 disposition table:** is each of D3A4-R1-RF-1, RF-2, RF-3 and NBO-1 resolved as you required?
   - **RF-1:** `AbsenceClock` (`supervisor.rs`) keeps the last admitted transition apart from the report pacing, with no busy loop. Check the fixed-instant clock control, `slow-long`'s growing reports, and the mutations `absence-report-resets-the-span` and `absence-schedule-ignores-the-report`.
   - **RF-2:** `terminal_observed` is recorded before `reach_terminal`'s early return. Check that `terminal_at`, the grace, the ladder, the first cause and the single terminal fact are unchanged. Check the fault-before-terminal control (on fixed instants through the real `reach_terminal`, with a known 150 ms interval; SCOPE says why a real-run version would only be timing-dependent), the real-run no-terminal fallback control, and the mutations `terminal-time-only-without-a-cause` and `teardown-without-its-trigger-fallback`.
   - **RF-3:** `the_stage_tables_equal_their_sources` compares member by member against the pinned carriers, startup and NE schemas, and the generated enums are matched exhaustively. Check:
     - `provider-reason-substituted-with-references`: same cardinality and length, with `registry.rs` and both references changed together. The registry tests, drift test included, pass on that mutant (`passesExitCode` 0), while the control fails.
     - `reason-source-gains-a-member` and `terminal-source-gains-a-member`.
   - **NBO-1:** LD-D3A4-3's two cases. The pre-Analyze `Unavailable` (`unavailable-early`, P3-21) records its terminal with `native-context-mismatch` and a zero analysis span, and no `crash` is synthesized. Check the mutation `pre-analyze-terminal-dropped`.
2. **No regression** in anything round 1 accepted, and the rules:
   - no new mint call outside operability;
   - no environment read;
   - no `let _ =`;
   - no new dependency.
3. **SCOPE's Self-review section** (the lead's pre-submission checklist), including the disclosed zeros and untested paths.
4. **The lane** `evidence/d3a4-r2-checks/`, including the coordinator-requested serial supervisor runs on the base and the candidate (`supervisor-serial.json`; only the candidate's gates), the base's move from `f16f50d` onto `7a4be0b`, and the three archived attempts SCOPE discloses and all 18 mutations (`controls.json`).

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `D3A4-R2-RF-n` / `D3A4-R2-NBO-n`.
