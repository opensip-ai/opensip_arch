"""CX-BV6-01: publish coveragePartitionLaw in the relation registry and ENFORCE it at retained
Run closure. Root's one-file proposal is the reference; two boundary choices differ (authority
location and fault attribution order) and are argued in assessment.md."""
import json, pathlib, collections

W = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v2/work')

# ---------------------------------------------------------------- 1. the published law
P = W / 'docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json'
raw = P.read_text(encoding='utf-8')
d = json.loads(raw, object_pairs_hook=collections.OrderedDict)
reg = d['x-opensip-relation-registry']
assert 'coveragePartitionLaw' not in reg

law = collections.OrderedDict()
law['standing'] = (
    "Normative and CLOSED. The DISJOINTNESS half of identity-and-evidence section 3's `Coverage "
    "scopes partition the claimed universe without overlaps or omissions`. The OMISSION half is "
    "coverageTotalityLaw above and is owed only where a relation carries a coverageTotality row. "
    "These two halves have different owners and different decidability, and neither implies the "
    "other."
)
law['whyItIsNeeded'] = (
    "The clause was stated and nothing derived or compared it. A retained Run could carry two "
    "subject-scopes of ONE view with the same snapshot, relation, rung and both universes, whose "
    "subject sets intersect, and close: the same subject was then claimed twice under one "
    "interpretation, and any count, completeness claim or universal negative read over that view "
    "double-counted it. This is the same defect class as the frozen-reference file@enumerated "
    "omission: a published law with no deciding boundary."
)
law['partitionKey'] = ['snapshotId', 'relation', 'resolution', 'sourceUniverse', 'targetUniverse']
law['keyRule'] = (
    "Two subject-scopes of the same view are in the same partition exactly when they agree on EVERY "
    "field of partitionKey. Within one partition their `subjects` arrays must be pairwise disjoint. "
    "Scopes in DIFFERENT partitions may name the same subject freely: a different relation, a "
    "different rung or a different universe is a different claim about that subject, not an overlap. "
    "This is the same tuple coverageTotalityLaw uses for `matchOn`, deliberately, so the key that "
    "decides which fact discharges a scope's obligation is the key that decides which scopes are "
    "comparable at all."
)
law['snapshotIsListedDeliberately'] = (
    "Run closure independently requires every subject-scope to carry the Run's own snapshotId, so "
    "within one admitted Run this field is constant and listing it changes no outcome today. It is "
    "listed for the same reason coverageTotalityLaw lists it: this law reads a property of a SHARED "
    "view, and a join that silently depends on an invariant enforced elsewhere is the implicit "
    "coupling both laws exist to remove."
)
law['scope'] = (
    "PER VIEW, over every subject-scope the view references - INCLUDING scopes that carry no "
    "Coverage entry. A scope with no Coverage reaches no other membership check at all, so a "
    "Coverage-keyed traversal would miss exactly the case that has no other guard. Distinct views "
    "of one Run may reference the SAME scope, and that is not an overlap: a view is one producer's "
    "interpretation, and the partition is a property of that interpretation."
)
law['whatRemainsAllowed'] = [
    "the same scope referenced by two different views of one Run",
    "the same subject in two scopes that differ on any partitionKey field",
    "a scope with no Coverage entry, which is still partitioned",
    "lawful partial, not-attempted and unknown Coverage states, which this law does not read",
    "an empty subjects array",
]
law['producerCannotDecideThis'] = (
    "admit_coverage_result_v3 admits ONE scope and its ONE Coverage entry and cannot see a second "
    "scope, so it cannot decide a between-scopes property and is not asked to. The authoritative "
    "boundary is retained Run closure, which holds the whole view. No host effect, provider call or "
    "protocol invocation is introduced by this law."
)
law['refusal'] = 'SUBJECT_SCOPE_PARTITION_OVERLAP'
law['refusalShape'] = (
    "SUBJECT_SCOPE_PARTITION_OVERLAP:<relation>@<rung>:<first overlapping subject in canonical "
    "order>, matching the COVERAGE_INVENTORY_TOTALITY_OMITS_PATH shape. It is an internal admission "
    "refusal: no public DomainDetailCode, no D9 class, exit or error code is added or changed."
)
law['enforcedAt'] = (
    "identity-model close_run, per view, AFTER each scope's own well-formedness checks "
    "(SCOPE_SOURCE_JOIN, UNSELECTED_ENUMERATOR, ENUMERATOR_CLOSURE_KIND) have run for every scope of "
    "that view, so a malformed scope refuses as ITSELF and the overlap refusal is never counted as "
    "coverage of a different fault. The key is READ from partitionKey here, never restated in code."
)

