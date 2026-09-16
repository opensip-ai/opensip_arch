All work verified. Report follows.

---

# Follow-up delta v2: version-dispatch boundary + portable verifier

**Standing.** Authored follow-up to `claude-discovery-correction.v1`. Not self-acceptance, not readiness, not product qualification. Final independent acceptance still required. v1 is retained byte-for-byte (55/55 manifest files unchanged, manifest sha `86eab347a181…`); candidate25 **12869/12869** and prior inputs **136/136** re-verified unchanged; only `claude-discovery-correction.v2/scratch` was written.

**v2 artifact manifest sha256 `cab93b6ea6ae7745c0956b714d00edea05446b9acca8a7f6071f5116636dd06f`** (54 files). It lists the **cumulative** authored result against frozen candidate25, so root can merge one overlay.

---

## 1. Both root counterexamples reproduced — and they were narrower than the defect

I re-ran root's probe surface against v1 and extended it. `evidence/version-surface-before.json`:

| Probe | v1 behaviour |
|---|---|
| `boundary_inventory_from_provenance(V1)` | **accepted**, emits `schemaVersion: 2` |
| …with version `7`, `True`, `"2"`, `None`, `2.0` | **all accepted**, all emit `2` |
| `discover_units(V1 inventory)` | raw `ValidationError: 'markerCountBasis' is a required property` |
| `require_admitted_boundaries(V1 inventory)` | **accepted**, returns version 1 |
| `assign_membership(V1 inventory)` | **silently accepted** |
| `unit_scope_descriptor(V1 inventory)` | **silently accepted**, produced a `scopeDigest` |

So the converter did not "relabel V1" — it **read no version member at all**. And three consumers were worse than root's CE2: two accepted a stale inventory **silently**, letting stale boundaries reach the scope descriptor and therefore `scopeDigest`/`plan2`/RunId with no signal. `require_admitted_boundaries` — the authoritative-lane gate I introduced in v1 — was itself version-blind.

Two of my initial probe rows (`assign_membership`, `unit_scope_descriptor`) first failed on malformed unit stubs I supplied, not on version handling; I re-probed with well-formed units before drawing the conclusion above rather than report the artifact as a finding.

---

## 2. Does anything need V1 execution? Evidence, then decision

| Question | Evidence | Answer |
|---|---|---|
| Any other producer of a boundary inventory? | `boundary_inventory_from_provenance` is the only one; it emits `BOUNDARY_INVENTORY_VERSION = 2` | No |
| Any fixture carrying a V1 inventory? | all four (`native-cases.v2.json` ×3, `discovery-cases.v1.json` ×1) are `schemaVersion: 2` | No |
| Do standalone/native/foundation callers need it? | `enumeration_model`, `check-identity`, both evaluator fixtures call the three consumers with `boundaries=None` — the standalone lane, not a V1 record | No |
| Does retained replay need it? | `admit_enumeration`'s `membership_derivation` is a keyword-only optional recompute input with an ad-hoc allowed-key set `{markers, files, explicit_workspace_roots, boundaries, mode}`, **present in no schema** and carrying no `schemaVersion`. It is not retained Run evidence; its `boundaries` is produced at recompute time by the current converter | No |

**Selected remedy (smallest lawful change): two explicit lanes.**

- **Read lane, unchanged and still both versions.** `S.validate_discovery_provenance` and `N.validate_boundary_inventory` keep admitting `{1, 2}` by dispatch. Historical bytes stay readable and schema-validatable.
- **Current-operation lane, requires current.** `DD.boundary_inventory_from_provenance` admits only `CURRENT_PROVENANCE_VERSION`; `N.admit_current_boundary_inventory` admits only `CURRENT_BOUNDARY_INVENTORY_VERSION`, and is now what `discover_units`, `assign_membership`, `unit_scope_descriptor` and `require_admitted_boundaries` call.

Old rows are **never upgraded**: no basis and no `observed-inventory` count is invented for rows that carry neither. Three distinguished conditions:

- `PROVENANCE_VERSION_SHAPE` / `native.boundary-inventory-shape` — non-integer version, bool included;
- `…_VERSION_UNKNOWN:<n>` — a version this kit does not define;
- `…_VERSION_UNSUPPORTED:<n>` — a **defined historical** version this current operation will not execute.

