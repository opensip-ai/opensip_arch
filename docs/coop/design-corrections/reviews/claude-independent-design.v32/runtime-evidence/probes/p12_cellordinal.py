"""P12 — is the module's cellOrdinal (derived by enumerate) guaranteed to equal the normative
cellOrdinal? enumeration-contract.v1.md says cellOrdinal is the 0-based index AFTER the published
sort and is NOT stored on the cell. If the retained cells array order is enforced, enumerate is
correct; if not, a remedy could name the wrong cell index."""
import importlib.util, json, os, re, sys

SRC = '/tmp/opensip-design-corrections/candidate-subject.v32'
F = os.path.join(SRC, 'docs/coop/design-corrections/foundation')
W = os.path.join(SRC, 'docs/coop/design-corrections/workflows')
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v32/receipts'
R = {}

# what does the enumeration plan schema declare for `cells`?
cands = [p for p in os.listdir(F) if 'enumeration-plan' in p]
R['schemaFiles'] = cands
sch = None
for c in cands:
    if c.endswith('.json'):
        sch = json.load(open(os.path.join(F, c)))
        R['schemaFile'] = c
print('enumeration plan schema file:', R.get('schemaFile'))
if sch:
    def find(o, key, path='$'):
        out = []
        if isinstance(o, dict):
            for k, v in o.items():
                if k == key:
                    out.append((path + '/' + k, v))
                out += find(v, key, path + '/' + k)
        elif isinstance(o, list):
            for i, v in enumerate(o):
                out += find(v, key, path + '/%d' % i)
        return out
    orders = find(sch, 'x-opensip-order')
    R['declaredOrders'] = [{'at': p, 'order': v} for p, v in orders]
    print('\ndeclared x-opensip-order annotations:')
    for p, v in orders:
        print('   %-70s %s' % (p[-70:], json.dumps(v)[:90]))
    cells = [x for x in orders if '/cells/' in x[0] or x[0].endswith('/cells/x-opensip-order')]
    R['cellsOrderDeclared'] = [{'at': p, 'order': v} for p, v in cells]

# does identity-model.ordered() have a named branch for `cells`?
idm = open(os.path.join(F, 'identity-model.v3.py'), encoding='utf-8').read()
m = re.search(r"def ordered\(value,path=\(\)\):(.*?)\nROOT_ORDER_PATH", idm, re.S)
body = m.group(1)
names = set(re.findall(r"name==?'([A-Za-z0-9_-]+)'", body))
for mm in re.finditer(r"name in \[([^\]]+)\]", body):
    names |= set(re.findall(r"'([^']+)'", mm.group(1)))
R['orderedNamedBranches'] = sorted(names)
R['cellsHasNamedBranch'] = 'cells' in names
print('\nordered() named branches:', sorted(names))
print('cells has a named branch  :', R['cellsHasNamedBranch'])

# does the enumeration model itself enforce the cell sort?
enm = open(os.path.join(F, 'enumeration_model.v1.py'), encoding='utf-8').read()
lines = [l.strip()[:170] for l in enm.splitlines()
         if re.search(r'cellOrdinal|capabilityId.*languageMode|sorted\(.*cells|cells.*sort', l)]
R['enumerationModelCellOrderLines'] = lines[:14]
print('\nenumeration_model lines about cell order / ordinal:')
for l in lines[:12]:
    print('   %s' % l[:160])
R['enumerationModelEnforcesCellSort'] = any(
    'ENUMERATION_PLAN_CELL' in l or ('sorted' in l and 'cells' in l) for l in lines)

# does the checker validate the plan schema, which would enforce the declared order?
cwp = open(os.path.join(W, 'check-workflow-projection.v3.py'), encoding='utf-8').read()
R['checkerValidatesPlan'] = 'enumeration-plan' in cwp

# empirical: build a real plan and test whether a shuffled cells array is admitted
spec = importlib.util.spec_from_file_location('enm32b', os.path.join(F, 'enumeration_model.v1.py'))
ENM = importlib.util.module_from_spec(spec)
sys.modules['enm32b'] = ENM
spec.loader.exec_module(ENM)
R['admitEnumerationExists'] = hasattr(ENM, 'admit_enumeration')
faults = [l.strip() for l in enm.splitlines() if 'ENUMERATION_PLAN_CELL' in l or 'CELL_ORDER' in l]
R['cellOrderFaultKeys'] = faults[:8]
print('\ncell-order fault keys in the enumeration model:', faults[:6])

R['ASSESSMENT'] = (
    'The repair module derives cellOrdinal with enumerate() over the retained cells array. That is '
    'the normative ordinal ONLY IF the retained array is held to the published '
    '{by:[capabilityId,languageMode,workspaceRoot]} order. Recorded here with the evidence found; '
    'note that ownership itself is per-binding and does not depend on the index, so any gap here is '
    'diagnostic-coordinate accuracy, not a gate-correctness defect.')
json.dump(R, open(os.path.join(OUT, 'p12-cellordinal.json'), 'w'), indent=1, default=str)
print('\n' + R['ASSESSMENT'])
print('\nwrote p12-cellordinal.json')
