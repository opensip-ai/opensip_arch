# C1A2-r2 review

Verdict: **ACCEPT-UNIT**

Required findings: none. Nonblocking observations: none.

## Exact subject

Verified the 13,345-byte subject manifest SHA-256 `8e9105aecc75b28256553886a4eb5d94f7da57fa043aa906fd175a788ff66498` and rehashed all 58 members. All 14 mapped candidate files match the worktree and architecture archives; all six parent pins match product base `56d0eb53a888572dd0129fbc595d0c1be16eaf3a`. The worktree remains detached at that base, with six edited and eight newly present files. Rechecked subject and candidate hashes before writing this review.

## Round-1 findings

**C1A2-R1-RF-1 resolved.** CandidateCustody::new delegates private-directory admission to security's admit_custody_directory, which calls the existing observe_private_directory predicate. That predicate takes one charged descriptor ACL capture, then judges the captured metadata and ACL in place. It requires the invoking owner, directory kind and exact 0700 permissions; unavailable/NOACL evidence is refused, not converted to an empty ACL. Unknown ACE flags/kinds and nonzero grants to other principals refuse. Inherit-only foreign grants are not skipped.

This establishes the required exclusion of other principals at the retained directory and prevents inheritance of an unauthorized grant into newly created custody files. Owner-only grants and deny entries do not grant another principal access. The invoking user's own processes and root remain outside this exclusion boundary; the retained parent/path and its lifecycle remain J1's responsibilities. The admission does not claim persistent protection against changes by those trusted principals.

The synthetic fixture's zero-rights owner allow is an adequate stand-in for the prepared private descendant: it uses the same platform append operation as security's private preparation, grants no access, and is then judged by the actual predicate. This is not proof of a future J1 caller or location. Native controls explicitly refuse a bare 0700 directory as AclUnavailable and reject both named and inherit-only foreign grants as ForeignAccess. Existing private_access and the ACL capture primitive are unchanged.

**C1A2-R1-RF-2 resolved.** PendingBlob::write charges WRITE before its single production file.write call. A short write and every error, including Interrupted, return immediately; there is no write_all or retry loop. Digest state is taken before the attempt and restored only after a full successful write, so a failed attempt cannot later be committed as a successfully hashed chunk. Each successful chunk is hashed once after writing. One WRITE edge per chunk is now the appropriate native-call bound; the model's normal successful-write term remains exact. Injected short/Interrupted controls and the uncharged-retry mutant cover the correction.

**C1A2-R1-RF-3 resolved.** read_once consumes SourceFile. The capture key and path-bearing change, read-error and attempt-exhaustion refusals move source.into_parts().0 rather than copying the logical path. Metadata-sample I/O failure retains the existing empty String representation, which allocates no buffer. Custody creation errors now carry native errors or a fieldless PendingExists; they no longer allocate formatted error strings. Existing collision errors move the already charged digest name.

Audited the remaining production allocation sites: the session buffer, pending name, digest names, capture-map entry and committed-set entry are charged before their allocations. The latter two use the shared owned-record overhead. Native helper work retains its published accounted boundaries. The new lexical pin checks the current allocation spellings, charged-site adjacency and seven path moves, and catches the refusal-path-copy mutant. It is a useful regression guard alongside this source audit, not a general Rust allocation analysis.

**C1A2-R1-RF-4 resolved.** All four ignored cleanup bindings are replaced with checked outcomes. The chmod status and directory removals are checked unless already unwinding from a test failure. No let _ = binding remains in any of the eleven new/edited Rust files, tests included.

**Prior NBO-1 appropriately carried.** The one-source-read pin remains explicitly scoped to the preparatory session, opener/walk and custody modules. Full B2/C2 read routing and the corresponding caller pin remain J1's work.

## Model, unchanged behavior and inventory

The model anchors the host admission call, security's delegation, the existing predicate's one capture and the host's actual price assertion: 1 object, 131 edges, 7,940 bytes. It pins private_access.rs whole in addition to the original three session files; snapshot_source.rs is also pinned by the walk output. Census prices remain imported unchanged.

Independently compared all 35 r1/r2 session-vector predictions: handed-file counts are unchanged and every prediction changes by exactly `(objects +1, edges +130, bytes +7428)`. This is precisely replacing the old `(0,1,512)` status sample with the `(1,131,7940)` ACL admission. The recorded native session-minus-plain-walk control still matches the model exactly on all 32 routed trees. The same three trees are pinned to their own X2 route refusals: vcs-unsupported, identity-contradiction and marker-custody. They are not counted as successful session controls.

No regression was found in the source read-attempt envelope, before/after observations and length checks, changed-capture refusal without rereading, path-byte-order inventory, leftovers, in-memory duplicate resolution or custody open-time verification. The reused buffer is still charged once at 126,976 bytes; the 64-chunk control still adds 126 attempt/write edges, and the 4 GiB sparse probe adds 131,070 edges versus one byte while retaining the same objects/bytes.

The platform exclusive rename implementation, platform exports, host module declarations, scenario helpers and route controls are byte-identical to r1. renameatx_np(RENAME_EXCL)/renameat2(RENAME_NOREPLACE), single-component validation, EEXIST classification, no overwriting fallback and pre-call charges are retained. filesystem.rs is unchanged. Both lawful route controls retain their fence/lease and identical-inventory assertions.

Inventory v214 already contains the planned snapshot.rs service row. Of the eight new filesystem paths, realize that inherited row and add the other seven rows. This review does not accept an inventory successor or binding.

## Verification

Independently ran only the two expressly permitted candidate commands:

- `python3 -I -B tools/security/snapshot_ledger_model.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip`: passed; both vector outputs verified.
- `python3 -I -B tools/check_operability.py source --repository .`: passed, 114 rows, no findings.

Inspected the pinned r2 raw logs, comparison data, runner and mutations:

| Suite | Base failures | Candidate failures | New passing tests |
| --- | --- | --- | --- |
| Host | 8 | Same 8 | 19 |
| Security | 14 | Same 14 | 1 |
| Platform | 0 | 0 | 2 |

These are equal-failure-set comparisons; host/security are not whole-suite passes. Focused host/security/platform tests pass. The separately run 4 GiB probe passes in 125.96 seconds. The eleven code and four model mutations each fail the intended focused control, including ACL omission, write retry and refusal-path copying; these are runtime test failures, not compilation failures.

The lane records successful rustfmt, warning-denied all-targets Clippy for the three crates, model and discovery-census checks, FW-01, environment exceptions, operability, unchanged census closure and design verification. Independently confirmed an empty intersection between all 14 candidate paths and the census's 19 pinned Rust closure files. No new prohibited from/into/pid/line/issue call form or production environment read was found. Temporary-directory setup stays in synthetic tests; no new production ambient input is introduced.

## Scope and boundaries

Acceptance is limited to this preparatory library/model unit. No production caller, snapshot profile, cap, sealing, complete C1a, Linux qualification or product qualification is inferred. C1a3, C1a4 with accepted M3-C r9, J1's composition and C1b/C1c retain their gates. The Linux primitive branch remains source-inspected only.

No Cargo/rustc/build/lane or additional Rust test was run by this review. The T2 census result was inspected as archived evidence only; no T2 store/cache was accessed. No network, other pane or delegation was used. No installation, private 413 fixture, signing key or held tree was read. Neither repository, candidate worktree nor control file was edited. Only REVIEW.md and review.json in the requested directory were written.
