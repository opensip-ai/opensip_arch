# Source follow-through: core anchor binding (U-1) and manifest-own-envelope custody (U-5)

Bounded source analysis for root. **Not approval.** No candidate/product/arch edit, commit or push;
output only in this directory. Root's four corrections to my proof draft (same-operation
root→root for S5 multi-hop chains; no blanket no-source exemption from T and phase-faithful S4.5
fixtures; acceptance as a lawful proven outcome rather than a universal role event; recovery
closure must join payload2 and mandatory direct-document envelope membership) are read and
accepted; my archived draft is left unchanged and is superseded on those points by root's.

Sources are my verified reference-201 extraction and the 215 r14 archive (pin and all 1445 members
verified by exact path in the previous task; `OWNER.md` d8165f14…, read from the tar). Pins at end.
Each statement is tagged **[source]** or **[proposal]**.

## 1. U-1 — core distribution closure identity, embedded root, retention

### 1.1 What is owned today [source]

| fact | where |
|---|---|
| `fromCoreClosure`/`toCoreClosure` are typed `ClosureId` (`^closure2:[0-9a-f]{64}`) | security-and-lifecycle l.1495; `security-lifecycle.schemas.v1.json` `$defs.ClosureId`; evaluator3 `invocation-record.schema.json` l.1999–2004 |
| `closure2` hashes `{kind, manifestDigest, tree, semanticVersion, protocolMajor, platform}`; `kind` ∈ `provider, evaluator, detector, toolchain, stdlib, rust-dev-llvm, grammar, adapter` — **no core kind** | security-and-lifecycle l.29–31; `identity-schemas.v3.json` `$defs.closure` |
| `manifestDigest` is defined as "the admitted **component manifest** body bytes … excluding the signature envelope"; its authenticated association is envelope kind `manifest`, role TR-COMPONENT | `identity-schemas.v3.json` `x-opensip-digest`; security-and-lifecycle l.35–40 |
| The core's signed metadata is a DIFFERENT document: the **inventory**, envelope kind `inventory`, domain `opensip.metadata.inventory.1`, role TR-CORE; nodes `{path, sha256}` over the FINAL executable bytes; each container ships "the identical signed files plus the inventory and envelope" | security-and-lifecycle l.1309; `signature-envelope-routes.v1.json` `inventory`; completion v1 §3.2 steps 4–5 (l.331–337), §8.5 (l.748–750); `report-asset-binding.v1.json` B14 |
| The inventory's member list is DR-101 `distribution-core-inventory-contract.v16` `inventorySchema` — status `CANDIDATE-NOT-APPLIED`, `binds: NOTHING`; it contains no embedded-root, bootstrap or trust-anchor member (searched) | that file, header fields |
| "signed core release manifest schema2" exists only as prose; the one typed piece is `CoreProfileBindingV2 {schemaVersion:2, platformProfileSetBodyDigest}` | security-and-lifecycle l.1450–1452; `security-lifecycle.schemas.v1.json` `/schemas/CoreProfileBindingV2` |
| The embedded chain is prose plus one scalar: "the core's embedded bootstrap payload"; "roles re-establish by the PRESENT event over the embedded chain"; model `migrate_floors(old_trust, core_embedded_chain_max, …)` | security-and-lifecycle l.416–417, l.1230–1235; `security_lifecycle_model_v1.py` l.2284–2290 |
| A core generation is immutable while selected; the OLD one is retained for rollback "inside the 30 d window" — not indefinitely | security-and-lifecycle l.885–888, l.1239 |

**Answer to "is there an existing typed core projection elsewhere?" — No.** I searched the
identity, security, workflow and native schemas, the kernel model and fixtures: no closure is ever
built with a core kind, no schema names an embedded-root member, and no path or body/envelope pair
for it exists. The `closure2:` typing of a core closure in S9 therefore has no defined preimage:
two of its six hashed members (`kind`, `manifestDigest`) are undefined for a core. **Primary needs
an explicit successor.** I do not pick `toolchain` or invent `core`.

One structural point the successor must respect [source-derived]: the TR-CORE signature cannot
authenticate the anchor. TR-CORE keys are delegated BY a root; using them to prove which root is
the anchor is circular. The anchor's authority is that the executing core's bytes are the verified
ones (DR-G07 "verified bytes equal executed bytes", completion v1 l.334) — a TCB premise of the
same class the contract already names for `host.closures[].trust='admitted'` (l.71). The signed
inventory is therefore BINDING evidence (which bytes), not AUTHORITY evidence (why trusted).

### 1.2 Smallest concrete completion [proposal]

Three explicit successors, each in its existing owner; none is drafted as law here.

