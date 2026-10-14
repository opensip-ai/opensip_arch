from pathlib import Path
import json, hashlib, statistics, difflib
# Read-only audit of U-5b (PLAN-r3 D-7, U-5): the Q0 9.2 cold-reset series over the Rust-row F and T components
# (F = SM-3 + SM-5 + SM-7 + SM-9; T = F + SM-4). Checks each cold runner against its accepted runner (only the cold
# insertions and the declared runner-specific redirections), one reset record per child in order (OpenSIP state absent,
# fresh empty per-run TMPDIR, page cache recorded), recomputes medians/maxima from the result records and the D-3 R8
# two-entry sums, and reports accepted warm medians beside the cold ones as information only. No F, T or outcome.
W = Path(__file__).resolve().parent; SP = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/spikes')
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest(); med = lambda v: dict(medianNanos=statistics.median(v), maxNanos=max(v))
IMPORT = "import sys as _s;_s.path.insert(0,str(Path(__file__).resolve().parent.parent));import cold_reset as _cr"
JOBS = {'sm3': ('run_ready.py', {'_cr.reset(env,T)', '_cr.write(B)'}), 'replay': ('run_sized_replay_r2.py', {'_cr.reset(env,T)', '_cr.write(H)'}),
        'sm4': ('run_bsabsent_static_profile_series_r1.py', {'_cr.reset(_cold_env,root)', '_cr.write(H)'}), 'sm5': ('run_u2c_sm5_two_part_r2.py', {'_cr.reset(env,T)', '_cr.write(W)'}), 'sm7': ('run_u2c_sm7_r3.py', {'_cr.reset(env,T)', '_cr.write(W)'})}
REDIRECT = {'replay': ({"for count in sorted({71,98,192,208,239,279,301,808}):  # U-5b: the eight Rust row sizes only"}, ["sized-replay-results-cold-rust.json", "H/'evidence'/f'replay-"], {"for count in sorted(int(c) for c in packets['packets']):"}, ["sized-replay-results-r2.json", "H/f'replay-r2-"]),
            'sm4': (set(), ["H = Path(__file__).resolve().parent; dest = H / 'bsabsent-static-profile-series-cold-rust.json'; assert not dest.exists(); _cold_env = {}"], set(), ["dest = V / 'bsabsent-static-profile-series-r1.json'; assert not dest.exists()"])}
def diff_ok(name, accepted, cold, allowed):
    added = []; removed = []
    for op in difflib.ndiff(accepted.split('\n'), cold.split('\n')):
        if op.startswith('+ '): added.append(op[2:])
        elif op.startswith('- '): removed.append(op[2:])
    extra = [l for l in added if l.strip() not in allowed and l != IMPORT]
    if name in REDIRECT:
        add_exact, add_sub, rem_exact, rem_sub = REDIRECT[name]
        extra = [l for l in extra if l.strip() not in add_exact and not any(x in l for x in add_sub)]
        removed = [l for l in removed if l.strip() not in rem_exact and not any(x in l for x in rem_sub)]
    return extra == [] and removed == [], dict(unexpectedAdded=extra, unexpectedRemoved=removed, added=len(added))
