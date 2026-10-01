"""Scratch-only static check of the X12-0 overrides. It applies each line override of successor.json
to its pinned parent in memory, parses the result with ast (nothing is imported or executed), and
reads PUBLIC_ROUTE_REMEDIES as a literal. Nothing is written to either repository.

It checks that:
- each parent changes on exactly its one selected line, and the result still parses;
- the table keeps its keys and every other value, and CONFIG.INVALID is the one new string;
- both selected copies carry the same string;
- the string still satisfies the remedy predicates foundation/check-identity.py applies to it
  (the unregistered-name and ownership-tuple sentences);
- it states the X12 policy conditions and fits DomainDetail.remedy (BoundedText, 1024 code points).

check-identity.py itself cannot run here: the native model refuses a Python whose Unicode case data is
not 15.0.0 (this Mac has 3.14.6 with 16.0.0), which it reports as an environment fault."""
import ast, hashlib, json
from pathlib import Path
A = Path(__file__).resolve().parents[5]
record = json.loads((A / 'docs/implementation/m2/config-remedy-x12-0/successor.json').read_text())

def table(source):
    for node in ast.parse(source).body:
        if isinstance(node, ast.Assign) and [t.id for t in node.targets if isinstance(t, ast.Name)] == ['PUBLIC_ROUTE_REMEDIES']:
            return ast.literal_eval(node.value)
    raise AssertionError('PUBLIC_ROUTE_REMEDIES not found')

results, widened = [], []
for o in record['passageOverrides']:
    raw = (A / o['parent']['path']).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == o['parent']['sha256'] and len(raw) == o['parent']['bytes']
    text = raw.decode('utf-8')
    lines = text.splitlines(keepends=True)
    n = o['selector']['line']
    assert lines[n - 1].rstrip('\n') == o['before']
    patched = ''.join(lines[:n - 1] + [o['after'] + '\n'] + lines[n:])
    old, new = table(text), table(patched)
    assert list(old) == list(new), 'keys changed'
    assert {k: v for k, v in old.items() if k != 'CONFIG.INVALID'} == {k: v for k, v in new.items() if k != 'CONFIG.INVALID'}
    s = new['CONFIG.INVALID']
    widened.append(s)
    checks = {
        'only-the-selected-line-differs': sum(a != b for a, b in zip(text.splitlines(), patched.splitlines())) == 1
            and len(text.splitlines()) == len(patched.splitlines()),
        'check-identity:every-remedy-this-key-reuses-states-the-ownership-tuple-condition-too':
            '(capabilityId, languageMode, workspaceRoot)' in s,
        'check-identity:the-widened-remedies-still-state-their-original-condition':
            'registered capability id from the native capability matrix' in s,
        'states-exactly-one-bundled-pack-id': 'name exactly one bundled policy pack id' in s,
        'states-no-own-or-third-party-policy-document': 'supply no policy document of your own or from a third party' in s,
        'no-new-code-named': 'POLICY.' not in s and 'PACK.' not in s,
        'fits-bounded-text': len(s) <= 1024,
        'ascii': s.isascii(),
    }
    results.append({'parent': o['parent']['path'], 'checks': checks})
assert len(set(widened)) == 1, 'copies disagree'
passed = all(all(r['checks'].values()) for r in results)
print(json.dumps({'passed': passed, 'remedy': widened[0], 'remedyChars': len(widened[0]), 'results': results}, indent=1))
raise SystemExit(0 if passed else 1)
