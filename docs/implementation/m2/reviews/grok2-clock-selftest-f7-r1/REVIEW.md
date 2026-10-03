# GROK2 review — F7 clock self-test

Verdict: **ACCEPT**.

Subject: uncommitted diff of `/Users/sb/code/opensip-ai/opensip-f7`, detached at `eb0d50398035fe3532dadc332f88cf1d8bc4cb69`. `subject.diff` is 1459 bytes, sha256 `31128abbbb408ad20fc9227eb06cc3d86c8aa20d05fb6c657a5b36aeaffa1dac`. One file, `crates/platform/src/crash_barrier/self_tests.rs`, +14 −2. No product code changes and no inventory successor. `~/Library/Application Support/OpenSIP` stayed absent. No crash-matrix lane and no full workspace lane was run.

## The bracket

The scripted half is unchanged. Ordinals 0, 1 and 2 still expect `E + 3600·k + n` on the `OUTCOME clock=` line, with `E = 1_790_985_600`.

The unscripted half spawns with `clock: None`. `MatrixChild::spawn_watched` calls `env_clear()` and sets `OPENSIP_X9_CLOCK` only when a script is present, so the child does not inherit a script. Law X9 r2 item 3 (`scripted_wall`) then returns `None`, and `observe_clock` reads `CLOCK_REALTIME`. The parent takes `SystemTime::now()` in whole seconds just before `spawn` and just after `finish`, and requires the child's whole seconds to lie in `before − 60 ..= after + 60`.

That is the OS clock, checked directly. The assertion contains no calendar constant, so it does not fail when the real clock sits in `[E, E + 3·3600)`. On a sane clock the bracket is also above `1_700_000_000` and outside that script window. A leaked scripted value is still outside the bracket except when the OS clock is already within 60 seconds of that value. Those two readings are the same number, and no value comparison can tell them apart.

Sixty seconds is enough for a small step between the parent and the child, and far tighter than a scripted ordinal, which moves by 3600 seconds. One `observe_clock` cannot hide a wrong epoch inside that margin.

The failure text prints `{before}..={after}` without the margin. The predicate itself uses the margin. That does not change the check.

## Checks

Private 0700 `TMPDIR` under `DARWIN_USER_TEMP_DIR`, `CARGO_TARGET_DIR` under this review directory, `nice -n 10`, `--locked --offline`:

- The one test: 1 passed.
- `crash_barrier::self_tests::`: 16 passed, 0 failed.
- `cargo clippy -p opensip-platform --features crash-matrix --all-targets -- -D warnings`: clean.
- `cargo fmt --all -- --check`: clean.
