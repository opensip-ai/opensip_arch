"""Disposable: build the M-1 subject-scope / coverage-admission fixtures and expected values."""
import hashlib, importlib.util, json, sys
from pathlib import Path
R = Path(sys.argv[1]); N = R / 'docs/coop/design-corrections/native'
spec = importlib.util.spec_from_file_location('m', N / 'native_evidence_model.v2.py')
M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
h = lambda s: hashlib.sha256(s.encode()).hexdigest()

SNAP = 'snapshot2:' + h('snapshot')
SRC = h('ts-universe'); TGT = SRC
ENUM = 'closure2:' + h('enumerator')
SUBJECTS = ['src/a.ts#bar', 'src/a.ts#foo', 'src/b.ts#main']

desc = M.subject_scope_descriptor(SNAP, 'references', 'resolved-binding', SRC, TGT, ENUM, SUBJECTS)
com = M.subject_scope_commitment(desc)

def entry(state='complete', count=0, classes=(), coverage='complete', terminal='complete', exhaustive=True, attempted=True):
    return {'relation': 'references', 'resolution': 'resolved-binding', 'coverage': coverage,
            'examinedUniverse': {'subjectScopeCommitment': com['subjectScopeCommitment'], 'subjectCount': len(SUBJECTS)},
            'resolutionCompleteness': {'state': state, 'attempted': attempted, 'examinedExhaustive': exhaustive,
                                       'stageTerminal': terminal, 'unresolvedEdgeCount': count,
                                       'unresolvedEdgeClasses': sorted(classes)},
            'closedWorld': {'exportsClosed': 'closed', 'entryPointsRecognized': 'all', 'nonliteralLoading': 'none',
                            'externalConsumers': 'none-declared', 'dynamicDispatch': 'not-applicable',
                            'reasons': [], 'deadCodeRepairEligible': True},
            'derivationKinds': [], 'confidenceMillionths': 1000000, 'deficiency': None, 'nativeCause': None}

payload = {'schemaVersion': 3,
           'key': {'relation': 'references', 'resolution': 'resolved-binding', 'sourceUniverse': SRC,
                   'targetUniverse': TGT, 'subjectScopeCommitment': com['subjectScopeCommitment']},
           'entry': entry()}
ok = M.admit_coverage_result_v3(payload, desc, [])

forged = json.loads(json.dumps(payload))
forged['key']['subjectScopeCommitment'] = 'sha256:' + h('claimant-chosen')
forged['entry']['examinedUniverse']['subjectScopeCommitment'] = forged['key']['subjectScopeCommitment']
bad_commit = M.admit_coverage_result_v3(forged, desc, [])

narrowed = M.subject_scope_descriptor(SNAP, 'references', 'resolved-binding', SRC, TGT, ENUM, SUBJECTS[:2])
narrowed_com = M.subject_scope_commitment(narrowed)
narrowed_payload = json.loads(json.dumps(payload))
narrowed_payload['key']['subjectScopeCommitment'] = narrowed_com['subjectScopeCommitment']
narrowed_payload['entry']['examinedUniverse'] = {'subjectScopeCommitment': narrowed_com['subjectScopeCommitment'],
                                                 'subjectCount': 2}
producer_subset = M.admit_coverage_result_v3(narrowed_payload, desc, [])

count_lie = json.loads(json.dumps(payload)); count_lie['entry']['examinedUniverse']['subjectCount'] = 99
count_out = M.admit_coverage_result_v3(count_lie, desc, [])

key_scope = json.loads(json.dumps(payload)); key_scope['key']['targetUniverse'] = h('other-universe')
key_out = M.admit_coverage_result_v3(key_scope, desc, [])

edge = {'relation': 'references', 'referrer': 'src/b.ts#main', 'edgeKind': 'computed-member-access'}
incomplete_payload = json.loads(json.dumps(payload))
incomplete_payload['entry'] = entry(state='incomplete', count=1, classes=['computed-member-access'])
incomplete = M.admit_coverage_result_v3(incomplete_payload, desc, [edge])
lying = json.loads(json.dumps(payload))
lying_rc = M.admit_coverage_result_v3(lying, desc, [edge])   # claims complete while an edge is admitted

# the same subject set under a different snapshot mints a different commitment (identity join)
other_desc = M.subject_scope_descriptor('snapshot2:' + h('other-snapshot'), 'references', 'resolved-binding',
                                        SRC, TGT, ENUM, SUBJECTS)
other_com = M.subject_scope_commitment(other_desc)

view = {'schemaVersion': 2, 'planId': 'plan2:' + h('plan'),
        'scopeIds': [com['scopeId']], 'facts': [], 'coverageIds': [ok['coverageId']],
        'producerClosure': 'closure2:' + h('producer'), 'schemaDigests': [M.schema_document_digest(M.NATIVE_SCHEMA_DOC)]}
use_ok = M.coverage_view_use(view, [ok])
foreign_view = dict(view, scopeIds=[other_com['scopeId']])
use_bad = M.coverage_view_use(foreign_view, [ok])
unadmitted_view = dict(view, coverageIds=['coverage2:' + h('unadmitted')])
use_unadmitted = M.coverage_view_use(unadmitted_view, [ok])

print(json.dumps({'snapshot': SNAP, 'sourceUniverse': SRC, 'enumeratorClosure': ENUM, 'subjects': SUBJECTS,
                  'descriptor': desc, 'commitment': com, 'otherCommitment': other_com,
                  'payload': payload, 'admit': ok,
                  'forgedCommitment': bad_commit, 'producerSubset': producer_subset,
                  'countLie': count_out, 'keyScope': key_out,
                  'incompletePayload': incomplete_payload, 'incomplete': incomplete, 'lyingComplete': lying_rc,
                  'view': view, 'useOk': use_ok, 'useForeign': use_bad, 'useUnadmitted': use_unadmitted,
                  'schemaDocumentDigest': M.schema_document_digest(M.NATIVE_SCHEMA_DOC)}, indent=1))
