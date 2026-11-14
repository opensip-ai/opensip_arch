# Errata of 2026-11-14 (b): one author draft (proposed; r2 after the reviews of r1)

It implements the lead coordinator's brief (`LC` = `/Users/sb/code/.opensip-implementation-cache/lead-2026-10-25`). It is
not accepted, adopted or bound. It is additive: accepted bytes stay frozen.

| File | Subject | Source | Form | Review |
|---|---|---|---|---|
| `ERRATUM-FA2-CENSUS-E3.md` | (A) The carrier of FCE1.7's population-rule binding: a member of the enumerator closure's tree, `opensip-interface/symbol-census/population-rule.json`, with exact bytes naming one rule id; a closed table of bindable rules per role subprotocol; the packager is its only writer. From adoption, the host makes four prospective checks at Plan time, before spawn: the member is present, it names a known rule, the rule fits the provider, and the rule's FA-2 successor is in the host's design lock. Each failure is §9.8's existing host invariant. Replay reads the retained digest under the law that could have made it (R-a to R-d), so a historical v2 member or a pre-carrier Rust closure is read, not refused. The carrier exists from adoption, and a rule stated only by an adopted erratum binds nothing until its successor is bound. (B) Statement 4: an export entry's declarations are classified one by one, by syntax; every alias declaration exposes its own targets, found by a finite walk (a cycle is unresolved); only expression `default`/`export=` values make other locals `unknown`; the entry is a row when any declaration is not an alias; and "alias" in the design note's F3 is statement 1's (F3 stays a design note). (C) Rule `native.symbol-census-population.typescript.v3` = bound v2 (by hash) plus statement 4; v2 is withdrawn before any use (scoped check). (D) 1,320 read-only probes at product `e3cd0bf5` (505 match, 815 fix owed); golden, replay controls, id moves, and what is not bound. | lead brief (FA2-CENSUS-E3); carrier plan `LC/f2min/census-rule-1b/PLAN.md` G1-G7; `LC/f2min/census-rule-1/QUESTIONS.md` item 12; LD-DEC-11 "Sentence owed" | erratum, adoption receipt | two (Claude, Codex) |

Owed: two reviews and the lead's adoption receipt. Then: the CENSUS-RULE-1a fix and golden for statement 4, the move of
the rule-id references to v3, the carrier units, the FA-2 contract successor stating E1-E3 with its `design-lock.json`
entry, and the one repackaging.
