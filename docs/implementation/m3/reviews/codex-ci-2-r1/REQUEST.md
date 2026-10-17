# Review request: CI-2-r1 (the component store, its installer and the retained-tree capability; law CI r5 items 4 to 7, with amendment CI-A2), round 1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-ci-2-r1/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, builds or the lane. Do not take the shared lane lock (`$(getconf DARWIN_USER_TEMP_DIR)opensip-lanes.lock`).
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, private test keys, held trees, any T2 store, the T2 cache or any held-out material.
- Do not use other panes and do not delegate.
- **Permitted:**
  - read-only reading, hashing, JSON parsing and Git queries;
  - in the candidate worktree, `python3 -I -B tools/check_operability.py source --repository .`;
  - the package's pure script `evidence/receipt_inputs.py`, run with `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B`, writing its output only under this review directory.

## Subject

- **Manifest:** `docs/implementation/m3/component-install/ci-2-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 18829 bytes, SHA-256 `56228f5744839f4fb563daa67286d912f2d448cbf5e6bf73f5d544d2d80e89d2`, 81 members. Rehash every member.
- **The candidate base:** product main `2ead5cf1796bb85f363c34fa8ff8fba715462369` (inventory v228 bound; 177 contract successors). The lane ran at this base.
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-ci2`, detached at that base. It holds the exact bytes that `product-map.json` lists: 16 files, 6 of them new.

## The amendment

This unit proposes law amendment **CI-A2** (SCOPE §4), in CI-A1's shape: each current LAW row or sentence is quoted, and its replacement given. **Accepting this unit accepts CI-A2, and a verdict of REQUIRED-FINDINGS against CI-A2 rejects both.** Until CI-A2 is accepted, LAW stands as written.

The lead decided the step-2 member-order index (CI-A2-a). The rest of CI-A2 was found during implementation:
- `B_open`'s index and association (CI-A2-b);
- `B_transfer`'s lookup (CI-A2-c);
- `tree/`'s own status read (CI-A2-d);
- the reserved admission bound (CI-A2-e), the lead's decision LD-CI2-3;
- CI-A1-b's index serving V1, step 4 and V2 (CI-A2-f);
- the stage's ACL sentinel (CI-A2-g).

## Authority

- **The plan:** `docs/implementation/m3/component-install/PLAN-r3.md` (your `codex-component-install-plan-r3`, ACCEPT, with amendment CI-A1): sub-units CI-2 and CI-3 as one package (the Q1 ruling); LD-CIP-1 to LD-CIP-11; §4's controls; §5's mutations.
- **The law:** `component-install/PROPOSAL-r5.md` (your `codex-component-install-r5`), items 2 and 4 to 8, as CI-A1 (accepted) amends them. CI-A2 quotes `PROPOSAL.md`'s lines 122, 156, 159, 178, 195, 207 and 229.
- **CI-1's codec:** `crates/security/src/archive_profile.rs` (your `codex-ci-1-r2`, ACCEPT-UNIT).
- **C2a-1's bridge:** `crates/security/src/{trust_admitted_components, component_closure}.rs` (your `codex-c2a-1-r1`).
- **The platform primitives used:**
  - `crates/platform/src/filesystem/{directory_publication, directory_effects, file_effects, directory_open, directory_entries}.rs`;
  - `crates/platform/src/work_ledger.rs` (`effect`, `ReservedPostchecks::prepaid`);
  - `crates/platform/src/macos.rs` (`append_owner_zero_allow_*`);
  - `crates/platform/src/locks.rs`.
- **Security's custody rule and its ACL requirement:** `crates/security/src/{snapshot_source, private_access}.rs`.
- **The fixture-site list:** `crates/security/src/crash_matrix_sites.rs` (law X9 r1 item 6; law X8 r3 item 4b).
- **The package policy:** `docs/implementation/m3/operability/o1-package-policy-r1/package-policy.json`.

## What to review

