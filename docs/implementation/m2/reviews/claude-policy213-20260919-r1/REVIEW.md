# Independent review — frozen `policy-capture-checkpoint-213`

Reviewer: Claude (independent; Codex remains owner). Date 2026-09-19. Review dir: this directory only.
Scope: the frozen 213 product bytes — a **fixed composition mechanism** in the security crate: full root-to-parent directory policy, bounded retained capture, and file policy on the exact retained descriptor, with typed causes and a privately constructed `Present`. UID/groups remain asserted; no host grant, lease, continuous custody, ABA or native-qualification claim; no store admission. The existing unchecked `storage::observe_marker` is unchanged and is *not* an admission path; the first host consumer is still owed. Scoped mechanism review, not cumulative approval.

## 1. Identity verified
| Item | Result |
|---|---|
| `subject.tar.xz` | SHA-256 `ffa7c6ef50f15d9c7a46b02ff7a261a92f9d9eeaeb1b4f2df2c4220fba6b99b1`, 4,248,144 B = request = `archive-pin.json` |
| Members | 422, all regular/safe, verified from the tar before extraction; re-verified at the end |
| Product pins | 355/355, none unpinned |
| Parent | equals **my own verified 211 extraction**; two changed: `security/lib.rs`, `security/custody.rs` |
| Host receipt 129 | 235 sources all equal product pins; no failed command |

## 2. Owner checks re-run (fresh scratch, offline, locked)
security 171/171, storage 92/92 (unchanged crate), strict workspace Clippy clean.

## 3. What the bytes do (read in full)
- `custody.rs`: two visibility changes only (`pub enum DirectoryPathRefusal`, `pub(crate) fn inspect_directory_path`); no predicate token changed.
- `lib.rs`: `observe_bound_operational_file_with_policy(parent, leaf, max_bytes, uid, groups)` calls the private `policy_capture_sequence` with three **fixed** closures — `custody::inspect_directory_path`, `observe_bound_operational_file`, `inspect_operational_file_policy`; the public signature offers no way to substitute a mechanism, a scope or a waiver.
- **Order and precedence:** `directories → read → directories → [Absent | Read failure | file policy → directories → File failure | Present]`. A directory failure at any of the three points **dominates** whatever the lower layer returned; `Absent` is reported only after the post-read directory sample passes; a file-policy refusal is reported only after the final directory sample passes, and that final sample runs *even when the file policy refused*. The directory closure is `FnMut` and re-observes the real chain each time.
- **Same reader:** file policy is applied to `captured.file()` — the descriptor 205/207 showed to be the one that was read; no reopen.
- **Types:** `PolicyCaptureFailure::{Directory, Read, File}` keeps the three causes distinct, each wrapping the existing typed diagnostic; `PolicyObservedOperationalFile` has private fields and **no public constructor**, exposing only `captured()` (by reference, so `into_parts` cannot be reached) and `descriptor()`. A `Present` of this type can only come out of the fixed sequence — that is the type-level form of what I asked for in 210 N-1, for the mechanism.

## 4. Independent checks
**Mutation** (12 mutants, all compiled; `io/mutation213.json`):

| Mutant | Result |
|---|---|
| directory policy before the capture omitted | killed |
| directory policy after the read omitted (absence / read result interpreted under an unchecked chain) | killed |
| final directory policy after the file sample omitted | killed |
| file-policy refusal returned *before* the final directory sample | killed |
| file-policy refusal still yields a non-refusal | killed |
| read failure reported as `Absent` | killed |
| directory failure reported as `Absent` | killed |
| public fn: directory mechanism replaced by `Ok(())` | killed (real unsafe-ancestor negative) |
| public fn: capture reads under a different bound | killed |
| **public fn: file policy replaced by a bare descriptor observation** | **survived** |
| **public fn: file policy evaluated for uid 0 instead of the supplied actor** | **survived** |
| **public fn: directory policy evaluated with widened groups instead of the supplied set** | **survived** |

So precedence, order and cause propagation are completely pinned by the private callback tests; what is *not* pinned is that the public function wires the **real file-policy mechanism with the caller's actor inputs**.

**Real-filesystem probe through the public function** (`probes/public213_probe.rs.txt`, scratch; fixture under `std::env::temp_dir()`, which on macOS is `/private/var/folders/…/T` — a chain with no group/other-writable component, owned root…root, user, user; `/private/tmp` would not do, it is 1777):

| Case (frozen 213) | Result |
|---|---|
| own file 0600, real uid | `Present(17 bytes, mode 600)` |
| own file 0602 | `Unavailable(File(Predicate(OthersWrite)))` |
| own file 0620, group not authorized / authorized | `File(Predicate(GroupWrite))` / `Present` |
| asserted uid = real uid + 1 | `Unavailable(Directory(Predicate{component: 5, ForeignOwner}))` — directory cause dominates, as designed |
| absent leaf | `Absent` |
| leaf directory 0770, group not authorized / authorized | `Directory(Predicate{component: 7, GroupWrite})` / `Present` |

