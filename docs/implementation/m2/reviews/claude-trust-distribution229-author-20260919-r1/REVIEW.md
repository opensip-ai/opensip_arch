# Author proposal 229: core distribution closure, embedded bootstrap anchor, payload outer frame

**AUTHOR assistance for root review — not approval, not selected, no installation or cumulative
readiness claim.** I authored this, so I cannot approve it. No product, architecture or candidate
file was edited; no commit or push; output only in this directory. Root's 227 raw-closure/DAG work
was not read or touched.

| file | content |
|---|---|
| `proposed/OWNER-PROSE.md` | one coherent successor text in four owner sections A–D; each sentence is proposal unless tagged [source] |
| `proposed/core-distribution.v1.json` | closed fragments `CoreInventoryV2`, `CorePlatformV2`, `TreeCommitment`/`TreeEntry`, `EmbeddedBootstrapV1`, `CoreAnchorNodeV1`; RFC 6902 patch for identity-schemas.v3; fixed-name constants; source pins. sha256 50241d9f…e9aa |
| `proposed/fixtures-check.json` | 38 conditional cases (recomputation + negatives). sha256 bf0f05a5…6cbf |
| `claude-out/probes/build_and_check.py` | builder and fixtures; frozen `canonical.py` validator and `identity()` recipe |

## The proposal in six sentences

1. `closure2` gains one kind, `core`; its `manifestDigest` is the raw SHA-256 of the inventory BODY,
   its `tree` is the existing file-entry projection of the platform's `TreeCommitment`, and
   version / protocol major / platform come from signed inventory fields and the four machine
   Platform ids. The eight component kinds and their rule are untouched, and no alias between an
   inventory and a component manifest is admissible.
2. The "signed core release manifest" is the inventory document itself (`CoreInventoryV2`, envelope
   kind `inventory`, TR-CORE): the closed route table gives TR-CORE no other kind. It carries
   S9.1's `CoreProfileBindingV2`, DR-126's TCB profiles and DR-101's graph by reference, each under
   its own owner's rules.
3. The inventory pair lives outside every tree it describes (`inventory.json`,
   `inventory.sig.json`), which removes the body→tree→body cycle.
4. The embedded bootstrap is an ordinary payload1 directory inside the tree, framed like any
   payload; the anchor is always its `rootChain[0]`, later embedded roots are ordinary in-order edges.
5. `CoreAnchorNodeV1` is recomputable from five retained raw pairs and proves only *which bytes the
   inventory declares as the index-0 root*; why they are trusted is the install/launch verified-bytes
   premise, outside the trust store, and TR-CORE's signature is never an input.
6. Payload framing uses root's fixed names `payload.json` / `payload.sig.json`, excludes them (and
   their custody-owner aliases) from the member namespace, reads no extras, and — correcting my
   earlier phrase — forbids search, not the bounded direct reads recovery needs before quorum.

## What I read (request: "end to end where relevant")

- Workflows §2 (l.257–328) in full: closure admission there is pivot/detector law — three
  current-trust origins, detector compatibility listing — and never mentions the core. Hence A.3.
- DR-101 v16 `inventorySchema` in full (layer taxonomy, `graphRules`, open decisions OD-101-1/2):
  nodes are `{path, sha256}` with no length; status CANDIDATE-NOT-APPLIED, binds NOTHING.
- DR-103 v11 `treeCommitmentShape` and `signatureBinding`; completion v1 §2.2, §3.1–3.3, §4.6,
  §6.5, §8.5; completion v8 l.198–201; security-and-lifecycle l.24–71, l.1086–1116, l.1224–1246,
  l.1294–1318, l.1438–1460, l.1488–1506; identity `closure`, `Blob`, `LogicalPath`; identity-model
  prefix/`identifier`; my anchor227 REVIEW and retention note; 215 r14 OWNER.md l.9, 32–47.

## Fixture results (all conditional on adopting the successors)

- Recomputed a core id with the frozen recipe: `closure2:69eed446…57d7`.
- The CURRENT identity schema refuses `kind: core` (shows the successor is required, not optional);
  under the patch all eight existing kinds still validate and hash to different ids.
- Anchor: index-0 admits; a later embedded root presented as anchor, wrong closure label, missing
  retained inventory or root envelope (`unavailable`), other platform, root not a tree member,
  bootstrap digest differing from the tree, and non-fixed bootstrap names all refuse with exact labels.
- The anchor function has parameters `{node, retained}` only, and a different TR-CORE envelope yields
  the same closure id and result: the signature is structurally not an input.
- Closure: inventory pair or its case alias inside the tree, case-fold path alias, display-alias
  platform, unsorted majors, non-canonical bytes, non-file entrypoint, schema 1, and a wrong-shaped
  profile binding refuse; length and manifest digest are identity members.
- Frame: payload1 and proposed payload2 route correctly; crossed domains, ordinary kind under
  schema 2, ninth-kind envelope on the manifest, unknown schema, and reserved member names (exact,
  case alias, NFD alias) refuse; the same leaf in a subdirectory admits.

