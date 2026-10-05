"""X3c-3's transcription of X9 r17 §RC's 22 rows (RC.4) into storage's
required-runs.v1.json, after its 381 rows. Every value below is copied from
§RC (PROPOSAL-r17-RC.md, RC.2 and RC.4); nothing is read from a run.

usage: transcribe_x3c3.py <landed required-runs.v1.json> <output>
The landed file's `runs` bytes must be unchanged inside the output.
"""
import json
import sys

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()

UNITS = ['X3c']
UNIT = 'X3c-3'
LABELS = {
    'death': ['process-death', 'scripted-clock', 'synthetic'],
    'injected': ['injected', 'scripted-clock', 'synthetic'],
    'mutation': ['mutation', 'scripted-clock', 'synthetic'],
    'plain': ['scripted-clock', 'synthetic'],
}
COMMITTED = 'Committed(latched=false)'
CH_PENDING = 'committed-historically:pendingSettlement:*'
CH_SETTLED = 'committed-historically:settled:*'
CH_ANY = 'committed-historically:*'
UAO = 'unknown-attempt-open'
TNC = 'terminal-not-committed'
E1 = [{'name': 'e1', 'spawn': 'commit'}, {'finish': 'e1'}]
RECOVER_E1 = [{'for': 'e1', 'name': 'e1-recover', 'spawn': 'recover'}, {'finish': 'e1-recover'}]

# RC.4's script templates.
def t_l():
    return E1 + [{'name': 'e2', 'spawn': 'commit', 'unchanged': True}, {'finish': 'e2'},
                 {'ladder': 'R1,R2,R3,R4', 'of': 'e2', 'r2': 'same'}] + RECOVER_E1

def t_k(point, ladder, recover):
    return E1 + [{'arm': f'{point}=hold', 'name': 'e2', 'spawn': 'commit', 'unchanged': True},
                 {'await': point, 'on': 'e2', 'then': 'kill'},
                 {'ladder': ladder, 'of': 'e2', 'r2': 'same'}] + (RECOVER_E1 if recover else [])

def t_i(point, action):
    return E1 + [{'arm': f'{point}={action}', 'name': 'e2', 'spawn': 'commit', 'unchanged': True}, {'finish': 'e2'},
                 {'ladder': 'R1,R2,R3,R4', 'of': 'e2', 'r2': 'same'}] + RECOVER_E1

def t_m(mutation, ladder, recover):
    return E1 + [{'mutate': mutation, 'of': 'e1'},
                 {'name': 'e2', 'spawn': 'commit', 'unchanged': True}, {'finish': 'e2'},
                 {'ladder': ladder, 'of': 'e2'}] + (RECOVER_E1 if recover else [])

def t_p():
    return [{'distinct': True, 'name': 'd', 'spawn': 'commit'}, {'finish': 'd'},
            {'mutate': 'plant-availability', 'of': 'd'},
            {'name': 'e2', 'spawn': 'commit', 'unchanged': True}, {'finish': 'e2'},
            {'ladder': 'R1,R3,R4', 'of': 'e2'}]

def t_r():
    staging, returned = 'x3d.publish.after-staging#1', 'x3d.publish.commit-returned#1'
    return E1 + [
        {'arm': f'{staging}=hold,{returned}=hold', 'name': 'e2', 'spawn': 'commit'},
        {'await': staging, 'on': 'e2', 'then': 'hold'},
        {'for': 'e1', 'name': 'e1-at-staging', 'spawn': 'reader'}, {'finish': 'e1-at-staging'},
        {'for': 'e2', 'name': 'e2-at-staging', 'spawn': 'reader'}, {'finish': 'e2-at-staging'},
        {'on': 'e2', 'resume': staging},
        {'await': returned, 'on': 'e2', 'then': 'hold'},
        {'for': 'e1', 'name': 'e1-at-returned', 'spawn': 'reader'}, {'finish': 'e1-at-returned'},
        {'for': 'e2', 'name': 'e2-at-returned', 'spawn': 'reader'}, {'finish': 'e2-at-returned'},
        {'on': 'e2', 'resume': returned},
        {'finish': 'e2'}]

def row(case, variant, script, labels, expected):
    return {'case': case, 'variant': variant, 'units': UNITS, 'unit': UNIT, 'labels': LABELS[labels],
            'script': script, 'expected': expected}

