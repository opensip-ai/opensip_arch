# Independent bounded review — retained directory path binding 161 (Rust, platform)

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-19.
Request: `directory161-20260919-REQUEST.md` (bytes as read: `claude-out/REQUEST-as-read.md`); README/PLAN read. Scope:
the delta of frozen `directory-binding-checkpoint-161` over frozen 159 — `platform/src/filesystem/path_binding.rs`
(new) and its two export lines. A **sampled name-binding mechanism**: not continuous exclusion, not custody, not 124 F-1
closure; no consumer is wired; Linux not executed. I infer none of those. No frozen/selected/product edit; scratch
only, `-I -B`, dedicated targets; no commit, push or delegation; no cumulative approval.

## 1. Subject verification (before use)
| Item | Value |
|---|---|
| `subject.tar.xz` | 4,202,608 bytes, SHA-256 `022666a9cb6701f8a1a3d4922a4c5dd0c010934f82a022b36202fecda800d8a4` = `archive-pin.json` (no digest in the request; archive pin and every member verified) |
| Members | 468/468 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified at the end |
| Product pins | 343/343; none unpinned |
| Parent | `parent-inputs.json` = **my own** verified 159 extraction (342/342); 340 unchanged; 2 changed (`filesystem.rs`: `mod` + `pub use`; `lib.rs`: re-export), 1 added |
| Host pins | host100 receipt: 223 sources all equal the product pins; no command failed |
| Owner checks, fresh scratch | 42/42 platform tests; strict workspace Clippy clean |

## 2. Audit of the code (read in full; 150 production lines)
- **Unsafe FFI.** One `openat` and one `File::from_raw_fd`. The parent descriptor is borrowed from a live retained
  `File` for the duration of the call; the name is a `CString` built from a component already screened for NUL; flags
  are `O_RDONLY|O_DIRECTORY|O_NOFOLLOW|O_CLOEXEC|O_NONBLOCK` with no creation flag. A non-negative result is wrapped
  in `File` on the next line, before any fallible call, so every later path (including `from_retained_handle` failing)
  closes it exactly once. No descriptor is returned raw, duplicated or borrowed out.
- **Descriptor ownership, measured** (`io/behaviour.txt` D1, C1): a depth-9 path holds exactly 10 descriptors; 50
  rechecks add 0; dropping returns to the baseline; a failing construction leaks 0.
- **Path shape.** Absolute only; NUL and `\` anywhere, empty components (so `//` and a trailing `/`), `.`, `..` and
  staging-prefixed names are refused before any syscall; the component bound is exact (9 opens, 8 refuses; `/` with
  bound 0 opens). Nothing is normalised; `/tmp` (a symlink here) is refused by the OS through `O_NOFOLLOW`.
- **Edge verification.** `recheck` compares the retained root with a fresh `/`, then re-resolves every name **from its
  retained parent** and compares device, inode, directory kind and non-zero link count. That is the right induction
  (current root ≡ retained root; retained parent + name ≡ retained child, for every edge), and construction runs it
  once before returning. It is, as documented, a sequence of samples.

## 3. Evidence
**3.1 Behaviour** (`probes/rust_probe.rs.txt` → `io/behaviour.txt`): leaf renamed away → `Ok(false)`; a new directory at
the name → `Ok(false)`; leaf removed → `Ok(false)`; A→B→A → `Ok(true)` (documented); ancestor `chmod 000` →
`Err(PermissionDenied)`; ancestor swapped for a look-alike tree between retention and the first check → construction
refuses (`InvalidData`). Substitution by a file or symlink → F-1.
**3.2 Privacy** (`probes/compile-boundaries.log`, clients in the parent module): 7/7 rejected — binding literal,
replacing the root, truncating the edges, reaching `open_inner`, `Clone`, `Default`, a forging impl.
**3.3 Mutants** (`probes/mutation.py`, 13, all compiled, baseline green): 7 killed by the owner's tests
(`O_NOFOLLOW`, `O_CLOEXEC`, every-error-is-false, staging prefix, backslash, bound off by one, construction without
recheck). 6 survive: **1 detected by my probe (F-1)**; 5 not observable on this host (N-1, N-5, disclosed).

