#!/usr/bin/env python3
"""The derivation's vectors (r3): each per-schema term over sample and stress records, the admission
composition of the two whole calls, the invocation-multiplicity check, the malformed records (r2),
the depth-gate records (NBO-1, F10), the retained-length gate (F11) and the census mutation
self-tests. Writes ../evidence/VECTORS-r4.json (the records themselves and every price), which the
Rust price's formula control (F5) must reproduce exactly."""
import sys, os, json, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.argv = sys.argv[:2]
from admission_model import *  # noqa: F401,F403

HERE = os.path.dirname(os.path.abspath(__file__))
H = lambda c: c * 64


def blob_rows(paths):
    rows = [{'bytes': 1000 + i, 'path': p, 'sha256': H('0123456789abcdef'[i % 16])} for i, p in enumerate(paths)]
    return sorted(rows, key=lambda r: r['path'].encode())


def closure(kind, paths, version='5.6.2'):
    return {'kind': kind, 'manifestDigest': H('a'), 'platform': 'macos-arm64', 'protocolMajor': 1,
            'schemaVersion': 2, 'semanticVersion': version, 'tree': blob_rows(paths)}


LIBS = ['dom', 'es2015', 'es2016', 'es2017', 'es2018', 'es2019', 'es2020', 'es2021', 'es2022', 'es5', 'esnext']
STDLIB_PATHS = [f'lib/lib.{n}.d.ts' for n in LIBS] + [f'lib/lib.es2022.part{i}.d.ts' for i in range(80)]
TOOL_PATHS = ['bin/node', 'package/package.json', 'package/lib/tsc.js', 'package/lib/typescript.js'] + \
             [f'package/lib/{n}/diagnosticMessages.generated.json' for n in ('cs', 'de', 'es', 'fr', 'it', 'ja', 'ko')] + \
             [f'package/lib/file{i:04d}.js' for i in range(150)]
ESCAPED = lambda i: f'd\u0001"q{i:04d}/é中\U0001F600\t\u001f'


def context(stdlib, tool, layout=None, lock=True):
    comps = sorted(({'component': r['path'].rsplit('/', 1)[1], 'sha256': r['sha256']} for r in stdlib['tree']
                    if r['path'].endswith('.d.ts')), key=lambda c: c['component'].encode())
    return {
        'schemaVersion': 2, 'languageMode': 'ts-tsconfig', 'moduleResolutionMode': 'bundler', 'packageModuleType': 'module',
        'toolchain': {'compilerName': 'typescript', 'compilerVersion': '5.6.2', 'compilerPackageDigest': H('1'),
                      'typescriptStdlibMerkleRoot': H('2'), 'standardLibraryComponentDigests': comps,
                      'libSelection': sorted(['dom', 'ES2022', 'esnext'], key=str.encode)},
        'toolClosure': {'closureId': 'closure2:' + H('3'), 'compiler': H('4'), 'runtime': H('5')},
        'configProjection': {
            'schemaVersion': 2, 'ancestorCarrierVerified': True, 'environmentSanitized': True,
            'typeAcquisitionEnabled': False, 'executableSelected': False,
            'configGraphPaths': ['packages/app/tsconfig.json', 'tsconfig.base.json'],
            'strippedOptions': [{'option': 'outDir', 'reason': 'emits-output'}],
            'honoredOptions': {'allowJs': False, 'checkJs': False, 'module': 'esnext', 'moduleResolution': 'bundler',
                               'target': 'es2022', 'strict': True, 'skipLibCheck': True, 'noEmit': True,
                               'types': ['node'], 'lib': ['ES2022', 'dom', 'esnext'], 'baseUrl': None,
                               'paths': [{'pattern': '@app/*', 'substitutions': ['packages/app/src/*']}],
                               'rootDirs': [], 'resolveJsonModule': True, 'allowSyntheticDefaultImports': True,
                               'esModuleInterop': True, 'customConditions': [], 'jsx': None}},
        'nodeModulesLayoutDigest': H('6') if layout else None,
        'lockfileIdentity': {'kind': 'pnpm-lock', 'path': 'pnpm-lock.yaml', 'contentSha256': H('7')} if lock else None,
    }


