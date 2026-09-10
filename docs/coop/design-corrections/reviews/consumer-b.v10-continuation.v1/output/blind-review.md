# Blind consumer B — OpenSIP DR-011-R10 (continuation)

**Verdict: ACCEPT-RECONSTRUCTABLE**

This is the same independent Grok origin after the first session hit the turn budget with no review file. No author implementation, fixtures, or prior verdicts were used. The design is reconstructable from the 79-file kit. That is not product qualification and not implementation authorization.

`newMustIssues` and `newShouldIssues` are empty because no remaining required or recommended *design* gap forced invention of a semantic recipe. Several charter vectors were executed as identity/schema/envelope controls rather than additional sealed Runs; those are reconstruction limitations, listed below, not contract defects.

## Input custody

| Item | Value |
|---|---|
| Kit | `/tmp/opensip-design-corrections/consumer-b.v10/subject` |
| Files | 79, all hashes and sizes match `consumer-input-manifest.json` |
| Kit manifest SHA-256 | `6af1cc95d0ee2d269c42436d5982c3386bc67a70e805979b912275a2558cfb8a` |
| Frozen parent subject SHA-256 | `652c800166a8d3f37eacfbf273c9786bb84f6fd6b5c6ead57b5a254315859a25` |
| Kit edited | no |
| Work directory | `/tmp/opensip-design-corrections/consumer-b.v10-continuation.v1/output` |
| Original first-pass output | preserved at `/tmp/opensip-design-corrections/consumer-b.v10/output` |

Re-verified after this continuation: kit unchanged.

Executable reconstruction (continuation tree):

```bash
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v10-continuation.v1/output/recon/main.py
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v10-continuation.v1/output/recompute.py
```

`recompute.py` re-hashes every retained H preimage frame. `recon/replay.py` is the required semantic replay: it parses store blobs, reconstructs evaluator inputs without reading claimed findings or verdict, rebuilds proof/evidence/seal/run, and compares exact canonical bytes and identities.

## What an implementer needs (owning contracts)

Zero-config discovery and typed configuration are owned by admission-and-qualification §1.1 and security S3. The resolved semantic configuration always has five sections; `analysis.profileId`, `analysis.capabilities` and the work budget are always present. Operational RequestId (`req1_`) and ExecutionId (`exec1_`) are CSPRNG, end-anchored, and excluded from Run identity. StepId is the DAG position. C-2 `executionId` provenance remains the historical `$` pattern; the product successor is `(?![\s\S])`.

Invocation/step/attempt law is workflows-and-surfaces §1. Analysis and verify may seal `run3`. Mutation, repair-apply, import, native-preparation and test-execution do not. Aggregate D9 class order over required steps: operational-failed > request-rejected > policy-failed > indeterminate > success.

Identities use H from identity-and-evidence §3:

`H(D,X) = SHA-256( ASCII("opensip.product.v1") ‖ 00 ‖ ASCII(D) ‖ 00 ‖ uint64BE(len(C(X))) ‖ C(X) )`

with prefixes snapshot2/plan2/fact2/coverage2/view2/proof3/evidence3/seal3/run3. CapabilityManifestId is the inherited CVE1 recipe, not H. Native contexts use H domains `native.context.{typescript,rust,syntax}.v2` and universes `native.semantic-universe.{typescript,rust,syntax}.v2`.

Provider sequencing is `protocol3-transitions.v1.json` (34 rows). Identity tokens must be negotiated in HelloAck before OpenUniverse. A missing token is P3-34 FAULT with `sourceBytesSent=false`. Terminals still require zero-exit then eof.

Evaluator output is identity-schemas.v3 / evaluator3. Policy is PolicyDocumentV2 and RuleProgramV2. Proof requires `executionInputsDigest`. Unchanged native/input identities keep major 2.

## First-pass defect (implementation, not design)

The first session minted six graphs and reported `replayMatch: true` by comparing an in-memory **logical summary** (verdict, finding count, work-unit charge, root atom values). Tamper was “the edited verdict string differs.” That does not satisfy composition §7.

This continuation:

