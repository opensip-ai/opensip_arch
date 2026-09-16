# Independent Grok advisory: current reference fixture composition for M2 A04

**Reviewer:** Grok (explicitly authorized). Root remains lead. Not Claude agreement.
**Kind:** Bounded reference-composition review for next retained-graph tests. **Not acceptance.** Not M2 complete. Not A05 replay. Not compiler or native qualification. Not Rust replay.
**Work tree:** `/tmp/opensip-implementation/m2-grok-current-fixture-composition-01/review` only. Live product, frozen unit, architecture history, and commits were not edited.

## Standing

Admission-runtime-selection-v1 is the live last contract successor (9 inventory / 13 contract). Frozen unit bytes are unchanged. Current producer admission hashes **exact full schema document bytes**. An old `$id` or major never authorizes new bytes. Historical `foundation/evaluator_graph_fixture.v3.py` may mint synthetic retained objects, but it reads **sibling files**. Those siblings in the architecture foundation/native/workflows trees are **not** the selected current documents for identity3 / native2 / policy2.

M2 A04 needs an exact **test-oracle / current-fixture binding**, not a new semantic law and not a rewrite of frozen producer files.

## Live lock (independent recount)

Live `design-lock.json` SHA `1af18e9a231ae115963d26732adffc927f91cf87c139848031dc4597f366982a` / 34330.

| List | Count | Last record |
| --- | --- | --- |
| inventorySuccessors | **9** | inventory v11 `0ae9d439…1f62` / 127200 |
| contractSuccessors | **13** | `docs/implementation/m2/admission-runtime-selection-v1/successor.json` `0a3c2694…1251` / 18049 |

Last contract subject `239574c8…f64a` / 17287. Independent Grok review `64238d1f…6bb6`. Root assent unit `92b5921d…3a7d`. Generation source-map remains **40**. Admission source-map is **48**. Current-dispatch names **14** current composition sources.

## Current source authority (bytes, not URI)

Selected source-selection-v2/v3 `source-map.json` + live `schemas/source-map.json` + live `schemas/admission-source-map.json` + `current-dispatch.json` agree on these **current producer** documents. Live product files equal the architectureSource SHAs.

| Logical document | `$id` (same historical and current) | Current authority | Historical sibling (must not be current) |
| --- | --- | --- | --- |
| `foundation/identity-schemas.v3.json` | `urn:opensip:product-v1:identity:v3` | live/source-selection `identity-v3` **197480 / `311c1feb…b68f`** | foundation **196987 / `a76c9e2f…db21`** |
| `native/native-evidence.schemas.v2.json` | `urn:opensip:product-v1:native:evidence-schemas:v2` | live/source-selection `native-v2` **280357 / `e5834d37…7773`** | native **277967 / `2d37b810…6043`** |
| `workflows/schemas/policy-document.v2.schema.json` | `urn:opensip:product-v1:policy-document:2` | live/source-selection `policy-v2` **26534 / `b221b5ed…9b55`** | workflows **27863 / `c8b0a907…3595`** |
| `foundation/framework-recognition-plan.schema.v1.json` | `opensip.product.framework-recognition-plan.1` | already in the 40: **10188 / `49aacd86…f822`** | **absent** from historical foundation |
| `foundation/relation-payload-schemas.v2.json` | `opensip.product.relation-payload.2` | **57623 / `53380a24…be9a`** | **same bytes** (no overlay) |

Handshake `9090e2ad…5f84` and fact-batch `b0ebc133…24e0` are also identical historical and current.

`payloadSchemaDigest` is SHA-256 of the **exact full file** named by the identity payload-registry row (or, for policyDigest/ruleProgram, the digest-domain canonical-record document). Current producer admission must not treat historical digests as current because `$id` matches.

## Required current files versus mere historical producer

Do **not** rewrite frozen `evaluator_graph_fixture.v3.py`. Overlay the documents it hashes.

### Required current overlays (exact selected bytes)

