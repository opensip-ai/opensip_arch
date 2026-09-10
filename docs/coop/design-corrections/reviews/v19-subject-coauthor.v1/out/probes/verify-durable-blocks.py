"""Verify the two proposed durable blocks WITHOUT rerunning either suite.

Two independent guarantees:
  1. NAME RESOLUTION - every module-level free name each block references is actually bound by its
     target checker (collected statically from that checker's own module-level assignments, defs,
     imports and comprehension targets). This is what catches a block that would NameError.
  2. EXECUTION - each block is exec'd against a faithful namespace built from the real modules, so
     its assertions are really evaluated. The blocks report through `check`, so a failing assertion
     shows up as a failing row rather than an exception.
No suite report is produced and no pin is touched.
"""
import ast
import builtins
import importlib.util
import json
import pathlib
import sys

ROOT = pathlib.Path('/tmp/opensip-design-corrections/v19-subject-coauthor.v1')
DC = pathlib.Path('/tmp/opensip-design-corrections/v19-native-coauthor.v1/work/docs/coop/design-corrections')
PROPOSED_DC = ROOT / 'out/disposable/dc-proposed'

out = {'nameResolution': {}, 'execution': {}}


def bound_names(path):
    """Module-level names a file binds: imports, defs, classes, assignments, for/with targets."""
    tree = ast.parse(pathlib.Path(path).read_text(encoding='utf-8'))
    names = set()

    def add_target(t):
        for node in ast.walk(t):
            if isinstance(node, ast.Name):
                names.add(node.id)

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, ast.Import):
            for a in node.names:
                names.add(a.asname or a.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            for a in node.names:
                names.add(a.asname or a.name)
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                add_target(t)
        elif isinstance(node, (ast.AnnAssign, ast.AugAssign)):
            add_target(node.target)
        elif isinstance(node, (ast.For, ast.AsyncFor)):
            add_target(node.target)
        elif isinstance(node, ast.With):
            for item in node.items:
                if item.optional_vars is not None:
                    add_target(item.optional_vars)
        elif isinstance(node, (ast.If, ast.Try)):
            for sub in ast.walk(node):
                if isinstance(sub, ast.Assign):
                    for t in sub.targets:
                        add_target(t)
                elif isinstance(sub, (ast.FunctionDef, ast.ClassDef)):
                    names.add(sub.name)
    return names


def free_names(path):
    """Names a block READS without binding them ANYWHERE in itself.

    A block binds inside for-bodies, try-bodies and its own functions too, so unlike `bound_names`
    - which answers the different question of what a TARGET module exposes at module level - this
    walks the whole tree. An earlier revision reused the module-level collector here and reported
    six of the block's own locals as unresolved.
    """
    tree = ast.parse(pathlib.Path(path).read_text(encoding='utf-8'))
    read = set()
    bound = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store)}
    bound |= {n.name for n in ast.walk(tree)
              if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            read.add(node.id)
        if isinstance(node, (ast.FunctionDef, ast.Lambda)):
            for a in node.args.args + node.args.kwonlyargs:
                bound.add(a.arg)
        if isinstance(node, ast.comprehension):
            for n in ast.walk(node.target):
                if isinstance(n, ast.Name):
                    bound.add(n.id)
        if isinstance(node, ast.ExceptHandler) and node.name:
            bound.add(node.name)
    return {n for n in read - bound if not hasattr(builtins, n)}


for block, target in (('checks/check_workflows.subject.block.py', 'workflows/check_workflows.v1.py'),
                      ('checks/check_integration.subject.block.py', 'check-integration.py')):
    needed = free_names(ROOT / block)
    have = bound_names(DC / target)
    missing = sorted(needed - have)
    out['nameResolution'][block] = {'target': target, 'needs': sorted(needed),
                                    'missingInTarget': missing, 'resolves': not missing}

# --------------------------------------------------------------------------------- execution
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


W = load('verify_wf', PROPOSED_DC / 'workflows/workflows_model.v1.py')
HOST = load('verify_host', PROPOSED_DC / 'integration-host-model.py')
assert HOST.W is not None and HOST.N is not None

# --- workflows checker namespace: check / must_valid / must_invalid / M / U, built the same way
import glob                                                                     # noqa: E402
from jsonschema import Draft202012Validator                                     # noqa: E402
from referencing import Registry, Resource                                      # noqa: E402
from referencing.jsonschema import DRAFT202012                                  # noqa: E402

canonical = load('verify_canonical', DC / 'foundation/canonical.py')
SCHEMAS = {}
for p in sorted(glob.glob(str(DC / 'workflows/schemas/*.schema.json'))):
    s = canonical.parse(pathlib.Path(p).read_bytes())
    Draft202012Validator.check_schema(s)
    SCHEMAS[s['$id']] = s
FOUNDATION = canonical.parse((DC / 'foundation/identity-schemas.v2.json').read_bytes())
REG = Registry().with_resources(
    [(k, Resource(contents=v, specification=DRAFT202012)) for k, v in SCHEMAS.items()]
    + [(FOUNDATION['$id'], Resource(contents=FOUNDATION, specification=DRAFT202012))])


def run_block(block, namespace, rows):
    src = (ROOT / block).read_text(encoding='utf-8')
    try:
        exec(compile(src, str(ROOT / block), 'exec'), namespace)               # noqa: S102
    except Exception as exc:                                                    # noqa: BLE001
        return {'raised': repr(exc)[:400], 'rows': rows}
    return {'raised': None, 'rows': rows}


rows_a = []
def check_a(cid, ok, detail=''):
    rows_a.append({'id': cid, 'ok': bool(ok), 'detail': detail if not ok else ''})
    return ok


def valid_a(ref, value):
    sid, _, frag = ref.partition('#')
    try:
        canonical.typed(value)
        canonical.ExactValidator({'$ref': sid + '#' + frag} if frag else {'$ref': sid},
                                 registry=REG).validate(value)
        return True, ''
    except Exception as e:                                                      # noqa: BLE001
        return False, str(e).splitlines()[0][:200]


ns_a = {'check': check_a, 'M': W, 'U': 'urn:opensip:product-v1:workflows:',
        'must_valid': lambda cid, ref, v: check_a(cid, *(lambda r: (r[0], r[1]))(valid_a(ref, v))),
        'must_invalid': lambda cid, ref, v: check_a(cid, not valid_a(ref, v)[0], 'unexpectedly valid')}
out['execution']['checks/check_workflows.subject.block.py'] = run_block(
    'checks/check_workflows.subject.block.py', ns_a, rows_a)

rows_b = []
def check_b(name, condition):
    rows_b.append({'id': name, 'ok': bool(condition), 'detail': ''})


ns_b = {'check': check_b, 'M': HOST}
out['execution']['checks/check_integration.subject.block.py'] = run_block(
    'checks/check_integration.subject.block.py', ns_b, rows_b)

# DISCRIMINATION. A control that passes against the unpatched model would prove nothing, so both
# blocks are re-run against the BEFORE model and are required to FAIL there. (The first run of this
# verifier discovered the same thing by accident: `integration-host-model.py` calls
# Path(__file__).resolve(), which followed the shadow tree's symlink back to the unpatched module,
# so the block was silently graded against the wrong bytes. Both shadow trees now hold a real copy
# of that file, and this section makes the negative deliberate.)
BEFORE_DC = ROOT / 'out/disposable/dc-before'
W_BEFORE = load('verify_wf_before', BEFORE_DC / 'workflows/workflows_model.v1.py')
HOST_BEFORE = load('verify_host_before', BEFORE_DC / 'integration-host-model.py')
neg = {}
for label, block, ns in (
        ('checks/check_workflows.subject.block.py', 'checks/check_workflows.subject.block.py',
         dict(ns_a, M=W_BEFORE)),
        ('checks/check_integration.subject.block.py', 'checks/check_integration.subject.block.py',
         dict(ns_b, M=HOST_BEFORE))):
    rows = []
    if 'workflows' in label:
        ns['check'] = lambda cid, ok, detail='', _r=rows: _r.append({'id': cid, 'ok': bool(ok)})
        ns['must_valid'] = lambda cid, ref, v, _r=rows: _r.append(
            {'id': cid, 'ok': valid_a(ref, v)[0]})
        ns['must_invalid'] = lambda cid, ref, v, _r=rows: _r.append(
            {'id': cid, 'ok': not valid_a(ref, v)[0]})
    else:
        ns['check'] = lambda name, condition, _r=rows: _r.append({'id': name, 'ok': bool(condition)})
    res = run_block(block, dict(ns), rows)
    neg[label] = {'raised': res['raised'],
                  'failedAgainstBeforeModel': [r['id'] for r in rows if not r['ok']],
                  'passedAgainstBeforeModel': [r['id'] for r in rows if r['ok']]}
    neg[label]['discriminates'] = bool(neg[label]['failedAgainstBeforeModel'])
out['discriminationAgainstBeforeModel'] = neg

for block, res in out['execution'].items():
    res['passed'] = sum(1 for r in res['rows'] if r['ok'])
    res['failed'] = [r for r in res['rows'] if not r['ok']]

out['note'] = ('Namespaces are reconstructed faithfully from the real modules; neither suite was '
               'run and no report or pin was written. The workflows namespace rebuilds the same '
               'schema registry that checker builds.')
(ROOT / 'out/evidence/durable-block-verification.json').write_text(
    json.dumps(out, indent=1) + '\n', encoding='utf-8')
print(json.dumps({b: {'resolves': v['resolves'], 'missing': v['missingInTarget']}
                  for b, v in out['nameResolution'].items()}, indent=1))
print(json.dumps({b: {'discriminates': v['discriminates'],
                      'failsOnBefore': len(v['failedAgainstBeforeModel'])}
                  for b, v in out['discriminationAgainstBeforeModel'].items()}, indent=1))
print(json.dumps({b: {'raised': v['raised'], 'passed': v['passed'],
                      'failed': [r['id'] for r in v['failed']]}
                  for b, v in out['execution'].items()}, indent=1))
