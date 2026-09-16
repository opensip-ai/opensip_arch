# Control C19 - negative controls for the v7 corrections.
#
# Each drift reintroduces one of the exact defects root found, or breaks one of the new laws, and
# the corresponding control must reject it. A control that cannot fail proves nothing.
#
# Sandboxes live under scratch/neg7 only; the real trees are never written.
#
# usage: python c19-negative-v7.py <runtimeRoot> <v6Root> <source25Root> <reportPath>
import json
import os
import shutil
import subprocess
import sys

ROOT, V6, SRC, OUT = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
NEG = os.path.join(ROOT, 'scratch', 'neg7')
EXE = sys.executable
PROPREL = 'scratch/proposal'
AC = PROPREL + '/docs/v2/architecture/attempt-custody.schema.v1.json'
DISP = PROPREL + '/docs/coop/design-corrections/security/carrier-dispatch.v3.json'
FMT = PROPREL + '/docs/coop/design-corrections/security/carrier-format.v3.md'
MIG = PROPREL + '/docs/coop/design-corrections/security/carrier-migration.v1.md'
REC = PROPREL + '/docs/v2/architecture/commit-recovery-readonly.v3.md'
CASES = PROPREL + '/docs/v2/architecture/carrier-fault-cases.v1.json'

# (name, targetRelPath, old, new, whichControl)
DRIFTS = [
    ('N1 the duplicate admitted key is reintroduced', AC,
     '"phaseOutcomeCoupling": {\n    "admitted":',
     '"phaseOutcomeCoupling": {\n    "admitted": "shadowed",\n    "admitted":', 'c17'),
    ('N2 attempt custody claims the reservation is already durable law', AC,
     '"whatExistingLawDoesNotGive"', '"whatExistingLawDoesNotGiveRenamed"', 'c17'),
    ('N3 attempt custody drops the ephemeral exclusion', AC,
     '"excludedModes"', '"excludedModesRenamed"', 'c17'),
    ('N4 the phase description licenses a cleanup-path write', AC,
     'A stopped cleanup-only session may NOT write it.',
     'The guarded cleanup path may also write it.', 'c17'),
    ('N5 the receipt join is made caller-conditional again', AC,
     'MANDATORY on all five.', 'Where the caller supplies them,', 'c17'),
    ('N6 the dispatch reverts to table-existence detection', DISP,
     '"observe": "the set of carrierFormat 3 object NAMES present in sqlite_master"',
     '"if": "table grant_journal_v3 exists AND table carrier_format exists"', 'c17'),
    ('N7 the dispatch stops reading the row last', DISP,
     '"rowIsReadLastAndOnlyAfterValidation": true',
     '"rowIsReadLastAndOnlyAfterValidation": false', 'c17'),
    ('N8 the fresh-install path claims it reads absent tables', DISP,
     '"readsAbsentTables": false', '"readsAbsentTables": true', 'c17'),
    ('N9 the prose reverts the second-migration-aborts phrasing', FMT,
     'historical C2 evidence', 'CURRENT recovery law', 'c17'),
    ('N10 the migration reclaims blanket usability', MIG,
     'Historical reading is unaffected', 'The carrier is fully usable', 'c17'),
    ('N11 recovery defers an operative rule to the superseded v2 draft', REC,
     '**Stated in full here.** This document is the current owner',
     'Unchanged from v2. This document is the current owner', 'c17'),
    ('N12 recovery drops the missing-custody-row law', REC,
     'custody-unknown-legacy', 'custody-unknown-renamed', 'c17'),
    ('N13 F47 requires a transition intent again', CASES,
     'NO installation transition intent or journal is written',
     'an intent written only after every lease is held', 'c17'),
    ('N14 F48 reverts to a blanket typed refusal', CASES,
     'A carrierFormat-AWARE core', 'A carrierFormat 1-or-2-only core', 'c17'),
    ('N15 F52 calls receipt-plus-admitted a contradiction again', CASES,
     'A receipt present while the attempt row is still admitted is the LAWFUL pre-settle interval',
     'A receipt present with the attempt still admitted is also a contradiction', 'c17'),
    ('N16 F40 drops the two-senses-of-terminal clarification', CASES,
     'TWO SENSES OF TERMINAL', 'TERMINAL SENSE', 'c17'),
    ('N17 F38 drops the aborted-action versus observer distinction', CASES,
     'ACTUAL ABORTED ACTION', 'ABORTED ACTION', 'c17'),
    ('N18 the dispatch drops the partial-object refusal step entirely', DISP,
     '"if": "some but not all seven names are present"',
     '"if": "this branch has been removed"', 'c17'),
    # N20 restores the exact law-deferral the selected validator found in carrier-migration §6.
    # A normative sentence whose content lives only in a correction-run directory is unresolvable
    # for a repo consumer, so the validator must reject it.
    ('N20 the migration defers PS-01 lineage law to a correction-run directory', MIG,
     'Lineage allocation is stated by that owner and is\n  deliberately not restated here',
     'Lineage\n  allocation is not duplicated here — it is in `owner-correction.v3`', 'check'),
]