1. Exports every H frame and canonical record as digest-keyed bytes.
2. Reloads only those bytes.
3. Reconstructs inventories, view facts, Coverage payloads, scopes, policy, program, emission plan, execution-inputs.
4. Re-runs the evaluator.
5. Rebuilds proof, evidence, seal and Run.
6. Compares **C(proof)**, **C(evidence)**, **C(seal)**, **C(run)** and the four H identities.
7. Refuses an unrehashed verdict edit (identity moves).
8. Refuses a **fully rehashed false claim** that keeps valid fact/view/finding citations and self-consistent new proof/evidence/seal/run identities.

Measured on TypeScript ordinary: claimed and recomputed proof SHA-256 are both `f7d2b499a0cc89ac3769744dbe41384103ae6a01f26929972af35db28a4eab0d` (5280 bytes). Reminted false proof `proof3:8acc2441…` is self-consistent H and still byte-unequal to the replayed proof.

## Complete positive Runs (executed)

All six claimed positives: schema errors 0, retained-data `proofBytesEqual` true, all enclosing identities equal, both tampers refused, snapshot file path/hash/length joins clean. `recompute.py` re-hashed 42–67 H frames per graph with no mismatch.

| Graph | Run | Universe path | Distinct measured behaviour |
|---|---|---|---|
| ts-ordinary | `run3:9fbaf4a4…` | `native.semantic-universe.typescript.v2` | 5 inventoried files joined; 3 clone facts (L0×2, L1×1); node_modules layout retained off-inventory; ScopeDocumentV1 bound in analysis-spec |
| rust-mixed | `run3:f664f97a…` | `native.semantic-universe.rust.v2` | Mixed editions; bin target 2024 vs package 2021; `#` marker dir `crates/foo#bar`; 2 L0 clones |
| rust-partial-ownership | `run3:0dc7fe3f…` | rust | Clones Coverage `unknown` + `input-closure-incomplete` + `body-language-owner-unenumerated`; zero clone facts |
| rust-lib-only-empty-clones | `run3:443d636c…` | rust | Explicit lib-only selection; complete empty clones is lawful (not partial enumeration) |
| syntax-typescript | `run3:7e73d581…` | `native.semantic-universe.syntax.v2` | Compiler-free code grammar; inventory + clones |
| syntax-json | `run3:f7ce83b8…` | syntax | Data/document grammar; clones `unknown` / `language-tier-unsupported` / `capability-missing` — not complete-empty |

File facts stay on `enumerated`. No resolved rung was invented for them.

## Other executed controls

**CVE1 / C / H / lexical.** All eight CVE1 types round-trip. C sorts object keys by UTF-8 bytes. `1.0`, `1e0`, duplicate keys and `-0` refuse before encoding. Boolean `schemaVersion` and decoded `1.0` fail ADM-TYPE and mask later gates.

**Capability manifest.** Four gates in order ADM-TYPE, ADM-CLOSED, ADM-DOMAIN, ADM-ORDER against `capability-manifest-domains.v2.json`. A `file` relation carrying `resolved-callee` fails ADM-DOMAIN (rung of another ladder). Unsorted `platformIds` fails ADM-ORDER with `RELEASE.CAPABILITY_MANIFEST_NOT_CANONICAL`.

**Protocol 3 (executed traces, not a host).** Complete rust dependency/no-prepared one-stage trace is DONE: P3-01…P3-08, P3-11…P3-13, P3-15, P3-20, P3-22, P3-24, P3-27, P3-31, P3-32. OpenUniverse without identity tokens: FAULT P3-34, `identityNegotiated=false`, no source bytes. Unavailable and cancel reach DONE through their terminals then zero-exit/eof. Process fault: P3-33. Post-terminal Hello: `post-terminal-frame`. Frame *payload* validation and D9 mapping of terminalKind remain prose-owned (native §9.1/§10) and were not executed as a live worker.

**Three-valued missing Coverage.** `exists` and `none` over clones with no Coverage entry are both indeterminate with cause `missing-relation-coverage`. They are not vacuous false/true.

**Min-resolution.** A `syntactic-specifier` imports fact does not satisfy `minResolution: resolved-target` (false under complete empty resolved Coverage). The same fact satisfies `syntactic-specifier` (true).

**JS body vs TS engine.** Suffix `.js` → `sourceVariant=js` → `languageId=javascript`. Relabelling `languageId` to `typescript` changes body identity.

**Config graph.** `tsconfig.custom.json` is kind `other`; `extendsResolved` retains `[base, strict, base]`; `jsconfig.json` shares the base. Schema-valid.

