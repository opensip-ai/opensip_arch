"""Build (or, with --check, verify) D2b-2's transition-table vectors (LD-D2B-4, D2b-T1).

The expected outcomes are the reference interpreters' own, run unchanged: trial 07's `tools/admission_ref.py`
`overlay_run` (the P3T table with the carriers' Rust overlay, the production major-3 table), the published
`native_evidence_model.v2.protocol3_run` (the base P3T table), and `provider_startup_model.v1.typescript_protocol2_run`
(T2O). Each function, and the module constants it reads, is extracted from its module's source with `ast` and executed
alone: the startup model imports `referencing` at module level, which the reference interpreters do not use and this
environment does not have. Nothing in them is restated here.

The traces: every event sequence of a breadth-first exploration of each table's reachable states (shortest path to
each distinct state), extended by every event of the alphabet (every frame any row names, the process observations,
`zero-exit`, `eof` and one unknown frame), under the observation variants the tables read (HelloAck negotiated or
not; OpenUniverse's dependency and prepared modes; Analyze under one and two stages; TS2's Unavailable payload
pre- and post-analyze). So every row, both catch-alls, the post-terminal law, the absorbing FAULT and the total
fallback over every reachable (state, event) pair are replayed. Trial 07's scripted transition traces are added as
nodes, and native-cases.v2's six protocol3_run cases are recorded with their own expectations asserted.

Usage: build_table_vectors.py <arch root> <product root> <out dir> [--check]
"""
import ast
import copy
import hashlib
import json
import sys
from pathlib import Path

NATIVE = 'docs/coop/design-corrections/native'
TRIAL = 'docs/implementation/m1/trials/native-wire-owner-07/subject/tools/admission_ref.py'


def extract(path, names):
    """The named top-level assignments and functions of `path`, executed in their source order."""
    tree = ast.parse(path.read_text(encoding='utf-8'))
    keep = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            keep.append(node)
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if any(isinstance(t, ast.Name) and t.id in names for t in targets):
                keep.append(node)
    found = {n.name if isinstance(n, ast.FunctionDef) else (n.targets[0] if isinstance(n, ast.Assign) else n.target).id for n in keep}
    assert found == set(names), (path, set(names) - found)
    module = ast.Module(body=[ast.ImportFrom(module='__future__', names=[ast.alias('annotations')], level=0)] + keep, type_ignores=[])
    ns = {'json': json, 'copy': copy, 'Path': Path, 'HERE': path.parent, '__name__': path.stem}
    exec(compile(ast.fix_missing_locations(module), str(path), 'exec'), ns)
    return ns


def references(arch, product):
    p3 = extract(arch / NATIVE / 'native_evidence_model.v2.py',
                 ['IDENTITY_TOKENS', 'PROTOCOL3_TRANSITIONS', 'PROTOCOL3_PHASES', 'PROTOCOL3_RULES', '_PRE_COMPLETE', '_PROCESS_FAULTS',
                  '_SOURCE_FRAMES', 'protocol3_run'])
    ts = extract(arch / NATIVE / 'provider_startup_model.v1.py',
                 ['IDENTITY_TOKENS', 'TS_ORDER', '_TS_PRE_TERMINAL', '_TS_PROCESS_FAULTS', '_TS_OBSERVATIONS', '_TS_SOURCE_FRAMES',
                  'typescript_protocol2_run'])
    ov = extract(arch / TRIAL, ['overlay_run'])
    carriers = json.loads((product / 'schemas/wire/native-carriers-v1.json').read_text(encoding='utf-8'))
    return p3, ts, ov, carriers


