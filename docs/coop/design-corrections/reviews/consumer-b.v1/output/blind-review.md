# OpenSIP DR-011-R10 — blind consumer reconstruction (consumer-b.v1)

**Verdict: CHANGES_REQUIRED**

Reviewer: actual Claude, fresh blind session. I authored none of this design, read
no author reference model, fixture, golden, report or prior review, and consulted
no directory other than `/tmp/opensip-design-corrections/consumer-b.v1/subject`.
Everything numeric below was computed by code I wrote from the prose, in
`output/work/`, with results in `output/vectors/`.

This is a *design-reference* reconstruction. Nothing here awards readiness,
qualifies a platform, or authorizes implementation.

---

## 1. Input custody and hash verification

Manifest: `subject/consumer-input-manifest.json`, declaring a subset of the
accepted parent subject `ccb2311ddbcaea7e8bd540030621c982fa6757792721095a505e4e47652c74cf`.

| Check | Result |
|---|---|
| Files declared | 42 |
| SHA-256 + byte length verified | **42 / 42 exact** |
| Undeclared files present in the kit | **0** |
| Total declared bytes | 1 951 574 (verified) |
| Manifest file SHA-256 | `0df93abd52a89674a1c4f93eb053675e3d057970dcdfa9831b8b418a6ab2f440` |
| My subset digest (SHA-256 over sorted `path\0digest\0`) | `11a21bb701b00434e97647504c144445de7a3c0355cbf9ba08611e888b27e90a` |