| Overlay path in private archroot | Source of bytes | SHA / bytes | Why required |
| --- | --- | --- | --- |
| `foundation/identity-schemas.v3.json` | selected identity3 | `311c1feb…` / 197480 | identity-model.v3 loads this document; candidate/shape/$defs |
| `native/native-evidence.schemas.v2.json` | selected native2 | `e5834d37…` / 280357 | fixture `blob((HERE.parent/'native/native-evidence.schemas.v2.json').read_bytes())`; native `schema_document_digest` |
| `workflows/schemas/policy-document.v2.schema.json` | selected policy2 | `b221b5ed…` / 26534 | identity digest-domain `policy` / `rule-program` foreign canonical-record; current-dispatch |
| `foundation/framework-recognition-plan.schema.v1.json` | selected recognition (already in 40) | `49aacd86…` / 10188 | proposed identity local registry; payload-registry document; historical foundation file does not exist |
| `foundation/canonical.py` | **accepted** exact-schema-profile-selection-v1 `reference/canonical.py` | `ad88e58f…` / 8995 | selected ExactValidator evolve/dialect law. Historical foundation canonical `d47f25db…` / 6465 is **not** the accepted oracle |
| `foundation/identity-model.v3.py` | source-selection-v2 `reference/models/identity_model.proposed.v3.py` | `5ba92896…` / 157728 | selected identity owner. Historical foundation model `a6dc5f99…` / 157684 differs by **one line**: local registry omits `framework-recognition-plan.schema.v1.json` |

Exact-profile successor is live-selected (`fe1ebd49…1940`). Admission-runtime README already names that canonical as the selected Python oracle composed with current identity schema bytes.

### Mere historical producer (byte-identical; do not rewrite)

These files mint and admit the synthetic graph **from sibling bytes**. Overlaying current siblings makes their hashes current. Repinning them would be a new semantic unit.

| File | Overlay SHA equals historical | Role |
| --- | --- | --- |
| `foundation/evaluator_graph_fixture.v3.py` | `36884a45…5f4e` / 40796 | input producer: `build_file_inputs` + `seal_fixture` |
| `foundation/evaluator_composition_model.v3.py` | `cceeb42b…cbda` / 16980 | compose findings/proof from admitted inputs |
| `native/native_evidence_model.v2.py` | `7d1c0acf…b8be` / 319376 | `admit_coverage_result_v3`; hashes `native/native-evidence.schemas.v2.json` |
| `workflows/workflows_model.v3.py` | `60f28dc9…6123` / 22494 | import/policy owner admission loaded by identity |
| `foundation/identity-model.py` (v1) | `12c9cc22…acb6` / 135671 | still imported by native for `IM.identifier` / `RELATIONS`; not the v3 walker |
| `foundation/relation-payload-schemas.v2.json` | `53380a24…be9a` / 57623 | already current |

`native_evidence_model.v2.py` binds `REPO = HERE.parents[3]` and `CORRECTIONS_DIR = HERE.parent`. The private overlay must therefore be an **archroot** (`review/archroot/docs/coop/design-corrections/...`) so `parents[3]` is the private root, not `/tmp/opensip-implementation`. Wire/attribution helpers also read `docs/coop/artifacts`. Copying those artifacts into the private archroot is part of making the owner stack importable; it is not a current-schema overlay.

### Feature / integration owners (A04 binding only)

Source-selection-v2 README: `reference/models/` and `reference/integration/` are **reference specifications**, not product modules. Current-dispatch is the 14-source current producer set.

For this A04 fixture:

- Identity owner: `identity_model.proposed.v3.py` placed as `foundation/identity-model.v3.py`. `open_run_closure` is the retained-join / annotation walker. It does **not** mint `ReplayedRun`.
- Native owner: historical `native_evidence_model.v2.py` against **current** native document bytes.
- Policy owner: current policy-v2 document at the workflows v2 path; identity walks `policyDigest` as that document’s `PolicyDocumentV2`.
- New-Plan / recognition (`reference/integration/new_plan_admission.py`, `new-plan-contract.md`): required for **new compiler-analysis Plans**, not for this default syntax-only file fixture. Still overlay recognition bytes so the selected local registry is complete.
- Report/query/fit/timing/catalogue models: not required to mint this retained graph. Do not silently import them as authority.

## Private overlay recipe (reproducible; private tree only)

