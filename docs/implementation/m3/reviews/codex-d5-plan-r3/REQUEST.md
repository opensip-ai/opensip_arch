# Review request: D5-PLAN-r3 (the DR-G21 controls, the fake providers and the escape controls; M3-D r5 items 18 and 27, F-7), round 3

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d5-plan-r3/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, private test keys, held trees, held-out entries, any T2 store or overlay, or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/d5-plan-r3-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 748 bytes, SHA-256 `c2a66656b043cdbd5d89e9e2d697d82e64df4cc86277e944d1121ae88f348283`. It has 3 members:
  - `d5/PLAN-r3.md`, the subject (56,565 bytes);
  - `d5/PLAN-r2.md`, history, unchanged since round 2 (`b09274a915bb…`);
  - `d5/PLAN-r1.md`, history, unchanged since round 1 (`9230130437fa…`).

  Rehash them.
- **Bases:** product main `4e475c753…`; architecture `e9474b1fe…`. These are the same as round 2. Read product files with `git show 4e475c7:<path>` if main moves.
- **Round 2:** your `/tmp/opensip-implementation/reviews/codex-d5-plan-r2/REVIEW.md` and `review.json` (REQUIRED-FINDINGS: RF-1 to RF-4 and NBO-1; Q6 to Q8 ruled).

## Round 2 disposition (to verify)

The "r3 changes" table at the top of PLAN-r3 answers each item. r3 changes only:
- LD-D5-6: the shared reachability graph, and D5-S1's three rules;
- LD-D5-9: per-attempt validity, with the POSIX `setsid` exception;
- LD-D5-11: the evidence states, the interaction control and the determinism contract;
- §5's matching controls and mutations;
- §9.

| Round 2 item | r3's answer |
| --- | --- |
| RF-1 (the launcher's `execve`) | Three separate rules after MD:192:<br>• `posix_spawn` file-bound to `process.rs`, with `Command`, `fork` and `vfork` refused except the exact test-only-feature rows;<br>• the PATH-search family refused everywhere, with no exception;<br>• one pinned `launcherExec` row for D1b's launcher, empty until D1b's review adds it, with no app or crate exemption.<br>Positive and negative controls in a temporary tree. |
| RF-2 (reachability) | `tools/rust_reachability.py`, a shared helper: Cargo target roots; external `mod`, `#[path]` and `include!` edges; `cfg(test)` and exact feature gates propagated; fail-closed on anything unparsed. Any production path blocks an exemption. The crash-matrix exception is validated through its gated ancestor chain. Controls: an external test module, a production `#[path]` helper, a file on both edges, and the shared fake source. |
| RF-3 (POSIX `setsid`) | Validity is per attempt. The provider's `setsid` expects POSIX `EPERM` both confined and unconfined, is labelled `posix-session-leader`, and is never credited. There is a non-leader sanity child, and a mutation that credits it as Seatbelt's. |
| RF-4 (automatic = 1) | Three evidence states: zero fit, automatic = 1 (interaction evidence outstanding), and automatic > 1. A separately labelled interaction control with asserted overlap. The mutation is caught only by a genuine overlap, or else recorded as not run. |
| NBO-1 | Strict fields for every script. The reap signal, later causes and stderr counts are compared only under a named per-script determinism contract, otherwise checked against their allowed set. |

## What to review

1. Is each round-2 finding resolved as you required, and is each Q6 to Q8 ruling applied?
2. Is the reachability graph's classification sound and fail-closed? Is the `launcherExec` row narrow enough, with the right ownership?
3. Does anything else in r3 regress what rounds 1 and 2 accepted?
4. Answer Q9 of PLAN-r3 §9 with an explicit ruling.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...], "rulings": {"Q9": "..."}}`, with ids `D5PLAN-R3-RF-n` / `D5PLAN-R3-NBO-n`.
