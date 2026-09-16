"""(A) Run the native effects probe unconfined and under the frozen child_profile()."""
import importlib.util, json, shutil, socket, subprocess, threading, sys
from pathlib import Path

WORK = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('g', WORK / 'base/tools/generate_contracts.py')
G = importlib.util.module_from_spec(spec); spec.loader.exec_module(G)

root = WORK / 'direct-profile'
shutil.rmtree(root, ignore_errors=True)
for name in ('code', 'inputs', 'out', 'outside-dir'): (root / name).mkdir(parents=True)
outside = root / 'outside-secret'; outside.write_text('outside secret bytes\n')
exe = root / 'code-exe'; shutil.copyfile(WORK / 'bin/probe-effects', exe); exe.chmod(0o700)

listener = socket.socket(); listener.bind(('127.0.0.1', 0)); listener.listen(8)
port = listener.getsockname()[1]
accepted = []
threading.Thread(target=lambda: [accepted.append(listener.accept()) for _ in range(4)], daemon=True).start()

def run(label, confined):
    for p in (root / 'out').iterdir(): p.unlink()
    for p in (root / 'outside-dir').iterdir(): p.unlink()
    for p in (root / 'inputs').iterdir(): p.unlink()
    argv = [str(exe), 'effects', str(root / 'out'), str(outside), str(root / 'outside-dir'), str(root / 'inputs'), str(port)]
    if confined:
        profile = root / 'child-profile.sb'
        profile.write_text(G.child_profile(argv[0], [root / 'code', root / 'inputs'], [root / 'out']))
        argv = ['/usr/bin/sandbox-exec', '-f', str(profile), *argv]
    before = len(accepted)
    r = subprocess.run(argv, cwd=root / 'code', env={'PATH': '/usr/bin:/bin', 'HOME': str(root), 'LANG': 'C', 'LC_ALL': 'C', 'TZ': 'UTC'},
                       stdin=subprocess.DEVNULL, close_fds=True, capture_output=True, text=True, timeout=60)
    import time; time.sleep(0.3)
    results = dict(line.split('=', 1) for line in r.stderr.splitlines() if '=' in line)
    results['listenerAcceptedConnections'] = len(accepted) - before
    results['exit'] = r.returncode
    results['outsideDirAfter'] = sorted(p.name for p in (root / 'outside-dir').iterdir())
    results['inputsAfter'] = sorted(p.name for p in (root / 'inputs').iterdir())
    results['outsideSecretUnchanged'] = outside.read_text() == 'outside secret bytes\n'
    results['outEntries'] = sorted(p.name for p in (root / 'out').iterdir())
    return results

report = {'profile': G.child_profile(str(exe), [root / 'code', root / 'inputs'], [root / 'out']),
          'unconfined': run('unconfined', False), 'confined': run('confined', True)}
# Parent collector on the confined child's output: links/fifo must refuse.
try:
    G.collect_outputs(root / 'out', {'regular'}); report['collector'] = 'ACCEPTED'
except Exception as exc:
    report['collector'] = type(exc).__name__ + ': ' + str(exc)
report['outsideSecretUnchangedAfterCollection'] = outside.read_text() == 'outside secret bytes\n'
print(json.dumps(report, indent=1))