Python: `/tmp/opensip-implementation/metadata-reference-env/bin/python -I -B` (CPython 3.14.6, jsonschema 4.25.1). No network. No live writes.

1. Create `review/archroot/docs/coop/design-corrections/{foundation,native,workflows}` from architecture `docs/coop/design-corrections/` copies.
2. Copy architecture `docs/coop/artifacts/` to `review/archroot/docs/coop/artifacts/` so `HERE.parents[3]/docs/coop/artifacts` resolves.
3. Replace four schema files with **live selected** bytes (equal to source-selection-v2 `schemas/sources/`):
   - `foundation/identity-schemas.v3.json`
   - `native/native-evidence.schemas.v2.json`
   - `workflows/schemas/policy-document.v2.schema.json`
   - `foundation/framework-recognition-plan.schema.v1.json` (new file at that historical path)
4. Replace `foundation/canonical.py` with exact-schema-profile-selection-v1 `reference/canonical.py`.
5. Replace `foundation/identity-model.v3.py` with `identity_model.proposed.v3.py`.
6. Leave `evaluator_graph_fixture.v3.py` and the other producer files untouched.
7. Import the overlay fixture module by file path. Call `build_file_inputs()`, `seal_fixture(graph)`, then `identity-model.v3.open_run_closure(run, objects, blobs)`.
8. Assert:
   - fact `payloadSchemaDigest` == current relation `53380a24…be9a`
   - coverage `payloadSchemaDigest` == current native `e5834d37…7773`
   - coverage digest is **not** historical native `2d37b810…6043`
   - `open_run_closure` returns a `run3:` candidate identity
   - native `admit_coverage_result_v3(..., historical_native_digest)` refuses

Independent pin check in this tree: overlay identity/native/policy/recognition equal live and equal source-selection; overlay canonical equals accepted exact-profile; overlay identity-model equals proposed; overlay fixture equals historical producer.

## Actual checks

Probe `review/probes/verify_pins.py` SHA `e262243a…4f29`. Result `review/results/verify_pins.json`. Earlier compose probe `review/probes/compose.py` SHA `715a5137…7570` / `review/results/composition.json`.

### 1. Historical digest is not current (counterexample)

Same `$id`, different bytes:

- Historical native document SHA `2d37b810bd9ffed741d74241fc8a11051606862d8af2f152eed16b92bdc66043`
- Current native document SHA `e5834d37aebd96d77d352975878da349033f8633ecbd83322ad0fbea461f7773`

On the **current** overlay, native owner `admit_coverage_result_v3` with the current digest: **ADMIT**. With the historical digest as a caller-chosen `payloadSchemaDigest`: **REFUSE** `native.coverage-payload-schema-not-registered`.

Identity `registered_schema_documents()` (closed payload-registry document set, 9 SHAs) **includes** current native `e583…` and current relation `53380a24…` and **excludes** historical native `2d37…`. Policy-v2 is **not** one of those 9 payload-registry document hashes; it is a digest-domain foreign canonical-record (`policy` / `rule-program`). Overlaying it is still required because `open_run_closure` admits `plan.policyDigest` through `workflows/schemas/policy-document.v2.schema.json`.

A current-producer test that expected coverage `payloadSchemaDigest == 2d37b810…` would be asserting historical SourceBytes as current. That is the forbidden substitution.

### 2. Synthetic current graph / Run via actual reference owners

Default `build_file_inputs()` + `seal_fixture()` on the overlay:

| Field | Value |
| --- | --- |
| objects / blobs (pre-seal) | 16 / 45 |
| facts / coverage | 3 / 2 |
| first fact `payloadSchemaDigest` | `53380a24…be9a` (current relation) |
| first coverage `payloadSchemaDigest` | `e5834d37…7773` (current native) |
| sealed objects | 28 |
| planId | `plan2:99218421…1d49` |
| snapshotId | `snapshot2:89800af4…4784` |
| evidenceId | `evidence3:ae347cf9…0c9f` |
| evaluationSealId | `seal3:34a73fb5…72c9` |
| compose `proof.verdict` | `fail` (synthetic composition result; **not** evaluator correctness and **not** a composition failure) |

