# Review 03: native inert carrier renderer, delta03

**Subject:** `/tmp/opensip-implementation/m1-native-wire-renderer-subject-03`
**Manifest SHA256:** `dbb6f55dbc5453cbe8e83fcf80d2e000807310559ca8e570111395d69cc7e856` (24 files)
**Verdict:** **changes required.** 1 narrow finding, 6 advisories.

Review02's RF-1 and RF-2 are both fixed, and all 12 targeted guard mutations are caught. Generation reproduces identically and every gate passes. The one remaining algorithm issue is that selection payloads aren't shape-checked, so a malformed selection can silently drop a declared frame. Once that is fixed, I see nothing else in scope blocking acceptance.

## Scope
- **In scope:**
  - Generic inert Rust/TS rendering of the declared owner01 input: 67 named types, 23 externs, 2 frame families.
  - Renderer validation of the input grammar it actually supports.
  - The generated tagged readers and TS frame correlation.
  - Reproduction, gates, review01/02 probe reruns and mutations.
- **Out of scope:**
  - Native owner semantics (owner02/author03 work); no owner agreement is implied.
  - Admission of general malicious IDL, the final closed profile and meta validation, source selection, owner rebind, generator closure, and product integration.
  - A production CBOR codec, canonical output, length-before-allocation and host resource bounds.
  - Hand-written admission: bounds, consts, NFC, order, joins, commitments, state.
  - Performance, platform and release qualification.

## Integrity and pins
- **Before:** the manifest hash, exact 24-file set, and every sha256 and size matched.
- **After:** the manifest hash, exact 24-file set, and every sha256 and size still matched after all probes, mutations and writes.
- **Changes from subject-02:** `UNIT.md`, `generated/type-probes.ts`, `render.py`, `src/tests.rs`, `test_render.py`. The generated outputs are identical to subject-02.
- **Pins:** all 11 copies are byte-equal to their origins: native owner01 input and meta schema, plus control01 extern contracts and TS. Owner helpers were not run.

## Reproduction
| Gate | Result |
|---|---|
| fresh `render.py` on own copy | `wire.rs`, `wire.ts`, `render-result.json` byte-identical |
| `cargo test --locked --offline` | 9 passed, plus 2 compile-fail doctests |
| Clippy `--all-targets -D warnings` | clean |
| `python3 -B test_render.py` | 12 OK |
| tsc 6.0.3 strict (candidate-02 path, node v24.16.0) | exit 0 |

## Review02 items: status
| Item | Status |
|---|---|
| RF-1: frame payload positions not validated | **Fixed.** 2^64, -1, `frame-payload` and const+enum are refused both as a direct payload and as a selection alternative. Mutations C3, C9 and C10 are caught. |
| RF-2: duplicate guard untested | **Fixed.** Every member and tag of all 4 records is repeated, before and after, with tag-last controls. C1 (generated code) and C2 (source change plus regeneration) are caught. |
| A1: codec callbacks | **Resolved by disclosure.** `UNIT.md` now requires `visit_u64` and `visit_unit`, and `visit_none`/`visit_i64` are refused on purpose. |
| A2: allocation before kind check | **Resolved by disclosure.** It is the dedicated codec's duty; no allocation qualification is claimed. |
| A3: operator-shape acceptance | **Fixed.** C4 to C7 are caught. |
| A4: repeated `memberOrder` entry | **Fixed.** C8 is caught. |
| A5: host-to-worker direction untested | **Fixed.** Widening either direction family fails tsc (C11, C12). |

## Required finding
### RF-1: Selection payload shape is unchecked, so a malformed selection can silently drop or narrow a declared frame
Selection payloads get the scalar walk, but nothing checks their layout.
- **Empty alternatives:** with `alternatives: {}`, the Ts2 FactBatch frame renders zero variants (by code) and **0 TS union rows**. Yet the header enum and frame table still declare FactBatch, so a declared frame can't be represented. Delta02's frame-table binding exists to prevent exactly this mismatch.
- **Other malformed selections:** one alternative, a missing `select`, `select: "bogus"`, and extra keys on the selection object all render.
- **Test gap:** the new Python test builds selections with the key `selector` instead of the declared `select`. Its refusals come from the scalar walk, so no test checks selection shape.

