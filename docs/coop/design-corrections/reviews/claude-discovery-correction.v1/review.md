All deliverables are in place. Here is the report.

---

# Authored correction: XA-01 + XA-02 / CR-25

**Standing.** This is **authored work, not acceptance of my own review findings**. Every new byte requires a fresh independent review after integration. No product implementation, no commits, no pushes, no other agents. Nothing outside `scratch/` was written.

**Bindings.** candidate25 `fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d`; prior input tree `da22d2d59f09227a4eafc58821af58e5a96ccc3e4be91b41fbe6b54bef29792b`; prototype manifest `b82bfb921494d9d41da661c434b18811b9b50da7149eb818e4ab9433e085407e`. Reference interpreter Python 3.12.13 / jsonschema 4.25.1.

**Frozen-input integrity, re-verified after all work:** candidate25 **12869/12869** bytes unchanged, prior inputs **136/136** unchanged, `claude-return-successor.v1` untouched.

Deliverables: `scratch/output/` — `artifact-manifest.json` (sha256 `86eab347a181accc7f7e9d2559a288142062f092dd04fb6acc3d02e2bce4cf92`), `changed-source.json`, `changed-files/` (16 full files), `patches/` (16 unified diffs), `source-pin-delta.json`, `scripts/` + `scripts/stages/`, `reproduce.sh`, `reports/`, `controls-xa02-cr25.py`, `identity-trace.md`.

---

## 1. What changed (16 files)

| Class | Files |
|---|---|
| Normative contract | `security-and-lifecycle.md`, `native-evidence.md` |
| Schema bundles | `security-lifecycle.schemas.v1.json`, `native-evidence.schemas.v2.json` |
| Reference models | `discovery-defaults.py`, `security_lifecycle_model_v1.py`, `native_evidence_model.v2.py`, `integration-host-model.py` |
| Checker / fixtures | `check-security-lifecycle.v1.py`, `discovery-cases.v1.json`, `native-cases.v2.json`, `native-evidence-report.v2.json` |
| Pin ledgers (scratch-only) | four `source-pins*.json` |

The XA-01 three-file cap correction is included **unchanged**, applied by the shipped `apply-reference-correction.py`; its `changed-source.json` rows reproduce the published ones exactly. The standalone default-on cap (`enforce_limit=True`) is preserved.

### Versioning

New records, with V1 retained as history and **explicit dispatch** so a changed record is never named V1:

- `PrunedTreeRowV2` (security) / `PrunedTreeV2` (native) — closed `{path, reason, markerCount, markerCountBasis}`, `markerCount` null **iff** basis is `not-enumerated`.
- `DiscoveryProvenanceV2`, `DiscoveryResultV2`, `AdmittedBoundaryInventoryV2` (both mirrors), `UnitDiscoveryV2`.
- Dispatchers: `S.validate_discovery_provenance`, `N.validate_boundary_inventory`. Both refuse an unknown version rather than falling back to the nearest neighbour (controls C12c/C12d).
- **Domain unification:** the native mirror allowed `markerCount` up to unsigned-64, the security mirror `I64NonNegative`. I added `I64NonNegative` to the native bundle so both mirrors now share one domain.

### CR-25 — anchors from the admitted directory observation

`pruned_anchors_from_directories()` in the shared rule takes the directory entries discovery already holds. **No descent:** `_segment_prune` returns the outermost pruned segment, so a directory deep inside a pruned tree maps to the same anchor and contributes no second anchor. Nothing reads, walks or counts inside a pruned tree.

### XA-02 — the basis is declared, never inferred

A new host-observation key `prunedTreeMarkerInventory ∈ {observed-inventory, not-enumerated}` is admitted into the closed vocabulary (misspelling stays `DISCOVERY_OBSERVATION_SHAPE`, control C4d). The disposable instrument's `fs` map is one complete supplied observation, so `observed-inventory` is its honest default; production discovery that does not descend declares `not-enumerated` and gets `null`.

**Per-row, not global:** an anchor whose *own* entry could not be read (`aclUnreadable`) is still reported, with a null count — a count drawn from a directory whose observation failed is not an observation. A single global basis could not express this.

### Native comparison — subset, not equality

