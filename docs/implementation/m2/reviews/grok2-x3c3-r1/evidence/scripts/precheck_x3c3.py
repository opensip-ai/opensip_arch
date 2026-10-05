"""Pre-integration diagnostic for X3c-3's lead sets (X9 r17 §RC.6). NOT a
matrix pass. It is X9-6's precheck_x96.py with two changes, both marked.

The checker's two-target `check` requires every record's product.commit to
be the reviewed commit on a clean worktree (law X9 item 7; forbidden
substitute "a matrix pass on a dirty worktree"). X3c-3 is reviewed
uncommitted, so its lead sets record worktreeClean false and `check` refuses
them by design. This script applies every other condition of `check`, using
the checker's own functions unchanged: each target's sets are checked as
check-unit checks a set (base commit, worktreeClean false admitted), the
per-target repetition agreement, one clockEpoch, and the union census's
kill-set coverage in each repetition. It reports matrixPass false always.

Change 1 (LD-RC-6): check-unit's set check also refuses a killed point
outside the target's kill set, which `check` does not (it lists such points
in killedOutsideKillSet). Under §RC.3 F03's two `#41` rows kill
`x3c.object/file-barrier.{before,after}#41`, which storage's kill set no
longer names. Exactly that one refusal, for storage, with exactly those two
points, is tolerated and recorded; any other refusal stands.
Change 2: the report adds killedOutsideKillSet over the union, as `check`'s.

usage: precheck_x3c3.py <repository> <base commit> <storage required> <storage set 1> <storage set 2> <host required> <host set 1> <host set 2>
"""
import importlib.util
import json
from pathlib import Path
import sys

repo = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location('m', repo / 'tools/check_crash_matrix.py')
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)
commit = sys.argv[2]
targets = [('storage', *map(Path, sys.argv[3:6])), ('host', *map(Path, sys.argv[6:9]))]
# Change 1.
OUTSIDE = ['x3c.object/file-barrier.after#41', 'x3c.object/file-barrier.before#41']
tolerated = []
current = {'target': None}
real_require = M.require
def require(condition, message):
    if (not condition and current['target'] == 'storage'
            and message == 'killed points outside the kill set: ' + ', '.join(OUTSIDE)):
        tolerated.append(message)
        return
    real_require(condition, message)
M.require = require
scopes = M.registry(repo)
epochs, firsts, seconds, killed, report = set(), [], [], ([], []), {}
for name, required, one, two in targets:
    current['target'] = name
    rows, epoch = M.check_required(M.load(required))
    epochs.add(epoch)
    a, a_runs, a_killed = M.check_set(one, rows, commit, scopes, epoch, unit=True)
    b, b_runs, b_killed = M.check_set(two, rows, commit, scopes, epoch, unit=True)
    M.agree(a, a_runs, b, b_runs, rows)
    firsts.append(a['census']); seconds.append(b['census'])
    killed[0].extend(a_killed); killed[1].extend(b_killed)
    report[name] = {'runs': len(rows), 'censusPoints': len(a['census']['points']), 'killSet': len(a['killSet']),
                    'killedPoints': len(set(a_killed)), 'censusTrace': a['census']['trace'],
                    'worktreeClean': [a['product']['worktreeClean'], b['product']['worktreeClean']],
                    'normalizedSha256': {'-'.join(i): a_runs[i]['postState']['normalizedSha256'] for i in sorted(rows)}}
current['target'] = None
M.require = real_require
M.require(len(epochs) == 1, 'clockEpoch differs')
union = M.union_points(firsts, scopes)
M.require(union == M.union_points(seconds, scopes), 'repetitions disagree on the union census')
union_kill = M.kill_set(union)
for n, points in enumerate(killed, 1):
    uncovered = [p for p in union_kill if p not in set(points)]
    M.require(not uncovered, f'repetition {n}: uncovered: ' + ', '.join(uncovered))
print(json.dumps({'passed': True, 'diagnostic': 'pre-integration, not a matrix pass', 'baseCommit': commit,
                  'targets': report, 'runs': sum(r['runs'] for r in report.values()), 'unionCensusPoints': len(union),
                  'killSet': len(union_kill), 'killedPoints': len(set(killed[0])),
                  'killedOutsideKillSet': sorted(set(killed[0]) - set(union_kill)),
                  'toleratedStorageOutsideRefusals': len(tolerated), 'repetitionsAgree': True,
                  'limits': list(M.LIMITS), 'matrixPass': False}, sort_keys=True))
