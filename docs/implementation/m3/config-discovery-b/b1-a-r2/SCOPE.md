# B1-a: the configuration resolver (M3-B r4 unit B1-a)

**Product unit, r2; for Codex review (ACCEPT-UNIT).** r2 answers Codex round 1 (`codex-b1a-r1`): RF-01 (step 7 checks the compiled defaults themselves) and RF-02 (pin/hold conflict attribution across layers). This implements accepted plan r2 (`config-discovery-b/b1-a/PLAN-r2.md`, Codex `codex-b1a-plan-r2`) on top of B-S10 (bound at product `08527ebf`).

**What it is.** The pure resolver: M3-B r4 items 1 to 8 and 11, and the X12 r4 order (item 10). It has no I/O, no caller and no CLI route. B1-b captures the carriers and computes the invocation mode.

## What it delivers

| File | What it is |
|---|---|
| `crates/host/src/configuration.rs` | X12's admission is unchanged. Added:<ul><li>the eleven-step pipeline and the typed inputs and outputs (`ResolverInputV1`, `CompiledDefaultsV1`, `FlagLayerV1`, `CapturedCarrierV1`, `InvocationModeV1`, `ResolvedConfigurationV1` with per-leaf provenance);</li><li>the two refusal rows;</li><li>`resolve_analysis_configuration` (resolve, then `admit_policy_selection` once on the resolved pack IDs);</li><li>`configuration_leaf` for the shared flags;</li><li>B-S9's remedy string.</li></ul> |
| `crates/host/src/configuration_classes.json` | The reviewed host-owned mapping (items 2 and 8): every PCS leaf's DRC class and admitting layers. |
| `crates/host/src/configuration_tables.rs` | Generated (item 8). It holds:<ul><li>the one-member profile registry (AQ:56);</li><li>the NCM capability and language-mode enums and the `NOT-SELECTED` cells;</li><li>the seven CINV shared flags with their classes;</li><li>the DRC class and layer enums, and the mapping as `FIELDS`.</li></ul> |
| `tools/host/generate_configuration_tables.py` | Its generator and drift check (`--check`). Its inputs:<ul><li>NCM, CINV and AQ at their v45-pinned bytes;</li><li>the pinned PCS and identity-v3 sources;</li><li>the mapping.</li></ul>It cross-checks the mapping against the PCS leaves and against identity-v3 `semantic-configuration`, and formats its output with the pinned rustfmt 1.9.0. |
| `tools/host/configuration_vectors.py` | Runs PCM at its accepted bytes over 52 fixtures and writes `configuration_vectors.json`. It imports `jsonschema` only from the generator-closure-pinned snapshot, after checking every file. |
| `crates/host/src/configuration_vectors.json` | The PCM byte vectors, each with its digest, semantic record and provenance, or a refusal class. |
| `crates/host/src/configuration_resolver_tests.rs`, `configuration_tests.rs` | The controls. The X12 remedy pin moves from 367 to 706 bytes (B-S9). |
| `tools/tests/test_configuration_tables.py` | The generator's drift and mutation controls. |
| `crates/host/src/lib.rs` | The module comment only. |
| `tools/operability/exceptions.json` | One audited mint-audit census row: `crates/host/src/configuration.rs`, `from`, call, 6. The six are five `BTreeMap::from` and one `i128::from`, none a mint. The record's own standing is a conservative lexical census, not mint authority. |

## The pipeline (item 4)

Steps 1 to 3 run for every layer, in precedence order, before any merge:
- **The order.** Compiled defaults, user-global, project, local and flags. Local runs only when `mode.interactive`; in CI it is never parsed. The environment is a typed constant: empty.
- **1, lexical.** `opensip_identity::parse_json`.
- **2, schema.** PCS through `RegisteredSchemas`. A `schemaVersion: 1` global, project or local file goes through the exact preview carrier's `$defs/<layer>`, is projected in memory to version 2 and re-admitted (item 11).
- **3, allowlist.** The mapping's per-layer allowlist.
- **Internal layers (RF-02).** The defaults and flags documents are encoded and run through the same steps.

The remaining steps run once, after every layer is admitted:
- **4, merge** by leaf: a higher layer replaces the whole value.
- **5, logical paths,** as PCM:23-27. `.` is the root sentinel only for `workspaceRoots` and `ignorePaths`.
- **6, registries:**
  - the profile;
  - capabilities, by NCM membership plus at least one selectable mode;
  - waivers: the registry is empty at M3;
  - component duplicates;
  - pin/hold duplicates and conflicts.
