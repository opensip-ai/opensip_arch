# Independent review — frozen `account-observation-checkpoint-218`

Reviewer: Claude (independent; Codex remains owner). Date 2026-09-19. Review dir: this directory only.
Scope: the frozen 218 product bytes — a new OS credential/account **producer** (`platform/src/account.rs`, exported from `platform/lib.rs`): real/effective UID sampled before and after a `getpwuid_r` lookup of the **real** UID, returning a privately constructed owned tuple with the account-database home. It is an observation mechanism: a differing effective UID is reported, not endorsed; no supplementary-group authority; no environment fallback; no wall-clock or no-OS-side-effect guarantee; no production caller; native qualification, custody and the S3 consumer remain owed. macOS only was exercised — nothing here is Linux qualification. Scoped mechanism review, not cumulative acceptance.

## 1. Identity verified
| Item | Result |
|---|---|
| `subject.tar.xz` | SHA-256 `ce10bc743c2f0840dcc266cbe542f319a54aff100666c6bbb56d27860f9ff9f8`, 4,239,744 B = request = `archive-pin.json` |
| Members | 419, all regular/safe, verified from the tar before extraction; re-verified at the end |
| Product pins | 356/356 rehash; none unpinned |
| Delta vs **my own verified 217 extraction** | one changed (`platform/src/lib.rs`: a `cfg(any(macos, linux))` module declaration under `#[allow(unsafe_code)]` and one `pub use`), one added (`platform/src/account.rs`, 286 lines); none removed |
| Host receipt 131 | 236 sources all equal product pins; no failed command |

## 2. Owner checks re-run (fresh scratch, offline, locked)
platform 48/48, strict workspace Clippy clean.

## 3. Unsafe/ABI audit (module read in full)
- **Three `unsafe` sites.** `getuid`/`geteuid` (no pointers); `mem::zeroed::<libc::passwd>()` (integers and raw pointers — all-zero is valid); one `getpwuid_r(uid, &mut record, bytes.as_mut_ptr().cast(), bytes.len(), &mut result)`. The length passed equals the slice length; `record` and `result` are live locals; nothing escapes — `os_lookup` returns `pw_uid` and the **address** of `pw_dir` as a `usize`.
- **No raw-pointer dereference anywhere.** `home_from_buffer` computes `address.checked_sub(bytes.as_ptr() as usize)`, then `bytes.get(offset..)`, then searches for NUL *within that bound*, then copies with `OsString::from_vec` (no UTF-8 assumption) and requires an absolute path. A null `pw_dir`, an address below or beyond the buffer, an address equal to its end, an unterminated tail, an empty or relative string all become `MalformedRecord`. Pointer→integer only; there is no integer→pointer cast, so no provenance question arises.
- **Result discipline:** `ERANGE` → retry; any other non-zero code → `Lookup(io::Error)` with the code preserved; `code == 0` with null `result` → `MissingAccount`; `result` must be pointer-identical to `&record`; the returned `pw_uid` must equal the requested UID.
- **Bounds:** fresh zeroed buffer per attempt, sizes 1024…65536 doubling, exactly seven calls, then `RecordTooLarge`; no arithmetic can overflow.
- **Credentials:** the lookup is keyed by the *real* UID sampled first; a second sample must equal the first or `CredentialsChanged`; both UIDs are reported. Private fields, no public constructor, not `Clone`.
- **OS semantics measured on this host** (`io/getpwuid_semantics.txt`, ctypes; booleans only, no account data printed): own UID with a 1- or 16-byte buffer → `ERANGE`; with 64 or 1024 bytes → 0, `result == &record`, `pw_dir` **and** `pw_shell` inside the caller's buffer; an unused UID → 0 with null `result`. Every assumption the code makes holds on macOS.

## 4. Mutation (16 mutants, all compiled; `io/mutation218.json`)
**10 killed:** after-lookup re-sample removed; lookup keyed by the effective UID; effective reported as real; returned-UID check removed; retry bound widened; non-`ERANGE` error retried; `Missing` mis-kinded; NUL terminator not required; relative path accepted; *name* field returned instead of home.
**6 survived:**

| Survivor | Assessment |
|---|---|
| address below the buffer `wrapping_sub` instead of refusing | **equivalent** — the wrapped offset is enormous and `bytes.get(offset..)` refuses; the owner's `address = 0` case still errors |
| **`os_lookup` returns the SHELL field instead of the HOME field** | **real gap — T-1** |
| **`os_lookup`: `ERANGE` reported as a hard error** | **real gap — T-1** |
| `os_lookup`: any non-zero code reported as `Missing` | no natural fault on a healthy host; carried by reading |
| `os_lookup`: `result` pointer identity unchecked | same |
| `HOME` environment fallback when the lookup fails | same: the no-`HOME` host lane proves the success path needs no variable, not that a failure path has none |

