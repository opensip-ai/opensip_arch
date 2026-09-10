"""CX-BV6-03 rework after the Codex note: separate runtime and history projections, bind every
input to an owning field, use the EXISTING completeness field for all-versus-any, and correct the
positive/negative and applicability wording."""
import json, pathlib, collections

W = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v2/work')
S = W / 'docs/coop/design-corrections/workflows/schemas'

P = S / 'imported-evidence.schema.json'
d = json.loads(P.read_text(encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
law = d['x-opensip-imported-requirement-law']

OUT = collections.OrderedDict([
 ('evidence-kind-unavailable', collections.OrderedDict([
   ('appliesTo', ['runtime', 'history']),
   ('meaning', "No admitted import of this relation's evidenceKind reaches this Run."),
   ('boundTo', "the admitted import set of the evidence Run named by RepairPlanDescriptor.evidenceRunId"),
   ('groundedIn', "section 5: an atom over imported evidence must be declared in evidenceUse and "
                  "REQUIRED evidence absent makes the rule indeterminate.")])),
 ('import-unmapped-only', collections.OrderedDict([
   ('appliesTo', ['runtime', 'history']),
   ('meaning', "An import of the kind exists but is unmapped-only for this Plan."),
   ('boundTo', "the StalenessRule disposition of that import against this Plan"),
   ('groundedIn', "section 4 StalenessRule: snapshot-differs, commit-differs, commit-equal-dirty and "
                  "build-identity-differs are unmapped-only, and unmapped-only evidence never feeds "
                  "a predicate. Explicitly SELECTING a stale import stays the separate "
                  "IMPORT.STALE_FOR_PLAN request refusal and is not this outcome.")])),
 ('subject-not-observable', collections.OrderedDict([
   ('appliesTo', ['runtime']),
   ('meaning', "A required target is carried by the runtime payload as `unobservable` or `unmapped`, "
               "so the capture made no claim about it in either direction."),
   ('boundTo', "RuntimeSubject.observability for that target"),
   ('groundedIn', "section 4: unobservable/unmapped never become unhit signals and the schema refuses "
                  "a hit count on them.")])),
 ('observation-window-insufficient', collections.OrderedDict([
   ('appliesTo', ['runtime']),
   ('meaning', "A mapped observation exists but its window or population does not meet what the "
               "recipe asked for."),
   ('boundTo', "RuntimePayloadV1.observationWindow and observedPopulation, compared against the "
               "admitted repair recipe's declared demand; the demand is an input, never inferred "
               "from the payload"),
   ('groundedIn', "section 4: positive and bounded-negative runtime evidence is admitted always "
                  "together with the observation window and population.")])),
 ('history-range-insufficient', collections.OrderedDict([
   ('appliesTo', ['history']),
   ('meaning', "A mapped history import exists but its revision range does not meet what the recipe "
               "asked for, or the range was truncated."),
   ('boundTo', "HistoryPayloadV1.revisionRange (from/to/commitCount/truncated)"),
   ('groundedIn', "HistoryPayloadV1 carries revisionRange with an explicit `truncated` flag and NO "
                  "observationWindow, observedPopulation or observability. History has its own "
                  "projection and the runtime one is never applied to it.")])),
 ('history-outside-collection-scope', collections.OrderedDict([
   ('appliesTo', ['history']),
   ('meaning', "A required target lies outside the scope the history collection covered, so its "
               "absence from the payload carries no information."),
   ('boundTo', "HistoryPayloadV1.collectionScope (all-paths | in-scope-paths | listed-paths)"),
   ('groundedIn', "collectionScope is a required member precisely so that an absent path can be "
                  "distinguished from an unexamined one.")])),
 ('import-absent-for-requirement', collections.OrderedDict([
   ('appliesTo', ['runtime', 'history']),
   ('meaning', "The kind is available and consumable and the target was in scope, but the payload "
               "carries no subject row reaching that target."),
   ('boundTo', "RuntimePayloadV1.subjects / HistoryPayloadV1.subjects, per target"),
   ('groundedIn', "the existing IMPORT.ABSENT_FOR_PREDICATE condition, applied per requirement "
                  "rather than per predicate. Named separately from evidence-kind-unavailable "
                  "because the remedies differ: import the evidence versus widen the capture.")])),
])
law['outcomes'] = OUT
law['precedence'] = ['evidence-kind-unavailable', 'import-unmapped-only', 'subject-not-observable',
                     'history-outside-collection-scope', 'observation-window-insufficient',
                     'history-range-insufficient', 'import-absent-for-requirement']
law['perKindApplicability'] = collections.OrderedDict([
    ('runtime-observation', [m for m, r in OUT.items() if 'runtime' in r['appliesTo']]),
    ('history-change', [m for m, r in OUT.items() if 'history' in r['appliesTo']]),
    ('rule', "Each relation may report only the outcomes its own payload can ground. A history "
             "requirement can never report a runtime observability or window outcome, and a runtime "
             "requirement can never report a history range or collection-scope outcome; the producer "
             "refuses rather than borrowing the other kind's projection."),
])
law['inputBinding'] = collections.OrderedDict([
    ('standing', "EvidenceRequirement carries only relation, minResolution, completeness, satisfied "
                 "and deficiency. Every other input this law reads is named here with the field that "
                 "owns it, so no untyped caller value stands in for a measured Run."),
    ('targets', "RepairPlanDescriptor.targets - the plan's own target fingerprints. Targets are NOT a "
                "field of EvidenceRequirement and none is added; the producer is evaluated against "
                "the plan it is being built for, which is the same binding repair_preview already "
                "uses when it checks that every target is present in the evidence Run."),
    ('allVersusAny', "RepairPlanDescriptor.evidenceRequirements[].completeness, which already exists "
                     "and already means exactly this. `complete` requires EVERY target to be "
                     "supported; `partial-acceptable` requires at least one. A draft of this producer "
                     "used `any()` unconditionally and therefore admitted a `complete` requirement "
                     "while one target was unsupported; that is corrected and controlled in both "
                     "directions."),
    ('requiredVersusOptional', "the rule's evidenceUse declaration (section 5). It is an INPUT to this "
                               "producer and is never defaulted to `optional`: an unknown or "
                               "unsupplied declaration is treated as REQUIRED, so an unresolved "
                               "condition is never silently satisfied."),
    ('windowDemand', "the admitted repair recipe's declared observation demand. It is an input; this "
                     "law does not infer a demand from the payload that would answer it."),
    ('admittedInputsOnly', "This is a PURE reference projection over inputs an authenticated importer "
                           "and the retained Run closure have ALREADY admitted. It does not itself "
                           "validate an opaque Run, does not re-derive source correspondence, and "
                           "does not admit payload, observation scope or polarity - those remain the "
                           "importer's and the evaluator's. Its preconditions are stated so a caller "
                           "cannot mistake it for that admission."),
])
law['whatASatisfiedOutcomeMeans'] = (
    "It means the requirement's evidential condition was met over the BOUND window, range and "
    "population - not that the evidence is positive. `observed-hit` is positive execution evidence "
    "and `observable-unhit` is BOUNDED NEGATIVE evidence; both can satisfy a requirement, and which "
    "one did is carried in the disclosure rather than collapsed. An OPTIONAL absence that satisfies "
    "under the evidenceUse rule is satisfied by ABSENCE, not by positive evidence, and its disclosure "
    "says so. Calling every satisfied outcome positive would contradict section 4 and would throw "
    "away the richer evidence the bounded-negative case exists to carry."
)
law['whatThisOutcomeNeverEstablishes'] = (
    "No imported observation establishes a universal negative. One window never establishes universal "
    "non-use, `observable-unhit` is not `unused`, and runtime coverage is never OpenSIP Coverage. In "
    "particular imported evidence can NEVER BY ITSELF establish the native closed world or authorize "
    "an unsafe delete or replace: EVERY delete and EVERY replace is decided against the evidence "
    "Run's own native ClosedWorldV2 (native section 4.5) before any descriptor exists, and no "
    "imported outcome changes deadCodeRepairEligible. It may, however, be an ADDITIONAL required "
    "condition alongside an already-established native safety basis - a recipe may lawfully require "
    "both - so it is wrong to say imported evidence can never affect applicability. Both directions "
    "are held by controls: an unsafe plan whose only requirement is a satisfied imported one is still "
    "refused by the closed-world gate, and an unsatisfied imported requirement still makes an "
    "otherwise-eligible plan inapplicable."
)
law['enforcedAt'] = (
    "workflows_model.admit_evidence_requirement decides the plane and refuses a cross-plane value or "
    "a shape violation at the repair-preview producer/consumer boundary; "
    "workflows_model.imported_requirement_outcome is the reference projection implementing the "
    "precedence and the per-kind applicability above, over already-admitted inputs. The vocabulary is "
    "mirrored into workflows common as ImportedRequirementDeficiency and held equal to this law."
)
d['x-opensip-imported-requirement-law'] = law
P.write_text(json.dumps(d, indent=2, ensure_ascii=True) + '\n', encoding='utf-8')

# ------------------------------------------------------------------ mirror the new member order
Q = S / 'common.schema.json'
raw = Q.read_text(encoding='utf-8')
start = raw.index('    "ImportedRequirementDeficiency": {')
enum_start = raw.index('"enum": [', start)
enum_end = raw.index(']', enum_start)
raw = raw[:enum_start] + '"enum": [\n' + ',\n'.join(
    '        "%s"' % m for m in law['precedence']) + '\n      ' + raw[enum_end:]
Q.write_text(raw, encoding='utf-8')
print('ok; members', len(law['precedence']))