def graph(n=2):
    nodes = [{'path': 'packages/app/tsconfig.json', 'contentSha256': H('8'), 'kind': 'tsconfig',
              'extendsResolved': ['tsconfig.base.json']},
             {'path': 'tsconfig.base.json', 'contentSha256': H('9'), 'kind': 'tsconfig', 'extendsResolved': []}]
    nodes += [{'path': f'packages/p{i:04d}/tsconfig.json', 'contentSha256': H('9'), 'kind': 'tsconfig',
               'extendsResolved': ['tsconfig.base.json']} for i in range(n - 2)]
    return {'schemaVersion': 1, 'entryConfigPath': 'packages/app/tsconfig.json',
            'nodes': sorted(nodes, key=lambda x: x['path'].encode())}


def universe(roots=50):
    return {'schemaVersion': 2, 'languageMode': 'ts-tsconfig', 'configOrigin': 'tsconfig', 'synthesizerVersion': None,
            'synthesizedOptions': None, 'packageModuleType': 'module', 'allowJs': False, 'checkJs': False,
            'jsAdmittedToProgram': False, 'jsDiagnosticsEnabled': False, 'resolutionCompletenessImplied': False,
            'jsRootFiles': [], 'programRootFiles': [f'packages/app/src/m{i:05d}.ts' for i in range(roots)],
            'lockfileKind': 'pnpm-lock', 'nodeModulesInReadSet': True, 'executionCapableResolution': False,
            'tsconfigGraphHash': H('b'), 'nativeContextId': 'sha256:' + H('c')}


def layout(n):
    rows = [{'contentSha256': H('d'), 'installPath': f'node_modules/p{i:05d}', 'packageName': f'p{i:05d}',
             'packageVersion': '1.0.0', 'realPath': f'node_modules/.pnpm/p{i:05d}@1.0.0/node_modules/p{i:05d}'}
            for i in range(n)]
    return {'schemaVersion': 1, 'entries': sorted(rows, key=lambda r: r['installPath'].encode())}


def snapshot(paths):
    return {'projectId': 'prj1-' + H('e'), 'resolvedConfigDigest': H('f'), 'schemaVersion': 1, 'scopeDigest': H('0'),
            'vcsDigest': H('1'), 'sourceInventory': sorted(({'bytes': 10, 'path': p, 'sha256': H('2')} for p in paths),
                                                          key=lambda r: r['path'].encode())}



MU = {sel: tau_size(doc, sel)[0] for doc, sel in ENTRIES}
CTX, UNI = '/$defs/TypeScriptNativeContextV2', '/$defs/TypeScriptUniverseV2ResolvedInputs'
GRAPH, LAYOUT = '/$defs/TypeScriptConfigGraphV1', '/$defs/ResolvedNodeModulesLayoutV1'
CTX_DOMAIN, UNI_DOMAIN = 'native.context.typescript.v2', 'native.semantic-universe.typescript.v2'
PFX = lambda domain: f'frame:{domain}:'.encode()


def rec(x, doc, sel, identity=False, clone=False, store=None, key=None):
    r = Record(x, doc, sel, identity, clone, store=store, key=key)
    assert r.census.invocations <= MU[sel] * r.st.N, (sel, r.census.invocations, MU[sel], r.st.N)
    return r


def store_for(records, blobs, overrides=None):
    """C2b-1a's retained map for a scenario: each frame under its frame digest at its frame length,
    each record under its record digest at its canonical length, filled to `blobs` entries. Built
    outside the boundary. `overrides` (F11) replaces a retained length."""
    overrides = overrides or {}
    entries, keys = [], {}
    def put(x, prefix, length, name):
        keys[name] = digest_key(x, prefix)                        # built here, outside the boundary
        entries.append((keys[name], overrides.get(name, length)))
    ctx_L = Record(records['context'], NATIVE, CTX).st.L
    put(records['context'], PFX(CTX_DOMAIN), FRAME_PREFIX + len(CTX_DOMAIN) + 1 + 8 + ctx_L, 'context')
    uni_L = Record(records['universe'], NATIVE, UNI).st.L
    put(records['universe'], PFX(UNI_DOMAIN), FRAME_PREFIX + len(UNI_DOMAIN) + 1 + 8 + uni_L, 'universe')
    put(records['graph'], b'', Record(records['graph'], NATIVE, GRAPH).st.L, 'graph')
    if records['layout']:
        put(records['layout'], b'', Record(records['layout'], NATIVE, LAYOUT).st.L, 'layout')
    i = 0
    while len(entries) < blobs:
        entries.append((hashlib.sha256(b'filler:%d' % i).digest(), 1000 + i)); i += 1
    return Store(entries), keys


