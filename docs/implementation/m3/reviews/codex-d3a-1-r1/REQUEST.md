# Review request: D3A-1-r1 (the supervisor's state machine, loop, joins, normal end and fault ladder; M3-D r5 items 12-15, 17 and 19's normal end), round 1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d3a-1-r1/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries; in the candidate worktree, `python3 -I -B tools/check_operability.py source --repository .`.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/d3a-1-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 15147 bytes, SHA-256 `25dd5d3ca9bbd39842d7634a8a21f5163e18396f727809dcbacba30a82165b87`, 65 members. Rehash every member.
- **The candidate base:** product main `3d1d771ecc5a8772d57f8393ce09cc82ce5f025a` (D3a-0, D2b-2, C1a4 and inventory v221 integrated; 174 contract successors).
- **The lane base:** `26e8df69479f4c69792d9e3c027ac4215ad68e06`. It differs from the candidate base by C1a4's code and the v221 lock, which share none of the candidate's paths, and a post-rebase focused check is recorded (LD-D3A1-7).
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-d3a1`, detached at `3d1d771`, holding the exact bytes that `product-map.json` lists (10 files, 3 new).

## Authority

- the D3a plan r4 (`docs/implementation/m3/supervisor-d/d3a/PLAN-r4.md`; your `codex-d3a-plan-r4`, ACCEPT, with the LD-D3A-17 amendment), sub-unit D3a-1 and LD-D3A-3 to LD-D3A-7, LD-D3A-9, LD-D3A-13 to LD-D3A-15;
- law M3-D r5 items 10 to 15, 17 and 19 (`supervisor-d/PROPOSAL-r5.md`), with D3-T1 to D3-T8, D3-T10 and D3-T11 as the plan scopes them to D3a-1;
- D2a's `ControlSession` (accepted `codex-d2a-r2`), D2b-1's `FrameAccumulator` (`codex-d2b-1-r2`), D2b-2's table engine and D3a-0's platform mechanisms, as integrated.

## What to review

`SCOPE.md` gives the change table, LD-D3A1-1 to LD-D3A1-7, five open questions, the tests and the checks. Judge:
1. **The state machine and single settlement** (item 12; LD-D3A-5):
   - the states and their transitions;
   - the private construction under the terminal guard;
   - the take-once settlement;
   - later triggers kept, and late events counted and dropped;
   - the bounded cross-thread channel;
   - `Drop`'s kill-once, reap to the ceiling, abandon, scratch removal and `abandoned` (LD-D3A-14).
2. **The readiness loop and the yield contract** (item 12, :449; LD-D3A-3; LD-D3A-13; LD-D3A1-1):
   - the platform's `wait_ready` (`poll(2)`), with no policy;
   - every wait bounded by its deadline;
   - the fixed service order;
   - one participant read and one write per turn;
   - the loop never touching fd1 or fd0.
3. **The control acquisition and handshake** (LD-D3A-4): the prefix judged before any body byte; no read past a frame; an over-bound prefix refused alone; sends only through `ControlSession::send`; the observations advanced.
4. **The joins** (item 13): EOF before the terminal delivered at once; EOF after it held; the death appended after J-3's drain; the protocols' process events only; `deadline` delivered only for the wall clock and the normal-exit grace. Judge LD-D3A1-5 (the first cause of an early death) and Q-D3A1-5.
5. **The normal end** (LD-D3A-15) and **the fault ladder** (LD-D3A-6, LD-D3A1-4): T-1's cancel reasons, T-2 at once, T-3 after the escalation, T-5 at the ceiling, and the normal end entering at T-2.
6. **Waits, liveness, progress and stderr** (items 14, 15 and 17): item 14's constants as cited, with Rust3's waits only from the participant (LD-D3A-7); health in STEADY; liveness never from traffic; progress only from admitted transitions; stderr counted in a fixed buffer, never held.
7. **The seam** (LD-D3A-3): `Participant`, `ParticipantStep`, the one-shot `TerminalOutput`, `ProcessEvent` with LD-D2B-6's shape, and the `Pushed` interface note.
8. **The fixture** (LD-D3A-9 r4, LD-D3A1-6):
   - harness-free;
   - located by the lane-written path and SHA-256, with no environment read;
   - `test-fixture` reached only from dev-dependencies;
   - the raw fd1 control;
   - the test-only `/bin/sh` group member.
9. **The open questions** Q-D3A1-1 to Q-D3A1-5: the scratch-fate and exit-absence cases beyond the law's closed sets, the RF7 nonce mismatch, a control `fault` frame, and an early death's later trigger. Say which are findings.
10. **The lane** `evidence/d3a1-checks-r1/`, SCOPE's attempt history, and **LD-D3A1-7's post-rebase check** (`evidence/d3a1-postrebase-check/`: components 64 passing, platform `process_tests` 32 passing, each as in the lane). Is keeping the lane with that check sufficient for this base difference?
    - components 43 → 64 and platform 328 → 329, with equal failure sets;
    - Clippy, rustfmt and the workspace check;
    - the fixture record, the edges, the feature scope, the environment exceptions, operability, the unchanged closure and verify_design;
    - twelve mutations.
11. **Rules:** no new mint-census call, no environment read, no `let _ =`, no async runtime or new third-party dependency (the lock gains one internal edge only).
12. **Inventory:** two new rows, and `supervisor.rs` realizing its planned row.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `D3A1-R1-RF-n` / `D3A1-R1-NBO-n`.
