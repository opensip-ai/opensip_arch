# Law review: 463 r9 and X4B r5

Both amendments are accepted. Together they close the contradiction the request describes: a release `InitialCore` admits may now carry one catalog pair and the component-manifest pairs, `InitialCore` still makes no trust decision on those pairs, and X4B verifies them before it writes a retained capsule.

## Subjects

| Law | File | Bytes | sha256 | Preserved snapshot |
| --- | --- | --- | --- | --- |
| 463 r9 | `initial-core-launch-463/PROPOSAL.md` | 23367 | `f47c22c0f5c1552b4016cb8eb08349da5d5aa5df9ded1e3b4598b4b18df68b6f` | `PROPOSAL-r8.md`, 17910 bytes, `a5bc3b60337b25aa36d2eb8a77b938f32efa934ec67a3f04719915bca4d6dbcf` |
| X4B r5 | `trust-bootstrap-x4b/PROPOSAL.md` | 21552 | `97c2eef3f0ad374b2004ce31d0c34fc593cba5de321f926cfe2d83aff77229a3` | `PROPOSAL-r4.md`, 17463 bytes, `a2fe66a320951e120735d658a517e2ca646abb20392f96884a5b87e441efea50` |

The r8 snapshot hash equals `subjectSha256` of `reviews/grok-initial-core463-r8/review.json` (ACCEPT). The r4 snapshot hash equals `subjectSha256` of `reviews/grok-trust-bootstrap-x4b-r4/review.json` (ACCEPT).

The 463 diff against the snapshot is the header (the r8 acceptance note the live r8 file already had, plus the r9 note), item 2's new store bullet and the annotated "Nothing else is stored" sentence, the restated item 9, and the new "r9 code successor" section. The X4B diff is the header (including the r4 acceptance note) and items 2, 4, 7, 10 and 11. Nothing else changed.

## What is consistent

S4 step 2 is unchanged in X4B item 3. A fresh install with no admissible payload still writes nothing. A missing catalog is not `TRUST.NO_ADMITTED_TIME_CONTEXT`: X4T r9 item 10 reserves that row for F absent and says it is used for nothing else. Once the catalog and component manifests verify, their issue times are verified-document times under the existing item 3 definition of A, and expiry still comes from the presented documents and is never set to false.

X4T r9 items 1 to 3 require `heads.catalog` in the retained closure and reverify that envelope as a catalog. `open_heads` in `current_trust_admission.rs` does that with `EnvelopeKind::Catalog` and `MetadataAdmissionNodeV1`, and a failure is `PAYLOAD-NOT-ADMISSIBLE` subject `catalog`. Item 10's continuation row is `component:` plus the role token; `token(Unbootstrapped)` is `unbootstrapped`. The schema requires `AcceptedHeads.catalog` (version, document, admission) and `PayloadMetadataClosureV1.catalog` as a `DocRef`. A capsule without a catalog is not a shape-valid retained record.

Law 462 still owns the profile set. Its files sit under the core tree root, not in the bootstrap payload, and 463 r9 does not open them. X4B leaves `TR-PROFILE` `Unbootstrapped`. That is the installation role, not the release root's `TR-PROFILE` standing that 462 consults. Law 467's P0 tree is the pre-acceptance publication X4B already succeeds; r5 does not change the publication protocol in item 5.

The product contradiction is as stated. `initial_core.rs` builds the body set from the root-chain digests plus the revocation digest, requires `members.envelopes` to have that same length, and removes each envelope's carrier stored digest (`BootstrapEnvelopeSet`). `signed_release` inserts `catalog-placeholder` and lists every `*.sig.json` as an envelope, with `manifests` empty, so an r8 release has a catalog member (the payload shape requires one) and no catalog envelope. `EnvelopeKind::Catalog` routes to `TR-INDEX` and `EnvelopeKind::Manifest` routes to `TR-COMPONENT`.

## Particulars

