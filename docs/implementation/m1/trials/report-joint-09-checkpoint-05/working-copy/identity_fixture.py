"""Fresh verified parent/successor reference trees for composed identity checks."""
from pathlib import Path
from contextlib import contextmanager
import hashlib,importlib.machinery,json,tempfile,types
HERE=Path(__file__).resolve().parent

def load_local(name):
 p=HERE/(name+'.py');m=types.ModuleType(name);m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m

@contextmanager
def models(validation,bridge):
 V=validation;B=bridge;R=load_local('retained_fixture')
 with R.world(V.read_unit,V.subjects) as parent,tempfile.TemporaryDirectory(prefix='opensip-joint09-identity-') as name:
  scratch=Path(name).resolve();expected={}
  for rel in json.loads(V.read_unit('history-selection','fixture-owner-files.json'))['files']:
   target=scratch/rel;target.parent.mkdir(parents=True,exist_ok=True)
   raw=parent['by_path'][str(parent['ARCH']/rel)];target.write_bytes(raw);expected[rel]=raw
  schema=(HERE/'composed-sources/identity.proposed.v3.schema.json').read_bytes();model=(HERE/'models/identity_model.proposed.v3.py').read_bytes();parameter=(HERE/'composed-sources/framework-recognition-plan.schema.v1.json').read_bytes()
  assert parameter==V.read_unit('report-evidence-design','owner/framework-recognition-plan.schema.v1.json')
  assert json.loads(schema)==json.loads(B.successor_identity_schemas(expected[B.DC+'foundation/identity-schemas.v3.json']))
  assert model==B.transform(expected[B.DC+'foundation/identity-model.v3.py'].decode(),B.OWNER_TRANSFORMS).encode()
  for rel,raw in [(B.DC+'foundation/identity-schemas.v3.json',schema),(B.DC+'foundation/identity-model.v3.py',model),(B.DC+B.PARAMETER_DOCUMENT,parameter)]:
   (scratch/rel).write_bytes(raw);expected[rel]=raw
  prior=importlib.machinery.SourceFileLoader.get_code;compiled=[]
  def verified(loader,fullname):
   path=Path(loader.path).resolve()
   if path.is_relative_to(scratch):
    rel=str(path.relative_to(scratch));raw=path.read_bytes();assert raw==expected[rel];compiled.append(rel);return compile(raw,str(path),'exec')
   return prior(loader,fullname)
  importlib.machinery.SourceFileLoader.get_code=verified
  try:
   foundation=scratch/B.DC/'foundation'
   ordinary=parent['load']('joint09_successor_fixture',foundation/'evaluator_graph_fixture.v3.py')
   replay=parent['load']('joint09_successor_replay',foundation/'evaluator_replay_model.v3.py')
   rel=B.DC+'foundation/evaluator_graph_fixture.v3.py';changed=B.transform(expected[rel].decode(),B.FIXTURE_TRANSFORMS).encode();expected[rel]=changed;(scratch/rel).write_bytes(changed)
   extended=parent['load']('joint09_successor_extended_fixture',scratch/rel)
   successor=types.SimpleNamespace(F=ordinary,Fx=extended,R=replay,root=scratch,expected=expected,compiled=compiled,load=parent['load'])
   yield parent,successor
   assert B.DC+'foundation/identity-model.v3.py' in compiled,'selected identity source verification must execute'
  finally:importlib.machinery.SourceFileLoader.get_code=prior
