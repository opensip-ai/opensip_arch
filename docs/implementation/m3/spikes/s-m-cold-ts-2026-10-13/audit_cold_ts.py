from pathlib import Path
import json, hashlib, statistics, difflib
# Read-only audit of U-5a (S-M report plan PLAN-r2, D-7): the Q0 §9.2 cold-reset series over the TS-row F and T
# components (SM-1, SM-5, SM-7, SM-2 incl. the express synthesized program, SM-9 at the six TS row sizes). Checks:
# each cold runner equals its accepted runner except the cold_reset import, one `_cr.reset(env,T)` as the first
# statement of the measured loop, `_cr.write(...)` before the lane is released, and (replay only) the TS-size
# restriction and redirected outputs; one reset record per measured child in order, each with OpenSIP state absent, a
# fresh empty per-run TMPDIR and a recorded page-cache state; medians and maxima recomputed. It reports the accepted
# warm medians beside the cold ones as information only, and computes no F, T or outcome. Writes cold-ts-checks.json.
W = Path(__file__).resolve().parent
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
JOBS = {'sm1': 'run_ready.py', 'sealing': 'run_set.py', 'transfer': 'run_transfer.py', 'cohort': 'run_cohort.py', 'synthesized': 'run_synthesized_ts.py', 'replay': 'run_sized_replay_r2.py'}
ALLOWED = {"import sys as _s;_s.path.insert(0,str(Path(__file__).resolve().parent.parent));import cold_reset as _cr"}
def diff_ok(name, accepted, cold):
    a = accepted.split('\n'); b = cold.split('\n'); added = []; removed = []
    for op in difflib.ndiff(a, b):
        if op.startswith('+ '): added.append(op[2:])
        elif op.startswith('- '): removed.append(op[2:])
    extra = [l for l in added if l.strip() not in ('_cr.reset(env,T)', '_cr.write(B)', '_cr.write(H)') and l not in ALLOWED]
    if name == 'replay':
        allowed_removed = {"for count in sorted(int(c) for c in packets['packets']):"}
        extra = [l for l in extra if 'sorted({141,193,678,936,1159,1381})' not in l and "sized-replay-results-cold-ts.json" not in l and "H/'evidence'/f'replay-" not in l]
        removed = [l for l in removed if l.strip() not in allowed_removed and "sized-replay-results-r2.json" not in l and "H/f'replay-r2-" not in l]
    return extra == [] and removed == [], dict(unexpectedAdded=extra, unexpectedRemoved=removed)
def series(name):
    d = W / name
    if name == 'replay':
        r = json.loads((d / 'sized-replay-results-cold-ts.json').read_text())
        out = []
        for s in r['sets']:
            runs = s['runs']; vals = [x['completeReplayNanos'] for x in runs if not x['warmup']]
            assert len(runs) == 10 and all(x['fullReplayPassed'] and x['findings'] == s['count'] for x in runs)
            out.append(dict(workload=f"replay-{s['count']}", runs=10, medianNanos=statistics.median(vals), maxNanos=max(vals)))
        return out
    r = json.loads((d / 'results.json').read_text())
    if name == 'sm1':
        runs = r['runs']; vals = [x['startToReadyNanos'] for x in runs if not x['warmup']]; assert len(runs) == 10
        return [dict(workload='SM-1', runs=10, medianNanos=statistics.median(vals), maxNanos=max(vals))]
    out = []
    for w in r['workloads']:
        runs = w['runs']; assert len(runs) == 10
        key = 'elapsedNanos' if name == 'sealing' else 'transferNanos' if name == 'transfer' and 'transferNanos' in runs[0] else 'wholeProcessNanos' if 'wholeProcessNanos' in runs[0] else None
        if key is None: key = [k for k in runs[0] if k.endswith('Nanos') and k not in ('startNanos',)][0]
        vals = [x[key] for x in runs if not x['warmup']]
        out.append(dict(workload=w['id'], runs=10, timedField=key, medianNanos=statistics.median(vals), maxNanos=max(vals)))
    return out
result = dict(standing='UNREVIEWED READONLY AUDIT OF U-5a COLD-RESET SERIES (TS-ROW COMPONENTS); LEAD macOS PRELIMINARY; NO F, T OR OUTCOME', components={})
for name, runner in JOBS.items():
    d = W / name; accepted = Path((d / 'ACCEPTED-RUNNER-SOURCE').read_text().strip())
    ok, why = diff_ok(name, accepted.read_text(), (d / runner).read_text())
    recs = json.loads((d / 'cold-reset-records.json').read_text())['records']
    rows = series(name); expected = sum(x['runs'] for x in rows)
    assert len(recs) == expected, (name, len(recs), expected)
    assert all(x['openSIPStateAbsent'] and x['runTMPDIREmpty'] and x['pageCache']['fileBackedPages'] is not None and x['pageCache']['pageSizeBytes'] > 0 for x in recs)
    assert len({x['runTMPDIR'] for x in recs}) == len(recs) and [x['index'] for x in recs] == list(range(len(recs)))
    result['components'][name] = dict(acceptedRunner=dict(path=str(accepted), sha256=sha(accepted)), coldRunner=dict(path=str(d / runner), sha256=sha(d / runner)), diffConfinedToColdInsertions=ok, diff=why,
                                      resetRecords=len(recs), oneResetPerChild=True, fileBackedPagesRange=[min(x['pageCache']['fileBackedPages'] for x in recs), max(x['pageCache']['fileBackedPages'] for x in recs)], series=rows)
interp = json.loads((W / 'cold-ts-interpretation.json').read_text())
for name in JOBS:
    row = interp['components'][name]; assert row['result']['sha256'] == sha(W / row['result']['path']) and row['resetLabel'].startswith('cold OpenSIP state, page cache recorded')
assert interp['components']['replay']['SM9LowerBoundOnly'] is False and interp['components']['replay']['lowerBoundEstablished'] is False
result.update(currentInterpretation=dict(path='cold-ts-interpretation.json', sha256=sha(W / 'cold-ts-interpretation.json')), replayInheritedLowerBoundFieldsObsolete=True,
              allDiffsConfined=all(c['diffConfinedToColdInsertions'] for c in result['components'].values()), label='cold OpenSIP state, page cache recorded (never claimed flushed); fresh empty per-run TMPDIR as the disposable cache; new process per run',
              FComputed=False, TComputed=False, outcomeRecorded=False, placeholderFilled=False, SMComplete=False, LG1Met=False, effectiveL=False)
(W / 'cold-ts-checks.json').write_text(json.dumps(result, indent=1) + '\n')
for n, c in result['components'].items():
    print(n, c['diffConfinedToColdInsertions'], c['resetRecords'], [(s['workload'], round(s['medianNanos'] / 1e6, 3)) for s in c['series']])
