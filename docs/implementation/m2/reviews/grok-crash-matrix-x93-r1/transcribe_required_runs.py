"""Transcribe X9-2's and X9-3's rows of law X9 r9 item 9 into required-runs.v1.json.

Inputs, all made before any kill run: the unarmed census of X9-2's commit
driver (census.json: points with occurrences; census-trace.txt: the trace in
order), and X9 r9's unarmed reference run (reference.json: (A) the
publication's new trust entries in creation order at ordinal 1, (B) the files
the next publication writes at ordinal 2, on the same installation). Only
the kill points, their order and each X4T dependency occurrence's collision
come from these (items 5 and 9, r9); every expected value is the law's row,
written here before any run and never read back from one. Standard library
only.

X9-3 (unit X9-3) extends it: with a fourth input, X9-3's unarmed census
(x93-census.json: the union of its commit, recover and sweep drivers'
censuses, X9 r8 item 5), X9-3's rows are appended after X9-2's, which are
unchanged byte for byte. X9-3's kill points come from that census; every
expected value is the law's row (X9 r9 item 9, with the owning laws it
names), written here before any run. X9-3's rows follow law X9 r14.

usage: transcribe_required_runs.py <census.json> <census-trace.txt> <reference.json> [<x93-census.json>] <out>
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
    out_path = sys.argv[-1]
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
    if len(sys.argv) == 6:
        x93_rows(json.load(open(sys.argv[4])), row)
    document = {'schema': 'opensip.x9.required-runs.v1', 'clockEpoch': EPOCH, 'runs': rows}
    raw = json.dumps(document, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()
    open(out_path, 'wb').write(raw)
    counts = {}
    for r in rows:
        counts[r['case']] = counts.get(r['case'], 0) + 1
    print(json.dumps({'runs': len(rows), 'byCase': counts}, sort_keys=True))


UAO = 'unknown-attempt-open'
UAU = 'unknown-attempt-unobserved'
UB = 'unavailable-busy'
TNC = 'terminal-not-committed'
UC = 'unknown-custody:*'
CH_PENDING = 'committed-historically:pendingSettlement:*'
CH_SETTLED = 'committed-historically:settled:*'
LABELS = ['scripted-clock', 'synthetic']
# X3d item 7 with X3c item 10: after an undetermined evidence COMMIT nothing
# is owed or appended, the settlement reserve is forfeited (no settlement
# failure), and the end step does not run.
UNDETERMINED_END = 'end(rev=false,cln=false,settlement=None,step=false,stepFailure=None)'


def x93_rows(census, row):
    """X9-3's rows (X9 r14 item 12, with r12's and r14's corrections): F11-F15, F23-F25, F27-F29, F33, F36,
    F42-F45, F49, F52 and F53. Kill points come from X9-3's census; each
    expected value is the law's row (item 9) or the owning law it names."""
    names = {p['name'] for p in census['points']}

    def point(name, k=1):
        assert name in names, name
        return f'{name}#{k}'

    left = {'scripted': 'killed', 'R1': UAO, 'R2.outcome': COMMITTED, 'R3': 'refused', 'R4': TNC}
    pending = {'scripted': 'killed', 'R1': CH_PENDING, 'R2.outcome': COMMITTED, 'R3': 'committed', 'R4': CH_SETTLED}
    # F11: a kill after each staged evidence table; the transaction rolls
    # back, the SEAL stays durable with no REV (item 9).
    stages = sorted(n for n in names if n.startswith('x3c.evidence.stage-'))
    for name in stages:
        row('F11', variant('kill', point(name)), ['X3c', 'X3d'], LABELS_KILL, kill_script(point(name)), dict(left))
    # F12: the evidence COMMIT fails after landing, or before.
    for phase, action, landed in (('after', 'fail-after', True), ('before', 'fail-before', False)):
        arm = f"{point(f'x3c.evidence.commit.{phase}')}={action}"
        row('F12', f'{action}-evidence-commit', ['X3c', 'X3d', 'X7'], LABELS_INJ, [{'arm': arm}],
            {'scripted': 'CommitUndetermined', 'scripted.end': UNDETERMINED_END,
             'R1': CH_PENDING if landed else UAO, 'R3': 'committed' if landed else 'refused',
             'R4': CH_SETTLED if landed else TNC})
    # F13 and F14: after the evidence COMMIT returned; F14's second kill is
    # the law's `x3d.finish.settle.before` (as F13).
    # X9 r12: R2 of F13, F14 and F15 commits the distinct candidate
    # variant; F14's `x3d.finish.settle.before` kill is X9-4's.
    distinct = [{'r2': 'distinct'}]
    p = point('x3d.publish.commit-returned')
    row('F13', variant('kill', p), ['X3c', 'X3d'], LABELS_KILL, kill_script(p) + distinct, dict(pending))
    p = point('x3d.publish.published')
    row('F14', variant('kill', p), ['X3d', 'X6'], LABELS_KILL, kill_script(p) + distinct, dict(pending))
    # F15: after the end step; R1 CH, and R2 (distinct, r12) Committed with
    # no second receipt for this ExecutionId.
    p = point('x3d.finish.end-step.after')
    row('F15', variant('kill', p), ['X6'], LABELS_KILL, kill_script(p) + distinct,
        {'scripted': 'killed', 'R1': 'committed-historically:*', 'R2.outcome': COMMITTED, 'R2.receipts': '1'})
    # F23: one half of the pair deleted (after the evidence COMMIT, the
    # attempt admitted); R1 UC, R3 writes nothing (one-sided).
    p = point('x3d.publish.commit-returned')
    for half in ('receipt', 'association'):
        row('F23', f'delete-{half}', ['X6'], LABELS_DEATH_MUT,
            kill_script(p) + [{'mutate': f'delete-{half}'}, {'ladder': 'R1,R2,R3'}],
            {'scripted': 'killed', 'R1': UC, 'R3': 'nothing', 'R3.left': 'one-sided'})
    # F24: an unreadable ledger or a wrong generation, over an admitted
    # attempt; R1 UC, R2 refused on its X3c or X3a row, R3 host I/O and
    # nothing written.
    p = point('x3c.attempt.commit.after')
    x3c_rows = ['not-prepared:Refused(HostIo)', 'not-prepared:Refused(LedgerCorrupt)',
                'not-prepared:Refused(Custody { subject: "private" })', 'operation:HostIo']
    for kind in ('ledger-mode-000', 'ledger-truncated-header'):
        row('F24', kind, ['X6', 'X3a'], LABELS_DEATH_MUT,
            kill_script(p) + [{'mutate': kind}, {'ladder': 'R1,R2,R3'}],
            {'scripted': 'killed', 'R1': UC, 'R2.outcome': list(x3c_rows), 'R3': 'nothing', 'R3.report': 'Unreadable'})
    # X9 r12: the owner's §2 "both absent, no row" under the admitted digest.
    row('F24', 'wrong-store-generation', ['X6', 'X3a'], LABELS_DEATH_MUT,
        kill_script(p) + [{'mutate': 'wrong-store-generation'}, {'ladder': 'R1,R2,R3'}],
        {'scripted': 'killed', 'R1': UAU, 'R2.outcome': COMMITTED, 'R3': 'nothing', 'R3.report': 'swept'})
    # F25: a committed object deleted or flipped; R1 CAD with its detail.
    # X9 r14: R1 only (R2 would re-commit the same Run at a drawn position).
    for kind, detail in (('object-deleted', 'evidence.missing'), ('object-flipped', 'evidence.corrupt')):
        row('F25', kind, ['X6'], LABELS_MUT, [{'mutate': kind}, {'ladder': 'R1'}],
            {'scripted': COMMITTED, 'R1': f'committed-availability-degraded:{detail}:*'})
    # F27: the association's binding swapped, or a request with another
    # binding; R1 BU.
    # X9 r12: the operation and execution swaps fail the snapshot's join.
    for member, standing in (('store-generation', 'binding-unusable:*'), ('namespace', 'binding-unusable:*'),
                             ('operation', 'unknown-custody:ledger-join'), ('execution', 'unknown-custody:ledger-join')):
        row('F27', f'association-{member}', ['X6'], LABELS_MUT, [{'mutate': f'association-{member}'}],
            {'scripted': COMMITTED, 'R1': standing})
    row('F27', 'request-operation', ['X6'], list(LABELS), [{'request': 'binding-operation'}, {'ladder': 'R1'}],
        {'scripted': COMMITTED, 'R1': 'binding-unusable:operation'})
    # F28: X6a's pruned-record shape, read in a fresh process; R1 UC.
    row('F28', 'pruned-generations', ['X6'], LABELS_MUT, [{'mutate': 'pruned-generations'}],
        {'scripted': COMMITTED, 'R1': UC})
    # F29: a reader while the writer holds; never mixed, no wait.
    for name, standing in (('x3c.attempt.commit.after', UAO),
                           ('x3b.append.seal.witness-committed/directory-barrier.after', UAO),
                           ('x3d.publish.after-staging', UAO),
                           ('x3d.publish.commit-returned', CH_PENDING)):
        p = point(name)
        row('F29', variant('reader-at', p), ['X6'], list(LABELS),
            [{'spawn': 'commit', 'name': 'writer', 'arm': f'{p}=hold'},
             {'await': p, 'on': 'writer', 'then': 'hold'},
             {'spawn': 'reader', 'name': 'reader', 'for': 'writer'},
             {'finish': 'reader'},
             {'resume': p, 'on': 'writer'},
             {'finish': 'writer'}],
            {'writer': COMMITTED, 'reader': standing})
    # F33: receipt bytes, signer, inventory or SEAL body digest altered.
    for kind in ('receipt-assurance', 'receipt-signer', 'run-material-inventory', 'association-seal-digest'):
        row('F33', kind, ['X6'], LABELS_MUT, [{'mutate': kind}], {'scripted': COMMITTED, 'R1': UC})
    # F36: the orphan SEALs of F09 and F11, then R2 commits the same RunId.
    for p in (point('x3b.append.seal.commit.after'), point(stages[0])):
        row('F36', variant('orphan', p), ['X3b', 'X3c', 'X6'], LABELS_KILL,
            kill_script(p) + [{'ladder': 'R1,R2,R3,R4,R5'}],
            {**left, 'R5': CH_SETTLED, 'R5.sameRunId': 'true'})
    # F42: a forgotten stopped session (after an evidence COMMIT that did
    # not land); and a reader during a held point.
    arm = f"{point('x3c.evidence.commit.before')}=fail-before"
    row('F42', 'forget-stopped-session', ['X3d'], LABELS_INJ, [{'arm': arm}, {'commit': 'forget'}],
        {'scripted': 'CommitUndetermined', 'scripted.end': 'forgotten', 'R1': UAO, 'R2.outcome': COMMITTED,
         'R3': 'refused', 'R4': TNC})
    p = point(stages[-1])
    row('F42', variant('reader-at', p), ['X3d'], list(LABELS),
        [{'spawn': 'commit', 'name': 'writer', 'arm': f'{p}=hold'},
         {'await': p, 'on': 'writer', 'then': 'hold'},
         {'spawn': 'reader', 'name': 'reader', 'for': 'writer'},
         {'finish': 'reader'},
         {'resume': p, 'on': 'writer'},
         {'finish': 'writer'}],
        {'writer': COMMITTED, 'reader': [UB, UAO]})
    # F43: the journal tail lost below the association's journalSeq.
    row('F43', 'journal-tail-lost', ['X6'], LABELS_MUT, [{'mutate': 'journal-tail-lost'}],
        {'scripted': COMMITTED, 'R1': [UB, 'unknown-quarantine-condition:*']})
    # F44 and F45: F39's script (admission, revocation, one observer tick,
    # the latch after admission), then A holds in its end-path REV append
    # while a reader recovers A's attempt. A is held after admission at
    # `x3c.evidence.commit.before`, the first point after the checkpoint
    # releases the shared monitor: held at `x4.gate.admit.after`, inside the
    # monitor, the observer's tick cannot take the monitor to latch (X9 r12:
    # law for F39, F44 and F45).
    admit = point('x3c.evidence.commit.before')
    tick = point('x4.observer.tick')
    latch = 'x4.gate.latch.after#1'
    for case, p, standing in (
            ('F44', 'x3b.append.rev.witness-pending/directory-barrier.after#1',
             'unknown-custody:pending-above-floor:witnessWouldRevert'),
            ('F45', 'x3b.append.rev.commit.after#1',
             'committed-historically:pendingSettlement:witness-pending-at-tail:witnessWouldAdvance:interior-bodies-not-authenticated')):
        row(case, variant('reader-at', p), ['X6'], list(LABELS),
            [{'spawn': 'commit', 'name': 'writer', 'arm': f"{tick.split('#')[0]}#*=hold,{admit}=hold,{p}=hold"},
             {'await': tick, 'on': 'writer', 'then': 'hold'},
             {'await': admit, 'on': 'writer', 'then': 'hold'},
             {'spawn': 'revoke', 'name': 'publisher', 'for': 'writer'},
             {'finish': 'publisher'},
             {'resume': tick, 'on': 'writer'},
             {'await': latch, 'on': 'writer', 'then': 'pass'},
             {'resume': admit, 'on': 'writer'},
             {'await': p, 'on': 'writer', 'then': 'hold'},
             {'spawn': 'reader', 'name': 'reader', 'for': 'writer'},
             {'finish': 'reader'},
             {'resume': p, 'on': 'writer'},
             {'finish': 'writer'}],
            {'writer': 'Committed(latched=true)', 'reader': standing})
    # F49 (a): a reader holds between bracket reads while a lawful writer
    # appends; (b) a reader's stale snapshot while the writer completes.
    j = point('x6.recover.after-j')
    row('F49', 'reader-skewed-by-append', ['X6'], list(LABELS),
        [{'spawn': 'commit', 'name': 'first'},
         {'finish': 'first'},
         {'spawn': 'reader', 'name': 'reader', 'for': 'first', 'arm': f'{j}=hold'},
         {'await': j, 'on': 'reader', 'then': 'hold'},
         {'spawn': 'commit', 'name': 'second'},
         {'finish': 'second'},
         {'resume': j, 'on': 'reader'},
         {'finish': 'reader'}],
        {'first': COMMITTED, 'reader': CH_PENDING})  # X9 r12
    a = point('x3c.attempt.commit.after')
    snap = point('x6.recover.after-ledger-snapshot')
    row('F49', 'reader-snapshot-before-commit', ['X6'], list(LABELS),
        [{'spawn': 'commit', 'name': 'writer', 'arm': f'{a}=hold'},
         {'await': a, 'on': 'writer', 'then': 'hold'},
         {'spawn': 'reader', 'name': 'reader', 'for': 'writer', 'arm': f'{snap}=hold'},
         {'await': snap, 'on': 'reader', 'then': 'hold'},
         {'resume': a, 'on': 'writer'},
         {'finish': 'writer'},
         {'resume': snap, 'on': 'reader'},
         {'finish': 'reader'}],
        {'writer': COMMITTED, 'reader': [UAO, UB]})
    # F52: the settlement matrix's eleven cells; exactly one is TNC.
    row('F52', 'admitted-none', ['X6'], LABELS_KILL, kill_script(a), dict(left))
    row('F52', 'admitted-both', ['X6'], list(LABELS), [{'ladder': 'R1'}], {'scripted': COMMITTED, 'R1': CH_PENDING})
    row('F52', 'settled-committed-both', ['X6'], list(LABELS),
        [{'spawn': 'commit', 'name': 'writer'}, {'finish': 'writer'},
         {'spawn': 'sweep', 'name': 'sweep', 'for': 'writer'}, {'finish': 'sweep'},
         {'ladder': 'R1', 'of': 'writer'}],
        {'writer': COMMITTED, 'sweep': 'committed', 'R1': CH_SETTLED})
    row('F52', 'settled-refused-none', ['X6'], LABELS_KILL,
        [{'spawn': 'commit', 'name': 'writer', 'arm': f'{a}=hold'},
         {'await': a, 'on': 'writer', 'then': 'kill'},
         {'spawn': 'sweep', 'name': 'sweep', 'for': 'writer'}, {'finish': 'sweep'},
         {'ladder': 'R1', 'of': 'writer'}],
        {'writer': 'killed', 'sweep': 'refused', 'R1': TNC})
    for cell, base, kind, standing in (
            ('settled-refused-both', None, 'settle-refused', UC),
            ('settled-committed-none', a, 'settle-committed', UC),
            ('no-row-none', a, 'delete-attempt', UAU),
            ('no-row-both', None, 'delete-attempt', 'committed-historically:legacyCustodyUnknown:*'),
            ('receipt-only', None, 'delete-association', UC),
            ('association-only', None, 'delete-receipt', UC),
            ('purged', None, 'availability-purged', 'committed-availability-degraded:evidence.purged:*')):
        if base:
            row('F52', cell, ['X6'], LABELS_DEATH_MUT, kill_script(base) + [{'mutate': kind}],
                {'scripted': 'killed', 'R1': standing})
        else:
            row('F52', cell, ['X6'], LABELS_MUT, [{'mutate': kind}], {'scripted': COMMITTED, 'R1': standing})
    # F53: the sweep over live, crashed, one-sided, inaccessible and already
    # settled attempts, and killed at its settle COMMIT.
    crashed = [{'spawn': 'commit', 'name': 'writer', 'arm': f'{a}=hold'}, {'await': a, 'on': 'writer', 'then': 'kill'}]
    sweep = [{'spawn': 'sweep', 'name': 'sweep', 'for': 'writer'}, {'finish': 'sweep'}]
    r1 = [{'ladder': 'R1', 'of': 'writer'}]
    row('F53', 'live', ['X6c'], list(LABELS),
        [{'spawn': 'commit', 'name': 'writer', 'arm': f'{a}=hold'},
         {'await': a, 'on': 'writer', 'then': 'hold'}] + sweep +
        [{'resume': a, 'on': 'writer'}, {'finish': 'writer'}],
        {'sweep': 'nothing', 'sweep.report': 'busy', 'writer': COMMITTED})
    row('F53', 'crashed', ['X6c'], LABELS_KILL, crashed + sweep + r1,
        {'writer': 'killed', 'sweep': 'refused', 'R1': TNC})
    c = point('x3d.publish.commit-returned')
    row('F53', 'one-sided', ['X6c'], LABELS_DEATH_MUT,
        [{'spawn': 'commit', 'name': 'writer', 'arm': f'{c}=hold'}, {'await': c, 'on': 'writer', 'then': 'kill'},
         {'mutate': 'delete-association', 'of': 'writer'}] + sweep,
        {'writer': 'killed', 'sweep': 'nothing', 'sweep.left': 'one-sided'})
    row('F53', 'inaccessible', ['X6c'], LABELS_DEATH_MUT,
        crashed + [{'mutate': 'ledger-mode-000', 'of': 'writer'}] + sweep,
        {'writer': 'killed', 'sweep': 'nothing', 'sweep.report': 'Unreadable'})
    row('F53', 'already-settled', ['X6c'], LABELS_KILL,
        crashed + [{'spawn': 'sweep', 'name': 'first', 'for': 'writer'}, {'finish': 'first'},
                   {'spawn': 'sweep', 'name': 'second', 'for': 'writer'}, {'finish': 'second'}] + r1,
        {'writer': 'killed', 'first': 'refused', 'second': 'nothing', 'R1': TNC})
    for phase, second in (('before', 'refused'), ('after', 'nothing')):
        k = point(f'x6.sweep.settle.commit.{phase}')
        row('F53', variant('kill', k), ['X6c'], LABELS_KILL,
            crashed + [{'spawn': 'sweep', 'name': 'first', 'for': 'writer', 'arm': f'{k}=hold'},
                       {'await': k, 'on': 'first', 'then': 'kill'},
                       {'spawn': 'sweep', 'name': 'second', 'for': 'writer'}, {'finish': 'second'}] + r1,
            {'writer': 'killed', 'first': 'killed', 'second': second, 'R1': TNC})


if __name__ == '__main__':
    main()
