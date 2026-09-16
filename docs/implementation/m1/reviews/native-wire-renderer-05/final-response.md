# Review 05 verdict: accepted within scope (0 required findings, 4 advisories), subject `ecdbdb5f…7635c4`

Review04's selector-order finding is fixed, and I found no required issues left in the inert rendering algorithm for the pinned owner01 input. This isn't approval of the native owner, codec, runtime, source selection or integration. `review.json` (it parses) and `review.md` are in `m1-native-wire-renderer-review-05/`.

**Integrity and reproduction:**
- The 24 files matched their hashes and all 11 input pins equalled their origins, before and after my work.
- A fresh render gives identical `wire.rs`, `wire.ts` and `render-result.json`, and the 14 Python groups pass.
- Since subject04, `wire.rs` gained only 8 `/// Host selector` doc lines, `render-result.json` gained the mapping, and `wire.ts` is unchanged.
- I didn't rebuild Rust or TS; that evidence comes from review03.

**Review04 finding (fixed):**
- **Order independence:** I reversed each of the four selection frames on its own, then all four together, reordering both the alternatives and `select`/`alternatives`. All five end-to-end renders matched the committed files exactly.
- **Mapping:** each of the 8 mapping rows matches its Rust doc line, the variant and type right after it, and a TS union row.
- **Same-type refusals:** these hold in both protocols:
  - Identical declarations are refused, including extern ones and ones with reordered keys.
  - Different declarations that produce the same Rust/TS types are refused, e.g. the same ref with an extra key, or the same extern with a different `schemaRef`.
- **Mutations caught:** rendering in input order, a swapped attribution key order, and a wrong mapping key.

## Advisories
- **A1:** some regressions are caught only by manually comparing regenerated output with the committed files; all 14 Python groups still pass:
  - swapping the host-phase key order
  - removing the Rust selector doc lines
  - review04's case of dropping Ts2 selection rows

  An automated golden test against `generated/`, or asserting all 8 mapping rows, would close this.
- **A2:** removing the same-emitted-type refusal passes all tests, because the test's identical declarations are refused by the earlier check. The guard itself works, but add a test with different declarations that emit the same type.
- **A3:** alternatives that are distinct aliases of the same underlying type (e.g. two `String` aliases) are accepted, as `UNIT.md` discloses. The fixed mapping and Rust docs still identify each selector.
- **A4:** carried items are all disclosed as final integration work:
  - `KeyError` for selections outside frame payloads
  - unvalidated extern names and member names
  - open type objects
  - codec duties

One of my mutations (suppressing the mapping rows) was malformed, so I've recorded it as inconclusive.
