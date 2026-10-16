Codex review: the B2-d implementation plan r1 (framework recognition host side, the closed YAML subset reader, and the recommendation evidence; M3-B items 16 and 18). A **plan review**. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only `REVIEW.md` and `review.json` under /tmp/opensip-implementation/reviews/codex-b2d-plan-r1.

**Rules:**
- Read-only: no repository edits, commits, pushes or delegation.
- No product build, test, generator or census run. Reading, hashing and `git show` / `git diff` are fine.
- Never touch `~/Library/Application Support/OpenSIP`, the private 413 UUID fixture, signing keys, or any T2 store or overlay.
- No network.

## Subject

- **Subject manifest:** `docs/implementation/m3/config-discovery-b/b2-d-plan-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted), SHA-256 `22709600ab21e0b6a6e8d8722ccad7c99dad759964955d5d21f0393000236adf`. It pins `b2-d/PLAN-r1.md`.
- **Bases:** product `/Users/sb/code/opensip-ai/opensip` at main `a50ae96` (clean); architecture at `4415adb5051de65c8e2b0e0ce493d1a59f2941c6`.

## Authority to check the plan against

- **Law M3-B r9** (`config-discovery-b/PROPOSAL-r9.md`): items 15 to 18, line 204, and "Units after the law" (the B2-d row).
- **NE §8:** `docs/v2/contracts/product-v1/native-evidence.md:2749-2777`.
- **CH13:59-75:** `docs/v2/architecture/13-evidence-workflows-and-product-contracts.md`.
- **The B-S9 native reference model,** contract successor 81: `config-discovery-b/b-s9/reference/native_evidence_model.py`, `recognize_frameworks` and `FRAMEWORK_HINTS`.
- **The unaccepted owner proposal S1** (FR-6 to FR-8): `docs/implementation/m1/trials/report-evidence-design-02/subject/owner/native-recognition-successor.v1.json`, and Grok's review stating S1 to S4 are unaccepted.
- **Product:**
  - `schemas/sources/framework-recognition-plan-v1.schema.json` and the generated `RecognitionPlan1*` types;
  - `crates/identity/src/closure.rs` (the `recognitionId` check);
  - `crates/host/src/configuration.rs` (`resolve`, `ProvenanceSourceV1`) and `schemas/sources/product-configuration-v2.schema.json` (the `discovery` section);
  - `crates/host/src/discovery.rs` and `jsonc.rs`;
  - `tools/host/dependency-policy.json` (M3-P0).

## Decide

1. **Coverage.** Does the plan cover everything item 16, item 18 and the B2-d row assign: the nine recognizers, FR-1 to FR-5, the readers, the YAML subset, the recommendation evidence and its resolver check, and the item 15 and 16 controls? Does it take nothing assigned elsewhere (C1 and J1 reading, C4 commitment, the provider side, M4)?
2. **B2-d0** (section 1): a wrapper over the B-S9 model with exactly four changes. Are they right? Are the two new disclosure strings (`Cargo.toml-not-toml`, `tsconfig-not-jsonc`), which mirror the model's `package.json-not-strict-json`, acceptable? Is a contract successor the right binding?
3. **LD-B2D-1, the YAML subset** (section 2). Is the grammar exactly item 16's "a `packages:` sequence of plain or quoted scalars only"? Is treating other top-level keys as outside the subset the right reading?
4. **LD-B2D-2, FR-4.** Should the entry-point bound be a disclosure (no truncation, no refusal) or a refusal? Is it acceptable that the other two bounds are assertions?
5. **Q1, LD-B2D-3, FR-2** (section 4). Is the reading within item 16? It declares recognition effects through `FrameworkRecognitionPlanV1`, with provenance as recognizer id and version, lets explicit `discovery.entryPoints` win per unit, and leaves the resolver's discovery fold empty. Or is a law clarification needed first?
6. **Q2, paths.** Unit-root-relative paths, as the reference emits them, while the schema's PROPOSED path note asks for repository-relative ones.
7. **Q3 and section 5.** The recommendation evidence: its five parts, the proposed settings (with none for `workspaceRoots`), the actual-resolver round trip, and an internal type with no schema record at M3.
8. **Order and gates** (section 6), and anything else that blocks acceptance.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `B2DPLAN-R1-RF-n` / `B2DPLAN-R1-NBO-n`.
