# Security, trust and platform-TCB completion

Author: Claude (Herdr `wH:p2`). Status: PROPOSED, awaiting independent review under D-368.
Scope: DR-112, DR-105, DR-114, DR-124, DR-126, DR-101 OD-101-2, plus the metadata
canonicalization and signature profile that DR-103 ID-DEP-1, DR-112 envelopePreimageJoin
and the DR-111/DR-103 lock serialization all wait on. Date: 2026-09-04.

This is a V2 architecture-preview design successor. It binds NOTHING until recorded under
D-368; it edits no register cell; it authorizes no implementation; it claims no platform
qualification. Every number below is a decided architecture target with a stated
falsifiability path (the D-006 form). Every value that can only exist at a future release is
marked RELEASE-MEASURED with its schema and its rejection rule; none is invented.

## 0. Pins, incorporation, and explicit supersessions

Measured at HEAD `12f8783` (`D-368: adopt reciprocal review and integrated architecture
closure`); file 08 unchanged at
`872f0929926f996ee475642426c6ba33bec7bd6aa3eec6b6a927f2b197618bd6`.

| Incorporated contract (docs/coop/artifacts/) | sha256 | Recorded at |
|---|---|---|
| `signed-index-trust-contract.v14.json` | `039a570244441709c8a773d2c92944fff7ad1b249718656ab2d87645feec6715` | D-309 |
| `platform-tcb-contract.v48.json` | `9511fca3f795ff66b101257796d4bf80d49c754271cc76139a015efed5fbb98c` | D-361 |
| `permission-truth-tables.v9.json` | `05d559647d103a47c18ed5177b71900a1d9dfcdea6b9a1255aefcec5f09eaccb` | D-128 |
| `host-effect-authorization.v25.json` | `b91b9f739b10b1bd30eb56b9d68feac81c483ad86f50e11ed33b95e98ae2d9b9` | D-126 |
| `doctor-contract.v4.json` | `df2e717555616db096e61548458f23b442f7f0e37b2d2461eabc2c33201e94b3` | D-035 |
| `doctor-actor-join-integration-contract.v8.json` | `c830f954605a4a1d47c5643230439340994a0c42c4a487359541c578d00bc662` | D-129 |
| `state-class-contract.v11.json` | `b5456c63e865b53738b1f11f46a898438afca7890a6069a8653aad6ea78d86bb` | D-284 lineage |
| `distribution-core-inventory-contract.v16.json` | `429b8c7a9cd5c8f2b495337c055ccbd262e796ba1cc42efb173779c72018fb5b` | D-114 |
| `component-manifest-schemas.v11.json` | `1c0b8868444a097256aaa7d9caf8ebaa1c6f73fb071dbb4dd712334abb17a005` | D-104 |
| `canonical-json-profile.v1.json` | `6f7c906cb739a1313d68f5dd8bc31285d5f213c63649d3d54e1f9e88e5496710` | cited by D-104 ID-DEP-1 |
| `control-protocol-contract.v2.json` | `c50a79fef566ecccbd8913a3d309b0cf7332f7d77f892474a548ef3d7b4ebdca` | D-015 |
| Paired draft `docs/coop/completion/distribution-runtime-completion.v1.md` | `506e40a4f831b476d1fb3ac066477203ff1371c6fb623cb7f2844c8434d0d6e7` | not recorded |
| Paired draft `docs/coop/completion/control-message-schema.v1.json` | `f446d1fdac6580e5d6f1125d0bc642f72f493f7bc63895c44d0b312a2bb9c8dd` | not recorded |

**Incorporation rule.** On application this contract incorporates, by exact section name,
the design sections listed per contract below. Status fields, `reviewGuidance`, repair logs,
`reMeasurementAtVn`, `honestyRepairsFromVn` and pre-recording disclaimers are provenance, not
fresh decisions. Nothing is incorporated by "latest filename".

**Superseded sentences, by name.** Only these change. Everything else in each contract stands.

1. `signed-index-trust-contract.v14` — incorporated: `roles`, `machine` (states, events,
   transitions, `statePrecedence`, `defaultTransition`, `fallbackByEvent`,
   `outcomeBranchDiscipline`, `recoveryTrustedEntry`, `refusalReasonVocabulary`, `failClosed`),
   `offlineRunningPolicy`, `airGapPayload`, `trustPolicyShape`, `recoveryAuthorityShape`,
   `recoveryCeremony`, `auditAndWaiver`, `monotonicStore`, `fixtureClasses`, `g08`, `g06`.
   Superseded: `namedOpenDecisions[OD-112-1].standing` "RESERVED. Named. Not minted." → §4.1;
   `[OD-112-2].standing` → §4.2; `[OD-112-4].standing` "RESERVED to product/release" → §4.4;
   `[OD-112-3].standing` residual axis → §4.3; `trustPolicyShape.standing` "SHAPE ONLY. No
   quorum, skew, or freshness NUMBER is minted" → numbers minted in §4;
   `trustPolicyShape.envelopeJoinStanding` "DECLARED and INACTIVE until ID-DEP-1 and this row's
   envelope semantics activate" → ACTIVE on joint application of §2 and this contract;
   `identityDependencies[ID-DEP-T2].consequence` and `[ID-DEP-T6].consequence` → §2 and §5.
   `machine.transitions[*].whenInactive` members remain as written for any host on which §2 is
   not applied; on an applied host every TRUSTED-entry member is ACTIVE.
2. `platform-tcb-contract.v48` — incorporated: `taxonomy`, `identityRuleShape`,
   `identityEvidenceUnion`, `signedEntry`, `resolutionPredicate`, `loaderTraces`,
   `negativeTests`, `tcbCarrier`, `platformProfile.selectorGrammar`,
   `platformProfile.filesystemMeasurementTarget`, `platforms`. Superseded:
   `platformProfile.slice1ProfileStems[*].supportedVersionOrBuildSelector.standing` and
   `[*].filesystemWhereItAffectsResolution.standing` "RESERVED" → populated in §8;
   `platformProfile.memberPopulation` "Per-OS concrete TCB members remain RESERVED" →
   populated in §8 with per-value source classes; `platformProfile.populationPacket` "Standing
   remains RESERVED" → this contract is the population packet (owner: Security + release +
   platform owners per D-341, delegated under D-367).
3. `permission-truth-tables.v9` — incorporated: `permissionVocabulary`, `truthTables`,
   `linearization`, `raceSemantics`, `refusalFamilies`, `acceptanceEvidenceFixtureClasses`,
   `identityDependencies`. Superseded: `identityDependencies[ID-DEP-P10]` (execution mode
   undecided) → §6.1 child-process only; `[ID-DEP-P5]` (journal class undecided) → §5.3;
   `[ID-DEP-P6]` (crash mechanics undecided) → §5.4; `[ID-DEP-P8]` (wire carriage) → §7;
   `[ID-DEP-P13]` (PR-6 trigger set) → §6.3 empty by decision; `truthTables.tables[*].rows[*]
   .ENFORCED.byExecutionMode.in-host-process` cells become INAPPLICABLE-IN-PREVIEW (mode not
   admitted), their text retained as the reason the mode is refused.
4. `host-effect-authorization.v25` — incorporated whole. Superseded: `layers.designContract`
   "Becomes a live prerequisite only when Operability+security jointly with Security+platform
   record it" → recorded by §6.2 (the delegated joint owners' act under D-367);
   `coveredActs.CA-3.subtypes[*].standing` → §6.4 per-subtype decisions;
   `coveredActs.CA-3.subtypes[PRIVILEGED_PLATFORM_FACILITY].productAdmissionAuthority`
   "UNOWNED" → Security + platform owners; `slice1EgressExecutionSide.namedArchitecturePreviewPaths
   [*].productAdmission` → §6.5; `effectCommit.processDeath` "The missing crash-report surface
   is UNOWNED-AND-NEEDED" → §6.6 names the surviving writer.
