# B2-b1 r1: what the candidate delivers (M3-B unit B2-b, sub-unit B2-b1: platform primitives)

**Lead scope record, 2026-10-15. Unreviewed candidate.** It implements section 1.1 of the accepted B2-b plan r4 (`config-discovery-b/b2-b/PLAN-r4.md`; Codex `codex-b2b-plan-r4`). Its base is product `7d0ac1b`, where B2-b0 is bound as contract successor 164.

## Paths

All five are existing, inventoried platform files. No path is added.

| Path | Change |
|---|---|
| `crates/platform/src/work_ledger.rs` | `WorkLedger::discovery_profile()` and its three provisional caps (2^20 objects, 2^21 edges, 2^30 bytes; MB:396). `with_limits` is unchanged and still cannot raise any cap. |
| `crates/platform/src/filesystem/directory_open.rs` | `ChildKind {Directory, File, Symlink, Other}`, `ChildObservation {Absent, Present{kind, metadata}}`, `ChildObservation::matches(&DescriptorMetadata)`, `RetainedDirectory::observe_child(name)` and `observe_child_accounted(name, work)`; four tests. |
| `crates/platform/src/filesystem.rs` | `DescriptorMetadata::from_stat(&libc::stat)`, crate-private, the same fields as `from_metadata`; the two re-exports. |
| `crates/platform/src/lib.rs` | The re-export of `ChildKind` and `ChildObservation`. |
| `crates/platform/tests/work_ledger_tests.rs` | Two tests of the profile. |

All new items are macOS-only, like `from_metadata` and `observe_descriptor_metadata`. Linux builds are unchanged.

## Plan 1.1, item by item

- **The discovery profile.**
  - It is the only constructor above the global caps: `with_limits(profile)` is still `Profile`.
  - Like every ledger it has no `Default` and no `Clone`, so a failed discovery ledger is never replaced.
  - Exhaustion is the existing per-component `Budget` failure and latches.
  - "Created once after the handoff, never recreated" is the owner's discipline (B2-b3). The type cannot express it beyond the absence of `Default` and `Clone`.
- **`observe_child`.**
  - One `fstatat(AT_SYMLINK_NOFOLLOW)` under the existing component grammar: no open, no creation, no following.
  - `ENOENT` is `Absent`; every other error is returned.
  - The kind comes from `S_IFMT`, and the full `DescriptorMetadata` (device, inode, mode, owner, links, size, times, flags) is kept.
  - The accounted form charges the existing `child_absence_observation_cost`: the same single status read.
- **`matches`.** It compares device, inode and kind with the descriptor later opened from the same name. `Absent` matches nothing.

## Tests

- **Each kind:** directory, file, symlink and FIFO, with identity equal to `lstat`. Absent. The name grammar refusals (`..`, `a/b`, empty).
- **No time changes:** the parent's and the child's atime, mtime and ctime are equal before and after the observation.
- **Same-kind replacement:**
  - an unchanged directory and file each match their opened descriptor;
  - a directory renamed away and recreated, and a file atomically replaced, do not match;
  - a kind mismatch does not match;
  - `Absent` never matches.
- **Accounting:** the accounted form charges exactly one status read.
- **The profile:**
  - each cap admits exactly its value and refuses one more, and the failure latches;
  - `charge(cap + 1)` on a fresh profile fails with that component's error;
  - `with_limits(profile)` is `Profile`;
  - a charge beyond every global cap fails on `new()` and succeeds on the profile.

## Check lanes

The evidence is lane r2. Lane r1 (kept in the work directory) failed on three counts, two of them fixed in the candidate and one in the runner.

**1. Platform tests are serial in r2.** The platform suite has raw-descriptor tests that race under parallel test threads:
- `harness_descriptor` asserts on fd 3, and the `locks` child probes are timing-sensitive;
- the **base** run, with no B2-b1 code, aborted with `IO Safety violation: owned file descriptor already closed`;
- the candidate run failed those three tests.

r2 runs the platform suite with `--test-threads=1` for base and candidate alike. Security and host are unchanged.

**2. The census `swallowed` count.** A new test discarded a result with `let _ =`, which raised the count. The test now asserts on it.

**3. The mint-audit census.** The census is lexical, and `from` is a mint member, so the new `u32::from`, `u64::from` and `usize::from` calls changed it. They are now `as` casts and `.min(1)`. The audited exceptions list is unchanged, so the census passes with no new row.

Behaviour is unchanged between r1 and r2.

## Lead decision

**LD-B2B1-1. No inventory successor for B2-b1.**
- B2-b1 adds no path, and every changed file keeps its inventory row and description.
- **Rejected:** a successor with no added row, which would record nothing.

## Not claimed

- No walker, no discovery-ledger owner, no custody and no caller (B2-b2, B2-b3).
- No T2 census (B2-b4).
- No qualification.