`boundaries["prunedTrees"] != derived` became a subset test over `(path, reason)`:
- every marker-derived anchor must appear in the admitted inventory with the **same reason** — missing anchor or mismatched reason still refuses `native.boundary-inventory-mismatch` (now carrying `missingAnchors`);
- an **additional** admitted anchor is accepted and carried, and the admitted rows are what the host projects;
- count and basis are never comparison keys.

### Mandatory admitted boundaries on the authoritative lane

`require_admitted_boundaries()` refuses `None` (`native.admitted-boundaries-required`) and is called from `admit_repository_discovery`. `discover_units(..., boundaries=None)` still works for the **standalone/algorithm lane** — the pure reference callers are untouched (controls C12a/C12b).

---

## 2. The identity trace — executed, not asserted

You asked me to trace this rather than handwave it. The result changed what I would otherwise have claimed.

`unit_scope_descriptor` reads **`t["path"]` only** into `excludedPathPrefixes`, and `scopeDigest = raw_sha256(C(descriptor))`. So:

- **Count/basis:** control **C5b** flips every count to null and every basis to `not-enumerated` and the `scopeDescriptor` and `scopeDigest` come back **bit-identical**; **C11a** shows the selected unit set identical; **C5a** shows they are not equality keys.
- **Your refinement is correct and I applied it:** control **C5c** shows the raw SHA-256 over the canonical boundary-inventory record **does** change. The bytes changed, so any *operational* digest over that record changes. I do not claim they "cannot enter any digest" — the claim is narrower: they do not alter semantic source scope, unit selection, native Coverage/Plan bounds or Run identity.

**One real semantic consequence, disclosed rather than buried.** CR-25 makes previously invisible anchors visible, and an anchor **path** does enter `excludedPathPrefixes` (control **C11b**: `vendorish/.hg`). For a repository holding a pruned anchor outside the conventional set (`.git`/`node_modules` under a unit root, `target` under a Cargo root), `scopeDigest` → `plan2` → RunId differs from the pre-correction value. The analysed byte set does **not** change — the segment rule already pruned the tree, and the descriptor documents that the segment rule applies in addition to the prefixes — but the Plan now discloses the exclusion instead of omitting it. This is the same class of disclosed discovery correction as XA-01. Historical Runs keep their bytes. A reviewer must accept this explicitly.

I considered and rejected suppressing observation-only anchors to keep identity bit-stable: it would make the Plan omit a known exclusion and make the descriptor depend on *how* an anchor became known — the same hidden-provenance dependence that produced XA-01.

---

## 3. Executed results

| Suite | Result | Baseline |
|---|---|---|
| Security | **464/464 cases, 11/11 sweeps** | matches pre-correction |
| Native | **375/375 cases**, 66 matrix cells, 0 open objects | matches |
| Integration | **412 passed, 0 failed** | matches |
| New controls | **29/29** | new |

Run after explicit **scratch-only pin rebinding** (28 pin rows across 4 ledgers; the two `files`-shaped ledgers — foundation and workflows — also pin these sources and were rebound; all four round-trip at their original formatting, so the diffs are only the changed hashes).

**Controls (all 29 pass):** no-marker `node_modules` anchor (C1); pruned tree with only non-marker files (C2); unreadable pruned directory keeps the anchor and nulls the count (C3); zero / 4200 supplied markers (C4a/C4b); declared `not-enumerated` yields null not zero (C4c); unknown basis is a shape error (C4d); count/basis not equality keys, `scopeDigest` bit-identical, unit set identical, operational digest *does* change, directory-only anchor reaches `excludedPathPrefixes` (C5a/C5b/C5c/C11a/C11b); extra admitted anchor accepted and carried (C6); missing marker-implied anchor refused (C7); mismatched reason refused (C8); nested repo/project exclusion, Cargo folding, marker-less `target` anchor, explicit-root parity (C9a–d); **4200+150 custody failures still 4051 in both instruments** (C10a/C10b), 4097 refuses, exactly 4096 admits (C10c/C10d); authoritative lane requires the inventory, standalone lane does not, unknown versions refuse, V2 records validate under their own names (C12a–e); full host composition on version 2 (C13).

