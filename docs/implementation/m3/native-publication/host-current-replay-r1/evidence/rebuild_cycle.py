from pathlib import Path
import ast,json,hashlib,copy,types
B=Path(__file__).resolve().parent;source=B/'rebuild_replay.py';tree=ast.parse(source.read_text());nodes=[]
for n in tree.body:
 if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='original'for t in n.targets):break
 nodes.append(n)
nodes.extend(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name in ['sub','rebuild_blob'])
g=types.ModuleType('current_shape_graph_authoring_definitions');g.__file__=str(source);exec(compile(ast.Module(body=nodes,type_ignores=[]),str(source),'exec'),g.__dict__)
P=g.P;W=g.W;rel='crates/evaluator/tests/fixtures/cycle-representative.v1.json';raw=(P/rel).read_bytes();f=json.loads(raw);records=[r for c in f['retainedCases']for r in c['objects']];blobs={k:{'digest':k,'hex':v}for k,v in f['retainedBlobPool'].items()};g.mapping={g.OLD:g.NEW}
for r in records:assert g.hid(r['domain'],r['descriptor'])==r['id']
for r in blobs.values():assert hashlib.sha256(bytes.fromhex(r['hex'])).hexdigest()==r['digest']
for iteration in range(len(records)+len(blobs)+1):
 changes={}
 for r in records:
  new=g.hid(r['domain'],g.order_identity(g.sub(r['descriptor'])))
  if new!=r['id']:changes[r['id']]=new;changes[r['id'].rsplit(':',1)[1]]=new.rsplit(':',1)[1]
 for r in blobs.values():
  new=hashlib.sha256(g.rebuild_blob(r)).hexdigest()
  if new!=r['digest']:changes[r['digest']]=new
 merged=dict(g.mapping,**changes)
 if merged==g.mapping:break
 g.mapping=merged
else:raise AssertionError('cycle graph did not settle')
new=g.sub(copy.deepcopy(f));new['retainedBlobPool']={hashlib.sha256(g.rebuild_blob(r)).hexdigest():g.rebuild_blob(r).hex()for r in blobs.values()}
for a,b in zip(f['retainedCases'],new['retainedCases']):
 assert a['label']==b['label']and a['expectedVerdict']==b['expectedVerdict']
 b['objects']=[dict(id=g.mapping.get(r['id'],r['id']),domain=r['domain'],descriptor=g.order_identity(g.sub(r['descriptor'])))for r in a['objects']]
assert new['cases']==f['cases']
out=W/'crates/evaluator/tests/fixtures/cycle-representative.current.v1.json';assert not out.exists();data=json.dumps(new,ensure_ascii=False,separators=(',',':')).encode()+b'\n';assert len(data)<=4*1024*1024;out.write_bytes(data);assert(P/rel).read_bytes()==raw and(W/rel).read_bytes()==raw
p=W/'crates/evaluator/src/atoms.rs';assert p.read_bytes()==(P/'crates/evaluator/src/atoms.rs').read_bytes();s=p.read_text();assert s.count('cycle-representative.v1.json')==2;p.write_text(s.replace('cycle-representative.v1.json','cycle-representative.current.v1.json'))
report=dict(standing='ISOLATED UNREVIEWED CURRENT SHAPE SYNTHETIC RETAINED CYCLE GRAPH',originalSha256=hashlib.sha256(raw).hexdigest(),currentSha256=hashlib.sha256(data).hexdigest(),originalBytes=len(raw),currentBytes=len(data),unchangedNonretainedCases=len(f['cases']),retainedCases=len(f['retainedCases']),objectRows=len(records),blobRows=len(blobs),settledRound=iteration,identityReferencesChanged=len(g.mapping),historicalBytesUnchanged=True,expectedVerdictsAndLabelsPreserved=True,parserLimitUnchanged=True,semanticRegistrationClaimed=False,testsPassed=False);(B/'cycle-rebuild.json').write_text(json.dumps(report,indent=2)+'\n');(B/'cycle-identity-map.json').write_text(json.dumps(g.mapping,indent=2)+'\n');print(json.dumps(report,indent=2))
