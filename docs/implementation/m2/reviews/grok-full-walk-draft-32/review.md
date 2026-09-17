# Draft critique: full structural walk (snapshot 32)

**Reviewer:** Grok. Root remains lead. Not Claude agreement.  
**Kind:** Bounded **draft source** critique of the immutable seven-file snapshot. **Not ACCEPT-DESIGN-UNIT. Not replay. Not fresh-blind. Not live install. Not M2 complete.**  
**Work tree:** `/tmp/opensip-implementation/m2-grok-full-walk-draft-32/review`. Snapshot, trial-32, live, frozen, and history were not edited.

Root remains implementation lead and is independently extending tests in editable `/tmp/opensip-implementation/m2-full-walk-trial-32`. This review does not treat those tests as closed, does not refresh identity source-policy, and does not run full workspace on 32.

## Pins

Snapshot `manifest.json` **1104** / `9df549752ecb64adb80afeb894389198ea41d4890e391981b800f1b468ed5842`. All **7** members still pin-match the **immutable snapshot** on disk. This critique’s subject is that snapshot, not later trial edits.

At first observation, trial-32 `product/` matched those seven paths. **Current** trial product has moved (format/source-policy plus registry-driven body/nested dispatch): six of seven paths **DIFF**; `relations.rs` still matches. Do not assert present trial equality. Live tree **DIFF**s all seven; live still has no `full_walk.rs`. Canonical-input / reference walk-order is **not** re-audited here; that bounded advisory is `/tmp/opensip-implementation/m2-grok-canonical-walk-order-33` (wH:p5).

| Path | Bytes | sha256 |
| --- | ---: | --- |
| `crates/identity/src/closure.rs` | 55265 | `86902be8d1610f129d03044d15bbff8e29c09462b0a7ecac00865b0d5fbcb3d3` |
| `crates/identity/src/lib.rs` | 1586 | `1f8bc4000b0959fa79f3b7ccc136f76990635e21d1214f9f9b10280b55fe1101` |
| `crates/identity/src/relations.rs` | 12985 | `672ae3d577ada9f8f22dd936e0a05e8607c9a48e6d3354e5a86d334104471967` |
| `crates/evaluator/src/lib.rs` | 2578 | `ca86766ad0d3e6ccb6eb9a778e9745efa80de1174ea198cd037710e6fe3ad85d` |
| `crates/evaluator/src/full_walk.rs` | 11371 | `ae27c088e24dcd82248531354245d5085568181877e138c608428cd517392374` |
| `crates/evaluator/src/native_retention.rs` | 16212 | `1c9c374cb33ba3adcf475626b63e0d612287815d6c09108c643a635edd2a582a` |
| `crates/evaluator/src/run_links.rs` | 11806 | `991fc946087ef5c17fbc6f2c79ab405439ae725ca8b12ad59db5212f8b58bd14` |

Selected identity overlay `identity_model.py` **158739** / `7b6750a918124128f045fc64e2c48a75b68ba8b4373e51f0c3b246c3835c0da2` (`open_run_closure`, not ReplayedRun). Selected Wv1 helper **142991** / `60dc11e2d997021ea43030d0b9912b41871fe9539bab7a0782c72c17a0adb180`. Unchanged Wv3 wrapper **22494** / `60f28dc97114cf918a92f5c8bb99a3b3e5d73a2608a7b9d289b7a9f652a36123`. Selected I+W is **wrapper + 60dc**, not replacing the wrapper with 60dc.

Advisory31: `advisory.md` **13918** / `868a8dfd…003d`, `advisory.json` **5029** / `871b9979…131f`, verdict **NOT ACCEPTANCE**.

This review observed live `design-lock.json` **66066** / `116fefcc033b2b7b2a441c6b55f414b581bada8586a3b3745ec39e0e445514e3` (**22** inventory / **31** contract; last inventory candidate v24; last contract native-runtime-selection-v15). Live now has `import_payloads.rs` **5836** / `acf9691d…1788` (byte-identical trial-32 product). Live still lacks `full_walk.rs`. That live movement is **not** a draft-32 omission.

## What this draft is

Identity owns `StructuralOwner` / `StructuralObligation`. Evaluator `inspect_retained_walk(inputs, run_id, limits)` is the fixed composition: no caller owner, no caller registry, no caller census. Default `inspect_identity_record` / `inspect_current_record` / `inspect_local_structure` still construct `RejectOwner`. `RetainedWalkChecks` is counts only — not ADMIT, not a Run, not replay.

