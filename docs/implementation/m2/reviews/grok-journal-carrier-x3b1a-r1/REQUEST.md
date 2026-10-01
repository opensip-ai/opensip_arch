Grok review: X3b-1a, the journal floor step, the file protocol, carrier classification and creation, with inventory v85. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-journal-carrier-x3b1a-r1. If you build, use a CARGO_TARGET_DIR under that directory.

Law: `docs/implementation/m2/journal-x3b/PROPOSAL.md`. r6 is accepted; its changes since r4 are only to item 5 step 7, the SEAL-path lock hold, which is outside this unit. This is the first half of X3b-1. X3b-1b (the carrier start's witness writes under the lease, and the end step) follows.

## Subject

Pins are in hashes.txt.
- **Product:** the worktree `/Users/sb/code/opensip-ai/opensip-x3b1`, based on 99f1c35. Save `git -C <worktree> diff` (new files are intent-to-add) as product.diff and report its sha256.
- **Arch:** v85 (parent v84, which is under review with X2a), `journal-carrier-inventory-v85-subject.json` and `journal-carrier-inventory-v85/`.

## What it does

- **`locations.rs`.** Now follows the law: the witness is `grant-journal.witness.json` and the floor is `trust/carrier-floors/N.v1`. The previous spellings came from reference checkpoint 201, which was reviewed but never selected. The selected `host-foundation-completion.v2` spells the witness `.json`, and no selected source spells a floor path. A per-generation floor would break the law's floor table.
- **`carrier_floor.rs`:**
  - `CarrierLocation`, with a test-only constructor; X3b-3 adds the production one.
  - `publish_private_file`, the item 5 file protocol:
    1. a private temporary file `<name>.<32 hex>`;
    2. write it, read it back and flush with `F_FULLFSYNC`;
    3. rename it over the target, then take the directory barrier;
    4. reopen by name and confirm the file and bytes.
  - `floor_step` (item 3): a `writer.lease` probe; read-only reads; classification first; the pure `decide_floor` table, reusing `reconcile_observations`; a floor-only write; and `carrier-floors` created on first need.
  - `create_carrier` (item 3a): re-checks INIT; creates the database exclusively; checks file identity before and after; sets WAL, FULL, `fullfsync` and a zero busy timeout; runs one `BEGIN IMMEDIATE` with the DDL and the format row `SHA-256(N)`; takes the file and directory barriers; writes the witness `COMMITTED 0`.
  - `CarrierRefusal::row()`.
- **Platform.** A charged same-directory `rename_replace_accounted`.

## Judgment calls: please rule on each

1. The X3b-1a / X3b-1b split.
2. No public 468c mapping yet; refusals name only their row.
3. Classification:
   - migrated format 3, or `MigrationRequiresValidation`, takes F46;
   - an object set with no format row, a row below the boundary, or bytes that aren't a database take `MIGRATION.CORRUPT`;
   - a zero-length file, or a WAL database with no objects, counts as no carrier;
   - a non-regular file or another read failure takes host I/O.
4. A malformed floor is a quarantine (`LedgerCorrupt`). The law doesn't name this case.
5. **Floor file custody gap.** The floor directory is judged private, but the floor file's own owner and mode are not, because the bounded reader doesn't return its handle. Is that acceptable, or required now?
6. **SQLite side files.** The `-wal` and `-shm` files get 0600 but not the zero-rights owner allow. Their custody is deferred to X3b-2 or X6. Acceptable?
7. Classification and creation are charged as fixed ceilings (8 objects, 32 or 48 edges, 4 MiB).

## Checks

- Workspace: 1212/0, on two runs. 20 new tests. Clippy and fmt are clean.
- `check_package_edges` passes.
- verify_scratch (v84 then v85) passes.

## Decide

- Does it implement X3b r4 items 3, 3a and 5 (the file protocol) exactly?
- Rule on the judgment calls.
- Is v85 right?
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256" (the sha256 of journal-carrier-inventory-v85-subject.json);
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes, sha256 of v85, parent (the v84 pin), successorRecord}.

Write REVIEW.md and review.json. Do not commit.