1. **Inventory body owner (DR-101 / DR-126 carrier): declare the embedded trust members.** Add one
   closed required member to the signed inventory body:
   `embeddedTrust: {rootChain: [{body:{path,sha256}, envelope:{path,sha256}}] (1..64)}`, each
   path also an ordinary inventory file node with the same digest. This reuses the 215 r14
   `rootRecoveryAuthorization` pair shape (OWNER.md l.32) and its reason: direct opens, no search,
   no magic filename. It forces the embedded chain to be DATA members of the closure. If the chain
   were compiled into the executable instead, no retained-byte proof of "this core embedded that
   root" is possible short of retaining and re-parsing the executable; the successor must rule
   that out explicitly.
2. **Identity owner (§3 / `identity-schemas`): define the core projection of `closure2`.** The
   minimal faithful form is a new `kind` value whose `manifestDigest` is the raw SHA-256 of the
   inventory BODY bytes (envelope kind `inventory`), with `tree` projected from the inventory's
   regular-file nodes exactly as l.43–48 projects a TreeCommitment. This changes an enum and the
   `x-opensip-digest.artifact` sentence, so it is a real identity-schema successor, not an edit I
   can assume. Until it exists, `ClosureId` for a core is a label with no recomputable preimage.
3. **227 anchor variant: bind bytes, not the label.** Replace my draft's
   `{coreClosure, root, binding}` with
   `{admissionSchema, kind:"anchor", coreInventory: DocRef, rootChainIndex, root: DocRef, binding: RootBinding, coreClosure: ClosureId}` where
   - `coreInventory` is the retained inventory body + envelope (raw refs);
   - `root` must equal `embeddedTrust.rootChain[rootChainIndex]` by both digests (index is
     `I64NonNegative`, < chain length; multi-hop embedded chains then use root's corrected
     same-operation root→root edges, anchor at index 0);
   - `coreClosure` is kept ONLY as the join to the S9 intent / selected generation and is
     verifiable only once successor 2 exists. If root prefers no unverifiable member, drop it
     until then; the proof does not depend on it.

### 1.3 Retention after a core update [proposal, from the 30 d source fact]

The old generation is not retained beyond the rollback window, so an original anchor proof may
not depend on it. At first use of an anchor (creation/first PRESENT, and again for each new core
whose embedded chain is relied on), copy into the trust store as ordinary ≤ 4 MiB raw records:

- the inventory body and its envelope;
- every embedded root body and envelope from index 0 through the relied-on index.

Historical verification then recomputes, from retained bytes only: envelope `storedSha256` /
`preimageSha256` joins; `embeddedTrust` entry ↔ root DocRef equality; root `binding`. Core
executable and other artifact bytes need NOT be retained: the inventory pins their digests and the
anchor claim is about the root members only. What this cannot re-prove later is the DR-G07 premise
(that those inventory-listed bytes were the ones executing). That was an install/launch-time
check; the honest record of it is the existing install/launch evidence owner, not a scalar
attestation in the trust node. A missing retained record is `unavailable`, never "anchor assumed".
All copies are charged to the 222 work profile before the node is written.

## 2. U-5 — the payload manifest's own envelope

### 2.1 What is owned today [source]

- Envelopes are DETACHED: "A detached envelope per signed document (DR-103 `signatureBinding`: the
  manifest carries no signature field)" — completion v1 §2.2 l.201; component-manifest-schemas.v11
  `signatureBinding`.
- The payload is "A directory whose manifest (`opensip.metadata.payload.1`, signed TR-BUNDLE
  2-of-3) carries `payloadKind` … and the `mustCarry` members as `{path, sha256}` nodes … A missing
  member refuses the whole payload; nothing is fetched." — completion v1 §4.6 l.420–426. Members
  are verified "on its opened fd against the signed inventory before publication" (v8 l.200).
- Primary envelope: `subject.kind=payload`, domain `opensip.metadata.payload.1`, role TR-BUNDLE —
  one of EIGHT primary kinds (security-and-lifecycle l.1303–1312; routes file). 215 r14 adds a
  ninth (`root-recovery-authorization`) and `payload.2`, and says to extend the primary eight-kind
  owner, "not the obsolete six-kind copy" (OWNER.md l.36).
- Commands carry one operand: `opensip trust import PATH`, `opensip trust recovery-import PATH`;
  `trust refresh` fetches "an ordinary air-gap payload (§4.6)" into the same path (command-inventory
  v3; completion v1 l.601).
- `members.envelopes` cannot hold the manifest's envelope: that envelope contains
  `storedSha256(manifest)`, and the manifest would contain the envelope's digest — a genuine hash
  cycle. 215 r14 l.47 avoids the analogous cycle for the authorization and l.32 gives it an explicit
  body/envelope pair for "two direct opens, not a pre-authentication search of up to 100000
  envelope files". Nothing does the same for the manifest itself.

**Finding: the manifest filename and the location of its envelope are unowned.** No source names
either; the v2 six-kind `security-schemas.v2/envelope.schema.json` is silent too. Every
implementation would have to guess, and a guess here is a pre-authentication search surface.

### 2.2 Closed framing [proposal]

