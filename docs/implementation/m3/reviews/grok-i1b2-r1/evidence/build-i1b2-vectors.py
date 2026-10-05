from pathlib import Path
import sys,importlib.util,json,hashlib,copy
arch=Path('/Users/sb/code/opensip-ai/opensip_arch')
root=Path('/Users/sb/code/opensip-ai/opensip-i1b2')
sys.path.insert(0,'/tmp/opensip-implementation/reviews/codex2-i1-l-r1/deps')
def module(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sys.modules[name]=m;sp.loader.exec_module(m);return m
base=arch/'docs/implementation/m3/preview-pack-i1/i1-l/evidence'
M=module('i1_model',base/'cycle_representative_model.py')
# Execute the checker with the four accepted follow-up precisions in a temporary copy.
s=(base/'check_cycle_representative.py').read_text()
insert=Path('/tmp/opensip-implementation/reviews/codex2-i1-l-r1/suggested-case-insertion.txt').read_text()
s=s.replace('\ndef op_law_cases(M):',insert+'\ndef op_law_cases(M):')
ns={'__file__':str(base/'check_cycle_representative.py'),'__name__':'i1_cases'};exec(compile(s,str(base/'check_cycle_representative.py'),'exec'),ns)
canon=lambda v:M.C.encode(v)
# The encoder's public name is obtained from the model's own cset implementation below.
C=M.C
print([k for k in vars(C) if 'encod' in k])

def universe(s):return s.encode().hex().ljust(64,'0') if s else None
closure='closure2:'+'c'*64
snapshot='snapshot2:'+'d'*64
cases=[]
for name,source,old,rule,expect in ns['cases'](M):
 result=M.evaluate_rule(rule,old)
 inp={'facts':{},'inventories':[],'scopes':{},'coverages':{},'coverageScopes':{},'enumerationPlan':{'cells':[]},'closures':{closure:{'kind':'provider'}},'targetAttributions':{},'universeDomains':{}}
 selected=[{'universe':universe(s['universe']),'kind':'file','row':{'path':s['path'],'nativeSubjectId':s['path']}} for s in old['selected']]
 def inventory(inv,ci,pi,kind=None,extra=None):
  v=copy.deepcopy(inv);v['universe']=universe(v['universe']);v['cellOrdinal']=ci;v['programOrdinal']=pi
  for row in v['rows']:row['kind']=v['kind']
  inp['inventories'].append(v)
 for ci,b in enumerate(old['bindings']):
  family={'typescript':'ts-tsconfig','rust':'rust-cargo','syntax':'syntax-only'}.get(b['family'],'ts-tsconfig')
  inp['enumerationPlan']['cells'].append({'capabilityId':'imports','languageMode':family,'required':b.get('required',True),'programBindings':[{'ordinal':0,'universe':universe(b['universe'])}]})
  for inv_id in b['inventories']:inventory(old['inventories'][inv_id],ci,0)
  if b['universe']:inp['universeDomains'][universe(b['universe'])]='native.semantic-universe.typescript.v2'
 # Unbound inventory observations still participate in P3, with unmatched locators.
 seen_ids={i for b in old['bindings'] for i in b['inventories']}
 for inv_id,inv in old['inventories'].items():
  if inv_id not in seen_ids:inventory(inv,1000,len(inp['inventories']))
 # Retained file/package rows make reconciled host occupancy explicit.
 extra_rows={}
 for s in old['selected']:extra_rows.setdefault(s['universe'],{}).setdefault('file',set()).add(s['path'])
 for fact in old['facts']:
  if fact['relation']!='imports':continue
  attr=fact.get('attribution')
  if attr and attr['occupancy']=='first-party' and attr['kind'] in ('file','package'):
   extra_rows.setdefault(fact['targetUniverse'],{}).setdefault(attr['kind'],set()).add(attr['evaluationNativeId'])
 for u,kinds in extra_rows.items():
  for kind,ids in kinds.items():
   rows=[{'nativeSubjectId':i,'path': i if kind=='file' else 'package/package.json','kind':kind} for i in ids]
   inp['inventories'].append({'universe':universe(u),'cellOrdinal':1000,'programOrdinal':1000,'kind':kind,'state':'complete','rows':rows})
 for sid,sc in old['scopes'].items():
  inp['scopes'][sid]={'schemaVersion':2,'snapshotId':snapshot,'enumeratorClosure':closure,**copy.deepcopy(sc)}
  inp['scopes'][sid]['sourceUniverse']=universe(sc['sourceUniverse']);inp['scopes'][sid]['targetUniverse']=universe(sc['targetUniverse'])
 for cid,cov in old['coverages'].items():
  answer=cov['sufficiency'];ok=answer['satisfied']
  inp['coverageScopes'][cid]=cov['scopeId']
  inp['coverages'][cid]={'key':{'relation':'imports','resolution':'resolved-target','sourceUniverse':universe(cov['sourceUniverse']),'targetUniverse':universe(cov['targetUniverse'])},'entry':{'resolution':'resolved-target','coverage':'complete','confidenceMillionths':1000000,'resolutionCompleteness':{'state':'complete' if ok else 'partial','examinedExhaustive':ok,'unresolvedEdgeCount':0 if ok else 1,'unresolvedEdgeClasses':[] if ok else ['unresolved-specifier']},'closedWorld':{'state':'not-applicable'},'deficiency':None,'nativeCause':answer['nativeCause']}}
 for fact in old['facts']:
  fid=fact['id'];v={'factId':fid,'relation':fact['relation'],'sourceUniverse':universe(fact['sourceUniverse']),'producerClosure':closure}
  if fact['relation']=='unresolved-edge':v['payload']={'relation':fact['payloadRelation'],'referrer':fact['referrer']}
  else:
   attr=fact.get('attribution');native=attr['evaluationNativeId'] if attr and attr['occupancy']=='first-party' else '@unplaced-target'
   v.update(resolution=fact['resolution'],targetUniverse=universe(fact['targetUniverse']),payload={'importer':fact['importer'],'resolvedTarget':native})
   if attr and attr['occupancy']=='external':
    inp['targetAttributions'][fid]={'sourceFactId':fid,'producerClosure':closure,'targetUniverse':universe(fact['targetUniverse']),'targetNativeId':native,'occupancy':'external','kind':'file','evaluationNativeId':None,'logicalPath':None,'exported':None,'packageManifestPath':None}
  inp['facts'][fid]=v
 expected=[]
 for r in result['subjects']:
  expected.append({'universe':universe(r['universe']),'path':r['path'],'value':'indeterminate' if r['value']=='unknown' else r['value'],'matchingFactIds':r['matchingFactIds'],'uncertainFactIds':r['uncertainFactIds'],'coverageIds':r['coverageIds'],'scopeIds':r['scopeIds'],'causes':[{**c,'universe':universe(c['universe'])} if c.get('universe') else c for c in r['causes']],'nativeDeficiencies':r['nativeDeficiencies']})
 cases.append({'label':name,'source':source,'selected':selected,'evidence':inp,'expected':expected})
out={'standing':'Synthetic already-admitted I1-L graph and census oracle cases; retained owner admission and full replay are tested separately. Native sufficiency is computed by the product, never supplied as a truth map.','cases':cases}
path=root/'crates/evaluator/tests/fixtures/cycle-representative.v1.json'
path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(len(cases),path.stat().st_size)
