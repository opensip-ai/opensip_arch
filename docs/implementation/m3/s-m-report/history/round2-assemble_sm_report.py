from pathlib import Path
import json, hashlib, statistics
# U-6 (PLAN-r3): assemble the S-M report data from accepted, committed records (and index-pinned working copies).
# Every component statistic is recomputed from its raw run records (3 warmups + 7 measured; median and max of the 7).
# F = start (SM-1 | SM-3) + SM-5 + SM-7 + SM-9; T = F + analysis (SM-2 | SM-4) (item 9, "Derived figures"), per row,
# under each reset S-M applied (warm D-7; cold U-5a/U-5b), as sums of component medians (and, beside, of maxima).
# R8 (D-3): SM-4, SM-5 and SM-7 are the sums of the two entry children; SM-3 enters F once per child (twice); SM-9 once.
# Outcomes (item 9; AQP 5.2/5.3 targets: edit target <= 2 s median WARM; medium budgets cold <= 30 s, warm <= 8 s):
# (B) iff warm F > 2 s; (C) iff cold T > 30 s or warm T > 8 s; (A) iff neither. Every outcome is conditional on D-1
# (SM-9 synthetic) and preliminary (lead macOS host, not the D12 runner). Sensitivities are reported, not substituted.
# Round 2 (Codex SM-U6-R1-RF-01, RF-02): every other figure (SM-5 populations, SM-6, SM-8, SM-10, SM-11, SM-12 incl. Sui,
# SM-13/14 decomposition, S_eff first term, the large-workload matrix) is materialized below in `otherFigures` from pinned
# accepted records; the timing components, F, T and outcomes are derived exactly as in round 1.
W = Path(__file__).resolve().parent; A = Path('/Users/sb/code/opensip-ai/opensip_arch'); SP = A / 'docs/implementation/m3/spikes'
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest(); pins = {}
def load(p): p = Path(p); pins[str(p.relative_to(A)) if str(p).startswith(str(A)) else str(p)] = sha(p); return json.loads(p.read_text())
def st(runs, key):
    assert len(runs) == 10 and [r['ordinal'] for r in runs] == list(range(10)) and all(r['warmup'] == (r['ordinal'] < 3) for r in runs)
    v = [r[key] for r in runs[3:]]; return dict(medianNanos=statistics.median(v), maxNanos=max(v), measured=7)
TS = {'js-medium-express': 141, 'poly-medium-napi-rs': 193, 'ts-medium-powertools-lambda': 936, 'ts-medium-smithy-typescript': 1159, 'ts-medium-umami': 1381, 'ts-medium-vite': 678}
RS = {'poly-medium-napi-rs': 239, 'rs-medium-aws-lambda-rust-runtime': 192, 'rs-medium-axum': 301, 'rs-medium-hyper': 98, 'rs-medium-serde': 208, 'rs-medium-serde-json': 71, 'rs-medium-tokio': 808, 'mr-rs-medium-serde-json': 279}
ORD = {'poly-medium-napi-rs': [0], 'rs-medium-aws-lambda-rust-runtime': [1], 'rs-medium-axum': [2], 'rs-medium-hyper': [3], 'rs-medium-serde': [4], 'rs-medium-serde-json': [5], 'rs-medium-tokio': [6], 'mr-rs-medium-serde-json': [7, 8]}
C5A = SP / 's-m-cold-ts-2026-10-13'; C5B = SP / 's-m-cold-rust-2026-10-14'; U2C = SP / 's-m-u2c-rust-sealing-transfer-2026-10-14'
# U-5b's SM-4 result is inside its raw archive; read the index-pinned working copy. U-1's series likewise (its large-records index).
c5b_raw = {m['member']: m['sha256'] for m in load(C5B / 'raw-evidence-index.json')['members']}
def c5b_sm4():
    p = Path('/Users/sb/code/.opensip-implementation-cache/work-2026-10-14/u5b/sm4/bsabsent-static-profile-series-cold-rust.json'); assert sha(p) == c5b_raw['sm4/bsabsent-static-profile-series-cold-rust.json']; pins['U-5b:sm4/bsabsent-static-profile-series-cold-rust.json'] = sha(p); return json.loads(p.read_text())
