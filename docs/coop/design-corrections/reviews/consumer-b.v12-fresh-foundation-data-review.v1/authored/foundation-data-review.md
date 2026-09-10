# Foundation data review

**Verdict: `FOUNDATION_DATA_ADMITS`**

This is a bounded technical review of original phases 0–4 standalone artifacts plus `R-IMPORTED-OBSERVATION-BOUNDARY`. It is not a full consumer `ACCEPT`, not implementation readiness, and not full Run admission or evaluator replay.

Claimed identities, `stockOk` flags, grades, and expected values inside the evidence JSON were comparison targets, never oracles. Input bytes were not repaired or reminted.

## Input custody

Independently hashed:

| Object | Expected SHA-256 | Result |
|---|---|---|
| kit manifest (`subject/consumer-input-manifest.json`) | `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` | match |
| parent subject | `a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb` | match |
| data manifest | `2751637973eeb7c113c630b9666424015b4717127b73efc01979f4134b8acfd4` | match |
| original charter | `57df2ed62cfb57173209dfcd55f8698c977173f4e854e42b7ad57e9e2eb8a8ec` | match |
| requirements.json | `855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495` | match |

All **80** kit files and **30** evidence files match declared SHA-256 and byte length. No extra or missing evidence files. Detail: `input-hash-verification.json`.

## Reproduction

```text
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-fresh-foundation-data-review.v1/output/independent-checker.py
```

The checker implements C, H, CVE1, raw lexical JSON, CAP-MANIFEST-ID-V1 gates, and protocol3 from the kit. Machine-readable output: `independent-results.json`.

## What was independently recomputed

### Canonical / H / CVE1 / lexical

C is UTF-8 key-ordered JSON with no whitespace, unescaped Unicode scalars, and exact integer/bool/null encoding. H is:

`SHA256(ASCII("opensip.product.v1") || 00 || ASCII(D) || 00 || uint64BE(len(C(X))) || C(X))`

with typed ids from the identity-and-evidence prefix table (`snapshot2`, `plan2`, `proof3`, `evidence3`, `seal3`, `run3`, `import2`, …).

Independently matching retained identities:

| Record | Independent typed id |
|---|---|
| snapshot-A | `snapshot2:3324a39a288b5ba16bbfc95ddf465e3ab5b9dee0d5a510cfdf4151c018806a97` |
| snapshot-B (vcsDigest change) | `snapshot2:496d208184f5fa41fc0aa93025fafe4d458452f9f90bd41b048b56069d150654` |
| plan | `plan2:61c9dfbb8f77da58191b4a0a1bea85c47101bf0e41c00cc12cd9b6c40f69152d` |
| view | `view2:407191e0ef949e6ace2b03ec77b9bde3bcd02d566098530749794191b4649f08` |
| proof-bundle | `proof3:f0db739981b1cb9044ee080b4f8ec8782c13e7e3b386df2a24a0020bc1fcc231` |
| semantic-evidence | `evidence3:8eafc7c5f9bc2c9db6822a243539f385d9be32d0561f2812d5cf6bd053febb29` |
| evaluation-seal | `seal3:551b4dfb1947635426737c6500fb78bfc31fe3c6a9a2bd82dbdd30d5eb05d6ac` |
| run | `run3:393213e5dcc5da1e769a0fb71d7f042fb61088a29e4318153fef83f2eb9b6b05` |
| capability manifest | `6e6f63c79285d280ea21d109c8eb6ce2f4107d464210c013a0f08d7d6d72652b` |
| import wrapper | `import2:e52a84643da40c64d94a586444b2340446db24ec1915066752b5dffde8044af8` |

Snapshot nested canonical-record digests (source-inventory, vcs-observation, scope-descriptor, semantic-configuration) recompute as `SHA256(C(record))` and join the snapshot fields. A semantic `vcsDigest` change moves H; RequestId/ExecutionId/wall-clock are not run fields and stuffing `requestId` into run is refused by `additionalProperties`.

All eight CVE1 types round-trip. Map encode is insertion-order independent. Independently, NFD strings refuse `NON_NFC_STRING` and floats refuse `FLOAT_FORBIDDEN` (the exhibit omitted those two raw inputs).