## Default reject (generic `StructuralOwner`)

`object` defaults to `Ok(())` (`closure.rs` **238**). `RejectOwner::resolve` maps the five Walker cuts to the same five live `Unsupported` strings (`closure.rs` **241–251**):

- Retention → `"retention owner join"`
- StageSchema → `"stage output schema owner join"`
- Capability → `"capability derivation"`
- NativeFrame → `"registered H-frame domain set"`
- Payload → `"payload-class owner joins"`

`inspect_relation_sources` still independently `Unsupported("relation body identity owner")` when the relation row has `bodyIdentityJoin` (`closure.rs` **367–368**). Default inspect never entered that API; body is now a Payload-arm dispatch. Limits observation `default-remains-unsupported` still gets `Unsupported("capability derivation")` on a Run. Walker no longer contains leftover `Unsupported` in `digest_field`; those five cuts call `owners.resolve`.

`Walker::visit` still does **not** implement `REFERENCE_SOURCE_JOIN` / `REFERENCE_PLAN_JOIN`. Those live only in `ClosedOwner::object_join` (`full_walk.rs` **88–107**). Default inspect of a lone fact therefore still does not emit them (first H-frame / payload / capability remains Unsupported). That matches advisory31.

`inspect_structure_with_owner` is public (`closure.rs` **604–616**). Advisory31 allowed an optional public diagnostic returning only `StructuralChecks`. `inspect_retained_walk` accepts **no** caller owner and always builds private `ClosedOwner`. Proposed `pub(crate)` cannot compile: `RetainedInputs` lives in `opensip-identity`, `ClosedOwner` in `opensip-evaluator`. No path from `StructuralChecks` to Run / replay / publication was identified. Finding `public-with-owner-deferred-ok` is **withdrawn** as required (reconsideration below).

## Fixed composition joins and order

`inspect_retained_walk` after `inspect_structure_with_owner` (`full_walk.rs` **190–213**):

1. `inspect_run_links_with_capabilities` (walk-derived `capability_ids`; standalone `inspect_run_links` still passes `&[]` so `FOREIGN_CAPABILITY_MANIFEST` is composition-only — `run_links.rs` **142–147**, **181–184**)
2. `inspect_plan_native` with **derived** `contexts` / `universes` (not caller census)
3. `UNIVERSE_FRAME_UNRETAINED` (`full_walk.rs` **201–203**)
4. `inspect_policy_program`
5. `inspect_stage_specs` (schema **admit**; walk only blobbed StageSchema)
6. `inspect_evidence_roots`
7. `inspect_predicate_witnesses`
8. per-view `inspect_view_joins`
9. `inspect_import_joins` (this owner already calls `parameter_selection` even with zero imports — trial `import_joins.rs` **280**)

That is the selected Python post-walk order (`identity_model.py` **1650–1986**). Residual Python `get` of evidence coverage/import/finding (**1987–1988**) is already implied by identity-schema walk of those prefixed ids plus `inspect_evidence_roots`. Not a missing composition call.

`object_join` matches selected `visit` (**1646–1647**): Snapshot/Fact/SubjectScope `snapshotId`/`projectId` vs Run; View/ProofBundle/SemanticEvidence/EvaluationSeal/ExecutionPlan `planId` vs Run. Missing Snapshot/Fact `projectId` uses the Run value (`unwrap_or`), same as Python `value.get(..., run[...])`. Trial `semantic-result.json` REFERENCE cases match named causes (outcome class). `fact-foreign-and-missing-child` / `view-foreign-and-missing-child` refuse the join **before** the missing child.

Walk-time Payload:

- Decode blob before class dispatch (`full_walk.rs` **137**), matching Python decode-before-registry.
- `import`: `import2:` + identity of **siblings** (the import descriptor), then `inspect_import_payload`. Not payload-digest-as-id. Two-key select stays inside that owner.
- `relation`: `inspect_relation_prefix` (ladder + anchor cardinality) on the first copied owner budget, then `inspect_syntax_fact` (new invocation), then `inspect_relation_snapshot` (full `payload_rules` + snapshot joins, new invocation), then optional body. That is selected walk-time order: prefix / `syntax_capability_supported` / rung-universe-NFC / `relation_source_joins` / body (`identity_model.py` **1297–1480**). Prefix-before-syntax is an early-fault match, not a late syntax.

