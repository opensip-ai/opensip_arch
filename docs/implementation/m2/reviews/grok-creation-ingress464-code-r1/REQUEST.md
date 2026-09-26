Grok review the 464 code, r1. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-creation-ingress464-code-r1. You own the serial native lane until your report is written. Host macOS 27.0 (26A428). Rust is /opt/homebrew/Cellar/rust/1.95.0/bin. Use cargo --locked --offline in /Users/sb/code/opensip-ai/opensip. Do not read or print the private 413 UUID fixture.

Law: docs/implementation/m2/creation-ingress-464/PROPOSAL.md r2, which you accepted. Product HEAD aed5e08. The change is uncommitted (`git diff`) in 4 files; pins are in hashes.txt. No file is added, so there is no inventory successor. Code goes into the existing rows for host request.rs ("typed request admission before effects"), security initial_installation.rs, and installation_observation.rs.

## Changes

- host request.rs: `installation_entry(Inventory3CommandName, ephemeral)`, an exhaustive match over all 45 generated command names with no wildcard. Creator = default, analyze, fit, audit. NotInitializedWhenAbsent = import, baseline-upgrade, repair-apply, repair-verify, test-run, native-prepare. Outside = help, version, completion, doctor, install, update, and analyze/fit with `--ephemeral`. Everything else is CommandOwnerDecides. `--ephemeral` elsewhere is `EphemeralNotAccepted`. `installation_precondition(entry, absent)` returns `INSTALLATION.NOT_INITIALIZED` only for NotInitializedWhenAbsent with positive absence. lib.rs re-exports them.
- security installation_observation.rs: `Error::installation_absent()` is true only for `Reason::Fence(installation_fence::Error::RootAbsent)`, the rechecked NotFound beneath an inspected retained prefix. It is false for everything else, and on non-macOS.
- security initial_installation.rs:
  - `CreatorCommand`, `BackupClassification` and constant-UNKNOWN `classify_backup`.
  - `storage_choice`: BACKED_UP without the flag gives `BackupChoiceRequired`.
  - `deliver_disclosure`: the stderr notice with the root, "retention DEFAULTED durable-unbounded" and the backup status. It writes and flushes, and any error refuses.
  - `CreationIntent`: private, non-Clone, lineage-bound. It carries the command, two 16-byte CSPRNG ids, the storage admission and the disclosure receipt. It has `recheck_target(actor)`, and `consume(self, attempt)` yields req1_/exec1_ hex and StepId 0, or None and a latch on the wrong attempt.
  - `InitialInstallationAttempt::mint_intent` runs owns(actor), classify, storage decision, the charged id draws (2 edges, 32 bytes), then the charged disclosure. Any refusal latches the attempt.
  - Nothing is wired to the CLI; the creator stays disabled.

## Lead's replay on this host

initial_installation: 10/0. Host request tests: 5/0. installation_observation: 13/0. Workspace: 944 passed, 0 failed, 2 ignored. Clippy `-D warnings` and fmt pass.

## Decide

Does the code implement 464 r2 exactly, with nothing wired to an effect? Is the disclosure written and flushed before anything that could count as a creation effect, and does every failure latch? Is the ordering right: storage refusal before id draws and disclosure; disclosure before any later owner step? Is `installation_absent` only positive absence? Are the costs honest: the ids draw two entropy calls, and the disclosure charges one allocation and its bytes? Note that the test for positive backup without the flag exercises `storage_choice` with the latch, not `mint_intent`, because the classifier is constant. Is that acceptable? Anything else wrong? Replay the security and host libs, workspace clippy and fmt.

review.json must contain top-level "verdict" (ACCEPT-UNIT or REQUIRED-FINDINGS) and "requiredFindings". Write REVIEW.md and review.json. Do not commit.
