# Review request: C2A-2-r2 (the shared synthetic component fixtures; M3-C r8 item 8, C2a plan r4 sub-unit C2a-2), round 2

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-c2a-2-r2/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, builds or the lane. The lane lock (`/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-lanes.lock`) is not yours to take.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, private test keys, held trees (E2s, J4a), any T2 store or the T2 cache. The module under review signs through the existing `sign` with the public test-only quorum62 seeds already in `core_authentication.rs`. Reading that public test code is in scope; no key file is.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries; in the candidate worktree, `python3 -I -B tools/check_operability.py source --repository .`.

## Subject

- **Manifest:** `docs/implementation/m3/snapshot-plan-c/c2a-2-r2-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 9287 bytes, SHA-256 `f190262afe305ec1eb05be4793eac9c23ce024fce85aa10fb202445f31f7b452`, 40 members. Rehash every member.
- **The candidate base:** product main `50f1ac1c9244681db87c2d2e62215dbca0846c48`, which holds C2a-1 r1 (your `codex-c2a-1-r1`, ACCEPT-UNIT; integrated at `e770404`), with the v223, v224 and v225 locks, D2b-3a and CI-1 since; none touches the candidate's paths.
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-c2a2`, detached at `50f1ac1`, holding the exact bytes that `product-map.json` lists (4 files, 2 new).

## Authority

- the C2a plan r4 (`snapshot-plan-c/c2a/PLAN-r4.md`; `codex-c2a-plan-r4`, ACCEPT), sub-unit C2a-2, LD-C2A-6 and the Q4 ruling;
- law M3-C r8 item 8 (`snapshot-plan-c/PROPOSAL-r8.md`:451-466), with C2-T6, C2-T7 and C2-T8's label half.

## Round 1

Your `codex-c2a-2-r1` (REQUIRED-FINDINGS) raised one finding, C2A2-R1-RF-1: JSON-escape the supplied tree paths and entrypoints. It also ruled Q-C2A2-1 and Q-C2A2-2 "not a finding". Its REQUEST, REVIEW.md and review.json are copied, byte for byte, into `docs/implementation/m3/reviews/codex-c2a-2-r1/` (uncommitted) and pinned in `source.json` with r1's subject.

**First judge RF-1's resolution** (SCOPE, "Round 2"):
- `body` and `release_row` now build every value as JSON and encode it through the identity crate's canonical encoder, so no supplied string is interpolated into JSON text;
- the `p1` bytes are unchanged;
- no ASCII restriction is imposed;
- the two new controls: the encoding and validation of escapable paths, and the escapable paths through the signed reader and candidate;
- the three new mutations.

Then confirm that nothing else changed from r1 apart from RF-1's changes and the base. r1's package is `snapshot-plan-c/c2a-2-r1/`; compare the product files.

## What to review

`SCOPE.md` gives the change table, LD-C2A2-1 to LD-C2A2-5 and the control map. Judge as in r1:
1. **The predicate** (LD-C2A2-1, Q-C2A2-2): the module included inside `core_authentication.rs`'s `tests` module, so under exactly `cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))`, with the crash-matrix site census unchanged; C2-T7's source pin; the lane's release build.
2. **Signers and root** (LD-C2A2-2): only `sign` with `COMPONENT_SIGNER` and `INDEX_SIGNER` under the existing synthetic root; no key, seed, root or feature introduced.
3. **Existing bytes** (LD-C2A2-3, Q-C2A2-1): `component_release` through `release_row` with `p1`, byte for byte; an empty `components` list unchanged; the existing suites' equal failure sets; `LABEL` on every row the module writes.
4. **Role validity** (LD-C2A2-4): every role's body passes the real body validation with C2PM-1's major 1 and CR-1's command, capability and permission rules; the tree is exactly the supplied bytes.
5. **C2-T6's leg** (LD-C2A2-5): the signed release of every role through the InitialCore, acceptance onto a P0 installation, the full ordinary reader over the accepted store, C2a-1's bridge and candidate for every role; nothing claims retention or admission.
6. **The lane** `evidence/c2a2-checks-r2/`: security 1240 → 1248 (+8) and host 412 → 412 (+0) with equal failure sets; Clippy, rustfmt (core_authentication.rs base-dirty and hand-edited, not reformatted), the workspace and feature checks, the release build, the focused tests, the environment exceptions, operability with an unchanged mint audit, the unchanged census closure and verify_design; 12 mutations, all caught.
7. **Rules:** no new mint-census call, no environment read, no `let _ =`, no signing or private test key read, no new key, root, role or feature.
8. **Inventory:** two new rows; the successor numbered at integration from the lock's last plus one, after the combined C1c-0 and C2a-1 v223 (so v224 or later).

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `C2A2-R2-RF-n` / `C2A2-R2-NBO-n`. Say whether C2A2-R1-RF-1 is resolved.
