# Independent Grok review: native/current-generator/report-codec integration02

**Reviewer:** Grok (authorized). Codex remains lead. Not Claude agreement.
**Subject:** `/tmp/opensip-implementation/m1-grok-native-integration-review-02/subject`
**Manifest SHA-256:** `dce81624e5459fdb4b30b8c7bdd3c38616cdae335b31c84c7b45f45557c76577`
**Entries:** 232
**Verdict:** **ACCEPT WITHIN STATED INTEGRATION SCOPE**

This is inert carrier integration, not native CBOR/admission, sender, product install, source-bridge promotion, milestone, or release. Native07 Grok acceptance covers the owner IDL bytes, not this guard or adapter. Renderer05 Claude acceptance covers unchanged `render.py` only (`b1f3e371…88566`, 27926 bytes, exact pin match).

## Custody

Verified before work and after. 232/232, no extras, missing, mismatches, or symlinks.

Pins checked: native07 wire-carriers + meta; generation02 options, TS projection, render-types, 140 compiler files/Node; codec02 output04 eight files; formatter binary `76cc5946…aca7`. Observed reproduction, not hermetic bootstrap.

Work used `review/copy` and `review/probes` only. Historical `save_checkpoint` scripts were not run.

## Author groups reproduced (copy)

| Run | Result |
| --- | --- |
| `check_closed_idl.py` | **6/6** groups, 0.663s |
| `test_render_current.py` | **14/14** groups, 0.071s |
| `render_checked.py output-g` | 68 native / 22 extern; `wire.rs`/`wire.ts`/`render-result.json` **byte-identical** to `output-c` |
| `assemble_eight.py eight-g` | 8 outputs, **byte-identical** to eight-e and eight-f |
| `tsc --project integrated02/tsconfig.json --rootDir generated --noEmit` | exit 0 (compile02 TS5011 preserved; compile03/rootDir correction holds) |
| Adapted `check_combined02.cjs` on freshly emitted `compiled-g/wire.js` | **71/71** (64 current cases, 4,202,613-byte dense exact round-trip, default 4MiB envelope `BYTE_LIMIT`, unselected/stale inventory+profile refusal) |

Seven of eight outputs match native01/codec02 Rust+provider TS. Only `report.ts` grows (2,140,727 → 2,166,673) by appending inert native types. All six current Rust files match native01 compiled bytes; Cargo tests were not rebuilt.

## Independent executable counterexamples

**Closed IDL + renderer** (`independent-guard.py`, 10/10):

- Unknown `int32` → `IDL_SCHEMA`; unselected extern → `IDL_EXTERN`; duplicate generated typeName → `IDL_EXTERN_REGISTRY`; duplicate native name → `IDL_NAME`; nullable self-ref → `IDL_CYCLE`; same-emitted selector uint64 alternatives → renderer refusal; widening FrameV2 header to text → `protocol major header differs`.
- Combined `admit`+render refuses a non-envelope `frame-payload` field (`frame-payload outside declared envelope`).
- **Layering:** `closed_idl.admit` alone **accepts** that shape (no frame-payload field edges in the cycle graph). Renderer then refuses. Not a silent combined accept.

**TS assembly joins** (`independent_assembly.cjs`, 5/5):

- Baseline 30 provider native / 12 external / 70 report native.
- Native type named `Baseline2Root` (already in report.ts) → `native name collision`.
- Duplicate `Ts2…` declaration → `duplicate native declaration`.
- `Ts2OrphanProbe = Ts2DoesNotExist` → `unresolved native type`.
- Adapter rejects non-type/interface statements, so appended native code cannot introduce executable parsers that shadow `parseReportExact`. Fresh 71 reader checks still pass on the combined `report.ts`.

## Clippy `infallible_try_from`

Preserved `clippy-integrated01` fails on typify `TryFrom` aliases in **generated** `invocation.rs`. `integrated/extern-contracts/src/lib.rs` allows `clippy::infallible_try_from` only on `pub mod generated`, with handwritten code still under `-D warnings`. That is appropriate for preserving typify’s generated API on this inert carrier. It is not runtime validation and must not migrate onto handwritten modules.

## Should-fix

**S1. `closed_idl.py` does not add graph edges for `{t: frame-payload}` fields.** Protocol-loop visits of envelope payloads still catch envelope↔payload ref cycles (author `cycle-frame`). A non-envelope record field of `frame-payload` is currently accepted by IDL and refused later by renderer layout. Add the implicit edge (origin → protocol envelope or payload types) so IDL_CYCLE matches the documented “cycles through implicit frame payload edges” without relying on renderer layout.

## Advisories / pending (not claimed complete)

- Source-only isolation, loader confinement, reproducible bootstrap, final source/inventory selection.
- No bounded CBOR parser, semantic admission, sender, or host/report behavior.
- Report profile 27,829,365 / depth 39 is the codec02 reader; default envelope remains 4MiB / 32. Those bounds are separate.
- `check_integration.py` still goldens native01 `eight-c`/`integrated/`; current bytes are `eight-e`/`eight-f`/`integrated02`.
- Formatter is an observed local binary pin, not a hermetic bootstrap.

## Commands

Python `-I -B` from `review/copy`. Node 24.16.0 pinned.

1. 232-file hash verify + pin verify
2. `check_closed_idl.py`, `test_render_current.py`
3. Independent guard + assembly probes
4. `render_checked.py output-g`, `assemble_eight.py eight-g`
5. `tsc --rootDir generated --noEmit` on `integrated02`; emit to `results/compiled-g`
6. Adapted combined-reader 71 checks
7. Completion freeze re-hash

## Verdict restated

**ACCEPT WITHIN STATED INTEGRATION SCOPE.** New closed-IDL guard and TS/Rust assembly joins hold under independent counterexamples; renderer05 `render.py` is unchanged; native07 owner bytes are inputs, not an automatic pass of this adapter. Combined profile6 reader still enforces the default 4MiB envelope. S1 is a justified IDL-graph should-fix, not a silent accept of recursive carriers. Not product, source promotion, or Claude agreement.
