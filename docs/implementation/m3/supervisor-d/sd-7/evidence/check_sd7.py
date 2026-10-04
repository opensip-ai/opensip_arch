"""Read-only checks of contract successor SD-7 r2. Run with python3 -I -B; it writes nothing. It reads the
architecture repository and, through read-only `git show`, the product lock and common-v4 schema at LOCK_REV. It never
imports a native model: both copies are parsed with `ast`.

1. Shape and pins: three parents (NE and B-S9's two model copies); one passageSupersessions entry and three
   passageOverrides; candidates equal the subject members other than the record.
2. The supersession is law VD2's (rule items 1-2): its target is SD-5's record pin exactly as the lock binds it, at an
   earlier position; the same parent pin and selector; `before` equals SD-5's `after` byte for byte; it is the first
   link of NE:3540's chain (no bound supersession names it); and the fold-report's supersededPassages equals the
   record's supersedes list, which is what the review must carry (rule item 2.7).
3. The effective NE (law VD2 item 4), folded here independently from the lock: every bound entry on NE in lock order,
   then SD-7's two entries. It equals SD-7 r1's NE7 byte for byte, and the r1 snapshot's NE7 file.
4. The conformed row: class, code and detail cells equal SD-5's; the carrier cell differs only by M3-D r5's remedy
   phrase; EE-3b keeps only its capability form; EE-5a states the predicate (a), (b), (c); no r3 residue.
5. The request-class row: five cells, request-rejected (2), REQUEST.UNSATISFIABLE, PROVIDER.NOT_SELECTED, subject
   excluded-form:<class>, after the NOT-SELECTED row; the quoted remedy equals the model's.
6. The remedy: ASCII and bounded; both original clauses kept; PUBLIC_ROUTE_REMEDIES otherwise unchanged and identical in
   both copies; only the NOT-SELECTED cell's key otherwise reaches PROVIDER.NOT_SELECTED.
7. Existing codes only; M3-D r5 (224b9228) and VD2 r1 (2e4f70b4) carry the quoted texts."""
import ast, hashlib, json, re, subprocess
from pathlib import Path

A = Path(__file__).resolve().parents[6]
PRODUCT = Path('/Users/sb/code/opensip-ai/opensip')
LOCK_REV = '4c761e8'
B = 'docs/implementation/m3/supervisor-d/'
D = B + 'sd-7/'
NE = 'docs/v2/contracts/product-v1/native-evidence.md'
SD5 = B + 'sd-5/successor.json'
NEMS = ['docs/implementation/m3/config-discovery-b/b-s9/reference/native_evidence_model.py',
        'docs/implementation/m3/config-discovery-b/b-s9/reference/native_evidence_model.v2.py']
R1_NE7 = 'docs/implementation/m3/reviews/grok-sd-7-r2/r1-members/sd-7/contracts/native-evidence.md'
MD5 = B + 'PROPOSAL-r5.md'
VD2 = 'docs/implementation/m3/verify-design-vd2/PROPOSAL-r1.md'
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
assert set(record) == {'schemaVersion', 'standing', 'parents', 'passageOverrides', 'passageSupersessions', 'candidates'}
assert sorted(r['path'] for r in record['parents']) == sorted([NE] + NEMS)
for row in record['parents'] + record['candidates'] + subject['files']:
    assert pin(row['path']) == row, row['path']
assert {r['path'] for r in record['candidates']} == {r['path'] for r in subject['files']} - {D + 'successor.json'}
ne = raw(NE).decode('utf-8').splitlines()
[sup] = record['passageSupersessions']
ov = record['passageOverrides']
assert [(o['parent']['path'], o['selector']) for o in ov] == [(NE, {'line': 3539})] + [(p, {'line': 1159}) for p in NEMS]
for o in ov:
    assert o['before'] == raw(o['parent']['path']).decode('utf-8').splitlines()[o['selector']['line'] - 1]
    assert o['after'] != o['before'] and o['after']
