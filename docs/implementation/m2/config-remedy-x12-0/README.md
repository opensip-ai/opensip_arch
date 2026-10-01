# CONFIG.INVALID remedy text — contract successor X12-0

2026-10-01. Claude Opus 5.5, implementation lead. This is the remedy-text contract successor that law X12 r3 item 7 ("Remedy keying", answering Grok X12 r1 RF-2) requires before X12b emits rows 1, 2 or 3a. The unit is PROPOSED and needs independent review and root assent before selection. It changes no code, class, exit code, route, schema, registry, generated code, inventory or product file.

## Why

`PUBLIC_ROUTE_REMEDIES` in the native reference model is keyed by public code. native-evidence's `remedyKeyingConstraint` says one string must stay true for every key that reaches its code. X12 rows 1, 2 and 3a reuse `CONFIG.INVALID` (detail `CONFIG.INVALID`) for an unregistered pack ID or a selection of zero or several sources (row 1), a supplied pack (row 2) and a supplied document that fails lexical or schema admission (row 3a). The published string speaks only of a capability selection, so it is not a true next step for those rows.

## The string

Before:

> the configured capability selection is invalid: name a registered capability id from the native capability matrix, and state at most one row per (capabilityId, languageMode, workspaceRoot)

After:

> the configured capability or policy selection is invalid: for capabilities, name a registered capability id from the native capability matrix, and state at most one row per (capabilityId, languageMode, workspaceRoot); for policy, name exactly one bundled policy pack id, written exactly as name:version, and supply no policy document of your own or from a third party

How it stays true for each key that reaches the code:

| Key | Next step the string gives |
|---|---|
| `native.requested-capability-unregistered` | name a registered capability id from the native capability matrix |
| `native.requested-capability-mode-unregistered` | the same sentence, unchanged from the published string; the matrix registers (capabilityId, languageMode) cells |
| `native.requested-capability-duplicate-ownership-tuple` | state at most one row per (capabilityId, languageMode, workspaceRoot) |
| X12 row 1, unregistered ID | name a bundled policy pack id, written exactly as name:version (law item 3: byte-exact, no normalization) |
| X12 row 1, `count:<n>` | name exactly one |
| X12 row 2, supplied pack | supply no policy document of your own or from a third party (`SuppliedProvenance` is `User` or `ThirdParty`) |
| X12 row 3a, malformed supplied document | the same sentence; a supplied document is refused whatever its bytes |

The capability sentence keeps its words byte for byte, so the two predicates `foundation/check-identity.py` applies to this string (`registered capability id from the native capability matrix` and `(capabilityId, languageMode, workspaceRoot)`) still hold. The string is 367 ASCII characters, within DomainDetail.remedy's BoundedText bound of 1024. The public code stays `CONFIG.INVALID`. No detail, alias or key is added.

## Overrides

Two line overrides, both on line 1158, the table's one `CONFIG.INVALID` row:
- `docs/coop/design-corrections/native/native_evidence_model.v2.py`, the frozen v2 source that law X12 names;
- `docs/implementation/m2/capability-totality-reference-selection-v1/reference/native_evidence_model.py`, the selected reference copy. That unit's README says the current native reference "becomes reference/native_evidence_model.py of this unit". Its line 1158 is byte-identical to the v2 source.

Line selectors are the precedent for a text parent (source-selection-v3 overrides `workflows_model.v1.py` line 380). verify_design refuses line selectors only on JSON parents.

## Copies not overridden

Every other accepted file that contains the string is historical review evidence under `docs/coop/design-corrections/reviews/` (before-images, work trees, diffs and tool logs of the v19 and v20 authoring rounds). Those record what was reviewed then. Overriding them would falsify that record, and they are not a current reference.

No product file contains any `PUBLIC_ROUTE_REMEDIES` string. The product's `native-v2` schema and the generated `report.ts` carry the `remedyKeyingConstraint` prose, not the table. That prose stays true ("adding a key that routes to an existing code obliges its author to check that code's remedy ... and to widen it"), so no schema byte, generation or drift change follows. X12b embeds this string, and item 10 tests it byte for byte.

The source comment above the table (lines 1150 to 1156) records the earlier ownership-tuple widening. It stays true and is not overridden.

## Evidence

- `evidence/build_x12_0.py` rebuilds `successor.json` and the subject manifest deterministically.
- `evidence/check_remedy.py` applies both overrides in memory, parses each result with `ast` without importing it, and checks the table's keys and other values, the agreement of the two copies, the check-identity predicates, the X12 conditions and the BoundedText bound. `check-identity.py` itself cannot run on this Mac: the native model refuses Python 3.14.6's Unicode 16.0.0 case data, against its declared 15.0.0, as an environment fault.
- `evidence/verify_scratch.py` runs the real verify_design with a synthetic in-memory review and assent.
