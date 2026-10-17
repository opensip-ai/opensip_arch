# Review request: C1B-PLAN-r6 (the VCS observation plan, M3-C r8 item 4 with VCS-1 and M3-B successor S4), round 6

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-c1b-plan-r6/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds, lanes, the evidence scripts or the scratch programs.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries.

## Subject

- **Manifest:** `docs/implementation/m3/snapshot-plan-c/c1b-plan-r6-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 4746 bytes, SHA-256 `09c05df25923bdcb370e6eb7d38cc71d66d207cbe379bfed68026cd4a5d71d15`, 22 members:
  - `c1b/PLAN-r6.md`, the subject;
  - `c1b/r6-evidence/vcs_term_r6.py` and `.output.json`, r6's derivation with the reach's names in UTF-8 bytes;
  - `c1b/r6-evidence/reach-cost-check/` (`Cargo.toml`, `Cargo.lock`, `src/main.rs`, `run.log`), the scratch check of the native reach charge and the byte bound, run under the lane lock;
  - every member of round 5's subject, unchanged: their pins must equal `c1b-plan-r5-subject.json`'s.

  Rehash all of them.
- **Bases:** product main `813d559` and architecture `fa875bfd`, as the manifest names. The scratch programs depend on the C1b-1 worktree's `crates/identity` and `crates/platform`, which `git diff caa71e2 813d559 -- crates/identity crates/platform` shows unchanged.
- **Your round 5:** `codex-c1b-plan-r5` (REQUIRED-FINDINGS: C1BPLAN-R5-RF-1), at `/tmp/opensip-implementation/reviews/codex-c1b-plan-r5/`.

## Authority

As in rounds 1 to 5, and also the product's:
- `crates/platform/src/filesystem/directory_open.rs`: `MAX_COMPONENT_BYTES` and `component` (:12-29), `open_child_directory_cost` (:32-43) and `open_child_directory` (:235 on);
- `crates/platform/src/filesystem.rs`: `open_regular` (:493 on);
- `crates/security/src/custody/git_tracking.rs`: `is_link_or_not_directory` (:640-644), `layout`'s not-file mappings (:910, :924) and `member_layout`'s reach (:1478-1530).

## What to review

`PLAN-r6.md` opens with an r6 changes table. Judge:
1. **R5-RF-1, the reach's names in UTF-8 bytes:**
   - the bound of 16,320 bytes, by the exhaustive separator count over `LogicalPath`'s scalar bounds and the 256-segment limit, against your conservative 4 × 4,096;
   - the base costs kept at 256 segments, separately;
   - the scratch check's cases and result in `run.log`;
   - that no path language is narrowed.
2. **The unit audit:** that every length in the term is in bytes, including the record's e(P), C1c-0's retention term and r9's subtotal.
3. **The reach's own allocations:** borrowed segments, no `MemberPath` copy, only the current directory held.
4. **The re-run:** D* and H* unchanged; the term, totals, doubled totals and residual margin in `vcs_term_r6.output.json`; the stated 4,096-byte difference from your arithmetic.
5. **The corrected long-component rule** (LD-C1B-2), found while checking the reach's pricing:
   - the platform's `InvalidInput` over 1,023 bytes and the kernel's `ENAMETOOLONG` both refusing `ref-name`, with the member projection;
   - `InvalidInput` tested before `is_link_or_not_directory`;
   - `<file>-not-file` for a Git file that is not regular.
6. **The added controls** (§4).
7. **No regression** in what rounds 1 to 5 found sound.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `C1BPLAN-R6-RF-n` / `C1BPLAN-R6-NBO-n`.
