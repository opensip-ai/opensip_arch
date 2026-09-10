# Closure-kind correction review (bounded coauthor)

**Verdict: ACCEPT_SCOPED**

This is a peer review of four isolated successor files against the already-published `closureKinds.byField` law. It is not whole-design acceptance, not a freeze, and not product qualification. Root still has to merge with a separate target-identity successor and run a fresh whole-design review.

No MUST findings. No patch is proposed. SHOULD items and limitations are recorded below and do not block this scoped acceptance.

## Standing

- Reviewer: actual Grok, fresh bounded session.
- Subject: `/tmp/opensip-design-corrections/closure-kind-successor.v1` (read-only) plus the four input copies.
- Normative law: frozen candidate24 `identity-schemas.v3.json` `x-opensip-digest-domains.closureKinds` / `closureMembership` (byte-identical in the successor).
- Python: `/tmp/opensip-architecture-review-env/bin/python -I -B`.
- Writes: only this output directory. No live/frozen source edits, no pin regeneration, no network, no subagents.

Root claims (imported producer omission; registry-driven admission at retained `get`, stage-spec `payload` before memoization, and cache/regeneration keys; native five kept on owning guards; fixture adapter corrected; 27 controls; full replay 65) were treated as claims and independently re-executed.

## Custody hashes

Input copies equal the isolated successor. All four differ from candidate24 (the controls file is new).

| File | Bytes | SHA-256 (input = successor) | candidate24 |
|---|---:|---|---|
| `identity-model.v3.py` | 139262 | `5219583b1dcc014cf3782977bf955fe6c32a0a9142fe1d37ce902a005697e111` | `f0822c2f2301d611ae7a916953042deb58672a0cb356f3f381981401b58f35c3` |
| `evaluator_graph_fixture.v3.py` | 22878 | `6f5bab73af09309b85930fbef4b36fa3de48d6d089082218c35289a09f186641` | `e5ab7fe7491523e487ac00e025caa1f9e8f6f26c2c2127b6a2c5c9d0ee958c30` |
| `closure_field_kind_controls.v3.py` | 8391 | `9e41c6a3c738eb1c0e37633e3cd6fd809a38b16bc9f6e1961b3d662b55cd47ff` | absent |
| `check-replay.v3.py` | 16278 | `6b310d855ed650db5abbf3482748d418a42b92032ac277a9c2d920a830c440d4` | `ec1833ff579b0bc0445650c8beff106c277946c3d9b484c883ba5d41a1af72ad` |

Related unchanged law:

- `identity-schemas.v3.json` successor = candidate24 = `b187a21c0fbbf74c39d70c5eee7c7ac38c1b97bd2dbf69bdfddb49e299caa3f3`
- Input `correction.patch` = `222d969dd6ab38bf15a7c208573926e84fa71f0e2c84da8501275cba9dc77021`
- Historical evaluator2 `identity-model.py` (candidate24) = `12c9cc226b582adc8e34a55e8a59671f2611c46d3e27d1d8289a472d78ccacb6` and still has no `admit_closure_field_kinds`

Independent rerun of successor `check-replay.v3.py` produced stdout SHA-256 `0678dd7fa1dd5a1a337b711216f8539d1113d8f1ffbf0af88b982554678965b6`, byte-identical to the input receipt, `passed: true`, `count: 65`, empty stderr. That count is a measurement, not an acceptance oracle.

## Published field set (15)

`closureKinds.byField` and the union of `closureMembership.{direct,equalToDirect,selectedThroughOtherInput}` are the same 15 names. No remainder.

