# Handoff v3 — blind consumer Bv2 corrections

**Author session:** actual Claude, coauthor. I am an author, **not** the reviewer, and I cannot and
do not accept my own work. Nothing here awards readiness, discharges a gate, qualifies a platform or
authorizes implementation. **A new frozen candidate, a fresh independent review and a NEW blind
consumer all remain mandatory.** Every number below is an unpinned development check taken while
root and I were both editing.

All new scratch, probes, runs and this handoff are in
`/tmp/opensip-design-corrections/digest-corrections-author.v3/`. I rewrote nothing under any
retained snapshot, and I made no commit, push, checkout, reset or clean.

---

## 1. Owned files changed

| Path | SHA-256 |
|---|---|
| `docs/v2/contracts/product-v1/identity-and-evidence.md` | `ce73b5f7a1bef5830b6e4f89bbfa34c91299bed1b2be5fe72df5212a7bf2e464` |
| `docs/v2/contracts/product-v1/native-evidence.md` | `5f02a5994f3bd418cd81028eaf1fa27fbbfd1485079a0a832825fdffc1a0c066` |
| `docs/coop/design-corrections/foundation/identity-schemas.v2.json` | `b28c5be44c0f54e60dc9761323c06602e77496aa062d3ed40adb924492abfd38` |
| **NEW** `docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json` | `b53503c8b65f29a5e67ea27134de7251cd2921f6d435e263ea8051067e3baeca` |
| `docs/coop/design-corrections/foundation/identity-model.py` | `37b352401b557600c291ca2582037cf6155e30ffa548a84f80ff2e048d23e2f0` |
| `docs/coop/design-corrections/foundation/check-identity.py` | `6e28b16a1b0c8670825e05f9935eaab06a33277457de6a4efa5c533166e07094` |
| `docs/coop/design-corrections/native/native_evidence_model.v2.py` | `5412e0777aa4cf8eb4888aba9d8988c8829e105ff3f552f3766d7fb83455d90e` |
| `docs/coop/design-corrections/native/native-evidence.schemas.v2.json` | `9b34fe11a9b3de54d489987727ad24c84498f2b8d986b2e7ad1e98dde6826941` |
| `docs/coop/design-corrections/native/native-cases.v2.json` | `ad033e19c6bb91d7fed975edf8068c8973d26a06433de40a6677d84589d5bf50` |
| **NEW** `docs/coop/design-corrections/native/capability-manifest-domains.v2.json` | `05bcab711fcfae33288c58b6b26df4ed0bf46c9f342583f37babd717ef0d5e99` |

**Both new files must be in the next blind kit.** `relation-payload-schemas.v2.json` is named by
identity §3 and native §4.4; `capability-manifest-domains.v2.json` is named by native §11 and
identity §3. Without the first, the fact payload law is unreconstructable (that *is* Bv2 M-2).

Untouched by me: `canonical.py`, any pin, any generated report, `public-detail-registry.v1.json`,
every workflow and security file, all integration files, source maps, README/governance/readiness.

## 2. Finding dispositions

| Bv2 | Disposition |
|---|---|
| **M-1 / G1** payload document cannot constrain its payload | **CLOSED.** The blanket root-type rule is **withdrawn** — it was the wrong half of the contradiction, and it made your own bundles non-conforming. Replaced by the closed `x-opensip-payload-registry`: full-document digest + registered selector, exactly the workflows/native rule, preserved unchanged. |
| **M-2 / G2** two encoders, no fact payload document | **CLOSED.** One explicit successor law: `fact2` payloads are `C`; every logical restriction of the superseded CBOR profile survives as an admission rule; historical `FactRecord1` CBOR bytes and provenance are untouched and are never a `fact2` preimage; the provider→host conversion is stated, not delegated. All **13** relation documents supplied. |
| **M-3 / G3** mainstream TypeScript universe not constructible | **CLOSED.** `ResolvedNodeModulesLayoutV1` defined; the ordinary `node_modules`-resolving universe closes a complete Run. Both branches now constructible. |
| **M-4 / G5** `tsconfigGraphHash` has no recipe | **CLOSED.** `TypeScriptConfigGraphV1` defined with entry, ordered multi-`extends`, snapshot-joined digests, reachability and acyclicity. |
| **S-1 / G4** "Retained:" list produces a refused record | **CLOSED.** §2.2 now says **Relocated to the context** and names where each of the three went. |
| **S-2 / G6** manifest cannot express `unresolved-edge` | **CLOSED.** Current ADM-DOMAIN successor registry; all four inherited gates carried; a positive current manifest with `unresolved-edge` is bound into the Plan closure. |
| **S-3 / G7** ExecutionId grammar admits a trailing newline | **CLOSED.** The C-2 selector is named as **provenance**; the successor grammar is end-anchored, exactly as security S9.1 does for `RootV1`. |
| **S-4 / G8** `plan.budget` unconstrained | **PREMISE FALSE, and the reviewer has since retracted it.** See §3. |
| **S-5 / G9** purge refusal has no public code | **ROOT's, landed.** identity §5 now points at workflow §12's projection; `EvidenceStore.purge` untouched. |
| **S-6 / G10** `configOrigin` has no derivable input | **CLOSED.** Derived from the **entry** node of the retained graph. |
| **A-1 / G11** enumerator closure kind unstated | **CLOSED.** `provider`, stated in the schema and a new `closureKinds` table; no new kind invented. |
| **A-2** Rust stdlib inventory asymmetry | **Noted, not changed.** See §7. |
| **A-3** shared discovery rule stated twice, implemented once | **Acknowledged**; the consumer reconstructed it correctly from prose. |
| **G12** governance exclusion | **Acknowledged**, no action; the consumer confirmed it was correct. |
| **ADV-B1** (clarification) two committed budgets | **CLOSED.** `plan.budget` must equal the resolved configuration's `analysis.budget`; a legitimate override must be in the resolved configuration first. |

