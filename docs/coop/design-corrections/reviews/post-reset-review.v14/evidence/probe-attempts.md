# Retained probe attempts, including the ones that failed first

Independent probes are recorded here in the order they were actually run, so a probe that
only passed after I corrected *my own* construction is not presented as a first-pass result.
Entries are appended only after the attempt has actually been executed.

## p1_anchor_cardinality.py — attempt 1 (3 of 37 probes did not hold)

```
{"allHold": false, "n": 37,
 "failed": ["A1-the-closed-maximum-is-the-shared-schema-bound-not-absent",
            "A7-negative-unanchored-control-flow-refuses-under-typescript",
            "A7-negative-unanchored-literal-refuses-under-typescript"]}
```

Diagnosis of each, and which side the fault was on:

| Probe | Refusal seen | Fault |
|---|---|---|
| `A1` | `AttributeError: module 'idmodel' has no attribute 'SCHEMAS'` | **Mine.** The module global is `M.SCHEMA`, not `M.SCHEMAS`. Corrected the accessor; the underlying claim then held. |
| `A7` control-flow | `AdmissionError: FIXTURE_RELATION_UNKNOWN:control-flow` | **Neither — a constructor limit.** The candidate's own `relation_fixture` has no payload shape for `control-flow` or `literal`, so no complete Run can be built for them by this harness. This is not an admission result and is **not** counted as evidence either way. Recorded as a limitation. |
| `A7` literal | `AdmissionError: FIXTURE_RELATION_UNKNOWN:literal` | as above |

Attempt 2 (accessor corrected, the two unconstructible relations withdrawn rather than
counted as passes): 35/35 hold. `evidence/probe-cb4-must-1.json` is attempt 2.

## p1b_totality.py — attempt 1 (2 of 12 probes did not hold)

```
{"allHold": false, "n": 12,
 "failed": ["T8-negative-a-fact-matching-only-sourceUniverse-does-not-discharge-the-scope",
            "T8-negative-a-fact-matching-only-targetUniverse-does-not-discharge-the-scope"]}
```

Both refused with `AdmissionError: RELATION_UNIVERSE_RULE:same-only`, not with the
`COVERAGE_INVENTORY_TOTALITY_OMITS_PATH` I predicted.

**Neither a candidate defect nor a construction slip — an unreachable premise.** I was trying
to show that each of the two universe coordinates in `coverageTotality.matchOn` is
*independently* load-bearing, by moving exactly one of them. `file` carries
`universeRule: same-only`, so its `sourceUniverse` and `targetUniverse` cannot diverge at all;
the fact is refused by that prior law before totality is ever reached. The negative still
refuses, at the law that actually owns it.

Attempt 2 re-expresses the probe to assert what is true (refusal at `same-only`) and adds
`T8b` recording why the independence question is unreachable for this relation. 13/13 hold.
That leaves a bounded, stated limit: the two universe coordinates are verified **jointly**
load-bearing (T7), not individually.

## p2_native_cause.py — attempt 1 (8 of 15 probes did not hold)

All eight failed with `KeyError: 'entries'`. **Mine.** A `CoverageResultV3` payload carries a
single `entry` object, not an `entries` array; my accessor was wrong, so every mutation was a
no-op and the negatives never reached the law under test. The positive control `B6` passed in
attempt 1, which is what showed the fault was in my accessor rather than in admission.
Attempt 2 (accessor corrected): 15/15 hold, each negative refusing with its own distinct key
(`native.coverage-cause-without-deficiency`, `…-carrier-unsupported`, `…-not-for-deficiency`,
`…-required`, `…-relation-not-in-scope`).

## p2b_run_closure_cause.py — attempt 1 (1 of 7 probes did not hold)

```
{"allHold": false, "n": 7, "failed": ["B16-positive-RC-3-complete-with-incomplete-state-and-no-deficiency-is-lawful"]}
```

`AdmissionError: COVERAGE_PRODUCER_ADMISSION: RC-2: incomplete needs >=1 edge, complete stage
and exhaustive examination; else partial`.

**Mine.** I hand-mutated an entry to `state: incomplete` while leaving `unresolvedEdgeCount`
at 0. RC-2 correctly refused *my* malformed entry — this is the candidate rejecting a bad
construction, not a defect. The lawful RC-3 shape has to carry a real admitted
`unresolved-edge` fact, so attempt 2 builds it
(`build(relation="references", unresolved_edges=[...])`) instead of forging it. That build
yields `coverage: complete`, `state: incomplete`, `deficiency: null` and closes a Run — the
RC-3 positive control, natively produced.

## p2b_run_closure_cause.py — attempt 2 (2 of 9 did not hold)

Both **mine**: I invented an `UnresolvedEdgeKindV1` member that does not exist
(`dynamic-import-specifier`; the real one is `dynamic-import-nonliteral`), and my edit had
dropped the `relabelled` helper (`NameError`). Attempt 3: 9/9 hold.

## p3_body_language.py — attempts 1–3

- **Attempt 1** (1 of 14): `C4` required `bodyLanguageLaw` on every universe row. **Mine, and
  over-strict**: that key belongs to the two `closed-suffix-table` rows; the Rust row's law is
  its `dialect.selectionLaw` plus a single-member `bodyLanguages: ["rust"]`, which is coherent
  because Rust has exactly one body language. Relaxed to what is actually normative.
