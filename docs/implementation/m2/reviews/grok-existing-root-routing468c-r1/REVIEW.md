# Review: existing-root routing 468c and inventory 76

Grok is the single reviewer. Claude Opus 5.5 leads. Review of the item 6 public mapping, the creator-to-gate route, and inventory v76, against law 468 r5 items 1, 3 and 6. No repository edits.

Product worktree `/Users/sb/code/opensip-ai/opensip-468c` at `d23100a59e8ff97a786ef7f84ebc241deef38095`. The nine product files match `hashes.txt`. `product.diff` is that diff (54045 bytes, sha256 `d89742f9f95dc196cfff5bbbd170510eea3fd0d16bdcb6851d7b4fad51607d3a`). The subject manifest matches `existing-root-routing-inventory-v76-subject.json` (2141 bytes, sha256 `8b0935868b55c2b23ace69174922d891fea0915211b7c7d3cdc281e5b0613cdc`).

## Verdict

**ACCEPT-UNIT.**

## Routing

`route` takes the attempt by value. The attempt is moved into a block that ends before `DurableWriteGate::begin`, and `admit` receives only `&InitialPlatform`. `Published`, `LostRace` and `NotPristine` all enter the gate. `AdmittedInstallation` holds how the invocation entered and the gate's installation. `Published` there is the values-only handoff. `produce_initial_core` and `produce_initial_platform` are re-exported from the trust module for that composition.

The refusal maps match each enum without a cross-variant wildcard. `Inventory`, `Release`, `Profile` and `Decision` ignore a private payload with `{ .. }` and still name that one variant. After a successful rename, a budget failure stays `BudgetExhausted` and every other inner refusal is `HostIo`, which is item 6's "any failure after the rename". `LostRace` is an `Outcome` before this match; the composition does not return it as `CreationRefusal::Rename`.

The host projection uses the 468a classes, exits, error codes, fault causes and details. `Incomplete` is `CONFIG.INVALID` / `CONFIG.CUSTODY_REFUSED` / `installation-incomplete`. `BudgetExhausted` is `SYSTEM.OUTCOME.ILLEGAL_STATE` / `host-invariant` / `WORK.BUDGET_EXHAUSTED`. `Busy` is `LEDGER.BUSY_TIMEOUT` / `ledger-busy` / `PROJECT.BUSY`. `HostIo` has no domain detail. The tests pin those sixteen shapes and the D9 pairs.

The routing tests use a scratch H. They admit `Published`, `NotPristine` and a real `LostRace`, send a foreign I to custody, a held fence to `Busy`, a tiny gate ledger to `BudgetExhausted` with the fence free, no premise to `ancestor-acl-omitted` with nothing created, and a scripted NotPerformed rename to `HostIo`. The live development build stops at `NoEmbeddedRelease` before an installation path. `~/Library/Application Support/OpenSIP` is absent.

## Judgment calls

1. `Invariant` is a faithful existing route. `HOST.INVARIANT_VIOLATED` is already a domain detail, and it pairs with operational-failed, exit 4, `SYSTEM.OUTCOME.ILLEGAL_STATE`, fault cause `host-invariant`. Latched, wrong attempt, a second allocation, `NotPristine` on the refusal path, a receipt that is not for its handle, `Manifest`, and `WorkReadFailure::InvalidLimit` are broken-caller states. Item 6 does not need another row.
2. `FenceBusy` on the creator's own new stage fence is foreign interference, so custody subject `stage-fence-busy` is right. `Busy` stays the installation fence held by another invocation.
3. `MissingAccount`, `RecordTooLarge`, `MalformedRecord` and `CredentialsChanged` are account admission. `Lookup(io)` is host I/O.
4. A malformed or unexpected process or boot response, a loader shape error, and a profile error are an unqualified platform. Native I/O on those observations is `HostIo`. `Unadmitted` still keeps the decision's own `NT-TCB-*` detail.
5. `TargetChanged` is the account target rebuilt from the actor, so `AccountRefused`. `StorageChanged` is 465 item 8, so `BackupChoiceRequired`.
6. `NotInitialized` is only `GateRefusal::Absent`: the walk did not find I. Creation's absent final name is `NotPristine` or the publish path, not this row.

## Inventory v76

v76 is v75 plus four sorted rows and nothing removed: 733 become 737. `installation_termination.rs` in security is `model`, the host file is `adapter`, `installation_routing.rs` is `composition`, and the tests are `test`. No inherited row changed. The eight projection rows are the same paths as v75, each parent selector matches, and the helper is byte-identical to v75. Its recorded run is 8 projection rows, PASS, and 43 corruptions refused.
