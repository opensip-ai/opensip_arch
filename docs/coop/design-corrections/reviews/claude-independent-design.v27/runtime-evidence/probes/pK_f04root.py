"""PROBE K (v27) — F-04 internal-root spelling: is it now normatively fixed on snapshot27,
is the sentinel spelling rejected at admission, and is a root-specific fault raised instead of
the misattributed ENUMERATION_BINDING_PROGRAM_ENTRY?

Executed against the frozen snapshot27 models, not asserted from prose.
"""
import importlib.util, json, os, re, sys

SRC = '/tmp/opensip-design-corrections/candidate-subject.v27'
F = os.path.join(SRC, 'docs/coop/design-corrections')
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v27/receipts'
os.makedirs(OUT, exist_ok=True)
R = {}

sch = json.load(open(os.path.join(F, 'native/native-evidence.schemas.v2.json')))
defs = sch.get('$defs', {})
print('--- $defs entries mentioning root ---')
for k in sorted(defs):
    if 'root' in k.lower():
        print('\n%s:' % k)
        print(json.dumps(defs[k], indent=1))
        R.setdefault('rootDefs', {})[k] = defs[k]

wu = defs['WorkspaceUnitV2']['properties']
R['workspaceUnitV2.rootPath'] = wu['rootPath']
R['workspaceUnitV2.memberPackageRoots'] = wu['memberPackageRoots']

# does the sentinel '.' now fail schema validation?
try:
    import jsonschema
    base = dict(sch)
    for cand in ('', '.', './', 'src', '/abs'):
        inst = {'$ref': '#/$defs/InternalUnitRootV1'}
        v = {'$schema': sch.get('$schema', 'https://json-schema.org/draft/2020-12/schema'),
             '$defs': defs, '$ref': '#/$defs/InternalUnitRootV1'}
        try:
            jsonschema.validate(cand, v)
            ok = 'ACCEPT'
        except Exception as ex:
            ok = 'REJECT: ' + str(ex).splitlines()[0][:90]
        print('InternalUnitRootV1 %-8r -> %s' % (cand, ok))
        R.setdefault('schemaValidation', {})[repr(cand)] = ok
except ImportError:
    R['schemaValidation'] = 'jsonschema unavailable'

# --- prose: native-evidence.md U-1 and the asymmetry ---
md = open(os.path.join(SRC, 'docs/v2/contracts/product-v1/native-evidence.md'), encoding='utf-8').read()
lines = md.splitlines()
hits = [(i + 1, l) for i, l in enumerate(lines)
        if re.search(r'rootPath|internal[- ]root|workspaceRoot|InternalUnitRoot', l)]
print('\n--- native-evidence.md lines touching root (%d) ---' % len(hits))
for n, l in hits:
    print('%5d  %s' % (n, l.strip()[:230]))
R['nativeEvidenceMdRootLines'] = [{'line': n, 'text': l.strip()} for n, l in hits]

# --- fault codes: does a root-specific code exist, and is it raised? ---
nem = open(os.path.join(F, 'native/native_evidence_model.v2.py'), encoding='utf-8').read()
enm = open(os.path.join(F, 'foundation/enumeration_model.v1.py'), encoding='utf-8').read()
codes = sorted(set(re.findall(r'[A-Z][A-Z0-9_]{6,}ROOT[A-Z0-9_]*', nem + enm)) |
               set(re.findall(r'[A-Z0-9_]*ROOT[A-Z0-9_]{4,}', nem + enm)))
R['rootFaultTokens'] = codes
print('\nroot-bearing fault tokens in native/enumeration models:', codes)
for c in codes:
    for src, name in ((nem, 'native_evidence_model.v2.py'), (enm, 'enumeration_model.v1.py')):
        for i, l in enumerate(src.splitlines(), 1):
            if c in l:
                print('  %-34s %s:%d  %s' % (c, name, i, l.strip()[:150]))

# --- execute: admission of a unit whose rootPath is the sentinel '.' ---
print('\n--- execution: does the model refuse rootPath="." at admission? ---')
spec = importlib.util.spec_from_file_location('nem27', os.path.join(F, 'native/native_evidence_model.v2.py'))
NEM = importlib.util.module_from_spec(spec)
sys.modules['nem27'] = NEM
spec.loader.exec_module(NEM)
R['modelCallables'] = [n for n in dir(NEM) if 'root' in n.lower() or 'unit' in n.lower()][:40]
print('root/unit callables:', R['modelCallables'])
for nm in ('spell_root', '_internal_root', '_under_unit', '_rel'):
    fn = getattr(NEM, nm, None)
    if fn is None:
        print('  %s: absent' % nm)
        R.setdefault('helpers', {})[nm] = 'absent'
        continue
    import inspect
    try:
        src = inspect.getsource(fn)
    except Exception as ex:
        src = '<%s>' % ex
    print('\n  --- %s ---\n%s' % (nm, '\n'.join('    ' + x for x in src.splitlines()[:22])))
    R.setdefault('helpers', {})[nm] = src[:1400]

json.dump(R, open(os.path.join(OUT, 'pK-f04root.json'), 'w'), indent=1, default=str)
print('\nwrote pK-f04root.json')
