# Law X5 r1 — replay-to-commit join

Law review only. No product cargo. The OpenSIP support directory is absent. `PROPOSAL.md` is 8969 bytes, sha256 `140c6338b1809ac83db8ca45997fc4842eacf21808532a8f10df48087d574428`, matching `hashes.txt`. Live product HEAD is `8452ab962ad42a5a17e4b4755188943874725423`. The proposal names `7e676a9`. `replay.rs`, `closure.rs`, `recovery.rs` and `ledger_store.rs` are unchanged between those commits, and `crates/host/src/fact_admission.rs` is still absent. There is no `crates/lifecycle/src/replay.rs`.

## What holds

The join is the M2 slice of `fact_admission.rs`: `replay_candidate` builds `RetainedInputs` and calls `replay_run` once, returning that `ReplayedRun`. `RunCandidateInputs` is the build plan's inert candidate. `REPLAY_LIMITS` is fixed at the commit boundary. The function is `pub(crate)`, and only X7 calls it. Replay stays off the attempt ledger. A `ReplayedRun` is consumed by one `prepare_commit`. The binding comparison stays X3d item 3 step 1. F01's substituted target or inventory is that check. No new public code.

DR-G24 is the policy-pack gate. The register defines it as refusing a non-bundled or non-declarative pack, and the build plan routes it to `evaluator/policy.rs` and `host/configuration.rs`. Fact admission's other gates are DR-G23 and DR-G25, both M3. X5 prepares F01 only. EXIT-PLAN already records that split as X12.

Item 3's order is a sound lead decision for F01. Replay is pure. A refusal ends before a fence, lease, attempt row, object or journal effect, so nothing authoritative is published and nothing has to be cleaned up. `prepare_commit` still runs under the writer lease, which is X3d's rule. The build plan's "guard owned through evaluation" is the rejected alternative, and rejecting it does not let a boolean, a RunId or a structural-only check reach the facade.

`ReplayError::Mismatch` matches the retained-regeneration route: operational-failed, `HOST.IO_FAILURE`, `host-io`, `evidence.regeneration-mismatch`, with the affected Run reference. That is the fault-contract route `complete-replay-mismatch:retained-regeneration` and identity's `RegenerationMismatch` carrier.

## RF-1

Item 5 maps all of `ReplayError::Input` to `EVALUATION.INPUT_REFUSED`. `Input` is `RetainedInputError`, and `MissingObject` / `MissingBlob` are how `replay_run` reports an absent retained object or blob. The host replay corpus treats that case as unavailable evidence. The evaluator-fault contract routes `promised-bytes-lost:evidence-store` to operational-failed, exit 4, `HOST.IO_FAILURE`, `host-io`, detail `evidence.missing`, with the missing reference. Identity's EvidenceUnavailable carrier and the composition contract keep an absent retained pointer on that route, separate from a schema or identity failure. Item 8 then requires the missing-object test to expect `EVALUATION.INPUT_REFUSED`. The prevail sentence does not repair the row: the table has already chosen the structural-input detail, and S12's I/O row is `HOST.IO_FAILURE`.

## Verdict

REQUIRED-FINDINGS. RF-1.