Capability ids are **collected** at walk (`full_walk.rs` **115**) and admitted only in run-links. Stage-output schema is **blobbed** in `digest_field` before `StageSchema` (`closure.rs` **863–872**); ClosedOwner then `Ok`s. Fragment / owner-retained do **not** blob; ClosedOwner `Ok`s; later explicit joins recompute. That is the selected split.

## Nested actual census

`NativeRetentionChecks::frame_digests` is `pub(crate)` (`native_retention.rs` **29–31**) and yields actually traversed `(set, digest)` pairs. Composition uses `inspect_native_frame_inputs` (`bind_universe=false`, **70–77**): Context still admits `inspect_native_context`; SemanticUniverse is stored, not bound; Nested identities are walked. Plan-native later re-walks derived lists under a **copied** owner budget and performs universe binding. Walk NativeFrame plus plan-native re-walk is double-walk, not one aggregate steps counter. Advisory31 allowed that.

ClosedOwner folds all three sets into `frames`, Context digests into `contexts`, SemanticUniverse digests into `universes` (`full_walk.rs` **128–132**). `UNIVERSE_FRAME_UNRETAINED` compares `object_join` Fact/SubjectScope `sourceUniverse`/`targetUniverse` (bare 64-hex via `sha256_text("sha256:{text}")`) against that universe set. Representation matches identity-v3 (`sourceUniverse` pattern `^[0-9a-f]{64}`).

Memo: after charging an invocation, duplicate `(set.name(), digest)` NativeFrame obligations skip (`full_walk.rs` **123–124**). Skip key includes **set**, so Nested vs SemanticUniverse of the same digest does not suppress the universe census. `inspect_syntax_fact` → `selected_syntax` also calls `inspect_native_frame_inputs` (trial `capability_support.rs` **192–206**) but does **not** write `ClosedOwner.frames`, so it cannot cause a premature skip of the later NativeFrame census. Payload decode is not memoized; each relation/import reference re-runs (Python: decode cacheable, admission not).

**Required hole:** `nestedIdentities` still `Law` unless `domainSet=="native-nested"` then always `NativeFrameSet::Nested` (`native_retention.rs` **325–340**). Selected `admit_frame` recurses with `join['domainSet']` (`identity_model.py` **1622**). Current identity-v3 nested rows are all `native-nested`, so the ten positive fixtures do not distinguish. A nested universe/context would never appear in `frame_digests(SemanticUniverse|Context)` and would refuse instead of entering Plan census. See `nested-identity-domainset`.

## Deferred obligations

Inside `ClosedOwner::resolve_owned` only (`full_walk.rs` **112–114**):

```
Retention | StageSchema => Ok(())
```

Capability records an id. NativeFrame and Payload run owners. That is the correct ClosedOwner policy.

The public `inspect_structure_with_owner` path is the defect: identity cannot know whether later owners will run. Make that API crate-private so only this composition can defer.

## Memo and three development bounds

`RetainedWalkLimits` is three **separate** fields (`full_walk.rs` **16–24**, comments **17–18**). `inspect_retained_walk` Limits immediately if walk steps/depth, owner steps/depth, or `owner_invocations` is 0 (**181–183**). `ClosedOwner::budget` decrements `remaining` then copies `limits.owner` (**84–86**) — copied local budgets are not one remaining-steps counter. Walk `TraversalBudget` is the `inspect_structure_with_owner` argument and is not subtracted from owner steps.

Invocation cap is shared across walk `resolve` calls **and** post-walk owners (each post-walk owner is one `budget()`). Plan-native internally copies the same owner budget into each retention (`plan_native.rs` **67–69**, **125**). That matches advisory31: one invocation for `inspect_plan_native` itself; nested retentions keep independent local bounds.

Relation Payload charges extra invocations for syntax / snapshot / body inside one Walker obligation (`full_walk.rs` **147–150**). Advisory listed those as separate owner dispatches. Default-packet measures **42** `ownerCalls`; `at-owner-boundary` is checked at 42; `one-below-owner-boundary` Limits. Internally consistent. Duplicate NativeFrame references also charge then skip — recursive cap, not selected Plan work-units.

`descriptor_work==0` is not in the early zero check; `walkWork-0` / `ownerWork-0` fail at schema Limit. Fine: that bound is per schema admit, not the invocation cap.

