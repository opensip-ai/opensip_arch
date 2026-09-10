# Handoff v2 — the Rust semantic-universe seam, nested native identities, and the cache boundary

**Author session:** actual Claude, coauthor (same session lineage as
`reviews/digest-corrections-author.v1/`). I am an author, **not** the reviewer, and I cannot and do
not accept my own work. Nothing here awards readiness, discharges a gate, qualifies a platform or
authorizes implementation. **Native and source-hash/frame registration work here is design and
reference work, not platform qualification.** A fresh independent whole review and a fresh blind
TS+Rust consumer both remain mandatory.

All new scratch, probes, runs and this handoff are in
`/tmp/opensip-design-corrections/digest-corrections-author.v2/`. I rewrote nothing under
`reviews/digest-corrections-author.v1/` or any other retained snapshot.

---

## 1. Changed files (all owned this session)

| Path | SHA-256 | Lines |
|---|---|---|
| `docs/v2/contracts/product-v1/identity-and-evidence.md` | `5341cd20f3238d789c5bdace632ad632891fe71e2f012451303b7cbaf6c24594` | 795 |
| `docs/v2/contracts/product-v1/native-evidence.md` | `f499b3a43fb329ad0b75497eeb0bc40f16603a5c503ba61baff95edfe66d8cd5` | 1843 |
| `docs/coop/design-corrections/foundation/identity-schemas.v2.json` | `e7d936045e4ffc67aae9a9248b4cf4bb19bb8c5e2db372df67363b3eadbb52b7` | 3050 |
| `docs/coop/design-corrections/foundation/identity-model.py` | `1692ea4d7c46f81b5f65ac9dea010418188dc411a6d4cbbc7a4d842dd1fc75fb` | 803 |
| `docs/coop/design-corrections/foundation/check-identity.py` | `6a112bcc2b03aceac0aef8c2303d50910f84fd14fa02de8344f81ef42f02e751` | 1375 |
| `docs/coop/design-corrections/native/native_evidence_model.v2.py` | `26392005913bc6157c6ccc89dd6b66d2f629578f54810faab4b5a1139b8456ba` | 2471 |
| `docs/coop/design-corrections/native/native-evidence.schemas.v2.json` | `491610805f97ff54b363ac5d34342d58d85b1c429daef98efc4d8bb551a26fa0` | 5115 |

**`native/native-cases.v2.json` and `native/check_native_evidence.v2.py` are unchanged**, so the
native suite stays at 132/132 and its generated report does not churn while you finalize pins. The
native-boundary unit checks that a Run closure cannot reach live in `check-identity.py` instead
(§6); lift them into `native-cases.v2.json` if you prefer them there.

I edited no `canonical.py`, no pin, no generated report, no shared integration file, no
security/workflow file, no configuration schema, no source map, no README/governance/readiness
record. Codex's array annotations, the typed order-refusal projection and the sorted owner fixture
are preserved untouched.

## 2. The Rust premise, resolved

**Your correction was right and my v1 handoff was wrong.** Native §11 already registered
`native.semantic-universe.rust.v2` and §2.1 already supplied `RustUniverseV2ResolvedInputs`. I said
otherwise and deferred the path to qualification. It is now closed, not deferred:

| Was | Now |
|---|---|
| identity registry held only the TypeScript universe domain | both domains registered, with language, binding entry point, context/agreement/snapshot/nested joins |
| no `bind_rust_universe` | `bind_rust_universe` implemented in the native model, pure, and re-run by Run closure exactly as the TypeScript binding is |
| `configProjectionSha256` said "H over CargoConfigProjectionV2" with no domain | domain `native.cargo-config-projection.v2` named in native §3.3/§11 and registered |
| `CargoConfigProjectionV2.projectionSha256` had no stated recipe | raw SHA-256 of the projected `.cargo/config.toml` **file** bytes; explicitly not the record identity and not raw `C(record)` |
| nested Rust ids were opaque strings | each is an H identity over a registered record, retained as its own frame and re-admitted, down to raw member bytes |
| a Rust context sat inside a TypeScript Run | a **complete Rust universe / fact / Coverage Run** closes, replays and commits, alongside the complete TypeScript one |

