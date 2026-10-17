# Review request: C1A2-r1 (candidate blob custody and the capture session; M3-C r8 item 1), round 1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-c1a2-r1/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries; in the candidate worktree, `python3 -I -B tools/security/snapshot_ledger_model.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip` and `python3 -I -B tools/check_operability.py source --repository .`.

## Subject

- **Manifest:** `docs/implementation/m3/snapshot-plan-c/c1a2-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 13858 bytes, SHA-256 `a4a7a620c76e2148a8fc7fc65cffd1239fa07c3aeebe3ca05ecba5248acc9bef`, 60 members. Rehash every member.
- **The candidate base and lane base:** product main `56d0eb53a888572dd0129fbc595d0c1be16eaf3a` (C1a1 integrated as `ac72a33`; inventory v214; 173 contract successors).
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-c1a2`, detached at `56d0eb5`, holding the exact bytes `product-map.json` lists (14 files, 8 of them new).

## Authority

- the C1a plan r4 (your `codex-c1a-plan-r4`), as amended by r5 and r6 (your `codex-c1a-plan-r6`): C1a2 is preparatory library and model work, with no `snapshot_profile`, no production caller and no census-closure file changed;
- law M3-C r8 item 1 (C1-T1 to T3, C1-T24, C1A-T1 to T3);
- C1a1 as integrated (your `codex-c1a1-r3`), including C1A1-R1-NBO-1's obligation (the route controls);
- the census's prices, imported unchanged.

## What to review

`SCOPE.md` states the change table, the tests, what is not delivered and the checks. Judge:
1. **Custody (LD-C1A-4, LD-C1A-9).** `CandidateCustody` and `PendingBlob`: the private, owned, empty directory; create-exclusive no-follow pending entries; the length checks at write and commit; duplicate resolution from the in-memory set with no re-read; placement only by `rename_exclusive_accounted`, which never replaces; `open`'s re-verification (type, mode, owner, length, digest). Is every step charged before it acts? Can anything held in custody be replaced or changed undetected?
2. **The platform primitives.** `renameatx_np(RENAME_EXCL)` / `renameat2(RENAME_NOREPLACE)` with no overwriting fallback, `EEXIST` as `EntryExists`, single-component names, and the charge before the name copy and the call. `filesystem.rs` is unchanged.
3. **The capture session (C1-T2, C1-T24, C1A-T1).** One reused buffer charged by the bounded reader's growth rule; `read_once`'s before sample, its envelope of `2·⌈size / 64 KiB⌉ + 2` attempts each charged first, its after sample and length check, no retry; `capture`'s reuse by the walk with the (device, inode, size, mtime, ctime) comparison; `inventory()` in path byte order and `leftovers()`. Is the session the one source-read site, and does the source pin establish it?
4. **The charge model.** The session terms of `tools/security/snapshot_ledger_model.py`, read by anchor with counts, the custody prices equal to the census's, and `snapshot_session_vectors.json`. Does the session control (native session walk minus plain walk equals the model's prediction) hold exactly on the 32 routed trees, and is the pinning of the three unrouted trees (vcs-unsupported, identity-contradiction, marker-custody) a sound account of why they have no durable route?
5. **The route controls (C1A-T2, C1A-T3)** in `snapshot_route_tests.rs` and `scenario.rs`'s `with_snapshot_root` / `with_snapshot_root_as`, inside the existing gated module.
6. **Pricing tests:** the buffer's single charge, the 64-chunk payload's 126 extra edges, and the 4 GiB sparse probe (`four-gibibyte-probe.log`).
7. **The lane** `evidence/c1a2-checks-r1/` (attempt 2, the lane of record), with attempt 1 in `evidence/c1a2-checks-r1-attempt1/` and SCOPE's account of its one finding (the host finalization `.finish()` pin, fixed by the associated form):
   - host 8 = 8 (16 new passing), security 14 = 14 (1 new), platform 0 = 0 (2 new), with equal failure sets;
   - Clippy and rustfmt;
   - the focused tests and the 4 GiB probe;
   - the model's `--check` and the T2 census `--check`;
   - FW-01, the environment exceptions, operability, the closure-unchanged check and verify_design;
   - 9 code and 3 model mutations.
8. **Rules:** no new `from(`, `into(`, `pid(`, `line(` or `issue(` call; no new environment read; no `let _ =` in product files; no census-closure file changed.
9. **Inventory:** eight new paths. `crates/host/src/snapshot.rs` is a planned row (CH14:495), to be realized rather than added; say whether that is right.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `C1A2-R1-RF-n` / `C1A2-R1-NBO-n`.
