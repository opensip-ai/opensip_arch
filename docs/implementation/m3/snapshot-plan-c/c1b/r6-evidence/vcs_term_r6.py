"""C1b plan r6: the VCS term under r6's pricing (LD-C1B-6 as r4 to r6 amend it), and the bounds r9's 2x rule supports.

Design evidence for the plan, not C1b-1's model. It reads the bound census's cost constants from a clean export of the
product base (`costs` verifies the whole cost closure first) and the member model's `read_envelope`, and adds 1 + 64
repositories to the accepted cumulative subtotal: r9's adopted (a)+(b') subtotal (RECORD-r9.md section 5;
`option3_r2.output.json`) plus C1c-0's accepted retention term (`c1c-0-r2/evidence/c1c0-checks-r2/retention-cap-evidence.json`,
whose r9 subtotal must equal option3's). The pricing (r4, r5):
- HEAD at its exact symbolic form, `ref: ` + the target + LF, of length H; its read, parse and retained target at H;
- `refs` and the target's directories, D of them, each opened no-follow and judged as a directory on H's volume; their
  name bytes together are at most H (every one is a part of HEAD's target);
- the loose ref at its exact form, 40 hex + LF (41 bytes), its name part of the same target;
- `packed-refs` at INDEX_CAP (the Q1 ruling), read and parsed in full;
- each member's reach at MAX_DEPTH segments, (r6, C1BPLAN-R5-RF-1) with its names' UTF-8 bytes at their largest over
  LogicalPath's scalar bounds (`reach_name_bytes_max`), never its scalar count;
- (r5, C1BPLAN-R4-RF-1) the VCS record's sealing allocation at its maximum canonical length: schema 3's fixed syntax,
  64 member rows' fixed syntax and separators, and each path's maximum escaped payload under the canonical encoder's
  rules (`record_max`); one owned record, the encoder's only allocation (LD-C1B-6).
D* is the largest D for which r9's 2x rule holds in every component, and H* the largest H at D*. Neither is a product
constant: work past them is charged as performed and refuses WORK.BUDGET_EXHAUSTED at the ledger's caps (r9's
typed-refusal regime). Usage: vcs_term_r6.py <clean product export> <option3_r2.output.json> <retention-cap-evidence.json>.
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


product, option3, retention = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
dc = load('discovery_census', product / 'tools/security/discovery_census.py')
dm = load('discovery_member_model', product / 'tools/security/discovery_member_model.py')
c = dc.costs(product)
r9 = json.loads(option3.read_bytes())['combinations']["a+b'"]
r9_subtotal = tuple(max(r9[v]['subtotal'][k] for v in r9) for k in ('objects', 'edges', 'bytes'))
c1c0 = json.loads(retention.read_bytes())
assert tuple(c1c0['r9Subtotal'][k] for k in ('objects', 'edges', 'bytes')) == r9_subtotal and c1c0['allPass']
subtotal = tuple(c1c0['total'][k] for k in ('objects', 'edges', 'bytes'))
assert subtotal == tuple(r9_subtotal[i] + c1c0['retentionWorstCase'][k] for i, k in enumerate(('objects', 'edges', 'bytes')))
CAPS = (1 << 21, 1 << 24, 1 << 33)
LOGICAL_PATH_MAX = 4096  # IDS LogicalPath's longest spelling, in Unicode scalars (descriptors.rs: chars().count())
UTF8_MAX = 4  # bytes per Unicode scalar in UTF-8 (RFC 3629)
LOOSE = 41  # gitrepository-layout: a loose ref holds the 40-hex object name and LF
KEYS = ('objects', 'edges', 'bytes')
# r5: the canonical encoding (identity `canonical.rs`, `Encoder::string`; C1a3's `string_len`): a scalar's payload is
# 2 for `"` and `\\` and for each of \b \f \n \r \t, 6 for every other control below U+0020, else its UTF-8 length
# (at most 4). LogicalPath forbids `\\` and NUL and allows the rest. So no scalar's payload exceeds 6.
WIDEST_SCALAR = 6
SEGMENT_MAX = 255  # LogicalPath: each segment at most 255 scalars
SEPARATOR = 1  # `/`
TOP3 = len('{"commitId":null,"dirty":false,"kind":"none","members":[') + len('],"schemaVersion":3,"sourceInventoryDigest":"') + 64 + len('"}')
MEMBER = len('{"commitId":"') + 40 + len('","dirty":true,"kind":"git","path":"') + len('"}')
GIT2 = len('{"commitId":"') + 40 + len('","dirty":true,"kind":"git","schemaVersion":2,"sourceInventoryDigest":"') + 64 + len('"}')


def path_payload_max():
    """The largest e(P) over LogicalPaths: with s separators, at most min(LOGICAL_PATH_MAX - s, SEGMENT_MAX * (s + 1))
    other scalars, each at most WIDEST_SCALAR. Exhaustive over s."""
    return max((WIDEST_SCALAR * min(LOGICAL_PATH_MAX - s, SEGMENT_MAX * (s + 1)) + SEPARATOR * s, s)
               for s in range(LOGICAL_PATH_MAX))


PATH_PAYLOAD_MAX, PATH_SEPARATORS = path_payload_max()


def reach_name_bytes_max():
    """(r6) The largest total UTF-8 bytes of a member path's directory names, which `open_child_directory_cost` charges
    (`name.as_bytes().len()`): with s separators (s + 1 <= MAX_DEPTH segments), at most min(LOGICAL_PATH_MAX - s,
    SEGMENT_MAX * (s + 1)) other scalars, each at most UTF8_MAX bytes. Exhaustive over s."""
    return max((UTF8_MAX * min(LOGICAL_PATH_MAX - s, SEGMENT_MAX * (s + 1)), s)
               for s in range(min(LOGICAL_PATH_MAX, c['MAX_DEPTH'])))


REACH_NAME_BYTES_MAX, REACH_SEPARATORS = reach_name_bytes_max()


def record_max():
    """The largest VCS record: schema 3 with 64 members, each path at PATH_PAYLOAD_MAX; schema 2 git is fixed and smaller."""
    return max(TOP3 + c['MAX_MEMBERS'] * (MEMBER + PATH_PAYLOAD_MAX) + c['MAX_MEMBERS'] - 1, GIT2)


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
        t.add((0, 0, REACH_NAME_BYTES_MAX))  # (r6) the names' UTF-8 bytes, not their scalar count
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
    owned(t, record_max())  # (r5) the VCS record, one owned buffer at its maximum canonical length
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
    r9Subtotal=dict(zip(KEYS, r9_subtotal)),
    c1c0Retention=c1c0['retentionWorstCase'],
    subtotal=dict(zip(KEYS, subtotal)),
    caps=dict(zip(KEYS, CAPS)),
    record=dict(top3=TOP3, member=MEMBER, git2=GIT2, pathPayloadMax=PATH_PAYLOAD_MAX, pathSeparatorsAtMax=PATH_SEPARATORS,
                recordMax=record_max(), r4Allowance=c['MAX_MEMBERS'] * (LOGICAL_PATH_MAX + c['RECORD'])),
    reach=dict(nameBytesMax=REACH_NAME_BYTES_MAX, separatorsAtMax=REACH_SEPARATORS, r5Allowance=LOGICAL_PATH_MAX),
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
