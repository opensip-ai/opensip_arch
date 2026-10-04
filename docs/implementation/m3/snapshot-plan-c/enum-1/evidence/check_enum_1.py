"""Check ENUM-1 without writing anything.

Usage: check_enum_1.py [--product PATH] [--rev REV]
(default /Users/sb/code/opensip-ai/opensip and 1799d3d; both read only, through `git show`).

It re-derives, independently of build_enum_1.py:
1. every parent pin against the arch bytes and as accepted in the product lock; the markdown parents
   have no complete copy in the chain, and each schema parent is the last complete copy of its name;
2. each override: no bound record overrides or supersedes its key, and `before` is the selected text
   at the selector (a line of a markdown parent, a JSON Pointer string of a schema parent);
3. what changed: every removed span lies inside the fragment the README names for that entry, every
   other sentence of each `before` survives verbatim, and each schema parent changes only at the
   overridden pointers;
4. the rule: the one case, its exact pair, what it covers, the stay-required clause, the
   inventory-cell clause and the residual refusal are stated; the refusal code is kept everywhere it
   was; no new refusal code, reason token or em dash appears; every entry names ENUM-1;
5. law agreement: M3-C r8 (the accepted snapshot) states X-8's recommendation and item 7's pair;
6. the owed code: the reference models and product main still refuse the case at the lines the
   README cites (ENUM-1 changes no code, so these are its consumers' work);
7. that the README names every passage, and that the review's supersededPassages list is empty.
Run with python3 -I -B at nice -n 19.
"""
import copy, difflib, hashlib, json, re, subprocess, sys
from pathlib import Path

A = Path(__file__).resolve().parents[6]
M = A / 'docs/implementation/m3/snapshot-plan-c'
D = M / 'enum-1'
args = list(sys.argv[1:])


def opt(name, default):
    if name in args:
        i = args.index(name)
        value = args[i + 1]
        del args[i:i + 2]
        return value
    return default


W = Path(opt('--product', '/Users/sb/code/opensip-ai/opensip'))
REV = opt('--rev', '1799d3d')
F = 'docs/coop/design-corrections/foundation/'
ENC, EXC, COMP = F + 'enumeration-contract.v1.md', F + 'execution-inputs-contract.v1.md', F + 'evaluator-composition-contract.v3.md'
S = 'docs/implementation/m3/syntax-e/syn-1f/design/foundation/'
EPS, EXS = S + 'enumeration-plan.schema.v1.json', S + 'execution-inputs.schema.v1.json'
MC8 = ('docs/implementation/m3/snapshot-plan-c/PROPOSAL-r8.md',
       '578c186ec9fc239f42d88713b8c31ec7085ab507251691f6cbba01e49b6607e1')
CODE = 'REQUIRED_UNSELECTED_ENUMERATOR'


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
accepted, current, names = {}, {}, {}
for key in ('sourceManifest', 'applicationManifest'):
    for row in json.loads(pinned(lock['approvals'][key]))['files']:
        accepted[row['path']] = {k: row[k] for k in ('path', 'bytes', 'sha256')}
for b in lock['contractSuccessors']:
    rec = json.loads(pinned(b['record']))
    for row in rec['candidates']:
        accepted[row['path']] = row
        names.setdefault(row['path'].rsplit('/', 1)[-1], []).append(row['path'])
    for e in rec.get('passageOverrides', []) + rec.get('passageSupersessions', []):
        current[keyof(e)] = b['record']
report = {'rev': REV, 'contractSuccessors': len(lock['contractSuccessors'])}

# 1. Parents.
assert set(record) == {'schemaVersion', 'standing', 'parents', 'passageOverrides', 'passageSupersessions', 'candidates'}
assert record['passageSupersessions'] == []
assert [p['path'] for p in record['parents']] == sorted([ENC, EXC, COMP, EPS, EXS])
raws = {}
for p in record['parents']:
    raws[p['path']] = pinned(p)
    assert accepted[p['path']] == p, p['path']
for path in (ENC, EXC, COMP):
    assert path.rsplit('/', 1)[-1] not in names, path
for path in (EPS, EXS):
    assert names[path.rsplit('/', 1)[-1]][-1] == path, names[path.rsplit('/', 1)[-1]]

