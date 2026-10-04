"""Read-only checks of contract successor SD-7. Run with python3 -I -B; it writes nothing. It reads the architecture
repository and, through read-only `git show`, the product lock and common-v4 schema at LOCK_REV. It never imports a
native model: both copies are parsed with `ast`.

1. Shape and pins: four parents (NE, SD-5's record, B-S9's two model copies), exactly the two line-1159 overrides,
   candidates equal the subject members other than the record.
2. The NE copy, recomputed independently from the lock: it is NE's effective text with exactly two hunks (difflib):
   one inserted line (item 25's row, directly after the NOT-SELECTED row) and one replaced line (SD-5's row). Every
   other line, including every other bound override's text, is carried byte for byte. The line map in
   copies-report.json is exact.
3. The conformed row: the class, code and detail cells equal SD-5's; the carrier cell differs only by M3-D r5's
   remedy phrase; EE-3b keeps only its capability form; EE-5a states the predicate (a), (b), (c) and admits an
   analyzer's own mounted root; no residue of the r3 wording remains.
4. The request-class row: five cells, request-rejected (2), REQUEST.UNSATISFIABLE, PROVIDER.NOT_SELECTED with subject
   excluded-form:<class>; item 25's three classes as M3-D r5 represents them; its quoted remedy equals the model's.
5. The remedy: ASCII and bounded; both original clauses kept word for word; PUBLIC_ROUTE_REMEDIES keeps every key
   and every other value in both copies; the two copies stay identical in that table; the only route registry key
   that reaches PROVIDER.NOT_SELECTED is the NOT-SELECTED cell's, so the widened string covers exactly two conditions.
6. Existing codes only, and the source law: every code-shaped token is an existing member; M3-D r5 (224b9228) carries
   SD-7's row, the remedy phrase, item 24's predicate and item 25's route as quoted."""
import ast, difflib, hashlib, json, re, subprocess
from pathlib import Path

A = Path(__file__).resolve().parents[6]
PRODUCT = Path('/Users/sb/code/opensip-ai/opensip')
LOCK_REV = '6190e66'
B = 'docs/implementation/m3/supervisor-d/'
D = B + 'sd-7/'
NE = 'docs/v2/contracts/product-v1/native-evidence.md'
COPY = D + 'contracts/native-evidence.md'
SD5 = B + 'sd-5/successor.json'
NEMS = ['docs/implementation/m3/config-discovery-b/b-s9/reference/native_evidence_model.py',
        'docs/implementation/m3/config-discovery-b/b-s9/reference/native_evidence_model.v2.py']
MD5 = B + 'PROPOSAL-r5.md'
NES = 'docs/coop/design-corrections/native/native-evidence.schemas.v2.json'
D9 = 'docs/coop/artifacts/d9-exit-contract.v1.14.json'
REG = 'docs/coop/design-corrections/public-detail-registry.v1.json'


def raw(p):
    return (A / p).read_bytes()


def pin(p):
    b = raw(p)
    return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


def show(path):
    return subprocess.run(['git', '-C', str(PRODUCT), 'show', '%s:%s' % (LOCK_REV, path)], check=True,
                          capture_output=True).stdout


def cells(row):
    return [c.strip() for c in row.split('|')[1:-1]]


checks = []

# 1. shape and pins
record = json.loads(raw(D + 'successor.json'))
subject = json.loads(raw(B + 'sd-7-subject.json'))
assert set(record) == {'schemaVersion', 'standing', 'parents', 'passageOverrides', 'candidates'}
assert sorted(r['path'] for r in record['parents']) == sorted([NE, SD5] + NEMS)
for row in record['parents'] + record['candidates'] + subject['files']:
    assert pin(row['path']) == row, row['path']
assert {r['path'] for r in record['candidates']} == {r['path'] for r in subject['files']} - {D + 'successor.json'}
assert [o['parent']['path'] for o in record['passageOverrides']] == NEMS
assert all(o['selector'] == {'line': 1159} for o in record['passageOverrides'])
for o in record['passageOverrides']:
    assert raw(o['parent']['path']).decode('utf-8').splitlines()[1158] == o['before']
checks.append('shape: 4 parents (NE, SD-5 record, 2 B-S9 model copies), 2 overrides (line 1159 of each copy), '
              'befores exact, candidates = subject - record')

# 2. the NE copy against an independent effective text
lock = json.loads(show('design-lock.json'))
ne = raw(NE).decode('utf-8').splitlines()
by_line = {}
for b in lock['contractSuccessors']:
    rec = json.loads(raw(b['record']['path']))
    assert not any(e['parent']['path'] == NE for e in rec.get('passageSupersessions', []))
    for e in rec.get('passageOverrides', []):
        if e['parent']['path'] == NE:
            by_line.setdefault(e['selector']['line'], set()).add(e['after'])
