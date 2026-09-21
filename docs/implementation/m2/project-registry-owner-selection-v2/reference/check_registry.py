"""Executable examples of proposed registry law. No native qualification."""
from copy import deepcopy
import hashlib
import itertools
import json
from pathlib import Path
import registry_model as m

cases=[]
def case(name, function, expected):
    try: value=function()
    except m.Refused as e: value={'refused':str(e)}
    accepted=value==expected if expected!='REFUSE' else type(value) is dict and 'refused' in value
    cases.append({'caseId':f'{len(cases):04d}','case':name,'expected':expected,'observed':value,'pass':accepted})
    assert accepted,(name,expected,value)

def row(i,status='ACTIVE',project=None,root=None,allocation='random'):
    return {'projectId':'prj1-'+f'{project if project is not None else i:064x}',
            'namespaceId':f'{i:08x}-0000-4000-8000-000000000000',
            'root':root or {'platform':'macos','canonicalPathBytesHex':f'/repos/{i}'.encode().hex(),
                          'volumeIdentity':{'kind':'macos-apfs-volume-uuid-v1','value':'1'*32},'inodeId':str(i+1),'birthSeconds':0,'birthNanoseconds':0},
            'status':status,'allocationKind':allocation}
def doc(*rows):return {'schemaVersion':2,'entries':list(rows)}
def valid(x): m.validate(x); return 'VALID'
def altered(x,key,value):
    y=deepcopy(x);y[key]=value;return y

a=row(1); p=a['projectId']; empty=doc(); base=doc(a)
case('empty-registry',lambda:valid(empty),'VALID')
case('active-singleton',lambda:m.decode(m.encode(base)),base)
case('marker-zero-exact92-sha',lambda:(len(m.marker('prj1-'+'0'*64)),hashlib.sha256(m.marker('prj1-'+'0'*64)).hexdigest()),(92,'1a791d57d6d4c0e137dd08d81d7d076a18a5a93a967a0b82ec176597c13a7ef1'))
case('marker-roundtrip',lambda:m.marker_id(m.marker(p)),p)
for name,b in [('BOM',b'\xef\xbb\xbf'+m.marker(p)),('CRLF',m.marker(p).replace(b'\n',b'\r\n')),('trailing',m.marker(p)+b' '),('no-final-LF',m.marker(p)[:-1]),('uppercase',m.marker(p).replace(b'prj1',b'PRJ1')),('JSON',m.encode({'projectId':p})),('nonascii',m.marker(p)[:-2]+b'\xff\n')]:
    case('marker-'+name,lambda b=b:m.marker_id(b),'REFUSE')
for field,value in [('schemaVersion',True),('schemaVersion',1),('extra',None),('entries',{}),('entries',[altered(a,'extra',0)]),('entries',[altered(a,'status','reserved')]),('entries',[altered(a,'projectId',p+'\n')]),('entries',[altered(a,'namespaceId',a['namespaceId'].replace('4000','5000'))])]:
    case('shape-'+field+'-'+str(value)[:50],lambda field=field,value=value:valid(altered(base,field,value)),'REFUSE')
for field,values in {'deviceId':['00','-1',str(1<<64),'1\n',1], 'inodeId':['+1',' 1',''], 'birthSeconds':[True,-(1<<63)-1,1<<63], 'birthNanoseconds':[-1,1_000_000_000,False], 'platform':['windows',None], 'canonicalPathBytesHex':['','2F','2','zz',b'/'.hex()+b'../x'.hex(),b'/a//b'.hex(),b'/a/'.hex(),b'/a/./b'.hex(),b'a'.hex(),b'/a\0'.hex(),(b'/'+b'a'*4096).hex()]}.items():
    for v in values:
        x=deepcopy(base);x['entries'][0]['root'][field]=v
        case('root-'+field+'-'+str(v)[:24],lambda x=x:valid(x),'REFUSE')
for name,path in [('root',b'/'),('nonutf8',b'/\xff'),('max',b'/'+b'x'*4095)]:
    x=deepcopy(base);x['entries'][0]['root']['canonicalPathBytesHex']=path.hex()
    case('path-'+name,lambda x=x:valid(x),'VALID')
