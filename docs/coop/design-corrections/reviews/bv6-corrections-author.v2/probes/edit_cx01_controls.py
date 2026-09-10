"""CX-BV6-01 permanent full-Run controls, and CX-BV6-08 removal of the v1 prose-substring controls."""
import pathlib

P = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v2/work/'
                 'docs/coop/design-corrections/foundation/check-identity.py')
s = P.read_text(encoding='utf-8')

# ---- CX-BV6-08: drop the two prose-substring / wrapping controls added in v1 -------------------
OLD_PROSE = """# The two prose statements now name each other, so a reader arriving at either is not left to
# reconcile them, and the symbol-attribution limit is not restated as a re-derivation.
_IDENTITY_MD=(H.parents[2]/'v2/contracts/product-v1/identity-and-evidence.md').read_text(encoding='utf-8')
_NATIVE_MD=(H.parents[2]/'v2/contracts/product-v1/native-evidence.md').read_text(encoding='utf-8')
check('identity-section-3-defers-the-omission-half-to-the-coverage-totality-registry',
      'coverageTotality' in _IDENTITY_MD and 'Disjointness' in _IDENTITY_MD
      and 'not re-derivable from the' in _IDENTITY_MD.replace('**',''))
check('native-section-1-2-names-the-identity-clause-it-is-the-successor-to',
      'without overlaps or omissions' in _NATIVE_MD and 'disjointness' in _NATIVE_MD)
"""
NEW_PROSE = """# CX-BV6-08: the v1 revision of this block asserted PROSE SUBSTRINGS and was sensitive to hard
# wrapping; one of those assertions failed for a line break rather than for a semantic reason. Text
# agreement is not established by substring search, so those two controls are removed rather than
# repaired. What replaces them is the enforcement below: the disjointness half is now DECIDED at
# retained Run closure against the published key, so the reconciled wording is held by behaviour.
"""
assert s.count(OLD_PROSE) == 1
s = s.replace(OLD_PROSE, NEW_PROSE)

