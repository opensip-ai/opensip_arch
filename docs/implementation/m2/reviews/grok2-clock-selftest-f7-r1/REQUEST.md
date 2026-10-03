Grok review: F7, a test-only fix for a date-dependent flake in X9-1's platform self-test `a_scripted_clock_gives_each_ordinal_its_own_increasing_wall_seconds`. Claude Opus 5.5 leads, and you are the single reviewer. Make no repository edits, commits, pushes or delegations. Write only under `/tmp/opensip-implementation/reviews/grok2-clock-selftest-f7-r1`.

**Subject.** The subject is the worktree `/Users/sb/code/opensip-ai/opensip-f7`, detached at product main `eb0d503` (X9-3). Save `git -C /Users/sb/code/opensip-ai/opensip-f7 diff` as `subject.diff`; it is 1459 bytes with sha256 `31128abbbb408ad20fc9227eb06cc3d86c8aa20d05fb6c657a5b36aeaffa1dac`. It changes one file, `crates/platform/src/crash_barrier/self_tests.rs`. That file is the crash barrier's self-test module (`mod self_tests;` in `crash_barrier.rs`), and it builds only under the test-only `crash-matrix` feature. No product code changes, and no file is added or removed, so there is no inventory successor.

Toolchain: `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin`, with your own `CARGO_TARGET_DIR` and a private 0700 `TMPDIR` under `getconf DARWIN_USER_TEMP_DIR`. Never touch the real `~/Library/Application Support/OpenSIP`; it is absent. **Do not run crash-matrix lanes or full workspace lanes.** Another unit's timing-sensitive lead sets share this machine. Run anything at `nice -n 10`, and keep to this one test and its module. The full lanes are run at integration.

## The bug

EXIT-PLAN, "X9 follow-ups (2026-10-03, from X9-3)", records it. The test's last part spawns a matrix child with no clock script (`OPENSIP_X9_CLOCK` unset), so the child's wall reading is the OS's. It then asserted:

    assert!(seconds > 1_700_000_000 && !(E..E + 3 * 3600).contains(&seconds));

`E = 1_790_985_600` is 2026-10-03 00:00:00 UTC. The scripted half of the test uses ordinals 0, 1 and 2, which cover `[E, E + 3·3600)`. So whenever the real clock reads 2026-10-03 00:00–03:00 UTC, the OS reading falls inside the excluded range and the test fails, even though the code is correct.

## What changed

The scripted half (ordinals 0 to 2, exact `OUTCOME clock=…` lines) is unchanged. The unscripted half now proves "the reading is the OS's" positively instead of by exclusion:

- The parent takes its own OS wall reading (`SystemTime::now()`, whole seconds) just before spawning the child and again just after it finishes.
- It asserts the child's reading lies in `before − 60 ..= after + 60`. The 60 s margin absorbs a small clock step between processes.
- The old `> 1_700_000_000` floor and the `E`-window exclusion are removed. The bracket implies both on any date when the clock is sane.

Law X9 r2 item 3 (`scripted_wall` in `crash_barrier.rs`) says a child with the script reads `E + 3600·k + n` in place of the OS's, and any other process reads the OS's. The test's intent for this half is that the unset script yields the OS's clock. The bracket checks that directly. It still fails if a scripted value leaks into an unscripted child, unless the real clock happens to be within 60 s of that scripted value. In that case the scripted and OS readings are indistinguishable by value, and no value-based assertion could separate them.

## Proof

There is no clock injection for the child's OS reading, and the system clock was not changed. Instead I moved the window onto today: the test's `E` was temporarily set to the start of the current UTC hour (`1791000000`, with the real clock at `1791003020`). That puts the real clock inside `[E, E + 3·3600)`, which is exactly the bad-window condition. Each edit below was temporary and reverted, and the subject file's pin was rechecked afterwards.

- **Old assertion, E in the window:** fails with `assertion failed: seconds > 1_700_000_000 && !(E..E + 3 * 3600).contains(&seconds)`. This reproduces the flake.
- **New assertion, E in the window:** passes.
- **New assertion, negative control:** the unscripted spawn was given `Some(ScriptedClock { epoch: E, ordinal: 0 })` with the original `E`. It fails with `1790985600 outside the OS readings 1791003028..=1791003028`, so a leaked script is still caught.

## Checks (narrow only)

All run with a private 0700 TMPDIR and `nice -n 10`:
- The test alone (`cargo test -p opensip-platform --features crash-matrix --lib -- crash_barrier::self_tests::a_scripted_clock_gives_each_ordinal_its_own_increasing_wall_seconds`): 1 passed.
- Its module (`crash_barrier::self_tests::`): 16 passed, 0 failed.
- `cargo clippy -p opensip-platform --features crash-matrix --all-targets -- -D warnings`: clean.
- `cargo fmt --all -- --check`: clean.

## Decide

- Does the bracket keep the test's intent (the unset script yields the OS's wall clock) and remove every date dependence?
- Is a 60 s margin reasonable, neither so tight that a clock step flakes nor so loose that it hides a leak?
- Is anything else wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256" (the sha256 of subject.diff: 31128abbbb408ad20fc9227eb06cc3d86c8aa20d05fb6c657a5b36aeaffa1dac). Write REVIEW.md and review.json. Do not commit.
