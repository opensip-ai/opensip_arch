Grok review: 468c, the item 6 public mapping, creator-to-gate routing, and inventory v76. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-existing-root-routing468c-r1.

Law: `docs/implementation/m2/existing-root-admission-468/PROPOSAL.md` r5 (accepted), items 1, 3 and 6. The 468a routes are in `existing-root-diagnostics-468a/diagnostic-routes.json` and its registry.

## Subject

Pins are in hashes.txt.
- **Product:** the worktree `/Users/sb/code/opensip-ai/opensip-468c`, based on d23100a. Its diff, including new files, is product.diff in your output directory.
- **Arch:** `repository-file-inventory.v76.json`, `existing-root-routing-inventory-v76-subject.json`, and `existing-root-routing-inventory-v76/`, including `evidence/build_v76.py` and `evidence/verify_scratch.py`.

## What it does

- **Termination vocabulary.** `security::installation_termination`: `InstallationTermination` is a closed set with one variant per item 6 row, plus `Invariant`.
- **Per-family maps.** `custody/installation_routing.rs` maps every refusal family of 459–468 to it with exhaustive matches and no wildcards: attempt, actor, intent, core, platform, chain, preparation, creation, gate and work. Four private-payload variants are matched as `{ .. }`.
- **Routing.** `run_initial_creator` and `route`:
  - The attempt is taken by value and ends in a block before `DurableWriteGate::begin`.
  - `admit` gets only `&InitialPlatform`.
  - `Published`, `LostRace` and `NotPristine` all enter the gate.
  - The result is `AdmittedInstallation { entered, installation }`.
- **Host projection.** `host::installation_termination` projects a row onto the generated Common4 types: class, exit, error code, fault cause, detail and subject.
- **Re-exports.** `produce_initial_core` and `produce_initial_platform` are re-exported at crate level.
- **Inventory v76.** Four new rows. The 8 inheritance rows are re-projected with parent v75.

## Judgment calls: please rule on each

1. **`Invariant` row.** Refusals only a broken caller can reach have no item 6 row: Latched, WrongAttempt, a second attempt, NotPristine on the refusal path, WriteReceipt, Manifest, and `WorkReadFailure::InvalidLimit`. They go to operational-failed, 4, `SYSTEM.OUTCOME.ILLEGAL_STATE`, host-invariant, with the existing detail `HOST.INVARIANT_VIOLATED`. Is that a faithful existing route? Or does law 468 need an r6 row?
2. **Stage `FenceBusy`.** Another holder of the creator's own new stage fence goes to Custody, subject `stage-fence-busy`, not Busy, because it is foreign interference.
3. **Account lookup failures.** MissingAccount, RecordTooLarge, MalformedRecord and CredentialsChanged go to AccountRefused. `Lookup(io)` goes to HostIo.
4. **Platform observation failures.** Malformed or unexpected process and boot responses, loader shape and profile errors go to PlatformUnqualified. Native I/O goes to HostIo.
5. **Intent refusals.** `IntentRefusal::TargetChanged` goes to AccountRefused, and `StorageChanged` goes to BackupChoiceRequired (465 item 8).
6. **`NotInitialized`.** Only `GateRefusal::Absent` produces it.

## Tests and checks

The routing tests use scratch homes and 462 signed test trees:
- `Published`, `NotPristine` and a real `LostRace` are each admitted.
- A foreign I at rename ends in Custody.
- A held admission makes a second invocation Busy.
- A tiny gate ledger ends in BudgetExhausted, with the fence free.
- No premise ends in Custody `ancestor-acl-omitted`, and nothing is created.
- A scripted NotPerformed rename ends in HostIo.
- A live dev build ends in NoEmbeddedRelease, and the real OpenSIP stays absent.
- The host tests pin all 16 row shapes against the 468a routes and the D9 pairing.

Results:
- Workspace: 1099/0, on two runs. Clippy and fmt are clean.
- `check_package_edges --lane host` passes.
- `verify_scratch` passes with v76.

## Decide

- Is the mapping total, and exactly law 468 r5 item 6?
- Does routing reuse nothing from the creator?
- Rule on judgment calls 1 to 6.
- Are v76 and the inheritance right?
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": a single string, the sha256 of existing-root-routing-inventory-v76-subject.json;
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes and sha256 of v76, parent (the v75 pin), successorRecord (the pin of existing-root-routing-inventory-v76/successor.json)}.

Write REVIEW.md and review.json. Do not commit.
