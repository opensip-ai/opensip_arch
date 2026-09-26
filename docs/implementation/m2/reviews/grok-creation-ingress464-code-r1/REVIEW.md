# Review: creation ingress 464 code r1

Grok is the single reviewer. Claude Opus 5.5 leads. Code review of the uncommitted 464 implementation. No repository edits.

Product HEAD `aed5e08d446aab64c03a6d375d48c7d8e2166887`. `git status` is the four pinned files, 664 insertions. Each matches `hashes.txt`. No file is added. Rustc `1.95.0` (`59807616e`) at `/opt/homebrew/Cellar/rust/1.95.0/bin`. `cargo --locked --offline`. The accepted law is 464 r2. The live `PROPOSAL.md` adds the acceptance stamp and is otherwise that text (6748 bytes, sha256 `61250cf61d81b17c7c831e5ad7c14def41005a0c3749540b1729b2cff8d4e3f8`).

## Verdict

**REQUIRED-FINDINGS.**

## Answers

The creator set, the disclosure text, the id draws, StepId 0, and the absence bit match 464 r2. Nothing in the diff is called from the CLI. `mint_intent` writes and flushes the notice and does not create a directory. Its order is actor ownership, `classify_backup` (constant `Unknown`), `storage_choice`, then the charged id draws, then the charged disclosure. A `BackedUp` refusal returns before either `run`. Exercising that refusal through `storage_choice` and `latch_on`, rather than `mint_intent`, is the right test while the classifier cannot return `BackedUp`: the test checks the same decision and the same latch, and `used()` stays unchanged.

`installation_entry` is an exhaustive match over all 45 `Inventory3CommandName` values. Creators are `default`, `analyze`, `fit`, and `audit`. `analyze` and `fit` with `--ephemeral` are `Outside`. `--ephemeral` on any other command is `EphemeralNotAccepted`, including `default` and `audit`. `NotInitializedWhenAbsent` is `import`, `baseline-upgrade`, `repair-apply`, `repair-verify`, `test-run`, and `native-prepare`. `installation_precondition` returns `INSTALLATION.NOT_INITIALIZED` only for that class when absence is true.

`Error::installation_absent` is true only for `Reason::Fence(RootAbsent)` on macOS, and false otherwise. `RootAbsent` is the fence result of `RootObservation::Missing`: a no-follow open returned `NotFound` under an inspected retained prefix, and the recheck saw `NotFound` again. A bare `NotFound`, a changed name, and an unreadable parent do not count.

`CreationIntent` is private, has no `Clone` derive, and is not deserializable. `consume` returns `req1_` and `exec1_` plus 32 lowercase hex and StepId 0, or `None` after latching a foreign attempt. Actor, storage, entropy, and disclosure failures latch through `owns`, `latch_on`, and `run`. The id reserve is honest: two `request_entropy` calls, `IDS_COST` of 0 objects, 2 edges, and 32 bytes, returned as stack arrays.

The notice is `retention DEFAULTED durable-unbounded`, the account-derived root, and `backup status unknown` for the constant classifier. `write_all` then `flush`; either error refuses and latches. That is the before-effect delivery. The path reserve and `recheck_target` are the findings below.

Read commands that require I (`query`, `recommend`, `baseline-show`, `policy-show`, `policy-test`, `candidates`, `inspect`, `review-brief`, `repair-preview`) are `CommandOwnerDecides`. `installation_precondition` emits `INSTALLATION.NOT_INITIALIZED` for the six named commands only. Owner §6 also names a read request that requires the installation. Those commands are not implemented in this unit, and whether a given request requires I is that command's admission. Positive absence is exposed for that owner. Doctor stays `Outside`, the report-channel case.

## Required findings

**RF-1.** The path buffers are under-reserved. `mint_intent` builds `installation_target` by cloning the home and appending the suffix before any charge for that buffer. `deliver_disclosure` then allocates the notice (`target` bytes plus 111 bytes for `unknown`, 113 for `backed-up`, 117 for `not-backed-up`) and a second `PathBuf` of the target. `disclosure_cost` reserves 1 object, 2 edges, and `target.len() + 160`. The notice and the two write calls fit. The two path buffers do not. `retained_record` says a temporary copy is a separate charge. `used()` reports the short reserve, so a later charge can pass a cap the allocations have already passed. `recheck_target` calls `installation_target` again with no charge.

**RF-2.** `recheck_target` does not latch the attempt. A lineage or target mismatch returns `IntentRefusal::TargetChanged` and leaves the owning attempt unlatched. `run` still accepts later work on that attempt, so the refusal does not stop the act. `recheck_actor`, `owns`, and `require_lineage` latch; this check does not.

## Replay

- `cargo test --locked --offline -p opensip-security --lib`: exit 0. 445 passed, 0 failed, 2 ignored. `initial_installation` 10 passed. `installation_observation` 13 passed, including `only_a_positively_absent_root_reads_as_installation_absent`.
- `cargo test --locked --offline -p opensip-host --lib`: exit 0. 76 passed, 0 failed. The three new `request` tests passed.
- `cargo clippy --locked --offline --workspace --all-targets -- -D warnings`: exit 0. Fingerprints for both crates are newer than the pinned sources.
- `cargo fmt --all -- --check`: exit 0.

Do not commit.