rows = []
# RC-1. A lawful re-commit (X3C:277-280).
rows.append(row('F15', 'recommit-lawful', t_l(), 'plain', {
    'e1': COMMITTED, 'e2': COMMITTED,
    'e1.stages': 'recovery_pair,run_material,availability,pins',
    'e2.stages': 'recovery_pair,run_material',
    'e2.objectsLinked': '0',
    'e2.ledgerRowsKept': 'true',
    'attemptRows': '2', 'receipts': '2', 'materialRows': '2',
    'commitSequences': '1,2',
    'materialIdentical': 'true',
    'availabilityRows': '1',
    'pinRows': '0',
    'R1': CH_PENDING,
    'R2.outcome': COMMITTED,
    'R3': 'committed', 'R3.others': 'next-writer=committed',
    'R4': CH_SETTLED,
    'e1-recover': CH_SETTLED,
}))
# RC-2. Kills in the confirm branch (X3C:281-283): F04, eight variants.
RC2 = {
    'e1': COMMITTED, 'e2': 'killed',
    'e2.ledgerRowsKept': 'true', 'e2.objectsKept': 'true',
    'R1': UAO,
    'R2.outcome': COMMITTED, 'R2.objectsLinked': '0',
    'R3': 'refused', 'R3.others': 'next-writer=committed',
    'R4': TNC,
    'e1-recover': CH_SETTLED,
}
for step, k in (('reopen-confirm.before', 1), ('reopen-confirm.before', 41), ('reopen-confirm.before', 82),
                ('reopen-confirm.after', 1), ('reopen-confirm.after', 41), ('reopen-confirm.after', 82),
                ('file-barrier.before', 164), ('file-barrier.after', 164)):
    slug = step.replace('.', '-')
    rows.append(row('F04', f'recommit-kill-x3c-object-{slug}-{k}',
                    t_k(f'x3c.object/{step}#{k}', 'R1,R2,R3,R4', True), 'death', dict(RC2)))
# RC-3. Staging kills (X3C:284-286): F11, two variants.
RC3 = {
    'e1': COMMITTED, 'e2': 'killed',
    'e2.ledgerRowsKept': 'true',
    'seals': '2', 'revs': '0',
    'receipts': '1', 'materialRows': '1',
    'availabilityRows': '1',
    'R1': UAO,
    'R2.outcome': COMMITTED, 'R2.witnessAction': 'OK',
    'R3': 'refused',
    'R4': TNC,
    'R5': CH_SETTLED, 'R5.sameRunId': 'true',
    'e1-recover': CH_SETTLED,
}
for table, slug in (('recovery_pair', 'recovery-pair'), ('run_material', 'run-material')):
    rows.append(row('F11', f'recommit-kill-x3c-evidence-stage-{slug}-1',
                    t_k(f'x3c.evidence.stage-{table}#1', 'R1,R2,R3,R4,R5', True), 'death', dict(RC3)))
# RC-4. The undetermined COMMIT (X3C:287-289): F12, two variants.
END = 'end(rev=false,cln=false,settlement=None,step=false,stepFailure=None)'
rows.append(row('F12', 'recommit-fail-before-evidence-commit', t_i('x3c.evidence.commit.before#1', 'fail-before'), 'injected', {
    'e1': COMMITTED, 'e2': 'CommitUndetermined', 'e2.end': END, 'e2.ledgerRowsKept': 'true',
    'receipts': '1', 'materialRows': '1', 'commitSequences': '1', 'availabilityRows': '1',
    'R1': UAO, 'R2.outcome': COMMITTED, 'R3': 'refused', 'R4': TNC, 'e1-recover': CH_SETTLED,
}))
rows.append(row('F12', 'recommit-fail-after-evidence-commit', t_i('x3c.evidence.commit.after#1', 'fail-after'), 'injected', {
    'e1': COMMITTED, 'e2': 'CommitUndetermined', 'e2.end': END, 'e2.ledgerRowsKept': 'true',
    'receipts': '2', 'materialRows': '2', 'commitSequences': '1,2', 'availabilityRows': '1',
    'R1': CH_PENDING, 'R2.outcome': COMMITTED, 'R3': 'committed', 'R4': CH_SETTLED, 'e1-recover': CH_SETTLED,
}))
# RC-5. The lost acknowledgement, with a same-Run next writer (X3C:290-292).
for case, point, slug in (('F13', 'x3c.evidence.commit.after#1', 'x3c-evidence-commit-after-1'),
                          ('F13', 'x3d.publish.commit-returned#1', 'x3d-publish-commit-returned-1'),
                          ('F14', 'x3d.publish.published#1', 'x3d-publish-published-1'),
                          ('F15', 'x3d.finish.end-step.after#1', 'x3d-finish-end-step-after-1')):
    rows.append(row(case, f'recommit-kill-{slug}', t_k(point, 'R1,R2,R3,R4', False), 'death', {
        'e1': COMMITTED, 'e2': 'killed', 'e2.ledgerRowsKept': 'true',
        'availabilityRows': '1',
        'R1': CH_ANY if case == 'F15' else CH_PENDING,
        'R2.outcome': COMMITTED, 'R2.commitSequence': '3', 'R2.receipts': '1', 'R2.availabilityRows': '1',
        'R3': 'committed',
        'R4': CH_SETTLED,
    }))