def row(name, price, r):
    return {'term': name, 'nodes': r.st.N, 'canonicalLength': r.st.L, 'invocations': r.census.invocations,
            'multiplicityBound': MU[r.selector] * r.st.N, 'censusCounted': list(r.census.counted),
            'censusCharged': list(r.census.charged), 'censusElements': r.census.elements,
            'censusScans': r.census.scans_started, 'censusComparisons': r.census.comparisons,
            'storeComparisons': r.census.store_comparisons, 'retainedLength': r.beta,
            'allocations': list(price.alloc), 'passes': list(price.passes), 'price': list(price.total())}


def terms(records, objects=3, blobs=400):
    out = {'rows': []}
    store, keys = store_for(records, blobs)
    tool = rec(records['tool'], IDENTITY, '/$defs/closure', identity=True, clone=True)
    std = rec(records['stdlib'], IDENTITY, '/$defs/closure', identity=True, clone=True)
    tc = T_CLOSURE('closure2:' + H('3'), tool, objects)
    sc = T_CLOSURE('closure2:' + H('2'), std, objects)
    out['rows'] += [row(f'T-CLOSURE[toolchain, {len(records["tool"]["tree"])} rows]', tc, tool),
                    row(f'T-CLOSURE[stdlib, {len(records["stdlib"]["tree"])} rows]', sc, std)]
    ctx = rec(records['context'], NATIVE, CTX, store=store, key=keys['context'])
    fc = T_FRAME(CTX_DOMAIN, 'native-context', ctx, blobs)
    uni = rec(records['universe'], NATIVE, UNI, store=store, key=keys['universe'])
    fu = T_FRAME(UNI_DOMAIN, 'native-semantic-universe', uni, blobs)
    gr = rec(records['graph'], NATIVE, GRAPH, store=store, key=keys['graph'])
    rg, wg = T_RECORD('#' + GRAPH, gr, blobs), W_REC(gr, blobs)
    out['rows'] += [row('T-FRAME-CTX', fc, ctx), row('T-FRAME-UNI', fu, uni), row('T-REC-GRAPH', rg, gr)]
    if records['layout']:
        la = rec(records['layout'], NATIVE, LAYOUT, store=store, key=keys['layout'])
        rl, wl = T_RECORD('#' + LAYOUT, la, blobs), W_REC(la, blobs)
        out['rows'].append(row('T-REC-LAYOUT', rl, la))
    else:
        rl = wl = PZ
    snap = rec(records['snapshot'], IDENTITY, '/$defs/snapshot', identity=True)
    gs = OBJECT_WRAPPER('snapshot2:' + H('9'), 'snapshot', snap.st, objects) + FROM_JSON('snapshot', snap)
    out['rows'].append(row('T-SNAPSHOT (generic, reference only)', gs, snap))
    out['snapshotWrapper'] = list(OBJECT_WRAPPER('snapshot2:' + H('9'), 'snapshot', snap.st, objects).total())
    clone = CLONE(tool) + CLONE(std)
    mint = 2 * fc + 2 * (tc + sc) + clone + rl + wl
    bind = 2 * fu + 2 * (rg + wg) + 4 * fc + 3 * (tc + sc) + 2 * clone + 2 * (rl + wl)
    out['mintAdmissionsExcludingSnapshot'] = {'allocations': list(mint.alloc), 'passes': list(mint.passes), 'total': list(mint.total())}
    out['bindAdmissionsExcludingSnapshot'] = {'allocations': list(bind.alloc), 'passes': list(bind.passes), 'total': list(bind.total())}
    census_sum = sum((C(*x['censusCharged']) for x in out['rows'] if not x['term'].startswith('T-SNAPSHOT')), Z)
    out['censusChargedSum'] = list(census_sum)
    return out


