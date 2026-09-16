"""R03 — R33-REC-02: execute the ROOT-AUTHORED optional selected-U missing-candidate full-Run
control against frozen33.

STANDING: this is a ROOT-AUTHORED control that I independently executed and whose output I verified.
It is NOT a new independent consumer implementation and not my own construction. I read the script
in full before running it: it transforms an exact reference fixture in memory, writes the before/after
copies into MY --out, never edits source, and records source hashes before and after.
"""
import hashlib, json, os, shutil, subprocess

BASE = '/tmp/opensip-design-corrections/claude-independent33-reconciliation.v1'
SRC = '/tmp/opensip-design-corrections/candidate-subject.v33'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v33.json'
OUT = os.path.join(BASE, 'receipts')
SCRIPT = os.path.join(BASE, 'root-optional-candidate-reference-control.py')
RUNOUT = os.path.join(BASE, 'fullrun-control-out')
PY = '/tmp/opensip-architecture-review-env/bin/python'
R = {'standing': ('root-authored control, independently executed by me; NOT a new independent '
                  'consumer implementation and NOT my own fixture construction')}

R['scriptSha256'] = hashlib.sha256(open(SCRIPT, 'rb').read()).hexdigest()
R['declaredScriptSha256'] = 'e32d15f09d79bf298613cfd81d43607ce4abd4df856b043ae894d495ae9f7572'
R['scriptShaMatchesDeclared'] = R['scriptSha256'] == R['declaredScriptSha256']
print('control script sha matches declared:', R['scriptShaMatchesDeclared'])
assert R['scriptShaMatchesDeclared'], 'refusing to run a script whose digest does not match'

man = {f['path']: f for f in json.load(open(MAN))['files']}


def drift():
    return sum(1 for p, f in man.items()
               if not os.path.isfile(os.path.join(SRC, p))
               or hashlib.sha256(open(os.path.join(SRC, p), 'rb').read()).hexdigest() != f['sha256'])


R['frozenDriftBefore'] = drift()
if os.path.isdir(RUNOUT):
    shutil.rmtree(RUNOUT)
r = subprocess.run([PY, '-I', '-B', SCRIPT, '--source', SRC, '--out', RUNOUT],
                   capture_output=True, text=True, timeout=3600)
R['returncode'] = r.returncode
R['stdout'] = r.stdout.strip()[-1500:]
R['stderrTail'] = (r.stderr or '')[-900:]
print('\ncontrol rc=%d' % r.returncode)
print(r.stdout.strip()[-1200:])
if r.returncode and r.stderr:
    print('--- stderr ---')
    print(r.stderr[-800:])
R['frozenDriftAfter'] = drift()
print('\nfrozen33 drift before/after: %d / %d' % (R['frozenDriftBefore'], R['frozenDriftAfter']))

rep = os.path.join(RUNOUT, 'report.json')
if os.path.isfile(rep):
    d = json.load(open(rep))
    R['report'] = {k: v for k, v in d.items() if k not in ('sourceBefore',)}
    R['structuralAdmission'] = d.get('structuralAdmission')
    R['semanticAdmission'] = d.get('semanticAdmission')
    R['runId'] = d.get('runId')
    R['verdict'] = d.get('verdict')
    R['executionDeficiencies'] = d.get('executionDeficiencies')
    R['candidateOutcome'] = d.get('candidateOutcome')
    R['sourceDrift'] = d.get('sourceDrift')
    R['passed'] = d.get('passed')
    print('\nstructuralAdmission :', R['structuralAdmission'])
    print('semanticAdmission   :', R['semanticAdmission'])
    print('runId               :', R['runId'])
    print('verdict             :', R['verdict'])
    print('executionDeficiencies:', json.dumps(R['executionDeficiencies'])[:200])
    print('candidate cell outcome:', json.dumps(R['candidateOutcome'])[:300])
    print('source drift reported by the control:', R['sourceDrift'])
    print('control passed      :', R['passed'])
    R['outputsWritten'] = sorted(os.listdir(RUNOUT))
    print('outputs written into my runtime:', R['outputsWritten'])

R['establishes'] = (
    'A FULL-RUN path for a SELECTED optional cell at a NON-NULL universe with NO retained candidate '
    'envelope and NO candidate reference: structural open_run_closure ADMIT, derive, seal, replay, and '
    'close_run equal to the replayed runId. The control additionally asserts the cell is not required, '
    'universe is non-null, enumeratorStatus is selected, candidateResultDigest is null, '
    'candidateResultRefs is empty, and the binding declares no deficiency or nativeCause — so no '
    'carrier was manufactured for the missing optional candidate.'
    if R.get('semanticAdmission') == 'ADMIT' else
    'NOT ESTABLISHED — see the recorded refusal/exception above; I claim nothing beyond it.')
R['doesNotEstablish'] = (
    'It is a synthetic reference fixture transformation, not provider, compiler, OS or host '
    'qualification, and not blind reconstruction. It says nothing about REQUIRED candidate cells, '
    'which still refuse EXECUTION_INPUTS_CANDIDATE_REQUIRED without an envelope.')
print('\nestablishes:', R['establishes'][:300])
json.dump(R, open(os.path.join(OUT, 'r03-fullruncontrol.json'), 'w'), indent=1, default=str)
print('\nwrote r03-fullruncontrol.json')
