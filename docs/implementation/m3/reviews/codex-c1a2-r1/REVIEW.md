# C1A2-r1 review

Verdict: **REQUIRED-FINDINGS** — four required findings and one nonblocking observation.

## Exact subject

Verified the 13,858-byte subject manifest SHA-256 `a4a7a620c76e2148a8fc7fc65cffd1239fa07c3aeebe3ca05ecba5248acc9bef` and rehashed all 60 members. All 14 product-map candidates equal the worktree and architecture archive bytes; the six parent pins equal product base `56d0eb53a888572dd0129fbc595d0c1be16eaf3a`. The candidate worktree is detached at that base and its changed/untracked paths match the map: six edited files and eight newly present files.

## Required findings

### C1A2-R1-RF-1: Establish private custody beyond mode bits and owner

Location: `crates/host/src/candidate_custody.rs:142`.

CandidateCustody::new accepts a retained directory after an fstat mode/uid check and an empty listing. RetainedDirectory does not admit custody, and observe_descriptor_metadata contains no ACL observation. On macOS, an owned 0700 directory can still have named ACL grants permitting another principal to traverse or alter entries; new 0600 files can also inherit ACL grants. Neither begin/commit nor open validates those grants. This does not establish LD-C1A-9's premise that nothing else writes custody. For example, an ACL-authorized actor can replace a pending name after its descriptor is sampled/closed and before the name-based exclusive rename; RENAME_EXCL protects the destination, not the binding of the source name to the written descriptor. The commit then records the original digest/length without verifying the substituted entry.

Required change: Accept an existing descriptor-bound private-custody proof, or establish the private-directory and created-file ACL premise using the existing custody/ACL machinery, with charges before observation. Preserve the distinction between omitted ACL evidence and a proved absence of unauthorized access. Add native controls with mode 0700 plus an unauthorized named directory ACL and inherited file ACLs; require refusal before custody use, or prove equivalent exclusion by a retained private parent. Do not claim mode/uid alone excludes writers.

### C1A2-R1-RF-2: Bound and charge every actual custody write attempt

Location: `crates/host/src/candidate_custody.rs:330`.

PendingBlob::write charges WRITE once and then calls std::io::Write::write_all. write_all retries Interrupted and completes short writes with additional write calls; regular files are not guaranteed to consume a chunk in one call. An arbitrary number of Interrupted results can therefore perform native attempts inside one charged edge, without an attempt envelope. The model anchors exactly one WRITE edge per chunk, so its edge bound does not bound this work. The 32 native/model comparisons and sparse probe cover ordinary full writes and cannot establish the missing fault-path bound.

Required change: Use a single charged write attempt that refuses short/interrupted writes, consistent with the existing bounded file-effect pattern, or implement an explicit finite write-attempt envelope with each attempt charged before the call. Hash/account only according to the chosen terminal write semantics. Update the model and add injected short-write/Interrupted controls and a mutation proving no retry is uncharged. No successful-path payload-byte charge is requested.

### C1A2-R1-RF-3: Charge or transfer owned paths on refusal branches

Location: `crates/host/src/snapshot.rs:316`.

The source path is copied with to_owned on ChangedSinceCapture (244), ChangedBeforeRead (316), ReadAttemptsExhausted (326), read I/O failure (344), and ChangedDuringRead (351/359), without a preceding owned_record charge for those new allocations. The source already owns a path, but copying it is a distinct allocation under the shared recipe; the normal Capture record charge is not reached on these branches. Thus the asserted complete session model omits work performed by actual typed refusals, potentially including a maximum-envelope logical path. Successful routed-tree comparisons and mutants deleting successful-path charges do not exercise this omission.

Required change: Move an already charged owned source path into the terminal refusal where possible, or charge the additional owned path before copying it, preserving the applicable budget/refusal precedence. Extend the model or explicitly bounded refusal allowance accordingly, and add long-path change/I/O/attempt-exhaustion controls plus an omitted-charge mutant. Audit the custody error-string allocation branches under the same recipe.

### C1A2-R1-RF-4: Remove the new ignored-result bindings prohibited by the request

Location: `crates/host/src/candidate_custody_tests.rs:11`.

Request item 8 says no let _ = in product files. Four new bindings occur in candidate_custody_tests.rs:11 and :16, snapshot_tests.rs:18, and custody_entry_tests.rs:12. These are test cleanup bindings rather than production behavior, but they are new mapped product files and the request supplies no test-file exception to this rule.

Required change: Replace these four bindings with explicitly handled cleanup/process outcomes consistent with the repository conventions. Keep cleanup scoped to the synthetic fixture directories; do not change production authority or swallow a failed chmod as a successful test control.

## Reviewed behavior

**Custody and primitives.** Exclusive no-follow creation, expected-length checks, in-memory duplicate resolution without rereading, digest names, exclusive rename and open-time type/mode/owner/length/digest checks are present. Both rename branches use the required exclusive flag, classify raw EEXIST as EntryExists, charge before CString copies/native calls and have no overwriting fallback. Unlink is likewise charged and rejects malformed components. `filesystem.rs` is unchanged. These mechanisms do not by themselves establish the missing ACL custody premise in RF-1. Open-time hashing verifies what was read at that time; it is not a proof that an unauthorized writer cannot mutate a file afterward.

