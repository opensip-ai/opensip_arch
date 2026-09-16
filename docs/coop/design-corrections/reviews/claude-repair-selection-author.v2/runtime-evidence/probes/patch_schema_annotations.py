"""Rewrite the `closedWorld` annotation in both repair schemas for RRS-A1/RRS-A2.

Field SHAPE is untouched: same five required members, same additionalProperties, same majors,
same key order, same formatting everywhere else. Proven by re-parsing both documents, blanking
that one annotation in each, and requiring the rest to be byte-identical.
"""
import hashlib, json, os

SRC = '/tmp/opensip-design-corrections/repair-selection-successor.v2/source'
DOCS = os.path.join(SRC, 'docs/coop/design-corrections/workflows/schemas')

NEW_DESC = (
    "AUTHOR_PENDING_REVIEW. The deterministic five-field DISPLAY SUMMARY of the native "
    "ClosedWorldV2 records that the workflows-and-surfaces section 6 SELECTION LAW selected "
    "from the evidence Run - NOT a copy, NOT a projection of one record, and NOT itself a "
    "native producer record. WHY A SUMMARY AND NOT A COPY: ClosedWorldV2 is a required member "
    "of ViewEntryV3 (native-evidence.md section 4.3), so a Run retains ONE PER COVERAGE ENTRY "
    "keyed by CoverageKeyV2, and identity-and-evidence.md section 3 makes several differing "
    "entries lawful in one Run. There is no Run-level ClosedWorldV2 to copy. ClosedWorldV2 is "
    "closed at SEVEN required members and a literal copy is REFUSED here (dynamicDispatch and "
    "reasons are not properties of this record). "
    "RELEVANT UNIVERSES: every universe reached by ALL matching occurrences of EVERY target "
    "fingerprint (finding3.subjectId -> subject3.universe) UNION every universe that owns an "
    "unsafe edited path in the RETAINED SELECTED-PROGRAM CENSUS of this Run's EnumerationPlanV1. "
    "That parameter is REQUIRED for evaluator3 (absent it refuses "
    "EVALUATOR_REQUIRED_PARAMETER_MISSING and full replay re-admits it), so the join is "
    "guaranteed and retained - never a caller-selected or optional unsigned map, never filename "
    "parsing. For each binding whose enumerator.status is `selected`, its applicable path census "
    "is its own extents[] per kind plus, on a candidate-only cell, candidateSourcePaths. A "
    "binding with a NON-NULL universe whose census contains the path contributes that universe. "
    "A SELECTED but UNAVAILABLE binding (universe=null, extents still populated from host "
    "membership) contributes TYPED UNRESOLVED OWNERSHIP: REPAIR.CLOSED_WORLD_NOT_ESTABLISHED "
    "that does NOT vanish because another owner of the same path is closed. An UNSELECTED "
    "binding is never inferred as an owner. Each extent kind is read as itself: file and package "
    "are host membership extents, symbol is the selected program's CODE scope, so all snapshot "
    "files are NOT treated as every compiler's programRootFiles and a selected program whose own "
    "census lacks the edit stays UNRELATED. Multiple ownership is preserved (one path under two "
    "Rust targets or editions is two bindings and both must be eligible). Retained source-path "
    "subject scopes (file, clones, vcs-change, all universeRule same-only) are an ADDITIONAL "
    "retained witness only: their subjectKindLaw proves those scopes NAME paths, not that they "
    "ENUMERATE every selected program owning one, and a universe bound only to a symbol-kind "
    "cell - owning a path through its retained symbol extent, with no file inventory and no "
    "lawful file@enumerated scope - is admitted. No path is reconstructed from an opaque native "
    "symbol ID; the census publishes the program's path extent directly. "
    "SELECTED RECORDS: EVERY retained native coverage2 whose scope sourceUniverse is relevant - "
    "independent of evidenceRequirements, so a recipe can neither pick a favourable relation or "
    "rung nor drop a conflicting record - deduplicated by retained coverage2 identity and "
    "ORDERED ON UTF-8 ENCODED BYTES by relation, resolution, sourceUniverse, targetUniverse, "
    "subjectScopeCommitment, then the coverage2 identity, which makes the order total even "
    "between two records agreeing on all five coordinates. "
    "GATE: eligibility for EVERY delete and EVERY replace in the plan is the NON-VACUOUS "
    "CONJUNCTION of deadCodeRepairEligible over those selected records, decided BEFORE this "
    "record is built. A relevant universe with no retained native Coverage, an unsafe path with "
    "no reconstructable owner, and an unresolved unavailable-binding ownership are each "
    "REPAIR.CLOSED_WORLD_NOT_ESTABLISHED - an empty evidence subset is not truth and no evidence "
    "is guessed. Each dissent remedy names ALL SIX ordering members UNABBREVIATED, including the "
    "exact retained coverage2 identity, because two lawfully distinct records can differ only in "
    "targetUniverse, only in subjectScopeCommitment, or only in the identity. Imported "
    "observations neither establish nor improve this gate; only native coverage2 records are "
    "selected. dynamicDispatch is NOT read by this gate and is NOT a global veto: native section "
    "4.5 affected_targets and section 4.6 sufficiency_v2 keep dynamic-edge effects "
    "target-relative and per-requirement, and those judgements stay separate from this boolean. "
    "REDUCTION: deadCodeRepairEligible is the conjunction; each other member takes the "
    "LEAST-CLOSED value present (closed<open<unknown, all<partial<none, none<present, "
    "none-declared<possible<unknown); and ABSENCE IS FOLDED IN, so a relevant universe with no "
    "Coverage or an unresolved ownership also opens the summary instead of hiding behind the "
    "records that do exist. With nothing selected the same rule yields the FIVE-FIELD "
    "LEAST-CLOSED DISPLAY SENTINEL {deadCodeRepairEligible:false, exportsClosed:unknown, "
    "entryPointsRecognized:none, nonliteralLoading:present, externalConsumers:unknown}. That is "
    "NOT an all-unknown record: only two members are unknown, the other three being a false "
    "boolean and the least-closed pole of each enum that cannot spell absence. A create-only plan "
    "activates no gate and an ineligible closed world alone adds NO unmet precondition to it, but "
    "it still READS the selection and still BUILDS this required member, so the descriptor and "
    "therefore repairPlanId stay deterministic. "
    "AUTHORITY: this record has NONE, and NO MEMBER OF IT IS AUTHORITATIVE, the boolean "
    "included. It is a descriptor member carried for display and for the repairPlanId preimage, "
    "and it is never the input to the gate, which reads the full selected records including the "
    "two members this one does not carry. Editing a field here cannot bypass anything: a missing "
    "required member is schema-invalid, any edit mints a different repairPlanId, and apply "
    "requires a security authorization bound to the exact repairPlanId, base snapshot and "
    "project. Recipe trust, policy consent and current-snapshot equality remain separately "
    "required, and preview is a Query-class step that authorizes nothing. IDENTITY: this "
    "member's SHAPE and the repairPlanId RECIPE are unchanged; its VALUE may differ from an "
    "implementation that used a caller-selected record, so the minted repairPlanId may differ. "
    "NO repairPlanId equality is claimed across different evidenceRunIds - evidenceRunId is in "
    "the preimage, so a different Run is a different plan identity however similar its evidence."
)