The four existing case fixtures needed 19 edits, each reported individually in `out-stage8/fixture-edits.json`. **No expected count, anchor, unit, refusal or exit was rewritten** — only basis added, inventory `schemaVersion` 1→2, and three `outputSchema` names. A changed anchor set would have shown as a remaining failure.

---

## 4. Explicitly not selected, and why

**Counting custody- and depth-excluded directories toward the cap.** My pass-2 report suggested this; you are right that it is a **policy change, not a fix for the refuted CR-12(b)**. I did not apply it. The corrected behaviour is preserved exactly: 4200 first-party directories with 150 custody failures still admit **4051 units in both instruments** (C10a/C10b). I looked for contract evidence making it mandatory and did not find any — S3 says custody-excluded units are "explicit unknown required scope, not a successful empty scope", which constrains how they are *reported*, not how they are *counted*. So there is no conflict to document, and I recorded the option in the S3 prose as a separately reviewable, **not-selected** alternative that would turn present ACCEPT results into refusals. Unknown custody still cannot become successful empty scope or examined-clean Coverage — I added that sentence to S3.

**No public work-budget flag or arbitrary product limit.** The S3 prose now states plainly that the 4096 cap was never an input bound (the shared rule materialises and sorts the supplied inventory before comparing cardinality, before *and* after XA-01), that bounding the host observation is the observation-admission and qualification responsibility, and that the synthetic trusted fs-map instrument accepting a large array is not a product limit.

**Downward depth bound documented.** S3 now records that the 256-level constant is reused as a downward unit-depth bound, that `DEPTH` exclusions are exported in `custodyExcludedUnits` so both instruments select the same directories, and that it is an exclusion with unknown standing, not a work budget.

---

## 5. Normative prose actually changed

Not a separate suggestion — the owner documents are edited:

- **`security-and-lifecycle.md` S3:** the sentence *"its anchor is recorded **once** in `prunedTrees` with the number of markers it hid"* — the XA-02 defect statement — is **withdrawn in place** and replaced with the observation-based anchor rule, the no-descent rule, the closed version-2 row, the basis semantics, "zero observed is never zero hidden", the provenance-only standing including the operational-digest caveat, plus the custody/depth and work-bound paragraphs.
- **`native-evidence.md` §1.4:** `UnitDiscoveryV2`/`PrunedTreeV2`, the observation-based anchor rule, the subset comparison replacing whole-list equality, the superset framing, the `require_admitted_boundaries` authoritative-lane rule, and the refusal-table row rewritten so an additional admitted anchor is lawful.

---

## 6. Additional normative defect found while doing this

**`DiscoveryResultV1` had to be versioned too.** It is an owning output schema whose `provenance` `$ref`s `DiscoveryProvenanceV1`; without a `DiscoveryResultV2` the checker would have validated a version-2 provenance under a version-1 output name — exactly the "changed schemaVersion named as V1" failure you warned against. Counterexample preserved: before `DiscoveryResultV2` existed, all discovery cases reported `schemaVersion: exact const type/value mismatch`. Smallest change: add `DiscoveryResultV2` (identical shape, version-2 provenance ref) and repoint the two checker name bindings. Applied.

**A second, smaller one (fixed in passing):** the two `markerCount` mirrors did not share a domain — native allowed unsigned-64, security `I64NonNegative`. Smallest change: add `I64NonNegative` to the native bundle and reference it from both V2 rows.

---

## 7. Limits

- Reference results only, over **synthetic trusted observations**. No product qualification, no OS/filesystem behaviour, no real scanner.
- The `fs`-map instrument is a design reference; the production observation-admission bound remains unowned and is stated as such rather than invented here.
- I did **not** touch the commit/recovery API, schema registry/release assets, report refinements, or author-package custody — those are yours, including the Rust lifetime and field-privacy issues in my illustrative callback sketch.
- Changes to shared native/schema files were kept patchable: both bundles round-trip byte-exactly at their own formatting, so the diffs are additions plus the specific edits.
- `native-evidence-report.v2.json` changed because the native checker writes its report there; it is a run artifact, not a source edit.
- All 27 tracked findings and the original blind-123/8/3 and application obligations remain open. This authored delta is unreviewed.
