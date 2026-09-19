# Independent bounded review — capture follow-ups 130 (Rust)

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-18.
Request: `capture130-20260918-REQUEST.md`. Scope: the delta of frozen `capture-followups-checkpoint-130` over frozen
129 — `platform/src/filesystem.rs` and `security/src/journal_store.rs` — as correction of my capture124 F-2
(reachability-error mapping unpinned) and F-3 (macOS `F_GETPATH` path limit surfacing as disk-full), plus the 126
N-2/N-3 comments. 126 N-1 is **not** claimed closed and is not re-raised. macOS host only; the Linux branch is
unchanged and unexecuted. Caller-side ancestor-anchored custody and operation exclusion remain required (124 F-1).
No frozen/selected/product edit; scratch builds, dedicated target dirs; no commit, push or delegation.

## 1. Subject verification (before use)

| Item | Value |
|---|---|
| `subject.tar.xz` | 4,148,020 bytes, SHA-256 `cf28725ffea4d958d6153dd536b09663158b954207ab01898a5b27e5f735b210` = request and `archive-pin.json` |
| Members | 377/377 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified clean at the end |
| Product pins | 330/330 equal; none unpinned |
| Parent | `parent-inputs.json` equals **my own** verified 129 extraction (330/330) |
| Changed | exactly 2: `crates/platform/src/filesystem.rs`, `crates/security/src/journal_store.rs`; 328 unchanged; no fixture changes |
| Host pins | host80 receipt: 210 sources, all equal the product pins |

## 2. What changed (complete diffs read)
`is_reachable`: an `F_GETPATH` failure with `ENOSPC` becomes `InvalidInput("retained directory path exceeds host
observation limit")`; every other errno is passed through. `linked_operational_parent`: `InvalidInput` →
`Unreadable(Context)`; other errors stay `Unreadable(Io)`; `Ok(false)` stays `Context`. Two real-filesystem tests
(directory removed and replaced by a regular file; a > PATH_MAX directory built in a **child process** so the
runner's cwd is never touched). Three doc/comment additions (path-limit and ancestor-permission limits; 126 N-2;
126 N-3). No behaviour change to confirmation or publication.

## 3. Evidence

**Owner checks, fresh scratch:** platform 33, security 79 pass; strict workspace Clippy clean. Owner's three mutants:
report read, each names the failing test.

**Real-filesystem path-length boundary** (`probes/rust_probe.rs.txt`, child process per length; absolute canonical
path built to an exact byte length; an existing and a missing leaf captured at each):

| Absolute path length | `is_reachable` | existing leaf | missing leaf |
|---|---|---|---|
| 900, 1000, 1020, 1021, 1022, **1023** | `Ok(true)` | `Present(7)` | `Absent` |
| **1024**, 1025, 1026, 1030, 1100, 2000 | `Err(InvalidInput)` | `Unreadable(Context)` | `Unreadable(Context)` |

The boundary is exact at `PATH_MAX` (1023 bytes + NUL fit; 1024 do not) and there is **no intermediate band** in
which `F_GETPATH` succeeds but the re-open fails with a name-too-long error. Above the limit a *missing* leaf is never
`Absent` and an *existing* leaf is never `Present` — the observation is refused as a whole, which is the conservative
direction, at the cost of availability in very deep custody paths (documented now).

**Real error classes** (`io/error-classes.txt`):

