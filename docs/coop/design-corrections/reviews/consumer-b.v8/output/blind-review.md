# OpenSIP DR-011-R10 — blind consumer-B reconstruction

**Verdict: CHANGES_REQUIRED.**

Two MUST-level and three SHOULD-level design gaps remain, each established by a
constructed and executed vector rather than by argument. Everything else in the
scope I was asked to reconstruct was reconstructable from the kit alone: I built
sixteen complete positive Run descriptor graphs across all six advertised
language modes and all three native universes, validated every record against its
owning normative schema, independently implemented the retained closure and the
cross-record joins, and re-verified every graph from a base64 export alone. No
author model, fixture, golden, report or prior review was read.

This is a disposable design-reference exercise. It is not product qualification,
not a readiness grade, and not implementation authorization.

---

## 1. Input custody

All **46** manifest files verify byte-exact (SHA-256 and byte length), with no
unlisted file on disk. Reproduce with
`/tmp/opensip-architecture-review-env/bin/python -I -B output/work/verify_manifest.py`.

One custody limitation, recorded rather than treated as a defect: the manifest
asserts `parentSubjectSha256 =
312db9d904d0ec1f9c91d84137feb3277490b79b07bf3a6d5efc0380caa0f24b` for a parent
subject of which this kit is a declared **subset**. That aggregate is not
recomputable from these bytes, so I verified the 46 members and treat the parent
digest as an unverified assertion of custody.

The index's distinction held throughout: the five contracts' retained/superseded
selector tables and their normative registries were sufficient, and no
readiness/review record was needed to construct any semantic recipe. Historical
narrative inside inherited normative documents (the CB3/CB4/PR/N-item prose) was
read as provenance only; no link to a review, model or fixture was followed.

---

## 2. What I executed

`sh output/run-all.sh` — 249 PASS assertions, 0 FAIL, exit 0.

| Layer | Executed |
|---|---|
| canonical encoder `C`, `H` framing, lexical/raw admission, CVE1 | own implementation from prose |
| capability-manifest admission (ADM-TYPE/CLOSED/DOMAIN/ORDER) | own implementation, 20 vectors |
| retained Run closure (schema + identity + every cross-record join) | own implementation, 4551 checks |
| provider protocol major 3 state machine | own implementation from the published table, 17 traces |
| workflow/public surfaces (invocation, availability, D9, envelopes) | own derivations, 53 assertions |
| baseline/comparison/repair/authorization/purge/replay | own derivations, 71 assertions |

**Sixteen complete positive Runs**, each closed by my checker and then
**re-verified from the base64 export alone**:

| Run | RunId | checks | objects |
|---|---|---|---|
| ordinary TypeScript project (node_modules, bare specifiers, retained config graph, JS clone body through the TS engine) | `run2:9be89fbe…` | 408 | 96 |
| Rust mixed-edition workspace, selection = lib | `run2:9a10e422…` | 346 | 99 |
| same physical file, selection = test target at edition 2024 | `run2:076d8a99…` | 346 | 99 |
| selection widened without changing the effective dialect | `run2:523ced33…` | 347 | 99 |
| ambiguous selected owners (disclosed pair, no body) | `run2:4a8e00e7…` | 330 | 95 |
| partial enumeration (empty clone view, disclosed pair) | `run2:e03ce05f…` | 329 | 95 |
| no committed ownership (no clone admissible) | `run2:99fd19ca…` | 316 | 95 |
| `rust-cargo-prepared`, inert `PreparedOutputSetV3`, `prepare-code` projection | `run2:1a0b85b1…` | 349 | 105 |
| `imported-inert` (projects only `read-import`) | `run2:b38b2d3c…` | 349 | 104 |
| compiler-free grammar-only repository (no TS and no Rust unit) | `run2:fc2db1d1…` | 308 | 76 |
| data/document-only repository (inventory complete, code capabilities unavailable) | `run2:673cc195…` | 242 | 65 |
| synthesized TypeScript configuration | `run2:b788ee3c…` | 171 | 53 |
| custom-named config, ordered bases incl. a repeated base | `run2:52a601d0…` | 190 | 59 |
| jsconfig inheriting a shared base of another filename | `run2:36798a5d…` | 176 | 56 |
| a TRUE predicate emitting a finding, verdict `fail` | `run2:7a8e9501…` | 172 | 60 |
| a Run with an admitted registered runtime `import2` | `run2:1e9dcf54…` | 172 | 66 |

Retained: `object-table.json` (typed identity, domain, kind and descriptor for all
699 distinct objects), `blobs.b64.json` (the exact bytes of every blob and every H
preimage frame, keyed by raw SHA-256), and `run-all.sh` as the from-scratch
command. `export.py` rebuilds each store **from the base64 alone**, re-hashes
every CAS key and re-closes every Run: 16/16, 0 failures.

---

## 3. The reconstructed pipeline, and who owns each decision

**Zero-config discovery → typed config/source.** Security S3 owns the authority
boundary: custody over O_NOFOLLOW handles, the ancestor walk, the nested-config
boundary (ADV-3), and the `AdmittedBoundaryInventoryV1` it exports. Native §1.4
U-1…U-8 owns language-unit existence *inside* that boundary and consumes the
inventory unchanged; the shared rule (`discovery-defaults.py`) is the single
source of pruning-by-segment, the 4096 first-party cap and the `.` root sentinel.
Admission §1.1 owns Config2 layering and the resolved semantic configuration.
The split is decidable: an explicit root without a language marker is *admitted
for custody by security* (warning `EXPLICIT_ROOT_WITHOUT_LANGUAGE_MARKER`) and
*refused by native* (`CONFIG.INVALID` / `native.explicit-root-without-marker`).

