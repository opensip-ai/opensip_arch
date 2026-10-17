# Review request: C2A-3K-r1 (the pure retained-tree verification kernel; M3-C r8 item 7, C2a plan r4 sub-unit C2a-3k), round 1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-c2a-3k-r1/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, builds or the lane. The lane lock (`/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-lanes.lock`) is not yours to take.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, private test keys, held trees (E2s, J4a), any T2 store or the T2 cache. The chain test signs through the existing `sign` with the public test-only seeds already in `core_authentication.rs`. Reading that public test code is in scope; no key file is.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries; in the candidate worktree, `python3 -I -B tools/check_operability.py source --repository .`.

## Subject

- **Manifest:** `docs/implementation/m3/snapshot-plan-c/c2a-3k-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 9340 bytes, SHA-256 `c3caf5fb8e818ff89b8f92aaead2813659b2e93f204fff030cbbea39ec2bd5f8`, 40 members. Rehash every member.
- **The candidate base:** product main `d704ed4551d65da8be18faf69f4aeed26be369c2` (contract successor 177, over the v227 lock and D3a-3), which holds C2a-1 r1 (your `codex-c2a-1-r1`, ACCEPT-UNIT; integrated at `e770404`) and C2a-2 r2 (your `codex-c2a-2-r2`, ACCEPT-UNIT; integrated at `1749259`), with the v226 lock since; nothing since C2a-2 touches the candidate's paths.
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-c2a3k`, detached at `d704ed4`, holding the exact bytes that `product-map.json` lists (3 files, none new).

## Authority

- the C2a plan r4 (`snapshot-plan-c/c2a/PLAN-r4.md`; `codex-c2a-plan-r4`, ACCEPT): sub-unit C2a-3k (§2's row, the r3 Q6 ruling), LD-C2A-5, LD-C2A-9, LD-C2A-10 (its C2a-3k prices, and "each comparison and digest is charged first"), LD-C2A-12, and §4's retention controls and §5's retention mutations;
- law M3-C r8 item 7 (`snapshot-plan-c/PROPOSAL-r8.md`:405-450);
- SL:41-48 (`docs/v2/contracts/product-v1/security-and-lifecycle.md`), `BLOB_LENGTH`.

## What to review

`SCOPE.md` gives the change table, the kernel's order and charges (§2), LD-C2A3K-1 to LD-C2A3K-5 and the control map. Judge:
1. **The kernel against the plan's row.** For each Blob, check that the slice is present, that its length equals `bytes`, and that its SHA-256 equals `sha256`. Then check that the body's raw SHA-256 equals `manifestDigest`. The result is typed `Retention(Missing | Length | Digest)`. The kernel must read no file, hold no custody and construct nothing admitted. Check that the signature is the plan's.
2. **The presence walk** (LD-C2A3K-1): its correctness over path-byte order, since the candidate's Blobs are sorted and unique (C2a-1) and `BTreeMap<&str, _>` iterates in byte order. Every key comparison must be charged. Lookalike keys must never match.
3. **Pricing** (LD-C2A3K-2, Q-C2A3K-2): each charge must come immediately before its comparison or digest. Check that only C2a-1's published `COMPARISON_COST` and `digest_cost` are used, that no object or byte is charged, and that nothing is allocated or copied. Check the exact-funding and every-smaller-allowance control, and the aggregate control.
4. **Extras** (LD-C2A3K-3, Q-C2A3K-1): a retained slice that is no Blob's is passed over and never accepted in a file's place, with the extra-file refusal left to the delivery law and C2a-3.
5. **Order and cause** (LD-C2A3K-4): length comes before digest, so no wrong-length slice is hashed. A corrupted tree or body keeps `Digest` and is never relabelled.
6. **C2-T6's kernel leg:** the synthetic signed trees of every role, default and escapable, go through the full chain into the same kernel. C2a-2's two tests must be otherwise unchanged.
7. **C2a-1's pins still hold:** the allocation pin over the extended production source, and the module's other controls.
8. **The lane** `evidence/c2a3k-checks-r1/`: security 1248 → 1257 (+9) and host 412 → 412 (+0) with equal failure sets; rustfmt (all three files base-clean), the exact edited set, Clippy, the workspace and feature checks, the release build, the focused tests, the environment exceptions, operability with an unchanged mint audit, the unchanged census closure and verify_design; 13 mutations, all caught.
9. **Rules:** no new mint-census call, no environment read, no `let _ =`, no signing or private test key read, no new key, root, role, feature, constant or cap; `lib.rs` untouched.
10. **Inventory:** no new path, so no successor.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `C2A3K-R1-RF-n` / `C2A3K-R1-NBO-n`. Rule on Q-C2A3K-1 and Q-C2A3K-2.
