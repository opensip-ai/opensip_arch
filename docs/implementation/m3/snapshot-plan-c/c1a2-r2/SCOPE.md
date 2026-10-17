# C1a2 r2: candidate blob custody and the capture session (M3-C r8 item 1)

**Lead scope record, 2026-10-16. Unreviewed candidate, round 2.** Round 2 answers Codex `codex-c1a2-r1` (REQUIRED-FINDINGS: four RFs, one NBO). The r1 package (`../c1a2-r1/`) is history.

## r2 changes

| Finding | Change | Controls |
| --- | --- | --- |
| **RF-1** (mode and owner alone are not private custody) | `CandidateCustody::new` no longer judges the directory itself. It calls security's new `snapshot_source::admit_custody_directory`, which takes one charged ACL capture of the retained descriptor (`descriptor_acl_capture_cost`, 1 object, 131 edges, 7,940 bytes) and applies the existing private-descendant predicate (`private_access::observe_private_directory`): a 0700 directory of the invoking user whose present ACL grants no right to anyone else, inherit-only entries included. An omitted ACL or the NOACL sentinel is `AclUnavailable`, distinct from a foreign grant (`ForeignAccess`) and from a wrong mode or owner (`NotPrivate`). Because no inheritable grant can pass the admission, no custody file inherits one. That is the premise LD-C1A-9 rests on. The invoking user's own processes and root are outside what any custody check excludes, as for every other private custody in the product. | `mode_and_owner_alone_do_not_admit_custody_and_foreign_acl_grants_refuse`: a bare 0700 directory refuses `AclUnavailable`; a named `group:everyone` grant and an inherit-only one each refuse `ForeignAccess` on a directory that was admitted before the grant. The mutation `custody-directory-not-private` now skips the admission. The model's `model-acl-capture-free`. |
| **RF-2** (unbounded write attempts) | `PendingBlob::write` makes one charged `write` call per chunk, as the platform's positioned writes do: a short write refuses `ShortWrite`, and any error, `Interrupted` included, refuses `Write`. Nothing retries, so the ledger's one `WRITE` edge per chunk bounds the native write calls, and the model's write term is exact. The chunk is hashed only after it is wholly written. A test seam injects a failure or a short count for the next attempt. | `an_interrupted_or_short_write_refuses_without_a_retry`: each refuses after exactly one charged edge. The mutation `write-retried-uncharged` retries the interrupted attempt. |
| **RF-3** (uncharged path copies on refusals) | `read_once` consumes the `SourceFile`. Every refusal, and the capture's key, takes the source's own path by move (`source.into_parts().0`); that path was charged when the source was made. No refusal copies a path. Custody's errors carry native errors (`Create(io::Error)`, `PendingExists`), never a formatted string. | `every_session_and_custody_allocation_is_at_a_charged_site`: a lexical pin of every allocation spelling in both modules' production code, each at its charged site (the buffer, the pending name, the two digest names), with the seven moves counted and the one copy being the test-only read-pass spy's. The mutation `refusal-path-copied` copies one refusal's path. |
| **RF-4** (`let _ =` in tests) | The four cleanup bindings are gone. Each `Drop` now checks its removal (and the chmod's status) unless the test is already failing. | The lane's operability census. |
| **NBO-1** (the source pin's scope) | Kept bounded: the pin covers the preparatory modules only. B2's and C2's reads through the session, and their half of the pin, remain J1's (Not delivered). | — |

It implements C1a2 of the C1a plan: r4 is accepted (Codex `codex-c1a-plan-r4`), amended by r5 and r6, and r6 is accepted (Codex `codex-c1a-plan-r6`). Under r6, C1a2 is **preparatory library and model work**:
- no `snapshot_profile`, and no production snapshot-ledger claim;
- no production caller;
- no census-closure file changed.

It completes the charge model with the read, retention and custody terms, which r9's term (a) needs. It carries C1A1-R1-NBO-1's obligation: the route controls C1A-T2 and C1A-T3.

**Base:** product main `56d0eb5` (inventory v214, 173 contract successors), with C1a1 integrated (`ac72a33`).

## What it changes

| File | Change |
| --- | --- |
| `crates/platform/src/custody_entry.rs` (new) | **The custody entry primitives.**<br>• `rename_exclusive_accounted(from, to)` uses `renameatx_np(RENAME_EXCL)` (`renameat2(RENAME_NOREPLACE)` on Linux). It never replaces anything at `to` and has no overwriting fallback. A raw `EEXIST` is `EntryExists`.<br>• `unlink_entry_accounted(name)` unlinks a non-directory entry.<br>• Both act inside one retained directory, take single-component names only, and charge their published costs (`rename_exclusive_cost`, `unlink_entry_cost`) before the name copy or the call.<br>It is a new file declared in platform's `lib.rs`. `filesystem.rs`, a census-closure file, is unchanged. |
| `crates/platform/src/custody_entry_tests.rs` (new) | 2 tests. Its cleanup checks its removal (r2). |
| `crates/platform/src/lib.rs` | The module (with `allow(unsafe_code)`, as for the other FFI adapters) and its re-exports. |
| `crates/host/src/candidate_custody.rs` (new) | **`CandidateCustody`** over the caller's retained directory (LD-C1A-4). The directory must be admitted private by security's `admit_custody_directory` (r2: mode, owner and ACL) and be empty.<br>**`begin(expected)`** returns a **`PendingBlob`** on a create-exclusive, no-follow `pending-<n>` entry, mode 0600. Its `write(chunk)` is one charged `write` attempt (r2): a short or failed write refuses, and the chunk is then hashed with `RawSha256`; writing past the expected length refuses.<br>**`commit`** checks the written length and the entry's size. A digest already committed is resolved from the in-memory set: the pending entry is unlinked and nothing is re-read (LD-C1A-9). Otherwise the blob is placed under its 64-hex digest name by the exclusive rename.<br>**`open(sha256)`** re-verifies the custody file: regular, mode 0600, the user's, the committed length and the digest, read through the caller's buffer.<br>Every step is charged first. The module never holds or reads a source descriptor. |
| `crates/host/src/candidate_custody_tests.rs` (new) | 8 tests (r2: two new). |
| `crates/host/src/snapshot.rs` (new) | **`CaptureSession`, the one source-read site (C1-T2).**<br>• **One buffer.** One reused 64 KiB buffer, charged once by the bounded reader's growth rule (`work_reader.rs` `next_buffer`: 4 KiB doubling to 64 KiB, every growth charged in full).<br>• **`capture(path, root, custody)`,** the pre-walk capture (B2's and C2's reads), through `SnapshotRoot::open`. A kept capture is returned with no second read.<br>• **`walk(root, custody, extent)`,** the extent walk. Each handed file is read once into custody. A captured path the walk reaches is compared with its capture (device, inode, size, mtime, ctime) and reused, or refused `ChangedSinceCapture` (C1-T24).<br>• **`read_once`:**<br>  – the sample at the read's start must be the observation (`ChangedBeforeRead`);<br>  – each `read` call is one attempt, charged first, within `2·⌈size / 64 KiB⌉ + 2` (`ReadAttemptsExhausted`);<br>  – every chunk goes to the pending blob;<br>  – the sample after EOF must equal the one before, and the length must be the size (`ChangedDuringRead`).<br>  Nothing is retried.<br>• **Results.** `inventory()` gives the reached captures in path byte order, with their side-record origin (`walk`; `read-set` is C1c's). `leftovers()` gives the captures the walk never reached.<br>• **Test seams:** a read-pass spy and a read hook (before the first sample, and before each call, which may inject that call's error). |
| `crates/host/src/snapshot_tests.rs` (new) | 11 tests (r2: the allocation pin) and one ignored lane probe (below). |
| `crates/host/src/snapshot_session_vectors.json` (new) | The model's session predictions for the 35 trees. |
| `crates/host/src/lib.rs` | The two modules (macOS, `allow(dead_code)`: library only, no caller). |
| `crates/security/src/snapshot_source.rs` | `STATUS_COST` and `owned_record`: the discovery walk's prices, exported so the snapshot has one price list. **(r2)** `admit_custody_directory` and `CustodyDirectoryRefusal`, a typed wrapper over `private_access`'s existing private-directory judgment, so the host's custody uses the product's one ACL predicate. Also the route-test module. |
| `crates/security/src/snapshot_route_tests.rs` (new) | The route controls (C1A-T2, C1A-T3). |
| `crates/security/src/scenario.rs` | `with_snapshot_root` and `with_snapshot_root_as`. They take `operation`'s durable snapshot root, with the invocation's custody judgment (by default, or the walk vectors' groups, waiver and foreign user), and lend it to a closure while the lease is held. Both sit inside the existing gated module, so no new feature site is added. |
| `tools/security/snapshot_ledger_model.py` | **The session terms.** Each host and platform charge shape is read by anchor, with its count:<br>• the buffer, the attempt, the write, the custody listing and visits;<br>• the custody admission's ACL capture (r2: anchored at its call, at security's one-capture judgment, and at the host test's price assertion);<br>• the pending name and its creation;<br>• the two read samples and the commit's sample;<br>• the unlink, the digest name, the rename and the committed set's entry;<br>• the capture record. The record sizes are pinned by the host test's own assertions.<br>The custody prices must equal the census's. The session files are pinned whole: the three of r1, and (r2) `crates/security/src/private_access.rs`. For every tree it writes `snapshot_session_vectors.json`, the session's charge beyond the walk's own: the custody's opening (its ACL-judged admission, then its listing), then per handed file its samples, its pending entry, its attempts (one per chunk, plus the EOF read), its chunk writes, the commit, and either the duplicate's unlink or the digest name, rename and set entry, then the capture record. |
| `crates/security/src/snapshot_ledger_vectors.json` | Regenerated: the model pins `snapshot_source.rs` whole. |

## The tests

- **C1-T1 and C1-T3:** each inventory row's custody bytes, read back through `open`'s verification as a recording sink would, are the bytes hashed, and the length is right. Equal bytes share one blob. A rewrite after the session changes nothing custody holds. Every file is read exactly once.
- **C1A-T1:** a path captured before the walk, and requested again, is read once. The walk reaches it, reuses it and marks its origin `walk`.
- **C1-T24:** a capture rewritten before the walk reaches it refuses `ChangedSinceCapture`, with no second read.
- **Leftovers:** a capture under `ignorePaths` is a leftover, never inventoried.
- **Changes:**
  - a file rewritten before its first sample refuses `ChangedBeforeRead`;
  - one that grows during its read refuses `ChangedDuringRead`, and so does one rewritten in place at the same length.
- **The envelope:**
  - interrupted reads are bounded by exactly the envelope's attempts, then refuse `ReadAttemptsExhausted`;
  - an I/O error refuses with that error;
  - the envelope's arithmetic is checked.
- **Pricing:**
  - the buffer's charge is 4 + 8 + 16 + 32 + 64 KiB, once;
  - a 64-chunk payload costs the same objects and bytes as a one-byte one, and exactly 126 more edges (its extra attempts and writes);
  - **the 4 GiB probe** (`#[ignore]`, run by the lane): a sparse 4 GiB file is charged the one-byte file's objects and bytes, plus its 65,535 extra attempts and 65,535 extra writes.
- **The session's charge model:** the native difference between a session walk and a plain walk of the same root must equal the model's prediction exactly. It does on the 32 routed trees. Three trees have no durable route, each refused by X2's own admission for its own reason, and the test pins them: a root `.git` with no tracking observation (`vcs-unsupported`), a root `.opensip` that is a file (`identity-contradiction`), and a root `.opensip/project-id.v1` that is not the marker (`marker-custody`). C1a1's walk control covers their walk terms.
- **C1-T2's source pin:** the session's production code has one source read (`source.file().read(`). The security opener and walk have no read call of any kind. Custody's one read is `open`'s verification of its own file, and custody never names `SourceFile`.
- **(r2) The allocation pin:** every allocation spelling in the session's and custody's production code is at its charged site, and every refusal moves the source's charged path (RF-3).
- **Custody:**
  - a blob is committed under its digest hex, mode 0600, and opened verified;
  - an existing digest is kept, and a duplicate is resolved without a read (the committed file is made unreadable first);
  - a corrupted custody file (digest, length or mode) is refused at open;
  - a length mismatch refuses at the write or the commit;
  - the custody directory must be private, the user's and empty;
  - **(r2)** a bare 0700 directory (no ACL) refuses `AclUnavailable`, and a named or inherit-only grant to another principal refuses `ForeignAccess` (RF-1);
  - **(r2)** an interrupted or short write refuses after one charged attempt, with no retry (RF-2);
  - an uncommitted digest is not opened.
- **The route controls (security):**
  - **C1A-T3:** on one synthetic installation, a read session admits the root and releases. With its snapshot root lent and unwalked, the fence is free, and a writer takes the fence and the APPEND_WRITE lease and hands off the durable operation.
  - **C1A-T2:** both routes walk the one tree to one inventory (paths, digests, lengths), and the registration's `.opensip/` is inventoried on neither.
- **The custody entry primitives (platform):**
  - the rename moves to a free name and never replaces a taken one, and it is charged exactly before each call;
  - the unlink removes one entry;
  - malformed names and an absent entry are refused.

## Not delivered

- **Sealing,** with the bounds, the carrier join and the leftover-capture refusal at sealing: C1a3. C1a2 provides `leftovers()`.
- **B2's and C2's reads through the session.** B2's marker and manifest reads still run in security's discovery today. Routing them, and C2's layout reads, through `CaptureSession::capture` is J1's composition, with C1-T24's B2 and C2 half of the source pin.
- **The caps and `snapshot_profile`:** C1a4, gated on M3-C r9. The tests use the discovery profile.

## Checks

Lane r2, `evidence/c1a2-checks-r2/`, on base `56d0eb5`:
- **the suites,** at base and candidate, with equal failure sets (isolated reruns for any differing test): host (19 new passing tests), security (1 new) and platform (serially; 2 new);
- **rustfmt** on the new and base-clean edited files, and warning-denied all-targets Clippy on the three crates;
- **the focused tests** and the 4 GiB probe;
- **the model's `--check`** (both outputs), and the T2 census `--check` over the lead-readable cache;
- **repository checks:** FW-01, the environment exceptions, the operability source census, the census-closure check (no closure file changed, so the blind receipt stays current) and verify_design;
- **mutations:**
  - **eleven code mutations,** each failing the focused tests: a captured path read again, a capture change not refused, the before sample not compared, the after sample not compared, the attempt envelope off by one, the buffer uncharged, a duplicate not resolved, `open`'s digest not verified, and (r2) the custody admission skipped, an interrupted write retried, and a refusal's path copied;
  - **four model undercounts,** each regenerated and each failing the session control: the EOF attempt free, the commit's sample free, the capture record free, and (r2) the admission's ACL capture free.

Round 1's lane (`../c1a2-r1/evidence/`) is history; its attempt 1 found the host finalization pin, as that SCOPE records.

## Not claimed

- No caller, no ledger profile and no cap.
- No sealing.
- No Linux claim: the custody entry primitives have a Linux branch, but nothing runs on Linux here.
- **(r2)** The custody admission (`admit_custody_directory`) is macOS-only, like the private-access predicate it wraps, and the host modules are macOS-only.
- No qualification.
- C1a's completion is not claimed.

## Inventory

New paths for the inventory after acceptance:
- `crates/platform/src/custody_entry.rs` and `crates/platform/src/custody_entry_tests.rs`;
- `crates/host/src/candidate_custody.rs` and `crates/host/src/candidate_custody_tests.rs`;
- `crates/host/src/snapshot.rs` and `crates/host/src/snapshot_tests.rs`;
- `crates/host/src/snapshot_session_vectors.json`;
- `crates/security/src/snapshot_route_tests.rs`.

`crates/host/src/snapshot.rs` is a planned inventory row (CH14:495). Before adding it, check whether it is inherited and realized rather than added.