Custody is clean. Two documents that the contract index names as governing are
**not in the kit** — the correction record
(`docs/coop/design-corrections/README.md`, the "crosswalk [that] names exact
successor selectors and retained obligations") and the readiness register
(`docs/v2/architecture/08-decision-and-readiness-register.md`, "the sole
completion checklist"). Their absence is *correct* for a blind design read: the
register grants readiness and the crosswalk records acceptance, neither of which
I may consume. I record it as scoped input-custody (S-5b) only because it means
successor-versus-inherited *disposition disputes* cannot be adjudicated from
these bytes alone. It did not block any reconstruction below.

---

## 2. Reconstructed end-to-end chain

I can reconstruct the full path an implementer needs. Owning selectors in
brackets.

**Discovery → typed config/source.** Zero-config discovery is deterministic over
`lstat`/ACL results through `O_NOFOLLOW` handles, with no env, `PATH` or `HOME`
[security S3]. Directory custody, config-file custody, the ≤256-level upward
walk, the boundary precedence (config > VCS marker > home > fs root > mount) and
the decision that a nested config *is* a project boundary are all closed
[security S3, ADV-3]. Language *workspace units* are a second, different thing
from *authority roots*: markers `Cargo.toml` / `package.json` / `tsconfig.json` /
`jsconfig.json`, automatic discovery, pruning by exact path segment, the 4096
first-party unit cap [security S3; native §1.4]. Security exports
`AdmittedBoundaryInventoryV1` and native `discover_units` consumes it unchanged
and must reproduce the same unit set, or refuse
`native.boundary-inventory-mismatch` [security S3 U-8; native §13 H-8]. Discovery
observations fold into a trusted `defaults` layer; then global → project →
interactive-local → explicit flags override, arrays replacing atomically and
records merging by named field [admission §1.1, §4]. The environment semantic
layer is empty; CI never probes the local carrier.

**Snapshot.** The host takes the *same* admitted boundary inventory used by
native discovery, removes nested-repository / nested-project /
custody-excluded paths *before opening or hashing source bytes*, then applies
per-file custody and exact hashing [identity §6 "Snapshot capture consumes the
same admitted boundary inventory"]. `snapshot2` = ProjectId + sorted source
inventory + `resolvedConfigDigest` + `scopeDigest` + `vcsDigest` [identity §3;
`identity-schemas.v2#/$defs/snapshot`].

**Invocation / step / attempt.** One host request = one `RequestId`, minted
*before* admission and retained on refusal [identity §2]. ≤64 ordered acyclic
steps, `StepId` = zero-based position, ≤3 attempts per step, each attempt a fresh
`ExecutionId` under EXECUTION-ID-V1 [workflows §1;
`c2-plan-stage-schema.v4.json $.planIntent.wireTypes.executionId`]. Only
`analysis` and `verify` seal or link a Run; eleven other kinds are operational
and mint none. The step DAG and the derivation DAG (`exec-plan2`, ≤1024 stages)
are disjoint: a step never depends on a stage, a stage never references a step
[workflows §1; `invocation-record.schema.json#/$defs/DerivationBinding`].

**Plan.** `plan2` binds snapshot, capability manifest (id *and* bytes digest),
semantic closures, analysis spec, resolved config, native contexts, imports,
policy, waivers, scope, budget and semantic grant [identity §3]. Waiver expiry
and duplicates resolve *at Plan construction* against the admitted trust clock,
so the evaluator never reads a wall clock [workflows §5; identity §3].

**Native facts / Coverage / view.** Providers contribute typed facts and
`CoverageResultV3`; the host mints `fact2` and `coverage2` by exact
payload-schema/payload digest. The load-bearing correction is that the
*examined* partition and *resolution completeness* are two different claims:
`coverage=complete` with `resolutionCompleteness.state=incomplete` is the honest,
expected entry, and a zero unresolved-edge count never implies `complete`
[native §4.1–§4.3, RC-2]. `view2` joins Plan, scopes, facts, Coverage, producer
and schema closure.

**Evaluation and proof verification.** The evaluator is pure and consumes only
Plan-bound, schema-admitted inputs; every consumed datum is in
`evaluationInputRefs`; no hidden lookup [identity §4]. Predicates are strong
Kleene with the exact incomplete-case table. Witness facts must be *exactly*
those the program selects over the complete admitted view — never a producer's
chosen subset. Before sealing, the host **independently replays** the program
against the retained closure and compares the complete normalized result, not a
producer checksum.

**Evidence / Seal / Run.** `evidence2` (Plan, views, Coverage, imports, findings,
proof) → `seal2` (adds evaluator, policy, verdict) → `run2` (ProjectId, snapshot,
Plan, evidence, seal, capability manifest). The graph is acyclic by construction:
proof carries no evidence/seal/Run id [identity §3].

**Durable receipt and current availability.** Default `opensip`/`analyze` is
DURABLE_AUTHORITATIVE with retention origin DEFAULTED disclosed before first
write [identity §5, CD-RT-5]. Commit order is: validate closure and replay proof
→ publish immutable blobs by digest with fsync → **one** synchronous ledger
transaction inserting Run manifest, object refs, availability generation, pins
and a commit receipt → only then acknowledge. A failure before step 3 publishes
no authoritative Run; a crash after ledger commit is `durability-undetermined`,
exit 4. Sealed assurance (`verified` / `verifiable` / `replayable`) is
**immutable**; current availability (`retained` / `partial` / `expired` /
`purged` / `corrupt` / `unavailable`) is a separate monotonic-generation record
that may improve, and a query reports both [identity §5].

### Semantic identity vs operational authority — the distinction is clean

| Semantic (enters `run2`) | Operational (excluded from `run2`) |
|---|---|
| ProjectId, snapshot, config/scope/spec/grant digests, closures, facts, Coverage, views, witnesses, proof, findings, policy/waiver digests, capability manifest | RequestId, ExecutionId, StepId, wall clocks, PIDs, credentials, authorization nonces, receipts, signer key, namespace locator, commit sequence, output destinations |

I verified this mechanically (vector **B7**): two attempts with different
RequestId, ExecutionId, wall clock, receipt signer, namespace and commit sequence
share one `run2`, and *no* operational token appears anywhere in the sealed
closure. The private namespace UUID is an operational storage locator bound
one-to-one to ProjectId and never enters a semantic identity [identity §2].

Mutation vs analysis steps are also cleanly separated. `analysis`/`verify` seal
Runs; `repair-apply`, `import`, `baseline adopt|export|upgrade`, `policy init`,
`waive`, `review join`, `purge`, `core`/`store` transitions are mutations with
receipts and no Run; `test-execution` has *no Plan at all*, and its observations
enter an analysis only through an admitted `import2` carrying its execution
provenance [identity §3; workflows §1, §7; security S10].

---

## 3. Independent vectors

I wrote `output/work/cb_canonical.py` (admission + canonical encoder + `H`)
entirely from prose, then built descriptors and expected results myself.
**106 vectors, 106 pass.** Full machine-readable results:
`output/vectors/vector-results.json`; the Run graph:
`output/vectors/run-descriptor-graph.json`.

| Series | Content | Result |
|---|---|---|
| A (31) | admission, canonical encoding, `H` framing, CAP-MANIFEST-ID-V1 | 31/31 |
| B (10) | complete minimal positive Run graph, semantic vs operational change | 10/10 |
| C (7) | refused hidden / mismatched / tampered inputs | 7/7 |
| D (24) | public terminations, positive and negative branch controls | 24/24 |
| E (23) | baseline audit, comparison, authorization, registry/inventory joins | 23/23 |
| F (11) | reproducible probes of gaps that force invention | 11/11 |

### 3.1 Exact admission (A1–A6, A18)

Duplicate keys, `1.0`, `1e0`, `1E0`, `1.0000000000000001`,
`9007199254740991.1`, `-0`, `NaN` and lone surrogates are all refused *before*
deserialization. Integer boundaries hold exactly: 2^64−1 and −2^63 admit, 2^64
and −2^63−1 refuse. `true` does not satisfy `const:2` and a decoded `1.0` does
not satisfy `const:1`.

**A18** is a real cross-document result: `exec1_<32hex>\n` is **refused** by the
product schemas' `(?![\s\S])` and **admitted** by the retained C-2 grammar's
bare `$`. The product resolves this correctly, and I confirmed the discipline is
universal: across the 12 product-successor schema documents, **335 patterns, 0
bare `$`**; only the 3 retained security-v8 documents (52 patterns) use `$`.
That is disciplined authorship, and it is why S-2 below is narrow rather than
systemic.

### 3.2 Canonical encoding (A7–A16)

Key ordering is by UTF-8 bytes including non-BMP (`a`, `b`, `～`, `😀`). The
escape set is exactly as specified — slash, U+007F and U+2028 unescaped, controls
as lowercase `\u00xx`. NFC and NFD mint different identities (no normalization).
Depth 32 admits, 33 refuses, with the root container counted as 1. Set arrays are
reorder-invariant and refuse duplicates rather than silently deduping.
Inventories sort by logical path (I verified this is genuinely *different* from
canonical-byte order). Stage arrays require contiguous ordinals. Predicate proofs
sort by `(ruleId, subjectId, predicateId)`. The `H` frame reproduces
`"opensip.product.v1" || 00 || D || 00 || u64be(len C(X)) || C(X)` byte-for-byte,
and domain separation holds on an identical descriptor.

**A17 — the retained capability-manifest recipe verifies.** I implemented
CAP-MANIFEST-ID-V1 from the one-line recipe alone and it reproduces **all seven**
published `committedBytesHex` → `capabilityManifestId` values in
`delivery.v4.json $.derivedFrom.operations[17].value.vectors.byId`, and all seven
`committedBytesSha256`. The retained DELIVERY v4 recipe is sound and correctly
restated in identity §3.

### 3.3 The complete minimal positive Run graph (B1–B10)

I built one from my own synthetic trusted observations: two TypeScript source
blobs, a scope descriptor, a resolved configuration, a VCS observation, three
signed closures, a capability manifest, a TS semantic universe, an analysis spec,
a semantic grant, a policy document with one non-gating `exists` rule, a resolved
empty waiver set, a compiled rule program, a subject scope, one `references@
resolved-binding` fact, a `CoverageResultV3` payload with
`resolutionCompleteness.state=complete`, a view, a 3-stage execution plan, a
predicate witness, a finding fingerprint, a finding, a proof bundle
(`verdict: pass`), evidence, a seal and a Run.

Everything validates against the normative closed schemas
(`identity-schemas.v2.json`, `native-evidence.schemas.v2.json#CoverageResultV3`
and `#TypeScriptUniverseV2ResolvedInputs`) with **zero** errors, and my
`close_run` closure checker — written from identity §3/§4's join rules — returns
zero refusals.

```
projectId        prj1-5d035e51f45cd0aef7d0848c61b7fc2c36ec78913678c0a6376e90f3869e8637
snapshot2        6a921f12bea1d22cf91f6f9a280136caccf1b765ef2c7216cd08b80609af6436
plan2            33c1c8b105290d4f074922fe5f0df97d6bf8d7894ab8021759ebd00011bf2a5a
scope2           63288ae366347a06193876211df947604edead8fe54e5f4276e91bf15c621925
fact2            413575a9d00a97cb16ffbfc3466c091e64ed331d85ac94bd2e677ee5f185e23a
coverage2        8aefc1eaa89874e733994c2674bd066b48936e8f87fa79889ba247803377f9f4
view2            be657df61e5f2c1fd496255aa3b6c4134f9d1f1767f2d797c1e081a8a5027d57
exec-plan2       4a752e5f7c751f124a7aa1d3e0c460331588d6bde7a4a16c7bbfb3da0b5ec7ce
finding-key2     020493edeafe3f6c0ce57befb8351e05b0b890c0d8cf4cdb4f1e85d8732d81de
finding2         23d8aae0809c7dc253a083646f38b31a8779bb2f2d51c6f4e86635190069cf4d
proof2           f983360894d8d5c246588f4c1e8bb8d6756e14fd54f390de11f7952543fedef7
evidence2        af7e0b7fa2788c229c35f920dca538e68c98ad75336becc55c09dbe44a4bec85
seal2            0f6063cb0aa2048844a432bff0006fd45ade07d488780ea9936fcb6b747bcf28
run2             a380ea4856817fae206f29209075d7857a74909a08b16f41fc7061b7d07caa85
```

**These values are conditional on two invented inputs** (M-1 and M-2 below) and
on one stated assumption (M-4). They are *not* an oracle; they are what my
reading produces, published so the divergence is auditable.

Semantic vs operational: changing `fact.confidenceMillionths` by one propagates
`fact2 → view2 → evidence2 → seal2 → run2` (B5); changing `snapshot.vcsDigest`
propagates `snapshot2 → plan2 → run2` (B6); changing every operational identity
changes nothing (B7). B10 confirms `cache-key` and `regeneration-key` have
byte-identical descriptor schemas and are separated *only* by the `H` domain —
which works, and is why the domain-framed preimage matters.

### 3.4 Refused hidden and mismatched inputs (C1–C7)

- **C1** A well-formed, hash-valid `fact2` cited by a finding but outside the
  evaluated view is refused. The forged graph is *schema-valid*; only the closure
  join rejects it. This is the exact "hidden finding evidence" case.
- **C2** An `import` in `evaluationInputRefs` that Plan never selected is refused
  as an extra authoritative input root.
- **C3** A fact bound to a different `snapshot2` is a refused cross-source join,
  again schema-valid and hash-valid.
- **C4** A witness naming a strict subset of the program-selected facts is
  refused — the producer cannot choose its own witness set.
- **C5** One byte of witness tampering moves `witnessDigest` and therefore
  `proof2`, `evidence2`, `seal2` and `run2`.
- **C6** A caller's `verified: true` cannot be carried: `run2` is
  `additionalProperties:false`.
- **C7** A plain SHA-256 of the committed manifest bytes does not equal the
  CAP-MANIFEST-ID-V1 value, so a supplied `capabilityManifestId` is detectably
  not authority.

### 3.5 Public terminations and comparison artifacts (D1–D24, E1–E23)

Sixteen positive terminations and eight negative branch controls, all validated
against `common.schema.json#/$defs/StepTermination`. The branch contract is tight
and enforced: `success` with an `errorCode` refuses; `operational-failed` without
a non-`none` `faultCause` refuses; `policy-failed` with neither `runId` nor
`authority=ephemeral` refuses; `authority=ephemeral` *with* a `runId` refuses;
`indeterminate` with an `errorCode` refuses; an unregistered `DomainDetailCode`
refuses; an unknown field (`exitCode`) refuses.

The event-position distinctions the contracts insist on are all representable and
all distinct:

| Situation | Class / exit | Owner of the decision |
|---|---|---|
| Purged evidence, query needs actual proof, **before** evaluation | request-rejected 2, `evidence.purged` | identity (retention/availability) |
| Retained bytes unreadable **during** a selected operation | operational-failed 4, `HOST.IO_FAILURE`, `evidence.missing` | identity (custody observation boundary) |
| Admitted-but-incomplete native inputs | **authoritative Run**, indeterminate 3, deficiency in the `coverage2` record | native (fault law §10) + host D9 |
| Worker fault / protocol violation | operational-failed 4, **no facts, no Coverage, no Run** | native (§10 `stage_authority`) |
| Required renderer fails after commit | operational-failed 4, `runId` retained, Run not rewritten | workflow (§8 delivery law) |
| Optional export sink fails | success 0 | workflow (egress never changes a verdict) |
| Doctor report produced with defects | success 0, `DOCTOR.DEFECTS_FOUND` | workflow §8 / security S11 |
| CI backup-managed root, no explicit choice | request-rejected 2, `storage.backup-choice-required` | security S3.1 admission + identity §5 |

Comparison (E1–E8): I built four schema-valid `ComparisonResultV1` instances and
three negative controls. The most important is **E1** — a current-baseline audit
with **zero entries on both sides** that still returns `verdict: indeterminate`
because a gating rule's required evidence was lost. That is the property that
makes the audit gate honest: entry counts cannot prove a finding's absence
[workflows §12]. **E2** covers whole-comparison indeterminacy (unmapped project,
zero entries, typed remedy). **E3** covers the deliberately conservative evidence
axis: a replaced import of the *same* kind is `INDETERMINATE`
(`evidence-content-changed`), never a claimed regression, even under
`full-current`. **E4** covers a changed detector with no current-trusted E0
pivot: E0 `unavailable`, entry `INDETERMINATE`, and B is never substituted for
E0.

### 3.6 Three joins that hold exactly (positives worth recording)

- **E19** The closed `public-detail-registry.v1.json` (270 records) and
  `common.schema.json#/$defs/DomainDetailCode` (270 members) are **exactly
  equal**, both sorted, with **zero** internal decision aliases leaking into the
  public enum. The §12 drift-check obligation is satisfied in these bytes.
- **E23** The §8 SARIF parity MUST holds exactly: `default`, `analyze`, `audit`
  and `repair-verify` are the four SARIF commands, and each declares all seven
  common parity fields. Zero omissions.
- **E20** Security S9.2 states as an open obligation that "the current
  nine-field, three-operation workflow schema cannot express a store operation".
  It is **already discharged** in these bytes:
  `invocation-record.schema.json#/$defs/CoreTransitionIntentV1` has 11 required
  fields and all five operations including `store-migrate`/`store-rollback`.

---

## 4. Issues

### MUST — these forced me to invent design, or make a conforming host unbuildable

**M-1. `subjectScopeCommitment` has no producing recipe.** *(vector F3)*

It is a required field of `CoverageKeyV2` **and** of `ExaminedUniverseV1`
(`native-evidence.schemas.v2.json#/$defs/CoverageKeyV2`, `#/$defs/
ExaminedUniverseV1`), so its value is inside the Coverage payload whose
`payloadDigest` mints `coverage2` → `view2` → `evidence2` → `seal2` → `run2`. No
document in the kit says how to compute it:

- Native §0 marks `c2-plan-stage-schema.v4.json $.coverageKey.key[subjectScope
  Commitment]` **Retained**, and that retained selector's own text is
  `"boundHere": "SHAPE ONLY; computation and verification stay deferred
  (R1-C2-03)."`
- The same document's published values carry
  `"This is an EXAMPLE ENCODING for the fixtures only. It is NOT a claim about
  how a product computes a real subject-scope commitment; that remains owned by
  the retention/evidence surface."`
- Identity §3's auxiliary-digest paragraph enumerates producing rules for
  `resolvedConfigDigest`, `scopeDigest`, `analysisSpecDigest`,
  `semanticGrantDigest`, `vcsDigest`, native-context/import/policy/rule-program/
  waiver-set/witness digests, blobs, inventories and schema documents — and does
  not mention this one.
- Native §11's identity-domain list has no member for it.

So the "retention/evidence surface" that C-2 deferred to never picked it up. Two
plausible recipes (`H` over the `scope2` identifier -> `sha256:2f58a507…145c`;
SHA-256 over the canonical subject array -> `sha256:b2248445…6d5c`) produce
different `coverage2` (`782defac…7885` vs `e8b2cd2d…4fee`) and therefore
different `run2`. I
invented one to build the graph, marked `INVENTED-subject-scope-commitment` in
the retained output. **Required:** state the producing recipe in identity §3's
auxiliary-digest list or as a native `H` domain, and say explicitly how it
relates to `scope2` (identical suffix? independent commitment? both are
defensible today).

**M-2. The TypeScript native context is never defined, but is required and
identity-bearing.** *(vector F4)*

`TypeScriptUniverseV2ResolvedInputs.nativeContextId` is a **required**
`sha256:<64hex>` field, and the TypeScript universe key is what keys `fact2`,
`subject-scope` and `CoverageKeyV2`, and what populates
`plan.nativeContextDigests`. But:

- The only native context record is `NativeContextV2`, which native §2.3 titles
  **"(Rust)"** and whose closed required fields are Rust-only (`targetTriple`,
  `hostTriple`, `toolchain`, `toolClosure`, `baseCfg`, `resolverVersion`,
  `dependencySourceSetId`, `unifiedFeaturesId`, `preparedOutputSetId`,
  `configProjection`).
- Native §11's domain list contains `native.context.rust.v2` and no TypeScript
  counterpart.
- Native §2.2 lists `nativeContextId` under "Added" without saying what it
  identifies for TypeScript.
- Compounding it: identity §3 and native §14 both assert that "native-context
  schema 2" carries **`typescriptStdlibMerkleRoot`** (defined as the 64-hex
  suffix of the `closure2` identity for `kind=stdlib`). I searched every closed
  native schema: `typescriptStdlibMerkleRoot` appears in **no** definition. The
  recipe exists; the record to hold it does not.

I invented `INVENTED-typescript-native-context`. **Required:** add the closed
TypeScript native-context descriptor and its `H` domain (presumably
`native.context.typescript.v2`), carrying `typescriptStdlibMerkleRoot`, and
correct the two contracts that already describe its contents.

**M-3. The canonical encoder cannot decide which arrays are sets.** *(vectors F2,
F2b)*

Identity §3 says "Arrays whose semantics are sets are sorted and unique by
canonical item bytes", then names exactly four exceptions (inventories by logical
path; predicate proofs by triple; stage arrays by ordinal; ordinal dependency
arrays numerically) and one priority array (`allowedScopes`). Every other array
in every registered payload, policy and native document is unclassified, and
there is no machine-readable discriminator: `uniqueItems` cannot serve, because
`execution-plan.stages` and `closure.tree` both carry `uniqueItems: true` while
§3 gives them a *different* order.

This is not theoretical. `PolicyDocumentV1.rules` declares "sorted ascending by
ruleId UTF-8 bytes" and `RuleProgramV1` hashes "ordered rule programs"
[workflows §5], while a rule object's canonical bytes sort first on `emitWhen`.
With two ordinary rules (`a.first` with `exists`, `b.second` with
`count-at-most`), the set reading and the declared-order reading produce
**different** `policyDigest`:

```
set reading            5ee54b80b34a1f2a8d425ffa0f5d4f541d12390bd6ae32a40e5f1531e21d5582
declared-order reading 4ffa33cc95a0c8d3e7c58054212fd2bdbce13039ccf19f97171175d73620b622
```

`policyDigest` enters `plan2` and `seal2`, so this diverges `run2` for the same
policy file. Neither array carries `uniqueItems`, so no heuristic rescues it.
**Required:** either (a) add a per-field ordering table covering every array in
every digest-bearing document, or (b) state one closing default (e.g. "an array
is a set unless its schema declares an order, and a declared order is
preserved") and mark the declared orders in the schemas machine-readably.

**M-4. `resolvedConfigDigest` has two admissible spellings.** *(vectors F1, F1b)*

Admission §1.1 says "Resolved semantic configuration contains analysis,
components, discovery, policy and evidence values", but
`identity-schemas.v2.json#/$defs/semantic-configuration` has
`required: ["analysis"]` and every section has `required: []`. Both
`{"analysis":{…}}` and `{"analysis":{…},"components":{},"discovery":{},
"policy":{},"evidence":{}}` validate, and they mint different
`resolvedConfigDigest` (`31608787…9036` vs `225729d8…bdc2`) → different
`snapshot2`, `plan2`, `run2` for the same project. This lands squarely on the zero-config path the contract index
foregrounds: for a repository with no config file, is `discovery` absent or `{}`?

F1b is the same defect one level down: the schema admits `{"analysis":{}}` with
no `profileId`, although admission §4 declares a missing profile
`CONFIG_PROFILE_MISSING`. The post-resolution requiredness exists only in prose.

I assumed all five sections present (assumption **CB-A1**, recorded in
`run-descriptor-graph.json`). **Required:** make the resolver's output shape
exact — either require all five sections in the schema, or state that empty
sections are omitted, and tighten `analysis` to its post-resolution required set.

**M-5. Security names public typed details that the closed registry cannot
express.** *(vector E21)*

Workflows §12 makes `public-detail-registry.v1.json` the single closed public
`DomainDetailCode` vocabulary, with "Owners register stable details before
emitting them; an unknown detail refuses admission" — and I confirmed the schema
enum equals the registry exactly (E19). But the security contract normatively
names details from two families with **zero** registered members:

- S9.1: "a **standalone** profile-set document is refused typed
  (`ROOT.SCHEMA_UNSUPPORTED`, detail `PROFILE_SET.NO_TR_PROFILE_ROLE`)" and
  "A different or older set refuses `PROFILE_SET.CORE_PIN_MISMATCH`".
- S8: a profile set keyed by a display alias "refuses
  `PROFILE_SET_KEY_NOT_MACHINE_ID`".
- S12: "`PAYLOAD-NOT-ADMISSIBLE` (incl. `ROOT.*`, `ENVELOPE.*`, `PROFILE_SET.*`
  details)".

Registry membership: `ROOT.*` → **38**; `TRANSITION.*` → **39**; `PROFILE_SET.*`
→ **0**; `ENVELOPE.*` → **0**. Security owns 180 of the 270 records, so this is
an omission, not a scope boundary. I confirmed that a termination carrying
`PROFILE_SET.NO_TR_PROFILE_ROLE` is schema-**refused**. A host implementing S9.1
literally cannot emit the refusal S9.1 mandates. **Required:** register the
`PROFILE_SET.*` and `ENVELOPE.*` details, or state in S12 that they travel as
`subject` data under `PAYLOAD-NOT-ADMISSIBLE` (the reading S12 uses for
`RECOVERY.REFUSED`, whose sub-details are likewise unregistered — but that
reading contradicts S9.1's explicit word "detail").

### SHOULD

**S-1. The D9 `hostTerminationUnion` field closure and nullability are never
dispositioned.** *(vector F7)* Workflows §0 retains `d9-exit-contract.v1.14.json`
as the "class/code/exit table" only. But the same document's
`$.hostTerminationUnion` declares `unknownFieldPolicy: reject` over a closed
field set `{runId, executionId, errorCode, reasonCodes, coverageId, signal,
details}` and `nullabilityPolicy: "No field is ever explicitly null; absence is
the only way to express 'not applicable'"`. `common.schema.json#/$defs/
StepTermination` adds three fields to that set — `authority`, `domainDetail`,
`faultCause` — and workflows §8 requires an output projection field `run-id` that
is "explicitly null in the projection's non-authoritative case". Both readings
are defensible (StepTermination is a workflow projection, not the D9 union; the
`run-id` projection field is not `termination.runId`), which is exactly the
problem: an implementer building the public JSON envelope must choose. Add a row
to the §0 disposition table naming `$.hostTerminationUnion` and stating whether
its field closure and nullability rule are retained, extended or superseded.

**S-2. Two schema-1 root documents disagree on admission.** *(vector F6)* S9.1
says "Root schema 1 is the v8 `root.schema.json` rule set, preserved with its
exact closed schema and semantic rules (`RootV1` in the schema bundle …)",
naming two documents. They are not equivalent: a root whose
`indexOrigin.url` ends in a newline is **admitted** by
`security-schemas.v8/root.schema.json` (bare `$`, `maxLength` 512 does not
defuse it) and **refused** by
`security/security-lifecycle.schemas.v1.json $.schemas.RootV1` (strict
`(?![\s\S])`). The same holds for role `namespaces` items. Name one document as
the admission boundary. (The product-successor schemas are otherwise flawless
here — 335 patterns, 0 exceptions.)

**S-3. Inventory ordering has no tie-break.** *(vector F5)* §3 says inventories
sort by UTF-8 logical path, but `uniqueItems` on `sourceInventory` applies to the
whole `Blob` object, so two rows sharing a `path` with different digests are
schema-valid and have **no** defined canonical order. Either enforce path
uniqueness in the schema or declare a tie-break. (My encoder refuses duplicate
paths; that is my choice, not the contract's.)

**S-4. `regeneration-mismatch` is an unregistered detail spelling.** Identity §4:
"A mismatch is `regeneration-mismatch`". It is spelled like the registered
lowercase details (`evidence.*`, `storage.*`, `native.*`) but has no registry
entry, and identity owns only 4 of the 270 records. Either register it or state
what carries it.

**S-5. Two by-reference dependencies are not resolvable inside the kit.**
(a) *(vector F8)* CAP-MANIFEST-ID-V1 is fully **verifiable** from these bytes —
I reproduced all seven vectors — but the encoder that *produces* those bytes,
CVE1, is defined by reference to
`resolved-inputs.v2#planIdContract.canonicalValueEncoding`, which is not in the
kit. `delivery.v4.json` restates four CVE1 properties and three type tags
(`04` text, `05` array, `06` map, plus `02` for `true`); the rest of its "eight
closed types" is not stated here. A host can check a committed manifest id but
cannot construct one. Since identity §3 makes the host *recompute* the id from
committed bytes, this is not blocking for the identity chain — but the release
builder path is incomplete from this subset. (b) *(vector F9)* The correction
record and readiness register named by the contract index are absent, as
discussed in §1.

**S-6. Discharged obligations are still written as open.** E20 shows S9.2's
`CoreTransitionIntentV1` obligation is satisfied in these bytes while the prose
still says "the current nine-field, three-operation workflow schema cannot
express a store operation … (obligation, Codex)". Several other "(obligation,
Codex)" notes appear across security S3/S10/S10.2 and native §13. A blind
implementer cannot tell which are genuinely open. Sweep them.

### Advisory

- **A-1.** Identity §3 and native §14 both say `rustcDevLlvmDigest` is "in
  native-context schema 2". It is at
  `NativeContextV2.toolchain.rustcDevLlvmDigest` (inside `ToolchainIdentityV1`).
  Reachable, but the citation should name the nesting — especially since its
  companion field in the same sentence (`typescriptStdlibMerkleRoot`) does not
  exist at all (M-2).
- **A-2.** Two textual identifier conventions coexist: identity §3's
  `<prefix>:<hex>` (`snapshot2:…`) and native §11's `sha256:<64 hex>` "where a
  `Sha256Text` is required". Both are used inside one graph (e.g.
  `CoverageKeyV2.subjectScopeCommitment` is `sha256:`-prefixed while its sibling
  `sourceUniverse` is bare hex). It is consistent, but one sentence in identity
  §3 saying native records use the `sha256:` text form for foundation-domain-less
  identities would remove the reader's doubt.
- **A-3.** `cache-key` and `regeneration-key` are byte-identical schemas
  distinguished only by `H` domain (B10). Correct, but a shared `$ref` with two
  domains would prevent them drifting apart.
- **A-4.** Identity §3's paragraph on the finding-fingerprint `discriminator`
  ("raw SHA256 of their canonical JSON string array") is one of the few recipes
  where I had to guess whether "canonical JSON string array" means my canonical
  encoder applied to the array (I assumed yes, and treated the token array as
  *ordered* — "in grammar order" — not as a set). Under M-3 this is the same
  defect; calling the array ordered explicitly would settle it.

---

## 5. What I had to invent, and what is legitimately left to implementation

**Invented (missing public/semantic contract):** the `subjectScopeCommitment`
recipe (M-1); the TypeScript native-context descriptor and domain (M-2); the
set-vs-ordered classification for `PolicyDocumentV1.rules` and
`RuleProgramV1.rules` (M-3); the resolved-configuration section-presence rule
(M-4). Each is marked in the retained output and each changes `run2`.

**Legitimately free (algorithm choice, not contract):** query planning (§4
explicitly makes it an optimization that must agree with a retained full-scan
reference); provider-internal extraction strategy; storage layout beneath the
digest-addressed CAS; retry/backoff scheduling within the stated bounds; clone
candidate scoring beyond the declared modes; framework recognizer internals; the
concrete SQLite schema behind the stated transaction and barrier obligations.
These are correctly unspecified and I did not count them as gaps.

**Correctly deferred to qualification, not design:** real fsync/SQLite/
process-death behaviour, flock semantics, O_NOFOLLOW/ACL races, sleep-inclusive
monotonic behaviour across suspend, Ed25519 ceremonies, process-group kill
bounds, native compiler measurements and the G13 lanes. I did not treat any of
these as design gaps.

---

## 6. Limitations of this review

- Every custody, signature, clock, lease, provider-protocol and OS observation in
  my vectors is a **synthetic assumption**, never native enforcement proof. My
  positive Run graph proves the *semantic* joins close; it proves nothing about
  durability, confinement or cryptography.
- I did not exercise: the provider wire protocol (native §9), clone equivalence
  modes (§6), framework recognition (§8), the Rust dependency-source/prepared-
  output paths (§3), the security trust-time state machine (S4/S4.5), lease and
  migration state machines (S7/S9), the G13 report gate (admission §2–§3), or
  HTML/agent rendering. I read them for reconstruction and ownership only.
- My canonicalizer is one reading of §3. Where §3 is ambiguous (M-3, M-4, S-3) I
  chose and disclosed; a different conforming reading yields different
  identities. That is the finding, not a defect in my code.
- I validated schemas with the kit's own documents and `jsonschema` 4.25.1 under
  Draft 2020-12. JSON Schema alone does not establish exact numeric admission —
  as §3 itself says — so my lexical layer runs first and is separately vectored.
- Passing 106 self-authored vectors is not independent acceptance, is not product
  qualification, and is not implementation authorization.

---

## 7. Verdict

**CHANGES_REQUIRED.**

The architecture is genuinely reconstructible, and more of it is exactly
specified than I expected from a blind read. The semantic/operational split is
clean and mechanically verifiable; the acyclic identity graph closes; the
closure-join rules correctly refuse hidden evidence, cross-source facts,
producer-chosen witnesses and forged manifest ids while those objects remain
schema-valid; the examined-vs-resolution completeness correction is the right
distinction and is enforced by RC-2 rather than asserted; the fault law
(worker fault → no facts/no Run, admitted-incomplete → authoritative
indeterminate Run) is coherent across three contracts; the D9 branch contract,
the detail registry drift-check and the SARIF parity obligation all hold exactly
in these bytes. The retained DELIVERY v4 capability-manifest recipe verifies
against all seven of its published vectors from prose alone.

It is not yet buildable. Four values that enter `run2` cannot be computed from
this input set without inventing design — a required Coverage commitment with no
recipe (M-1), a required TypeScript context with no record (M-2), an array
ordering rule that stops short of the documents it must cover (M-3), and a
resolved-configuration shape with two admissible spellings (M-4) — and a fifth
defect makes a normatively mandated security refusal unemittable under the closed
public vocabulary (M-5). Every one of these is a *public semantic contract* gap
rather than algorithm freedom: each changes a committed identity or a public
termination, so two conforming implementations would disagree on `run2` for
identical source, which is precisely what FW-06 and identity §3 exist to prevent.

They are also all narrow. M-1 and M-2 are missing paragraphs, not missing
subsystems. M-3 and M-4 are closing rules for machinery that is otherwise fully
specified. M-5 is a registry omission. None requires rethinking the design; all
require finishing it. I would expect a corrected subject to clear a re-review.

---

### Retained artifacts

```
output/work/cb_canonical.py    admission + canonical encoder + H (from prose only)
output/work/cb_vectors.py      series A–D: admission, Run graph, refusals, terminations
output/work/cb_workflows.py    series E: comparison, authorization, registry/inventory
output/work/cb_gaps.py         series F: reproducible invention-forcing probes
output/work/run_all.py         runner
output/vectors/vector-results.json      all 106 vectors with selectors and values
output/vectors/run-descriptor-graph.json  the complete positive Run descriptor graph
output/blind-review.json       machine-readable verdict and findings
```