# insert immediately after coverageTotalityLaw
out = collections.OrderedDict()
for k, v in reg.items():
    out[k] = v
    if k == 'coverageTotalityLaw':
        out['coveragePartitionLaw'] = law
d['x-opensip-relation-registry'] = out
P.write_text(json.dumps(d, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

# ---------------------------------------------------------------- 2. enforce it
Q = W / 'docs/coop/design-corrections/foundation/identity-model.py'
s = Q.read_text(encoding='utf-8')

OLD_LOAD = "RELATION_DIGEST_LAW=RELATION_DOCUMENT['x-opensip-digest-law']\n"
NEW_LOAD = ("RELATION_DIGEST_LAW=RELATION_DOCUMENT['x-opensip-digest-law']\n"
            "# The DISJOINTNESS half of identity section 3, read from its published law rather than\n"
            "# restated: which fields make two subject-scopes of one view comparable at all. It is the\n"
            "# same tuple coverageTotalityLaw matches facts on, so the key that decides which fact\n"
            "# discharges a scope's obligation is the key that decides which scopes may not overlap.\n"
            "COVERAGE_PARTITION_LAW=RELATION_DOCUMENT['x-opensip-relation-registry']['coveragePartitionLaw']\n")
assert s.count(OLD_LOAD) == 1
s = s.replace(OLD_LOAD, NEW_LOAD)

OLD = """        for scope_id in view['scopeIds']:
            scope=get(scope_id,'subject-scope')
            if scope['snapshotId']!=run['snapshotId']:raise C.AdmissionError('SCOPE_SOURCE_JOIN')
            if scope['enumeratorClosure'] not in plan['semanticClosures']:raise C.AdmissionError('UNSELECTED_ENUMERATOR')
            if get(scope['enumeratorClosure'],'closure')['kind']!=DIGESTS['closureKinds']['byField']['subject-scope.enumeratorClosure']:
                raise C.AdmissionError('ENUMERATOR_CLOSURE_KIND')
"""
NEW = """        for scope_id in view['scopeIds']:
            scope=get(scope_id,'subject-scope')
            if scope['snapshotId']!=run['snapshotId']:raise C.AdmissionError('SCOPE_SOURCE_JOIN')
            if scope['enumeratorClosure'] not in plan['semanticClosures']:raise C.AdmissionError('UNSELECTED_ENUMERATOR')
            if get(scope['enumeratorClosure'],'closure')['kind']!=DIGESTS['closureKinds']['byField']['subject-scope.enumeratorClosure']:
                raise C.AdmissionError('ENUMERATOR_CLOSURE_KIND')
        # Identity section 3's DISJOINTNESS half, decided here because only this boundary holds the
        # whole view. `admit_coverage_result_v3` admits ONE scope and its ONE Coverage entry, so it
        # cannot see a second scope and cannot decide a between-scopes property; a stated law that
        # nothing compares is the defect this closes. Two scopes are comparable exactly when they
        # agree on every field of the PUBLISHED partition key; a different relation, rung or universe
        # is a different claim about the subject, not an overlap. This runs AFTER every scope of the
        # view has passed its own well-formedness checks above, so a foreign-snapshot or unselected
        # enumerator refuses as ITSELF and an overlap refusal is never miscounted as covering it.
        # Scopes with NO Coverage entry are included deliberately: they reach no other membership
        # check. The map is per VIEW, so two views of one Run may reference the same scope.
        partition_subjects={}
        for scope_id in view['scopeIds']:
            scope=get(scope_id,'subject-scope')
            partition=tuple(scope[field] for field in COVERAGE_PARTITION_LAW['partitionKey'])
            seen=partition_subjects.setdefault(partition,set())
            overlapping=seen.intersection(scope['subjects'])
            if overlapping:
                raise C.AdmissionError(COVERAGE_PARTITION_LAW['refusal']+':'+scope['relation']+'@'
                                       +scope['resolution']+':'+sorted(overlapping)[0])
            seen.update(scope['subjects'])
"""
assert s.count(OLD) == 1
s = s.replace(OLD, NEW)
Q.write_text(s, encoding='utf-8')
print('ok')
