"""AUTHOR construction from synthetic source inputs and frozen reference helpers.

This is neither independent reconstruction nor a repair of received review exports.
New synthetic scopes/coverage are explicit fixture assertions, not compiler evidence.
Final proof is derived by the frozen reference; a separate process validates exports.
"""
from pathlib import Path
import copy,importlib.util,json,sys,tomllib,traceback
ROOT=Path(__file__).resolve().parent;F=ROOT.parent/'candidate-subject.v25/docs/coop/design-corrections/foundation'
sys.path.insert(0,str(ROOT/'output'))
from helpers import runs,builder,h,order,store

def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
T=load('author_transport',ROOT.parent/'check-blind13-exported-graphs.v4.py')
R=load('author_replay',F/'evaluator_replay_model.v3.py');M=R.M;E=R.E;C=M.C
X=load('author_capture',F/'execution_inputs_fixture.v3.py');S=load('author_seed',F/'evaluator_semantic_fixture.v3.py')

def language(p):
 for suffix,lang in [('.rs','rust'),('.ts','typescript'),('.json','json'),('.toml','toml'),('.md','markdown')]:
  if p.endswith(suffix):return lang
 return 'unspecified'

def finalizer(st,**kw):
 
 for content in [builder.REL_BYTES,builder.NAT_BYTES,builder.POL_V2_BYTES,builder.POL_V1_BYTES,builder.IMP_BYTES,builder.ENUM_PLAN_BYTES,builder.EMIT_PLAN_BYTES,builder.ATTR_V2_BYTES]:st.put_blob(content)
 name=kw['name'];plan=copy.deepcopy(kw['plan']);snap=kw['snap'];snapid=kw['snap_id'];source={r['path']:st.blobs[r['sha256']] for r in snap['sourceInventory']};paths=sorted(source)
 raw=lambda d:json.loads(st.blobs[d]);blob=lambda v:st.put_raw_digest_record(v)
 spec=copy.deepcopy(raw(plan['analysisSpecDigest']));enum=copy.deepcopy(next(raw(p['payloadDigest']) for p in spec['parameters'] if p['schemaDigest']==builder.ENUM_PLAN_DIGEST));membership=copy.deepcopy(raw(enum['membershipDigest']))
 for unit in membership['units']:
  if unit['rootPath']=='.':unit['rootPath']=''
 enum['membershipDigest']=blob(membership)
 primary=enum['cells'][0]['programBindings'][0]['universe']
 if name=='rust' and SELECTION != 'default':
  candidates=[]
  for meta in st.frames.values():
   if meta['domain']!='native.semantic-universe.rust.v2':continue
   universe=st.objects[meta['identity']];own=st.objects[universe['sourceUnitOwnershipId']]
   selected=set(own['selectedUnitIds']);units=[u for u in own['units'] if u['unitId'] in selected]
   if (SELECTION=='bin' and any(u['targetKind']=='bin' for u in units)) or (SELECTION=='lib-only' and len(units)==1 and units[0]['targetKind']=='lib'):
    candidates.append(meta['identity'].split(':',1)[1])
  assert len(candidates)==1,(SELECTION,candidates)
  primary=candidates[0]
  for cell in enum['cells']:
   for binding in cell['programBindings']:binding['universe']=primary
 provider=enum['cells'][0]['programBindings'][0]['enumerator']['closureId']
 packages=[]
 for p in paths:
  if p.split('/')[-1]=='Cargo.toml':
   package=tomllib.loads(source[p].decode()).get('package',{});pkg=package.get('name')
  elif p.split('/')[-1]=='package.json':pkg=json.loads(source[p]).get('name')
  else:continue
  if pkg:packages.append((p,pkg))
 syms=[]
 for fact in kw['facts']:
  if fact['relation']=='declares':
   payload=fact['_payload'];p=fact['anchors'][0]['path'];syms.append({'nativeSubjectId':payload['declared'],'kind':'symbol','path':p,'qualifiedName':payload['declared'],'subjectLanguage':language(p),'signatureTokens':[],'projections':[],'exported':'unknown'})
 file_rows=[{'nativeSubjectId':p,'kind':'file','path':p,'qualifiedName':p,'subjectLanguage':language(p),'signatureTokens':[],'projections':[]} for p in paths]
 package_rows=[{'nativeSubjectId':pkg,'kind':'package','path':p,'qualifiedName':pkg,'subjectLanguage':language(p),'signatureTokens':[],'projections':[]} for p,pkg in packages]
 rows_by_kind={'file':file_rows,'package':package_rows,'symbol':syms}
 extents={'file':paths,'package':[p for p,_ in packages],'symbol':[p for p in paths if p.endswith(('.ts','.tsx','.rs','.js'))]}
 for cell in enum['cells']:
  for binding in cell['programBindings']:
   binding['programEntry']=None
   binding['extents']=[{'kind':k,'paths':extents[k]} for k in sorted(cell['kinds'])]
 ep=blob(enum)
 for p in spec['parameters']:
  if p['schemaDigest']==builder.ENUM_PLAN_DIGEST:p['payloadDigest']=ep
 for p in spec['parameters']:
  if p['schemaDigest']==builder.EMIT_PLAN_DIGEST:
   emission=copy.deepcopy(raw(p['payloadDigest']))
   by_rule={rule['ruleId']:rule for rule in kw['policy']['rules']}
   for rule in emission['rules']:
    rule.update({key:by_rule[rule['ruleId']]['ruleProgramRef'][key] for key in ['contributionId','ruleStableId','semanticsMajor']})
   p['payloadDigest']=blob(emission)
 plan['analysisSpecDigest']=blob(spec);planid=st.put_canonical_record('plan',plan)
 inventories=[];population={}
 for ci,cell in enumerate(enum['cells']):
  for bi,binding in enumerate(cell['programBindings']):
   for kind in cell['kinds']:
    rows=copy.deepcopy(rows_by_kind[kind]);rows.sort(key=lambda r:(r['nativeSubjectId'].encode(),r['path'].encode()))
    inv={'schemaVersion':1,'planId':planid,'parameterDigest':ep,'cellOrdinal':ci,'programOrdinal':bi,'kind':kind,'state':'complete','deficiency':None,'nativeCause':None,'examinedPaths':extents[kind],'rows':rows};inventories.append((blob(inv),inv))
    for row in rows:
     desc={'schemaVersion':3,'universe':binding['universe'],'kind':kind,'nativeSubjectId':row['nativeSubjectId']}
     if kind=='package':desc['packageManifestPath']=row['path']
     sid=st.put_canonical_record('evaluation-subject',desc);population[sid]={'subjectId':sid,'universe':binding['universe'],'kind':kind,'row':row,'collisionPopulationComplete':True}
 # Complete file enumeration for this synthetic fixture, including non-code files.
 facts=copy.deepcopy(kw['facts']);have={(f['sourceUniverse'],f['_payload'].get('path')) for f in facts if f['relation']=='file'}
 for p in paths:
  if (primary,p) not in have:
   f,_=runs.make_fact(st,snapid,'file','enumerated',primary,provider,runs.file_payload(p,source[p]),[]);facts.append(f)
 for p,pkg in packages:
  f,_=runs.make_fact(st,snapid,'package','manifest-declared',primary,provider,{'packageName':pkg,'packageVersion':'0.0.0','manifestPath':p},[]);facts.append(f)
 groups={}
 for fact in facts:
  key=(fact['sourceUniverse'],fact['relation'],fact['resolution'],fact['producerClosure'])
  if fact['relation']=='file':sub=fact['_payload']['path']
  elif fact['relation']=='clones':sub=fact['anchors'][0]['path']
  elif fact['relation']=='declares':sub=fact['_payload']['declared']
  elif fact['relation']=='package':sub=fact['_payload']['packageName']
  else:raise ValueError('Unhandled synthetic relation '+fact['relation'])
  groups.setdefault(key,set()).add(sub)
 # Preserve supplied partial/unknown Coverage inputs. Replace complete partitions
 # with the newly constructed synthetic census to avoid overlapping scopes.
 preserved=[c for c in kw['coverages'] if c['_payload']['entry']['coverage']!='complete']
 partial_keys=set()
 for c in preserved:
  sc=st.objects[c['scopeId']];key=(sc['sourceUniverse'],sc['relation'],sc['resolution'],sc['enumeratorClosure']);partial_keys.add(key)
  assert key not in groups,'Do not claim complete synthetic coverage across a preserved unknown partition'
 groups.setdefault((primary,'package','manifest-declared',provider),set()).update(pkg for _,pkg in packages)
 if any(c['capabilityId']=='syntax' for c in enum['cells']):
  for rel in ['declares','literal','control-flow']:groups.setdefault((primary,rel,'syntactic',provider),set()).update(s['nativeSubjectId'] for s in syms)
 scopes=[c['scopeId'] for c in preserved];coverages=list(preserved)
 for (uni,rel,rung,producer),subjects in sorted(groups.items()):
  sc,scid,commit=runs.make_scope(st,snapid,rel,rung,uni,producer,sorted(subjects));cp=runs.coverage_payload(rel,rung,uni,commit,len(subjects));cov,cid=runs.make_coverage(st,scid,cp);scopes.append(scid);coverages.append(cov)
 view=copy.deepcopy(kw['view']);view.update(planId=planid,scopeIds=order.cset(scopes),coverageIds=order.cset(c['id'] for c in coverages),facts=order.cset(f['id'] for f in facts));vid=st.put_canonical_record('view',view)
 views=[]
 for universe in sorted({st.objects[s]['sourceUniverse'] for s in scopes}):
  one=copy.deepcopy(view);one['scopeIds']=order.cset(s for s in scopes if st.objects[s]['sourceUniverse']==universe)
  one['coverageIds']=order.cset(c['id'] for c in coverages if c['scopeId'] in one['scopeIds'])
  one['facts']=order.cset(f['id'] for f in facts if f['sourceUniverse']==universe)
  if universe==primary:views.append(st.put_canonical_record('view',one))
 
 stage={'schemaVersion':2,'planId':planid,'producerClosure':provider,'operation':'author-synthetic-analysis','parameters':[],'outputDomains':['view'],'outputSchemaDigest':builder.NAT_DIGEST};sd=blob(stage)
 execution={'schemaVersion':2,'planId':planid,'stages':[{'ordinal':0,'stageSpecDigest':sd,'requires':[],'outputDomains':['view']}]};xid=st.put_canonical_record('execution-plan',execution)
 # Decode exact retained inputs; no claimed old proof is used in normalization.
 objects,blobs=T.decode_store(json.dumps(st.export()).encode(),M)
 policy=kw['policy'];rules={}
 for rule in policy['rules']:
  kind=rule['subjectEnumeration']['subjectKind'];rules[rule['ruleId']]={'state':'complete','inventoryRefs':E.cset([{'domain':'subject-inventory','digest':d} for d,v in inventories if v['kind']==kind]),'selectedSubjectIds':E.cset([sid for sid,s in population.items() if s['kind']==kind]),'unresolvedSubjectIds':[],'incompleteInventoryRefs':[]}
 emission=next(raw(p['payloadDigest']) for p in spec['parameters'] if p['schemaDigest']==builder.EMIT_PLAN_DIGEST)
 inputs={'plan':plan,'planId':planid,'executionPlanId':xid,'evaluatorClosure':kw['evaluator_id'],'policy':policy,'effectiveWaivers':raw(plan['waiverDigest']),'emissionPlan':emission,'population':population,'enumerations':rules,'enumerationDeficiencies':{r:[] for r in rules},'requiredEvidenceDeficiencies':{r:[] for r in rules},'executionDeficiencies':[],'evaluationInputRefs':[],'inventoryRowCount':sum(len(v['rows']) for _,v in inventories),'inventoryLocatorCount':len(inventories),'factCount':len(facts),'observationCount':0,'coverageCount':len(coverages),'importKinds':{},'closures':{i:o for i,(d,o) in objects.items() if d=='closure'}}
 graph={'objects':objects,'blobs':blobs,'inputs':inputs,'snapshot':snap,'enumerationPlan':enum,'inventoryResults':inventories,'viewIds':order.cset(views),'scopeIds':order.cset([s for vid in views for s in st.objects[vid]['scopeIds']]),'coverageIds':order.cset([c for vid in views for c in st.objects[vid]['coverageIds']])}
 capture=X.attach_host_capture(graph)
 (out/(name+'-capture.json')).write_text(json.dumps(capture['admission'],indent=2)+'\n')
 if capture['admission']['result']!='ADMIT':raise ValueError('Host capture: '+str(capture['admission']['refusals']))
 seed,objects,blobs,_=S.seed_seal(graph);_,owner=M.open_run_closure(seed,objects,blobs)
 derived=R.derive(planid,xid,kw['evaluator_id'],inputs['evaluationInputRefs'],objects,blobs,owner)
 run,objects,blobs=S.seal_derived(graph,derived,objects,blobs);rid=M.identifier('run',run);objects[rid]=('run',run)
 # Rebuild a new export from derived typed objects and exact retained raw blobs.
 final=store.Store()
 for b in blobs.values():final.put_blob(b)
 for domain,obj in objects.values():final.put_canonical_record(domain,obj)
 final.meta.update(runId=rid,authorAssisted=True,qualificationClaimed=False)
 return {'store':final,'runId':rid,'authorCapture':capture['admission']}

runs.seal_graph=finalizer
out=ROOT/'rust-selection-examples1';out.mkdir();claims=[];status=[]
for SELECTION in ['bin','lib-only']:
 name='rust-'+SELECTION;fn=runs.build_rust_run
 try:
  g=fn();p=name+'.store.json';(out/p).write_text(json.dumps(g['store'].export(),indent=2,sort_keys=True)+'\n');claims.append({'name':name,'path':p,'runId':g['runId']});status.append({'name':name,'constructed':True})
 except Exception as e:status.append({'name':name,'constructed':False,'error':str(e),'traceback':traceback.format_exc()})
(out/'claims.json').write_text(json.dumps(claims,indent=2)+'\n');(out/'construction.json').write_text(json.dumps(status,indent=2)+'\n');print(json.dumps(status,indent=2))
