# CODEX2 Review — D2b-3c r1

## Verdict

**REQUIRED-FINDINGS**

## Required findings

### D2B3C-R1-RF-1 — Correct the false TS2 aggregate-bound claim in the frozen scope

`SCOPE.md` states in LD-D2B3C-1 that the TS2 participant spools the admitted payloads “under its existing aggregate bound.” That bound does not exist. Accepted LD-D2B-8 explicitly records that TS2 has no aggregate response bound and adds none, while the actual `Spool::push` appends each payload to an unaccounted `Vec<Vec<u8>>`. The candidate correctly leaves that accepted behavior unchanged.

This is a blocking subject-description defect because the frozen scope claims a resource control that neither the accepted law nor the implementation provides. Produce an exact successor whose scope says that the individual frames remain subject to their applicable admission bounds, but the aggregate TS2 spool remains uncapped under LD-D2B-8. Do not add a product aggregate cap under this correction; that would require separate authority. Re-freeze and rehash the successor package, preserving the current source and evidence bytes if they are otherwise unchanged.

## Independent assessment

The frozen package otherwise reconciles cleanly. I independently rehashed the manifest (`df0c418d0ddb04038fb6e77d9b6f7aeb9f0f19262e369ff27e8134d16b8b2d08`), all 254 members, all 25 archived and live authority pins, and the exact 13-path product map. The map contains the declared eight existing and five new paths; each parent byte image matches pinned accepted main, and every candidate image matches both the live candidate and its frozen archive. The stage contains no undeclared member. The protected shared matcher, native-profile, registry, alias, carrier, and source-map inputs remain byte-identical to accepted main, and the two identity files remain exact to the accepted source preflight.

The implementation is consistent with the accepted D2b decisions I inspected. It binds the exact census token before disclosure, rejects request/response token mismatches in both directions, preserves the historical path, applies the Dempty join, keeps wire and relation depth accounting separate, validates census nullability, count, order, path membership, row extent, closed signature-token shape, scalar types, and byte bounds, and routes admitted raw census and entry payloads to H in receipt order. Over-bound responses become the typed event without assigning provider fault; clean terminal variants retain exact echoes. The tests exercise the material joins, including all commitment fields, both mismatch directions, boundary and one-over cases, malformed census rows, terminal handoff, signature-token decomposition, and the preservation of non-symbol behavior.

The final owning-r3-retry records exact-source success and nine compiled runtime mutation kills, followed by restoration of all 13 source files and a recompiled positive run. I did not count setup or compile failures as mutation evidence. The Trial07 evidence is correctly limited to a 353-vector raw corpus, a 352-vector selected-by-value corpus, 15 replayed TS2 families, and 16 other-owner families; it does not claim 352 TS2 executions. The deferred Rust3 float `0.0` vector remains byte-exact and assigned to D2b-4c. The public receipt bindings and four data pins remain current, with zero real blind runs.

This verdict identifies no product-code defect in the frozen candidate. It withholds unit acceptance because the scope is part of the reviewed subject and materially misstates the implemented and accepted resource boundary. The five-path additive inventory and direct current-meaning projection remain mandatory follow-on obligations. This review grants no integration, inventory acceptance, source39 registration, or whole-project qualification.