# ---- CX-BV6-01: full-Run partition controls, beside the totality ones -------------------------
ANCHOR = """check('the-disjointness-half-is-stated-over-the-full-owning-tuple',
      M.RELATIONS['file']['coverageTotality']['matchOn']
      ==['snapshotId','relation','resolution','sourceUniverse','targetUniverse'])
"""
NEW = '''check('the-disjointness-half-is-stated-over-the-full-owning-tuple',
      M.RELATIONS['file']['coverageTotality']['matchOn']
      ==['snapshotId','relation','resolution','sourceUniverse','targetUniverse'])
# ---------------------------------------------------------------------------------------------
# CX-BV6-01. The DISJOINTNESS half is now DECIDED here, not merely stated. The frozen reference
# admitted a complete Run carrying two subject-scopes of ONE view with the same snapshot, relation,
# rung and both universes whose subject sets intersected, so one subject was claimed twice under one
# interpretation and every count, completeness claim and universal negative over that view
# double-counted it. `admit_coverage_result_v3` admits ONE scope and cannot see a second, so this is
# decidable only where the whole view is held: retained Run closure. The key is the PUBLISHED
# coveragePartitionLaw.partitionKey, which is the same tuple coverageTotalityLaw matches facts on.
check('the-partition-key-is-published-and-equals-the-totality-match-key',
      M.COVERAGE_PARTITION_LAW['partitionKey']==M.RELATIONS['file']['coverageTotality']['matchOn']
      and M.COVERAGE_PARTITION_LAW['refusal']=='SUBJECT_SCOPE_PARTITION_OVERLAP')
def partition_run(mutate,with_coverage=True):
    """A lawful Run plus ONE more subject-scope in the same view, optionally with its own Coverage."""
    run,objects,blobs=build(resolved=True,has_match=True)
    original=copy.deepcopy(next(v for d,v in objects.values() if d=='subject-scope'))
    scope=copy.deepcopy(original);mutate(scope,original)
    sid=M.identifier('subject-scope',scope);objects[sid]=('subject-scope',scope)
    vid=objects[run['evidenceId']][1]['viewIds'][0];view=copy.deepcopy(objects[vid][1])
    cid=None
    if with_coverage:
        paths=[r['path'] for r in objects[run['snapshotId']][1]['sourceInventory']]
        payload=coverage_result(scope,scope['sourceUniverse'],True,blobs,paths)
        schema=next(v['payloadSchemaDigest'] for d,v in objects.values() if d=='coverage')
        if N.admit_coverage_result_v3(payload,scope,[],schema)['result']!='ADMIT':
            raise C.AdmissionError('FIXTURE_PARTITION_COVERAGE')
        coverage={'schemaVersion':2,'scopeId':sid,'payloadSchemaDigest':schema,
                  'payloadDigest':put_blob(blobs,payload)}
        cid=M.identifier('coverage',coverage);objects[cid]=('coverage',coverage)
        view['coverageIds'].append(cid)
    view['scopeIds'].append(sid);rekey(objects,vid,view,run)
    if cid:
        evidence=copy.deepcopy(objects[run['evidenceId']][1]);evidence['coverageIds'].append(cid)
        rekey(objects,run['evidenceId'],evidence,run)
    resync_witness(objects,blobs,run);resync_proof_refs(objects,blobs,run)
    return M.close_run(run,objects,blobs)
_OVERLAP=lambda s,o:s.update(subjects=sorted(set(o['subjects']+['independent-symbol'])))
# The counterexample root demonstrated on the frozen reference, now refused with its exact cause.
rejects_because('overlapping-scopes-of-one-view-in-one-partition-are-refused',
    lambda:partition_run(_OVERLAP),
    'SUBJECT_SCOPE_PARTITION_OVERLAP:references@resolved-binding:foo')
# A scope with NO Coverage entry reaches no other membership check, so it is exactly the case a
# single-Coverage producer could never see. It is partitioned too.
rejects_because('an-overlapping-scope-with-no-coverage-entry-is-still-refused',
    lambda:partition_run(_OVERLAP,with_coverage=False),
    'SUBJECT_SCOPE_PARTITION_OVERLAP:references@resolved-binding:foo')
# Everything lawful still closes. These are the regressions that would fire if the key were too
# coarse or the map were global rather than per view.
check('disjoint-scopes-in-one-partition-still-close-a-run',
      partition_run(lambda s,o:s.update(subjects=['independent-symbol'])).startswith('run2:'))
check('a-disjoint-scope-with-no-coverage-entry-still-closes-a-run',
      partition_run(lambda s,o:s.update(subjects=['independent-symbol']),
                    with_coverage=False).startswith('run2:'))
check('an-empty-subject-scope-is-not-an-overlap',
      partition_run(lambda s,o:s.update(subjects=[])).startswith('run2:'))
# A DIFFERENT relation and rung is a different claim about the same subject, not an overlap.
check('the-same-subject-under-a-different-relation-and-rung-is-not-an-overlap',
      partition_run(lambda s,o:s.update(relation='declares',resolution='syntactic',
                                        subjects=sorted(set(o['subjects']+['independent-symbol'])))
                    ).startswith('run2:'))
def same_scope_two_views():
    """PER-VIEW ISOLATION. One scope referenced by TWO views of one Run. A global partition map
    would call this an overlap of the scope with itself; the law is per view because a view is one
    producer's interpretation, and two views legitimately share a scope."""
    run,objects,blobs=build(resolved=True,has_match=True)
    sid=next(k for k,(d,v) in objects.items() if d=='subject-scope')
    vid=objects[run['evidenceId']][1]['viewIds'][0]
    other=copy.deepcopy(objects[vid][1]);other['scopeIds']=[sid]
    other['coverageIds']=[];other['facts']=[]
    ovid=M.identifier('view',other);objects[ovid]=('view',other)
    evidence=copy.deepcopy(objects[run['evidenceId']][1])
    evidence['viewIds']=sorted(set(evidence['viewIds']+[ovid]))
    rekey(objects,run['evidenceId'],evidence,run)
    pkey=objects[run['evaluationSealId']][1]['proofBundleId'];proof=copy.deepcopy(objects[pkey][1])
    proof['evaluationInputRefs'].append({'domain':'view','digest':ovid.split(':')[1]})
    rekey(objects,pkey,proof,run)
    resync_witness(objects,blobs,run);resync_proof_refs(objects,blobs,run)
    return M.close_run(run,objects,blobs)
check('one-scope-referenced-by-two-views-of-one-run-is-not-an-overlap',
      same_scope_two_views().startswith('run2:'))
'''
assert s.count(ANCHOR) == 1
s = s.replace(ANCHOR, NEW)
P.write_text(s, encoding='utf-8')
print('ok')