### 2.1 The registered domain table

`identity-schemas.v2.json#/x-opensip-digest-domains/domainSets`:

| Domain set | Domain | Record | Owning admission |
|---|---|---|---|
| `native-context` | `native.context.typescript.v2` | `TypeScriptNativeContextV2` | `admit_native_context('typescript', …)` |
| `native-context` | `native.context.rust.v2` | `NativeContextV2` | `admit_native_context('rust', …)` |
| `native-semantic-universe` | `native.semantic-universe.typescript.v2` | `TypeScriptUniverseV2ResolvedInputs` | `bind_typescript_universe(universe, admission, context)` |
| `native-semantic-universe` | `native.semantic-universe.rust.v2` | `RustUniverseV2ResolvedInputs` | `bind_rust_universe(universe, admission, context, retained, snapshotInventory)` |
| `native-nested` | `native.dependency-source-set.v1` | `DependencySourceSetV1` | frame + record; chains to each package's file manifest |
| `native-nested` | `native.dependency-file-manifest.v1` | `DependencyFileManifestV1` | frame + record; every row's `contentSha256` retained at its exact `byteLength` |
| `native-nested` | `native.unified-features.rust.v1` | `UnifiedFeaturesV1` | frame + record |
| `native-nested` | `native.prepared-output-set.v3` | `PreparedOutputSetV3` | frame + record; every inert row's blob retained at its exact length |
| `native-nested` | `native.cargo-config-projection.v2` | `CargoConfigProjectionV2` | frame + record; `replacedSnapshotConfigs` snapshot-joined; projected config file bytes retained |

Each row declares its `closureJoins`, `snapshotJoins`, `nestedIdentities`, `blobJoins`,
`contextDomain`, `contextAgreementFields` and `binding.arguments`, so the closure is registry-driven
rather than special-cased per language.

### 2.2 `bind_rust_universe` — the exact API

```python
bind_rust_universe(universe, admission, context, retained=None, snapshot_inventory=None) -> dict
# retained: {'dependencySourceSet':…, 'unifiedFeatures':…, 'preparedOutputSet':… or absent}
# returns  {'result':'ADMIT'|'REFUSE','refusals':[…],'universeId':'sha256:…',
#           'sourceUniverse':'<64 hex>','nativeContextId':'sha256:…'}
```

`context`, `retained` and `snapshot_inventory` are all **required**: omission is
`native.universe-retained-inputs-not-supplied` / `native.universe-context-not-supplied`, never an
ADMIT, for the same reason `bind_typescript_universe` has no context-free path. It executes no
cargo, rustc, build script, proc macro or filesystem read; every input is a retained descriptor or
an explicitly trusted observation. Supporting helpers, all pure:

```python
cargo_config_projection_identity(projection)   # H(native.cargo-config-projection.v2, CargoConfigProjectionV2)
unified_features_identity(features)            # H(native.unified-features.rust.v1, UnifiedFeaturesV1)
prepared_output_set_identity(prepared)         # H(native.prepared-output-set.v3, PreparedOutputSetV3)
dependency_source_set_identity(descriptor)     # H(native.dependency-source-set.v1, DependencySourceSetV1)
rust_universe_context_field_faults(universe, context)
rust_universe_retained_input_faults(universe, context, retained, snapshot_inventory)
NATIVE_UNIVERSE_DOMAINS, NATIVE_UNIVERSE_DEFS, CARGO_CONFIG_PROJECTION_DOMAIN,
UNIFIED_FEATURES_DOMAIN, PREPARED_OUTPUT_SET_DOMAIN, DEPENDENCY_SOURCE_SET_DOMAIN,
DEPENDENCY_FILE_MANIFEST_DOMAIN
```

`admit_native_context('rust', …)` also gained the Rust counterpart of the TypeScript tool checks,
which CC-4 already required: `rustc`, `cargo` and `procMacroServer` (and `linker`/`ar` when
selected) must be members of the retained signed tool closure, the closure's `semanticVersion` must
be the declared `rustcVersion`, `toolchain.targetTriple` must equal the context's, the stdlib
component list must be ordered and unique, and `executableSelected` must be false. No existing case
admitted a Rust context, so nothing regressed.

