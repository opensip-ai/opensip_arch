"""Rewrite the `closedWorld` annotation in both repair schemas, by EXACT textual
substitution of that one JSON string value.

Field SHAPE is untouched: same five required members, same additionalProperties, same
majors, same key order, same file formatting everywhere else. The whole document is
re-parsed afterwards and diffed against the original with only that one annotation
normalised, so any other byte change would fail the assertion.
"""
import json, hashlib, os

SRC = '/tmp/opensip-design-corrections/repair-selection-successor.v1/source'
DOCS = os.path.join(SRC, 'docs/coop/design-corrections/workflows/schemas')

NEW_DESC = (
    "AUTHOR_PENDING_REVIEW. The deterministic five-field DISPLAY SUMMARY of the native "
    "ClosedWorldV2 records that the workflows-and-surfaces section 6 SELECTION LAW selected "
    "from the evidence Run - NOT a copy, NOT a projection of one record, and NOT itself a "
    "native producer record. WHY A SUMMARY AND NOT A COPY: ClosedWorldV2 is a required member "
    "of ViewEntryV3 (native-evidence.md section 4.3), so a Run retains ONE PER COVERAGE ENTRY "
    "keyed by CoverageKeyV2 (relation, resolution, sourceUniverse, targetUniverse, "
    "subjectScopeCommitment), and identity-and-evidence.md section 3 makes several differing "
    "entries lawful in one Run. There is no Run-level ClosedWorldV2 to copy. ClosedWorldV2 is "
    "closed at SEVEN required members and a literal copy is REFUSED here (dynamicDispatch and "
    "reasons are not properties of this record). "
    "SELECTION (section 6, normative): the relevant universes are every universe reached by "
    "ALL matching occurrences of EVERY target fingerprint (finding3.subjectId -> "
    "subject3.universe) UNION every universe that owns an unsafe edited path, read from "
    "retained subject scopes of the source-path relations (file, clones, vcs-change - all "
    "universeRule same-only) whose subjects ARE snapshot paths. Ownership is never inferred "
    "from a path prefix, a display string, a sidecar, an unreferenced host observation or a "
    "symbol-kind scope, whose symbol-to-path attribution the registry states is not "
    "re-derivable from a retained Run. targets and edits are separate arrays with no "
    "published correspondence and none is invented. The selected records are EVERY retained "
    "native coverage2 whose scope sourceUniverse is relevant - independent of "
    "evidenceRequirements, so a recipe can neither pick a favourable relation/rung nor drop a "
    "conflicting record - deduplicated by retained coverage2 identity and ordered by the full "
    "partition key then that identity. "
    "GATE: eligibility for EVERY delete and EVERY replace in the plan is the NON-VACUOUS "
    "CONJUNCTION of deadCodeRepairEligible over those selected records, decided BEFORE this "
    "record is built. A relevant universe with no retained native Coverage, or an unsafe path "
    "with no reconstructable owning universe, is REPAIR.CLOSED_WORLD_NOT_ESTABLISHED - an "
    "empty evidence subset is not truth and no evidence is guessed. Imported observations "
    "establish and improve nothing here; only native coverage2 records are selected. "
    "dynamicDispatch is NOT read by this gate and is NOT a global veto: native section 4.5 "
    "affected_targets and section 4.6 keep dynamic-edge effects target-relative and "
    "per-requirement, and those judgements stay separate from this boolean. "
    "REDUCTION: deadCodeRepairEligible is the conjunction, false when nothing was selected; "
    "each other member takes the LEAST-CLOSED value present (closed<open<unknown, "
    "all<partial<none, none<present, none-declared<possible<unknown), and with nothing "
    "selected the least-closed member of its own enum. nonliteralLoading has no unknown "
    "member in the owner enum, so its empty value is `present`: that is this display rule "
    "applied uniformly, not an observation, and widening the native enum is not this "
    "schema's to do. A create-only plan activates no gate and an ineligible closed world "
    "alone adds NO unmet precondition to it, but it is still summarised by this same "
    "reduction, so the descriptor and therefore repairPlanId stay deterministic. "
    "AUTHORITY: this record has NONE. It is a descriptor member carried for display and for "
    "the repairPlanId preimage, and it is never the input to the gate, which reads the full "
    "selected records including the two members this one does not carry. Editing a field here "
    "cannot bypass anything: a missing required member is schema-invalid, any edit mints a "
    "different repairPlanId, and apply requires a security authorization bound to the exact "
    "repairPlanId, base snapshot and project. Preview is a Query-class step and is not "
    "authorization. IDENTITY: this member's SHAPE and the repairPlanId RECIPE are unchanged; "
    "its VALUE may differ from an implementation that used a caller-selected record, so the "
    "minted repairPlanId may differ. No repairPlanId equality is claimed across different "
    "Runs - evidenceRunId is in the preimage."
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
        rows.append({'path': rel, 'alreadyPatched': True,
                     'afterSha256': hashlib.sha256(raw).hexdigest(), 'afterBytes': len(raw),
                     'onlyChange': '$defs/RepairPlanDescriptor/properties/closedWorld/description'})
        continue

    # The two files do not use the same escaping for non-ASCII, so try both spellings and
    # require exactly one to match exactly once. No regex, no fuzzy matching.
    candidates = [json.dumps(old, ensure_ascii=True), json.dumps(old, ensure_ascii=False)]
    hits = [c for c in dict.fromkeys(candidates) if text.count(c) == 1]
    assert len(hits) == 1, (rel, [text.count(c) for c in candidates])
    old_literal = hits[0]
    replacement = json.dumps(NEW_DESC, ensure_ascii=(old_literal == candidates[0]))
    new_text = text.replace(old_literal, replacement)

    # Proof that nothing else moved: parse both, normalise ONLY this annotation, compare.
    after = json.loads(new_text)
    a, b = json.loads(text), json.loads(new_text)
    a['$defs']['RepairPlanDescriptor']['properties']['closedWorld']['description'] = ''
    b['$defs']['RepairPlanDescriptor']['properties']['closedWorld']['description'] = ''
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True), rel
    assert after['$defs']['RepairPlanDescriptor']['properties']['closedWorld']['required'] == EXPECT_REQUIRED
    assert list(after['$defs']['RepairPlanDescriptor']['properties']) == list(doc['$defs']['RepairPlanDescriptor']['properties'])

    open(path, 'w').write(new_text)
    rows.append({'path': rel,
                 'beforeSha256': hashlib.sha256(raw).hexdigest(), 'beforeBytes': len(raw),
                 'afterSha256': hashlib.sha256(new_text.encode()).hexdigest(),
                 'afterBytes': len(new_text.encode()),
                 'onlyChange': '$defs/RepairPlanDescriptor/properties/closedWorld/description',
                 'oldDescriptionChars': len(old), 'newDescriptionChars': len(NEW_DESC)})
    print('patched', rel, len(raw), '->', len(new_text.encode()))

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schema-annotation-patch.json')
json.dump(rows, open(out, 'w'), indent=2)
print('WROTE', out)
