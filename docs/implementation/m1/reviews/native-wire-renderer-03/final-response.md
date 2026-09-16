# Review 03 verdict: changes required (1 finding, 6 advisories), subject `dbb6f55d…c7e856`

Both review02 findings are fixed, and every guard mutation I tried is caught. One real gap remains: selection payloads are never shape-checked. I found nothing else in scope that should block acceptance. `review.json` (it parses) and `review.md` are in `m1-native-wire-renderer-review-03/`.

**Integrity and gates:**
- The 24 files matched their hashes and sizes before and after my work.
- All 11 input pins equal their origins (native owner01 plus the control01 externs).
- A fresh render gives identical `wire.rs`, `wire.ts` and `render-result.json`.
- Everything passes: 9 Rust tests plus 2 compile-fail doctests, Clippy with `-D warnings`, 12 Python tests, and strict tsc 6.0.3.

**Review02 findings:**
- **RF-1 (frame payloads):** the uint literals 2^64 and -1, a nested `frame-payload`, and const+enum are now refused both as a direct payload and inside a selection alternative.
- **RF-2 (duplicate keys):** removing the duplicate guard now fails the new test. That holds whether I delete it from `wire.rs` or from the `render.py` template and regenerate.
- **Advisories:** A3 to A5 are fixed and caught by mutations; A1 and A2 are now stated in `UNIT.md` as duties of the future codec.

**Mutations:** all 12 were caught. They covered both duplicate-guard variants, the frame-payload walk and location check, the uint domain, the enum, bool-const, sequence, variant-count and `memberOrder` checks, and both TS direction families. My review01 and review02 serde probes gave the same results as before: every wrong kind is refused and lawful kinds are accepted.

## Required finding
- **RF-1: selection payloads aren't shape-checked.** With `alternatives: {}`, the Ts2 `FactBatch` frame gets no TS union rows (and, reading the code, no Rust variant), even though the header and frame table still declare it. So a declared frame silently can't be represented.
  - One alternative, a missing or unknown `select`, and extra keys all render too.
  - The new Python test uses the key `selector` instead of the declared `select`, so nothing actually tests selection shape.
  - **Fix:** require exactly `{select, alternatives}`, a declared `select` value and exactly two alternatives. Correct the test key and add refusal tests.

## Advisories
- **A1:** extern `generatedType` values go straight into the Rust and TS output unchecked; a value like `Foo>); pub fn evil() {} //` lands in both files. Member and frame names aren't pattern-checked either. This is integration and closed-profile work, not a claim this unit makes.
- **A2:** type objects accept unknown keys; for example, the typo `enumm` silently renders an unconstrained `String`.
- **A3:** `nullable(nullable(T))` and `nullable(null)` are accepted even though they are redundant.
- **A4:** a frame payload can reference its own envelope record.
- **A5:** codec duties, restated.
- **A6:** limits already disclosed, plus a cosmetic probe variable name.

**Not verified:** I didn't compile or type-check the renders for RF-1 or the advisory cases. Those rest on what the renderer accepted and emitted, plus code reading. No CBOR crate was cached, so codec behaviour was modelled with hand-written serde deserializers. This request didn't restate the tsc path, so I reused review02's and confirmed it reports 6.0.3.