u1p = Path('/tmp/opensip-implementation/sm-command-data-bsabsent-2026-10-13/bsabsent-static-profile-series-r1.json')
assert sha(u1p) == {m['member']: m for m in load(SP / 's-m-u1-build-script-outputs-absent-2026-10-13/large-records-index.json')['members']}['bsabsent-static-profile-series-r1.json']['sha256']; pins['U-1:bsabsent-static-profile-series-r1.json'] = sha(u1p)
comp = {}  # (row, lang, figure, reset) -> stat
def put(row, lang, fig, reset, s, source, **kw): comp[(row, lang, fig, reset)] = dict(row=row, language=lang, figure=fig, reset=reset, source=source, **s, **kw)
# TS
for reset, d, srcname in [('warm', load(SP / 's-m-sm1-ready-closure-2026-10-09/results.json'), 's-m-sm1-ready-closure-2026-10-09'), ('cold', load(C5A / 'sm1/results.json'), 's-m-cold-ts-2026-10-13/sm1')]:
    s = st(d['runs'], 'startToReadyNanos')
    for row in TS: put(row, 'tsjs', 'SM-1', reset, s, srcname)
for reset, coh, syn, cs, ss in [('warm', load(SP / 's-m-ts-cohort-2026-10-09/results.json'), load(SP / 's-m-ts-synthesized-2026-10-10/results.json'), 's-m-ts-cohort-2026-10-09', 's-m-ts-synthesized-2026-10-10 (D-4)'),
                                ('cold', load(C5A / 'cohort/results.json'), load(C5A / 'synthesized/results.json'), 's-m-cold-ts-2026-10-13/cohort', 's-m-cold-ts-2026-10-13/synthesized (D-4)')]:
    for w in coh['workloads']:
        if w['id'] in TS and w['id'] != 'js-medium-express': put(w['id'], 'tsjs', 'SM-2', reset, st(w['runs'], 'wholeProcessNanos'), cs)
    w = next(x for x in syn['workloads'] if x['id'] == 'js-medium-express'); put('js-medium-express', 'tsjs', 'SM-2', reset, st(w['runs'], 'wholeProcessNanos'), ss)
for fig, key, warm, cold, wn, cn in [('SM-5', 'elapsedNanos', SP / 's-m-sealing-typed-2026-10-09/results.json', C5A / 'sealing/results.json', 's-m-sealing-typed-2026-10-09', 's-m-cold-ts-2026-10-13/sealing'),
                                     ('SM-7', 'transferNanos', SP / 's-m-transfer-2026-10-09/results.json', C5A / 'transfer/results.json', 's-m-transfer-2026-10-09', 's-m-cold-ts-2026-10-13/transfer')]:
    for reset, d, n in [('warm', load(warm), wn), ('cold', load(cold), cn)]:
        for w in d['workloads']:
            if w['id'] in TS: put(w['id'], 'tsjs', fig, reset, st(w['runs'], key), n, label='repository-only (T2 pins no node_modules tree; SM-6)' if fig == 'SM-7' else 'snapshot2/plan2-equivalent typed sealing')
rw = {s['count']: s for s in load(SP / 's-m-replay-sized-2026-10-13/sized-replay-results-r2.json')['sets']}; rc5a = {s['count']: s for s in load(C5A / 'replay/sized-replay-results-cold-ts.json')['sets']}
for row, n in TS.items():
    for reset, d, src in [('warm', rw, 's-m-replay-sized-2026-10-13 (r2)'), ('cold', rc5a, 's-m-cold-ts-2026-10-13/replay')]:
        assert all(r['fullReplayPassed'] and r['findings'] == n for r in d[n]['runs']); put(row, 'tsjs', 'SM-9', reset, st(d[n]['runs'], 'completeReplayNanos'), src, sources=n, label='synthetic SM-9 under D-1')