Native `admit_coverage_result_v3` ran inside the fixture producer against the current native document.

Identity **`open_run_closure`** (A04 retained-join / annotation walker) succeeded:

- `runId` = `run3:697e7fb028de4a95e807c7de6af264a8db158ef8b4e4f7fc7254cc7752cf244d`
- Owner resolvers present: `get`, `visit`, `blob`, `payload`, `foreign_payload`, `registered_payload`, `registry_row`, `nativeContexts`, `nativeUniverses`, plan/snapshot/grant/analysisSpec/execution
- This is a **candidate run identity** from admitted retained structure. It is **not** `ReplayedRun`. `close_run` / complete semantic replay was **not** executed (M2 A05).

### 3. What would block if the overlay were omitted

If tests imported architecture `foundation/evaluator_graph_fixture.v3.py` in place:

- Coverage `payloadSchemaDigest` would be historical native `2d37b810…`
- Identity schema would be historical `a76c9e2f…`
- Policy foreign records would validate against historical policy-v2 `c8b0a907…`
- Recognition would be missing from the local ExactValidator registry
- Canonical would be historical `d47f25db…` (pre exact-profile evolve law)

Current admission-runtime aliases refuse those historical native/policy documents as current sources. Silent fallback to historical sibling files is the wrong oracle.

## Proposed owner fix (advisory)

For M2 A04 retained-graph tests, bind the **current** documents above. Do not edit frozen foundation/native/workflows files. Do not freeze historical payloadSchemaDigests as expected current values.

Concrete options (owner chooses one; this review does not install either):

1. **Private/test overlay** matching this recipe: current schema bytes + accepted exact-profile canonical + proposed identity-model.v3, historical fixture remaining the producer.
2. **Explicit pin table in the A04 test** naming current SHAs (`311c…`, `e583…`, `b221…`, `49aa…`, `53380a24…`, canonical `ad88…`, proposed model `5ba9…`) and loading those files by path, never by `$id`.

Negative oracle: a coverage or payload whose `payloadSchemaDigest` is historical native `2d37b810…` or historical policy `c8b0a907…` must refuse as current (`native.coverage-payload-schema-not-registered` / `PAYLOAD_SCHEMA_NOT_THE_REGISTERED_DOCUMENT` / admission `SourceBytes`). URI agreement is not enough.

Do **not** repin unaccepted semantic model changes. The only identity-model delta used here is the already-selected proposed v3 local-registry recognition filename. Exact-profile canonical is already an accepted live successor.

## Limits (not waived)

- Advisory. Not acceptance of A04, A05, M2, or release.
- No compiler execution, no native toolchain qualification, no claim that Rust identity/replay reproduced this graph.
- `close_run` / evaluator complete replay was not run. `open_run_closure` is the A04 primitive.
- Compose verdict `fail` is the synthetic proof output of the default file fixture; it is not a pass/fail on this composition review.
- Native still loads historical `identity-model.py` v1 for some identifier/relation helpers. That did not block this graph. It is not a license to treat v1 as the current identity walker.
- Report/query/fit/catalogue integration models were not exercised.
- New-Plan recognition duty was not exercised (syntax-only default fixture).
- Root is independently working a pure annotation walker. This private overlay is test-oracle composition evidence for that walker, not a product materialization.
- Generation registry stays 40. Admission closure stays 48. This review does not change either map.

## Conclusion

Exact current source authority for the next retained-graph tests is the **selected source-selection-v2/v3 and admission-runtime documents**, installed live after 9/13. Historical evaluator fixture Python is a valid **producer** only when its sibling identity/native/policy/recognition files are those current bytes and the identity/canonical models are the selected proposed + accepted exact-profile pair.

This private overlay demonstrates one synthetic current graph and `run3:` candidate through actual native coverage admission and identity `open_run_closure`. Historical native digest `2d37b810…` is a concrete current-producer refusal, not an alias.

**Verdict: NOT ACCEPTANCE.** Fixture-binding recipe is reproducible and sufficient for M2 A04 oracle work. Remaining native-owner, complete replay, storage, report, and M6 obligations stay open.
