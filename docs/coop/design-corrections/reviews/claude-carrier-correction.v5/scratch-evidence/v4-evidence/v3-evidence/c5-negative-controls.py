# Control C5 - negative controls for check-carrier-v3.py.
#
# A checker that cannot fail proves nothing. This deliberately drifts a copy of the proposal
# tree and asserts the checker rejects each drift. Copies live under scratch/neg only; the
# real proposal tree, the inputs and Source25 are never touched.
#
# usage: python c5-negative-controls.py <source25Root> <runtimeRoot> <reportPath>
import json
import os
import shutil
import subprocess
import sys

SRC, ROOT, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
NEG = os.path.join(ROOT, 'scratch', 'neg')
EXE = sys.executable
SECREL = 'scratch/proposal/docs/coop/design-corrections/security'

# a drift is (name, relative path under the sandbox root, old substring, new substring)
DRIFTS = [
    ('alias re-admitted into the carrierFormat 3 platform set',
     SECREL + '/carrier-dispatch.v3.json',
     '"platformSet": ["macos-aarch64", "macos-x86_64", "linux-x86_64-gnu", "linux-aarch64-gnu"]',
     '"platformSet": ["macos-arm64", "macos-x86_64", "linux-x86_64-gnu", "linux-aarch64-gnu"]'),
    ('TERMINAL promoted into the operational (schema 3) type set',
     SECREL + '/carrier-dispatch.v3.json',
     '"operationalRecordTypes": ["GRANT", "RA", "ICI", "RCI", "ICO", "RCO", "REV", "CLN", "SEAL"]',
     '"operationalRecordTypes": ["GRANT", "RA", "ICI", "RCI", "ICO", "RCO", "REV", "CLN", "SEAL", "TERMINAL"]'),
    ('dispatch claims TERMINAL is a public JournalRecord',
     SECREL + '/carrier-dispatch.v3.json',
     '"terminalIsPublicJournalRecord": false',
     '"terminalIsPublicJournalRecord": true'),
    ('a frozen carrierFormat 2 fact is misstated',
     SECREL + '/carrier-dispatch.v3.json',
     '"hasContiguityTrigger": true,\n      "hasTerminalClosureTrigger": true',
     '"hasContiguityTrigger": false,\n      "hasTerminalClosureTrigger": false'),
    ('the schema-1 / schema-3 segregation CHECK is removed from the DDL',
     SECREL + '/grant-journal.carrier.v3.sql',
     "  CHECK ((record_schema = 3 AND record_type <> 'TERMINAL')\n      OR (record_schema = 1 AND record_type = 'TERMINAL')),\n",
     ''),
    ('the reserved terminal slot trigger is removed from the DDL',
     SECREL + '/grant-journal.carrier.v3.sql',
     "9007199254740991 is the reserved terminal slot",
     "slot is available"),
    ('an alias spelling is admitted by the DDL platform CHECK',
     SECREL + '/grant-journal.carrier.v3.sql',
     "'macos-aarch64','macos-x86_64'",
     "'macos-arm64','macos-x86_64'"),
    ('the high-water cap is widened past the physical uint53 cap',
     SECREL + '/carrier-highwater.schema.v1.json',
     '"maximum": 9007199254740991,\n   "description": "Highest sequence observed',
     '"maximum": 9223372036854775807,\n   "description": "Highest sequence observed'),
    ('the high-water record is opened to unknown members',
     SECREL + '/carrier-highwater.schema.v1.json',
     '"additionalProperties": false,\n "required"',
     '"additionalProperties": true,\n "required"'),
    ('a proposal document asserts acceptance',
     'scratch/proposal/docs/coop/design-corrections/security/carrier-format.v3.md',
     '**Standing.** Proposed versioned',
     '**Standing.** This correction is now accepted. Proposed versioned'),
    ('a proposal document drops every non-acceptance standing marker',
     SECREL + '/carrier-highwater.schema.v1.json',
     ' "status": "PROPOSED-NOT-SELF-ACCEPTED",\n "standing": "Design/reference proposal only: no acceptance, no readiness, no application and no implementation authorization.",\n',
     ''),
    ('an inherited F00-F37 conclusion is altered by the patch',
     'scratch/patched/docs/v2/architecture/commit-recovery-plan.v1.json',
     '"id": "F16",\n      "checkpoint": "Required projection/HTML/output fails after commit",\n      "possibleStoredState": "Committed Run remains intact",\n      "initialConclusion": "committed-delivery-failed"',
     '"id": "F16",\n      "checkpoint": "Required projection/HTML/output fails after commit",\n      "possibleStoredState": "Committed Run remains intact",\n      "initialConclusion": "committed"'),
]

results = []
for i, (name, rel, old, new) in enumerate(DRIFTS):
    sand = os.path.join(NEG, 'n%02d' % i)
    if os.path.isdir(sand):
        shutil.rmtree(sand)
    os.makedirs(sand)
    for sub in ('scratch/proposal', 'scratch/patched', 'inputs'):
        shutil.copytree(os.path.join(ROOT, sub), os.path.join(sand, sub))
    os.makedirs(os.path.join(sand, 'scratch', 'out'), exist_ok=True)
    target = os.path.join(sand, rel)
    txt = open(target, encoding='utf-8').read()
    if txt.count(old) != 1:
        results.append({'drift': name, 'anchorOccurrences': txt.count(old),
                        'checkerRejected': None, 'error': 'drift anchor not unique'})
        continue
    with open(target, 'w', encoding='utf-8') as fh:
        fh.write(txt.replace(old, new))
    rep = os.path.join(sand, 'scratch', 'out', 'neg.json')
    r = subprocess.run([EXE, os.path.join(sand, SECREL, 'check-carrier-v3.py'),
                        SRC, sand, rep], capture_output=True, text=True)
    failed = None
    if os.path.exists(rep):
        failed = json.load(open(rep, encoding='utf-8'))['failed']
    results.append({'drift': name, 'path': rel, 'checkerExit': r.returncode,
                    'checkerFailedChecks': failed,
                    'checkerRejected': bool(failed) or r.returncode != 0,
                    'stderrTail': r.stderr[-200:] if r.returncode != 0 else ''})

rep = {'control': 'c5-negative-controls',
       'drifts': len(DRIFTS),
       'rejected': sum(1 for x in results if x.get('checkerRejected')),
       'allRejected': all(x.get('checkerRejected') for x in results),
       'results': results}
with open(OUT, 'w', encoding='utf-8') as fh:
    fh.write(json.dumps(rep, indent=1) + '\n')
print('WROTE', OUT)
print('drifts %d rejected %d allRejected %s' % (rep['drifts'], rep['rejected'], rep['allRejected']))
for x in results:
    mark = 'REJECTED' if x.get('checkerRejected') else 'NOT-REJECTED'
    print(' ', mark, x['drift'], '(failed checks: %s)' % x.get('checkerFailedChecks'))
