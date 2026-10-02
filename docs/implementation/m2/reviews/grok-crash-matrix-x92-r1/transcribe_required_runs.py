"""Transcribe X9-2's rows of law X9 r9 item 9 into required-runs.v1.json.

Inputs, all made before any kill run: the unarmed census of X9-2's commit
driver (census.json: points with occurrences; census-trace.txt: the trace in
order), and X9 r9's unarmed reference run (reference.json: (A) the
publication's new trust entries in creation order at ordinal 1, (B) the files
the next publication writes at ordinal 2, on the same installation). Only
the kill points, their order and each X4T dependency occurrence's collision
come from these (items 5 and 9, r9); every expected value is the law's row,
written here before any run and never read back from one. Standard library
only.

usage: transcribe_required_runs.py <census.json> <census-trace.txt> <reference.json> <out>
"""
import json
import re
import sys

EPOCH = 1791072000
LABELS_KILL = ['process-death', 'scripted-clock', 'synthetic']
LABELS_TORN = ['injected', 'process-death', 'scripted-clock', 'synthetic']
LABELS_INJ = ['injected', 'scripted-clock', 'synthetic']
LABELS_MUT = ['mutation', 'scripted-clock', 'synthetic']
LABELS_DEATH_MUT = ['mutation', 'process-death', 'scripted-clock', 'synthetic']
COMMITTED = 'Committed(latched=false)'


