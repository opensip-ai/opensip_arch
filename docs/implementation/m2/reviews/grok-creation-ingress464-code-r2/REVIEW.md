# Review: creation ingress 464 code r2

Grok is the single reviewer. Claude Opus 5.5 leads. Re-review of the uncommitted 464 implementation after code r1. No repository edits.

Product HEAD `aed5e08d446aab64c03a6d375d48c7d8e2166887`. The four files match `hashes.txt`. `lib.rs`, `request.rs`, and `installation_observation.rs` are the r1 bytes. Only `initial_installation.rs` changed (30867 bytes, sha256 `2561820ed28ef2528a1ab62d25fd1178812f505b7c0c2e7213c8bae50af918d3`). Rustc `1.95.0` (`59807616e`). `cargo --locked --offline`.

## Verdict

**REQUIRED-FINDINGS.**

## Answers

RF-1 is closed. `target_cost` reserves 1 object and the home length plus the fixed suffix (`Library`, `Application Support`, `OpenSIP`, `preview-v1`, each with its slash). `mint_intent` builds that path inside `run` before classify and `storage_choice`. `disclosure_cost` reserves 2 objects, 2 edges, and `2 * target + 160` bytes: the notice (target plus 111, 113, or 117 fixed bytes) and the receipt's `PathBuf`, then one `write_all` and one `flush`. Both copies fit. `recheck_intent_target` rebuilds the path inside the same `target_cost` reserve.

RF-2 is closed for the recheck itself. `CreationIntent::recheck_target` is gone. `InitialInstallationAttempt::recheck_intent_target` returns `TargetChanged` through `run`, and `run` latches the attempt. A foreign attempt's recheck latches that attempt. The owning attempt latches when handed another attempt's actor. Storage, entropy, and disclosure refusals still latch. The id draws remain two stack arrays, 0 objects, 2 edges, 32 bytes.

`consume` is the remaining hole. `require_lineage` returns true whenever the lineage matches, including when the attempt is already latched, and the `then` closure still builds the invocation. After `TargetChanged`, `run` will refuse a later `mint_intent`, and `consume` will still return the `req1_` / `exec1_` binding. Those two `String`s are also uncharged: `req1_` plus 32 hex is 37 bytes, `exec1_` plus 32 hex is 38 bytes, two objects. `IDS_COST` reserved the 32 raw bytes on the stack at draw time.

The three security-lib runs were each 445 passed, 0 failed, 2 ignored. The unnamed 444/1 failure did not appear.

## Required findings

**RF-1.** `consume` does not observe the latch. `recheck_intent_target` latches the attempt and returns `TargetChanged`. `consume` on that same attempt sees a matching lineage and returns `IntentInvocation`. The refusal stops `run` and does not stop the handoff of the creation ids.

**RF-2.** The rendered ids are allocated outside a reservation. On a matching lineage, `consume` builds two `String`s with `hex_id` and no `run` charge. The attempt's `used()` omits those 2 objects and 75 bytes, so a later charge can pass a budget those strings have already taken.

## Replay

- `cargo test --locked --offline -p opensip-security --lib`, three times: exit 0, 445 passed, 0 failed, 2 ignored. `initial_installation` 10 passed on each run.
- `cargo test --locked --offline -p opensip-host --lib`: exit 0. 76 passed, 0 failed.
- `cargo clippy --locked --offline --workspace --all-targets -- -D warnings`: exit 0.
- `cargo fmt --all -- --check`: exit 0.

Do not commit.
