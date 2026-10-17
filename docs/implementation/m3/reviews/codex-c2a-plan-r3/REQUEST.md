# Review request: C2A-PLAN-r3 (the C2a implementation plan: closure admission and the core role closures; M3-C r8 items 7, 8 and 9), round 3

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-c2a-plan-r3/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes.
- No network.
- Do not read the private 413 fixture, the installation directory, **signing keys or private test keys**, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries. You may check the size arithmetic by hand or with inert JSON, but do not run the scratch program.

## Subject

- **Manifest:** `docs/implementation/m3/snapshot-plan-c/c2a-plan-r3-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 1775 bytes, SHA-256 `4c02809d2000e6a582c1c89623af24112abfaf02a1069e80c1a9da5c8e64f7cf`, 8 members:
  - `c2a/PLAN-r3.md` (the subject);
  - `c2a/PLAN-r2.md` and `c2a/PLAN-r1.md` (history);
  - `c2a/X-C2A-1-r1.md` and `c2b/C2B-GATING-r1.md` (context);
  - `c2a/evidence/size-check-r3/{Cargo.toml, src/main.rs, run.log}`: the scratch program that checked the size formula against the real `opensip_identity::canonical_bytes`, and its output. This is evidence, not product code.

  Rehash all eight.
- **Bases:** as the manifest names (product `b753854`, unchanged from round 2).
- **Your round 2:** `codex-c2a-plan-r2` (REQUIRED-FINDINGS: R2-RF-1, R2-NBO-1, R2-NBO-2, the Q5 and Q6 rulings), at `/tmp/opensip-implementation/reviews/codex-c2a-plan-r2/`.

## Authority

As in round 2. In addition:
- `opensip/crates/identity/src/canonical.rs` (:5, :267-312, :315-350);
- `crates/identity/src/digests.rs` (:52-66);
- `crates/identity/src/descriptors.rs` (`IdentityDomain::Closure`, :486);
- `crates/host/src/snapshot_seal.rs` (:36, :390-394), C1a3's accepted admission precedent;
- `crates/evaluator/src/native_context.rs` (:189-223).

## What to review

`PLAN-r3.md` opens with an r3 changes table. Judge:
1. **R2-RF-1** (LD-C2A-3, LD-C2A-10):
   - the corrected Blob size of 96 + d(N) + e(P), and the descriptor size of 175 + … + max(n − 1, 0), with e(·) defined from the encoder's escaping. Check them against the encoder source and the recorded run;
   - that the prediction runs before encoding, with an `Encoding` refusal before allocation;
   - the published `WorkCost` prices for every owned representation: the Blob objects and maps, the tree array, the in-place sort's edges, the descriptor members, the encoder's growth-bound buffer, the admission and identity under `SCHEMA_BUDGET` by the C1a3 precedent, the id string, and the kernel's digest work;
   - that borrowed trust evidence is not charged again;
   - the new predicted-versus-encoded vectors.

   Are the conservative std-derived prices (`size_of`, the B-tree capacity of 11, the doubling bound) acceptable as published prices, or must any be exact?
2. **R2-NBO-1** (LD-C2A-1): row 8 adds no new component-manifest admission and never re-verifies a signature; downstream re-admission and the retention or I/O failures stay at their owners; and the post-draw promised-object control.
3. **R2-NBO-2** (LD-C2A-12): the `AdmittedClosure` sum type with a separate authenticated-core constructor, and core roles needing no delivery law or fixture root.
4. **The Q5 ruling** applied: D4's and J1's production work profile as a named gate of C2a-4; test scopes identified as such.
5. **The Q6 ruling** applied: C2a-1, C2a-2 and the pure kernel C2a-3k staged early with no production authority, while C2a-3's production constructor and C2a-4 wait.
6. **No regression** from rounds 1 and 2.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `C2APLAN-R3-RF-n` / `C2APLAN-R3-NBO-n`.
