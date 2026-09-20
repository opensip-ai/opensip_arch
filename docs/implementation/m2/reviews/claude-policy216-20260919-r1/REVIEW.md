# Independent review — frozen `policy-capture-wiring-checkpoint-216`

Reviewer: Claude (independent; Codex remains owner). Date 2026-09-19. Review dir: this directory only.
Scope: the frozen 216 product bytes — correction of my 213 T-1 / W-1 / N-2 and a new bounded macOS per-account temporary-location mechanism used by the new real-fixture test. UID/groups remain supplied assertions; no policy-during-read, continuous custody, ABA, lease or native-filesystem qualification claim; the unchecked `storage::observe_marker` is unchanged and not an admission path. A passing macOS host lane is **not** Linux qualification. Scoped mechanism review, not cumulative approval.

## 1. Identity verified
| Item | Result |
|---|---|
| `subject.tar.xz` | SHA-256 `778f64ed12ab3cd0244ea9f8fed251ea15c7c82370faeeab8a80a887904b5ed0`, 4,253,540 B = request = `archive-pin.json` |
| Members | 418, all regular/safe, verified from the tar before extraction; re-verified at the end |
| Product pins | 355/355, none unpinned |
| Parent | equals **my own verified 213 extraction**; three changed: `security/lib.rs`, `platform/lib.rs`, `platform/macos.rs`; none added/removed |
| Host receipt 130 | 235 sources all equal product pins; no failed command |

## 2. Owner checks re-run (fresh scratch, offline, locked)
security 172/172, platform 44/44, strict workspace Clippy clean. Additionally I ran the security policy-capture tests with **`HOME` and `TMPDIR` removed from the environment**: pass (`owner/security-noenv.log`) — the fixture location does not come from either variable.

## 3. Closure of 213
| 213 | 216 | Evidence |
|---|---|---|
| **T-1** public file-policy wiring and actor inputs unpinned (3 survivors) | new real-fixture test under the OS account temp location: own-file positive with exact bytes; `uid+1` → `Directory(ForeignOwner)`; `0o602` → `File(OthersWrite)`; `0o620` ± owning group; leaf directory `0o770` ± owning group; absence | my **213 harness re-run verbatim** (diffed; paths only): **12/12 killed** — the three survivors (bare descriptor observation, uid 0, widened groups) now die on `public_policy_wiring_checks_real_file_and_directory_permissions_and_actor`. **Closed.** The production `security/lib.rs` code is unchanged; only doc comments and the test were added |
| **W-1** type doc | `PolicyObservedOperationalFile`: "does not establish file policy DURING the read; only caller-held exclusion can provide that guarantee. Directory samples are checked and discarded, not retained in this value" | **closed** |
| **N-2** precedence | "A directory failure takes precedence even if the file independently failed" | **closed** |