# Rust
for reset, d, n in [('warm', load(SP / 's-m-sm3-ready-2026-10-09/results.json'), 's-m-sm3-ready-2026-10-09'), ('cold', load(C5B / 'sm3/results.json'), 's-m-cold-rust-2026-10-14/sm3')]:
    s = st(d['runs'], 'startToReadyNanos')
    for row in RS: put(row, 'rust', 'SM-3', reset, s, n, perChild=True)
def entries(d, key, k):
    out = {}
    for w in d[key]: out[w['entry']] = st(w['runs'], k)
    return out
def rsum(parts): return dict(medianNanos=sum(p['medianNanos'] for p in parts), maxNanos=sum(p['maxNanos'] for p in parts), measured=7)
for fig, fname, key, k in [('SM-5', 'sm5-two-part-results-r2.json', 'workloads', 'elapsedNanos'), ('SM-7', 'sm7-results-r3.json', 'results', 'transferNanos')]:
    for reset, d, n in [('warm', load(U2C / fname), f's-m-u2c-rust-sealing-transfer-2026-10-14/{fname}'), ('cold', load(C5B / ('sm5' if fig == 'SM-5' else 'sm7') / fname), f"s-m-cold-rust-2026-10-14/{'sm5' if fig == 'SM-5' else 'sm7'}")]:
        e = entries(d, key, k)
        for row in RS:
            if row == 'mr-rs-medium-serde-json':
                pair = [e['mr-rs-medium-serde-json/rs-medium-serde'], e['mr-rs-medium-serde-json/rs-medium-serde-json']]; put(row, 'rust', fig, reset, rsum(pair), n, entryChildren=pair, label='two entry children (D-3): sums of medians and of maxima')
            else: put(row, 'rust', fig, reset, e[row], n)
rc5b = {s['count']: s for s in load(C5B / 'replay/sized-replay-results-cold-rust.json')['sets']}
for row, n in RS.items():
    for reset, d, src in [('warm', rw, 's-m-replay-sized-2026-10-13 (r2)'), ('cold', rc5b, 's-m-cold-rust-2026-10-14/replay')]:
        assert all(r['fullReplayPassed'] and r['findings'] == n for r in d[n]['runs']); put(row, 'rust', 'SM-9', reset, st(d[n]['runs'], 'completeReplayNanos'), src, sources=n, label='synthetic SM-9 under D-1')
u1 = {s['ordinal']: s for s in json.loads(u1p.read_text())['series']}; acc = {s['ordinal']: s for s in load(SP / 's-m-actual-static-profile-series-2026-10-10/actual-static-profile-samples-r1.json')['series']}; c4 = {s['ordinal']: s for s in c5b_sm4()['series']}
for row, ords in ORD.items():
    for reset in ['warm', 'cold']:
        parts = []
        for o in ords:
            s = (acc[o] if (reset == 'warm' and o == 3) else u1[o]) if reset == 'warm' else c4[o]
            parts.append(st(s['runs'], 'wholeGraphNanos'))
        src = ('s-m-actual-static-profile-series-2026-10-10 (D-5; U-1 changes no hyper unit)' if row == 'rs-medium-hyper' else 's-m-u1-build-script-outputs-absent-2026-10-13 (D-5)') if reset == 'warm' else 's-m-cold-rust-2026-10-14/sm4 (U-1 runner)'
        put(row, 'rust', 'SM-4', reset, rsum(parts) if len(parts) > 1 else parts[0], src, entryChildren=parts if len(parts) > 1 else None, label='whole-graph span; partial coverage (SM-11; U-4b)')