### 2.3 Design choices I had to make explicit, and did

- **`CargoConfigProjectionV2` has two digests.** `projectionSha256` = raw SHA-256 of the projected
  `.cargo/config.toml` file bytes (CC-5's single materialized file). `configProjectionSha256` =
  64-hex suffix of `H("native.cargo-config-projection.v2", CargoConfigProjectionV2)`. Non-circular,
  both retained, neither substitutes for the other. Stated in native §2.1, §3.3 and the schema.
- **`cfgSets` relate to `baseCfg` by addition only.** §2.1 said "default `[primary, primary+test]`"
  without saying how a set relates to the context's `baseCfg`. It now states that every set's `cfg`
  contains every member of `baseCfg` and that `cfgSetId` is unique: a set that dropped a base cfg
  would analyse a configuration nothing selected.
- **Language-mode ownership.** `analysis-spec.requestedCapabilities[].languageMode` must be a
  registered native `LanguageMode`, and every admitted universe's language must be one the Plan
  requested; a prepared resolution additionally requires the prepared mode
  (`rust-cargo-prepared`). The map lives in
  `x-opensip-digest-domains.languageModes`. This is the "language/request/universe ownership join"
  you asked me to make explicit or disclaim — it exists, in the pure graph, and its mismatches are
  exercised.

## 3. Nested identity audit — the answer to "not opaque strings"

`dependencySourceSetId`, `unifiedFeaturesId`, `preparedOutputSetId` and `configProjectionSha256` are
no longer accepted because an outer frame hashes. Each is admitted through the same frame law:
retained frame → exact prefix/domain/length/canonicality → validated under the record its **domain**
registers → `H` recomputed. Then the chain continues:

```
rust context / rust universe
 ├─ dependencySourceSetId  → DependencySourceSetV1
 │    └─ packages[].fileManifestSha256 → DependencyFileManifestV1
 │         └─ [].contentSha256 retained blob, length == [].byteLength
 ├─ unifiedFeaturesId      → UnifiedFeaturesV1
 ├─ preparedOutputSetId    → PreparedOutputSetV3        (null stays null)
 │    └─ rows[].blob.sha256 retained blob, length == rows[].blob.byteLength
 └─ configProjectionSha256 → CargoConfigProjectionV2
      ├─ replacedSnapshotConfigs[] must be inventoried snapshot paths
      └─ projectionSha256 retained blob (the projected config file)
```

Joins the binding then enforces against the universe and context: dependency set identity and its
`lockfileIdentity`; unified features identity, `targetTriple` and `resolverVersion`; prepared set
identity, `preparation.dependencySourceSetId`, `preparation.toolchain`, `preparation.cfgSetId` and
`preparation.kind` ↔ `preparedResolution`; `Cargo.lock` bytes, `crateRootPaths` and
`replacedSnapshotConfigs` against the snapshot inventory.

**Optional absent preparation stays absent.** `preparedOutputSetId = null` means no prepared set;
a retained prepared set that no universe selected is refused
(`native.universe-retained-input-unselected:preparedOutputSet`) rather than drifting into the
resolution. **Execution authority stays operational**: `preparedResolution` projects the grant
operation the native contract names (`host-prepared` → `prepare-code`, `imported-inert` →
`read-import`), a universe that consumed prepared products without it refuses
(`PREPARED_RESOLUTION_GRANT_JOIN`), and `executionCapableResolution` remains a statement about what
the resolution consumed, checked to be exactly `preparedResolution != none`.

## 4. The cache gap — resolved, with the boundary stated exactly

`cache_identifier` is replaced by two functions, because you were right that one helper was doing
two different jobs and the old one overclaimed.

```python
cache_key(domain, key) -> 'cache2:…' | 'regen2:…'
    # PURE. Exact schema admission and canonical order only. Reads no bytes, resolves no
    # reference. A host may compute it before loading anything and MISS cheaply. It grants nothing.

admit_cache_entry(domain, key, run, objects, blobs) -> {'identity','runId','stageSpec',
                                                        'consumedRefs','grantsEvidenceAuthority':False,'note'}
```

**Lifecycle boundary, stated honestly and in the contract.** `admit_cache_entry` is a
**post-construction conformance check over an admitted Run**, not the product's pre-analysis cache
scheduling API. A host schedules with `cache_key`, provisionally loads producer bytes on a match,
and those bytes then face ordinary stage and closure admission before anything gains Run authority.
Nothing requires a Run to consume an intermediate hit, so there is no dependency cycle. The question
this function answers is the later one: *given a Run and its admitted closure, was this entry
consumable under exactly that closure?*

What it checks: the stage must be one the **execution plan actually carries**
(`CACHE_STAGE_NOT_IN_THE_EXECUTION_PLAN`); its spec must join this Plan; the producing closure must
be retained and Plan-selected; every `scopeIds` member must be a retained `subject-scope` of this
snapshot; the output schema document must be retained; and every `inputRefs` entry is dispatched
through the **same** `x-opensip-digest-domains` registry the Run uses — so a consumed native context
must be Plan-selected, a consumed import must be Plan-selected, and a bare `coverage-payload` /
`import-payload` / `fact-payload` reference is refused as an authoritative root
(`CACHE_INPUT_PAYLOAD_REF_NOT_A_ROOT`) rather than resolved under a guessed schema.

**What it does not do, said plainly:** it does not model a miss (a miss is not a failure — the host
recomputes normally), it does not fetch or validate the cached **output** bytes, and it does not
decide reuse policy. It validates a lookup key and its consumed input closure against an admitted
Run. It is **not** a complete cache subsystem and I am not claiming it is.

**Your foreign-object hypothesis, assessed rather than assumed.** You were right that it might
already be closed. It is: `visit()` applies `REFERENCE_PLAN_JOIN` and `REFERENCE_SOURCE_JOIN` to
objects first reached through a cache reference too. I added the negatives anyway rather than
reasoning about it — a self-consistent, correctly-hashed view from another Plan refuses
(`REFERENCE_PLAN_JOIN`), and a scope from another snapshot refuses (`CACHE_SCOPE_SOURCE_JOIN`),
both from a store that contains both Runs' objects, with a control showing the Run's own view still
admits from that same mixed store.

## 5. Fixture coherence — your 12:35 observation

Also correct, and fixed. `build(universe_language='rust')` was a Rust universe under a TypeScript
question. Now the request, the source and the rule are one language:

| | typescript | rust |
|---|---|---|
| `requestedCapabilities[].languageMode` | `ts-tsconfig` | `rust-cargo` (`rust-cargo-prepared` when prepared) |
| analysed source | `a.ts`, `export const foo = 1;` | `src/lib.rs`, `pub fn root() {}` |
| fact anchor | that file's inventoried bytes | that file's inventoried bytes |
| `RULE.subjectEnumeration.universe` | `typescript` | `rust` |

`POLICY`/`RULE` became `policy_for(language)`/`rule_for(language)`; the module-level `POLICY` and
`RULE` remain the TypeScript ones, so existing TypeScript behaviour is unchanged and the shared
integration builder stays adaptable. `source_path` now defaults to `None` meaning "the language's
own source"; explicit values still get the TypeScript bytes, so `source_path='foreign.ts'` and
`source_path='run2:literal-filename'` behave exactly as before. The obsolete bottom-of-file
`RUST_SOURCES` / `rust_universe_run` scaffold you spotted is gone — there is one `RUST_SOURCES`, at
the top, and no late global rebinding.

The synthetic evaluator limitation stays explicit: the fixture interpreter still evaluates a
single-atom subset of the real closed DSL, and that is recorded in the report's `limits`.

## 6. Names the shared integration builder needs

Copy these module-level declarations from `foundation/check-identity.py` (AST-identical copy, as
before). New or changed since your last copy are marked.

```
ATOM
rule_for, policy_for            # NEW (replace the old RULE/POLICY constants)
RULE, POLICY, WAIVERS, compiled_program
COVERAGE_PAYLOAD_SCHEMA, FACT_PAYLOAD_SCHEMA, STAGE_OUTPUT_SCHEMA
TS_SOURCES
RUST_TARGET, RUST_DEP_KEY, RUST_DEP_FILE, RUST_PROJECTED_CONFIG,
RUST_SOURCES, RUST_PREPARED_DIRECTIVES                      # NEW
rust_inputs                                                  # NEW
LANGUAGE_FIXTURE                                             # NEW
native_inputs
build       # build(resolved=True, has_match=False, source_path=None, with_finding=False,
            #       stdlib_body=b'declare const es2022: unknown;\n',
            #       universe_language='typescript', prepared=None, grant_operations=None)
rekey, resync_stage_spec, rekey_plan, put_blob, graph_with_import
```

Module prelude unchanged: `M` (identity-model), `C` (`M.C`), `W` (workflows model), `N` (native
model), `NATIVE_FIXTURES` (the `fixtures` object of `native/native-cases.v2.json`).

**Codex has already refreshed the shared builder from these exact declarations** (their 12:47 note)
and reports **360/360 in-repo**, including five new cross-unit checks for a coherent `rust-cargo`
request / Rust policy / Rust universe / Rust source and a missing Rust source's shared
`StepTermination` / exit 4. I re-ran it in-repo and confirm **360/360, 0 failed**, and I verified
mechanically that all 29 copied builder declarations are AST-identical to mine (only the module
prelude bindings `H`, `spec`, `W`, `N` differ, as they must). `check-integration.py` itself needed
no change on my account.

## 7. Public diagnostics — the distinction you asked me to preserve

Every diagnostic this session added is an **internal** admission cause, not a public
`DomainDetail` code. None is emitted through a public termination, and **I added no public code and
no registry entry**. The public registry stays at exactly 282 records, and the only public
terminations this unit emits remain the two already registered: `evidence.missing` and
`evidence.regeneration-mismatch`. Three checks assert this mechanically
(`new-native-and-cache-causes-are-not-public-domain-detail-codes`,
`no-new-public-detail-code-was-added-by-this-session`,
`identity-public-terminations-remain-the-registered-two`). If you later decide any of these should
become public, it needs an explicit registry + `DomainDetailCode` enum delta; I did not assume one.

New internal causes, for your records: `NATIVE_CONTEXT_ADMISSION`, `NATIVE_UNIVERSE_BINDING`,
`NATIVE_UNIVERSE_BINDING_UNAVAILABLE`, `NATIVE_UNIVERSE_CONTEXT_LANGUAGE`,
`NATIVE_UNIVERSE_CONTEXT_FIELD_MISMATCH`, `NATIVE_{CONTEXT,UNIVERSE,NESTED}_PATH_NOT_INVENTORIED`,
`NATIVE_{CONTEXT,UNIVERSE}_SOURCE_MISMATCH`, `NATIVE_NESTED_NESTED_IDENTITY_REQUIRED`,
`NATIVE_NESTED_MEMBER_LENGTH`, `PREPARED_RESOLUTION_GRANT_JOIN`,
`PREPARED_RESOLUTION_MODE_NOT_REQUESTED`, `UNIVERSE_LANGUAGE_NOT_REQUESTED`,
`ANALYSIS_SPEC_LANGUAGE_MODE_UNREGISTERED`, `CACHE_STAGE_NOT_IN_THE_EXECUTION_PLAN`,
`CACHE_INPUT_PAYLOAD_REF_NOT_A_ROOT`, `CACHE_INPUT_DOMAIN_UNREGISTERED`,
`CACHE_INPUT_CONTEXT_NOT_SELECTED`, `CACHE_INPUT_IMPORT_NOT_SELECTED`, `CACHE_SCOPE_SOURCE_JOIN`,
`CACHE_UNSELECTED_PRODUCER`; and native's own `native.universe-*` refusal strings.

## 8. Checks and suite results (intermediate, unpinned)

`foundation/check-identity.py`: **275 → 354, 0 failed**, 89 new check ids. Ten v1 ids no longer
appear, and none of them lost coverage — the disposition of every one is in `handoff.json` under
`checks.removedCheckIdDisposition`:

- **Two are superseded because the thing they asserted is no longer true.**
  `rust-universe-binding-is-declared-required-and-missing` and
  `rust-universe-refuses-until-native-provides-its-binding` asserted that `bind_rust_universe` did
  not exist. It does now, so those are false statements; they are replaced by
  `rust-universe-binding-entry-point-exists` and the complete positive Rust Run.
- **Eight are renames with equal or stronger coverage**, e.g. `cache-missing-stage-spec-bytes` →
  `cache-hit-refuses-stage-spec-bytes` (now the stronger
  `CACHE_STAGE_NOT_IN_THE_EXECUTION_PLAN` join), and
  `rust-universe-must-agree-with-its-context-{dependency-set,unified-features}` →
  `rust-universe-overlap-{dependencySourceSetId,unifiedFeaturesId}`, which now point the universe at
  a **second genuinely retained record** so they test the overlap rule rather than missing
  retention.

| Suite | Result | How run |
|---|---|---|
| `foundation/check-identity.py` | **354/354** (was 275) | direct, in-repo |
| `foundation/check-foundation.py` | 231/231 | direct, in-repo |
| `foundation/check-product-configuration.py` | 28/28 | direct, in-repo |
| `foundation/check-product-quality.py` | 24/24 | direct, in-repo |
| `workflows/check_workflows.v1.py` | 1253/1253 | direct, in-repo |
| `check-integration.py` | **360/360, 0 failed** | in-repo, against Codex's refreshed `integration-fixtures.py` (AST-identical builders) |
| `native/check_native_evidence.v2.py` | 132/132, 60 cells, 0 qualified, 0 open objects | disposable copy, pins regenerated **in that copy only** |
| `security/check-security-lifecycle.v1.py` | 456/456, 10/10 sweeps | disposable copy, pins regenerated **in that copy only** |

Expected `foundation/run-reference-checks.py` aggregate after repinning: **231 + 354 + 28 + 24 =
637**. These are **intermediate, unpinned development checks**; I repinned nothing in the repo and
regenerated no in-repo report. Codex finalizes CURRENT pins.

**Your v7 TypeScript counterexample stays closed.** Re-ran your probe script unchanged except for
output paths, against a fresh capture of the current tree
(`probes/p1_codex_v7_recheck.py`, subject `/tmp/opensip-design-corrections/native-run-probe.v7-recheck/`):
`reframedCompleteRun.admitted = false`,
`AdmissionError:NATIVE_CONTEXT_ADMISSION:native.native-context-field-mismatch:moduleResolutionMode`.
Your original admitting result and the corrected recheck are both retained; the original finding was
real and I am not relabelling it.

## 9. Selected new checks

Complete positive Rust path: `rust-universe-complete-run-closes`,
`rust-run-scope-and-fact-carry-the-rust-universe`, `rust-run-coverage-binds-the-rust-scope`,
`rust-run-replays-and-commits`, `rust-and-typescript-runs-are-different-runs`,
`rust-run-request-source-and-rule-are-one-language`,
`rust-imported-inert-prepared-run-closes`.

Nested identities: `rust-nested-identity-is-a-retained-record-*`,
`rust-config-projection-identity-is-the-named-domain`,
`rust-config-projection-file-digest-is-not-the-record-identity`,
`rust-dependency-package-file-manifest-is-a-retained-record`,
`rust-dependency-member-bytes-are-retained`,
`prepared-output-set-is-a-retained-record-of-its-domain`,
`prepared-inert-row-bytes-are-retained-with-their-exact-length`.

Negatives, each asserting its **exact** refusal string via `rejects_because`, with
`rust-run-harness-positive-control-closes` and `prepared-run-harness-positive-control-closes` so a
refusal is attributable to the mutation: overlap on `dependencySourceSetId`, `unifiedFeaturesId`,
`configProjectionSha256`, `rustflags`, cfg-set base-drop, duplicate cfg-set id,
`executionCapableResolution`, prepared resolution without a set; source correspondence on crate
roots, `Cargo.lock` bytes and replaced snapshot configs; retained-input joins on lockfile identity,
unified-features target; grant joins for `read-import` and `prepare-code`; prepared set bound to
another dependency set / cfg set / preparation kind; missing nested frame, missing dependency member
bytes and missing prepared row bytes as **retention loss** versus malformed bytes as
`BLOB_DIGEST`; raw `C(X)` offered where `H(D,X)` is required; and cross-language binding refused in
both directions.

Language ownership: `rust-universe-needs-a-rust-language-mode-request`,
`syntax-only-requests-no-semantic-universe`, `an-unregistered-language-mode-refuses`,
`prepared-run-requests-the-prepared-language-mode`.

Cache: `cache-key-construction-reads-no-bytes`, `cache-hit-admits-against-the-runs-own-closure`,
`cache-hit-grants-no-evidence-authority`, `cache-hit-refuses-{output-schema,producer,plan,stage-spec-bytes}`,
`cache-hit-refuses-a-bare-payload-reference-*`, `cache-hit-refuses-an-unselected-native-context`,
`cache-hit-admits-a-plan-selected-native-context`,
`cache-hit-refuses-a-self-consistent-foreign-{view,scope}`,
`cache-hit-still-admits-the-runs-own-view-in-the-mixed-store`,
`regeneration-hit-admits-the-same-way`.

Native boundary (rules a Run closure cannot reach):
`native-bind-rust-universe-has-no-{input,context}-free-admit-path`,
`native-bind-rust-universe-refuses-an-unselected-prepared-set`,
`native-bind-rust-universe-refuses-a-missing-required-input`,
`native-bind-rust-universe-refuses-a-dependency-set-that-is-not-the-named-identity`,
`native-bind-rust-universe-refuses-a-typescript-admission`,
`native-binding-refuses-a-prepared-resolution-with-no-prepared-set`,
`native-cargo-config-projection-identity-is-not-{the-projected-file-digest,raw-canonical-sha}`.

## 10. Limitations and remaining work

- **Design and reference work only.** No compiler, cargo, OS, filesystem or repository code runs
  anywhere in this. Every toolchain, lockfile, dependency, feature and prepared-output observation
  is an explicit synthetic trusted input. Nothing here qualifies a native carrier or a platform,
  and real compiler/OS/crypto/fsync/end-to-end measurement remains a release gate.
- The Rust dependency source set is one vendored registry package over a two-package `Cargo.lock`.
  Real crate graphs, workspace member enumeration, feature unification by an actual `cargo metadata`
  run and missing-external-crate Coverage remain the native unit's own cases and later
  qualification.
- The fixture evaluator still interprets a single-atom subset of the real closed
  `PolicyDocumentV1`/`RuleProgramV1` DSL. The record shapes, digests and joins are real; the
  interpreter is small, and that is unchanged from v1.
- `admit_cache_entry` is bounded exactly as §4 says: it does not fetch or validate cached output
  bytes and is not a complete cache subsystem.
- Relation and Coverage **payload schema registration** remains the native/workflow adapter
  boundary; identity checks retention, canonicality and validation under the retained document.
- `native-cases.v2.json` gained nothing, deliberately (§1). The Rust binding's own unit rules are
  exercised, just from `check-identity.py`.
- Pins and generated reports: seven owned files changed, nothing repinned, no in-repo report
  regenerated, `integration-fixtures.py` needs one re-copy (§6).
- **No acceptance.** A fresh independent whole review and a fresh blind TS+Rust consumer are both
  still mandatory, and neither is performed here.

## 11. Retained artifacts

```
/tmp/opensip-design-corrections/digest-corrections-author.v2/
  handoff.md, handoff.json
  CODEX-FOLLOW-UP-NOTE.txt            (Codex's, read before this handoff; §2/§4/§5/§7 answer it)
  probes/p1_codex_v7_recheck.py       Codex's v7 probe, re-run against current bytes
  runs/identity.json                  354/354
  runs/f.json, runs/w.json            foundation 231, workflows 1253
  runs/integration.json               355/355 (disposable shim), integration-in-repo.json 360/360
  runs/security.json                  456/456 (disposable copy)
  scratch/, scratch-native/, scratch-final/   disposable trees for pin-regenerated runs
/tmp/opensip-design-corrections/native-run-probe.v7-recheck/   v7 recheck subject and result
```
