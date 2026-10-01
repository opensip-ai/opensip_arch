Grok re-review: X4T-a2 and X4T-b r2, after your r1 RF-1, with inventory v106 rebuilt on v112. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-trust-floor-x4tb-r2. If you build or test, use a CARGO_TARGET_DIR under that directory. Run git only read-only, and only against the worktree below.

Law: `docs/implementation/m2/trust-admission-x4t/PROPOSAL.md` r9 (accepted). Your r1 review is `reviews/grok-trust-floor-x4tb-r1/` (REQUEST.md there describes the whole unit; it is unchanged except as listed here). r1 found one required finding (RF-1), accepted judgment calls 1 to 10, 12 and 13, and assessed inventory v106 on v105 as ACCEPT.

## Subject

Pins are in hashes.txt.
- **Product:** the worktree `/Users/sb/code/opensip-ai/opensip-x4tb`, now based on f1b8321 (F4 and X3d-0 integrated, inventory v112 selected). Save `git -C <worktree> diff` (the two new files are intent-to-add) as product.diff and report its sha256. Lead's value: 513adaeb1cf17b361cfd45479ca4696d2bb3eb665ec48537596f6fb4b82cbb6d, 106921 bytes, 13 files, 2079 insertions and 86 deletions.
- **Arch:** v106 (parent v112): `trust-floor-x4tb-inventory-v106-subject.json` and `trust-floor-x4tb-inventory-v106/`.

## Rebase

Four changes integrated after r1, and the diff applied to each base with no conflict:
- **X12b** (6dd7363, inventory v109) touched only `crates/host`.
- **X2d** (9d51f33, inventory v110) touched `custody.rs`, `first_registration.rs`, `installation_read.rs` and `ordinary_writer.rs`, and added `namespace_lease.rs`. This unit changes none of those files.
- **F4** (8bd0283) changed only test fixtures (`installation_read_fixture.rs`, `installation_observation_tests.rs`).
- **X3d-0** (f1b8321, inventory v112) added `WorkLedger`'s settlement reserve in `platform/src/work_ledger.rs`. It leaves `effect`, `prepaid`, `spend`, `charge` and `scope` unchanged, so this unit's reservation is unaffected. The unit's 40 targeted tests pass on f1b8321.

At each base, `git diff` is byte-identical to the r2 diff first made on 0206ce8.

v106 got parent-only rebuilds: one more PRIOR entry each, for v109, v110 and v112, in `build_v106.py`. The README, `verify_scratch.py`'s docstring, `verify_projection.py`'s comment and `verifier-anchor.json` now name v112 and f1b8321. v106 has 791 files: all 789 v112 rows by value, plus the same two rows. Only the two added rows' descriptions changed, for RF-1 (below). The number 106 sits below its parent's 112; succession is by the lock's parent pin.

## RF-1: the exact rereads

`capped_read` (2·len + 8192) is gone. Both rereads now reserve the platform's own `read_bounded_cost(len, attempts(len))`. That is `exact_read`, which `file_cost` (an existing content-addressed record's reread) and `confirmation_cost` (the post-rename reread) both use.
- `attempts` is the read session's bound: one per growth to len + 1, the EOF read, and four spare. That is `installation_session::attempts`, made `pub(crate)` and reused, not copied.
- `read_bounded_accounted` charges one object, one edge per growth or attempt, and every requested growth's bytes. `read_bounded_cost` is that exact sum for a file of length len read at max = len, with the edge term at the session's attempt bound.

**Nothing is charged after the first effect.** r1's `publish` ended with an owner recheck charged outside the reservation. That recheck is the confirmation's second judged sample, which `confirmation_cost` has always reserved, so the trailing charge is removed.
- `publish` now charges only the opening owner recheck and then the single `effect`. A short ledger therefore refuses on that charge, before the first write.
- `fenced_first_read` likewise returns right after a publication, with no further charge. On the no-write path, it keeps its closing recheck.

**No other estimate in the diff has this problem.**
- Every other reserved term is a published platform cost: the ACL captures, the owner allow, child opens, the absence probe, `write_new_regular_cost`, `rename_replace_cost`, the directory barrier and `open_regular_cost`.
- X3b's `publish_private_file` reopen is its own `work.run(reopen_confirmation_cost)`, mirrored exactly.
- The read-only admission's reads go through `Budget::load`, under its own ledger accounting.

**Test (new): `the_reservation_covers_both_exact_rereads_at_every_growth_boundary`.** For each of 16384, 20480, 32768, 53248, 65536, 118784 and 131072 (the parser cap):
- the capsule is padded to exactly that length (a namespace on TR-CORE's acceptance), and an equal content-addressed record of the same length is already present, so `publish` runs both exact rereads;
- a measuring run gives the ledger total;
- on a fresh site, a ledger with exactly that total completes, and the pointer and the owner advance;
- on another fresh site, one byte less refuses on the budget row, with `state.v1` unchanged and no `state.v1.*` temporary file beside it.

With r1's formula substituted back, this test fails at 16384 with `ReservedPostcheck`. The lead ran that check and reverted it.

## Checks

- **X4T-b tests:** 13/13 (r1's 12 plus the boundary test). X4T-a's 19, X4T-0's 7 and the gate's advance test pass.
- **Workspace:** two full runs on f1b8321 plus this diff. Results: 1433 passed, 0 failed, 3 ignored, each time.
- **Clippy and fmt:** `--workspace --all-targets -D warnings` and `fmt --check` are clean.
- **Package edges:** `check_package_edges --lane host` against v106 passes.
- **verify_scratch:** v106 appended over the worktree's lock at f1b8321 passes: 74 inventory successors, 72 contract successors, 16 inheritance rows, v106 selected.
- **verify_projection** against the real lock: 16 rows, 83 corruptions refused. `build_v106.py` reruns produce the same bytes.
- **Real home:** `~/Library/Application Support/OpenSIP` is absent.

## Decide

- Is RF-1 closed? In particular:
  - both rereads at the platform's exact cost with the session's attempt bound;
  - every lawful capsule up to 131072 bytes completes when the ledger can pay;
  - a short ledger fails before the first effect.
- Is the rebuild of v106 on v112 right?
- Is anything new wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": the sha256 of `trust-floor-x4tb-inventory-v106-subject.json`;
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes, sha256 of v106, parent (the v112 pin), successorRecord}.

Write REVIEW.md and review.json. Do not commit.
