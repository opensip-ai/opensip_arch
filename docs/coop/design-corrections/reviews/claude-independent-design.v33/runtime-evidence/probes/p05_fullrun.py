"""P05 — the full-Run column: does it actually assert exact proof ExecutionInputs digest equality,
and are these genuinely admitted Runs? Also extract the first-match precedence control in full."""
import json, os, re, subprocess

PY = '/tmp/opensip-architecture-review-env/bin/python'
KIT = '/tmp/opensip-design-corrections/claude-independent-design.v33/disposable/kit33'
SRC = '/tmp/opensip-design-corrections/candidate-subject.v33'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v33/receipts'
p = os.path.join(KIT, 'docs/coop/design-corrections/foundation/check-execution-inputs.v1.py')
r = subprocess.run([PY, '-I', '-B', p], capture_output=True, text=True, cwd=os.path.dirname(p))
d = json.loads(r.stdout)
R = {}

fr = [c for c in d['cases'] if c.get('fullRun')]
rows = []
for c in fr:
    f = c['fullRun']
    rows.append({'case': c['case'], 'innerCase': f.get('case'), 'runId': f.get('runId'),
                 'verdict': f.get('verdict'),
                 'executionCausePairs': f.get('executionCausePairs'),
                 'proofRefDigests': [x[1] for ref in (f.get('executionInputRefs') or []) for x in ref],
                 'sameGraphAdmissionResult': f.get('sameGraphAdmissionResult'),
                 'sameGraphExecutionInputsDigest': f.get('sameGraphExecutionInputsDigest'),
                 'keys': sorted(f)})
R['fullRunRows'] = rows
print('=== full-Run rows (%d) ===' % len(rows))
for x in rows:
    print('\n%s' % x['case'])
    print('   runId   : %s' % x['runId'])
    print('   verdict : %s' % x['verdict'])
    print('   causes  : %s' % json.dumps(x['executionCausePairs']))
    print('   proofRef: %s' % json.dumps(x['proofRefDigests'])[:120])
    print('   sameGraph: result=%s digest=%s' % (x['sameGraphAdmissionResult'],
                                                 str(x['sameGraphExecutionInputsDigest'])[:24]))
    print('   fields  : %s' % x['keys'])

R['allHaveRealRunIds'] = all(str(x['runId']).startswith('run3:') for x in rows)
R['allHaveProofRefDigest'] = all(x['proofRefDigests'] for x in rows)
R['digestEqualityAsserted'] = [x['case'] for x in rows if x['sameGraphExecutionInputsDigest']]
print('\nall full-Run rows carry a real run3 id      :', R['allHaveRealRunIds'])
print('all carry a proof ExecutionInputs ref digest:', R['allHaveProofRefDigest'])
print('rows asserting same-graph digest equality   :', len(R['digestEqualityAsserted']))

# does the CHECKER source assert equality between the proof ref digest and the recomputed digest?
src = open(os.path.join(SRC, 'docs/coop/design-corrections/foundation/check-execution-inputs.v1.py'),
           encoding='utf-8').read()
lines = [l.strip()[:190] for l in src.splitlines()
         if re.search(r'sameGraphExecutionInputsDigest|executionInputsDigest.*==|== *.*executionInputsDigest', l)]
R['checkerDigestEqualityLines'] = lines[:12]
print('\nchecker lines asserting ExecutionInputs digest equality:')
for l in lines[:10]:
    print('   %s' % l[:170])
R['checkerAssertsDigestEquality'] = bool(lines)

prec = next((c for c in d['cases'] if c.get('precedenceTable')), None)
R['precedenceControl'] = prec['precedenceTable'] if prec else None
print('\n=== first-match precedence control cases ===')
for row in (R['precedenceControl'] or []):
    ok = row.get('want') == row.get('got')
    print('   %-50s want=%-26s got=%-26s %s' % (row.get('case', '')[:50], row.get('want'),
                                                row.get('got'), 'OK' if ok else 'MISMATCH'))
R['precedenceAllMatch'] = all(x.get('want') == x.get('got') for x in (R['precedenceControl'] or []))
print('all precedence cases match:', R['precedenceAllMatch'])
json.dump(R, open(os.path.join(OUT, 'p05-fullrun.json'), 'w'), indent=1, default=str)
print('\nwrote p05-fullrun.json')