out = dict(standing='UNREVIEWED READONLY AUDIT OF U-5b COLD-RESET SERIES (RUST-ROW F AND T COMPONENTS); LEAD macOS PRELIMINARY; NO F, T OR OUTCOME', components={})
# warm (accepted) references, information only
warm_sm3 = json.loads((SP / 's-m-sm3-ready-2026-10-09/results.json').read_text())['medianStartToReadyNanos']
warm_replay = {s['count']: statistics.median(x['completeReplayNanos'] for x in s['runs'] if not x['warmup']) for s in json.loads((SP / 's-m-replay-sized-2026-10-13/sized-replay-results-r2.json').read_text())['sets']}
u1idx = {m['member']: m for m in json.loads((SP / 's-m-u1-build-script-outputs-absent-2026-10-13/large-records-index.json').read_text())['members']}
u1p = Path('/tmp/opensip-implementation/sm-command-data-bsabsent-2026-10-13/bsabsent-static-profile-series-r1.json'); assert sha(u1p) == u1idx['bsabsent-static-profile-series-r1.json']['sha256']
u1 = {s['ordinal']: s for s in json.loads(u1p.read_text())['series']}
U2C = SP / 's-m-u2c-rust-sealing-transfer-2026-10-14'
warm5 = {w['entry']: w for w in json.loads((U2C / 'sm5-two-part-results-r2.json').read_text())['workloads']}; warm7 = {w['entry']: w for w in json.loads((U2C / 'sm7-results-r3.json').read_text())['results']}
def series(name):
    d = W / name
    if name == 'sm3':
        r = json.loads((d / 'results.json').read_text()); v = [x['startToReadyNanos'] for x in r['runs'] if not x['warmup']]; assert len(r['runs']) == 10
        return [dict(workload='SM-3', runs=10, **med(v), warmMedianNanos=warm_sm3)]
    if name == 'replay':
        r = json.loads((d / 'sized-replay-results-cold-rust.json').read_text()); rows = []
        for s in r['sets']:
            assert len(s['runs']) == 10 and all(x['fullReplayPassed'] and x['findings'] == s['count'] for x in s['runs'])
            rows.append(dict(workload=f"replay-{s['count']}", runs=10, **med([x['completeReplayNanos'] for x in s['runs'] if not x['warmup']]), warmMedianNanos=warm_replay[s['count']]))
        assert sorted(int(x['workload'].split('-')[1]) for x in rows) == [71, 98, 192, 208, 239, 279, 301, 808]; return rows
    if name == 'sm4':
        r = json.loads((d / 'bsabsent-static-profile-series-cold-rust.json').read_text()); rows = []
        for s in r['series']:
            w = u1[s['ordinal']]; assert len(s['runs']) == 10 and s['populationRepeated'] and s['readSetsRepeated'] and s['acceptedAnalysedUnitsStillAnalysed'] and s['metadataRepeatForEveryAnalyzedUnit']
            assert s['analysedUnits'] == w['analysedUnits'] and s['incompleteUnits'] == w['incompleteUnits'] and [u['index'] for u in s['newlyAnalysedUnits']] == [u['index'] for u in w['newlyAnalysedUnits']]
            rows.append(dict(workload=f"{s['ordinal']}:{s['id']}", ordinal=s['ordinal'], runs=10, **med([x['wholeGraphNanos'] for x in s['runs'] if not x['warmup']]), analysedUnits=s['analysedUnits'], populationEqualsU1=True, warmMedianNanos=w['medianWholeGraphNanos']))
        return rows
    if name == 'sm5':
        r = json.loads((d / 'sm5-two-part-results-r2.json').read_text()); rows = []
        for w in r['workloads']:
            assert len(w['runs']) == 10 and w['acceptedTypedRepositoryShapeReproduced'] and w['shape'] == warm5[w['entry']]['shape']
            m = [x for x in w['runs'] if not x['warmup']]
            rows.append(dict(workload=w['entry'], runs=10, **med([x['elapsedNanos'] for x in m]), repositoryPart=med([x['repositoryPartNanos'] for x in m]), dependencyPart=med([x['dependencyPartNanos'] for x in m]), shapeEqualsU2c=True, warmMedianNanos=warm5[w['entry']]['elapsed']['median']))
        return rows
    r = json.loads((d / 'sm7-results-r3.json').read_text()); assert r['positiveControl']['exitCode'] == 0 and len(r['controls']) == 20 and all(c['exitCode'] != 0 for c in r['controls']); rows = []
    for w in r['results']:
        a = warm7[w['entry']]; assert len(w['runs']) == 10 and w['manifestSha256'] == a['manifestSha256'] and w['dependencySeal'] == a['dependencySeal'] and w['dependencyManifestSha256'] == a['dependencyManifestSha256']
        rows.append(dict(workload=w['entry'], runs=10, **med([x['transferNanos'] for x in w['runs'] if not x['warmup']]), sealAndManifestEqualU2c=True, warmMedianNanos=a['medianTransferNanos']))
    return rows
