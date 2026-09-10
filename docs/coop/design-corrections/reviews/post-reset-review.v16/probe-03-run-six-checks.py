#!/usr/bin/env python3
"""Probe 03: execute all six recorded reference-check commands inside a named
disposable full exact copy, capture exits/stdout/stderr, and diff the copy
against the frozen manifest afterwards to record exactly what each command
wrote in-tree.

Usage: probe-03-run-six-checks.py <copy-name>
"""
import hashlib, json, os, subprocess, sys

MANIFEST = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v16.json'
OUT = '/tmp/opensip-design-corrections/post-reset-review.v16'
PY = '/tmp/opensip-architecture-review-env/bin/python'
copy_name = sys.argv[1]
COPY = os.path.join(OUT, copy_name)

def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()

rc = json.load(open(os.path.join(
    COPY, 'docs/coop/design-corrections/reviews/codex-post-reset.v1/final-reference.v16/reference-checks.json')))

results = []
for c in rc['commands']:
    argv = [PY if a == PY else a for a in c['command']]
    p = subprocess.run(argv, cwd=COPY, capture_output=True, text=True)
    stdout = p.stdout
    results.append({
        'name': c['name'],
        'argv': argv,
        'cwd': COPY,
        'exitCode': p.returncode,
        'declaredExitCode': c['exitCode'],
        'exitMatches': p.returncode == c['exitCode'],
        'stdout': stdout,
        'stdoutSha256': hashlib.sha256(stdout.encode()).hexdigest(),
        'stderr': p.stderr[-4000:],
        'stderrLen': len(p.stderr),
        'declaredLogSha256': sha256(os.path.join(
            COPY, 'docs/coop/design-corrections/reviews/codex-post-reset.v1/final-reference.v16', c['log'])),
        'declaredLogContent': open(os.path.join(
            COPY, 'docs/coop/design-corrections/reviews/codex-post-reset.v1/final-reference.v16', c['log'])).read(),
    })
    print(f"[{c['name']}] exit={p.returncode} (declared {c['exitCode']})")

# post-execution in-tree delta of the copy vs frozen manifest
m = json.load(open(MANIFEST))
declared = {r['path']: (r['sha256'], r['bytes']) for r in m['files']}
modified, removed, added = [], [], []
on_disk = set()
for dp, dn, fns in os.walk(COPY):
    for fn in fns:
        rel = os.path.relpath(os.path.join(dp, fn), COPY)
        on_disk.add(rel)
for path, (dig, nb) in declared.items():
    full = os.path.join(COPY, path)
    if not os.path.isfile(full):
        removed.append(path); continue
    got = sha256(full)
    if got != dig:
        modified.append({'path': path, 'frozenSha256': dig, 'afterRunSha256': got,
                         'frozenBytes': nb, 'afterRunBytes': os.stat(full).st_size})
added = sorted(on_disk - set(declared))

res = {
    'probe': 'probe-03-run-six-checks',
    'copyName': copy_name,
    'copyPath': COPY,
    'commandsExecuted': len(results),
    'allExitsMatchDeclared': all(r['exitMatches'] for r in results),
    'results': results,
    'inTreeDelta': {
        'modifiedCount': len(modified), 'modified': modified,
        'addedCount': len(added), 'added': added,
        'removedCount': len(removed), 'removed': removed,
    },
    'notProductQualification': True,
}
with open(os.path.join(OUT, f'probe-03-run-six-checks.{copy_name}.json'), 'w') as f:
    json.dump(res, f, indent=2, sort_keys=True)
print('in-tree modified:', len(modified), 'added:', len(added), 'removed:', len(removed))
for x in modified:
    print('  M', x['path'])
for x in added:
    print('  A', x)
