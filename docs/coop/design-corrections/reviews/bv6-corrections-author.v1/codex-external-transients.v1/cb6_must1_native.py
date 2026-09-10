import json, pathlib, collections

P = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v1/work/'
                 'docs/coop/design-corrections/native/native-evidence.schemas.v2.json')
raw = P.read_text(encoding='utf-8')
d = json.loads(raw, object_pairs_hook=collections.OrderedDict)

reg = d['x-opensip-deficiency-cause-registry']
assert 'perRequirementConsumerBoundary' not in reg

block = collections.OrderedDict()
block['standing'] = (
    "Normative and CLOSED. WHERE a per-requirement sufficiency_v2 outcome travels once it leaves "
    "this unit, and in WHICH vocabulary. This block adds no member to DeficiencyV2, changes no "
    "carrier row above, adds no D9 class, code, exit or public detail code, and changes no D9 "
    "projection: it names the consumer boundary that was previously unnamed."
)
block['producer'] = (
    "native-evidence.md section 4.6 `sufficiency_v2`, evaluated once per RequirementV2 against one "
    "view. It is TOTAL and its result shape is closed: either {satisfied: true, disclosures} with "
    "NO deficiency, or {satisfied: false, deficiency} carrying exactly ONE DeficiencyV2 member "
    "selected by the section 10 precedence over every applicable cause. There is no third shape, "
    "so a consumer record has no lawful reason to omit the value."
)
block['consumers'] = [
    collections.OrderedDict([
        ("record", "workflows/schemas/repair.schema.json#/$defs/EvidenceRequirement"),
        ("field", "deficiency"),
        ("carries", "the DeficiencyV2 member sufficiency_v2 returned for THIS requirement"),
        ("vocabulary", "urn:opensip:product-v1:workflows:common#/$defs/NativeSufficiencyDeficiency, "
                       "a generated/drift-checked mirror of #/$defs/DeficiencyV2 in its declared "
                       "member order; the workflows bundle resolves only workflows URNs and takes "
                       "no cross-bundle $ref, so the vocabulary is mirrored, never re-owned"),
        ("presenceLaw", "REQUIRED exactly when satisfied is false; FORBIDDEN when satisfied is "
                        "true. Schema-enforced in repair.schema.json and admitted again by "
                        "workflows_model.admit_evidence_requirement at repair_preview."),
        ("authorityLimit", "The field is a DISCLOSURE, not a grant and not a gate input. `applicable` "
                           "is false whenever any requirement is unsatisfied, the evidence authority "
                           "stays the sealed Run named by evidenceRunId, and apply requires a "
                           "security authorization bound to the exact repairPlanId - which every "
                           "edit to this value changes."),
    ]),
]
block['whyNotTheD9Vocabulary'] = (
    "The field previously named workflows common#/$defs/D9Deficiency, which cannot express four of "
    "the nine members its only producer emits: derivation-policy-unmet, external-consumers-unknown, "
    "input-closure-incomplete and resolution-incomplete have no member there. Only three readings "
    "were conforming and no document chose between them: write the D9-mapped value, which is "
    "`verdict-indeterminate` for ALL FOUR and therefore collapses exactly the per-row distinction "
    "this registry exists to keep - including resolution-incomplete, which section 4.6 step 6 "
    "mandates for a universal negative under unresolvedEdgePolicy=forbid over an affected target "
    "and which is the outcome a destructive unused-code repair recipe turns on; write the "
    "sufficiency value and be schema-invalid for four of nine; or omit the optional field and drop "
    "the disclosure. The repair is to retype the ONE per-requirement field, not to widen "
    "D9Deficiency: that enum is the whole-Run and comparison-step termination vocabulary of the "
    "inherited D9 exit contract, three of its members (convergence-exhausted, "
    "baseline-recipe-unsupported, query-completeness-unmet) name outcomes no per-requirement "
    "evaluation can produce, and widening it would change a D9 vocabulary to fix a workflows "
    "record. The DomainDetailCode route does not resolve it either: that registry carries a "
    "DIFFERENT five of the nine (budget-exhausted plus the four above), so the union of the two "
    "covers all nine and neither single field does."
)
block['threeDistinctThingsNotToConflate'] = collections.OrderedDict([
    ("nativeOutcome", "the DeficiencyV2 member for one requirement - what this block routes."),
    ("publicD9Termination", "the class/exit/errorCode of the Run or step that carries the "
                            "requirement - unchanged, still the section 10 table columns "
                            "(indeterminate (3) with VERDICT.INDETERMINATE, "
                            "COVERAGE.PROVIDER_UNAVAILABLE or COVERAGE.BUDGET_EXHAUSTED) and still "
                            "spelled with D9Deficiency where a D9 record needs a deficiency."),
    ("retainedCause", "the Coverage entry's own cause carrier - entry.nativeCause or the named "
                      "structured field per the `deficiencies` rows above. The requirement record "
                      "carries the OUTCOME and never the carrier: several outcomes are "
                      "requirement-relative (the confidence floor lives in RequirementV2; "
                      "external-consumer state matters only for a universal negative about an "
                      "exported target) and required-relation-missing has no entry at all, so a "
                      "carrier could not be copied here even in principle."),
    ("satisfiedState", "a boolean about THIS requirement, not a verdict and not a coverage state. "
                       "satisfied=true may still carry section 4.6 disclosures, which are not "
                       "deficiencies and are not carried by this field."),
])
block['enforcedAt'] = (
    "workflows_model.admit_evidence_requirement (the repair-preview producer/consumer boundary, run "
    "before any descriptor exists, refusals native.sufficiency-outcome-*), the repair.schema.json "
    "presence law, and the cross-unit enum parity control in "
    "docs/coop/design-corrections/check-integration.py."
)
block['driftIsAFailureNotAWidening'] = (
    "A member added to or removed from DeficiencyV2 without the same change in the workflows mirror "
    "fails the cross-unit parity control. The mirror is never allowed to be a superset: a workflows "
    "record must not be able to state a native outcome this unit does not define."
)

reg['perRequirementConsumerBoundary'] = block

out = json.dumps(d, indent=1, ensure_ascii=True) + '\n'
P.write_text(out, encoding='utf-8')
print('ok', len(raw), '->', len(out))
