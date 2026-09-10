# OpenSIP DR-011-R10 — blind consumer-B reconstruction (v7)

**Verdict: CHANGES_REQUIRED** — one MUST and two SHOULD design gaps remain.

I am a fresh session with no prior review context and no authorship of this
design. Everything below was reconstructed from the 45 files of
`consumer-b.v7/subject` alone. I read no author reference implementation (none
is in the kit), no fixtures, no goldens, no prior review, and no other
`/tmp/opensip-design-corrections` directory. Every helper — the canonical
encoder `C`, the exact typed/lexical admitter, `H(D,X)` and its retained frame,
CVE1, `CAP-MANIFEST-ID-V1` and its four gates, the FACT-IDENTITY body frame, the
`x-opensip-order` admission layer and the whole retained-closure checker — was
written from prose and schemas in this session and is in
`output/work/`.

---

## 1. Input custody

`consumer-input-manifest.json` declares 45 files, parent subject
`cd6e828c22c6bc0ecf07ab8fe1f4bd5d1a5a8726708e0deffac99960bdc25a44`.

| Check | Result |
|---|---|
| SHA-256 of every declared file | 45/45 match |
| Byte length of every declared file | 45/45 match |
| Files present but undeclared | 0 |
| Total bytes | 2 689 025 |

Two independent corroborations that the manifest digests really are the
`raw-artifact` representation the digest law names: my
`sha256(exact document bytes)` for `identity-schemas.v2.json`,
`relation-payload-schemas.v2.json` and `native-evidence.schemas.v2.json`
reproduce the manifest values, and those same values are what a `fact2`
`payloadSchemaDigest` and a `coverage2` `payloadSchemaDigest` must carry.

**No input-custody problem was found.** Every normative recipe I needed was
present in the kit. The contracts name reference *files* that are deliberately
excluded (`foundation/canonical.py`, `foundation/identity-model.py`,
`native/native_evidence_model.v2.py`, `discovery-defaults.py`,
`integration-host-model.py`, the checkers); in every case the **law** those
files implement is published in prose or in a machine-readable registry, and I
reconstructed and executed it. Two bounded exceptions are recorded as
advisories in §7 (`PROTOCOL3_RULES`, `UNICODE_CASE_DATA_VERSION`); neither
blocked any vector.

---

## 2. The reconstructed chain

Zero-config discovery → typed config/source → invocation/step/attempt →
Plan → native facts/Coverage/view → proof verification → Evidence/Seal/Run →
receipt and current availability. Owner of each decision, by exact selector:

| Stage | Decides | Owner |
|---|---|---|
| project authority root, custody, nested boundaries | which tree is the project | security `S3`; output `DiscoveryProvenanceV1`, `AdmittedBoundaryInventoryV1` |
| language workspace units inside that root | which units exist, `WorkspaceUnitV2`, `FileMembershipRowV1` | native `§1.4` U-1…U-8; boundaries come **from** security, never re-derived |
| shared prune rule (`node_modules`, VCS, Cargo `target`) | what is not walked | one rule, consumed by both instruments (security `S3` "One shared discovery rule", native `§1.4` U-4a) |
| resolved semantic configuration | five always-present sections; `analysis` always carries `profileId`/`capabilities`/`budget` | admission-and-qualification `§1.1`; shape closed by `identity-schemas.v2#/$defs/semantic-configuration` |
| capability request | matrix-fixed default: every capability whose `(capability, mode)` cell is not `NOT-SELECTED` | `native-capability-matrix.v2.json#/capabilityIdLaw` (11 members) + native `§1.4` |
| release **availability** (never scope) | which capabilities this build declares | `native-evidence.schemas.v2.json#/$defs/ReleaseCapabilityRegistryV1`; absence disclosed on `CommandEnvelope.availability` |
| snapshot | `snapshot2` over ProjectId, inventory, config, scope, VCS digests | identity `§3` |
| native context / universe | what interpreted the bytes | native `§2.3`/`§2.4`/`§1.2`; H domains registered in `x-opensip-digest-domains.domainSets` |
| Plan | `plan2` binding snapshot, capability manifest, closures, spec, contexts, imports, policy, waivers, scope, budget, grant | identity `§3` |
| facts / scopes / Coverage | native producer boundary, then re-decided at Run closure | native `§4.1a`, `§4.3`; `relation-payload-schemas.v2#/x-opensip-relation-registry` |
| view | one producer's interpretation; partition disjointness decided **here** | `coveragePartitionLaw` |
| proof | pure evaluator, predicate node addressing, witnesses | identity `§4` + `program-predicate` |
| evidence / seal / Run | acyclic: proof ⊄ evidence, evidence ⊂ seal, seal ⊂ Run | identity `§3` domain table |
| receipt / availability | operational custody, excluded from semantic identity | identity `§5`, `commit-receipt`, `availability` |

**Semantic identity vs operational authority.** RequestId, ExecutionId, StepId,
wall clocks, PIDs, consent, nonces, receipts, `authorizationRef`,
`securityGrantRef` and output destinations are operational and enter no content
identity. I verified the non-equivalence the identity contract claims for
`ExecutionId`: the inherited `c2-plan-stage-schema.v4` pattern ends in a bare
`$` and **admits** `exec1_<32 hex>\n`; the product successor
`^exec1_[0-9a-f]{32}(?![\s\S])` and `common.schema.json#/$defs/ExecutionId`
both **refuse** it. Measured, both directions.

**Mutation vs analysis steps.** Only `analysis` and `verify` seal or link a
`run2`. `mutation`, `import`, `repair-apply`, `native-preparation`,
`test-execution`, `comparison`, `query`, `render`, `export-delivery`, `doctor`
mint no Run. I reconstructed both idempotency recipes and confirmed they are
different recipes, not two spellings of one:

* generic mutation — `H("workflow.mutation-intent", MutationReplayScopeV1)`
  over the closed `{schemaVersion, requestId, stepId, projectId, operation}`,
  returned as **bare 64-hex**:
  `f1063d3970320b6780c080f0d79b7ff0f7df3ed7ecbc1b730548f314c2fce599`.
  A different fresh `RequestId` yields
  `77a796cf706e7388c705db7138091679a7550f3bb8d3da45ef8d1c9a0dda158f` — fresh
  requests never deduplicate each other's mutations.
* repair apply — **raw SHA-256** of
  `C({operation, projectId, repairPlanId, baseSnapshotId})` =
  `0cc864d2bb47701cfa385c3b712886992d42b4a2a59f5e6daf3da22de5437b1c`, and
  `repair-apply` is refused by an explicit `not` in **both** generic fields.

