# Advisory: Plan-native owner vs `open_run_closure` native block

**Reviewer:** Grok. Root remains lead. **Not** ACCEPT-DESIGN-UNIT. **Not** fresh-blind (retention-13 archived). Did not edit private-14, live, frozen, or history.

Work tree: `/tmp/opensip-implementation/m2-grok-plan-native-boundary-14`.

## Sources

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| selected `identity_model.py` | 158555 | `619d6e3c…41e6` |
| selected `native_evidence_model.py` | 319944 | `e6784aa1…e2b9` |
| identity-v3 `languageModes` (same `311c1feb…`) | — | map + `preparedModes.rust=rust-cargo-prepared` |

Focus: `admit_frame` universe arm **1640–1641** (store only) vs context arm **1624–1639** (closures + **mandatory** `admit_native_context`); native block **1689–1755**.

## The census API (not a Run)

A diagnostic Plan-native owner should take:

- explicit **observed context digest census** (bare hex, same as `plan.nativeContextDigests`)
- explicit **observed universe digest census**
- Plan-selected context set, requestedCapabilities, grant `analysisOperations`, snapshot inventory/layouts
- retained objects/blobs

It must **not** walk facts, scopes, seals, or `UNIVERSE_FRAME_UNRETAINED`. That is later composition.

**Do not** implement this slice by calling public `inspect_native_retention` on each universe. Retention-13 **always** follows `contextField`, `frame_candidate`s the named context, runs the context owner, then binds. A missing **unselected** context then surfaces as `MissingBlob` / unavailable **before** `UNIVERSE_CONTEXT_NOT_SELECTED`.

## Reference order (keep this)

`admit_frame(universe)` retains nested raw/H/blob joins and **does not** resolve `nativeContextId`. Contexts enter `native_contexts` only when `admit_frame`d as `native-context` (owner + kind-then-visit closures). Then:

1. **`NATIVE_CONTEXT_SET_JOIN`** — `sorted(native_contexts.keys()) == sorted(set(plan.nativeContextDigests))`. Extra or missing selected contexts both use this tag. Plan list is a **set** (duplicates collapse).
2. Foundation: each `languageMode` ∈ identity-v3 map, else `ANALYSIS_SPEC_LANGUAGE_MODE_UNREGISTERED`.
3. **`admit_requested_capabilities`** (native class, re-wrap `ANALYSIS_SPEC_CAPABILITY`). Vocabulary then unique `(capabilityId, languageMode, workspaceRoot)`. Not cardinality.
4. Per universe, in this order:
   - `UNIVERSE_LANGUAGE_NOT_REQUESTED` — `row.language` not in `{map[m] for m in requested}-{None}`
   - if `preparedResolution != "none"`: `PREPARED_RESOLUTION_MODE_NOT_REQUESTED` — `preparedModes[language]` (`rust` → `rust-cargo-prepared`) must be **in requested modes**
   - read `contextField` as `sha256-text`; **`UNIVERSE_CONTEXT_NOT_SELECTED`** if prefix/form wrong **or** id ∉ `{sha256:+d for d in plan.nativeContextDigests}`
   - **then** `native_contexts[bare]`. After a passing SET_JOIN this cannot miss a **selected** digest. Do not fetch the blob to decide “unselected”.
   - `NATIVE_UNIVERSE_CONTEXT_LANGUAGE` if admitted context domain ≠ `row.contextDomain`
   - `contextAgreementFields` (`equal_typed`)
   - actual `N.{bind_syntax,bind_typescript,bind_rust}_universe` with `{universe, admission, context, retained: context|universe retained merged, snapshotInventory}` — missing entryPoint `NATIVE_UNIVERSE_BINDING_UNAVAILABLE`; refusals `NATIVE_UNIVERSE_BINDING:`; identity `NATIVE_UNIVERSE_ADMITTED_IDENTITY` (`sourceUniverse` is **bare** hex)
   - **then** grant: `preparedResolutionGrantOperations[preparedResolution]` if not null must be in `grant.analysisOperations` (`host-prepared`→`prepare-code`, `imported-inert`→`read-import`, `none`→no check)