# F, T, outcomes
NS = 1e9; rows = []
for lang, R, start, ana in [('tsjs', TS, 'SM-1', 'SM-2'), ('rust', RS, 'SM-3', 'SM-4')]:
    for row in R:
        out = dict(row=row, language=lang, sources=R[row])
        for reset in ['warm', 'cold']:
            g = lambda f: comp[(row, lang, f, reset)]
            k = 2 if row == 'mr-rs-medium-serde-json' else 1
            for stat in ['medianNanos', 'maxNanos']:
                F = k * g(start)[stat] + g('SM-5')[stat] + g('SM-7')[stat] + g('SM-9')[stat]; T = F + g(ana)[stat]
                out[f'F_{reset}_{stat}'] = F; out[f'T_{reset}_{stat}'] = T
            out[f'F_{reset}_withoutSM9_medianNanos'] = out[f'F_{reset}_medianNanos'] - g('SM-9')['medianNanos']
            if lang == 'tsjs': out[f'T_{reset}_minusDoubleCountedStart_medianNanos'] = out[f'T_{reset}_medianNanos'] - g('SM-1')['medianNanos']
        Fw = out['F_warm_medianNanos'] / NS; Tw = out['T_warm_medianNanos'] / NS; Tc = out['T_cold_medianNanos'] / NS
        B = Fw > 2; Cw = Tw > 8; Cc = Tc > 30; C = Cw or Cc
        out['outcomes'] = sorted([x for x, f in [('B', B), ('C', C)] if f]) or ['A']
        out['outcomeDetail'] = dict(warmFOver2s=B, warmTOver8s=Cw, coldTOver30s=Cc)
        sens = {}
        sens['BHoldsWithoutSM9'] = (out['F_warm_withoutSM9_medianNanos'] / NS) > 2 if B else None
        sens['warmCHoldsWithoutSM9'] = ((out['T_warm_medianNanos'] - comp[(row, lang, 'SM-9', 'warm')]['medianNanos']) / NS) > 8 if Cw else None
        sens['coldCHoldsWithoutSM9'] = ((out['T_cold_medianNanos'] - comp[(row, lang, 'SM-9', 'cold')]['medianNanos']) / NS) > 30 if Cc else None
        if lang == 'tsjs':
            sens['warmCHoldsWithoutDoubleCountedStart'] = (out['T_warm_minusDoubleCountedStart_medianNanos'] / NS) > 8 if Cw else None
            sens['coldCHoldsWithoutDoubleCountedStart'] = (out['T_cold_minusDoubleCountedStart_medianNanos'] / NS) > 30 if Cc else None
        sens['outcomeSameUnderSumOfMaxima'] = (sorted([x for x, f in [('B', out['F_warm_maxNanos'] / NS > 2), ('C', out['T_warm_maxNanos'] / NS > 8 or out['T_cold_maxNanos'] / NS > 30)] if f]) or ['A']) == out['outcomes']
        out['sensitivity'] = sens; rows.append(out)
report = dict(standing='U-6 S-M REPORT DATA (UNREVIEWED); LEAD macOS PRELIMINARY, NOT D12; F, T AND OUTCOMES CONDITIONAL ON D-1', components=list(comp.values()), rows=rows, pins=pins,
              targets=dict(editTargetWarmMedianSeconds=2, mediumColdMedianSeconds=30, mediumWarmMedianSeconds=8, source='analysis-quality PLAN.md (AQP r6) 5.2 table and 5.3 decision'),
              rules=dict(F='start (SM-1 TS | SM-3 Rust) + SM-5 + SM-7 + SM-9', T='F + analysis (SM-2 TS | SM-4 Rust)', statistic='sum of component medians (each the median of 7 measured runs); sums of maxima beside', R8='D-3: SM-3 twice; SM-4, SM-5, SM-7 entry sums; SM-9 once',
                         B='warm F > 2 s', C='cold T > 30 s or warm T > 8 s', A='neither B nor C'))
