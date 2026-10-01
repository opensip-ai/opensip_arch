Grok review: X3c-2, evidence object publication and the prepared ledger commit (law X3c r7 items 4 to 7 and 9 to 11, with item 12a's X3c-2 cases), with inventory v100. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-ledger-blob-x3c2-r1. If you build or test, use a CARGO_TARGET_DIR under that directory. Run git only read-only, and only against the worktree below.

Law: `docs/implementation/m2/ledger-blob-x3c/PROPOSAL.md` r7 (accepted). X3c-1 (items 1 to 3) is integrated at product 859089a. X3d r3 (accepted) is the composition this unit serves; its item 4 fixes the call order around these types.

## Subject

Pins are in hashes.txt.
- **Product:** the worktree `/Users/sb/code/opensip-ai/opensip-x3c2`, based on 46b1d60 (X3b-1b integrated, inventory v97 selected). Save `git -C <worktree> diff` (the new files are intent-to-add) as product.diff and report its sha256. Lead's value: d8d9dada327f4e4c27e94b37b6568ab12e4492d42b7ce30fbeedaa04468193ac, 70208 bytes.
- **Arch:** v100 (parent v97), `ledger-blob-x3c2-inventory-v100-subject.json` and `ledger-blob-x3c2-inventory-v100/`.

## What it does

The new code is `crates/storage/src/ledger_store/project_commit.rs`, project_ledger.rs's child module `commit`. Everything is crate-private, runs under the namespace writer lease the caller holds, and is charged to the operation's ledger.

- **Objects (item 4, step 3).** `publish_objects(&AdmittedAttempt, &ObjectDirectory, Vec<DeclaredObject>, work) -> PublishedObjects`.
  - It first reserves the whole commit in one charge: per object, a fixed cost plus its byte length. A commit that does not fit refuses on the budget row before any write.
  - It then checks every object (length and SHA-256 via `VerifiedBlob`, no repeated digest) before the first write. A failed check is `ObjectDeclaration`, on the invariant row.
  - Each object goes through `blob_store`'s `publish`: `publish_new_regular` (temporary file, `F_FULLFSYNC`, exclusive link, directory barrier). Only an exclusive-link `EEXIST` with unchanged visibility falls through to `confirm_existing_regular`, which does a full byte comparison and its own barriers.
  - **Classification.** These are `LEDGER.CORRUPT` (`Corrupt`), and the entry is never overwritten:
    - Prepare's refusal of a non-regular entry at the name;
    - a confirmation `InvalidData` (unequal bytes, a length mismatch, a second link, or group or other write);
    - a confirmation `InvalidInput`, or `ELOOP`.

    An unreachable objects directory during confirmation is the custody row (name-changed). Anything else, including an indeterminate link or barrier, is host I/O.
  - A failure stops publication. Earlier objects stay, and nothing is deleted, renamed or reused.
- **`PreparedLedger` (item 5, step 4).** `begin_prepared_ledger(&AdmittedLedger, &AdmittedAttempt, PublishedObjects, work)`:
  - It checks the ledger's file identity, then `open_verified` (`open_existing` with `busy_timeout = 0`, plus the whole-schema equality), then `BEGIN IMMEDIATE`.
  - Busy is the busy row, and the refusal holds no transaction.
  - It consumes the published set, so level 3 is taken only after every object's barriers. Objects from another attempt refuse.
  - The type is owned, single use and not Clone, with no SQL surface. Its Drop is `WriteTransaction`'s local rollback.
- **Staging (item 6, step 6).** `PreparedLedger::stage(self, schemas, CommitRows, StagingLimits, work) -> PreparedLedgerCommit`. It charges the fixed staging and `COMMIT` costs plus the staged body bytes, then, in the open transaction:
  1. checks that the association's operationRef is the attempt's;
  2. runs `stage_recovery_pair`, which handles the join, the savepoint and poisoning;
  3. runs the new `stage_run_material`, whose returned blob digests must equal the published set exactly;
  4. runs `stage_availability` with no expected generation, so the record is the initial one;
  5. runs `stage_pin_change` as a first publication from an empty set under the attempt's operationRef.

  `stage` consumes `self`, so any failure drops the transaction and nothing is committed (F11). Classification: a stored schema that isn't the selected DDL is `Corrupt`; SQLite and I/O failures are host I/O; non-joining values, a retained-key collision, and availability, pin or material refusals are `StagingMismatch` (the invariant row).
- **The adapter and durability (item 7).** `PreparedLedgerCommit` is owned and not Clone. Its one consuming method, `commit(self) -> LedgerCommitOutcome`, performs only `COMMIT`:
  - success is `Committed { execution }`;
  - any error is `Undetermined { execution }`, which `refusal()` maps to `CommitUndetermined` on the `DURABILITY.COMMIT_FAILED` row.

  Nothing is retried, read back or settled. Dropping the adapter rolls back.
- **Supporting edits.**
  - `project_ledger.rs`: `admit_attempt` now returns `AdmittedAttempt`; three refusal variants and their rows; the `commit` module declaration.
  - `recovery_material.rs`: `WriteTransaction::stage_run_material` (the schema check, `paired_run`, `parse_material`, then the insert).
  - `blob_store.rs`: crate visibility, plus a `cfg(test)` byte accessor.
  - `lib.rs`: a `cfg(test)` `test_scratch` (F3's per-process scratch parent).
  - `project_ledger_tests.rs`: the fixture is `pub(super)` and lives under that parent.
- **Test-only hooks (item 11).**
  - `publish_objects_crashing` and `ObjectStep`, which exist only under `cfg(test)` and are reached through a `#[cfg(test)]` parameter of the private inner function;
  - `PreparedLedgerCommit::with_commit_hook`.

## Judgment calls: please rule on each

1. **The security types are not named here.** X3b's `JournalSealBinding`, X3d-1's `JournalWriteTxn` and X4's `AdmissionPermit` are either not built or `pub(super)` inside security. So staging takes the joined values (exact receipt and association candidates and the carrier digest), and the adapter's `commit` is a plain consuming method. X3d calls it only as `permit.consume(|adapter| adapter.commit())`: `AdmissionPermit<T>` owns its prepared value, so X3d makes the adapter that `T`. Journal before ledger, and never under level 4, is X3d's order to enforce. The storage half is enforced by types: no object without `AdmittedAttempt`, no level 3 without `PublishedObjects`, no adapter without staging, and no second commit.
2. **A new run-material mechanism.** Item 6 says "through their existing private mechanisms", but `commit_run_material` had only a reader. `stage_run_material` sits beside its DDL and reuses recovery's schema check and `parse_material`, so it admits exactly what recovery would read back. It does not change the law; it is the narrowest addition.
3. **"Object references" are the inventory's `blobDigests`.** The schema describes each `blobDigests` entry as "a retained blob published by this commit; the CAS key is the digest itself". Staging requires that set to equal the published set exactly. The typed `objects` identities stay inside the inventory body; X3c-2 publishes no typed object.
4. **Pins.** They are staged as a first publication from an empty expected set, under the attempt's operationRef. An empty pin set is a no-op.
5. **Availability.** It must be the initial generation (expected none). No state rule is added: the law names none.
6. **Wider corrupt set.** Blob confirmation also refuses a second hard link or a group- or other-writable mode. I map those to `LEDGER.CORRUPT` along with item 4's three cases, since none can be confirmed or overwritten. An objects directory that becomes unreachable during confirmation is custody (name-changed), not corrupt.
7. **Invariant row for caller errors.** Item 10 has no row for a bad declaration or for staged values that don't join. Both are a broken composition, never a retry, so they get the invariant row as a reused ExecutionId does. That covers `ObjectDeclaration` (length, digest, repeated digest) and `StagingMismatch` (operation, blob set, pair join or collision, availability, pins, and objects from another attempt).
8. **Costs.**
   - Per object: 1 object, 12 edges and 512 bytes, plus its length, all reserved in one charge before the first write. So 256 MiB also bounds one commit's object bytes, as item 9 says.
   - `BEGIN`, and staging plus `COMMIT`, have fixed costs, plus the staged body bytes.
   - The `COMMIT` is reserved at staging, so `commit()` needs no ledger inside the permit closure.
9. **Crash points.** Storage cannot inject faults into the platform's publication primitive. So each `cfg(test)` crash point writes the on-disk state that step leaves, through the retained directory's exclusive create, and stops the attempt with no cleanup:
   - temporary write: a partial staging file;
   - before the file barrier: a full staging file;
   - after the link: the digest name holds the bytes;
   - before the directory barrier: the link was lost on power loss, leaving a full staging file.

   The `COMMIT` fault is a real failing `COMMIT`, caused by a deferred foreign-key violation in the connection's temp schema.
10. **The directory barrier against the handle.** Item 4 says the receipt's directory barrier is checked against the handle. The platform receipts from `publish_new_regular` and `confirm_existing_regular` expose only the barrier kind. Both run on the retained `objects/sha256` handle itself (`ObjectDirectory`), so the binding holds by construction. Each `PublishedObject` records its barrier kind.
11. **`AdmittedAttempt`.** X3c-1's `admit_attempt` now returns a token (not Clone), which publication requires. That enforces item 3's "before the first object" by type.
12. **Storage scratch.** security's `test_scratch` is private to its crate, so storage gets its own F3 per-process parent, and X3c-1's fixture moves under it. Storage fixtures walk no ancestors, so no lock or settled retry is needed.
13. **A poisoned adapter.** Staging returns the adapter only when it is unpoisoned, and the adapter has no other method. `WriteTransaction::commit`'s poisoned refusal is therefore unreachable. If it were reached, it would be classified as `Undetermined`, which is conservative: it never claims a commit.
14. **Stale descriptions.** project_ledger.rs's "No object publication, staging, commit, …" and recovery_material.rs's read-only description now understate their files. They go to the same description-only successor as carrier_floor.rs (see the v100 README).

## Tests

`ledger_store/project_commit_tests.rs`, 15 tests, on X3c-1's scratch location with a held test writer lease. No real home is touched; fixtures are under `<temp>/opensip-test/<pid>-<nanos>`.
- **Publication.**
  - New objects are 0600 with one link, both barriers and no residue. A second attempt confirms them byte for byte without rewriting (same inode).
  - A wrong length, a wrong digest or a repeated digest refuses as invariant before any write.
  - At an object name, all of these refuse as `LEDGER.CORRUPT`, with the entry unchanged and earlier objects kept: unequal, short and long bytes, a directory, a symlink, a 0666 file, and a second hard link.
  - A commit short of budget refuses before the first object.
- **Crashes.** At each of the four steps: earlier objects and the residue stay, the attempt row stays `admitted`, nothing is staged, and a fresh attempt completes. It confirms the earlier objects, and confirms the crashed object after `AfterLink` (otherwise it publishes it new).
- **Level 3.**
  - A busy ledger refuses in under 1 s and holds nothing.
  - A held `PreparedLedger` is busy to other writers and is released on drop.
  - Another attempt's objects refuse.
- **Staging and commit.**
  - A staged commit is invisible to a reader until `COMMIT`. After it, every one of the six tables holds its row, the pair joins as recovery reads it (`ContinueCarrier`, pending settlement), and the attempt stays `admitted`.
  - A failure at each stager commits nothing. A trace confirmed each case fails at its intended stager: the pair-sequence collision, the blob set, the availability Run, the availability generation, the pin Run, and a reused pin operation. An operation mismatch fails before any insert.
  - A dropped ledger or adapter commits nothing.
  - An injected `COMMIT` error is `Undetermined` with the ExecutionId on the durability row; nothing is committed, and the attempt and objects stay.
  - Staging short of budget refuses.
- **Rows and source pin.** The item 10 rows. A source pin checks that project_commit.rs contains no delete, unlink, rename, `OR REPLACE`, attempt update, `ReadSnapshot`, `Duration` or `busy_timeout(`, and exactly one `.commit()`.

## Checks

- X3c-2 tests 15/15; X3c-1's 18/18 still pass.
- Full workspace, two runs: 1318 passed, 0 failed, 3 ignored each time.
- Clippy `--workspace --all-targets -D warnings` and fmt are clean.
- `~/Library/Application Support/OpenSIP` is absent.
- `check_package_edges --lane host` against v100 passes.
- verify_scratch (v100 appended over the real lock at 46b1d60) passes: 66 inventory successors, 71 contract successors, 16 inheritance rows, v100 selected.
- verify_projection against the real lock: 16 rows, 83 corruptions refused.
- `build_v100.py` reruns produce the same bytes.

## Decide

- Does X3c-2 implement X3c r7 items 4 to 7 and 9 to 11 exactly? In particular:
  - no object before the attempt row, and no level 3 before every barrier;
  - a non-waiting acquisition that holds nothing on failure;
  - all rows or none;
  - only `COMMIT` in the adapter;
  - `Undetermined` never inferred as commit or absence.
- Rule on the judgment calls, in particular 1, 2, 3, 7 and 9.
- Is v100 right on v97?
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": the sha256 of `ledger-blob-x3c2-inventory-v100-subject.json`;
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes, sha256 of v100, parent (the v97 pin), successorRecord}.

Write REVIEW.md and review.json. Do not commit.

**Lead note on ordering.** X2b-2's inventory99 is built on the same parent, v97. If X2b-2 integrates first, `build_v100.py` rebuilds v100 on v99 (it follows the lock's selected inventory), and the rebuilt v100 gets a quick rebase-only recheck. This review judges v100 on v97 as submitted.