**Invocation / step / attempt lifecycle.** Workflows §1 owns it. `RequestId` is
minted before admission and retained for refusal; each admitted attempt gets a
fresh `ExecutionId`; `StepId` is the zero-based DAG position; at most 64 steps
and 3 attempts. I validated both the single-step `default` invocation record and
the named multi-step `audit` invocation (analysis, pivot analysis, comparison,
render) against `invocation-record.schema.json`. The successor `ExecutionId`
grammar is end-anchored `(?![\s\S])`; the C-2 `planIntent.wireTypes.executionId`
bare `$` is retained provenance and is *not* an alternative admission boundary —
I confirmed the successor pattern in `common.schema.json` and in
`identity-schemas.v2.json#/$defs/commit-receipt/properties/executionId`.

**Semantic identity vs operational authority.** The line is sharp and I exercised
it: `RequestId`/`ExecutionId`/receipts/`authorizationRef`/`securityGrantSetRef`
are operational and enter no content identity; the Plan binds only the
*semantic-grant projection*. My `rust-cargo-prepared` Run projects
`trusted-repository-code` + `prepare-code` from a consumed preparation grant,
while the `imported-inert` Run projects only `read-import` — and a
`trusted-repository-code` principal offered under `imported-inert` refuses
(`GRANT_PREPARE_CODE_PRINCIPAL_JOIN`). Prepared bytes in custody never imply an
execution grant.

**Mutation vs analysis steps.** `analysis` and `verify` seal or link a
content-derived `run2`; the other eleven step kinds never mint one. Generic
mutation replay is `H("workflow.mutation-intent", MutationReplayScopeV1)` over
`{schemaVersion,requestId,stepId,projectId,operation}` — request-scoped, so two
fresh requests never deduplicate (measured: two distinct keys). `repair-apply` is
the content-derived exception, `raw SHA-256 of C({operation, projectId,
repairPlanId, baseSnapshotId})`, and is refused by an explicit `not` in **both**
generic fields. `import` and `native-preparation` share the H recipe but not the
lookup meaning (delivery-only / not replay).

**Plan → native facts / Coverage / view → proof → Evidence → Seal → Run.** I
re-derived the whole graph and its acyclicity: proof carries no evidence, seal or
run reference (checked by byte search over `C(proof)`); evidence may carry proof;
seal carries both; Run carries seal. Every identity is recomputed, never trusted.

**Durable receipt and current availability.** Reconstructed from identity §5 and
validated as records: `commit-receipt` + `commit-inventory` (operational custody,
excluded from semantic IDs) and the separate monotonic-generation `availability`
record with its six states. Sealed assurance and historical verdict never change;
availability may improve. A regeneration mismatch is
`HOST.IO_FAILURE`/`host-io`/`evidence.regeneration-mismatch` (exit 4) and cannot
replace the sealed Run — validated as a `StepTermination`.

**Provider sequencing and state law, derived independently.** I implemented the
22 phases, 34 rows, the two wildcards, the pre-match order, the guard-equality
law, the state updates, the `ANALYZING_OR_READY_COMPLETE` stage-dependent
transition and the terminal law from `protocol3-transitions.v1.json` and §9, and
asserted the published pairwise-disjointness claim rather than assuming it
(it holds). Traces executed:

* complete Rust exchange in dependency mode, prepared mode, and neither;
* **identity negotiation before source disclosure**: `OpenUniverse` before Hello
  faults with `sourceBytesSent=false`, and a `HelloAck` missing one identity
  token leaves `identityNegotiated=false` so `OpenUniverse` is unreachable and no
  source byte is sent;
* unavailable before Analyze and during Analyze; `BudgetExhausted`;
* cancellation (`Cancel`→`Cancelled`→terminal, then still `zero-exit`/`eof`);
* `ProviderFault`; out-of-band process fault from any phase; crash mid-stage;
* **terminal process handling**: a post-terminal frame between the terminal and
  `zero-exit` faults, a process fault after a clean terminal is still a fault,
  and `FAULT` absorbs everything after it;
* multi-stage: one `CoverageV3` per stage, only the last may be followed by
  `Complete`; an early `Complete` matches no row (`P3-34`).

Terminal-kind → authority (prose-owned, §10): a fault contributes **no** facts,
Coverage or Run (`operational-failed` 4 / `PROVIDER.PROTOCOL_VIOLATION`);
cancellation is `interrupted` 130 with the same no-facts rule; `unavailable` and
`budget-exhausted` are clean typed terminals whose prior facts are admitted, the
Run is authoritative and the stage is `partial`.

**Executed vs assumed.** Every trace above and every closure result is *executed*
in my reconstruction over synthetic inputs. What is *assumed about a future host*:
that a real worker emits these frames in this order; that OS process exit/EOF,
`fsync`, SQLite, flock, ACL/O_NOFOLLOW custody, signature verification and
cancellation bounds behave as the contracts require; and that a real compiler,
Cargo, grammar bundle or coverage tool produces the observations I supplied. No
compiler, cargo, provider, repository, filesystem, crypto or network operation
ran anywhere in this work.

---

## 4. Capability-manifest admission before encoding

The effective registry is selected **by name** by identity §3 and listed again by
native §11: `native/capability-manifest-domains.v2.json`. I built my own CVE1
encoder and decoder and my own gate implementation from the prose, then my own
minimal descriptor vectors.

Positive manifest → `capabilityManifestId =
950b823df11bfd667f443303d966644187e06bc83c16f96eb6d42310ed534227`, and
`admit_committed` round-trips the committed bytes.

| Vector | Gate | First observed refusal |
|---|---|---|
| `schemaVersion: true` | ADM-TYPE | not a JSON integer |
| `schemaVersion: "1"` | ADM-TYPE | not a JSON integer |
| undeclared key on `ProviderCapability` | ADM-CLOSED | key set ≠ declared |
| missing `deficiency` on `AbsentCapability` | ADM-CLOSED | key set ≠ declared |
| `declares: resolved-callee` | ADM-DOMAIN | rung of another relation's ladder |
| unregistered relation key | ADM-DOMAIN | not in `RELATION-DOMAIN-V2` |
| `LINUX-X86_64-GNU` | ADM-DOMAIN | exact NFC bytes, no case folding |
| unsorted `relationIds` | ADM-ORDER | not strictly ascending |
| unsorted `providers` | ADM-ORDER | not strictly ascending by `providerId` |
| duplicate `platformId` | ADM-ORDER | a duplicate is an ordering violation |