for name, (runner, allowed) in JOBS.items():
    d = W / name; accepted = Path((d / 'ACCEPTED-RUNNER-SOURCE').read_text().split('\n')[0].strip())
    ok, why = diff_ok(name, accepted.read_text(), (d / runner).read_text(), allowed)
    recs = json.loads((d / 'cold-reset-records.json').read_text())['records']; rows = series(name)
    assert len(recs) == sum(x['runs'] for x in rows), (name, len(recs))
    assert all(x['openSIPStateAbsent'] and x['runTMPDIREmpty'] and x['pageCache']['fileBackedPages'] is not None and x['pageCache']['pageSizeBytes'] > 0 for x in recs)
    assert len({x['runTMPDIR'] for x in recs}) == len(recs) and [x['index'] for x in recs] == list(range(len(recs)))
    out['components'][name] = dict(acceptedRunner=dict(path=str(accepted), sha256=sha(accepted)), coldRunner=dict(path=f'{name}/{runner}', sha256=sha(d / runner)), diffConfinedToColdInsertions=ok, diff=why, resetRecords=len(recs), oneResetPerChild=True,
                                    fileBackedPagesRange=[min(x['pageCache']['fileBackedPages'] for x in recs), max(x['pageCache']['fileBackedPages'] for x in recs)], series=rows)
assert (W / 'cold_reset.py').read_bytes() == (SP / 's-m-cold-ts-2026-10-13/cold_reset.py').read_bytes()
c = out['components']; pair = lambda rows: [r for r in rows if r['workload'].startswith('mr-rs-medium-serde-json/')]
r8 = dict(SM4=dict(medianSumNanos=sum(r['medianNanos'] for r in c['sm4']['series'] if r['ordinal'] in (7, 8)), maxSumNanos=sum(r['maxNanos'] for r in c['sm4']['series'] if r['ordinal'] in (7, 8))))
for k, n in [('SM5', 'sm5'), ('SM7', 'sm7')]:
    p = pair(c[n]['series']); assert len(p) == 2; r8[k] = dict(medianSumNanos=sum(r['medianNanos'] for r in p), maxSumNanos=sum(r['maxNanos'] for r in p))
interp = json.loads((W / 'cold-rust-interpretation.json').read_text())
for n in JOBS: row = interp['components'][n]; assert row['result']['sha256'] == sha(W / row['result']['path']) and row['resetLabel'].startswith('cold OpenSIP state, page cache recorded') and row['inheritedStandingObsolete']
assert interp['components']['replay']['SM9LowerBoundOnly'] is False
out.update(R8TwoEntryChildren=dict(label="two entry children (PLAN-r3 D-3): sums of the two entries' medians and of their maxima", **r8), coldResetModuleEqualsU5a=True, currentInterpretation=dict(path='cold-rust-interpretation.json', sha256=sha(W / 'cold-rust-interpretation.json')),
           allDiffsConfined=all(x['diffConfinedToColdInsertions'] for x in c.values()), label='cold OpenSIP state, page cache recorded (never claimed flushed)', FComputed=False, TComputed=False, outcomeRecorded=False, placeholderFilled=False, SMComplete=False, LG1Met=False, effectiveL=False)
(W / 'cold-rust-checks.json').write_text(json.dumps(out, indent=1) + '\n')
for n, x in c.items(): print(n, x['diffConfinedToColdInsertions'], x['resetRecords'], [(s['workload'], round(s['medianNanos'] / 1e6, 3), round(s['warmMedianNanos'] / 1e6, 3)) for s in x['series']])
print(json.dumps(out['R8TwoEntryChildren']))