assert set(sup) == {'parent', 'selector', 'before', 'after', 'supersedes'}
assert set(sup['supersedes']) == {'record', 'parent', 'selector'}
checks.append('shape: 3 parents (NE, 2 B-S9 model copies), 1 supersession (NE:3540), 3 overrides (NE:3539; line 1159 '
              'of each copy), befores exact, candidates = subject - record')

# 2. the supersession under law VD2
lock = json.loads(show('design-lock.json'))
order = [b['record']['path'] for b in lock['contractSuccessors']]
sd5_binding = lock['contractSuccessors'][order.index(SD5)]
assert sup['supersedes']['record'] == sd5_binding['record'] == pin(SD5)
sd5 = json.loads(raw(SD5))['passageOverrides'][0]
assert sup['supersedes']['parent'] == sup['parent'] == sd5['parent'] == pin(NE)
assert sup['supersedes']['selector'] == sup['selector'] == sd5['selector'] == {'line': 3540}
assert sup['before'] == sd5['after']
assert sup['after'].split('\n')[0] == ne[3539] and sup['after'].count('\n') == 1
for b in lock['contractSuccessors']:
    rec = json.loads(raw(b['record']['path']))
    for e in rec.get('passageSupersessions', []):
        assert e['parent']['path'] != NE, 'NE:3540 already has a bound link'
    for e in rec.get('passageOverrides', []):
        if e['parent']['path'] == NE:
            assert e['selector']['line'] != 3539, 'NE:3539 is already bound'
            if e['selector']['line'] == 3540:
                assert b['record']['path'] == SD5
report = json.loads(raw(D + 'evidence/fold-report.json'))
assert report['reviewSupersededPassages'] == [s['supersedes'] for s in record['passageSupersessions']]
checks.append('supersession: names SD-5\'s bound record pin (position %d of %d at %s), same parent and selector, '
              'before = SD-5\'s after, first link of NE:3540; review list = [SD-5 NE:3540]'
              % (order.index(SD5) + 1, len(order), LOCK_REV))

# 3. the effective NE (VD2 item 4), folded independently
text = {}
for b in lock['contractSuccessors']:
    rec = json.loads(raw(b['record']['path']))
    for e in rec.get('passageOverrides', []) + rec.get('passageSupersessions', []):
        if e['parent']['path'] == NE:
            text[e['selector']['line']] = e['after']
before_fold = ('\n'.join(text.get(i, l) for i, l in enumerate(ne, 1)) + '\n').encode('utf-8')
for e in ov[:1] + [sup]:
    text[e['selector']['line']] = e['after']
after_fold = ('\n'.join(text.get(i, l) for i, l in enumerate(ne, 1)) + '\n').encode('utf-8')
assert hashlib.sha256(before_fold).hexdigest() == report['effectiveBeforeSD7']['sha256']
assert hashlib.sha256(after_fold).hexdigest() == report['effectiveAfterSD7']['sha256'] == \
    '0dd155c2e2439b2223cdcfaec2ecad61c89bcf6a348f3be3c8f3350e9555ebd3' and len(after_fold) == 380848
assert raw(R1_NE7) == after_fold
eff = after_fold.decode('utf-8').splitlines()
checks.append('effective NE after SD-7 r2 = SD-7 r1\'s NE7 byte for byte (380848 bytes, 0dd155c2...), and equals the r1 '
              'snapshot file; before SD-7 it is %s...' % report['effectiveBeforeSD7']['sha256'][:8])

# 4. the conformed row
old_row = sd5['after'].split('\n')[1]
new_row = sup['after'].split('\n')[1]
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
             'root-command claim', 'a command tree is never an `EE-3b` form', 'keeps that route',
             'conformed by contract successor SD-7 to law M3-D r5'):
    assert kept in new_row, kept
tail = 'No Plan, Coverage, Run or closure selection follows'
assert oc[0][oc[0].index(tail):] == nc[0][nc[0].index(tail):]
checks.append('conformed row: cells equal SD-5\'s except r5\'s remedy phrase; EE-3b capability form only; EE-5a predicate '
              '(a), (b), (c); mounted root admitted; route sentences carried')

