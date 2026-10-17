# Review request: CI r1, the law "component release installation and tree custody", round 1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-component-install-r1/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes. Do not take the shared lane lock.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, private test keys, held trees, any T2 store, the T2 cache or any held-out material.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries in both repositories.

## Subject

- **Manifest:** `docs/implementation/m3/component-install/proposal-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 579 bytes, SHA-256 `3a055f6d23ffc5b5580ec21d40261b1ff41213f874126aab624ae0c3942c42d8`, 2 members. Rehash both.
  - `docs/implementation/m3/component-install/PROPOSAL-r1.md` is the subject.
  - `docs/implementation/m3/snapshot-plan-c/c2a/X-C2A-1-r1.md` is the input memo. It is not law.
- **Bases:** as the manifest names, product main `b7538549` and architecture `a87c1234`.
- **Context:** you assessed the memo in `codex-c2a-plan-r2` (its RF and Q rulings, including Q5 and Q6), and ruled in `codex-c2a-plan-r1` (Q3). Nothing in the memo was pre-approved.

## Authority

- M3-C r8 item 7 (retention, the no-trust-view path) and item 8 (synthetic signed closures), in `docs/implementation/m3/snapshot-plan-c/PROPOSAL.md`.
- SL (`docs/v2/contracts/product-v1/security-and-lifecycle.md`): S1, the catalog and TreeCommitment identity projection at :30-48, the S7 lease and fence rules at :575-670, and S8's platform table at :700-711.
- WS (`workflows-and-surfaces.md`) :293-299 and :1374-1375; IE §5 and :1399-1411; NE :1493-1499.
- The packaging contract's archive profile, `docs/coop/artifacts/component-packaging-contract.v14.json` `archiveProfile` (standing CANDIDATE-NOT-APPLIED, DR-120), and the manifest schemas `component-manifest-schemas.v11.json`.
- The product's admitted manifest and catalog shapes: `crates/security/src/component_manifest.rs`, `generated/component_manifest_shape.rs` and `trust/recovery_catalog.rs`. Also the custody primitives it cites.
- The registered public codes: `docs/coop/design-corrections/workflows/schemas/common.schema.json` and `public-detail-registry.v1.json`.

## What to review

Judge whether this is a sound, narrow and implementable law, and whether it answers the gap. In particular:
1. **Scope and authority:** that the lead may own it as DR-103's delivery owner, and that its exclusions hold.
2. **Items 1 and 2:** what is installed; the source; exactly what `archiveDigest` and `sha256` hash, including LD-CI-1's `artifact-digest-split` rule; and LD-CI-2's platform-token lookup (Q2).
3. **Item 3:** adopting PKG-AP alone by pinned reference (Q6). Check that every limit is sourced as the table says, that no new constant is introduced (Q1), the hostile-input parsing bounded by signed data, LD-CI-3's capacity refusal, and the claim that no new dependency is needed.
4. **Item 4:** the offline handoff (Q3), with no network acquisition; the fence and trust instant; the stage, verify and publish transaction; and LD-CI-5's "nothing installed" rule, which explicitly covers existing published generations and partial staging.
5. **Item 5:** the store's location (LD-CI-7), custody, immutability, the generation record, retention by raw SHA-256 and `BLOB_LENGTH` through the materialized tree, and LD-CI-8's refuse-never-repair rule.
6. **Item 6:** whether the read interface is concrete enough for C2a-3 to bind, with no operational custody choice left frozen elsewhere: its typed failures, its charging, the work profile left to D4/J1, and the fixture path running the same installer and verifier.
7. **Item 7:** custody and immutability across R10a and Run retention (LD-CI-9, Q4); durable versus ephemeral.
8. **Item 8:** every route mapped onto existing codes only (Q5), with the durable and ephemeral failure routes.
9. **Item 9:** the units and controls.
10. **Q1 to Q7:** rule on each.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...], "questionRulings": {"Q1": "...", ...}}`, with ids `CI-R1-RF-n` / `CI-R1-NBO-n`. Accepting this law accepts no code, binding or qualification.