That last distinction is the precise boundary root asked for: "readable" and "executable" are now different answers with different labels.

**No new public D9 code.** The converter raises the existing `BoundaryError`, which the existing security wrapper already maps to `Reject('BOUNDARY_INVENTORY:' + detail)` — control V6 asserts the full string `BOUNDARY_INVENTORY:PROVENANCE_VERSION_UNSUPPORTED:1`.

### A labelling defect in my own v1 work

`NativeRefusal` subclassed `ValueError`, so it sat **outside every** `except (NV.AdmissionError, AdmissionError, ValidationError)` site in the kit — notably `enumeration_model.admit_enumeration`, which would have turned a labelled composition refusal into an uncaught exception instead of its `ENUMERATION_ADMISSION_MEMBERSHIP_DERIVATION` fault. It now subclasses the shared `AdmissionError` (`canonical.AdmissionError`). Control V12 asserts the subclass relation. This is the correct label for an admitted-input violation and is what makes the new refusals non-regressing.

`evidence/version-surface-after.json` shows all 23 probe rows at their intended outcome.

---

## 3. A v1 regression I found and fixed — and my v1 validation scope was too narrow

Running `foundation/check-identity.py` (which v1 never ran) gave **1595 passed / 1 failed**: `v20-native-view-fixture-declares-current-registered-schemas`.

Baselined against three trees:

| Tree | Result |
|---|---|
| frozen candidate25 | **1596 / 0** |
| v1 successor | 1595 / **1** |
| v2 before fix | 1595 / 1 |

So **my v1 delta introduced it**, and neither of us caught it because v1's validation scope was security/native/integration only.

Cause: `NATIVE_FIXTURES['coverageView']['schemaDigests']` declared `d8e9a1fcaa98…`, which is exactly the **pre-v1** digest of `native-evidence.schemas.v2.json`. `registered_schema_documents()` keys documents by the raw SHA-256 of their exact bytes, so changing a registered schema document invalidated the fixture's declaration — precisely what that fixture-drift guard exists to catch. Fix: repoint the single declared digest to the current document digest `5b13740dc2b9…` (one line; patch in `patches/`). The guard is not loosened, and the security bundle's digest is declared by no fixture.

**This is the lesson for merge:** any change to a registered schema document requires the fixture-drift guard to be re-run. Root's F04 patch touches native model/schema — it must run `foundation/check-identity.py` too.

---

## 4. Validation scope, and why it is what it is

Changed in v2: `discovery-defaults.py`, `native_evidence_model.v2.py`, `security_lifecycle_model_v1.py`, `native-cases.v2.json`, plus rebound pins.

| Suite | Result | Why run |
|---|---|---|
| security | **464/464 cases, 11/11 sweeps** | consumes all three changed models |
| native | **375/375** | the boundary-inventory consumer |
| integration | **412 passed, 0 failed** | exercises the real security→boundary→native composition |
| foundation identity | **1596 / 0** | the `NativeRefusal` base-class change touches foundation exception handling, and it is the fixture-drift guard |
| controls | **55/55** (29 from v1 + 26 new) | direct coverage of the version surface |

I did not re-run the workflows or other foundation suites: nothing in this delta touches their sources, and the boundary-inventory path does not reach them. If root disagrees, `verify-reconstruction.py --skip-suites` gives a clean tree to run anything against.

### New controls (26), covering all three paths root named

- **Read path:** genuine V1 provenance with no pruned rows (V1) and with legacy rows (V2) stay readable; V1 boundary inventory empty (V7) and with legacy rows (V8) stay readable. Plus **V2b**: a record claiming version 1 while carrying version-2 rows is refused — emptiness or relabelling cannot forge a version.
- **Converter path:** V1 refused whether pruned rows are empty (V3) or present (V4); current V2 still converts (V5); the security wrapper mapping (V6).
- **Current-admission path:** all five entry points (`discover_units`, `assign_membership`, `unit_scope_descriptor`, `require_admitted_boundaries`, `admit_current_boundary_inventory`) refuse a V1 inventory (V9) and an **empty** V1 inventory (V10) with the same label; a V2 inventory is admitted unchanged (V11).
- **Unknown/bool:** V13 runs `7`, `True`, `"2"`, `None`, `2.0` across read-provenance, convert, read-inventory and current-admission — all four refuse each, with UNKNOWN vs SHAPE distinguished.
- **Label:** V12, the `AdmissionError` subclass.

