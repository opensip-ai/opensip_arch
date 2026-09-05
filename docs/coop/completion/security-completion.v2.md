# Security, trust and platform-TCB completion — turn 2

Author: Claude (Herdr `wH:p2`). Status: PROPOSED, turn 2 under D-368, awaiting the lead's
independent review. Scope unchanged: DR-112, DR-105, DR-114, DR-124, DR-126, DR-101 OD-101-2,
plus the metadata canonicalization and signature profile (DR-103 ID-DEP-1). Date: 2026-09-04.

Turn 1 (`security-completion.v1.md` `a5bdd005…`) drew OBJECT at 8 MUST-FIX / 2 SHOULD-FIX
(`security-codex-review.v1.md` `d43fe11ce2e07261d73eb466fb7647cc82f0d1689b3e6f3d2ec16392e7f5b32d`).
Every finding is landed by name in §0.3. This version also folds in the lead's later integration
points: the `trustEpoch` quadruple, the lock/lease discipline, the catalog/registry split, the
locator encoding, signed-i64 counters, the RF-5 unreachability under the closed control bodies, and
the FC-REDACT supersession. It binds NOTHING, edits no register cell, authorizes no implementation,
and claims no platform qualification.

## 0. Pins, incorporation, supersessions, repair map

### 0.1 Pins

HEAD `12f8783` (`D-368: adopt reciprocal review and integrated architecture closure`) at authoring;
the lead's source-custody checkpoint `867175a` landed during authoring and changes no pinned input; file 08
`872f0929926f996ee475642426c6ba33bec7bd6aa3eec6b6a927f2b197618bd6`. The incorporated recorded
contracts and their digests are exactly the table in `security-completion.v1.md` §0 (unchanged:
`signed-index-trust-contract.v14` `039a5702…`, `platform-tcb-contract.v48` `9511fca3…`,
`permission-truth-tables.v9` `05d55964…`, `host-effect-authorization.v25` `b91b9f73…`,
`doctor-contract.v4` `df2e7175…`, `doctor-actor-join-integration-contract.v8` `c830f954…`,
`state-class-contract.v11` `b5456c63…`, `distribution-core-inventory-contract.v16` `429b8c7a…`,
`component-manifest-schemas.v11` `1c0b8868…`, `canonical-json-profile.v1` `6f7c906c…`,
`control-protocol-contract.v2` `c50a79fe…`). Paired unrecorded drafts read for integration:
`distribution-runtime-completion.v1.md` `9282d9599a84a8f141cd0d2185e3442b89c6faf5b765b19bceb39f14f4c68a45`,
`control-message-schema.v1.json` `f446d1fd…`, the frozen analysis-quality unit
(`analysis-quality-freeze.v1.json`) for the capability registry.