## 5. Findings

### T-1 (medium as a test gap) — the real OS adapter is tested only for "returns something absolute"
Everything below `lookup_home` is exercised through injected closures; the only test that reaches `os_lookup` asserts the two UIDs and `home().is_absolute()`. Consequently a mutant that hands back **the login shell's address** (`pw_shell`, e.g. an absolute `/bin/…`) passes all 48 tests — the single datum this mechanism exists to produce is unverified. (The *name* swap dies only because a name happens not to be absolute.) Likewise the real `ERANGE → LargerBuffer` mapping is never driven by the OS, only simulated one layer up.
Both are deterministically testable on this host without environment data and without printing anything (`probes/oracle218_probe.rs.txt` → `io/oracle218.txt`):
- **independent-API oracle:** `libc::getpwuid(uid)` (the non-reentrant entry point, libc-owned storage) `pw_dir` bytes equal `observe_account().home()` — frozen 218: `true`, and `pw_shell` differs; under the shell mutant: `false`/`true`. This compares two OS answers, not an environment variable, and asserts equality only.
- **real `ERANGE`:** `os_lookup(own_uid, &mut [0u8; 1])` → `LargerBuffer` on frozen 218, `Err` under the mutant.
- **real missing account:** `os_lookup(3_999_999_999, …)` → `Missing` on this host (host-dependent choice of UID; the owner may prefer to probe for an unused UID first).

### W-1 (low) — `#[derive(Debug)]` on the public observation prints the home path and UIDs
The owner's own test comment says "Do not log account names, home paths…". `AccountObservation` derives `Debug`, so any `{:?}` — in an `unwrap` panic, an error context, a future trace — emits the real user's home path. `AccountObservationError::Lookup(io::Error)` is harmless. A manual `Debug` that redacts `home` (length or a fixed token) keeps the rule enforceable rather than advisory. No current caller, so nothing leaks today.

### Notes
- **N-1 Linux is compiled, not qualified.** `cfg(any(macos, linux))` builds this on Linux, where "not found" may be reported by some libcs as `ENOENT/ESRCH/EBADF/EPERM` rather than `0 + NULL` (it would become `Lookup(_)`, still fail-closed), and where glibc NSS can load provider modules. The header already says providers may block or consult services; the README says no Linux claim. Worth keeping that sentence attached to the `cfg`.
- **N-2 what is *not* observed:** real/effective/saved GIDs and supplementary groups are not sampled, by design ("no supplementary group auth"); custody predicates therefore still receive groups as caller assertions. A saved set-UID differing from both samples is also invisible. Stated, not a defect.
- **N-3 `EINTR`** is reported as `Lookup`, not retried; correct for a bounded mechanism (a retry policy belongs to a caller with a deadline).
- **N-4** absolute ≠ meaningful: system accounts legitimately have homes like `/var/empty`; the doc comment's "consumer must separately resolve/admit it under its discovery policy" is the right boundary (S3 owns that).
- **N-5** the frozen author script's Python `SyntaxWarning` and the completed rehash are as the request describes; the archived module bytes equal the pinned product file (pins verify).

## 6. Limits and disclosure
macOS (one host), unprivileged, real UID == effective UID — a genuine set-UID difference was exercised only through the injected sampler, not by the OS. Mutants/probes only in `build218-*`/`target218-*` scratch copies created after asserting absence, restored from frozen bytes; nothing deleted; no compile failure occurred. My ctypes and Rust probes call the same account lookups as the product (they may touch the OS directory-service cache) and print booleans only. No sanitizer run; `len + 1`-style ABI mutants are unobservable without one and were not attempted. Host isolation not re-run (receipt verified against pins). Linux not exercised.

## 7. Verdict (bounded)
**The FFI is sound: caller-owned storage of exactly the passed length, a result pointer checked for identity, the returned UID checked against the request, and the home string recovered by bounds-checked offset arithmetic with no raw-pointer dereference; macOS's measured `getpwuid_r` behaviour matches every assumption; the lookup is keyed by the real UID with before/after credential agreement, seven bounded attempts, no environment fallback in the code, and a privately constructed result. Ten of sixteen mutants are killed and one survivor is equivalent. The gap is evidential (T-1): the real adapter is asserted only to return an absolute path, so returning the shell field instead of the home field — and breaking the real `ERANGE` mapping — pass the suite; both have deterministic, environment-free tests on this host. W-1: the public type's derived `Debug` prints the home path.** No approval of actor admission, elevated execution, custody, the S3 consumer, Linux behaviour, installation or cumulative readiness.