EXPECT_REQUIRED = ['deadCodeRepairEligible', 'exportsClosed', 'entryPointsRecognized',
                   'nonliteralLoading', 'externalConsumers']

rows = []
for rel in ('repair.schema.json', 'evaluator3/repair.schema.json'):
    path = os.path.join(DOCS, rel)
    raw = open(path, 'rb').read()
    text = raw.decode()
    doc = json.loads(text)
    node = doc['$defs']['RepairPlanDescriptor']['properties']['closedWorld']
    assert node['required'] == EXPECT_REQUIRED, rel
    assert node['additionalProperties'] is False, rel
    old = node['description']
    if old == NEW_DESC:
        print('already patched, skipping', rel)
        continue

    candidates = [json.dumps(old, ensure_ascii=True), json.dumps(old, ensure_ascii=False)]
    hits = [c for c in dict.fromkeys(candidates) if text.count(c) == 1]
    assert len(hits) == 1, (rel, [text.count(c) for c in candidates])
    old_literal = hits[0]
    new_text = text.replace(old_literal, json.dumps(NEW_DESC, ensure_ascii=(old_literal == candidates[0])))

    a, b = json.loads(text), json.loads(new_text)
    a['$defs']['RepairPlanDescriptor']['properties']['closedWorld']['description'] = ''
    b['$defs']['RepairPlanDescriptor']['properties']['closedWorld']['description'] = ''
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True), rel
    after = json.loads(new_text)
    assert after['$defs']['RepairPlanDescriptor']['properties']['closedWorld']['required'] == EXPECT_REQUIRED
    assert list(after['$defs']['RepairPlanDescriptor']['properties']) == list(doc['$defs']['RepairPlanDescriptor']['properties'])

    open(path, 'w').write(new_text)
    rows.append({'path': rel, 'beforeSha256': hashlib.sha256(raw).hexdigest(),
                 'beforeBytes': len(raw),
                 'afterSha256': hashlib.sha256(new_text.encode()).hexdigest(),
                 'afterBytes': len(new_text.encode()),
                 'onlyChange': '$defs/RepairPlanDescriptor/properties/closedWorld/description'})
    print('patched', rel, len(raw), '->', len(new_text.encode()))

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schema-annotation-patch.json')
json.dump(rows, open(out, 'w'), indent=2)
print('WROTE', out)