## 4. Findings
- **F-1 (low–medium) — a name replaced by a file or a symlink is reported as an I/O error, not as "different".**
  Request and README say "missing/different → false; I/O errors remain errors". Measured: a regular file at the leaf
  name → `Err(NotADirectory)`; a symlink at the leaf name **pointing at the very directory that is retained** →
  `Err(NotADirectory)`; an ancestor replaced by a symlink to itself → `Err(NotADirectory)`. Those are definite
  substitutions of a named edge, the central case this type exists for, and they surface in the class a host will
  most naturally treat as "could not observe — retry / unavailable". The owner's test asserts only
  `!matches!(recheck(), Ok(true))`, which accepts either answer, so the classification is unpinned: a mutant mapping
  `ENOTDIR`/`ELOOP` on a named edge to `Ok(false)` passes all 42 tests (my probe sees it). On a retained *directory*
  parent, `ENOTDIR` from `openat(O_DIRECTORY|O_NOFOLLOW)` can only mean "the name exists and is not a directory (or is
  a symlink)" — macOS reports both as `ENOTDIR`, Linux reports the symlink as `ELOOP`. Recommend: classify those two
  as `Ok(false)`, keep `EACCES`/`EIO`/`EMFILE`/… as errors, and assert the exact result per replacement kind. If the
  owner prefers to keep them as errors, say so in the doc comment and pin *that*, because 164 will branch on it.
- **N-1 (note) — the link-count test is inert on this filesystem.** After `rmdir`, the retained directory still
  reports `nlink = 2` on APFS (R7); removal is detected by the name lookup instead. The check matters where inode
  numbers are reused and removed directories report 0 (Linux ext4); APFS does not reuse inode numbers. Keep it, but it
  is unexecuted everywhere so far — consistent with "Linux not executed".
- **N-2 (note, for consumer 164) — a name is not an identity on this volume.** `Café`, `CAFÉ` and the NFD spelling
  `Cafe◌́` are three byte-distinct paths; all three open, all three are the *same* directory (dev/ino) and all three
  recheck `true`. "Native bytes reach the OS unchanged" is true and means the binding retains the *caller's* spelling.
  Any consumer that compares locations (the 149 N-2 obligation: journal / witness / floor must be related) has to
  compare retained identities, never path strings.
- **N-3 (note, functional limit) — every ancestor must be *readable*, not just searchable.** With an ancestor at mode
  0311, ordinary resolution of the leaf works, but `open` fails `PermissionDenied` because directories are opened
  `O_RDONLY`. macOS `O_SEARCH` / Linux `O_PATH|O_DIRECTORY` would bind without read permission; if `O_RDONLY` is kept
  deliberately (the leaf must be readable anyway), state that search-only ancestors are unsupported.
- **N-4 (note)** `RetainedDirectoryPath` is `pub` and re-exported from the platform crate — a public facade addition,
  unlike the private security/storage candidates of this series. It exposes only `open`, `directory`, `recheck`; I
  mention it so it is a decision rather than an accident.
- **N-5 (disclosed, not observable here)** Removing the root comparison, the device comparison or `is_dir` from
  `same()` survives both suites: they need a changed process root, a cross-device inode collision, or a non-directory
  behind a `RetainedDirectory` (excluded by that type's own invariant). The README already says device/root
  comparisons were inspected, not qualified. One of my mutants ("walk the reopened chain") was a no-op edit — my slip.

No memory-safety or descriptor-ownership defect found.

## 5. Bounded verdict
**161: reviewed, no blocking finding. The unsafe surface is one `openat` whose result is owned on the next line;
descriptor accounting is exact (depth + 1 held, none added by rechecks, none leaked on failure); path shape is strict
and unnormalised; every named edge is re-resolved from its retained parent; the type cannot be forged, edited, cloned
or hooked from outside (7/7). F-1: substitution of a named edge by a file or symlink comes back as `Err(NotADirectory)`
rather than `Ok(false)`, contrary to the stated "different → false", and the owner's test accepts either — decide and
pin it before 164 consumes it. N-2: on this case- and normalisation-insensitive volume three byte-distinct names bind
the same directory, so consumers must compare identities, not strings.** Not exclusion, not custody, not 124 F-1
closure, not Linux, not approval of any consumer or cumulative standing.

Evidence (`claude-out/`): `pin-verification.json`, `pins.py` → `product-pins.json`, `diffs/`, `owner/`,
`probes/{rust_probe.rs.txt, mutation.py, mutation.json, mutation.log, compile-boundaries.json/.log}`,
`io/behaviour.txt`, `hashes.txt`.