# ---- other figures (round 2) ----
OF = {}
typed = {w['id']: w for w in load(SP / 's-m-sealing-typed-2026-10-09/results.json')['workloads']}
u2c5 = {w['entry']: w for w in load(U2C / 'sm5-two-part-results-r2.json')['workloads']}
BREP = dict(rows=100000, descriptorBytes=4194304, bytes=8589934592, source='item 9 SM-5 (PROPOSAL-r6:559); D-9')
BDEP = dict(packages=4096, entries=1000000, bytes=8589934592, descriptorBytes=None, source='NE:2931-2932 ProtocolLimitsV3; DependencySourceSetV1 packages maxItems 4096; no descriptor-bytes bound found')
def repo(sh): return dict(rows=sh['rows'], bytes=sh['bytes'], snapshotDescriptorBytes=sh['snapshotEquivalentDescriptorBytes'], withinRows=sh['rows'] <= BREP['rows'], withinDescriptor=sh['snapshotEquivalentDescriptorBytes'] <= BREP['descriptorBytes'], withinBytes=sh['bytes'] <= BREP['bytes'])
pop = []
for row in TS: pop.append(dict(row=row, language='tsjs', repository=repo(typed[row]['shape']), dependency=None, source='s-m-sealing-typed-2026-10-09/results.json'))
for e, w in u2c5.items():
    dp = w['shape']['dependency']
    pop.append(dict(row='mr-rs-medium-serde-json' if e.startswith('mr-') else e, entryChild=e.split('/', 1)[1] if e.startswith('mr-') else None, language='rust', repository=repo(w['shape']['repository']),
                    dependency=dict(packages=dp['packages'], entries=dp['entries'], bytes=dp['bytes'], descriptorCanonicalBytes=dp['descriptorCanonicalBytes'], dependencySourceSetId=dp['dependencySourceSetId'], withinPackages=dp['packages'] <= 4096, withinEntries=dp['entries'] <= 1000000, withinBytes=dp['bytes'] <= 8589934592, descriptorBound=None),
                    source='s-m-u2c-rust-sealing-transfer-2026-10-14/sm5-two-part-results-r2.json'))
OF['SM5Populations'] = dict(repositoryBounds=BREP, dependencyBounds=BDEP, rows=pop, rule='D-9: the dependency part is reported beside snapshot2 rows, never added; R8 per entry (D-3)')
sm6 = load(SP / 's-m-sm6-readset-2026-10-09/results.json')
OF['SM6'] = dict(label='repository-only (T2 pins no dependency tree)', rows=[dict(row=w['id'], entries=w['entries'], bytes=w['bytes'], snapshotDescriptorBytes=w['snapshotEquivalentDescriptorBytes'], TS2EntriesWithin200000=w['TS2EntriesWithin200000'], snapshot2RowsWithin100000=w['snapshot2RowsWithin100000'], descriptorWithin4MiB=w['snapshot2DescriptorWithin4194304'], bytesWithin8GiB=w['snapshot2BytesWithin8589934592']) for w in sm6['workloads']])
u4a = load(SP / 's-m-desk-u4a-2026-10-13/u4a-desk-records.json')
OF['SM8'] = dict(definition=u4a['SM8']['definition'], label=u4a['SM8']['granularityLabel'], rows=[dict(row=r, source=x['source'], medianNanos=x['medianNanos'], maxNanos=x['maxNanos'], callNames=sorted(set(x['callNamesAtMedianAndMax']))) for r, x in u4a['SM8']['rows'].items()])
OF['SEffFirstTerm'] = dict(definition=u4a['SEffFirstTerm']['definition'], bounds=u4a['SEffFirstTerm']['bounds'], rows=u4a['SEffFirstTerm']['rows'], dependencyPartBeside=[dict(row=p['row'], entryChild=p.get('entryChild'), **{k: p['dependency'][k] for k in ['packages', 'entries', 'bytes']}) for p in pop if p['dependency']], SEffFilled=False)
u4b = load(SP / 's-m-desk-u4b-2026-10-14/u4b-desk-records.json')
OF['SM10'] = dict(entries=u4b['SM10'], informational=u4b['SM10Informational'], uniqueKey=u4b['SM10UniqueKey'], leadDecisions=u4b['leadDecisions'])
large = load(SP / 's-m-large-site-census-2026-10-13/large-site-census-checks-r1.json'); cov = SP / 's-m-large-site-census-2026-10-13/large-workload-entry-coverage.md'; pins[str(cov.relative_to(A))] = sha(cov)
OF['SM11'] = dict(medium=u4b['SM11'], large=[dict(id=w['id'], entries=w['entries'], S=w['subjectCountS'], firstPartySubjectsWithSites=w['firstPartySubjectsWithSites'], subjectCoverage=w['subjectCoverage'], coverageExact=w['coverageExact']) for w in large['workloads']], largeNotAnalysed=['poly-large-rspack', 'rs-very-large-sui'], largeEntryCoverage=str(cov.relative_to(A)), quotientsRecorded=0)
scope = load(SP / 's-m-rust-scope-2026-10-09/results.json'); sui = load(SP / 's-m-sui-scope-series-2026-10-10/source.json')
OF['SM12'] = dict(labels=dict(time='reconstruction/commitment/array-CBOR span after input parsing', memory='whole-process wait4 RSS, native bytes (macOS) with identity conversion; process peak, not incremental algorithm heap accounting (D-8)', workerPrototype='worker-prototype is a separate process repeating the second implementation; not the operational native worker', pending='domainCommitment with bound keys and the worker derivation wait for the completion round'),
                  rows=[dict(workload=w['id'], S=w['subjectCount'], arraysAndCommitmentsEqual=w['threeActorArraysAndCommitmentsEqual'], actors=[dict(actor=a['actor'], medianNanos=a['medianNanos'], maxNanos=a['maxNanos'], peakRssBytes=a['measuredPeakProcessRssBytes']) for a in w['actors']]) for w in scope['workloads']]
                       + [dict(workload='rs-very-large-sui', S=sui['subjects'], arraysAndCommitmentsEqual=sui['allArraysScopeDomainAndCborMatch'], actors=[dict(actor=x['actor'], medianNanos=x['medianNanos'], maxNanos=x['maxNanos'], peakRssBytes=x['processPeakRssBytes']) for x in sui['statistics']])])