Raw lexical admission was executed on retained bytes, not `json.loads`: duplicate keys, floats, exponents, `-0`, leading zeros, integer range, unpaired surrogates, BOM, and unescaped controls all refuse at the claimed first code. Parsed-object encode of `{"a":1}` is distinct from the raw duplicate-key refusal.

### Acyclic joins (not a full Run)

The standalone chain is actual source → Plan → View → Proof → Evidence → Seal → Run:

- `plan.snapshotId` = snapshot typed id
- `view.planId` = `proof.planId` = `evidence.planId` = `seal.planId` = `run.planId` = plan typed id
- `evidence.viewIds` = `[view]`
- `evidence.proofBundleId` = `seal.proofBundleId` = proof typed id
- `seal.evidenceId` = `run.evidenceId` = evidence typed id
- `run.evaluationSealId` = seal typed id
- proof-bundle does not contain `evidenceId` or `runId`

The cycle input is the illegal proof-bundle with `evidenceId`; stock `additionalProperties` refuses it. That is the published acyclicity law, not a substitute graph.

Plan nested H-identities (closures, native-context digests, analysis-spec, policy, waiver, grant, capability-manifest bytes) are cited without retained preimages. Those citations are **not** accepted as full Run closure and were not replaced by another graph. This vector was not upgraded into a complete Run requirement.

### Capability admission

Gate order from the current registry (`capability-manifest-domains.v2.json`): **ADM-TYPE → ADM-CLOSED → ADM-DOMAIN → ADM-ORDER**.

The positive manifest admits before encoding. Independent CVE1 committed bytes (1509) recompute capabilityManifestId as `SHA256(UTF8("opensip.capability-manifest.v1") || 0x00 || committedBytes)` = `6e6f63c7…652b`.

Named negatives, first gate, and masking:

| Vector | Independent first gate | Masks later |
|---|---|---|
| boolean schemaVersion | ADM-TYPE | yes |
| string schemaVersion | ADM-TYPE | yes |
| undeclared key | ADM-CLOSED | yes |
| missing key | ADM-CLOSED | yes |
| `ALL-SUPPORTED` platform | ADM-DOMAIN | yes |
| `calls: enumerated` (cross-ladder) | ADM-DOMAIN | yes |
| unsorted platformIds | ADM-ORDER | no |
| unsorted providers | ADM-ORDER | no |
| boolean schemaVersion plus extra key | ADM-TYPE | yes (masks CLOSED) |

OPEN positions (`schemaVersion`, `profile`, `providerId`, `language`, `providerVersionSource`, `toolchainIdentitySource`) were type-checked only. No value enum was invented for them. `schemaVersion` remains an exact JSON integer, not a closed `{1}` registry.

### Protocol traces (executed vs host)

protocol3 was executed from `protocol3-transitions.v1.json`. Frame payload schemas, OS pipes, and process spawn are future-host assumptions and were not claimed as enforcement.

- Complete: Hello → … → P3-27 complete → P3-31 → P3-32 DONE. Identity tokens present on HelloAck (`source-identity-snapshot2`, `plan-identity-plan2`, `fact-identity-fact2`, `coverage-v3`). `sourceBytesSent` becomes true on OpenUniverse, after negotiation.
- Unavailable: P3-21 at `WAIT_NATIVE_CONTEXT_VERIFIED`, terminal `unavailable`, DONE.
- Cancel: P3-29 / P3-30, terminal `cancelled`, DONE.
- Fault: `deadline` → P3-33 FAULT, no source bytes.
- Terminal: after DONE, `FactBatch` is `post-terminal-frame` → FAULT.
- OpenUniverse without identity tokens: identityNegotiated false, no match for P3-03, P3-34 FAULT, **sourceBytesSent remains false** because stateUpdates apply only after a successful row match.

Every step is labeled executed vs host.

**Claimed-value miss (should, not a failed discriminating trace):** unavailable and fault exhibits claim `final.stageCount = 1`. Published `initialState.stageCount` is 0 and only Analyze writes stageCount. Those traces never send Analyze. Independent finals have `stageCount = 0`. P3 ids, terminals, identity, and source-byte flags still match.

### Relation / count / matrix / modes

The 13-relation table matches `relation-payload-schemas.v2.json#/x-opensip-relation-registry` (ladder, subjectKind, universeRule, anchor class). `file` ladder is `[enumerated]` only; no resolved rung was invented.

