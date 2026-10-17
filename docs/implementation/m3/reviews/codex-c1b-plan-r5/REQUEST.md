# Review request: C1B-PLAN-r5 (the VCS observation plan, M3-C r8 item 4 with VCS-1 and M3-B successor S4), round 5

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-c1b-plan-r5/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds, lanes, the evidence scripts or the scratch program.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries.

## Subject

- **Manifest:** `docs/implementation/m3/snapshot-plan-c/c1b-plan-r5-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 3276 bytes, SHA-256 `02575ae6857e4172e911de083d06b78493b77bf659161ae977c6d653187111ec`, 15 members:
  - `c1b/PLAN-r5.md`, the subject;
  - `c1b/r5-evidence/vcs_term_r5.py` and `.output.json`, r5's derivation with the record's canonical length;
  - `c1b/r5-evidence/record-size-check/` (`Cargo.toml`, `Cargo.lock`, `src/main.rs`, `run.log`), the scratch check of the record formula against the real canonical encoder and the identity registry, run under the lane lock;
  - `c1b/PLAN-r4.md` and `c1b/r4-evidence/` (four files), round 4's subject, unchanged;
  - `c1b/PLAN-r3.md`, `PLAN-r2.md` and `PLAN-r1.md`, history and unchanged.

  Rehash all of them. The r4 members must equal `c1b-plan-r4-subject.json`'s pins.
- **Bases:** product main `813d559` and architecture `fa875bfd`, as the manifest names. Round 4's evidence was built on product `caa71e2`; C1c-0 has integrated since (`813d559`), and r5's derivation runs on `813d559`. The scratch program's identity dependency is the C1b-1 worktree's `crates/identity`, which `git diff caa71e2 813d559 -- crates/identity` shows unchanged.
- **Your round 4:** `codex-c1b-plan-r4` (REQUIRED-FINDINGS: C1BPLAN-R4-RF-1, with rulings on Q6 and Q7), at `/tmp/opensip-implementation/reviews/codex-c1b-plan-r4/`.

## Authority

As in rounds 1 to 4, and also:
- **The canonical encoder:** the product's `crates/identity/src/canonical.rs` (`encode`, `Encoder::string`), and C1a3's `string_len`/`push_string` in `crates/host/src/snapshot_seal.rs`:133-165;
- **`LogicalPath`:** `crates/identity/src/descriptors.rs`:31-62 and identity-v3's `$defs/LogicalPath`, `vcs-observation-v3` and `vcs-member-observation` (`schemas/sources/identity-v3.schema.json`);
- **the cumulative subtotal:** C1c-0's accepted retention evidence (`docs/implementation/m3/snapshot-plan-c/c1c-0-r2/evidence/c1c0-checks-r2/retention-cap-evidence.json`; C1c-0 r2, Codex ACCEPT-UNIT);
- **the method:** C2a plan r4's size derivation (`docs/implementation/m3/snapshot-plan-c/c2a/PLAN-r4.md`:113-119) and its scratch check (`c2a/evidence/size-check-r3/`).

## What to review

`PLAN-r5.md` opens with an r5 changes table. Judge:
1. **R4-RF-1, the record's canonical length** (LD-C1B-6):
   - the formula: 167 + Σ(91 + e(Pᵢ)) + (n − 1) for schema 3, with schema 2 fixed at 190 (`git`) and 154 (`none`);
   - e(·) as the encoder escapes;
   - the largest e(P) of 24,496 over `LogicalPath`'s scalar and segment bounds, by the exhaustive separator count;
   - the maximal record of 1,573,798 bytes;
   - the scratch check's cases and its result in `run.log`, including the registry's admission of the maximal record.
2. **The ownership:** one owned buffer of the exact length, the member paths borrowed, the commit ids retained and charged by C1b-1, no temporaries, and equality with `canonical_bytes`, or `Internal`.
3. **The re-run on `813d559`:**
   - the cumulative subtotal, r9's plus C1c-0's retention term;
   - D* = 226 and H* = 1,048,575, unchanged;
   - the corrected term, totals and residual margin in `vcs_term_r5.output.json`;
   - that the caps and the law gate are unaffected.
4. **The added encoded-length and allocation controls,** for C1b-1 and C1b-2 (§4).
5. **The adopted qualifications** of your Q6 ruling and disposition 4 (LD-C1B-2, LD-C1B-6, §7):
   - D* and H* as evidence-envelope coordinates;
   - the 4 MiB cap acknowledged as `HEAD`'s length bound and distinct from a 2× fit;
   - r9's guarantee conditional on all work that is not a row together;
   - exhaustion possibly before classification, with no partial observation;
   - the member projection of `ref-name`.
6. **No regression** in what rounds 1 to 4 found sound.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `C1BPLAN-R5-RF-n` / `C1BPLAN-R5-NBO-n`.
