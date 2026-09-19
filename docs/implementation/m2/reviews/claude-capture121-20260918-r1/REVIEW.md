# Independent bounded review — operational byte capture 121 (Rust)

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-18.
Request: `REQUEST.md`. Scope: the private `capture_operational_bytes` added to
`crates/security/src/journal_store.rs` in frozen `operational-capture-checkpoint-121` — the *presence
and owned-bytes* part of 118 I-2 only. Not root custody, hard links, cross-file or SQLite coherence,
generation/association logic, OS qualification, or 119 I-1/I-2/R-3. No frozen/selected/product edit;
scratch builds with dedicated target directories; no commit, push or delegation.

## 1. Subject verification (before extraction)

| Item | Value |
|---|---|
| `subject.tar.xz` | 4,088,924 bytes, SHA-256 `4fd501344377e5c1859051ce3c6ca76558f0f253b3a9876f2e43e794d236f10c` = request and `archive-pin.json` |
| Members | 394/394 regular, each length + SHA-256 equal to the manifest from the tar; 0 unsafe/extra; re-verified clean afterwards |
| Product pins | 330/330 equal; none unpinned |
| Parent | `parent-inputs.json` equals **my own** verified 119 extraction; 329 unchanged |
| Changed | `crates/security/src/journal_store.rs` `70a78536…7a55`, +204 / −0 (one function, two enums, three tests) |

## 2. What it does (read in full, with `RetainedDirectory::open_regular`)
Context refusals first (`leaf` empty, `.`/`..`, any `/`, `\`, NUL, the `.opensip-stage-` prefix;
`max_bytes` 0 or above `metadata::MAX_BYTES`) → `Unreadable(Context)`. Then one
`openat(parent_fd, leaf, O_RDONLY|O_CLOEXEC|O_NOFOLLOW|O_NONBLOCK)` through the existing public API,
which also requires a regular file. **Only `ErrorKind::NotFound` from that open is `Absent`**; every other
open error is `Unreadable(Io)`. Then `take(max+1).read_to_end`: any read error → `Unreadable(Io)`;
more than `max` → `Unreadable(Bound)`; otherwise `Present(owned Vec)`. No size metadata is trusted; no
codec is called; empty is `Present`.

## 3. Evidence
Scratch build: security **71 passed / 0 failed**.

**Real-filesystem presence probe** (`probes/presence.txt`, APFS, non-root):

| Situation | Observation |
|---|---|
| leaf mode 000 | `Unreadable(Io EACCES)` |
| parent mode 000 after retention — leaf exists / does **not** exist | `Unreadable(Io EACCES)` in both: absence is not claimed when it cannot be observed |
| 300-byte leaf name | `Unreadable(Io ENAMETOOLONG)` |
| FIFO leaf | `Unreadable(Io InvalidInput)`, returns immediately (`O_NONBLOCK`) |
| 1 TiB sparse file, limit 4096 | `Unreadable(Bound)` after reading 4,097 bytes |
| exactly 4096 bytes | `Present(4096)` |
| limit 0 / limit MAX+1 / staging-prefix leaf | `Unreadable(Context)` ×3 |
| leaf `WITNESS` when only `witness` exists | `Present` (case-insensitive volume) |
| **retained parent directory unlinked, a new directory with a valid witness created at the same path** | **`Absent`** |

**Mutation** (12 mutants, all compiled, baseline green): **10 killed** — every failure mapped to Absent;
InvalidInput mapped to Absent; empty bytes reported Absent; read limit without `+1` (silent truncation to
`Present`); bound off by one; bound check removed; both `max_bytes` context checks; nested leaf; staging
prefix. **2 survived**: `PermissionDenied` also mapped to Absent, and a read error returning the partial
bytes as `Present` (the second is the gap the owner disclosed).

## 4. Findings

- **F-1 (medium) — an unlinked retained parent is reported as `Absent`.** `openat` on a directory that
  has been removed returns `ENOENT` for every name, so the function's one absence signal cannot tell
  "this file is not in the custody directory" from "the custody directory no longer exists". In the
  probe a valid witness sits at the very path the caller believes it is reading, and the observation is
  `Absent`. This matters more than an ordinary misclassification because of where `Absent` goes: the
  writer dispatcher turns definite absence over a non-empty journal into a **durable
  `witnesslessRestore` marker**, and on the read-only side absence is *stable* across both captures, so
  Step 4's stability gate does not save it. The request rightly leaves parent custody to the caller, but
  this one is observable from inside the capture at no cost: a retained directory whose link count is 0
  is a context failure. `RetainedDirectory` wraps the `File`, so it needs either a small public method
  (e.g. `is_linked()` from `fstat`) checked before and after the leaf open, or `open_regular` returning a
  distinguishable error. Until then the caller obligation must say "and has verified the retained
  directory is still linked", which no caller can do without that method.
- **F-2 (low, tests) — the two survivors.** A `chmod 000` case kills the permission mutant (expected
  value differs when tests run as root; say so). For the partial read, a seam is enough and needs no
  `unsafe`: move the bounded read into `fn read_bounded(reader: impl Read, max)`. I built that in scratch
  only (`probes/seam_demo.py`): the frozen behaviour is unchanged, a reader that yields 21 bytes and then
  fails is `Unreadable(Io)`, and **both surviving mutants are killed** by one eleven-line test.
- **F-3 (note) — case-insensitive volumes.** `WITNESS` opens `witness`. Harmless while leaf names are
  fixed lowercase constants chosen by the caller; it becomes a collision question only if a leaf is ever
  derived from data. Worth one line beside the leaf rules.
- **F-4 (note) — disclosed limits I agree with**: not a snapshot of in-place writers (publish by
  replacement is a precondition); no cross-file or SQLite coherence; `O_NOFOLLOW` covers the leaf only,
  the parent's own custody is the caller's; hard links are not examined.

## 5. Codec separation and ownership
`Present(vec![])` reaches the 109 codec and is `Decode` there (owner test; consistent with my 109
addendum: a present empty file is malformed, never absent). The returned bytes are an owned `Vec`; the
owner's "new inode at the same leaf" test shows an earlier capture is unaffected by a later
replacement. Nothing in this function produces `Absent` from content.

## 6. Bounded verdict
**Capture 121: reviewed; the presence/owned-bytes rules are right and well tested (10 of 12 mutants
killed), with one finding to fix before anything consumes `Absent` — F-1, an unlinked retained parent
reads as absence — and F-2 as a small test follow-up.** This closes only the presence part of 118 I-2;
it is not approval of custody, coherence, callers, or any cumulative, OS or target qualification.

Evidence: `claude-out/pin-verification.json`, `product-pins.json`, `journal_store.diff`,
`probes/rust_probe.rs.txt`, `presence.txt` (+ `presence.FAILED-r1.txt`), `mutation.{py,json,log}`,
`seam_demo.py`, `seam-demo.json`, `hashes.txt`.
