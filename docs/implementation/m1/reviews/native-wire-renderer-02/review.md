# Review 02: native inert carrier renderer, delta02

**Subject:** `/tmp/opensip-implementation/m1-native-wire-renderer-subject-02`
**Manifest SHA256:** `545492bceff46d01b6176ccc9b537ee9d5d86ec48f4730450a87e74916a6e04b` (24 files)
**Verdict:** **changes required.** 2 required findings, 6 advisories.

Both review01 required findings are fixed and independently confirmed. The two new required findings are small. One is a gap in a claimed validation check; the other is a missing test.

## Scope
- **In scope:**
  - Generic inert Rust/TS rendering of the declared owner01 input: 67 named types, 23 externs, 2 frame families.
  - The four manual generated tagged-record readers.
  - The renderer's layout and name checks.
  - TS frame correlation probes.
  - Reproduction of outputs and test gates.
- **Out of scope:**
  - Native owner semantics (owner02 findings are pending with author03). No owner agreement is implied.
  - Source selection, owner rebind, the closed IDL profile, full tool closure, and product integration.
  - A production CBOR codec, canonical output, host resource bounds, and hand-written admission (bounds, consts, NFC, order, joins, commitments, state).
  - Performance, platform and release qualification.

## Integrity and reproduction
- **File set:** before and after the work, the manifest hash, exact 24-file set, and every sha256 and size matched. Subject-01 is also unchanged.
- **Delta from subject-01:** `UNIT.md`, `generated/type-probes.ts`, `generated/wire.rs`, `render.py`, `src/tests.rs`, `test_render.py`.
- **Input pins:** all 11 copies are byte-equal to their origins. Owner helpers were not run.
- **Fresh render:** a run on my own copy reproduced `wire.rs`, `wire.ts` and `render-result.json` byte-for-byte.
- **Gates:**
  - `cargo test --locked --offline`: 8 passed, plus 2 compile-fail doctests.
  - Clippy `--all-targets -D warnings`: clean.
  - Python `-B test_render.py`: 10 OK.
  - tsc 6.0.3 strict: exit 0.
  - All runs used my own `TMPDIR` and `CARGO_TARGET_DIR`.

## Review01 findings: status
| Finding | Status | Evidence |
|---|---|---|
| RF-1: `{}` accepted as required null in tagged records | Fixed | `{}` and `[]` refused at every tagged null position; the map-as-null mutation is caught |
| RF-2a: text, key and tag kind lost in tagged records | Fixed | review01 loose and strict probes: bstr text, bstr or u64 tag, bstr or u64-index keys all refused |
| RF-2b: vacuous TS wrong-direction probe | Fixed for one direction | widening worker-to-host is caught; widening host-to-worker is not (A5) |

## Required findings
### RF-1: Layout validation skips frame payload type positions
`validate_layout` only walks the `scalars` and `records` tables. `kind()` still renders `protocols[*].frames[*].payload` and its selection alternatives, but nothing validates them. So two claims in `UNIT.md` don't hold for frame payloads: that `frame-payload` is confined to its envelope position, and that out-of-domain uint64 literals are refused.

The renderer accepted each of these without error:
- Payload `uint64 const "18446744073709551616"`: `wire.ts` contains `18446744073709551616n`.
- Payload `uint64 const "-1"`: `wire.ts` contains `-1n`.
- Payload `frame-payload`: `wire.rs` contains `Hello(Box<Ts2FrameV2Payload>)`.
- A FactBatch alternative with both text `const` and `enum`: the enum silently wins.

**Required change:** walk frame payloads and alternatives with the same checks, never allow `frame-payload` there, and add Python refusal tests.

*Not verified:* I did not compile or run tsc on these mutated renders, because the tool permission was denied.

### RF-2: The duplicate-member guard has no test
The generated guard works. On an unmodified copy, JSON and typed probes refuse both duplicate members and duplicate tags. But removing all 4 guards still passes 8/8 tests and 2/2 doctests. Without a test, a regression to silent last-wins overwrite would go unnoticed.

