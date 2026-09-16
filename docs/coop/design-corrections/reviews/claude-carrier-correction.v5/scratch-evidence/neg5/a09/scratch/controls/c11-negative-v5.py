# Control C11 - negative controls for the v4 additions.
#
# Two kinds, because a control that cannot fail proves nothing:
#   A. MODEL drifts - reintroduce the exact bug each schedule/gate control was written to catch,
#      and assert the control now reports violations.
#   B. ARTIFACT drifts - break an owner patch or artifact invariant and assert the reference
#      validator rejects it.
#
# Everything happens in scratch/neg4 sandboxes. The real trees are never written.
#
# usage: python c11-negative-v4.py <source25Root> <runtimeRoot> <reportPath>
import json
import os
import shutil
import subprocess
import sys

SRC, ROOT, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
NEG = os.path.join(ROOT, 'scratch', 'neg5')
EXE = sys.executable

# --------------------------------------------------------------- A. model drifts
MODEL_DRIFTS = [
    ('A1 reader reports an adverse condition without any stability gate',
     'scratch/controls/c6-schedules.py',
     "            if isCorruptionClaim and not (cap['stableW'] and cap['stableH'] and stableTail):\n"
     "                cover['skewSuppressedCorruptionClaim'] = True\n"
     "                return 'unavailable-busy'\n",
     '',
     'false-quarantine-from-lawful-writer'),
    ('A2 corruption gate keeps the brackets but drops the two-agreeing-tails requirement',
     'scratch/controls/c6-schedules.py',
     "            if isCorruptionClaim and not (cap['stableW'] and cap['stableH'] and stableTail):",
     "            if isCorruptionClaim and not (cap['stableW'] and cap['stableH']):",
     'false-quarantine-from-lawful-writer'),
    ('A3 reader treats ANY absent receipt as terminal absence (the v1 behaviour)',
     'scratch/controls/c6-schedules.py',
     "    if k is None:\n"
     "        if cust is None:\n"
     "            return 'unknown-attempt-unobserved'\n"
     "        if phase == 'admitted':\n"
     "            return 'unknown-attempt-open'\n"
     "        if outcome == 'refused':\n"
     "            return 'terminal-not-committed'\n"
     "        return 'unknown-custody'\n",
     "    if k is None:\n"
     "        return 'terminal-not-committed'\n",
     'false-terminal-not-committed'),
    ('A4 observer stores LATCHED instead of fetch-ORing it, losing ADMITTED',
     'scratch/controls/c7-gate-bits.py',
     '        self.state |= LATCHED\n',
     '        self.state = LATCHED\n',
     'latched'),
    ('A5 the commit permit is reusable',
     'scratch/controls/c7-gate-bits.py',
     "        if self.permit != 'unused':\n"
     "            self.events.append('commit refused: no unused permit')\n"
     "            return False\n",
     '        pass\n',
     'permit reused by a retry'),
    ('A6 state 3 relabels a confirmed commit as uncommitted',
     'scratch/controls/c7-gate-bits.py',
     "    if a.state & LATCHED:\n"
     "        return {'standing': 'committed-delivery-failed',\n",
     "    if a.state & LATCHED:\n"
     "        return {'standing': 'uncommitted',\n",
     'state 3 relabelled a confirmed commit'),
    ('A8 the reader ignores the receipt-present-but-unsettled contradiction (conservative policy)',
     'scratch/controls/c6-schedules.py',
     "    if phase == 'admitted' or outcome == 'refused':\n"
     "        return 'unknown-custody'\n",
     '',
     'committed-without-receipt-in-snapshot'),
    ('A9 the settlement matrix lets settled+committed with no receipt be a negative',
     'scratch/controls/c14-settlement.py',
     "        if o == 'refused':\n"
     "            return 'terminal-not-committed'\n"
     "        return 'unknown-custody'          # settled+committed with no receipt: contradiction\n",
     "        return 'terminal-not-committed'\n",
     'exactly one matrix cell yields the negative conclusion'),
    ('A10 the sweep writes while a writer may still be live',
     'scratch/controls/c14-settlement.py',
     "    if not leaseFree:\n        return 'no-write:skip-and-retain'\n",
     '',
     'sweep case: live writer'),
    ('A11 migration detection is keyed on the tables instead of the format row',
     'scratch/controls/c13-migration-prefixes.py',
     "    if 'grant_journal_v3' in n and format_row(c) is not None:\n        return 3\n",
     "    if 'grant_journal_v3' in n:\n        return 3\n",
     'prefix recovery is exact'),
    ('A12 first_generation is fixed early instead of recomputed at act C',
     'scratch/controls/c13-migration-prefixes.py',
     "    mx = c.execute('SELECT COALESCE(MAX(grantGeneration),0) FROM grant_journal').fetchone()[0]\n",
     "    mx = gen\n",
     'first_generation recomputed'),
    ('A7 required delivery is started from a latched attempt',
     'scratch/controls/c7-gate-bits.py',
     "        if self.state & LATCHED:\n"
     "            self.events.append('delivery phase not started: attempt is latched/cancelling')\n"
     "            return False\n",
     '        pass\n',
     'delivery started while latched'),
]

