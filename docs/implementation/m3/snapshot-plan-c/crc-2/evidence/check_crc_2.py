"""Check CRC-2 without writing anything.

Usage: check_crc_2.py [--product PATH] [--rev REV]
(default /Users/sb/code/opensip-ai/opensip and 21e428d; both read only, through `git show`).

It re-derives, independently of build_crc_2.py:
1. every parent pin against the arch bytes, and every parent as accepted in the product lock;
2. each supersession: it names the bound CRC-1 record by exact pin, the same parent and selector,
   its `before` equals CRC-1's `after`, CRC-1's entry is still the key's current meaning (no later
   record supersedes it), and the selector resolves in the raw parent;
3. each override: its parent is SYN-1F's copy, the last complete identity-schema copy in the
   chain; no bound record overrides the key; `before` is the string at the pointer, and equals
   CRC-1's `after` on I1-L's copy; with both `after`s applied, nothing else in the document changes;
4. what changed: every removed span lies inside the sentences CRC-2 rewrites, and every other
   sentence of each `before` survives verbatim;
5. the rule: use (3)'s relations, four fields and exclusions are named, "exactly two" is gone,
   and the three membership statements (IE:285, IE:1377, selectionLaw) carry the same clause;
6. law agreement: M3-C r8's item 9 (the live PROPOSAL.md) names the same relations and fields;
7. that the README names every passage, and the supersededPassages list the review must carry.
Run with python3 -I -B at nice -n 19.
"""
import copy, difflib, hashlib, json, re, subprocess, sys
from pathlib import Path

A = Path(__file__).resolve().parents[6]
M = A / 'docs/implementation/m3/snapshot-plan-c'
D = M / 'crc-2'
args = list(sys.argv[1:])


def opt(name, default):
    if name in args:
        i = args.index(name)
        value = args[i + 1]
        del args[i:i + 2]
        return value
    return default


W = Path(opt('--product', '/Users/sb/code/opensip-ai/opensip'))
REV = opt('--rev', '21e428d')
IE = 'docs/v2/contracts/product-v1/identity-and-evidence.md'
IDS = 'docs/implementation/m3/syntax-e/syn-1f/design/foundation/identity-schemas.v3.json'
IDS_I1L = 'docs/implementation/m3/preview-pack-i1/i1-l/design/foundation/identity-schemas.v3.json'
CRC1 = 'docs/implementation/m3/snapshot-plan-c/crc-1/successor.json'


def show(path):
    return subprocess.run(['git', '-C', str(W), 'show', '%s:%s' % (REV, path)], check=True,
                          capture_output=True).stdout


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


record = json.loads((D / 'successor.json').read_bytes())
lock = json.loads(show('design-lock.json'))
accepted, current, order, copies = {}, {}, [], []
for key in ('sourceManifest', 'applicationManifest'):
    for row in json.loads(pinned(lock['approvals'][key]))['files']:
        accepted[row['path']] = {k: row[k] for k in ('path', 'bytes', 'sha256')}
for b in lock['contractSuccessors']:
    rec = json.loads(pinned(b['record']))
    order.append(b['record'])
    for row in rec['candidates']:
        accepted[row['path']] = row
        if row['path'].endswith('/design/foundation/identity-schemas.v3.json'):
            copies.append(row['path'])
    for e in rec.get('passageOverrides', []) + rec.get('passageSupersessions', []):
        current[keyof(e)] = (b['record'], e)
crc1_pin = [p for p in order if p['path'] == CRC1][0]
crc1 = json.loads(pinned(crc1_pin))
crc1_entries = {keyof(e): e for e in crc1['passageOverrides']}
report = {'rev': REV, 'contractSuccessors': len(order)}

# 1. Parents.
assert set(record) == {'schemaVersion', 'standing', 'parents', 'passageOverrides', 'passageSupersessions', 'candidates'}
assert [p['path'] for p in record['parents']] == sorted([IE, IDS])
for p in record['parents']:
    pinned(p)
    assert accepted[p['path']] == p, p['path']

# 2. Supersessions.
ie_lines = pinned(record['parents'][[p['path'] for p in record['parents']].index(IE)]).decode('utf-8').splitlines()
sup = record['passageSupersessions']
assert [s['selector'] for s in sup] == [{'line': 285}, {'line': 1377}]
for s in sup:
    assert set(s) == {'parent', 'selector', 'before', 'after', 'supersedes'}
    assert s['supersedes'] == {'record': crc1_pin, 'parent': s['parent'], 'selector': s['selector']}
    target = crc1_entries[keyof(s)]
    assert target['parent'] == s['parent'] and target['after'] == s['before']
    owner, entry = current[keyof(s)]
    assert owner == crc1_pin and entry == target, 'CRC-1 is no longer the current meaning'
    assert ie_lines[s['selector']['line'] - 1] == target['before']
    assert s['after'] != s['before']

# 3. Overrides.
assert copies[-1] == IDS, copies
ids_raw = pinned(accepted[IDS])
ids = json.loads(ids_raw)
ov = record['passageOverrides']
assert [o['selector'] for o in ov] == [{'jsonPointer': '/x-opensip-digest-domains/closureKinds/note'},
                                        {'jsonPointer': '/x-opensip-digest-domains/closureMembership/selectionLaw'}]
after_doc = copy.deepcopy(ids)
for o in ov:
    assert set(o) == {'parent', 'selector', 'before', 'after'} and o['parent'] == accepted[IDS]
    assert keyof(o) not in current, 'already overridden'
    assert resolve(ids, o['selector']['jsonPointer']) == o['before']
    carried = crc1_entries[(IDS_I1L, json.dumps(o['selector'], sort_keys=True))]
    assert carried['after'] == o['before']
    assign(after_doc, o['selector']['jsonPointer'], o['after'])
