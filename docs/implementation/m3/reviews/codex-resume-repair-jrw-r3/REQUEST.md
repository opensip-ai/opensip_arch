Codex review: J-RW r3, the resume/repair writer law. This is a **law and contract-soundness** review, round 3. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex-resume-repair-jrw-r3.

**Lead note (product base).** r3 reads the product at `cd5958b`. Main has since moved to `d2c00a9`:
- **X4-F2** (`988f6ed`) changed `crates/security/src/trust/current_trust_admission.rs` and `floor_publication.rs`, which r3 cites for N-T2's routing. Judge those citations at `cd5958b`, using `git show cd5958b:<path>`.
- **The other commits since** are I1-a, X3a-2 (the read-side endpoint), VD2-a/F8c (tools) and binding-only lock rows. None changes the storage ledger code that k and RW-C17 rest on.

If X4-F2 changes any routing that J-RW relies on, raise it as a finding. Don't run cargo.


**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- No product builds or test runs: a timing-sensitive crash-matrix run may be using this machine. Do not run any lead set, SQLite fixture or wraparound loop.
- Never touch the real home.
- Never read the 413 fixture.
- Use read-only scratch scripts under your review directory if you need them, at low priority, as in rounds 1 and 2.

## Subject

The pins are in `hashes.txt`. The subject is untracked in arch until it is accepted.
- **The subject:** `docs/implementation/m3/resume-repair-jrw/PROPOSAL.md`, law J-RW r3. It is the subject of `subjectSha256`.
- **For diffing:** `docs/implementation/m3/resume-repair-jrw/PROPOSAL-r2.md`, r2's exact bytes (`7bff3d55…`), the subject of your round-2 review.
- **Your round-2 review**, copied into arch: `docs/implementation/m3/reviews/codex-resume-repair-jrw-r2/{review.json,REVIEW.md}`. Two required findings at P2 (JRW-R2-01, JRW-R2-02) and one observation (JRW-R2-NB-01).
  - A note on your source line numbers: your `src/build.c:1934-1958` and `src/vacuum.c:329-352` are your reading of the GitHub tag. r3 cites the amalgamation the product actually bundles (SQ-SRC, below), whose line numbers differ.
  - At the GitHub tag `version-3.53.2`, `sqlite3ChangeCookie` is at `src/build.c:2028-2053`.
- **One pin outside both repositories: the bundled engine's source (SQ-SRC).**
  - **The file:** `/Users/sb/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/libsqlite3-sys-0.38.2/sqlite3/sqlite3.c`, 9,507,037 bytes, sha256 `0a409f1633283fa31a9126b11fbfd64a1991c5d30defad07e5745d4667f5e23d`.
  - **Why it is the engine:** it declares `SQLITE_VERSION "3.53.2"` at `:470`, and the product's `Cargo.lock` selects `libsqlite3-sys` 0.38.2 and `rusqlite` 0.40.2 (`Cargo.lock:168-169`, `:314-315`).
  - **What r3 cites in it:** `:128440-128455`, `:100736-100741`, `:161652-161670`, `:129318`, `:130875-130877` and `:158430`.
  - Read it; do not build it.
- **The product:** `/Users/sb/code/opensip-ai/opensip` at main **`cd5958b`**, read-only.
  - **What changed in crates since `e093e90`:** only X4-F1's ten files (commit `15c0779`), all in `crates/security/src/`:
    - `custody/operation_guard.rs` and `custody/operation_live_tests.rs`;
    - `trust_time.rs`;
    - under `trust/`: `current_trust_admission.rs`, `current_trust_admission_tests.rs`, `floor_publication_tests.rs`, `live_observation.rs`, `live_observation_tests.rs`, `role_machine.rs` and `trust_bootstrap_tests.rs`.
  - **Which of them r3 cites:** only `current_trust_admission.rs`, **re-checked at `cd5958b`**. Its `TrustRow` enum is at `:56`, `code()` at `:89-104` (`HOST.IO_FAILURE` at `:100`, `WORK.BUDGET_EXHAUSTED` at `:101`), and `subject()` at `:105-114` (`installation-incomplete` at `:107`). These are 4 lines lower than the `:84-110` you cited at `e093e90`; the mapping is unchanged.
  - **Unchanged since `e093e90`:** `floor_publication.rs`, `private_access.rs`, the storage crate and the platform crate.

