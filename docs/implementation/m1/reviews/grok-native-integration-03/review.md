# Independent Grok review: native integration03 (S1 guard delta)

**Reviewer:** Grok (explicitly authorized). Codex remains implementation lead. Not Claude agreement.
**Subject:** `/tmp/opensip-implementation/m1-grok-native-integration-review-03/subject`
**Manifest SHA-256:** `b323785fcf3bdee525fb4b84e47d10250a6bf93f57176f10ab92023c7e95069a`
**Members:** 257
**Parent (native02):** `dce81624…6577` — Grok **ACCEPT WITHIN STATED INTEGRATION SCOPE** with should-fix S1. This freeze is the guard-only successor.
**Verdict:** **ACCEPT WITHIN STATED DELTA SCOPE**

Not product, source-promotion, native codec/admission, or milestone acceptance. Cargo and the 71-check reader were not rerun; they apply only to unchanged carrier/codec bytes.

## Delta

`closed_idl.py` now admits `{t:frame-payload, protocol}` only as the **direct payload member** of that protocol’s declared envelope (`frame_slot` and `origin == envelope`). Other placements refuse `IDL_PROTOCOL` at the IDL layer, before rendering.

This is not the 02-suggested origin→envelope cycle edge. That edge would be a self-loop on every valid envelope (the payload marker’s origin **is** the envelope; the protocol loop already expands actual payload alternatives). The slot check is the correct behavioral fix. Parent `closed_idl-native02.py` is byte-identical to native02 `closed_idl.py`.

Unchanged vs native02: `render.py` (`b1f3e371…88566`), `assemble_eight.py`, `assemble_ts.cjs`, `render_checked.py`, owner/meta/options pins, and all eight assembly files.

## Custody

Verified before and after. Work used only `review/copy` and `review/probes`. Frozen subject not written.

| Check | Result |
| --- | --- |
| Manifest | `b323785f…069a` |
| Files | 257 listed = 257 walk; extra/missing/mismatch none |
| Copy | `cp -a`; 257/257 exact |
| After | frozen hash and `closed_idl.py` unchanged |

## Seven guard groups

`check_closed_idl.py` in the copy: **7/7 pass**, including the new `test_frame_payload_markers_only_occupy_exact_envelope_slots` (non-envelope, hidden-nullable, protocol-payload, other-envelope-field → `IDL_PROTOCOL`). True `IDL_CYCLE` cases still refuse.

## Original S1 counterexample

Native02 independent probe: a non-envelope record field `{t:frame-payload}` plus envelope payload `{t:ref, ref:victim}`. Parent IDL **accepts**; combined renderer then refused `frame-payload outside declared envelope`.

On 03 standalone `IDL.admit`: **`IdlRefusal:IDL_PROTOCOL`**. Parent `closed_idl-native02.admit` still **accepts** the same tree. Combined admit also refuses at IDL. S1 closed at the IDL layer.

## Independent bypasses

`review/probes/independent_s1.py` → `review/results/independent-s1.json`. **19/19** after preserving attempt01 (three cases expected `IDL_PROTOCOL` but meta schema refused first as `IDL_SCHEMA`; not subject holes).

| Case | Result |
| --- | --- |
| Valid owner | still 68 native / 22 extern / 8 selectors; renderer runs |
| Original S1 shape | `IDL_PROTOCOL` (parent still accepts) |
| Self-ref / pair-ref | `IDL_CYCLE` |
| Non-envelope field, nullable wrap, protocol-frame marker, non-payload envelope field | `IDL_PROTOCOL` |
| Correct envelope, wrong protocol; Rust envelope + TS protocol | `IDL_PROTOCOL` |
| Variant member; array-wrapped marker on payload slot; select alternative | `IDL_PROTOCOL` |
| Scalar / alias / unknown protocol name | `IDL_SCHEMA` (grammar closes first) |

## Fresh eight-output equality

Unused labels `output-i` and `eight-i` in the copy:

- `output-i` `wire.rs` / `wire.ts` / `render-result.json` byte-identical to `output-c`
- `eight-i` **8/8** files byte-identical to copy `eight-e`, `eight-f`, `eight-h`, and native02 `eight-e`/`eight-f`

## S1 disposition

**Closed** by the envelope-slot rule, not by adding cycle-graph edges for `{t:frame-payload}`.

## Must-fix / should-fix

None in this delta freeze.

## Retained limits

Inert carriers only. No CBOR/admission/sender/host. Fixture inventory, browser bundler, package-manager, tooling-exception, and generation-source closure remain other tracks. Prior native02 compiler/reader/clippy evidence applies only to these exact output bytes.