for name,b in [('space',m.encode(base)+b' '),('duplicate',b'{"entries":[],"schemaVersion":1,"schemaVersion":1}'),('negative-zero',m.encode(base).replace(b'"birthSeconds":0',b'"birthSeconds":-0')),('float',m.encode(base).replace(b'"birthSeconds":0',b'"birthSeconds":0.0')),('exponent',m.encode(base).replace(b'"birthSeconds":0',b'"birthSeconds":0e0')),('over-cap',b' '*(m.CAP+1)),('invalid-utf8',b'\xff')]:
    case('decode-'+name,lambda b=b:m.decode(b),'REFUSE')
case('duplicate-N-across-terminal',lambda:valid(doc(row(1,'RETIRED'),row(1,'ABANDONED'))),'REFUSE')
case('reverse-N',lambda:valid(doc(row(2),row(1))),'REFUSE')
for s,t in itertools.product(sorted(m.STATES),repeat=2):
    expected='REFUSE' if s in m.LIVE and t in m.LIVE else 'VALID'
    case('same-project-'+s+'-'+t,lambda s=s,t=t:valid(doc(row(1,s,7),row(2,t,7))),expected)
    case('same-root-'+s+'-'+t,lambda s=s,t=t:valid(doc(row(1,s),row(2,t,root=a['root']))),expected)
for s,t,kind in itertools.product(sorted(m.STATES),sorted(m.STATES),('activate','abandon','retire')):
    expected=doc(row(1,t)) if (kind,s,t) in {('activate','RESERVED','ACTIVE'),('abandon','RESERVED','ABANDONED'),('retire','ACTIVE','RETIRED')} else 'REFUSE'
    case('edge-'+kind+'-'+s+'-'+t,lambda s=s,t=t,kind=kind:m.transition(doc(row(1,s)),doc(row(1,t)),kind),expected)
case('deletion-refuses',lambda:m.transition(base,empty,'retire'),'REFUSE')
case('namespace-reassignment-refuses',lambda:m.transition(base,doc(row(2)),'move'),'REFUSE')
case('root-edit-outside-move',lambda:m.transition(base,doc(row(1,'RETIRED',root=row(2)['root'])),'retire'),'REFUSE')
case('active-move-delta-only',lambda:m.transition(base,doc(row(1,root=row(2)['root'])),'move'),doc(row(1,root=row(2)['root'])))
case('project-rewrite-refuses',lambda:m.transition(base,doc(row(1,project=2)),'move'),'REFUSE')
old=doc(row(1,'RETIRED'))
new=doc(row(1,'RETIRED'),row(2,'RESERVED',1,allocation='adopt'))
case('adoption-fresh-N-historical-project',lambda:m.transition(old,new,'reserve-adopt'),new)
case('random-cannot-reuse-historical-project',lambda:m.transition(old,doc(row(1,'RETIRED'),row(2,'RESERVED',1,allocation='random')),'reserve-random'),'REFUSE')
case('adoption-cannot-duplicate-active-project',lambda:m.transition(base,doc(row(1),row(2,'RESERVED',1,allocation='adopt')),'reserve-adopt'),'REFUSE')
case('no-direct-ACTIVE-insertion',lambda:m.transition(empty,base,'reserve-random'),'REFUSE')
for status,obs,expected in [('ACTIVE','absent','ONE_SIDED'),('ACTIVE','matching','MATCHED_ACTIVE'),('RESERVED','absent','RECOVERY_REQUIRED'),('RESERVED','matching','RECOVERY_REQUIRED'),('RETIRED','absent','FIRST_USE_CANDIDATE'),('RETIRED','matching','ONE_SIDED'),('ABANDONED','absent','FIRST_USE_CANDIDATE'),('ABANDONED','matching','ONE_SIDED')]:
    observation=m.marker(p) if obs=='matching' else obs
    case('observe-'+status+'-'+obs,lambda status=status,observation=observation:m.classify(doc(row(1,status)),a['root'],observation),expected)