results = []
for i, (name, rel, old, new, expect) in enumerate(MODEL_DRIFTS):
    sand = os.path.join(NEG, 'a%02d' % i)
    if os.path.isdir(sand):
        shutil.rmtree(sand)
    os.makedirs(os.path.join(sand, 'scratch', 'out'), exist_ok=True)
    shutil.copytree(os.path.join(ROOT, 'scratch', 'controls'),
                    os.path.join(sand, 'scratch', 'controls'))
    target = os.path.join(sand, rel)
    txt = open(target, encoding='utf-8').read()
    if txt.count(old) != 1:
        results.append({'drift': name, 'kind': 'model', 'anchorOccurrences': txt.count(old),
                        'detected': None, 'error': 'drift anchor not unique'})
        continue
    open(target, 'w', encoding='utf-8').write(txt.replace(old, new))
    # the proposal tree is needed by c13 and c14, which read the DDL and the record shape
    if not os.path.isdir(os.path.join(sand, 'scratch', 'proposal')):
        shutil.copytree(os.path.join(ROOT, 'scratch', 'proposal'),
                        os.path.join(sand, 'scratch', 'proposal'))
    rep = os.path.join(sand, 'scratch', 'out', 'drift.json')
    V3SQL = 'scratch/proposal/docs/coop/design-corrections/security/grant-journal.carrier.v3.sql'
    if 'c13-' in rel:
        argv = [SRC, V3SQL, rep]
    elif 'c14-' in rel:
        argv = [sand, rep]
    else:
        argv = [rep]
    r = subprocess.run([EXE, target] + argv, capture_output=True, text=True, cwd=sand)
    detected, count, how = None, None, ''
    if r.returncode != 0:
        detected, how = True, 'control crashed on the drifted model'
    elif os.path.exists(rep):
        d = json.load(open(rep, encoding='utf-8'))
        count = d.get('violationCount', d.get('failed', len(d.get('violations', []))))
        blob = json.dumps(d)
        detected = count > 0
        how = ('violations reported' if count else 'no violations') + \
              ('; expected marker present' if expect in blob else '; expected marker ABSENT')
    results.append({'drift': name, 'kind': 'model', 'path': rel, 'expectedMarker': expect,
                    'violationCount': count, 'detected': bool(detected), 'how': how})

# ----------------------------------------------------------- B. artifact drifts
ARTIFACT_DRIFTS = [
    ("B1 root's F32 typed-route fix is overwritten",
     'commit-recovery-plan.v1.json',
     'Storage returns CarrierCapacityExhausted {grantGeneration, provenTailSeq} to '
     'host/finalization.rs.',
     'Pause or close the generation through the owner lifecycle.'),
    ('B2 an unregistered errorCode is introduced into the S12 projection',
     'scratch/controls/apply-owner-patches.py',
     "'4 / `LEDGER.CORRUPT`, `faultCause` `ledger-corrupt`, **`domainDetail` omitted** |\\n'",
     "'4 / `RECOVERY.CARRIER_SKEW`, `faultCause` `ledger-corrupt` |\\n'"),
    ('B3 the added case ids are no longer sequential',
     'scratch/proposal/carrier-fault-cases.v1.json',
     '"id": "F53"',
     '"id": "F39b"'),
    ('B4 the attempt-custody record is opened to unknown members',
     'scratch/proposal/attempt-custody.schema.v1.json',
     '"additionalProperties": false,',
     '"additionalProperties": true,'),
    ('B5 the attempt-custody phase is no longer monotone two-valued',
     'scratch/proposal/attempt-custody.schema.v1.json',
     '"enum": ["admitted", "settled"]',
     '"enum": ["admitted", "settled", "reopened"]'),
    ('B6 the narrow assurance limit is removed from the identity patch',
     'scratch/controls/apply-owner-patches.py',
     "    'is therefore `confirmed-under-retained-custody`, never a cryptographic proof, and an "
     "unmet\\n'",
     "    'is therefore a cryptographic proof of the retained prefix, and an unmet\\n'"),
    ('B7 the identity patch reintroduces an in-memory liveness check',
     'scratch/controls/apply-owner-patches.py',
     'never from a separately timed liveness probe or an in-memory\\n',
     'after confirming the attempt is absent from the active set and an in-memory\\n'),
]