def alphabet(table, protocol, tokens):
    frames = sorted({r['frame'] for r in table['rules'] if not r['frame'].startswith('*')})
    events = []
    for f in frames + sorted(table['wildcards']['*PROCESS_FAULT']['frames']) + ['Unknown']:
        if f == 'HelloAck':
            events += [{'frame': f, 'capabilities': list(tokens)}, {'frame': f, 'capabilities': ['sealed-vfs-v1']}]
        elif f == 'OpenUniverse' and protocol == 'rust3':
            events += [{'frame': f, 'dependencyMode': d, 'preparedMode': p} for d in (True, False) for p in (False, True)]
        elif f == 'Unavailable' and protocol == 'ts2':
            events += [{'frame': f, 'unavailablePayload': u} for u in ('pre-analyze', 'post-analyze')]
        else:
            events.append({'frame': f})
    return events


def hidden(path):
    """An exploration key's hidden part, for deduplication only (never an expected value): the last HelloAck's token
    set, the last OpenUniverse's modes, and the output and coverage seen since the last Analyze."""
    caps, modes, output, coverage = None, None, False, 0
    for e in path:
        if e['frame'] == 'HelloAck':
            caps = tuple(e.get('capabilities', []))
        elif e['frame'] == 'OpenUniverse':
            modes = (e.get('dependencyMode'), e.get('preparedMode'))
        elif e['frame'] == 'Analyze':
            output, coverage = False, 0
        elif e['frame'] in ('FactBatch', 'Coverage', 'CoverageV3'):
            output = True
            coverage += e['frame'] != 'FactBatch'
    return [caps, modes, output, coverage]


def explore(run, events, stage_count, limit=40):
    """Shortest event sequences to each distinct reachable state, by breadth-first search."""
    seen, frontier, paths = set(), [[]], []
    while frontier:
        nxt = []
        for path in frontier:
            out = run(path, stage_count)
            key = json.dumps([out['finalPhase'], out['terminalKind'], out['trace'][-1:], hidden(path)], sort_keys=True)
            if key in seen:
                continue
            seen.add(key)
            # FAULT is absorbing: one canonical FAULT path probes absorption, below.
            if out['finalPhase'] == 'FAULT':
                continue
            paths.append(path)
            if len(path) < limit and out['finalPhase'] != 'DONE':
                nxt += [path + [e] for e in events]
        frontier = nxt
    return paths


def compact(event):
    return {k: v for k, v in event.items()}


def scripted(tokens, protocol):
    """Trial 07's scripted transition traces (`tools/check_reference.py` `transitions`), as its inputs state them."""
    f = lambda *names: [{'frame': x} for x in names]
    if protocol == 'ts2':
        tbase = f('Hello') + [{'frame': 'HelloAck', 'capabilities': list(tokens)}] + f(
            'OpenUniverse', 'UniverseAccepted', 'SnapshotManifest', 'SnapshotSeal', 'SnapshotAccepted', 'NativeContextVerified', 'Analyze')
        post = {'frame': 'Unavailable', 'unavailablePayload': 'post-analyze'}
        return {'ts2-after': (tbase + f('FactBatch') + [post], 1), 'ts2-before': (tbase + [post], 1), 'ts2-cancel-start': (f('Cancel'), 1)}
    caps = {'frame': 'HelloAck', 'capabilities': list(tokens)}
    head = f('Hello') + [caps, {'frame': 'OpenUniverse', 'dependencyMode': True, 'preparedMode': False}] + f(
        'UniverseAccepted', 'SnapshotManifest', 'SnapshotFileChunk', 'SnapshotSeal', 'SnapshotAccepted',
        'DependencySourceManifest', 'DependencySourceChunk', 'DependencySourceSeal', 'DependencySourceAccepted')
    prepared_head = f('Hello') + [caps, {'frame': 'OpenUniverse', 'dependencyMode': True, 'preparedMode': True}] + f(
        'UniverseAccepted', 'SnapshotManifest', 'SnapshotSeal', 'SnapshotAccepted', 'DependencySourceManifest', 'DependencySourceSeal',
        'DependencySourceAccepted', 'PreparedOutputManifest', 'PreparedOutputChunk', 'PreparedOutputSeal', 'PreparedOutputAccepted')
    base = head + f('NativeContextVerified', 'Analyze')
    tail = f('zero-exit', 'eof')
    return {'complete': (base + f('FactBatch', 'CoverageV3', 'Complete') + tail, 1),
            'two-stage': (base + f('FactBatch', 'CoverageV3', 'CoverageV3', 'Complete') + tail, 2),
            'prepared': (prepared_head + f('NativeContextVerified', 'Analyze', 'CoverageV3', 'Complete') + tail, 1),
            'unavailable-before-output': (base + f('Unavailable') + tail, 1),
            'unavailable-after-output': (base + f('FactBatch', 'Unavailable'), 1),
            'pre-analyze-unavailable': (head + f('Unavailable') + tail, 1),
            'budget': (base + f('FactBatch', 'BudgetExhausted') + tail, 1),
            'fault': (head[:4] + f('ProviderFault') + tail, 1),
            'cancel': (head[:6] + f('Cancel', 'Cancelled') + tail, 1),
            'cancel-start': (f('Cancel'), 1),
            'no-identity': (f('Hello', 'HelloAck', 'OpenUniverse'), 1),
            'post-terminal': (base + f('Unavailable', 'FactBatch'), 1)}