One control initially failed (V2) and it was **my control that was wrong**, not the code: I had built the "V1" record by flipping only `schemaVersion`, leaving V2 rows in place. I split it into a genuine-V1 case and the hybrid-refusal case rather than relaxing the assertion.

---

## 5. Portable reconstruction verifier

`verify-reconstruction.py` — `--frozen-source`, `--out`, `--interpreter`, optional `--skip-suites`. Bundled files resolve from `Path(__file__).resolve().parent`, so the deliverable is relocatable.

**No audit dependency.** Because the overlay applies the authored **full files**, which already contain the XA-01 result, neither the crosscut audit package nor `apply-reference-correction.py` is needed.

Order: verify all 54 bundled artifacts against the manifest → verify all 16 before-hashes against the frozen source and all 16 bundled after-hashes → copy frozen source into the new root → exact full-file overlay with per-file before/after assertions → re-check the frozen source is unwritten → run suites and controls.

**Fresh execution from frozen candidate25 (rc 0):** 54 artifacts verified, 16 before/after hashes agreed, overlay applied, frozen source re-checked unwritten, then security 464/464, native 375/375, integration 412/0, foundation identity 1596/0, controls 55/55.

Refusal paths, all executed and all writing nothing:

| Condition | Result |
|---|---|
| output root already exists | `REFUSED: output root already exists` |
| output root inside the frozen source | `REFUSED: output root overlaps the frozen source` |
| frozen source has no `docs/` | `REFUSED: frozen source has no docs/ tree` |
| one bundled artifact tampered | `REFUSED: 1 bundled artifacts do not match the manifest`; output root **not created** |

### On root's three critiques of the v1 script

1. **Confirmed** — it named `WORK/apply-correction.py` and `WORK/stages/*.json` without ever copying them there.
2. **Not confirmed, and I verified it rather than assume.** Running `apply-reference-correction.py` with a missing `--copy` exits 1 with `FileNotFoundError`: it reads `(copy/rel)` and asserts equality with the source bytes, so it **requires** an existing tree and owns neither creation nor freshness. The pre-copy was correct. Evidence: `evidence/xa01-applier-requires-existing-copy.txt`.
3. **Confirmed** — `mkdir -p` accepted a populated directory; the verifier now refuses.

The broken script is preserved verbatim at `evidence/reproduce.sh.v1-broken-preserved`. No failed output directory was deleted or reused: `work/out-g1…g4`, `evidence/`, `reconstruct-1/` and `tamper/` all remain.

---

## 6. Deliverables

`scratch/output/`: `artifact-manifest.json`, `changed-source.json` (16 files, before/after hashes), `changed-files/` (full files), `patches/` (16 unified diffs), `source-pin-delta.json` (scratch-only, 12 rows), `verify-reconstruction.py`, `controls-xa02-cr25.v2.py`, `scripts/`, `reports/`, `evidence/`.

Files changed this delta: `discovery-defaults.py` (`f91d63658c98` → `f30b68502b6f`), `native_evidence_model.v2.py` (`2b57bfc34af4` → `3bf179e31e31`), `security_lifecycle_model_v1.py` (`8f43155d7c02` → `fca87329efad`), `native-cases.v2.json` (`6f6ce5f915a1` → `c78ea7f5d3d4`), plus the four pin ledgers.

---

## 7. Limits and open items

- Reference results over synthetic trusted observations. No product qualification, no OS or filesystem behaviour.
- The new-anchor effect on scope/Plan/Run identity is unchanged from v1 and remains a disclosed semantic consequence, not a count/basis effect.
- Pin rebinding is scratch-only bookkeeping; root will rebind after merging F04.
- I did not touch commit/recovery, schema registry/release assets, report refinements or author-package custody, and I did not duplicate the F04 native patch.
- Remaining decision for root: whether `assign_membership` and `unit_scope_descriptor` should refuse V1 as I selected, or only warn. I chose refusal because they feed the scope descriptor, where silent acceptance was the worst of the four observed behaviours.
- All authored bytes remain unreviewed. Source25 and both prior reports remain historical; no self-acceptance.
