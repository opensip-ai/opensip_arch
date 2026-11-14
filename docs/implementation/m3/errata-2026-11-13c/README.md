# Errata of 2026-11-13 (c): one author draft (proposed; r2 after two REQUIRED-FINDINGS reviews of r1)

It implements a recorded lead ruling (`LC` = `/Users/sb/code/.opensip-implementation-cache/lead-2026-10-25`). It is not
accepted, adopted or bound. It is additive: accepted bytes stay frozen.

| File | Subject | Source | Form | Review |
|---|---|---|---|---|
| `ERRATUM-FA2-CENSUS-E2.md` | A new rule `native.symbol-census-population.typescript.v2`: bound FA2-CENSUS-E1's v1 unchanged (by reference, with its sha256), plus two statements. (1) "Alias" is defined by meaning, with C19's list illustrative: entity-name exports stay excluded, and C18's merged meanings stay included. (2) An export entry whose value is a class, function or arrow expression is a row under C5 (`(export).K`, `(export=)`), including TypeScript `export = class …`; the expression's name and members stay excluded by C22. v1 is withdrawn before any use. Five forms owe a code fix (CENSUS-RULE-1a). | LD-DEC-11, "Ruling after both reviews of FA2-CENSUS-E2 r1" | erratum, adoption receipt | both reviewers of E1 |

Owed: the lead's adoption receipt; then the CENSUS-RULE-1a fix, its golden cases, and the move of its rule-id references to v2.