**1. Item 9 keeps the pairing closed, and the store matches it.** The body set is every root-chain body, the revocation body, every `members.manifests` body, and `members.catalog` only when one listed envelope's carrier stored digest equals that body. `members.envelopes` must bijection with that set by carrier stored digest. A second catalog envelope is a second digest hit and fails the bijection; the "at most one" sentence states the same refusal. A component manifest without an envelope leaves a body with no digest and fails it. Any other listed envelope fails it. Digest identity is the same set rule the r8 code already uses (`BTreeSet` length, then `remove`), so two bodies that share a digest still refuse. An r8 release lists neither a catalog envelope nor a component manifest, so its body set is still the chain plus the revocation and it still passes. The payload shape's required catalog member stays a tree row (`bootstrap-member-tree`) and is not stored unless item 9 admits its envelope.

Item 2 stores that catalog pair only in that case, and stores each manifest body with its envelope whenever the release is admitted. Admission already implies the envelope, because item 9 refused the release otherwise. The anchor, the inventory pair and the payload pair stay the store entries they were; they are not `members.envelopes` entries. The parenthetical on "Nothing else is stored" widens Evidence's root-chain open sentence to exactly this member list. Item 1's two fixed inventory names are a different open. Custody item 10 already covers every opened file.

**2. "No trust decision" matches items 4, 5 and 8.** The sentence is about the catalog and component-manifest pairs only. Item 4 still verifies the inventory under `TR-CORE` and the bootstrap manifest under `TR-BUNDLE` after item 5's re-filter. Item 5 still authenticates the chain, the revocation, and those two quorums, and still admits no trust fact before that re-filter. It does not verify the new envelopes. Item 8 still withholds `namespace` and `catalogSnapshot` from `InitialCore`, which matches not judging the stored catalog. X4B reverifies the pairs against the final root with the embedded revocation keys excluded, and X4T's confirming admission still runs `admit_revocation`, which refuses a closure whose catalog snapshot the list names.

**3. The no-catalog refusal is the existing row.** `PAYLOAD-NOT-ADMISSIBLE` subject `catalog` is the row `open_heads` already uses for a catalog envelope, body or quorum failure, and it is the authentication row X4T item 10 names. X4B item 7 adds the missing catalog and a failed catalog or component reverification to that same row, before any write. There is no lawful `AcceptedHeads` or payload closure to publish without a catalog, so this is a payload refusal rather than an incomplete store. Item 10's new cases use that row for no catalog and for a signature outside the role, and they write nothing.

**4. One `PresentOrdinary` for `TR-COMPONENT` matches `decide`.** `decide` takes one `EntryObservation` for the role. From `Unbootstrapped`, `Admissible` stores `Trusted`. The machine does not take a document list. Item 2 verifies every listed manifest under `TR-COMPONENT` first, and any failure is `PAYLOAD-NOT-ADMISSIBLE` with nothing written, so `decide` is reached only when every listed manifest has already verified. One joint `PresentOrdinary` is then the role's single `EV-PRESENT-PAYLOAD`, which is what item 10 requires and what `accepted.by` names. With no manifest listed, no event is dispatched, the role stays `Unbootstrapped`, and the confirming admission refuses `component:unbootstrapped`. `TR-CORE`, `TR-BUNDLE` and `TR-INDEX` each have one document and one event. `continuation` admits `InstallGateRequiredForNewProcess` when core, index and component are `Trusted`; profile and repair are outside that join, so their `Unbootstrapped` states match the first test case.

## Contract check

No contract successor is needed. `EmbeddedBootstrapV1` is `{directory, manifest, envelope}` and does not list the envelope set. `index_payload_shape` requires `members.catalog` and `members.revocation` and allows `manifests` and `envelopes` from zero up to their existing caps; `admitted_payload_paths::admit` already classifies the catalog as `Catalog`, each manifests row as `Manifest`, and envelope rows as untyped paths. `core_anchor::capture` already requires every admitted manifest member to be a tree row. `bootstrap-envelope-set` is the internal subject in `installation_routing.rs`; no public detail registry names it. `core-auth323.ndjson` drives `core_authentication::authenticate` from the fixture's own stores, not from `signed_release`, so the golden stays put while 463h replaces `catalog-placeholder`.

Unit 463h is the right code successor: F8 through F10, the r9 pairing, a crate-private accessor that returns raw bytes and grants nothing, and the test-builder signatures under `TR-INDEX` and `TR-COMPONENT`. X4B-a depending on 463h matches item 11. 463h depends on nothing new.

## Verdict

463 r9: ACCEPT. X4B r5: ACCEPT. No required findings.