**Scope.** r3 answers the three round-2 items and re-pins product lines. It should change nothing else of substance. Diff r2 against r3: every change should belong to a row of the "r3 changes and review responses" table, or to the re-pinned product lines.

## What r3 changes

1. **JRW-R2-01: C-LEDGER is kept, and its guarantee is now exact** (item 3.3).
   - **The wrap.** The cookie is shown to wrap, from the bundled engine's source. r2's "not reachable", and its coverage of "any writer that changes the schema only by SQL schema statements or VACUUM", are withdrawn.
   - **The bound.** The guarantee is scoped to OpenSIP's writers by **k = 26**, the most cookie increments they can commit in a ledger's lifetime. It is established in five steps:
     1. X3c item 2's one DDL transaction holds 26 `CREATE` statements: 6 tables, 1 explicit index and 19 triggers (`project_ledger.rs:33-43` and the six fragments it names);
     2. each increments the cookie exactly once in 3.53.2 (`sqlite3.c:129318`, `:130875-130877`, `:158430`);
     3. the transaction commits at most once (`project_ledger.rs:537-564`);
     4. no other product SQL changes a ledger's schema: a census at `cd5958b` finds every storage `DROP` inside `#[cfg(test)]` modules, no `VACUUM`, `ALTER`, `ANALYZE`, `REINDEX`, `PRAGMA optimize`, `auto_vacuum`, `incremental_vacuum`, `writable_schema` or `schema_version` statement in non-test product source, and only two defensive production openers;
     5. no migration exists (X3C:85).
   - **Foreign writers.** A non-OpenSIP same-uid writer that commits 2³² − k or more schema changes, which is your counterexample, joins raw-byte forgery under "Not established".
   - **New controls:** RW-C17 (a code-inspection census of product SQL, authored by J4c and kept by X3c's owner), and RW-C5's pin of cookie 26 after creation.
   - **Unchanged:** the stop rule and the N-L0 fallback.
   - **Carried into:** RW-S3, X-RW-9, the forbidden substitutes, LD-5 and "Not claimed".
2. **JRW-R2-02: N-T2 is split at the existing failure boundary** (item 3.6, item 5, RW-C15, new LD-15).
   - **N-T2a.** A symlink or non-directory at a publication-parent name fails the native open and keeps `HOST.IO_FAILURE`.
   - **N-T2b.** Only a directory that is opened and reaches the custody judgment takes `installation-incomplete`.
   - **Budget.** A budget failure keeps the budget row, and X4T r11 item 10's preserved rows (X4T:153) are unchanged.
   - **C-ACL** runs only on the retained directory `open_private` returned.
   - **RW-N12** is unchanged.
3. **JRW-R2-NB-01: point identities versus physical records** (item 1, item 3.6, item 4, RW-D1).
   - **Host traces.** `-a` (1009 records, 11 bases) and `-b` (165 records, 7 bases) share 3 bases, so their union has **15**. You reported 14; r3 lists every base so the count can be checked.
   - **Physical events.** Storage's `#6` has two physical records (commit `:112`, refused-end `:1256`). So there are three trace/point selections and four physical directory events.
   - **RW-D1** arms the commit child.

## Decide

1. **JRW-R2-01.**
   - Is the guarantee now stated exactly and no wider than k supports?
   - Is k = 26 established by item 3.3's five steps, against the product at `cd5958b` and SQ-SRC?
   - Are the foreign-writer cases correctly placed outside the custody threat model?
   - Do RW-C17, with its owner, and RW-C5's pin of 26 keep k true?
   - Are the stop rule and fallback unchanged?
2. **JRW-R2-02.**
   - Does the N-T2a/N-T2b split leave every existing row unchanged, at `floor_publication.rs:58-69`, `:164-166` and `:170`, and at `current_trust_admission.rs:100` and `:107` at `cd5958b`?
   - Does C-TDIR now run only after a successful native open, on the retained handle?
   - Does RW-C15 match?
3. **JRW-R2-NB-01.** Are the census descriptions accurate, the union count of 15 included?
4. **Scope.** Does r3 change anything else in r2?

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with id, location, problem or claim, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: PROPOSAL.md's sha256.

This is a law review, not a `verify_design` unit. J4's sub-units each need their own inventory-unit review, and RW-S1 to RW-S6 each need their own review. Do not commit.