`PATH` names a directory. The OUTER PAIR is two reserved entries directly in that directory; they
are the only bytes read before authentication:

1. Open PATH as a directory (no-follow), then open exactly two fixed reserved names relative to
   that directory fd, each a regular file, no-follow, each bounded by the existing 4 194 304-byte
   metadata cap BEFORE parsing (215 r14 l.34). No enumeration, no glob, no fallback name.
2. Envelope decodes as `opensip-signature-envelope.2`, `subject.kind == "payload"`,
   `subject.domain` ∈ {`opensip.metadata.payload.1`, `opensip.metadata.payload.2`} and equal to the
   domain selected by the body's `payloadSchema`; `storedSha256` == raw SHA-256 of the manifest
   bytes read; `preimageSha256` == recomputed preimage. Then TR-BUNDLE authority as today
   (ordinary: accepted/prospective root per 215; recovery: the authorized prospective root, l.43).
3. The two reserved names are excluded from the signed member namespace: a manifest whose any
   `members.*.path` equals either reserved name refuses. This keeps one meaning per path and makes
   the cycle unrepresentable rather than merely avoided.
4. The retained `DocRef {body, envelope}` of this pair is exactly `PayloadMetadataClosureV1.manifest`.
   Nothing about the original PATH or the names is retained or needed later.
5. Kinds: the manifest envelope stays the existing primary kind `payload`; the ninth kind remains
   for the authorization only. No tenth kind, no change to the eight.

Two decisions I deliberately leave to the primary owner rather than invent:

- **The two literal names.** They must be fixed constants in the payload contract successor (the
  same successor 215 r14 l.36 already requires). I propose none as law; any pair works if it
  satisfies rule 3.
- **Unlisted extra directory entries.** Source says a missing member refuses; it is silent on
  extras. Since members are opened by signed path and nothing is enumerated, extras are never read;
  whether their presence refuses is unowned. I recommend "never read, not a refusal cause"
  (consistent with 222's foreign-name treatment), but it is a choice, not a finding.

## 3. Pins (sha256 of files cited; reference-201 paths under `candidate/docs/`)

- `v2/contracts/product-v1/security-and-lifecycle.md` 7c982d877dfa051c07ce6c4976c1ca63a70152a60570fa8fedbd45e8144b7ec4
- `coop/design-corrections/foundation/identity-schemas.v3.json` a76c9e2f07e8f8e52ee611f157548f6a09061866308652e3a0f7e3c24893db21
- `coop/design-corrections/workflows/schemas/evaluator3/invocation-record.schema.json` 3377d456a3d94ca388a9b1acf5726d35801b65d4face9b018d5c99964e819d07
- `coop/design-corrections/security/security-lifecycle.schemas.v1.json` 535800dfbce9172d491b4a99c3a40120b27d8dc5107f1930bd156789459d683c
- `coop/design-corrections/security/signature-envelope.schema.json` 48b7f4b5e7d3ae622f199aa2b5f07cb9f235ead67919cb5d428c547a5e67c8d1
- `coop/design-corrections/security/signature-envelope-routes.v1.json` 4b42bcb9122710350d390066504d5a75c447060231ac642f828af5332e519a58
- `coop/design-corrections/security/security_lifecycle_model_v1.py` df45c9c5444790b5f89b458efbee5cb068781d5fc1e82483c2678d2f10712299
- `coop/design-corrections/workflows/command-inventory.v3.json` 6adbb91413f5bc8ed89f1ab8b4d8a7d5eabb9ff79ccb38e85d0919684f09dfdd
- `coop/artifacts/distribution-core-inventory-contract.v16.json` 429b8c7a9cd5c8f2b495337c055ccbd262e796ba1cc42efb173779c72018fb5b
- `coop/artifacts/component-manifest-schemas.v11.json` 1c0b8868444a097256aaa7d9caf8ebaa1c6f73fb071dbb4dd712334abb17a005
- `coop/completion/security-completion.v1.md` a5bdd005660b7a566fdb3af60278f8bc140d26e4c493916b6cfbca47210e9004
- `coop/completion/security-completion.v8.md` 54f3a6901d4192c5b6af82d4aad4414a84ee3b7748aa67cae06272a481e38c2d
- `v2/architecture/report-asset-binding.v1.json` 71363c0637d4405d9394782f805f33c294588834990614388a26a2dbd98027a6
- 215 r14 archive cd338af6deccb4ea052f42d4a6acc869849af748ac7f455d097d8bef8af5dd9c; `OWNER.md` d8165f14a161d4fd7453afd0bc4af5a9c2f2a0f73be5eee35976b99cc9ef19fa

Limits: "no typed core projection exists" is a negative from bounded searches (`coreClosure`,
`closure2:`, `embedded`, `bootstrap`, `inventory.1`, core-kind literals) over the reference-201
candidate docs; I did not read workflows §2 closure admission end to end, and did not search
outside reference-201 and 215 r14. No checks were run; this task produced no schema or model.
