"""Read-only checks of contract successor B-S9. Run with python3 -I -B; it writes nothing. It reads
the product lock at e093e90 through read-only `git show`.

1. successor.json: no passage override or supersession; parents and candidates pinned; candidates
   equal the subject members other than the record.
2. Each copy, recomputed independently: it is its parent's effective text under the lock (every
   bound entry on that path applied), with exactly line 1158 different. It parses as Python, and
   its PUBLIC_ROUTE_REMEDIES has the same keys and the same values except CONFIG.INVALID.
3. The two copies differ from each other exactly as their raw parents do, so the
   capability-totality correction is carried.
4. The S9 remedy: ASCII, at most 1024 characters (BoundedText), with both foundation
   check-identity predicates and every next step of the README's truth table."""
import ast, difflib, hashlib, json, subprocess
from pathlib import Path

A = Path(__file__).resolve().parents[6]
PRODUCT = Path('/Users/sb/code/opensip-ai/opensip')
B = 'docs/implementation/m3/config-discovery-b/'
D = B + 'b-s9/'
PAIRS = [('docs/implementation/m2/capability-totality-reference-selection-v1/reference/native_evidence_model.py',
          D + 'reference/native_evidence_model.py'),
         ('docs/coop/design-corrections/native/native_evidence_model.v2.py', D + 'reference/native_evidence_model.v2.py')]


def raw(p):
    return (A / p).read_bytes()


def pin(p):
    b = raw(p)
    return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


record = json.loads(raw(D + 'successor.json'))
subject = json.loads(raw(B + 'b-s9-subject.json'))
assert set(record) == {'schemaVersion', 'standing', 'parents', 'passageOverrides', 'candidates'}
assert record['passageOverrides'] == []
for row in record['parents'] + record['candidates'] + subject['files']:
    assert pin(row['path']) == row, row['path']
assert {r['path'] for r in record['candidates']} == {r['path'] for r in subject['files']} - {D + 'successor.json'}

lock = json.loads(subprocess.run(['git', '-C', str(PRODUCT), 'show', 'e093e90:design-lock.json'],
                                 check=True, capture_output=True).stdout)


def table(text):
    for node in ast.parse(text).body:
        if isinstance(node, ast.Assign) and any(getattr(t, 'id', '') == 'PUBLIC_ROUTE_REMEDIES' for t in node.targets):
            return ast.literal_eval(node.value)


copies = {}
for parent, cpath in PAIRS:
    lines = raw(parent).decode('utf-8').splitlines()
    n_applied = 0
    for b in lock['contractSuccessors']:
        rec = json.loads(raw(b['record']['path']))
        for e in rec.get('passageOverrides', []) + rec.get('passageSupersessions', []):
            if e['parent']['path'] == parent:
                assert lines[e['selector']['line'] - 1] == e['before']
                lines[e['selector']['line'] - 1] = e['after']
                n_applied += 1
    assert n_applied == 1, n_applied
    out = raw(cpath).decode('utf-8')
    assert out.endswith('\n') and out.split('\n')[:-1] == out.splitlines()
    got = out.splitlines()
    assert len(got) == len(lines) and [i + 1 for i, (a, b) in enumerate(zip(lines, got)) if a != b] == [1158]
    before_t, after_t = table('\n'.join(lines) + '\n'), table(out)
    assert set(before_t) == set(after_t)
    assert all(before_t[k] == after_t[k] for k in before_t if k != 'CONFIG.INVALID')
    copies[cpath] = (got, after_t['CONFIG.INVALID'])

(p0, c0), (p1, c1) = PAIRS
raw_diff = list(difflib.unified_diff(raw(p0).decode('utf-8').splitlines(), raw(p1).decode('utf-8').splitlines(), n=0, lineterm=''))[2:]
copy_diff = list(difflib.unified_diff(copies[c0][0], copies[c1][0], n=0, lineterm=''))[2:]
assert raw_diff == copy_diff and raw_diff, 'the copies must differ exactly as their parents do'
remedy = copies[c0][1]
assert remedy == copies[c1][1] and remedy.isascii() and len(remedy) <= 1024
for phrase in ('registered capability id from the native capability matrix', '(capabilityId, languageMode, workspaceRoot)',
               'name exactly one bundled policy pack id', 'written exactly as name:version',
               'supply no policy document of your own or from a third party', 'well-formed for its schema and layer',
               'no unknown key', 'a supported schemaVersion', 'canonical project-relative paths that exist',
               'a nonempty workspaceRoots when one is given', 'name only a registered profile',
               'registered or admitted ids', 'state each component once with no conflicting pin and hold'):
    assert phrase in remedy, phrase
report = json.loads(raw(D + 'evidence/copies-report.json'))
assert [c['copy'] for c in report['copies']] == [pin(c) for _, c in PAIRS]
assert report['s9Remedy'] == remedy
print(json.dumps({'passed': True, 'copies': [pin(c) for _, c in PAIRS], 'linesChanged': [1158],
                  'boundEntriesApplied': 1, 'parentDifferenceCarried': len(raw_diff),
                  's9': {'chars': len(remedy), 'ascii': True}}, indent=1))