Census `contexts`/`universes` are `BTreeSet`s, so plan-native binding first-fault order is sorted digest order, not Python insertion order. Outcome class is unchanged; named-cause first-fault is not claimed (330 oracle is outcome-class only).

## Early / late vs selected Python (not silent accepts)

These are wrapping / phase observations from trial `semantic-result.json`. Outcome classes matched; they are not product defects inferred from the initial wrong oracle.

| Probe | Python | Draft | Note |
| --- | --- | --- | --- |
| `fact-sourceUniverse-0` missing universe blob | `EVIDENCE_UNAVAILABLE:1111…` | `Syntax(Retention(…MissingBlob(1111…)))` | `payloadDigest` < `sourceUniverse` in BTree walk, so `inspect_syntax_fact` loads the universe **during Payload**, before the NativeFrame obligation. Selected `syntax_capability_supported` also `admit_frame`s during payload. Same phase; Syntax wrapping is early relative to NativeFrame, not relative to Python. |
| `subject-scope-sourceUniverse-0` | `EVIDENCE_UNAVAILABLE` | `Retention(…MissingBlob)` | Scope has no relation Payload; NativeFrame is first. |
| `file-payload-path-*` snapshot join | `RELATION_PATH_NOT_INVENTORIED` / `RELATION_FILE_CONTENT_JOIN` | `Graph(RelationRule("path not inventoried"))` / `"file content join"` | After prefix+syntax, during snapshot. Selected order. |
| `clone-body-*` | named `BODY_*` | `Body(Refused("BODY_*"))` | Body runs **after** snapshot. `clone-body-mapped` ownerCalls **55** vs default **42**. |
| Extra context discovered only via syntax `contextField` | `NATIVE_CONTEXT_SET_JOIN` (syntax `admit_frame` writes `native_contexts`) | `UNIVERSE_CONTEXT_NOT_SELECTED` later in plan-native (syntax does not write ClosedOwner census) | Both refuse; draft cause is **late** / renamed. No silent accept. |

## Trial evidence (not compiler qualification)

Ten positive fixtures: all `checked` (`positive-result.json` **2213** / `ee54025c…2c55`). Contexts 1; universes 1 except `two-universes-packet` (2). Synthetic reference packets, not compiler qualification.

Corrected 330 missing/corrupt-store oracle (`missing-result.json` **460** / `8b37d4c6…2e7e`, `workflowSha256` **60dc**): **0** outcome-class mismatches; 6 checked, 125 invalid (`BLOB_DIGEST`), 199 unavailable. Actual rows serialize `error` vs expected `unavailable` for missing store — label-level mapping, **not** selected-vs-Rust law disagreement.

Initial harness replaced the Wv3 wrapper with Wv1 (`initial-wrong-workflow-loader/missing-result.json` **2821** / `2434fab1…1655`): **6** false `RULE_PROGRAM_COMPILATION_JOIN` on golden / missing / corrupt blobs of `two-universes-packet` and `all-import-kinds-packet` (those cases actually `checked` under wrapper+60dc). **Do not infer a product defect from that oracle.**

Limits 19/19 class-aligned (`limits-result.json` **3607** / `83450de8…8374`). Semantic 49, variant 15, shared 8: `mismatches: []` on outcome class under the canonical-map comparison. Preserved insertion-order and incomplete-rekey oracles are separate (below); do not fold them into this row.

Known pending, **not** draft omissions: host regression corpus, identity source-policy refresh, full workspace on 32.

## requiredFindings (immutable snapshot)

Finding `public-with-owner-deferred-ok` is **withdrawn** (see reconsideration). Two snapshot holes remain. Trial product later adopted both; those trial bytes are **not** this snapshot and are **not** accepted here.

### 2. `body-dispatch-clones-not-flag`

Payload relation body arm (`full_walk.rs` **149–151**):

```
if text(field(siblings, "relation")?)? == "clones" {
    inspect_body_identity(...)
}
```

Selected law is the relation-payload row flag (`identity_model.py` **1480** `if 'bodyIdentityJoin' in row`; `inspect_relation_sources` **367** `contains_key("bodyIdentityJoin")`). Today only `clones` carries the object (`relation-payload-v2.schema.json` **152**), so the ten fixtures and `clone-body-*` variants pass. The program is still the relation **name**.

Sibling `inspect_body_identity` (trial `body_identity.rs` **407–421**, not in this snapshot) also requires `relation=="clones"` and reads `body-registry.json` `"clones"` rather than the payload-v2 row. Composition dispatch must still use the flag; generalizing that sibling is a follow-up if a non-clones row ever carries `bodyIdentityJoin`.

