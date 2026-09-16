"""Assemble a package-layout view over the FRESH exports and run the four portable probes.

The probes take --package as the artifact root, so the view holds the new exports in the
package's directory layout plus the bundled transport they load. Nothing is written into the
input package or source.
"""
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ENV = '/tmp/opensip-architecture-review-env/bin/python'
R = Path('/private/tmp/opensip-design-corrections/claude-author-remint.v1')

LAYOUT = [('a-checkpoint3/checkpoint3', 'checkpoint3'),
          ('b-normalized/normalized-examples6', 'normalized-examples6'),
          ('c-rust-selection/rust-selection-examples1', 'rust-selection-examples1'),
          ('d-controls/semantic-controls1', 'semantic-controls1')]


def build_view(outroot, package, view):
    if view.exists():
        shutil.rmtree(view)
    view.mkdir(parents=True)
    for src, dst in LAYOUT:
        shutil.copytree(outroot / src, view / dst)
    shutil.copy2(package / 'check-export.v4.py', view / 'check-export.v4.py')
    return view


def run(name, script, args, evidence):
    t = time.time()
    p = subprocess.run([ENV, '-I', '-B', str(script)] + [str(x) for x in args],
                       capture_output=True, text=True)
    row = {'probe': name, 'returncode': p.returncode, 'seconds': round(time.time() - t, 1),
           'stdout': p.stdout[-3000:], 'stderr': p.stderr[-2000:],
           'command': [str(script)] + [str(x) for x in args]}
    print('%-26s rc=%-3s %5ss' % (name, p.returncode, row['seconds']))
    if p.returncode != 0:
        print('   STDERR:', p.stderr[-900:])
    return row


def main():
    outroot = Path(sys.argv[1]).resolve()
    source = Path(sys.argv[2]).resolve()
    package = Path(sys.argv[3]).resolve()
    ev = Path(sys.argv[4]).resolve()
    ev.mkdir(parents=True, exist_ok=True)
    view = build_view(outroot, package, ev / 'exports-view')

    rows = []
    rows.append(run('properties', package / 'check-author-properties.py',
                    ['--source', source, '--package', view, '--out', ev / 'author-properties.json'],
                    ev))
    rows.append(run('query', package / 'check-author-query.py',
                    ['--source', source, '--package', view, '--out', ev / 'query-checks1'], ev))
    if (ev / 'query-checks1').exists():
        rows.append(run('query-assessment', package / 'assess-author-query.py',
                        ['--input', ev / 'query-checks1', '--out', ev / 'query-assessment.json'], ev))
    rows.append(run('mixed-universe', package / 'probe-mixed-universe-view.py',
                    ['--source', source, '--package', view, '--out', ev / 'mixed-universe.json'], ev))

    json.dump({'standing': 'AUTHOR probes re-run over the freshly reminted exports.',
               'exportsView': str(view), 'source': str(source), 'probes': rows},
              open(ev / 'probe-run.json', 'w'), indent=1)
    return 0 if all(r['returncode'] == 0 for r in rows) else 1


if __name__ == '__main__':
    raise SystemExit(main())