## 3. G8 — counterevidence, and the reviewer's own retraction

Bv2 S-4 said `plan.properties.budget` was "a bare `{"type":"object"}`". The bytes the consumer was
given say otherwise, and the current file is **byte-identical** to the kit's
(`e7d936045e4ffc67aae9a9248b4cf4bb19bb8c5e2db372df67363b3eadbb52b7` at the time I measured):

```
{"type":"object","additionalProperties":false,"required":["unit","limit"],
 "properties":{"unit":{"const":"work-units"},
               "limit":{"type":"integer","minimum":1,"maximum":9007199254740991}}}
```

I did **not** change the schema to fit the premise. Probe: `probes/p0_g8_counterevidence.py`,
result `runs/g8-counterevidence.json`. The reviewer's own clarification has since retracted S-4, and
root's independent countercheck agrees. The clarification's *real* finding, ADV-B1, is closed in §2.

## 4. New normative inputs

### 4.1 `foundation/relation-payload-schemas.v2.json`

One closed `$def` per relation for all thirteen: the twelve inherited from
`fact-plane.v1#relationPayloadSchemaRegistryV1` plus native §4.4 `unresolved-edge`. Each reproduces
the inherited `schemaId`, `schemaVersion`, `required`, `optional`, field types, enums, `universeRule`
and rung ladder **exactly** — asserted mechanically, not claimed
(`relation-payloads-reproduce-every-inherited-required-optional-type-enum-rung-and-universe-law`).
Its own `x-opensip-relation-registry` carries the rows, so relation, selector, universe rule and
ladder cannot drift from the schemas they describe.

### 4.2 `identity-schemas.v2.json#/x-opensip-payload-registry`

| Class | Keyed by | Document / selector |
|---|---|---|
| `relation` | `fact.relation` | `foundation/relation-payload-schemas.v2.json` + that document's row |
| `coverage` | `payload.schemaVersion` | `native/native-evidence.schemas.v2.json#/$defs/CoverageResultV3` |
| `import` | `import.kind` + `payload.payloadDomain` | the workflow `PayloadRegistryV1` rows, **re-derived from your registry at closure and refused on drift** |
| `parameter` | the cited `schemaDigest` | a document on the closed list (today only `foundation/import-source-context.schema.json`) |

Law: `payloadSchemaDigest` is the raw SHA-256 of the **exact full document bytes**; validation is by
the row **selector**; the codec is `C`; a key with no row **refuses** — no default row, no
caller-selected schema. A `payload.`-prefixed key name reads from the payload, every other from the
naming record.

### 4.3 `native/capability-manifest-domains.v2.json`

The current CAP-MANIFEST-ID-V1 ADM-DOMAIN successor: `RELATION-DOMAIN-V2` (12 inherited + 1),
`RELATION-LADDER-DOMAIN-V2` (per-relation ladders), the platform/deficiency/coverage-state registries
verbatim, the **declared-OPEN table** verbatim, all four gates, the traversal order, the record
shapes and the decoder bounds. `delivery.v4.json` and `fact-plane.v1.json` bytes are untouched. It
states that CVE1 (capability manifest), the superseded relation CBOR profile and `C` are three
different things and none substitutes for another. No provider or language registry is invented.

