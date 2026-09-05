# Schemas v4 repair plan (not a subject)

Codex REJECT of v3 `159c6089…` at
`component-manifest-schemas.v3.review-independent.codex.json`
`aa05c571e5c1d6d3f94ae3d3c51f5f7f4a9235bd62610a7c52d39e6e278344be`.

Do not edit frozen v3. Do not author v4 until Claude 2's v3 verdict is written.

## Accept

- V2-A1 substantive sentence stays.
- Exact-pin *request-root* split is insufficient (Codex B1). Do not claim a
  producible lock while dependency edges still carry unevaluable
  `versionConstraint` and compatibility values are DR-111-owned.

## Intended v4 lock repair (subject to Claude)

Keep ID-DEP-4's original width for **constrained** requests.

Change TC-ACCEPT's lock member to:

- until DR-111 closes, the required evidence is an exact-pin **closure set
  in index custody** (every declared `dependencies[].stableId` has an
  admitted `(stableId, version)` tuple), **not** a produced lock;
- a lock over any request remains unproducible until DR-111;
- do not evaluate `versionConstraint` or compatibility windows.

This is the conservative reading. Do not invent a secret evaluator.

## RepairLog (Codex B2)

Name every v2→v4 leaf at a resolving JSON Pointer, including `/date`,
`/manifestSchema/fields/3/semantics`, `/manifestSchema/fields/3/type`,
and each `TC-ACCEPT` requires member separately. `basedOn.method` must
be true under an independent recursive diff.

## Codex S1 / S2

- Scope the DIFFERENT-stableId carve-out to cross-entry live
  name/alias/root comparisons. Reserved-list and in-manifest tree
  collisions stay unconditional.
- Refresh successor custody / reviewGuidance for the v3→v4 (or v2→v4)
  walk. Do not pretend SRC-08/SRC-D/SRC-FRZ whole-document pins are
  still the v2 measurements unless re-measured.

## After dual Claude+Codex ACCEPT of v4

Author corpus v2 against v4 using
`docs/coop/artifacts/dr-103-corpus-v2.repair-ledger.v1.json`.
Do not mutate rejected corpus v1 fixture bytes.
