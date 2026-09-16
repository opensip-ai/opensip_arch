"""Probe: can a per-TARGET universe be recovered from an admitted Run with today's
retained records, i.e. without any new identity version?

Repair targets are finding-key2 fingerprints, and the finding-fingerprint frame carries
NO universe. But finding3 also carries subjectId (subject3), and the evaluation-subject
frame DOES carry `universe`. If the Run retains the subject enumeration with its frames,
a target -> universe map is derivable from existing records.
"""
import json, importlib.util, sys
from pathlib import Path

SRC = Path('/tmp/opensip-design-corrections/candidate-subject.v31')
FOUND = SRC / 'docs/coop/design-corrections/foundation'
OUT = Path(__file__).resolve().parent / 'probe-target-universe.json'

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

P = load('probe_replay_check', FOUND / 'check-replay.v3.py')
F, R, M = P.F, P.R, P.M

report = {'scope': 'target -> universe recoverability', 'parts': []}
def step(name, **kw):
    row = {'part': name, **kw}
    report['parts'].append(row)
    print(json.dumps(row, default=str)[:1500])
    return row

# frame shapes, from the frozen identity schema
ids = json.loads((FOUND / 'identity-schemas.v3.json').read_text())
step('frame-shapes',
     findingFingerprintFrameFields=sorted(ids['$defs']['finding-fingerprint']['required']),
     findingFingerprintCarriesUniverse='universe' in ids['$defs']['finding-fingerprint']['properties'],
     evaluationSubjectFrameFields=sorted(ids['$defs']['evaluation-subject']['required']),
     evaluationSubjectCarriesUniverse='universe' in ids['$defs']['evaluation-subject']['properties'],
     findingDisplaySubjectFields=sorted(ids['$defs']['finding']['properties']['subject']['required']),
     findingRecordHasSubjectId='subjectId' in ids['$defs']['finding']['required'])

# a real admitted multi-universe Run
g = F.build_file_inputs(multiple_universes=True)
seed, objects, blobs, _ = F.seal_fixture(g)
_, owner = M.open_run_closure(seed, objects, blobs)
i = g['inputs']
result = R.derive(i['planId'], i['executionPlanId'], i['evaluatorClosure'],
                  i['evaluationInputRefs'], objects, blobs, owner)
run, objects, blobs = P.seal(g, result, objects, blobs)
run_id = M.close_run(run, objects, blobs)

evidence = objects[run['evidenceId']][1]
seal = objects[run['evaluationSealId']][1]
proof = objects[seal['proofBundleId']][1]

rows = []
for fid in evidence['findingIds']:
    finding = objects[fid][1]
    rows.append({'findingId': fid[:20], 'fingerprint': (finding['fingerprint'] or '')[:20],
                 'subjectId': finding['subjectId'][:20],
                 'displaySubjectKeys': sorted(finding['subject'].keys())})

subject_frames = sorted(proof.keys())
enum_sample = None
for key, value in proof.items():
    if isinstance(value, list) and value and isinstance(value[0], dict) and 'universe' in value[0]:
        enum_sample = {'field': key, 'memberKeys': sorted(value[0].keys()),
                       'carriesUniverse': True, 'count': len(value)}
        break

universes = set()
if enum_sample:
    for member in proof[enum_sample['field']]:
        if 'universe' in member:
            universes.add(member['universe'])

# and: are the subject3 preimage frames themselves retained as objects in the closure?
subject_objects = {k: v for k, (d, v) in objects.items() if d == 'evaluation-subject'}
subject_universes = sorted({v['universe'][:12] for v in subject_objects.values()})

step('retained-run',
     runId=run_id,
     findings=rows,
     proofFields=subject_frames,
     proofUniverseBearingEnumeration=enum_sample,
     distinctUniversesInThatEnumeration=len(universes),
     retainedEvaluationSubjectRecords=len(subject_objects),
     retainedSubjectUniverses=subject_universes,
     note='if the proof retains the subject enumeration with its universe, then '
          'target fingerprint -> finding3 -> subject3 frame -> universe is derivable '
          'from records that already exist')

# Negative check: is the subject3 record actually REQUIRED by the closure, or merely
# present in this fixture? Drop them and re-close the same Run.
import copy
pruned = {k: v for k, v in objects.items() if v[0] != 'evaluation-subject'}
try:
    M.close_run(copy.deepcopy(run), pruned, copy.deepcopy(blobs))
    dropped = 'ADMIT'
    detail = 'closure did not demand the subject3 records'
except Exception as exc:
    dropped = 'REFUSE'
    detail = type(exc).__name__ + ': ' + str(exc)[:180]
step('subject-records-required',
     withoutEvaluationSubjectRecords=dropped, detail=detail,
     note='decides whether target -> universe is derivable from records the closure '
          'GUARANTEES, or only from ones this fixture happened to retain')

OUT.write_text(json.dumps(report, indent=2, default=str) + '\n')
print('\nWROTE', OUT)
