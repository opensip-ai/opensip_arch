"""CX-BV6-03: publish the OWNING outcome law for imported-evidence repair requirements."""
import json, pathlib, collections

W = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v2/work')
S = W / 'docs/coop/design-corrections/workflows/schemas'

# ------------------------------------------------- 1. the law, in the document that owns the plane
P = S / 'imported-evidence.schema.json'
d = json.loads(P.read_text(encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
assert 'x-opensip-imported-requirement-law' not in d

MEMBERS = collections.OrderedDict([
 ('evidence-kind-unavailable', collections.OrderedDict([
   ('meaning', "No import of this relation's evidenceKind is available to this Run at all."),
   ('groundedIn', "workflows-and-surfaces.md section 5: an atom over imported evidence must be "
                  "declared in evidenceUse, and REQUIRED evidence absent makes the rule "
                  "indeterminate. The same absence makes a required repair requirement unsatisfied."),
   ('optionalCounterpart', "When the requirement is OPTIONAL the same absence is not a deficiency: "
                           "it is the existing IMPORT.ABSENT_FOR_PREDICATE disclosure and the "
                           "requirement is satisfied with that disclosure. The required/optional "
                           "distinction is NOT re-invented here; it is the same one evidenceUse "
                           "already carries.")])),
 ('import-unmapped-only', collections.OrderedDict([
   ('meaning', "An import of the kind exists but is unmapped-only for this Plan, so it never feeds "
               "a predicate and cannot support a requirement either."),
   ('groundedIn', "workflows-and-surfaces.md section 4 StalenessRule: snapshot-differs, "
                  "commit-differs, commit-equal-dirty and build-identity-differs are all "
                  "unmapped-only, and `unmapped-only evidence may be listed and queried but never "
                  "feeds a predicate`. Explicitly SELECTING a stale import for a Plan remains the "
                  "separate IMPORT.STALE_FOR_PLAN request refusal and is not this outcome.")])),
 ('subject-not-observable', collections.OrderedDict([
   ('meaning', "The requirement's target subjects are carried by the payload as `unobservable` or "
               "`unmapped`, so the capture made no claim about them in either direction."),
   ('groundedIn', "workflows-and-surfaces.md section 4: `unobservable`/`unmapped` never become "
                  "unhit signals and the schema refuses a hit count on them. Reading either as "
                  "negative evidence is exactly the error this member exists to name.")])),
 ('observation-window-insufficient', collections.OrderedDict([
   ('meaning', "An observation exists and is mapped, but its window or population does not meet "
               "what the requirement asks."),
   ('groundedIn', "workflows-and-surfaces.md section 4: positive and bounded-negative runtime "
                  "evidence is admitted `always together with the observation window and "
                  "population`, and RuntimePayloadV1 carries observationWindow and "
                  "observedPopulation as required members.")])),
 ('import-absent-for-requirement', collections.OrderedDict([
   ('meaning', "The kind is available and consumable, but no observation in it reaches this "
               "requirement's targets."),
   ('groundedIn', "The existing IMPORT.ABSENT_FOR_PREDICATE condition, applied per requirement "
                  "rather than per predicate. Named separately from evidence-kind-unavailable "
                  "because the remedies differ: import the evidence versus widen the capture.")])),
])

law = collections.OrderedDict()
law['standing'] = (
    "Normative and CLOSED. THE outcome law for a repair EvidenceRequirement whose relation is one of "
    "the two imported-evidence relations registered above. It adds no relation, no rung, no import "
    "kind, no payload domain and no D9 class, code or exit."
)
law['whyItIsOwed'] = (
    "repair.schema.json#/$defs/EvidenceRequirement admits ANY relation that repair_preview's "
    "admit_atom admits, which is the thirteen native fact relations OR the two relations in this "
    "registry. Native section 4.6 `sufficiency_v2` ranges only over a native VIEW: asked about "
    "runtime-observation or history-change it returns `required-relation-missing`, because there is "
    "no view entry for a relation that mints no fact2. So a requirement over an imported relation "
    "was admissible with no defined producer for its outcome, and the earlier claim that "
    "sufficiency_v2 is the ONLY producer of that field was wrong for exactly these two relations."
)
law['twoPlanesOneField'] = (
    "The planes are NOT merged. A native requirement carries a DeficiencyV2 member; an imported "
    "requirement carries a member of this vocabulary. They are different sets because they name "
    "different machinery: DeficiencyV2 speaks of Coverage states, rungs, universes and resolution "
    "completeness, none of which an imported observation has. Writing `resolution-incomplete` about "
    "a runtime capture, or `import-unmapped-only` about a native view, is a category error and is "
    "refused. Which plane applies is decided at ADMISSION from the relation's registry membership - "
    "the same place the two planes are already separated by the evidenceDeclarationRule - and never "
    "guessed from the value."
)
law['outcomes'] = MEMBERS
law['precedence'] = ['evidence-kind-unavailable', 'import-unmapped-only', 'subject-not-observable',
                     'observation-window-insufficient', 'import-absent-for-requirement']
law['precedenceRule'] = (
    "Most specific first, in the order a consumer can act on: an absent kind is imported, an "
    "unmapped-only import is re-mapped or re-captured against the current snapshot, an unobservable "
    "subject is instrumented, an insufficient window is widened, and only then is the observation "
    "genuinely silent about the target. Every applicable condition is evaluated; the reported "
    "outcome is the first in this order."
)
law['whatThisOutcomeNeverEstablishes'] = (
    "A satisfied imported requirement is POSITIVE, BOUNDED evidence and is never a universal "
    "negative. `observable-unhit` is not `unused`, one window never establishes universal non-use, "
    "and runtime coverage is never OpenSIP Coverage. In particular an imported requirement can never "
    "be the evidence that makes an unsafe repair applicable: EVERY delete and EVERY replace is "
    "decided against the evidence Run's own native ClosedWorldV2 (native section 4.5) BEFORE any "
    "descriptor exists, and no imported requirement, satisfied or not, changes "
    "deadCodeRepairEligible. That separation is held by a control, not assumed."
)
law['whatIsPreserved'] = [
    "the original evidence Run named by evidenceRunId remains the authority; nothing here is a "
    "substitute for it",
    "per-target evaluation: the outcome is decided against THIS requirement's targets, not against "
    "the payload as a whole",
    "observation window and observed population travel with every positive and bounded-negative "
    "claim, exactly as section 4 requires",
    "required versus optional stays where evidenceUse already puts it; an optional absence is the "
    "existing IMPORT.ABSENT_FOR_PREDICATE disclosure and is not a deficiency",
    "the native sufficiency guard is untouched: sufficiency_v2 still owns every native relation and "
    "is not asked about these two",
]
law['enforcedAt'] = (
    "workflows_model.admit_evidence_requirement decides the plane and refuses a cross-plane value or "
    "a shape violation at the repair-preview producer/consumer boundary; "
    "workflows_model.imported_requirement_outcome is the reference producer implementing the "
    "precedence above. The vocabulary is mirrored into workflows common as "
    "ImportedRequirementDeficiency and held equal to this law by a control."
)
d['x-opensip-imported-requirement-law'] = law
P.write_text(json.dumps(d, indent=2, ensure_ascii=True) + '\n', encoding='utf-8')

# ------------------------------------------------- 2. the mirrored vocabulary
Q = S / 'common.schema.json'
raw = Q.read_text(encoding='utf-8')
OLD = '''    "NativeSufficiencyDeficiency": {
      "type": "string",
'''
NEW = '''    "ImportedRequirementDeficiency": {
      "type": "string",
      "enum": [
%s
      ],
      "description": %s,
      "x-opensip-vocabulary": {
        "authority": "workflows/schemas/imported-evidence.schema.json#/x-opensip-imported-requirement-law/outcomes",
        "producer": "workflows_model.imported_requirement_outcome, per requirement",
        "admittedBy": "workflows_model.admit_evidence_requirement, which decides the plane from the relation registry before reading the value",
        "note": "GENERATED/DRIFT-CHECKED from the law's outcome keys in its declared precedence order. It is a DIFFERENT vocabulary from NativeSufficiencyDeficiency and the two never mix: a native requirement carrying an imported outcome, or the reverse, is refused."
      }
    },
    "NativeSufficiencyDeficiency": {
      "type": "string",
''' % (
    ',\n'.join('        "%s"' % m for m in law['precedence']),
    json.dumps(
        "The IMPORTED-EVIDENCE per-requirement outcome vocabulary, owned by "
        "imported-evidence.schema.json#/x-opensip-imported-requirement-law. It applies to a repair "
        "EvidenceRequirement whose relation is `runtime-observation` or `history-change` - relations "
        "that mint no fact2, carry no sourceUniverse/targetUniverse and have no Coverage entry, so "
        "native section 4.6 `sufficiency_v2` cannot produce an outcome for them and is not asked to. "
        "Every member names an already-published import condition: evidence-kind availability, "
        "unmapped-only staleness, subject observability, and observation window/population. A "
        "satisfied imported requirement is positive bounded evidence and NEVER a universal negative: "
        "one window does not establish universal non-use, and the unsafe-repair gate stays the native "
        "ClosedWorldV2."),
)
assert raw.count(OLD) == 1
Q.write_text(raw.replace(OLD, NEW), encoding='utf-8')
print('ok; members', law['precedence'])
