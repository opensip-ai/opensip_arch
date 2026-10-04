"""Check CR-1 without writing anything.

Usage: check_cr_1.py [--product PATH] [--rev REV]
(default /Users/sb/code/opensip-ai/opensip and 9c11c53; both read only, through `git show`).

It re-derives, independently of build_cr_1.py:
1. every parent pin against the arch bytes and the product lock's accepted set; every `before`
   against its parent; no selector already bound; every `after` only inserts;
2. that the DR-103 overrides change exactly the role field's `type` and `semantics` strings;
3. that the security-and-lifecycle table is word for word law M3-C r7 item 7's table, and that
   the successor copy's role enum is that table's roles in its order;
4. that the copy is the completed manifest schema (the architecture application's M.SCHEMA pin,
   equal to the product's security generation input at REV) with only /properties/role changed,
   in the parent's own serialization, and that the copies report and materialization map pin the
   files on disk;
5. that no existing negative role case (arch cases, product shape and semantic fixtures) uses a
   role of the widened enum;
6. that the README states every changed passage by path and selector.
Run with python3 -I -B at nice -n 19.
"""
import copy, difflib, hashlib, json, re, subprocess, sys
from pathlib import Path

A = Path(__file__).resolve().parents[6]
M = 'docs/implementation/m3/snapshot-plan-c/'
D = A / M / 'cr-1'
args = list(sys.argv[1:])


def opt(name, default):
    if name in args:
        i = args.index(name)
        value = args[i + 1]
        del args[i:i + 2]
        return value
    return default


W = Path(opt('--product', '/Users/sb/code/opensip-ai/opensip'))
REV = opt('--rev', '9c11c53')
SL = 'docs/v2/contracts/product-v1/security-and-lifecycle.md'
DR103 = 'docs/coop/artifacts/component-manifest-schemas.v11.json'
COMPLETED = 'docs/coop/completion/manifest-schema.completed.v1.json'
COPY = M + 'cr-1/completion/manifest-schema.completed.v1.json'


def show(path):
    return subprocess.run(['git', '-C', str(W), 'show', '%s:%s' % (REV, path)], check=True,
                          capture_output=True).stdout


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def tokens(pointer):
    return [t.replace('~1', '/').replace('~0', '~') for t in pointer[1:].split('/')]


def step(doc, t):
    return doc[int(t)] if isinstance(doc, list) else doc[t]


def resolve(doc, pointer):
    for t in tokens(pointer):
        doc = step(doc, t)
    return doc


def assign(doc, pointer, value):
    ts = tokens(pointer)
    for t in ts[:-1]:
        doc = step(doc, t)
    if isinstance(doc, list):
        doc[int(ts[-1])] = value
    else:
        doc[ts[-1]] = value


record = json.loads((D / 'successor.json').read_bytes())
lock = json.loads(show('design-lock.json'))
accepted, bound = {}, set()
for key in ('sourceManifest', 'applicationManifest'):
    for row in json.loads((A / lock['approvals'][key]['path']).read_bytes())['files']:
        accepted[row['path']] = row
for b in lock['contractSuccessors']:
    rec = json.loads((A / b['record']['path']).read_bytes())
    for row in rec['candidates'] + [b['record']]:
        accepted[row['path']] = row
    for e in rec.get('passageOverrides', []) + rec.get('passageSupersessions', []):
        bound.add((e['parent']['path'], json.dumps(e['selector'], sort_keys=True)))

# 1-2.
parents = {p['path']: p for p in record['parents']}
assert [p['path'] for p in record['parents']] == sorted(parents) == sorted([SL, DR103])
docs, texts = {}, {}
for path, p in parents.items():
    raw = (A / path).read_bytes()
    assert len(raw) == p['bytes'] and sha(raw) == p['sha256'], path
    assert accepted[path]['sha256'] == p['sha256'] and accepted[path]['bytes'] == p['bytes'], path
    try:
        docs[path] = json.loads(raw)
    except ValueError:
        texts[path] = raw.decode('utf-8').splitlines()
original = copy.deepcopy(docs[DR103])
for o in record['passageOverrides']:
    path, sel = o['parent']['path'], o['selector']
    key = (path, json.dumps(sel, sort_keys=True))
    assert parents[path] == o['parent'] and key not in bound, key
    if path in texts:
        assert set(sel) == {'line'} and texts[path][sel['line'] - 1] == o['before'], key
        texts[path][sel['line'] - 1] = o['after']
    else:
        assert set(sel) == {'jsonPointer'} and resolve(docs[path], sel['jsonPointer']) == o['before'], key
        assign(docs[path], sel['jsonPointer'], o['after'])
    ops = difflib.SequenceMatcher(None, o['before'], o['after'], autojunk=False).get_opcodes()
    assert all(tag in ('equal', 'insert') for tag, *_ in ops) and o['before'] != o['after'] and 'CR-1' in o['after'], key