| Parent state | `is_reachable` | capture |
|---|---|---|
| removed; **new directory** at the same name | `Ok(false)` (other inode) | `Unreadable(Context)` |
| removed; **symlink** to a directory that *holds the leaf* | `Err(ENOTDIR)` (`O_NOFOLLOW`) | `Unreadable(Io)` — planted leaf never read |
| removed; regular file at the name (owner's case) | `Err(ENOTDIR)` | `Unreadable(Io)` |
| ancestor mode 000 | `Err(EACCES)` | `Unreadable(Io)` for existing **and** missing leaf |
| removed, nothing there | `Ok(false)` | `Unreadable(Context)` |
| **renamed elsewhere** | `Ok(true)` | `Absent` for a missing leaf — unchanged 124 F-1 caller obligation, as disclosed |

**Mutants** (10, all compiled, baseline green; both crates' lib tests): **8 killed**, among them the 124 F-2 survivor
family in every position — reachability error treated as reachable (owner's), every error classed `Context`,
`Ok(false)` treated as reachable, and the pre-open / post-open / post-read checks removed one at a time — plus
path-limit reported as `Ok(false)`, re-open `NotFound` turned into an error, and identity compared on device only.
**2 survived:**
- *`ENOSPC` mapping applied to every `F_GETPATH` errno* — I could not construct another `F_GETPATH` failure on a live
  directory descriptor (the others are `EBADF`-class); unreachable in practice, reported as unpinned, not as a defect.
- *`O_NOFOLLOW` dropped from the re-open* — re-ran my error-class probe under this mutant: only the symlink row
  changes, from `Unreadable(Io ENOTDIR)` to `Unreadable(Context)` (the identity comparison still rejects the
  target). It never moves toward `Absent` or `Present`. So `O_NOFOLLOW` is defence in depth here and only the
  *class* is unpinned: N-2.

## 4. Closure

| 124 / 126 item | Status |
|---|---|
| 124 **F-2** reachability error must never become absence; mapping unpinned | **Closed** — real `ENOTDIR` path, seam proven not to open, all six placement/mapping mutants killed |
| 124 **F-3** `ENOSPC` from `F_GETPATH` shown as storage-full `Io` | **Closed** — `InvalidInput` → `Unreadable(Context)`, real > PATH_MAX directory, exact boundary measured, both owner mutants and mine killed |
| 126 **N-2**, **N-3** | comments added, accurate to the code I reviewed in 126 |
| 126 **N-1** native-ops choice | open, as the owner says |
| 124 **F-1** relocated parent | open caller obligation, reproduced again above |

## 5. Findings

- **N-1 (low) — `Context` is selected by `ErrorKind`, not by cause.** `linked_operational_parent` maps *any*
  `InvalidInput` to `Context`. Rust maps `EINVAL` to that kind too, so an `EINVAL` from `fstat`/`fcntl`/`open` inside
  `is_reachable` would be reported as "context" rather than `Io`, losing the errno. Both are `Unreadable`, so nothing
  unsafe follows; but the classification the README describes ("path limit ⇒ Context") is wider in code than in
  words. A dedicated marker (a private error type or a distinct `Ok` variant such as `Reachability::Unobservable`)
  would make the mapping exact and would also let the platform crate stop encoding meaning in a message string.
- **N-2 (note)** — the symlink-replacement row is `Io` only because of `O_NOFOLLOW`; without it the result is
  `Context`. Either is acceptable; no test says which is intended.
- **N-3 (note, availability)** — custody directories whose canonical path is ≥ 1,024 bytes can never be captured on
  macOS (every observation `Unreadable(Context)`, including for files that exist). That is the right failure
  direction and is now documented; whoever owns project-root admission should refuse or warn about such roots
  up-front rather than let every later operation fail one at a time.

## 6. Unresolved limits
macOS/APFS only; the Linux `Ok(true)` branch performs no reachability check at all and was not executed. Reachability
is an instantaneous observation; it is not custody. Length boundary measured on this host's `PATH_MAX`; no claim for
other volumes or kernels. No OS, release or cumulative standing.

## 7. Bounded verdict
**130: reviewed, no blocking finding. capture124 F-2 and F-3 are closed on real filesystem states — including an
exact PATH_MAX boundary with no unsafe middle band and a planted-symlink case that is never read — with 8/10 of my
mutants killed and the two survivors shown to be unreachable or class-only. N-1 (kind-based `Context`) is a small
precision issue; 124 F-1 and 126 N-1 remain open as the owner states.** Not approval of custody, Linux, OS, release
or any cumulative standing.

Evidence: `claude-out/pin-verification.json`, `product-pins.json`, `filesystem.rs.diff`, `journal_store.rs.diff`,
`owner/`, `probes/{rust_probe.rs.txt,mutation.py,mutation.json,mutation.log}`, `io/{path-boundary.txt,error-classes.txt}`,
`io-nofollow-mutant/error-classes.txt`, `hashes.txt`.
