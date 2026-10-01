Grok review: law X12 r1, configuration and policy-pack admission (release gate DR-G24, `host/src/configuration.rs` and `evaluator/src/policy.rs`). Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-policy-admission-x12-r1. Law review; no product cargo. Product HEAD is fc7dce7.

Subject: docs/implementation/m2/policy-admission-x12/PROPOSAL.md r1 (pin in hashes.txt). X5 r1 split DR-G24 out of X5; see `replay-join-x5/PROPOSAL.md` item 1.

Context:
- **Register:** DR-G24 (`08-decision-and-readiness-register.md` line 369) and DR-131 (line 320).
- **The DR-131 contract:** `docs/coop/artifacts/preview-analyze-contract.v2.json`, sections `$.pack`, `$.planIdMembership` and NT-1/NT-2.
- **The G24 artifacts:** the harness occupancy `harness.DR-G24.preview-analyze-well-formed-admission.preview.v3.json` and `g24-input-corpus.v1.json`.
- **The build plan:** lines 886, 887 and 1028.
- **Layout and evidence workflows:** `14-repository-and-module-layout.md` lines 364 and 478, and `13-evidence-workflows-and-product-contracts.md` §10.
- **Product contracts:**
  - admission-and-qualification §1, §1.1 and §5;
  - workflows-and-surfaces §5 and its D9 table;
  - native-evidence's invalid-capability-request route row and remedy-keying constraint;
  - `docs/coop/design-corrections/public-detail-registry.v1.json`;
  - the reference resolver `foundation/product-configuration-model.py` (`CONFIG_PACK_UNREGISTERED`).
- **Accepted laws:** X5 r2 and 468 r5 item 6.
- **Product:** `crates/evaluator/src/policy.rs`, `atom-registry.json`, the identity-v3 `analysis-spec.policyPackIds`, and the generated `Common4*` enums.

The lead decisions to check:
1. Scope is pack admission only.
2. "Bundled" means an `include_bytes!` registry in the evaluator.
3. A pack ID is spelled `name:version`.
4. The release registry has zero rows in M2, because the DR-131 rule IR is not frozen; tests use a `cfg(test)` synthetic pack.
5. The input is an inert `PackSource` with a refuse-only `Supplied` variant, and the result is an opaque `AdmittedPack`.
6. Item 7's rows reuse existing codes only.
7. Admission is pure and runs before all custody and evaluation. This includes the EXIT-PLAN correction that X12 does not depend on X1.
8. `check_plan_pack` is provided but not wired into replay until M3 (X12d).

## Decide

Does every numbered decision match the design sources and the accepted laws? Are the lead decisions sound, each with its rejected alternative? In particular:
- Is a zero-row release registry with a `cfg(test)` pack a lawful M2 state for DR-G24?
- Is `name:version` a lawful use of the existing `packIds` and `policyPackIds` carriers that invents no PlanId recipe?
- Are the item 7 rows right? Check them against admission-and-qualification §1 (external input versus host-generated layer), the native unregistered-capability precedent and the public detail registry.
- Is deferring the replay join to X12d safe, given that X5 commits caller-supplied candidates?
- Do the tests cover NT-1 (both limbs), NT-2 and the four corpus initial states?
- Are the units and successors right?
- Is anything else wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256" (the PROPOSAL.md sha256 in hashes.txt). Write REVIEW.md and review.json. Do not commit.
