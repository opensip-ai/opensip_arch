# NSS-F4: the TypeScript release-closure interface rulings (X-F4-1, X-F4-3, X-F4-4), contract successor r3

2026-10-30. Author: Claude Opus 5.5 (high), R3-FRONTIER, Herdr w1R:p1, under coordinator decision LD-Q-53 (session
9ce22ffd, w1:p1). Status: **PROPOSED, r3**, after Codex REVIEW-r1 (REQUIRED-FINDINGS: RF-1, RF-2; NB-1) and REVIEW-r2 (`REVIEW-r2.md`, REQUIRED-FINDINGS: R2-RF-1). It needs Codex `NSS-F4: ACCEPT` (R3-FRONTIER, gpt-6-astra/high) and
coordinator adoption under OD-AUTO-1. Documents only: no product or architecture file is changed here; binding is a
later step (§9, X-NSS4-B).

**Pins.** Product main `d6434107` (191 contract successors); architecture `fb396900f`. Every parent is checked at its
exact bytes by `evidence/build_overrides.py` and `evidence/build_nss_f4.py`.

**What it answers.** F4's three interface items it may not decide (`f4/MSG-coordinator-r1.md`, `1ae13359…`;
`f4/plan/PLAN-r1.md` §6, `1d7104e4…`; carried unchanged into `f4/plan/PLAN-r2.md` §6, `13c74a80…`). F4 cannot freeze
F4-a, F4-b or F4-c before they are answered. The coordinator ruled X-F4-2 itself; §5 records this author's check that
it changes no release-format byte.

## r3 changes

| # | Finding | Change | Where |
|---|---|---|---|
| 1 | **NSS-F4-R2-RF-1** | N4-6 no longer lists the intended positive case as a failure. It is split: **N4-6a**, the positive case, after the existing admission and Plan-token prerequisites succeed, where exactly one TS2 protocol row, no row of another `roleSubprotocol` or version, and `(closureProtocolMajor, providerProtocol)` = `(2,2)` supply the native selection, with no relation row included; **N4-6b**, the unavailable selections (no protocol row; a preview or other-version row beside it), each adding no manifest refusal and replacing no earlier one; duplicate protocol ids stay the earlier uniqueness refusal. | §7 |

Nothing else changes: LD-N4-2, N4-7, the overrides, the schema copy, the evidence and every digest recipe are r2's.

## r2 changes

| # | Finding | Change | Where |
|---|---|---|---|
| 1 | **NSS-F4-R1-RF-1** | `runtimePayloadSha256`'s `files` is now an explicit **runtime-support inventory**, never "what the process reads". It excludes the executable, both identity descriptors, every license notice, the compiler and stdlib members and the worker application's inputs, each of which keeps its own commitment. That also removes the self-reference a read-based rule would create through the runtime descriptor. The M3 inventory is exactly `{etc/openssl.cnf}`; any other inventory is a successor. The digest is unchanged. N4-9 gains membership controls. | LD-N4-3; NE:2984 insertion (`evidence/build_overrides.py`, `overrides.json`); §7 |
| 2 | **NSS-F4-R1-RF-2** | The native selection now runs only after the existing parse, shape, body-semantic and closure-admission duties, and never replaces their refusals. Among admitted releases it adds no new manifest refusal. N4-6 and N4-7 are split into the reviewer's cases: an admitted release that cannot supply the session; `(closureProtocolMajor, providerProtocol)` = `(2,1)` and `(3,2)`, which keep C2PM-1's analyzer-mismatch refusal; and `(3,3)`, which reaches `native.closure-protocol-unsupported` only after its prerequisites, with C2PM-1's missing-declaration and descriptor-mismatch precedence kept. | LD-N4-2; DR103 insertion; §7 |
| 3 | NB-1 | The closure-recipe evidence is stated as it is: three TypeScript-universe recomputations (two toolchains, one stdlib), plus the runtime suffix extraction. There is no provider-join vector. | LD-N4-1 |

No ruling, recipe value, branch, schema byte or identity changes. The schema copy and the evidence vectors are
byte-identical to r1's.