# 5. the request-class row
request_row = ov[0]['after'].split('\n')[1]
assert ov[0]['after'].split('\n')[0] == ne[3538] and ne[3538].startswith('| **unsatisfiable capability REQUEST**')
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
assert eff.index(request_row) == eff.index(ne[3538]) + 1 and eff.index(new_row) == eff.index(request_row) + 2
row_remedy = re.search(r'remedy "([^"]*)"', rc[4]).group(1)
checks.append('request-class row: request-rejected (2), REQUEST.UNSATISFIABLE, PROVIDER.NOT_SELECTED, subject '
              'excluded-form:<class>; effective order NOT-SELECTED row, request row, release row, conformed row')

# 6. the remedy
def table(src):
    for node in ast.parse(src).body:
        if isinstance(node, ast.Assign) and any(getattr(t, 'id', '') == 'PUBLIC_ROUTE_REMEDIES' for t in node.targets):
            return ast.literal_eval(node.value)


tables = []
for o in ov[1:]:
    lines = raw(o['parent']['path']).decode('utf-8').splitlines()
    before_t = table('\n'.join(lines))
    lines[1158] = o['after']
    after_t = table('\n'.join(lines))
    assert set(before_t) == set(after_t)
    assert all(before_t[k] == after_t[k] for k in before_t if k != 'PROVIDER.NOT_SELECTED')
    tables.append(after_t)
assert tables[0] == tables[1]
widened = tables[0]['PROVIDER.NOT_SELECTED']
assert widened == row_remedy and widened.isascii() and len(widened) <= 1024
assert widened.startswith('this capability is not selected for that language mode') and 'no promise is made for it' in widened
keys = json.loads(raw(NES))['x-opensip-public-route-registry']['keys']
assert [k for k, v in keys.items() if 'PROVIDER.NOT_SELECTED' in json.dumps(v)] == ['native.requested-capability-mode-not-selected']
checks.append('remedy (%d ASCII chars): both clauses kept; table otherwise unchanged, identical in both copies; quoted '
              'exactly in the request row' % len(widened))

# 7. existing codes and the source laws
d9 = json.loads(raw(D9))
reg = {r['code'] for r in json.loads(raw(REG))['records']}
product = set(json.loads(show('schemas/sources/common-v4.schema.json'))['$defs']['DomainDetailCode']['enum'])
known = reg | product | set(d9['codeVocabulary']['errorCodes']) | set(d9['codeVocabulary']['reasonCodes'])
tokens = set()
for r in (new_row, request_row):
    tokens |= set(re.findall(r'`([A-Z][A-Z0-9_-]*(?:\.[A-Z0-9_]+)+|[A-Z][A-Z0-9]*(?:-[A-Z0-9]+){2,})`', r))
assert tokens and tokens <= known, tokens - known
for s in ('becomes "claim a project hook, a reserved or additional root command, or a probe"',
          '`request-rejected` 2, `REQUEST.UNSATISFIABLE`, with `domainDetail` `PROVIDER.NOT_SELECTED` and subject '
          '`excluded-form:<class>`'):
    assert s in md5, s
vd2 = raw(VD2).decode('utf-8')
assert hashlib.sha256(raw(VD2)).hexdigest().startswith('2e4f70b4')
for s in ('- **`passageSupersessions`:** NE:3540, naming SD-5\'s record (5,805 bytes, `5e115818…`), NE and '
          '`{"line": 3540}`.',
          '- **`passageOverrides`:** NE:3539, a fresh key that no bound successor overrides.',
          '**Explicit review (lead decision).** The record\'s review document carries `supersededPassages`'):
    assert s in vd2, s
checks.append('existing codes only %s; M3-D r5 and VD2 r1 carry the quoted texts' % sorted(tokens))
print(json.dumps({'passed': True, 'checks': checks}, indent=1, ensure_ascii=False))