def scenario(name, tool_paths, stdlib_paths, layout_rows, graph_nodes=2, roots=50, verdict='admit'):
    tool, stdlib = closure('toolchain', tool_paths), closure('stdlib', stdlib_paths)
    lay = layout(layout_rows) if layout_rows is not None else None
    r = {'tool': tool, 'stdlib': stdlib, 'context': context(stdlib, tool, lay), 'universe': universe(roots),
         'graph': graph(graph_nodes), 'layout': lay,
         'snapshot': snapshot([f'packages/app/src/m{i:05d}.ts' for i in range(roots)] +
                              ['packages/app/tsconfig.json', 'tsconfig.base.json', 'pnpm-lock.yaml'])}
    return name, r, verdict


LONG = lambda i: '/'.join([f'{i:03d}' + 'x' * 252] + ['x' * 255] * 14 + ['y' * 254, 'z'])   # 4,096 scalars, distinct
DUP_LONG = lambda i: '/'.join([chr(97 + i % 26) + 'x' * 254] * 15 + ['y' * 254, 'z'])     # r1's: 26 distinct of 200

SCENARIOS = [
    scenario('typical', TOOL_PATHS, STDLIB_PATHS, 120),
    scenario('no-layout', TOOL_PATHS, STDLIB_PATHS, None),
    scenario('closure-long-paths', [LONG(i) for i in range(200)], STDLIB_PATHS, 10),
    scenario('closure-escaped-paths', [ESCAPED(i) for i in range(300)], STDLIB_PATHS, 10),
    scenario('closure-2000-rows', [f'package/f{i:05d}.js' for i in range(2000)], STDLIB_PATHS, 10),
    scenario('large-universe', TOOL_PATHS, STDLIB_PATHS, 5000, graph_nodes=500, roots=20000),
]


def malformed():
    """REVIEW-r1 RF-2: ordinary malformed values. Each is priced (the census is total) and each
    has the evaluator verdict F8 must assert; the verdict is by construction from the cited lines,
    not executed here."""
    base = closure('toolchain', TOOL_PATHS[:20])
    cases = []
    def m(name, x, sel, verdict):
        cases.append((name, x, sel, verdict))
    c = json.loads(json.dumps(base)); c['tree'] = [None]
    m('closure tree [null]', c, '/$defs/closure', 'refuse: Candidate(Schema(Mismatch)) — items type (schema.rs:544-553, :613-620)')
    c = json.loads(json.dumps(base)); c['tree'][0]['path'] = 7
    m('closure row path = 7', c, '/$defs/closure', 'refuse: Candidate(Schema(Mismatch)) — Blob path type (schema.rs:544-553)')
    c = json.loads(json.dumps(base)); c['tree'] = [{'bytes': 1, 'path': 'a', 'sha256': H('0')}] * 2
    m('closure duplicate rows', c, '/$defs/closure', 'refuse: Candidate(Schema(Mismatch)) — uniqueItems (schema.rs:634-644)')
    c = json.loads(json.dumps(base)); c['tree'] = [{'bytes': 1, 'path': DUP_LONG(i), 'sha256': H('0123456789abcdef'[i % 16])} for i in range(200)]
    c['tree'].sort(key=lambda r: r['path'].encode())
    m('closure 200 long paths, 26 distinct (r1 vector)', c, '/$defs/closure', 'refuse: Candidate(Schema(Mismatch)) — x-opensip-order NonIncreasing (descriptors.rs:301-308)')
    c = json.loads(json.dumps(base)); c['extra'] = {'deep': [[{'k': 'v'}]]}
    m('closure extra key', c, '/$defs/closure', 'refuse: Candidate(Schema(Mismatch)) — additionalProperties false (schema.rs:701-704)')
    m('closure is an array', [base], '/$defs/closure', 'refuse: Candidate(Schema(Mismatch)) — type object (schema.rs:544-553)')
    g = graph(4); del g['nodes'][1]['path']
    m('graph node without path', g, GRAPH, 'refuse: Schema(Mismatch) — required (schema.rs:664-669)')
    g = graph(4); g['nodes'][0]['kind'] = 'unknown'
    m('graph node kind outside enum', g, GRAPH, 'refuse: Schema(Mismatch) — enum (schema.rs:530-543)')
    l = layout(20); l['entries'][3]['installPath'] = None
    m('layout installPath null', l, LAYOUT, 'refuse: Schema(Mismatch) — CanonicalPath type (schema.rs:544-553)')
    u = universe(10); u['programRootFiles'] = ['../escape.ts']
    m('universe root with dot segment', u, UNI, 'refuse: Schema(Mismatch) — CanonicalPath pattern (schema_patterns.rs:497-503)')
    tool, std = closure('toolchain', TOOL_PATHS), closure('stdlib', STDLIB_PATHS)
    x = context(std, tool); x['toolchain']['libSelection'] = 5
    m('context libSelection not an array', x, CTX, 'refuse: Schema(Mismatch) — type array (schema.rs:544-553)')
    return cases


