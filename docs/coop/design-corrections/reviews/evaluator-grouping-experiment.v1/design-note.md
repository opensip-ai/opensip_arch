# Configuration occurrences and empty-population uncertainty

Codex working proposal, September 8, 2026. This is a bounded design experiment
pending Grok assessment and integration into the corrected evaluator contract.
It is not accepted product source, schema admission, a complete replay verifier,
or evidence that OpenSIP is ready for implementation.

## Proposed choice

Keep each configuration's finding as an evidence-bearing occurrence. Group only
the baseline projection by stable logical fingerprint. This preserves different
parameters and citations without choosing a representative occurrence or placing
volatile universe identities in a stable fingerprint. An occurrence is evaluated
against its own universe and subject. Its existence does not establish another
universe's completeness.

The baseline group must agree on every field in the existing `BaselineEntry`:
fingerprint, ruleId, detectorId, stabilityClass, subjectPath, waived, and both
presence and value of optional legacyFingerprint. A disagreement refuses this
projection; neither encounter order nor a permissive merge chooses the answer.
The logical baseline contains one entry per group, sorted by fingerprint. Exact
duplicate evaluation occurrences are refused upstream rather than counted twice.

Distinct declaration ambiguity is a separate admission/correspondence question.
Grouping assumes each member has independently established the same logical
subject key. It cannot manufacture correspondence from a shared path or a string
that merely resembles a fingerprint. Its counterpart in the eventual normative
design must compare the complete recomputed fingerprint descriptor as well as
its digest, and obey the existing anonymous/signature ambiguity law.

Messages, parameters and evidence references may differ across configurations;
they remain on their original occurrence. They are not baseline fields. Their
full content must be replayed and compared. The experiment demonstrates four
same-count mutations that change this retained projection. It does not validate
their underlying fact, witness or native closure, and is not complete Run replay.

## Unknown enumeration remains visible with zero findings

Every enabled rule needs a retained enumeration outcome even if it selects zero
known subjects. A complete empty population is distinct from an unavailable
population and from otherwise-eligible symbols with unknown export membership.
The eventual typed record must retain enough authoritative inputs to recompute
that distinction. A bare producer assertion of `complete` is insufficient.

Known eligible subjects still evaluate when other candidates are unresolved.
A known live gating finding yields fail; otherwise unresolved required selection
yields indeterminate; otherwise pass. Waiving a known finding does not satisfy
unknown export membership or missing required execution coverage. Advisory
selection uncertainty stays disclosed. Required execution obligations survive
a policy composed entirely of advisory rules. Operational failures have their
existing outer precedence and are not inputs to this three-valued composition.

The probe accepts effective gating and emitted findings as explicit hypothetical
inputs. It does not decide severity thresholds, policy enablement, imports,
waiver resolution or native sufficiency. Those remain the pending evaluator's
other laws, and the experiment must not be used as an alternative specification.

## Existing contracts this must extend coherently

All paths below are relative to frozen21; the source manifest is
`360c2758c0409ebc307966c7a385c385c2d7f580b4623dd760b7ba0e26bf18c1`.

- `docs/coop/design-corrections/workflows/schemas/baseline-artifact.schema.json`
  `#/$defs/BaselineEntry` and
  `#/$defs/BaselineDescriptor/properties/entries`: complete entry fields and
  strict unique fingerprint ordering.
- `docs/coop/design-corrections/workflows/schemas/comparison-result.schema.json`
  `#/$defs/RuleDeficiency` and `#/$defs/RuleCoverage`: existing comparison-side
  carriers independent of finding existence. These do not alone fill the missing
  retained evaluator proof record.
- `docs/v2/contracts/product-v1/workflows-and-surfaces.md` §§3–5: audit-profile
  gate semantics, independent required-evidence deficiencies and explicit waiver
  targets. Code-regression still uses baseline-or-current policy and does not let
  a waiver added in the change hide a new code regression.
- `docs/coop/design-corrections/foundation/identity-schemas.v2.json`
  `#/$defs/proof-bundle`, `#/$defs/finding`, `#/$defs/finding-fingerprint`: current
  retained proof, finding and stable correspondence shapes.

## Still required

Grok's concrete GR1/GR2 refinement must settle where the enumeration record is
retained and bound, the exact schema/identity changes, and presentation rules for
occurrence versus logical counts. GR3 must provide the complete expected
population and provider-selection obligation so omitted inventories cannot look
like a complete empty population. GR4–GR8 and G3–G9 still govern source language,
subject metadata, scope/atom binding, imported witnesses, coverage, identifiers,
waivers and verdict composition. No full-schema or semantic acceptance follows
from the probe's passing cases.
