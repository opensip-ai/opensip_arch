"""Bounded construction loader for focused discriminating controls.

Root's diagnostic instrument extracts a fixed 54-definition set of fixture constructors out of
check-identity.py by AST and executes them as a standalone module, so a probe pays for the
constructors it needs instead of the whole 1133-call checker. This is the same technique, with two
differences: the extracted module is written to a DISPOSABLE path and never into the released work
tree, and the loader records the exact source hashes it read.

It is an instrument, not accepted source."""
import ast,hashlib,importlib.util,json,pathlib,sys

NAMES=set(ast.literal_eval(ast.parse(pathlib.Path(
    '/tmp/opensip-design-corrections/codex-post-reset.v1/adapt-integration-builder-v13.py'
).read_text()).body[next(i for i,n in enumerate(ast.parse(pathlib.Path(
    '/tmp/opensip-design-corrections/codex-post-reset.v1/adapt-integration-builder-v13.py'
).read_text()).body) if isinstance(n,ast.Assign) and any(
    getattr(t,'id','')=='names' for t in n.targets))].value))

PRELUDE='''import copy,hashlib,json,importlib.util,re
from pathlib import Path
H=Path(__file__).resolve().parent/'foundation'
spec=importlib.util.spec_from_file_location('bounded_identity',H/'identity-model.py')
M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
C=M.C
W=M.workflow_admission()
spec=importlib.util.spec_from_file_location('bounded_native',H.parent/'native/native_evidence_model.v2.py')
N=importlib.util.module_from_spec(spec);spec.loader.exec_module(N)
NATIVE_FIXTURES=json.loads((H.parent/'native/native-cases.v2.json').read_text())['fixtures']
'''

def load(work,tag='bounded'):
    """Extract the fixture constructors out of `work`'s check-identity.py and import them.

    `work` is a design-corrections directory. The generated module is written beside it ONLY when
    that directory is itself disposable; callers pass a disposable copy. Returns (module, hashes)."""
    dc=pathlib.Path(work)
    source=dc/'foundation/check-identity.py'
    raw=source.read_text();tree=ast.parse(raw)
    blocks=[];found=set()
    for n in tree.body:
        declared=({n.name} if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))
                  else ({t.id for t in n.targets if isinstance(t,ast.Name)} if isinstance(n,ast.Assign) else set()))
        hit=NAMES&declared
        if hit:blocks.append(ast.get_source_segment(raw,n));found|=hit
    missing=NAMES-found
    if missing:raise RuntimeError('bounded loader could not find: '+','.join(sorted(missing)))
    target=dc/('bounded-fixtures.%s.py'%tag)
    target.write_text(PRELUDE+'\n\n'.join(blocks)+'\n')
    spec=importlib.util.spec_from_file_location('bounded_fixtures_'+tag,target)
    mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    hashes={str(p.relative_to(dc)):sha(p) for p in [
        source,dc/'foundation/identity-model.py',dc/'foundation/identity-schemas.v2.json',
        dc/'foundation/relation-payload-schemas.v2.json',dc/'native/native_evidence_model.v2.py',
        dc/'native/native-evidence.schemas.v2.json',dc/'native/native-capability-matrix.v2.json']}
    return mod,hashes
