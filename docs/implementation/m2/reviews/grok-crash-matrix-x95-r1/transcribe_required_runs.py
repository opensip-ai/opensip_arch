"""Transcribe X9-5's rows of law X9 r15 item 9 (with r13's host rulings) into host's required-runs.v1.json.

Inputs, all made before any kill run: X9 r11's host census (census.json:
the union of three unarmed runs, each run twice and equal) and the trace of
its run (b), the exhausted-carrier `finalize` whose `finish` runs the
rollover (census-trace-b.txt). Only F32's kill points and their place in
X3b item 13's crash table come from these (items 5 and 9); every expected
value is the law's row, or the owning law's outcome it names, written here
before any run and never read back from one. Standard library only.

usage: transcribe_required_runs.py <census.json> <census-trace-b.txt> <out>
"""
import json
import re
import sys

EPOCH = 1791072000  # storage's file's clockEpoch (X9 r10: the same epoch)
SYN = ['scripted-clock', 'synthetic']
LABELS = SYN
LABELS_INJ = ['injected'] + SYN
LABELS_KILL = ['process-death'] + SYN
LABELS_MUT = ['mutation'] + SYN
LABELS_MUT_KILL = ['mutation', 'process-death'] + SYN

DELIVERY = 'terminated:DELIVERY.REQUIRED_FAILED/DELIVERY.RENDERER_FAILED_AFTER_COMMIT'
DURABILITY = 'terminated:DURABILITY.COMMIT_FAILED/-'
BUSY = 'terminated:LEDGER.BUSY_TIMEOUT/PROJECT.BUSY'
INVARIANT = 'terminated:SYSTEM.OUTCOME.ILLEGAL_STATE/HOST.INVARIANT_VIOLATED'
AUTHORITATIVE = 'authoritative:0'
CH = 'committed-historically'
UC_MISSING = 'unknown-custody:ledger-missing'
UAU = 'unknown-attempt-unobserved'
# X9 r12: F39's script holds at the first point after admission where the
# shared monitor is released.
HOLD = 'x3c.evidence.commit.before#1'
REVOKE = ['x4.observer.tick#*=hold', f'{HOLD}=hold']
DISTINCT = {'r2': 'distinct'}


