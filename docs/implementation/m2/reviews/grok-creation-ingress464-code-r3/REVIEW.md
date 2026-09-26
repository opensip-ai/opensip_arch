# Review: creation ingress 464 code r3

Grok is the single reviewer. Claude Opus 5.5 leads. Re-review of the uncommitted 464 implementation after code r2. No repository edits.

Product HEAD `aed5e08d446aab64c03a6d375d48c7d8e2166887`. The four files match `hashes.txt`. `lib.rs`, `request.rs`, and `installation_observation.rs` are the r2 bytes. Only `initial_installation.rs` changed (31990 bytes, sha256 `93ce214afd1537b42ab33488cc5544a8d1440e17afee61b053738eed2d229f68`). Rustc `1.95.0` (`59807616e`). `cargo --locked --offline`.

## Verdict

**ACCEPT-UNIT.**

## Answers

r2 RF-1 is closed. `consume` returns `Result` and goes through `attempt.run`. `run` checks the latch before the closure and returns `Budget(Closed)`. The test latches the owning attempt with `TargetChanged`, then `spare.consume` matches `Budget(Closed)`. No `IntentInvocation` comes back, so the creation ids are not handed off.

r2 RF-2 is closed. `RENDERED_IDS_COST` is 2 objects, 0 edges, and 37 + 38 bytes. `work.run` reserves that cost before `hex_id`. The success path renders `req1_` plus 32 hex and `exec1_` plus 32 hex, and the test asserts those lengths and that `used()` grew by exactly `RENDERED_IDS_COST`.

A foreign attempt returns `IntentRefusal::WrongAttempt` from inside `run`, which latches that attempt and does not build the invocation. The test's foreign `consume` runs after that attempt is already latched, so it takes the `Budget(Closed)` path. The unlatched foreign path reserves the id cost and then returns `WrongAttempt` before `hex_id`. Both paths stop the handoff.

The other refusal paths still latch and still stop later work: storage, entropy, disclosure, and `recheck_intent_target`. The path and disclosure reserves from r2 are unchanged. `consume` is the only new allocation, and it sits inside its reserve. No directory is created, and the CLI still does not call this unit.

## Replay

- `cargo test --locked --offline -p opensip-security --lib`, three times: exit 0, 445 passed, 0 failed, 2 ignored. `initial_installation` 10 passed on each run. No intermittent failure.
- `cargo test --locked --offline -p opensip-host --lib`: exit 0. 76 passed, 0 failed.
- `cargo clippy --locked --offline --workspace --all-targets -- -D warnings`: exit 0.
- `cargo fmt --all -- --check`: exit 0.

Do not commit.
