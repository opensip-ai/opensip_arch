# Independent review — frozen `retained-marker-checkpoint-205`

Reviewer: Claude (independent; Codex remains owner). Date 2026-09-19. Review dir: this directory only.
Scope: the frozen 205 product bytes — correction of my 202 W-1 (public mechanism returns bytes without the descriptor) and W-2 (unpinned marker name). Still data-only: no policy, exclusion, native qualification, lease or admitted store is claimed, and a `Present` observation can still carry unsafe permissions until a caller applies policy. Root's 203 draft is not part of this. No selection, installation or cumulative approval.

## 1. Identity verified
| Item | Result |
|---|---|
| `subject.tar.xz` | SHA-256 `8488fb7800ef32d23f39cd606e255a849924807fa2a4c32fe76576b2466d588a`, 4,278,296 B = request = `archive-pin.json` |
| Members | 422, all regular/safe, verified from the tar before extraction; re-verified at the end |
| Product pins | 354/354, none unpinned |
| Parent | equals **my own verified 204 extraction**; five changed: `security/lib.rs`, `security/journal_store.rs`, `…/bound_operational.rs`, `security/custody.rs` (tests only), `storage/store_root.rs`; none added/removed |
| Host receipt 127 | 234 sources all equal product pins; no failed command |

## 2. Owner checks re-run (fresh scratch, offline, locked)
storage 91/91, security 161/161, strict workspace Clippy clean.

## 3. What changed (all diffs read in full)
- `capture_operational_retained` is the former checked capture with the same sequence — leaf/bound validation → `check` → open → **`check` even when open failed** → classify (`NotFound` ⇒ `Ok(None)`, other ⇒ `Io`) → bounded read through `&mut reader` → `check` → result — now returning `Ok(Some((reader, bytes)))`. The old bytes-only function is a thin wrapper that drops the reader: **existing internal users get no new value and no new authority**. `?` replaces the explicit early returns with identical order (the owner's Clippy-r1 failure and correction are preserved). On every error path the reader is a local and is dropped — no descriptor escapes on refusal. An impossible `Absent` from the bounded reader maps to `Context` (refusal), not to absence.
- Public surface: `OperationalFileObservation::{Absent, Present(ObservedOperationalFile), Unreadable}`; `ObservedOperationalFile` has private fields and `file()`, `bytes()`, `into_parts()`. Doc comments state what the handle does *not* establish (current linkage, name binding, exclusion, local-filesystem qualification, lease).
- `store_root.rs`: pure `DecodedMarker` + `CapturedMarker { marker, file }`; on a codec refusal the descriptor is dropped with the bytes. `assert_eq!(MARKER_NAME, "store-instance.v1")` added.
- New tests: inner-function hook replacing the leaf between the read and the last check (retained descriptor keeps the original `dev/ino`, bytes are the original's); a custody test applying 198/200's `inspect_operational_file` to `captured.file()` while the *original* object is made world-writable, hard-linked, then unlinked (`OthersWrite`, `HardLinked`, `Unlinked`) and a clean replacement at the same name stays admissible — i.e. exactly the refusals a reopen-by-name would have hidden.

## 4. Closure of 202
| 202 | Status |
|---|---|
| W-1 descriptor not returned | **closed in design and in the mechanism**: the predicate can now be applied to the object that supplied the bytes; demonstrated by the custody test. See T-1 for how far the *tests* pin it |
| W-2 marker name unpinned | **closed**: my 202 survivor (name changed to `.v2`) is now **killed** by the literal assertion. The single-owner wiring to `StoreNames::marker_relative` is correctly left for the first `lifecycle→storage` caller |

## 5. Findings

### T-1 (medium as a test gap) — "no reopen by name" is pinned only in the innermost function; three outer layers can reopen undetected
Mutants, all compiled (`io/mutation205.json`):

| Mutant | Result |
|---|---|
| marker name drift (202 W-2) | killed |
| after-read chain check omitted | killed (3 tests) |
| after-open chain check omitted (ENOENT → Absent under a moved parent) | killed |
| **public `observe_bound_operational_file` returns a descriptor reopened by name** | **survived** 161 + 91 |
| **`capture_bound_operational_file` wrapper reopens by name** | **survived** |
| **`observe_marker` keeps a reopened descriptor instead of the capture's** | **survived** |

Why: the hook that swaps the leaf *during* the capture exists only for `capture_inner_retained`; every test at the public and marker layers replaces the leaf **after** the call returns, when a reopen has already found the same inode. So the property 205 exists to provide is carried, at the three layers a caller actually uses, by reading the code. (The owner's "reopen after read" mutant was evidently placed inside the inner function, where the hook sees it.)
A deterministic public-layer oracle exists and needs no hook (`probes/offset205_probe.rs.txt` → `io/offset205.txt`): **the descriptor that performed the read has its offset at the end; a reopened one is at 0.** Frozen 205: `bytes 17, offset 17`. Under the lib.rs-layer and wrapper-layer reopen mutants: `offset 0`. One assertion — `file.stream_position() == bytes.len()` on a non-empty file — in the public test and in the marker test kills all three. (It relies on the bounded reader consuming to EOF, which it must to detect `Bound`; say so beside the assertion.)

### N-1 — the predicate is still private to the security crate
`inspect_operational_file` has no `pub`; today only code inside `opensip-security` can join descriptor and policy (as the new custody test does). That is consistent with "future host can apply…", but the first storage-side caller will need either a public predicate entry point or a security-side "observe + policy" function. Prefer the latter: it keeps uid/group provenance handling in one crate and avoids a caller forgetting the join — a `Present` that has not been through policy is, as the README says, possibly unsafe.

### N-2 — what a retained `File` lets a caller do
`file()` hands out `&File`, through which a caller can `read`/`seek` (shared offset) and `into_parts()` transfers ownership with no lifetime tie to any lease. Both are inherent in "data-only", and the docs say the handle is not authority. Worth one sentence that `bytes()` is the evidence and the descriptor is for *metadata policy only* — re-reading through it is an unbracketed read that none of the three chain checks cover.

### N-3 — undecodable markers cannot be policy-inspected
On a codec refusal the descriptor is dropped. Correct for now (nothing admits an unavailable marker); a future diagnostic wanting "who could have written these bad bytes" would need it. Not a request.

## 6. Limits and disclosure
macOS, unprivileged. Mutants and probes only in `build205-*`/`target205-*` scratch copies created after asserting absence, restored from frozen bytes; nothing deleted; no compile failure occurred. Host isolation not re-run (receipt verified against pins). In-place writers and concurrent replacement beyond the owner's hook test were not probed; the README disclaims a snapshot against in-place writes.

## 7. Verdict (bounded)
**205 closes 202 W-1 and W-2: the shared mechanism now returns the very descriptor it read, with unchanged check order, no descriptor escaping on any refusal, and no new value or authority for the existing bytes-only users; the custody test shows the three refusals a reopen would have hidden; the marker name is pinned. The remaining gap is evidential (T-1): a reopen-by-name at the public function, the wrapper or the marker observer survives the whole suite, because only the inner function has a mid-capture hook. A one-line offset assertion at the public layer closes it deterministically.** No approval of policy integration, admission, leases, installation or cumulative readiness.