Retained with this document, all under `docs/coop/completion/`: `security-schemas.v2/`
(ten closed JSON Schemas plus `grant-journal.sql`), `security-fixtures.v2/` (26 example and
fixture files, including a grant-journal SQLite database built through the DDL and two scoped
registry views),
`security-vectors.v2.json`, `security_unit_lib_v2.py`, `check-security-unit.v2.py`, and the
frozen report `security-unit.v2.report.json` (82 checks, 0 failures, with input digests,
environment, and cross-validation of every schema and example through `jsonschema` 4.25.1 in
the lead's review environment).

### 0.2 Incorporation and explicit supersessions

The incorporation rule and the per-contract lists of `security-completion.v1.md` §0 stand,
with these additions and corrections:

1. `component-manifest-schemas.v11 indexSchema` — its **per-install custody half** (`installId`,
   `admittedAt`, `ownershipTransfers`, `retiredIds`, `custodyRule`) is carried whole as the LOCAL
   ADMITTED REGISTRY (`opensip-registry.1`, §4.5, host-written, SC-OPS, never enveloped). Its
   **release half** (which releases exist, their digests and artifacts, the reserved root
   commands) is superseded by the RELEASE CATALOG (`opensip-catalog.1`, TR-INDEX signed). The v11
   sentence "Admission writes the manifest custody record ... and the registry custody record ...
   in one admission act" stands; the new custody rule adds that an entry may be admitted only from
   a release present in the currently TRUSTED catalog snapshot, and pins that snapshot. The
   lead's turn-1 finding that an installation cannot obtain release signatures over locally
   minted custody is thereby answered without giving the host any K-index key.
2. `platform-tcb-contract.v48` — two further named supersessions, each a **semantic successor
   (v49) that this unit specifies and the pair must adopt as its own reviewed act before the
   macOS profiles can freeze**: (a) `platformAttestationOperation.macosCodesign.pathlessInput`
   ("the running kernel / OS ABI code object as the SecCode guest") and `subjectByScheme.codesign`
   for the OS ABI class, measured unavailable (§8.3); (b) nothing else. The Linux OS ABI rule
   (`fromBootLockdown.presentState`: `/proc/sys/kernel/kexec_load_disabled` MUST be absent;
   `kexecAbsenceDerivation`; `builderAttestation`) is NOT superseded; v1's "kexec_load_disabled=1"
   contradicted it and is withdrawn (§8.4).
3. `doctor-contract.v4 acceptanceEvidenceFixtureClasses[FC-REDACT].passProperty` TIER 1 sentence
   "in whole or in any prefix or suffix of length greater than zero" — superseded by the
   noninterference property in §6.8 (the literal is unsatisfiable: every single character of a
   secret collides with JSON syntax and ordinary report text).
4. `control-protocol-contract.v2` CC-8 — the lead's successor is mirrored in §7.4.
5. `canonical-json-profile.v1` — as v1 §0 item 10, unchanged.

### 0.3 Repair map for the turn-1 findings

| Finding | Landed at |
|---|---|
| SEC-M1 evaluation clock can move backwards; §4.7 example inconsistent | §4.2 persisted evaluation high-water with write-ahead durability; §4.7 rewritten with every role's state |
| SEC-M2 witness violates lock order; crash gap | §5.4: per-carrier write-ahead witness owned by the same operation-lease writer; no lifecycle-lock write from a project writer; every crash point enumerated; install-root high-water updated only at operation boundaries under the fence |
| SEC-M3 whole-store rollback undetectable | §5.5: threat boundary stated; restore protocol is fail-closed (restored trust state re-enters through an ordinary payload); what is and is not detected |
| SEC-M4 Linux profile contradicts v48; macOS acquisition infeasible | §8.4 kexec-absent OpenSIP-built kernel, presentState absent; §8.3 measured infeasibility and the v49 `macos-sealed-boot` scheme; §8.6 product consequence stated |
| SEC-M5 carriers are prose fragments | `security-schemas.v2/` closed schemas for root, revocation, catalog, registry, payload, envelope, journal records, permission policy, profile templates; §5.4 chain preimage, genesis, locator; four profile templates validated; `verifiedInstallRoot` two-comparison rule §8.5; Linux certificate-store members §8.4 |
| SEC-M6 ceremony vs V8 JIT; tar/Gatekeeper claim | §3.2 per-binary, per-architecture entitlements with Apple's allow-jit rule cited; the extraction claim removed |
| SEC-M7 wrong capability registry | §2.2 manifest rebuilt against `typescript.imports/references/calls/types/reachability` with `{relation, rung}`; wrong-rung and unknown-capability negatives; admission checker |
| SEC-M8 unsigned routing fields | §2.2 signed subject includes kind, domain, role, namespace; closed routing table; namespace binding; precedence; role-confusion, namespace-mismatch, unauthorized-key and malformed negatives |
| SEC-S1 machine-readable report; Unicode version | `security-unit.v2.report.json` with input digests, environment, and the Unicode table disclosure (reference 16.0.0 vs production 15.1) |
| SEC-S2 PR-6 trigger set | §6.3: the closed policy schema carries no confinement member (checked); a future member that requires confinement refuses PR-6 when unenforceable |

Pre-freeze advisories from the lead, also landed: typed const/enum equality in the reference
validator (a boolean never equals an integer) with boolean-mutant negatives for every versioned
document and cross-validation against `jsonschema` 4.25.1 in the review environment when present
(§9); controlled parse refusals for invalid UTF-8, nesting beyond 64, integers beyond signed-i64,
oversize and malformed input (§2.1); the full v11 `indexSchema` custody shape retained in the
admission store with project binding and scoped views (§4.5); publisher and version carrier
bounds relaxed to the 4 MiB ceiling so no inherited value is narrowed (§4.5); the journal `seq`
capped at the control plane's uint53 with a reserved terminal slot and generation rollover (§5.4).

## 1. Threat model boundary

Unchanged from `security-completion.v1.md` §1, with one addition made explicit by SEC-M3: a
coherent offline rollback of an entire install root (trust store, registry, projects and
journals together) is not locally distinguishable from an old but honest state. The design
therefore never lets restored or rolled-back trust state admit anything by itself: trust is
re-established only by an ordinary payload whose counters are checked against the origin
(§5.5), and stale state ages into refusal (§4.2). Rollback yields denial, not stale authority.

## 2. Metadata canonicalization and signature profile (closes DR-103 ID-DEP-1)

### 2.1 `opensip-metadata-canonical.1`

Unchanged from v1 §2.1 (CJ-R01..CJ-R14 with UR-1 scalar-value order, UR-2 signed-i64, UR-3
reject non-NFC, UR-4 CJ-R08 escaping, UR-5 reject lone surrogates; duplicate keys reject at
parse). All counters that appear in metadata (`rootVersion`, `snapshotVersion`,
`revocationVersion`, `grantGeneration`, `seq`, `trustEpoch` members) live in the canonical
signed-i64 range `1 .. 9223372036854775807`, matching the lifecycle carrier.

Domain-tag registry (closed):

| Tag | Document | Enveloped |
|---|---|---|
| `opensip.metadata.manifest.1` | component manifest (v11 `manifestSchema`) | yes, TR-COMPONENT |
| `opensip.metadata.catalog.1` | release catalog (§4.5) | yes, TR-INDEX |
| `opensip.metadata.root.1` | trust root document (§3.1) | yes, ROOT |
| `opensip.metadata.revocation.1` | revocation list (§4.5) | yes, ROOT |
| `opensip.metadata.inventory.1` | signed-closure inventory, the DR-126 carrier (§8.5) | yes, TR-CORE |
| `opensip.metadata.payload.1` | air-gap payload manifest (§4.6) | yes, TR-BUNDLE |
| `opensip.metadata.registry.1` | local admitted registry (§4.5) | never |
| `opensip.metadata.lock.1` | component lock (paired draft §3) | never |
| `opensip.metadata.policy.1` | permission policy (§6.3) | never; digest-pinned in the lock |
| `opensip.metadata.journal.1` | grant-journal record bodies (§5.4) | never |
| `opensip.metadata.envelope.2` | the signed subject of an envelope (§2.2) | is the signature message |
| `opensip.metadata.test.1` | vectors only | never |

**Parse refusals (controlled, never an interpreter exception).** Before canonicalization or
schema validation a metadata document is admitted through one strict loader: over 4 194 304 bytes
→ `METADATA_TOO_LARGE`; invalid UTF-8 → `INVALID_UTF8`; a byte-order mark → `BOM_FORBIDDEN`;
bracket nesting beyond 64 (scanned before any recursive parse) → `NESTING_TOO_DEEP`; an integer
outside signed-i64 (checked on the token, so a 5 000-digit literal never reaches integer
conversion) → `INTEGER_OUT_OF_RANGE`; floats and non-finite constants → `FLOAT_FORBIDDEN` /
`NON_FINITE_FORBIDDEN`; duplicate keys → `DUPLICATE_JSON_KEY`; anything else → `MALFORMED_JSON`.
Each is a typed refusal on the DR-103 admission surface and each is exercised by the checker.

Vectors are retained in `security-vectors.v2.json`; the canonical-profile ones are those of v1
(V-UR1 `ee5518aa…`, V-UR2 `78523d08…`, V-UR3-NFC `7ade765e…`, V-UR4 `7d80874a…`, the six
rejects) plus V-DUP-KEY-REJECT. The v1 fragment vector V-MAN-1 is withdrawn.

### 2.2 `opensip-signature-envelope.2` (supersedes the unrecorded `.1` of turn 1)

```json
{ "envelopeSchema": 2,
  "subject": { "kind": "manifest", "domain": "opensip.metadata.manifest.1",
               "storedSha256": "<hex64>", "preimageSha256": "<hex64>" },
  "role": "TR-COMPONENT", "namespace": "opensip",
  "signatures": [ { "keyId": "<hex64>", "alg": "ed25519", "signature": "<hex128>" } ] }
```

**Signed subject and message (SEC-M8).** The message signed is the 32 bytes of
`SHA-256( "opensip.metadata.envelope.2" || 0x00 || canonical({kind, domain, storedSha256,
preimageSha256, role, namespace}) )`. Every routing field is therefore under the signature; a
valid signature cannot be re-presented under another kind, domain, role or namespace.

**Closed routing table.** `kind` selects the domain and the role, no other combination is
lawful: manifest → `…manifest.1` → TR-COMPONENT; catalog → `…catalog.1` → TR-INDEX; root →
`…root.1` → ROOT; revocation → `…revocation.1` → ROOT; inventory → `…inventory.1` → TR-CORE;
payload → `…payload.1` → TR-BUNDLE. Registry, lock, policy and journal are never enveloped; an
envelope naming them is malformed.

**Namespace binding.** For a manifest, `namespace` MUST equal `manifest.provenance.publisher`.
For catalog, root, revocation, inventory and payload the namespace is the release namespace
`opensip`. A role key set is authorized for the namespaces the root document lists for it
(`roleToKeyAndDelegatedNamespace`).

**Verification order and precedence.**

1. No envelope, or an envelope that fails the closed schema (`envelope.schema.json`) → `RJ-4
   UNSIGNED`. A malformed envelope is never partially read: no field of it is used.
2. `kind` is not the expected kind, or `domain`/`role` do not follow the routing table → `RJ-4
   ENVELOPE_MISMATCH`.
3. `sha256(stored bytes) != storedSha256` → `RJ-4 DIGEST_MISMATCH`.
4. Canonicalize the stored bytes under `domain` (duplicate keys, floats, non-NFC refuse) and
   recompute; a refusal or `preimageSha256` mismatch → `RJ-4 ENVELOPE_MISMATCH`.
5. `namespace` does not bind to the document's publisher → `RJ-4 ENVELOPE_MISMATCH`.
6. For each signature whose `keyId` the root document authorizes for `role`+`namespace`, verify
   Ed25519 over the message; a signature from an unauthorized key is ignored and audited; zero
   valid signatures → `RJ-4 ENVELOPE_MISMATCH`.
7. Count distinct valid keys against the role threshold; a shortfall is DR-112's
   `thresholdEvaluation` refusal (stay non-TRUSTED), not RJ-4.

`keyId = SHA-256(32-byte public key)`; `signatures` sorted by ascending `keyId`, no duplicates.

**Schema-valid fixture pair (SEC-M7), retained under `security-fixtures.v2/`.**
`typescript-analyzer.manifest.json` conforms to `component-manifest-schemas.v11`: `role:
analyzer`; the control tuple `{roleSubprotocol: "typescript", subprotocolVersion: 1}`; exactly
the five host capability IDs of the analysis-quality unit §3 with the closed `declarationData
{relation, rung}` — `typescript.imports {imports, resolved-target}`, `typescript.references
{references, resolved-binding}`, `typescript.calls {calls, resolved-callee}`, `typescript.types
{types, checked}`, `typescript.reachability {reachability, from-resolved-calls}`; four structured
platform trees; `permissions[].permission` from the closed PT set; six digest-bound
declarations; typed-null reserved points; `compatibility.hostCore` `[0.1.0, 0.2.0)`.

| Item | Value |
|---|---|
| `storedSha256` | `ce6c943513188ccf785065332b754fdd68a3f672fbb66af5177234fa7f0b7401` |
| `preimageSha256` (`opensip.metadata.manifest.1`) | `9b7811957432386ddea14c084f3c11c62badec96cb8ad1ec6d2c9bf5e9fdd227` |
| positive envelope | two TR-COMPONENT signatures (TEST keys K-comp-1 `64923ff5…` and K-comp-2), threshold 2 met → VERIFIED |
| `envelope-mismatch` | preimage `3c8c647d…` computed over `version 1.0.1`; valid signature over that; step 4 → ENVELOPE_MISMATCH |
| `envelope-role-confusion` | K-comp-1 signs a subject claiming kind catalog / role TR-INDEX; step 2 (and step 6) → ENVELOPE_MISMATCH |
| `envelope-namespace-mismatch` | namespace `evil` ≠ publisher `opensip`; step 5 → ENVELOPE_MISMATCH |
| `envelope-unauthorized-key` | signed by a key the root does not list; step 6 → ENVELOPE_MISMATCH |
| `envelope-malformed` | empty `signatures`; step 1 → UNSIGNED |
| `manifest.wrong-rung` | `typescript.types` with rung `resolved-target` → refused by the capability-registry check before any signature is consulted |
| `manifest.unknown-capability` | `typescript.findings` → refused likewise |

The admission checker (`check-security-unit.v2.py`, `admit_manifest`) applies the v11 subset it
can encode (required members, kind, UUID, role, name charset, root-command binding, PT tokens,
path rule, reserved points, the interval form) and the registry; the refusal code for a registry
mismatch is owned by the DR-103 successor and is not minted here.

### 2.3 Activation

As v1 §2.3: ID-DEP-1 closes for metadata; RJ-4 ENVELOPE_MISMATCH is decidable; DR-112
`envelopePreimageJoin` is ACTIVE on an applied host; the lock serializes under
`opensip.metadata.lock.1` with `resolutionInputs.canonicalProfileId = "opensip-metadata-canonical.1"`
and `indexDigest` = the `preimageSha256` of exactly one catalog snapshot (§4.5).

## 3. DR-101 OD-101-2: code-signing ceremony and OS notarization

### 3.1 Key hierarchy (`opensip-root.1`, schema `root.schema.json`, example `root.example.json`)

Unchanged from v1 §3.1: root 2-of-3, recovery 3-of-5 disjoint, role sets 2-of-3 for TR-CORE,
TR-INDEX, TR-COMPONENT, TR-BUNDLE, TR-REPAIR typed absence, KB-1 kernel attestation key, TUF
§6.1 root chaining, 365-day root document. The root document now also carries
`indexOrigin {url, spkiSha256}` (§6.5) and `kernelAttestationKeys`. The example root lists the
two TEST component keys and EXAMPLE placeholder key ids for every other role (their public
keys do not exist until the first ceremony; the placeholders are labelled and cannot verify
anything).

### 3.2 Release ceremony and entitlements (SEC-M6)

Steps 1–7 of v1 §3.2 stand with these corrections:

- **Per-binary, per-architecture entitlements.** The core executable is signed with the
  hardened runtime and **zero** entitlements. The bundled Node.js 24 runtime (a component
  closure member, not core) cannot run V8 under the hardened runtime without JIT permission:
  Apple documents that with the hardened runtime "the system allows your app to call mmap with
  the MAP_JIT flag" only when `com.apple.security.cs.allow-jit` is present, and that Apple
  silicon enforces write-xor-execute for every process. Decision: the bundled `node` Mach-O is
  signed with the hardened runtime and exactly `com.apple.security.cs.allow-jit` on arm64, and
  `com.apple.security.cs.allow-jit` plus `com.apple.security.cs.allow-unsigned-executable-memory`
  on x86_64 (V8's x64 code space predates MAP_JIT); never `disable-library-validation`,
  `allow-dyld-environment-variables`, `disable-executable-page-protection` or
  `get-task-allow`, which the Node project's own development plist enables and which this
  ceremony expressly does not. Falsifiability: G14 and the G13 corpus run under exactly these
  entitlements; if V8 on x86_64 fails without a further entitlement, that measurement drives a
  successor (or a jitless runtime qualified by G13), never an ad-hoc widening.
- **Gatekeeper.** The unconditional claim that tarball extraction avoids Gatekeeper is
  withdrawn. What is claimed: the `.pkg` channel carries a stapled ticket and is verifiable
  offline by Gatekeeper; the tarball channel carries the same Developer-ID-signed, notarized
  Mach-O plus the OpenSIP inventory envelope, and OpenSIP's own verification (§3.3) is the trust
  OpenSIP relies on; Gatekeeper's treatment of a file with or without a quarantine attribute is
  the OS's behavior and is not a product security invariant.
- Everything else (secure timestamp, `notarytool submit --wait`, digests over the signed
  Mach-O, stapler formats, non-reproducibility disclosure) stands as written in v1.

### 3.3 Verification at install and launch

As v1 §3.3.

## 4. DR-112 numbers and policy

### 4.1 OD-112-1 — unchanged from v1 §4.1.

### 4.2 OD-112-2 and the evaluation clock (SEC-M1)

The floors stand (root 365 d, catalog snapshot 90 d, revocation freshness 90 d, +24 h future
tolerance). The clock rule is replaced:

- **Persisted evaluation high-water.** SC-TRUST holds `evalHighWater`, a UTC time. Whenever
  the trust machine evaluates any expiry, staleness or future-time predicate it first computes
  `t = max(evalHighWater, wallClockNow, lastAcceptedIssuedAt)`, **durably writes** `evalHighWater
  = t` (its own SQLite transaction, `synchronous=FULL`) and only then evaluates against `t`.
  Evaluation never uses a time lower than any time previously used for a decision, across
  restarts, because the write precedes the decision (write-ahead). A wall clock below
  `evalHighWater` is recorded on the audit record as a clock observation and changes nothing.
- **Future time.** Metadata with `issuedAt > wallClockNow + 24 h` refuses; it does not advance
  `evalHighWater` (only accepted documents advance `lastAcceptedIssuedAt`). A wall clock more
  than 24 h ahead of `evalHighWater` is accepted as time passing; a wall clock can only push
  `t` forward, never back.
- **Restart.** `evalHighWater` is read before the first evaluation; if absent (fresh install) it
  is `max(wallClockNow, issuedAt of the presented root)`.
- **Retained cases (G08 FC-EVENT-ORDER successors):** forward-then-back (expire in January by
  wall clock, reset to December, same document stays expired); back-then-forward; future
  document refused then accepted after real time passes; restart between observation and
  decision (the persisted high-water carries).

### 4.3, 4.4 — unchanged from v1 (OD-112-3 `refuse` without stage qualifier; waiver 30 d + one
renewal).

### 4.5 Documents: catalog, registry, revocation (SEC-M5, and the lead's index finding)

- **Release catalog** `opensip-catalog.1` (`catalog.schema.json`, `catalog.example.json`):
  `snapshotVersion`, `issuedAt`, `expiresAt`, `rootVersionRequired`,
  `revocationVersionRequired`, `reservedRootCommands`, `releases[]` each with `stableId`,
  `publisher`, `sourceClass`, `version`, `manifestDigest` (stored), `manifestPreimageSha256`,
  `envelopeDigest`, `hostCoreConstraint` (the interval), and per-platform `artifacts[]`
  `{platform, archiveProfileId, archiveDigest, sha256}` — the paired draft's §6 fields, inside
  the signed preimage. Signed TR-INDEX 2-of-3 at the release ceremony; immutable; the machine's
  `TR-INDEX` role state is about this document. The lock's `indexDigest` names exactly one
  catalog snapshot by `preimageSha256`.
- **Local admission store** `opensip-registry.1` (`registry.schema.json`,
  `registry.example.json`): the complete per-install admission store, host-written, SC-OPS,
  never enveloped. **Every v11 `indexSchema` entryShape member is retained** under its own name
  — `stableId`, `provenance` (object, moved only by a recorded transfer), `version`,
  `manifestDigest`, `signatureRef` (sha256 of the verified envelope bytes), `admittedAt`,
  `scope`, `mountedRootCommand`, `namesSnapshot {name, aliases, mountedRootCommand}`,
  `status ∈ {active, deprecated-alias-window, retired, revoked}`, `deprecation {oldName,
  deprecatedAtRelease, deprecatedAtDate, windowEndsNoEarlierThan, doctorRemediation: reserved
  riding DR-114}` (D-012 clause 5 dual clock), `ownershipTransfers[] {fromPublisher, toPublisher,
  transferredAt, hostAuthorityRecordRef}` — plus `retiredIds[] {stableId, provenance, retiredAt,
  reason}` (the never-readmit ledger; a retired or revoked entry appears in both records),
  `reservedRootCommands` (copied from the catalog), and `trustMetadata` populated with the trust
  counters (v11 reserved this binding point to DR-112; this unit is DR-112's supply). One
  addition: **`projectKey`** on every entry, null exactly when `scope` is `global`, so two project
  namespaces never collide. One removal from the store: `shadowedBy` is not stored, because
  "project shadows global" is true only inside one project; it is a view property (below).
  Uniqueness (RJ-1, RJ-2) and the never-readmit check run over the complete store. Publisher and
  version carry no bound below the 4 MiB carrier ceiling.
- **Scoped registry view** `opensip-registry-view.1` (`registry-view.schema.json`, two examples):
  the immutable export a lock consumes. `scopeContext {projectKey | null, allowedScopes}` equals
  the lock's; `entries` are the store entries visible in that scope (that project's entries plus
  every global entry) with **`shadowedBy` computed for that scope only** — a LIVE global entry is
  shadowed by the LIVE project entry of the same `(stableId, provenance, version)` in the
  selected project, and by nothing else; `sourceStoreDigest` pins the store the view was cut
  from. The two examples show the same global entry shadowed in project A and unshadowed in
  project B. This is the model the paired solver schema consumes; no competing shadow state
  exists.
- **Lock digest meanings.** `resolutionInputs.indexDigest` = the `preimageSha256` of exactly one
  release catalog snapshot (`opensip.metadata.catalog.1`); `resolutionInputs.registryViewDigest`
  = the `preimageSha256` of exactly one scoped registry view (`opensip.metadata.registry-view.1`)
  whose `scopeContext` equals the lock's. Both are custody pins; neither is authority.
- **Revocation list** `opensip-revocation.1` (`revocation.schema.json`): entries by
  `subjectKind` `keyId | namespace | release | catalogSnapshot`; monotonic `revocationVersion`.

### 4.6 Air-gap payload — schema `payload.schema.json`, example `payload.example.json`;
`payloadKind` inside the preimage; `repairMaterial` as typed absence riding DR-110.

### 4.7 Worked transitions (rewritten; every role's state shown)

Root v1 issued 2026-10-01 (expires 2027-10-01). Catalog snapshot 9 and revocation list 3 both
issued 2026-12-20 (catalog expires 2027-03-20). Ordinary payload accepted 2026-12-21.

| Case | Evaluation time `t` | CORE | INDEX | COMPONENT | Effect |
|---|---|---|---|---|---|
| Steady state 2027-01-05 | 2027-01-05 | TRUSTED | TRUSTED | TRUSTED | admit and run |
| 2027-03-21, no payload since 2026-12-21 | 2027-03-21 | STALE-REVOCATION (list 91 d old) | EXPIRED (catalog) — precedence shows EXPIRED, stale audited | STALE-REVOCATION | `CONTINUE-CORE-NOT-TRUSTED`: continuation and new admission both refuse; only an ordinary payload heals |
| 2027-03-15, revocation list refreshed 2027-03-01 but catalog not refreshed | 2027-03-15 | TRUSTED | TRUSTED (85 d) | TRUSTED | admit and run |
| 2027-03-21, revocation refreshed 2027-03-01, catalog not | 2027-03-21 | TRUSTED | EXPIRED | TRUSTED | already-running verified components continue; `EV-INSTALL` refuses `INSTALL-NOT-TRUSTED` |
| Wall clock reset to 2026-11-01 after the row above | `evalHighWater` = 2027-03-21 | unchanged | unchanged | unchanged | nothing un-expires; clock observation audited |
| Payload carrying catalog 7 after 9 was accepted | — | — | refused `PAYLOAD-NOT-ADMISSIBLE` (anti-rollback) | — | state unchanged |
| Catalog signed by one TR-INDEX key | — | — | threshold 1 < 2, refused | — | stay |
| Root v3 signed by 2 of v2's keys but 1 of v3's | — | refused (TUF chaining) | — | — | stay |

The turn-1 "January continuation" row was wrong: with the list unrefreshed every role goes
stale at 90 days and CORE refuses; the third and fourth rows above are the honest versions.

## 5. DR-124: trust state, index custody, and the grant journal

### 5.1 SC-TRUST — as v1 §5.1 with two changes

- Members add `evalHighWater` (§4.2) and the per-project journal high-water witnesses (§5.4,
  updated only under the lifecycle fence at operation boundaries).
- **`trustEpoch`** (aligned with the lifecycle carrier): the quadruple `{rootVersion,
  catalogSnapshotVersion, revocationVersion, permissionPolicyDigest}` captured under the
  lifecycle fence at READY and at selection; a selected generation whose captured epoch is not
  equal to the current quadruple is re-verified under current trust by the connection-local
  pure verifier callback the paired carrier defines, before use. No cross-database transaction
  is claimed anywhere in this design.

### 5.2 Remaining placements — as v1 §5.2, with catalog snapshot bytes in SC-TRUST and the
admitted registry in SC-OPS (§4.5).

### 5.3 SUP-124-GRANT-JOURNAL concurrence — as v1 §5.3.

### 5.4 Grant-journal carrier (SEC-M2, SEC-M5)

**Encoding.** One SQLite database per project under the host-owned project state namespace
(`grant-journal.sqlite`), WAL, `synchronous=FULL`, foreign keys on. The DDL is retained as
`security-schemas.v2/grant-journal.sql` and is exercised by the checker: append-only triggers
refuse UPDATE and DELETE; a contiguity trigger refuses any `seq` other than tail+1; a terminal
trigger refuses appends after `TERMINAL`; a CHECK requires every `GRANT` record to bind
`install_generation_id`, `manifest_digest`, `platform` and `token`. Columns are projections of
the record body; the body (`opensip.metadata.journal.1`, schema `journal-record.schema.json`,
one closed shape per record type) is the authority, and the checker asserts column equals body.

**Writer and locks.** The sole writer is the host broker holding the project's OPERATION
lease (permission v9's "project/operation lock"). It never touches `trust.sqlite`. The global
lifecycle fence is taken only at operation start and operation end, never while the operation
lease is held, and never waits on a lease: garbage collection takes a non-blocking census of
lease locks under the fence and skips any lease it cannot prove released (the lead's rule).
Lock order is therefore fence → lease, with the fence released before the lease is acquired.

**Sequence and identity.** `seq = COALESCE(MAX(seq),0)+1` for the carrier inside one `BEGIN
IMMEDIATE` transaction (the trigger enforces it). **Representation cap:** `seq` is bounded at
`9007199254740991` (JSON uint53) because the control plane's `effectResult.decisionSeq /
outcomeSeq` carry it under the accepted control contract; the last value is the reserved
terminal slot (an ordinary record at that value is refused by trigger), so when the tail reaches
`9007199254740990` the writer appends `TERMINAL` with cause `grantGenerationClosure` and rolls
to a new grant generation before any unrepresentable sequence can exist. `grantGeneration` is
string-encoded in the locator and bounded at signed-i64. `grantGeneration` is a per-project integer
starting at 1 that advances only at grant-generation closure (whole-generation REV, or project
purge, per `terminalization`); it is not the lifecycle install generation. `operationRef` is a
preview operational correlation id `op-<32 hex>` minted by the host per operation, surface-local;
it is not a DR-006 identity and the record schema says so. `projectKey` is the paired lock
schema's opaque host-owned key (with the host's canonical-root → key registry the lead's
contributor is adding); the locator is `gj:<base64url(projectKey bytes, unpadded)>:<grantGeneration>:<seq>`,
unambiguous because base64url contains no `:`.

**Hash chain.** `body_sha256 = SHA-256("opensip.metadata.journal.1" || 0x00 ||
canonical(body))`; `prev_sha256` of seq 1 is the genesis value `SHA-256("opensip.journal.genesis.1"
|| 0x00 || projectKey || 0x00 || decimal(grantGeneration))`; for seq n>1 it is the
`body_sha256` of seq n−1. `CHECKPOINT` records carry `tailSha256`. Tamper-evident, not
tamper-proof; the witness (below) holds the head.

**Write-ahead witness (the SEC-M2 protocol).** A per-carrier file
`grant-journal.witness.json` in the same project namespace, owned by the same operation-lease
writer, written by write-to-temp, fsync, rename, fsync-directory:

1. Open `BEGIN IMMEDIATE`; compute the record and its `body_sha256`.
2. Write witness `{state: PENDING, seq: n, bodySha256}` durably.
3. `COMMIT` the journal (durable by `synchronous=FULL`).
4. Write witness `{state: COMMITTED, seq: n, bodySha256}` durably.
5. Only now may the broker initiate the external effect an `RCI`/`ICI` authorizes.

Reconciliation on open (every crash point): PENDING n with journal tail n−1 → the append never
became durable; witness reverts to COMMITTED n−1, nothing lost. PENDING n with tail n and the
same `bodySha256` → step 3 completed; witness advances to COMMITTED n. COMMITTED n with tail
< n → durable records were lost after commit: `uncertainTailLoss`, `carrier_quarantine` row,
`failClosedNoAppend`, continuation only on a new grant generation. Tail > witness seq (either
state) → impossible under the protocol; treated as `uncertainTailLoss`. Witness file absent with
a non-empty journal → `witnesslessRestore`, quarantine. Because the effect is initiated only
after step 4, no effect can exist whose authorizing record could later be found missing without
quarantine.

**Install-root high-water.** At operation start and end, under the fence and with no lease
held, the host copies `{project, grantGeneration, tailSeq, tailSha256}` into SC-TRUST. It
detects a project-namespace rollback (journal and witness restored together) whose tail is
below the recorded high-water: the carrier is quarantined at the next operation start. It does
not detect a rollback of the whole install root; that is §5.5.

**Crash matrix.** FX-4 enumerates, on this schema, every crash point: before step 2, between 2
and 3, inside the SQLite commit (WAL append vs. WAL sync), between 3 and 4, after 4 before the
effect, and each restore variant above, on both platforms.

### 5.5 Backup, restore and the rollback boundary (SEC-M3)

- Trust floors (`trust.sqlite`) are excluded from the lifecycle backup set and from every
  generation rollback. They are backed up, if at all, as a separate SC-TRUST set.
- **Restore is fail-closed.** Restoring any SC-TRUST bytes marks every role
  `ST-UNBOOTSTRAPPED` with audit reason `RESTORED`; counters and `evalHighWater` are retained
  as floors (never decreased), but nothing is admitted and nothing continues until an ordinary
  payload is presented whose `rootVersion`, `catalogSnapshotVersion` and `revocationVersion`
  are each ≥ the restored floors. The payload, not the restored bytes, re-establishes trust.
- **Detected:** partial loss or torn restore of a journal (§5.4 witness); project-namespace
  rollback (§5.4 high-water); a trust store restored with counters below any document still on
  disk; any restored state, because restore itself is the trigger.
- **Not detected locally, stated:** a coherent rollback of the whole install root by an
  attacker who also suppresses the restore marker. Mitigations that remain: the rolled-back
  state ages into refusal (§4.2) and cannot be refreshed without an origin whose counters have
  advanced; the consented refresh path (§6.5) compares counters against the origin; a
  revocation published at the origin cannot be un-published by a local rollback. No claim of
  filesystem-wide rollback detection is made.
- Retained cases: ordinary generation rollback (trust untouched, selection re-verified under
  the current `trustEpoch`); whole-project restore below high-water (quarantine); whole-install
  restore (UNBOOTSTRAPPED/RESTORED until payload); witnessless restore.

## 6. DR-105 and DR-114

### 6.1 Execution mode — child-process only (unchanged from v1).
### 6.2 FC-C1 — recorded (unchanged).

### 6.3 Outcome vocabularies and PR-6 (SEC-S2)

Host and component outcomes as v1 §6.3. **PR-6.** The pre-existing-policy carrier is the closed
schema `permission-policy.schema.json` (`grants`, `denies`, `consents`; `additionalProperties:
false`); the checker asserts it has no member whose name contains "confine" or "sandbox". The
preview therefore has no way to express a confinement requirement, so PR-6's trigger set is
empty by construction, not by default. If a later policy schema adds such a member, an effect
carrying it on a platform/mode where confinement is not enforced refuses PR-6 (file 03:
"required confinement refuses when unenforceable"); first-party trust never satisfies it.

### 6.4, 6.5, 6.6 — as v1 (CA-3 per-subtype dispositions; CA-4 `PATH-TRUST-STATE-REFRESH`
admitted with the root-pinned SPKI and an exact `endpointSet`, the fetched bytes entering as an
ordinary payload; surviving writer). The refresh path also compares the origin's advertised
counters with the local floors; a lower origin counter refuses.

### 6.7 Authoring — as v1; the lead's child workers are authoring FX/R6/R10/doctor/join/G08
with checkers.

### 6.8 FC-REDACT supersession (classified-secret noninterference)

`doctor-contract.v4` FC-REDACT TIER 1 "in whole or in any prefix or suffix of length greater
than zero" is superseded by:

1. **Noninterference.** For any classified secret value `s` and any other value `s'` of the
   same class, the complete report bytes produced with `s` equal those produced with `s'`, holding
   every other input fixed. The report carries the handle and a presence boolean, never a
   function of the value.
2. **Absence of the full value.** The exact secret bytes, in any encoding doctor could emit
   (raw, JSON-escaped, base64, hex), do not occur in the report.
3. **No derived previews or oracles.** No prefix, suffix, hash, length, or truncation of the
   value appears in a member; the `secretPreviewsAreForbidden` rule stands.
4. **Public identifiers are classified separately** (credential handle names, declared variable
   names, component ids) and may appear; the classification is host-known at construction.

The pinned corpus asserts 1 by running each tier-1 input twice with two distinct secret values
and comparing the reports byte-for-byte, 2 by search, and 3 by construction review of the
report schema. Tier 2 remains disclosure with the unmasked high-entropy negative case.

## 7. Control-plane effect bodies

### 7.1, 7.2 — as v1: `effectRequest {effectClass HE-1|HE-2, authorizationRef gj:…, operationRef}`;
`effectResult {requestSeq, decisionSeq, outcomeSeq, commitClass, effectOutcome COMPLETED|FAILED|INDETERMINATE,
resultRef?}`; a not-performed request is a `refusal` RF-6 carrying `decisionClass PR-n`.

### 7.3 Refusal precedence and channel ownership (aligned with control-completion v2)

Under the closed preview vocabulary (16 message types; effect bodies HE-1/HE-2), a locally
originated `RF-5` is unreachable: every unknown structured semantic token is `RF-2`; every
forbidden direction or state (a provider sending `select`) is `RF-7`; every unauthorized host
effect is `RF-6` with its PR-n; a finding-shaped payload on the provider data plane is a
provider-protocol rejection, not a control refusal. The family `RF-5` remains recognized in the
vocabulary for wire compatibility; no local classifier produces it, and no
`semanticActionRequested` flag exists. The security contract merges no channels.

### 7.4 CC-8 — as v1 §7.4 (opaque `detail`; PASS-smuggling dual invariance).

## 8. DR-126 profiles (SEC-M4, SEC-M5)

### 8.1 Value-source legend — as v1 §8.1. Templates carry `valueSource` per member and typed
`{"$releaseMeasured": {field, form, source}}` placeholders; a placeholder that is still present
at qualification refuses that profile.

### 8.2 Core build decisions — as v1 §8.2 (static-PIE musl on Linux, adopted by the lead;
libSystem-only on macOS), with one wording correction: the certificate-store **class** is not
absent on Linux — it holds exactly two DIGEST-BOUND members (§8.4); what is absent on every
profile is a TLS trust-store dependency.

### 8.3 macOS profiles and the measured infeasibility of v48's pathless acquisition

Measured 2026-09-04 on macOS 26.6.2 build 25G83 (Apple silicon):

- `SecCodeCopyGuestWithAttributes` with `kSecGuestAttributePid = 0` returns `errSecCSNoSuchCode`
  (100003): **there is no SecCode guest for the kernel**, so v48's `macosCodesign.pathlessInput`
  ("the running kernel / OS ABI code object as the SecCode guest") cannot be acquired. The same
  call succeeds for pid 1 (`com.apple.xpc.launchd`, cdhash `a7cd36d5…`) and for an ordinary
  process, so the interface itself works.
- `codesign -dvvv` on `/System/Library/Kernels/kernel.release.t6050` and on
  `/System/Library/KernelCollections/BootKernelExtensions.kc` reports "code object is not signed
  at all": the kernel bytes on the sealed system volume carry no per-file code signature.
- `sysctl kern.uuid` = `8D3E13A0-01FC-381D-9DA3-7F0AF537CB32` equals the `LC_UUID` of
  `kernel.release.t6050`; `csrutil authenticated-root status` = enabled; SIP enabled.

**v49 successor scheme `macos-sealed-boot` (this unit's specification; adoption is a reviewed
pair act).** OS ABI identity on macOS is the sealed boot chain, not a code signature:
`authenticityCore {scheme: macos-sealed-boot, payload: {kernUuid, osversion,
bootKernelCollectionSha256, authenticatedRoot, secureBoot}}`. Acquisition: `sysctl kern.uuid`
and `kern.osversion`; SHA-256 of the boot kernel collection file on the sealed volume; `csrutil
authenticated-root status`; boot policy via `bputil -d` (Apple silicon) or
`system_profiler SPiBridgeDataType` (T2 Intel). Trust decision: authenticated root enabled AND
boot policy Full Security AND `kern.uuid` equal to the `LC_UUID` of the kernel image in the
sealed collection selected by `osversion`. Soundness: on Apple silicon the boot chain is
hardware-enforced and the system volume is sealed, so the running kernel is the sealed one by
construction; there is no kexec on macOS. Refuses: reduced/permissive security, unsealed root,
UUID mismatch, x86_64 without T2. This is a semantic successor of v48
`platformAttestationOperation.macosCodesign` for the OS ABI class only; loader and libc keep
v48's schemes. The templates mark the OS ABI entries `schemeStanding: v49-successor-required`.

Profiles `P-MACOS-ARM64-25G83-APFS` and `P-MACOS-X86_64-25G83-APFS` (templates
`security-fixtures.v2/profile.P-MACOS-*.json`, validated): selector `25G83` (MEASURED for arm64;
RELEASE-MEASURED for x86_64 — Apple has generally shipped one build number across architectures,
and a differing runner observation makes the x86_64 profile carry its own selector);
filesystem `apfs`; OS ABI as above (`kern.uuid` measured for arm64); loader `/usr/lib/dyld`
PLATFORM-ATTESTED codesign, arm64e cdhash `9d380d573d6f221b038725112b3b1f206737a429` measured,
x86_64 RELEASE-MEASURED; libc DIGEST-BOUND over the dyld shared-cache file (release-measured,
companion `sonameAbi`); framework, certificate store, font, ICU absent with inapplicability
proofs. Runner requirements: Full Security boot policy, sealed root, SIP, build 25G83.

### 8.4 Linux profiles (v48 honoured as written)

Withdrawn from v1: "kexec_load_disabled=1" and "Ubuntu stock kernel". v48 requires the kernel
member to be structurally kexec-absent (IKCONFIG with `CONFIG_KEXEC`, `CONFIG_KEXEC_FILE`,
`CONFIG_KEXEC_CORE`, `CONFIG_CRASH_DUMP`, `CONFIG_KEXEC_JUMP` unset), attested by the KB-1
`builderAttestation` over the official-header payload, with `/proc/sys/kernel/kexec_load_disabled`
**absent** and `kexec_loaded` 0 if present. Stock distribution kernels enable kexec and cannot
satisfy this. Decision: the Linux OS ABI member is an **OpenSIP-built kexec-absent kernel
package** (`opensip-qual-kernel-6.8-<arch>`) built from the Ubuntu 24.04 kernel source with those
options unset and `CONFIG_IKCONFIG=y`, shipped as an EFI-stub PE image signed for Secure Boot
with the OpenSIP kernel signing key enrolled in db/MOK, installed from the OpenSIP-signed apt
repository so `apt-secure` attests `{name, version, digest}`. KB-1 signs the v48
`builderAttestation` preimage (`memberSha256, peCoffImageDigest, payloadDigest,
kexecCapability, kernelRelease, consumeRelation, headerKind`).

Profiles `P-LINUX-X86_64-UBUNTU2404-EXT4` and `P-LINUX-ARM64-UBUNTU2404-EXT4` (templates
validated): selector `ubuntu:24.04` (PUBLISHED-FACT), filesystem `ext4`; OS ABI
PLATFORM-ATTESTED package-db pathless with the full v48 `linuxForm` (`measuredBootTranscriptDigest`,
`kexecCapability: kexec-absent`, `builderRoot`, `builderPublicKey`, `builderSignature`,
`builderRootDigest`, `ikconfigDigest`), every value RELEASE-MEASURED with its form and source;
**two certificate-store DIGEST-BOUND members**: the KB-1 public key (the `builderRoot` member)
and the qualification runner's TPM AK certificate (`akCertificateMember`); loader, libc,
framework, font, ICU absent with proofs (static-PIE musl core has no `PT_INTERP`). Runner
requirements: UEFI + TPM 2.0 (vTPM acceptable) + TCG2 log, Secure Boot enabled, the OpenSIP
kernel package, `kexec_load_disabled` absent, ext4 install root. The D-006 runner-class
successor records these.

### 8.5 Carrier and `verifiedInstallRoot` (SEC-M5)

The carrier is the inventory document (`opensip.metadata.inventory.1`, TR-CORE 2-of-3) with
the `inventorySchema` TCB field keyed by complete `platformProfileKey` and the non-inventory
`verifiedInstallRoot` field. Per v48 `filesystemMeasurementTarget.signedBinding.serialization`,
the **signed token** `T` is the single character `/` when the verified tree root itself is the
target, else a relative NFC path; the host joins `T` with its local exact-byte install anchor
`A` and canonicalizes `join(A, T)`; two comparisons apply — token bytes against the signed
carrier (carrier defect on mismatch) and the canonical host path against the preselection
observation (volume defect on mismatch). `verifiedInstallRoot` is therefore not "automatically
`/`" as a host path: it is `T = "/"` in the signed carrier resolved to the actual canonical host
path at preselection.

### 8.6 Product consequence (stated, not hidden)

Under the accepted v48 grammar a Linux host selects a qualified profile only when its running
kernel is an allowlisted kexec-absent member. For the architecture preview that means the
OpenSIP-provided kernel/runner image; a host on a stock distribution kernel selects no
qualified profile and the core refuses (NT-TCB-1/NT-TCB-3), never degrading. Linux remains in
D-002's slice 1; nothing is removed from scope. A later reviewed v48 successor could widen
this only with an equivalent running-kernel binding; runtime `kexec_load_disabled=1` is not
such a binding (a kernel reached by kexec can report anything). This is one of the consequential
decisions the lead may choose to surface to the user under D-367.

## 9. Evidence, checker report, and what remains authoring

`check-security-unit.v2.py --report security-unit.v2.report.json` reproduces every vector,
validates every example against its schema, runs the envelope positive and five negatives in
the §2.2 order, runs the manifest admission positive and two negatives, recomputes the journal
chain and column/body binding on the retained SQLite database, re-exercises the append-only,
contiguity, GRANT-binding and terminal guards on a fresh database from the retained DDL, and
validates the four profile templates. The report records the sha256 of every input, the
checker's own digest, Python 3.14.6, SQLite 3.53.3, OpenSSL 3.6.3, and the Unicode table:
**reference 16.0.0 versus the production freeze at 15.1** (paired draft §4); the collision
cases in this unit contain no code point whose properties changed between those tables, and
production must vendor 15.1 as declared.

Still authoring, not decided here (D1 with checkers): FX-1..FX-13, R-10, R-6, twelve doctor FC
and thirteen join implementations, G08 FC-*, G22 fixtures against the frozen templates, the G21
CC-8 successor golden, and the v49 macOS successor's own acquisition fixture.

## 10. Leftover obligation mapping

As v1 §10 with these changes: DR-126 `OBL-RESERVED-TABLES` populated in typed templates with a
named v49 dependency for macOS OS ABI; DR-103 index custody split recorded (§4.5) as a scoped
successor of v11 `indexSchema`; DR-114 FC-REDACT superseded (§6.8); DR-105/DR-114 `OBL-BLK-*`
as v1.

## 11. External references

As v1 §11, plus: Apple, "Porting just-in-time compilers to Apple silicon" (allow-jit,
MAP_JIT, write-xor-execute); Node.js `tools/osx-entitlements.plist` (v24.x) as the record of what
Node's own builds enable; nodejs.org v24 single-executable-applications (macOS arm64 only);
`SecCodeCopyGuestWithAttributes` behavior measured locally 2026-09-04.

## 12. What this contract does not do

As v1 §12, plus: does not adopt the v49 successor (it specifies it); does not build or sign a
kernel; does not claim rollback detection beyond §5.5; does not give the host any release key.