**Action:** resolve the relation-payload-v2 row from `siblings.relation` (already done for prefix/snapshot). Call `inspect_body_identity` iff the row has `bodyIdentityJoin`. Do not special-case the string `"clones"`.

**Probe:** (a) current clones fact — body still runs (variant `clone-body-mapped` ownerCalls 55; `clone-body-missing-map` `BODY_NORMALIZATION_MAP_MISSING`). (b) synthetic `file` (or other) row with `bodyIdentityJoin` copied from clones — Python runs `body_identity_join`; snapshot skips. (c) clones row with the flag deleted — Python skips body; snapshot still calls. (b) and (c) are distinguishing; they are **not** valid inputs to the source-pinned current registry. Sibling `inspect_body_identity` still only supports current clones. Trial product later returns the flag from `inspect_relation_prefix` (trial `closure.rs` **376**) and dispatches on `body_required` (trial `full_walk.rs` **213–216**); that is not this snapshot. Future registry changes remain separately reviewed.

### 3. `nested-identity-domainset`

`native_retention.rs` **325–327** / **340**: nested identities refuse unless `domainSet=="native-nested"`, then always `self.frame(..., NativeFrameSet::Nested)`. `frame_digests` then cannot emit that digest as Context or SemanticUniverse. Selected `admit_frame` uses `join['domainSet']` (**1622**). ClosedOwner census (**128–132**) trusts those set names for `NATIVE_CONTEXT_SET_JOIN` / `UNIVERSE_FRAME_UNRETAINED`.

**Action:** map `join['domainSet']` to `NativeFrameSet` (`native-context` / `native-semantic-universe` / `native-nested`); recurse with that set; keep `frame_digests` as the actual traversal export. Unknown set remains Law. Do not hardcode Nested.

**Probe:** current fixtures unchanged (all published nestedIdentities rows are `native-nested`, identity-v3 **4158+**). Distinguishing probe: a universe (or context) nestedIdentities row with `domainSet: native-semantic-universe` (or `native-context`). Python adds the child to `native_universes` / `native_contexts`. Snapshot Laws at **325–327** and never folds the digest into `owner.universes` / `owner.contexts`. Mutated registry rows are **not** valid inputs to the source-pinned current registry; they only distinguish the algorithm. Trial product later maps `join['domainSet']` (trial `native_retention.rs` **328–346**); that is not this snapshot.

## What is correct (not required)

- Five-string `RejectOwner`; default `inspect_*` fail-closed; `object` default Ok so REFERENCE is composition-only.
- `inspect_retained_walk` derives census; no caller owner/registry/census; `inspect_run_links` standalone still `&[]`.
- Post-walk owner order vs selected I; import two-key via `inspect_import_payload(import_id)`; parameter selection inside `inspect_import_joins`.
- Stage-schema blob-at-walk / admit-at-`inspect_stage_specs`; fragment skip only in ClosedOwner.
- Three separate development limits; copied owner budgets; plan-native independent per-retention bounds; `frame_digests` crate-private.
- Relation nonstring still unreachable after fact/scope `type:string`; `relations::row` still takes `&str`.
- Never `match Unsupported(_) => Ok(())`.

## Limits / not claimed

Not ACCEPT-DESIGN-UNIT, not replay / `ReplayedRun` / publication custody, not fresh-blind, not M2 complete, not compiler qualification, not host regression corpus, not identity source-policy refresh, not full workspace on 32, not live install of these seven files.

Do not treat 330 `error` vs expected `unavailable` as a selected-law mismatch. Do not treat the six initial `RULE_PROGRAM_COMPILATION_JOIN` mismatches as product defects. Do not treat 47+76 exploration owner-isolation checks as this full walk.

Named-cause / first-fault parity is **not** claimed (BTree census order; Syntax wrapping of missing universe blobs; `UNIVERSE_CONTEXT_NOT_SELECTED` vs `NATIVE_CONTEXT_SET_JOIN` for syntax-only extra contexts). Compound-fault precedence on non-canonical Python dicts is extra-product; comparison is on the canonical map domain only (limitation below).

## Reconsideration: `public-with-owner-deferred-ok` withdrawn