**Keys.** Generic mutation is `H("workflow.mutation-intent", MutationReplayScopeV1)`. Repair-apply is raw SHA-256 of `C({operation,projectId,repairPlanId,baseSnapshotId})`. They differ. `repair-apply` is refused as a generic mutation operation.

**Public envelopes (schema-validated complete objects, not termination fragments).** CONFIG.INVALID (request-rejected/2); pinned purge with `evidence.pinned` and the three-consequence disclosure; HOST.INVARIANT_VIOLATED with `faultCause=host-invariant`; PROVIDER.PROTOCOL_VIOLATION; BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER. Availability notices carry typed `{capabilityId, languageMode, workspaceRoot}` on two analysis steps with different units. Candidate-only `clones-near` has no Coverage entry.

**Hidden/mismatched inputs.** TypeScript lockfile bytes ≠ claimed lock digest: join refusal, masks replay. Rust lock identity ≠ inventoried Cargo.lock: `input-closure-incomplete` / `lockfile-missing`, masks clone identity and replay. node_modules is not a snapshot inventory path.

## Pipeline ownership

| Decision | Owner |
|---|---|
| Lexical number/key admission | admission-and-qualification §1; identity §3 |
| Root/project marker | security S3; identity §2 |
| Capability request vs installed availability | admission §1.1; native §1.4; CommandEnvelope.availability |
| Manifest encoding identity | DELIVERY CAP-MANIFEST-ID-V1 + capability-manifest-domains.v2 |
| Native facts/Coverage | native-evidence + relation-payload-schemas.v2 |
| Clone body frames | fact-identity-policy.v2 + identity clones successor (L0 double length prefix) |
| Dialect / ownership pairings | identity body-language-version; native §11 |
| Pure evaluation | evaluator composition/atom/enumeration/execution-inputs |
| Proof vs seal vs Run | identity §3 acyclic graph |
| Public class/exit/detail | D9 + evaluator3 common + native public-route-registry |
| Repair apply vs generic mutation | workflows §1; repair.schema.json maps |
| Durable receipt / pins / purge | identity §5; PinnedPurgeDisclosure |

## Helper bugs vs design gaps

Every helper bug above had a precise existing normative answer. They are not new design gaps. Original failures: logical-summary replay; `KeyError: hex` on extra min-resolution Coverage objects; node_modules inventoried; inventory `digest` field validated against schema; UnifiedFeatures producer spelling; protocol trace missing SnapshotSeal.

## Unexecuted reconstruction (honest limits)

These recipes exist in the kit. This consumer did **not** mint separate sealed Runs for all of them:

- `js-synthesized` language mode as its own Run.
- An analysis whose *entry* config is the custom-named file (the repeated-base graph is a schema/identity vector).
- JavaScript clone facts inside the TypeScript ordinary Run (identity vector only).
- Imported runtime/test/history observation Runs.
- `sufficiency_v2` at resolved rungs (closed-world, unresolved-edge, universal-negative). This evaluator treats non-resolved rungs with RC-1 `not-applicable` and does not implement the resolved five-pair law. That is incomplete implementation.
- IncomingSearchV1 / TargetAttributionV1 members.
- Baseline E0 vs E1–E3 comparison graph (ScopeDocumentV1 *is* bound on ts-ordinary; a comparison axis that changes only that parameter was not sealed).
- Repair-apply descriptor graph and native-prepare authorization graph.

Synthetic TCB observations are assumptions. No compiler, OS, crypto, or SQLite measurement was performed or claimed.

## Advisories (non-blocking)

1. Use evaluator3 `D9FaultCause` `host-invariant` as selected; do not expect it on frozen `d9-exit-contract.v1.14.json`.
2. Capability-manifest platform domain is broader than the four product machine IDs; encoding admission is not a support grant.
3. Enumeration-plan digest annotations still cite identity-schemas.v2.json for `scope-descriptor`.

## Verdict

The kit supplies the semantic recipes needed to build identities, admit capability manifests, run the protocol state machine, seal language-specific Runs, replay proofs from retained bytes, and project public failures. Required positive controls that this continuation **claimed** were executed with byte-equal replay and reminted-false-claim refusal. Remaining charter items that were not sealed as additional Runs are implementation limits of this reconstruction, not missing public contracts.

**ACCEPT-RECONSTRUCTABLE.** No implementation authorization. No full-product qualification.
