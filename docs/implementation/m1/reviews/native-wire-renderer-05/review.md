# Review 05: native inert carrier renderer, delta05

**Subject:** `/tmp/opensip-implementation/m1-native-wire-renderer-subject-05`
**Manifest SHA256:** `ecdbdb5fc5cb329c0938197010507e3a34ae05e878a22e5962d1272d957635c4` (24 files)
**Verdict:** **accepted within scope.** 0 required findings, 4 advisories.

Review04's RF-1 is fixed. One shared `SELECTOR_KEYS` table now governs both validation and render order, so the binding no longer depends on JSON member order. The binding is recorded in `render-result.json` and in Rust variant docs.

This acceptance covers only the inert Rust/TS carrier rendering algorithm over the pinned owner01 input. It is not approval of the native owner, codec, runtime, source selection or integration.

## Scope
- **In scope:**
  - The inert rendering algorithm over the declared owner01 input: 67 named types, 23 externs, 2 frame families.
  - Delta05's selector ordering, same-type refusal, mapping and tests.
  - Results carried from reviews 01 to 04 for byte-identical compiled code.
- **Relied on:** review03's Rust build (9 tests plus 2 compile-fail doctests), Clippy `-D warnings` and strict TS 6.0.3. The only Rust change since then is 8 doc-comment lines, and `wire.ts` is byte-identical to subject-04, so I did not rebuild.
- **Out of scope:**
  - Native owner semantics and source selection; no owner agreement is implied.
  - The final closed IDL profile and extern/name/alias-cycle/injection validation.
  - Generator closure, product integration and install.
  - The CBOR codec, canonical output, allocation and resource bounds.
  - Hand-written admission; runtime, performance, platform and release qualification.
  - Universal alias-equivalence of alternative types, which is explicitly not claimed.

## Integrity
- **Before and after:** the manifest hash, exact 24-file set, and every sha256 and size matched. All 11 pins still equal their origins.
- **Delta from subject-04:**
  - Changed: `render.py`, `test_render.py`, `UNIT.md`.
  - `wire.rs`: only 8 added `/// Host selector …` lines.
  - `render-result.json`: adds `selectorMappings`.
  - Unchanged: `wire.ts`, the Rust tests, the TS probes, the externs and the inputs.
- **Reproduction:**
  - A fresh render on my own copy gave byte-identical outputs.
  - 14 Python groups OK.
  - The re-serialized owner01 input renders identical bodies.

## Review04 items: status
| Item | Status |
|---|---|
| RF-1: variant identity depended on JSON order, and the selector key wasn't recorded | **Fixed** (evidence below) |
| A1: non-dict payload guards untested | **Fixed.** `None` and `[]` fixtures added |
| A2: TS positive assertion not protocol-specific | **Fixed.** The test isolates the `Ts2FrameV2` union and counts 2 rows |
| A3, A4 | Still open; `UNIT.md` discloses them as final integration duties |

## Evidence for RF-1
- **Order independence:** I ran `render.py` end to end with each of the 4 selection frames reversed individually, then all 4 together. Each run reversed both the alternatives' order and the `select`/`alternatives` member order. In all 5 runs, `wire.rs`, `wire.ts` and the `render-result` bodies were identical to the committed files.
- **Mapping consistency:** each of the 8 mapping rows matches its Rust `/// Host selector <mechanism> = <key>; not a wire tag.` line, which directly precedes `<variant>(Box<rustType>)`, and a matching frameType/payload row in the TS union.
- **Same-type refusals** (both protocols):
  - Identical declarations are refused, including extern declarations and declarations whose keys are reordered.
  - Different declarations that emit the same types are refused: the same ref with an extra key, the same extern with a different `schemaRef`, and `uint64` against `uint64` with `max`.
  - Alias-equal pairs are accepted, as disclosed (A3).
- **Mutations caught:** rendering in input order (E1), a swapped attribution key order (E2), and a wrong mapping key (E8).

## Advisories
- **A1: several regressions are caught only by manually comparing regenerated output.**
  - Swapping the host-phase key order (E3) passes all 14 Python groups.
  - Removing the Rust selector doc lines (E7) passes too.
  - The review04 D8 case (dropping Ts2 selection TS rows) behaves the same way.

  Each of these changes the committed generated files, which only reviewer or root byte comparison catches, and the ordering test pins mapping rows only for Ts2 FactBatch. Add an automated golden test comparing renderer output and `selectorMappings` with `generated/`, or assert all 8 rows and doc lines.
- **A2: the emitted-type refusal has no dedicated test.** Removing it (E5) passes, because the test uses identical declarations and those are refused earlier. The guard works on its own; add one case with different declarations that emit the same type.
- **A3: alias-equal alternatives are accepted, as disclosed.** For example `Ts2DigestHex` vs `Ts2Sha256Text` (both `String`), or enum `['a']` vs const `'a'`. Selector meaning is still recoverable from the fixed mapping and the Rust variant docs. The TS union can't tell such a pair apart, which fits the disclosure that TS doesn't carry host selection.
- **A4: carried integration duties.**
  - Selections outside frame payload positions raise `KeyError`.
  - Extern and name emission is unvalidated, and type objects are open.
  - Redundant nullability and payload self-envelope refs are accepted.
  - Codec callback and length duties remain.
  - Rust frame fields are uncorrelated, and derived tagged `Serialize` order isn't qualified.

## Mutations
| ID | Change | Result |
|---|---|---|
| E1 | render in input order | caught |
| E2 | swap attribution key order | caught; generated files differ |
| E3 | swap host-phase key order | **not caught** by the tests; generated files differ (A1) |
| E4 | remove the identical-declaration refusal | caught |
| E5 | remove the identical-emitted-type refusal | **not caught** (A2) |
| E6 | suppress mapping recording | inconclusive (my mutation was malformed); by reading, the test asserts 8 rows |
| E7 | remove Rust selector docs | **not caught** by the tests; `wire.rs` differs (A1) |
| E8 | wrong mapping key | caught; `render-result.json` differs |
| E9 | compare declarations without `sort_keys` | not a defect: the emitted-type check still refuses |

## Limitations
- Rust and TS were not rebuilt in this review. That rests on review03 plus confirming that the Rust delta is doc comments only and TS is byte-identical.
- Rebinding to a corrected native owner requires regenerating and reviewing the outputs again.
