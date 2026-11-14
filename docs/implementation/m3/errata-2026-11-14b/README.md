# Errata of 2026-11-14 (b): one author draft (proposed; r1)

It implements the lead coordinator's brief (`LC` = `/Users/sb/code/.opensip-implementation-cache/lead-2026-10-25`). It is
not accepted, adopted or bound. It is additive: accepted bytes stay frozen.

| File | Subject | Source | Form | Review |
|---|---|---|---|---|
| `ERRATUM-FA2-CENSUS-E3.md` | (A) The carrier of FCE1.7's population-rule binding: a member of the enumerator closure's tree, `opensip-interface/symbol-census/population-rule.json`, with exact bytes naming one rule id; a closed table of bindable rules per role subprotocol; the packager is its only writer. The host checks it at Plan time before spawn, and the evaluator checks it at replay. A missing, unknown or withdrawn binding, or one for another provider, is §9.8's existing host invariant. The carrier exists from adoption. `complete` is honoured only after the FA-2 successor stating the rule is in `design-lock.json`. (B) Statement 4: an export entry's declarations are classified one by one, by syntax; every alias declaration exposes its own target; the entry is a row when any declaration is not an alias; and "alias" in the design note's F3 is statement 1's (F3 stays a design note). (C) Rule `native.symbol-census-population.typescript.v3` = bound v2 (by hash) plus statement 4; v2 is withdrawn before any use (scoped check). (D) 1,298 read-only probes at product `e3cd0bf5` (486 match, 812 fix owed); golden, id moves, and what is not bound. | lead brief (FA2-CENSUS-E3); carrier plan `LC/f2min/census-rule-1b/PLAN.md` G1-G7; `LC/f2min/census-rule-1/QUESTIONS.md` item 12; LD-DEC-11 "Sentence owed" | erratum, adoption receipt | two (Claude, Codex) |

Owed: two reviews and the lead's adoption receipt. Then: the CENSUS-RULE-1a fix and golden for statement 4, the move of
the rule-id references to v3, the carrier units, the FA-2 contract successor stating E1-E3 with its `design-lock.json`
entry, and the one repackaging.
