# GROK2 review: F7 r2

**Verdict: ACCEPT.**

Test-only change in `crates/platform/src/crash_barrier/self_tests.rs` on product main `8dcfe37` (X9-5 integrated). No inventory. The staged diff is 1685 bytes, sha256 `55842223d37f11fc0e5cd7b7104644e6f7807923837b00451150b7fbda82dec8`. The worktree matches the index. `~/Library/Application Support/OpenSIP` is absent. No repository edit or commit.

## What r2 changes

The scripted half is unchanged: ordinals 0, 1 and 2 still expect `E + 3600·k + n` with `E = 1_790_985_600`. The unscripted half still spawns `clock_child(None, 1)` and requires the child's whole seconds in `before − 60 ..= after + 60`.

r1 took `before` and `after` from `SystemTime::now()` inside this file. That token is forbidden by `crash_matrix_tests::barrier_sources_admit_no_sleep_polling_or_timed_wait`. r2 takes the same two readings from `/bin/date +%s`, once before the child and once after it, and parses the Unix seconds. The 60-second margin and the failure text are the same shape as r1.

## Intent

The unset script still has to yield the OS clock. The child gets that reading from `os::wall()` (`clock_gettime(CLOCK_REALTIME)` on this host) when `scripted_wall()` returns `None`. `/bin/date +%s` is the same Unix epoch, and the bracket requires the child's whole seconds to sit within a minute of those samples. A leaked script still fails unless the OS clock is already within 60 seconds of that scripted value, which is the same limit r1 accepted. On this host the clock was `1791009793`, about 24193 seconds after `E`, so an ordinal-0 leak would fall outside the bracket.

## Source pin

The pin scans `crash_macros.rs`, `crash_barrier.rs`, `crash_barrier/driver.rs`, and `crash_barrier/self_tests.rs`, skips comments, and forbids the timing tokens, including `SystemTime` and `Instant`. The only allowed `recv_timeout` is the driver's watchdog. The new lines contain none of those tokens. The two `date` calls are assertion samples around one child. They are not a sleep, a poll, or a timed wait. Waiting for `/bin/date` to print the time and exit is how the sample is taken.

The pin test passed. `crash_barrier::self_tests` passed, 16 tests, 0 failed. Both used `cargo test --locked --offline -p opensip-platform --features crash-matrix --lib` at `nice -n 10`, with a private target directory and a private 0700 temp directory. The lead's full lanes are not re-run here.

Required findings: none.