def kill_set(points):
    out = []
    for p in points:
        if p['durability']:
            n = p['occurrences']
            for k in sorted({1, (n + 1) // 2, n}):
                out.append(f"{p['name']}#{k}")
    return out


def slug(point):
    name, k = point.rsplit('#', 1)
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-') + f'-{k}'


def main():
    census = json.load(open(sys.argv[1]))
    trace_b = [line.split('|') for line in open(sys.argv[2]).read().splitlines()]
    kills = set(kill_set(census['points']))
    position = {}
    for i, fields in enumerate(trace_b):
        point = fields[2]
        if point != '-' and point not in position:
            position[point] = i
    rows = []

    def row(case, variant, units, labels, script, expected):
        rows.append({'case': case, 'variant': variant, 'units': units, 'labels': labels,
                     'script': script, 'expected': expected})

    # F01 (X5 r3 items 3, 5 and 7; X3d item 3 step 1): refused before
    # prepare_commit writes anything; no attempt row; no SEAL; the ledger and
    # carrier logical state unchanged. A replay refusal ends before any
    # custody, so the whole state is unchanged.
    # r13: the replay-refused variants leave the whole post-state unchanged;
    # the substituted variants add exactly the latched gate's one REV.
    f01 = {'attemptRows': '0', 'sealRows': '0', 'ledgerPresent': 'false',
           'finalize1.runId': 'no', 'finalize1.deliveryPhase': 'not-started'}
    for variant, outcome, subject, remedy, replay in (
            ('replay-run-object-missing', 'terminated:HOST.IO_FAILURE/evidence.missing', 'runId', 'evidence-missing', True),
            ('replay-run-descriptor-altered', 'terminated:PROVIDER.PROTOCOL_VIOLATION/EVALUATION.INPUT_REFUSED', '-', 'input-refused', True),
            ('substituted-target', INVARIANT, '-', '-', False),
            ('substituted-inventory', INVARIANT, '-', '-', False)):
        expected = {**f01, 'finalize1': outcome, 'finalize1.subject': subject, 'finalize1.remedy': remedy}
        if replay:
            expected.update({'stateUnchanged': 'true', 'ledgerCarrierUnchanged': 'true', 'carrierAdded': ''})
        else:
            expected['carrierAdded'] = 'REV'
        row('F01', variant, ['X5'], LABELS, [{'candidate': variant}, {'run': 'finalize'}], expected)

    # F12 and F40's caller route (X7 items 3 and 5): the durability row, the
    # ExecutionId as subject, the namespace beside it, no RunId, the later
    # recovery remedy, no delivery. Ladder per F12's row.
    def undetermined(phase):
        landed = phase == 'after'
        return {'finalize1': DURABILITY, 'finalize1.subject': 'executionId', 'finalize1.runId': 'no',
                'finalize1.namespace': 'yes', 'finalize1.remedy': 'commit-undetermined',
                'finalize1.deliveryPhase': 'not-started',
                'R1': f'{CH}:pendingSettlement' if landed else 'unknown-attempt-open',
                'R3': 'committed' if landed else 'refused',
                'R4': CH if landed else 'terminal-not-committed'}

    for phase in ('after', 'before'):
        arm = f'x3c.evidence.commit.{phase}#1=fail-{phase}'
        landed = phase == 'after'
        # r13: after a committed (landed) Run, R2 commits r12's distinct
        # variant and is expected Committed.
        r2 = [DISTINCT] if landed else []
        extra = {'R2.outcome': AUTHORITATIVE} if landed else {}
        for case, units in (('F12', ['X3c', 'X3d', 'X7']), ('F40', ['X3d', 'X7'])):
            row(case, f'fail-{phase}-evidence-commit', units, LABELS_INJ,
                r2 + [{'arm': arm}, {'run': 'finalize'}], {**undetermined(phase), **extra})
    # F40 with F39's latch (r13): landed only, r12's admission hold, the
    # latch does not convert it; R2 is refused at admission (C5), unscored.
    row('F40', 'latched-fail-after-evidence-commit', ['X3d', 'X7'], LABELS_INJ,
        [DISTINCT] + [{'arm': a} for a in REVOKE] + [{'arm': 'x3c.evidence.commit.after#1=fail-after'}, {'run': 'finalize'},
                                                    {'await': HOLD, 'then': 'revoke-latch-resume'}],
        {**undetermined('after'), 'finalize1.gateLatched': 'true'})

    # F16 (X7 items 3 and 4): DELIVERY.REQUIRED_FAILED, exit 4, the RunId
    # kept; R1 CH (the standing; X9 names no typed member).
    row('F16', 'fail-before-required-delivery', ['X7'], LABELS_INJ,
        [DISTINCT, {'arm': 'x7.delivery.required.before#1=fail-before'}, {'run': 'finalize'}],
        {'finalize1': DELIVERY, 'finalize1.exit': '4', 'finalize1.runId': 'yes',
         'finalize1.remedy': 'renderer-failed-after-commit', 'finalize1.delivered': '0', 'R1': f'{CH}:*',
         'R2.outcome': AUTHORITATIVE})
    # F17 (L9): committed; the optional failure disclosed; result unchanged.
    row('F17', 'fail-before-optional-delivery', ['X7'], LABELS_INJ,
        [DISTINCT, {'arm': 'x7.delivery.optional.before#1=fail-before'}, {'run': 'finalize'}],
        {'finalize1': AUTHORITATIVE, 'finalize1.optional': 'failed', 'finalize1.delivered': '19',
         'finalize1.runId': 'claimed', 'R1': f'{CH}:*', 'R2.outcome': AUTHORITATIVE})
    # F39's delivery half: committed with latchedAfterAdmission; host
    # projects DELIVERY.REQUIRED_FAILED with the RunId and starts no delivery
    # phase; R1 CH.
    row('F39', 'latched-after-admission-delivery', ['X3d', 'X4', 'X7'], LABELS,
        [DISTINCT] + [{'arm': a} for a in REVOKE] + [{'run': 'finalize'},
                                                    {'await': HOLD, 'then': 'revoke-latch-resume'}],
        {'finalize1': DELIVERY, 'finalize1.runId': 'yes', 'finalize1.remedy': 'renderer-failed-after-commit',
         'finalize1.deliveryPhase': 'not-started', 'finalize1.gateLatched': 'true', 'R1': f'{CH}:*'})

    # F32 (X7 items 6 and 6a; X3b items 5a and 13), over the reserved-slot
    # setup. At ...987 a SEAL still fits (it takes ...988), so the attempt
    # commits and the next writer meets the exhausted generation. At ...988
    # no SEAL fits: CarrierCapacityExhausted, finish, the rollover in the end
    # step (G+1 opened), the busy row naming N; the next writer proceeds in
    # G+1. The exhausted attempt writes no ledger (X3d item 3 step 3), so R1
    # is UC ledger-missing (X6 F24) and R4 is UAU once a writer created it.
    # r13: the planted tail is not contiguous from 1, so recovery
    # quarantines (owner's section 2, "sequence contiguity 1..t"); R2 commits
    # the distinct variant and reaches the exhausted generation first.
    contiguity = 'unknown-quarantine-condition:journalContiguity'
    row('F32', 'tail-987', ['X3b-4', 'X7b'], LABELS_MUT, [DISTINCT, {'plant': 'tail-987'}, {'run': 'finalize'}],
        {'finalize1': AUTHORITATIVE, 'R1': contiguity, 'R2.outcome': BUSY, 'R2.rollover': 'rolled:2', 'R4': contiguity})
    row('F32', 'tail-988', ['X3b-4', 'X7b'], LABELS_MUT, [{'plant': 'tail-988'}, {'run': 'finalize'}],
        {'finalize1': BUSY, 'finalize1.subject': 'namespace', 'finalize1.rollover': 'rolled:2',
         'finalize1.endStep': '-', 'attemptRows': '0', 'R1': UC_MISSING, 'R2.outcome': AUTHORITATIVE,
         'R2.rollover': '-', 'R3': 'nothing', 'R4': UAU})
    # Each kill in the rollover, from its reservation to the end step's
    # fence release, at its census (b) position in X3b item 13's crash table.
    start = position['x3b.rollover.reserved#1']
    end = position['x2.fence.end/unlock.after#1']
    pending = position['x3b.append.terminal.witness-pending/rename.after#1']
    terminal = position['x3b.append.terminal.commit.after#1']
    opened = position['x3b.rollover.open.witness/rename.after#1']
    floor = position['x3b.end.floor.write/rename.after#1']
    assert start < pending < terminal < opened < floor < end
    f32_kills = sorted((p for p, at in position.items() if start <= at <= end and p in kills), key=position.get)
    for point in f32_kills:
        at = position[point]
        if at < terminal:
            # Nothing durable, or a PENDING witness with no row: the next
            # writer (REVERTs, then) finds G exhausted again and its own end
            # step runs the rollover with a fresh token.
            r2 = {'R2.witnessAction': 'OK' if at < pending else 'REVERT', 'R2.outcome': BUSY,
                  'R2.rollover': 'rolled:2', 'R4': UC_MISSING}
        else:
            # X3b item 4a case 2 (item 13 step 3's table): a TERMINAL tail
            # whose witness reconciles OK or ADVANCE against it takes one
            # action, OPEN: the witness COMMITTED (G+1, 0). Item 13's crash
            # table's "ADVANCEs on the closing tail, which is OPEN" is that
            # one write. Once the G+1 witness is durable, the start is OK.
            action = 'OPEN' if at < opened else 'OK'
            r2 = {'R2.witnessAction': action, 'R2.outcome': AUTHORITATIVE, 'R2.rollover': '-', 'R4': UAU}
        row('F32', 'kill-' + slug(point), ['X3b-4', 'X7b'], LABELS_MUT_KILL,
            [{'plant': 'tail-988'}, {'arm': f'{point}=hold'}, {'run': 'finalize'}, {'await': point, 'then': 'kill'}],
            {'finalize1': 'killed', 'attemptRows': '0', 'R1': UC_MISSING, 'R3': 'nothing', **r2})

    # F53's store-gc step (X6 r3 item 7, X6c): skip, settle, or write
    # nothing; after a killed sweep the next sweep settles each row exactly
    # once.
    swept = lambda settled: f'swept[settled={settled};left=;more=false;stopped=-]:row=-;ended=-'
    hold = 'x3c.attempt.commit.after#1'
    crashed = [{'arm': f'{hold}=hold'}, {'run': 'finalize'}, {'await': hold, 'then': 'kill'}]
    row('F53', 'store-gc-committed', ['X6c'], LABELS,
        [{'run': 'finalize'}, {'run': 'store-gc'}, {'run': 'store-gc'}],
        {'finalize1': AUTHORITATIVE, 'gc1': swept('committed'), 'gc2': swept('')})
    row('F53', 'store-gc-crashed', ['X6c'], LABELS_KILL,
        crashed + [{'run': 'store-gc'}, {'run': 'store-gc'}],
        {'finalize1': 'killed', 'gc1': swept('refused'), 'gc2': swept('')})
    row('F53', 'store-gc-live', ['X6c'], LABELS,
        [{'arm': f'{hold}=hold'}, {'run': 'finalize'}, {'await': hold, 'then': 'store-gc-resume'}, {'run': 'store-gc'}],
        {'gc1': 'skipped:row=-;ended=-', 'finalize1': AUTHORITATIVE, 'gc2': swept('committed')})
    row('F53', 'store-gc-inaccessible', ['X6c'], LABELS_MUT,
        [{'run': 'finalize'}, {'mutate': 'ledger-mode-000'}, {'run': 'store-gc'},
         {'mutate': 'ledger-mode-restore'}, {'run': 'store-gc'}],
        {'finalize1': AUTHORITATIVE, 'gc1': 'Unreadable:row=HOST.IO_FAILURE/-;ended=-', 'gc2': swept('committed')})
    for phase, next_settles in (('before', 'refused'), ('after', '')):
        point = f'x6.sweep.settle.commit.{phase}#1'
        assert point in kills, point
        row('F53', f'kill-sweep-settle-commit-{phase}', ['X6c'], LABELS_KILL,
            crashed + [{'arm': f'{point}=hold'}, {'run': 'store-gc'}, {'await': point, 'then': 'kill'},
                       {'run': 'store-gc'}, {'run': 'store-gc'}],
            {'finalize1': 'killed', 'gc1': 'killed', 'gc2': swept(next_settles), 'gc3': swept('')})

    for r in rows:
        for step in r['script']:
            if 'r2' in step:
                continue
            if step.get('then') == 'kill' or 'arm' in step:
                p = step.get('await') or step['arm'].split('=')[0]
                if not p.endswith('#*'):
                    assert p.split('#')[0] in {q['name'] for q in census['points']}, p
            if step.get('then') == 'kill':
                assert step['await'] in kills, step['await']
    document = {'schema': 'opensip.x9.required-runs.v1', 'clockEpoch': EPOCH, 'runs': rows}
    raw = json.dumps(document, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()
    open(sys.argv[3], 'wb').write(raw)
    counts = {}
    for r in rows:
        counts[r['case']] = counts.get(r['case'], 0) + 1
    print(json.dumps({'runs': len(rows), 'byCase': counts, 'f32Kills': len(f32_kills)}, sort_keys=True))


if __name__ == '__main__':
    main()
