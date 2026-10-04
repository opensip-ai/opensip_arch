"""Transcribe X9 r16's 50 coverage rows ("unit": "X9-6") into both
required-runs.v1.json files.

Inputs, all made before any kill run: the landed storage and host
required-runs files (product main 2967905), X9-6's storage census
(x96-census-storage: census.json and census-trace.txt, parts commit,
recover, sweep, refused-end) and host's census (x96-census-host:
census.json). The uncovered points are the union kill set (r10/r11) less the
landed rows' kills; each point's crash window comes only from its position in
the census trace (r16's window table), and every expected value is r16's
(the owning law's existing row for that window), written here before any
run. Prior rows stay byte for byte. Standard library only.

usage: transcribe_x96.py <storage required> <host required> <storage census dir> <host census dir> <storage out> <host out>
"""
import copy
import json
import re
import sys

COMMITTED = 'Committed(latched=false)'
KILL = ['process-death', 'scripted-clock', 'synthetic']
LEFT = {'scripted': 'killed', 'R1': 'unknown-attempt-open', 'R2.outcome': COMMITTED,
        'R3': 'refused', 'R4': 'terminal-not-committed'}
CH = {'scripted': 'killed', 'R1': 'committed-historically:pendingSettlement:*', 'R2.outcome': COMMITTED,
      'R3': 'committed', 'R4': 'committed-historically:settled:*'}
UNITS = {'F02': ['X3c'], 'F07': ['X3b'], 'F11': ['X3c', 'X3d'], 'F13': ['X3c', 'X3d'], 'F14': ['X3d', 'X6'],
         'F16': ['X7'], 'F17': ['X7']}


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()