- **7, defaults completeness.** (r2, RF-01) The compiled defaults themselves must carry capabilities and budget; no higher layer can repair a missing compiled value (AQ:132-137).
- **8, partition** by `FIELDS`.
- **9, normalize** to canonical sets; `allowedScopes` keeps its order.
- **10, semantic shape:** identity-v3 `semantic-configuration`.
- **11, digest:** `resolvedConfigDigest`, the raw SHA-256 of the canonical semantic bytes.

## The refusal rows

The layer's kind chooses the row, not the step:
- **External carriers:** `CONFIG.INVALID` (request-rejected, exit 2, with B-S9's remedy).
- **The defaults and flags layers, incomplete defaults, and an invalid resolved record:** the host-invariant row, shaped as X12 row 4.

No new code.

## Lead decisions within the plan

Each was made under the owner's standing direction to decide on the lead's recommendation.

**LD-B1A-1, `NOT-SELECTED`.**
- A `NOT-SELECTED` cell is judged per (capability, mode) when the analysis spec is built (NE:1005-1013 and NE:3577). There it is `REQUEST.UNSATISFIABLE` / `PROVIDER.NOT_SELECTED`, whichever boundary the request came from.
- The resolver knows no mode. It therefore admits a configured capability that is an NCM member with at least one selectable mode. Today all eleven qualify.
- It exports `NOT_SELECTED_CELLS` for spec construction.
- **Rejected:** refusing `clones-cross-tsjs` in configuration. It is selectable for every TS and JS mode.

**LD-B1A-2, pins and holds.** Following `compatibility-selection-model.v3.py:180-191`, a stable ID may appear once across `pins` and `holds`:
- a second appearance at the same version is DUPLICATE-PIN-HOLD;
- at another version it is PIN-HOLD-CONFLICT.

(r2, RF-02) Pins and holds can win from different layers, so the refusal is attributed this way:
- when an external layer's occurrence is involved, the subject names it (the second appearance, when both occurrences are external), and the row is `CONFIG.INVALID`;
- when both occurrences come from host-built layers, the conflict is the host invariant.

`request` stable IDs must be unique (one leaf, one layer). Dangling pins and holds need the component index, which belongs to the deterministic component resolver, not B1-a.

**LD-B1A-3, the per-layer allowlist.** It is part of the reviewed mapping, because item 8 forbids hand-maintained lists. The defaults layer admits only what item 2's table names for it:
- `analysis.profileId`, `capabilities` and `budget`;
- the component defaults;
- the default policy selection.

It admits no operational or discovery leaf.

**LD-B1A-4, subjects.**
- **External or internal layer:** `layer:<name>:<JSON pointer>`. The pointer is empty for a whole-document lexical or schema refusal, because the schema engine reports no pointer.
- **Profile:** `profile:missing` and `profile:<id>`, per plan r2 section 4.
- **Host faults:** `registry`, `resolved:semantic-configuration`, and `class:<leaf>` for an unclassified leaf.

**LD-B1A-5, the defaults layer is typed.**
- An unknown key cannot be expressed through it. The unknown-key control therefore runs the internal admission directly.
- An unregistered defaults profile is the host invariant (the layer's kind). A missing profile after the merge is `profile:missing` (plan r2 section 4).

**LD-B1A-6, the vectors re-express `check-product-configuration.py`'s cases under item 2's allowlist.**
- **What moved.** The check's defaults carry discovery, evidence, waivers, retention and UI, so those move to a project layer. Its flags-layer UI and budget cases move to the global layer.
- **What holds.** Every property the check tests still holds: CI non-consumption, operational exclusion, set order, the always-present sections, the required analysis fields, explicit overrides and the root sentinel.
- **Schema-one vectors.** These give PCM the version-2 projection, since PCM reads version 2 only.

**LD-B1A-7, outside B1-a.**
- Evidence `importIds` are checked against the admitted context only with the store, and an absent selected path is refused only through I/O. Both belong to B2 or the import unit; B1-a applies the schema pattern only.
- The environment structural check (item 9) is B1-b's.

## Not claimed

- No caller, CLI route, carrier capture, discovery or environment check.
- No S-OP-5 field, and no release-registry content or authentication.
- No inventory successor yet: v188 follows the accepted code.
- No product qualification.