def build(arch, product):
    p3, ts, ov, carriers = references(arch, product)
    tokens = p3['IDENTITY_TOKENS']
    assert list(tokens) == list(ts['IDENTITY_TOKENS'])
    p3table = p3['PROTOCOL3_TRANSITIONS']
    rust = lambda ev, n: ov['overlay_run'](carriers, p3table, tokens, ev, n)
    base = lambda ev, n: p3['protocol3_run'](ev, stage_count=n)
    tsrun = lambda ev, n: ts['typescript_protocol2_run'](ev, stage_count=n)
    out = {}
    for protocol, run, table in (('rust3', rust, p3table), ('ts2', tsrun, ts['TS_ORDER'])):
        events = alphabet(table, protocol, tokens)
        traces, keys = [], set()
        for n in (1, 2):
            for path in explore(run, events, n):
                # Every event from every live (or DONE) state, then one event after a fallback FAULT (absorption).
                for ev in [path] + [path + [e] for e in events] + [path + [{'frame': 'Unknown'}, {'frame': 'Hello'}]]:
                    k = json.dumps([n, ev], sort_keys=True)
                    if k in keys:
                        continue
                    keys.add(k)
                    traces.append(('explored', n, ev))
        out[protocol] = (run, traces, tokens)
    # native-cases.v2's protocol3_run cases (base table) and trial 07's scripted traces.
    corpus = json.loads((arch / NATIVE / 'native-cases.v2.json').read_text(encoding='utf-8'))
    cases, fixtures = corpus['cases'], corpus['fixtures']

    def resolve(v):
        if isinstance(v, str) and v.startswith('$fixtures.'):
            return fixtures[v[len('$fixtures.'):]]
        if isinstance(v, list):
            return [resolve(x) for x in v]
        if isinstance(v, dict):
            return {k: resolve(x) for k, x in v.items()}
        return v
    native = []
    for c in cases:
        for st in c['steps']:
            if st['fn'] == 'protocol3_run':
                args = resolve(st['args'])
                # The case's own expectations hold for the base runner.
                got = p3['protocol3_run'](args['events'], stage_count=args.get('stage_count', 1))
                checked = 0
                for k, v in c['expect'].items():
                    if k.startswith('$' + st['bind'] + '.') and k.count('.') == 1:
                        assert got[k.split('.', 1)[1]] == v, (c['id'], k, got)
                        checked += 1
                assert checked, c['id']
                # The base runner reads an absent OpenUniverse mode as false; it is made explicit, so the overlay
                # runner (whose dependencyMode default is true) is run on the same event.
                events = [dict(e, dependencyMode=bool(e.get('dependencyMode', False)), preparedMode=bool(e.get('preparedMode', False)))
                          if e['frame'] == 'OpenUniverse' else e for e in args['events']]
                native.append((c['id'], args.get('stage_count', 1), events))
    assert len(native) == 6, len(native)
    # A prefix tree per (protocol, stage count): node i is its parent's events plus one, with the step's trace entry
    # and the state after it, as the reference reports them for the whole sequence.
    def token(e):
        f = e['frame']
        if f == 'HelloAck':
            return f + ('+' if set(tokens) <= set(e.get('capabilities', [])) else '-')
        if 'dependencyMode' in e:
            return f + ':' + 'TF'[not e['dependencyMode']] + 'TF'[not e['preparedMode']]
        if 'unavailablePayload' in e:
            return f + ':' + e['unavailablePayload'].split('-')[0]
        return f
    files = {}
    pins = {'reference': {p: hashlib.sha256((arch / p).read_bytes()).hexdigest() for p in
                          (NATIVE + '/native_evidence_model.v2.py', NATIVE + '/provider_startup_model.v1.py', TRIAL, NATIVE + '/native-cases.v2.json')},
            'identityTokens': list(tokens), 'tokens': {'HelloAck+': 'every identity token', 'HelloAck-': ['sealed-vfs-v1'],
                                                       'OpenUniverse:XY': 'dependencyMode X, preparedMode Y', 'Unavailable:pre|post': 'unavailablePayload'}}
    for protocol, (run, traces, _) in out.items():
        nodes, index = [], {}
        def node(n, ev):
            key = json.dumps([n, [token(e) for e in ev]])
            if key in index:
                return index[key]
            parent = node(n, ev[:-1]) if ev else -1
            r = run(ev, n)
            row = {'n': n, 'p': parent}
            if ev:
                row['e'] = token(ev[-1])
                row['t'] = r['trace'][-1]
            row['phase'] = r['finalPhase']
            row['terminal'] = r['terminalKind']
            if protocol == 'ts2':
                row.update(source=r['sourceBytesSent'], stages=r['stagesCompleted'], identity=r['identityNegotiated'], cancel=r['cancelPhase'])
            else:
                b = base(ev, n)
                row.update(source=b['sourceBytesSent'], stages=b['stagesCompleted'], identity=b['identityNegotiated'])
                if (b['finalPhase'], b['terminalKind'], b['trace']) != (r['finalPhase'], r['terminalKind'], r['trace']):
                    row['baseDiffers'] = {'phase': b['finalPhase'], 'trace': b['trace'][-1:]}
            index[key] = len(nodes)
            nodes.append(row)
            return index[key]
        for _, n, ev in traces:
            node(n, ev)
        for name, (ev, n) in scripted(tokens, protocol).items():
            node(n, ev)
        named = []
        if protocol == 'rust3':
            for cid, n, ev in native:
                b = base(ev, n)
                named.append({'id': cid, 'n': n, 'events': [token(e) for e in ev], 'phase': b['finalPhase'], 'terminal': b['terminalKind'],
                              'trace': b['trace'], 'source': b['sourceBytesSent'], 'identity': b['identityNegotiated'],
                              'overlayTrace': run(ev, n)['trace']})
        body = ',\n'.join(json.dumps(r, sort_keys=True, separators=(',', ':')) for r in nodes)
        head = json.dumps(dict(pins, artifact='opensip.d2b.table-vectors', protocol=protocol, version=1, nativeCases=named, nodes=[]),
                          sort_keys=True, separators=(',', ':'))
        files['table-vectors.%s.v1.json' % protocol] = (head.replace('"nodes":[]', '"nodes":[\n' + body + '\n]') + '\n').encode()
    return files


def main(argv):
    arch, product, out = Path(argv[1]), Path(argv[2]), Path(argv[3])
    files = build(arch, product)
    stale = []
    for name, data in files.items():
        if '--check' in argv[4:]:
            if (out / name).read_bytes() != data:
                stale.append(name)
        else:
            (out / name).write_bytes(data)
            print(name, len(data), hashlib.sha256(data).hexdigest(), data.count(b'\n') - 2, 'nodes')
    if '--check' in argv[4:]:
        print('stale' if stale else 'current', stale)
        return 1 if stale else 0
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