RC-0/RC-1/RC-2 applied to retained inputs: `file@enumerated` is `not-applicable` / `attempted=false` with and without facts; `imports@resolved-target` with zero unresolved edges and a complete exhaustive stage is `complete`; one unresolved edge is `incomplete`. Zero count never implies complete on a resolved rung.

Grammar capability registry class law matches the exhibit: `javascript`/`rust`/`typescript` are code (clones present); `json`/`markdown`/`toml`/`yaml` are data-document (no body identity). All six `languageModes` have representable analysis paths (`ts`/`js` → typescript context/universe, rust modes → rust, `syntax-only` → syntax grammar bundle).

Cited frozen-store file facts (membership only, not Run admission):

| Store | fact2 suffix | Independent relation/resolution |
|---|---|---|
| syntax-code | `852404c1…a717` | file / enumerated |
| ts | `af864a7d…f4a3` | file / enumerated |
| rust | `61b48e7d…f853` | file / enumerated |
| syntax-data | `97e82756…95ac` | file / enumerated |
| rust-partial-clones | `8376fa81…d863` | file / enumerated |

### Imported observation boundary

Import wrapper C/H independently match. Nested canonical-record digests rejoin:

- `payloadDigest` = SHA256(C(RuntimePayloadV1))
- `sourceCorrespondenceDigest` = SHA256(C(SourceCorrespondence)) and snapshotId = snapshot-A
- `buildDigest` = SHA256(C(BuildIdentityV1))
- `observationDigest` = SHA256(C(ImportObservationV1))
- `scopeDigest` = h-helper scope digest
- `payloadSchemaDigest` = SHA-256 of the exact `imported-evidence.schema.json` document bytes (`edce21a3…594b9e`)

Stock schema of the wrapper and nested records passed; stock is not admission. The wrapper is not `fact2` and not native Coverage. Kit limits (no universal negative, no native closed world, no unsafe delete/replace, no native fact2 identity) are stated. Frozen TS store contains `import2:98fee8f9…2c1c` as domain `import` (membership only). `producerClosure` / `adapterClosure` are cited without retained closure preimages and were not upgraded into a Run.

## Original ID map (actual results)

See `original-id-map.json`. Summary:

| ID | Independent status |
|---|---|
| S-FRESH-ORIGIN, S-NOT-PRODUCT, S-KIT-ONLY, S-NO-ORACLE, S-MISSING-DEP-IS-CUSTODY, S-CONTINUATION | **external-root-custody-required** — cannot be authenticated from these JSON bytes |
| S-MANIFEST-VERIFY, S-PROFILE-CURRENT | executed-pass (this review’s hashes and current majors) |
| R-FIVE-CONTRACTS-INDEX, R-SOURCE-MAP-SCOPE, R-CVE1-TYPES-AVAILABLE | executed-pass |
| R-H-HELPER … R-ADVERTISED-MODE-PATHS, R-IMPORTED-OBSERVATION-BOUNDARY | executed-pass |

Phases 5–11 complete Runs, remaining phase-6 vectors, envelopes, query, and evaluator replay are **outside this bounded task**.

## First refusals / not reached

Independently matching first refusals are in `first-refusals.json` (10 lexical, 9 capability gates, acyclic `evidenceId`, identity-before-source P3-34).

Not reached here, and not demanded:

- Full Run admission/replay of the five frozen stores
- Real OS/compiler/crypto/SQLite or host authentication
- Author-process S-* custody from these JSON alone
- Phases 5–11 except the imported-observation standalone vector

`data/foundation/reconstruction-results.json` cites a command under another actor directory. That path was not followed.

## Existing-law misses vs missing/contradictory norms

- **Existing law, exhibit claimed value:** `final.stageCount=1` on unavailable/fault contradicts `protocol3-transitions.v1.json` initialState/stateUpdates. Discriminating traces still hold. Recorded as a should-issue, not a missing recipe.
- **Missing or contradictory kit norm for this scope:** none identified. OPEN scalar positions were not given invented enums.

Helper-corrections in the evidence are historical process notes. They were not used as oracles.

## Verdict boundary

`FOUNDATION_DATA_ADMITS` means the scoped standalone technical records independently recompute and join under current owning norms.

It does **not** mean:

- `ACCEPT-RECONSTRUCTABLE`
- product qualification
- implementation authorization
- that the five frozen Run stores are admitted
- that S-* author origin/oracle custody was observed
