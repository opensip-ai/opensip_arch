from pathlib import Path
import os, subprocess, tempfile, time, json, statistics
# U-2c SM-5 dependency-source part series: ds_probe.py per Rust entry, 3 warmups + 7 measured fresh children, parent and child
# priority 10, lane held for the whole set, private 0700 TMPDIR (the accepted sealing run_set.py recipe shape).
W = Path(__file__).resolve().parent; os.setpriority(os.PRIO_PROCESS, 0, 10); assert os.getpriority(os.PRIO_PROCESS, 0) == 10
PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'; D = Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T'); lane = D / 'opensip-lanes.lock'; owned = False
inputs = json.loads((W / 'u2c-inputs.json').read_text())['entries']; dest = W / 'sm5-ds-results-r1.json'; assert not dest.exists(); E = W / 'sm5-evidence'; E.mkdir()
while True:
    try: lane.mkdir(); owned = True; break
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-u2c-sm5-', dir=D)); T.chmod(0o700); env = dict(PATH='/opt/homebrew/bin:/usr/bin:/bin', TMPDIR=str(T)); env.update({k: os.environ[k] for k in ['HOME', 'LANG', 'LC_ALL', 'TZ'] if k in os.environ})
    results = []
    for e in inputs:
        ip = E / f"{e['slug']}.input.json"; ip.write_text(json.dumps(e) + '\n'); runs = []
        for n in range(10):
            out = E / f"{e['slug']}-{n}.stdout"; err = E / f"{e['slug']}-{n}.stderr"
            with out.open('wb') as o, err.open('wb') as x:
                child = subprocess.Popen([PY, '-I', '-B', str(W / 'ds_probe.py'), str(ip)], cwd=T, env=env, stdout=o, stderr=x); cn = os.getpriority(os.PRIO_PROCESS, child.pid); assert cn == 10
                _, status, usage = os.wait4(child.pid, 0); code = os.waitstatus_to_exitcode(status)
            assert code == 0, err.read_text(); r = json.loads(out.read_text()); assert r['allDigestsAndIdentitiesMatched'] and r['files'] == e['files'] and r['bytes'] == e['bytes']
            runs.append(dict(ordinal=n, warmup=n < 3, elapsedNanos=r['elapsedNanos'], observedChildNiceness=cn, rssNative=int(usage.ru_maxrss), rssUnit='bytes'))
        vals = [r['elapsedNanos'] for r in runs if not r['warmup']]
        results.append(dict(entry=e['entry'], slug=e['slug'], dependencySourceSetId=e['dependencySourceSetId'], packages=len(e['packages']), files=e['files'], bytes=e['bytes'], runs=runs, medianNanos=statistics.median(vals), maxNanos=max(vals)))
        print(e['entry'], round(statistics.median(vals) / 1e6, 3), flush=True)
        dest.write_text(json.dumps(dict(standing='UNREVIEWED U-2c SM-5 DEPENDENCY-SOURCE PART SERIES (D-2); LEAD macOS PRELIMINARY; GENERATED-LOCK SETS ARE SIZING STAND-INS', results=results, TMPDIR=str(T), laneHeldForEntireSet=True, nice=10, SM5ValueRecorded=False), indent=1) + '\n')
finally:
    if owned: lane.rmdir()
    assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
