# Review 04: native inert carrier renderer, delta04

**Subject:** `/tmp/opensip-implementation/m1-native-wire-renderer-subject-04`
**Manifest SHA256:** `606639b214ca6cd25702319146faf4ced4510d967b3ee0e46b839f37e11671b5` (24 files)
**Verdict:** **changes required.** 1 narrow representation finding, 4 advisories.

Review03's RF-1 is fixed: selection shape is closed, and a declared frame can no longer silently disappear. The pinned owner01 input still renders byte-identically.

The remaining finding has been present since subject-01, and I missed it in earlier reviews. Generated selection variants are bound to alternatives by JSON member order, and no generated artifact records which admitted selector each variant belongs to.

## Scope
- **In scope:** the delta04 selection grammar validation and its tests; reproduction of generated outputs; how selection alternatives are represented in generated Rust/TS.
- **Relied on from review03:** Rust tests, Clippy and strict TS results. Nothing compiled changed (see Integrity), so I did not rebuild.
- **Out of scope:**
  - Native owner semantics, including which frames use which selection mechanism.
  - The final closed IDL profile and external reference/name/injection validation.
  - Source selection, generator closure and integration.
  - The codec, admission and resource bounds.
  - Platform, performance and release qualification.

## Integrity
- **Before and after:** the manifest hash, exact 24-file set, and every sha256 and size matched. All 11 pins still equal their origins (native owner01 input and meta schema; control01 extern contracts and TS).
- **Delta from subject-03:** only `render.py`, `test_render.py` and `UNIT.md` changed. All Rust/TS sources, probes, inputs and generated outputs are byte-identical.
- **Reproduction:** a fresh `render.py` run on my own copy produced identical `wire.rs`, `wire.ts` and `render-result.json`. `python3 -B test_render.py` passed 13 OK.

## Review03 RF-1: fixed
These were all refused with `ValueError`:
- empty, one or three alternatives
- missing or unknown `select`
- an extra key, or the `selector` typo key
- host-phase keys under the attribution mechanism
- list alternatives
- a string alternative, or a nested selection as an alternative
- `frame-payload` or uint 2^64 as an alternative
- a payload with both `t` and `select`
- a type object carrying a `selector` member
- a string or null payload

The negative fixture now uses the real `select` key. Mutations D1 to D5 are caught by the new test group.

## Required finding
### RF-1: Selection variant identity depends on JSON member order, and the selector key isn't recorded
`render.py` names selection variants by enumeration index: `pascal(frameType) + str(index)` over `alternatives.items()`.
- **Baseline output:** `FactBatch0(Box<Ts2FactBatchV1>)`, `FactBatch1(Box<Ts2FactBatchV3>)`, `Unavailable0/1`. No selector value (`false`/`true`, `WAIT_NATIVE_CONTEXT_VERIFIED`/`ANALYZING`) appears in `wire.rs`, `wire.ts` or `render-result.json`.
- **Reordering an equivalent input:** putting `true` before `false` renders fine, but variant 0 becomes the V3 alternative. JSON member order isn't semantically significant, yet it changes the binding.
- **Same-type alternatives:** these render too, and then the order-derived index is the only thing distinguishing them.
- **Test coverage:** the new positive test pins `FactBatch0` to V1, which itself relies on input order.

With today's pinned input the two types differ, so a hand-written M3 decoder is protected by type checking. But `UNIT.md` requires M3 to decode by frame tag *and* admitted host selector, so the carrier should bind selector to variant deterministically.

**Required change:** bind variants to the declared selector keys regardless of input order. Either:
- derive names from the key (`FactBatchFalse`/`FactBatchTrue`, `UnavailableWaitNativeContextVerified`/`UnavailableAnalyzing`), or
- iterate in the renderer's fixed per-mechanism key order and emit the selector key per variant, as a doc comment or a render-result mapping.

Also refuse, or explicitly disclose, same-type alternatives, and add a test that a reordered alternatives object produces identical output. The second option keeps current outputs byte-identical if the fixed order matches the pinned input.

## Advisories
- **A1: two new guards have no test.** Removing the non-dict payload check (D6) or the alternatives-must-be-a-map check (D7) still passes all 13 groups. Without them, the bad input still fails, but with `TypeError` rather than `ValueError`. Add string/null payload cases and a non-empty list of alternatives.
- **A2: the positive TS assertion isn't protocol-specific.** `"frameType": "FactBatch"` also matches Rust3 rows. Omitting only the Ts2 selection rows (D8) passes the Python tests and is caught only by comparing generated output. Assert on the `Ts2FrameV2` block's two rows instead.
- **A3: selections in non-frame positions fail with `KeyError('t')`.** A selection inside `nullable`, or used as a record member type, fails closed but outside the `ValueError` refusal contract.
- **A4: review03 advisories carried.** These cover unvalidated extern and name emission, unknown keys in type objects, redundant nullability, payload self-references to the envelope, codec duties, uncorrelated Rust frame fields, and derived `Serialize` order. `UNIT.md` now assigns closed-profile, name and injection validation to final integration.

## Mutations
| ID | Change | Result |
|---|---|---|
| D1 | drop the exact `{select, alternatives}` key check | caught |
| D2 | allow a subset of alternatives (the review03 regression) | caught |
| D3 | drop the `select` mechanism check | caught (error) |
| D4 | drop the alternative type-object check | caught (error) |
| D5 | drop the mixed type/selection refusal | caught |
| D6 | drop the non-dict payload check | **not caught** (A1) |
| D7 | drop the alternatives map-type check | **not caught** (A1) |
| D8 | omit Ts2 selection TS rows | caught only by comparing generated output (A2) |
| D9 | swap selection variant indices | caught; `wire.rs` also differs |

## Limitations
- Rust and TS were not rebuilt this round; that evidence comes from review03 on byte-identical files.
- If RF-1 is fixed by renaming variants, `wire.rs` changes, and the next delta needs a Rust/TS rebuild review.