## 5. New and changed APIs

```python
# native_evidence_model.v2.py
bind_typescript_universe(universe, admission, context, retained=None, snapshot_inventory=None)  # CHANGED
typescript_config_graph_digest(graph)            # raw SHA-256 of C(TypeScriptConfigGraphV1)
typescript_config_origin(graph)                  # derived from the ENTRY node
typescript_config_graph_faults(graph)            # membership / reachability / acyclicity / kind-vs-path
resolved_node_modules_layout_digest(layout)      # raw SHA-256 of C(ResolvedNodeModulesLayoutV1)
typescript_universe_retained_input_faults(universe, context, retained, snapshot_inventory)
cve1_encode(value) / cve1_decode(raw)            # eight closed types, NFC, bounded depth 64 and 2^20 items
capability_manifest_identity(committed_bytes)
admit_capability_manifest(committed_bytes)       # ADM-TYPE -> ADM-CLOSED -> ADM-DOMAIN -> ADM-ORDER
capability_manifest_gate_vectors()               # the four gates on the live golden + three bad values
native_digest_annotation_coverage()              # 68/68 annotated, 0 unannotated

# identity-model.py
PAYLOADS, RELATIONS, RELATION_SCHEMA_DOCUMENT
validate_registered_record(document, selector, value)   # foundation docs local, others via the owner
```

`admit_capability_manifest` reproduces the published `DCM-1-core` identity
`508f24c718a0564c52fe18a1e6a5308d53bdd6012a50ad186ffbc208bb18881b` from the live delivery.v4 bytes,
and `cve1_encode(cve1_decode(golden)) == golden`.

## 6. Root's three confirmed counterexamples — all closed, re-run with root's own scripts

| Root finding | Now |
|---|---|
| **Payload memo bypass** — memo key omitted schema/rung context, so a second fact sharing one canonical payload inherited the first fact's admission | **CLOSED.** The **decode** is cached, the **admission** never is: registry-row selection, schema-document digest, rung and universe rule run on every reference. Root's `memo-probe.py`, re-run: the two-fact graph now refuses `PAYLOAD_SCHEMA_NOT_THE_REGISTERED_DOCUMENT`, control still admits. Regressions `shared-payload-does-not-cache-a-second-facts-{schema,rung}-admission` exercise **two** facts, not the invalid one alone. |
| **Coverage producer admission never re-run at Run closure** — a self-rehashed schema-valid Coverage with `subjectCount=999`, or `complete` without `attempted`, closed a Run and committed | **CLOSED.** `close_run` now re-runs `admit_coverage_result_v3` over the **retained** scope descriptor and the **retained** `unresolved-edge` facts of the view, and requires the re-derived `coverageId`. Root's `probe.py`, re-run: both vectors refuse with the native boundary's own cause; positive control closes. |
| **Capability admission incomplete** — `schemaVersion=True`, duplicate `platformId`, duplicated provider all admitted | **CLOSED.** All four inherited gates carried: ADM-TYPE with `type(x) is int` (never `isinstance`), strict-**unique** ordering, collection type checks before iteration, declared traversal order, decoder depth bound. Root's `probe.py`, re-run: all three refuse (`adm-type:…schemaVersion`, `adm-order:platformIds`, `adm-order:providers`); the inherited golden still admits. |

Recheck probes retained: `probes/p2_codex_coverage_recheck.py`, `p3_codex_memo_recheck.py`,
`p4_codex_capability_recheck.py`. Root's original successful-bypass evidence is untouched; those
results were real and I am not relabelling them.

**Root's tsconfig representation note is also accepted and closed**: `extendsResolved` is now an
**ordered array** (TypeScript 5.0 multiple `extends`, later wins), the graph carries a selected
`entryConfigPath`, and `configOrigin` derives from the **entry** — so a `jsconfig.json` extending a
shared `base.json` is a jsconfig program, which the earlier all-nodes rule got wrong.

## 7. Checks and suites (unpinned development checks)