| Field | Required kind | Membership class | Owning admission | Wrong-kind fault |
|---|---|---|---|---|
| `subject-scope.enumeratorClosure` | provider | direct | `open_run_closure.get` (and retained later named check) | `ENUMERATOR_CLOSURE_KIND` |
| `view.producerClosure` | provider | direct | `get` | `CLOSURE_FIELD_KIND:view.producerClosure:provider` |
| `fact.producerClosure` | provider | equalToDirect (enclosing view) | `get` | `CLOSURE_FIELD_KIND:fact.producerClosure:provider` |
| `finding.ruleClosure` | detector | direct | `get` | `CLOSURE_FIELD_KIND:finding.ruleClosure:detector` |
| `evaluation-seal.evaluatorClosure` | evaluator | direct | `get` | `CLOSURE_FIELD_KIND:evaluation-seal.evaluatorClosure:evaluator` |
| `proof-bundle.evaluatorClosure` | evaluator | equalToDirect (seal) | `get` | `CLOSURE_FIELD_KIND:proof-bundle.evaluatorClosure:evaluator` |
| `import.producerClosure` | provider | selectedThroughOtherInput (`plan.importIds`) | `get` | `CLOSURE_FIELD_KIND:import.producerClosure:provider` |
| `import.adapterClosure` | adapter | selectedThroughOtherInput (`plan.importIds`) | `get` | `CLOSURE_FIELD_KIND:import.adapterClosure:adapter` |
| `stage-spec.producerClosure` | provider | direct | `payload` before `parsed` memo | `CLOSURE_FIELD_KIND:stage-spec.producerClosure:provider` |
| `cache-key.producerClosure` | provider | direct | `admit_cache_entry` (also regeneration-key via shared schema) | `CLOSURE_FIELD_KIND:cache-key.producerClosure:provider` |
| `TypeScriptToolClosureV1.closureId` | toolchain | selectedThroughOtherInput (`nativeContextDigests` + `closureJoins`) | `admit_native_context` | `native.native-context-closure-kind-mismatch:toolClosure.closureId` |
| `ToolClosureV1.closureId` | toolchain | same | `admit_native_context` | `native.native-context-closure-kind-mismatch:toolClosure.closureId` |
| `toolchain.typescriptStdlibMerkleRoot` | stdlib | same | `admit_native_context` (suffix form) | `native.native-context-closure-kind-mismatch:toolchain.typescriptStdlibMerkleRoot` |
| `toolchain.rustcDevLlvmDigest` | rust-dev-llvm | same | `admit_native_context` (suffix form) | `native.native-context-closure-kind-mismatch:toolchain.rustcDevLlvmDigest` |
| `SyntaxGrammarBundleV1.closureId` | grammar | same | `admit_native_context` | `native.native-context-closure-kind-mismatch:grammarBundle.closureId` |

Identity-schema `closure2:` fields that are **not** in `byField` are mixed-kind sets, not single-role fields: `plan.semanticClosures[]` and `semantic-grant.principals[].closureId`. No new public role is invented for them. Selection of those closures remains Plan/grant membership, not a kind enum.

Native `closureJoins` in `identity-schemas.v3.json` are exactly the five native rows above (TS tool + stdlib suffix, rust tool + llvm suffix, syntax grammar). Identity-model still joins those kinds at `admit_frame` (`NATIVE_CONTEXT_CLOSURE_KIND`) and then re-runs `admit_native_context`. The helper is not applied to native nested records.

## Owner call graph

```
close_run / public Run / admit_cache_entry
  -> complete replay (strong profile)
  -> open_run_closure
       get(key, domain)
         identifier + domain check
         admit_closure_field_kinds(domain, value, get(., 'closure'))
         return
       payload(digest, kind)          # stage-spec lives here, not in get()
         canonical + schema
         admit_closure_field_kinds    # BEFORE parsed[(local,digest,kind)] = value
         memoize
         walk
       visit -> get then walk
       admit_frame(native-context)
         closureJoins kind
         native_admission().admit_native_context
admit_cache_entry
  -> close_run
  -> open_run_closure
  -> cache_key / identifier
  -> admit_closure_field_kinds(cache-key|regeneration-key aliased to cache-key)
  -> CACHE_PLAN_JOIN / CACHE_STAGE_* / CACHE_UNSELECTED_PRODUCER
```