# 2. Overrides: fresh keys, and before is the selected text.
ov = record['passageOverrides']
EXPECTED = [(ENC, {'line': 53}), (ENC, {'line': 75}), (ENC, {'line': 145}),
            (EPS, {'jsonPointer': '/$defs/SelectedEnumeratorRef/description'}),
            (EPS, {'jsonPointer': '/$defs/UnselectedEnumeratorRef/description'}),
            (EPS, {'jsonPointer': '/$defs/EnumeratorRef/description'}),
            (EXC, {'line': 103}), (EXC, {'line': 110}), (EXC, {'line': 131}),
            (EXS, {'jsonPointer': '/x-opensip-derived-carrier-law/candidateCarrier'}),
            (COMP, {'line': 235})]
assert [(o['parent']['path'], o['selector']) for o in ov] == EXPECTED
for o in ov:
    assert set(o) == {'parent', 'selector', 'before', 'after'}
    assert keyof(o) not in current, ('bound at %s' % REV, keyof(o), current.get(keyof(o)))
    raw = raws[o['parent']['path']]
    if 'line' in o['selector']:
        assert o['parent']['path'].endswith('.md')
        assert raw.decode('utf-8').splitlines()[o['selector']['line'] - 1] == o['before']
    else:
        assert resolve(json.loads(raw), o['selector']['jsonPointer']) == o['before']
    assert o['after'] != o['before']
report['freshKeys'] = len(ov)

# 3. What changed.
ANCHORS = [
    '`required=true` plus unselected refuses (`ENUMERATION_PLAN_REQUIRED_UNSELECTED_ENUMERATOR`).',
    'A `required=true` cell still may not be unselected',
    'required+unselected enumerator;',
    'refuses pre-Plan (no fictional closure).',
    'Optional-cell enumerator not selected. Lawful only on UnavailableProgramBindingV1 when the cell required=false.',
    'when required=false.',
    '`EXECUTION_INPUTS_CANDIDATE_REQUIRED` first.',
    'on an available binding or a required cell, and',
    '(an optional',
    'refuses EXECUTION_INPUTS_CANDIDATE_REQUIRED first.',
    'before reaching this bridge.',
]


def sentences(text):
    out, start = [], 0
    for m in re.finditer(r'(?<=[.;])\s+', text):
        out.append((start, m.start()))
        start = m.end()
    out.append((start, len(text)))
    return [(a, b) for a, b in out if b > a]


kept_total = 0
for o, anchor in zip(ov, ANCHORS):
    lo = o['before'].index(anchor)
    hi = lo + len(anchor)
    assert o['before'].count(anchor) == 1, anchor
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, o['before'], o['after'], autojunk=False).get_opcodes():
        if tag in ('replace', 'delete'):
            assert lo <= i1 and i2 <= hi, (o['selector'], o['before'][i1:i2])
        if tag == 'insert':
            assert lo <= i1 <= hi, (o['selector'], o['after'][j1:j2][:60])
    for a, b in sentences(o['before']):
        if not (a < hi and lo < b):
            assert o['before'][a:b] in o['after'], (o['selector'], o['before'][a:b][:80])
            kept_total += 1
report['sentencesKept'] = kept_total
for path in (EPS, EXS):
    doc = json.loads(raws[path])
    after_doc = copy.deepcopy(doc)
    for o in ov:
        if o['parent']['path'] == path:
            assign(after_doc, o['selector']['jsonPointer'], o['after'])
    assert after_doc != doc
    for o in ov:
        if o['parent']['path'] == path:
            assign(after_doc, o['selector']['jsonPointer'], o['before'])
    assert after_doc == doc, path

# 4. The rule.
enc53 = ov[0]['after']
for phrase in ('`required=true` plus unselected refuses (`ENUMERATION_PLAN_REQUIRED_UNSELECTED_ENUMERATOR`), except in one'
               ' case (contract successor ENUM-1',
               'no admitted closure can lawfully be the binding\'s selected enumerator, because a closure the cell\'s'
               ' mode needs is not admitted for the request',
               'for a TypeScript or Rust mode, its provider closure; for `syntax-only`, a grammar closure',
               '`{status:"unselected", reason:"optional-unselected"}`',
               'Its pair is exactly deficiency `provider-unavailable` with `nativeCause` null.',
               'Its `universe` is null, its host extents are still populated, and its inventories are empty'
               ' `unavailable` with that pair.',
               'It covers a required provider closure that is not installed, or that current trust does not admit',
               '"required provider closure not installed"', 'an ephemeral request with no admitted trust view',
               'The cell stays required.', '`requiredCellDeficiencies`', 'required-cell totality is unchanged',
               'A required cell whose closure is admitted never takes this shape',
               'An `inventory` cell never meets the case', 'admission checks the shape',
               'A required unselected binding with any other pair still refuses.',
               'Non-null universe plus unselected refuses', '`PROVIDER.NOT_SELECTED` is **not** this case'):
    assert phrase in enc53, phrase