| Name | Document | Bytes | sha256 |
|---|---|---|---|
| **NE** | `docs/v2/contracts/product-v1/native-evidence.md` | 329,013 | `83b99783…` |
| **IE** | `docs/v2/contracts/product-v1/identity-and-evidence.md` | 135,448 | `c82404f3…` |
| **DR103** | `docs/coop/artifacts/component-manifest-schemas.v11.json` (DR-103's field authority) | 139,492 | `1c0b8868…` |
| **C2PM** | `docs/implementation/m3/snapshot-plan-c/c2pm-1-r2/CONTRACT.md` (accepted, bound) | 13,644 | `58d285ca…` |
| **CMS** | the current complete manifest schema, C2PM-1's copy `docs/implementation/m3/snapshot-plan-c/c2pm-1-r2/completion/manifest-schema.completed.v1.json`, byte-identical to the product's generator input `tools/security/inputs/manifest-schema.json` | 25,247 | `80254f9e…` |
| **CR-1** | `docs/implementation/m3/snapshot-plan-c/cr-1/README.md` (role→kind table) | | |
| **SD-2** | `docs/implementation/m3/supervisor-d/sd-2/CONTRACT.md` (accepted: the native control select tuple) | | |
| **MD** | `docs/implementation/m3/supervisor-d/PROPOSAL.md` (M3-D r5, accepted), item 9 | | |
| **DLV** | `docs/coop/artifacts/delivery.v2.json` `typescriptSemanticSubstrate` | 143,995 | `47b6cfd1…` |
| **RI** | `docs/coop/artifacts/resolved-inputs.v2.json` `planIdContract.semanticUniverseSchemas.typescript-v1` | | |
| **NSS-F1** | `lead-2026-10-25/nss-f1/` r2, adopted (LD-COORD-NSSF1); its handshake successor copy `260fb535…` | | |

Unit files, under `nss-f4/`: this document; `completion/manifest-schema.completed.v1.json` (the CMS successor copy,
31,970 B, `e698f9d6…`); `overrides.json` (six insert-only overrides, generated); `evidence/build_overrides.py`;
`evidence/build_nss_f4.py`; `evidence/vectors.json`.

## 1. The three gaps, exactly

- **X-F4-1.** `TypeScriptSemanticUniverseV2` requires `runtimeArtifactSha256` and `providerArtifactSha256` (RI
  `required`; startup schema). RI's `deliveryJoin` copies them from "exact typescript-runtime and typescript-provider
  ArtifactEntry rows" of a signed `ReleaseManifestV1`. M3 has no `ReleaseManifestV1`: the TS bytes are three admitted
  closures (CR-1's table; NE §2.4; F4 LD-F4-1): **T** (`toolchain`, holding `bin/node` and the compiler), **S**
  (`stdlib`) and **P** (`analyzer` → `provider`). No M3 text says what the two members are. They are not HelloAck joins
  (startup `handshakeJoin`), not `resolvedInputs` members, and not `plan2` members.
- **X-F4-3.** Three settled facts do not meet:
  - the control select tuple is `analyzer`/`typescript-semantic`/2, from the admitted manifest's `role` and
    `compatibility.providerProtocol` (MD item 9; SD-2, accepted);
  - SD-2 says the tuple's `roleSubprotocol` and version are "the exact opaque tokens of the admitted capability
    declaration", and that "the pinned completed structural manifest schema … admits only typescript/version1
    branches … That upstream schema/materialization duty stays open" (SD-2 `CONTRACT.md`, "Confirmed tuples");
  - C2PM-1 admits an analyzer's `closureProtocolMajor` "only under the already selected named analyzer role
    subprotocol", and the product's `AnalyzerSubprotocol` has no production constructor
    (`crates/security/src/component_closure.rs`:101-121).

  Separately, NE §9.1 says "Hello carries exactly the selected signed row's tokens", but no text says where in a
  signed release that row is. D2b takes the array from "the selection" (LD-D2B-18), and FA-2 and NSS-F1 both name
  "signed capability rows" that must carry their tokens.
- **X-F4-4.** The runtime descriptor's closed member `runtimePayloadSha256` (DLV `identity.runtimeDescriptor`) has no
  recipe. DLV's runtime is "a Node.js executable and its required shared runtime payload". The official macOS arm64
  Node 24 build has no separate payload file: ICU and OpenSSL are linked into the executable.

## 2. Lead decisions

### LD-N4-1. The artifact members are closure identities (X-F4-1)

- **Decision.**
  - `runtimeArtifactSha256` = the 64-hex suffix of the context's `toolClosure.closureId`, i.e. of T's `closure2`
    identity. T is the closure that holds the runtime (NE §2.4: `toolClosure.runtime` is a member of it).
  - `providerArtifactSha256` = the 64-hex suffix of P's `closure2` identity, which is a member of the verified
    `plan.semanticClosures` (C item 16: "the selected provider closures").
  - `runtimeArtifactId` and `providerArtifactId` keep their constants (`typescript-runtime`, `typescript-provider`).
  - These are **explicit successor recipes despite the retained delivery names**, the form IE §3 already uses for
    `typescriptStdlibMerkleRoot` and `rustcDevLlvmDigest` (IE:265-271).
- **Who binds, and the checks.**
  - The host that mints the universe for the Plan (C4a, with C2b-1a's adapter) takes both values from the admitted
    closures; it refuses before spawn, as a host invariant, a `providerArtifactSha256` naming no selected provider
    closure.
  - `bind_typescript_universe` adds `runtimeArtifactSha256` to its overlap checks against the bound context and refuses
    a disagreement under its existing key family, `native.universe-context-field-mismatch:runtimeArtifactSha256`
    (NE:1593-1598). No new key family or public code.
  - The worker does not check them; they stay outside the HelloAck join.
- **Why `closure2`, not F4's proposed `manifestDigest`.**
  1. **It is the identity the Plan already binds.** P's id is in `plan.semanticClosures`; T's id is in the context, so
     in `plan.nativeContextDigests`. Each member becomes a checkable join to a Plan-bound value, instead of a free
     value with no verifier.
  2. **It commits what DLV's artifact digest was for, plus kind.** `closure2` = `H("closure", {kind, manifestDigest,
     platform, protocolMajor, schemaVersion, semanticVersion, tree})` (IE §3; reproduced on the product fixture's
     three toolchain and stdlib closures of the TypeScript universe, `evidence/vectors.json` `closureJoins`; there is no provider-join vector). It pins every byte through the tree rows and the body
     through `manifestDigest`, and its `kind` stops a provider value from naming a toolchain. `manifestDigest` alone
     carries no kind and joins nothing Plan-bound.
  3. **It is signature-independent**, as OD-SIGN-2 needs: `manifestDigest` excludes the envelope (IE:272-276), so
     synthetic (A) and authoritative (B) signing give the same values.
- **Identity effect.** None on any existing record. The two members are outside `resolvedInputs`, so the universe
  identity (`H(native.semantic-universe.typescript.v2, resolvedInputs)`, IE:353-356) is unchanged; they are not
  `plan2` members; and no TypeScript release, Plan or universe exists yet. DLV's `planIdRule` ("PlanId commits …
  artifact IDs and sha256 values") is met at M3 through the closures those values name.
- **Not decided here.** `manifestId` (RI: "the verified signed manifest") has no M3 source either. It is C4a's to name;
  this unit flags it (X-NSS4-C4) and does not choose one. `capabilityManifestId` is IE:224-235's.

### LD-N4-2. The TypeScript native capability declaration surface (X-F4-3)

- **Decision: register six native capability branches** in a CMS successor copy, all with `roleSubprotocol`
  `typescript-semantic` and `subprotocolVersion` 2:
  1. **`typescript-semantic.protocol`**, `declarationData: {capabilityTokens}`: an array of 4 to 13 unique
     `TypeScriptCapabilityToken` values (the enum of NSS-F1's handshake successor copy, `symbol-census-v1` and
     `native-context-inputs-v1` included), in any order. **This is NE §9.1's "signed capability row"**, and Hello's
     `expectedCapabilities` is its token set in ascending UTF-8 byte order.
  2. **`typescript-semantic.imports`, `.references`, `.calls`, `.types`, `.reachability`**, `declarationData:
     {relation, rung}` with the native capability matrix's pairs (`imports`/`resolved-target`,
     `references`/`resolved-binding`, `calls`/`resolved-callee`, `types`/`checked`,
     `reachability`/`from-resolved-calls`), the same pairs CMS's preview `typescript`/1 rows carry.
- **The rules that already apply, and one extended.** `capabilityId` is unique within a manifest
  (`component_manifest.rs`:472-477), so a manifest has at most one protocol row. The preview's
  "`reachability` requires `calls`" rule (`:478-482`) is extended to the native pair, through the same refusal
  (`Error::Capability`, RJ-6). Capability rows stay **metadata-only at admission** (DR103 field 9).
- **The native selection (SD-2's session-selection boundary).** It runs only on a release the existing duties have
  already admitted: parse, shape, body semantics (C2PM-1's analyzer equality included, which both body validators
  refuse, `component_manifest.rs`:507-513) and closure admission (C2PM-1's guard order: missing declaration, analyzer
  inequality, descriptor mismatch, unsupported). It never replaces one of their refusals. Among admitted releases, a
  TypeScript native session is selectable only if the manifest has exactly one `typescript-semantic.protocol` row, no
  capability row of another `roleSubprotocol` or version, and `compatibility.providerProtocol` and
  `closureProtocolMajor` both 2. An admitted release that fails this supplies no native selection, which SD-2 already
  classifies as a session-selection failure; NSS-F4 adds no manifest refusal. The token-level Plan rules are unchanged: NE §9.1 step 1
  (the four identity tokens, and every token the Plan needs, NSS-F1's included) refuses at Plan time with
  `capability-missing`.
- **C2PM-1's analyzer subprotocol is now selected for TypeScript.** An analyzer whose authenticated body declares the
  protocol row selects the named subprotocol `typescript-semantic`, whose only supported closure major is 2. The
  product's `AnalyzerSubprotocol` gets its production constructor from that admitted declaration and nothing else.
  Rust stays unselected (X-NSS4-G2).
- **T and S.** They declare `closureProtocolMajor` 1 (C2PM-1's role table) and `capabilities: []` (CR-1). Their
  `compatibility.providerProtocol` has no consumer; this unit fixes it at 1 so that equal bytes give one identity.
- **What F4 does with it.** P declares the protocol row with exactly the tokens its worker implements (F1's to state;
  NSS-F1 makes `native-context-inputs-v1` needed for every TS worker), and a relation row only for a relation its worker
  emits (none for F1-min). `symbol-census-v1` appears only in a release that implements it (FA2 X-FA2-FG).
- **Why a schema copy, and why it is not a release-format change.** DR103 field 9 makes `capabilityId` a
  host-registered vocabulary with "schema-checked" `declarationData`; registering a value is a schema edit, as CMS's
  preview rows were. The copy only **adds `oneOf` branches**: no field, role, envelope, catalog, signature, manifest
  version or existing branch changes, and every existing manifest keeps its verdict (§6). The product's generator
  accepts it (only its existing keywords and no new pattern are used).
- **Rejected:**
  - **Reusing the preview `typescript`/1 rows** for TS2. SD-2 forbids it ("not M3 TS2 or Rust3 tokens"), and their
    version would contradict `providerProtocol` 2.
  - **Putting the token array in every relation row.** One protocol row gives one source; copies could disagree.
  - **Requiring the identity tokens or the UTF-8 order in the schema.** The product generator supports neither
    `contains` nor an order keyword (`tools/security/generators/manifest_shape.py`:28), and NE §9.1 step 1 already
    refuses a row without the identity tokens at Plan time. The order is the host's projection.
  - **A new manifest semantic refusal for "exactly one protocol row".** At most one already holds; the rest is
    selection, which SD-2 keeps out of general manifest admission.

### LD-N4-3. `runtimePayloadSha256` (X-F4-4)

- **Decision.** `runtimePayloadSha256` = `hex(SHA-256(JCS({schemaVersion: 1, files})))`, where `files` holds one
  `{path, sha256, bytes}` row, ascending by the UTF-8 bytes of `path`, for each member of the **runtime-support
  inventory** (r2, RF-1).
  - **The inventory is an explicit selection,** published in this successor, of T members that are support files of
    the runtime itself. It is never derived from what the process reads, so the worker's compiler, library and
    descriptor reads add nothing.
  - **It excludes** the runtime executable (`executableSha256`), both identity descriptors (each has its own
    descriptor digest), every license notice (`licenseNoticeSha256`), the compiler and standard-library members (the
    context and the provider descriptor commit them), and the worker application's inputs (P). Excluding the runtime
    descriptor also keeps the digest free of a self-reference.
  - **For M3's only cell**, `macos-aarch64` with the official Node.js build, the inventory is exactly
    `{etc/openssl.cnf}`, the configuration `LaunchSpec::typescript` passes (`--openssl-config`). With F4's zero-byte
    file the value is `e502fb7e…97bd2` (`evidence/vectors.json` `runtimePayload`).
  - **Any other inventory**, for another cell or build (a shared library, an ICU data file), is a successor that names
    its members. `files` is never inferred from a directory listing or a trace.
- **Why.**
  1. **It names exactly the bytes DLV calls the runtime payload**, and nothing another member already commits:
     `executableSha256` commits `bin/node` and `licenseNoticeSha256` the notice.
  2. **It is a canonical record, so it cannot be ambiguous.** JCS over `{schemaVersion, files}` gives one digest per
     file set, and an added member changes it.
  3. **It matches the offline-asset list.** DLV `offlineAssets` lists `node-shared-runtime-payload` and
     `node-unicode-icu-data` as runtime-supplied. For this build both are inside the executable, so `executableSha256`
     covers them, and `files` names the one separate file the runtime reads.
- **Rejected:**
  - **F4's r1 proposal** (the JCS array of `bin/node`, `etc/openssl.cnf` and `LICENSES/node.txt`). It repeats two
    members that other descriptor fields commit, and an unkeyed array has no version for a later extension.
  - **SHA-256 of the empty string** for "no payload". The runtime does read `etc/openssl.cnf`, and an empty-string
    digest would leave that read unnamed.

## 3. Within the existing law

| Changed | Not changed |
|---|---|
| the values of four existing fields (two universe members, one descriptor member, and P's `closureProtocolMajor`/`providerProtocol`), stated as recipes | any identity domain, `H` recipe, universe identity, `plan2` member, `PlanId` of an existing Plan |
| six new `oneOf` branches in the manifest capability vocabulary | any manifest field, role, envelope, catalog, signature or schema version; any existing branch or verdict |
| one existing semantic rule extended to the native pair | any refusal code, route, DomainDetailCode or D9 row |
| C2PM-1's analyzer subprotocol selected for TypeScript | any protocol major, frame, token, limit or the control tuple (SD-2) |

## 4. What changes (exact texts in `overrides.json` and the copy)

| Parent | Selector | Inserted |
|---|---|---|
| NE | line 2839 (§9.1 token order) | for TS2 the signed row is the one `typescript-semantic.protocol` declaration; Hello's array is its set in UTF-8 order |
| NE | line 2984 (§9.4 descriptors) | where the two descriptors sit in T and P; `runtimePayloadSha256`'s recipe (LD-N4-3) |
| NE | line 3175 (§9.7 TS OpenUniverse) | the artifact members' recipe, the minting host's check and the bind check (LD-N4-1) |
| IE | line 272 (§3 closure recipes) | the two members join the explicit successor recipes |
| C2PM | line 30 (analyzer support) | the TypeScript analyzer subprotocol selection; T/S majors and `providerProtocol` 1 (LD-N4-2) |
| DR103 | `/manifestSchema/fields/9/semantics` | the native capability registration, the extended pair rule, and SD-2's selection requirement |
| CMS | complete successor copy | six `oneOf` branches appended to `$defs/capability`; serialization `json.dumps(indent=2)` + LF, as the parent |

`evidence/build_overrides.py` checks every parent at its pinned bytes, that each override is insert-only, and that no
selector is bound by the product lock's 191 successors **or by NSS-F1's adopted overrides** (NE 125, 127, 1620, 2853,
2862, 2953, 3007, 3192, 3215; startup and order-table pointers).

## 5. X-F4-2 checked: no release-format byte changes

The coordinator ruled that F4 follows M3's closure law. This unit checked the consequence and agrees:
- **DLV's two artifacts are release grouping.** `typescript-runtime` and `typescript-provider` are `ReleaseManifestV1`
  artifact entries (DLV `packaging.releaseManifestEdges`). M3 builds no `ReleaseManifestV1`, so no artifact byte exists
  to change.
- **DLV's binding sentences hold by digest.** "The descriptor, compiler JavaScript, standard-library corpus … are
  inside the signed typescript-provider artifact": in M3 the provider descriptor is in P and names
  `typescriptCompilerSha256` (T's `lib/typescript.js`) and `typescriptStdlibMerkleRoot` (S's identity), so P's
  identity commits to those bytes, and T and S commit the bytes themselves.
- **The descriptors are byte-for-byte DLV's.** Both keep DLV's closed member lists and JCS canonicalization; LD-N4-3
  only gives one member its recipe.
- So F4's three-closure packaging changes no release-format byte. If a later release unit builds `ReleaseManifestV1`,
  mapping its two artifacts onto T/S/P is that unit's question.

## 6. The retained-identity check (LD-Q-10's lesson)

| Document whose digest moves | Pins (product `d6434107`, by `git grep`) | Class | Retained identity? |
|---|---|---|---|
| CMS `80254f9e…` → copy `e698f9d6…` | `tools/security/inputs/sources.json`, `crates/security/src/generated/component_manifest_shape.rs` | live generation pins, which move at binding | **no**: the manifest schema digest is in no `closure2` descriptor (whose `manifestDigest` is over the body bytes), no catalog, envelope or Plan member; architecture hits are historical `verify-design.log` copies |
| NE, IE, DR103, C2PM | — | parents frozen; overrides live in the successor record | no change |

- **Verdict audit.** The copy gives the same verdict as the parent on all 11,010 cases of the product's shape oracle
  (`crates/security/tests/fixtures/manifest268-shape.ndjson`), and the parent reproduces every fixture verdict
  (jsonschema 4.25.1, vendored). No case in that file, the 186 semantic cases or the 301 inventory cases mentions
  `typescript-semantic`, so the semantic-rule extension turns no verdict either.
- **New cases** (13): five valid native manifests (protocol row alone; with `imports`; all six; tokens in any order;
  with `symbol-census-v1`), each refused by the parent and admitted by the copy; eight refused by both (an unknown token,
  a duplicate, three tokens, an extra member, a wrong rung, the native subprotocol at version 1, the preview subprotocol
  at version 2, an unregistered id). The copy never refuses what the parent admits.
- **Generator.** The product's `tools/security/generators/manifest_shape.py` generates from the copy (exit 0;
  `component_manifest_shape.rs` `2c2a1e56…`), run in `evidence/gen-scratch/`.
- **Token source.** The protocol row's enum is read from NSS-F1's adopted handshake copy at its pinned bytes
  (`260fb535…`).

## 7. Controls the implementing units carry

| ID | Control | Owner |
|---|---|---|
| N4-1 | Universe minting: `runtimeArtifactSha256` equals the context's toolchain closure suffix; `providerArtifactSha256` equals the selected provider closure's suffix; a provider value naming no selected closure refuses before spawn | C4a / C2b-1a |
| N4-2 | `bind_typescript_universe` refuses a runtime-artifact disagreement with `native.universe-context-field-mismatch:runtimeArtifactSha256` | C2b-1a |
| N4-3 | The same values under synthetic (A) and authoritative (B) signing of the same bodies | F4-b |
| N4-4 | The 13 new manifest cases and the 11,010-case oracle, run against the regenerated product shape | binding unit / C2a successor |
| N4-5 | `typescript-semantic.reachability` without `.calls` refuses (`Error::Capability`) | security semantic owner |
| N4-6a | **Positive selection** (r3): after the existing admission and Plan-token prerequisites succeed, an analyzer release with exactly one `typescript-semantic.protocol` row, no capability row of another `roleSubprotocol` or version, and `(closureProtocolMajor, providerProtocol)` = `(2,2)` supplies the native selection `analyzer`/`typescript-semantic`/2, including with no relation row (F1-min) | D4 / C4a |
| N4-6b | **Unavailable selection among admitted releases** (r2, RF-2; r3): no protocol row; a preview `typescript`/1 row, or any row of another `roleSubprotocol` or version, beside the protocol row → no native selection, no manifest refusal, and no earlier refusal replaced. Two protocol rows refuse earlier, by capability-id uniqueness. | D4 / C4a |
| N4-7 | Earlier refusals are kept (r2, RF-2): `(closureProtocolMajor, providerProtocol)` = `(2,1)` and `(3,2)` refuse with C2PM-1's analyzer mismatch (`ClosureProtocolMismatch` in both body validators; `native.closure-protocol-analyzer-mismatch` at projection), never as a selection failure; `(3,3)` with the TS2 protocol row and a matching descriptor reaches `native.closure-protocol-unsupported` only after its prerequisites; a missing declaration and a descriptor mismatch keep their earlier places in C2PM-1's order. `AnalyzerSubprotocol` is constructed only from an admitted protocol row. | security semantic owner / C2a successor |
| N4-8 | Hello's `expectedCapabilities` is the protocol row's set in UTF-8 order; a reordered manifest array gives the same Hello | D2b / C4a |
| N4-9 | `runtimePayloadSha256` for F4's T equals `e502fb7e…97bd2` when `etc/openssl.cnf` is zero bytes. Membership (r2, RF-1): T's `lib/typescript.js`, `lib/lib.*.d.ts`, `package.json`, `typescript-runtime/identity.json` and `LICENSES/*` add no row, and neither does a P file; a change to `etc/openssl.cnf`'s bytes changes the digest; a support member named by a successor inventory adds a row and changes the digest | F4-a |

## 8. Not claimed

- No product, architecture, registry, generated or review file is changed. No release is built, signed or admitted.
- No decision on `manifestId`, on Rust's capability rows or analyzer subprotocol, on `ReleaseManifestV1`, or on F4's
  other plan items.
- No measurement of a Node.js build. LD-N4-3's claim that the official macOS arm64 build links ICU and OpenSSL rests
  on the release's published metadata, which F4 records (F4 PLAN-r2 §4); CF-1's tier-1 trials are the first real check.

## 9. Cascade

| ID | For | Item |
|---|---|---|
| **X-NSS4-B** | binding (recommended: F4's first unit, with the C2a successor that regenerates the shape) | Materialize `successor.json` in FA-2's form from `overrides.json` and the copy, under `docs/implementation/m3/native-successors-fa/nss-f4/`. Copy the CMS successor to `tools/security/inputs/manifest-schema.json`, regenerate the shape, re-pin `sources.json`. Bind after NSS-F1's binding, re-running `build_overrides.py` against the then-current lock. |
| **X-NSS4-F4** | F4 | P's protocol row and relation rows, `providerProtocol`/`closureProtocolMajor` 2; T and S at 1; `runtimePayloadSha256` per LD-N4-3; `closure-build.json` publishes the two artifact values per LD-N4-1. |
| **X-NSS4-C4** | C4a (and C2b-1a) | Mint the two artifact members (LD-N4-1); name `manifestId`'s M3 source, which no text gives. |
| **X-NSS4-SEC** | security semantic owner / C2a successor | The extended pair rule; `AnalyzerSubprotocol`'s production constructor. |
| **X-NSS4-D** | D4, D2b | The selection rule of LD-N4-2; Hello's array from the protocol row. |
| **X-NSS4-G2** | G2 (Rust closures) | The same form applies to `rust-semantic`/3; not decided here. |