def kill_set(points):
    out = []
    for p in points:
        if p['durability']:
            n = p['occurrences']
            for k in sorted({1, (n + 1) // 2, n}):
                out.append(f"{p['name']}#{k}")
    return out


def variant(prefix, point):
    name, k = point.rsplit('#', 1)
    slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
    return f'{prefix}-{slug}-{k}'


def kill_script(point):
    return [{'arm': f'{point}=hold'}, {'await': point, 'then': 'kill'}]


def main():
    census = json.load(open(sys.argv[1]))
    trace = [line.split('|') for line in open(sys.argv[2]).read().splitlines()]
    reference = json.load(open(sys.argv[3]))
    position = {}
    for i, fields in enumerate(trace):
        point = fields[2]
        if point != '-' and point not in position:
            position[point] = i
    points = census['points']
    occurrences = {p['name']: p['occurrences'] for p in points}
    kills = kill_set(points)
    for k in kills:
        assert k in position, k
    draw = position['x3d.session.execution-draw#1']
    ddl_after = position['x3c.ledger-create.ddl.commit.after#1']
    attempt_after = position['x3c.attempt.commit.after#1']
    rows = []

    def row(case, var, units, labels, script, expected):
        rows.append({'case': case, 'variant': var, 'units': units, 'labels': labels,
                     'script': script, 'expected': expected})

    # F00: every kill-set point before x3c.attempt.commit.after (X9 r6 split
    # for R1 and R4; X9 r8 and r9 for R2 by the crash state the kill leaves).
    committed_r2 = {'R2.witnessAction': ['OK', 'INIT', 'REVERT', 'ADVANCE'], 'R2.outcome': COMMITTED}
    reserved = position['x2.fence.register.reserved/rename.after#1']
    active = position['x2.fence.register.active/rename.before#1']
    custody = {'x3c.ledger-create.projects/create.after', 'x3c.ledger-create.namespace/create.after',
               'x3c.object.objects/create.after', 'x3c.object.sha256/create.after', 'x3c.ledger-create/create.after'}
    wal_gap = {'x3c.ledger-create.wal', 'x3c.ledger-create.ddl.commit.before'}
    # X9 r9: each X4T dependency occurrence's leaf in A, and whether B writes it.
    created = reference['a']
    files = [e for e in created if e['file']]
    writes = {e['path'] for e in reference['b']}
    root = 'operation:ProjectRootCustody { subject: "%s" }'

    def r2_for(point):
        name, k = point.rsplit('#', 1)
        k = int(k)
        if reserved <= position[point] <= active:
            subject = {'x2.fence.register.marker/create.after': 'marker-custody',
                       'x2.fence.register.marker/write.before': 'identity-contradiction'}.get(name, 'identity-recovery-required')
            return {'R2.outcome': root % subject}, False
        if name in custody:
            return {'R2.outcome': 'not-prepared:Refused(Custody { subject: "private" })'}, True
        if name == 'x3b.floor.directory/create.after':
            return {'R2.outcome': 'operation:HostIo'}, False
        if name in wal_gap:
            return {'R2.outcome': 'not-prepared:Refused(LedgerCorrupt)'}, True
        if name in ('x4t.floor-publication.dependency/create.after', 'x4t.floor-publication.dependency/write.before'):
            entry = created[k - 1] if name.endswith('create.after') else files[k - 1]
            assert entry['file'], point  # no directory occurrence in this kill set (r9)
            if entry['path'] in writes:
                return {'R2.outcome': 'operation:Incomplete'}, False
        return dict(committed_r2), False

    for point in sorted((k for k in kills if position[k] < attempt_after), key=lambda k: position[k]):
        r2, no_ledger = r2_for(point)
        expected = {'scripted': 'killed', 'attemptRows': '0', 'R3': 'nothing', **r2}
        if position[point] <= draw:
            pass  # before the draw (a hold at the draw precedes it): R1 and R4 not applicable
        elif position[point] < ddl_after:
            expected['R1'] = ['unknown-custody:ledger-missing', 'unknown-custody:ledger-unreadable']
            expected['R4'] = (['unknown-custody:ledger-missing', 'unknown-custody:ledger-unreadable']
                              if no_ledger else 'unknown-attempt-unobserved')
        else:
            expected['R1'] = 'unknown-attempt-unobserved'
            expected['R4'] = 'unknown-attempt-unobserved'
        row('F00', variant('kill', point), ['X2', 'X3a', 'X3b', 'X4T-b'], LABELS_KILL, kill_script(point), expected)

    left = {'scripted': 'killed', 'R1': 'unknown-attempt-open', 'R2.outcome': COMMITTED,
            'R3': 'refused', 'R4': 'terminal-not-committed'}

    def at(name):
        n = occurrences[name]
        return [f'{name}#{k}' for k in sorted({1, (n + 1) // 2, n})]

    # F02: torn at the first, middle and last object write.
    for point in at('x3c.object/write.before'):
        row('F02', variant('torn', point), ['X3c'], LABELS_TORN,
            [{'arm': f'{point}=torn'}, {'await': point, 'then': 'kill'}], dict(left))
    # F03, F04, F05: kills at the object's barriers and link.
    for case, steps in (('F03', ('file-barrier',)), ('F04', ('link',)), ('F05', ('directory-barrier',))):
        for step in steps:
            for phase in ('before', 'after'):
                for point in at(f'x3c.object/{step}.{phase}'):
                    row(case, variant('kill', point), ['X3c'], LABELS_KILL, kill_script(point), dict(left))
    # F04: the unequal-collision mutation variant (X3c item 10's row).
    point = 'x3c.object/link.after#1'
    row('F04', 'kill-link-after-1-unequal-collision', ['X3c'], LABELS_DEATH_MUT,
        kill_script(point) + [{'mutate': 'object-unequal'}],
        {'scripted': 'killed', 'R2.outcome': 'not-prepared:Refused(LedgerCorrupt)'})
    # F07 to F10 (r5: R1 is plain UAO; the witness expectation is R2's).
    seal = 'x3b.append.seal'
    pending = [n for n in sorted(occurrences, key=lambda n: position[f'{n}#1']) if n.startswith(f'{seal}.witness-pending/')]
    committed = [n for n in sorted(occurrences, key=lambda n: position[f'{n}#1']) if n.startswith(f'{seal}.witness-committed/')]
    pending_rename = position[f'{seal}.witness-pending/rename.after#1']
    for name in pending + [f'{seal}.insert.before']:
        visible = position[f'{name}#1'] >= pending_rename  # X9 r8: REVERT from the rename on
        row('F07', variant('kill', f'{name}#1'), ['X3b'], LABELS_KILL, kill_script(f'{name}#1'),
            {**left, 'R2.witnessAction': 'REVERT' if visible else 'OK'})
    for name in (f'{seal}.insert.after', f'{seal}.commit.before'):
        row('F08', variant('kill', f'{name}#1'), ['X3b'], LABELS_KILL, kill_script(f'{name}#1'),
            {**left, 'R2.witnessAction': 'REVERT'})
    row('F09', variant('kill', f'{seal}.commit.after#1'), ['X3b'], LABELS_KILL, kill_script(f'{seal}.commit.after#1'),
        {**left, 'R2.witnessAction': 'ADVANCE'})
    for phase, action, witness in (('after', 'fail-after', 'ADVANCE'), ('before', 'fail-before', 'REVERT')):
        row('F09', f'{action}-seal-commit', ['X3b'], LABELS_INJ, [{'arm': f'{seal}.commit.{phase}#1={action}'}],
            {**left, 'scripted': 'CommitUndetermined', 'R2.witnessAction': witness})
    rename_after = position[f'{seal}.witness-committed/rename.after#1']
    for name in committed:
        survived = position[f'{name}#1'] >= rename_after
        row('F10', variant('kill', f'{name}#1'), ['X3b'], LABELS_KILL, kill_script(f'{name}#1'),
            {**left, 'R2.witnessAction': 'OK' if survived else 'ADVANCE'})
    # Mutation rows: R1 and R2 only (item 8).
    quarantine = {'scripted': COMMITTED, 'R1': 'unknown-quarantine-condition:*', 'R2.outcome': 'operation:LedgerCorrupt'}
    row('F20', 'witness-malformed', ['X6', 'X3b'], LABELS_MUT, [{'mutate': 'witness-malformed'}], dict(quarantine))
    row('F20', 'witness-mismatched-digest', ['X6', 'X3b'], LABELS_MUT, [{'mutate': 'witness-mismatched-digest'}], dict(quarantine))
    row('F21', 'witness-deleted', ['X6', 'X3b'], LABELS_MUT, [{'mutate': 'witness-deleted'}],
        {**quarantine, 'R1': 'unknown-quarantine-condition:witnesslessRestore'})
    hold = 'x3c.attempt.begin#1'
    row('F22', 'restore-earlier-carrier', ['X6', 'X3b'], LABELS_MUT,
        [{'arm': f'{hold}=hold'}, {'await': hold, 'then': 'copy-carrier-and-resume'}, {'mutate': 'restore-earlier-carrier'}],
        dict(quarantine))
    row('F22', 'tail-hash-changed', ['X6', 'X3b'], LABELS_MUT, [{'mutate': 'tail-hash-changed'}], dict(quarantine))
    for fmt in ('1', '2'):
        row('F31', f'inherited-format-{fmt}', ['X3b'], LABELS_MUT, [{'mutate': f'inherited-format-{fmt}'}],
            {'scripted': COMMITTED, 'R2.outcome': 'operation:HostIo'})
        row('F46', f'inherited-format-{fmt}', ['X6'], LABELS_MUT, [{'mutate': f'inherited-format-{fmt}'}],
            {'scripted': COMMITTED, 'R1': 'unknown-carrier-incompatible'})
    # F46's 'association below first_generation' is not transcribed: a fresh
    # carrier's first generation is 1 and the ledger's CHECK admits no
    # association generation below 1, so only a migrated carrier (L5) has one.
    document = {'schema': 'opensip.x9.required-runs.v1', 'clockEpoch': EPOCH, 'runs': rows}
    raw = json.dumps(document, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()
    open(sys.argv[4], 'wb').write(raw)
    counts = {}
    for r in rows:
        counts[r['case']] = counts.get(r['case'], 0) + 1
    print(json.dumps({'runs': len(rows), 'byCase': counts}, sort_keys=True))


if __name__ == '__main__':
    main()
