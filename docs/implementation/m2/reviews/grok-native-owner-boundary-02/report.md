# Advisory: native owner integration into retained graph (boundary 02)

**Reviewer:** Grok. Root remains lead. Not Claude agreement. **Not acceptance. Not Rust07 selection. Not ReplayedRun.**
**Work tree:** `/tmp/opensip-implementation/m2-grok-native-owner-boundary-02/review`. Live, frozen, and private07 product were not edited. No giant corpora.

## Standing

Live lock is **9 inventory / 15 contract** after capability-totality reference selection (receipt `m2/trials/capability-reference-selection-01/receipt.json`; unit `ACCEPTED-DESIGN-UNIT` `f9c3c13a…cfbb`). Runtime sources still unchanged (202). Selected native model is `m2/capability-totality-reference-selection-v1/reference/native_evidence_model.py` `e6784aa1…e2b9`. Selected identity `619d6e3c…41e6`, canonical `ad88e58f…96f7`. Overlay obligation from the unit: later compositions must load **this** native file with current schemas, not historical `native_evidence_model.v2.py` by filename.

`ACTIVE-WORK.md` still describes older 9/14 / graph07-codec text; the receipt and live `design-lock.json` last contract row are the lock authority. Work-map **M2-A04** remaining is the owner of this boundary: native contexts/universes, Plan/snapshot/evidence references; schema/identity closure must never mint ReplayedRun. **M2-A05** is complete replay (`evaluator/src/replay.rs` — **absent in private07**).

Private07 `/tmp/opensip-implementation/m2-retained-graph-trial-07` is an **unselected** prototype: identity has CVE1 codec + relations diagnostics; evaluator has capability ADMIT only. Do not treat it as live.

## Crate DAG (accepted, do not invert)

| Crate | May depend on | Must not depend on |
| --- | --- | --- |
| identity | contracts + reviewed pure registry crates | evaluator, host, platform IO |
| evaluator | identity (+ contracts if needed) | host, storage |
| host | identity, evaluator, platform | — |

Python `identity_model.py` is a **monolith file**, not the crate boundary. It lazily imports native (`native_admission`) and replay (`close_run` → `evaluator_replay_model.v3.replay`). Porting that file wholesale into `crates/identity` would create identity→evaluator/native edges the inventory forbids.

**Composition that matches the DAG:** evaluator (or host fact-admission) **orchestrates**; identity supplies `RetainedInputs`, frames, hashes, CVE1, relation payload/source diagnostics. Native ADMIT functions live beside capability ADMIT in evaluator (or a later native-pure module that evaluator depends on), never as identity→evaluator callbacks that identity *calls by crate name*.

A `trait` on identity implemented by evaluator is optional inversion. It is **not** required for the next slice: evaluator can call identity primitives. Python’s lazy `native_admission()` is the cycle-break for the **reference file**, not a mandate to genericize `open_run_closure` in identity.

Deferred obligations already exist in identity as `GraphError::Unsupported(...)`. Keep those until the **owner crate** can discharge them. Do not relabel Unsupported as ADMIT.

## `open_run_closure` vs `close_run`