assert all(len(v) == 1 for v in by_line.values())
eff_lines = []
for i, line in enumerate(ne, 1):
    eff_lines.extend((next(iter(by_line[i])) if i in by_line else line).split('\n'))
copy_lines = raw(COPY).decode('utf-8').splitlines()
assert raw(COPY).endswith(b'\n') and b'\r' not in raw(COPY)
ops = [op for op in difflib.SequenceMatcher(None, eff_lines, copy_lines, autojunk=False).get_opcodes()
       if op[0] != 'equal']
assert len(ops) == 2, ops
(t1, i1, i2, j1, j2), (t2, k1, k2, l1, l2) = ops
assert t1 == 'insert' and i1 == i2 and j2 - j1 == 1, ops[0]
assert t2 == 'replace' and k2 - k1 == 1 and l2 - l1 == 1, ops[1]
request_row = copy_lines[j1]
old_row, new_row = eff_lines[k1], copy_lines[l1]
assert copy_lines[j1 - 1] == ne[3538] and ne[3538].startswith('| **unsatisfiable capability REQUEST**')
assert eff_lines[k1 - 1] == ne[3539] and old_row == next(iter(by_line[3540])).split('\n')[1]
sd5 = json.loads(raw(SD5))
assert old_row == sd5['passageOverrides'][0]['after'].split('\n')[1]
report = json.loads(raw(D + 'evidence/copies-report.json'))
assert report['copy'] == pin(COPY) and report['parent'] == pin(NE)
assert len(report['boundEntriesApplied']) == len(by_line)
at = 0
for start, end, copy_start in report['lineMap']['runs']:
    for k in range(end - start + 1):
        assert copy_lines[copy_start - 1 + k] == ne[start - 1 + k]
        at += 1
expanded = {e['rawLine'] for e in report['lineMap']['expanded']}
assert at + len(expanded) == len(ne) and expanded == set(by_line) | {3539}
checks.append('NE copy: effective NE at %s (%d bound overrides from %d records) plus exactly one inserted line '
              '(copy line %d, after the NOT-SELECTED row) and one replaced line (copy line %d, SD-5\'s row); line map '
              'exact over all %d raw lines' % (LOCK_REV, len(by_line),
                                               len({a['record']['path'] for a in report['boundEntriesApplied']}),
                                               j1 + 1, l1 + 1, len(ne)))

# 3. the conformed row
oc, nc = cells(old_row), cells(new_row)
assert len(oc) == len(nc) == 5 and oc[1:4] == nc[1:4] == ['', '`request-rejected` (2)', '`EXTENSION.ADMISSION_REJECTED`']
assert nc[4] == oc[4].replace('declare a project hook, root command or probe',
                              'claim a project hook, a reserved or additional root command, or a probe') != oc[4]
for gone in ('`commands` entry for role `analyzer`', 'a project hook, root command or contribution-granted probe',
             'declare a project hook, root command or probe'):
    assert gone not in new_row, gone
for kept in ('`EE-3b`, a claim of policy, persistence, rendering, termination or host-lifecycle authority (a capability '
             'outside the native capability matrix\'s provider capabilities)',
             '(a) a closure-only manifest (role `toolchain`, `stdlib`, `rust-dev-llvm` or `grammar`) that declares '
             '`commands` at all',
             '(b) an `analyzer` manifest whose command tree does not have exactly one entry without `parent`, or whose '
             'parentless entry\'s `name` differs from the manifest\'s `name`',
             '(c) a reserved root-command name among its root-namespace keys (its `name`, each of its `aliases` and, '
             'for `analyzer`, each alias of its parentless entry)',
             'An `analyzer` manifest\'s own name-bound mounted root, with any declared depth below it, is not a '
             'root-command claim', 'a command tree is never an `EE-3b` form',
             'keeps that route', 'conformed by contract successor SD-7 to law M3-D r5'):
    assert kept in new_row, kept
oc0, nc0 = oc[0], nc[0]
tail = 'No Plan, Coverage, Run or closure selection follows'
assert oc0[oc0.index(tail):] == nc0[nc0.index(tail):], 'the route-boundary sentences are carried'
assert oc0[:oc0.index('`EE-3b`')].replace('(contract successor SD-5 of law M3-D r3, item 24)',
    '(contract successor SD-5 of law M3-D r3, item 24; conformed by contract successor SD-7 to law M3-D r5, item 24, '
    'lead decision LD-R4-1)') == nc0[:nc0.index('`EE-3b`')]
