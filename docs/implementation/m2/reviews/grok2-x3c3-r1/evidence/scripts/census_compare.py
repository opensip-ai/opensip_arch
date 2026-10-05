"""X3c-3's census check against X9 r17 §RC.3, before transcription.

Compares the census-only run's storage and host censuses with C's accepted
censuses (crash-matrix-x9/evidence/3d2d5b5.../{storage,host}/matrix.json),
by the checker's own functions: point counts, occurrence changes, each
target's and the union's kill set, the kill-set points added and removed,
and whether the first four storage parts' traces (commit, recover, sweep,
refused end) are C's, point and event for point and event.

usage: census_compare.py <repository> <C evidence dir> <storage census dir> <host census dir>
"""
import importlib.util
import json
import sys
from pathlib import Path

repo, evidence, storage, host = map(Path, sys.argv[1:5])
spec = importlib.util.spec_from_file_location('m', repo / 'tools/check_crash_matrix.py')
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)
scopes = M.registry(repo)
c_storage = M.load(evidence / 'storage/matrix.json')['census']
c_host = M.load(evidence / 'host/matrix.json')['census']
n_storage = M.load(storage / 'census.json')
n_host = M.load(host / 'census.json')

def points(census):
    return {p['name']: p for p in census['points']}

def diff(old, new):
    o, n = points(old), points(new)
    return {
        'added': sorted(set(n) - set(o)),
        'removed': sorted(set(o) - set(n)),
        'changed': {k: [o[k]['occurrences'], n[k]['occurrences']] for k in sorted(set(o) & set(n))
                    if o[k]['occurrences'] != n[k]['occurrences'] or o[k]['durability'] != n[k]['durability']},
    }

def kill(points_list):
    return M.kill_set(points_list)

c_union = M.union_points([c_storage, c_host], scopes)
n_union = M.union_points([n_storage, n_host], scopes)
c_union_kill, n_union_kill = kill(c_union), kill(n_union)

def trace_shape(path, parts):
    out = {}
    for line in Path(path).read_text().splitlines():
        part, thread, seq, point, event, *_ = line.split('|')
        if part in parts:
            out.setdefault(part, []).append(f'{point}|{event}')
    return out

first_four = ('commit', 'recover', 'sweep', 'refused-end')
c_shape = trace_shape(evidence / 'storage/census-trace.txt', first_four)
n_shape = trace_shape(storage / 'census-trace.txt', first_four)
parts_in_new = []
for line in (storage / 'census-trace.txt').read_text().splitlines():
    p = line.split('|', 1)[0]
    if not parts_in_new or parts_in_new[-1] != p:
        parts_in_new.append(p)
result = {
    'storage': {'censusPoints': [len(c_storage['points']), len(n_storage['points'])],
                'killSet': [len(kill(c_storage['points'])), len(kill(n_storage['points']))],
                'trace': [c_storage['trace'], n_storage['trace']],
                'diff': diff(c_storage, n_storage),
                'killSetAdded': sorted(set(kill(n_storage['points'])) - set(kill(c_storage['points']))),
                'killSetRemoved': sorted(set(kill(c_storage['points'])) - set(kill(n_storage['points'])))},
    'host': {'censusPoints': [len(c_host['points']), len(n_host['points'])],
             'equal': c_host == n_host, 'diff': diff(c_host, n_host)},
    'union': {'censusPoints': [len(c_union), len(n_union)],
              'killSet': [len(c_union_kill), len(n_union_kill)],
              'killSetAdded': sorted(set(n_union_kill) - set(c_union_kill)),
              'killSetRemoved': sorted(set(c_union_kill) - set(n_union_kill))},
    'storagePartsInOrder': parts_in_new,
    'firstFourPartsTraceShapeEqualToC': {p: c_shape.get(p) == n_shape.get(p) for p in first_four},
}
print(json.dumps(result, indent=1, sort_keys=True))
