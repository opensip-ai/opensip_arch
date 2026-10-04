"""Build contract successor B-S9 (law M3-B r2 successor S9, split out of B-S1 by lead decision).

Form: complete successor copies (capability-totality-reference-selection-v1's form for this same
file; 468a's and I1-L's for schemas). Each candidate copy is its parent's EFFECTIVE text under
the product lock, meaning the raw parent with every passage override and supersession the lock
binds to that path applied in lock order, with line 1158 then replaced by the S9 remedy. Nothing
else changes.

Writes, deterministically: b-s9/reference/native_evidence_model.py,
b-s9/reference/native_evidence_model.v2.py, b-s9/evidence/copies-report.json,
b-s9/successor.json and ../b-s9-subject.json. It reads the architecture repository and the
product lock at PRODUCT_REV through read-only `git show`. Run with python3 -I -B."""
import ast, hashlib, json, subprocess
from pathlib import Path

A = Path(__file__).resolve().parents[6]
PRODUCT = Path('/Users/sb/code/opensip-ai/opensip')
PRODUCT_REV = 'e093e90'
B = 'docs/implementation/m3/config-discovery-b/'
D = B + 'b-s9/'
X12_0 = 'docs/implementation/m2/config-remedy-x12-0/successor.json'
COPIES = [
    ('docs/implementation/m2/capability-totality-reference-selection-v1/reference/native_evidence_model.py',
     D + 'reference/native_evidence_model.py', 'the current selected native reference'),
    ('docs/coop/design-corrections/native/native_evidence_model.v2.py',
     D + 'reference/native_evidence_model.v2.py', 'the frozen v2 native model that law X12 names'),
]
LINE = 1158
S9_REMEDY = (
    'the configuration or selection is invalid: make each configuration file, flag and request well-formed for its '
    'schema and layer, with no unknown key, a supported schemaVersion, canonical project-relative paths that exist, and '
    'a nonempty workspaceRoots when one is given; name only a registered profile and registered or admitted ids, and '
    'state each component once with no conflicting pin and hold; for capabilities, name a registered capability id '
    'from the native capability matrix, and state at most one row per (capabilityId, languageMode, workspaceRoot); for '
    'policy, name exactly one bundled policy pack id, written exactly as name:version, and supply no policy document of '
    'your own or from a third party')
S9_AFTER = '    "CONFIG.INVALID": ' + json.dumps(S9_REMEDY) + ','
HAND = [D + 'README.md', D + 'evidence/build_b_s9.py', D + 'evidence/check_b_s9.py', D + 'evidence/verify_scratch.py']


