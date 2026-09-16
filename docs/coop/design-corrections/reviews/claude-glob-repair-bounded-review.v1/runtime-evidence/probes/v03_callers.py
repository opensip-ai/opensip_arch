"""V03 — compare the contract's composition clause with the ACTUAL owning schemas and callers.

The instruction names ScopeDocument versus string FieldFilter specifically. The contract states one
composition rule (ScopeDocument) and explicitly defers absent/empty-list behaviour to other owners.
I check whether that deferral is honest: do the real callers actually differ, and is the difference
covered by the contract's own scoping?
"""
import importlib.util, inspect, json, os, re, sys

SNAP = '/tmp/opensip-design-corrections/candidate-subject.v31'
G = '/tmp/opensip-design-corrections/glob-semantics-successor.v1/source'
OUT = '/tmp/opensip-design-corrections/claude-glob-repair-bounded-review.v1/receipts'
W = os.path.join(SNAP, 'docs/coop/design-corrections/workflows')
spec = importlib.util.spec_from_file_location('wfm31b', os.path.join(W, 'workflows_model.v1.py'))
WFM = importlib.util.module_from_spec(spec)
sys.modules['wfm31b'] = WFM
spec.loader.exec_module(WFM)
R = {}

# ---------------- every caller of glob_match ----------------
src = open(os.path.join(W, 'workflows_model.v1.py'), encoding='utf-8').read()
lines = src.splitlines()
callers = [(i, l.strip()) for i, l in enumerate(lines, 1)
           if 'glob_match(' in l and not l.strip().startswith('def ')]
R['callSites'] = [{'line': i, 'text': t[:190]} for i, t in callers]
print('--- glob_match call sites in workflows_model.v1.py ---')
for i, t in callers:
    print('%5d  %s' % (i, t[:170]))

# ---------------- ScopeDocument composition ----------------
print('\n--- in_scope (ScopeDocument) ---')
print(inspect.getsource(WFM.in_scope))
R['inScopeSource'] = inspect.getsource(WFM.in_scope)
cases = [
    ({'include': ['src/**'], 'exclude': []}, 'src/a.ts', True, 'plain include'),
    ({'include': ['src/**'], 'exclude': ['src/**/*.js']}, 'src/a.js', False, 'exclusion wins'),
    ({'include': ['src/**'], 'exclude': ['src/**/*.js']}, 'src/a.ts', True, 'non-matching exclude'),
    ({'include': [], 'exclude': []}, 'src/a.ts', False, 'EMPTY include selects nothing'),
    ({'include': ['**'], 'exclude': ['**']}, 'x', False, 'exclude beats include on equal patterns'),
]
rows = []
for scope, cand, want, note in cases:
    got = WFM.in_scope(scope, cand)
    rows.append({'scope': scope, 'candidate': cand, 'expected': want, 'actual': got,
                 'note': note, 'agrees': got == want})
    print('  %-42s %-12r -> %-5s (expected %s)' % (note, cand, got, want))
R['scopeDocumentCases'] = rows
R['scopeCompositionMatchesContract'] = all(r['agrees'] for r in rows)

# ---------------- the OTHER caller: enumeration filter ----------------
print('\n--- the enumeration filter caller (a different absent/empty-list rule) ---')
for i in range(1480, 1495):
    if i - 1 < len(lines):
        print('%5d  %s' % (i, lines[i - 1][:150]))
R['enumerationFilterRegion'] = '\n'.join(lines[1479:1494])


def enum_filter(enum, s):
    """Exactly the shape at workflows_model.v1.py:1486-1488."""
    if enum.get('include') and not any(WFM.glob_match(g, s) for g in enum['include']):
        return False
    if any(WFM.glob_match(g, s) for g in enum.get('exclude', [])):
        return False
    return True


div = []
for enum, cand in (({'include': [], 'exclude': []}, 'src/a.ts'),
                   ({'exclude': []}, 'src/a.ts'),
                   ({'include': ['src/**'], 'exclude': []}, 'other/a.ts')):
    a = enum_filter(enum, cand)
    b = None
    try:
        b = WFM.in_scope({'include': enum.get('include', []), 'exclude': enum.get('exclude', [])}, cand)
    except Exception as ex:
        b = 'ERROR:' + type(ex).__name__
    div.append({'input': enum, 'candidate': cand, 'enumerationFilter': a, 'scopeDocument': b,
                'differs': a != b})
    print('  enum=%-38s cand=%-12r enumFilter=%-5s in_scope=%-5s differs=%s'
          % (json.dumps(enum), cand, a, b, a != b))
R['absentEmptyListDivergence'] = div
R['divergenceExists'] = any(d['differs'] for d in div)
R['contractDefersThisExplicitly'] = True
print('\nabsent/empty-list behaviour genuinely differs between the two callers :', R['divergenceExists'])

# ---------------- string FieldFilter with cmp: glob ----------------
print('\n--- FieldFilter cmp:glob ---')
m = re.search(r"'glob': lambda[^,]*", src)
R['fieldFilterGlobLambda'] = m.group(0) if m else None
print('  dispatch:', R['fieldFilterGlobLambda'])
R['callerCoercesWithStr'] = "glob_match(x, str(v))" in src
print("  caller applies str(v) before matching:", R['callerCoercesWithStr'])

# does the owning schema restrict cmp:glob to string fields?
found = {}
for rel in ('schemas/common.schema.json', 'schemas/evaluator3/common.schema.json'):
    p = os.path.join(G, 'docs/coop/design-corrections/workflows', rel)
    if not os.path.isfile(p):
        continue
    d = json.load(open(p))
    txt = json.dumps(d)
    for name, dd in d.get('$defs', {}).items():
        s = json.dumps(dd)
        if '"glob"' in s and ('cmp' in s or 'Filter' in name):
            found[rel + '#' + name] = dd
R['fieldFilterDefs'] = {k: json.dumps(v)[:1200] for k, v in found.items()}
for k, v in found.items():
    print('\n  %s:' % k)
    print('   ', json.dumps(v)[:1100])

json.dump(R, open(os.path.join(OUT, 'v03-callers.json'), 'w'), indent=1, default=str)
print('\nwrote v03-callers.json')