**Gate order is load-bearing and I measured the masking**: a manifest that
violates ADM-TYPE *and* ADM-ORDER at once reports ADM-TYPE; the ADM-ORDER
violation on `coverageForAbsent[0].relationIds` is never reached. The declared
`traversalOrder` is what makes "the first violation" reproducible, and I publish
the complete violation list per vector so nothing depends on it.

**`unresolved-edge` is genuinely outside the inherited twelve**: a manifest
without it mints `b1e6ef03…`, with it mints `950b823d…`, and the string is not a
member of `RELATION-DOMAIN-V2.inheritedMembers`.

**Raw-input admission is exercised separately from encoding a parsed object.**
`admit_committed` decodes *bytes*: trailing byte, unknown tag, non-NFC text,
duplicate map key and unsorted map keys each refuse at the decoder, before any
gate. Independently, `admit_raw` over raw JSON bytes refuses duplicate keys,
`1.0`, `1e0`, `-0`, `NaN`, a lone-surrogate escape, `01`, an over-range integer,
malformed UTF-8 and depth 33 (depth 32 admits). And the codec separation holds:
CVE1 **refuses** a non-NFC string, while `C` admits the same string unchanged
(`{"k":"e\xcc\x81"}`) — CVE1's NFC rule applies to the capability manifest only.

**Semantic vs operational change.** Any semantic field change moves the identity;
`RequestId`, `ExecutionId`, receipts, wall clocks and authorization references
appear in no descriptor I hashed. Measured instances: dropping a repeated
`extends` base moves `tsconfigGraphHash` and therefore the universe
(`cee6f8a4…` → `686d543f…`); changing only the bound `ScopeDocumentV1` moves
`analysisSpecDigest`, `PlanId` and `RunId` while `plan.scopeDigest` and the
snapshot are byte-identical.

---

## 5. Native evidence: the discriminating vectors

### 5.1 TypeScript (`js-allowjs`, the ordinary project)

`node_modules` is pruned by segment, so `ResolvedNodeModulesLayoutV1` is a
retained *resolution read-set observation* joined by digest, not a snapshot
inventory row; `nodeModulesInReadSet` is exactly `nodeModulesLayoutDigest is not
null`. Bare specifiers therefore resolve. The retained `TypeScriptConfigGraphV1`
drives `configOrigin` by derivation, and node `kind` is a total function of the
basename under the published law.

**Body language is the BODY's, not the provider's.** `src/a.ts` and `src/util.js`
carry byte-identical body spans. Under one TypeScript **engine** universe they
mint different `bodyIdentity` values because the derived `body-language-version`
differs only in `languageId`/`dialect`:

```
ts  {"compilerBuild":"def966b8…","compilerName":"typescript","compilerVersion":"5.6.3",
     "dialect":{"sourceVariant":"ts"},"languageId":"typescript","schemaVersion":1}
     -> sha256:d205afac9672af96de9e3023df7e136f4451ab1194d732d15eaeae46498e5d54
js  {…,"dialect":{"sourceVariant":"js"},"languageId":"javascript",…}
     -> sha256:0d7220bc3d5cda99fca58009b7b640ea572c612c5e8f542f85f3fbe06d97a96d
```

An L1-lexical identity over the same `.ts` body is a third value
(`sha256:c8f88612…`). I recomputed the L0 payload framing independently and it
agrees with the worked example in identity §3: a 4-byte span `a=1\n` gives an L0
payload `00000004 613d310a` (8 bytes), contributing the final frame component
`00000008 00000004 613d310a` (12 bytes) — the payload is length-prefixed twice.

Custody negatives, each with its first observed refusal:
`normalisationVersion` drifting from the framed `levelVersion`
(`BODY_FRAME_LEVEL_VERSION`); level-specification bytes not retained
(`EVIDENCE_UNAVAILABLE`); a `.js` body framed with the provider's language
(`BODY_FRAME_LANGUAGE_ID`, "typescript vs derived javascript"); an L0 payload that
is not the enclosing fact's anchor span (`BODY_L0_PAYLOAD_NOT_ANCHOR_SPAN`).

File-fact inventory joins: wrong content hash (`SNAPSHOT_JOIN_DIGEST`), wrong byte
length (`SNAPSHOT_JOIN_LENGTH`), path in no snapshot
(`SNAPSHOT_JOIN_PATH_NOT_INVENTORIED`). Anchor law: an inventory fact carrying an
anchor, an unanchored `declares` fact **under a TypeScript universe**, and a
two-anchor `clones` fact all refuse `FACT_ANCHOR_CARDINALITY`.

Context/universe negatives: relabelled config-node kind
(`native.config-graph-kind-contradicts-path`); stdlib inventory missing an
**unselected** declaration library
(`native.native-context-stdlib-inventory-incomplete`); compiler version not the
admitted manifest's; a tool digest outside the named closure tree; a universe
contradicting its admitted context. Frame negatives: an altered frame that still
parses and is still canonical (`H_IDENTITY_MISMATCH`); a missing preimage
(`EVIDENCE_UNAVAILABLE`); a raw canonical payload offered where a frame is
required (`FRAME_PREFIX`); a **fully re-framed and re-keyed** Run built around a
context under an unregistered H domain (`H_DOMAIN_UNREGISTERED`); a hidden
hash-valid context no Plan selected (`PLAN_CONTEXT_SET_MISMATCH`).

### 5.2 Configuration variants