results = []
for i, (name, rel, old, new, which) in enumerate(DRIFTS):
    sand = os.path.join(NEG, 'n%02d' % i)
    if os.path.isdir(sand):
        shutil.rmtree(sand)
    os.makedirs(os.path.join(sand, 'scratch', 'out'), exist_ok=True)
    shutil.copytree(os.path.join(ROOT, 'scratch', 'proposal'),
                    os.path.join(sand, 'scratch', 'proposal'))
    shutil.copytree(os.path.join(ROOT, 'scratch', 'controls'),
                    os.path.join(sand, 'scratch', 'controls'))
    # the selected validator also reads the patched planning inputs
    shutil.copytree(os.path.join(ROOT, 'scratch', 'patched'),
                    os.path.join(sand, 'scratch', 'patched'))
    target = os.path.join(sand, rel)
    txt = open(target, encoding='utf-8').read()
    if txt.count(old) != 1:
        results.append({'drift': name, 'anchorOccurrences': txt.count(old), 'detected': None,
                        'error': 'drift anchor not unique'})
        continue
    with open(target, 'w', encoding='utf-8') as fh:
        fh.write(txt.replace(old, new, 1))
    rep = os.path.join(sand, 'scratch', 'out', 'drift.json')
    if which == 'c17':
        cmd = [EXE, os.path.join(sand, 'scratch/controls/c17-strict-json-propagation.py'),
               sand, V6, rep]
    elif which == 'check':
        cmd = [EXE, os.path.join(sand, PROPREL, 'docs/coop/design-corrections/security/'
                                 'check-carrier-v3.py'), SRC, sand, rep]
    else:
        cmd = [EXE, os.path.join(sand, 'scratch/controls/c18-selected-dispatch.py'), SRC,
               os.path.join(sand, PROPREL,
                            'docs/coop/design-corrections/security/grant-journal.carrier.v3.sql'),
               os.path.join(sand, DISP), rep]
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=sand)
    failed, crashed = None, r.returncode != 0
    if os.path.exists(rep):
        failed = json.load(open(rep, encoding='utf-8'))['failed']
    results.append({
        'drift': name, 'path': rel, 'control': which,
        'controlFailedChecks': failed, 'controlCrashed': crashed,
        'detected': bool(failed) or crashed,
        'how': ('control reported %s failed checks' % failed) if failed
               else ('control crashed: ' + (r.stderr.strip().splitlines() or [''])[-1][:110]
                     if crashed else 'NOT DETECTED'),
        'cleanFailure': bool(failed) and not crashed})

# also run C18 against a dispatch whose declared object list is wrong
sand = os.path.join(NEG, 'n90')
if os.path.isdir(sand):
    shutil.rmtree(sand)
os.makedirs(os.path.join(sand, 'scratch', 'out'), exist_ok=True)
shutil.copytree(os.path.join(ROOT, 'scratch', 'proposal'),
                os.path.join(sand, 'scratch', 'proposal'))
shutil.copytree(os.path.join(ROOT, 'scratch', 'controls'),
                os.path.join(sand, 'scratch', 'controls'))
dj = os.path.join(sand, DISP)
d = json.load(open(dj, encoding='utf-8'))
d['openDispatch']['sevenCarrierFormat3Objects'] = ['carrier_format', 'grant_journal_v3']
with open(dj, 'w', encoding='utf-8') as fh:
    fh.write(json.dumps(d, indent=2) + '\n')
rep = os.path.join(sand, 'scratch', 'out', 'drift.json')
r = subprocess.run([EXE, os.path.join(sand, 'scratch/controls/c18-selected-dispatch.py'), SRC,
                    os.path.join(sand, PROPREL,
                                 'docs/coop/design-corrections/security/'
                                 'grant-journal.carrier.v3.sql'),
                    dj, rep], capture_output=True, text=True, cwd=sand)
failed = json.load(open(rep, encoding='utf-8'))['failed'] if os.path.exists(rep) else None
results.append({'drift': 'N19 the dispatch declares fewer than seven objects', 'path': DISP,
                'control': 'c18', 'controlFailedChecks': failed,
                'controlCrashed': r.returncode != 0,
                'detected': bool(failed) or r.returncode != 0,
                'how': ('control reported %s failed checks' % failed) if failed
                       else ('control crashed' if r.returncode else 'NOT DETECTED'),
                'cleanFailure': bool(failed) and r.returncode == 0})

undetected = [x['drift'] for x in results if not x.get('detected')]
rep_out = {'control': 'c19-negative-v7', 'drifts': len(results),
           'detected': sum(1 for x in results if x.get('detected')),
           'undetected': undetected, 'allDetected': not undetected,
           'cleanFailures': sum(1 for x in results if x.get('cleanFailure')),
           'results': results}
with open(OUT, 'w', encoding='utf-8') as fh:
    fh.write(json.dumps(rep_out, indent=1) + '\n')
print('WROTE', OUT)
print('drifts %d detected %d clean %d' % (rep_out['drifts'], rep_out['detected'],
                                          rep_out['cleanFailures']))
for x in results:
    print(('  DET  ' if x.get('detected') else '  MISS '), x['drift'][:66], '|',
          (x.get('how') or x.get('error') or '')[:70])