`get('closure', ...)` does not recurse: no `byField` name starts with `closure.`. Prefix matching is not greedy across `ToolClosureV1` vs `TypeScriptToolClosureV1`. `regeneration-key` is aliased to the published `cache-key.producerClosure` name, matching `$ref` of the regeneration-key schema onto cache-key.

Candidate24 `open_run_closure.get` had no kind helper. The published import producer/adapter kinds were therefore unenforced on the current identity owner. That is the confirmed omission.

## Membership without flattening

On a complete imported positive Run (`run3:979039ae13a999d41a5069e5d45b008b5c7304ef481b86a93cc9bc55f43d2189`):

- `import.producerClosure` kind `provider` and **is** in `plan.semanticClosures` (the enumerator/provider is reused).
- `import.adapterClosure` kind `adapter` and **is not** in `plan.semanticClosures`.
- `semanticClosures` kinds remain `{detector, evaluator, provider}`.
- Native contexts remain Plan-selected via `nativeContextDigests` (one syntax context in this fixture), not by copying native tool/stdlib/grammar closures into `semanticClosures`.

The fixture now mints a distinct adapter descriptor instead of passing the enumerator provider as adapter. Workflow `build_import` still only stores the two identities; kind is enforced at identity `get`, which is the right owner.

## Current vs historical profile and public routing

- Current evaluator3 (`identity-model.v3.py`) gains the helper on `get` / `payload` / cache keys.
- Historical evaluator2 (`identity-model.py`) is unchanged and still only has the later `ENUMERATOR_CLOSURE_KIND` join. That split is coherent: this successor is current-profile only.
- `ENUMERATOR_CLOSURE_KIND` is preserved as the enumerator fault name (helper special-case plus the old later check).
- New `CLOSURE_FIELD_KIND:<field>:<expected>` is an internal `AdmissionError`, like `UNSELECTED_*` / `REFERENCE_IDENTITY`. It is not a `DomainDetailCode` and does not add a public role enum.
- Combined defects now fail kind at `get` before `UNSELECTED_ENUMERATOR` / `REFERENCE_SOURCE_JOIN`. That is a current-profile order change for *combined* defects only. Isolated unselected-correct-kind and isolated wrong-kind-selected still keep their old names. See SHOULD.

## Tests actually reach the stated boundaries

Controls are not helper reflection or a registry-count assert with a standing sentence. They:

- remint hostile record identities and call `owner['get']` for the eight local identity fields;
- call `owner['payload']` twice on a wrong stage-spec digest (canonical-record, not get);
- call `admit_cache_entry` for cache-key and regeneration-key, with detector as wrong kind while detector **is** Plan-selected (role, not membership);
- remint every H identity of a whole import graph and call `open_run_closure` only, with boundary text that semantic replay is not reached;
- call `native_admission().admit_native_context` on reminted closure identities for all five native fields, after constructing the native fixture with the required TypeScript source inventory (`TS_SOURCES` plus `a.ts`). The earlier missing-inventory attempt failed construction (`FIXTURE_NATIVE_UNIVERSE`) and was not graded.

The imported positive is a complete `R.replay`, not a registry walk. Independent replay of that graph admitted with the same run id as the input control row.

The whole-import negatives are structural: independent `open_run_closure` and even `R.replay` both return `CLOSURE_FIELD_KIND:import.{producer,adapter}Closure:...` and never `EVALUATOR_COMPLETE_PROOF_REPLAY`. Existing full semantic-negative suite is untouched.

## Independent discriminating probes

Script: `output/probes/independent_closure_kind_probes.py` (SHA-256 `76a1d49ee2a157ea498d6fd818611d056f983514599f681673078e9571d8291f`). Results: `output/probes/independent_closure_kind_probes.json`. Full replay: `output/probes/independent-full-replay.stdout.json`.

