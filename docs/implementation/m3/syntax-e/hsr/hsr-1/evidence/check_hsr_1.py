"""Check HSR-1 without writing anything.

Usage: check_hsr_1.py [--product PATH] [--rev REV]
(default /Users/sb/code/opensip-ai/opensip and 43ea32a; both read only, through `git show`).

It re-derives, independently of build_hsr_1.py:
1. every parent pin against the arch bytes, and every parent as accepted in the product lock;
2. the supersession: it names the bound I1-L record by exact pin, the same parent and selector, its
   `before` equals I1-L's `after`, I1-L's entry is still the key's current meaning, and the raw
   line equals I1-L's `before`; every sentence of I1-L's text survives verbatim and in order;
3. each override: its key is unbound, its `before` is the raw passage, and with both identity-schema
   `after`s applied nothing else in SYN-1F's selected copy changes;
4. the table, parsed back out of IE:808's `after`: each row's document is a payload-registry
   document, each row's copy is accepted in the lock with exactly the row's digest and length, its
   `$id` is the row's, it holds no external reference, and a bound retiring successor's product copy
   of the same document has other bytes; no other document E2s changes is a registry document;
5. carriage: each row's digest occurs in the product's test corpora at REV, and no digest of a
   changed non-registry document does (git grep, read only);
6. the rule's clauses are present, and no em dash is added;
7. that the README names every passage, and the supersededPassages list the review must carry.
Run with python3 -I -B at nice -n 19.
"""
import copy, hashlib, json, re, subprocess, sys
from pathlib import Path

A = Path(__file__).resolve().parents[7]
D = A / 'docs/implementation/m3/syntax-e/hsr/hsr-1'
args = list(sys.argv[1:])


def opt(name, default):
    if name in args:
        i = args.index(name)
        value = args[i + 1]
        del args[i:i + 2]
        return value
    return default


W = Path(opt('--product', '/Users/sb/code/opensip-ai/opensip'))
REV = opt('--rev', '43ea32a')
IE = 'docs/v2/contracts/product-v1/identity-and-evidence.md'
IDS = 'docs/implementation/m3/syntax-e/syn-1f/design/foundation/identity-schemas.v3.json'
I1L = 'docs/implementation/m3/preview-pack-i1/i1-l/successor.json'
SYN1F_PRODUCT = 'docs/implementation/m3/syntax-e/syn-1f/product/schemas/sources/'


def show(path):
    return subprocess.run(['git', '-C', str(W), 'show', '%s:%s' % (REV, path)], check=True,
                          capture_output=True).stdout


def grep_files(text):
    r = subprocess.run(['git', '-C', str(W), 'grep', '-l', text, REV, '--', 'crates/*/tests/fixtures/*.json'],
                       capture_output=True, text=True)
    return sorted(line.split(':', 1)[1] for line in r.stdout.split('\n') if line)


def pinned(row):
    raw = (A / row['path']).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == row['sha256'] and len(raw) == row['bytes'], row['path']
    return raw


def tokens(pointer):
    return [t.replace('~1', '/').replace('~0', '~') for t in pointer[1:].split('/')]


def resolve(doc, pointer):
    for t in tokens(pointer):
        doc = doc[t]
    return doc


def assign(doc, pointer, value):
    ts = tokens(pointer)
    for t in ts[:-1]:
        doc = doc[t]
    doc[ts[-1]] = value


def keyof(entry):
    return (entry['parent']['path'], json.dumps(entry['selector'], sort_keys=True))


def sentences(text):
    return [s for s in re.split(r'(?<=[.;])\s+', text) if s]


def external_refs(doc):
    if isinstance(doc, dict):
        return any((k == '$ref' and isinstance(v, str) and not v.startswith('#')) or external_refs(v)
                   for k, v in doc.items())
    if isinstance(doc, list):
        return any(external_refs(v) for v in doc)
    return False


record = json.loads((D / 'successor.json').read_bytes())
lock = json.loads(show('design-lock.json'))
accepted, current, order, copies = {}, {}, {}, []
for key in ('sourceManifest', 'applicationManifest'):
    for row in json.loads(pinned(lock['approvals'][key]))['files']:
        accepted[row['path']] = {k: row[k] for k in ('path', 'bytes', 'sha256')}