for i, (name, rel, old, new) in enumerate(ARTIFACT_DRIFTS):
    sand = os.path.join(NEG, 'b%02d' % i)
    if os.path.isdir(sand):
        shutil.rmtree(sand)
    os.makedirs(sand)
    for sub in ('scratch/proposal', 'scratch/controls'):
        shutil.copytree(os.path.join(ROOT, sub), os.path.join(sand, sub))
    PLANROOT = '/tmp/opensip-design-corrections/claude-carrier-correction.v4'
    for f in ('commit-recovery-plan.v1.json', 'implementation-boundaries-and-build-plan.md'):
        shutil.copy2(os.path.join(PLANROOT, f), os.path.join(sand, f))
    os.makedirs(os.path.join(sand, 'scratch', 'out'), exist_ok=True)
    # the validator reads the model reports; copy the real ones so the only difference is the drift
    for f in ('c6.json', 'c7.json', 'c12.json', 'c13.json', 'c14.json'):
        shutil.copy2(os.path.join(ROOT, 'scratch', 'out', f),
                     os.path.join(sand, 'scratch', 'out', f))
    target = os.path.join(sand, rel)
    txt = open(target, encoding='utf-8').read()
    if txt.count(old) != 1:
        results.append({'drift': name, 'kind': 'artifact', 'anchorOccurrences': txt.count(old),
                        'detected': None, 'error': 'drift anchor not unique'})
        continue
    open(target, 'w', encoding='utf-8').write(txt.replace(old, new))
    # re-apply the patches inside the sandbox, then validate
    # PLANROOT is the sandbox itself, so a drifted planning-input copy is actually the input
    ap = subprocess.run([EXE, os.path.join(sand, 'scratch/controls/apply-owner-patches.py'),
                         SRC, sand, sand], capture_output=True, text=True, cwd=sand)
    if ap.returncode != 0:
        results.append({'drift': name, 'kind': 'artifact', 'path': rel, 'detected': True,
                        'how': 'patch application refused the drift: '
                               + ap.stderr.strip().splitlines()[-1][:150]})
        continue
    rep = os.path.join(sand, 'scratch', 'out', 'neg.json')
    r = subprocess.run([EXE, os.path.join(sand, 'scratch/controls/check-correction-v5.py'),
                        SRC, sand, rep], capture_output=True, text=True, cwd=sand)
    failed = None
    if os.path.exists(rep):
        failed = json.load(open(rep, encoding='utf-8'))['failed']
    results.append({'drift': name, 'kind': 'artifact', 'path': rel,
                    'validatorExit': r.returncode, 'validatorFailedChecks': failed,
                    'detected': bool(failed) or r.returncode != 0,
                    'cleanFailure': bool(failed) and r.returncode == 0,
                    'stderrTail': r.stderr.strip().splitlines()[-1][:160] if r.returncode else '',
                    'how': ('validator reported %s failed checks' % failed) if failed
                           else ('validator crashed' if r.returncode else 'NOT DETECTED')})

undetected = [x['drift'] for x in results if not x.get('detected')]
rep = {'control': 'c11-negative-v4',
       'modelDrifts': len(MODEL_DRIFTS), 'artifactDrifts': len(ARTIFACT_DRIFTS),
       'total': len(results),
       'detected': sum(1 for x in results if x.get('detected')),
       'undetectedDrifts': undetected,
       'allDetected': all(x.get('detected') for x in results),
       'undetectedDisposition': {
           'A8 the reader ignores the receipt-present-but-unsettled contradiction': (
               'NOT DETECTED, and reported rather than removed. Confirming a commit from a '
               'present receipt while the custody row is still admitted is not actually unsafe: '
               'the receipt IS the authority, so the drift produces a defensible answer rather '
               'than a false one. That means the receipt-present-but-unsettled contradiction rule '
               'is a CONSERVATIVE POLICY, like the two-agreeing-tails clause, and not a '
               'correctness requirement. It is retained because a receipt whose attempt was never '
               'settled indicates a broken write ordering worth surfacing, but these controls do '
               'not prove it necessary and root may drop it.'),
           'A2 corruption gate keeps the brackets but drops the two-agreeing-tails requirement': (
               'NOT DETECTED, and reported as such rather than removed. In a lawful append the '
               'tail only moves together with the witness, so any schedule where the tail moves '
               'between the two captures also moves the witness, and the second capture then '
               'lands on a usable PENDING-at-tail or COMMITTED-at-tail anchor instead of an '
               'adverse one. These schedules therefore do not show the two-agreeing-tails clause '
               'to be independently load-bearing. It is retained as defence in depth against a '
               'writer or repair path that moves the tail without moving the witness, which the '
               'current protocol does not contain but which the clause would cover. Root may '
               'drop it; this control does not justify keeping it.'),
       },
       'results': results}
with open(OUT, 'w', encoding='utf-8') as fh:
    fh.write(json.dumps(rep, indent=1) + '\n')
print('WROTE', OUT)
print('drifts %d detected %d allDetected %s' % (rep['total'], rep['detected'], rep['allDetected']))
for x in results:
    print(' ', 'DETECTED    ' if x.get('detected') else 'NOT-DETECTED', x['drift'])
    print('      ', x.get('how') or x.get('error'))
