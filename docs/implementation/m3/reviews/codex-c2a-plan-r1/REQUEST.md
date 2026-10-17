# Review request: C2A-PLAN-r1 (the C2a implementation plan: closure admission and the core role closures; M3-C r8 items 7, 8 and 9), round 1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-c2a-plan-r1/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes.
- No network.
- Do not read the private 413 fixture, the installation directory, **signing keys or private test keys**, held trees, any T2 store or the T2 cache. Cite fixture signers by their source names (for example `INDEX_SIGNER`); never open key material.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries.

## Subject

- **Manifest:** `docs/implementation/m3/snapshot-plan-c/c2a-plan-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 577 bytes, SHA-256 `70a44150f3428325f0733f4692beedc126b767d509807faf860d3cc9d3c299d4`, 2 members:
  - `c2a/PLAN-r1.md` (the subject);
  - `c2b/C2B-GATING-r1.md` (the gating record that names this unit, context only).

  Rehash both.
- **Bases:** as the manifest names (product `3d1d771`).

## Authority

- M3-C r8 (`docs/implementation/m3/snapshot-plan-c/PROPOSAL.md`):
  - items 7 to 9 (:409-557);
  - row 8's narrowing (:71);
  - the Units table (:1183).
- SL:21-60 and IE:272-285 (`docs/v2/contracts/product-v1/`).
- The identity schema's `closure` (`opensip/schemas/sources/identity-v3.schema.json`:253).
- CR-1, CRC-1 and CRC-2 (bound).
- J1's R10a and ER10a (`host-pipeline-j/PROPOSAL.md`:394, :406-411), and M3-D item 24.
- X4B (`docs/implementation/m2/trust-bootstrap-x4b/PROPOSAL.md`).
- The product code the plan cites (`opensip/crates/security/src/component_manifest.rs`, `trust_ordinary_metadata.rs`, `trust/core_inventory.rs`, `trust/initial_core.rs`, `trust/core_authentication.rs`, `trust/native_census.rs`; `crates/evaluator/src/composition.rs`).

## What to review

1. **The split and its order** (§2): C2a-1 for identity and projection, C2a-2 for the synthetic generator, and C2a-3 for retention, which is gated.
2. **Composition** (LD-C2A-1): C2a-1 consumes only the ordinary trust reader's verified components, after R10a, and never verifies signatures itself.
3. **The kind, the projection and the descriptor** (LD-C2A-2 to LD-C2A-4): is the platform spelling from the signed catalog's `artifacts[].platform` sourced and right? Is leaving `protocolMajor` open (Q2) correct, rather than guessing a manifest member?
4. **The retention gate** (LD-C2A-5, cross-law item X-C2A-1): is it right that no accepted law or code installs or extracts component trees, so whole-tree retention needs component delivery's owner (DR-103)? Is the interim fail-closed reading (Q3) lawful under item 7 and `PROPOSAL.md`:435-436?
5. **The synthetic generator** (LD-C2A-6): only the existing public test-only signers and synthetic root, under the joint fixture predicate, with no new key, root or role, and the release-build source pin. Is this how test signing is lawfully done in the existing X4B and 463 work (`core_authentication.rs`:563-600, :696-713; `native_census.rs`:648-651)?
6. **Item 9's legs** (LD-C2A-8): what remains for C2a (the C2-T9 vector check), and the field-use restrictions assigned to X12d, C4a and H. Is that mapping complete and correctly owned?
7. **Controls and mutations** (§4, §5) against C2-T1 to C2-T8, C2-T9 and C2-T18.
8. **Rule on Q1 to Q4.**

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `C2APLAN-R1-RF-n` / `C2APLAN-R1-NBO-n`.