# RC-6. A regeneration mismatch (X3C:293-295).
rows.append(row('F33', 'recommit-run-material-inventory', t_m('run-material-inventory', 'R1,R3,R4', False), 'mutation', {
    'e1': COMMITTED, 'e2': 'Refused(Invariant)',
    'e2.rev': 'true', 'e2.cln': 'true',
    'e2.stages': '',
    'e2.ledgerRowsKept': 'true',
    'receipts': '1', 'materialRows': '1',
    'commitSequences': '1',
    'availabilityRows': '1',
    'R1': UAO, 'R3': 'refused', 'R4': TNC,
}))
# RC-7. A one-sided Run (X3C:296-302).
rows.append(row('F23', 'recommit-one-sided-material-only', t_m('delete-availability', 'R1,R3,R4', False), 'mutation', {
    'e1': COMMITTED, 'e2': 'Refused(LedgerCorrupt)',
    'e2.rev': 'true', 'e2.cln': 'true', 'e2.stages': '', 'e2.ledgerRowsKept': 'true',
    'receipts': '1', 'materialRows': '1', 'availabilityRows': '0',
    'R1': UAO, 'R3': 'refused', 'R4': TNC,
}))
rows.append(row('F23', 'recommit-one-sided-availability-only', t_p(), 'mutation', {
    'd': COMMITTED, 'e2': 'Refused(LedgerCorrupt)',
    'e2.rev': 'true', 'e2.cln': 'true', 'e2.stages': '', 'e2.ledgerRowsKept': 'true',
    'receipts': '1', 'materialRows': '1', 'availabilityRows': '2',
    'R1': UAO, 'R3': 'refused', 'R4': TNC,
}))
# RC-8. Reader isolation (X3C:303-304).
rows.append(row('F29', 'recommit-readers-across-publish', t_r(), 'plain', {
    'e1': COMMITTED, 'e2': COMMITTED,
    'e1-at-staging': CH_PENDING, 'e1-at-returned': CH_PENDING,
    'e2-at-staging': UAO,
    'e2-at-returned': CH_PENDING,
}))
# RC-9. A non-retained record (X3C:305-307).
rows.append(row('F52', 'recommit-purged', t_m('availability-purged', 'R1', True), 'mutation', {
    'e1': COMMITTED, 'e2': COMMITTED,
    'e2.objectsLinked': '1',
    'e2.stages': 'recovery_pair,run_material',
    'e2.ledgerRowsKept': 'true',
    'availabilityRows': '2',
    'R1': CH_PENDING,
    'e1-recover': CH_PENDING,
}))

assert len(rows) == 22, len(rows)
landed_raw = open(sys.argv[1], 'rb').read()
landed = json.loads(landed_raw)
assert canonical(landed) == landed_raw, 'landed file is not canonical'
assert len(landed['runs']) == 381, len(landed['runs'])
identities = {(r['case'], r['variant']) for r in landed['runs']}
for r in rows:
    assert (r['case'], r['variant']) not in identities, r['variant']
document = dict(landed, runs=landed['runs'] + rows)
out = canonical(document)
# The landed rows' bytes are unchanged inside the new file.
old_runs = canonical(landed['runs'])[1:-1]
assert old_runs in out
assert out.index(old_runs) == len(b'{"clockEpoch":%d,"runs":[' % landed['clockEpoch'])
open(sys.argv[2], 'wb').write(out)
print(json.dumps({'rows': len(document['runs']), 'added': len(rows), 'bytes': len(out)}))