def kill_set(points):
    out = []
    for p in points:
        if p['durability']:
            n = p['occurrences']
            out += [f"{p['name']}#{k}" for k in sorted({1, (n + 1) // 2, n})]
    return out


def variant(prefix, point):
    name, k = point.rsplit('#', 1)
    return f"{prefix}-{re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')}-{k}"


def kills(row):
    return [s['await'] for s in row['script'] if isinstance(s, dict) and s.get('then') == 'kill']


def main():
    storage_raw, host_raw = open(sys.argv[1], 'rb').read(), open(sys.argv[2], 'rb').read()
    storage, host = json.loads(storage_raw), json.loads(host_raw)
    assert canonical(storage) == storage_raw and canonical(host) == host_raw
    s_census = json.load(open(sys.argv[3] + '/census.json'))
    h_census = json.load(open(sys.argv[4] + '/census.json'))
    union = {}
    for census in (s_census, h_census):
        for p in census['points']:
            if p['name'] in union:
                union[p['name']]['occurrences'] = max(union[p['name']]['occurrences'], p['occurrences'])
            else:
                union[p['name']] = dict(p)
    union_kill = kill_set([union[n] for n in sorted(union)])
    killed = {k for doc in (storage, host) for r in doc['runs'] for k in kills(r)}
    uncovered = [p for p in union_kill if p not in killed]
    # Positions per census part, from the storage trace.
    position = {}
    for i, line in enumerate(open(sys.argv[3] + '/census-trace.txt').read().splitlines()):
        part, _, _, point = line.split('|')[:4]
        position.setdefault(part, {}).setdefault(point, i)
    commit, sweep = position['commit'], position['sweep']
    at = lambda p: commit[p]
    seal_begin, built = at('x3b.append.seal.begin#1'), at('x3b.append.seal.built#1')
    w2_start = at('x3b.append.seal.witness-committed/directory-barrier.after#1')
    ev_before, ev_after = at('x3c.evidence.commit.before#1'), at('x3c.evidence.commit.after#1')
    published, end_floor = at('x3d.publish.published#1'), at('x3b.end.floor.probe/lock.before#1')
    attempt_after = at('x3c.attempt.commit.after#1')
    settle_before, settle_after = sweep['x6.sweep.settle.commit.before#1'], sweep['x6.sweep.settle.commit.after#1']
    f19 = next(r for r in storage['runs'] if r['case'] == 'F19' and r['variant'] == 'kill-x3b-append-rev-begin-1-after-revoke')
    f53 = {v: next(r for r in storage['runs'] if r['case'] == 'F53' and r['variant'] == v)
           for v in ('kill-x6-sweep-settle-commit-before-1', 'kill-x6-sweep-settle-commit-after-1')}
    new_storage, new_host, windows = [], [], {}

    def plain(case, point, expected, distinct=False):
        script = [{'arm': f'{point}=hold'}, {'await': point, 'then': 'kill'}] + ([{'r2': 'distinct'}] if distinct else [])
        return {'case': case, 'variant': variant('kill', point), 'units': UNITS[case], 'labels': KILL,
                'script': script, 'expected': dict(expected), 'unit': 'X9-6'}

    def swap(template, old, point, var):
        text = json.dumps(template['script']).replace(old, point)
        row = copy.deepcopy(template)
        row.update({'variant': var, 'script': json.loads(text), 'unit': 'X9-6'})
        return row

    for point in uncovered:
        name = point.rsplit('#', 1)[0]
        if point in commit:
            p = commit[point]
            assert p > attempt_after, point
            if name.startswith('x3c.object/'):
                w, row = 'W1a', plain('F02', point, LEFT)
            elif seal_begin <= p <= built:
                w, row = 'W1b', plain('F07', point, {**LEFT, 'R2.witnessAction': 'OK'})
            elif w2_start < p <= ev_before:
                w, row = 'W2', plain('F11', point, {**LEFT, 'R2.witnessAction': 'OK'})
            elif ev_after <= p < published:
                w, row = 'W3', plain('F13', point, CH, distinct=True)
            elif published < p < end_floor:
                w, row = 'W4', plain('F14', point, CH, distinct=True)
            else:
                raise SystemExit('no window for ' + point)
            new_storage.append(row)
        elif point in position['refused-end'] and point not in sweep:
            w = 'W5'
            new_storage.append(swap(f19, 'x3b.append.rev.begin#1', point, variant('kill', point) + '-after-revoke'))
        elif point in sweep:
            if sweep[point] < settle_before:
                w, template = 'W6a', f53['kill-x6-sweep-settle-commit-before-1']
                new_storage.append(swap(template, 'x6.sweep.settle.commit.before#1', point, variant('kill', point)))
            elif sweep[point] > settle_after:
                w, template = 'W6b', f53['kill-x6-sweep-settle-commit-after-1']
                new_storage.append(swap(template, 'x6.sweep.settle.commit.after#1', point, variant('kill', point)))
            else:
                raise SystemExit('no window for ' + point)
        elif name.startswith('x7.delivery.'):
            w = 'W7'
            case = 'F16' if name.startswith('x7.delivery.required') else 'F17'
            new_host.append({'case': case, 'variant': variant('kill', point), 'units': UNITS[case], 'labels': KILL,
                             'script': [{'r2': 'distinct'}, {'arm': f'{point}=hold'}, {'run': 'finalize'},
                                        {'await': point, 'then': 'kill'}],
                             'expected': {'finalize1': 'killed', 'R1': 'committed-historically:pendingSettlement',
                                          'R2.outcome': 'authoritative:0', 'R3': 'committed',
                                          'R4': 'committed-historically'},
                             'unit': 'X9-6'})
        else:
            raise SystemExit('no window for ' + point)
        windows.setdefault(w, []).append(point)
    old_runs = {'storage': canonical(storage['runs']), 'host': canonical(host['runs'])}
    for doc, new in ((storage, new_storage), (host, new_host)):
        ids = {(r['case'], r['variant']) for r in doc['runs']}
        for r in new:
            assert (r['case'], r['variant']) not in ids, r['variant']
            ids.add((r['case'], r['variant']))
        doc['runs'] = doc['runs'] + new
    out_s, out_h = canonical(storage), canonical(host)
    # Prior rows byte for byte: the old array is a prefix of the new.
    for raw, out, key, new in ((storage_raw, out_s, 'storage', new_storage), (host_raw, out_h, 'host', new_host)):
        before = old_runs[key]
        after = before[:-1] + b''.join(b',' + canonical(r) for r in new) + b']'
        assert raw.count(before) == 1 and out == raw.replace(before, after), 'prior bytes changed'
    open(sys.argv[5], 'wb').write(out_s)
    open(sys.argv[6], 'wb').write(out_h)
    print(json.dumps({'uncovered': len(uncovered), 'storageRuns': len(storage['runs']), 'hostRuns': len(host['runs']),
                      'windows': {k: len(v) for k, v in sorted(windows.items())},
                      'byCase': {c: sum(1 for r in new_storage + new_host if r['case'] == c)
                                 for c in sorted({r['case'] for r in new_storage + new_host})}}, sort_keys=True))


if __name__ == '__main__':
    main()
