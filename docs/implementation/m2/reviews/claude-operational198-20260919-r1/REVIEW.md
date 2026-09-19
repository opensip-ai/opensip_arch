# Independent review — frozen `operational-custody-checkpoint-198`

Reviewer: Claude (independent; Codex remains owner). Date 2026-09-19. Review dir: this directory only.
Scope: the frozen 198 product bytes — correction of my 196 F-1/T-1/T-2 in both SQLite readers, and the S7 operational-file predicate with its private descriptor adapter (195 owner). Not: actor/group provenance, ancestor/name custody, local-filesystem admission, exclusion, lease-held consumption, Linux ACL, SQLite's own descriptors, host mapping — all declared owed. No installation or cumulative approval.

## 1. Identity verified

| Item | Result |
|---|---|
| `subject.tar.xz` | SHA-256 `9138265f191522524a434d372bc8faa24acdb8518772b7293be25a00ba55d42e`, 4,292,992 B = request = `archive-pin.json` |
| Members | 435, all regular/safe, verified from the tar before extraction; re-verified at the end |
| Product pins | 352/352, none unpinned |
| Parent | equals **my own verified 196 extraction**; exactly three changed (`ledger_store.rs`, `journal_store.rs`, `custody.rs`); none added/removed |
| Host receipt 125 | 232 sources equal product pins; no failed command |

## 2. Owner checks re-run (fresh uniquely named scratch, offline, locked)
storage 87/87, security 159/159, strict Clippy clean (`claude-out/owner/`).

## 3. Closure of my 196 items — each proved by re-applying the 196 survivor

| 196 item | 198 change | My mutant on 198 | Result |
|---|---|---|---|
| F-1 busy read-back after first DB-touching query | read-back moved into `configure_connection_controls`, before the encoding query, **for writers too**; later loop kept | — | **closed** by reading; see T-1 for what cannot be tested |
| T-1 order unpinned (ledger `query_only`) | stage function + "no sidecar after the stage" test + post-fault state assertions | `query_only` moved after encoding | **killed** (both new tests) |
| T-1 (ledger NO_CKPT late) | same | NO_CKPT moved after encoding | **killed** |
| T-1 (journal NO_CKPT late) | `configure_reader_controls` stage, 3 encodings | NO_CKPT moved after `journal_mode` | **killed** |
| T-2 effect tests blind to NO_CKPT | test-only writable connection through the same controls; negative control disables it | NO_CKPT omitted **and** helper flag assertion removed (the exact 196 survivor), ledger / journal | **killed by physical effect** both |
| (new) stage purity | — | encoding query / `journal_mode` query moved *into* the control stage | **killed** by the sidecar-absence assertion — the file system works as the order spy |

The negative control in the writable test is sound: with NO_CKPT disabled the WAL is removed and main changes; with it retained both are byte-identical. No production writable-reader path exists (diff: the open boundary still refuses `!is_readonly`).

## 4. Operational-file predicate

Code read in full (`check`, l.69–127): regular only; symlink/directory/other refused; owner must be root or invoker **regardless of `waive_owner`**; others-write refused; group-write only for an authorized owning group; every ACL writer must be trusted; `links == 1`; configuration's 4 MiB cap not applied. That is 195 S7 exactly ("regular, not a symlink, one hard link, same owner/mode/ACL predicates, no waiver… no unlimited read is granted" — the adapter reads nothing, so no read bound is implied).

Mutants (all compiled; `io/mutation198.json`): waiver honoured, cap applied, link check skipped, links==0 admitted, directory admitted, adapter using `ConfigurationFile` scope, group-write always trusted, ACL check skipped — **8/8 killed**. Overall 15/16.

My real-descriptor probe (`probes/operational198_probe.rs.txt` → `io/operational198.txt`), cases the owner test does not have:

| Case | Result |
|---|---|
| real SQLite `main`, `-wal` (12,392 B), `-shm` (32,768 B) with a live connection | all `Ok`, links 1, mode 644 — the predicate admits what the engine actually creates |
| empty regular file (a fresh 0 B WAL) | `Ok` |
| directory descriptor | `NotRegular` |
| mode 0660, group not authorized / owning group authorized | `GroupWrite` / `Ok` |
| file unlinked after open (links 0) | refused — as `HardLinked` (see W-1) |

## 5. Findings

No defect in the changed behaviour. One labelling point, one residual, notes.

### W-1 (low) — an unlinked retained file is refused as `HARD_LINKED`
`links != 1` maps both 0 and ≥2 to `Refusal::HardLinked` (`"HARD_LINKED"`); the owner test pins `links: 0 → HardLinked`. For configuration files that never mattered. For operational files it is a *lawful, expected* state: 195 §2 — "Sidecars may lawfully disappear and reappear before this reader fixes its snapshot when another connection closes last." A retained `-wal`/`-shm` descriptor observed after another connection's last close has `st_nlink == 0`. Refusing is right (the descriptor no longer names the path); calling it a hard link will misdirect the future host mapping and any diagnostic, and it is exactly the case 195 says must not be treated as an identity failure before the snapshot is fixed. Add an `Unlinked` refusal before the adapter gets a production caller.

### T-1 (residual, no test demanded) — position of the busy read-back
Mutant "busy read-back moved back after the encoding query" **survives** 87/87: the value is 0 either way, and the post-fault assertion reads the pragma itself. I agree with the README that this belongs to the class the engine cannot naturally fault (same as the read-back/access-mode survivors I listed in 196). Recorded so the closure of F-1 is understood as *by construction and review*, not by test. No test is demanded. One small consistency point: the journal stage carries the comment "This stage may execute connection-control SQL, never data/schema queries"; the ledger stage has only "before the first data/schema query" on the read-back. Giving the ledger stage the same sentence states the invariant the new sidecar-absence test enforces.

### Notes
- **N-1** `inspect_operational_file` has no production caller (tests only). That matches the README ("private adapter… grants no authority"); integration is where 195's before/after rechecks and W-1 will bite.
- **N-2** SQLite creates sidecars with main's mode. A main created under umask 002 (0664) yields group-writable sidecars that this predicate refuses unless the owning group is authorized — correct by S7, and worth stating where ledger/journal *creation* fixes the mode, so a later read does not fail on a mode the product itself produced. I did not check the creators in this review.
- **N-3** the ledger writable-reader test calls `configure(&c, true)` (full path), the journal one calls only the control stage and then queries `grant_journal_v3` directly — both adequate for the effect being shown.
- **N-4** my retry note still applies unchanged; 198 adds no retry or timeout, as stated.

## 6. Limits and disclosure
macOS, one engine build, unprivileged runner. Mutants/probes only in `build198-*`/`target198-*` scratch copies created after asserting absence, restored by copying frozen bytes; **nothing was deleted**; no compile failure occurred, none would have been counted. Build targets are excluded from `hashes.txt`. I did not re-run the host-isolation pipeline (receipt sources verified against pins only).

## 7. Verdict (bounded)
**198 closes 196 F-1, T-1 and T-2: every 196 survivor I carried forward is now killed, the two NO_CKPT omissions by physical effect rather than by a configuration assertion, and sidecar absence after the control stage works as a genuine order spy in all three journal encodings. The operational-file predicate implements 195 S7 exactly and admits the files SQLite really creates. Remaining: W-1 (links 0 reported as `HARD_LINKED`, a state 195 calls lawful for sidecars) and the untestable busy read-back position.** No approval of integration, custody completeness, or cumulative readiness.