def nest(inner, containers):
    """`inner` wrapped in `containers` arrays (NBO-1 / F10)."""
    x = inner
    for _ in range(containers):
        x = [x]
    return x


def depth_gate():
    """The depth gate is the encoder's (canonical.rs:536): a container at container depth 32
    refuses. 32 nested containers are accepted (the innermost at depth 31); 33 refuse, whatever
    the innermost container holds; a scalar inside the 32nd container is accepted."""
    cases = [('32 nested arrays, innermost []', nest([], 31), 'price'),
             ('33 nested arrays, innermost []', nest([], 32), 'PriceUnavailable'),
             ('32 nested arrays, innermost {}', nest({}, 31), 'price'),
             ('33 nested arrays, innermost {}', nest({}, 32), 'PriceUnavailable'),
             ('32 nested arrays around a scalar', nest(1, 32), 'price'),
             ('33 nested arrays around a scalar', nest(1, 33), 'PriceUnavailable')]
    out = []
    for name, x, expected in cases:
        try:
            r = Record(x, IDENTITY, '/$defs/closure', identity=True)
            got = 'price'; detail = {'nodes': r.st.N, 'censusCounted': list(r.census.counted), 'censusCharged': list(r.census.charged)}
        except PriceUnavailable as e:
            got = 'PriceUnavailable'; detail = {'reason': str(e)}
        assert got == expected, (name, got, expected)
        out.append({'name': name, 'expected': expected, 'result': got, **detail})
    return out


def beta_gate():
    """F11: a retained length that is not the value's own encoding length refuses PriceUnavailable
    before any term work; the census (with its funded lookup) still holds counted <= charged. A
    digest absent from the store is priced at the full term: the fetch refuses `MissingBlob` after
    its search (closure.rs:85-96), which the term's BLOB covers."""
    _, records, _ = SCENARIOS[0]
    out = []
    uni_L = Record(records['universe'], NATIVE, UNI).st.L
    for name, override, build, expected in [
        ('graph record retained at 1 MiB', {'graph': 1 << 20},
         lambda s, k: T_RECORD('#' + GRAPH, rec(records['graph'], NATIVE, GRAPH, store=s, key=k['graph']), 400), 'PriceUnavailable'),
        ('universe frame retained one byte short', {'universe': FRAME_PREFIX + len(UNI_DOMAIN) + 1 + 8 + uni_L - 1},
         lambda s, k: T_FRAME(UNI_DOMAIN, 'native-semantic-universe', rec(records['universe'], NATIVE, UNI, store=s, key=k['universe']), 400), 'PriceUnavailable'),
        ('graph record absent from the store', {'graph': None},
         lambda s, k: T_RECORD('#' + GRAPH, rec(records['graph'], NATIVE, GRAPH, store=s, key=k['graph']), 400), 'price'),
    ]:
        entries, keys = store_for(records, 400, override)
        if override.get('graph', 0) is None:
            entries = Store([e for e in entries.entries if e[0] != keys['graph']])
        try:
            price = build(entries, keys); got = 'price'; detail = {'price': list(price.total()), 'note': 'the full term; the fetch refuses MissingBlob after its search'}
        except PriceUnavailable as e:
            got = 'PriceUnavailable'; detail = {'reason': str(e)}
        assert got == expected, (name, got, expected)
        out.append({'name': name, 'expected': expected, 'result': got, **detail})
    return out