| Probe | Result |
|---|---|
| Imported complete replay, all object identities valid | ADMIT `run3:979039ae13a999d41a5069e5d45b008b5c7304ef481b86a93cc9bc55f43d2189` |
| Adapter not in `semanticClosures`; producer is; kinds adapter/provider | confirmed |
| `get(import)` does not recurse | ADMIT |
| Reminted wrong enumerator via `get` | `ENUMERATOR_CLOSURE_KIND` |
| Wrong-kind **and** unselected enumerator via `get` | `ENUMERATOR_CLOSURE_KIND` (kind before unselected) |
| All eight local identity fields via reminted `get` | exact expected faults; identities valid |
| Stage-spec wrong producer, three retries + new owner | all `CLOSURE_FIELD_KIND:stage-spec.producerClosure:provider`; good digest still admits |
| Cache/regen positive; detector-as-producer (selected) | ADMIT then `CLOSURE_FIELD_KIND:cache-key.producerClosure:provider` for both domains |
| Cache unselected **correct** kind | `CACHE_STAGE_SPEC_PRODUCER_JOIN` (membership still a later join; this key also fails producer-join) |
| Whole-import wrong producer/adapter, identities reminted | structural `CLOSURE_FIELD_KIND`; replay same fault, not semantic |
| Whole-run reminted `view.producerClosure` | `CLOSURE_FIELD_KIND:view.producerClosure:provider` |
| Native TS/rust/syntax positives | empty refusals |
| Native five reminted provider-kind closures | each expected `native.native-context-closure-kind-mismatch:...` only |
| Independent `check-replay.v3.py` | passed 65, stdout byte-identical to input receipt |

## MUST findings

None.

Registered roles are enforced on the actual owning paths. Caching of failed stage-spec payloads does not bypass kind. Record traversal `visit` always `get`s first. Native five remain on `admit_native_context` (and identity `closureJoins`). Plan membership is not flattened. No further single-kind field in bounded scope is missing from `byField`. No new public role enum.

## SHOULD findings

1. **Combined-defect order (enumerator).** `get` now raises `ENUMERATOR_CLOSURE_KIND` before `UNSELECTED_ENUMERATOR` / `REFERENCE_SOURCE_JOIN`. Isolated cases keep their names. If a later consumer ever asserted “unselected wins combined defects,” current v3 would disagree with historical evaluator2. Not required for this scoped law: kind is a property of the retained descriptor.

2. **Do not reuse `admit_closure_field_kinds` for native nested records.** Prefix `toolchain.` would match both language suffix fields. Current code does not call the helper for those records; native admission stays the owner.

3. **Local identity negatives are extra-record `get`s** except import whole-graph and the independent whole-run view probe. That matches the stated boundary (“not whole Run”). A later whole-design review should keep at least one reminted-graph case per identity field if it wants visit-order coverage as well as `get` coverage.

## Limitations

- Did not read consumer stores, blind helpers, other successor copies, or private CLI logs. The input “exact prior import refusal” row is therefore a claim about historical consumer bytes; equivalent producer=`adapter` graphs were constructed from the successor fixture and refused at the new guard.
- Did not run historical `check-identity.py` / evaluator2 close_run. Historical profile is out of this successor’s four files.
- Did not qualify a compiler, provider, or product implementation.
- Did not freeze source pins or merge with the target-identity successor.
- `admit_cache_entry` still requires a strong Run first; a wrong-kind key is not a cheap miss. That is existing cache-admission standing, not a bypass.
- Public envelope mapping of identity `AdmissionError` strings is unchanged and still not a DomainDetailCode concern.

## Conclusion

ACCEPT_SCOPED. The published import producer/adapter kinds are now enforced on the current identity owner; the other thirteen registered fields are accounted to an actual owning path with discriminating reminted identities; Plan selection is not flattened; native five stay on native admission; the controlled whole-import negative is structural. Fresh whole-design review remains required after the non-overlapping merge.
