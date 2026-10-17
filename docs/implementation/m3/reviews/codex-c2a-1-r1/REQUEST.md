# Review request: C2A-1-r1 (the unadmitted closure candidate; M3-C r8 items 7 and 8, C2a plan r4 sub-unit C2a-1), round 1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-c2a-1-r1/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, builds or the lane. The lane lock (`/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-lanes.lock`) is not yours to take.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, private test keys, held trees (E2s, J4a), any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries; in the candidate worktree, `python3 -I -B tools/check_operability.py source --repository .`.

## Subject

- **Manifest:** `docs/implementation/m3/snapshot-plan-c/c2a-1-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 13147 bytes, SHA-256 `cc9916f71c928a85ddb3bcf901d226f141180f3fb06e55d803e2f365a86ae0b7`, 56 members. Rehash every member.
- **The candidate base:** product main `813d559efccbfc30b81b7530833c8427bb4f7dfd` (C1c-0, on D3a-2, C1b-0's successor 176 and the v222 lock).
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-c2a1`, detached at `813d559`, holding the exact bytes that `product-map.json` lists (6 files, 3 new). It was created at `3742822` and moved onto main before the lane. Main has since changed one of its paths: C1c-0's own append to `lib.rs`, which C2a-1's append now follows (SCOPE).

## Authority

- the C2a plan r4 (`docs/implementation/m3/snapshot-plan-c/c2a/PLAN-r4.md`; your `codex-c2a-plan-r4`, ACCEPT, with its NBO-1 and NBO-2), sub-unit C2a-1, LD-C2A-2 to LD-C2A-4 and LD-C2A-9 to LD-C2A-12;
- law M3-C r8 items 7 and 8 (`snapshot-plan-c/PROPOSAL-r8.md`:405-466);
- C2PM-1 (`snapshot-plan-c/c2pm-1-r2/CONTRACT.md`, bound), whose body half is in the product.

## What to review

`SCOPE.md` gives the change table, the candidate's order (§2), LD-C2A1-1 to LD-C2A1-10, the control map, the mutations and five open questions. Judge:
1. **The bridge** (LD-C2A1-1): `AuthenticatedComponent` constructed only inside `crate::trust`; `Evidence::admitted_components` lending each verified component's own pair, borrowed and uncharged; the `cfg(test)` `TestComponent` running the real body validation. Judge the reader choice (the full ordinary reader, not the current-trust inventory reader's `InventoryBody`) and Q-C2A1-5.
2. **The platform join** (LD-C2A-3, NBO-1): the selected row, the catalog's four tokens (pinned to `recovery_catalog.rs`), the same release's artifact, the catalog token as the closure's platform, and core spellings refused.
3. **The kind and the projection** (LD-C2A-2, SL:41-48): CR-1's table only; `type=file` rows only; the two visits and their price (LD-C2A1-5, Q-C2A1-2).
4. **The charged merge sort and the duplicate pass** (R3-RF-2, NBO-2): one edge before each comparison, `Budget` before an unfunded one, the n·⌈log₂ n⌉ reference price, r3's old estimate sufficient, the one-short allowance refused, n < 2 at zero.
5. **C2PM-1** (LD-C2A-11): the presence check; the four guards in order; guard 3 over the admitted descriptor as a host bug; the role support table with no numeric union or cross-role equivalence; the analyzer seam with no production constructor (LD-C2A1-3, Q-C2A1-3); the exact `protocolMajor` copy, never from `providerProtocol`; the carried origins (LD-C2A1-4); the placement of `Encoding` and `Field` between guards 2 and 3 (LD-C2A1-2, Q-C2A1-1).
6. **The descriptor and its encoder** (R3-RF-1, NBO-1): D predicted by LD-C2A-3's formula and bounded before any charge or allocation; one `Vec::with_capacity(D)`; the production check of length and capacity only, with `canonical_bytes` equality a control; `from_json` under the scoped exception; the id charged before it is copied.
7. **The published prices** (LD-C2A-10, LD-C2A1-6): each a `const fn` or constant from `size_of`, charged before its work, and the funding controls (exact, one byte or object short at the descriptor, one object short at the id, aggregate exhaustion in the second component).
8. **The labelled legs** (LD-C2A1-7, Q-C2A1-4): the unreachable `maxItems` and upstream legs, and the 4 MiB boundary at the encoder's edge.
9. **The lane** `evidence/c2a1-checks-r1/`: security 1198 → 1212 (+14) and host 412 → 412 (+0) with equal failure sets; Clippy, rustfmt (lib.rs base-dirty, append-only), the workspace and feature checks, the release build, the focused tests, the environment exceptions, operability with an unchanged mint audit, the unchanged census closure and verify_design; 26 mutations, all caught.
10. **Rules:** no new mint-census call, no environment read, no `let _ =`, no signing or private test key read, no new key, root, role or feature, no production caller.
11. **Inventory:** three new rows, no realized planned row; the successor numbered at integration from the lock's last plus one (v223 or later).

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `C2A1-R1-RF-n` / `C2A1-R1-NBO-n`. For each open question, say whether it is a finding.