5. **`snapshot_pruned_tree_faults`** over snapshot inventory and layouts from **selected** TS contexts only (`nodeModulesLayoutDigest` set **and** retained layout present). VCS segment faults first; nested `node_modules` needs its own layout row. First path only is raised.

## Ordering traps

| If you… | You get the wrong first fault |
| --- | --- |
| `inspect_native_retention` / follow `contextField` while retaining a universe | missing unselected context → **unavailable**, not `UNIVERSE_CONTEXT_NOT_SELECTED` |
| Bind universes before SET_JOIN | extra census context never reported as set-join; unselected layouts can leak into pruned-tree |
| Lookup `native_contexts` before the selected-set test | KeyError/missing-context for a digest the Plan never selected |
| Check grant before bind | grant-shaped refusals hide `NATIVE_UNIVERSE_BINDING` |
| Treat `rust-cargo` and `rust-cargo-prepared` as the same requested mode | unprepared rust universe is allowed whenever **language** rust is requested; **prepared** universe additionally needs mode `rust-cargo-prepared` |
| Catch native `AdmissionError` with identity’s class | vocabulary faults silently drop (`ANALYSIS_SPEC_CAPABILITY` comment ~1707–1712) |
| Reuse `syntax_universe_selection` (~1143–1147) as universe retain | it **does** `admit_frame` context immediately — same early-bind trap |
| Mix `sha256:` vs bare hex in census vs plan vs `selected_contexts` | SET_JOIN vs `UNIVERSE_CONTEXT_NOT_SELECTED` swap |

Context owner stays **mandatory** on every census context (`admit_native_context` / `inspect_native_context`). Descriptor-only success is not retention of tree bytes; Plan may reuse retention-13 **context/nested** roots, not the **universe** root.

`native_contexts[d][2]` is the admission object bind must receive — re-running the owner is required; do not synthesize ADMIT.

## Suggested tests (diagnostic API)

1. Universe names context C **not** in plan set; C blob **absent** → `UNIVERSE_CONTEXT_NOT_SELECTED`, not `MissingBlob`.
2. Same, C blob **present** but C **not** in context census → still `UNIVERSE_CONTEXT_NOT_SELECTED` (do not admit C as a side effect of the universe).
3. C in census and store, **not** on plan, census otherwise exact → `NATIVE_CONTEXT_SET_JOIN` **before** universe-context-not-selected.
4. Plan selects C, census omits C → `NATIVE_CONTEXT_SET_JOIN` (missing selected), not per-universe missing.
5. Plan selects C, census includes C, owner refusals → `NATIVE_CONTEXT_ADMISSION` / `Refused`; universe bind must not run.
6. Syntax/TS/Rust census contexts: owner runs; grammar tree bytes missing fails **context retain**, not bind.
7. Prepared rust universe + only `rust-cargo` requested → `PREPARED_RESOLUTION_MODE_NOT_REQUESTED`.
8. `imported-inert` universe, bind ADMIT, grant lacks `read-import` → `PREPARED_RESOLUTION_GRANT_JOIN` **after** bind.
9. TS selected context with layout vs inventory path under VCS segment → `SNAPSHOT_PRUNED_TREE_NOT_A_READ`; layout from an **unselected** TS context must not authorize.
10. Duplicate plan context digests: set equality still passes one admission.
11. Universe `contextForm` not `sha256-text` → `UNIVERSE_CONTEXT_NOT_SELECTED` (same tag as unselected).
12. Bind `sourceUniverse` vs census digest (bare hex).
13. Do **not** require facts; `UNIVERSE_FRAME_UNRETAINED` stays out of this API.

## Limits

Not full `open_run_closure`. Not Plan graph authority. Not retention-13 public universe API. Not 14-file split acceptance. Root implements; this is ordering/boundary advice only.

**Verdict: NOT ACCEPTANCE.**
