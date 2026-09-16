from pathlib import Path
import json,hashlib,importlib.util
B=Path('/tmp/opensip-design-corrections');S=B/'candidate-subject.v32';O=B/'root-blind18-canonical-vectors.v1';assert not O.exists();O.mkdir();sha=lambda b:hashlib.sha256(b).hexdigest();mf=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v32.json');assert sha(mf.read_bytes())=='3897e8d1bb389f3d39669997d3078d5a44fa024f29d97bd17854a48916610bf2';members={r['path']:r for r in json.loads(mf.read_bytes())['files']};rel='docs/coop/design-corrections/foundation/canonical.py';p=S/rel;assert sha(p.read_bytes())==members[rel]['sha256'];sp=importlib.util.spec_from_file_location('root_canonical32',p);C=importlib.util.module_from_spec(sp);sp.loader.exec_module(C)
inputs={}
for n in ['phase1-canonical-h-lexical.json','cve1-eight-types.json']:
 raw=(B/'consumer-b.v18/output/vectors'/n).read_bytes();(O/n).write_bytes(raw);inputs[n]={'sha256':sha(raw),'bytes':len(raw)}
d=json.loads((O/'phase1-canonical-h-lexical.json').read_bytes());checks=[]
def check(n,ok,detail=None):checks.append({'id':n,'passed':bool(ok),'detail':detail})
for row in d['R-H-HELPER']:
 k=row['kind']
 if k in ['canonical-record','escape-and-key-order']:
  raw=C.canonical(row['value']);check(k,raw.decode()==row['cBytes'] and len(raw)==row['cByteLength'] and sha(raw)==row['rawSha256OfC'])
 elif k=='array-admitted-order-preserved':check(k,C.canonical(row['valueA']).decode()==row['cA'] and C.canonical(row['valueB']).decode()==row['cB'] and C.canonical(row['valueA'])!=C.canonical(row['valueB']))
 elif k=='h-frame':check(k,C.identity('closure',row['value'])==row['H'] and row['typedId']=='closure2:'+row['H'])
 elif k=='integer-bound':
  try:raw=C.canonical({'n':int(row['n'])});ok=True
  except C.AdmissionError:ok=False
  check(k+':'+row['n'],ok==row['accepted'])
for row in d['R-LEXICAL-ADMISSION+R-RAW-VS-PARSED']['rawInputNegatives']:
 raw=bytes.fromhex(row['rawInputHex'])
 try:C.parse(raw);refused=False;reason=None
 except C.AdmissionError as e:refused=True;reason=str(e)
 check('raw:'+row['case'],refused,{'rootRefusal':reason,'consumerRefusal':row['firstRefusal'],'scope':'Refusal of retained hex only. Internal codes/precedence need not match; truncated diagnostic inputs are not original execution bytes.'})
op=d['R-SEMANTIC-VS-OPERATIONAL'];a=op['runDescriptor'];b=dict(a);b[op['semanticFieldChange']['field']]=op['semanticFieldChange']['newValue'];check('semantic-run-frame','run3:'+C.identity('run',a)==op['runId'] and 'run3:'+C.identity('run',b)==op['semanticFieldChange']['newRunId'] and a!=b)
# Positive CVE1 vectors can be checked directly from their declared eight type encodings;
# do not claim this small encoder replays absent negative-input bytes or whole capability admission.
def enc(v):
 if v is None:return b'\0'
 if v is False:return b'\1'
 if v is True:return b'\2'
 if type(v) is int:return (b'\3'+v.to_bytes(8,'big')) if v>=0 else b'\7'+v.to_bytes(8,'big',signed=True)
 if type(v) is str:
  b=v.encode();return b'\4'+len(b).to_bytes(4,'big')+b
 if type(v) is list:return b'\5'+len(v).to_bytes(4,'big')+b''.join(enc(x) for x in v)
 if type(v) is dict:return b'\6'+len(v).to_bytes(4,'big')+b''.join(enc(k)+enc(v[k]) for k in sorted(v,key=lambda x:x.encode()))
 raise ValueError(type(v))
for row in json.loads((O/'cve1-eight-types.json').read_bytes())['roundTrips']:
 if 'value' in row:raw=enc(row['value']);check('cve1:'+row['type'],raw.hex()==row['encodedHex'] and len(raw)==row['encodedLength'] and C.equal_typed(row['value'],row['decoded']))
order=d['R-ACYCLIC-JOINS']['derivationOrder'];edges=d['R-ACYCLIC-JOINS']['declaredForwardEdges'];alias={'plan2':'plan','snapshot2':'snapshot','view2':'view','fact2':'fact','scope2':'subject-scope','coverage2':'coverage','proof3':'proof-bundle','evidence3':'semantic-evidence','seal3':'evaluation-seal','exec-plan2':'execution-plan','closure2':'closures'};viol=[]
for name,refs in edges.items():
 if name not in order:continue
 for r in refs:
  dep=alias.get(r)
  if dep in order and order.index(dep)>order.index(name):viol.append({'record':name,'dependsOn':dep,'recordIndex':order.index(name),'dependencyIndex':order.index(dep)})
record={'standing':'Root bounded assessment of captured18 canonical/CVE1 vector bytes using exact source32 canonical owner and direct prescribed positive CVE1 encodings. Not final19 acceptance, full charter audit or graph admission. Not supplied to blind consumer.','inputs':inputs,'sourceManifestSha256':sha(mf.read_bytes()),'ownerSha256':sha(p.read_bytes()),'checks':checks,'passed':all(r['passed'] for r in checks),'pendingDescriptiveRecordCorrection':{'artifact':'phase1-canonical-h-lexical.json#/R-ACYCLIC-JOINS/derivationOrder','violationsOfItsOwnDeclaredDependencyOrder':viol,'scope':'The declared graph can be acyclic while this displayed construction order is not topological. Actual Run construction/admission is assessed separately. Recheck final19bytes before carrying this stale explanatory-order discrepancy; no normative design defect inferred.'},'limits':['CVE1 negative inputs not replayed: their source values are not all retained in this standalone report.','No current Run/receipt schema or closure admission from the illustrative H records.','Raw diagnostic hex may be truncated; root refusal does not authenticate original first-boundary claim.']};(O/'assessment.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({'checks':len(checks),'passed':record['passed'],'descriptiveOrderViolations':viol}));assert record['passed']