**Required change:** add Rust tests for a duplicate member and a duplicate discriminator (including tag-last order), and confirm the guard-removal mutation fails them.

## Advisories
- **A1: Tagged readers refuse some lawful serde callbacks.** Null delivered via `visit_none` or `visit_some(unit)` is refused, and unsigned 5 delivered via `visit_i64` is refused. Flat serde types accept `visit_i64(5)`. This fails closed, but some codecs could have lawful values refused. Either map these callbacks, or state the exact required callbacks as a codec duty.
- **A2: Allocation happens before the kind check.** Each text or bytes value is fully allocated before its declared kind is checked, and unknown keys are allocated before refusal. At most 7 values are held, but their length is unbounded until the codec's length-before-allocation checks exist. A per-member `DeserializeSeed` would check the kind before allocating.
- **A3: Some operator shapes are still accepted.**
  - `enum: []` renders as unconstrained `String`, a silent widening.
  - A bool `const: "yes"` renders the TS literal `"yes"`.
  - A single-variant record renders.
  - The envelope `sequence` member's type is unchecked.
- **A4: Duplicate entries in `memberOrder` aren't refused.** A repeated discriminator renders a duplicate match arm and an extra value slot. Refuse repeated names. The compile and Clippy effect was not verified.
- **A5: The TS direction check covers only worker-to-host.** Add a symmetric host-to-worker negative with a valid payload. The generated TS itself is correct.
- **A6: Carried limits, already disclosed in `UNIT.md`.**
  - The Rust frame struct's tag, direction and payload fields are independent of each other.
  - Derived tagged `Serialize` emits the tag first even when `memberOrder` puts it later, and it is not qualified CBOR.
  - Flat serde records depend on the codec honouring type hints: a non-hinting deserializer still gets bstr accepted as `String` and bstr or u64-index keys accepted.
  - Consts stay inert in Rust.

## Mutations
| ID | Change | Result |
|---|---|---|
| M1 | remove duplicate guard | **not caught** (RF-2) |
| M2 | map read as null | caught |
| M3 | bytes or u64 map keys accepted | caught |
| M4 | `false` read as null | caught |
| M5 | UTF-8 bytes read as text | caught |
| M6 | widen worker-to-host direction rows | caught |
| M7 | widen host-to-worker direction rows | **not caught** (A5) |

## Independent probes
- **review01 probes rerun:**
  - All tagged wrong-kind cases are refused; the baselines are accepted.
  - `probes2` panicked on its own `unwrap` of the `{}` input, which is now refused. That is expected after the fix.
- **Typed callback probes (`probes3`):**
  - Accepted: tag-last input with borrowed bytes, uint via `visit_u8`, text via `visit_char`.
  - Refused: newtype text, u64 as bool, empty seq as null, a u64, char or unknown tag, missing null, missing tag, and unknown keys.
  - The flat `visit_none` comparison was inconclusive: my probe deserializer lacked enum support.
- **Renderer probes:**
  - Refused as expected: nullable or record-ref variant members, a discriminator missing from `memberOrder`, inconsistent bounds.
  - `main()` refuses duplicate input keys, floats and NaN.
- **Grammar stress:** a variant record combining a keyword discriminator `type`, quoted tag `a"b`, tag `self`, enum and const text, a bytes alias, null, and bool/uint consts.
  - It renders, passes tsc and Clippy `-D warnings`, and decodes correctly from JSON and typed input.
  - An undeclared enum value and wrong-kind bytes are refused.

## Manual reader assessment
- **Field completeness:** every non-discriminator member is assigned in every variant, and dispatch is on the exact text tag. No field or correlation loss was found.
- **Duplicates:** duplicate keys are refused (the test gap is RF-2), and duplicate snake-case names are refused at generation. Duplicate `memberOrder` entries are not refused (A4).
- **Grammar:** the current input is all scalar members, and complex members are refused at generation.

## Limitations
- The compile, tsc and Clippy runs for the RF-1 and A4 mutated renders were not executed, because tool permission was denied.
- No CBOR crate was cached, so codec callback behaviour was modelled with hand-written serde deserializers.