census = load(SP / 's-m-rust-site-census-v2-2026-10-13/site-census-checks-v2.json'); fixed = load(SP / 's-m-rust-site-census-v2-2026-10-13/sm13-fixed-bytes.json')
OF['SM13'] = dict(label='a decomposition, not a value: sites, not candidates; owned parameters unset', sitesMedium=[dict(id=w['id'], ordinal=w['ordinal'], S=w['subjectCountS'], firstPartySubjectsWithSites=w['firstPartySubjectsWithSites'], firstPartySitesOfferedByRelation=w['firstPartySitesOfferedByRelation'], dependencyCrateSitesOfferedByRelation=w['dependencyCrateSitesOfferedByRelation']) for w in census['workloads']],
                  sitesLarge=[dict(id=w['id'], S=w['subjectCountS'], firstPartySitesOfferedByRelation=w['firstPartySitesOfferedByRelation'], dependencyCrateSitesOfferedByRelation=w['dependencyCrateSitesOfferedByRelation']) for w in large['workloads']],
                  fixedBytes={k: fixed[k] for k in ['perCandidate', 'b_spool', 'c_payload', 'd_frames', 'e_census', 'a_candidates']}, unsetParameters=fixed['unsetParameters'], ambiguities=fixed['ambiguities'], valueDerived=False)
OF['SM14'] = dict(formula=fixed['SM14'], S={w['id']: w['subjectCountS'] for w in census['workloads']} | {w['id']: w['subjectCountS'] for w in large['workloads']}, valueDerived=False)
OF['LargeWorkloads'] = dict(SEffFirstTerm={k: v for k, v in u4a['SEffFirstTerm']['rows'].items() if 'large' in k}, census=OF['SM11']['large'], entryCoverage=str(cov.relative_to(A)), noOutcomeDependsOnThem=True)
report['otherFigures'] = OF; report['pins'] = pins
(W / 'sm-report-data.json').write_text(json.dumps(report, indent=1) + '\n')
for r in rows: print(f"{r['language']:5} {r['row']:38} Fw {r['F_warm_medianNanos']/NS:8.3f} Fc {r['F_cold_medianNanos']/NS:8.3f} Tw {r['T_warm_medianNanos']/NS:8.3f} Tc {r['T_cold_medianNanos']/NS:8.3f} {r['outcomes']} {r['sensitivity']}")
