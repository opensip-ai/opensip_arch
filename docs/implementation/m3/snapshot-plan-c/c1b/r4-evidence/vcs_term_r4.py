"""C1b plan r4: the VCS term under r4's pricing (LD-C1B-6 as r4 amends it), and the bounds r9's 2x rule supports.

Design evidence for the plan, not C1b-1's model. It reads the bound census's cost constants from a clean export of the
product base (`costs` verifies the whole cost closure first) and the member model's `read_envelope`, and adds 1 + 64
repositories to r9's adopted (a)+(b') subtotal (RECORD-r9.md section 5; `option3_r2.output.json`). r4's pricing:
- HEAD at its exact symbolic form, `ref: ` + the target + LF, of length H; its read, parse and retained target at H;
- `refs` and the target's directories, D of them, each opened no-follow and judged as a directory on H's volume; their
  name bytes together are at most H (every one is a part of HEAD's target);
- the loose ref at its exact form, 40 hex + LF (41 bytes), its name part of the same target;
- `packed-refs` at INDEX_CAP (the Q1 ruling), read and parsed in full;
- each member's reach at MAX_DEPTH segments, at most LOGICAL_PATH_MAX name bytes in all;
- the VCS record's sealing allocation at its maximum (schema 3, 64 rows each at LOGICAL_PATH_MAX).
D* is the largest D for which r9's 2x rule holds in every component, and H* the largest H at D*. Neither is a product
constant: work past them is charged as performed and refuses WORK.BUDGET_EXHAUSTED at the ledger's caps (r9's
typed-refusal regime). Usage: vcs_term_r4.py <clean product export> <option3_r2.output.json>.
"""
import importlib.util
import json
import sys
from pathlib import Path


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


product, option3 = Path(sys.argv[1]), Path(sys.argv[2])
dc = load('discovery_census', product / 'tools/security/discovery_census.py')
dm = load('discovery_member_model', product / 'tools/security/discovery_member_model.py')
c = dc.costs(product)
r9 = json.loads(option3.read_bytes())['combinations']["a+b'"]
subtotal = tuple(max(r9[v]['subtotal'][k] for v in r9) for k in ('objects', 'edges', 'bytes'))
CAPS = (1 << 21, 1 << 24, 1 << 33)
LOGICAL_PATH_MAX = 4096  # IDS LogicalPath's longest spelling (the member rows and the reach's names)
LOOSE = 41  # gitrepository-layout: a loose ref holds the 40-hex object name and LF
KEYS = ('objects', 'edges', 'bytes')


class Term:
    def __init__(self):
        self.v = [0, 0, 0]

    def add(self, cost, times=1):
        for i in range(3):
            self.v[i] += cost[i] * times


def judge(t):  # judge_decided: the capture, then the premise check (its dearer branch)
    t.add(c['CAP'])
    t.add(c['FS'])


def judge_file(t):  # X2's file custody: H's volume, the judgment, the status
    t.add(c['FS'])
    judge(t)
    t.add(c['GIT_STATUS'])


def capped_file(t, length, cap):  # custody, then a read of a `length`-byte file under `cap`, and its parse
    judge_file(t)
    t.add(dm.read_envelope(c, length, cap)[:3])
    t.add((1, 1, min(length, cap)))


def owned(t, length):
    o, e = c['OWNED']
    t.add((o, e, length + c['RECORD']))


def repository(member, head, dirs):
    t = Term()
    o, e, b = c['OPEN_DIR']
    if member:  # item 6b's reach from W: open, device status, four marker lookups per segment
        t.add((o, e, b), c['MAX_DEPTH'])
        t.add((0, 0, LOGICAL_PATH_MAX))
        t.add(c['GIT_STATUS'], c['MAX_DEPTH'])
        for marker in ('.git', '.hg', '.svn', '.jj'):
            oo, oe, ob = c['OBS']
            t.add((oo, oe, ob + len(marker)), c['MAX_DEPTH'])
    t.add((o, e, b + 4))  # `.git` reopened, judged, sampled for the evidence recheck
    t.add(c['FS'])
    judge(t)
    t.add(c['GIT_STATUS'])
    ro, re_, rb = c['OPEN_REG_1']
    t.add((ro, re_, rb + 4))  # HEAD
    capped_file(t, head, c['INDEX_CAP'])
    owned(t, head)  # the retained target
    t.add((o, e, b), dirs)  # `refs` and the target's directories; their names are within HEAD's bytes
    t.add((0, 0, head))
    t.add(c['FS'], dirs)
    t.add(c['CAP'], dirs)
    t.add(c['FS'], dirs)
    t.add((ro, re_, rb))  # the loose ref (its name is within HEAD's bytes too)
    capped_file(t, LOOSE, c['INDEX_CAP'])
    t.add((ro, re_, rb + len('packed-refs')))
    capped_file(t, c['INDEX_CAP'], c['INDEX_CAP'])  # `packed-refs`, at its cap
    owned(t, 40)  # the retained commit
    return t.v


def total(head, dirs):
    t = Term()
    t.add(repository(False, head, dirs))
    t.add(repository(True, head, dirs), c['MAX_MEMBERS'])
    owned(t, c['MAX_MEMBERS'] * (LOGICAL_PATH_MAX + c['RECORD']))  # the VCS record at its maximum
    grand = tuple(subtotal[i] + t.v[i] for i in range(3))
    return dict(term=dict(zip(KEYS, t.v)), total=dict(zip(KEYS, grand)),
                twice=dict(zip(KEYS, (2 * g for g in grand))),
                holds=dict(zip(KEYS, (2 * grand[i] <= CAPS[i] for i in range(3)))))


def holds(head, dirs):
    return all(total(head, dirs)['holds'].values())


def shortest(dirs):  # `ref: refs/a/.../a` + LF: `refs` and dirs - 1 one-byte directories, then a one-byte leaf
    return len('ref: refs') + 2 * dirs + 1


# D*: the largest directory count with some admissible HEAD, at its shortest form.
low, high = 0, c['INDEX_CAP']
while low < high:
    mid = (low + high + 1) // 2
    if holds(shortest(mid), mid):
        low = mid
    else:
        high = mid - 1
dirs = low
# H*: the largest HEAD at D*, up to the read cap.
low, high = shortest(dirs), c['INDEX_CAP']
while low < high:
    mid = (low + high + 1) // 2
    if holds(mid, dirs):
        low = mid
    else:
        high = mid - 1
head = low
out = dict(
    standing=__doc__.splitlines()[0],
    subtotal=dict(zip(KEYS, subtotal)),
    caps=dict(zip(KEYS, CAPS)),
    derived=dict(refDirectories=dirs, headBytes=head),
    atDerived=total(head, dirs),
    onePastDirectories=total(shortest(dirs + 1), dirs + 1),
    onePastHead=total(head + 1, dirs),
    uniformIndexCapHead=total(c['INDEX_CAP'], dirs),
)
assert out['atDerived']['holds'] == dict(objects=True, edges=True, bytes=True)
assert not all(out['onePastDirectories']['holds'].values()) and not all(out['onePastHead']['holds'].values())
json.dump(out, sys.stdout, indent=1)
print()