---

## 3. Complete positive Run graphs

Eight complete graphs. For each, every record is validated against its owning
normative schema, every declared `x-opensip-order` is admitted, every identity
is recomputed from its retained descriptor, every H preimage frame is fetched
and re-parsed, and the retained closure and cross-record joins are executed.

`output/work/verify.py` reloads only the exported object table and blob bytes
and re-runs everything **from scratch**:

```
/tmp/opensip-architecture-review-env/bin/python -I -B \
    /tmp/opensip-design-corrections/consumer-b.v7/output/work/verify.py
```

| Graph | objects | blobs | closure checks | result |
|---|---|---|---|---|
| RUN-TS | 46 | 120 | 326 | ADMITTED |
| RUN-RS-A | 41 | 114 | 280 | ADMITTED |
| RUN-RS-A2 | 41 | 114 | 280 | ADMITTED |
| RUN-RS-B | 40 | 110 | 272 | ADMITTED |
| RUN-RS-PARTIAL-ENUMERATION-DISCLOSED | 37 | 99 | 248 | ADMITTED |
| RUN-RS-NO-OWNERSHIP-DISCLOSED | 37 | 99 | 246 | ADMITTED |
| RUN-SYN-CODE | 31 | 82 | 169 | ADMITTED |
| RUN-SYN-DATA | 28 | 78 | 153 | ADMITTED |

**8 graphs, 1974 closure checks, 0 failures.**

### RUN-TS — the ordinary TypeScript project

Repository I chose: `package.json`, `package-lock.json`,
`project.tsconfig.json` (an **explicitly selected custom-named** entry config
extending `["tsconfig.base.json", "tsconfig.strict.json", "tsconfig.base.json"]`
— three ordered bases with the **first base repeated**, precedence retained in
the `extendsResolved` sequence), `tsconfig.base.json`, `tsconfig.strict.json`,
`src/a.ts`, `src/b.js`, `shared/config.base.json`, `web/jsconfig.json`
(a **JavaScript config inheriting a shared base with another filename**),
`web/app.js`, `pkg/package.json` (marker-only → **synthesized configuration**),
`pkg/index.js`, and `node_modules/left-pad/package.json`, which is **pruned from
the snapshot inventory** and retained instead as a
`ResolvedNodeModulesLayoutV1` read-set row joined by digest.

Three TypeScript native contexts under one Plan (`ts-tsconfig`, `js-allowjs`,
`js-synthesized`) — the contract's "several of the same language" case.
`nodeModulesInReadSet=true` on the first, so the `imports@resolved-target` fact
resolves the **bare specifier** `left-pad`; the other two carry `null` layouts.

`configOrigin` is **derived, never asserted**: the custom-named entry is
`kind: other` under the exact-basename law and still derives `tsconfig`; the
`web/jsconfig.json` entry derives `jsconfig`; the empty graph derives
`synthesized`.

File facts carry the inventoried path/hash/length joins for all 12 inventory
rows, and the `complete file@enumerated` Coverage discharges its totality
obligation against the view's own facts on the full five-coordinate `matchOn`
tuple.

Clone body identities (my own bytes, my own computation):

| body | level | languageId | bodyIdentity |
|---|---|---|---|
| `src/a.ts` | `L0-verbatim` | `typescript` | `sha256:c71533d8…5815507` |
| `src/a.ts` | `L1-lexical` | `typescript` | `sha256:117666ac…4f7f4390` |
| `src/b.js` | `L0-verbatim` | **`javascript`** | `sha256:5b7de0f8…6318fccf` |

