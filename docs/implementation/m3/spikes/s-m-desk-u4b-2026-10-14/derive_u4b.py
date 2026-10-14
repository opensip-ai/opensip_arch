from pathlib import Path
import json, hashlib, statistics
# S-M desk record U-4b ROUND 2 (Codex SM-U4B-R1-RF-01: Express SM-2 is the synthesized program only, D-4; the cohort's
# Express entry is informational, kept apart; every current entry is unique per language/row/component/reset/entry).
# (PLAN-r3 U-4, D-3, D-4, D-5, D-7): SM-10 per F/T component for all 14 item-9 rows under both resets, and
# SM-11's labelled SM-4/SM-10 by covered units for the eight medium Rust rows. Desk only: reads committed (or index-pinned)
# result records; runs nothing; fills no placeholder; computes no F, T or outcome.
# SM-10 (item 9): per-process wait4 ru_maxrss, information only, in the native unit labelled as recorded (macOS: bytes),
# with the checked conversion to bytes (identity for 'bytes'; asserted 0 <= v < 2**64). Per component and row: the
# median and maximum over the 7 measured runs of that run's process peak. SM-4 runs many compiler children: its per-run
# value is the largest single compiler child's peak (the executor parent's own peak is not recorded), with the child count.
# R8 (two Cargo entries, D-3): RSS is reported per entry child and as the larger of the two; peaks of sequential children
# are not summed (lead decision LD-U4B-R8-RSS).
W = Path(__file__).resolve().parent; A = Path('/Users/sb/code/opensip-ai/opensip_arch'); SP = A / 'docs/implementation/m3/spikes'
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest(); load = lambda p: json.loads(Path(p).read_text())
pins = {}
def src(p): p = Path(p); pins[str(p)] = sha(p); return load(p)
def byts(run, native='rssNative', unit='rssUnit'):
    v = run[native]; u = run.get(unit, 'bytes'); assert u == 'bytes' and isinstance(v, int) and 0 <= v < 2**64; return v
def stat(vals): return dict(medianBytes=statistics.median(vals), maxBytes=max(vals), runs=len(vals))
def measured(runs): m = [r for r in runs if not r['warmup']]; assert len(runs) == 10 and len(m) == 7; return m
TS = {'js-medium-express': 141, 'poly-medium-napi-rs': 193, 'ts-medium-powertools-lambda': 936, 'ts-medium-smithy-typescript': 1159, 'ts-medium-umami': 1381, 'ts-medium-vite': 678}
RS = {'poly-medium-napi-rs': 239, 'rs-medium-aws-lambda-rust-runtime': 192, 'rs-medium-axum': 301, 'rs-medium-hyper': 98, 'rs-medium-serde': 208, 'rs-medium-serde-json': 71, 'rs-medium-tokio': 808, 'mr-rs-medium-serde-json': 279}
C5A = SP / 's-m-cold-ts-2026-10-13'; U2C = SP / 's-m-u2c-rust-sealing-transfer-2026-10-14'
C5B = Path('/Users/sb/code/.opensip-implementation-cache/work-2026-10-14/u5b')  # U-5b working copy; every file read is pinned against the PUBLISHED U-5b subject or raw index (codex-sm-cold-rust-r1)
U1 = Path('/tmp/opensip-implementation/sm-command-data-bsabsent-2026-10-13/bsabsent-static-profile-series-r1.json')
u1idx = {m['member']: m for m in load(SP / 's-m-u1-build-script-outputs-absent-2026-10-13/large-records-index.json')['members']}; assert sha(U1) == u1idx['bsabsent-static-profile-series-r1.json']['sha256']
c5bsubj = load(SP / 's-m-cold-rust-2026-10-14-subject.json'); c5b_files = {f['path'].split('s-m-cold-rust-2026-10-14/', 1)[1]: f['sha256'] for f in c5bsubj['files'] if 's-m-cold-rust-2026-10-14/' in f['path']}
c5b_raw = {m['member']: m['sha256'] for m in load(A / c5bsubj['prefix'] / 'raw-evidence-index.json')['members']}
def c5b(rel):
    p = C5B / rel; h = sha(p); assert c5b_files.get(rel) == h or c5b_raw.get(rel) == h, rel; pins[f'U-5b:{rel}'] = h; return load(p)