`SCOPE.md` gives the change table, LD-CI2-1 to LD-CI2-4 (the lead's decisions), ID-CI2-1 to ID-CI2-8, CI-A2, the interfaces, the controls, the lane and the census impact. Judge:
1. **The platform primitives** (`component_tree.rs`; LD-CIP-1, -2, -10, -11):
   - one charged native call each, with no retry or fallback;
   - the no-follow, close-on-exec, kind-checked `TreeFile`;
   - the opaque `StandaloneBarrierReceipt`, bound to its exact handle;
   - `try_pin`: one `flock`, busy handed back, release by close alone;
   - P-7's identical expression;
   - macOS only, with every other target refusing before any charge or call.
2. **The transaction** (LAW item 4):
   - admission before acquisition;
   - the reserved bound (LD-CI2-3, CI-A2-e);
   - the store-sibling stage and its ACL sentinel (CI-A2-g);
   - step 2's member order and streaming, with chunk writes at 64 KiB file offsets (ID-CI2-4);
   - V1, with staging modes and every byte re-read;
   - the branch-local finalization (CI-A1-c; ID-CI2-6), every mode before its barrier;
   - V2;
   - the funded same-parent publication and its routes (`LostRace`, `NotPerformed`, `Indeterminate`, an uncertain barrier);
   - no cleanup (LD-CI-12);
   - the re-install path (LD-CI-6).
3. **The shared structural walk** (ID-CI2-5): every row found by its own status read, each directory entered once and listed once at its pop, and the count rule standing in for set equality. Is that rule sound?
4. **The capability** (LAW items 6 and 7):
   - full re-verification;
   - association by bytes and by Blob (ID-CI2-7);
   - the pin, taken before anything else of the generation is read and never recreated;
   - the retained handles, buffer and index;
   - `transfer`'s per-component descent, re-check and verified sink protocol;
   - `PinRequest`;
   - the typed failures and their causes.
5. **The prices:** `install_bound`, `open_bound` and `transfer_bound` against LAW's recipes as CI-A1 and CI-A2 amend them. Also the controls' independent enumeration: objects and bytes exact, and edges exact except comparisons and read attempts, which are bounded by their worst cases.
6. **CI-A2** (SCOPE §4): is each part needed, correctly quoted, correct and narrow, changing no other rule? Is any other LAW text still in conflict with the code?
7. **LD-CI2-1:** C2a-1's bridge made public without a second trust interface, and shared fixture gates 7 and 8, by name. Is that the right authority path under law X9 r1 item 6 and law X8 r3 item 4b?
8. **The controls and the mutations** (SCOPE §6): what is covered, and what is stated as not exercised (CI-T11's signed half, CI-T16, the crashed-holder release, and an injected parent-barrier failure). Do those gaps need a finding here?
9. **The lane** `evidence/ci2-r1-checks/`: lifecycle 32 → 73 (41 new), platform 331 → 340 serially (9 new), security 1281 → 1281, each with equal failure sets; warning-denied Clippy on the three crates, the workspace check and four feature checks; the release and fixture builds' symbol checks against their own rlibs; package edges; rustfmt (security `lib.rs` append-only); the environment exceptions; operability; the census closure and CI-PT-4; verify_design; and all 27 mutations caught. Also SCOPE §6b's attempt history: three rebases (D3a-3's `Cargo.lock`, C2a-3k's `component_closure.rs`, C1b-1's `lib.rs`), and the defects attempts 2 and 4 found, with their fixes.
10. **Rules:** no census-bound file changed; no new mint-census call; no environment read; no `let _ =`; no new third-party dependency (one new internal edge, which the policy permits); security's `lib.rs` changed append-only.
11. **Inventory:** the new rows and `installation.rs` realizing its planned row; an inventory successor follows acceptance.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "amendmentCIA2": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `CI2-R1-RF-n` / `CI2-R1-NBO-n`. Accepting this unit accepts no CI-4 code.