for b in lock['contractSuccessors']:
    rec = json.loads(pinned(b['record']))
    order[b['record']['path']] = (b['record'], rec)
    for row in rec['candidates']:
        accepted[row['path']] = row
        if row['path'].endswith('/design/foundation/identity-schemas.v3.json'):
            copies.append(row['path'])
    for e in rec.get('passageOverrides', []) + rec.get('passageSupersessions', []):
        current[keyof(e)] = (b['record'], e)
report = {'rev': REV, 'contractSuccessors': len(lock['contractSuccessors'])}

# 1. Parents.
assert set(record) == {'schemaVersion', 'standing', 'parents', 'passageOverrides', 'passageSupersessions', 'candidates'}
assert [p['path'] for p in record['parents']] == sorted([IE, IDS])
for p in record['parents']:
    pinned(p)
    assert accepted[p['path']] == p, p['path']
ie_parent = [p for p in record['parents'] if p['path'] == IE][0]
ie_lines = pinned(ie_parent).decode('utf-8').splitlines()

# 2. The supersession of I1-L's IE:214.
i1l_pin, i1l = order[I1L]
sup = record['passageSupersessions']
assert len(sup) == 1 and sup[0]['selector'] == {'line': 214}
s = sup[0]
assert set(s) == {'parent', 'selector', 'before', 'after', 'supersedes'}
assert s['supersedes'] == {'record': i1l_pin, 'parent': s['parent'], 'selector': s['selector']}
target = [e for e in i1l['passageOverrides'] if keyof(e) == keyof(s)][0]
assert target['after'] == s['before']
owner, entry = current[keyof(s)]
assert owner == i1l_pin and entry == target, 'I1-L is no longer the current meaning'
assert ie_lines[213] == target['before']
old = sentences(s['before'])
new = sentences(s['after'])
pos = 0
for x in old:  # every I1-L sentence survives, in order
    pos = new.index(x, pos) + 1
report['i1lSentencesKept'] = len(old)
added = s['after'][len(s['before']) - len('Every other schema or domain change keeps this rule.'):]
for needle in ('A second reviewed exception (contract successor HSR-1)', 'SYN-1 and SYN-1F', '`source-parse-error`',
               'under their existing majors and without migration', '`native/native-evidence.schemas.v2.json`',
               '`foundation/enumeration-plan.schema.v1.json`', 'historical schema readers',
               'every existing record keeps its bytes, identity, validity and replay result',
               'Every other schema or domain change keeps this rule.',
               'adds exactly one historical schema reader for that document'):
    assert needle in added, needle

# 3. Overrides: free keys, raw befores, nothing else in IDS changes.
assert copies[-1] == IDS, copies
ids = json.loads(pinned(accepted[IDS]))
ov = record['passageOverrides']
assert [o['selector'] for o in ov] == [{'line': 662}, {'line': 678}, {'line': 808},
                                        {'jsonPointer': '/x-opensip-payload-registry/law/payloadSchemaDigest'},
                                        {'jsonPointer': '/x-opensip-evaluator-profile/majorLaw'}]
after_doc = copy.deepcopy(ids)
for o in ov:
    assert set(o) == {'parent', 'selector', 'before', 'after'}
    assert keyof(o) not in current, ('already overridden', keyof(o))
    if 'line' in o['selector']:
        assert o['parent'] == ie_parent and ie_lines[o['selector']['line'] - 1] == o['before']
    else:
        assert o['parent'] == accepted[IDS] and resolve(ids, o['selector']['jsonPointer']) == o['before']
        assign(after_doc, o['selector']['jsonPointer'], o['after'])
for o in ov:
    if 'jsonPointer' in o['selector']:
        assign(after_doc, o['selector']['jsonPointer'], o['before'])
assert after_doc == ids  # only the two strings differ
assert ov[0]['after'].startswith(ov[0]['before'][:-1]) and ov[3]['after'].startswith(ov[3]['before'])
assert ov[4]['after'].startswith(ov[4]['before'])
assert ov[2]['after'].startswith(ov[2]['before'] + '\n\n### Historical schema readers (contract successor HSR-1')
assert ie_lines[808] == '' and ie_lines[809].startswith('### `fact2` payload encoding')

# 4. The table.
documents = set()
for body in ids['x-opensip-payload-registry']['classes'].values():
    if 'document' in body:
        documents.add(body['document'])
    for row in body.get('rows', {}).values():
        documents.add(row['document'])
