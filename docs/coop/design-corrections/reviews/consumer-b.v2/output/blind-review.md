# OpenSIP DR-011-R10 — blind consumer B (v2) design-reference reconstruction

**Verdict: CHANGES_REQUIRED**

Four MUST-level defects and six SHOULD-level defects remain. Every one of them is
a *missing or conflicting public/semantic contract*, not an algorithm the design
deliberately left to implementation. One promised vector (the mainstream
`node_modules`-resolving TypeScript universe) is **not constructible** from these
normative inputs; I report the exact blocker rather than inventing the record.

This is a design-reference reconstruction only. Nothing here is a readiness grade,
a product-qualification claim or implementation authorization. Every OS, compiler,
Cargo, provider and filesystem observation in my vectors is a **synthetic trusted
observation** — a stated TCB assumption — and never native enforcement proof.

---

## 0. Input custody and hash verification

| Check | Result |
|---|---|
| `consumer-input-manifest.json` declared files | 43 |
| Files present on disk under `subject/` | 43 |
| SHA-256 **and** byte-length matches | **43 / 43** |
| Mismatches | 0 |
| Missing | 0 |
| Undeclared extra files | 0 |
| Manifest self-digest (SHA-256) | `785b829ae6ad8ac965e159e2397c20eba860fe6562ec01fdf30cd6a45168a004` |
| Declared parent subject | `b5cfb5d316eb0101950476a37a2095ed0d9c5d51263408d3462f105d63165f7b` |

The declared parent subject digest is an assertion I cannot verify from a subset;
I verified only that this kit is internally exact and complete against its own
manifest.

**Excluded governance records are correctly excluded.** The index
(`docs/v2/contracts/product-v1/README.md`) states the distinction the
reconstruction needs: the five contracts' retained/superseded selector tables
determine the applicable recipes, while the correction record and the central
readiness register "grant standing; they are not additional semantic recipes."
I never needed either to build a vector, and I raise no input-custody complaint
about their absence (probe `G12`). Every selector I needed to resolve a semantic
recipe was inside the kit; where one was not, that is a design gap and is
reported as such below, not as custody.

