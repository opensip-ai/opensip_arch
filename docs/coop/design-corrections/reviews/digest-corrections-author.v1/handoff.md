# Handoff — identity digest law (NEW-MUST-1, NEW-ADV-2)

**Author session:** actual Claude, identity/digest author. I am an author, **not** the reviewer, and
I cannot and do not accept my own work. Nothing here awards readiness, discharges a gate, qualifies a
platform or authorizes implementation. The corrected successor requires a **fresh independent
review**; `post-reset-review.v6` remains CHANGES_REQUIRED until one is performed.

Scope of my ownership this session: `docs/v2/contracts/product-v1/identity-and-evidence.md`,
`docs/coop/design-corrections/foundation/identity-schemas.v2.json`,
`.../foundation/identity-model.py`, `.../foundation/check-identity.py`. I edited nothing else.
No `canonical.py`, pin, report, native, security, workflow, integration, configuration-schema,
README, index, crosswalk, governance or readiness file was touched by me. All scratch work is in
`/tmp/opensip-design-corrections/digest-corrections-author.v1/`.

---

## 1. Changed files

| Path | SHA-256 (after) | Lines |
|---|---|---|
| `docs/v2/contracts/product-v1/identity-and-evidence.md` | `0cf0fc9b0beb994bd277871fe7515d6d4f8acee60b97e5366f1c79f99f7129c5` | 738 |
| `docs/coop/design-corrections/foundation/identity-schemas.v2.json` | `3cd4825dacf2cfd96cbefd1ba5ad4dad728a969274093b4b5d018fa674ccbfff` | 2878 |
| `docs/coop/design-corrections/foundation/identity-model.py` | `6131c1ff7a1c29ae71cf406d0f10e11e6602c8a74254cb319b9d504ee61fa2ea` | 692 |
| `docs/coop/design-corrections/foundation/check-identity.py` | `0eb4fbe3063e4f1347fa3d30dec565d1275083b551decdf99e66fe00142d6378` | 875 |

Recompute with `shasum -a 256`. These are the bytes I measured everything below against.
`docs/coop/design-corrections/integration-fixtures.py` and `check-integration.py` were adapted
**concurrently by Codex** from my updated builders — see §8.

## 2. The correction, in one paragraph

The review's NEW-MUST-1 was a **defect class**, not three strings: identity-bearing 64-hex fields
whose producing recipe existed nowhere, and a closure checker that recovered meaning from a field
**name** (`walk()` treated any key ending in `Digest`/`Digests`, or named `sha256`, as a raw blob
SHA-256). That heuristic was itself the bug: it silently mis-typed `plan.nativeContextDigests`
(H identities) and the four universe fields, and it gave unregistered records no recipe at all.
The fix is systemic. Every 64-hex field in `identity-schemas.v2.json` now carries a machine-readable
`x-opensip-digest` annotation naming its **representation** and **retention mode**; the closure
checker dispatches on that annotation and refuses an unannotated field; and the law closes by
admitting **no default**, so a future field added without an annotation refuses rather than
inheriting a plausible rule. Six missing closed records were added and the five named fields now have
exact producing recipes with enforced joins.

## 3. Exact field recipes — all 57 sites, 0 unannotated

Representations (closed): `raw-artifact` = raw SHA-256 of the exact retained artifact bytes;
`canonical-record` = raw SHA-256 of `C(record)` under a named registered record;
`h-identity` = lowercase hex of `H(D,X)`; `capability-manifest-id` = the inherited CVE1 recipe.
Retention modes (closed): `preimage` (default — the exact preimage bytes are retained in the CAS
under this digest), `fragment`, `derived`, `owner-retained`.

