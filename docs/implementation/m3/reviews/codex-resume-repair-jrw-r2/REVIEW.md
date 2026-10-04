# J-RW r2 — Codex law review

**REQUIRED-FINDINGS: two required findings, one non-blocking observation.**

Subject: [PROPOSAL.md](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/resume-repair-jrw/PROPOSAL.md), 87,080 bytes, SHA-256 `7bff3d5548fa627c4cf0fd14b869a83c42a74a6e2059573e716788aa6bac8a4b`.

All 34 supplied pins match. This reviews the law and its contracts against product baseline `e093e908dd7fe735356a896f3cf4b97e1d93198e`. It grants no implementation-unit or successor-law acceptance.

## Required findings

### JRW-R2-01 — Qualify the schema cookie's history guarantee (P2)

Location: item 3.3, lines 200–226, especially 211 and 220–226; its basis at 236; RW-S3 at 538; X-RW-9 at 578–581.

The cookie fixes the original CREATE/INSERT/DROP/VACUUM counterexample. It does not prove the stated universal guarantee against every writer that uses SQL schema statements or VACUUM. The cookie wraps modulo 2³². Item 3.3 acknowledges this case but calls it unreachable, then still asserts that a recovered zero establishes no committed schema history.

The pinned product uses bundled `rusqlite =0.40.2` (`crates/storage/Cargo.toml:13`). Its underlying `libsqlite3-sys 0.38.2` identifies the bundled SQLite as 3.53.2. [Primary crate documentation](https://docs.rs/crate/libsqlite3-sys/0.38.2).

SQLite 3.53.2's `sqlite3ChangeCookie` uses unsigned arithmetic to increment the cookie; the preceding comment explicitly allows repeated changes to restore an earlier value (`src/build.c:1934–1958`). VACUUM reads the cookie into `u32 meta`, adds one and preserves the encoding and both application IDs (`src/vacuum.c:329–352`). [SQLite build.c](https://raw.githubusercontent.com/sqlite/sqlite/version-3.53.2/src/build.c), [SQLite vacuum.c](https://raw.githubusercontent.com/sqlite/sqlite/version-3.53.2/src/vacuum.c).

A static counterexample is:

1. Start with cookie 0 in a private WAL database, UTF-8, both IDs zero.
2. Commit CREATE TABLE, INSERT, and DROP TABLE.
3. Complete 2³² − 2 ordinary VACUUM operations.

The committed schema increments total 2³². The final cookie is zero; the schema is empty, and VACUUM permits the same one-page, zero-freelist footprint. The file has nevertheless held committed data. This sequence requires no raw-byte write, cookie assignment, writable-schema mode, or non-defensive operation. It was **not executed**.

Defensive mode at `ledger_store.rs:125–133` prevents the cited direct reset operations; it does not bound the lifetime number of ordinary schema increments. RW-C5's finite negative fixtures cannot supply that bound. The law already names wraparound as a limitation, so the necessary correction is a precise, consistent qualification of the guarantee.

**Required fix:** state explicitly that the relevant file history starts at cookie zero, has fewer than 2³² committed schema-cookie increments, and has no reset/forgery. Identify the no-wrap condition as an assumption about custody and producer history, which L-UNC cannot infer from the current file. Remove the ordinary-interface unreachability claim and qualify the coverage of arbitrary SQL/VACUUM writers. Propagate that qualification through the basis, RW-S3 and X-RW-9. If a universal guarantee is retained, an independent history discriminator is required, or C-LEDGER must remain withdrawn for histories it cannot establish. Keep the existing positive-view stop rule and N-L0 fallback. No wraparound stress run is requested.

### JRW-R2-02 — Preserve the existing native-open refusal row (P2)

Location: item 3.6 at line 300, N-T2 at 350, RW-C15 at 431; compare the unchanged-row rule at 331 and RW-C2 at 407.

N-T2 places symlinks and non-directories in the `installation-incomplete` row. RW-C15 requires that result. These cases instead fail a native directory open and produce `HOST.IO_FAILURE` at the pinned product baseline:

- `floor_publication.rs:434` calls `open_private` before directory creation. The open at 164–166 maps failures through `lift(TrustRow::HostIo)`; only the subsequent private-directory judgment at 170 maps through `TrustRow::Incomplete`.
- `platform/src/filesystem/directory_open.rs:61–73` treats only NotFound as absence. At 134–150, `O_DIRECTORY | O_NOFOLLOW` causes a symlink/non-directory to return its native error.
- `floor_publication.rs:58–69` preserves the supplied operation-failure row and separately preserves the budget row.
- At `e093e90`, `current_trust_admission.rs:84–110` maps `HostIo` to `HOST.IO_FAILURE`, with no `installation-incomplete` subject. `Incomplete` maps to `CONFIG.CUSTODY_REFUSED` with that subject.
- Accepted X4T r11 item 10, line 153, preserves host I/O and budget rows.

For example, a regular file at the current pointer's successor directory name is outside the admitted reference closure. The unchanged fenced read can succeed, then publication's parent-directory open fails before custody sampling. It must retain the host I/O row.

**Required fix:** split N-T2 by the existing failure boundary. A successfully opened directory whose custody/completion predicate fails keeps `CONFIG.CUSTODY_REFUSED / installation-incomplete`. Native directory-open failures, including symlink/non-directory failures, keep `HOST.IO_FAILURE`; budget failures keep their budget row. Apply this distinction to item 3.6 and RW-C15. C-ACL requires an obtained retained directory and precisely P-ACL, without recovering or reclassifying a native open failure.

RW-N12's specific non-empty ACL-omitted directory reaches the custody judgment, so its `installation-incomplete` expectation is correct and stays unchanged.

## Non-blocking observation

### JRW-R2-NB-01 — Distinguish point identities from recorded child events

Location: item 1, lines 104–110; item 3.6, 290–293; RW-T3 and the count at 325–327.

The state coverage is adequate, but the host traces do not have the same creation bases. Trace `-a` has 11 `create.after` bases, trace `-b` has seven, and their union has 14. They share the dependency-publication shape; their journal witness bases differ.

Storage records the predecessor-directory point twice: `commit` at line 112 and `refused-end` at line 1256, both `dependency/create.after#6`. Host `-a` and `-b` each record #5 at line 40. Thus the cited three trace/point selections correspond to **four physical directory events** across publishing children. Manifest-verified host `-c` has 21 records and no `create.after`.

Clarify these distinctions and note the refused-end occurrence. This does not demand another state or row: that event leaves the same RW-T3 state, RW-D1 explicitly uses the commit driver, and the differing host bases remain covered by P states or existing journal owners. Neither target samples its predecessor-directory point in its kill set.

## Decisions on the six requested items

| Request item | Assessment |
|---|---|
| 1. L-UNC | The original compacted-history counterexample is excluded. The history guarantee needs JRW-R2-01's qualification. RW-C5, its stop rule and N-L0 retain the safety bias if either positive bundled-engine view differs. |
| 2. C-REG | Resolved. The absent-N branch requires absent marker; every present marker requires the complete namespace. The whole join precedes every effect. N-R9's ACL-omitted and private-malformed rows match the existing product. RW-S1/RW-S2 and RW-C16/RW-N10 carry the order. |
| 3. C-TDIR and X9 | The omitted crash-state completion is specified and reachable through unchanged trust admission. Its new neighbour-row contract needs JRW-R2-02. The census accounting needs the non-blocking clarification above. No additional L11 state was found. |
| 4. Original observations | All three edits address their intended points: the named SQLite exception to byte preservation, disjoint exact/prefix neighbour wording, and the seven-creates-per-publication example. |
| 5. Accepted X3c r8 | The joins are compatible subject to JRW-R2-01's qualification. Item 2 is unchanged; CL-3 remains; RC/RW sections are separate; whichever implementation integrates second reruns both, without adding a J4 dependency on X3c-3. |
| 6. Scope | All 19 diff hunks belong to the response table, requested follow-ups, accepted-snapshot repins or their propagated controls/units/matrix/cross-law passages. No unrelated substantive change found. |

C-REG's rows were checked at `project_admission.rs:602–603` (ACL-omitted marker custody), 616 and 684–685 (private malformed marker contradiction), and the creation order at `first_registration.rs:2260–2293`. The earlier finding JRW-R1-02 is closed. The independently specified completion chooses no competing identity, so IE needs no passage successor.

C-TDIR remains after the reference-directed fenced read and under the publication fence. It is restricted to the three `may_create` names, an empty same-filesystem directory with owner/private mode and ACL precisely omitted, and the reached publication parent step. It completes the directory's and parent's barriers before leaf publication continues. The original omission in JRW-R1-03 is closed; JRW-R2-02 concerns the new refusal table.

RW-D1 explicitly covers the unsampled predecessor-directory state. RW-K10 uses a three-child ladder and the repair directory barriers. RW-N12 is a labelled mutation with R1/R2 only. Runs without an ExecutionId omit R1/R4. The law requires reference transcription before scored runs, uses the existing commit driver, and retires L11 only after the future RW rows pass and RW-C5 pins hold. These follow X9 r16's cited rules; none was executed in this review.

X3c r8's subject hash `ba638efbacda47fdddb32bfe5c4e035752c772812cf62fd63bf5766bf38760b7` matches GROK2's ACCEPT record with no findings. J-RW creates no attempt or per-Run evidence during completion. Its RW-S3 successor is based on those accepted bytes and leaves re-commit's standing decision under item 6a. The universal no-history reasoning in X-RW-9 needs the same qualification as item 3.3.

## Evidence and execution boundary

[pin-verification.json](pin-verification.json) records 34/34 supplied pin matches. [input-audit.json](input-audit.json) records static census groupings, target kill-set checks, three additional files verified through the pinned EV manifest, diff hunk ranges and baseline source digests. [diff-r1-r2.patch](diff-r1-r2.patch) records the compared document bytes.

The product checkout advanced to `15c077935a9fdd9d2550726922669d576e7f6c4b` during this review. Judgments remain against `e093e90`. The two declared `crates/` diffs, `3e64266 → e093e90` and `e093e90 → 0ceb9ad`, are empty. The changed `current_trust_admission.rs` was read with `git show e093e90:...`; its cited enum/mapping uses baseline line numbers. The other recorded cited owner files still match that baseline.

Only read-only hash, file and diff tabulation, Git object reads, and primary-source browsing were performed. Scratch Python used the pinned interpreter at `nice -n 19`, with `-I -B` and private review-local HOME/TMPDIR. No product build/test, SQLite fixture, crash matrix, lead set or `verify_design` ran. No repository edit, commit, push, delegation, real-home access or 413-fixture access occurred during this review. All writes are in the authorized review directory.

J4's inventory sub-units and RW-S1 through RW-S6 still require their separate reviews. No executed evidence retiring L11 is granted.

