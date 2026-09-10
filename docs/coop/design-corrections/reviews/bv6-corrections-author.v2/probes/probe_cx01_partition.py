"""Develop the CX-BV6-01 full-Run partition controls against the corrected bytes.
Run: python -I -B probe_cx01_partition.py <work-root>"""
import copy, importlib.util, json, sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
H = ROOT / 'docs/coop/design-corrections/foundation'
spec = importlib.util.spec_from_file_location('ck', H / 'check-identity.py')
# check-identity runs its whole suite on import; instead load the pieces we need the same way it does.
def load(name, path):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

F = load('fx', ROOT / 'docs/coop/design-corrections/integration-fixtures.py')
M, C, N = F.M, F.M.C, F.N

rows = []

def second_scope_run(mutate, with_coverage=True, second_view=False):
    """Build a lawful Run, then add ONE more subject-scope to the same view (optionally with its
    own Coverage, optionally in a second view) and close."""
    run, objects, blobs = F.build(resolved=True, has_match=True)
    original = copy.deepcopy(next(v for d, v in objects.values() if d == 'subject-scope'))
    scope = copy.deepcopy(original)
    mutate(scope, original)
    sid = M.identifier('subject-scope', scope); objects[sid] = ('subject-scope', scope)
    vid = objects[run['evidenceId']][1]['viewIds'][0]
    view = copy.deepcopy(objects[vid][1])
    cid = None
    if with_coverage:
        paths = [r['path'] for r in objects[run['snapshotId']][1]['sourceInventory']]
        payload = F.coverage_result(scope, scope['sourceUniverse'], True, blobs, paths)
        schema = next(v['payloadSchemaDigest'] for d, v in objects.values() if d == 'coverage')
        producer = N.admit_coverage_result_v3(payload, scope, [], schema)
        if producer['result'] != 'ADMIT':
            raise RuntimeError('fixture second coverage refused: ' + json.dumps(producer))
        coverage = {'schemaVersion': 2, 'scopeId': sid, 'payloadSchemaDigest': schema,
                    'payloadDigest': F.put_blob(blobs, payload)}
        cid = M.identifier('coverage', coverage); objects[cid] = ('coverage', coverage)
    if second_view:
        other = copy.deepcopy(view)
        other['scopeIds'] = [sid]; other['coverageIds'] = [cid] if cid else []; other['facts'] = []
        ovid = M.identifier('view', other); objects[ovid] = ('view', other)
        evidence = copy.deepcopy(objects[run['evidenceId']][1])
        evidence['viewIds'] = sorted(evidence['viewIds'] + [ovid])
        if cid: evidence['coverageIds'].append(cid)
        F.rekey(objects, run['evidenceId'], evidence, run)
    else:
        view['scopeIds'].append(sid)
        if cid: view['coverageIds'].append(cid)
        F.rekey(objects, vid, view, run)
        evidence = copy.deepcopy(objects[run['evidenceId']][1])
        if cid: evidence['coverageIds'].append(cid)
        F.rekey(objects, run['evidenceId'], evidence, run)
    F.resync_witness(objects, blobs, run); F.resync_proof_refs(objects, blobs, run)
    return M.close_run(run, objects, blobs)

def case(label, mutate, expect, **kw):
    try:
        rid = second_scope_run(mutate, **kw)
        rows.append({'case': label, 'expect': expect, 'actual': 'ADMIT', 'runId': rid})
    except Exception as exc:
        rows.append({'case': label, 'expect': expect, 'actual': 'REFUSE',
                     'error': type(exc).__name__ + ':' + str(exc)})

case('disjoint-same-partition',
     lambda s, o: s.update(subjects=['independent-symbol']), 'ADMIT')
case('overlap-same-partition',
     lambda s, o: s.update(subjects=sorted(set(o['subjects'] + ['independent-symbol']))), 'REFUSE')
case('overlap-different-relation',
     lambda s, o: s.update(relation='declares', resolution='syntactic',
                           subjects=sorted(set(o['subjects'] + ['independent-symbol']))), 'ADMIT')
case('overlap-no-coverage-entry',
     lambda s, o: s.update(subjects=sorted(set(o['subjects'] + ['independent-symbol']))),
     'REFUSE', with_coverage=False)
case('disjoint-no-coverage-entry',
     lambda s, o: s.update(subjects=['independent-symbol']), 'ADMIT', with_coverage=False)
def same_scope_in_two_views():
    """PER-VIEW ISOLATION. The SAME existing scope is referenced by a second view of the same
    Run. A global partition map would call that an overlap with itself; a per-view map admits it,
    which is required because a view is one producer's interpretation.

    The first attempt (retained in evidence/) minted a SECOND scope with identical subjects, which
    is the same content and therefore the same identity, so its Coverage id duplicated inside
    evidence.coverageIds and the run refused on uniqueItems before reaching the partition law. That
    was a harness defect, not a design result."""
    run, objects, blobs = F.build(resolved=True, has_match=True)
    sid = next(k for k, (d, v) in objects.items() if d == 'subject-scope')
    vid = objects[run['evidenceId']][1]['viewIds'][0]
    other = copy.deepcopy(objects[vid][1])
    other['scopeIds'] = [sid]; other['coverageIds'] = []; other['facts'] = []
    ovid = M.identifier('view', other); objects[ovid] = ('view', other)
    evidence = copy.deepcopy(objects[run['evidenceId']][1])
    evidence['viewIds'] = sorted(set(evidence['viewIds'] + [ovid]))
    F.rekey(objects, run['evidenceId'], evidence, run)
    # EVALUATION_VIEW_ROOTS requires the proof to name every view of the evidence, so the second
    # view must be a real evaluation input rather than an orphan appended to the evidence.
    pkey = objects[run['evaluationSealId']][1]['proofBundleId']
    proof = copy.deepcopy(objects[pkey][1])
    proof['evaluationInputRefs'].append({'domain': 'view', 'digest': ovid.split(':')[1]})
    F.rekey(objects, pkey, proof, run)
    F.resync_witness(objects, blobs, run); F.resync_proof_refs(objects, blobs, run)
    return M.close_run(run, objects, blobs)

try:
    rows.append({'case': 'same-scope-in-two-views', 'expect': 'ADMIT', 'actual': 'ADMIT',
                 'runId': same_scope_in_two_views()})
except Exception as exc:
    rows.append({'case': 'same-scope-in-two-views', 'expect': 'ADMIT', 'actual': 'REFUSE',
                 'error': type(exc).__name__ + ':' + str(exc)})
case('empty-subjects-second-scope',
     lambda s, o: s.update(subjects=[]), 'ADMIT')

print(json.dumps({'sourceRoot': str(ROOT), 'cases': rows}, indent=1))
