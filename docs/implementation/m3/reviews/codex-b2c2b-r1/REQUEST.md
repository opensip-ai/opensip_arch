# Review request: B2-C2B-r1 (item 14a's record bounds and the S10b remedy carrier; M3-B r10)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b2c2b-r1/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 store.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries; in the candidate worktree, `python3 -I -B tools/host/typescript_config_vectors.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip` and `python3 -I -B tools/tests/test_discovery_fw01.py`.

## Subject

- **Manifest:** `docs/implementation/m3/config-discovery-b/b2-c2b-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 7944 bytes, SHA-256 `4260206becd3d5b5f2c15ee53451908ff3563daf7326e1cd20c096f4992d6b87`, 34 members. Rehash every member.
- **Bases:** product main `00ec6492c673c67399ab740bcb4acfda4a33184d`, clean (S10b bound; 172 contract successors; inventory v212); architecture `6d360470b303feec780249644ac8a836b063317f`.
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-b2c2b`, detached at the product base, holding the exact bytes `product-map.json` lists.

## Authority

- **Law M3-B r10** item 14a (`config-discovery-b/PROPOSAL-r10.md`; your `codex-m3b-r10-r2`): the "Bounds" bullet, the `bound` row, termination step 3, the r10 controls, and the check order in the "r10 changes" section.
- **S10b** (contract successor 172; your `codex-s10b-remedy-r1`) and its LD-S10B-1: B2-c2b writes the product carrier.
- **B2-c2 r2** (your `codex-b2c2-r2`): the walk order LD-B2C2-4 and O-1.
- **The record:** `$defs/TypeScriptConfigGraphV1` and `CanonicalPath` in `schemas/sources/native-v2.schema.json`.

## What to review

`SCOPE.md` describes the change and LD-B2C2B-1 and -2. Judge:
1. **r10's bounds.** Does `typescript_config.rs` refuse exactly as r10 says?
   - A node path over 4,096 characters, counted in characters, at that node, before its bytes are judged, the entry included.
   - An `extends` array over 64 entries, repetitions included, at that file, after JSONC and types and before any entry is classified or resolved.
   - Both as `native.typescript-config-bound`, in r10's order relative to the 32-node, 64 KiB and type checks.
   - Is LD-B2C2B-1 (one guard for path and bytes) unobservable as claimed?
2. **The reference reading.** Does the builder's Python reading implement the same rules independently? Do its eleven new controls cover r10's control bullet: at and one past each bound, the refusal before any entry resolves even with a malformed specifier or missing base, the wrong-typed entry still malformed, and a non-ASCII path?
3. **Schema admission (LD-B2C2B-2).**
   - Are every replayed graph's admission by the embedded schema and the new bounds test sound?
   - Are the constants tied to the schema's numbers?
   - Is one past each bound refused by the schema?
4. **The S10b carrier.** Is `REMEDY_TYPESCRIPT_CONFIG_UNRESOLVED` S10b's string byte for byte? Are the vectors' `d9.remedy` and pins S10b's and r10's, with S10's registry and alias rows unchanged? Is row 59 still tied to the model?
5. **O-1.** Is it closed: is every graph the reader admits an admissible `TypeScriptConfigGraphV1`?
6. **Evidence.**
   - Host 8 = 8 with one new test, Clippy and rustfmt;
   - the vector checks, FW-01, the environment exceptions, the operability census and verify_design;
   - the seven mutations;
   - the mint and environment rules.
7. **Inventory.** No new paths. Is the plan for a description successor of the four rows `SCOPE.md` names right, and are any other rows now false?

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `B2C2B-R1-RF-n` / `B2C2B-R1-NBO-n`.