5. `doctor-contract.v4` — incorporated: `modes`, `stableMachineSchema`, `consentModel`,
   `redaction`, `outcomeStructure`, `degradedAndHostileInputs`, `doctorRemediationRecord`.
   Superseded: `consentModel.mandatoryPostReport.rule` "the record is written with the reserved
   effectOutcome member unpopulated" → populated per `host-effect-authorization.v25
   .outcomeVocabulary.serialization.normativeBinding` (already the binding after D-126; restated
   here so the two artifacts agree at application). `permissionRef` stays reserved (D-032).
6. `doctor-actor-join-integration-contract.v8` — incorporated: `extractedDecidedClauses`,
   `joinFixtureClasses`, `remainingNamedNotResolved`. Superseded:
   `remainingNamedNotResolved.items[0]` (FC-C1 unrecorded) → §6.2.
7. `state-class-contract.v11` — incorporated: `classes`, `bytePlacement`, `manifestDeclaration`,
   `negativeTests`, `g19`, `proposedSupersession` SUP-124-GRANT-JOURNAL. Superseded:
   `proposedSupersession.standing` "Application requires ... a user-express D-096 (A) grant
   covering every named role" → concurrence recorded in §5.3 by the delegated owners under
   D-367; `bytePlacement[trust roots / revocation observations / expiry floors / anti-rollback
   counters].standing` "EXPRESSLY-RESERVED" → SC-TRUST (§5.1); `bytePlacement[component index
   custody records]` → §5.2; `bytePlacement[rollback slots and provisional generations]` and
   `[prepared migrations and repair state]` → §5.2 (SC-OPS for the lifecycle half; repair state
   stays reserved with DR-110).
8. `distribution-core-inventory-contract.v16` — incorporated: `inventorySchema`, `threeCores`,
   `defaultInstall`, `gatesG01G05`. Superseded: `namedOpenDecisions[OD-101-2].standing`
   "RESERVED" → §3.
9. `component-manifest-schemas.v11` — incorporated: `manifestSchema.signatureBinding`,
   `manifestSchema.encodingRule`, `indexSchema.custodyRule`, `rejectionRules` RJ-3/RJ-4/RJ-6.
   Superseded: `identityDependencies[ID-DEP-1].ridesOn` "This artifact invents NO
   canonicalization rule" → §2 supplies it; `rejectionRules[RJ-4].conditionalSubcode`
   "ENVELOPE_MISMATCH ... is DECLARED here and INACTIVE" → ACTIVE on application of §2.
10. `canonical-json-profile.v1` — incorporated: `theRecoveredFunction.rules` CJ-R01..CJ-R14,
    `orderingPlanes`, `jcsHazardMeasured`. Superseded for the METADATA profile only:
    `undeterminedRegister` UR-1..UR-5 → decided in §2.1. The V1 PlanIntent commitment
    (`opensip-canonical-json-v1` as used by `c2-plan-stage-schema`) is NOT edited: §2 defines a
    separately named profile for V2 metadata, byte-identical to the recovered function wherever a
    vector forces it, and settles the undetermined region only under the new name.
11. `control-protocol-contract.v2` — not superseded. §7 supplies effect-message body
    vocabulary that the lead's `control-message-schema.v1.json` binds; the CC-8 successor the
    lead proposed (opaque `detail`) is endorsed in §7.4 with the channel and refusal-family
    precedence the lead stated.

**Sub-obligation rides (Limb D, per claude-initial-audit.md §2 C1 and the lead's agreement).**
Recorded here with re-entry triggers, no scope removed: DR-105/DR-114 BLK-1 (CA-2) rides
D-002's DR-105 scoping; CA-3 KEYCHAIN rides DR-108; DR-124 SC-EVIDENCE rides D-002 "touched
classes"; DR-122 `FC-OUTFAIL.committed-run-preserved` rides D-077. See §10.

## 1. Threat model boundary this contract holds

File 03's laws are carried whole: deny wins; absence denies; a manifest, repository or publisher
cannot grant authority to itself; required confinement refuses when unenforceable; CI never
prompts and needs pre-existing policy; trusted-code fallback needs explicit consent bound to
exact component bytes, operation, scope and platform. A child process is fault containment,
not a sandbox. Nothing below claims confinement of first-party trusted code; the ENFORCED
column stays DISCLOSURE-ONLY on every cell it is DISCLOSURE-ONLY today, except the one cell
§6.1 makes ENFORCED-BY-CONSTRUCTION by admitting only the child-process mode.

Adversaries this contract must defeat at the byte level: a tampered or substituted release
artifact; a replayed stale index; a rolled-back trust store; an ambient library or loader
substitution; a manifest that grants itself authority; a component that smuggles a verdict
through free text; a metadata document whose parsed identity differs between admitter and
consumer. Adversaries it does not claim to defeat: malicious first-party code with the user's
ambient authority (disclosed, not contained), a compromised OS, a compromised Apple or
distribution signing chain.

## 2. Metadata canonicalization and signature profile (closes DR-103 ID-DEP-1)

### 2.1 `opensip-metadata-canonical.1`

The function is `opensip-canonical-json-v1` exactly as recovered in `canonical-json-profile.v1`
rules CJ-R01 to CJ-R14, with the five undetermined points decided as follows. Where a decision
below and a future settlement of the V1 PlanIntent profile ever disagree, the metadata profile
is versioned to `.2`; V1 bytes are never reinterpreted.

| UR | Decision | Reason |
|---|---|---|
| UR-1 key order plane | Ascending Unicode scalar value, which equals unsigned UTF-8 byte order. UTF-16 code-unit order is refused as an implementation. | Both prose witnesses agree; JCS diverges only in the vector-blind region and must not be used (jcsHazardMeasured). |
| UR-2 integers | Signed 64-bit two's complement range, `-9223372036854775808` to `9223372036854775807`. Zero is the single byte `0`. Negatives carry one leading `-`. Out of range refuses `INTEGER_OUT_OF_RANGE`. | Matches CVE1's i64 bound so no metadata integer can exceed what a sibling encoding can carry. |
| UR-3 NFC | REJECT non-NFC strings and keys (`NON_NFC_STRING`); keys that collide after NFC reject (`NFC_KEY_COLLISION`). The encoder never normalizes. | Signing must never transform supplied bytes (the DR-103 path rule: "never normalize a supplied path and thereby change signed bytes"). |
| UR-4 escaping | Exactly CJ-R08: `\"`, `\\`, `\b` `\t` `\n` `\f` `\r`, `\u00xx` lowercase for other code points below U+0020, nothing else escaped; solidus and all code points at or above U+0020 emitted raw as UTF-8. | Shortest, deterministic, no ASCII-only mode. |
| UR-5 lone surrogates | Reject (`LONE_SURROGATE`). | The data model is Unicode scalar values. |

Also binding: duplicate keys reject at parse (CJ-R11, and RJ-6 DUPLICATE_JSON_KEY names the key);
floats reject (CJ-R12); non-string keys and non-model leaves reject (CJ-R13); empty containers
are present (CJ-R07); array order preserved (CJ-R09).

**Domain-separated digest.** `preimageSha256 = SHA-256( UTF-8(domainTag) || 0x00 ||
canonicalBytes )`, rendered as 64 lowercase hex characters. The closed domain-tag registry:

| Tag | Document |
|---|---|
| `opensip.metadata.manifest.1` | component manifest (DR-103 `manifestSchema`) |
| `opensip.metadata.index.1` | signed index snapshot (DR-103 `indexSchema`, §4.5 trust members) |
| `opensip.metadata.lock.1` | component lock (DR-103 `lockSchema`, serialized per the paired draft §3) |
| `opensip.metadata.root.1` | trust root document (§3.1) |
| `opensip.metadata.revocation.1` | revocation list (§4.5) |
| `opensip.metadata.inventory.1` | published signed-closure inventory, the DR-126 carrier (§8.5) |
| `opensip.metadata.payload.1` | air-gap payload manifest (§4.6) |
| `opensip.metadata.envelope.1` | the `subject` block of a signature envelope (§2.2) |
| `opensip.metadata.journal.1` | grant-journal record bodies (§5.4) |
| `opensip.metadata.test.1` | vectors only; never a shipped document |

An unregistered tag is a refusal, not an extension point.

**Vectors** (retained at `security-vectors.v1.json`, sha256
`62212a6ac0ab52e751f28ac8813b2e214027bb147393b551e18e86653e41f876`; checker
`check-security-vectors.v1.py`, run green on 2026-09-04):

- V-MAN-1, a manifest-shaped object, canonical bytes
  `{"kind":"component","manifestSchemaVersion":1,"name":"typescript-provider",...}` under
  `opensip.metadata.manifest.1` → `e8f375b364c8bdbe32ebe40966a565c88ab55646da866d166a7b2516af13b548`.
- V-UR1, keys U+E000 and U+10000: canonical hex `7b22ee8080223a312c22f0908080223a327d`
  (U+E000 first) → `ee5518aadcef59a07c852773b056bc1a5fe745377942b2503ba532051061ac4e`.