- **Attempt 2** (1 of 22): `C15` expected `BODY_LANGUAGE_GRAMMAR_VARIANT_UNKNOWN` from
  `build()` and got `FIXTURE_NO_ADMISSIBLE_PAYLOAD:clones` — the fixture *catches* the
  selector's refusal and degrades to a scope-only clones fixture. **A fixture behaviour, not
  the law's answer**, so the probe was redirected at the selector itself.
- **Attempt 3** (2 of 22): I called `CI.body_language_version`, which is check-identity's own
  fixture copy (`FIXTURE_SOURCE_VARIANT_UNKNOWN`), not the model's. **Mine.** Switched to
  `M.body_language_version`. Final: 22/22.

## p4_capability.py — attempts 1–3

- **Attempt 1** (2 of 16): `ValidationError: array order utf8: strict unique order required`.
  **Mine** — my synthetic release registry listed `languageModes` in matrix order, not sorted
  order. The refusal is the ordering law working on my malformed input.
- **Attempt 2** (same 2): `array order canonical-set` — the registry *rows* also need
  canonical order, not just the modes. **Mine.** Final: 16/16.

## p4b_capability_bounds.py — attempt 1 (4 of 18 did not hold)

| Probe | What happened | Fault |
|---|---|---|
| `E4`, `E8` | returned a non-empty list | **Mine.** `admit_release_capability_registry` / `admit_requested_capabilities` **admit by returning the rows** and refuse by raising; I asserted an empty fault list. |
| `E16` | `ValidationError: 'clones@normalized-body-hash' does not match '^[a-z][a-z0-9._:-]*(?![\s\S])'` | **Mine.** The `@` spelling is refused **by shape, before membership** — exactly what `capabilityIdLaw` says should happen, and an earlier refusal than the one I predicted. |
| `E12` | **closed a Run** (`run2:0c33087c…`) | **Mine, and the most important correction.** I assumed `has_match=False` under a syntax universe *was* the false-complete graph. It is not: the fixture honestly emits `coverage: unknown` / `language-tier-unsupported` / `capability-missing`, so closing is the **correct** outcome. Attempt 2 retains that as a positive control (`E12a`) and **forges** the false claim instead — `coverage: complete`, `deficiency: null` — which refuses with `SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE`, plus a relabelling case refusing with `SYNTAX_CAPABILITY_DEFICIENCY_MISMATCH`. |

Attempt 2: 20/20.

## p5_public_errors.py — attempt 1 (4 of 24 did not hold)

All four traced to one root cause: **mine.** I guessed the origin token spellings
(`user-configuration`, `external-supplied-spec`); the registry's actual `possibleOrigins` are
`external-configuration`, `externally-supplied-spec` and `host-generated-internal-layer`.
Notably `F3` (origin laundering) *passed* in attempt 1 only because my invented origin was
refused as impossible — a pass for the wrong reason, so attempt 2 re-aims it at a real origin
the key cannot have. Attempt 2 also adds `F6b` (one key, three origins, three distinct
answers). Final: 25/25.

## p6_d9.py — attempt 1 (3 of 15 did not hold)

**Mine.** `StepTermination.properties.faultCause` is a `$ref` to `#/$defs/D9FaultCause`;
I read the enum off the `$ref` stub, which has no `enum`. Re-pointed at the real definition.
Final: 15/15.

## p7_safeguards.py — attempts 1–3 (all faults mine)

- **Attempt 1** (3 of 20): `S3` used `M.identifier("analysis-spec", …)` — `analysis-spec` is
  not a registered *identity* domain (`IDENTITY_DOMAIN`); re-aimed at
  `N.validate_foundation`. `S5` was a forward reference (`NameError`). `S17` passed a tuple
  where `digest_sites` wants a string path.
- **Attempt 2** (1 of 21): my `S3b` positive control asserted `in (None, True)`;
  `validate_foundation` returns the validated record. Final: 21/21.

## p8_delivery.py — attempt 1 (1 of 5)

**Mine.** `H1` called `_codes` in a lambda that `probe()` evaluates immediately, before the
function was defined. Hoisted it. Final: 6/6, and the measured result is exactly
0 changed / 1 added fault-cause mapping.

## p4c_bounds.py — attempts 1–2

- **Attempt 1** failed to load: `KeyError: 'CapabilityAvailabilityStepV1'`. **Mine** — the
  availability records live in the *workflow* `common.schema.json`, not the native schema
  document.
- **Attempt 2** (2 of 10): `K6`/`K8` expected `release_absence_notices` /
  `invocation_availability` to **refuse** an oversized input. They do not — and, importantly,
  they do not truncate either: the 1025-notice step came back whole with `noticeCount: 1025`,
  which is the honest direction. The bound is held in two other places, so attempt 3 checks
  those instead of asserting a guard the helper never claimed:
  - **unreachable by construction** — `analysis-spec.requestedCapabilities` is itself capped
    at 1024 and one selection yields at most one absence per requested row, and `StepId` is
    0–63 so an invocation cannot exceed 64 steps;
  - **refused if forced** — validating the oversized step, the 65-step invocation and a
    `stepId: 64` record against the real schema each refuses, with a lawful record admitted
    as the positive control.

  Final: 15/15. Net finding: no silent truncation, counts exact at the edge, and the
  overflow cases are unreachable rather than merely unguarded.