rows = []; info = []
def add(lang, row, comp, reset, source, s, **kw): rows.append(dict(language=lang, row=row, component=comp, reset=reset, source=source, unit='bytes', conversion='bytes = native (macOS rss_unit bytes; checked)', **s, **kw))
# --- TS rows ---
for reset, sm1 in [('warm', src(SP / 's-m-sm1-ready-closure-2026-10-09/results.json')), ('cold', src(C5A / 'sm1/results.json'))]:
    s = stat([byts(r) for r in measured(sm1['runs'])])
    for row in TS: add('tsjs', row, 'SM-1', reset, 'sm1-ready-closure' if reset == 'warm' else 'U-5a sm1', s, note='one shared TS start figure')
for reset, coh, syn in [('warm', src(SP / 's-m-ts-cohort-2026-10-09/results.json'), src(SP / 's-m-ts-synthesized-2026-10-10/results.json')), ('cold', src(C5A / 'cohort/results.json'), src(C5A / 'synthesized/results.json'))]:
    for w in coh['workloads']:
        if w['id'] == 'js-medium-express': info.append(dict(language='tsjs', row='js-medium-express', component='cohort configuration run (NOT D-4 SM-2)', reset=reset, source='ts-cohort' if reset == 'warm' else 'U-5a cohort', unit='bytes', **stat([byts(r) for r in measured(w['runs'])]), note='D-4 selects the synthesized program for Express SM-2; this cohort entry is information only'))
        elif w['id'] in TS: add('tsjs', w['id'], 'SM-2', reset, 'ts-cohort' if reset == 'warm' else 'U-5a cohort', stat([byts(r) for r in measured(w['runs'])]))
    w = next(x for x in syn['workloads'] if x['id'] == 'js-medium-express'); add('tsjs', 'js-medium-express', 'SM-2', reset, 'ts-synthesized (D-4)' if reset == 'warm' else 'U-5a synthesized', stat([byts(r) for r in measured(w['runs'])]))
for comp, warmp, coldp in [('SM-5', SP / 's-m-sealing-typed-2026-10-09/results.json', C5A / 'sealing/results.json'), ('SM-7', SP / 's-m-transfer-2026-10-09/results.json', C5A / 'transfer/results.json')]:
    for reset, d in [('warm', src(warmp)), ('cold', src(coldp))]:
        for w in d['workloads']:
            if w['id'] in TS: add('tsjs', w['id'], comp, reset, ('sealing-typed' if comp == 'SM-5' else 'transfer') if reset == 'warm' else f"U-5a {'sealing' if comp == 'SM-5' else 'transfer'}", stat([byts(r) for r in measured(w['runs'])]))
rw = {s['count']: s for s in src(SP / 's-m-replay-sized-2026-10-13/sized-replay-results-r2.json')['sets']}; rc = {s['count']: s for s in src(C5A / 'replay/sized-replay-results-cold-ts.json')['sets']}
for row, n in TS.items():
    for reset, d in [('warm', rw), ('cold', rc)]: add('tsjs', row, 'SM-9', reset, 'replay-sized r2' if reset == 'warm' else 'U-5a replay', stat([byts(r) for r in measured(d[n]['runs'])]), sources=n, label='synthetic SM-9 under D-1')
# --- Rust rows ---
for reset, d in [('warm', src(SP / 's-m-sm3-ready-2026-10-09/results.json')), ('cold', c5b('sm3/results.json'))]:
    s = stat([byts(r) for r in measured(d['runs'])])
    for row in RS: add('rust', row, 'SM-3', reset, 'sm3-ready' if reset == 'warm' else 'U-5b sm3', s, note='one shared Rust start figure')
def sm4_rows(series, reset, source):
    out = {}
    for s in series:
        per = []; kids = []
        for r in measured(s['runs']):
            obs = [u['observationInformational'] for u in r['result']['unitResults'] if u.get('compilerLaunched')]
            per.append(max(byts(o, 'rss_native', 'none') for o in obs)); kids.append(len(obs))
        out[s['ordinal']] = (stat(per), kids)
    return out
