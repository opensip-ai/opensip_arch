"""C1b-1 r1: the VCS term's feasibility under r9's caps (C1b plan r3, LD-C1B-6), before any model change.

Design evidence only. It reads the bound census's cost constants from a clean export of the C1b-1 base (`costs`
verifies the whole cost closure first) and the member model's `read_envelope`, prices one repository's VCS reads at
their dearer branches exactly as LD-C1B-4 and LD-C1B-6 state them, and adds 1 + 64 of them to r9's adopted (a)+(b')
subtotal (RECORD-r9.md section 5, `option3_r2.output.json`). The 2x rule is r9's: each component's total, doubled, must
not exceed its cap. Usage: vcs_term_feasibility.py <clean product export> <option3_r2.output.json>.
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
NAME_MAX = 255  # a segment's name bytes, at its dearest
LOGICAL_PATH_MAX = 4096  # the longest member LogicalPath (the VCS record's rows)


class Term:
    def __init__(self):
        self.v = [0, 0, 0]

    def add(self, cost, times=1):
        for i in range(3):
            self.v[i] += cost[i] * times


def open_dir(t, name_bytes):
    o, e, b = c['OPEN_DIR']
    t.add((o, e, b + name_bytes))


def open_regular(t, name_bytes):
    o, e, b = c['OPEN_REG_1']
    t.add((o, e, b + name_bytes))


def judge(t):  # judge_decided: the capture, then the premise check (its dearer branch)
    t.add(c['CAP'])
    t.add(c['FS'])


def judge_dir(t):  # Directory custody on H's volume: the filesystem sample, then the judgment
    t.add(c['FS'])
    judge(t)


def judge_file(t):  # X2's file custody (`judge_file`): H's volume, the judgment, the status
    t.add(c['FS'])
    judge(t)
    t.add(c['GIT_STATUS'])


def capped_file(t, name_bytes, cap):  # open, custody, a capped read at its dearer branch, the parse over the cap
    open_regular(t, name_bytes)
    judge_file(t)
    t.add(dm.read_envelope(c, cap + 1, cap)[:3])
    t.add((1, 1, cap))


def owned(t, length):
    o, e = c['OWNED']
    t.add((o, e, length + c['RECORD']))


def repository(member, head_cap, ref_dirs, loose_cap, packed_cap):
    t = Term()
    if member:  # item 6b's reach from W: each segment opened, sampled for its device, four markers looked up
        for _ in range(c['MAX_DEPTH']):
            open_dir(t, NAME_MAX)
            t.add(c['GIT_STATUS'])
            for marker in ('.git', '.hg', '.svn', '.jj'):
                o, e, b = c['OBS']
                t.add((o, e, b + len(marker)))
    open_dir(t, 4)  # `.git`, reopened, judged and sampled for the evidence recheck
    judge_dir(t)
    t.add(c['GIT_STATUS'])
    capped_file(t, 4, head_cap)  # HEAD
    for _ in range(ref_dirs):  # `refs` and every directory segment of the target
        open_dir(t, NAME_MAX)
        judge_dir(t)
    capped_file(t, NAME_MAX, loose_cap)  # the loose ref
    capped_file(t, 11, packed_cap)  # packed-refs
    owned(t, head_cap)  # the retained target name, at HEAD's cap
    owned(t, 40)  # the retained commit
    return t.v


def total(head_cap, ref_dirs, loose_cap, packed_cap):
    t = Term()
    t.add(repository(False, head_cap, ref_dirs, loose_cap, packed_cap))
    t.add(repository(True, head_cap, ref_dirs, loose_cap, packed_cap), c['MAX_MEMBERS'])
    owned(t, c['MAX_MEMBERS'] * (LOGICAL_PATH_MAX + 128))  # the VCS record's sealing allocation, at its maximum
    grand = tuple(subtotal[i] + t.v[i] for i in range(3))
    return {
        'term': dict(zip(('objects', 'edges', 'bytes'), t.v)),
        'total': dict(zip(('objects', 'edges', 'bytes'), grand)),
        'holds': dict(zip(('objects', 'edges', 'bytes'), (2 * grand[i] <= CAPS[i] for i in range(3)))),
    }


INDEX_CAP = c['INDEX_CAP']
cases = {}
# PLAN-r3 as accepted: every Git file at INDEX_CAP; the target's directories bounded only by HEAD's capped length.
cases['plan-r3-uniform-index-cap'] = total(INDEX_CAP, (INDEX_CAP - len('ref: \n') + 1) // 2, INDEX_CAP, INDEX_CAP)
# The closed forms' own lengths for HEAD and the loose ref, each at a candidate target-name bound.
for label, name_cap in (('path-max-1024', 1024), ('name-max-255', 255)):
    head = len('ref: ') + name_cap + 1
    cases['closed-forms-name-' + label] = total(head, (name_cap + 1) // 2, 41, INDEX_CAP)
# The member-depth reuse: at most 256 directories.
cases['closed-forms-dirs-256'] = total(len('ref: ') + 1024 + 1, 256, 41, INDEX_CAP)
# The largest directory count for which edges hold, with the closed forms for HEAD (PATH_MAX target) and the loose ref.
low, high = 0, INDEX_CAP
while low < high:
    mid = (low + high + 1) // 2
    if total(len('ref: ') + 1024 + 1, mid, 41, INDEX_CAP)['holds']['edges']:
        low = mid
    else:
        high = mid - 1
out = {
    'standing': __doc__.splitlines()[0],
    'subtotal': dict(zip(('objects', 'edges', 'bytes'), subtotal)),
    'caps': dict(zip(('objects', 'edges', 'bytes'), CAPS)),
    'cases': cases,
    'largestRefDirectoriesForEdges': low,
}
json.dump(out, sys.stdout, indent=1)
print()
