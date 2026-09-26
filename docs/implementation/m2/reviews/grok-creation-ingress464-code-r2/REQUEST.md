Grok re-review the 464 code, r2, after your r1 findings. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-creation-ingress464-code-r2. You own the serial native lane until your report is written. Host macOS 27.0. Rust is /opt/homebrew/Cellar/rust/1.95.0/bin. Use cargo --locked --offline. Do not read or print the private 413 UUID fixture.

Product HEAD aed5e08; the change is uncommitted (pins in hashes.txt). host lib.rs, request.rs and installation_observation.rs are the r1 bytes. Only initial_installation.rs changed.

## Changes

- RF-1: new `target_cost(actor)` (1 object, home bytes plus fixed-suffix bytes). `mint_intent` builds the target inside a charged `run` step. `disclosure_cost` is now 2 objects and `2 * target + 160` bytes: the notice (target plus at most 117 fixed bytes, within 160) and the receipt's copy of the target, with one write and one flush.
- RF-2: `CreationIntent::recheck_target` is removed. `InitialInstallationAttempt::recheck_intent_target(&intent, &actor)` rebuilds the target inside a charged `run` step. A lineage mismatch (intent or actor) or a target difference returns `TargetChanged` through `run`, which latches the attempt.
- Tests: the charged total now includes `target_cost`. The recheck charge is asserted. A foreign attempt's recheck refuses and latches it. The owning attempt latches when handed another attempt's actor. Consumption is tested on a fresh attempt.

## Lead's replay

initial_installation: 10/0. The security lib passed 445/0 three times in a row. One earlier run reported 444/1, and the failing test did not reproduce and could not be named. Please say if you see an intermittent failure. Host lib 76/0. Clippy `-D warnings` and fmt pass.

## Decide

Are RF-1 and RF-2 closed? Is any allocation still outside its reservation, and does every refusal latch? Anything new wrong? Replay at least the security and host libs (run security more than once), workspace clippy and fmt.

review.json must contain top-level "verdict" (ACCEPT-UNIT or REQUIRED-FINDINGS) and "requiredFindings". Write REVIEW.md and review.json. Do not commit.