| Field | Representation → record/artifact |
|---|---|
| `Ref.digest`, `ProofInputRef.digest`, `FindingEvidenceRef.digest` | by-domain, through `x-opensip-digest-domains.byDomain` |
| `Blob.sha256` | raw-artifact |
| `snapshot.resolvedConfigDigest`, `plan.resolvedConfigDigest` | canonical-record → `#/$defs/semantic-configuration` |
| `snapshot.scopeDigest`, `plan.scopeDigest`, `import.scopeDigest`, `semantic-grant.scopeDigest` | canonical-record → `#/$defs/scope-descriptor` |
| `snapshot.vcsDigest` | canonical-record → `#/$defs/vcs-observation` |
| `vcs-observation.sourceInventoryDigest` | canonical-record → `#/$defs/source-inventory` **(new)** |
| `closure.manifestDigest` | raw-artifact |
| `import.payloadSchemaDigest`, `coverage.payloadSchemaDigest`, `fact.payloadSchemaDigest`, `view.schemaDigests`, `analysis-spec.parameters[].schemaDigest`, `stage-spec.parameters[].schemaDigest`, `stage-spec.outputSchemaDigest`, `cache-key.outputSchemaDigest`, `commit-inventory.blobDigests[]` | raw-artifact |
| `import.payloadDigest` | canonical-record → workflow `PayloadRegistryV1` row keyed by `kind` + `payloadDomain`, against the exact registered schema document bytes |
| `coverage.payloadDigest`, `fact.payloadDigest`, `analysis-spec.parameters[].payloadDigest`, `stage-spec.parameters[].payloadDigest` | canonical-record → the record `registeredBy` the sibling schema-document digest (which must constrain the payload directly) |
| `import.sourceCorrespondenceDigest` | canonical-record → `workflows/schemas/common.schema.json#/$defs/SourceCorrespondence` |
| `import.buildDigest` / `import.observationDigest` | canonical-record → `imported-evidence.schema.json#/$defs/BuildIdentityV1` / `ImportObservationV1` |
| `plan.analysisSpecDigest` | canonical-record → `#/$defs/analysis-spec` |
| `plan.semanticGrantDigest` | canonical-record → `#/$defs/semantic-grant` |
| `plan.policyDigest`, `evaluation-seal.policyDigest`, `policy-derivation.policyDigest` | canonical-record → `policy-document.schema.json#/$defs/PolicyDocumentV1` |
| `plan.waiverDigest`, `policy-derivation.waiverDigest` | canonical-record → `#/$defs/WaiverSetV1` (resolved effective set) |
| `proof-bundle.ruleProgramDigest`, `program-predicate.ruleProgramDigest` | canonical-record → `#/$defs/RuleProgramV1` |
| `proof-bundle.predicateProofs[].witnessDigest` | canonical-record → `#/$defs/predicate-witness` |
| **`predicate-witness.programPredicateDigest`** | canonical-record → `#/$defs/program-predicate` **(new)** |
| **`program-predicate.nodeDigest`** | canonical-record → `policy-document.schema.json#/$defs/Predicate`, retention `fragment` |
| **`finding.parameterDigest`** | canonical-record → `#/$defs/finding-parameters` **(new)** |
| **`execution-plan.stages[].stageSpecDigest`** and **`cache-key.stageSpecDigest`** | canonical-record → `#/$defs/stage-spec` **(new)** — one record, one recipe, byte-identical annotations |
| **`commit-receipt.inventoryDigest`** | canonical-record → `#/$defs/commit-inventory` **(new)** |
| `semantic-grant.principals[].ownerSourceDigest` | canonical-record → `#/$defs/owner-source-set` **(new)** |
| `owner-source-set[].ownerFileManifestSha256` | raw-artifact, retention `owner-retained` (security's `RepoExecutionGrantV2` owner admission) |
| `plan.nativeContextDigests[]` | h-identity → domain set `native-context` |
| `fact.sourceUniverse`/`targetUniverse`, `subject-scope.sourceUniverse`/`targetUniverse` | h-identity → domain set `native-semantic-universe` |
| `plan.capabilityManifestId`, `run.capabilityManifestId` | capability-manifest-id, retention `derived` from `plan.capabilityManifestBytesDigest` |
| `plan.capabilityManifestBytesDigest`, `fact.anchors[].blobDigest` | raw-artifact |

`x-opensip-digest-domains.byDomain` registers **every** member of every `domain` enum (32 domains, exactly the `Ref` enum);
an unregistered domain refuses. `coverage-payload`/`import-payload`/`fact-payload` are resolved
through their owning object's `payloadSchemaDigest` and are excluded from the proof input vocabulary.

## 4. The new closed records (schema selectors and joins)

### `#/$defs/program-predicate`
```
{schemaVersion:2, ruleProgramDigest, ruleId, predicateId, operation, nodeDigest}
```
It **addresses** one predicate node of the admitted `RuleProgramV1`. **No second policy or compiler
language was introduced**: the node's schema is the workflow contract's own
`policy-document.schema.json#/$defs/Predicate`, and the program is the workflow contract's own
`RuleProgramV1`, admitted through `workflows_model.validate_import_record`.

**Node address grammar** (also the meaning of `predicateProofs[].predicateId` and
`predicate-witness.childPredicateIds`): rule root `emitWhen` is `p`; the *i*-th operand of an
`and`/`or` node at `a` is `a.i` (zero-based, shortest decimal, no leading zero); the operand of a
`not` node at `a` is `a.0`.

Joins enforced in `close_run`: `ruleProgramDigest == proof.ruleProgramDigest`;
`ruleId`/`predicateId`/`operation` equal the predicate proof's; `ruleId` names a rule of the program;
`node.op == operation`; `SHA256(C(addressed node)) == nodeDigest`;
`witness.childPredicateIds == predicate_child_addresses(node, predicateId)`; every child is itself
proven for the same `(ruleId, subjectId)`; `witness.countLimit == node.n` for `count-at-most` and
`null` otherwise; `program.policyDigest == plan.policyDigest`; and
`W.rule_program_digest(plan-selected policy) == proof.ruleProgramDigest` — the compiled program must
be exactly the projection of the admitted policy.

### `#/$defs/finding-parameters`
```
{schemaVersion:2, messageCode, parameters:{<name>: string|integer|boolean}}
```
`parameters` is an **object map**, so names are unique and ordered by the canonical encoder itself —
no ordering annotation to elect and no new `x-opensip-order` vocabulary value needed.
Join: `parameters.messageCode == finding.messageCode`. Also newly joined: `finding.ruleClosure` must
be a Plan-selected semantic closure.

### `#/$defs/stage-spec`
```
{schemaVersion:2, planId, producerClosure, operation, parameters[{schemaDigest,payloadDigest}],
 outputDomains, outputSchemaDigest}
```
**NEW-ADV-2 answered explicitly** in prose and mechanically: `execution-plan.stages[].stageSpecDigest`
and `cache-key.stageSpecDigest` carry byte-identical annotations, so one spelling is one recipe over
one record. Joins: `spec.planId == plan`; `spec.producerClosure ∈ plan.semanticClosures`;
`spec.outputDomains == stage.outputDomains`; every `spec.parameters` row is also a Plan
`analysis-spec` parameter row (no hidden stage input); and for a cache/regeneration key,
`key.planId`, `key.producerClosure` and `key.outputSchemaDigest` must equal the stage spec's.

### `#/$defs/commit-inventory`
```
{schemaVersion:2, runId, objects[], blobDigests[]}
```
`inventoryDigest = SHA256(C(record))`. The store now builds and retains it.

### `#/$defs/source-inventory`
The snapshot inventory as a record in its own right (`x-opensip-order: path`), so
`vcs-observation.sourceInventoryDigest` names a record rather than an unnamed canonical fragment;
the closure requires `equal_typed(inventory record, snapshot.sourceInventory)`.

### `#/$defs/owner-source-set`
`[{ownerKey, source, ownerFileManifestSha256}]`, `x-opensip-order: {"by":["ownerKey"]}` — mirroring
security's `RepoExecutionGrantV2` owner projection (`integration-host-model.owner_rows`/`owner_digest`).
Uses the generic field-order form Codex added to `canonical.py`, so the order is schema-enforced,
not only model-enforced.

## 5. Raw bytes vs canonical record vs H identity — the closing law and its exceptions

`H(D,X) = SHA256(ASCII("opensip.product.v1") ‖ 00 ‖ ASCII(D) ‖ 00 ‖ uint64BE(len(C(X))) ‖ C(X))`.
Because H is SHA-256 of a framed preimage, the object retained under a bare-hex `h-identity` digest
is **the exact frame**, so a single CAS keyed by raw SHA-256 retains raw artifacts, canonical records
and H identities uniformly.

Frame admission is exact, and is **not** an arbitrary blob escape: literal prefix match; domain
`\0`-terminated, ASCII-strict, and a member of the annotation's **named domain set**; declared
`uint64BE` length equal to the remaining byte count; remainder byte-identical to `C` of its own
parse; parsed payload validated against the record the domain set registers, through the pinned
local schema registry with no network retrieval; and `C.identity(domain, value)` re-equal to the
digest.

Directionality is closed both ways and demonstrated:

- A raw payload SHA offered for an `h-identity` field refuses (`H_FRAME_PREFIX`), because `C(X)`
  does not begin with the framing prefix. Check `native-context-raw-payload-sha-is-not-an-h-identity`.
- A frame offered where a `canonical-record` is required refuses, because a frame is not JSON.
  Check `h-frame-refused-where-a-canonical-record-is-required`.
- An unregistered H domain refuses (`H_FRAME_DOMAIN_UNREGISTERED`). Check
  `native-context-unregistered-h-domain-refused`.
- The review's own alternative reading — `H("rule-program", record)` instead of
  `SHA256(C(record))` for `programPredicateDigest` — now refuses, so exactly one reading closes.
  Checks `program-predicate-h-framed-reading-refused-so-one-reading-remains` and
  `program-predicate-two-readings-are-different-digests`.

The three exceptions are named, closed and enumerated in the schema's `retention` registry:
`fragment` (only `program-predicate.nodeDigest`, recomputed at its `locatedBy` address inside the
retained rule program rather than stored twice), `derived` (only `capabilityManifestId`), and
`owner-retained` (only `owner-source-set[].ownerFileManifestSha256`, owned by security).

## 6. Codex's hypothesis about `nativeContextDigests` — confirmed, and closed

**Confirmed.** The old `close_run.walk` did treat every bare `*Digest(s)` 64-hex as a raw blob
SHA-256, and `plan.nativeContextDigests` is an H digest, so a Plan with a non-empty native context
set could not have closed under the old checker at all — every positive Run in `check-identity.py`
and every integration Run used `nativeContextDigests=[]`, and integration proved the native
context → Plan projection but never a complete Run. The same latent mis-typing applied to
`fact`/`subject-scope` `sourceUniverse`/`targetUniverse`, which the old checker did not examine at
all (they do not end in `Digest`), so a Run could carry arbitrary 64-hex universes with nothing
retained.

**Closed, after Codex caught my first attempt.** My first draft retained the frame and re-derived
the closure joins, but nothing more — and Codex's probe
(`/tmp/opensip-design-corrections/native-run-probe.v7/result.retry1.json`) executed the exact
counterexample: a context mutated so `moduleResolutionMode` contradicts
`honoredOptions.moduleResolution`, which `admit_native_context` refuses, could be **re-framed and
re-keyed into a complete admitted Run**. That was a genuine gap, not a labelling problem: a frame
proves **retention**, never **admission**, and my §3 sentence claiming otherwise was wrong and has
been removed. `close_run` now additionally re-runs the owning contract's own admission over the
retained bytes and the Run's own retained `closure2` descriptors —
`admit_native_context(language, retained_context, retained_closures)` must return zero refusals with
a matching digest and domain, and `bind_typescript_universe(retained_universe, that_admission,
retained_context)` must return `ADMIT` with a matching `sourceUniverse`. Either refusal becomes a Run
admission refusal carrying the native contract's own typed string. Nothing is re-executed: no
compiler, cargo, provider, repository or filesystem operation runs at Run closure. I re-ran **Codex's
own probe script**, unchanged except for output paths, against a fresh capture of the current tree:
it now reports `admitted: false`,
`AdmissionError:NATIVE_CONTEXT_ADMISSION:native.native-context-field-mismatch:moduleResolutionMode`.
Both their original result and this recheck are preserved as development evidence; the original
finding was correct and is not being relabelled.

The corrected representation is H-preimage-frame retention (§5) **plus owner re-admission**. A
complete Run with a non-empty native context set closes, using the **actual** native admission
functions over retained (small) compiler and stdlib closure trees:

- `native_evidence_model.typescript_native_context(...)` builds the descriptor;
  `admit_native_context('typescript', ctx, retained_closures)` must return zero refusals;
  `bind_typescript_universe(universe, admission, ctx)` must return `ADMIT`. No `ADMIT` flag is read
  by the identity closure — it re-derives everything it names from the retained frame.
- **Both** registered context domains close in the same Run: `native.context.typescript.v2` and
  `native.context.rust.v2` (the latter with its own closure-join table,
  `toolchain.rustcDevLlvmDigest` → kind `rust-dev-llvm`).
- Identity-side closure joins, derived from the frame alone: `toolClosure.closureId` must be a
  retained `closure2` of kind `toolchain`; `toolchain.typescriptStdlibMerkleRoot` /
  `toolchain.rustcDevLlvmDigest` prefixed with `closure2:` must be retained closures of kind
  `stdlib` / `rust-dev-llvm` whose recomputed identity equals them and whose complete trees are
  retained (every tree member's bytes and exact length); and every retained universe frame's
  `nativeContextId` must be `sha256:` plus a member of `plan.nativeContextDigests`.
- Source/config/context join: a single changed stdlib byte moves the stdlib `closure2`, the context
  identity, the universe identity and the `run2`. Check
  `changed-stdlib-byte-moves-context-universe-and-run`.
- **Snapshot source correspondence**, discharging a §3 promise that was previously prose-only: every
  `TypeScriptConfigProjectionV2.configGraphPaths` and `CargoConfigProjectionV2.replacedSnapshotConfigs`
  entry must be an inventoried snapshot path, and a non-null `lockfileIdentity` must name an
  inventoried path whose inventory `sha256` equals its `contentSha256`. The fixture snapshot now
  carries `tsconfig.json`, `tsconfig.base.json` and `package-lock.json`.
- **Re-frame-and-re-key negatives**, each asserting the native boundary's own refusal string via a new
  `rejects_because(name, fn, token)` helper, with a
  `reframe-harness-positive-control-closes` control so a refusal is attributable to the mutation and
  not to staleness: contradicting honored options; compiler package digest and runtime digest outside
  the tool closure; `libSelection` set mismatch; incomplete stdlib inventory; stdlib component digest
  not the retained tree's; compiler version not from the manifest; universe/context `allowJs` and
  `checkJs` mismatch; universe bound to unselected context bytes; config graph path not inventoried;
  lockfile path not inventoried; lockfile bytes not the snapshot bytes.

### Exact API for integration

```python
IM.h_preimage_frame(domain, descriptor) -> bytes
IM.retain_h_identity(domain, descriptor, blobs) -> str      # bare 64-hex; writes blobs[digest]=frame
IM.native_context_frame(domain, descriptor, blobs) -> str   # domain restricted to the context registry
IM.native_universe_frame(domain, descriptor, blobs) -> str  # domain restricted to the universe registry
IM.parse_h_frame(frame, domain_set) -> (domain, value, registry_row)
IM.predicate_node_at(emit_when_root, address) -> node
IM.predicate_child_addresses(node, address) -> [address, ...]
IM.cache_identifier(domain, key, objects, blobs, plan_id) -> 'cache2:…' | 'regen2:…'
IM.commit_inventory(run_id, objects, blobs) -> (record, digest)
IM.DIGESTS  # SCHEMA['x-opensip-digest-domains'], the normative registry
```

Host call sequence after `typescript_context_inputs(ctx, trees, universe)`:
```python
digest = IM.native_context_frame('native.context.typescript.v2', ctx, blobs)
assert digest == joined['nativeContextDigests'][0]
IM.native_universe_frame('native.semantic-universe.typescript.v2', universe, blobs)
```

### Native-side follow-up (I did not edit any native file)

Optional but recommended, for whoever owns `native/`: have
`admit_native_context` and `bind_typescript_universe` return the H **preimage frame** bytes
alongside `planNativeContextDigest`/`sourceUniverse`, so a host cannot mint the digest and forget to
retain the frame. Today the host must call `IM.native_context_frame` / `IM.native_universe_frame`
itself. Nothing is *unsound* without this — a forgotten frame refuses with
`EVIDENCE_UNAVAILABLE` at Run closure — but it is an avoidable footgun. No native change is required
for correctness, and none was made.

## 7. Tests and mutation sensitivity

`foundation/check-identity.py`: **141 → 275 checks, 0 failed, 126 new distinct check ids, 0 removed.**
Every pre-existing check id is retained and still passes; no earlier semantics were dropped.

Independent digest vectors. Three independent implementations agree: a hand-written canonical encoder
inside `check-identity.py` (which does not call `canonical.py`), `canonical.py` itself, and a fourth
encoder written separately in
`/tmp/opensip-design-corrections/digest-corrections-author.v1/probes/p2_vectors.py` from the §3
prose, whose outputs are embedded as literals:

```
program-predicate    d0402034ed9f6e2c4e113e36760a4889ec54b349b0a7951fcceb5bec8f591e09
finding-parameters   ec8b5959e7d27b01817b6eb830787c8dc02281cf8758f74bcfdf336b25d6a73e
stage-spec           056a6dbac737e36856e7e6cd6c27aae85869f058bc2ec436511fdf09256553c8
commit-inventory     d87ef7db470cd9d8531141beddaba1bb0d5ae3b82a07452e1ba7cab0f34c9a0b
owner-source-set     c6190a240894608b027e9c85ea4079a55847e66cd010b2090b84b50475a02975
H frame  (sample)    337ddc07b6ef1a161c63fc18e4c1a3900ccfc89a87a38952d3fe22740fb2badb
raw C(X) (same X)    06786637e56951a14b4ae81e1328fc97914dcec404fb80b14253b89e554c72c5
```
The five record vectors are pairwise distinct, and every single-field mutation of each moves its
digest. The last two lines are the discriminating pair: same payload, different representation,
different digest.

Negatives, all through the **actual graph checker** `close_run`, not a schema sample:

| Class | Checks |
|---|---|
| altered record | `program-predicate-altered-node-digest`, `-wrong-operation`, `-wrong-address`, `-wrong-rule`, `-foreign-rule-program`; `finding-parameters-message-code-must-join`, `-not-a-registered-record`, `-open-value-type`; `stage-spec-output-domains-must-join-the-stage`, `-foreign-plan`, `-unselected-producer`; `cache-output-schema-cannot-diverge-from-the-stage-spec`, `cache-producer-cannot-diverge-…`, `cache-foreign-plan-refused`; `native-context-frame-bytes-must-hash-to-the-identity` |
| missing preimage | `program-predicate-missing-preimage-is-retention-loss`, `finding-parameters-missing-preimage-…`, `stage-spec-missing-preimage-…`, `stage-spec-missing-output-schema-bytes`, `cache-missing-stage-spec-bytes`, `native-context-frame-missing-is-retention-loss`, `native-context-stdlib-closure-must-be-retained`, `native-context-tool-closure-must-be-retained`, `plan-named-context-without-a-retained-frame-refuses` |
| wrong preimage / wrong representation | `program-predicate-h-framed-reading-refused-so-one-reading-remains`, `h-frame-refused-where-a-canonical-record-is-required`, `native-context-raw-payload-sha-is-not-an-h-identity`, `native-context-unregistered-h-domain-refused`, `rule-program-must-compile-from-the-selected-policy` |
| hidden input | `program-predicate-hidden-child`, `program-predicate-invented-count-limit`, `stage-spec-hidden-parameter`, `universe-must-bind-a-plan-selected-native-context`, `universe-context-must-stay-plan-selected-when-the-plan-drops-it`, plus the retained `review-hidden-predicate-input`, `review-extra-authoritative-coverage-root`, `review-finding-foreign-fact` |
| law coverage | `digest-law-covers-every-64-hex-field` (57/57), `digest-law-has-no-unregistered-representation`, `digest-law-names-{programPredicateDigest,parameterDigest,stageSpecDigest,outputSchemaDigest,inventoryDigest}`, `digest-law-stage-spec-is-one-record-two-sites`, `digest-law-registry-domains-cover-every-ref-enum`, `digest-law-record-registered-*` |
| Rust universe path | `rust-universe-domain-is-registered`, `rust-universe-binding-is-declared-required-and-missing`, `rust-universe-refuses-until-native-provides-its-binding`, `rust-universe-crate-root-must-be-inventoried`, `rust-universe-lockfile-bytes-must-be-the-snapshot-bytes`, `rust-universe-must-agree-with-its-context-{dependency-set,unified-features}`, `typescript-universe-cannot-bind-a-rust-context` |
| native re-admission (Codex probe v7) | `reframe-harness-positive-control-closes` (control), then `reframed-context-contradicting-honored-options-refused`, `-compiler-digest-not-in-tool-closure-`, `-runtime-not-in-tool-closure-`, `-lib-selection-set-mismatch-`, `-lib-selection-order-refused-by-the-native-schema`, `-stdlib-inventory-incomplete-`, `-stdlib-component-digest-mismatch-`, `-compiler-version-not-from-manifest-`, `reframed-universe-context-overlap-mismatch-{allowJs,checkJs}`, `reframed-universe-bound-to-other-context-bytes-refused`, `reframed-context-config-graph-path-not-inventoried`, `reframed-context-lockfile-bytes-not-the-snapshot-bytes`, `reframed-context-lockfile-path-not-inventoried` — each asserting the **exact** refusal string via `rejects_because` |
| positive complete Runs | `native-context-nonempty-plan-closes`, `native-context-both-registered-domains-close`, `native-context-digest-is-the-native-admission-value`, `program-predicate-positive-run-closes`, `finding-parameters-positive-run-closes`, `stage-spec-positive-run-closes`, `owner-source-set-positive-run-closes`, `receipt-inventory-*`, all four `valid-replay-*` / `commit-*` |

The fixture `replay` is genuinely independent: it parses the **admitted `PolicyDocumentV1`**,
compiles the `RuleProgramV1` itself, addresses node `p` itself, and recomputes the
`program-predicate` record and witness from scratch. It reads no claimed outcome, no claimed program
digest and no claimed witness.

## 8. Suite results (intermediate, unpinned)

Both Codex and I were editing while these ran. `foundation/source-pins.v1.json`,
`native/source-pins.v2.json`, `workflows/source-pins.v1.json` and `security/source-pins.v1.json`
are all currently **off their pins**, for my four files and for Codex's concurrent
`canonical.py` / workflow-schema / native-schema / security-schema edits. **I did not repin
anything, and I did not regenerate any in-repo report.** Everything below is therefore intermediate
evidence measured against working-tree bytes, not a pinned reproduction.

| Suite | Result | How run |
|---|---|---|
| `foundation/check-identity.py` | **275/275** (was 141) | direct, in-repo |
| `foundation/check-foundation.py` | 231/231 | direct, in-repo |
| `foundation/check-product-configuration.py` | 28/28 | direct, in-repo |
| `foundation/check-product-quality.py` | 24/24 | direct, in-repo |
| `workflows/check_workflows.v1.py` | 1253/1253 | direct, in-repo |
| `check-integration.py` | **355/355, 0 failed** | **disposable copy**, with `integration-fixtures.py` re-copied from my current builders; the in-repo copy is one revision behind (see §8) |
| `native/check_native_evidence.v2.py` | 132/132, 60 cells, 0 qualified, 0 open objects | **disposable copy** with pins regenerated in that copy only |
| `security/check-security-lifecycle.v1.py` | 456/456, 10/10 sweeps | **disposable copy** with pins regenerated in that copy only |

`foundation/run-reference-checks.py` refuses to execute at all while pins are stale, which is correct
behaviour; its expected aggregate after repinning is **231 + 275 + 28 + 24 = 558** (was 424).
`foundation/identity-report.json` and `foundation/validation-report.json` are pinned reports I do not
own and did not touch; they must be regenerated by their owner when the tree settles.

Integration: my early interface note
(`/tmp/opensip-design-corrections/digest-corrections-author.v1/interface-note.v1.md`) flagged
`integration-fixtures.py` and `check-integration.py` as needing adaptation. **Codex adapted both
concurrently**, and at that point integration passed 353/353 with all 14 shared declarations
AST-identical to mine. My builders then changed again to close Codex's native-admission
counterexample (§6) and to add the `TS_SOURCES` snapshot rows, so the in-repo
`integration-fixtures.py` is now **one revision behind and integration fails in-repo** with
`NATIVE_CONTEXT_PATH_NOT_INVENTORIED:tsconfig.base.json`. This is a stale copy, not a design
disagreement: in a disposable copy where only `integration-fixtures.py` is replaced by a shim
delegating to my current builders, `check-integration.py` passes **355/355, 0 failed**, with **no
change to `check-integration.py` itself**. `AUTHOR-REPLY-TO-CODEX.v1.md` §6 lists every declaration
to re-copy, the `build()` signature, the module prelude and the answers to Codex's specific
questions. I did not edit any integration file.

## 9. Limitations, honestly stated

- **I am not the reviewer and I award nothing.** No self-acceptance. `readinessChanged: false`;
  condition 5 remains NOT MET; the v6 verdict stands until a fresh independent review of the changed
  bytes.
- All suite numbers above are **intermediate and unpinned**, taken during concurrent editing. Native
  and security were run on disposable copies with pins regenerated **in the copy only**.
- The reference fixture now carries a **real** `PolicyDocumentV1` and its compiled `RuleProgramV1` in
  the product DSL, so the record shapes, digests and joins are exercised as specified — but its
  *interpreter* is small, evaluating a single-atom subset. It qualifies neither the declarative
  language nor a native Coverage or relation payload registry. §3 of the contract now says this
  instead of the previous, now-inaccurate "not the product DSL".
- Relation and Coverage payload schema **registration** remains the native/workflow adapter boundary.
  Identity checks retention, canonicality, that the retained schema document constrains the payload
  directly (so a multi-record bundle cannot pass vacuously), and validation under it — not which
  schema is the right one for that relation.
- Native context and universe **internals** beyond the joins in §6 (option agreement, lib selection
  order, stdlib inventory completeness, universe/context field agreement) are admitted at the native
  boundary before a Plan exists. Identity requires that the retained bytes are exactly the bytes that
  boundary admitted, which frame admission establishes; it does not restate those rules.
- Closure trees in the fixture are small synthetic files. Real compiler/stdlib trees, OS durability,
  fsync, SQLite, process death and cross-machine replay remain **release gates**, unchanged.
- `owner-source-set` depends on the generic `{"by":[...]}` `x-opensip-order` form Codex added to
  `canonical.py`. If that form is withdrawn, the annotation must change with it.
- The `x-opensip-order` vocabulary paragraph in §3 now lists `canonical-order`, `utf8` and the
  `{"by":[...]}` form because `canonical.py` implements them. That paragraph and `canonical.py` must
  be kept in step; `canonical.py` is not mine.

## 10. Remaining joins I did not close

1. **`cache-key.inputRefs` payload-domain references.** `coverage-payload`, `import-payload` and
   `fact-payload` reference digests are declared as resolved through the owning object's
   `payloadSchemaDigest`, but a cache key is not reached from a Run, so nothing in the Run closure
   exercises that resolution. Registered and stated, not exercised.
2. **`availability.missingRefs`.** Operational disclosure; validated and ordered, not closure-joined.
   Unchanged from before, and correct as far as I can tell, but I did not deepen it.
3. **`owner-source-set` against security.** Identity re-checks the projection's shape, order and
   uniqueness and joins the digest; it does not re-run security's `admit_repo_execution_grant`. A
   cross-unit check that `integration-host-model.owner_digest(grant['owners'])` equals the
   `ownerSourceDigest` a Plan's semantic grant carries would close the last hop, and belongs in
   integration.
4. **The Rust semantic-universe path — a REQUIRED native-side follow-up, not optional.** Codex was
   right that my earlier draft of this section was wrong: native §11 already registers
   `native.semantic-universe.rust.v2` and §2.1 names `RustUniverseV2ResolvedInputs`, so leaving it
   out of the identity registry would have refused the promised Rust path as unregistered. It is now
   registered, with its context-language, context-agreement
   (`dependencySourceSetId`/`unifiedFeaturesId`/`preparedOutputSetId`) and snapshot joins
   (`crateRootPaths`, `Cargo.lock`) specified and enforced. **But it still cannot seal a Run**, and
   deliberately so: the native reference model provides no `bind_rust_universe` entry point, and
   native §3.3/§11 does not name a producing domain for
   `RustUniverseV2ResolvedInputs.configProjectionSha256`. Rather than admit a Rust universe unbound —
   which would be exactly the weakness Codex's v7 probe just made me fix for TypeScript — identity
   refuses it with the typed cause `NATIVE_UNIVERSE_BINDING_UNAVAILABLE:bind_rust_universe`, and the
   registry row carries `binding.status = REQUIRED-NOT-YET-PROVIDED-BY-THE-OWNING-CONTRACT` with the
   reason. Checks `rust-universe-domain-is-registered`,
   `rust-universe-binding-is-declared-required-and-missing`,
   `rust-universe-refuses-until-native-provides-its-binding` and four Rust join negatives assert
   this. **Handing back explicitly:** both items need `native/` files I do not own. Until they land,
   Rust facts and Coverage cannot seal a Run, and the D-371 TS/JS/Rust design is not complete. I am
   not claiming otherwise.
5. **Nested native semantic identities.** `dependencySourceSetId`, `unifiedFeaturesId` and
   `preparedOutputSetId` appear inside both the Rust context and the Rust universe. Identity now
   joins them for context/universe agreement, but does **not** retain or re-admit their own H frames,
   because that needs their record selectors registered in a domain set and the owning native
   contract has not named record shapes for `native.dependency-source-set.v1`,
   `native.unified-features.rust.v1` and `native.prepared-output-set.v3` in a form I can register
   without inventing them. This audit belongs with item 4.
6. **`node_modules` / read-set members.** I join a native context's config graph and lockfile to the
   snapshot inventory, but not `nodeModulesLayoutDigest` or resolution read-set members: whether such
   a member must be snapshot-inventoried is a native discovery question, and I would rather leave it
   named than assert it.
7. **Rust native context closure trees.** The Rust domain closes through a complete Run with my own
   small `rust-dev-llvm` and `toolchain` closures, but no Rust *universe* domain is registered or
   exercised (only `native.semantic-universe.typescript.v2` exists today). When native registers a
   Rust universe domain, add it to `x-opensip-digest-domains.domainSets['native-semantic-universe']`.
8. **Pins and reports.** Four files changed, nothing repinned, no report regenerated. Whoever owns
   the pins and `foundation/identity-report.json` / `validation-report.json` must update them, using
   the aggregate in §8.

## 11. Retained artifacts

```
/tmp/opensip-design-corrections/digest-corrections-author.v1/
  interface-note.v1.md            early interface note (integration adaptation)
  handoff.md, handoff.json        this handoff
  patch_schema.py                 the schema annotation patch I applied
  probes/p0_sweep.py              pre-change enumeration of every 64-hex field
  probes/p1_coverage.py           annotation coverage sweep (57/57, 0 missing)
  probes/p2_vectors.py            fourth independent canonical encoder + the literal vectors
  probes/p3_codex_v7_recheck.py   Codex's own v7 probe, re-run against the corrected bytes
  AUTHOR-REPLY-TO-CODEX.v1.md     reply to CODEX-INTEGRATION-NOTE.txt / CODEX-ORDER-INTERFACE.txt
  runs/identity.json              252/252
  runs/f.json, w.json             foundation 231, workflows 1253
  runs/integration.json           353/353
  runs/security.json              456/456 (disposable copy)
  scratch2/, scratch3/            disposable trees used for pin-regenerated native/security runs
```