The same probe under the three survivors (`io/public213.txt`, `io/public213_groupdir.txt`): *bare observation* → 0602 and unauthorized 0620 become `Present`; *uid 0* → the own-file positive becomes `File(ForeignOwner)`; *widened groups* → the 0770 directory becomes `Present`. **Each survivor is distinguishable by a deterministic test on this host.**

## 5. Findings

### T-1 (medium as a test gap) — the public function's file-policy wiring and actor inputs are unpinned
Three behavioural mutants at the public layer survive 171 tests (above). The owner's real tests are an absence/unsafe-ancestor pair and a read-only system file (`/etc/hosts`): the system file is root-owned, mode 0644, single link, so it passes *any* file policy for *any* uid — it cannot tell the real predicate from none, nor the supplied uid from 0. The directory negative kills the directory-mechanism mutant but uses no group-writable component, so group handling is untested there too. The README says the callback seam tests "only order/causes"; agreed — and the consequence is that the claim "Public function fixes actual mechanisms" is carried for the file leg by reading the three lines at l.137–141. The per-user temp directory gives a passing chain for an unprivileged test, so the fix is the six-line table in §4 as a permanent test (own-file positive; 0602; 0620 ± group; 0770 directory ± group). No system file contents are involved.

### W-1 (low) — is the private `Present` claim too strong? One thing to tighten in words
The type is sound: it cannot be built outside the sequence. What it *means* is "at three instants the chain passed and at one instant, after the read, the descriptor passed". Two readings a consumer might wrongly make, both already disclaimed in the doc comment but worth putting on the **type** (where a consumer will look) rather than only on the function:
1. *the bytes were read from a policy-conforming file* — not established: the file sample follows the read, so the mode/owner/links at read time are unknown (a file that was world-writable while read and tightened afterwards is `Present`). The struct doc says "the file-policy sample performed **after** that read" — good; it should add that this does not characterise the file *during* the read, and that only caller-held exclusion can.
2. *the directory samples are retained* — they are not: `inspect_directory_path(...).map(|_| ())` discards the chain observations, so `Present` carries the file's `DescriptorObservation` but nothing about which directories were sampled or what they looked like. Fine for a mechanism; a future diagnostic/audit consumer will want them, and adding them later changes the type — cheaper to decide now.
Neither is a defect in 213.

### Notes
- **N-1 (210 N-1 status)** closed **for the mechanism**: a policy-sampled capture is now a distinct, unforgeable type. It is not yet closed for storage: `observe_marker` still returns the unchecked `CapturedMarker`, and the README says so ("must not be used as admission"). The first host consumer should take `PolicyObservedOperationalFile` (or a storage wrapper built only from it), at which point the unchecked path can become test-only.
- **N-2** cause precedence is a choice worth stating once in the doc: when *both* a directory and a file refuse, the caller learns only `Directory`. That is the safe direction (a lower-layer result under an unadmitted chain means nothing) and the tests pin it; it does mean a diagnostic may hide a simultaneous file problem until the chain is fixed.
- **N-3** `DirectoryPathPolicyFailure::Predicate{component, refusal}` exposes a component *index*, not a name — appropriate for a workspace diagnostic (no path disclosure); the host mapper will need the retained path to render it.
- **N-4** three full chain observations per capture (each re-`stat`s every component and reads ACLs) is the honest cost of bracketing; no caching is attempted, correctly.

## 6. Limits and disclosure
macOS, unprivileged, APFS. Mutants and probes only in `build213-*`/`target213-*` scratch copies created after asserting absence, restored from frozen bytes; nothing deleted; no compile failure occurred. My probe fixtures were created and removed under the per-user temp directory by the probe itself. ACL-bearing components, Linux, and concurrent mutation between samples were not exercised (the latter is explicitly disclaimed by the owner). Host isolation not re-run (receipt verified against pins).

## 7. Verdict (bounded)
**213 is a correct fixed composition: directory policy brackets the capture three times and dominates every lower-layer result, absence is reported only under a passing chain, file policy runs on the exact retained descriptor and its refusal is still bracketed, the three causes stay typed and distinct, and `Present` cannot be constructed outside the sequence. Nine of twelve mutants are killed; the three survivors (T-1) show that the public function's file-policy mechanism and its uid/group inputs are verified only by reading, because the real positive uses a root-owned system file that passes any policy — a deterministic test in the per-user temp directory distinguishes all three. W-1 asks that the type's documentation say what the after-read sample does not establish.** No approval of actor provenance, exclusion, leases, store admission, installation or cumulative readiness.