case('first-use-no-row-no-marker',lambda:m.classify(empty,a['root'],'absent'),'FIRST_USE_CANDIDATE')
case('inaccessible-marker-not-absence',lambda:m.classify(empty,a['root'],'unavailable'),'UNAVAILABLE')
case('tracked-marker-refuses',lambda:m.classify(base,a['root'],m.marker(p),'tracked'),'TRACKING_REFUSAL')
case('unknown-tracking-refuses',lambda:m.classify(base,a['root'],m.marker(p),'unknown'),'TRACKING_REFUSAL')
case('different-marker-refuses',lambda:m.classify(base,a['root'],m.marker(row(2)['projectId'])),'CONTRADICTION')
case('moved-marker-is-not-auto-move',lambda:m.classify(base,row(2)['root'],m.marker(p)),'CONTRADICTION')
case('other-project-registry-update-independent',lambda:m.classify(doc(row(1),row(2)),a['root'],m.marker(p)),'MATCHED_ACTIVE')
case('S9-retained-retired-not-abandoned',lambda:m.namespace_list(doc(row(1),row(2,'RETIRED'),row(3,'ABANDONED'))),[row(1)['namespaceId'],row(2)['namespaceId']])
case('S9-pending-reservation-blocks',lambda:m.namespace_list(doc(row(1),row(2,'RESERVED'))),'REFUSE')
case('row-bound4096',lambda:valid(doc(*(row(i,'ABANDONED') for i in range(4096)))),'VALID')
case('row-bound4097',lambda:valid(doc(*(row(i,'ABANDONED') for i in range(4097)))),'REFUSE')
large=[row(i,'ABANDONED') for i in range(512)]
for r in large:r['root']['canonicalPathBytesHex']=(b'/'+b'x'*4095).hex()
case('aggregate-byte-cap-not-just-rows',lambda:valid(doc(*large)),'REFUSE')
# Bounded allocation: ninth fresh candidate cannot rescue eight collisions.
case('project-eight-collisions-not-ninth',lambda:m.allocation_candidate(base,[p]*8+[row(2)['projectId']],[row(2)['namespaceId']],set()),'REFUSE')
case('project-eighth-fresh',lambda:m.allocation_candidate(base,[p]*7+[row(2)['projectId']],[row(2)['namespaceId']],set()),(row(2)['projectId'],row(2)['namespaceId']))
case('namespace-eight-collisions-not-ninth',lambda:m.allocation_candidate(base,[row(2)['projectId']],[a['namespaceId']]*8+[row(2)['namespaceId']],set()),'REFUSE')
case('historical-N-never-reused',lambda:m.allocation_candidate(doc(row(1,'ABANDONED')),[row(2)['projectId']],[a['namespaceId']]*8,set()),'REFUSE')
case('occupied-new-N-refuses',lambda:m.allocation_candidate(empty,[p],[a['namespaceId']],{a['namespaceId']}),'REFUSE')
case('abandoned-old-N-does-not-occupy-new-N',lambda:m.allocation_candidate(doc(row(1,'ABANDONED')),[row(2)['projectId']],[row(2)['namespaceId']],{a['namespaceId']}),(row(2)['projectId'],row(2)['namespaceId']))
case('depth33-before-shape',lambda:m.decode(b'['*33+b'0'+b']'*33),{'refused':'depth'})
# Conditional recovery prefixes; external authorization/custody is assumed.
for mode,ns,marker_state in itertools.product(('ordinary-recovery','admitted-adoption'),('absent','complete-initial','incomplete','foreign','unavailable'),('absent','exact','malformed','different','unavailable')):
    expected='UNAVAILABLE'
    if ns in ('absent','complete-initial') and marker_state in ('absent','exact'):
        expected=[('publish-namespace' if ns=='absent' else 'reconfirm-namespace-durability'),('create-marker' if marker_state=='absent' else 'reconfirm-marker-durability'),'publish-ACTIVE']
    if mode=='ordinary-recovery' and ns=='absent' and marker_state=='exact': expected='ORDINARY_PREFIX_REFUSED'
    case('supplied-observation-'+mode+'-'+ns+'-'+marker_state,lambda mode=mode,ns=ns,marker_state=marker_state:m.reservation_completion(doc(row(1,'RESERVED',allocation=('adopt' if mode=='admitted-adoption' else 'random'))),a['namespaceId'],ns,marker_state,True,False,mode,p if mode=='admitted-adoption' else None),expected)
for ns,marker_state,durable,stopped in itertools.product(('absent','complete-initial'),('absent','exact'),(True,False),(True,False)):
    if stopped or not durable:
        case('uncertain-stop-'+str((ns,marker_state,durable,stopped)),lambda ns=ns,marker_state=marker_state,durable=durable,stopped=stopped:m.reservation_completion(doc(row(1,'RESERVED')),a['namespaceId'],ns,marker_state,durable,stopped,'ordinary-recovery'),'STOP')
