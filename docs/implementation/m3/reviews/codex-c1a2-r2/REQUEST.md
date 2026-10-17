# Review request: C1A2-r2 (candidate blob custody and the capture session; M3-C r8 item 1), round 2

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-c1a2-r2/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries; in the candidate worktree, `python3 -I -B tools/security/snapshot_ledger_model.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip` and `python3 -I -B tools/check_operability.py source --repository .`.

## Subject

- **Manifest:** `docs/implementation/m3/snapshot-plan-c/c1a2-r2-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 13345 bytes, SHA-256 `8e9105aecc75b28256553886a4eb5d94f7da57fa043aa906fd175a788ff66498`, 58 members. Rehash every member.
- **The candidate base and lane base:** product main `56d0eb53a888572dd0129fbc595d0c1be16eaf3a` (unchanged since round 1).
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-c1a2`, detached at `56d0eb5`, holding the exact bytes `product-map.json` lists (14 files, 8 new).
- **Your round 1:** `codex-c1a2-r1` (REQUIRED-FINDINGS: C1A2-R1-RF-1 to RF-4, NBO-1), archived at `docs/implementation/m3/reviews/codex-c1a2-r1/`. The r1 package is history.

## Authority

As in round 1: the C1a plan r4 as amended by r5 and r6; law M3-C r8 item 1; C1a1 as integrated; the census's prices. Also security's `private_access.rs` (the existing private-descendant judgment and its law 461 reading of an omitted ACL) and the platform's positioned-write pattern (`file_effects.rs` `write_at_zero`).

## What to review

`SCOPE.md` opens with the r2 changes table. Judge:
1. **RF-1.** `snapshot_source::admit_custody_directory` and its use in `CandidateCustody::new`: one charged ACL capture of the retained descriptor, then `observe_private_directory`'s predicate. Does refusing an omitted ACL (`AclUnavailable`), a named foreign grant and an inherit-only foreign grant (`ForeignAccess`) establish LD-C1A-9's premise, and is the argument that no custody file can then inherit a grant sound? Is the stated boundary (the invoking user's own processes and root) right? The tests prepare custody with the zero-rights owner allow that security's own preparation appends; is that an adequate stand-in for J1's custody location?
2. **RF-2.** `PendingBlob::write`'s single charged attempt: a short write and any error, `Interrupted` included, refuse; nothing retries; the chunk is hashed only once written. Is the ledger's one `WRITE` edge per chunk now an exact bound on native write calls, and is the model's write term exact?
3. **RF-3.** `read_once` consuming the `SourceFile`, every refusal moving the source's charged path, and custody's errors carrying native errors instead of formatted strings. Does `every_session_and_custody_allocation_is_at_a_charged_site` pin the allocation sites adequately, and did the audit miss any uncharged allocation on a refusal branch?
4. **RF-4.** The cleanup bindings replaced by checked outcomes.
5. **The model.** The custody opening is now the ACL capture (anchored at the host call, at security's one-capture judgment, and at the host test's price assertion: 1 object, 131 edges, 7,940 bytes), and `private_access.rs` is pinned whole. Does the session control still hold exactly on the 32 routed trees?
6. **No regression** in round 1's accepted parts (the read envelope, the samples, capture reuse, duplicates, `open`'s verification, the route controls, the platform primitives).
7. **The lane** `evidence/c1a2-checks-r2/`: host 8 = 8 (19 new), security 14 = 14 (1 new), platform 0 = 0 (2 new), equal failure sets; Clippy and rustfmt; the focused tests and the 4 GiB probe; the model and T2 census checks; FW-01, the environment exceptions, operability, closure-unchanged and verify_design; 11 code and 4 model mutations.
8. **Rules:** no new `from(`, `into(`, `pid(`, `line(` or `issue(` call; no new environment read; no `let _ =` in any new or edited product file, tests included; no census-closure file changed.
9. **Inventory:** eight new paths; `crates/host/src/snapshot.rs` realizes its planned row.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `C1A2-R2-RF-n` / `C1A2-R2-NBO-n`.
