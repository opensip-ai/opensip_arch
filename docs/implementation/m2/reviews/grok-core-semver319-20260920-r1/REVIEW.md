# Independent review — core SemVer reference completion 319

**Standing:** bounded source/reference review of frozen `core-semver-reference-319`. Unselected semantic **composition**: after full `CoreInventoryV2` shape, require the existing catalog `SEM.version` grammar before original 229 `project_core`. Not a schema mutation, new parser, native 318 freeze, TCB/signature admission, or product installation. Native 318 remains unfrozen and is **not** approved from this packet. Installed product remains `fa72e50`. 316 and 317 reviews were not edited.

Python 3.12.13 `-I -B`. No native tests. No product/frozen edits.

Pins **before** extract: **2322720 B, 513 members, SHA256 `96222a19f0bc7f8eafcb9ae83d87bf7a83a768782e447e6b913b5be2e56d32b4`**. Extract rehashed **513/513**. Nested 229 r3 pin `edde8b4f…6b4e` (live tar match). Nested 312 pin `f04b5b42…6e5b` (live tar match). `distribution_model_local.py`, `time_provenance_reference312.py`, and catalog `check_compatibility_design_v2.py` are **byte-identical** to frozen 312. Wrapper SHA256 `2a406227…6b3c`.

Preserved: 317 REVIEW `0740164f…2943`; 316 REVIEW `1ef324da…d059`; 315 REVIEW `87e3cd2d…e0e8`. 317 is closed **policy** clarification only; this freeze does not implement 317 constructors.

---

## Shape vs semantic admission

229 OWNER **A.2**: inventory `semanticVersion` is the signed field hashed into `closure2` and must use **the same SemVer grammar the catalog uses** for `version` / `hostCoreConstraint`.

Catalog 267 already splits:

- **Structural schema** (inventory `maxLength` 256 + loose `-[0-9A-Za-z.-]+` / `+[0-9A-Za-z.-]+`) admits consecutive dots and numeric prerelease leading zeros.
- **Semantic admission** is `MF.SEM.version` from `check_compatibility_design_v2.py` (`version-constraint-schema.completed.v2.json` oneOf[0] pattern): no empty identifiers, no leading zeros on **numeric** prerelease; build metadata may contain leading zeros; hyphen-only identifiers such as `1.0.0--` match as a non-empty non-numeric identifier.

Original `project_core` only `schema('CoreInventoryV2')` then protocol/platform/tree/bootstrap/closure. That is **shape-only**. It accepted `1.0.0-01` and `1.0.0-alpha..x`. Body shape is **not** catalog-equivalent semantic admission. Do not equate them.

**Concrete missing gate on this path:** a mandatory `SEM.version(inventory.semanticVersion)` **after** full inventory shape and **before** protocol/tree/platform/closure derivation. 319’s wrapper is that gate. Original `project_core` stays the shape/projection owner (unchanged bytes). The wrapper does not invent a second SemVer implementation, trim, fixed-width numeric conversion, or caller `hostCoreConstraint`.

This is **necessary** before original-core **closure binding**: A.2 puts `semanticVersion` into `closure2` identity. A shape-only projection would bind catalog-invalid versions. It is **not** a claim that 229’s loose regex was a schema bug to mutate; 267 already keeps schema looser than semantic admission.

Refusal label: private `core-semver`. No new public diagnostic selected.

---

## Wrapper

```
value = canonical CoreInventoryV2
schema(CoreInventoryV2)          # unchanged 229
SEM.version(semanticVersion)     # exact catalog Python SEM.version
return original project_core(...)
```

On success, returned closure/identity **equals** original `project_core` (checked for all 10 positives). Arbitrary-width numeric cores/prereleases that satisfy strict grammar remain identities (200-digit majors, `1.0.0-0`, `1.0.0+00`). Inventory **256**-character schema cap still applies (`1.0.0+` + 250 `x` is in-cap and admitted). Build metadata remains part of the exact identity field even where ordering ignores it.

---

## Reproduction (review-local copy; frozen logs not overwritten)

`check_core_semver319.py` and `check_controls319.py` in `grok-out/repro/`. Frozen `check-report.json` / `controls-r1/` unchanged.

| Kind | Result |
|---|---|
| Cases | **22** |
| Positive (shape ∧ strict) | **10** |
| New rejections (old `project_core` accepted, wrapper refuses `core-semver`) | **4**: `1.0.0-01`, `1.0.0-alpha..x`, `1.0.0+build..x`, `1.0.0-0`+199 nines |
| Live report SHA | `f5ea48b8…f648` frozen-equal |
| Controls + baseline | 3 syntax-valid (`omit-strict-grammar`, `truncate-prerelease`, `invent-machine-width`) + baseline; report SHA `13226187…2e0a` frozen-equal |

`omit-strict-grammar` would accept the four new rejections; `truncate-prerelease` would drop prerelease/build; `invent-machine-width` would refuse wide numeric cores that SEM admits. All caught.

No signatures, native TCB, or qualified physical tree claimed.

---

## Findings

1. **Gate is required and was absent** on original-core projection. 319 names it without changing 229 wire/schema.
2. **Valid-input identity unchanged** vs original `project_core`.
3. **Do not freeze/approve native 318 from this packet.** 318 r1/r2 evidence is against the loose projection. After this review, root must apply the guard to 318, regenerate oracle fixtures, and rerun checks/controls on **new** bytes before freezing.

**Actionable defects in this freeze:** none that make the wrapper self-contradictory with 229 A.2 / catalog 267 SEM.

---

## Remaining (do not count closed)

Native 318 freeze, 229 executable/signature/root/TCB, 312 embedded resolver, 317 scoped constructors, M2–M6. No migration policy from uninstalled format.

---

## Verdicts

- [x] **319 as unselected semantic composition:** archive verified; 229/312/catalog modules unchanged; missing catalog-equivalent SemVer gate after shape is real; wrapper is that gate; 22/10/4 and 3 controls frozen-equal.
- [ ] **Not** native 318 approval, schema change, TCB, publication, or product installation.
