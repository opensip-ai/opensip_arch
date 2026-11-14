# Adoption receipt: ERRATUM FA2-CENSUS-E2, r5 (TypeScript census rule v2)

**Prepared by the records clerk on the lead coordinator's binding instruction (OD-LEAD-1); the lead's merge of this branch is its adoption.** The decision behind the erratum is the lead's LD-DEC-11 (`LC/decisions/LD-DEC-11-census-population/DECISION.md`, 19,588 bytes, sha256 `79acc299b95f21d48dc2750171658ff6fd8737f2680804135002fd22810cefdc`; the E2 sections at its end). E2 is an erratum to FA2-CENSUS-E1 (bound) and through it to FA-2 section 9.8. The accepted bytes of FA-2, E1 and their records are NOT edited; E2 is read with them.

**Adopted:** the exact bytes `docs/implementation/m3/errata-2026-11-13c/ERRATUM-FA2-CENSUS-E2.md` (r5, 35,800 bytes), sha256 `56723546361dd29bed388b22837f57f2fbb4ae131e61a7a957544ab0ad6f031e`, and its index `README.md` (1,526 bytes, sha256 `2b5e164ab4324dad3db857604011d666217f4e8407b3d2fa8717bab9ce1ba405`), at head `b038d897e28162852dc3b77dba407675abe6be8b`, the bytes both reviewers accepted.

**Substance, in plain words:**
- E2 defines the rule `native.symbol-census-population.typescript.v2` as the bound v1 (E1's rule, referenced by hash and incorporated unchanged) plus four syntactic statements: (0) a closed list of transparent wrappers; (1) a closed definition of alias (C19's forms, plus export entries whose unwrapped value is an entity name; JavaScript require declarations are a class, and an alias holds nothing); (2) expression-valued export entries are rows under C5, with their expression's name and members excluded by C22; (3) "held by a variable" in C27 is a closed list of holding positions with exact operator sets, and C27's predicate is its colon clause.
- v1 is withdrawn before any use (FCE2.3). It stays in E1 as bound, is never bound to any enumerator closure, and every reference to it moves to v2. The claim of non-use is scoped to the tracked sources the erratum names (the code unit at `02b97f74`, its closure tool, and product main `616024f7`); it does not prove that no untracked artifact names v1, and an artifact found outside that scope keeps v1's interpretation and binding.

**What this does NOT bind or accept:**
- No code. CENSUS-RULE-1a (the provider's fixes: 53 owed at code head `02b97f74`, per the erratum's generated table of 135 probed cases, 82 matching and 53 differing) is owed, with its golden cases (FCE2.5) and the move of its rule-id references to v2.
- The rule carrier (CENSUS-RULE-1b): no enumerator closure is bound to v2, or to any rule, by this receipt.
- The FA-2 contract successor that states v2 in section 9.8 with E1 and E2, and its `design-lock.json` entry: still owed and not generated, as for E1 (FA-2 is a design-lock input).
- **The complete-census prohibition stays in force:** until CENSUS-RULE-1 (1a and 1b) is accepted and its binding exists, the TypeScript provider sends no `complete` census.

**Known editorial defect of the accepted bytes (not changed):** Codex's nonblocking note: `ERRATUM-FA2-CENSUS-E2.md:29` still says "The author ran no probe"; the later round-5 probe account (135 probes) supersedes that stale provenance sentence, and the reviewer reproduced the probe results independently. The bytes are not changed.

**Basis, bound by value:** Codex gpt-6.1-sol/high, session `01a1d760-d5f9-7972-a79d-38d555a7979b` (`reviews/codex-fa2-census-e2-r1/review.json`): ACCEPT at the final head. Claude claude-opus-5-5/medium (`reviews/claude-fa2-census-e2-r1/review.json`): ACCEPT at the same head. Earlier verdicts on earlier heads (REQUIRED-FINDINGS or REJECT) are history.
