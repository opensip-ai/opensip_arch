# Capability-totality reference selection v1 — scoped design-unit review

**Verdict: `ACCEPT-DESIGN-UNIT`**

Not Rust/CVE1-codec/NFC-dependency/runtime selection. Not native context, universe, compiler Run, or complete replay. Not M2 complete. Frozen/live/history not edited. Activation still needs root assent after this review.

Subject `docs/implementation/m2/capability-totality-reference-selection-v1-subject.json` SHA-256 `9b4a4a67938fcb3b6c1e16b42117a1c8c4a9c29f86600ca6216d2fa27ce6a7aa` (2823 bytes, **12/12** files). Successor `…/successor.json` 3596 bytes SHA-256 `6421e727f91c5635c29d0182f9dd105e4002462e1e10a9a6fcb46bdb650df064`. Candidates (11) are sorted unique and equal the subject minus the successor record. Parents (4) sorted unique and pin-match: capability-manifest-domains.v2, historical `native_evidence_model.v2.py` `7d1c0acf…b8be`, exact-profile canonical `ad88e58f…96f7`, recognition-derived successor `4b771e6e…4711` (selected identity model `619d6e3c…41e6`). `passageOverrides: []`. Unit directory has no extra or missing files.

Archived advisory `docs/implementation/m2/reviews/grok-capability-totality-01/report.json` `b0c4ff34…40d1` / 3856 bytes is the pinned soundness read (`evidence/advisory-pins.json`).

## What changed

One function, `admit_capability_manifest`, implementing the **existing** type-before-content / total-refusal law (no passage override):

- non-map CVE1 root reaches existing `capability.adm-closed:CapabilityManifestV1` before `.get`
- `strict_unique` does not sort/hash once any ordered-collection element is not a string (type already recorded at `[]`)
- `AbsentCapability.relationIds[]` string type before set membership / domain

Historical `docs/coop/design-corrections/native/native_evidence_model.v2.py` is **untouched**. The new current native-reference is this unit’s `reference/native_evidence_model.py` (`e6784aa1…e2b9`). Later compositions must overlay that file with selected identity `619d6e3c…`, current native schemas/domains, and exact canonical `ad88e58f…`. HERE-relative imports in old artifacts are not rewritten.

## Bounded checks (portable `--architecture`)

Independent run of frozen `evidence/check-totality.py --architecture $ARCH` (actual extracted functions/constants, selected canonical `AdmissionError`, unchanged domain registry): **8/8**, byte-equal to `evidence/bounded-result.json`.

| Check | Independent |
| --- | --- |
| only-one-function-AST-delta (remainder AST) | pass |
| CVE1 encode/decode/read + identity recipe source-identical | pass |
| 666 structured results + predecessor **exception types** | pass |
| 278 original exceptions preserved as exceptions | pass |
| 278 → structured REFUSE; 0 candidate exceptions | pass |
| existing structured ADMIT/REFUSE class unchanged | pass (388/388 non-exception rows) |
| golden id `508f24c7…8881b` unchanged | pass |
| changed diagnostics | 296 |

Top-level `FunctionDef`+`ClassDef`: 144 names; **143** other than `admit_capability_manifest` unchanged (140 other functions + 3 classes). README’s “143 other top-level functions” matches that callable/class remainder, not 140 FunctionDefs alone.

Type gate skips order when any element is non-string (300 mixed-type refusals in the corpus have no accompanying `adm-order`). All-string order faults remain (6 `adm-order` rows without `[]` type faults). Checker-account: predecessor **messages** can reverse operand names across process hash order; portable gate compares exception **type** plus exact candidate structured JSON. Initial checker (`check-totality.initial.py`) is retained as evidence of that correction, not as the portable gate.

## Scope limits honored

- No CVE1 codec change; encode/decode/read bytes identical.
- No OPEN domains invented: admit still has no `adm-domain` for schemaVersion, providerId, language, or profile. Parent `declaredOPEN` keys unchanged. Profile remains OPEN as a registry; DL-CUST-3 release ProfileEntry custody is separate and still mandatory.
- Platform-domain membership still grants no selected platform support.
- No native context, universe, Run, or complete replay claim. Checker sets `fullRunTested: false`, `runtimeSelected: false`.
- Root’s private 774 Rust comparisons are **not** this unit and are not selected.
- Unicode/NFC identity dependency work is a separate lane.

## requiredFindings

None.

## shouldFix

None that block this unit. Portable gate is `check-totality.py --architecture`.
