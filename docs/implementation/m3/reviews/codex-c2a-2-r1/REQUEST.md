# Review request: C2A-2-r1 (the shared synthetic component fixtures; M3-C r8 item 8, C2a plan r4 sub-unit C2a-2), round 1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-c2a-2-r1/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, builds or the lane. The lane lock (`/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-lanes.lock`) is not yours to take.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, private test keys, held trees (E2s, J4a), any T2 store or the T2 cache. The module under review signs through the existing `sign` with the public test-only quorum62 seeds already in `core_authentication.rs`. Reading that public test code is in scope; no key file is.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries; in the candidate worktree, `python3 -I -B tools/check_operability.py source --repository .`.

## Subject

- **Manifest:** `docs/implementation/m3/snapshot-plan-c/c2a-2-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 8558 bytes, SHA-256 `1e64f3800a4a47259969e8fde95562c9877d460ef78563efb5a17c8ee8182f44`, 37 members. Rehash every member.
- **The candidate base:** product main `e770404a8e6e1f5a604c54e7b0626c6309d76381`, which holds C2a-1 r1 (your `codex-c2a-1-r1`, ACCEPT-UNIT; integrated at `e770404`).
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-c2a2`, detached at `e770404`, holding the exact bytes that `product-map.json` lists (4 files, 2 new).

## Authority

- the C2a plan r4 (`snapshot-plan-c/c2a/PLAN-r4.md`; `codex-c2a-plan-r4`, ACCEPT), sub-unit C2a-2, LD-C2A-6 and the Q4 ruling;
- law M3-C r8 item 8 (`snapshot-plan-c/PROPOSAL-r8.md`:451-466), with C2-T6, C2-T7 and C2-T8's label half.

## What to review

`SCOPE.md` gives the change table, LD-C2A2-1 to LD-C2A2-5, the control map and two open questions. Judge:
1. **The predicate** (LD-C2A2-1, Q-C2A2-2): the module included inside `core_authentication.rs`'s `tests` module, so under exactly `cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))`, with the crash-matrix site census unchanged; C2-T7's source pin; the lane's release build.
2. **Signers and root** (LD-C2A2-2): only `sign` with `COMPONENT_SIGNER` and `INDEX_SIGNER` under the existing synthetic root; no key, seed, root or feature introduced.
3. **Existing bytes** (LD-C2A2-3, Q-C2A2-1): `component_release` through `release_row` with `p1`, byte for byte; an empty `components` list unchanged; the existing suites' equal failure sets; `LABEL` on every row the module writes.
4. **Role validity** (LD-C2A2-4): every role's body passes the real body validation with C2PM-1's major 1 and CR-1's command, capability and permission rules; the tree is exactly the supplied bytes.
5. **C2-T6's leg** (LD-C2A2-5): the signed release of every role through the InitialCore, acceptance onto a P0 installation, the full ordinary reader over the accepted store, C2a-1's bridge and candidate for every role; nothing claims retention or admission.
6. **The lane** `evidence/c2a2-checks-r1/`: security 1212 → 1218 (+6) and host 412 → 412 (+0) with equal failure sets; Clippy, rustfmt (core_authentication.rs and lib.rs base-dirty, not reformatted), the workspace and feature checks, the release build, the focused tests, the environment exceptions, operability with an unchanged mint audit, the unchanged census closure and verify_design; 9 mutations, all caught.
7. **Rules:** no new mint-census call, no environment read, no `let _ =`, no signing or private test key read, no new key, root, role or feature.
8. **Inventory:** two new rows; the successor numbered at integration from the lock's last plus one, after the combined C1c-0 and C2a-1 v223 (so v224 or later).

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `C2A2-R1-RF-n` / `C2A2-R1-NBO-n`. For each open question, say whether it is a finding.