- V-UR2, `{"a":0,"b":-1,"c":9223372036854775807,"d":-9223372036854775808}` →
  `78523d08b6efcd8bc5ad716ac902de8dfdce7cd75e8c9d0d3bb58fba761ea887`; 2^63 and -2^63-1 reject.
- V-UR3, NFD `e`+U+0301 rejects `NON_NFC_STRING`; NFC `é` canonical hex `7b2273223a22c3a9227d` →
  `7ade765ed188e8688cb77c70342dff95e2c41b97589b19c20e8b92e6ad01a600`.
- V-UR4, `a"b\c/de<TAB>fég😀` canonical hex `7b2273223a22615c22625c5c632f64655c7466c3a967f09f9880227d` →
  `7d80874a55486504f8b9c0d69dbb5e48e937aa8072899fbf636b1917096023de`.
- V-UR5 lone surrogate, V-FLOAT, V-NFC-KEY-COLLISION reject with the named codes.

### 2.2 `opensip-signature-envelope.1`

A detached envelope per signed document (DR-103 `signatureBinding`: the manifest carries no
signature field). JSON, itself canonicalizable under §2.1:

```json
{
  "envelopeSchema": 1,
  "subject": {
    "kind": "manifest",
    "domain": "opensip.metadata.manifest.1",
    "storedSha256": "<hex64: sha256 of the exact stored bytes; the DR-103 admission digest>",
    "preimageSha256": "<hex64: domain-separated canonical digest per 2.1>"
  },
  "role": "TR-COMPONENT",
  "namespace": "opensip",
  "signatures": [
    { "keyId": "<hex64>", "alg": "ed25519", "signature": "<hex128>" }
  ]
}
```

- `kind` is the closed set `manifest | index | lock | root | revocation | inventory | payload`.
- `role` is one of the DR-112 roles; `namespace` is the delegated publisher namespace the role
  key set is authorized for (`roleToKeyAndDelegatedNamespace`).
- **Message signed:** the 32 raw bytes of `preimageSha256` (pure Ed25519, RFC 8032, no
  prehash, empty context). Signing the digest rather than the document keeps the signer's input
  fixed-size and makes the envelope independent of document length.
- `keyId = SHA-256(32-byte Ed25519 public key)` as hex64, the same form `platform-tcb-contract
  .v48` uses for `builderRootDigest`. `alg` is closed at `ed25519`; an unknown `alg` refuses.
- `signatures` is ordered by ascending `keyId` bytes; duplicates of one `keyId` refuse.

**Verification order and refusal mapping** (RJ-4 owns the byte level; DR-112 owns trust):

1. Envelope absent where policy requires one → `RJ-4 UNSIGNED`.
2. `sha256(stored bytes) != subject.storedSha256` → `RJ-4 DIGEST_MISMATCH`.
3. Canonicalize the stored bytes under `subject.domain`; a §2.1 refusal, or
   `preimageSha256 != recomputed` → `RJ-4 ENVELOPE_MISMATCH` (now ACTIVE).
4. For each signature: `keyId` resolves in the current trust root for `role`+`namespace`;
   Ed25519 verify over the 32 preimage bytes fails → that signature is discarded and the failure
   audited; if every signature fails → `RJ-4 ENVELOPE_MISMATCH`.
5. Count valid signatures from distinct authorized keys against the role threshold (§4.1). Below
   threshold → DR-112 `thresholdEvaluation` failure (trust-policy refusal; stay non-TRUSTED),
   not RJ-4.

Example (V-SIG-1, TEST key, never a release key): public key
`4bf28e164456cfc58888eadfa2c80b92ea5722191ffc800564cd8853abdaa620`, keyId
`64923ff5a4ac3969a0828d819d4849d6ec20ff367417d587fe44a3e58d82a81b`, signature over the V-MAN-1
preimage bytes `0989b2560b0beb9488d0ae3fff122c4f21dc6f412de00eb0c2795c94917754934d1f1e5762c6dd1c
22630f2164986d87877598fb5a8589a0a5dd0b2319c92d0b`, verified with OpenSSL 3.6.3 `pkeyutl -verify
-rawin`.

**Standing of V-MAN-1:** a FRAGMENT-ONLY canonicalization vector (its role, platforms and
permissions shapes are not the accepted `component-manifest-schemas.v11` shapes). It exercises
§2.1 and nothing else; it is never an admission fixture.

**Schema-valid pair (retained under `security-fixtures.v1/`, verified by the checker):**
`typescript-analyzer.manifest.json` is a full manifest conforming to
`component-manifest-schemas.v11` — `role: analyzer`; the control tuple
`{roleSubprotocol: "typescript", subprotocolVersion: 1}` on each of five capability declarations
(`typescript.parse-fidelity`, `.semantic-resolution`, `.graph-construction`, `.facts`,
`.coverage`, each carrying `declarationData` with `language`, `rungs` and `relations`); four
structured platform trees with `entrypoint: bin/entry`; `permissions[].permission` from the
closed PT-* set; six digest-bound declarations; typed-null `stateMigration` / `updateData`;
and `compatibility.hostCore` as the interval `{min: "0.1.0", max: "0.2.0", includeMin: true,
includeMax: false}` — the cross-surface decision that the initial provider must not pin the host
release exactly, so `0.1.x` host patches (which preserve accepted APIs and component-state major
1) stay compatible while `0.2.0` refuses; the paired draft's selection fixtures add the core
`0.1.1` positive and `0.2.0` negative cases. Its bytes are fixture placeholders (a stub runtime
node, a stub entry script), never a shipped component.

