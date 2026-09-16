# Independent Grok review: generator development activation design unit v1

**Reviewer:** Grok (explicitly authorized). Codex remains lead. Not Claude agreement.
**Subject manifest:** `docs/implementation/m1/generator-selection-v1-subject.json`
**Manifest SHA-256:** `224029710644805c04486de173e64dc08a613ef5bed9433233d336702ece342b`
**Members:** 42
**Verdict:** **ACCEPT-DESIGN-UNIT**

This is a **design selection** of the already-reviewed generator04 maintenance lane on these exact frozen architecture bytes. The prior implementation verdict ACCEPT-UNIT is **not** this approval. Root substantive assent remains separate. This unit does not settle root/report/provider/checker bootstrap, add schema semantics, loosen runtime authority, approve release, or bypass the public activation gate.

## Custody and verifier-definition joins

42/42 subject members match architecture bytes before and after. Subject paths are POSIX-sorted unique.

Using the product `verify_design.py` definitions (imported read-only; no forged lock):

- `pin_rows` accepts `successor.candidates` (41) and `successor.parents` (2) as sorted unique path lists.
- The successor record is in the subject. Candidates **cover** every subject member except that record, with identical path/bytes/sha256 pins.
- No candidate or record path reuses a currently accepted lock input, inventory, or contract path.
- Parents are live accepted pins: inventory v4 candidate `c6c85fb8…fe84f5` and source-selection-v3 successor `e638c55c…4ae4`. Architecture bytes match. Current product lock still verifies without this unit.

`passageOverrides` is empty (no schema/owner/runtime meaning change).

## Semantic selection

The unit copies **37** owned product inputs byte-identical to frozen generator04 (`f3bee6f2…6e35`). Finite **348**-file `generator-closure.json` (`5e3e77c4…8635`) and `schemas/registry.json` (`ec893f08…0554`) are unchanged. The materialization map has those 37 destinations; every `productPath` is among the proposed inventory-v5 additions. Inventory v5 is **not** in the live lock; `selection-validation.json` records `actualInventory5Accepted: false`. Materialization requires that separate inventory acceptance.

Selected behavior is the generator **maintenance** lane only: npm 11.13.0 / TypeScript 6.0.3 via this package’s manifests; observed macOS Node/Python/Rust pins; explicit offline `build_contracts.py` / `provision_python.py`. Report/provider/checker bootstrap and the root workspace package manager are not overridden.

Public `generate_contracts.py` still requires these exact closure bytes among an accepted design unit’s inputs. That gate **currently refuses** (implementation review 04: workdir not created, including `--write`). This design unit does not insert a synthetic successor into the product lock and does not claim public positive/write/drift evidence in advance. After genuine root assent, those branches belong in a private product copy.

D01–D04 remain disclosed: post-selection public write/drift exercise (D01); 13-file wrapper subset backed by 348-file snapshot equality (D02); native `tools/contracts` subpath grant (D03); developer-host trust, not hermetic release (D04).

Review-basis pins for the 04 review, root receipt, and frozen generator04 subject match architecture bytes.

Unchanged generator internals were not re-run; 04 already reproduced eight outputs/input-closure and 23 reviewer controls with `sourceApproved: false`.

## Later unbound checker discovery (does not unwind this selection)

Root evidence `m1-tooling-orchestration-candidate-01/generator-discovery01.json` (copied at `review/results/generator-discovery01.json`, SHA-256 `d576998e…3640`) is an **unbound-trial** check-boundary run (`selectedToolPolicy: null`, `passed: false`) against the generator04 `tools/contracts` package on live inventory v4. It is not a bound positive and is not M1/static-boundary closure.

Confirmed in frozen generator04 / selection copies (immutable):

- `runtime/{exact-json,patterns,schema}.ts` are TypeScript templates with no lane tsconfig in this unit (checker: config-invalid).
- `assemble-native.cjs` does `require('./node_modules/typescript')` (external-by-path). Sibling `render-types.cjs` / `validate-schemas.cjs` use package `require('typescript')`.
- `validate-schemas.cjs` does `require(file)` of a just-written scratch module (computed-require; needs a finite exact local loader policy).
- Materialized TypeScript 6.0.3 `typescript.js` has `require(modulePath)` and a **guarded** optional `source-map-support` (MODULE_NOT_FOUND).

These are **outstanding integration duties** for a later generator05 / tsconfig inventory path / selected tool-policy work. They are **not** required findings against this narrow design selection, which never claimed checker-lane or static-boundary qualification and left checker bootstrap/policy unset. Inventory v5’s 77 additions do not include a tsconfig; that is a future additive path, not a hole in the 77-file layout. No fabricated policy was used to produce a bound pass.

## Must-fix / should-fix

None in this design-selection scope. Required findings remain empty.

## Remaining

Root ACCEPTED-DESIGN-UNIT assent; selecting accepted inventory v5 before materializing owned product modules; public generation/write/drift on a private product copy after that; **generator05/tsconfig and a selected finite loader/path policy before any bound checker positive**; checker bootstrap/policy; HostAssetPin; M1; release; fresh blind consumer B.