assert 'Outside ENUM-1\'s one case' in ov[1]['after']
assert 'required+unselected enumerator outside ENUM-1\'s one case' in ov[2]['after']
for o in ov:
    assert 'ENUM-1' in o['after'], o['selector']
    assert o['after'].count('—') == o['before'].count('—'), o['selector']
    assert o['after'].count(CODE) == o['before'].count(CODE), o['selector']
    assert set(re.findall(r'\b[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+\b', o['after'])) == \
        set(re.findall(r'\b[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+\b', o['before'])), ('new code token', o['selector'])
    assert set(re.findall(r'reason:"([a-z-]+)"', o['after'])) <= {'optional-unselected'}
    assert 'capability-missing' not in o['after'] or 'capability-missing' in o['before']
for o in ov[3:6]:
    assert 'provider-unavailable' in o['after'] and 'nativeCause null' in o['after']
report['ruleClauses'] = 'pass'

# 5. Law agreement: M3-C r8's accepted snapshot.
law_raw = (A / MC8[0]).read_bytes()
assert hashlib.sha256(law_raw).hexdigest() == MC8[1]
law = law_raw.decode('utf-8')
x8 = law[law.index('- **X-8 (r8, for the enumeration owner, with J1).**'):law.index('- **X-9 (r8,')]
for needle in ('ENUMERATION_PLAN_REQUIRED_UNSELECTED_ENUMERATOR', 'enumeration_model.v1.py:740-745',
               'exactly when no closure for the cell\'s mode is admitted, with the `provider-unavailable` pair',
               'required-cell indeterminacy is unchanged', 'C4a\'s and J2c\'s legs for that case wait for it'):
    assert needle in x8, needle
assert 'deficiency `provider-unavailable` with `nativeCause` null' in law
assert 'An `inventory` binding names the core provider closure' in law or 'every `inventory` binding names the core provider closure' in law

# 6. The owed code still refuses the case where the README says it does.
REF = A / 'docs/implementation/m2/enumeration-locator-totality-reference-selection-v1/reference/enumeration_model.v1.py'
ref = REF.read_text(encoding='utf-8').splitlines()
assert 'if cell.get("required") is True or available:' in ref[758] and CODE in ref[759]
EXM = A / 'docs/coop/design-corrections/foundation/execution_inputs_model.v1.py'
exm = EXM.read_text(encoding='utf-8').splitlines()
assert 'cell["required"] and cell["capabilityId"] in CANDIDATE_CAPS' in exm[1197] and 'CANDIDATE_REQUIRED' in exm[1198]
assert '"optional-unselected" if not required else "unavailable-binding"' in exm[527]
join = show('crates/evaluator/src/enumeration_join.rs').decode('utf-8').splitlines()
assert 'field(cell, "required")? == &V::Bool(true)' in join[561] and CODE in join[564]
exi = show('crates/evaluator/src/execution_inputs.rs').decode('utf-8').splitlines()
assert 'field(b.cell, "required") == &V::Bool(true)' in exi[1169] and 'CANDIDATE_REQUIRED' in exi[1173]
report['owedCode'] = {'referenceEnumeration': 'enumeration_model.v1.py:759-760',
                      'productEnumeration': 'crates/evaluator/src/enumeration_join.rs:560-566',
                      'referenceExecutionInputs': 'execution_inputs_model.v1.py:1198-1199',
                      'productExecutionInputs': 'crates/evaluator/src/execution_inputs.rs:1170-1175'}

# 7. README and the review's list.
readme = (D / 'README.md').read_text(encoding='utf-8')
for o in ov:
    where = str(o['selector'].get('line', o['selector'].get('jsonPointer')))
    assert o['parent']['path'] in readme and where in readme, where
for path, line in (('enumeration_model.v1.py', '759-760'), ('enumeration_join.rs', '560-566'),
                   ('execution_inputs_model.v1.py', '1198-1199'), ('execution_inputs.rs', '1170-1175')):
    assert path in readme and line in readme, (path, line)
report['supersededPassages'] = []
report['passageOverrides'] = len(ov)
report['check'] = 'pass'
print(json.dumps(report, indent=1))
