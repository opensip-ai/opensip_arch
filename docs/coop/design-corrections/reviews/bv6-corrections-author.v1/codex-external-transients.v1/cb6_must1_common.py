import io, re, pathlib

P = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v1/work/'
                 'docs/coop/design-corrections/workflows/schemas/common.schema.json')
s = P.read_text(encoding='utf-8')

OLD = '''    "D9Deficiency": {
      "type": "string",
      "enum": [
        "none",
        "required-relation-missing",
        "provider-unavailable",
        "language-tier-unsupported",
        "budget-exhausted",
        "confidence-floor-unmet",
        "convergence-exhausted",
        "baseline-recipe-unsupported",
        "verdict-indeterminate",
        "query-completeness-unmet"
      ]
    },
'''

D9_DESC = (
    "The HOST TERMINATION deficiency vocabulary of the D9 exit contract, carried by a whole "
    "Run, analysis result or comparison step: AnalysisResult.deficiency / .secondaryDeficiencies, "
    "ComparisonStepResult.d9Deficiency and comparison-result. It is NOT the per-requirement native "
    "sufficiency vocabulary, and the two are deliberately different sets. Three members "
    "(convergence-exhausted, baseline-recipe-unsupported, query-completeness-unmet) belong to "
    "evaluation, baseline and query outcomes that no per-requirement sufficiency evaluation can "
    "produce; `none` is the whole-Run `nothing was deficient` state, which a per-requirement record "
    "expresses by satisfied=true and the absence of the field. Four native sufficiency outcomes "
    "(derivation-policy-unmet, external-consumers-unknown, input-closure-incomplete, "
    "resolution-incomplete) have NO member here at all: they project outward as their own "
    "DomainDetailCode members and as the D9 class `indeterminate` (3) with the existing error code, "
    "per native-evidence.md section 10. Widening this enum to carry them was refused: it would put "
    "per-requirement causes into a whole-Run vocabulary and would change the D9 exit contract. Use "
    "#/$defs/NativeSufficiencyDeficiency wherever the value is one requirement's own outcome."
)

NEW = '''    "D9Deficiency": {
      "type": "string",
      "enum": [
        "none",
        "required-relation-missing",
        "provider-unavailable",
        "language-tier-unsupported",
        "budget-exhausted",
        "confidence-floor-unmet",
        "convergence-exhausted",
        "baseline-recipe-unsupported",
        "verdict-indeterminate",
        "query-completeness-unmet"
      ],
      "description": %s
    },
    "NativeSufficiencyDeficiency": {
      "type": "string",
      "enum": [
        "language-tier-unsupported",
        "provider-unavailable",
        "input-closure-incomplete",
        "budget-exhausted",
        "confidence-floor-unmet",
        "derivation-policy-unmet",
        "resolution-incomplete",
        "external-consumers-unknown",
        "required-relation-missing"
      ],
      "description": %s,
      "x-opensip-vocabulary": {
        "authority": "native/native-evidence.schemas.v2.json#/$defs/DeficiencyV2",
        "law": "native/native-evidence.schemas.v2.json#/x-opensip-deficiency-cause-registry/perRequirementConsumerBoundary",
        "producer": "native-evidence.md section 4.6 sufficiency_v2, per requirement",
        "admittedBy": "workflows_model.admit_evidence_requirement at the repair-preview producer/consumer boundary; enum parity re-checked cross-unit by check-integration.py",
        "note": "GENERATED/DRIFT-CHECKED: this enum is exactly DeficiencyV2 in DeficiencyV2's own declared member order, mirrored here because the workflows schema bundle resolves only urn:opensip:product-v1:workflows:* references and takes no cross-bundle $ref. It is the same closed vocabulary, not a workflows-owned successor: a member added or removed on either side is a drift failure, never a widening of this one."
      }
    },
''' % (
    __import__('json').dumps(D9_DESC),
    __import__('json').dumps(
        "The NATIVE PER-REQUIREMENT sufficiency outcome vocabulary: the exact nine members of "
        "DeficiencyV2, whose only defined producer is native-evidence.md section 4.6 "
        "`sufficiency_v2`, evaluated once per requirement. A record carrying one requirement's own "
        "outcome carries THIS vocabulary and never D9Deficiency, because four of these nine members "
        "have no D9Deficiency preimage and the D9-mapped value for all four is the same "
        "`verdict-indeterminate`, which would collapse exactly the distinction native-evidence.md "
        "section 10 preserves per row - including `resolution-incomplete`, the outcome section 4.6 "
        "step 6 mandates for a universal negative under unresolvedEdgePolicy=forbid over an "
        "affected target, and the outcome a destructive unused-code repair recipe turns on. This "
        "record-level vocabulary is orthogonal to two other things and replaces neither: the PUBLIC "
        "D9 TERMINATION of the Run that carries the requirement (still #/$defs/D9Deficiency and the "
        "section 10 class/code columns), and the retained CAUSE CARRIER of the Coverage entry the "
        "outcome was read from (still entry.nativeCause or the named structured carrier, per the "
        "native deficiency-cause registry). `none` is deliberately absent: a satisfied requirement "
        "is satisfied=true with the field omitted, which is what sufficiency_v2 returns."
    ),
)

assert s.count(OLD) == 1, s.count(OLD)
P.write_text(s.replace(OLD, NEW), encoding='utf-8')
print('ok')
