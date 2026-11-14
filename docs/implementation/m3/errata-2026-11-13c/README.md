# Errata of 2026-11-13 (c): one author draft (proposed; r5 after the reviews of r4)

It implements a recorded lead ruling (`LC` = `/Users/sb/code/.opensip-implementation-cache/lead-2026-10-25`). It is not
accepted, adopted or bound. It is additive: accepted bytes stay frozen.

| File | Subject | Source | Form | Review |
|---|---|---|---|---|
| `ERRATUM-FA2-CENSUS-E2.md` | A new rule `native.symbol-census-population.typescript.v2`: bound FA2-CENSUS-E1's v1 unchanged (by reference, with its sha256), plus four syntactic statements: (0) a closed list of transparent wrappers; (1) a closed definition of alias (C19's forms, plus export entries whose unwrapped value is an entity name); (2) expression-valued export entries are rows under C5, with their expression's name and members excluded by C22; (3) "held by a variable" in C27 is a closed list of holding positions with exact operator sets, and C27's predicate is its colon clause. Alias part (a′) defines JavaScript require declarations as a class (no `export` modifier, no JSDoc `@type`), and an alias holds nothing. The code fixes and golden cases are generated from 135 read-only probes at code `02b97f74` (53 fix owed). v1 is withdrawn before any use. Code fixes are owed in CENSUS-RULE-1a. | LD-DEC-11, "Ruling after both reviews of FA2-CENSUS-E2 r1" and "Correction, 2026-11-14" | erratum, adoption receipt | both reviewers of E1 |

Owed: the lead's adoption receipt; then the CENSUS-RULE-1a fix, its golden cases, and the move of its rule-id references to v2.