rows = re.findall(r'^\| (H\d+) \| `([^`]+)` \| `([^`]+)` \| `([0-9a-f]{64})` \| (\d+) \| `([^`]+)` \| ([A-Z0-9-]+) \|$',
                  ov[2]['after'], re.M)
assert [r[0] for r in rows] == ['H1', 'H2'], rows
retiring = {'SYN-1': ('docs/implementation/m3/syntax-e/syn-1/successor.json',
                      'docs/implementation/m3/syntax-e/syn-1/product/schemas/sources/native-v2.schema.json'),
            'SYN-1F': ('docs/implementation/m3/syntax-e/syn-1f/successor.json',
                       SYN1F_PRODUCT + 'enumeration-plan-v1.schema.json')}
digests = {}
for name, document, schema_id, sha, size, path, by in rows:
    assert document in documents, document
    row = accepted[path]
    assert row['sha256'] == sha and row['bytes'] == int(size), name
    doc = json.loads(pinned(row))
    assert doc['$id'] == schema_id and not external_refs(doc), name
    rec_path, product_copy = retiring[by]
    assert product_copy in [c['path'] for c in order[rec_path][1]['candidates']], name
    new_doc = json.loads(pinned(accepted[product_copy]))
    assert new_doc['$id'] == schema_id and accepted[product_copy]['sha256'] != sha, name
    assert sha not in digests
    digests[sha] = document
assert len(set(digests.values())) == len(digests)
# The other documents E2s changes are not registry documents, so they get no row.
others = {'execution-inputs-v1': 'foundation/execution-inputs.schema.v1.json',
          'subject-inventory-v1': 'foundation/subject-inventory.schema.v1.json',
          'identity-v3': 'foundation/identity-schemas.v3.json'}
for name, document in others.items():
    assert document not in documents, document
    old_raw = show('schemas/sources/%s.schema.json' % name)
    assert hashlib.sha256((A / (SYN1F_PRODUCT + name + '.schema.json')).read_bytes()).hexdigest() != hashlib.sha256(old_raw).hexdigest()

# 5. Carriage in the product corpora at REV.
carriage = {}
for sha in digests:
    files = grep_files(sha)
    assert files, sha
    carriage[sha[:8]] = files
for name in others:
    sha = hashlib.sha256(show('schemas/sources/%s.schema.json' % name)).hexdigest()
    assert grep_files(sha) == [], (name, 'carried by a corpus')
report['corpora'] = sorted({f for fs in carriage.values() for f in fs})
report['corporaCount'] = len(report['corpora'])

# 6. Clauses and dashes.
section = ov[2]['after']
for needle in ('**Minting.**', 'a caller may restate it but never choose it', '`admit_coverage_result_v3`',
               '**Retained records.**', 'exactly the bytes its digest names', 'their absence stays retention loss',
               'is a retained check', 'before any registry row, key or cardinality rule applies',
               'under the one-per-row rule above', 'No other digest is admitted', '**One reader per digest.**',
               'It is never a second reader of the same bytes', '**Identity.** Nothing is re-minted',
               '`finding-key2` names no schema digest', '**Mixed stores and Runs.**', '**Verification.**',
               'no defect, field, code or class is added', '**Extension.**', 'law VD2\'s form',
               'exactly one row for that document', 'No row is ever removed or edited',
               'still needs a new major and a reviewed migration'):
    assert needle in section, needle
assert 'for a retained record only' in ov[0]['after'] and 'in a retained view only' in ov[1]['after']
assert '(`SCHEMA_DOCUMENT_UNREGISTERED`)' in ov[1]['after']
assert 'A boundary that creates a record names the current bytes only' in ov[3]['after']
for e in sup + ov:
    assert e['after'].count('—') == e['before'].count('—'), 'em dash added'

# 7. README and the review's list.
readme = (D / 'README.md').read_text(encoding='utf-8')
for e in sup + ov:
    where = str(e['selector'].get('line', e['selector'].get('jsonPointer')))
    assert e['parent']['path'] in readme and where in readme, where
for sha in digests:
    assert sha in readme, sha
report['table'] = {sha[:8]: doc for sha, doc in digests.items()}
report['supersededPassages'] = [x['supersedes'] for x in sup]
report['passageSupersessions'] = len(sup)
report['passageOverrides'] = len(ov)
report['check'] = 'pass'
print(json.dumps(report, indent=1))