## Limitations — read before relying on any of this

- **`TreeCommitment` schema is my transcription** of DR-103's prose definition (mode pattern
  `^[0-7]{3,4}$` and `maxItems` are mine). DR-103's own OD-1 leaves tree size open; here the 4 MiB
  inventory-body cap is the effective bound.
- **`servedProtocolMajors` and hashing its maximum is a design choice**, grounded only in workflows
  §2's plural wording. If the host in fact serves one major, a single integer field is simpler.
- **"The core release manifest is the inventory" is an inference** from the closed route table plus
  prose; no source states it. If root holds that a distinct release-manifest document exists, it
  needs its own envelope kind and B.1 changes; A, C and D do not.
- **Alias comparison in the probe is NFC + casefold**, a stand-in. The law proposed is "the existing
  custody owner's alias rules"; I did not locate or exercise that owner here.
- `tcbProfiles` is validated only as an empty list; the external `$ref` is never resolved by the probe.
- DR-101's graph rules (roots, acyclicity, duplicate digest, layer cardinality) are cited, not checked.
- Catalog representation of a core release (if any) was not examined; nothing here depends on it.
- No signature, threshold, custody, S4, 222 publication or execution evidence is exercised. The
  fixtures' "envelopes" are opaque bytes. The probe contains one unused helper (`reserved`).
- All fixtures passed on the first run; I did not seed a deliberate failure to prove the harness
  can fail beyond the 27 refusal cases (26 with exact labels, 1 a validator refusal), each of which asserts an exact refusal label.

## Pins (reference-201 `candidate/docs/…`, my verified extraction)

- `v2/contracts/product-v1/security-and-lifecycle.md` 7c982d877dfa051c07ce6c4976c1ca63a70152a60570fa8fedbd45e8144b7ec4
- `v2/contracts/product-v1/workflows-and-surfaces.md` 8d8551c6544f5240c4a032e95e7dd6c5059a834305de6ddcfc981fa508d73d05
- `coop/design-corrections/foundation/identity-schemas.v3.json` a76c9e2f07e8f8e52ee611f157548f6a09061866308652e3a0f7e3c24893db21
- `coop/design-corrections/foundation/identity-model.py` 12c9cc226b582adc8e34a55e8a59671f2611c46d3e27d1d8289a472d78ccacb6
- `coop/design-corrections/foundation/canonical.py` d47f25db0fb09ceb84282a89fdf74055cb81ccb9de26f85a5a70b032b9a6b442
- `coop/design-corrections/security/security-lifecycle.schemas.v1.json` 535800dfbce9172d491b4a99c3a40120b27d8dc5107f1930bd156789459d683c
- `coop/design-corrections/security/signature-envelope.schema.json` 48b7f4b5e7d3ae622f199aa2b5f07cb9f235ead67919cb5d428c547a5e67c8d1
- `coop/design-corrections/security/signature-envelope-routes.v1.json` 4b42bcb9122710350d390066504d5a75c447060231ac642f828af5332e519a58
- `coop/completion/security-schemas.v2/payload.schema.json` bb9ab011b8b8d3f819552a7aa8924a1df9e6e00abf447f0a5e99330060b43da0
- `coop/completion/security-schemas.v2/tcb-profile-template.schema.json` d0b24d76fdcb5c6a5af7f59d4f77e0a62588af9c41fd30997824cb84ddb4d181
- `coop/completion/security-schemas.v2/envelope.schema.json` (obsolete six-kind copy, NOT extended) 82baf6967b8315546a93d955a2523805161f37bd22cb6728198442491e3cc3c1
- `coop/artifacts/distribution-core-inventory-contract.v16.json` 429b8c7a9cd5c8f2b495337c055ccbd262e796ba1cc42efb173779c72018fb5b
- `coop/artifacts/component-manifest-schemas.v11.json` 1c0b8868444a097256aaa7d9caf8ebaa1c6f73fb071dbb4dd712334abb17a005
- `coop/completion/security-completion.v1.md` a5bdd005660b7a566fdb3af60278f8bc140d26e4c493916b6cfbca47210e9004
- `coop/completion/security-completion.v8.md` 54f3a6901d4192c5b6af82d4aad4414a84ee3b7748aa67cae06272a481e38c2d
- 227 r5 `trust-time-inputs.v1.json` d308f4dd8c005bd0f30d7009f7ffd2b6ef522ad692532ad8c5739abd2ff568b5 (shared ref defs copied verbatim)
- 215 r14 archive cd338af6deccb4ea052f42d4a6acc869849af748ac7f455d097d8bef8af5dd9c, `OWNER.md` d8165f14a161d4fd7453afd0bc4af5a9c2f2a0f73be5eee35976b99cc9ef19fa
- my anchor227 `REVIEW.md` d95b6e5ec1d30e8414b02cc1603b8e364b8074a74b3389105e52da3bc04c65cc and `NOTE-retention-wording.md` 6aaf21906be099f4f470aafa5a91e47ce8550b3d25a66d772e9abf84d5a40875