def lookup_controls():
    """REVIEW-r3 RF-1: the declared-key search is one three-way comparison per iteration. For the
    context root slot (K = 9) and its `honoredOptions` slot (K = 18), keys below the first, equal
    to the first, equal to the last, above the last and undeclared in the middle are looked up
    with every static key wrapped in an observer that counts relational operations. Required:
    observed relational operations = 0 (every comparison is the counted byte read), counted
    comparisons <= bitlen(K), counted bytes <= the member charge's lookup allowance
    2(bitlen(K) + 1)(|k| + 1). The same for the store (|blobs| = 400)."""
    root = root_slot(NATIVE, CTX)
    hon = root.children[root.keys.index('configProjection')]
    hon = hon.children[hon.keys.index('honoredOptions')]
    out = []
    for slot_name, slot in (('context root', root), ('honoredOptions', hon)):
        K = len(slot.keys)
        probes = [('below the first key', b'!'), ('the first key', slot.key_bytes[0]), ('the last key', slot.key_bytes[-1]),
                  ('above the last key', b'~'), ('undeclared, in the middle', slot.key_bytes[K // 2] + b'0')]
        for name, kb in probes:
            j, comps, byts, ops, bl = observe_keys(slot, kb)
            allowance = 2 * (bl + 1) * (len(kb) + 1)
            ok = ops == 0 and comps <= bl and byts <= allowance and (j is None) == (kb not in slot.key_bytes)
            out.append({'slot': slot_name, 'K': K, 'key': kb.decode(), 'index': j, 'comparisons': comps, 'bitlenK': bl,
                        'bytes': byts, 'allowance': allowance, 'observedRelationalOps': ops, 'ok': ok})
            assert ok, out[-1]
    # the store
    _, records, _ = SCENARIOS[0]
    store, keys = store_for(records, 400)
    for name, key in (('a present digest', keys['graph']), ('below every digest', b'\x00' * 32), ('above every digest', b'\xff' * 32)):
        c = Census(); c.charge(C(0, 10 ** 9, 10 ** 12), ('observe',))
        beta = store.lookup(key, c); c.close()
        bl = bitlen(len(store.entries)); k = map_search(len(store.entries))
        ok = c.store_comparisons <= bl and c.counted[2] <= 2 * k * 33
        out.append({'slot': 'store', 'K': len(store.entries), 'key': name, 'found': beta is not None, 'comparisons': c.store_comparisons,
                    'bitlenK': bl, 'bytes': c.counted[2], 'allowance': 2 * k * 33, 'ok': ok})
        assert ok, out[-1]
    # r3's defect under the observer: two relational operations per iteration, one counted
    j, comps, byts, ops, bl = observe_keys(root, b'!', mutation='two-sided')
    out.append({'slot': 'context root', 'K': len(root.keys), 'key': '! (two-sided mutation)', 'index': j, 'comparisons': comps,
                'bitlenK': bl, 'bytes': byts, 'allowance': 2 * (bl + 1) * 2, 'observedRelationalOps': ops, 'ok': ops > comps,
                'result': 'caught: observed relational operations exceed the counted comparisons' if ops > comps else 'NOT CAUGHT'})
    assert ops > comps
    return out


def mutation_selftests():
    """The census controls' mutations. Each must be caught: `unique-extra` adds an unpriced extra
    traversal per UNIQUE item (counted > charged, per element); `linear-lookup` replaces the
    declared-key binary search with a linear scan (its counted comparisons exceed the member's
    charge); `scan-first` scans a string before its charge (caught by the exhaustion control,
    scripts/exhaustion.py, which this reports too)."""
    out = {}
    tool = closure('toolchain', TOOL_PATHS)
    try:
        Record(tool, IDENTITY, '/$defs/closure', identity=True, unique_steps=4)
        out['unique-extra'] = 'NOT CAUGHT'
    except AssertionError as e:
        out['unique-extra'] = f'caught: {e}'
    _, records, _ = SCENARIOS[0]
    try:
        Record(records['context'], NATIVE, CTX, mutation='linear-lookup')
        out['linear-lookup'] = 'NOT CAUGHT'
    except AssertionError as e:
        out['linear-lookup'] = f'caught: {e}'
    import exhaustion
    out['scan-first'] = exhaustion.scan_first_mutation(records['context'], NATIVE, CTX)
    return out


if __name__ == '__main__':
    result = {'pin': PIN, 'revision': 4, 'multiplicity': MU, 'scenarios': [], 'malformed': []}
    for name, r, verdict in SCENARIOS:
        t = terms(r)
        result['scenarios'].append({'name': name, 'expectedVerdict': verdict, 'records': r, **t})
        print(f'== {name} (expected: {verdict})')
        for x in t['rows']:
            print(f"  {x['term']:42} N {x['nodes']:6} L {x['canonicalLength']:8} inv {x['invocations']:7}<={x['multiplicityBound']:7}"
                  f" census {tuple(x['censusCounted'])}<={tuple(x['censusCharged'])} elements {x['censusElements']} scans {x['censusScans']} beta {x['retainedLength']}")
            print(f"  {'':42} alloc {tuple(x['allocations'])} passes {tuple(x['passes'])} total {tuple(x['price'])}")
        print('  mint admissions (excl. snapshot)', tuple(t['mintAdmissionsExcludingSnapshot']['total']))
        print('  bind admissions (excl. snapshot)', tuple(t['bindAdmissionsExcludingSnapshot']['total']))
        print('  census charged, sum over the priced records (excl. snapshot)', tuple(t['censusChargedSum']))
    print('== malformed (priced; verdict by construction)')
    for name, x, sel, verdict in malformed():
        doc = IDENTITY if sel in ('/$defs/closure', '/$defs/snapshot') else NATIVE
        r = rec(x, doc, sel, identity=(doc == IDENTITY))
        if sel == '/$defs/closure':
            price = T_CLOSURE('closure2:' + H('3'), r, 3)
        elif sel in (CTX, UNI):
            dom = (CTX_DOMAIN, 'native-context') if sel == CTX else (UNI_DOMAIN, 'native-semantic-universe')
            price = T_FRAME(dom[0], dom[1], r, 400)
        else:
            price = T_RECORD('#' + sel, r, 400)
        result['malformed'].append({'name': name, 'selector': sel, 'expectedVerdict': verdict, 'record': x, **row(name, price, r)})
        print(f"  {name:48} inv {r.census.invocations:5} census {tuple(r.census.counted)}<={tuple(r.census.charged)} total {tuple(price.total())}")
    print('== depth gate (NBO-1, F10)')
    result['depthGate'] = depth_gate()
    for d in result['depthGate']:
        print(f"  {d['name']:40} {d['result']}" + (f"  nodes {d['nodes']} census {tuple(d['censusCounted'])}<={tuple(d['censusCharged'])}" if d['result'] == 'price' else ''))
    print('== lookup controls (REVIEW-r3 RF-1: one three-way comparison per iteration)')
    result['lookupControls'] = lookup_controls()
    for d in result['lookupControls']:
        print(f"  {d['slot']:14} K {d['K']:3} {d['key']:28} comparisons {d['comparisons']} <= bitlen {d['bitlenK']}  bytes {d['bytes']} <= {d['allowance'] if 'allowance' in d else '-'}"
              f"  observed ops {d.get('observedRelationalOps', '-')}  {d.get('result', 'OK' if d['ok'] else 'FAIL')}")
    print('== retained-length gate (F11)')
    result['betaGate'] = beta_gate()
    for d in result['betaGate']:
        print(f"  {d['name']:40} {d['result']}  {d.get('reason', d.get('note', ''))}")
    result['mutationSelfTests'] = mutation_selftests()
    print('== census mutations')
    for k, v in result['mutationSelfTests'].items():
        print(f'  {k:16} {v}')
    os.makedirs(os.path.join(HERE, '..', 'evidence'), exist_ok=True)
    with open(os.path.join(HERE, '..', 'evidence', 'VECTORS-r4.json'), 'w') as f:
        json.dump(result, f, indent=1, ensure_ascii=False)
