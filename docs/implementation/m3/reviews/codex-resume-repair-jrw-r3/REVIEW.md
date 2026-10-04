**REQUIRED-FINDINGS — law J-RW r3.** Two required findings, both P2. No new non-blocking observations.

Reviewer: Codex. Subject: `docs/implementation/m3/resume-repair-jrw/PROPOSAL.md`, 103,333 bytes, SHA-256 `9aa304106bfe7926cee4f43ed5c51dadcc906c0920ed97751c7cd78f4d2b6dee`. Product citations were judged at `cd5958b3608f44a0035566c9d4500e5005c62e91` as directed. The additional X4-F2 routing check used integrated product `d2c00a96c3136fe45b901bc067b6d0ca51f0c9c1`; its lines are identified separately below.

**JRW-R3-01 — the mandatory DDL census asserts the wrong object counts (P2).**

Location: `PROPOSAL.md:248`, `:512` (RW-C17), and the response table at `:15`.

The selected DDL has **7 tables, 1 explicit index and 18 triggers**, totaling 26 statements. The subject repeatedly says 6 tables and 19 triggers, and RW-C17 makes that split a required assertion. That control cannot pass against its own baseline. The total k = 26 is correct and does not need to change.

At `cd5958b`, `project_ledger.rs:33-43` selects these six fragments:

| Fragment | Tables | Explicit indexes | Triggers | Total | Source |
|---|---:|---:|---:|---:|---|
| ATTEMPT_DDL | 1 | 0 | 3 | 4 | `ledger_store.rs:441-469` |
| PAIR_DDL | 2 | 0 | 6 | 8 | `ledger_store.rs:476-503` |
| AVAILABILITY_DDL | 1 | 1 | 3 | 5 | `ledger_store.rs:761-774` |
| recovery_material::DDL | 1 | 0 | 3 | 4 | `ledger_store/recovery_material.rs:13-26` |
| recovery_pins::DDL | 1 | 0 | 0 | 1 | `ledger_store/recovery_pins.rs:14-23` |
| pin_transactions::DDL | 1 | 0 | 3 | 4 | `ledger_store/pin_transactions.rs:16-31` |
| **Total** | **7** | **1** | **18** | **26** | |

In particular, PAIR_DDL creates both `commit_receipts` and `commit_associations`. `sql-source-census.json` records every selected CREATE statement. This is text enumeration, with no SQLite execution.

Required change: correct the breakdown throughout the subject and the RW-C17 specification to 7/1/18. Retain k = 26, the correct per-fragment totals, RW-C5 and its stop rule/fallback. The future census should enumerate the selected statements; the product schema should not be changed to satisfy the erroneous prose.

**JRW-R3-02 — compose trust completion with X4-F2's deferred clock refusal (P2).**

Location: `PROPOSAL.md:147-155` (item 2), `:336` (C-TRUST), `:347` and `:365` (C-TDIR), `:504` (RW-C15), and `:624` (RW-S5).

At the declared base, the fenced read obtains an `AdmittedCurrentTrust` before publishing (`floor_publication.rs:958-995`). J-RW relies on that successful-admission order: completion is inside an admitted durable write; its trust proof says the fenced read admitted the closure; C-TDIR runs after that admission; RW-C15 requires the preceding admitted view.

Integrated X4-F2 changes this enclosing route. At `d2c00a9`, `current_trust_admission.rs:243-259` separates `Admission::View` from `Admission::Clocked`. At `:1113-1125`, a refused clocked standing retains time, floors and a pending write-ahead. `floor_publication.rs:961-995` checks the floors, takes that pending write, and calls `publish` at `:993` before converting the admission into its result at `:995`. `current_trust_admission.rs:283-289` converts the clocked variant into an error, never an admitted view. Consequently, the publication's `parent_dir` and `write_dependency` steps are reachable on a clock-refused request too.

Consider, by source inspection only, an authenticated store with RW-T3's empty ACL-omitted predecessor directory. S4 proposes a floor advance, while EV-CLOCK yields `core:stale-revocation` or `core:expired`. The mandatory write-ahead reaches the directory before that continuation refusal. Completing C-TDIR would finish the floor publication and then return the continuation refusal; no view, lease or committed request follows. A gate requiring a successful admitted view would leave this otherwise repairable directory blocking the required publication. Running completion there instead needs an explicit law premise because the proposal currently places it after successful admission.

X4T r12 states this route at `PROPOSAL-r12.md:170-175` and `:205`: the same write-ahead and owner advance precede a clocked refusal, and no view is returned. Integrated test source `floor_publication_tests.rs:801-849` describes a confirmed write-ahead followed by `CONTINUE-CORE-NOT-TRUSTED`; it was inspected, not run. RW-S5 still calls its amendment X4T r12, although that revision now carries X4-F2's rule.