`src/b.js` is read by the **TypeScript engine universe** and still carries
`languageId: javascript` — the body language, not the provider identity, exactly
as the `bodyLanguageByVariant` selector requires. At `L0` I recompute the
payload from the enclosing fact's own anchor span and check
`payload_len == raw_byte_len + 4` (the payload is length-prefixed twice, per the
identity contract's disambiguation of the inherited grammar). At `L1` I check
retained-preimage custody and token-stream framing only, and claim nothing about
the tokenisation. `languageVersion` is the raw 32 bytes of
`SHA-256(C(body-language-version))`, with the record **recomputed** from the
universe, the admitted context and the anchor — never accepted.

### RUN-RS — the mixed-edition Rust workspace

`Cargo.toml` (workspace, `wsroot` 2021), `crates/legacy` (2018),
`crates/modern` (2021 with a `[[bin]] tool` target whose `targetEdition` is
**2024**, differing from its package default), `crates/#odd` (a **valid `#`
marker directory**, admitted by the canonical path contract and closing a
complete Run), `shared/dual.rs` (the **same physical file owned by two targets
at two editions**), a `.cargo/config.toml` replaced by the projection, and a
**21-crate edition map**.

`unitId` is `H("native.compilation-unit.v1", {schemaVersion, markerPath,
targetKind, targetName})`, re-derived at admission — the published four-field
preimage, not a delimiter label. Measured results across four explicit
selections:

| selection | `shared/dual.rs` dialect | body identity |
|---|---|---|
| A `{legacy-lib, modern-bin, odd-lib}` | `{edition: 2018}` | `sha256:04de09ed…9ca08a60` |
| A2 = A ∪ `{legacy-test}` (same effective edition) | `{edition: 2018}` | `sha256:04de09ed…9ca08a60` |
| B `{modern-lib, modern-bin, odd-lib}` | `{edition: 2021}` | `sha256:5e8713e6…271176df` |

* the **same physical path under two distinct explicitly selected target
  editions** mints two body identities under two `sourceUniverse`s — two
  analyses, not two readings of one;
* **selection change without a dialect change keeps the body identity** while
  changing the universe identity (A vs A2) — the required stability control;
* an **ordinary mixed-edition workspace closes in one universe**: bodies of
  2018, 2021 and 2024 all admit under selection A.

Ambiguity and partial enumeration, derived and enforced rather than asserted.
I re-derive the owed `(deficiency, nativeCause)` from the committed ownership
record and **this scope's own subjects**, in the selection law's fixed order:

| case | Coverage | measured |
|---|---|---|
| partial enumeration, correctly disclosed | `unknown` / `input-closure-incomplete` / `body-language-owner-unenumerated`; seal indeterminate | **ADMITTED** (positive control) |
| no committed ownership, correctly disclosed | `unknown` / `input-closure-incomplete` / `body-language-ownership-missing` | **ADMITTED** (positive control) |
| **empty clone view claiming `complete` from partial ownership** | — | **REFUSED** ×3: `COVERAGE_DIALECT_PREREQUISITE`, `…_UNDISCLOSED`, `…_CAUSE_MISMATCH` |
| both owners of `shared/dual.rs` selected, editions disagree, claiming `complete` | — | **REFUSED** ×3, cause `body-language-owner-ambiguous` |

Enumeration completeness and resolution completeness stay separate throughout:
no `file` fact carries a resolved rung, and RC-1 forces every non-resolved rung
to `not-applicable` / `attempted:false` / count 0 / classes `[]`.

### RUN-SYN-CODE and RUN-SYN-DATA — compiler-free syntax-only

RUN-SYN-CODE is a repository with **no TypeScript and no Rust compilation unit
at all**: `lib/util.js`, `README.md`, `tool/main.py`. Selected grammars:
`javascript` (`syntaxClass: code`) and `markdown` (`data-document`).

* inventory (`file@enumerated`) is **complete over every inventoried path**,
  including `tool/main.py`, which has **no bundled grammar** and is
  `unsupported-file / no-bundled-grammar` — inventory capabilities are exempt
  from grammar ownership at both boundaries, and the fact carries zero anchors
  so there is no anchor path to gate;
* `declares@syntactic` and `clones@normalized-body-hash` close over
  `lib/util.js`;
* `references@resolved-binding` is **correctly unavailable**: `coverage:
  unknown`, `language-tier-unsupported`, `capability-missing`, with
  `resolutionCompleteness.state: not-attempted`, `attempted: false`, count 0;
* a `README.md`-scoped clone request is **unavailable even in this mixed
  snapshot** — a supported code file elsewhere does not serve it.

RUN-SYN-DATA is the already bundled data/document set (`json`, `toml`,
`markdown`, `yaml`). Its declared **inventory** capability closes with a genuine
`complete`; `clones` and `declares` are disclosed unavailable. A **complete
empty result does not conceal unsupported analysis** — asserting `complete` on
either produces three refusals.

Code-versus-data was verified against the published matrix and the body law,
not assumed: a `data-document` grammar claiming `code` refuses
(`SYNTAX_GRAMMAR_CLASS_CONTRADICTS_REGISTRY`), a Markdown-anchored `declares`
fact refuses (`SYNTAX_CAPABILITY_UNSUPPORTED_FACT`), and selecting a grammar the
bundle does not contain refuses (`native.syntax-grammar-not-in-bundle`).

**Grammar parse ≠ compiler parse.** The identical body bytes
`function pad(n) {\n  return String(n);\n}\n`, both at `L0-verbatim`, both
`languageId: javascript`, mint

* `sha256:5b7de0f8…6318fccf` under the TypeScript engine universe, and
* `sha256:e61fb1e4…c4155341` under the grammar-only syntax universe,

because `languageVersion` binds the component that interprets the span — the
compiler in one case, the bundled grammar parser in the other. Required, not
incidental.

---

## 4. Admission before encoding

### Raw-input lexical admission (on BYTES, before decoding)

Refused, each with its own boundary: duplicate key; `1.0`; `1e0`; `1E0`;
`1.0000000000000001`; `9007199254740991.1`; `-0`; `NaN`; `Infinity`;
`18446744073709551616`; `-9223372036854775809`; lone surrogate; malformed
UTF-8; a raw control in a string; trailing bytes; depth 33.
Admitted: an ordinary integer; an **escaped** newline in ordinary text; depth
32; a surrogate pair. This is a genuinely separate gate from encoding an
already-parsed object, and both are exercised: on **decoded** values the exact
type gate refuses `True`, `1.0` and `"1"` for an integer field while `C` still
happily encodes `true` and `"1"` — which is why the gate, not the encoder,
is what decides.

### Canonical encoder `C`

Nine hand-spelled byte vectors, all reproduced: UTF-8 key byte order (`Z < a <
b < é`), non-BMP key ordering (`U+FFFD` before `U+1F600`), arrays in **admitted
order** (`[3,1,2]` stays `[3,1,2]`), ` `/`` lowercase escapes with
`\t`/`\n` short forms, `U+007F` and `U+2028` **unescaped**, slash not escaped,
NFC and NFD kept **distinct** (and therefore distinct digests), integer bounds
`[-2^63, 2^64-1]`.

### `H` and the retained frame

`H("subject-scope", {"schemaVersion":2})` =
`0ec16b65c5012397b2ee7ec6ca96b5e118e68bf0335893ea814ba364a07fa3fc`; the frame
`6f70656e7369702e70726f647563742e763100 7375626a6563742d73636f7065 00
0000000000000013 7b22736368656d6156657273696f6e223a327d` equals my hand-spelled
concatenation, and `H ≠ SHA256(C(X))`. Offering a raw canonical payload where a
frame is required fails on the prefix; offering a frame where a
`canonical-record` is required fails parsing. Both measured.

### Capability-manifest admission — registry selected by name

The effective ADM-DOMAIN registry is
`docs/coop/design-corrections/native/capability-manifest-domains.v2.json`,
selected by identity `§3` and listed by native `§11`. My own manifest (two
providers, one absent row) is admitted by all four gates in the inherited order
and commits 884 bytes with
`capabilityManifestId = 6edad58e40bf4029a4c2c7e7f2d95c83a0b4997281bef74c63cca453404dff54`;
`decode(encode(x)) == x` holds literally.

Eleven negatives, each refused by exactly one named gate, and each showing the
id a skipped gate **would** have minted (CVE1 is total on booleans and strings,
so only the gate refuses):

| gate | vector | would mint |
|---|---|---|
| ADM-TYPE | `schemaVersion: true` | `3739a3a6…` |
| ADM-TYPE | `schemaVersion: "1"` | `4c0ae24a…` |
| ADM-CLOSED | undeclared key on `ProviderCapability` | `3b30db0c…` |
| ADM-CLOSED | missing `language` | `80a6390d…` |
| ADM-DOMAIN | `platformIds: ["MACOS-AARCH64"]` (case variant) | `a1342ce1…` |
| ADM-DOMAIN | relation key not in `RELATION-DOMAIN-V2` | `9fcb7550…` |
| ADM-DOMAIN | `clones: "resolved-callee"` — a rung of another relation | `30c8b10b…` |
| ADM-DOMAIN | deficiency outside `DEFICIENCY-DOMAIN-V1` | `73a81f56…` |
| ADM-ORDER | `providers` unsorted | `98ad2dd5…` |
| ADM-ORDER | `platformIds` unsorted | `09181c14…` |
| ADM-ORDER | duplicate `platformId` | `b561631b…` |

The successor registry is doing real work: `unresolved-edge` is a member of
`RELATION-DOMAIN-V2` (13) and was **not** expressible under the inherited
twelve-member domain, and `RELATION-LADDER-DOMAIN-V2.ladders` is **equal and in
order** to the single ladder authority
`relation-payload-schemas.v2#/x-opensip-relation-registry/relations[].ladder`
(drift-checked; zero differences).

*Implementation cross-check, clearly separated from my own vectors:* my
independently written CVE1 encoder/decoder, id recipe and gates reproduce all
seven retained normative vectors of `delivery.v4` byte-exactly, re-encode them
literally, and admit all seven. That checks my implementation against retained
normative **measurements**; it is not an oracle for any expected value above.

### The declared-order admission layer is load-bearing

`x-opensip-order` is a real admission step, not decoration. A `subject-scope`
whose `canonical-set` `subjects` array is reversed is **admitted by JSON Schema
alone** (`uniqueItems` is satisfied) and **refused** by the declared-order
admission (`ORDER_NOT_ASCENDING`). I enforce it on every retained record in the
closure.

---

## 5. Registered relation / rung applicability

Derived from the registry, not restated: 18 registered `(relation, rung)` pairs
over 13 relations. Five are **resolved** rungs (`imports@resolved-target`,
`references@resolved-binding`, `calls@resolved-callee`, `types@checked`,
`reachability@from-resolved-calls`) and take a state from
complete/incomplete/partial/not-attempted; the other **thirteen** are
`not-applicable` with `attempted:false`, count 0, classes `[]` — including
`unresolved-edge@observed`, which is **not** a resolved rung because the
relation records the edges resolution did not close. `reachability` is the case
that shows ladder length is not the rule: one rung, and it is resolved.

Anchor law, applied in every universe: `source-text` ≥ 1 (nine relations),
`body-identity` = 1 (`clones`), `inventory` = 0 (`file`, `package`,
`vcs-change`). Both cardinality violations refuse
(`FACT_ANCHOR_CARDINALITY`) — an unanchored `declares` under a **TypeScript**
universe and an anchored `file` fact.

Coverage laws applied **even where no fact is present**: RC-0 decides the pair
before any fact is read; `coverageTotality` exists only for `file@enumerated`
and is discharged on the full five-coordinate tuple against the view's own
facts (a cross-universe fact does not pay another universe's obligation);
`coveragePartitionLaw` disjointness is decided at retained closure over every
scope the view references, **including scopes with no Coverage entry**.

Minimum-resolution satisfaction is ladder-index comparison **inside one
relation**, with no global rank:

| relation | fact rung | `minResolution` | result |
|---|---|---|---|
| `declares` | `syntactic` | `syntactic` | satisfied |
| `references` | `syntactic-name-match` | `resolved-binding` | **insufficient** |
| `references` | `resolved-binding` | `resolved-binding` | satisfied |
| `types` | `annotated` | `checked` | **insufficient** |
| `types` | `checked` | `checked` | satisfied |
| `imports` | `resolved-target` | `syntactic-specifier` | satisfied (stronger ≥ weaker) |
| `declares` | `resolved-callee` | `syntactic` | **REFUSED** — a rung of another relation |
| `clones` | `normalized-body-hash` | `checked` | **REFUSED** — cross-relation comparison |

Repair evidence requirements and the imported-observation boundary: the plane is
decided at admission from the relation's registry membership, never from the
value. A native requirement claiming `import-unmapped-only` and an imported
requirement claiming `resolution-incomplete` are both refused as cross-plane;
`declares@resolved-callee` is refused on the ladder; the two vocabularies are
disjoint and the schema `oneOf` agrees.

---

## 6. Public surface, workflow and lifecycle

**Zero-config over several workspace units.** The matrix-fixed default requests
11 capabilities for each `ts-*`/`js-*` unit and 10 for `rust-*` and
`syntax-only` (the three `clones-cross-tsjs` cells are `NOT-SELECTED`). For my
three-unit repository that is 31 rows. With a release declaring less than the
product requires, the **original invocation** discloses the absence on
`CommandEnvelope.availability`:

* a single-step command projects one `CapabilityAvailabilityStepV1` with 5
  notices; a named multi-step invocation projects one entry **per analysis step
  that made a selection**, with different selections at steps 1 and 3 (4 notices
  total);
* each notice carries the **complete ownership tuple in typed fields** —
  `capabilityId`, `languageMode`, `workspaceRoot` — never concatenated, with
  `code: native.capability-unavailable`;
* a step that selected and found nothing absent contributes an **empty** entry;
  an invocation that selected nothing carries `{0, 0, []}` rather than omitting
  the field;
* **candidate-only** capabilities (`clones-near`, `clones-cross-tsjs`) have
  empty matrix `relations`, so this is their *only* public route — they have no
  Coverage entry at all. Fact-producing absences keep their `relation@rung`
  Coverage, and `language-tier-unsupported` outranks `provider-unavailable`
  where both apply.
* All four collections validate against
  `common.schema.json#/$defs/CapabilityAvailabilityV1`.
* Bounded cardinality and ordering: `notices ≤ 1024` (exactly the analysis-spec
  request bound, so a step can never truncate), `steps ≤ 64` (the invocation's
  own `StepId` bound), order is the selection's own `sequence`,
  `noticeCount`/`totalNoticeCount` are exact sums.
* Applicable output formats come from the inventory, not from prose:
  `capability-availability` is a declared `parityField` of every
  `requestClass: analysis` command — `default`, `analyze`, `fit`, `audit`,
  `repair-verify` — and each carries it in *its own* declared formats
  (`fit` has no SARIF; `repair-verify` has no HTML).
* Availability is not qualification: no cell is `QUALIFIED`,
  `platformQualified` stays false, and an explicit `analysis.capabilities`
  override changes the **request**, not the obligation.

**Failure envelopes, complete rather than a termination fragment.** Seven
public examples, each a full `CommandEnvelope` major 2 validated against
`command-envelope.schema.json`, composed from an actual internal refusal plus
its originating boundary:

| origin | class / exit | errorCode | `errors[0].code` |
|---|---|---|---|
| external **configuration** input | request-rejected / 2 | `CONFIG.INVALID` | `CONFIG.INVALID` |
| externally supplied / **retained** spec | request-rejected / 2 | `REQUEST.PRECONDITION_FAILED` | `native.capability-spec-invalid` (termination `domainDetail` lawfully **absent**) |
| **host-generated invalid internal record** | operational-failed / 4 | `SYSTEM.OUTCOME.ILLEGAL_STATE`, `faultCause: host-invariant` | `HOST.INVARIANT_VIOLATED` |
| **producer boundary** failure | operational-failed / 4 | `PROVIDER.PROTOCOL_VIOLATION`, `faultCause: provider-protocol` | `native.coverage-cause-unsupported` |
| `NOT-SELECTED` cell (origin-independent) | request-rejected / 2 | `REQUEST.UNSATISFIABLE` | `PROVIDER.NOT_SELECTED` |
| required renderer after commit | operational-failed / 4 | `DELIVERY.REQUIRED_FAILED`, `faultCause: delivery-required`, `runId` retained | `DELIVERY.RENDERER_FAILED_AFTER_COMMIT` |

Bounded diagnostics: a structurally valid 4096-character `languageMode`
composes a 4149-character subject. My `bounded_subject` elides in **Unicode
scalars** (what `BoundedText.maxLength` counts), preserving the registered key,
producing exactly **1024** code points and appending the SHA-256 of the
untruncated UTF-8 bytes — verified to be the digest of the untruncated value.

**D9 extension checked against the inherited contract.**
`d9-exit-contract.v1.14.json#/codeMaps/faultCauseToErrorCode` has ten members
and `#/scenarioAxesSchema/properties/faultCause/enum` eleven (with `none`).
`common.schema.json#/$defs/D9FaultCause` has twelve. The successor adds
**exactly** `host-invariant`, mapped to the existing `SYSTEM.OUTCOME.ILLEGAL_STATE`,
which is the **only** error code with no cause preimage in the inherited maps —
consistent with the contract's precision that "total and injective" is over the
declared cause domain. Classes, exit codes and reason codes are unchanged
(measured equal).

**Pinned-purge refusal, complete.** `evidence.pinned` →
`request-rejected` / `REQUEST.PRECONDITION_FAILED` / exit 2, in a `kind=failure`
envelope carrying that `DomainDetail` in **both** the termination and `errors`,
with `subject` = the RunId and the closed `PinnedPurgeDisclosure`: the same
RunId, the complete `activePins` inventory sorted uniquely by `pinId`
(`baseline.main`, `export.q3`, `repair.plan-7`), and the three ordered
consequences. No pin omitted, truncated or aggregated. Schema-valid.

**Current-baseline audit and comparison.** Four descriptors, all schema-valid:

* a **removed detector** — E1…E4 false, E0 `unavailable`, `E0` never
  substituted with B, entry `INDETERMINATE`
  (`pivot-detector-unavailable`), gates, verdict indeterminate;
* **evidence content changed** on a gating rule — `INDETERMINATE`
  (`evidence-content-changed`) with a `required-evidence-unavailable` rule
  deficiency, not a non-gating `EVIDENCE-DELTA`;
* an **empty result on both sides** with a missing required E2 re-evaluation —
  zero entries, still `indeterminate`, because a missing evaluation can hide a
  finding that appears in neither set;
* whole-comparison indeterminacy (unmapped project) — `comparisonPerformed:
  false`, zero entries, typed remedy.

**The `ScopeDocumentV1` scope-policy axis, bound for real.** I bound a real
`ScopeDocumentV1` into the retained analysis spec as a `parameter` row under its
exact registered document — `workflows/schemas/policy-document.schema.json`,
digest `012505da479197875602899c027b3d0daea9e23e01e490e3dc94bbe3d7062e18`, whose
row selector is `#/$defs/ScopeDocumentV1`. Two Plans differ **only** in that
parameter's `payloadDigest` (`5186a5c7…` vs `339fad44…`) and mint different
PlanIds (`plan2:bda01711…` vs `plan2:eaa543e1…`), while the foundation
`scope-descriptor` that `plan.scopeDigest` names is **byte-identical**
(`4718b316…`). The comparison then attributes the change to E2→E3 with
`contextDelta.scopeChanged: true` and `SCOPE-DELTA` — the policy's include/
exclude glob selection, distinct from the repository extent actually walked and
from discovery scope.

**Repair descriptor projection from original native evidence.** The
`RepairPlanDescriptor.closedWorld` is the **five-field projection**; a literal
copy of the seven-member `ClosedWorldV2` is refused by the schema
(`'dynamicDispatch', 'reasons' were unexpected`). The authority boundary holds:
the gate is decided against the evidence Run's own full record *before* any
descriptor is built, and the projection grants no evidence authority of its own.
Discriminating controls I chose:

| control | `applicable` | unmet |
|---|---|---|
| closed world established, requirements satisfied | true | — |
| `deadCodeRepairEligible: false` on a `delete` edit | false | `REPAIR.CLOSED_WORLD_NOT_ESTABLISHED` with the record's own `reasons` |
| `evidenceOrigin: imported-prepared-declared`, closed world otherwise eligible | false | same code — a DECLARED prepared expansion is not authority for an unsafe repair |
| an unsatisfied native requirement | false | `resolution-incomplete` (and see SHOULD-1) |

**Explicit test / preparation / repair authorization.** All four effect
selections are **copied** from `permission-truth-tables.v9.json`, in the
`child-process` execution mode those owners run in, on both platform tables:
`subprocess`→`PT-PROC-EXEC-DECLARED`=`DISCLOSURE-ONLY`,
`filesystemWrite`→`PT-FS-WRITE-HOST-STATE`=`DISCLOSURE-ONLY`,
`network`→`PT-NET-EGRESS`=`DISCLOSURE-ONLY`,
`environment`→`PT-ENV-READ`=`ENFORCED-BY-CONSTRUCTION`.
`PT-HOST-EFFECT-BROKERED` (the one `ENFORCED-AT-HOST-BROKER` token) and the two
read-only tokens are projected by **no** effect name. A `RepoExecutionGrantV2`
for build-script/proc-macro owners, a test-runner grant whose `owners` is `[]`
and whose `ownerSourceDigest` is the digest of the canonical empty owner array —
my independently computed
`4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`, which is the
value security S10 cites — an `AuthorizedExecutionV2` preflight with the
mandatory pre-execution sentence and declared-provenance disclosure, and a
`RepairApplyAuthorizationV1` bound to the exact `repairPlanId`, base snapshot and
project with `repositoryExecution` constant false: all schema-valid. A display
alias as `platformId` is refused by the schema; an over-claimed
`ENFORCED-PLATFORM:seatbelt` is schema-shaped but is **not equal** to the pinned
table and is refused at security admission — a distinction I record rather than
blur, because the schema alone does not decide it.

**Purge / replay / required-output failure** positions, kept distinct:
query of the retained manifest after purge is success 0; a query requiring
actual proof refuses `REQUEST.PRECONDITION_FAILED` (2) **before** evaluation
with `evidence.{expired,purged,missing,corrupt}`; inability **during** a
selected operation is `HOST.IO_FAILURE` (4); successfully admitted partial
native inputs seal an **authoritative** Run and terminate indeterminate (3); a
regeneration mismatch is `HOST.IO_FAILURE` (4) with
`evidence.regeneration-mismatch` and cannot replace the sealed Run;
`--ephemeral` against a baseline/repair prerequisite is
`REQUEST.UNSATISFIABLE` (2) with
`WORKFLOW.EPHEMERAL_CANNOT_SUPPLY_AUTHORITY`.

---

## 7. Negative controls and first refusal boundaries

29 negatives, all refused. Each is a **single-field** mutation of an otherwise
complete positive graph, so valid controls stay distinct from invalid mutations.
Where an earlier boundary masks a later hypothesised check I say so:

| vector | first observed refusal | masking |
|---|---|---|
| raw payload offered where an H identity is required | `FRAME[native-context]: FRAME_PREFIX` | masks the later domain-registry and record-validation checks |
| altered frame | `FRAME_DIGEST` | masks frame parsing and every downstream universe join |
| missing preimage | `MISSING_PREIMAGE` | masks all downstream context/universe joins |
| re-framed under an unregistered domain, Plan unchanged | `FRAME_DIGEST` | **masks** the unregistered-domain check — so I built a second vector that names the bogus-domain digest in the Plan, which reaches `UNREGISTERED_H_DOMAIN[native-context]: native.context.made-up.v9` |
| Rust `configProjectionSha256` mismatch | `MISSING_PREIMAGE[nested/configProjectionSha256]` | masks `native.universe-context-field-mismatch`, which the same run also reports |
| `file` payload digest wrong | `RELATION_SNAPSHOT_JOIN_DIGEST` | followed by `…_BYTES_NOT_RETAINED` |
| `declares@resolved-callee` | `RELATION_RUNG_NOT_ON_LADDER` | followed by `VIEW_FACT_HAS_NO_MATCHING_SCOPE` |
| stdlib inventory missing an **unselected** library | `native.native-context-stdlib-inventory-incomplete: lib.dom.d.ts` | fires once per context sharing the toolchain |

A refused hidden/mismatched input **per language**: TypeScript — context bytes
that are not the admitted ones (`altered-frame`) and a Plan that omits a
retained context (`PLAN_CONTEXT_SET_MISMATCH: retained=3 plan=2`); Rust — a
universe naming a context this Plan did not select
(`UNIVERSE_CONTEXT_NOT_PLAN_SELECTED`) and a projection-digest mismatch;
syntax — a hidden context and a `parserVersion` not from the grammar closure
manifest (`native.syntax-grammar-version-not-from-manifest`).

**Native dependency and configuration H preimages**, reconstructed from the
recipes and shown as exact bytes (all recompute; for all six the raw SHA-256 of
the canonical payload **differs** from the H identity, as the digest law
requires): `native.dependency-file-manifest.v1` (122 canonical bytes),
`native.unified-features.rust.v1` (219), `native.cargo-config-projection.v2`
(425), `native.dependency-source-set.v1` (722), `native.context.rust.v2` (1884),
`native.source-unit-ownership.v1` (2163). `CargoConfigProjectionV2` carries
**two non-interchangeable digests**: its own `projectionSha256` (raw digest of
the projected `.cargo/config.toml` **file bytes**) and the universe's
`configProjectionSha256` (the 64-hex suffix of the H over the whole record).

**Laws the contracts state about their own documents, independently checked.**
All hold: every one of the 58 annotated 64-hex fields in `identity-schemas.v2`
carries exactly one `x-opensip-digest`, with **zero** unannotated 64-hex fields,
every representation terminal or a registered `by-domain` selector, and every
reference-`domain` enum member registered; the `x-opensip-order` vocabulary is
closed across all 17 current schema documents (263 annotations, zero outside);
`relation-payload-schemas.v2`'s own digest law reaches every governed top-level
occurrence with one declared `not-joined` exemption
(`vcs-change.previousPath`); the ladder mirrors are equal **and in order**; the
matrix `cells` array is exactly the 11×6 = 66 product; and the published bound
arithmetic reproduces (93 TypeScript units at 1023 rows, 94 at 1034).

**The import mirror differential is proved, not asserted.** One instance
validated against **both** the foundation `identity-schemas.v2#/$defs/import`
and the workflow `imported-evidence#/$defs/ImportWrapperV2`, on exactly the
boundaries the contract says once disagreed: zero blobs, one blob, unsorted and
sorted `omissions`, an absolute blob path, a `..` blob path, 268 435 456 and
268 435 457 blob bytes, and 4097 blobs. **All eleven verdicts agree**, with six
discriminating negatives refused by both — so the check cannot pass by both
documents being permissive.

---

## 8. Findings

### MUST-1 — a TypeScript/JavaScript clone body-dialect refusal has no published Coverage classification (identity-affecting)

**Selectors.**
`foundation/identity-schemas.v2.json#/x-opensip-digest-domains/domainSets/native-semantic-universe/native.semantic-universe.typescript.v2/languageVersionBinding/dialect/onUnknown`
= `BODY_LANGUAGE_SOURCE_VARIANT_UNKNOWN`;
`docs/v2/contracts/product-v1/native-evidence.md` §10, "Clones ownership
disclosure is typed, not null (CB3-MUST-5)" and its closing paragraph "The
remaining selection-law refusals get no cause and that is deliberate:";
`native/native-evidence.schemas.v2.json#/$defs/NativeCause`;
`native/native-evidence.schemas.v2.json#/x-opensip-deficiency-cause-registry/deficiencies/input-closure-incomplete/allowedCauses`.

**What is missing.** §10 closes the clones-ownership disclosure for the three
Rust ownership states and then enumerates the refusals that deliberately get no
cause — `BODY_LANGUAGE_OWNER_NOT_COMPILED`, `BODY_LANGUAGE_OWNER_NOT_SELECTED`,
`BODY_LANGUAGE_DIALECT_ABSENT`, `BODY_LANGUAGE_DIALECT_AMBIGUOUS`. All four are
Rust. The TypeScript binding's own `onUnknown` refusal is named **nowhere in
any prose contract**: I grepped the whole kit and it occurs only at that one
registry line. So for a `clones@normalized-body-hash` subject-scope under a
TypeScript universe whose subject path has a suffix outside the closed
source-variant table, two conforming readings exist and no document selects
between them:

* §10's general sentence — "a clones scope which cannot determine a body dialect
  [must] mint no body identity, report the incompleteness in its Coverage, and
  leave the predicate and seal indeterminate" — makes a disclosure **owed**; but
  the only deficiency that could carry it, `input-closure-incomplete`, requires a
  `NativeCause` from a closed twelve-member list containing no variant-unknown
  member, and §10 states that a null cause "records that a disclosure was owed
  and not made rather than making it";
* the narrow reading treats it like `BODY_LANGUAGE_OWNER_NOT_COMPILED` —
  examined, correctly no fact, `complete` lawful.

**Measured.** A Run whose view carries a `clones@normalized-body-hash` scope over
the inventoried path `package.json` under the TypeScript universe, with
`coverage: complete`, `deficiency: null` and no fact, **closes**: 339 checks,
zero refusals, under a checker that implements every published law
(`output/vector-results.json#/typescriptVariantUnknownProbe`). The body-dialect
selector for that same path refuses `BODY_LANGUAGE_SOURCE_VARIANT_UNKNOWN`, so
no body identity is representable for the subject the scope claims to have
examined completely.

**Why MUST.** The Coverage record reaches `coverage2` → `view2` → `evidence2` →
`seal2` → `run2`. Two conforming hosts therefore mint different RunIds for the
same repository and the same question, which defeats independent replay across
machines. This is the same determinacy-gap class the design already calls a
defect in its own words for RC-1's `unresolved-edge@observed` ("a determinacy
gap in the contract"), for the `capabilityId` vocabulary, and for the config
node-kind law — each of which was closed.

**Not a gap for the other two universes, and I verified that.** Under the syntax
universe the grammar-capability guard fires first at both boundaries — a scope
naming a path no selected grammar reads is unavailable, and a fact anchored
there refuses `SYNTAX_CAPABILITY_UNSUPPORTED_FACT` — so
`BODY_LANGUAGE_GRAMMAR_VARIANT_UNKNOWN` is defensive only. Under the Rust
universe the ownership law is total. The guard is explicitly
"syntax-universe specific" and nothing plays that role for TypeScript.

**What would close it.** One sentence in §10 assigning the TypeScript (and, for
symmetry, syntax) `onUnknown` refusal to one of the two existing classes — either
"compatible with `coverage: complete`" alongside `OWNER_NOT_COMPILED`, or a
disclosure with a named `NativeCause` member. I do **not** propose which; both
are defensible and the choice is the owner's.

### SHOULD-1 — the mandated per-requirement cause carrier cannot express 11 of 16 producible outcomes

**Selectors.** `docs/v2/contracts/product-v1/workflows-and-surfaces.md` §6,
"the exact cause is carried into that requirement's unmet precondition so two
different causes are two different remedies";
`workflows/schemas/repair.schema.json#/$defs/RepairPlanDescriptor/properties/unmetPreconditions`
(items are `common#/$defs/DomainDetail`, whose `code` is the closed
`DomainDetailCode`); `common#/$defs/NativeSufficiencyDeficiency` (9 members);
`common#/$defs/ImportedRequirementDeficiency` (7 members).

**Measured.** Only **5 of 16** producible per-requirement outcomes are members of
`DomainDetailCode`: `input-closure-incomplete`, `budget-exhausted`,
`derivation-policy-unmet`, `resolution-incomplete`,
`external-consumers-unknown`. Not members: the four native
`language-tier-unsupported`, `provider-unavailable`, `confidence-floor-unmet`,
`required-relation-missing`, and **all seven** imported outcomes
(`evidence-kind-unavailable`, `import-unmapped-only`, `subject-not-observable`,
`history-outside-collection-scope`, `observation-window-insufficient`,
`history-range-insufficient`, `import-absent-for-requirement`). No generic
"evidence requirement unsatisfied" code is registered; the nearest,
`REPAIR.CLOSED_WORLD_NOT_ESTABLISHED`, names a different condition and using it
would collapse two causes into one remedy, which the same sentence forbids.
Registering a new code is forbidden by workflows §12 ("an unknown detail refuses
admission"). My projection therefore emits the cause where it is expressible and
records the gap otherwise; a `history-range-insufficient` requirement produces
an unmet-precondition entry that cannot be written.

**Why SHOULD and not MUST.** `unmetPreconditions` is in the `repairPlanId`
preimage, so the under-determination does move that identity — but `repair
preview` is a Query-class step that mints no Run, `applicable` is false by
construction in exactly these cases, no authorization is issued for an
inapplicable plan, and the exact cause is retained in the same descriptor at
`evidenceRequirements[].deficiency`. Nothing is lost from the retained record;
only the public unmet-precondition projection is under-determined.

### SHOULD-2 — reachable Plan cardinality boundaries with no published typed refusal

**Selectors.** `identity-schemas.v2.json#/$defs/plan/properties/nativeContextDigests`
(`maxItems: 128`), `…/semanticClosures` (128), `…/importIds` (256), against
`docs/v2/contracts/product-v1/native-evidence.md` §14, which publishes the typed
`PROJECT.SCOPE_LIMIT` / `REQUEST.UNSATISFIABLE` (exit 2) refusal with subject
`field:count>limit` for exactly **four** bounded selection arrays across
**two** record families — and states that "a `maxItems` breach is reported
generically, restating the entire instance and naming no field, count or limit;
an oversized ordinary selection is not a malformed record and is not published
as one".

**Measured reachability.** 129 distinct TypeScript units with an explicit
`analysis.capabilities: ["inventory"]` override give 129 `requestedCapabilities`
rows (bound 1024, admitted) and 129 `workspaceRoots` (bound 1024, admitted) but
**129 distinct native contexts** against a Plan bound of 128 — and §14 itself
calls units 94…1024 "ordinary repositories the scope law admits". Separately,
the resolved semantic configuration admits up to **1024** already-imported
`import2` IDs (`semantic-configuration.evidence.importIds`) while
`plan.importIds` binds at most **256**. I confirmed the overflow projection is
exactly the generic fault §14 rejects: the JSON Schema error restates the entire
129-element array and names no field, count or limit.

**What would close it.** Either extend §14's accounting to the `plan` record
family under the same code and law (its own rationale — "the remedy class is
identical: narrow the selection explicitly, nothing was truncated" — applies
unchanged), or state that these three bounds are unreachable and why. Today an
implementer must choose between widening a closed accounting the contract states
as exact and emitting the projection the contract rejects.

### Advisories (non-blocking)

* **A-1 — the D9 successor artifact is a live, disclosed obligation.** Confirmed
  by measurement: `d9-exit-contract.v1.14.json` contains no `host-invariant`
  cause, so a checker reading it alone refuses a lawful `host-invariant`
  operational-failed termination. The contract discloses this precisely, names
  the owner and forbids repinning the historical bytes. Nothing was left for me
  to invent.
* **A-2 — the matrix-fixed default cannot express 94…1024-unit TypeScript
  repositories.** 94 × 11 = 1034 > 1024. Disclosed with a typed refusal and an
  explicit remedy; a real product limitation, not a design gap.
* **A-3 — `PLATFORM-ID-DOMAIN-V1` is broader than the product promise.** Eight
  encoding members including two Windows ids and `linux-x86_64-musl`, against
  four selected machine platform ids. The successor registry discloses this and
  says why it is not narrowed. Confirmed: no product surface reads it as a
  support claim, and `RepoExecutionGrantV2.platformId` is closed to the four.
* **A-4 — `PROTOCOL3_RULES` is named, not published.** Native §9.2 gives 22
  phases and the reject-before-disclosure ordering, but the "34-rule
  first-match/total-fallback table" exists only as a named identifier in an
  excluded model file. It blocked no vector here (it is a first-party host↔
  provider wire concern, outside descriptor closure), but an implementer of a
  conforming provider would be reading code rather than a contract. I cannot
  distinguish "the table is in the excluded file" from "no normative table is
  published"; I flag the selector rather than assume either.
* **A-5 — `UNICODE_CASE_DATA_VERSION` is a prose constant.** Native §2.4 binds
  `fold` to UCD 15.0.0 and names the model constant. I implemented the fold as
  the full non-tailored default lowercase mapping and note the bounded
  limitation honestly: every `lib` name in the current option vocabulary is
  ASCII, where the three candidate operations coincide, so my vectors do not
  discriminate `U+0130`, `Final_Sigma` or `U+00DF`. The contract states this
  limitation itself.

---

## 9. What I had to decide, and what I did not have to invent

**Algorithm freedom explicitly left to implementation** (correctly, and I did
not treat it as a gap): query planning; the L1–L3 tokenisers (the design
explicitly qualifies no normalizer and requires only retained-preimage custody
and framing); enumerator strategy; the symbol-to-file attribution, which is a
*stated trust boundary* rather than an omission; and the internal diagnostic
record behind an absent public `domainDetail`.

**Choices I had to make and record** (none of which is a missing contract):
the synthetic level-specification bytes and their digests; my synthetic trusted
observations (dependency manifests, toolchain/stdlib/grammar trees, ownership
enumeration); the subject-id spellings; and — for the two SHOULDs and the MUST —
the reading I proceeded under, stated at each finding.

**Nothing forced me to invent a semantic recipe.** Every identity, preimage,
join, gate and refusal I needed was published. That is the strongest positive
result of this pass, and it is why the verdict turns on three narrow gaps rather
than on reconstructability.

---

## 10. Limitations of this review

* My closure checker is my own code written from prose. A defect in it is mine,
  not the design's. Where my helper had a bug I corrected it from the normative
  kit and kept both states: I initially omitted `languageId` from the derived
  `body-language-version` record (three schema refusals across RUN-TS), and I
  initially had no clones-ownership disclosure prerequisite at all, so the
  ambiguous-selection Run closed with 0 errors until I derived and added the
  law — the same class of "a law nothing compares" the contract itself names.
  Both corrections came from the kit and both are preserved in the record.
* Schema validation, helper predicates, full retained closure and future host
  enforcement are four different things and I keep them apart. Everything here
  is the first three. **Nothing here is host enforcement**: every OS, compiler,
  crypto, SQLite, filesystem, custody, revocation and confinement observation in
  my vectors is a **synthetic TCB assumption**, never native enforcement proof.
* My positive Runs use synthetic trusted observations for provider output. They
  demonstrate that the descriptor graphs are constructible and that the retained
  closure admits them; they qualify no provider, no compiler, no grammar, no
  normalizer and no platform.
* I did not reconstruct the trust-time (S4/S4.5), root-chain (S5), revocation
  (S6), lease (S7), migration (S9) or installation-journal (S9.2) state
  machines beyond reading them; they were outside the reconstruction asked for
  and no vector depends on them.
* No claim of product qualification and no implementation authorization is made
  or implied. Real measurements on the four selected platforms remain future
  qualification work under the named gates.

---

## 11. Verdict

**CHANGES_REQUIRED.**

The design is reconstructable to a very high degree. From these 45 files alone I
built and closed eight complete Run descriptor graphs across the TypeScript,
Rust and syntax-only universes, with 1974 executed closure checks and zero
failures under a from-scratch reload; I reproduced every identity recipe,
admitted the capability manifest through all four inherited gates with eleven
single-gate negatives, and refused 29 independent negative vectors each at a
named boundary. The hard cases the contracts spent most of their text on — the
frame-versus-payload law, the cross-universe totality discharge, the partition
key, the Rust compilation-target dialect selection with its selection/enumeration
distinction, the grammar-versus-compiler body identity, the syntax capability
guard and the deficiency/cause carriers — all reconstruct exactly and all
behave as specified under adversarial construction.

It is not accepting, because one identity-affecting determinacy gap remains
(MUST-1: a TypeScript clone scope over an unlisted suffix has two conforming
Coverage readings and therefore two RunIds), and two public-contract gaps remain
(SHOULD-1: a mandated disclosure carrier that cannot express 11 of 16 producible
values; SHOULD-2: reachable Plan cardinality boundaries with no published typed
refusal). Each is narrow, each has an exact selector, and each is the same class
of defect the design has already closed elsewhere in its own words — which is
why I am confident they are oversights rather than deliberate silences, and why
closing them looks like a small edit rather than a redesign.

---

### Reproducing this review

```
cd /tmp/opensip-design-corrections/consumer-b.v7/output/work
/tmp/opensip-architecture-review-env/bin/python -I -B run_all.py   # build + measure
/tmp/opensip-architecture-review-env/bin/python -I -B verify.py    # from-scratch closure
```

Artifacts: `output/vector-results.json` (every vector and measured result),
`output/verify-report.json`, `output/vectors/<run>.objects.json` (typed
identity → domain + descriptor + recomputed H), `output/vectors/<run>.blobs.json`
(every exact blob and H-frame byte, base64, keyed by digest),
`output/work/*.py` (the independent reference code).
