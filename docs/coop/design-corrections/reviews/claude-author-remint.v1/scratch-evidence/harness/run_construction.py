"""Drive the four portable construction entry points into a fresh output root.

Every path is an argument. Nothing is read from a historical working directory.
"""
import json
import subprocess
import sys
import time
from pathlib import Path

ENV = '/tmp/opensip-architecture-review-env/bin/python'
R = Path('/private/tmp/opensip-design-corrections/claude-author-remint.v1')
PORT = R / 'scratch/portable'


def run(script, out, source, package, helpers, extra=()):
    cmd = [ENV, '-I', '-B', str(PORT / script),
           '--source', str(source), '--package', str(package), '--out', str(out)]
    if helpers:
        cmd += ['--helpers', str(helpers)]
    cmd += list(extra)
    t = time.time()
    p = subprocess.run(cmd, capture_output=True, text=True)
    return {'script': script, 'out': str(out), 'returncode': p.returncode,
            'seconds': round(time.time() - t, 1), 'stdout': p.stdout[-4000:],
            'stderr': p.stderr[-4000:], 'command': cmd}


def main():
    outroot = Path(sys.argv[1]).resolve()
    source = Path(sys.argv[2]).resolve()
    package = Path(sys.argv[3]).resolve()
    helpers = Path(sys.argv[4]).resolve() if len(sys.argv) > 4 and sys.argv[4] != '-' else None
    report = sys.argv[5] if len(sys.argv) > 5 else None

    rows = []
    rows.append(run('build-checkpoint3.py', outroot / 'a-checkpoint3', source, package, helpers))
    rows.append(run('build-normalized-examples6.py', outroot / 'b-normalized', source, package, helpers))
    rows.append(run('build-rust-selection-examples.py', outroot / 'c-rust-selection', source, package, helpers))
    rows.append(run('build-semantic-controls.py', outroot / 'd-controls', source, package, helpers,
                    extra=['--positive', str(outroot / 'a-checkpoint3' / 'checkpoint3')]))

    for r in rows:
        print('%-34s rc=%-3s %5ss' % (r['script'], r['returncode'], r['seconds']))
        if r['returncode'] != 0:
            print('   STDERR:', r['stderr'][-1500:])
        elif r['stdout'].strip():
            print('   ', r['stdout'].strip().splitlines()[0][:150])
    if report:
        json.dump({'standing': 'AUTHOR portable construction run; not acceptance.',
                   'outRoot': str(outroot), 'source': str(source), 'package': str(package),
                   'helpers': str(helpers) if helpers else None, 'steps': rows},
                  open(report, 'w'), indent=1)
    return 0 if all(r['returncode'] == 0 for r in rows) else 1


if __name__ == '__main__':
    raise SystemExit(main())
