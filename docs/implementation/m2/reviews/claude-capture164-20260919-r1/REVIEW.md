# Independent bounded review — named operational capture 164 (Rust)

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-19.
Request: received as a chat message (`claude-out/REQUEST-as-read.md`); subject README read. Scope: the delta of frozen
`bound-operational-capture-checkpoint-164` over frozen 163 — new `journal_store/bound_operational.rs`; the common
bounded reader in `journal_store.rs` generalised over a check closure; `FileSource` now requires
`RetainedDirectoryPath`; the 161 F-1 correction in `path_binding.rs`; fixture construction in two other files. **Not**
exclusion, ABA protection, owner/ACL admission, SQLite path binding, a host mapper, or 124 F-1 / 118 I-2 closure; I
infer none. No frozen/selected/product edit; scratch only, `-I -B`, dedicated targets; no commit, push or delegation; no
cumulative approval.

## 1. Subject verification (before use)
| Item | Value |
|---|---|
| `subject.tar.xz` | 8,505,876 bytes, SHA-256 `515222bb5a564f095b1b6c2fb7b06a612d151303b32c99f92ca6bf1845a57db7` = request = `archive-pin.json` |
| Members | 442/442 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified at the end |
| Product pins | 344/344; none unpinned |
| Parent | `parent-inputs.json` = **my own** verified 163 extraction (343/343); 338 unchanged, 5 changed, 1 added |
| Host pins | host101 receipt: 224 sources all equal the product pins; no command failed |
| Owner checks, fresh scratch | 126/126 security + 42/42 platform tests; strict workspace Clippy clean |

The README's disclosed count correction (352 → 355, reporting only) does not touch any pinned byte I verified.

## 2. What changed (read in full)
`capture_operational_checked(parent, leaf, max, open, check)` is the old reader with its three
`linked_operational_parent` calls replaced by a caller-supplied `check`; the descriptor-only entry passes the old
immediate-parent check, the new bound entry passes `binding.recheck()` mapped as `true → ok`, `false → Context`,
`Err → Io`. Order is unchanged and right: grammar → **check** → open → **check (also when the open failed, before
`ENOENT` may mean Absent)** → bounded read → **check**. The bracket's four reads all call the bound entry, and
`FileSource.parent` is `&RetainedDirectoryPath`, so the adapter cannot be handed the weaker type. In the platform,
`ENOTDIR`/`ELOOP` on a named edge now return `Ok(false)`; the test asserts `!recheck().unwrap()` per replacement kind.

## 3. Evidence
**3.1 Every change kind × every phase × three file states** (`probes/rust_probe.rs.txt` → `io/phases.txt`, real
renames through the private sequencing hook; 57 rows):
- leaf directory renamed with a look-alike holding **new bytes**, ancestor renamed with a look-alike **tree**, leaf
  directory replaced by a **symlink to the retained directory** — at before-open, after-open and after-read, for a
  present, an empty and an absent file: always `Unreadable(Context)`; never the old bytes, never the new bytes, **never
  `Absent`** (for the absent file, the relocation at after-open is caught before `ENOENT` is interpreted);
- ancestor `chmod 000` at any phase → `Unreadable(Io PermissionDenied)` — an error, not a name change;
- the *file* replaced by rename while the chain is untouched → before-open: the new bytes; later: the bytes of the
  descriptor already open — ordinary replacement semantics, no false refusal;
- A→B→A inside one hook → accepted, as documented;
- bound = size → `Present`; size − 1 → `Bound`; 0 → `Context`; leaf symlink → `Io(FilesystemLoop)`; leaf directory →
  `Io`; `../witness` and empty leaf → `Context`.
An absent file is decided after two checks (nothing is read afterwards), so there is no third check in that case —
consistent with the law.

**3.2 Mutants** (`probes/mutation.py`, 11, all compiled, baseline green; complementary to the owner's ten): absence
interpreted before the post-open check; post-open check only when the open succeeded; no check after the read; no
check before the open; changed chain tolerated; recheck errors flattened to `Context`; recheck errors tolerated; name
chain consulted at one check only; `ENOTDIR` no longer a substitution; `EACCES` classified as substitution — **10/10
killed by the owner's tests**. One survives both suites: `ELOOP` removed from the substitution set — unobservable on
macOS, which reports a symlink under `O_NOFOLLOW|O_DIRECTORY` as `ENOTDIR` (N-1).

**3.3 Boundaries** (`probes/compile-boundaries.log`): giving the adapter a bare `RetainedDirectory` is a type error
(E0308); the bound reader's hook and phase enum are unreachable from the parent (E0603); a spec cannot outlive its
binding (E0515). Two compile and mark the line (N-2).

## 4. Findings
No defect and no finding of substance.
- **N-1 (note)** The `ELOOP` half of the 161 F-1 correction is unexecuted: it is the Linux spelling of the same
  substitution. Already covered by "Linux unexecuted"; it should be the first thing a Linux lane asserts.
- **N-2 (note, module-internal surface)** Inside `journal_store` the common reader accepts *any* check closure
  (an always-`Ok` one compiles), and the descriptor-only `capture_operational_bytes` remains callable with its
  caller-custody contract. Both are private to the module and the bracket adapter is closed by type, so this is not a
  hole — but the guarantee "every witness/floor read is name-checked" is a property of the *adapter*, not of the
  reader. A future second consumer inside this module must go through `capture_bound_operational_bytes`.
- **N-3 (note, carried from 161 N-2, now visible at the leaf)** `WITNESS` reads the same file as `witness` on this
  volume. The source comment says leaves are fixed lower-case constants chosen by the caller; keep them constants.
- **N-4 (note, cost)** Each bound read performs three full root-to-leaf re-resolutions (depth + 1 opens each); a
  bracketed capture therefore does twelve. Correct and bounded by the caller's component cap; worth knowing before this
  sits on a hot path.
- Carried and correctly still open: no relation between the journal's location and the two file bindings (149 N-2 —
  SQLite path binding is explicitly not claimed), A→B→A, exclusion through consumption, 150 F-2 host mapping.

## 5. Closure of my 161 items
| Item | Status |
|---|---|
| **F-1** file/symlink substitution reported as an I/O error | **Closed** on this platform — `Ok(false)`, exact per-kind assertions, permission errors remain `Err`; consumer maps `false → Context`, `Err → Io` (pinned by two mutants) |
| **N-2**, **N-3**, **N-4** | documented accurately in the type's doc comment and README |
| **N-1**, **N-5** | unchanged, disclosed |

## 6. Bounded verdict
**164: reviewed, no finding of substance. All four witness/floor reads of the bracket go through one bounded reader
that re-resolves the complete retained name chain before the open, after the open even when it failed, and after the
read; across 57 real-rename scenarios a relocated or substituted leaf or ancestor is always `Unreadable(Context)` —
never stale bytes, never a look-alike's bytes, never `Absent` — while permission failures stay I/O errors and ordinary
file replacement still reads normally; the adapter cannot be given the weaker descriptor type; 10 of my 11 mutants are
killed by the owner's tests and the eleventh is the Linux-only `ELOOP` arm.** Not exclusion, not ABA protection, not
SQLite path binding, not custody, not 124 F-1 closure, not Linux, and not any cumulative standing.

Evidence (`claude-out/`): `pin-verification.json`, `pins.py` → `product-pins.json`, `diffs/`, `owner/`,
`probes/{rust_probe.rs.txt, mutation.py, mutation.json, mutation.log, compile-boundaries.json/.log}`, `io/phases.txt`,
`hashes.txt`.