case('mode-string-not-admitted-context',lambda:m.reservation_completion(doc(row(1,'RESERVED')),a['namespaceId'],'absent','exact',True,False,'caller-adopt'),'NO_COMPLETION_AUTHORITY')
case('unknown-mode-no-create',lambda:m.reservation_completion(doc(row(1,'RESERVED')),a['namespaceId'],'absent','absent',True,False,None),'NO_COMPLETION_AUTHORITY')
footprint=[{'name':name,'kind':'regular','mode':0o600,'bytes':0,'links':1} for name in ('writer.lease','readers.lease')]
case('complete-initial-value-footprint',lambda:m.initial_namespace_footprint(0o700,footprint),True)
for name,entries,mode in [('empty',[],0o700),('extra',footprint+[{'name':'foreign'}],0o700),('missing-reader',footprint[:1],0o700),('duplicate',footprint[:1]*2,0o700),('wrong-dir-mode',footprint,0o755)]:
    case('initial-footprint-'+name,lambda entries=entries,mode=mode:m.initial_namespace_footprint(mode,entries),False)
for field,value in [('kind','symlink'),('kind','directory'),('mode',0o644),('bytes',1),('links',2),('links',True),('name','foreign')]:
    wrong=deepcopy(footprint);wrong[0][field]=value
    case('initial-footprint-'+field+str(value),lambda wrong=wrong:m.initial_namespace_footprint(0o700,wrong),False)
ordinary_prefixes=[('reserved-only','absent','absent'),('namespace-before-marker','complete-initial','absent'),('marker-before-active','complete-initial','exact')]
for name,ns,marker_state in ordinary_prefixes:
    case('ordinary-durable-prefix-'+name,lambda ns=ns,marker_state=marker_state:m.reservation_completion(doc(row(1,'RESERVED')),a['namespaceId'],ns,marker_state,True,False,'ordinary-recovery')[-1],'publish-ACTIVE')
# An adoption can be new to this installation: no historical-row heuristic.
for history in (False,True):
    adopted=row(2,'RESERVED',project=1,allocation='adopt')
    document=doc(row(1,'RETIRED'),adopted) if history else doc(adopted)
    for ns,marker_state in itertools.product(('absent','complete-initial'),('absent','exact')):
        case('adopt-never-ordinary-'+str((history,ns,marker_state)),lambda document=document,ns=ns,marker_state=marker_state:m.reservation_completion(document,adopted['namespaceId'],ns,marker_state,True,False,'ordinary-recovery'),'ADOPTION_CONTEXT_REQUIRED')
    case('adopt-context-matching-'+str(history),lambda document=document:m.reservation_completion(document,adopted['namespaceId'],'complete-initial','exact',True,False,'admitted-adoption',p)[-1],'publish-ACTIVE')
    case('adopt-context-wrong-project-'+str(history),lambda document=document:m.reservation_completion(document,adopted['namespaceId'],'complete-initial','exact',True,False,'admitted-adoption',row(9)['projectId']),'ADOPTION_PROJECT_MISMATCH')
case('random-cannot-switch-to-adoption-context',lambda:m.reservation_completion(doc(row(1,'RESERVED')),a['namespaceId'],'complete-initial','exact',True,False,'admitted-adoption',p),'CONTEXT_KIND_MISMATCH')
case('kind-immutable-on-activation',lambda:m.transition(doc(row(1,'RESERVED')),doc(row(1,'ACTIVE',allocation='adopt')),'activate'),'REFUSE')
case('kind-immutable-on-move',lambda:m.transition(base,doc(row(1,root=row(2)['root'],allocation='adopt')),'move'),'REFUSE')
case('random-reservation-needs-random-kind',lambda:m.transition(empty,doc(row(1,'RESERVED',allocation='adopt')),'reserve-random'),'REFUSE')
case('adopt-reservation-needs-adopt-kind',lambda:m.transition(empty,doc(row(1,'RESERVED')),'reserve-adopt'),'REFUSE')
case('missing-kind-refuses-not-migration',lambda:valid(doc({k:v for k,v in a.items() if k!='allocationKind'})),'REFUSE')
case('unknown-kind-refuses',lambda:valid(doc(altered(a,'allocationKind','legacy'))),'REFUSE')
case('nonreserved-row-cannot-complete',lambda:m.reservation_completion(base,a['namespaceId'],'complete-initial','exact',True,False,'ordinary-recovery'),'REFUSE')
result={'standing':'Author pure reference cases, supplied observations only; no native authority or final owner acceptance', 'caseCount':len(cases),'failed':sum(not c['pass'] for c in cases),'cases':cases}
out=Path(__file__).with_name('reference-results.inherited379.json');require_new=not out.exists()
assert require_new,'do not overwrite run evidence'
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'cases':len(cases),'failed':0,'output':str(out)}))
