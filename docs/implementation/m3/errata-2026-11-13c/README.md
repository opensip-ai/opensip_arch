# Errata of 2026-11-13 (c): one author draft (proposed, unreviewed)

It implements a recorded lead reading (`LC` = `/Users/sb/code/.opensip-implementation-cache/lead-2026-10-25`). It is not
accepted, adopted or bound. It is interpretive and additive: accepted bytes stay frozen.

| File | Subject | Source | Form | Review |
|---|---|---|---|---|
| `ERRATUM-FA2-CENSUS-E2.md` | The rule `native.symbol-census-population.typescript.v1` (bound erratum FA2-CENSUS-E1 r5, `../errata-2026-11-13b/ERRATUM-FA2-CENSUS-E1.md`): "alias" means C19's forms, not every symbol the compiler flags as an alias. Four CommonJS export forms follow: `exports.K = class/function …` and `module.exports = class/function …` each give their entry a row under C5, and the expression's own name and members stay excluded by C22. Two of the four have a code fix owed (CENSUS-RULE-1a). No new rule id is minted; the alternative (`…typescript.v2`) is stated for the reviewers. | LD-DEC-11, "Reading needed after the code reviews" | interpretive erratum, adoption receipt | both reviewers of E1, before the rule is first bound to any closure |

Owed: the lead's adoption receipt; then the CENSUS-RULE-1a fix and four golden cases.