**Required change:** treat a payload as a selection only when it has no `t` key and its keys are exactly `{select, alternatives}`. Require `select` to be one of the declared values and exactly two alternatives, each a type. Fix the test key and add refusal tests for 0, 1 and 3 alternatives, a missing or unknown `select`, and extra keys.

## Advisories
- **A1: Extern types and names go into code unvalidated.** The extern `generatedType` `Foo>); pub fn evil() {} //` is emitted verbatim into both `wire.rs` and `wire.ts`. A member name `a-b` renders as an invalid Rust identifier. These belong to integration: generator closure and the closed profile must validate them against the meta patterns and the actual export set. No malicious-IDL claim is made.
- **A2: Type objects aren't closed.**
  - A typo key `enumm` silently renders unconstrained `String`.
  - Unknown uint keys and bytes without min/max render.
  - Ts2 frame direction values go unchecked.
  - A non-string text const raises `TypeError` (still fails closed).
- **A3: Redundant nullability is accepted.** `nullable(nullable(T))` renders `Option<Option<T>>`, and `nullable(null)` renders `Option<()>`. Refuse or canonicalize these.
- **A4: A frame payload can reference its own envelope,** rendering `Box<Ts2FrameV2>`. Consider refusing that.
- **A5: Codec duties, restated.**
  - Tagged readers need `visit_u64` (or u8/u16/u32) and `visit_unit`, and accept `visit_char` as text.
  - Flat records rely on the codec honouring type hints.
  - Text and bytes length is unbounded until the codec exists.
- **A6: Carried limits.**
  - Rust frame fields are uncorrelated.
  - Derived tagged `Serialize` emits the tag first and is not qualified CBOR.
  - Consts are inert in Rust.
  - Cosmetic: the TS probe variable `seal` holds a `Rust3DependencySourceChunkV3`.

## Mutations (all caught)
| ID | Change | Caught by |
|---|---|---|
| C1 | remove 4 generated duplicate guards | duplicate test |
| C2 | remove the guard in the `render.py` template and regenerate | duplicate test |
| C3 | remove the frame payload walk | payload test |
| C4 | remove the enum validity check | payload test |
| C5 | remove the bool const check | payload test |
| C6 | remove the sequence type check | order/variant/sequence test |
| C7 | remove the two-variant check | same |
| C8 | remove the `memberOrder` duplicate check | same |
| C9 | disable the frame-payload location check | 2 tests |
| C10 | widen the uint64 domain | uint literal test |
| C11 | widen host-to-worker direction rows | tsc TS2578 |
| C12 | widen worker-to-host direction rows | tsc TS2578 |

## Independent probes
- **review01 serde probes:** same results as in review02. All tagged wrong kinds are refused whether or not the deserializer honours type hints. JSON duplicates, floats, negatives, overflow, `{}` and `[]` are refused.
- **review02 typed-callback probes:** same results. Lawful u64/u8/unit/char values, borrowed bytes and tag-last order are accepted. `visit_none`, `visit_i64`, newtype values, wrong kinds, duplicates, unknown keys and missing keys are refused.
- **review02 RF-1 cases:** all refused, both as a direct payload and as a selection alternative.
- **review03 grammar probes:**
  - The RF-1 selection cases and advisory cases A1 to A4 are accepted (these are the problems above).
  - A nested selection fails closed with `KeyError`.
  - Switching the discriminator to an existing member is refused.

## Limitations
- The RF-1 and advisory mutated renders were not compiled or type-checked. Those findings rest on renderer acceptance, the emitted text and code reading.
- No CBOR crate was cached, so codec callback behaviour was modelled with hand-written serde deserializers.
- The tsc path was reused from review02; I checked it reports version 6.0.3.
