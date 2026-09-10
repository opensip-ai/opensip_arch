I’ll trace the exact catalog/release/closure admission path that binds `closure2` identity (tree, platform, protocol) to `manifestDigest` bytes, then write only the v6 assessment.I'll continue the bounded trust-join assessment from the current root sources: identity §3, delivery selectors, and W v11 projection, then write only v6 reports.The workspace is `grok-atom-contract.v1`; I'll read the current prompt, v6 join reports, and successor sources so the assessment uses live files.The live task is the v6 trust-join question. I'll read that prompt, the v5 proposal, and the identity/delivery/W sources next.I'll locate the live identity, catalog, detector-manifest, delivery, and W v11 binding points, plus the root SEAL prefix change.The broad find is too slow; I'll read identity §3, catalog/envelope schemas, and W projection next, then search v11 on a narrower path.The isolated tree cites v11 but does not contain it. I'll hash the live cited file, then read delivery, registry, and the security chapter.The binding owner is the DR-103 component manifest plus `closure2`, not DetectorManifestV1. I'll add one security-chapter paragraph and write only the v6 reports.W v11 moved under root while I was reading it. I'll re-read the live detector projection before locking the report hashes.**Finding:** trust-trio admission binds this `closure2` / tree / platform / protocol to the **component-manifest** bytes, not to `DetectorManifestV1`. The listing inherits those coordinates only **after** that association, via the admitted `closure2` plus a closed host receipt. `host.closures[].trust='admitted'` is TCB, not the delivery selector.

## What is already bound

Identity `closure2` is `H(kind, manifestDigest, tree, semanticVersion, protocolMajor, platform)` (`identity-and-evidence.md` §3; `identity-schemas.v3.json` `$defs/closure`). Swapping tree with the same digest **must** mint a different id.

`closure.manifestDigest` is raw SHA-256 of the admitted **component** manifest body (envelope excluded). The signed association of those bytes is already owned:

| Selector | What it binds | `closure2`? |
|---|---|---|
| Envelope.2 `kind=manifest`, domain `opensip.metadata.manifest.1` | stored/preimage of DR-103 body | no |
| Catalog.1 `releases[]` `{manifestDigest, envelopeDigest, artifacts[{platform, archiveDigest}]}` | release + per-platform archive | **no** |
| DR-103 v11 `platforms[]` `{os, arch, tree: TreeCommitment, entrypoint}` + RJ-3 | selected tree/platform/component | delivery refuse |
| Workflows §2 trio | retained generation / installed signed release **with the same `closure2`** / signed `closureBundle` | yes |

Identity §3’s “refused by delivery admission” sentence points at v11 `platforms[]` + RJ-3, not at the listing schema. Live cited v11 bytes match `1c0b8868…` (139492); that file is **not** in this isolated tree’s `docs/coop/artifacts/`.

## What is not bound

`DetectorManifestV1` is only `{schemaFamily, schemaMajor, compatibleClosures}` (`additionalProperties` false; sha256 `ce54903a…`). It cannot be the v11 body (required `platforms`, role, commands, …). Catalog, registry, envelope domains, v11 fields, lock tuples, and baseline `closureBundle` `{path, sha256, bytes}` do **not** list `compatibleClosures` or name `closure2` on a release row.

W still titles that listing as the `closure.manifestDigest` preimage. Root W v11 `project_admitted_detector_compatibility` has the receipt **shape** and copies `tree`/`platform`/`protocolMajor` from the **object-map descriptor** after TCB `trust='admitted'`. It still parses DetectorManifestV1 from `blobs[manifestDigest]`. This owner did not edit W.

`identity-model.v3` `raw-artifact` only checks `SHA-256(bytes)==digest`. It does not parse a component manifest and does not compare `closure.tree` to `platforms[]`.

**Tree-swap retaining listing bytes:** new `closure2`. Trio “same `closure2`” does not admit it. Delivery cannot read tree from a three-field body. The hole is a host that marks the new id `trust='admitted'` (fixture TCB) or treats catalog digest match as closure admission.

## Receipt (no second verifier)

After envelope + catalog + v11 + trio admit `closure2` *C*:

`{closureId, manifestDigest, admissionOrigin}` with `admissionOrigin` ∈ `retained-generation` | `installed-signed-release` | `signed-closure-bundle`.

Parse the single W listing **only** under that receipt, from bytes that are **not** `closure.manifestDigest`. Do not fork the W `$id`. Do not add `signatureVerified`.

## Design law vs TCB

- **Law:** `closure2` concatenation; component-manifest digest; v11/RJ-3 delivery refuse; trio keyed by that `closure2`.
- **TCB:** `verify_envelope` already-accepted signers; workflow `host.closures[].trust='admitted'`.
- **Not in the identity model:** tree vs `platforms[]`.

## This turn

One S1 paragraph in `security-and-lifecycle.md` (92851 bytes, `983a5a24…`). Reports: `grok-evaluator3-contract-joins.v6/trust-join-assessment.md`, `review.md`, `review.json`. Native/admission chapters unchanged. Official suites not run. SEAL adapter not re-run; root 9/9 with `_RUN3.fullmatch` and `prefix-trailing-newline-refused` is as read.