masked = [copy.deepcopy(original), copy.deepcopy(docs[DR103])]
for doc in masked:
    assert resolve(doc, '/manifestSchema/fields/7/name') == 'role'
    for leaf in ('type', 'semantics'):
        assign(doc, '/manifestSchema/fields/7/' + leaf, None)
assert masked[0] == masked[1], 'DR-103 changes more than the role field strings'
for row in record['candidates']:
    raw = (A / row['path']).read_bytes()
    assert len(raw) == row['bytes'] and sha(raw) == row['sha256'] and row['path'] not in accepted, row['path']

# 3. The table.
law = (A / M / 'PROPOSAL-r7.md').read_text(encoding='utf-8')
law_table = re.findall(r'^    \| `([a-z-]+)` \| `([a-z-]+)` \|$', law, flags=re.M)
sl70 = [o for o in record['passageOverrides'] if o['parent']['path'] == SL][0]['after']
sl_table = re.findall(r'^\| `([a-z-]+)` \| `([a-z-]+)` \|$', sl70, flags=re.M)
assert sl_table == law_table and len(law_table) == 5, (sl_table, law_table)
copy_raw = (A / COPY).read_bytes()
copied = json.loads(copy_raw)
assert copied['properties']['role'] == {'enum': [r for r, _ in law_table]}
for needle in ['`evaluator`, `detector` and `adapter` are never manifest roles', '**closure-only**',
               '`capabilities` is `[]`', '`permissions` is `[]`', 'need not be executable', 'never executes',
               'mounts and dispatches none of its commands', '`closureKinds.byField`', 'CRC-1', 'EC1']:
    assert needle in sl70, needle

# 4. The copy, the report and the map.
parent_raw = (A / COMPLETED).read_bytes()
assert show('tools/security/inputs/manifest-schema.json') == parent_raw
application = json.loads((A / 'docs/coop/completion/architecture-application.v1.json').read_bytes())
found = []


def walk(value):
    if isinstance(value, dict):
        if 'M.SCHEMA' in value:
            found.append(value['M.SCHEMA'])
        for x in value.values():
            walk(x)
    elif isinstance(value, list):
        for x in value:
            walk(x)


walk(application)
assert len(found) == 1 and {'path': COMPLETED, 'pin': sha(parent_raw), 'selector': ''} in found[0]['sources']
parent = json.loads(parent_raw)
assert parent['properties']['role'] == {'const': 'analyzer'}
reverted = copy.deepcopy(copied)
reverted['properties']['role'] = {'const': 'analyzer'}
assert reverted == parent and list(reverted['properties']) == list(parent['properties'])
assert copy_raw == json.dumps(copied, indent=2).encode() + b'\n'
assert parent['$id'] == copied['$id']
report = json.loads((D / 'evidence/copies-report.json').read_bytes())
entry = report['copies'][0]
assert entry['parent'] == {'path': COMPLETED, 'bytes': len(parent_raw), 'sha256': sha(parent_raw)}
assert entry['copy'] == {'path': COPY, 'bytes': len(copy_raw), 'sha256': sha(copy_raw)}
mat = json.loads((D / 'materialization-map.json').read_bytes())
assert mat['files'] == [{'productPath': 'tools/security/inputs/manifest-schema.json', 'candidatePath': COPY,
                         'before': {'bytes': len(parent_raw), 'sha256': sha(parent_raw)},
                         'after': {'bytes': len(copy_raw), 'sha256': sha(copy_raw)}}]
for other in mat['alsoChangedByC2a']:
    raw = show(other['productPath'])
    assert other['base'] == {'path': other['productPath'], 'bytes': len(raw), 'sha256': sha(raw)}

# 5. The role-case audit, recomputed.
roles = set(copied['properties']['role']['enum'])
cases = json.loads((A / 'docs/coop/completion/manifest-cases.completed.v1.json').read_bytes())['cases']
arch_values = {op['value'] for c in cases for op in c['operations'] if op.get('op') == 'set' and op.get('path') == ['role']}
assert arch_values and not arch_values & roles
n = 0
for line in show('crates/security/tests/fixtures/manifest268-shape.ndjson').decode('utf-8').splitlines():
    q = json.loads(line)
    if "('role',)" in q['label'] or q['label'].endswith('/()/role'):
        value = q['value'].get('role')
        assert q['valid'] is False and not (isinstance(value, str) and value in roles), q['label']
        n += 1
assert n == report['roleCaseAudit']['productShapeFixture']['roleCases']

# 6. The README states every changed passage.
readme = (D / 'README.md').read_text(encoding='utf-8')
for o in record['passageOverrides']:
    sel = o['selector']
    assert o['parent']['path'] in readme, o['parent']['path']
    assert (('| %d |' % sel['line']) if 'line' in sel else ('`%s`' % sel['jsonPointer'])) in readme, sel
assert COPY.split('cr-1/')[1] in readme
print(json.dumps({'passed': True, 'rev': REV, 'overrides': len(record['passageOverrides']),
                  'table': law_table, 'copy': entry['copy'], 'productShapeRoleCases': n,
                  'archRoleValues': sorted(arch_values)}, indent=1))