| Suite | Result |
|---|---|
| `foundation/check-identity.py` | **445/445** (was 420 at session start, 354 in v2) |
| `foundation/check-foundation.py` | 231/231 |
| `foundation/check-product-configuration.py` / `check-product-quality.py` | 28/28 / 24/24 |
| `workflows/check_workflows.v1.py` | 1290/1290 (root's) |
| `native/check_native_evidence.v2.py` | **150/150** (was 132), 60 cells, 0 qualified, 0 open objects — disposable copy, pins regenerated in that copy only |
| `security/check-security-lifecycle.v1.py` | 456/456 — same |
| `check-integration.py` | **363/363, 0 failed** — disposable copy where **only `integration-fixtures.py`** is refreshed from my builders |

Expected `run-reference-checks.py` foundation aggregate after repinning: **231 + 445 + 28 + 24 = 728**.

**Integration in-repo currently fails** with
`FIXTURE_NATIVE_UNIVERSE:native.universe-retained-inputs-not-supplied` for one reason only: the
copied `integration-fixtures.py` predates my builders. Root has **already** adapted
`integration-host-model.py` and `check-integration.py` (verified: the new `typescript_context_inputs`
signature, the `entry.coverage` and `.get('name')` reads, and the evaluator-by-kind selection are all
in the repo). Only the builder re-copy remains, and the exact declaration list is in
`interface-note.md` §F.

Limitations recorded in the report's `limits`: single-atom fixture interpreter over the real DSL;
one vendored registry package; synthetic trusted observations throughout; no compiler, cargo, OS or
repository execution anywhere; `admit_cache_entry` is a post-construction conformance check, not a
cache subsystem. **A-2 (Rust stdlib inventory `sequence`/`minItems:0` asymmetry) is left as the
consumer found it** — the completeness rule is stated for TypeScript only, and tightening Rust's
would be a native semantic change I would rather have reviewed than slip in with a correction pass.

## 8. Bounded recommendation on the generic mutation key (no workflow edits)

You asked for a recommendation; you have since implemented essentially it, and **I agree** —
recorded so agreement is not inferred from silence.

`MutationReplayScopeV1 {schemaVersion:1, requestId, stepId, projectId, operation}` under
`H("workflow.mutation-intent", …)` is the right shape, for three reasons. (a) It removes an
underspecified "effect preimage" without inventing a semantic effect schema per operation — the same
move identity §3 made for `program-predicate`, which addresses an existing record rather than
restating one. (b) Scoping to one admitted immutable `(requestId, stepId)` is what makes
`sourceStep` position meaningful: a position is stable **inside** a retained invocation and
meaningless across fresh requests, so cross-request accidental dedup becomes impossible by
construction rather than by convention. (c) Keeping `repair-apply` on its dedicated content-derived
`rawSHA(C({operation, projectId, repairPlanId, baseSnapshotId}))` preserves the shipped cross-request
completed-repair replay, which a request-scoped key would have broken.

Two things worth stating explicitly in workflow §1 if they are not already: the key is **not**
authority (the ledger binding and the admitted immutable params/result preimages are), and a
recovery request links the original intent through the existing journals rather than by
reconstructing the key. I have made no workflow edit.

## 9. What is still open

- **Not accepted.** New frozen candidate + fresh independent review + **new** blind consumer are all
  mandatory. Every suite number here is an unpinned development check.
- **Pins and reports**: ten owned files changed (two new); I repinned nothing and regenerated no
  in-repo report. Both new files need adding to the pin sets and to the blind kit.
- **`integration-fixtures.py`** needs one re-copy from the final `check-identity.py`.
- **A-2** left unchanged, deliberately (§7).
- The `parameter` payload class has exactly one registered document today; adding another is a
  registry row, not a code change.
- Root's `PinnedPurgeDisclosure` surface is yours; I emit no public code and added none. The public
  registry is at 283 records including your `evidence.pinned`, and my three assertions confirm this
  session added nothing to it.

## 10. Retained artifacts

```
/tmp/opensip-design-corrections/digest-corrections-author.v3/
  interface-note.md                     early note + measured root-side adaptation addendum
  handoff.md, handoff.json
  CODEX-PUBLIC-NOTE.md                  root's note, read before this handoff
  probes/p0_g8_counterevidence.py       G8 premise, observed bytes
  probes/p1_native_digest_sweep.py      native 64-hex sweep: 68 sites, 68 annotated
  probes/p2_codex_coverage_recheck.py   root's coverage counterexample, re-run
  probes/p3_codex_memo_recheck.py       root's memo counterexample, re-run
  probes/p4_codex_capability_recheck.py root's capability counterexample, re-run
  runs/identity.json 445/445, f.json 231, w.json 1290, integration.json 363, security.json 456
  runs/g8-counterevidence.json
  scratch-native/, scratch-suites/, scratch-final/   disposable trees
```
