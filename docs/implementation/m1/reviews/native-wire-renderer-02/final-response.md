# Review 02 verdict: changes required (2 findings, 6 advisories), subject `545492bc…6e04b`

Both review01 findings are fixed, and I confirmed that on my own copy. The two new findings are small: one validation check is incomplete, and one guard has no test. I wrote `review.json` (it parses) and `review.md` to `m1-native-wire-renderer-review-02/`.

**Integrity and gates:**
- The 24 files matched their hashes and sizes before and after my work; subject-01 is also unchanged.
- All 11 input pins match their origins, and a fresh render gives identical `wire.rs`, `wire.ts` and `render-result.json`.
- Everything passes: 8 Rust tests plus 2 compile-fail doctests, Clippy with `-D warnings`, 10 Python groups, and strict tsc 6.0.3.

**Review01 findings:**
- **Required null and value kinds:** tagged records now refuse `{}` and `[]` as null. They also refuse byte strings as text or tag, integer tags, and byte-string or integer keys. My review01 probes confirm this whether or not the deserializer honours type hints, and lawful values are still accepted.
- **TS direction probe:** it now catches widening of the worker-to-host rows.

## Required findings
- **RF-1: frame payload types aren't validated.** `validate_layout` checks only the `scalars` and `records` tables. `UNIT.md` says `frame-payload` stays in its envelope position and out-of-range uint64 literals are refused, but inside frame payloads neither holds. The renderer accepted all of these without error:
  - A uint const of 2^64, emitted as `18446744073709551616n`, and a const of `-1`, emitted as `-1n`.
  - A `frame-payload` used as a payload, emitted as `Hello(Box<Ts2FrameV2Payload>)`.
  - A selector alternative with both `const` and `enum`, where the enum silently wins.
  - **Fix:** apply the same checks to frame payloads and selector alternatives, and add Python refusal tests.
- **RF-2: the duplicate-key guard has no test.** The guard works: duplicate members and duplicate tags are refused. But removing all 4 guards still passes every Rust test, so a regression to silent last-wins overwrite would go unnoticed.
  - **Fix:** add tests for duplicate member and duplicate tag, including with the tag last.

## Advisories
- **A1:** the tagged readers refuse lawful null sent through `visit_none` and a lawful unsigned value sent through `visit_i64`, which flat types accept. This fails safe, but either accept these callbacks or state them as a codec duty.
- **A2:** each member's text or bytes is fully allocated before its kind is checked. At most 7 values are held, but their length isn't bounded yet.
- **A3:** `enum: []` silently renders as plain `String`; a non-boolean bool const, single-variant records and the envelope `sequence` type also go unchecked.
- **A4:** a name repeated in `memberOrder` isn't refused and renders a duplicate match arm.
- **A5:** widening the host-to-worker direction rows in TS is still undetected; the generated TS itself is correct.
- **A6:** limits already disclosed in `UNIT.md`:
  - Rust frame fields aren't tied to each other.
  - Derived `Serialize` puts the tag first and isn't qualified CBOR.
  - Flat records rely on the codec honouring type hints.
  - Consts are not enforced in Rust.

## Other evidence
- **Stress render:** I built a tagged record with a keyword discriminator `type`, a quoted tag `a"b`, a `self` tag, enum and const text, a bytes alias, null, and bool/uint consts. It renders, passes tsc and Clippy, decodes correctly, and refuses bad kinds.
- **Mutations:** 5 of 7 were caught; the two misses are RF-2 and A5.

**Not verified:** my compile and tsc run on the RF-1 and A4 mutated renders was blocked by tool permissions. Those two points rest on what the renderer accepted and emitted. No CBOR crate was cached, so I modelled codec behaviour with hand-written serde deserializers. I wrote only inside `review-02/`.