def pin_bytes(path, b):
    return {'path': path, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


def pin(p):
    return pin_bytes(p, (A / p).read_bytes())


def dump(p, value):
    (A / p).parent.mkdir(parents=True, exist_ok=True)
    (A / p).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def lock_entries(path):
    """Every passage override and supersession the product lock binds to `path`, in lock order."""
    lock = json.loads(subprocess.run(['git', '-C', str(PRODUCT), 'show', PRODUCT_REV + ':design-lock.json'],
                                     check=True, capture_output=True).stdout)
    out = []
    for binding in lock['contractSuccessors']:
        record = json.loads((A / binding['record']['path']).read_bytes())
        assert pin(binding['record']['path']) == binding['record']
        for kind in ('passageOverrides', 'passageSupersessions'):
            for entry in record.get(kind, []):
                if entry['parent']['path'] == path:
                    out.append((binding['record'], kind, entry))
    return out


def effective(path):
    raw = (A / path).read_bytes()
    text = raw.decode('utf-8')
    assert text.endswith('\n') and text.split('\n')[:-1] == text.splitlines() and '\r' not in text
    lines = text.splitlines()
    applied = []
    for record, kind, entry in lock_entries(path):
        n = entry['selector']['line']
        assert entry['parent'] == pin_bytes(path, raw), 'a bound entry names another revision of the parent'
        if kind == 'passageOverrides':
            assert lines[n - 1] == entry['before'] == text.splitlines()[n - 1]
        else:
            assert lines[n - 1] == entry['before']
        lines[n - 1] = entry['after']
        applied.append({'record': record, 'kind': kind, 'selector': entry['selector']})
    return raw, lines, applied


def table(source):
    for node in ast.parse(source).body:
        if isinstance(node, ast.Assign) and any(getattr(t, 'id', '') == 'PUBLIC_ROUTE_REMEDIES' for t in node.targets):
            return ast.literal_eval(node.value)
    raise AssertionError('no PUBLIC_ROUTE_REMEDIES')


x12 = json.loads((A / X12_0).read_bytes())
report = {'schemaVersion': 1, 'productRev': PRODUCT_REV, 'line': LINE, 's9Remedy': S9_REMEDY, 'copies': []}
parents = [pin(X12_0)]
for parent_path, copy_path, role in COPIES:
    raw, lines, applied = effective(parent_path)
    assert [a['record']['path'] for a in applied] == [X12_0], applied   # the only bound entry today
    x12_after = [o['after'] for o in x12['passageOverrides'] if o['parent']['path'] == parent_path]
    assert lines[LINE - 1] == x12_after[0]
    eff = ('\n'.join(lines) + '\n').encode('utf-8')
    lines[LINE - 1] = S9_AFTER
    out = ('\n'.join(lines) + '\n').encode('utf-8')
    (A / copy_path).parent.mkdir(parents=True, exist_ok=True)
    (A / copy_path).write_bytes(out)
    raw_lines, out_lines = raw.decode('utf-8').splitlines(), out.decode('utf-8').splitlines()
    assert len(raw_lines) == len(out_lines)
    changed_raw = [i + 1 for i, (a, b) in enumerate(zip(raw_lines, out_lines)) if a != b]
    changed_eff = [i + 1 for i, (a, b) in enumerate(zip(eff.decode('utf-8').splitlines(), out_lines)) if a != b]
    assert changed_raw == changed_eff == [LINE]
    before_t, after_t = table(eff.decode('utf-8')), table(out.decode('utf-8'))
    assert set(before_t) == set(after_t) and all(before_t[k] == after_t[k] for k in before_t if k != 'CONFIG.INVALID')
    assert after_t['CONFIG.INVALID'] == S9_REMEDY
    parents.append(pin_bytes(parent_path, raw))
    report['copies'].append({
        'role': role, 'parent': pin_bytes(parent_path, raw),
        'boundEntriesApplied': applied,
        'effectiveParent': {'bytes': len(eff), 'sha256': hashlib.sha256(eff).hexdigest()},
        'copy': pin(copy_path),
        'linesChangedFromRawParent': changed_raw, 'linesChangedFromEffectiveParent': changed_eff,
        'line1158': {'effective': x12_after[0], 'copy': S9_AFTER},
    })
dump(D + 'evidence/copies-report.json', report)

candidates = sorted([pin(p) for p in HAND + [c for _, c, _ in COPIES] + [D + 'evidence/copies-report.json']],
                    key=lambda r: r['path'])
record = {
    'schemaVersion': 1,
    'standing': ('PROPOSED B-S9 contract successor (law M3-B r2 successor S9, split out of B-S1 by lead decision): the '
                 'PUBLIC_ROUTE_REMEDIES["CONFIG.INVALID"] remedy widened so that it stays true for every external '
                 'configuration refusal B1 adds to that code, keeping the capability and policy clauses word for word. '
                 'Complete successor copies at new paths, the form of capability-totality-reference-selection-v1 for '
                 'this same file: each copy is its parent\'s effective text under the product lock at e093e90 '
                 '(X12-0\'s line-1158 override, the only bound entry on either file, applied) with line 1158 replaced '
                 'by the S9 remedy and no other byte changed. Current selected native reference becomes '
                 'docs/implementation/m3/config-discovery-b/b-s9/reference/native_evidence_model.py, and the successor '
                 'text of the frozen native_evidence_model.v2.py that law X12 names is '
                 'docs/implementation/m3/config-discovery-b/b-s9/reference/native_evidence_model.v2.py; the parents and '
                 'X12-0\'s meaning on them become historical. No passage override or supersession; no code, class, '
                 'exit, route, public code, inventory or product change. The exact frozen candidate requires actual '
                 'independent review and root assent.'),
    'parents': sorted(parents, key=lambda r: r['path']),
    'passageOverrides': [],
    'candidates': candidates,
}
dump(D + 'successor.json', record)
subject = {'schemaVersion': 1, 'files': sorted(candidates + [pin(D + 'successor.json')], key=lambda r: r['path'])}
dump(B + 'b-s9-subject.json', subject)
print(json.dumps({'copies': [c['copy'] for c in report['copies']], 's9Chars': len(S9_REMEDY),
                  'subject': pin(B + 'b-s9-subject.json')}, indent=1))