**Session.** The reused buffer is charged once at the bounded reader growth price, 4+8+16+32+64 KiB (126,976 bytes). Source reads have one production call site, a charged attempt before each read, the finite `2*ceil(size/65536)+2` envelope, start/end observations and exact length checks. Interrupted reads consume attempts. Capture reuse compares device/inode/size/mtime/ctime against the walk's observation through its enumerating parent, without a second source read. Reached inventory is in path byte order; unreached captures remain leftovers. Sealing and its leftover refusal are correctly deferred to C1a3. RF-2 concerns custody writes, not the correctly bounded source-read loop.

**Model and routes.** The model imports census prices unchanged, reads/counts its anchors, pins the three session files whole and reproduces both checked-in vector outputs. The archived native control records exactly 32 session-minus-plain-walk comparisons. The other three trees are explicitly pinned to their X2 admission refusals: pruned-anchors-all-four/vcs-unsupported, opensip-file-at-the-root/identity-contradiction, and opensip-anchors-root-and-member/marker-custody. They are not silently counted as successful session routes; C1a1 covers their walk terms. These checks establish the recorded normal-path charges, with the failure-path gaps in RF-2/RF-3 still outstanding.

C1A-T2/T3 use the released-read and durable-operation roots on the same synthetic installation and compare paths, digests and lengths. While the ephemeral root is retained and unwalked, a writer acquires the fence and APPEND_WRITE lease and completes handoff; both walks omit the registration's `.opensip/` anchor. The scenario helpers sit in the existing gated module and lend the durable root while the operation remains alive.

**Pricing.** The archived controls establish one buffer charge, 126 extra attempt/write edges for 64 chunks versus one byte, and 131,070 extra edges for the 4 GiB sparse file (65,535 extra reads and writes each). The ignored probe was explicitly run and passed in 124.67 seconds. It establishes bounded memory accounting on that path, not a short-write or Interrupted-write bound.

## Evidence and independent checks

I ran only the two expressly permitted candidate commands:

- `python3 -I -B tools/security/snapshot_ledger_model.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip`: passed; both vector files verified.
- `python3 -I -B tools/check_operability.py source --repository .`: passed, 114 rows, no findings.

Inspected the pinned attempt-2 raw logs, comparison data, check definitions and mutation records. They support:

| Suite | Base failures | Candidate failures | New passing tests |
| --- | --- | --- | --- |
| Host | 8 | Same 8 | 16 |
| Security | 14 | Same 14 | 1 |
| Platform | 0 | 0 | 2 |

Host/security are baseline-comparison results, not whole-suite passes. Focused host/security/platform runs, warning-denied all-targets Clippy, formatting of the eleven edited/new Rust files, model check, discovery census check, FW-01, environment exceptions, operability, unchanged-closure check and design verification are recorded successful. Each of the nine code and three model mutants fails its intended focused control; these results do not cover the newly identified failure paths. No mutation, build or Rust test was rerun by this review.

Attempt 1 records the new structural finalization failure. The candidate now uses associated `RawSha256::finish(digest)` at both production hash-finalization sites, and attempt 2's host failure set equals the base. The fix does not confer commit authority on custody.

Independently found an empty intersection between all changed/new product paths and the census's 19 pinned Rust closure files. The filesystem module and census tool are unchanged; generator-closure.json is not changed. The recorded census/receipt check was inspected only; no T2 store or cache was accessed or rerun.

## Rules, inventory and scope

No new production environment read or production call of the prohibited `from`, `into`, `pid`, `line` or `issue` forms was found. Test-only temporary-directory fixture setup is separate from production input handling. The new ignored-result bindings are reported explicitly in RF-4 rather than treating item 8 as satisfied.

The eight filesystem additions do **not** require eight new inventory rows. In v214, `crates/host/src/snapshot.rs` already has the planned opensip-host service row, description “Capture exact admitted source/read-set bytes through the selected custody boundary,” standing proposed. Realize that inherited row; add only the other seven paths. No inventory successor or binding is accepted by this code review.

The candidate stays within plan r6's preparatory boundary: no production caller, snapshot profile, caps, sealing or qualification. C1a3, C1a4 with accepted M3-C r9, J1's B2/C2 read routing, C1b/C1c and downstream integrations remain separate gates. Linux's rename branch is source-inspected only; the recorded lane makes no Linux claim.

## Nonblocking observation

**C1A2-R1-NBO-1 — Keep the source-pin claim bounded to the preparatory modules** (`crates/host/src/snapshot_tests.rs:460`). Inspection confirms one source.file().read call in the session and no content read in the security opener/walk; custody reads its own retained directory only. The lexical pin is useful but does not prove the full future J1 composition has no alternate reader. SCOPE correctly leaves B2/C2 routing and their half of C1-T24 to J1; retain that limitation when integrating and extend the pin with those callers.

## Boundaries

All findings are based on source and authority inspection; no adversarial ACL/write probe was executed. No repository, candidate worktree or control file was edited. No Cargo/rustc/build/lane, network, other pane or delegation was used. No installation, private 413 fixture, signing key, held tree, T2 store or cache was read. Only REVIEW.md and review.json in the requested directory were written.