for o in ov:
    assign(after_doc, o['selector']['jsonPointer'], o['before'])
assert after_doc == ids  # only the two strings differ

# 4. What changed: removed spans lie in the rewritten sentences; other sentences survive.
REWRITTEN = {
    285: ['(contract successor CRC-1, 2026-10-04)', 'has exactly two admitted uses',
          '`CandidateProducerResultV1.producerClosure`. It is a `plan.semanticClosures` member exactly when the Plan'
          ' selects a syntax universe, and is never selected otherwise, not even explicitly. It is never the producer'
          ' of a TypeScript or Rust record.',
          'closure keeps kind `grammar` and is never a producer, and a TypeScript or Rust provider closure is never the'
          ' producer of a syntax record.',
          'registers each syntax stage\'s output schema'],
    1377: ['(contract successor CRC-1, above)', 'syntax.v2` universe,'],
    'note': ['exactly two uses under one identity: the import.producerClosure of a dependency or prepared import, and',
             'syntax.v2 identity; it never produces a TypeScript or Rust record.'],
    'selectionLaw': ['(contract successor CRC-1):', 'syntax.v2 universe,'],
}


def removed(before, after):
    out = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, before, after, autojunk=False).get_opcodes():
        if tag in ('replace', 'delete'):
            out.append((i1, i2))
    return out


def sentences(text):
    """(start, end) spans of sentences, split after '.' or ';' followed by whitespace."""
    out, start = [], 0
    for m in re.finditer(r'(?<=[.;])\s+', text):
        out.append((start, m.start()))
        start = m.end()
    out.append((start, len(text)))
    return [(a, b) for a, b in out if b > a]


for name, entry in ((285, sup[0]), (1377, sup[1]), ('note', ov[0]), ('selectionLaw', ov[1])):
    spans = [entry['before'].index(f) for f in REWRITTEN[name]]
    windows = [(s, s + len(f)) for s, f in zip(spans, REWRITTEN[name])]
    for i1, i2 in removed(entry['before'], entry['after']):
        assert any(a <= i1 and i2 <= b for a, b in windows), (name, entry['before'][i1:i2])
    kept = [entry['before'][a:b] for a, b in sentences(entry['before'])
            if not any(a < wb and wa < b for wa, wb in windows)]
    for x in kept:
        assert x in entry['after'], (name, x[:80])
    report.setdefault('sentencesKept', {})[str(name)] = len(kept)

# 5. The rule.
ie285, ie1377 = sup[0]['after'], sup[1]['after']
note, law = ov[0]['after'], ov[1]['after']
for text in (ie285, note):
    assert 'exactly two' not in text and ('exactly three admitted uses' in text or 'exactly three uses' in text)
    for rel in ('file@enumerated', 'package@manifest-declared', 'vcs-change@vcs-reported'):
        assert rel in text, rel
    for field in ('enumerator.closureId', 'stage-spec.producerClosure', 'view.producerClosure',
                  'fact.producerClosure', 'subject-scope.enumeratorClosure'):
        assert text.count(field) >= 2, field  # in use (2) and again in use (3)
    assert 'CRC-2' in text
assert 'available or not' in ie285
for phrase in ('a record of another relation', 'a record a language provider returned',
               'the enumerator of a binding that owes a symbol inventory', 'Apart from use (3)',
               'no language provider closure is the producer or enumerator of an'):
    assert phrase in ie285, phrase
assert 'Apart from that third use' in note and 'no language provider closure produces or enumerates' in note
for text in (ie285, ie1377):
    assert 'exactly when the Plan selects a' in text and 'or requests an `inventory` cell, and is never selected otherwise, not even explicitly' in text
assert 'or requests an inventory cell, and is never selected otherwise, not even explicitly' in law
for e in sup + ov:
    assert e['after'].count('\u2014') == e['before'].count('\u2014')
# The detector and adapter bullets, and the closing paragraph, are CRC-1's verbatim.
for marker in ('- **The core detector closure**', '- **The core adapter closure**', 'Security derives every core role closure'):
    seg = [l for l in sup[0]['before'].split('\n') if l.startswith(marker)][0]
    assert seg in ie285.split('\n'), marker

# 6. The law agrees: M3-C r8 item 9.
law_text = (M / 'PROPOSAL.md').read_text(encoding='utf-8')
assert '# Sealed snapshot and Plan \u2014 proposal M3-C r8' in law_text.split('\n')[0]
use3 = law_text[law_text.index('3. **(r8, X-H3) the producer and enumerator of host inventory records'):]
use3 = use3[:use3.index('- **Its `semanticClosures` membership.**')]
for needle in ('file@enumerated', 'package@manifest-declared', 'vcs-change@vcs-reported', 'enumerator.closureId',
               'stage-spec.producerClosure', 'view.producerClosure', 'fact.producerClosure',
               'subject-scope.enumeratorClosure', 'available or not', 'owes a symbol inventory',
               'CandidateProducerResultV1.producerClosure'):
    assert needle in use3, needle
assert 'or requests an `inventory` cell (r8)' in law_text

# 7. README and the review's list.
readme = (D / 'README.md').read_text(encoding='utf-8')
for e in sup + ov:
    where = str(e['selector'].get('line', e['selector'].get('jsonPointer')))
    assert e['parent']['path'] in readme and where in readme, where
report['supersededPassages'] = [s['supersedes'] for s in sup]
report['passageSupersessions'] = len(sup)
report['passageOverrides'] = len(ov)
report['check'] = 'pass'
print(json.dumps(report, indent=1))
