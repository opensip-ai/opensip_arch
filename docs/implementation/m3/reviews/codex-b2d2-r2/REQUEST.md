# Review request: B2-D2-r2, round 2 (host-side framework recognition; M3-B unit B2-d, sub-unit B2-d2)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b2d2-r2/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 store.
- Do not use other panes and do not delegate.
- **Permitted:**
  - read-only reading, hashing, JSON parsing and Git queries;
  - in the candidate worktree, `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B tools/host/framework_recognition_vectors.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip`;
  - in the candidate worktree, `python3 -I -B tools/tests/test_discovery_fw01.py`;
  - loading the bound B2-d0 reference read-only (`load(arch, packages)`) to try inputs.

## Subject

- **Manifest:** `docs/implementation/m3/config-discovery-b/b2-d2-r2-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 16009 bytes, SHA-256 `34aaf0b29b3f4ddfe293843d6ddf84db6fdaa36fd5f1c93e8fdb4b4ca30b3e16`, 67 members. Rehash every member.
- **Bases:** product main `86cf86432b22bf52d8a861d9aedbd71ed211a99a`, clean (B2-d1 and inventory v210; 171 contract successors); architecture `f8576e5c82378df3318a05bc0fed6ed4854653d8`.
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-b2d2`, detached at the product base, holding the exact bytes `product-map.json` lists.

## Authority

- **The B2-d plan r3,** sections 3 and 4 (your `codex-b2d-plan-r3`), with its Q1 to Q3 settlements.
- **The bound B2-d0 reference** (your `codex-b2d0-reference-r4`), including the carried B2D0REF-R3-NBO-1 and R4-NBO-1. The reference is `recognize`, `unit_recognition`, `cargo_workspace_fact` and `discovered_provenance`, together with the model's `recognize_frameworks`.
- **B2-d1** (your `codex-b2d1-r1`).
- **Law M3-B r9 items 15 and 16;** NE §8.
- **Product:** `crates/identity/src/closure.rs` (the `recognitionId` check), `schemas/sources/framework-recognition-plan-v1.schema.json` and the generated `RecognitionPlan1*` types.

## Round 1

Your `codex-b2d2-r1` returned three findings, B2D2-R1-RF-1 to RF-3:
- **RF-1:** the evidence-bytes preflight;
- **RF-2:** real schema admission;
- **RF-3:** the TOML profile and recursion controls.

The round-2 package is `b2-d2-r2/`; round 1's, `b2-d2-r1/`, is history. Its `SCOPE.md` "r2 changes" table maps each finding to its fix, controls and mutant. The tests are now nine and the mutations twelve. Lane r2's attempt 1 failed only on Clippy's `collapsible_if`, and attempt 2 is the lane of record.

## What to review

0. **The three findings.** Is each one resolved, with no new defect? Look closely at:
   - the preflight's order and the error it names;
   - the admission entry (`opensip.product.framework-recognition-plan.1#/$defs/UnitRecognitionV1`) and its budget;
   - whether keeping the recursion cases product-only, with stated expectations, separates them correctly from the reference-equal vectors.

`SCOPE.md` describes the unit. Judge:
1. **Equivalence.** Is `framework_recognition.rs` the reference rule for rule? Check:
   - each recognizer's trigger, evidence path and field, assurance, effects, unresolved choices and order;
   - exact JSON admission versus the model's `C.parse`, including non-objects, floats and duplicate keys;
   - the JSONC check and its 64 KiB bound; the YAML subset; the TOML tables, inline tables included;
   - route selection; the configuration orders; hints;
   - the sort; FR-4's structural and per-unit entry bounds; the FR-2 explicit override and the FR-1 state rule;
   - every evidence hash taken over the bytes.

   Construct inputs where the Rust and the reference might differ, and run them against the reference.
2. **Identity and shape.** Does `unit_recognition`'s `recognitionId` equal what `closure.rs` checks? Does admission by the generated type (canonical bytes, then `serde_json`) prove schema validity?
3. **Inputs.** Is the input contract sound for J1? That is: member paths, the bytes of each of the fifteen evidence files present, and explicit entry points that are absent or a carrier-won list. Is refusing a present evidence file without bytes right?
4. **The vectors and tests.** Are 49 unit, 12 bound, 7 fact and 3 provenance cases adequate? Is the carried NBO, the explicit-non-empty single-result overflow, now covered? Are the direct bound tests and the canary control right?
5. **FW-01:** the recognizers covered and pure.
6. **Evidence:** host 8 = 8 with nine new tests; Clippy and rustfmt; the twelve mutations; verify_design. Also the mint and environment rules: `as` casts only, no forbidden constructor names, no environment read.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `B2D2-R2-RF-n` / `B2D2-R2-NBO-n`.
