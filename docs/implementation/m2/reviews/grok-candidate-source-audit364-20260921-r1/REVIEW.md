# Independent review — candidate source/inventory audit 364

**Standing:** read-only **source regeneration and inventory-gap audit** of frozen `candidate-source-audit-364`. No source moves, no inventory/runtime selection, no native filesystem tests, no full-crate tests. **365** generated layout and **inventory v33 draft** are WIP and **outside** this verdict. Product remains `fa72e50`. Prior 363 REVIEW `a45bc8a5…8569` (6669 B, no ADDENDUM), 362 `168809c4…dff1`, SOURCE-NOTE `772694b0…0cb8` were read and are **unchanged**. No Claude agreement is claimed (06:41 Fable quota).

Python 3.12.13 `-I -B` from `/tmp/opensip-implementation/source-audit364-env` (UCD **15.0.0**). Rustfmt 1.95.0. Isolated `grok-out/live`; freeze workdir **not** overwritten. **This review reproduced:** 268/313/363 archive member rehashes; three generated schema files byte-equal to 363 after rustfmt; Unicode 15 unassigned **707** ranges and **1530** fold mappings over **1112064** scalars; inventory 32 vs candidate 363 gap; reader registry **136** rows / **29** roots.

---

## Verification

Archive-pin and every `subject.json` member matched **before** extract. Frozen archive: **764700 B, 239 members, SHA256 `163a7387367b1e78a6937d827fc6346e97c87db39ba9600d6f088f90d44c3ddf`**. Extract rehash: 0 mismatches. Standing: “Read-only source inventory and generation audit; no runtime selection.”

Independently rehashed parent archives used as generator inputs:

| Archive | Members / bytes / SHA256 |
|---|---|
| host-installation-trust-checkpoint-363 | 574 / 6895004 / `b07f1a6d…e3ad` |
| native-provenance-checkpoint-313 | 1008 / 9483840 / `355396bd…ee39` |
| native-manifest-checkpoint-268 | 587 / 5001656 / `40fbfe5f…a5ba` |

Inventory v32 pin `105a260d…b72e` (409 rows). UnicodeData.txt `806e9aed…6a73`.

---

## Regeneration (268/313 vs 363)

One explicit path adapter on `generate_manifest268_schema.py` (input JSON only). Both 313 generators unchanged. Isolated replay with the archived dependency tree + rustfmt 1.95:

| File | SHA256 / bytes | Equal 313 and 363 |
|---|---|---|
| `component_manifest_shape.rs` | `efb068ac…70d8` / 23210 | yes |
| `trust_record_shape_nodes.rs` | `8446f0f8…10d3` / 203595 | yes |
| `trust_record_visit_nodes.rs` | `43836933…2249` / 140150 | yes |

Reader generation report: **136** registry rows, **29** roots (`BeginBatchV1` … `TrustEventV1`). Exporting that registry does not invent new edge targets.

Handwritten wrappers still present in 363 and still name the generated modules: `component_manifest.rs`, `trust_record_shapes.rs`, `trust_record_reader.rs`. Unicode table constants remain in `metadata_unicode15.rs` / `metadata_casefold15.rs`. LAYOUT’s three physical moves into `generated/` plus two table splits are **proposal only** (365).

---

## Unicode 15 tables

Independent reconstruction from pinned UnicodeData.txt + Python 3.12 casefold over every valid scalar (surrogates excluded):

- unassigned ranges: **707** (exact match to `UNASSIGNED`)
- non-identity fold mappings: **1530** (exact match to `TABLE`)
- scalars: **1112064**
- all-scalar sequence SHA256 `b6b067c3…e891` (byte-equal frozen `unicode-table-audit.json`)

Data-table audit only. Normalization wrappers and any Unicode 16 bridge are **not** requalified.

---

## Inventory gap (v32 vs candidate 363)

508 candidate files, 409 inventory rows, **213** unlisted, **114** inventory rows not in the candidate. `unlisted-files.json` accounts for every extra path. That is **not** runtime/source-policy acceptance.

Independent recount of the 213 extras:

| Classifier | Fixtures | Non-fixture (.rs) |
|---|---|---|
| r4 `/tests/fixtures/` | **132** | **81** (includes `storage/fixtures/pin-budget174.json`) |
| r5 `/fixtures/` (frozen JSON) | **133** | **80** |
| Independent `/fixtures/` | **133** | **80** (all `.rs`; `otherUnlisted` empty) |

`pin-budget174.json` is unlisted and is a fixture under `/fixtures/` but not under `/tests/fixtures/`. That is the r4 misclassification. Frozen r5 `result.json` / `unlisted-files.json` report **133** fixtures, consistent with this recount.

README (and the review request) say r5 supersedes 80/133 with **79/134**. Those 79/134 numbers **do not** match r5 JSON or this recount (80 .rs + 133 fixtures = 213). Do **not** relabel r5 JSON. The pin-budget correction is real; the 79/134 arithmetic is not.

LAYOUT’s next inventory successor must still list all 213 plus any new generator/table paths, remove no inherited row without an explicit successor, and keep fixture vs generated vs handwritten vs OS adapter vs public API distinct. Inventory v33 draft is **outside** this verdict.

---

## Failed-run history (not passes)

| Run | Result |
|---|---|
| r1 | `ModuleNotFoundError: jsonschema` (`generate_reader313.py`; uv CPython 3.12 without packages) |
| r2 | `ModuleNotFoundError: jsonschema` (`native-case15-reference-env`) |
| r3 | `ModuleNotFoundError: attrs` (copied incomplete site-packages) |
| r4 | regeneration/Unicode **PASS**; fixture class `/tests/fixtures/` missed `pin-budget174.json` (132 fixtures) |
| r5 | `/fixtures/` includes `pin-budget174.json`; regeneration/Unicode PASS; JSON fixtures **133** |

No failed run is counted as passing.

---

## Findings

Regeneration of the three schema files and both Unicode 15 tables **reproduces** 363 bytes. The 213-path gap is fully listed and is not product acceptance. Registry export is 136/29 as required for a later portable generator, without new target law.

**Actionable audit defect:** README/request 79-source/134-fixture split is inconsistent with r5 `unlisted-files.json` and with independent classification (80 `.rs` / 133 fixtures). Report the JSON split; do not treat 79/134 as verified.

**Must not be counted closed:** inventory/runtime selection; 365 layout implementation; five-member `StoreGenerationBindingV1`; current authority; writers; M2–M6; Unicode wrapper requalification.

---

## Remaining (do not count closed)

365 private generated layout if later frozen. Inventory v33 draft. Portable `tools/generate_security_tables.py --check`. `trust.rs` size remains a maintainability note in LAYOUT, not this audit’s implementation.

---

## Verdicts

- [x] **364 as frozen read-only source/inventory audit:** 239-member archive verified; three generated files byte-equal 268/313/363; Unicode 707/1530/1112064 reproduced; 213 unlisted / 114 missing-from-candidate accounted; 136 registry rows / 29 roots; r1–r3 import failures retained; r4 fixture miss identified; r5 JSON is 80 `.rs` + 133 fixtures. Not inventory or runtime acceptance.
- [ ] **Not** 365 layout, inventory v33, selected-I/current authority, writers, or product installation.
