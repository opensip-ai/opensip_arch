"""S01 — status of the interrupted v1 p04 successor rehearsal, from file metadata and retained outputs only (no process
listing, no writes to v1). Establishes (a) whether p04 can still be active (latest write time of any p04 output or kit file
versus now), (b) which phases completed, and (c) what the completed phases already measured."""
import hashlib, json, os, time

V1 = '/tmp/opensip-design-corrections/claude-consumer23-gap-assessment.v1'
RC1 = os.path.join(V1, 'receipts')
KIT = os.path.join(V1, 'disposable/kit36-successor')
OUT = '/tmp/opensip-design-corrections/claude-consumer23-gap-assessment.v2/receipts'
os.makedirs(OUT, exist_ok=True)
now = time.time()
iso = lambda t: time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(t))
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
R = {'nowUtc': iso(now)}
outs = {}
for d, _, fs in os.walk(RC1):
    for f in fs:
        p = os.path.join(d, f)
        if 'p04' in os.path.relpath(p, RC1):
            outs[os.path.relpath(p, RC1)] = {'mtimeUtc': iso(os.path.getmtime(p)), 'bytes': os.path.getsize(p), 'mtime': os.path.getmtime(p)}
R['p04Outputs'] = {k: {kk: vv for kk, vv in v.items() if kk != 'mtime'} for k, v in sorted(outs.items(), key=lambda kv: kv[1]['mtime'])}
kit_latest = max((os.path.getmtime(os.path.join(d, f)), os.path.relpath(os.path.join(d, f), KIT)) for d, _, fs in os.walk(KIT) for f in fs)
out_latest = max((v['mtime'], k) for k, v in outs.items())
R['latestP04OutputWrite'] = {'utc': iso(out_latest[0]), 'path': out_latest[1], 'secondsAgo': round(now - out_latest[0])}
R['latestKitWrite'] = {'utc': iso(kit_latest[0]), 'path': kit_latest[1], 'secondsAgo': round(now - kit_latest[0])}
rdir = os.path.join(RC1, 'p04_successor_rehearsal')
R['runnerReceiptDir'] = {'exists': os.path.isdir(rdir), 'contents': sorted(os.listdir(rdir)) if os.path.isdir(rdir) else None,
                         'dirMtimeUtc': iso(os.path.getmtime(rdir)) if os.path.isdir(rdir) else None}
R['summaryReceiptWritten'] = os.path.isfile(os.path.join(RC1, 'p04-successor-rehearsal.json'))
PHASES = {'patch': os.path.join(V1, 'successor-patch/successor-v23-gaps.patch'), 'check-query-projection': os.path.join(RC1, 'p04-kit-check-query-projection.stdout'),
          'native': os.path.join(RC1, 'p04-kit-native.stdout'), 'foundation-reference': os.path.join(RC1, 'p04-kit-foundation-reference.stdout'),
          'evaluator3-launcher': os.path.join(RC1, 'p04-kit-evaluator3-launcher.stdout'), 'integration': os.path.join(RC1, 'p04-kit-integration.stdout'),
          'security': os.path.join(RC1, 'p04-kit-security.stdout'), 'workflows-reference': os.path.join(RC1, 'p04-kit-workflows-reference.stdout')}
R['phaseOutputs'] = {k: os.path.isfile(v) for k, v in PHASES.items()}
R['evaluator3ChildrenStarted'] = sorted(f for f in os.listdir(os.path.join(RC1, 'p04-kit-evaluator3'))) if os.path.isdir(os.path.join(RC1, 'p04-kit-evaluator3')) else []
R['patchSha256'] = sha(PHASES['patch'])
try:
    q = json.load(open(os.path.join(RC1, 'p04-kit-check-query-projection.json')))
    NEW = ('closed-request-admission-leaves-absent-package-coordinate-to-section-2', 'response-graph-endpoint-still-requires-package-coordinate',
           'package-endpoint-without-coordinate-is-endpoint-ambiguous', 'empty-package-coordinate-is-params-malformed',
           'package-coordinate-on-file-endpoint-is-params-malformed', 'host-availability-unavailable-refuses-evidence-missing',
           'host-availability-corrupt-refuses-evidence-corrupt', 'host-availability-partial-does-not-refuse-by-itself')
    by = {c['id']: c for c in q['checks']}
    R['completedQueryControls'] = {'passed': q['passed'], 'count': q['count'], 'failedCount': q['failedCount'], 'new': {n: by.get(n, {}).get('ok') for n in NEW},
                                   'sha256': sha(os.path.join(RC1, 'p04-kit-check-query-projection.json'))}
except Exception as exc:  # noqa: BLE001
    R['completedQueryControls'] = {'error': str(exc)}
for name in ('check-query-projection', 'native', 'foundation-reference'):
    so = open(os.path.join(RC1, 'p04-kit-%s.stdout' % name)).read()
    se = open(os.path.join(RC1, 'p04-kit-%s.stderr' % name)).read()
    R.setdefault('completedSuiteTails', {})[name] = {'stdoutLastLine': (so.strip().splitlines() or [''])[-1][-300:], 'stderrBytes': len(se), 'stderrTail': se[-600:],
                                                   'stdoutSha256': hashlib.sha256(so.encode()).hexdigest()}
try:
    f = json.load(open(os.path.join(RC1, 'p04-kit-foundation.json')))
    R['completedFoundation'] = {k: f.get(k) for k in ('passed', 'sourcePinsValid', 'sourceFileCount', 'checksExecuted', 'timedOut')}
except Exception as exc:  # noqa: BLE001
    R['completedFoundation'] = {'error': str(exc)}
try:
    nr = json.load(open(os.path.join(KIT, 'docs/coop/design-corrections/native/native-evidence-report.v2.json')))
    res = nr.get('cases', {}).get('results') or []
    R['kitNativeReport'] = {'result': nr.get('result'), 'pins': nr.get('pins'), 'cases': len(res), 'failed': [c['id'] for c in res if not c.get('passed')],
                            'newCase': [c for c in res if c['id'] == 'run-termination-derives-the-d9-exit-contract-reason-code-for-each-deficiency']}
except Exception as exc:  # noqa: BLE001
    R['kitNativeReport'] = {'error': str(exc)}
atoms = os.path.join(RC1, 'p04-kit-evaluator3/atoms.stdout')
R['launcherAtomsStdoutTail'] = open(atoms).read()[-400:] if os.path.isfile(atoms) else None
print(json.dumps({k: v for k, v in R.items() if k not in ('p04Outputs',)}, indent=1, default=str))
json.dump(R, open(os.path.join(OUT, 's01-p04-status.json'), 'w'), indent=1, default=str)
print('wrote s01-p04-status.json')