| | `open_run_closure` (`identity_model.py:909`) | `close_run` (`identity_model.py:866`) |
| --- | --- | --- |
| Authority | Retained identity/schema/**native owner joins**. Returns resolvers. **Not** semantic output authority. | Public evaluator3 admission: calls complete replay, then runId. |
| Rust owner | Split: identity structural walk (`closure.rs`) + evaluator native/capability/import owners | `crates/evaluator/src/replay.rs` (**missing in private07**) |
| Failures | `EvidenceUnavailable` (missing promised bytes); `AdmissionError` (joins) | Replay `UNAVAILABLE`→`EvidenceUnavailable`; `MISMATCHES`→`CompleteReplayMismatch`; owner `REFUSALS`→`AdmissionError` |
| Token | Must **not** mint `ReplayedRun` | Opaque `ReplayedRun` only after successful complete boundary (A05) |

Cache/regeneration admission must pass **`close_run`**, not `open_run_closure` alone.

## What private07 already has (unwired)

Identity (`crates/identity`):

- `capability_codec.rs` / `decode_cve1`+`encode_cve1` — encoding only
- `relations.rs` + `RetainedInputs::inspect_relation_payload` / `inspect_relation_sources` — ladder/NFC/snapshot inventory; **body identity `Unsupported`**
- `FramedCandidate` / `NativeFrameSet::{Context,SemanticUniverse,Nested}` — **shape + H only**, comment at `closure.rs:1142` forbids native ADMIT
- digest walk: `capability-manifest-id` → `Unsupported("capability derivation")` (`closure.rs:710`)
- H-frame without explicit domain → `Unsupported("registered H-frame domain set")` (`closure.rs:746`)
- recognition derived H already inlined (J-FRP-ID)

Evaluator (`crates/evaluator`):

- `capabilities.rs::admit_capability_manifest` — closed current CAP-MANIFEST-ID-V1 gates, opaque `CapabilityManifest` (`compile_fail` forge)
- **no** `replay.rs`, **no** `admit_native_context`, **no** universe binding

Identity Cargo: `unicode-normalization =0.1.24` default-features false (unselected live). Evaluator Cargo: identity only.

## Callgraph (selected reference)

`open_run_closure` walk → `admit_frame(digest, domain_set)`:

1. `parse_h_frame` + snapshot joins + blobJoins + nestedRecords + nestedIdentities (identity structural; frames03/records04 already cover shape/H/nested records **without** native ADMIT)
2. If `native-context`: closure-kind joins, then **`N.admit_native_context(language, value, closure_trees)`** (`identity_model.py:1635`). Refusals → `NATIVE_CONTEXT_ADMISSION`. Identity mismatch → `NATIVE_CONTEXT_ADMITTED_IDENTITY`
3. If `native-semantic-universe`: stash row; **binding later**

After walk (`:1689+`):

4. `NATIVE_CONTEXT_SET_JOIN` vs `plan.nativeContextDigests`
5. `CAPABILITY_JOIN` / `CAPABILITY_BYTES_JOIN` (identity hash of `opensip.capability-manifest.v1\0`+bytes)
6. **`N.admit_capability_manifest(cap_bytes)`** (`:1662`) — now the **selected** totality function
7. `N.admit_requested_capabilities` on analysis-spec
8. Per universe: language in requested modes; `contextField` sha256-text ∈ selected contexts; **`row['binding']['entryPoint']`** ∈ `{bind_typescript_universe, bind_syntax_universe, bind_rust_universe}`
9. Relation facts: `relation_payload_rules` (already in identity diagnostics) then `syntax_capability_supported` then `relation_source_joins` (snapshot done; **`body_identity_join` needs universe+context**)
10. Imports: `workflow_admission().validate_import_record` / `admit_source_mapping` (`:1949`), **not** native

`native_admission()` still **loads `HERE.parent/'native/native_evidence_model.v2.py'`** (`identity_model.py:41`). That filename is historical. Overlay **must** bind `e6784aa1…` or tests will silently run pre-totality ADMIT. This is the highest-priority trap for any new native-owner oracle.

## Minimum coherent NEXT slice

**Do not** start with universe binding, clones `bodyIdentityJoin`, import VCS, or `close_run`. Those require admitted contexts and/or replay.rs.

**Next slice: Plan capability-manifest join (evaluator orchestrates, identity stays structural).**

Private07 already has both halves unwired. Connecting them is the smallest A04 increment that uses the **now-selected** native totality law.

### API (evaluator, not identity)

```text
admit_plan_capability(
  inputs: &RetainedInputs,          // identity
  plan_id: &str,                    // plan2:…
  budget: TraversalBudget,
) -> Result<CapabilityManifest, PlanCapabilityError>
```

**Inputs (exact):**

- `plan` object via `inputs.object(plan_id, IdentityDomain::Plan, …)`
- `plan.capabilityManifestId` (64 hex)
- `plan.capabilityManifestBytesDigest` (blob key)
- retained blob bytes (re-hashed by `RetainedBlob`)

**Identity primitives used:** `RetainedInputs::object`, `blob`, `raw_sha256`, `decode_cve1` only inside existing `admit_capability_manifest`.

**Evaluator authority:** `admit_capability_manifest(raw)` → opaque `CapabilityManifest`. Compare `hex(identity())` to `plan.capabilityManifestId`. Do **not** sort, NFKC, infer platforms, or join ProfileEntry.

**Return:** opaque `CapabilityManifest` (already non-constructible). This is **not** a Run, not platform support, not release custody.

**Failure categories (keep distinct):**

| Category | When | Code / cause |
| --- | --- | --- |
| Unavailable | blob/object missing | identity `MissingBlob` / `MissingObject` → operational, not a false predicate |
| Identity | blob SHA or plan identifier mismatch | `ObjectIdentity` / `BlobDigest` / `CAPABILITY_BYTES_JOIN` |
| Encoding | CVE1 refuse | `capability.cve1-decode:*` |
| Closed/type/domain/order | totality gates | existing `capability.adm-*` |
| Manifest identity | ADMIT but id ≠ plan field | `CAPABILITY_MANIFEST_IDENTITY` |
| Join | run.capabilityManifestId ≠ plan (later, when run is in the fixture) | `CAPABILITY_JOIN` |

Do **not** implement `FOREIGN_CAPABILITY_MANIFEST` until the walker records `capability_ids` from digest fields (still `Unsupported("capability derivation")` in identity). Next slice is Plan bytes+id only.

**Context-per-reference:** one Plan, one bytes blob. Still re-run ADMIT on every Plan that names those bytes (decode may memoize; admission must not — same law as `relation_source_joins`).

### Compact fixtures (positive / negative)

Reuse private07 `crates/evaluator/tests/fixtures/capability-manifest.golden.cve1` (DCM-1-core; id `508f24c7…8881b`).

| Recipe | Expect |
| --- | --- |
| Plan + golden bytes + matching id | `Ok(CapabilityManifest)` |
| Golden bytes, id flipped one hex | `CAPABILITY_MANIFEST_IDENTITY` |
| Bytes digest blob missing | Unavailable |
| Non-map CVE1 root (`0x00`) | `adm-closed:CapabilityManifestV1` (totality) |
| Mixed `platformIds` `[all-supported, false]` | `adm-type:…platformIds[]`, **no** panic |
| All-string duplicate platformIds | `adm-order:platformIds` |
| `schemaVersion=2` / `language=cobol` | still ADMIT at this gate (OPEN); **no** new enums |
| `profile=not-core` | ADMIT here; **do not** check ProfileEntry (custody separate) |
| Forge `CapabilityManifest { .. }` | compile_fail (already) |

Keep fixtures **Plan+blob**, not a 28-object Run.

## Sequence after that (do not merge into the next slice)

1. **Native-context structural (identity)** using `FramedCandidate` + existing nested-record/blob joins + `admit_closure_field_kinds` for context `closureJoins`. Still no ADMIT. Failure: `NATIVE_CONTEXT_CLOSURE_KIND`, blob length, `UnregisteredFrameDomain`.
2. **`admit_native_context` in evaluator** (`native_evidence_model.py:2311`): language, descriptor, `closure_trees: BTreeMap<closure2:id, closure record>`. Recompute `identifier("closure", record)` via identity; kind match; TS lib/stdlib inventory. Per-context, every Plan reference (no skip because another context already admitted). Returns refusals list; identity/evaluator maps to `NATIVE_CONTEXT_ADMISSION`.
3. **Universe set + binding (evaluator):** `NATIVE_CONTEXT_SET_JOIN`; `contextForm==sha256-text` and digest ∈ plan set; `bind_*_universe` entryPoint from the **retained frame row**, never a caller-chosen language function. Needs admitted context + snapshot inventory. `UNIVERSE_LANGUAGE_NOT_REQUESTED` uses analysis-spec modes **after** `admit_requested_capabilities`.
4. **Relation remaining owners (evaluator, after 2–3):** `syntax_capability_supported`; `body_identity_join` (today identity `Unsupported("relation body identity owner")`); admitted-target is **not** in `relation_payload_rules` — do not pretend inspect_relation_payload covers it.
5. **Import owner (evaluator + workflow, not native):** `IMPORT_JOIN`, `read-import` grant, `validate_import_record`. Identity already has import closure roles (`closure.rs:155`).
6. **`close_run` / `replay.rs` (A05):** only after open-path owners exist. Never mint ReplayedRun from `StructuralChecks`.

## Traps (concrete)

1. **Filename overlay:** `identity_model.py:41` still names `native_evidence_model.v2.py`. Oracles that `import` via HERE will miss totality (`e6784aa1`). Explicit overlay, same as recognition 619d.
2. **Python monolith ≠ crate:** `open_run_closure` calling `N.admit_*` must become **evaluator calling identity**, not identity depending on evaluator.
3. **Do not lift `admit_capability_manifest` into identity** to “make the walk compile.” Codec stays identity; gates stay evaluator (already the private07 split).
4. **`GraphError::Unsupported("capability derivation")`:** digest-field `capability-manifest-id` is a **later** join (capability_ids set). Next slice is Plan blob path (`CAPABILITY_BYTES_JOIN`), not that representation.
5. **`body_identity_join` before universes:** will false-fail or skip; keep Unsupported until step 4.
6. **Memoize decode, not admission.** `relation_source_joins` docstring (`identity_model.py:1458`): same payload, second fact/snapshot must re-join. Same for every native context digest in `plan.nativeContextDigests`.
7. **Native AdmissionError class:** Python catches **native’s** `AdmissionError`, not identity’s (`identity_model.py:1708`). Rust should use evaluator error types wrapping identity errors, not `From` that collapses Unavailable into Law.
8. **Platform domain ≠ support.** Manifest `platformIds` membership is ADM-DOMAIN only (capability registry comment in `capabilities.rs:1`).
9. **OPEN fields.** Do not add language/provider/schemaVersion/profile registries. Profile custody is DL-CUST-3, outside this slice.
10. **Boolean vs integer.** Python `type(x) is int` refuses JSON true. Identity `JsonValue` must keep Bool distinct from Integer (canonical already does).
11. **No `replay.rs` yet.** Do not stub `close_run` as `open_run_closure`.
12. **Private07 unicode pin** is not live-selected; do not expand NFC work in this slice.

## What this does not claim

No native ADMIT from `FramedCandidate`. No import completeness. No coverage totality. No compiler/provider. No full Run. No private07 freeze or live install.
