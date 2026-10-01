Grok law review: two linked amendments, reviewed together.
- **Law 463 r9:** the `InitialCore` bootstrap envelope set.
- **Law X4B r5:** first trust acceptance from the embedded bootstrap payload.

Claude Opus 5.5 leads, and you are the single reviewer. Make no repository edits, commits or pushes, and delegate nothing. Write only under `/tmp/opensip-implementation/reviews/grok-initial-core-463-r9-trust-bootstrap-x4b-r5/`. This is a law review: run no product cargo. The lead keeps the native lane.

## Subjects
Paths are under `/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/`.
1. `initial-core-launch-463/PROPOSAL.md`, r9, sha256 f47c22c0f5c1552b4016cb8eb08349da5d5aa5df9ded1e3b4598b4b18df68b6f, 23367 bytes.
   - Accepted r8 is preserved as `PROPOSAL-r8.md`, sha256 a5bc3b60337b25aa36d2eb8a77b938f32efa934ec67a3f04719915bca4d6dbcf, 17910 bytes. That equals the `subjectSha256` of `reviews/grok-initial-core463-r8/review.json`.
   - The live r8 file differed from the snapshot only by its "r8 ACCEPTED by Grok 463 r8 on 2026-09-26." note, which r9 keeps.
2. `trust-bootstrap-x4b/PROPOSAL.md`, r5, sha256 97c2eef3f0ad374b2004ce31d0c34fc593cba5de321f926cfe2d83aff77229a3, 21552 bytes.
   - Accepted r4 is preserved as `PROPOSAL-r4.md`, sha256 a2fe66a320951e120735d658a517e2ca646abb20392f96884a5b87e441efea50, 17463 bytes. That equals the `subjectSha256` of `reviews/grok-trust-bootstrap-x4b-r4/review.json`.

## Why: a contradiction between accepted laws, found while implementing X4B-a
- Law 463 r8 item 9 requires that the bootstrap's `members.envelopes` pair one-to-one with the root-chain bodies plus the revocation body, and refuses any other listed envelope. The product enforces it in `crates/security/src/trust/initial_core.rs`: F9, then the `BootstrapEnvelopeSet` check.
  - So a release that `InitialCore` admits carries no TR-INDEX-signed catalog and no TR-COMPONENT-signed component manifest.
  - The test release builder (`core_authentication.rs`, `tests::signed_release`) uses an unsigned `catalog-placeholder`.
- X4B r4 item 2 takes exactly that payload. Item 5 requires a catalog `MetadataAdmissionNodeV1`.
- The selected trust-record schema (`tools/security/inputs/trust-record-schema.json` in the product) requires a catalog in two places:
  - `AcceptedHeads.catalog`, as version, document and admission;
  - `PayloadMetadataClosureV1.catalog`.
- X4T r9 items 1 to 3 open `heads.catalog` and reverify its envelope as a catalog (`open_heads` in `current_trust_admission.rs`). X4T's continuation join refuses an index or component role that is not trusted.

So X4B r4 could write no shape-valid retained capsule from a real release, and its item 10 first case could never pass. The lead's recommendation was taken as a lead decision under the owner's standing direction: amend 463 so the bootstrap may carry these documents, and have X4B carry TR-INDEX and TR-COMPONENT.

## Changes
**463 r9**
- The header gains the r9 note, covering:
  - the contradiction;
  - the rejected alternatives: a second payload source, unsigned placeholders, and not carrying TR-COMPONENT;
  - the release-embedding format change, with no shipped artifact affected (no owner-signed release exists).
- Item 2 gains a store bullet: when item 9 admits it, the catalog pair, plus each `members.manifests` body with its envelope.
  - They are read by the same no-follow opens and judged by the same custody predicate, then held and rechecked.
  - They stay within `MAX_MEMBERS` and `MAX_MEMBER_BYTES`.
  - `InitialCore` makes no trust decision on them.
- Item 2's "Nothing else is stored" sentence is annotated.
- Item 9 is restated with a new body set: root-chain bodies, the revocation body, every component-manifest body, and the catalog body when one envelope for it is listed (at most one).
  - It must biject with `members.envelopes` by carrier stored digest. Anything else is `BootstrapEnvelopeSet`.
  - The signing role is not judged here.
  - An r8-shaped release still passes.
- A new closing section, "r9 code successor", names unit 463h and records the contract check: no contract successor is needed.

**X4B r5**
- The header gains the r5 note.
- Item 2:
  - names the catalog and component-manifest pairs that `InitialCore` retains as the source;
  - reverifies them under TR-INDEX and TR-COMPONENT against the payload's final root, with the embedded revocation keys excluded;
  - refuses a bootstrap without a catalog as `PAYLOAD-NOT-ADMISSIBLE` (subject `catalog`) before any write.
- Item 4 states the carried roles:
  - core from the inventory;
  - bundle from the manifest;
  - index from the catalog;
  - component from the component manifests: one `PresentOrdinary`, and only when at least one is listed.

  TR-PROFILE and TR-REPAIR are not carried. With no component manifest, TR-COMPONENT stays `Unbootstrapped` and the confirming admission refuses as `component:unbootstrapped`.
- Item 7's authentication row names these failures.
- Item 10's first case now expects:
  - core, bundle, index and component `ST-TRUSTED`;
  - profile and repair `ST-UNBOOTSTRAPPED`;
  - standing `InstallGateRequiredForNewProcess`.

  Three cases are added: no catalog, a wrong-role signature, and no component manifest.
- Item 11: X4B-a depends on 463h.

Diff each subject against its preserved snapshot, and confirm that nothing else changed.

## Decide
For each law: is the amendment consistent with the other accepted laws? Check S4 step 2, X4T r9 items 1 to 3 and 10, law 462, law 467, the trust-record schema, and the product code it cites. Is the contract check correct? Is anything new wrong?

In particular:
1. Does 463 r9 item 9's body set keep the pairing closed and the store exact?
2. Is "no trust decision in `InitialCore`" consistent with items 4, 5 and 8?
3. Is X4B r5's no-catalog refusal the right existing row?
4. Is one `PresentOrdinary` for TR-COMPONENT over all listed manifests consistent with `role_machine::decide`?

## Output
Write REVIEW.md and review.json. Do not commit.

review.json carries one verdict per law:

```json
{
  "laws": {
    "initial-core-463-r9": {"verdict": "ACCEPT|REQUIRED-FINDINGS", "requiredFindings": [], "subjectSha256": "f47c22c0f5c1552b4016cb8eb08349da5d5aa5df9ded1e3b4598b4b18df68b6f"},
    "trust-bootstrap-x4b-r5": {"verdict": "ACCEPT|REQUIRED-FINDINGS", "requiredFindings": [], "subjectSha256": "97c2eef3f0ad374b2004ce31d0c34fc593cba5de321f926cfe2d83aff77229a3"}
  }
}
```