Synthesized (`entryConfigPath: null`, empty nodes, `synthesizerVersion 1`);
an explicitly selected **custom-named** config `configs/app.build.json` whose
entry `kind` is `other` and which still derives `configOrigin: tsconfig`,
inheriting from three ordered bases **including a repeated one** whose precedence
is retained in `extendsResolved` — dropping the repeat moves the graph hash and
the universe; and a **jsconfig** inheriting `base.settings.json` (entry kind
`jsconfig` → `configOrigin: jsconfig`; the base's kind is `other`). Negatives:
relabelling the custom entry as `tsconfig`, and a jsconfig entry asserting
`configOrigin: tsconfig` (`native.universe-config-origin-not-derived`).

### 5.3 Rust

Mixed-edition workspace with a **target-specific edition differing from its
package default** (`cb-core` package edition 2021, test target `shared_it`
`targetEdition 2024`), a valid `#` marker directory
(`crates/tools#gen/Cargo.toml`), a 21-entry edition map (438 raw bytes — which is
why the map is hashed, not embedded in a `u8`-framed component), and the nested
`DependencySourceSetV1` / `DependencyFileManifestV1` / `UnifiedFeaturesV1` /
`CargoConfigProjectionV2` / `SourceUnitOwnershipV1` records retained and joined.

**The same physical file under two selections:** `crates/core/src/shared.rs`
under `selectedUnitIds=[lib]` yields `{edition: 2021}` →
`sha256:4f002643…`; under `selectedUnitIds=[test]` yields `{edition: 2024}` →
`sha256:ef50d75f…`. Two analyses, not two readings of one.

**Stability under a selection-only change:** widening the selection to
`[lib, bin]` changes the `sourceUniverse` (the selection is inside the record
whose identity the universe names) but the body identity is **unchanged**
(`4f002643…`), because `body-language-version` carries the selected value, never
the selection.

**Ownership disclosure, derived and re-derived.** For an ambiguous selection,
partial enumeration and absent ownership, the owed
`(deficiency, nativeCause)` pair is derived from the committed ownership record
and this scope's subjects, in the selection law's own order, and re-derived at
closure. All four refusals are separable and measured: false `complete`
(`COVERAGE_DIALECT_PREREQUISITE`), undisclosed null deficiency (`…_UNDISCLOSED`),
wrong deficiency (`…_DEFICIENCY_MISMATCH`), wrong cause (`…_CAUSE_MISMATCH`).
**Enumeration completeness is not resolution completeness**: the partial case
mints no body identity, its Coverage carries the incompleteness, and no resolved
rung is invented for the file facts.

Native H preimages recomputed from the published recipes: the
`DependencySourceSetV1` and `UnifiedFeaturesV1` frames re-hash to their
identities; the `DependencyFileManifestV1` bare-hex identity re-derives; the
**three** cargo-config digests are pairwise distinct — `projectionSha256` (raw
SHA-256 of the projected `.cargo/config.toml` **file**),
`configProjectionSha256` (64-hex suffix of
`H("native.cargo-config-projection.v2", record)`) and the raw SHA-256 of the
canonical record, **which is neither**. `unitId` re-derives from the published
four-field `UnitIdentityV1` preimage, and the `#` marker directory closes a
complete Run.

Rust negatives: a cfg set dropping a base cfg; a crate root outside the snapshot;
dependency member bytes not retained; a hidden Rust context; and a retained
`DependencySourceSetV1` frame edited under its own identity
(`H_IDENTITY_MISMATCH`).

*Honest note on masking:* dropping the vendored dependency member's bytes reports
`EVIDENCE_UNAVAILABLE` naming the **snapshot source blob**, because the one
content-addressed store is keyed by raw SHA-256 and the vendored member and the
snapshot file are byte-identical. The snapshot-inventory custody check is reached
first and masks the dependency-file-manifest `blobJoin`, which would have
produced the same code.

### 5.4 `rust-cargo-prepared`

An admitted `PreparedOutputSetV3` of **inert rows only** (`build-script-directives`
and `generated-file`), `preparedResolution: host-prepared`,
`executionCapableResolution: true`, and the `prepare-code` semantic-grant
projection with a `trusted-repository-code` principal whose `ownerSourceDigest`
names a retained `owner-source-set`. A `proc-macro-dylib` row relabelled with an
inert media type refuses `native.prepared-output-not-inert` **regardless of the
media type it claims** — kind decides. The `imported-inert` Run projects only
`read-import`, and a repository-code principal under it refuses.

### 5.5 Compiler-free syntax-only

A repository with **no TypeScript and no Rust compilation unit**: `scripts/tool.js`
(code grammar), `docs/notes.md` and `data/config.yaml` (data-document grammars),
and `tool/main.py` (no bundled grammar). The bundle carries all seven bundled
languages; the universe **selects** three.

* Inventory capabilities are never grammar-gated: `tool/main.py` gets an admitted
  `file@enumerated` fact under the syntax universe, and the `file@enumerated`
  Coverage is genuinely `complete`.
* The code grammar produces `declares@syntactic` and a `clones` body identity
  whose `body-language-version` is bound to the **grammar bundle**, not a
  compiler: `{"compilerName":"opensip-grammars","compilerVersion":"0.9.0",
  "compilerBuild":"62a22a87…","dialect":{"grammarVariant":"js"},
  "languageId":"javascript"}`. A grammar parse therefore never mints the same
  identity as a compiler parse over the same bytes — required, not incidental.
* A data-document path bears no body: a `clones` scope over `docs/notes.md` is
  `unknown` / `language-tier-unsupported` / `capability-missing`, and a false
  `complete` refuses at the **producer** boundary
  (`COVERAGE_SOURCE_VARIANT_UNSUPPORTED_SCOPE`) before the grammar guard, exactly
  as `scopeCapabilityLaw.guardOrder` says.
* **A complete empty result does not conceal unsupported analysis**: over the
  data-only repository, a `complete` empty `declares` Coverage refuses
  `SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE`.
* Semantic capabilities are correctly unavailable: `references@resolved-binding`
  under the syntax universe carries `coverage: unknown`,
  `resolutionCompleteness.state: not-attempted`, `language-tier-unsupported` /
  `capability-missing`; a false `complete` refuses.
* A Markdown-anchored code fact refuses (`SYNTAX_CAPABILITY_UNSUPPORTED_FACT`);
  a data grammar declaring `syntaxClass: code` refuses at bundle admission; a
  `parserVersion` not from the grammar closure manifest refuses; selecting a
  grammar the bundle lacks refuses (`native.syntax-grammar-not-in-bundle`); and
  an **unselected** code grammar lends no capability, so a `.js` clone fact
  refuses when only data grammars are selected.

I verified the code-versus-data distinction against the published matrix and the
body/normalizer laws rather than assuming it: the registry's `code` set is exactly
`{rust, typescript, javascript}`, those three and only those are members of the
`body-language-version.languageId` enum, no data suffix appears in the syntax
dialect table, and `.py` is `unsupported-file` / `no-bundled-grammar`.

**Every advertised mode has a representable analysis path.** All six:
`ts-tsconfig`, `js-allowjs`, `js-synthesized`, `rust-cargo`,
`rust-cargo-prepared`, `syntax-only` — each in a Run that closes.

### 5.6 The registered relation/rung applicability table

Derived from the single ladder authority and applied to retained scopes and
Coverage **even where no fact is present**:

* **17** registered `(relation, rung)` pairs over a **15**-token flat rung
  vocabulary — schema vocabulary is not relation membership.
* **5** resolved rungs (`imports@resolved-target`, `references@resolved-binding`,
  `calls@resolved-callee`, `types@checked`, `reachability@from-resolved-calls`);
  the other **12** are `not-applicable` with `attempted=false`, count 0 and empty
  classes. `reachability` is one-rung and *is* resolved — ladder length is not the
  rule. `unresolved-edge@observed` is one-rung and is *not* resolved.
* Only `file@enumerated` carries a `coverageTotality` row; a `complete`
  `file@enumerated` Coverage omitting an inventoried subject refuses
  (`COVERAGE_INVENTORY_TOTALITY_OMITS_PATH`).
* Anchor classes: inventory = exactly 0 (three relations), body-identity =
  exactly 1 (`clones`), source-text ≥ 1 (nine relations).
* Only `file`, `package` and `vcs-change` bind a snapshot join.
* Disjointness is decided per view over the full owning tuple: two `clones`
  scopes sharing the partition key and a subject refuse
  (`SUBJECT_SCOPE_PARTITION_OVERLAP`).

RC-0/RC-1/RC-2 and the deficiency/cause registry are applied at both boundaries.
A fact-free entry over an empty scope is judged the same way.

### 5.7 Findings, imports, and the citation closure

A TRUE predicate emits a finding; the Run seals `fail`. `finding-key2` and
`finding2` re-derive; `finding-parameters.messageCode` must equal the finding's;
the rule closure must be of kind `detector`. The **discriminator** is the raw
SHA-256 of the canonical JSON *ordered* string array of declaration-signature
tokens in grammar order (`9d39092d…`). Citations cannot introduce extra
authoritative input roots: a finding citing a fact outside the evaluated view
refuses, as does one citing a raw blob that is not an explicit blob input.

The `import2` Run carries an actual registered `RuntimePayloadV1` selected through
the closed payload-registry row. Negatives: an unregistered payload schema digest;
a commit name alone (`IMPORT.SOURCE_MAPPING_REQUIRED` — source mapping is
mandatory); `completeness ≠ complete` with empty `omissions`; an adapter closure
of the wrong kind; and a hit count on an `unmapped` subject, which never becomes
an admissible payload. The **imported-observation boundary** holds in both
directions: `observable-unhit` ≠ unused, `unobservable`/`unmapped` ≠ unhit, the
payload schema refuses a hit count on either, and imported evidence mints no
`ViewEntryV3` at all.

**A meaningful asymmetry, confirmed and not a defect.** A retained, hash-valid
fact frame referenced by **no** view is an unreferenced CAS blob: it is not an
evaluation input and it does **not** refuse — identity §3 says exactly that.
`plan.nativeContextDigests` is deliberately different: it *is* a set equality, and
a hidden context refuses. I built both controls to keep them apart.

---

## 6. Workflows and public surfaces

**Zero-config selection over multiple units with an incomplete release.** Three
units (`ts-tsconfig`, `rust-cargo`, `syntax-only`); the matrix-fixed default
requests 11 + 10 + 10 = **31** rows — every cell that is not `NOT-SELECTED`,
`UNSUPPORTED-TYPED` cells **included** (they are answered by disclosure), and the
three `NOT-SELECTED` `clones-cross-tsjs` cells never requested. A release that
declares nine capabilities produces **16** absence notices, each carrying the
complete ownership tuple in typed fields — `capabilityId`, `languageMode`,
`workspaceRoot` — never concatenated, so two units requesting one capability stay
distinguishable. Candidate-only capabilities (`clones-near`,
`clones-cross-tsjs`) have empty matrix `relations`, so their projection is
`selection-account-only`; fact-producing capabilities keep `coverage-entry`.

**Bounded cardinality and ordering.** Steps ≤ 64 (`StepId` 0–63), attempts ≤ 3,
per-step notices ≤ 1024 (exactly the `requestedCapabilities` bound), steps ≤ 64;
`totalNoticeCount` is the exact sum, not a truncation residue; order is the
selection's own (`sequence`); a step that selected and found nothing absent
contributes an **empty** entry — the positive statement that it checked.

**Output formats.** From the inventory, not from prose: `default`/`analyze`/
`audit` carry human/json/sarif/html/agent; `fit` has no SARIF; `repair-verify`
has no HTML; exactly four commands advertise SARIF, and each declares the seven
common fields. `capability-availability` is a declared parity field of every
`requestClass: analysis` command.

**Product promise vs installed availability vs override vs prerequisite.** Four
distinct things, each exercised: the matrix fixes the default (promise); the
authenticated release registry states availability only; explicit
`analysis.capabilities` overrides the *request* with its own provenance; and a
semantic prerequisite (`references` under `syntax-only`) is a Coverage
`language-tier-unsupported` that **outranks** `provider-unavailable`.

**Public failure envelopes from actual internal refusals.** Five, each a complete
`CommandEnvelope` validated against the real schema, not a termination fragment:

| Originating boundary | class / exit | errorCode | envelope detail |
|---|---|---|---|
| configuration input | request-rejected 2 | `CONFIG.INVALID` | `CONFIG.INVALID` |
| retained external input | request-rejected 2 | `REQUEST.PRECONDITION_FAILED` | `native.capability-spec-invalid` |
| host-generated invalid internal record | operational-failed 4 | `SYSTEM.OUTCOME.ILLEGAL_STATE` (`host-invariant`) | `HOST.INVARIANT_VIOLATED` |
| producer boundary | operational-failed 4 | `PROVIDER.PROTOCOL_VIOLATION` (`provider-protocol`) | `native.coverage-cause-unsupported` |
| well-formed `NOT-SELECTED` request | request-rejected 2 | `REQUEST.UNSATISFIABLE` | `PROVIDER.NOT_SELECTED` |

An origin a key cannot have refuses; an unregistered raw key refuses rather than
passing through; `bounded_subject` produces exactly 1024 **code points**
preserving the registered key verbatim and appending `...#sha256:` + the SHA-256
of the untruncated UTF-8 (a non-ASCII case measured at 1024 code points / 1927
bytes, so the two units are not conflated).

**The selected D9 extension, checked against the inherited contract.** The
inherited `d9-exit-contract.v1.14.json`
`scenarioAxesSchema.properties.faultCause.enum` has 11 members and does **not**
contain `host-invariant`; `codeMaps.faultCauseToErrorCode` has 10 rows and no
preimage for `SYSTEM.OUTCOME.ILLEGAL_STATE`. The selected composition adds
**exactly one** member, removes none, maps it to an **existing** error code, and
changes no class, exit code or reason code. The declared precedence
(`faultCause > rejectionCause > deficiency`) is unchanged. The successor-artifact
obligation is disclosed and attributed by the kit; I record it as a live
cross-unit obligation rather than a new finding, because a consumer validating
against the inherited artifact alone would still refuse a lawful `host-invariant`
termination.

**Pinned-purge refusal, complete.** `evidence.pinned` /
`REQUEST.PRECONDITION_FAILED` / exit 2, with the closed `PinnedPurgeDisclosure`
carrying the RunId, the complete `activePins` inventory sorted uniquely by
`pinId`, and the three **ordered** consequences. Truncating the consequence list
refuses; an empty `activePins` refuses; `purgeDisclosure` on any other detail code
refuses.

**Purge / replay / required-output failure.** `evidence.{expired,purged,missing,
corrupt}` before evaluation are `request-rejected` (2); the *same* detail **during
a selected operation** is `HOST.IO_FAILURE` (4) — different event positions, not
interchangeable spellings. Required-output failure after commit is
`DELIVERY.REQUIRED_FAILED` / `delivery-required` (4) with the RunId retained and
the Run unrewritten; an optional export sink failure leaves `success`.

**Comparison where only the scope policy changes.** A real `ScopeDocumentV1` is
bound as an analysis-spec parameter through its exact registered document digest
and selector (`workflows/schemas/policy-document.schema.json#/$defs/
ScopeDocumentV1`). Two Runs differ only in that parameter:
`plan.scopeDigest` (the foundation `scope-descriptor` — the repository extent
actually walked) and the snapshot are **identical**, while
`analysisSpecDigest`, `PlanId` and `RunId` move.
`EvaluationContext.scopeDigest` equals the bound parameter's `payloadDigest`, and
the entry is attributed to the **scope** axis (E2 → E3), not to code. The two
scope records never substitute for each other. Also constructed: a **missing**
prior detector (typed indeterminacy, never a two-way fallback), an
**evidence-changed** gating rule (replacing an artifact of the same kind is still
an evidence change), and an **empty result** where both finding sets are empty but
a required re-evaluation is unbound for a gating rule — indeterminate, because
zero emitted findings never establish complete analysis.

**Repair descriptor projection and its authority boundary.** The
`RepairPlanDescriptor` carries the **five-field** `closedWorld` projection; a
literal copy of the seven-field `ClosedWorldV2` is refused there. The whole
descriptor is the `repairPlanId` preimage, so editing the projection moves the
plan id and therefore no authorization names it. Per-target evidence requirements
are admitted by **plane**, decided from the relation's registry membership and
never from the value: a native requirement claiming an imported outcome refuses,
an imported one claiming a native outcome refuses, a rung of another relation's
ladder refuses, and an explicit `null` deficiency refuses in both branches. An
unsatisfied requirement makes the plan inapplicable and emits its own unmet
precondition carrying that requirement's cause.

**Minimum-resolution predicates at three levels.** Satisfaction is ladder-index
comparison **inside one relation**: `declares@syntactic` qualifies for
`syntactic`; `references@syntactic-name-match` is insufficient for
`resolved-binding` while `resolved-binding` qualifies; `types@annotated` is
insufficient for `checked` while `checked` qualifies. A cross-relation rung —
in either the `have` or the `minResolution` position — **refuses** and is never a
true or false predicate. The full strong-Kleene atom table
(`exists`/`none`/`count-at-most`/`all-covered` × complete/incomplete) was executed;
a zero count under incomplete Coverage is `indeterminate`, never `false`.

---

## 7. Findings

### MUST

**CB-GAP-1 — the `parameter` payload class admits two `ScopeDocumentV1`
parameters and nothing decides which one is the Plan's scope policy.**
*Selectors:* `foundation/identity-schemas.v2.json#/x-opensip-payload-registry/
classes/parameter` (`keyedBy: [the cited schemaDigest]`);
`foundation/identity-schemas.v2.json#/$defs/analysis-spec/properties/parameters`;
`identity-and-evidence.md` §3 "The `ScopeDocumentV1` parameter row (CB3-MUST-4)"
and "Where the binding is actually decided, and where it is only asserted".
*Measured:* I built an analysis spec carrying **two** parameter rows, both citing
`policy-document.schema.json` with different `ScopeDocumentV1` payloads. Both
validate under the one registered selector, and the Run **closes** (190 checks, no
fault). The published verifier is existential — "the scope document's canonical
digest must be the `payloadDigest` of **a** selected parameter row citing the
registered `ScopeDocumentV1` document digest" — so it is satisfied by either.
*Why it matters:* `EvaluationContext.scopeDigest` is the comparison scope axis
(E2 → E3). Two conforming hosts can bind different scope documents out of **one
admitted Plan**, so the same `PlanId` attributes a finding to the scope axis or
not depending on an unpublished choice. `uniqueItems` does not help (the rows
differ), and `x-opensip-order: canonical-set` orders them rather than refusing
them.
*What would close it:* the rule identity §3 already gives the sibling row —
"No parameter means an empty set; more than one is refused" — stated for this row
too, or a published selection rule.

**CB-GAP-3 — `coverage: complete` and `resolutionCompleteness.examinedExhaustive:
false` are both admissible on one entry.**
*Selectors:* `native/native-evidence.schemas.v2.json#/$defs/ViewEntryV3/properties/
coverage`; `…#/$defs/ResolutionCompletenessV2/properties/examinedExhaustive`;
`native-evidence.md` §4.1 claim 1, §4.3 RC-1 ("`examinedExhaustive` stays the
independent examined-partition claim of §4.1") and RC-3.
*Measured:* I edited a `file@enumerated` entry to carry `coverage: complete` with
`examinedExhaustive: false`, re-keyed the view/evidence/seal/Run around it, and
the Run **closes** (422 checks, no fault).
*Why it matters:* both fields encode §4.1's claim 1 ("did we look at every
subject?"), and no join is published. `COVERAGE_INVENTORY_TOTALITY_OMITS_PATH`
keys on `coverage` alone, so this sealed entry simultaneously carries the total
`file@enumerated` obligation and denies that the partition was examined
exhaustively. RC-2 reads `examinedExhaustive` for a resolved rung only, so on the
twelve non-resolved pairs nothing reads it at all. The one direction that is
genuinely contradictory is `complete` + `examinedExhaustive: false`; the reverse
(`unknown` + `examinedExhaustive: true`) is meaningful and I used it in the
syntax-only Runs.
*What would close it:* the same rule identity §3 states for `plan.budget` against
the resolved configuration — "the value is committed in two places and neither
silently wins" — i.e. `coverage == "complete"` ⇒ `examinedExhaustive == true`,
decided at closure.

### SHOULD

**CB-GAP-2 — an analysis spec may carry two `requestedCapabilities` rows for one
`(capabilityId, languageMode, workspaceRoot)` differing only in `required`.**
*Selectors:* `foundation/identity-schemas.v2.json#/$defs/analysis-spec/properties/
requestedCapabilities`; `native-evidence.md` §1.4 "The release declaration
registry" (which *does* refuse a duplicate `capabilityId` for exactly this
reason). *Measured:* schema validation admits; my capability admission admits.
Requiredness decides whether a missing Coverage entry contributes indeterminate,
and both rows enter `analysisSpecDigest` and therefore `PlanId`, so the
contradiction is committed.

**CB-GAP-4 — `stage-spec.operation` and both `outputDomains` arrays are unbounded
`Text` with no named vocabulary, while `stageSpecDigest` reaches `RunId`.**
*Selectors:* `foundation/identity-schemas.v2.json#/$defs/stage-spec/properties/
operation`; `…/stage-spec/properties/outputDomains/items`;
`…/execution-plan/properties/stages/items/properties/outputDomains/items`.
*Measured:* none of the three carries an `x-opensip-vocabulary` annotation, while
the sibling `analysis-spec.requestedCapabilities[].capabilityId` does. Two
conforming hosts describing one stage may write `native.analyze` vs `analyze`, or
`subject-scope` vs `scope2`, and mint different `stageSpecDigest` →
`exec-plan2` → `proof2` → `seal2` → `RunId`. This is the exact defect class
CB4-SHOULD-2 closed for `capabilityId` and `x-opensip-config-node-kind-law` closed
for `TypeScriptConfigGraphV1.kind`; identity §3's requirement that the spec's
`outputDomains` *equal the stage's* is an internal consistency rule between two
places that may both be spelled the same wrong way.

**CB-GAP-5 — the membership rule for `plan.semanticClosures` is published for
exactly one field.** *Selectors:* `foundation/identity-schemas.v2.json#/$defs/plan/
properties/semanticClosures`; `…/$defs/subject-scope/properties/enumeratorClosure`
(the one field whose description states "The closure must also be a member of
`plan.semanticClosures`"); `…#/x-opensip-digest-domains/closureKinds/byField`
(which states *kind*, not membership). *Measured:* `fact.producerClosure` carries
no description at all, and no membership statement exists for
`view.producerClosure`, `stage-spec.producerClosure`, `cache-key.producerClosure`,
`proof-bundle.evaluatorClosure`, `evaluation-seal.evaluatorClosure`,
`finding.ruleClosure`, `import.producerClosure`, `import.adapterClosure`, or the
native context's toolchain / stdlib / rust-dev-llvm / grammar closures. The array
is a canonical set inside the Plan descriptor and therefore a `PlanId` input, so
two hosts analysing one repository with one toolchain can mint different `PlanId`s
depending on whether they list the toolchain and stdlib closures. **This absence
forced a choice on me**: I included them. I did not construct a closing Run with
the narrower set, because every retained view, scope and fact names the original
`plan2`, so re-minting all of them would be a second complete graph rather than a
discriminating control; the finding rests on the selector inspection above.

### Advisory (non-blocking)

* **ADV-1.** `view.schemaDigests` is defined as "the registered documents a view
  admitted, and each member must be one of them". Membership is stated; the
  required *set* is not mechanically derivable from the retained record, and the
  value enters `view2` → `evidence2` → `seal2` → `RunId`. It is determined by what
  the view actually admitted, so this is a checkability gap rather than an
  ambiguity. I chose the relation-payload document and the native document (plus
  the imported-evidence document for the import Run).
* **ADV-2.** No join is published between `semantic-evidence.importIds` and
  `plan.importIds`. Identity §3 requires every *evaluated* import to belong to
  Plan and to appear in `evaluationInputRefs` (which I enforce), but not that the
  evidence record's list equal the Plan's. I set them equal.
* **ADV-3.** The one content-addressed store keyed by raw SHA-256 means a
  byte-identical artifact reachable by two joins yields one first refusal on
  loss, masking the second. Measured in CB-RS-N7. This is a consequence of the
  contract's own single-store design and is noted so a reader does not read the
  refusal name as the only applicable join.
* **ADV-4.** The kit's disclosed, attributed obligation on the D9 unit (publish a
  successor artifact carrying `host-invariant`) remains live: a checker reading
  `d9-exit-contract.v1.14.json` alone still refuses a lawful `host-invariant`
  termination. I verified all three halves (the inherited artifact omits it, the
  selected composition carries it, the disclosure is present).

---

## 8. What I had to invent, and what I did not

**Invented (authoring freedom, no public contract missing).** Message codes and
remedy texts; `SubjectIdV1` spellings for symbol subjects (opaque by design);
`ownerKey` and `cfgSetId` tokens; the specific repository shapes, file bytes and
level-specification bytes; the declaration-signature token projection (the
contract explicitly leaves the projection to the selected detector closure and
fixes only the encoding, which I implemented).

**Invented because a contract is missing or ambiguous** — these are the findings
above, not free choices: which of two `ScopeDocumentV1` parameters is the Plan's
scope policy (CB-GAP-1); the `coverage`/`examinedExhaustive` join (CB-GAP-3);
the `stage-spec.operation`/`outputDomains` vocabulary (CB-GAP-4); the
`plan.semanticClosures` membership set (CB-GAP-5).

**Assumed, never proved.** Every TCB observation: closure signatures and
manifests, custody results, provider frame emissions, enforcement values,
grammar-bundle contents, ledger pin inventories, dependency checksums and the
existence of the artifacts my inventories name. Synthetic TCB observations are
assumptions, never native enforcement proof.

**Bugs in my own code, corrected against the kit and preserved.** Three, all with
a precise existing normative answer, so none is a new design gap:
1. My capability-manifest ADM-TYPE gate typed *absent* keys, so a missing required
   key reported ADM-TYPE instead of ADM-CLOSED. ADM-TYPE types a **present**
   scalar; ADM-CLOSED owns the key set. Corrected; CB-CM-5 now observes ADM-CLOSED.
2. My closure discovered native contexts by reading `plan.nativeContextDigests`,
   so a hidden retained context was invisible. Identity §3 requires the retained
   frame **set** to equal that array; I now scan the store. CB-TS-N12 was the
   failing control that exposed it.
3. My closure discovered universes by scanning for well-formed frames, so a raw
   canonical payload offered where a frame is required was silently skipped
   (CB-TS-N10 reported a downstream `SCOPE_UNIVERSE_NOT_RETAINED`). Universes are
   now **resolved by digest** from the scopes and facts that name them, and the
   refusal is the prefix failure the closing digest law states.

Two of my *expectations* were also wrong and the kit was right, which I record
rather than quietly restate: a byte flip inside a retained frame refuses at frame
**parsing**, not at the identity check, so the identity check is masked unless the
mutation keeps the payload canonical (CB-TS-N8); and there are **17** registered
`(relation, rung)` pairs, not 15 — 15 is the size of the flat rung vocabulary.

---

## 9. Limitations

* Nothing here is product qualification, a readiness grade, or implementation
  authorization. No cell is `QUALIFIED`; `SUPPORTED-DESIGN` is unchanged.
* No real OS, compiler, Cargo, provider, renderer, SQLite, filesystem, crypto or
  network operation was performed. Real measurements are future qualification work
  and I do not demand that the product already exist.
* I did not build: `CloneCandidateGroupV2` near/cross-tsjs candidate records
  (candidate-only, no fact relation); a full `BaselineArtifactV1` instance (I built
  the comparison descriptor and its evaluation contexts); the security unit's own
  signed records (`RootV1`/`RootV2`, `RepoExecutionGrantV2`,
  `InstallationTransitionJournalV1`, the trust-recovery epoch) beyond the
  workflow-side projections that consume them; the HTML/SARIF/agent renderers;
  the policy-test suite; and the graph-query surface.
* My closure checker is *stricter* than the contract in one place I am aware of:
  it applies snapshot and relation joins to every retained fact frame, including
  ones no view references. That is conservative, not a refusal — the unreferenced
  frame still admits (CB-TS-N24).
* The public detail registry has 287 members and I exercised a small named subset.
* Coverage of the 66-cell matrix is by *mode and universe*, not by cell: I built
  at least one Run in every language mode and every native universe, and exercised
  the inventory, syntax, clones-fact, references and unresolved-edge capabilities.

---

## 10. Verdict

The design is **reconstructable to a working implementation** for the scope I was
asked to cover: an independent reader with only these 46 files can build the
canonical encoder, the identity and framing law, the capability-manifest
admission, the three native universes and their contexts, the relation registry
and its anchor/totality/partition laws, the body-identity grammar and its
per-language dialect selection, the Coverage admission and deficiency/cause
registry, the provider state machine, the Plan/proof/evidence/seal/Run closure,
the D9 composition and the public failure surface — and can make sixteen complete
Runs close and re-close from a byte export. That is a substantial and unusually
complete design.

It is nevertheless **CHANGES_REQUIRED**, on two MUST issues that are the same
class of defect this contract set repeatedly and explicitly closes elsewhere:
one committed value with two admissible readings (CB-GAP-1), and one claim
committed in two places with no join deciding which wins (CB-GAP-3). Both are
reachable by ordinary valid inputs, both survive a complete retained-Run closure
in my independent implementation, and both change what a sealed Run means to a
second conforming host. The three SHOULD issues are determinacy gaps of the same
family that the kit has already closed for sibling fields, so the remedy pattern
is established rather than novel.