u1 = load(U1)['series']; pins[str(U1)] = sha(U1); acc = src(SP / 's-m-actual-static-profile-series-2026-10-10/actual-static-profile-samples-r1.json')['series']
c4 = c5b('sm4/bsabsent-static-profile-series-cold-rust.json')['series']
w4 = sm4_rows(u1, 'warm', 'U-1'); a4 = sm4_rows(acc, 'warm', 'static-profile'); k4 = sm4_rows(c4, 'cold', 'U-5b')
ORD = {0: 'poly-medium-napi-rs', 1: 'rs-medium-aws-lambda-rust-runtime', 2: 'rs-medium-axum', 3: 'rs-medium-hyper', 4: 'rs-medium-serde', 5: 'rs-medium-serde-json', 6: 'rs-medium-tokio', 7: 'mr-rs-medium-serde-json', 8: 'mr-rs-medium-serde-json'}
for o, row in ORD.items():
    ent = {7: 'rs-medium-serde (entry 7)', 8: 'rs-medium-serde-json (entry 8)'}.get(o)
    warm = a4[o] if o == 3 else w4[o]
    add('rust', row, 'SM-4', 'warm', 'static-profile series (D-5; U-1 changes no hyper unit)' if o == 3 else 'U-1 static-profile, build-script outputs absent (D-5)', warm[0], entryChild=ent, perRunCompilerChildren=sorted(set(warm[1])), label='largest single compiler child per run; executor parent not recorded')
    add('rust', row, 'SM-4', 'cold', 'U-5b sm4 (U-1 runner)', k4[o][0], entryChild=ent, perRunCompilerChildren=sorted(set(k4[o][1])), label='largest single compiler child per run; executor parent not recorded')
for comp, warmp, coldrel, key in [('SM-5', U2C / 'sm5-two-part-results-r2.json', 'sm5/sm5-two-part-results-r2.json', 'workloads'), ('SM-7', U2C / 'sm7-results-r3.json', 'sm7/sm7-results-r3.json', 'results')]:
    for reset, d in [('warm', src(warmp)), ('cold', c5b(coldrel))]:
        for w in d[key]:
            e = w['entry']; row = 'mr-rs-medium-serde-json' if e.startswith('mr-') else e
            add('rust', row, comp, reset, ('U-2c sm5 r2' if comp == 'SM-5' else 'U-2c sm7 r3') if reset == 'warm' else f"U-5b {'sm5' if comp == 'SM-5' else 'sm7'}", stat([byts(r) for r in measured(w['runs'])]), entryChild=e.split('/', 1)[1] if e.startswith('mr-') else None,
                label='receiver child process (sender is the measuring parent)' if comp == 'SM-7' else 'probe child process')
rcr = {s['count']: s for s in c5b('replay/sized-replay-results-cold-rust.json')['sets']}
for row, n in RS.items():
    for reset, d in [('warm', rw), ('cold', rcr)]: add('rust', row, 'SM-9', reset, 'replay-sized r2' if reset == 'warm' else 'U-5b replay', stat([byts(r) for r in measured(d[n]['runs'])]), sources=n, label='synthetic SM-9 under D-1')
# R8 per-entry rows: also the larger of the two entry children (LD-U4B-R8-RSS)
for comp in ['SM-4', 'SM-5', 'SM-7']:
    for reset in ['warm', 'cold']:
        pair = [r for r in rows if r['row'] == 'mr-rs-medium-serde-json' and r['component'] == comp and r['reset'] == reset]; assert len(pair) == 2
        rows.append(dict(language='rust', row='mr-rs-medium-serde-json', component=comp, reset=reset, source='larger of the two entry children (LD-U4B-R8-RSS)', unit='bytes', medianBytes=max(p['medianBytes'] for p in pair), maxBytes=max(p['maxBytes'] for p in pair), entryChild='max of entries 7 and 8'))