I read no original repository, no author Python/TypeScript reference model, no
fixtures, cases, goldens, reports or prior reviews, and no other
`/tmp/opensip-design-corrections` directory. Historical review narratives inside
the inherited normative documents (for example `delivery.v4.json`'s own
`standing: CANDIDATE / NOT-APPLIED`, and the native/security "joint correction
provenance" paragraphs) I treated as provenance only, and I followed no links out
of the kit.

**Retained outputs** (all under `output/`):

| Path | Contents |
|---|---|
| `blind-review.md`, `blind-review.json` | this review |
| `vectors.json` | 109 machine-readable vectors, 0 failures |
| `terminations.json` | 22 public termination examples, schema-validated |
| `gaps.json` | 12 mechanical gap probes with the observed bytes |
| `work/osref.py` | my canonicalizer `C`, `H`, order keyword, CVE1 |
| `work/graph.py` | my `admit_native_context`, `bind_*_universe`, coverage boundary |
| `work/build.py` | the two Run graph constructions |
| `work/closure.py` | my Run-closure re-admission |
| `work/run_vectors.py`, `work/terminations.py`, `work/gaps.py` | drivers |

---

## 1. Reconstructed end-to-end chain

Owning contract in **bold**; the selector is the exact one I read.

### 1.1 Zero-config discovery → typed configuration and source

1. **security-and-lifecycle S3** decides the *authority* boundary: an O_NOFOLLOW,
   lstat/ACL-only walk with no environment, no `PATH`, no `HOME`. `--project`
   examines one resolved path; otherwise the walk runs upward ≤ 256 levels,
   selecting `mode: config` at the first custody-passing directory holding a
   config, else `vcs-default` at a VCS marker root, else `cwd-default`. A nested
   config below a VCS root is a **deliberate project boundary** (ADV-3), recorded
   in `nestedProjects` and never entered.
2. The **one shared discovery rule** (`discovery-defaults.py`, consumed by
   security S3 and **native-evidence §1.4 U-4a** and restated by neither) prunes
   `node_modules`, `.git/.hg/.svn/.jj` and a `target` segment whose parent holds
   `Cargo.toml` — by exact path **segment**, never substring. `packages/target`
   and `src/target` stay ordinary source. A pruned tree is one `prunedTrees`
   record with a marker count, so 4200 installed manifests are one record and
   never 4200 units.
3. After `ACCEPT`, security exports the closed `AdmittedBoundaryInventoryV1`
   (`boundary_inventory(result)`), and the host passes it **unchanged** to native
   `discover_units` / `assign_membership` / `unit_scope_descriptor`. Native never
   re-derives a boundary from caller input; an inventory whose pruned trees
   disagree refuses `PROJECT.DISCOVERY_INVENTORY_MISMATCH`.
4. **native-evidence §1.4** then decides *language* units: one unit per directory
   **per language family**, so a root holding both `Cargo.toml` and
   `package.json` yields two units at one `rootPath` (U-1). A file belongs to the
   deepest unit **of its own family** (U-3). Every inventory file lands in exactly
   one `FileMembershipRowV1`; `erasedFiles` is a schema-constant empty array (U-4).
5. **admission-and-qualification §1.1** resolves `product-configuration.schema.v2`:
   compiled authenticated defaults, then global, project, interactive local and
   explicit flags; arrays replace atomically, records merge by named field; the
   environment layer is empty; CI never probes the interactive carrier. All five
   sections of the resolved semantic record are always present, an unselected
   section being exactly `{}`. Absent `entryPoints` means automatic recognition;
   explicit `[]` is deliberate empty intent. `resolvedConfigDigest` is SHA-256 of
   the canonical semantic value; UI, retention bounds and custody acknowledgements
   are operational and cannot move it.
6. **identity-and-evidence §3 / §5** captures `snapshot2` over ProjectId, the
   sorted source inventory, `resolvedConfigDigest`, `scopeDigest` and `vcsDigest`.
   Snapshot capture consumes the *same* admitted boundary inventory as native
   discovery; boundary anchors enter the Plan scope descriptor.

### 1.2 Invocation / step / attempt lifecycle — operational authority

**workflows-and-surfaces §1** and **identity §2**. These are the operational
identities and they are excluded from every semantic identity:

- `RequestId` (`req1_` + 32 hex) — one host request, minted **before** admission
  and retained for refusal as well as success.
- `ExecutionId` (`exec1_` + 32 hex, EXECUTION-ID-V1) — one per admitted *attempt*;
  retry always gets a fresh one. Both are independent 16-byte host-CSPRNG draws,
  reserved with uniqueness checked in the operational ledger; caller-supplied IDs
  and reuse refuse; neither is derived from a content hash.
- `StepId` — the zero-based position in the invocation's ordered acyclic list of
  ≤ 64 steps; ≤ 3 attempts per step.

Only `analysis` and `verify` steps seal or link a `run2`. `comparison`, `query`,
`render`, `import`, `repair-preview`, `repair-apply`, `test-execution`,
`native-preparation`, `mutation`, `export-delivery` and `doctor` are **operational
steps that never mint a Run** — this is the distinction between mutation/analysis
steps that the task asks about, and it is enforced by schema (`retryPolicy=none`
by schema for the mutating kinds; `idempotent-retry` lawful only for
`faultCause=ledger-busy`).

The **step DAG and the derivation DAG are disjoint**: a step never depends on a
stage and a stage never references a step. Each analysis/verify *attempt* owns
one `exec-plan2` of ≤ 1024 stages.

### 1.3 Analysis Plan

`plan2` binds snapshot, `capabilityManifestId`, the semantic closure set, the
analysis spec, resolved configuration, `nativeContextDigests`, imports, policy,
waivers, scope, a deterministic budget and the **semantic grant projection**. The
grant projects only `read-source` / `read-import` / `native-analysis` /
`prepare-code`. Storage, rendering and repair effect authority stay in the
operational request and cannot be fabricated by this projection; `test-code` is
not an analysis operation, and a test-execution step has **no Plan at all**
(security S10, "Operational admission precedes any Plan").

`capabilityManifestId` is the inherited applied CVE1 recipe, **derived** and never
trusted: the host recomputes it from the committed artifact bytes named by
`plan.capabilityManifestBytesDigest`.

### 1.4 Native facts, Coverage and view

**native-evidence §2, §4, §9, §11.** The host resolved-inputs adapter computes the
language context (`TypeScriptNativeContextV2` / `NativeContextV2`) from admitted
retained bytes before PlanId — never from a `tsc --version` string, a worker claim
or the environment — then binds the universe to it
(`bind_typescript_universe` / `bind_rust_universe`), with the retained context
bytes a **required** argument because "an optional field-agreement check is not a
rule."

The provider protocol is reject-before-disclosure: a capability row lacking any of
the four identity tokens is **never spawned**; Hello→HelloAck exchanges no source
bytes; `OpenUniverse` is admitted only when `identityNegotiated=true`.

Coverage separates two claims that were previously conflated: the **examined
partition** (`subjectScopeCommitment`, `subjectCount`) and **resolution
completeness** (`ResolutionCompletenessV2`). RC-2 is the load-bearing rule: a zero
unresolved-edge count never implies `complete`; `complete` additionally requires
`attempted`, `examinedExhaustive` and `stageTerminal=complete`.

`subjectScopeCommitment` is **the identical digest** to `coverage.scopeId` in a
different textual form, so it cannot drift from the scope it names; the host
builds the scope descriptor from its **own** enumeration and a provider-supplied
commitment is never an input to that step. A provider that examined a narrower
partition than the host enumerated "is detected here, and by nothing else."

### 1.5 Pure evaluation and proof verification

**identity §4.** The evaluator consumes only Plan-bound, schema-admitted finite
views, Coverage, imports, program, policy and waivers; all consumed data are in
`evaluationInputRefs` and no hidden lookup is allowed. Strong Kleene three-valued
logic; `all-covered` is true only with admitted resolution-complete coverage.
Before sealing, the host **independently replays** the admitted deterministic
program against the retained closure and compares the *complete normalized result*
— not a producer checksum.

`program-predicate` addresses one node of the admitted `RuleProgramV1` by a total
deterministic address (`p`; `a.i` for the *i*-th `and`/`or` operand, zero-based
shortest decimal; `a.0` for `not`), so a witness cannot name a predicate the
program does not contain. The compiled program is not a free artifact: it must be
exactly the projection of the Plan-selected policy's rules in the policy's own
`ruleId` order.

### 1.6 Evidence, seal, Run — acyclic

`proof2` does not include `evidence2` or `run2`; `evidence2` may include the
proof; `seal2` includes both; `run2` includes the seal. My closure checker
enforces this by refusing `run` / `semantic-evidence` / `evaluation-seal` /
`proof-bundle` in any proof or finding `Ref` domain (vector `V-REF-40`).

### 1.7 Durable receipt and current availability — two different facts

**identity §5.** Commit order: validate closure and independently replay proof →
write immutable blobs to private temp, verify digest/length, fsync, atomically
publish under digest, fsync directories → **one** synchronous ledger transaction
inserting the Run manifest, object references, the availability generation, pins
and a commit receipt → only then acknowledge. A failure before the ledger
transaction publishes no authoritative Run; a crash after ledger commit but before
acknowledgement is `durability-undetermined`, exit 4, with an ExecutionId for
read-only recovery.

**Sealed assurance is immutable and current availability is a separate monotonic
generation record.** Assurance is `verified` / `verifiable` / `replayable` (the
default authoritative profile requires `replayable` at seal). Availability is
`retained` / `partial` / `expired` / `purged` / `corrupt` / `unavailable` and may
*improve* through verified restoration or regeneration — but "sealed assurance and
historical verdict never change." A query reports both. This is the single
sharpest semantic-vs-operational distinction in the design and I found it stated
consistently in identity §5, §4 (regeneration mismatch is an *operational*
refusal) and workflows §8.

---

## 2. Independent vectors

I wrote `C`, `H`, the `x-opensip-order` keyword, the `x-opensip-digest` walker and
CVE1 directly from prose. No author code exists in the kit and I copied none. All
descriptors below are my own minimal authored vectors; I did not use any embedded
normative example as an oracle. Full machine-readable results: `vectors.json`
(**109 vectors, 0 failures, 0 unexpected admissions**).

### 2.1 Encoder and exact admission (13 vectors)

`H(D,X) = SHA256("opensip.product.v1" ‖ 00 ‖ D ‖ 00 ‖ uint64BE(|C(X)|) ‖ C(X))`.

| Vector | Result |
|---|---|
| `V-C-01` non-BMP key order | `C({"\uffff":2,"\U0001f600":1,"a":0})` = `{"a":0,"\uffff":2,"\U0001f600":1}` — UTF-8 byte order puts U+FFFF **before** U+1F600, which UTF-16 code-unit order would not |
| `V-C-02` escaping | `["a/b","x\ty","\u007f","\u2028","q\u0001r","\\","\""]` → slash unescaped, `\t` short escape, U+007F and U+2028 **unescaped**, U+0001 as lowercase `\u0001` |
| `V-C-03` no normalization | NFC `"é"` and NFD `"é"` produce distinct canonical bytes |
| `V-C-04` integers | `18446744073709551615` and `-9223372036854775808` admitted; both boundaries+1 refuse `ADMIT.INTEGER_RANGE` |
| `V-C-05` ×6 | duplicate key, `1.0`, `1e0`, `-0`, `NaN`, `\ud800` each refuse with a distinct typed cause |
| `V-C-06` depth | depth 32 admitted, depth 33 refuses; a scalar at the root has container depth 0 (root container counts as 1) |
| `V-C-07` order keyword | all ten vocabulary members exercised; `{"by":[…]}` tuple form exercised; an annotation outside the vocabulary **refuses** rather than passing silently |
| `V-C-08` sequence | `["z","a","z"]` round-trips unchanged — C never sorts, deduplicates or infers a set from `uniqueItems` |

### 2.2 Semantic vs operational identity change (6 vectors)

`V-H-01` — one changed byte in `src/a.ts` moves the whole chain:

```
base    snapshot2:befaa6bd… → plan2:e71889b3… → run2:e648c33a…
changed snapshot2:f4577565… → plan2:0d9ec4dd… → run2:7922e660…
```

`V-H-02` — a second attempt under a different `RequestId`, `ExecutionId`, wall
clock, PID, receipt signer and output destination reproduces
`run2:e648c33a489d317d37c2ae96d9d1616a1907169e22a8069fba4d57aa1eb46d15` exactly.
Identical semantic inputs produce the same Run on two attempts; attempts remain
separately auditable.

`V-H-03` — for each of the five records identity §3 defines because nothing else
does (`program-predicate`, `predicate-witness`, `stage-spec`, `owner-source-set`
row, `commit-inventory`), **every single-field mutation moves the canonical
digest**: 6/6, 6/6, 7/7, 3/3, 4/4.

`V-H-04` — `H("plan", plan)` = `e71889b3…` and `SHA256(C(plan))` = `eb5a11df…` are
different values; offering the payload where a frame is required fails the prefix
(`CLOSURE.FRAME_PREFIX`), and offering the frame where a canonical record is
required fails parsing.

`V-H-05` — `scope2:458a1aa3…` and `sha256:458a1aa3…` are one digest, recomputed
independently with `hashlib` from the scope descriptor.

`V-H-06` — the three admitted textual forms agree:
`sha256:c77fc9a6…` (native `Sha256Text`) = `c77fc9a6…` (Plan bare hex).

### 2.3 Capability manifest — all eight CVE1 types (6 vectors)

`V-CM-01` exercises every one of the eight closed CVE1 types with my own values:

```
null 00   false 01   true 02
unsigned-64(0)            030000000000000000
unsigned-64(2^64-1)       03ffffffffffffffff
negative-signed-64(-1)    07ffffffffffffffff
negative-signed-64(i64min)0780000000000000 00
"a"                       040000000161
[]  0500000000   [1,true] 05000000020300000000000000010 2
{}  0600000000   {"b":1,"a":2} 06000000020400000001610300…  (key-sorted)
```

`V-CM-02`/`03` — a non-NFC string, a float and an out-of-range integer each refuse
under CVE1 while `C` continues to admit non-NFC text unchanged: CVE1's NFC
admission "applies to the capability manifest only and does not change C's
no-normalization product descriptor profile," and my two encoders demonstrate that
separation.

`V-CM-04` — my own `CapabilityManifestV1` (548 committed bytes) yields

```
capabilityManifestId = a433ab1f6c807d53f26600d9afab6073a5e55848188dd6d18e98c5e697cc2b7f
```

recomputed by the closure from the committed artifact bytes and agreeing with the
Plan and Run fields. `V-CM-06` shows the profile name alone moves it.

`V-CM-05` executes the four gates in the declared traversal order: unsorted
`platformIds` → `NOT_CANONICAL`; a relation key outside fact-plane's twelve →
`DOMAIN`; `declares: "checked"` (a rung of another relation's ladder) → `DOMAIN`.
That same vector is what surfaces gap **G6**.

### 2.4 Complete minimal positive Run graphs — BOTH languages

Two **separate** Runs over two separate snapshots, each with a non-empty selected
native context set and each exercising its **own** language's universe / fact /
Coverage path. A Rust context sitting inside a TypeScript graph would not have
exercised the Rust universe path, so I did not do that; `V-REF-20` separately
proves a Rust universe cannot bind a TypeScript context.

**V-RUN-TYPESCRIPT** (53 retained objects, 15 closure steps)

| | |
|---|---|
| snapshot2 | `befaa6bddfdffcd9a01d8c452d4c28bf752b3273a533b15bd87c3e25ed551b7c` |
| native context (`native.context.typescript.v2`) | `sha256:c77fc9a6c1d4553529c626871da49f3692ebdeb2ee6b6f02084aeb8eb4d93368` |
| `plan.nativeContextDigests[0]` | `c77fc9a6c1d4553529c626871da49f3692ebdeb2ee6b6f02084aeb8eb4d93368` |
| universe (`native.semantic-universe.typescript.v2`) | `d3c9cf1220ccc40a96f907315fd48d1524be812ff8a1139819cfc2c0e601add7` |
| scope2 | `458a1aa36177f9700b2572275f0d1d4f2ed445c7e8c3904e16f94bcfb909369d` |
| coverage2 | `dc8ed2ddaa93e5438dbd9f0821e76122619aa701a46ea4dc9d8986e963949744` |
| fact2 | `3cb36537d31d8abfe0943a9638c5ae70ef27fcaf073e711ce4e45cea859e3449` |
| view2 | `5b66bafa674aa10c0608c6223ba5ea04d7e210413893f4f21d9236ebc76b0355` |
| exec-plan2 | `2ab5c69a75b725f155a7c343f4b8d8376ee074ad97964eb99d6531e980c668aa` |
| proof2 | `f82926170101db7bac394747d13f655b0be654d210b22e25cff44f71217e3179` |
| evidence2 | `f0fef4e4b5d366e449b92b4254a64069f0212808d87dd8e3d70ed955201203cc` |
| seal2 | `aea62294e5b0264d5bf5b51801b4b5549715e01e3639cdd1744017aee653b763` |
| **run2** | **`e648c33a489d317d37c2ae96d9d1616a1907169e22a8069fba4d57aa1eb46d15`** |

**V-RUN-RUST** (59 retained objects, 15 closure steps)

| | |
|---|---|
| snapshot2 | `9dee393118c0103a9f237782d4bbd41a4f9badd819931e4b542f14434fb82a77` |
| native context (`native.context.rust.v2`) | `sha256:0da65dc408862665905df22ee73c06c6c6936e853f451facb5eeabe88404c02f` |
| universe (`native.semantic-universe.rust.v2`) | `b58c558eb0e02d6967896a2f8d29564e6a4cc69788d24a92001c30c6d63d2eed` |
| scope2 | `2584709e428a9aeba6f23cd3d86c8103dd7dc146b6745a1310c0044cd6dc6f9a` |
| coverage2 | `be22eaa698fa28ee59969b9a541f5b1b7e14f175201a0b3de622884924a403bd` |
| fact2 | `a402530c1c8d830c2e9325657e47e52007ce7eb0155351b8dd61c039bc8a9416` |
| view2 | `20f3713981528566247acca81e1115c894423e52c0cb3508f80a04f9475ee533` |
| exec-plan2 | `942e76d94ba191290bef61a88c75a7d1eacd06b1cd8bf268af7374302bb0949f` |
| proof2 | `2421aede3dc7036bf6db4d84e374db94b8fedaf84ba309e3021757558b97e42a` |
| evidence2 | `bc7bed40ad7a385d51c729bebe75feef69c8857bab72ce7b51a3b0ccacd51ffe` |
| seal2 | `0ebfa3ae1c7b4e6b790fc2f11599f078b03f71ac83ff7c6c106fc606be4f0c7b` |
| **run2** | **`1f53718a0a5140d4651dec56dbfd0fb6a1b4f11fd31965d54cca77e7f1707bb7`** |
| capabilityManifestId | `92c7f51308cdfecdfb48c19839b3f331b40ccf18a038765a2a4c923792a5ca47` |

The Rust graph reconstructs the **native dependency and configuration H preimages
from the normative recipes**, all the way down to raw bytes:

- `DependencyPackageSourceV1.fileManifestSha256` =
  `H("native.dependency-file-manifest.v1", sorted [{path,contentSha256,byteLength}])`,
  with every member's bytes retained at exactly its declared `byteLength`;
- `dependencySourceSetId` = `sha256:` + `H("native.dependency-source-set.v1", set)`,
  packages ordered by `(name, version, sourceId)`;
- `unifiedFeaturesId` = `sha256:` + `H("native.unified-features.rust.v1", …)`;
- `rust-v2.configProjectionSha256` = the 64-hex suffix of
  `H("native.cargo-config-projection.v2", CargoConfigProjectionV2)` over the whole
  record, while `CargoConfigProjectionV2.projectionSha256` is the **raw** SHA-256
  of the projected `.cargo/config.toml` **file** bytes. My closure retains both and
  checks that neither substitutes for the other, and that neither is the raw
  SHA-256 of the canonical projection bytes.
- `rustcDevLlvmDigest` and `typescriptStdlibMerkleRoot` are re-prefixed with
  `closure2:` and joined to a retained closure of kind `rust-dev-llvm` / `stdlib`
  whose recomputed identity equals them and whose complete tree is retained.

My closure checker (`work/closure.py`) re-runs, over retained descriptors alone
with nothing re-executed: `admit_native_context`; `bind_typescript_universe` /
`bind_rust_universe`; `set(retained context frames) == plan.nativeContextDigests`;
every universe frame's `nativeContextId` ∈ `plan.nativeContextDigests`; the
closure-kind joins; the snapshot joins for `configGraphPaths`,
`replacedSnapshotConfigs`, `crateRootPaths` and both lockfiles; the
`capabilityManifestId` re-derivation; the acyclic proof/evidence/seal/Run joins;
`RuleProgramV1` = the policy projection; the predicate node addressing; and the
per-view agreement on Plan source, universes, relation/rung and producer.

**Cache key vs cache hit** (`V-CACHE-01/02`): key construction is pure — the same
record under two H domains yields `cache2:` and `regen2:` values that differ only
by domain, and it reads no bytes. Hit *admission* needs the Run's whole closure,
so a consumed native context outside `plan.nativeContextDigests` refuses.

### 2.5 Refused hidden / mismatched inputs (32 vectors, ≥ 1 per language)

Selected; all 32 are in `vectors.json`.

| Vector | Language | Typed refusal |
|---|---|---|
| `V-REF-TS-01` hidden context frame no Plan reached | TS | `CLOSURE.CONTEXT_SET_MISMATCH` |
| `V-REF-RS-01` hidden context frame no Plan reached | Rust | `CLOSURE.CONTEXT_SET_MISMATCH` |
| `V-REF-TS-02` universe field contradicts context | TS | `native.universe-context-field-mismatch:packageModuleType` |
| `V-REF-RS-02` cfg set drops a base cfg | Rust | `native.universe-context-field-mismatch:cfgSets:drops-base-cfg` |
| `V-REF-03` altered frame (same length, still valid canonical JSON) | TS | `CLOSURE.IDENTITY_MISMATCH` |
| `V-REF-04` missing preimage | TS | `HOST.IO_FAILURE` / `evidence.missing:<ref>` |
| `V-REF-05` wrong preimage under a digest | TS | `CLOSURE.CAPABILITY_MANIFEST_ID_MISMATCH` |
| `V-REF-06` unregistered H domain | — | `CLOSURE.FRAME_DOMAIN_NOT_IN_SET:native.context.python.v2` |
| `V-REF-07` raw payload offered as an H identity | — | `CLOSURE.FRAME_PREFIX` |
| `V-REF-TS-10..15` | TS | closure-unretained, tool-not-in-closure, stdlib-inventory-incomplete (a *deselected* `lib.es5.d.ts`), compiler-version-not-from-manifest, config-graph-path-outside-snapshot, lockfile-digest-disagrees |
| `V-REF-RS-10..12` | Rust | closure-kind-mismatch, replaced-config-outside-snapshot, nested-identity-unretained |
| `V-REF-20` Rust universe bound to a TypeScript context | Rust | `native.native-context-language-mismatch` |
| `V-REF-21` TS universe bound without the retained context | TS | `native.universe-context-not-supplied` |
| `V-REF-22` Rust universe bound without retained inputs | Rust | `native.universe-retained-inputs-not-supplied` |
| `V-REF-30..34` coverage producer boundary | TS | claimant-chosen commitment, narrower partition, `complete` with an edge, zero-edges-≠-complete, key universe outside the host scope |
| `V-REF-35` coverage outside the view, in a **fully re-framed and re-keyed** Run | TS | `native.coverage-subject-scope-outside-view` |
| `V-REF-40` proof cites the Run it produces | TS | `CLOSURE.PROOF_REF_DOMAIN_FORBIDDEN:run` |
| `V-REF-41` bare `coverage-payload` reference as an authoritative root | TS | `CLOSURE.PAYLOAD_DOMAIN_AS_AUTHORITATIVE_ROOT` |
| `V-REF-42` compiled program is not the policy projection | TS | `CLOSURE.PROGRAM_NOT_POLICY_PROJECTION` |

`V-REF-03` and `V-REF-35` are deliberately hard cases: the altered frame remains
well-formed canonical JSON of exactly the original length, so only re-hashing the
frame catches it; and the grafted Coverage **was** properly admitted at the
producer boundary over its own scope, then grafted into a Run whose view, proof,
evidence, seal and Run identities were all recomputed — so nothing stale remains
and only the view-membership join can refuse it. That is the concrete
demonstration of "a frame proves retention, never admission."

### 2.6 Schema validation (48 vectors)

Every descriptor in both graphs validated against the kit's own closed schemas via
`jsonschema` Draft 2020-12 with a pinned local registry (no network): all 20
identity `$defs` instances (× 2 languages), both native contexts, both universes,
`DependencySourceSetV1`, `UnifiedFeaturesV1`, `CargoConfigProjectionV2`,
`DependencyFileManifestV1`, both `CoverageResultV3` payloads, `PolicyDocumentV1`
and `RuleProgramV1`. **48 valid, 0 invalid.**

---

## 3. Public terminations and subsystem ownership

22 termination examples, each validated against
`common.schema.json#/$defs/StepTermination` and — where the envelope is complete —
`command-envelope.schema.json` (CommandEnvelope major 2). Full text with the story
and owning selector for each: `terminations.json`.

**All 22 StepTermination records valid. All detail codes are members of the closed
`public-detail-registry.v1.json` — with exactly one exception, which is finding
G9.** I confirmed the registry and the workflow `DomainDetailCode` enum are
identical sets of 282 members.

| Scenario | Class / exit | Code | Detail | Deciding subsystem |
|---|---|---|---|---|
| TERM-01 clean audit vs current baseline | success 0 | — | — | workflow comparison owns the gate; the analysis Run keeps its own verdict under `verdictGate=delegated` |
| TERM-02 pivot detector unavailable | indeterminate 3 | `BASELINE.RECIPE_UNSUPPORTED` | `BASELINE.PIVOT_DETECTOR_UNAVAILABLE` | workflow baseline resolves the closure; **security** decides its current trust |
| TERM-03 required evidence lost | indeterminate 3 | `VERDICT.INDETERMINATE` | `COMPARISON.REQUIRED_EVIDENCE_UNAVAILABLE` | workflow comparison; identity owns the `import2` identity that moved |
| TERM-04 **empty result, still indeterminate** | indeterminate 3 | `VERDICT.INDETERMINATE` | `COMPARISON.PIVOT_REEVALUATION_UNAVAILABLE` | workflow comparison — entry counts cannot prove the absence of a finding that missing evaluation could hide |
| TERM-05 interactive test consent in CI | request-rejected 2 | `REQUEST.PRECONDITION_FAILED` | `TEST.INTERACTIVE_CONSENT_IN_CI` | **security** admits `RepoExecutionGrantV2`; workflow only consumes the host projection |
| TERM-06 confinement claim | request-rejected 2 | `REQUEST.PRECONDITION_FAILED` | `TEST.CONFINEMENT_CLAIM_REFUSED` | **security** owns `permission-truth-tables.v9`; native and workflow *copy*, never assert |
| TERM-07 preparation not authorized in CI | request-rejected 2 | `REQUEST.PRECONDITION_FAILED` | `native.execution-not-authorized` | security admits the grant; native owns the preflight; workflow owns the step (never a Run) |
| TERM-08 repair consent not bound | request-rejected 2 | `REQUEST.PRECONDITION_FAILED` | `REPAIR.CONSENT_NOT_BOUND` | **security S10.1** — repair apply is first-party host-brokered mutation, *not* repository execution |
| TERM-09 repair preimage mismatch | request-rejected 2 | `REQUEST.PRECONDITION_FAILED` | `REPAIR.TARGET_PREIMAGE_MISMATCH` | workflow repair mechanics; identity owns the inventory digest compared |
| TERM-10 recovery blocked | operational-failed 4 | `HOST.IO_FAILURE` / `host-io` | `REPAIR.RECOVERY_BLOCKED` | workflow recovery table; security S10.2 admits the recovery authorization; neither may waive the guarded mechanics |
| TERM-11 **purge of a pinned Run** | request-rejected 2 | `REQUEST.PRECONDITION_FAILED` | *(no registered code — finding G9)* | identity retention; workflow owns the baseline pin |
| TERM-12 query needing proof after purge | request-rejected 2 | `REQUEST.PRECONDITION_FAILED` | `evidence.purged` | identity retention — the manifest query still answers; purged is not deleted-history |
| TERM-13 regeneration mismatch | operational-failed 4 | `HOST.IO_FAILURE` / `host-io` | `evidence.regeneration-mismatch` | identity availability — an operational refusal, never a new verdict |
| TERM-14 **required renderer failed after commit** | operational-failed 4 | `DELIVERY.REQUIRED_FAILED` / `delivery-required` | `DELIVERY.RENDERER_FAILED_AFTER_COMMIT`, `runId` retained | workflow output; identity owns the already-committed Run that delivery may not rewrite |
| TERM-15 optional export sink failed | success 0 | — | — | workflow output — egress never changes a verdict |
| TERM-16 ephemeral cannot supply authority | request-rejected 2 | `REQUEST.UNSATISFIABLE` | `WORKFLOW.EPHEMERAL_CANNOT_SUPPLY_AUTHORITY` | workflow invocation; identity owns the durable custody rule |
| TERM-17 **admitted-but-incomplete native inputs** | indeterminate 3 | `VERDICT.INDETERMINATE`, `runId` + `coverageId` | *(typed detail lives in the coverage2 record, native H-3)* | native owns the deficiency/nativeCause; host owns the class; **an authoritative Run is still sealed** |
| TERM-18 worker fault | operational-failed 4 | `PROVIDER.PROTOCOL_VIOLATION` / `provider-protocol` | `native.worker-fault` | native fault law — no facts, no Coverage, no Run |
| TERM-19 SIGINT before settle | interrupted 130 | — | signal + `runId` | workflow cancellation; after-settle would **not** be reclassified |
| TERM-20 doctor defects | success 0 | — | `DOCTOR.DEFECTS_FOUND` | workflow doctor — CI gates on `.outcome`, never the exit code |
| TERM-21 backup custody choice in CI | request-rejected 2 | `REQUEST.PRECONDITION_FAILED` | `storage.backup-choice-required` | security S3.1 before the first source-derived write; UNKNOWN status would instead admit with a mandatory disclosure |
| TERM-22 workspace unit limit | request-rejected 2 | `REQUEST.UNSATISFIABLE` | `PROJECT.WORKSPACE_UNIT_LIMIT` | the *one* shared discovery rule — both instruments refuse the same population under the same public code |

TERM-17 and TERM-18 are the pair that makes the fault law legible: a **clean**
stage over successfully admitted but incomplete inputs seals an authoritative Run
and terminates indeterminate; a **faulting** worker contributes nothing at all.
These are different event positions, not interchangeable error spellings — the
same point identity §5 makes for `REQUEST.PRECONDITION_FAILED` (exit 2) before
evaluation vs `HOST.IO_FAILURE` (exit 4) during a selected operation vs an
indeterminate Run (exit 3).

---

## 4. Issues

Every item below is substantiated by a probe in `gaps.json` that reports the
observed bytes.

### MUST

**M-1 (G1) — a registered payload schema document cannot constrain its payload,
so the closing rule and the registry contradict each other.**
Selectors: `identity-and-evidence.md` §3 ("a document offered as a *payload*
schema must constrain the payload directly, so a multi-record bundle cannot pass
vacuously"); `native-evidence.md` §7.1 registry and §4.1a step 6 / §7.2 ("the
exact full schema DOCUMENT file bytes"); `workflows-and-surfaces.md` §4;
`identity-schemas.v2.json` `#/$defs/{coverage,fact,import}.payloadSchemaDigest`.
Observed: `native-evidence.schemas.v2.json`, `imported-evidence.schema.json` and
`test-execution.schema.json` each have **zero** root constraint keys, and an
arbitrary object `{"this":"is not any registered payload","n":1}` validates
against each whole document. The one control that behaves as §3 demands is
`foundation/import-source-context.schema.json`, which identity §3 names by name.
Must invent: whether `payloadSchemaDigest` names the document while validation
uses the registry row's `#/$defs` selector (making §3's sentence false as written)
or whether each payload needs its own single-record document (which no registry
row names). The choice changes which bytes are hashed and therefore every
`coverage2`, `import2` and `fact2` identity.

**M-2 (G2) — two different canonical encoders for one fact payload, and no fact
payload schema *document* exists.**
Selectors: `identity-schemas.v2.json` `#/$defs/fact.payloadDigest`
(`x-opensip-digest.representation = canonical-record`); identity §3's
`canonical-record` row ("raw SHA256 of `C(record)`");
`fact-plane.v1.json` `$.factRecordContractV1.relationPayloadSchemaRegistryV1.canonicalPayloadEncoding`;
`native-evidence.md` §0 (which **extends** that registry rather than superseding
its encoding). Observed: the registry declares RFC 8949 deterministic CBOR with
map order by CBOR key bytes and **forbids negative integers and non-NFC text**,
while `C` admits both. The registry's rows are a bespoke
`required`/`optional`/`fields`/`enums` grammar inside a 59 KiB artifact, not
schema documents, so `fact.payloadSchemaDigest`'s "the exact complete registered
relation payload schema document bytes" has no referent. Must invent: the encoder
and the document. Two conforming implementations mint different `fact2` identities
for one provider output — which defeats FW-06 determinism and independent replay.
My `fact2` values are computed under an explicitly stated assumption and are **not**
claimed to be the design's values (`vectors.json` → `blocked` →
`V-BLOCKED-02`).

**M-3 (G3) — the mainstream TypeScript universe is not constructible.**
Selectors: `native-evidence.md` §2.4 table row `nodeModulesLayoutDigest` ("raw
SHA-256 of the canonical `resolvedNodeModulesLayout` record");
`native-evidence.schemas.v2.json`
`#/$defs/TypeScriptNativeContextV2.properties.nodeModulesLayoutDigest`. Observed:
no `$def` matching `resolvedNodeModulesLayout` exists in the 100-definition native
bundle, or anywhere else in the kit. The digest is `null` exactly when
`nodeModulesInReadSet=false`, so the only admissible TypeScript context is one in
which `node_modules` is **not** in the read set — i.e. every bare specifier is an
`unresolved-module-specifier` edge. **This blocked a promised vector:** my
positive TypeScript graph is forced to `nodeModulesInReadSet=false`. I report the
blocker rather than inventing the record (`V-BLOCKED-01`).

**M-4 (G5) — `tsconfigGraphHash` is a universe key with no producing recipe.**
Selectors: `native-evidence.schemas.v2.json`
`#/$defs/TypeScriptUniverseV2ResolvedInputs.tsconfigGraphHash`;
`native-evidence.md` §2.2; `resolved-inputs.v2.json`
`$.planIdContract.semanticUniverseSchemas.typescript-v1.resolvedInputs.canonicalization`.
Observed: the field is `{"type":"string","pattern":"^[0-9a-f]{64}(?![\\s\\S])"}`
with no description and no recipe anywhere. The closing digest law that would have
forbidden this — "a 64-hex field carrying no annotation is inadmissible" — is
scoped to `identity-schemas.v2` and does not reach the native bundle: the identity
bundle carries **57** `x-opensip-digest` annotations, the native bundle carries
**0**. Because any universe field change changes PlanId, two conforming hosts
analysing one repository mint different PlanIds and RunIds. I had to invent a
preimage to build my vector.

### SHOULD

**S-1 (G4)** — `native-evidence.md` §2.2's "Retained:" list names `compilerOptions`,
`packageLockIdentity` and `resolvedNodeModulesLayout`, none of which the closed
`TypeScriptUniverseV2ResolvedInputs` (`additionalProperties: false`) can carry. An
implementer building from the prose produces a record that fails admission. The
values relocated to the context; the prose should say "relocated" rather than
"retained".

**S-2 (G6)** — native §0 extends the relation registry with `unresolved-edge` (the
native `Relation` enum has 13 members; fact-plane's registry has 12), but
CAP-MANIFEST-ID-V1's ADM-DOMAIN gate binds `ProviderCapability.relations` keys and
`AbsentCapability.relationIds` to the twelve members it **measured** on the live
fact-plane bytes (`delivery.v4.json`
`$.derivedFrom.operations[17].value.valueDomains.registries['fact-plane.v1#relationRegistry.relations']`).
A provider declaring the new relation as a capability cannot be expressed in a
capability manifest, which is a PlanId input. Executed as `V-CM-05`.

**S-3 (G7)** — `identity-and-evidence.md` §2 makes
`c2-plan-stage-schema.v4.json $.planIntent.wireTypes.executionId` *the* normative
ExecutionId grammar; that pattern ends with a bare `$` and therefore admits
`exec1_<32hex>\n`, which `admission-and-qualification.md` §1 declares malformed and
`common.schema.json#/$defs/ExecutionId` refuses. `security-and-lifecycle.md` S9.1
handles precisely this situation for `RootV1` by stating in terms that the
successor is deliberately not byte-equivalent; identity §2 makes no such statement
while naming the older selector as the grammar.

**S-4 (G8)** — `identity-schemas.v2.json` `#/$defs/plan.properties.budget` is a
bare `{"type":"object"}`: no `additionalProperties`, no `required`, no order
annotation — inside the record whose bytes *are* the PlanId. Every other field of
that record is closed and every 64-hex field is annotated. The closed
`{unit, limit}` shape already exists at
`#/$defs/semantic-configuration…analysis.budget`; the Plan simply does not
reference it. The digest law's own reasoning ("a new field added without an
annotation refuses at admission instead of silently inheriting a plausible rule")
does not reach this field.

**S-5 (G9)** — `identity-and-evidence.md` §5 normatively requires a purge refusal
that names the active pins and discloses consequences, and the closed
`public-detail-registry.v1.json` (282 members, identical to the workflow
`DomainDetailCode` enum) has **no** member for it. Since a `kind=failure` envelope
requires a non-empty `errors` array of registered `DomainDetail`s, **no admissible
public envelope exists** for that refusal — demonstrated by
`terminations.json` TERM-11 (`envelopeConstructible: false`). This is the same
class of defect the previous blind consumer's M-5 raised against the security unit
(closed by registering eleven codes); the identity unit's retention refusals were
not swept the same way.

**S-6 (G10)** — `native-evidence.md` §2.4 requires `bind_typescript_universe` to
check `configOrigin` against the retained context, and
`TypeScriptNativeContextV2` has no `configOrigin` field. Only the
synthesized/non-synthesized distinction is derivable (empty `configGraphPaths`);
nothing distinguishes `tsconfig` from `jsconfig`. Because `configOrigin` is a
universe field, an unchecked spelling mints two universe identities — and two
PlanIds — for one admitted context. My reference implements the synthesized
agreement and leaves the `tsconfig`/`jsconfig` spelling unchecked.

### Advisory

**A-1 (G11)** — `subject-scope.enumeratorClosure` must be a `closure2`, the closed
`closure.kind` enum has no `enumerator` member, and nothing states which kind is
lawful — unlike `toolClosure.closureId` (`toolchain`),
`typescriptStdlibMerkleRoot` (`stdlib`) and `rustcDevLlvmDigest`
(`rust-dev-llvm`), each pinned by kind in `x-opensip-digest-domains.domainSets`.
Low risk: the Plan-selection join already constrains it. I used `kind=provider`.

**A-2** — `ToolchainIdentityV1.standardLibraryComponentDigests` (Rust) declares
`x-opensip-order: "sequence"` with `minItems: 0`, while its TypeScript counterpart
declares `{"by":["component"]}` with `minItems: 1` and a complete-inventory
admission rule. The asymmetry may be intentional (native §2.4 states the
completeness rule only for TypeScript), but a Rust standard-library inventory that
is unordered, incomplete or empty currently admits.

**A-3** — `security-and-lifecycle.md` S3 and `native-evidence.md` §1.4 U-4a both
name `docs/coop/design-corrections/discovery-defaults.py` as the single shared
discovery rule and each says the other does not restate it. That file is not in
this kit. It is correctly excluded (it is reference code, not a semantic recipe)
and both prose statements were complete enough for me to reconstruct pruning,
the `.` sentinel and the 4096/1024 caps — but an implementer should note the rule
is *stated* in prose twice and *implemented* once, so the prose is the contract.

### Algorithm freedom I explicitly did **not** count as a gap

These are choices the design deliberately leaves to implementation, and I treated
them as such rather than as missing contracts: query planning ("an optimization
only: a retained full-scan reference must agree on selected facts"); the near-clone
Jaccard implementation given fixed parameters and a fixed `scoreMeaning`; the
filesystem transaction algorithm behind the repair journal states; SQLite WAL and
fsync mechanics behind the stated commit order and barriers; the concrete
recognizer implementations behind the nine pinned recognizer IDs and their
declared effects; and the ProjectId / RequestId / ExecutionId CSPRNG draws, whose
grammar and uniqueness discipline are specified and whose entropy source is an
implementation matter.

---

## 5. What I had to invent

| Invention | Why | Consequence for my vectors |
|---|---|---|
| `tsconfigGraphHash` preimage (raw SHA-256 of the canonical `[{path,sha256}]` array of the resolved extends graph) | M-4: no recipe exists | the TypeScript universe identity `d3c9cf12…`, and therefore that Run's PlanId and RunId, are mine, not the design's |
| `fact2.payloadDigest` encoder (foundation `C`) and `fact2.payloadSchemaDigest` bytes (the whole `native-evidence.schemas.v2.json` document) | M-2: the two owning statements disagree and no per-relation document exists | both `fact2` values are assumption-dependent |
| `configOrigin` agreement limited to synthesized-vs-not | S-6: the `tsconfig`/`jsconfig` distinction is not derivable | my binder admits a universe whose `configOrigin` spelling the context cannot confirm |
| `enumeratorClosure` kind = `provider` | A-1: no kind rule | cosmetic |
| `plan.budget` = `{unit:"work-units", limit:100000}` | S-4: the Plan's budget is unconstrained; I borrowed the closed configuration shape | another host may legitimately choose a different key set and mint a different PlanId |
| `nodeModulesInReadSet=false` | M-3: the true branch is unconstructible | my TypeScript vector does not exercise bare-specifier resolution at all |

Everything else in both graphs was derived from the normative text without a
choice: the framing, the encoder, the order keyword, CVE1, CAP-MANIFEST-ID-V1, the
closure joins, the `subjectScopeCommitment` recipe, the coverage producer
boundary, the node addressing, the policy projection and the acyclic joins.

---

## 6. Limitations

- **No product qualification, no implementation authorization.** Nothing here
  grades a readiness row, qualifies a native cell or a platform, or authorizes
  implementation. Real OS, compiler, cryptographic and SQLite measurements are
  future qualification work and I make no claim that a product exists; I did not
  demand one.
- **Synthetic TCB observations are assumptions.** Every closure tree, signed
  manifest body, lockfile, dependency tarball, `cargo metadata` result, custody
  observation and platform truth-table value in my vectors is asserted by me. They
  exercise the *design's joins*; they are never native enforcement proof, and my
  `admit_native_context` re-running cleanly proves nothing about a real compiler.
- **My implementations are one reading.** `osref.py`, `graph.py` and `closure.py`
  are my reconstruction of the prose. Where the prose is unambiguous I expect
  another implementer to agree byte-for-byte; where it is not (the six inventions
  above) my values are explicitly not authoritative. No author encoder existed in
  the kit to converge against, so my digests have **no independent oracle** beyond
  `hashlib` and my own hand-spelled preimages.
- **Coverage of the design is partial by construction.** I reconstructed the
  identity/native/evaluation spine and the termination surface in depth. I did not
  build vectors for: the comparison pivot chain B→E0→E4 as executed records; the
  baseline artifact and its pivot-closure resolution; the repair journal state
  machine; the security trust-time floor, root chain, recovery epoch, lease/lock
  order or transition journal; the clone equivalence modes; the import wrapper and
  source-mapping law; or the G13 qualification report gate. My reading of those is
  the prose reading recorded in §1 and §3, unexercised.
- **Only one snapshot per Run.** I built two single-language Runs to exercise both
  universe paths honestly. I did not build a mixed TS+Rust Run, so U-5 per-unit
  evaluation and joining, and the `mixed-native-partial` shape, are unexercised.
- **The parent subject digest is unverified.** I verified this kit against its own
  manifest only.

---

## 7. Verdict

The spine reconstructs. Working only from these bytes I built, and independently
re-admitted, two complete Run descriptor graphs with real language-specific
universe/fact/Coverage paths; recomputed the capability manifest identity through
all eight CVE1 types; reproduced the `subjectScopeCommitment` = `scope2` identity
from prose; and made twenty distinct hostile constructions refuse with the owning
contract's own typed cause, including a fully re-framed and re-keyed Run and a
Coverage record that had legitimately passed the producer boundary. The two
closing laws — arrays close by naming a default, digests close by admitting none —
did real work, and the "a frame proves retention, never admission" rule is the
reason a re-keyed hostile Run is still refusable. That is a genuinely strong
design and most of it is implementable from these bytes as written.

It is not yet reconstructable without invention, and the gaps are not peripheral.
Two of them (M-1, M-2) leave the *bytes that get hashed* undetermined for
Coverage, imports and every fact — the innermost thing the identity contract
exists to fix — and M-2 does so by leaving two owning statements in direct
contradiction, which the index itself calls "a design defect, never reviewer
discretion." M-4 leaves a universe key with no recipe, so two conforming hosts
mint different RunIds for one repository, which is exactly the determinism claim
(FW-06) the design makes. M-3 makes the ordinary TypeScript project — the one with
dependencies — unrepresentable, so the contract's own mainstream case cannot be
built. Notably, all four sit in the same place: **the closing digest law's
strongest property is that it admits no default, and its scope stops at
`identity-schemas.v2`.** The native bundle, which carries the universe keys and
the payload-schema references, has zero such annotations and inherits none of that
protection. Extending the law's scope to the native and workflow bundles would
close M-1, M-4 and A-2 structurally rather than one field at a time.

The SHOULD items are smaller but real: a prose "Retained:" list that would produce
a refused record, a relation the capability manifest cannot express, an identifier
grammar that admits a trailing newline the rest of the product calls malformed, an
unconstrained object inside a PlanId, a normatively required refusal with no
admissible public envelope, and a required agreement check with no derivable
input.

Any remaining MUST or SHOULD design gap requires **CHANGES_REQUIRED**, and ten
remain. I recommend closing M-1 through M-4 before implementation begins, since
each of them changes identity bytes and therefore invalidates any fixtures or
goldens authored against the current reading.