checks.append('conformed row: class, code and detail cells equal SD-5\'s; carrier differs only by r5\'s remedy phrase; '
              'EE-3b capability form only; EE-5a predicate (a), (b), (c); mounted root admitted; route sentences carried')

# 4. the request-class row
rc = cells(request_row)
assert request_row.count('|') == 6 and rc[1:4] == ['', '`request-rejected` (2)', '`REQUEST.UNSATISFIABLE`']
assert rc[4].startswith('`PROVIDER.NOT_SELECTED`, carried as `domainDetail` with subject `excluded-form:<class>`')
assert 'no runId and no executionId' in rc[4] and 'every `ExcludedForm` goes to the operational record' in rc[4]
md5 = raw(MD5).decode('utf-8')
assert hashlib.sha256(raw(MD5)).hexdigest().startswith('224b9228')
for cls in ('a PlanIntent or admission request that requires an external discovery or public-lifecycle endpoint',
            'a PlanIntent requesting untrusted native or WASM admission',
            'a PlanIntent whose analysis branch requests network-granted analysis'):
    assert cls in md5 and cls in rc[0], cls
row_remedy = re.search(r'remedy "([^"]*)"', rc[4]).group(1)

# 5. the remedy
def table(text):
    for node in ast.parse(text).body:
        if isinstance(node, ast.Assign) and any(getattr(t, 'id', '') == 'PUBLIC_ROUTE_REMEDIES' for t in node.targets):
            return ast.literal_eval(node.value)


tables = []
for o in record['passageOverrides']:
    lines = raw(o['parent']['path']).decode('utf-8').splitlines()
    before_t = table('\n'.join(lines))
    lines[1158] = o['after']
    after_t = table('\n'.join(lines))
    assert set(before_t) == set(after_t) and all(before_t[k] == after_t[k] for k in before_t if k != 'PROVIDER.NOT_SELECTED')
    tables.append(after_t)
assert tables[0] == tables[1]
widened = tables[0]['PROVIDER.NOT_SELECTED']
assert widened == row_remedy and widened.isascii() and len(widened) <= 1024
assert widened.startswith('this capability is not selected for that language mode') and 'no promise is made for it' in widened
for form in ('external discovery or public-lifecycle endpoint', 'untrusted native or WASM admission',
             'network-granted analysis', 'restate the request without it'):
    assert form in widened, form
keys = json.loads(raw(NES))['x-opensip-public-route-registry']['keys']
reaching = [k for k, v in keys.items() if 'PROVIDER.NOT_SELECTED' in json.dumps(v)]
assert reaching == ['native.requested-capability-mode-not-selected'], reaching
checks.append('remedy (%d ASCII chars): both original clauses kept, the three request-class forms and the next step '
              'added; PUBLIC_ROUTE_REMEDIES otherwise unchanged and identical in both copies; NE row quotes it exactly; '
              'only %s otherwise reaches PROVIDER.NOT_SELECTED' % (len(widened), reaching[0]))

# 6. existing codes and the source law
d9 = json.loads(raw(D9))
reg = {r['code'] for r in json.loads(raw(REG))['records']}
product = set(json.loads(show('schemas/sources/common-v4.schema.json'))['$defs']['DomainDetailCode']['enum'])
known = reg | product | set(d9['codeVocabulary']['errorCodes']) | set(d9['codeVocabulary']['reasonCodes'])
tokens = set()
for r in (new_row, request_row):
    tokens |= set(re.findall(r'`([A-Z][A-Z0-9_-]*(?:\.[A-Z0-9_]+)+|[A-Z][A-Z0-9]*(?:-[A-Z0-9]+){2,})`', r))
assert tokens and tokens <= known, tokens - known
assert d9['codeMaps']['rejectionCauseToErrorCode']['unsatisfiable'] == 'REQUEST.UNSATISFIABLE'
for s in ('becomes "claim a project hook, a reserved or additional root command, or a probe"',
          '`request-rejected` 2, `REQUEST.UNSATISFIABLE`, with `domainDetail` `PROVIDER.NOT_SELECTED` and subject '
          '`excluded-form:<class>`',
          'When one request carries several forms, the subject names the first class in this table\'s order',
          'it declares `commands` at all, with any value',
          'An `analyzer` manifest whose tree has one parentless entry named for the component'):
    assert s in md5, s
checks.append('existing codes only %s; M3-D r5 (224b9228) carries SD-7\'s remedy phrase, item 24\'s predicate and item '
              '25\'s route as quoted' % sorted(tokens))
print(json.dumps({'passed': True, 'checks': checks}, indent=1, ensure_ascii=False))