Root’s crate split is correct. `inspect_structure_with_owner` is a method on identity `RetainedInputs`. Evaluator `ClosedOwner` must call it. `pub(crate)` would not compile across `opensip-identity` / `opensip-evaluator`. Advisory31 already allowed an optional **public** diagnostic with-owner that returns only `StructuralChecks`, not an admission token. Public `inspect_retained_walk` takes no owner and always constructs private `ClosedOwner`. `StructuralChecks` cannot mint a Run id, replay result, or publication ledger. A no-op callback owner can produce diagnostic counts only; that is already documented as no semantic guarantee. Default `inspect_*` remain `RejectOwner`.

No authority/acceptance path from this public diagnostic API to full closure was identified. Equating diagnostic counts with `inspect_retained_walk` would be the defect; the API does not do that. **Withdrawn as required.** Remaining limit: hosts must call `inspect_retained_walk` for the composition; `inspect_local_structure` must stay fail-closed.

## Projection limitation (walk-order not re-audited here)

Deep normative audit of Python `dict.items` vs Rust `BTreeMap` is **wH:p5** `/tmp/opensip-implementation/m2-grok-canonical-walk-order-33` (`advisory.md` **4382** / `9a1aefca8420ccf466d07d2643bc9ae450c60221b726e8f816cf07d3bae911d4`, `advisory.json` **3984** / `e4944999f1c548000c9993c92bf3cad84bf69aa8a2e271390c1125d62192005f`): narrow oracle projection is sufficient; no identity successor now.

This composition critique records only the **limitation**: Rust structural comparison is against `C.parse(C.canonical(v))` / retained C bytes, not arbitrary CPython insertion-order first-fault. Insertion-order oracle (`initial-insertion-order-oracle/shared-result.json` **4271** / `78a7eb91…9b02`, two class mismatches) stays negative evidence. Incomplete-rekey old-view `MissingObject` (`view2:633a6f58…`) was a fixture hole, not a missing body/anchor owner.

After complete retained-record rekey, current `shared-result.json` **3128** / `7046de64…9d48`: `shared-payload-valid` **checked** on both sides; invalid second span is exact `BODY_IDENTITY_BODY_SPAN` / `Body(Refused("BODY_IDENTITY_BODY_SPAN"))`; range `ANCHOR_RANGE`; path `ANCHOR_SOURCE`. Not a claim that selected I.walk is already canonical.

## Current trial receipts (not snapshot acceptance)

Observed on trial-32 product **after** it diverged from the snapshot. Not frozen-source acceptance, not workspace-as-this-snapshot.

| Receipt | Pin | Result |
| --- | --- | --- |
| Workspace `--all-targets` | `workspace.stdout` **12883** / `000270ff…604d` | **122** passed (sum of `test result: ok` counts) |
| Clippy | `clippy.stderr` **538** / `c7177b7b…716a` | `Finished` dev, no diagnostics |
| Identity source-policy | `identity-policy.stdout` **269** / `73868a67…8db3` | **110** source files verified, passed |
| Expanded host fixture | `expanded-host-check.json` **256** / `b9b79de3…bbf2`; pin **154** / `4638140a…e976` | **526** durable cases, exit 0 |
| Corpus overlay | `corpus-result.json` **936** / `2aea56e7…9a6c` | 526 rows, 0 class mismatches |

**42** compound missing+corrupt-store controls: `compound-result.json` **287** / `56946b11…2a8f`, 42/42, 0 class mismatches (28 unavailable / 14 invalid). Scope: two simultaneous faults, class ordering, not replay. User: these remain **underway** to probe **owner prefetch ordering**. Class alignment is not a closed prefetch/first-fault claim.

## Verdict

**NOT ACCEPTANCE. Not frozen source acceptance.** Immutable seven-file snapshot still has two required corrections: body dispatch on `bodyIdentityJoin` (`full_walk.rs` **149–151** in the snapshot), nestedIdentities on `join['domainSet']` (`native_retention.rs` **325–340** in the snapshot). Trial product later adopted both (`inspect_relation_prefix` → `bool` at trial `closure.rs` **329–376**; `body_required` at trial `full_walk.rs` **202–216**; `child_set` match at trial `native_retention.rs` **328–346**). Those trial bytes are not this snapshot.

`public-with-owner-deferred-ok` withdrawn: `pub(crate)` is crate-wrong; advisory31 already allowed public diagnostic `StructuralChecks`; no Run/replay authority path. Walk-order successor question is advisory33, not this unit. Projection limitation: compare Rust on the canonical map domain only. Root continues independently.
