# Independent review — frozen `account-oracles-checkpoint-220`

Reviewer: Claude (independent; Codex remains owner). Date 2026-09-19. Review dir: this directory only.
Scope: the frozen 220 product bytes — closure of my 218 T-1 (real adapter asserted only to return an absolute path) and W-1 (derived `Debug` discloses the home path), in `platform/src/account.rs` only. Production `getpwuid_r` call, retry loop, OS sampling and parser are claimed unchanged; the only new `unsafe` is a macOS-only **test** oracle. Linux is neither executed nor compiled in these lanes and nothing here qualifies it. Scope only — no cumulative approval.

## 1. Identity verified
| Item | Result |
|---|---|
| `subject.tar.xz` | SHA-256 `2f75920db26c43e4e205d92f6c9f71b43b0fbef78630fbdfb4b9907867af2997`, 4,249,996 B = request = `archive-pin.json` |
| Members | 409, all regular/safe, verified from the tar before extraction; re-verified at the end |
| Product pins | 356/356 rehash; none unpinned |
| Delta vs **my own verified 218 extraction** | exactly one file: `crates/platform/src/account.rs`; none added/removed |
| Host receipt 132 | 236 sources all equal product pins; no failed command |

## 2. Owner checks re-run (fresh scratch, offline, locked)
platform 50/50; strict workspace Clippy clean; the account tests also pass with **`HOME` and `TMPDIR` removed** from the environment (`owner/platform-noenv.log`).

## 3. Production lookup unchanged — checked, not assumed
`io/production_unchanged.txt`: the whole region before `#[cfg(test)] mod tests` is **byte-identical to 218** once `#[derive(Debug)]` is removed from one side and the seven-line manual `impl Debug` from the other; and `os_lookup`, `lookup_home`, `home_from_buffer`, `observe_with`, `credentials`, `observe_account` are each identical as function bodies. My 218 FFI audit and OS measurements therefore carry over unchanged.

## 4. Closure of 218 — my 218 harness re-run **verbatim** (paths only), plus three new mutants (`io/mutation220.json`)
| Mutant | 218 | 220 |
|---|---|---|
| `os_lookup` returns the **SHELL** field instead of home | survived | **killed** — "observed home differs from native account oracle" |
| `os_lookup`: `ERANGE` reported as a hard error | survived | **killed** — `actual_adapter_reports_erange_for_a_one_byte_buffer` |
| returns the NAME field | killed | killed |
| (new) returns the GECOS field | — | killed (`MalformedRecord`) |
| (new) `Debug` discloses the home path | — | **killed** |
| (new) `Debug` discloses the UIDs only | — | **killed** (exact string `AccountObservation { .. }`) |
| nine other behavioural mutants | killed | killed |
| `wrapping_sub` (equivalent); non-zero code → `Missing`; result pointer identity unchecked; `HOME` fallback on failure | survived | survived — unchanged class: one equivalent, three with no natural fault on a healthy host (218 §4) |

**218 T-1 closed. 218 W-1 closed** — `finish_non_exhaustive()` over an empty `debug_struct`: no field can leak by later addition without changing the asserted string.

## 5. The points the request singled out
- **Oracle thread lifetime.** `getpwuid(3)` on this host: "these routines are thread-safe and return a pointer to a thread-specific data structure. The contents … are automatically released by subsequent calls to any of these routines on the same thread". The test calls `observe_account()` **first**, then `getpwuid`, null-checks the entry and `pw_dir`, and copies `pw_dir` with `CStr::from_ptr(..).to_bytes().to_vec()` before anything else — there is no account lookup between obtaining the pointer and copying it, and Rust's test harness runs each test on its own thread, so another test's lookup cannot release this storage. The SAFETY comments state exactly that. Excluding Linux, where the non-reentrant result is process-global static storage that parallel tests could race, is the right call.
- **No hard-coded unused UID** — the missing-account case I offered as host-dependent was not adopted; agreed.
- **Sensitive path in failure output.** The comparison is `assert!(a == b, "fixed message")`, not `assert_eq!`, so neither side is printed. Checked empirically: I looked up the real home path and searched every failing mutant log and all my evidence files for it — **0 occurrences** (`mut220-13/16/17/18.log`); the `Debug` regression uses the synthetic `/sample`. `observe_account().unwrap()` can only print `AccountObservationError`, which carries no path.
- **Independence of the oracle.** It is a different libc entry point with libc-owned storage, compared for byte equality only; it shares the OS account database with the product (as any oracle must) but none of the product's buffer/offset logic, which is what the shell/GECOS mutants confirm.

## 6. Findings
None. Notes:
- **N-1** `AccountObservationError` still derives `Debug`; its variants hold an `io::Error` or nothing, so no account datum can appear. If a future variant ever carries a path or name, it needs the same treatment.
- **N-2** the redaction covers `Debug` only; the getters remain the deliberate disclosure points, and a caller can still log `observed.home()` — that is the caller's policy, correctly outside this mechanism.
- **N-3** the remaining three fault-only survivors are inherent to testing a healthy OS without injection; 218's reading-level audit of those lines stands because the lines are unchanged.
- **N-4** proposed inventory v52 already covers this file with an accurate description (my 219 N-1 anticipated exactly this successor); no inventory change is implied.

## 7. Limits
macOS (one host), unprivileged, real UID == effective UID. Mutants only in `build220-*`/`target220-*` scratch copies created after asserting absence, restored from frozen bytes; nothing deleted; no compile failure occurred. To check path disclosure I obtained the real home path in my shell and used it only as a search string — it is not written to any evidence file. Host isolation not re-run (receipt verified against pins). Linux not exercised, not compiled here, not claimed.

## 8. Verdict (bounded)
**220 closes 218 T-1 and W-1: with the production lookup proven byte-identical to 218, my unchanged harness now kills the shell-for-home and real-`ERANGE` mutants, and `Debug` is reduced to a fixed non-exhaustive token pinned by an exact-string test. The macOS oracle respects the documented thread-specific storage lifetime (copied before any further lookup, on the test's own thread), and failing assertions disclose no account path — verified by searching the actual failure output. No finding.** No approval of actor admission, custody, the S3 consumer, Linux behaviour, installation or cumulative readiness.