## 4. The FFI mechanism — audited
`platform/macos.rs::account_temporary_directory` (crate-private; re-exported `pub` under `cfg(target_os="macos")` in `lib.rs`): zero-initialised `vec![0u8; 4096]`; one `unsafe` call `libc::confstr(_CS_DARWIN_USER_TEMP_DIR, ptr, len)` with `len == bytes.len()`; the result goes to a **safe** parser `account_directory_bytes(&bytes, needed)`.
- **Buffer safety:** the length passed equals the allocation; the pointer cast `*mut u8 → *mut c_char` is sound; no other `unsafe`. The SAFETY comment states the contract accurately.
- **OS semantics measured** (`io/confstr_semantics.txt`, ctypes against this host's libc): full query returns 50 = value length + 1; with buffers of 0/1/8/49 bytes the call returns 50 (> size) and stores a NUL-terminated truncated prefix; an invalid name returns 0 with `EINVAL`. So the parser's `needed > bytes.len()` refusal is exactly the "truncated" case and the truncated prefix is never used; `needed == 0` (error / no value) falls under `needed < 2`.
- **Byte handling:** requires the terminator at `needed-1`, no interior NUL, builds the path with `OsString::from_vec` (no UTF-8 assumption), requires absolute. No `HOME`/`TMPDIR` lookup or fallback in the code.
- **Parser mutants** (`io/mutation216p.json`, all compiled): over-bound accepted, terminator not required, interior NUL accepted, relative accepted, NUL kept in the path — **5 killed**. Three survive, analysed:
  - *`needed < 1` instead of `< 2`* — **equivalent**: `needed == 1` yields the empty path, which the absolute-path check refuses; the owner's `(b"\0", 1)` case still errors.
  - *length passed as `len + 1`* — a one-byte overflow that only manifests for a ≥4096-byte value; not observable by any ordinary test (sanitizer territory). Correctness here rests on reading the single call, which is right.
  - *`TMPDIR` fallback added on failure* — survives because the real query never fails on a healthy host. The no-environment lane proves the **success** path needs no variable; it cannot prove the **failure** path has no fallback. That property is carried by reading (the function body is three statements). See T-1.

## 5. Findings

### W-1 (low-medium) — the "query" is not a pure observation: macOS creates the directory
`confstr(3)` on this host: "`_CS_DARWIN_USER_TEMP_DIR` Provides the path to a user's temporary items directory. **The directory will be created it if does not already exist.** This directory is created with access permissions of 0700…". The doc comments call the function a "location query" whose result is "location data only… not … creation consent", and the README says "no custody/creation consent from path data" — true of the *data*, silent about the *call*. Today the only caller is a test, where creating the account temp directory is harmless. But the function is `pub` in `opensip-platform`, and this project has strict write-free laws for pre-lease admission and report-only surfaces (195/197/201): a future caller on such a path would perform a file-system creation through an innocent-looking getter. Say so in both doc comments ("the OS may create the directory as a side effect; never call on a write-free path"), or make the public item `#[cfg(test)]`/test-support only until a production need exists.

### T-1 (low) — "no HOME/TMPDIR fallback" is unpinned on the failure path
As analysed above. If root wants it pinned without a fault-injecting libc: make the outer function a thin `account_directory_bytes(&bytes, needed)` **and nothing else** (it already is) and add a source-independent assertion in the parser test that an error from the parser is what the outer function would return — i.e. keep the fallback impossible by construction (no `Result` combinator after the parser). A comment forbidding `or_else` there is the cheap version. Not a behavioural defect.

### Notes
- **N-1** the returned value is raw OS data: on this host `/var/folders/…/T/` — a *symlinked* prefix (`/var → /private/var`) and a trailing slash. `RetainedDirectoryPath::open` refuses non-canonical shapes, so every caller must canonicalise and then admit each component; the security test does (`fs::canonicalize`), and the doc comment says "callers must admit every directory component". Worth adding "not canonical" explicitly, since the natural mistake is to pass it straight to the retained-path opener and read the refusal as a custody failure.
- **N-2** error cause: a zero return (invalid name, `errno` set) and an over-bound result both become `InvalidData` with one message; `io::Error::last_os_error()` is not consulted. Fine for a test helper; a production caller would want the two separated.
- **N-3** the fixture uses the file's own uid/gid and says "Fixture uid/gid only; production actor inputs have separate provenance" — and the uid-0 and widened-groups mutants prove the production path uses the supplied values.
- **N-4** the new `pub fn` exists only on macOS; any non-test consumer must be `cfg`-gated. No Linux counterpart is claimed.

## 6. Limits and disclosure
macOS (APFS), unprivileged, one host. Mutants/probes only in `build216-*`/`target216-*` scratch copies created after asserting absence, restored from frozen bytes; nothing deleted; no compile failure occurred. The ctypes measurement calls the same OS query and therefore has the same creation side effect (the directory already existed). No sanitizer run. Host isolation not re-run (receipt verified against pins). Linux not exercised and not claimed.

## 7. Verdict (bounded)
**216 closes 213 T-1, W-1 and N-2: my unchanged 213 harness now kills all twelve mutants, the three public-wiring survivors by a real owned-fixture test that needs neither `HOME` nor `TMPDIR`. The FFI call passes exactly the allocation length, the OS's truncation/zero-return semantics are as the parser assumes (measured), and five of eight parser/FFI mutants are killed with one survivor equivalent and two unobservable without fault injection. One thing to fix in words or visibility: W-1 — on macOS this query *creates* the account temp directory if absent, so it is not an observation and must never be used on a write-free path.** No approval of actor provenance, exclusion, leases, admission, Linux behaviour, installation or cumulative readiness.
