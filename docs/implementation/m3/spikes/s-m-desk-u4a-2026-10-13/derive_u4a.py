from pathlib import Path
import json, hashlib, statistics
# U-4a desk record under the accepted S-M report plan (docs/implementation/m3/s-m-report-plan/PLAN-r2.md):
# (1) SM-8 under D-6: per measured SM-2 run, the longest single public TypeScript compiler API call the driver made
#     (max over every configuration's retained calls[], incomplete configurations included, with its call name), with
#     each completed configuration's recorded maxPublicCompilerCall cross-checked; median and max over the 7 measured runs. Express uses the synthesized program
#     (D-4). Read-only over accepted committed evidence; no new run.
# (2) S_eff's first term under D-9: SM-5's measured snapshot2-equivalent population per Rust workload (rows, total
#     bytes, descriptor bytes, bound standing), copied from the accepted sealing checks. No ceiling is extrapolated.
# Writes u4a-desk-records.json beside itself. Fills no placeholder; computes no F or T.
H = Path(__file__).resolve().parent; A = Path('/Users/sb/code/opensip-ai/opensip_arch'); SP = A / 'docs/implementation/m3/spikes'
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
def evidence(spike, run):
    p = SP / spike / 'evidence' / Path(run['stdout']).name; assert p.is_file(), p; return p
def sm8_rows(spike, ids):
    res = json.loads((SP / spike / 'results.json').read_text()); out = {}
    for w in res['workloads']:
        if w['id'] not in ids: continue
        runs = [r for r in w['runs'] if not r['warmup']]; assert [r['ordinal'] for r in runs] == list(range(3, 10)) and all(r['exitCode'] == 0 for r in runs)
        per = []
        for r in runs:
            p = evidence(spike, r); d = json.loads(p.read_text()); assert d['id'] == w['id'] and d['emitPerformed'] is False and d['repositoryCodeExecuted'] is False
            best = None
            for c in d['configurations']:
                # Every configuration retains its public calls, incomplete ones included; the recorded per-configuration
                # maximum (present on completed configurations) must equal the maximum of its retained calls.
                top = max(c['calls'], key=lambda x: x['elapsedNanos'])
                if 'maxPublicCompilerCall' in c: m = c['maxPublicCompilerCall']; assert (m['name'], m['elapsedNanos']) == (top['name'], top['elapsedNanos']), (w['id'], c.get('config'))
                else: assert c['standing'] == 'incomplete', (w['id'], c.get('config'))
                if best is None or top['elapsedNanos'] > best['elapsedNanos']: best = dict(name=top['name'], elapsedNanos=top['elapsedNanos'], configuration=c.get('config', c.get('origin')), configurationStanding=c['standing'])
            per.append(dict(ordinal=r['ordinal'], evidence=dict(path=str(p.relative_to(A)), sha256=sha(p)), longestCall=best))
        vals = [x['longestCall']['elapsedNanos'] for x in per]
        out[w['id']] = dict(source=spike, measuredRuns=per, medianNanos=statistics.median(vals), maxNanos=max(vals), callNamesAtMedianAndMax=sorted({x['longestCall']['name'] for x in per}))
    return out
sm8 = sm8_rows('s-m-ts-cohort-2026-10-09', {'poly-medium-napi-rs', 'ts-medium-powertools-lambda', 'ts-medium-smithy-typescript', 'ts-medium-umami', 'ts-medium-vite'})
sm8.update(sm8_rows('s-m-ts-synthesized-2026-10-10', {'js-medium-express'}))
assert len(sm8) == 6
RUST = ['poly-medium-napi-rs', 'rs-medium-aws-lambda-rust-runtime', 'rs-medium-axum', 'rs-medium-hyper', 'rs-medium-serde', 'rs-medium-serde-json', 'rs-medium-tokio', 'mr-rs-medium-serde-json',
        'rs-large-smithy-rs', 'poly-large-rspack', 'poly-very-large-deno', 'rs-very-large-sui']
seal = {}
for spike in ['s-m-sealing-typed-2026-10-09', 's-m-sealing-typed-remaining-2026-10-11']:
    for w in json.loads((SP / spike / 'checks.json').read_text())['workloads']:
        if w['id'] in RUST:
            assert w['id'] not in seal and w.get('outcome', 'SEALED-EQUIVALENT') == 'SEALED-EQUIVALENT'
            seal[w['id']] = dict(source=dict(path=f'docs/implementation/m3/spikes/{spike}/checks.json', sha256=sha(SP / spike / 'checks.json')), rows=w['regularRows'], totalBytes=w['bytes'],
                                 snapshotDescriptorBytes=w['snapshotDescriptorBytes'], bounds=w['bounds'], withinAllBounds=all(w['bounds'].values()),
                                 dependencySourcePart='owed by U-2 under D-2 (reported beside, not added to snapshot2 rows)')
assert sorted(seal) == sorted(RUST)
result = dict(standing='UNREVIEWED DESK RECORD U-4a UNDER S-M REPORT PLAN r2 (D-6, D-9); LEAD macOS PRELIMINARY; NO PLACEHOLDER FILLED; NO F OR T',
              plan='docs/implementation/m3/s-m-report-plan/PLAN-r2.md',
              SM8=dict(definition='D-6: per measured SM-2 run, the longest single public TypeScript compiler API call the SM-2 driver made, with its name; median and max over the 7 measured runs',
                       granularityLabel='driver call granularity: createProgram per configuration, getSemanticDiagnostics per file; a provider calling program-wide would block longer (label for the D law liveness floor)',
                       rows=sm8),
              SEffFirstTerm=dict(definition='D-9: SM-5 measured snapshot2-equivalent population per Rust workload (rows, total bytes, descriptor bytes, bound standing); no extrapolated ceiling; S_eff not filled',
                                 bounds=dict(rows=100000, descriptorBytes=4 * 1024 * 1024, totalBytes=8 * 1024 ** 3), rows=seal),
              placeholderFilled=False, FComputed=False, TComputed=False, outcomeRecorded=False, SEffFilled=False, SMComplete=False, LG1Met=False, effectiveL=False)
(H / 'u4a-desk-records.json').write_text(json.dumps(result, indent=1) + '\n')
for k, v in sm8.items(): print('SM-8', k, round(v['medianNanos'] / 1e6, 3), round(v['maxNanos'] / 1e6, 3), v['callNamesAtMedianAndMax'])
for k in RUST: v = seal[k]; print('SM-5', k, v['rows'], v['snapshotDescriptorBytes'], v['totalBytes'], v['withinAllBounds'])