| Item | Value |
|---|---|
| stored bytes sha256 (`storedSha256`, the admission digest) | `d855bbcd6486077f1b915d11b7b9b84d5cefb1cd136f08391125ccdb0f1b3fa5` |
| canonical bytes (`typescript-analyzer.manifest.canonical.bin`, 5525 bytes) | as produced by §2.1 |
| `preimageSha256` under `opensip.metadata.manifest.1` | `4dac747d7c1dcdf1f4a8606d61c8145a9be8df3453317d6a46fb28bb0931959a` |
| `typescript-analyzer.envelope.json` | one TR-COMPONENT signature by the TEST key (keyId `64923ff5…`) over those 32 bytes; verifies at every step of the order above (threshold evaluation is DR-112's and is outside the vector) |
| `typescript-analyzer.envelope-mismatch.json` | same `storedSha256`; `preimageSha256` `77546c0ddf2548ac2894dcd871d7dad9de43dcfee48a62d25110834d6e86765e` computed over the same manifest with `version` `1.0.1`; the signature is cryptographically valid over that carried digest |

Verification of the mismatch envelope: step 1 passes (envelope present), step 2 passes
(`storedSha256` matches), step 3 recomputes `4dac747d…` ≠ carried `77546c0d…` →
`RJ-4 ENVELOPE_MISMATCH`, admission refused. Because the manifest is schema-valid, no RJ-6
structural refusal can fire first and mask the crypto mismatch; this is the isolated-admission
case the DR-103 TC-SIG class and the conditional G15 C-ENVELOPE / C-CANON cases need.

### 2.3 What activates on application

- DR-103 ID-DEP-1 closes for metadata; RJ-4 ENVELOPE_MISMATCH is decidable.
- DR-112 `envelopePreimageJoin` is ACTIVE; every `whenInactive` branch becomes unreachable on an
  applied host, and `FC-ENVELOPE-INACTIVE` becomes a negative fixture that asserts the branch is
  unreachable (not that it fires).
- The DR-103 lock (paired draft §3) serializes under `opensip.metadata.lock.1`; lock production
  is enabled only when both this contract and the paired draft are applied, as that draft states.
- The DR-126 signed carrier (§8.5) is the inventory document under `opensip.metadata.inventory.1`.

## 3. DR-101 OD-101-2: code-signing ceremony and OS notarization

### 3.1 Key hierarchy (`opensip-root.1`)

| Role | Keys | Threshold | Custody | Expiry of the signed document |
|---|---|---|---|---|
| Root anchor | R-1, R-2, R-3 | 2 of 3 | offline, hardware-backed (FIDO2/HSM class), three distinct holders | root document 365 days |
| Recovery authority | RA-1..RA-5, disjoint from R-* | 3 of 5 | offline, distinct holders | bound to the root document |
| TR-CORE | K-core-1..3 | 2 of 3 | release-signing HSM/KMS, two-person approval per use | listed in root; rotate at least yearly |
| TR-INDEX | K-index-1..3 | 2 of 3 | same | same |
| TR-COMPONENT (first-party) | K-comp-1..3 | 2 of 3 | same | same |
| TR-BUNDLE | K-bundle-1..3 | 2 of 3 | same | same |
| TR-REPAIR | none minted | typed absence | DR-110 deferred | — |
| Kernel attestation (§8.4) | KB-1 | 1 of 1, plus the inventory it lives in is TR-CORE 2-of-3 | release engineering HSM | listed in root |

The root document carries: `rootVersion` (strictly increasing integer), the root key set and
threshold, every role key set with its threshold and delegated namespace(s), the recovery
authority set, `issuedAt`, `expiresAt`, and the pinned SPKI (§6.5) of the index origin. It is
signed under `opensip.metadata.root.1` by root threshold. **Rotation follows the TUF root
chaining rule:** root version N+1 is accepted only when signed by the threshold of keys listed
in version N and by the threshold of keys listed in version N+1 (TUF specification §6.1).
Role keys rotate by publishing a new root document. Revocation of a key or a namespace is a
revocation-list entry (§4.5) signed by root threshold. Compromise of a single role key changes
nothing without a second key; compromise of two of three role keys is recovered by root
rotation; loss of two root keys is the recovery ceremony (`recoveryCeremony`, 3-of-5).

### 3.2 Release ceremony (order is normative)

1. Reproducible build of every platform artifact from the pinned tool closure (paired draft §2).
2. **macOS:** `codesign --sign "Developer ID Application: <team>" --options runtime --timestamp
   --entitlements <minimal.plist> <mach-o>` for every Mach-O in the closure. Hardened runtime and
   library validation on; entitlements file contains no `com.apple.security.get-task-allow` and no
   JIT/unsigned-memory entitlements; the secure timestamp is mandatory (Apple: "Include a secure
   timestamp with your code-signing signature"). Then `xcrun notarytool submit
   core-macos-<arch>.zip --keychain-profile <profile> --wait` and retain the notarization log
   (`notarytool log <id>`).
3. **Linux:** no OS signing exists for ELF; step 4 is the whole trust.
4. Compute the inventory (`inventorySchema` nodes `{path, sha256}`) over the FINAL executable
   bytes: on macOS that is the code-signed Mach-O (codesign rewrites the file; notarization does
   not). Sign the inventory under `opensip.metadata.inventory.1` with TR-CORE 2-of-3. This
   envelope is what DR-G07 "verified bytes equal executed bytes" checks at install and at launch.
5. Assemble distribution containers: (a) macOS `.pkg` (flat installer) signed with the
   Developer ID Installer identity, notarized, then `xcrun stapler staple <pkg>`; (b) a
   `.tar.zst` per platform containing the identical signed files plus the inventory and envelope.
   Sign each container's sha256 list under TR-BUNDLE (TR-BUNDLE is named; a preview may ship the
   `.pkg` and tarball without an offline-bundle role payload, as a typed absence).
6. Publish the signed index snapshot (TR-INDEX 2-of-3, §4.5) that names the release entries and
   their digests; publish the revocation list if changed.
7. Ceremony audit: every signing act appends an `auditAndWaiver.audit` record (role, event,
   outcome, payload digests, clock observation). CI runners never hold R-*, RA-* or K-* private
   keys; they hold a submission credential for the KMS that enforces two-person approval.

**Honesty about the bytes.** The secure timestamp and the Apple signature make the signed Mach-O
non-reproducible from source alone; the reproducibility claim is for the UNSIGNED payload tuple
(paired draft §2) and the signed bytes are custody-pinned, never described as reproducible. A
bare executable cannot carry a stapled ticket: `stapler` supports UDIF disk images, code-signed
bundles and flat installer packages only (Apple documentation and the local `xcrun stapler`
usage text on 2026-09-04). Therefore the `.pkg` is the offline-Gatekeeper-verifiable channel;
the tarball relies on the OpenSIP inventory envelope, and a tarball extracted by `tar` carries
no quarantine attribute so Gatekeeper does not assess it. Both channels ship the same signed
Mach-O; the inventory digests are identical across channels.

### 3.3 What the host verifies, and when

At install: the container's TR-BUNDLE list (when present), then the inventory envelope
(TR-CORE), then every inventory node's sha256 against extracted bytes, in private staging, before
publication (paired draft §5 step 2). At launch: the DR-G07 open-then-verify of the same
immutable objects, plus the DR-126 resolution predicate (§8). Failure anywhere refuses the
generation; never a warning.

## 4. DR-112 numbers and policy

### 4.1 OD-112-1 quorum and threshold cardinality — DECIDED

Thresholds are those of §3.1. `EV-QUORUM-OBSERVE` counts the role's keys that are listed in
the current accepted root document, not expired, and not revoked; the observed cardinality
below the role threshold enters `ST-QUORUM-LOST`. The recovery threshold is 3 of 5.
Falsifiability: if a release process cannot reach two signers within its release window, the
lawful path is a root document that adds keys (threshold unchanged) or a reviewed successor with
the measured evidence; never a single-signer release.

### 4.2 OD-112-2 clock skew and freshness floors — DECIDED

| Quantity | Value | Machine effect |
|---|---|---|
| Root document expiry | 365 days from `issuedAt` | `ST-EXPIRED` for every role when the root expires |
| Index snapshot expiry | 90 days from `issuedAt` | `TR-INDEX` → `ST-EXPIRED` |
| Core / component release entries | no independent expiry; bound by the index snapshot that names them | — |
| Revocation-list freshness floor | 90 days: `now − revocationList.issuedAt > 90 d` → `ST-STALE-REVOCATION` for every role | `EV-CLOCK` |
| Future-time tolerance | 24 hours: metadata with `issuedAt > now + 24 h` refuses (`expiryAndFutureTime`) | payload refused, state unchanged |
| Clock monotonicity | the host's evaluation clock is `max(wallClock, lastAcceptedIssuedAt)` where `lastAcceptedIssuedAt` is the newest `issuedAt` of any accepted document, held in SC-TRUST; a wall clock earlier than that is used only for audit and cannot un-expire anything | `EV-CLOCK` |
| Anti-rollback | per-role `snapshotVersion` and `rootVersion` counters in SC-TRUST; a presented document with a lower counter refuses; equal counter with different bytes refuses | `antiRollback` |

Consequences, stated so they are not discovered: an offline install that receives no payload for
90 days can continue already-running verified components but admits nothing new
(`offlineRunningPolicy`, INDEX expired + COMPONENT trusted + CORE trusted); at 365 days without a
root refresh it refuses everything. The consented online refresh path (§6.5) exists so this
cliff is reachable only by choice. Falsifiability: the numbers bind G08 fixtures FC-EXPIRED,
FC-FUTURE, FC-STALE-REV, FC-EVENT-ORDER; if operations show them infeasible, a successor with
the measured evidence changes them.

### 4.3 OD-112-3 — residual axis DECIDED

The `alreadyRunning` token for `TR-COMPONENT` in `ST-REVOKED` is `refuse`, with no
product-stage qualifier: fail-closed at every stage, not only preview. OD-112-3 leaves
`namedOpenDecisions` and is recorded as DECIDED; `refusalReason` stays
`CONTINUE-COMPONENT-NOT-TRUSTED`.

### 4.4 OD-112-4 G08 waiver — DECIDED

A G08 waiver: maximum 30 days, one renewal of at most 30 days, each carrying product AND release
authority, an `expiresAt`, a measured residual, and an `auditAndWaiver.audit` record; it never
waives an inherited semantic or trust blocker and never waives a `ST-REVOKED` refusal.

### 4.5 Documents the machine consumes

- **Index snapshot** (`opensip.metadata.index.1`): `indexSchema` fields plus trust members
  `snapshotVersion`, `issuedAt`, `expiresAt`, `rootVersionRequired`. Signed TR-INDEX 2-of-3.
- **Revocation list** (`opensip.metadata.revocation.1`): `revocationVersion`, `issuedAt`,
  entries `{subject: keyId | namespace | stableId+version | snapshotVersion, reason, revokedAt}`.
  Signed root 2-of-3. Monotonic: a list with a lower `revocationVersion` refuses; an accepted
  list advances `lastKnownRevocation` (`EV-REVOKE`).
- **Root document** (§3.1).

### 4.6 Air-gap payload

A directory whose manifest (`opensip.metadata.payload.1`, signed TR-BUNDLE 2-of-3) carries
`payloadKind` (`ordinary | recovery`, inside the signed preimage so a presenter cannot relabel it),
and the `mustCarry` members as `{path, sha256}` nodes: root chain (every root version from the
install's accepted version to the newest), index snapshot, revocation list, expiry information
(the `issuedAt`/`expiresAt` of each), manifests, payloads, permission policy documents, and
repair material as `{"repairMaterial": "absent-by-typed-absence", "ridesOn": "DR-110"}`. A
missing member refuses the whole payload; nothing is fetched.

### 4.7 Worked transitions with the numbers

| Case | Observation | Result |
|---|---|---|
| Fresh install, ordinary payload, root v1 issued 2026-10-01 | `EV-PRESENT-PAYLOAD`, all `requiredOnEveryTrustedEntry` hold | every role `ST-TRUSTED`; counters set |
| 2027-01-05, no payload since | index `issuedAt` 2026-10-01 + 90 d < now | `TR-INDEX` `ST-EXPIRED`; `analyze` with an already-installed verified component continues; `EV-INSTALL` refuses `INSTALL-NOT-TRUSTED` |
| Revocation list issued 2026-10-01, now 2027-01-05, index refreshed 2026-12-20 | `now − 2026-10-01 > 90 d` | every role `ST-STALE-REVOCATION` (index not expired); no new admission |
| Payload with index `snapshotVersion` 7 after 9 was accepted | `antiRollback` | refused `PAYLOAD-NOT-ADMISSIBLE`; state unchanged |
| Index signed by one valid TR-INDEX key | `thresholdEvaluation` 1 < 2 | refused; stay non-TRUSTED |
| Root v3 presented signed by 2 of v2's keys but 1 of v3's | TUF chaining | refused |
| Wall clock set back to 2026-01-01 after accepting index issued 2026-12-20 | clock monotonicity | evaluation clock stays at 2026-12-20; audit records the observation |

## 5. DR-124: trust state class, index custody, and the grant journal

### 5.1 New class SC-TRUST — "Monotonic trust state"

| Field | Value |
|---|---|
| Members | accepted root documents (all versions), current index snapshot bytes, revocation list, per-role state (`ST-*`), `lastAcceptedIssuedAt`, per-role `snapshotVersion`, `rootVersion`, `revocationVersion`, `lastKnownRevocation`, grant-journal high-water witnesses (§5.4), the pinned index-origin SPKI |
| Owner | Security + operations (DR-112's row owner) |
| Sole writer | the trust machine inside the core, holding the install-root lifecycle lock |
| Lifecycle | never rolled back by a generation rollback (`monotonicStore.rule`); never purged by project purge; survives core reinstall; migration forward-only |
| Backup / restore | included in the install-root backup; a restored store whose counters are LOWER than any accepted document still on disk, or whose journal witnesses are lower than a surviving journal tail, is quarantined and the install refuses until an ordinary payload re-establishes state; a restore never decreases a counter |
| Plan/Run | excluded from Plan/Run identity; never promoted |
| Encoding | its own SQLite database `trust.sqlite` at the install root, WAL, `synchronous=FULL` (SQLite: "FULL is atomic, consistent, isolated, and durable (ACID) in WAL mode"), a separate file from the lifecycle database precisely so lifecycle restore cannot carry trust state |

**trustEpoch.** The paired draft's `generation.trustEpoch` is the pair `{rootVersion,
indexSnapshotVersion}` read from SC-TRUST at verification time; a selected generation whose
`trustEpoch` is below the current pair is re-verified under current trust before use.

Why a fourth class: SC-OPS would let it roll with operational purge; SC-ANALYSIS contradicts
D-002; SC-CACHE contradicts non-rebuildability (state-class-contract.v11 warrant). File 04's
monotonic-store bullet requires exactly this class.

### 5.2 Remaining reserved placements — DECIDED

| Bytes | Class | Writer |
|---|---|---|
| component index custody records (accepted snapshot bytes and the admission registry) | SC-TRUST for snapshot bytes; SC-OPS for the per-install admission registry (`indexSchema.custodyRule`) | trust machine; admission under the lifecycle lock |
| rollback slots and provisional generations | SC-OPS, encoded in the paired draft's lifecycle database (`generation` table states) | lifecycle owner under the lifecycle lock |
| prepared migrations | SC-OPS (paired draft §5, copy-on-write before READY) | same |
| repair state | stays EXPRESSLY-RESERVED with DR-110 (deferral limb) | — |
| binding retention policy and tombstones | stays EXPRESSLY-RESERVED with DR-008/DR-113 (inherit-blocked) | — |

### 5.3 SUP-124-GRANT-JOURNAL — concurrence recorded

The grant journal is SC-OPS under SUP-124-GRANT-JOURNAL with every displacement and every
surviving clause exactly as `state-class-contract.v11.proposedSupersession` states. The owners
whose concurrence that supersession names (Semantic, Evidence, storage, operability, lifecycle,
DR-105 security/platform, V1 coordinator) are architecture roles delegated to the pair by D-367;
this contract records their concurrence. Overturn restores the three prohibitions for new writes
and freezes written records, as v11 states.

### 5.4 Grant-journal carrier encoding (closes ID-DEP-P5, ID-DEP-P6)

One SQLite database per project under the host-owned project state namespace,
`grant-journal.sqlite`, opened WAL with `synchronous=FULL`; foreign keys on. Written only by the
DR-105 host broker holding the project/operation lock (the same lock the paired draft's
`project_selection` uses). Lock order when both are needed: install-root lifecycle lock first,
then project/operation lock; released in reverse; a writer never blocks on the lifecycle lock
while holding the project lock.

```sql
CREATE TABLE grant_journal (
  grantGeneration INTEGER NOT NULL,          -- grant generation (carrier); NOT the lifecycle install generation
  seq          INTEGER NOT NULL,             -- strictly increasing per generation
  record_type  TEXT    NOT NULL CHECK (record_type IN
                 ('GRANT','NARROW','EXPIRY','RA','RCI','RCO','ICI','ICO','REV','CLN','AUD',
                  'CHECKPOINT','MIGRATION','TERMINAL')),
  operation_ref TEXT   NOT NULL,             -- operation identity value rides DR-006; structure only
  request_ref  TEXT,                         -- broker request id (RA/RCI/RCO/ICI/ICO)
  token        TEXT,                         -- PT-* on grant-bearing records
  body         TEXT    NOT NULL,             -- opensip-metadata-canonical.1 bytes, domain opensip.metadata.journal.1
  body_sha256  TEXT    NOT NULL CHECK (length(body_sha256) = 64),
  prev_sha256  TEXT    NOT NULL CHECK (length(prev_sha256) = 64), -- chain: sha256 of previous record's body_sha256||seq
  install_generation_id TEXT,                -- lifecycle generation the grant binds (ID-DEP-P2, recorded identity)
  manifest_digest TEXT CHECK (manifest_digest IS NULL OR length(manifest_digest) = 64),
  platform     TEXT CHECK (platform IN ('macos-arm64','macos-x86_64','linux-x86_64','linux-arm64') OR platform IS NULL),
  CHECK (record_type <> 'GRANT' OR (install_generation_id IS NOT NULL AND manifest_digest IS NOT NULL AND platform IS NOT NULL)),
  PRIMARY KEY (grantGeneration, seq)
) WITHOUT ROWID;
CREATE TRIGGER gj_no_update BEFORE UPDATE ON grant_journal
  BEGIN SELECT RAISE(ABORT, 'grant journal is append-only'); END;
CREATE TRIGGER gj_no_delete BEFORE DELETE ON grant_journal
  BEGIN SELECT RAISE(ABORT, 'grant journal is append-only'); END;
CREATE TABLE carrier_quarantine (              -- carrierQuarantineRecord: external, non-appending
  grantGeneration INTEGER PRIMARY KEY,
  reason     TEXT NOT NULL CHECK (reason IN ('uncertainTailLoss','witnesslessRestore')),
  observed_tail_seq INTEGER,
  body       TEXT NOT NULL
);
CREATE TABLE carrier_capacity_pause (          -- capacityPause: proven tail intact
  grantGeneration INTEGER PRIMARY KEY,
  proven_tail_seq INTEGER NOT NULL,
  reserved_terminal_slot INTEGER NOT NULL DEFAULT 1
);
```

Rules bound to the schema:

- **Grant generation.** A per-project integer starting at 1 that advances only at grant-generation
  closure (a REV of the whole generation, or project purge, per `terminalization`); it is not the
  lifecycle install generation. Every `GRANT` record binds `install_generation_id`,
  `manifest_digest` and `platform`, so a grant is bound to the recorded component bytes
  (ID-DEP-P2) and cannot authorize a different generation or manifest
  (FC-CROSS-GENERATION-REPLAY, FC-WRONG-MANIFEST).
- **Sequence.** Inside one `BEGIN IMMEDIATE` transaction: `seq = COALESCE(MAX(seq),0)+1` for the
  grant generation, then insert, then commit. The record is ORDERED when and only when the commit is
  durable (`synchronous=FULL` in WAL mode syncs the WAL at each commit). Nothing external is
  initiated before the RCI/ICI commit returns.
- **Terminal marker.** `TERMINAL` is appended by the first of {projectPurge, grantGenerationClosure}
  on a healthy carrier; a later one is a no-op (`terminalization.openHealthy`). Capacity pause
  keeps one reserved slot for it.
- **Witness.** After each durable commit the writer updates the SC-TRUST high-water witness
  `{project, grantGeneration, lastSeq, tailSha256}`. Restore compares: `witness.lastSeq >
  MAX(seq)` → `uncertainTailLoss` quarantine; no witness → `witnesslessRestore` quarantine; either
  way `failClosedNoAppend` and continuation only on a new generation. A stale witness (lower
  than the tail) is safe and is advanced.
- **Recovery.** Replay from the last `CHECKPOINT` record; `RA` without successor →
  CANCELED-BY-RECOVERY; `RCI` without outcome → run the class inverse and record `CLN`; `ICI`
  without outcome → `ICO` INDETERMINATE (`irreversibleBoundary.indeterminateOutcome`); `REV`
  read first. The FX-4 crash matrix enumerates every write and fsync boundary of this schema
  on both platforms.
- **Secrets.** Secret VALUES never enter `body`; handles do (file 03).
- **Hash chain.** Tamper-evidence for audit, not tamper-proof; the chain head is in the witness.

## 6. DR-105 and DR-114: joint-owner decisions

### 6.1 Execution mode (ID-DEP-P10) — DECIDED

The architecture preview admits components in **child-process mode only**. `in-host-process`
is refused at admission (RJ-6 RESERVED_FIELD_POPULATED if a manifest asks for it; no token).
Consequence in the truth tables: `PT-ENV-READ` becomes ENFORCED-BY-CONSTRUCTION in every cell
(the host constructs the child's environment block; FX-3 proves it); the other six tokens stay
DISCLOSURE-ONLY with their affirmative disclosure obligation; the pinned prototype's
`isolation: 'host'` behavior is a named difference, not carried.

### 6.2 FC-C1 — recorded

`host-effect-authorization.v25` is recorded as the joint-owner design contract by Operability +
security jointly with Security + platform owners, roles delegated to the pair under D-367. FC-C1
holds on an applied host. FC-C2..FC-C6 are unchanged and still each deny on absence. Recording
admits no surface: FC-C4 product admission is §6.4 and §6.5, per subtype.

### 6.3 BLK-3 outcome vocabulary — closed

Host acts: `COMPLETED | DEFINITELY_NOT_PERFORMED | INDETERMINATE` at
`consentRecords[].effectOutcome`, mandatory on every attempted host act. Component tail (§7):
`COMPLETED | FAILED | INDETERMINATE` as the ICO/RCO value, with `BEFORE-REVOCATION` as an
ordering disclosure derived from `n < r`, never a wire outcome. The two vocabularies never share
a field. PR-6 (required-confinement-unenforceable) has an EMPTY trigger set by decision for the
preview: no effect requires confinement because every admitted component is first-party or
explicitly trusted code (D-002, DR-128); the family stays so a later enumeration lands there.

### 6.4 BLK-2 CA-3 subtypes — per-subtype disposition

| Subtype | Disposition | Bound |
|---|---|---|
| OUT_OF_ROOT_READ | ADMITTED for the preview, read-only, `resourceScope` enumerated per invocation from this closed list: `/etc/os-release`; the mount table via the `platform-tcb-contract.v48` setns helper; `statfs` on the verified install root; `sysctl kern.osversion` / `kern.osproductversion`; the SC-TRUST store (read). Anything else is a scope mismatch (FC-SCOPE-MISMATCH). | doctor profile-observation checks and trust-state reporting |
| LOCAL_SOCKET_OR_PIPE | NOT ADMITTED; rides D-002's DR-105 scoping ("consented doctor probes" names no socket probe). Re-entry trigger: a doctor check that needs it, by successor. | — |
| KEYCHAIN | rides DR-108 (deferral limb) | — |
| PRIVILEGED_PLATFORM_FACILITY | owner assigned: Security + platform owners; NOT ADMITTED; re-entry by successor | — |

### 6.5 BLK-1 and CA-4 host paths

- CA-2 (customer tool execution): every CA-2 execution is UNEXERCISABLE in the preview and
  rides D-002's DR-105 scoping (Limb D). Re-entry trigger: the D-000 product/authorization
  decision `host-effect-authorization.v25` names, owned by the DR-119 product owner jointly with
  Security + platform. DR-119 remains necessary and not sufficient.
- CA-4 `PATH-TRUST-STATE-REFRESH`: ADMITTED as a consented departure (explicit invocation-time
  naming or pre-existing policy; CI never prompts). `endpointSet` is exactly the index origin
  named in the root document; the TLS server identity is verified against the **SPKI pinned in
  the root document**, not the OS certificate store, so no certificate-store TCB member is
  introduced (§8). The payload fetched is an ordinary air-gap payload (§4.6) and enters the
  machine through `EV-PRESENT-PAYLOAD`; the network path grants nothing by itself.
- CA-4 `PATH-INDEX-REACH` and `PATH-DECLARED-EXTERNAL-SERVICE`: NOT ADMITTED in the preview
  (the refresh payload already carries the index; no first-party external service is declared).
  Re-entry by successor.
- CA-1 SPAWN: exercisable subject to DR-G21 containment and the admitted manifest (FC-C6);
  CA-1 IN_PROCESS stays UNEXERCISABLE (consistent with §6.1).

### 6.6 Surviving writer for process death — DECIDED

Every consented host act that can commit an irreversible effect (CA-1 SPAWN, CA-4) is executed
by a child worker process of the doctor/host process; the doctor/host process is the surviving
writer that emits `INDETERMINATE` (or a report-integrity failure, OC-5) when the worker dies
with commit-versus-not unknown. Owner: Operability + security jointly with Security + platform.
If the doctor/host process itself dies, the invoking CI runner or shell sees a non-zero exit and
no report; that is the `UNEMITTED-CRASH` bound and it is disclosed as such, not narrated as a
result.

### 6.7 What stays authoring, not decision

The fourteen FX decision-record fixtures, the R-10 expiry-materialization and R-6 process-death
byte sets, the twelve doctor FC implementations and the thirteen actor-join implementations are
D1 authoring against the now-decided values; each ships with a retained checker (D-368 clause 1).

## 7. Control-plane effect bodies (for `control-message-schema.v1.json`)

### 7.1 `effectRequest.body`

```json
{ "effectClass": "HE-1", "authorizationRef": "gj:<projectKey>:<grantGeneration>:<seq>", "operationRef": "<opaque>" }
```

`authorizationRef` names the `GRANT` record; the grant binds token, scope, operation, expiry
and platform (file 03's tuple), so the request carries nothing else. Preview effect-class
registry, closed: `HE-1` HOST-STAGED-STATE-WRITE (a host-staged write into the component's
declared SC-OPS/SC-CACHE namespace; CONDITIONALLY REVERSIBLE per `effectCommitDefinitions`),
`HE-2` PROJECT-READ-RETURNED (a brokered read whose bytes the host returns; reversible-by-class).
Extension is by successor; an unknown class is RF-2.

### 7.2 `effectResult.body`

```json
{ "requestSeq": 12, "decisionSeq": 40, "outcomeSeq": 41, "commitClass": "REVERSIBLE",
  "effectOutcome": "COMPLETED", "resultRef": "<opaque, optional, bounded>" }
```

`effectOutcome` ∈ `COMPLETED | FAILED | INDETERMINATE` (the RCO/ICO value). `decisionSeq` is
the RA sequence, `outcomeSeq` the RCO/ICO sequence, both from the grant journal. A brokered
request the host will not perform is never an `effectResult`; it is a `refusal` with family
`RF-6` and `decisionClass` ∈ `PR-1..PR-9` (add `decisionClass`, required when `family ==
"RF-6"`, to the lead's refusal body). `COMPLETED-BEFORE-REVOCATION` and
`DEFINITELY_NOT_PERFORMED` are not wire members (§6.3).

### 7.3 Refusal precedence and channel ownership (as the lead stated; recorded so the
security contract does not merge channels)

`RF-2` structure (unknown member, out-of-enum type, oversize) → `RF-7` direction/state (a
provider sending `select`) → `RF-5` schema-valid but unauthorized semantic act on the control
plane not already RF-2/RF-7 → `RF-6` unauthorized host effect (carries PR-n). A finding-shaped
payload on the provider data plane (fd0/fd1) is a provider-protocol rejection, not a control
refusal.

### 7.4 CC-8 successor — endorsed

`fault.detail` and every free-text member are OPAQUE: bounded (the lead's 1024), redaction tier
2 (doctor `redaction.twoTierStructure`), never parsed for meaning, never promoted into facts,
Coverage, policyOutcome, D9, exit or findings, surfaced only inside a `diagnostics[]` member
labelled with provider provenance. The PASS-smuggling golden asserts two invariants: the
provider byte stream in the retained transcript is bit-identical, and every host semantic
output member equals the no-smuggling baseline run.

## 8. DR-126: complete platform profiles

### 8.1 Value-source legend

| Tag | Meaning | Rejection rule |
|---|---|---|
| MEASURED-2026-09-04 | observed on the authoring machine (macOS 26.6.2 build 25G83, Apple silicon, APFS) with the named interface | a qualification run that observes a different value on the same selector fails NT-TCB-3 |
| PUBLISHED-FACT | cited primary source in §11 | successor if the source changes |
| RELEASE-MEASURED | schema fixed here; value exists only at a release/qualification run | absent, malformed, or failing its stated recomputation → the profile refuses; never defaulted |

### 8.2 Core build decisions this section depends on

- **Linux core target is static-PIE musl** (`x86_64-unknown-linux-musl`, `aarch64-unknown-linux-musl`).
  Consequence: the Linux core has no dynamic loader and no libc member in L-TCB; its L-TCB is the
  OS ABI (kernel) alone. The bundled Node.js runtime's glibc floor (Node 24: "kernel >= 4.18,
  glibc >= 2.28" on Linux x64 and arm64) is the TypeScript component closure's platform
  dependency under DR-119, declared in that component's manifest, not core TCB. This is a
  dependency on the paired draft (which selects Rust but names no target); it is stated here as
  the security decision and flagged for the lead.
- **macOS core links libSystem only.** No framework is linked by the core executable; the
  qualification verifier (a separate process) may use Security.framework for the codesign
  attestation operation. NT-TCB-1 enforces this for every profile.
- **No certificate-store member in the preview**: TLS for the one admitted network path uses the
  SPKI pinned in the root document (§6.5). Font and ICU classes are absent (the core renders no
  text and uses no ICU). Each absence is carried as an inapplicability proof object naming the
  probe that would observe a resolution attempt.

### 8.3 macOS profiles

`P-MACOS-ARM64-25G83-APFS` and `P-MACOS-X86_64-25G83-APFS`:

| Member | Value | Source |
|---|---|---|
| `osFamily` / `architecture` | `macos` / `arm64`, `x86_64` | grammar |
| `supportedVersionOrBuildSelector` | `{ tag: EXACT-BUILD, identifierScheme: macos-product-build, canonicalIdentifier: "25G83" }` | MEASURED-2026-09-04 (`sw_vers -buildVersion`, `kern.osversion` = 25G83) for arm64; RELEASE-MEASURED for x86_64 (Apple has generally shipped one product build number across architectures; the x86_64 runner observation is retained at qualification and must equal the profile, otherwise the x86_64 profile carries its own distinct selector value) |
| `filesystemWhereItAffectsResolution` | `apfs` | MEASURED-2026-09-04 (`statfs.f_fstypename` = `apfs` on the volume containing `/usr/local`; f_fsid observed `[16777232, 26]` is a run value, not a profile member) |

Signed entries (each the four-field `signedEntry`; `platformProfileKey` = the profile id):

| Class | identityEvidence | originSearchPolicy / volumeConstraint | Value source |
|---|---|---|---|
| OS ABI (kernel) | PLATFORM-ATTESTED, `{scheme: codesign, payload: {cdhash}}`, pathless subject `{kind: running-kernel-codesign, cdhash}` | `PATHLESS-PLATFORM-ATTESTED`, macosForm | cdhash RELEASE-MEASURED per build/arch via `SecCodeCopyGuestWithAttributes` on the running kernel guest (`platformAttestationOperation.macosCodesign`) |
| loader `/usr/lib/dyld` | PLATFORM-ATTESTED codesign, cdhash | `EXTERNAL-ORIGIN`, canonicalOrigin `/usr/lib/dyld`; `allowedLoaderOrSearchOrder` = [`/usr/lib/dyld`]; environmentInfluence: `DYLD_*` FORBIDDEN | arm64e slice cdhash MEASURED-2026-09-04 `9d380d573d6f221b038725112b3b1f206737a429` (identifier `com.apple.darwin.ignition`, universal x86_64/arm64e); the x86_64 slice cdhash is RELEASE-MEASURED |
| libc `libSystem.B.dylib` | DIGEST-BOUND over the dyld shared-cache file that supplies it, `{algorithmId: sha-256, digest}` with companion `sonameAbi {soname: "libSystem.B.dylib", abiSelector: "macos-26.6.2"}` | `EXTERNAL-ORIGIN`, canonicalOrigin = the cache path under `/System/Volumes/Preboot/Cryptexes/OS/System/Library/dyld/` (`dyld_shared_cache_arm64e` / `dyld_shared_cache_x86_64`); search order = [that cache] | digest RELEASE-MEASURED per build/arch; reason for DIGEST-BOUND: `/usr/lib/libSystem.B.dylib` does not exist as a file on this build (measured: "No such file or directory"); the library is mapped from the cache, and `classMap.libc` permits DIGEST-BOUND |
| framework | none; inapplicability proof: `otool -L` of the core shows only `libSystem.B.dylib`; probe = dyld image-load events | MEASURED on the hello-world control binary 2026-09-04; RELEASE-MEASURED on the core |
| certificate store, font, ICU | absent by design with inapplicability proofs (§8.2) | — |

### 8.4 Linux profiles

`P-LINUX-X86_64-UBUNTU2404-EXT4` and `P-LINUX-ARM64-UBUNTU2404-EXT4` (initial qualified set;
`debian:12` profiles are the next population, not populated here):

| Member | Value | Source |
|---|---|---|
| `supportedVersionOrBuildSelector` | `{ tag: EXACT-BUILD, identifierScheme: linux-distro-userspace, canonicalIdentifier: "ubuntu:24.04" }` | PUBLISHED-FACT (`/etc/os-release` ID `ubuntu`, VERSION_ID `24.04`; libc6 2.39-0ubuntu8.8 = glibc 2.39, relevant only to the component closure) |
| `filesystemWhereItAffectsResolution` | `ext4` | decided; the qualification runner's install-root volume must be ext4 (mountinfo record selected per `filesystemMeasurementTarget.linux`) |

Signed entries:

| Class | identityEvidence | volumeConstraint | Value source |
|---|---|---|---|
| OS ABI (kernel) | PLATFORM-ATTESTED, `{scheme: package-db, payload: {name, version, digest}}` via `apt-secure`; pathless subject `{kind: firmware-launched-kernel-package, name, version, digest}` | `PATHLESS-PLATFORM-ATTESTED` linuxForm: `pathlessObservation`, `measuredBootTranscriptDigest`, `kexecCapability: "kexec-absent"`, `builderRoot`, `builderPublicKey`, `builderSignature`, `builderRootDigest`, plus `ikconfigDigest` on the present branch | name/version RELEASE-MEASURED (the pinned `linux-image-*` package of the runner image); digest RELEASE-MEASURED (sealed archive snapshot); transcript digest RELEASE-MEASURED (TCG2 event log, PCR 4 EV_EFI_BOOT_SERVICES_APPLICATION, TPM2_Quote over PCRs 0,1,2,4,7 per `measuredBootBind`); `builderPublicKey` = KB-1 (§3.1), `builderRootDigest = sha256(KB-1)`, `builderSignature` RELEASE-MEASURED (KB-1 over the PE/COFF image digest of the exact kernel member); `kexec-absent` requires `kexec_load_disabled=1` on the runner image |
| loader | none: static-PIE has no `PT_INTERP`; inapplicability proof = `readelf -l` of the core shows no INTERP segment, probe = execve/mmap trace | RELEASE-MEASURED on the core |
| libc | none: statically linked musl is core bytes, not a system resolution | same proof |
| certificate store | exactly one DIGEST-BOUND member: the KB-1 public key (`{algorithmId: sha-256, digest: sha256(KB-1)}`), which `builderRoot` must equal | KB-1 minted at the first release ceremony; RELEASE-MEASURED |
| AK certificate (measuredBootBind `akCertificateMember`) | DIGEST-BOUND certificate-store member per qualification runner | RELEASE-MEASURED per runner |
| font, ICU, framework | absent with inapplicability proofs | — |

**Runner-class consequence (amends D-006's Linux runner class by successor):** Linux
qualification runners must boot UEFI with Secure Boot enabled and expose a TPM 2.0 (a cloud
vTPM is acceptable), with `kexec_load_disabled=1`. Without that, the accepted v48 grammar cannot
attest the Linux OS ABI and G22 cannot qualify; this contract does not weaken the grammar to fit
cheaper runners.

### 8.5 Carrier, ceremony and refusal examples

The carrier is the inventory document (§2.1 tag `opensip.metadata.inventory.1`) signed TR-CORE
2-of-3 (§3.2 step 4); it carries the `inventorySchema` TCB field keyed by complete
`platformProfileKey` and the non-inventory `verifiedInstallRoot` field (`"/"` for the tree root).

Example signed entry (macOS loader):

```json
{ "platformProfileKey": "P-MACOS-ARM64-25G83-APFS", "class": "loader",
  "identityEvidence": { "authenticityCore": { "scheme": "codesign",
      "payload": { "cdhash": "9d380d573d6f221b038725112b3b1f206737a429" } } },
  "originSearchPolicy": { "allowedLoaderOrSearchOrder": ["/usr/lib/dyld"],
      "environmentInfluence": { "DYLD_LIBRARY_PATH": {"standing": "FORBIDDEN"},
        "DYLD_INSERT_LIBRARIES": {"standing": "FORBIDDEN"}, "DYLD_FALLBACK_LIBRARY_PATH": {"standing": "FORBIDDEN"},
        "PATH": {"standing": "FORBIDDEN"} },
      "classAppropriateLookup": null,
      "volumeConstraint": { "tag": "EXTERNAL-ORIGIN", "canonicalOrigin": "/usr/lib/dyld" } } }
```

Refusal examples: NT-TCB-3 — a run on build 25G83 observing dyld cdhash ≠ `9d380d57…` refuses
the generation; NT-TCB-2 — a `libSystem` resolution from any path other than the profile's cache
path refuses; NT-TCB-1 — any framework image load by the core refuses; NT-TCB-KEXEC — a Linux
runner with `kexec_loaded = 1` refuses; profile refusal — a Linux host whose `/etc/os-release`
VERSION_ID is absent, or whose install root is on `xfs`, selects no complete profile and refuses.

## 9. Acceptance examples and fixtures this contract makes authorable

| Gate / row | Case | Expected |
|---|---|---|
| DR-103 TC-SIG | ENVELOPE_MISMATCH pair (§2.2) | refuse / admit |
| DR-103 TC-PATH | `bin/entry -> ../outside` with declared `outside`: contained resolution proves the containment test; still RJ-3 (pathRule forbids `..` in symlink targets, retained); `bin/entry -> ../../outside` RJ-3 escape; `bin/entry -> target` with declared `bin/target` full admission | as the lead stated; no target grammar widened |
| G08 FC-EXPIRED / FC-FUTURE / FC-STALE-REV / FC-QUORUM / FC-RECOVER / FC-EVENT-ORDER | §4.7 numbers | named states and refusal reasons |
| G08 FC-ENVELOPE-INACTIVE | applied host | branch unreachable; asserted as such |
| G09 FX-3 | child env block | ENFORCED-BY-CONSTRUCTION |
| G09 FX-4 | §5.4 schema crash matrix | one total order after every recovery |
| G09 FX-5, FX-6, FX-11 | `n < r` disclosure wording | COMPLETED/FAILED/INDETERMINATE-BEFORE-REVOCATION |
| G12 / G32 FC-JOIN-* | §6.2–§6.6 | each class's fate as v8 states, with FC-C1 now true |
| G22 NT-TCB-1..4, KEXEC | §8 profiles | refuse cases above |
| G21 CC-8 successor | PASS-smuggling golden | dual invariance (§7.4) |
| canonical profile | V-* vectors | `check-security-vectors.v1.py` PASS |

## 10. Leftover obligation mapping

| Row | Obligation | Disposition here |
|---|---|---|
| DR-112 | OBL-RESERVED-NUMBERS | decided §4.1, §4.2, §4.4 |
| DR-112 | OBL-G08-FX-AUTHORING | authorable against §4; authoring remains D1 |
| DR-101 | OBL-D2 (OD-101-2) | decided §3 |
| DR-124 | OBL-MONOTONIC | decided §5.1 (SC-TRUST) |
| DR-124 | OBL-GRANT-JOURNAL | concurrence §5.3; encoding §5.4 |
| DR-124 | OBL-INHERIT-BLOCKED | Limb D ride on D-002 "touched classes"; re-entry when SC-EVIDENCE becomes designable (DR-002..008 chain) |
| DR-105 / DR-114 | OBL-FC-C1 | recorded §6.2 |
| DR-105 / DR-114 | OBL-BLK-3 | closed §6.3 |
| DR-105 / DR-114 | OBL-BLK-4 | closed §5.3, §5.4, §6.6 (doctor never writes the journal) |
| DR-105 / DR-114 | OBL-BLK-2 | per-subtype §6.4; KEYCHAIN rides DR-108 |
| DR-105 / DR-114 | OBL-BLK-1 | Limb D ride on D-002 DR-105 scoping; re-entry trigger §6.5 |
| DR-105 | OBL-FX-AUTHORING, OBL-R10-AUTHORING, OBL-R6-AUTHORING | authorable; D1 |
| DR-114 | OBL-DOCTOR-FX-AUTHORING, OBL-JOIN-FX-AUTHORING | authorable; D1 |
| DR-126 | OBL-RESERVED-TABLES | populated §8 with value-source classes |
| DR-126 | OBL-G22-FX-AUTHORING | authorable against §8 |
| DR-103 | OBL-ENVELOPE-MISMATCH | concrete case §2.2; authoring D1 |
| DR-103 | ID-DEP-1 | closed §2 |
| DR-122 | OBL-FC-OUTFAIL-FX (`committed-run-preserved`) | Limb D ride on D-077; the lead's opaque-object non-mutation fixture is acceptable if it never decodes the object |

## 11. External references (primary; checked 2026-09-04)

- Apple, "Notarizing macOS software before distribution" and "Customizing the notarization
  workflow" (developer.apple.com/documentation/security/…): Developer ID requirement, hardened
  runtime, secure timestamp, `notarytool submit --wait`, accepted containers (UDIF, flat pkg,
  ZIP), stapler item types, "you can't staple to [a ZIP] directly".
- `man codesign` (macOS 26.6.2): `--timestamp`, `--options runtime` (hardened runtime, library
  validation); `xcrun stapler` usage text; `xcrun notarytool --help` (1.1.2).
- The Update Framework specification, latest: §2.1 roles, §4.3/§6.1 threshold and root
  chaining, §5.3.10/§5.4.4/§5.5.6/§5.6.5 expiry, §5.5.5 rollback.
- RFC 8032 (Ed25519, pure variant, no prehash). FIPS 180-4 (SHA-256).
- SQLite `PRAGMA synchronous` and WAL documentation: FULL is durable in WAL mode; NORMAL may roll
  back after power loss.
- Node.js `BUILDING.md` v24.x platform list: Linux x64/arm64 Tier 1 "kernel >= 4.18, glibc >= 2.28";
  macOS >= 13.5.
- packages.ubuntu.com/noble/libc6 (2.39-0ubuntu8.8); packages.debian.org/bookworm/libc6
  (2.36-9+deb12u14). os-release(5).
- TCG PC Client Platform Firmware Profile / TPM 2.0 Library (as already cited inside
  `platform-tcb-contract.v48` `measuredBootBind`).

## 12. What this contract does not do

Does not SATISFY any row; does not execute any fixture; does not QUALIFY any platform; does not
claim four-platform qualification; does not mint a RunId, EvidenceDigest, PlanId or D9 code; does
not edit V1 canonicalization; does not authorize `docs/v2/implementation/`; does not admit CA-2,
IN_PROCESS, KEYCHAIN, LOCAL_SOCKET_OR_PIPE, PRIVILEGED_PLATFORM_FACILITY, PATH-INDEX-REACH or
PATH-DECLARED-EXTERNAL-SERVICE; does not shrink D-002's platforms or independent-release
machinery; does not choose a confinement primitive (every DISCLOSURE-ONLY cell stays so).