# --- SM-11: coverage labels for the eight medium Rust rows (D-5 populations; item 9's quotient rule) ---
graphs = {e['ordinal']: e for e in load('/tmp/opensip-implementation/sm-command-data-bsabsent-2026-10-13/bsabsent-command-source-maps-r1.json')['results']}
sm11 = []
for s in u1:
    o = s['ordinal']; g = graphs[o]; assert sha(g['graph']['path']) == g['graph']['sha256']; units = load(g['graph']['path'])['units']
    first = s['runs'][3]['result']['unitResults']; st = {u['index']: u for u in first}
    fp = [i for i, u in enumerate(units) if u['pkg_id'].startswith('path+')]; dep = [i for i in range(len(units)) if i not in fp]
    an = lambda ids: [i for i in ids if st.get(i, {}).get('standing') == 'analysis-and-metadata-completed']
    fp_an = an(fp); dep_an = an(dep); fp_not = [dict(unit=units[i]['target']['name'], kind=units[i]['target']['kind'], standing=st.get(i, {}).get('standing', 'not-in-graph-results'), reason=st.get(i, {}).get('reason')) for i in fp if i not in fp_an]
    includes_dep = len(dep_an) > 0; misses_fp = len(fp_not) > 0; quotient = not includes_dep and not misses_fp
    t_w = (a4 if o == 3 else w4)[o][0]; t_ws = next(x for x in (acc if o == 3 else u1) if x['ordinal'] == o); t_c = next(x for x in c4 if x['ordinal'] == o)
    sm11.append(dict(ordinal=o, row=ORD[o], entryChild={7: 'rs-medium-serde', 8: 'rs-medium-serde-json'}.get(o), S=RS[ORD[o]], SM4=dict(warm=dict(medianNanos=t_ws['medianWholeGraphNanos'], maxNanos=t_ws['maxWholeGraphNanos'], source='static-profile' if o == 3 else 'U-1'), cold=dict(medianNanos=t_c['medianWholeGraphNanos'], maxNanos=t_c['maxWholeGraphNanos'], source='U-5b')),
        SM10=dict(warm=t_w, cold=k4[o][0], label='largest single compiler child per run'), coveredUnits=dict(firstPartyAnalysed=sorted(f"{units[i]['target']['name']} ({'/'.join(units[i]['target']['kind'])})" for i in fp_an), firstPartyNotAnalysed=fp_not, dependencyUnitsAnalysed=len(dep_an), graphUnits=len(units)),
        includesDependencyCrates=includes_dep, missesFirstPartyUnit=misses_fp, quotientRecorded=quotient, quotientReason=None if quotient else ' and '.join(x for x, f in [('includes dependency crates', includes_dep), ('misses first-party units', misses_fp)] if f)))
keys = [(r['language'], r['row'], r['component'], r['reset'], r.get('entryChild')) for r in rows]; assert len(keys) == len(set(keys)), 'duplicate current SM-10 entry'
expected = 6 * 5 * 2 + 8 * 5 * 2 + 3 * 2 + 3 * 2; assert len(rows) == expected, (len(rows), expected)  # 60 TS + 80 Rust (one per row/component/reset) + 6 (R8's SM-4/5/7 x 2 resets have two entry children, not one) + 6 R8 larger-of-two
out = dict(standing='U-4b DESK RECORD (SM-10 PER F/T COMPONENT, BOTH RESETS; SM-11 LABELLED COVERAGE); LEAD macOS PRELIMINARY; NO PLACEHOLDER, F, T OR OUTCOME', SM10=rows, SM10Informational=info, SM10UniqueKey='language,row,component,reset,entryChild', SM11=sm11, round=2, sourcePins=pins,
           leadDecisions=dict(LD_U4B_R8_RSS='R8 RSS is per entry child and the larger of the two; sequential children peaks are not summed (D-3 sums apply to per-child time figures)', LD_U4B_SM4_RSS='SM-4 SM-10 is the largest single compiler child per run; the executor parent is not a recorded process'),
           placeholderFilled=False, FComputed=False, TComputed=False, outcomeRecorded=False, SM11QuotientsRecorded=sum(1 for x in sm11 if x['quotientRecorded']))
(W / 'u4b-desk-records.json').write_text(json.dumps(out, indent=1) + '\n')
print(len(rows), 'current SM-10 entries;', len(info), 'informational;', 'SM-11 quotients', out['SM11QuotientsRecorded'])
for x in sm11: print(x['ordinal'], x['row'], x['S'], len(x['coveredUnits']['firstPartyAnalysed']), len(x['coveredUnits']['firstPartyNotAnalysed']), x['coveredUnits']['dependencyUnitsAnalysed'], x['quotientReason'])