Required change: explicitly compose C-TRUST/C-TDIR with the authenticated-closure and pending-write authority for this required publication before a deferred clock refusal. Preserve the non-reference proof, fence, checks and refusal precedence, without treating that refusal as an admitted view. Update item 2, items 3.5/3.6, applicable terminal wording and RW-C14/RW-C15. Specify future controls for completion followed by the existing clocked continuation refusal, plus native/custody/budget failures on that route. RW-S5 must succeed X4T r12 and preserve its clock/write-ahead clauses. Earlier authentication/time refusals and report-only reads still write nothing. This finding requests a law revision, not execution of those controls now.

The N-T2a/N-T2b helper split itself remains correct: X4-F2 leaves `open_private` and its native/custody failure mappings unchanged. This finding is the routing check expressly requested in the lead note.

**Disposition of the r2 items.**

- **JRW-R2-01:** the universal-history overclaim is answered. The guarantee is conditional on exclusive creation and OpenSIP-only history, not inferred from custody or the cookie alone. The source supports k = 26; the incorrect control breakdown is now JRW-R3-01.
- **JRW-R2-02:** resolved at `cd5958b`. Native directory-open failures map to `HOST.IO_FAILURE`; an opened directory's failed custody judgment maps to `CONFIG.CUSTODY_REFUSED` / `installation-incomplete`; budget remains separate. C-TDIR requires the retained handle after native success, RW-C15 agrees, and RW-N12 is unchanged.
- **JRW-R2-NB-01:** resolved. My r2 union count of 14 was incorrect. Host -a has 11 bases, -b has 7 and they share 3, yielding **15**. Storage #6 appears at lines 112 (commit) and 1256 (refused-end), and host -a/-b #5 each appear at line 40. Three trace/point selections yield four physical directory events. RW-D1 explicitly arms the commit child. `census-audit.json` contains the complete recount.

**Bound and scope assessment.**

The pinned SQLite 3.53.2 amalgamation explicitly implements wrapping 32-bit cookie increments at `:128440-128455`, stores the cookie at `:100736-100741`, and increments it for VACUUM at `:161652-161670`. Its table, explicit-index and trigger creation paths increment once at `:129318`, `:130875-130877` and `:158430`. The selected tables use WITHOUT ROWID and no AUTOINCREMENT; implicit constraint indexes add no separate increment. Thus the corrected DDL breakdown still establishes 26 increments.

`project_ledger.rs:492-502` executes the six fragments in one BEGIN IMMEDIATE/COMMIT transaction. At `:537-564`, later openings with the committed selected schema take Existing and do not repeat creation. The read-only product-source census found no additional production ledger schema SQL. Storage's additional DROP/CREATE statements are test-gated; security's schema statements operate on the separate journal. Other textual schema-version matches are unrelated Rust identifiers. The two production file openers are `ledger_store.rs:151-176` and `project_ledger.rs:462`, configured defensively at `ledger_store.rs:89-90`, `:125-133` and `project_ledger.rs:474`. In-memory comparison engines and test/fixture feature seams do not increase a production ledger's cookie.

With the explicitly bounded producer history, cookie 0 means no committed schema change, hence no committed row. Foreign same-uid SQL/reset/raw-byte histories are explicitly outside this guarantee. RW-C17 has an assigned owner and RW-C5 requires the future post-DDL cookie pin of 26. The positive-view stop rule and N-L0 fallback remain unchanged: a failed positive view withdraws C-LEDGER without widening L-UNC and leaves L11 open. No runtime pin has been established in this review.

All **22** r2-to-r3 diff hunks belong to the declared three responses or product-base/line re-pins. No unrelated substantive change was found. The X4-F2 finding follows the request's additional current-routing check.

**Verification and acceptance boundary.**

All 38 supplied pins and the extra bundled SQLite source pin matched at the beginning and end. Source snapshots, the diff, named CREATE enumeration and trace recount are retained in this review directory. Scratch analysis used Python with `-I -B` at `nice -n 19`, with isolated HOME and TMPDIR. There were no Cargo commands, builds, product tests, SQLite fixtures, wraparound loops, crash-matrix runs, repository edits, commits, delegation, real-home use or reads of the private 413 fixture. All writes stayed under `/tmp/opensip-implementation/reviews/codex-resume-repair-jrw-r3`.

This is a law review. It accepts no J4 sub-unit, RW-S1 to RW-S6 successor or inventory unit, and supplies no evidence to retire L11.
