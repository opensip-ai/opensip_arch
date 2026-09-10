# Independent v5 probes, group B: ADV-a..e + source-pin closure. Reviewer-authored.
import json,sys,os,hashlib,importlib.util,copy
from pathlib import Path
SUB='/tmp/opensip-design-corrections/post-reset-review.v5/scratch/subject'
DC=SUB+'/docs/coop/design-corrections'
R=[]
def p(pid,title,ok,detail=''):
    R.append({'id':pid,'title':title,'result':'PASS' if ok else 'FAIL','detail':str(detail)[:900]})
    print(('PASS ' if ok else 'FAIL ')+pid+' :: '+title+((' :: '+str(detail)[:280]) if detail else ''))
def sha(p_): return hashlib.sha256(Path(p_).read_bytes()).hexdigest()

# ---------------- ADV-a: unique integration identifiers
rep=json.load(open(DC+'/integration-report.v1.json'))
ids=[c['id'] for c in rep['checks']]
p('B1','integration report ids all distinct and count equals distinct count',
  len(ids)==len(set(ids))==319 and rep['passed']==319,{'checks':len(ids),'distinct':len(set(ids))})
p('B1b','both retention-loss lanes separately identifiable',
  {'missing-retained-closure-is-typed-operational-loss-blobs','missing-retained-closure-is-typed-operational-loss-objects'}<=set(ids),'')
src=Path(DC+'/check-integration.py').read_text()
p('B1c','checker itself asserts identifier uniqueness','integration-check-identifiers-unique' in src and 'len({c[\'id\'] for c in checks}) == len(checks)' in src,'')
# the two lanes must genuinely differ in what is missing
p('B1d','lane naming matches the actually-missing map (blobs lane passes empty blobs)',
  "(('blobs',eobjects,{}),('objects',{},eblobs))" in src,'')

# ---------------- ADV-b: real security discovery -> admitted boundaries -> native scope
sys.path.insert(0,DC)
os.chdir(DC)
spec=importlib.util.spec_from_file_location('integ_model',DC+'/integration-model.py') if os.path.exists(DC+'/integration-model.py') else None
p('B2','operational 1024/1025 checks present and passing in report',
  all(any(c['id']==k and c['passed'] for c in rep['checks']) for k in ('operational-scope-1024','operational-scope-1025')),'')
p('B2b','operational path composes security discovery, not the standalone instrument',
  'M.admit_repository_discovery(observed_input, marker_inventory, [])' in src and 'unit_scope_descriptor' not in src.split('Operational 1024/1025-root path')[1].split('Host-observation typos')[0],'')
p('B2c','1025 lane asserts exact typed exit 2 and field:count>limit subject',
  "term['domainDetail']['subject'] == 'workspaceRoots:1025>1024'" in src and "M.W.exit_code(term) == 2" in src,'')
p('B2d','1024 lane asserts a positive admitted size of exactly 1024 roots',
  "len(composed['scope']['scopeDescriptor']['workspaceRoots']) == 1024" in src,'')
# v4's standalone-only evidence retained as unit evidence
p('B2e','standalone unit evidence retained alongside (scope-1024/1025 roots checks still present)',
  {'scope-1024-roots-admitted','scope-1025-roots-typed-refusal'}<=set(ids),'')

# ---------------- ADV-c: canonical boundary-code prose
nat=Path(SUB+'/docs/v2/contracts/product-v1/native-evidence.md').read_text()
row=[l for l in nat.splitlines() if 'explicit-root-without-marker' in l and 'EXPLICIT_PATH_INVALID' in l]
p('B3','native section 10 row groups grammar+boundary under one code, marker separately',
  len(row)==1 and '(missing marker)' in row[0] and '(grammar or boundary crossing)' in row[0]
  and row[0].count('PROJECT.EXPLICIT_PATH_INVALID')==1,row[0][-190:] if row else 'row not found')

# ---------------- ADV-d: numeric metric comparability restated in owning contract
wf=Path(SUB+'/docs/v2/contracts/product-v1/workflows-and-surfaces.md').read_text()
sec=wf.split('### Numeric comparisons and metric redistribution (FW-11)')
has=len(sec)==2
body=sec[1] if has else ''
p('B4','FW-11 comparability restated in the owning workflow contract',
  has and 'same metric definition' in body and 'supplied diff scope' in body and 'comparison base' in body
  and 'reported incompatible' in body and 'redistribution' in body,
  {'sectionPresent':has})
p('B4b','restatement names the inherited owner (architecture 13 section 6) rather than forking it',
  '13' in body and '6' in body and 'inherited' in body.lower(),'')

# ---------------- ADV-e: discovery host-observation seam
spec=importlib.util.spec_from_file_location('slm',DC+'/security/security_lifecycle_model_v1.py')
S=importlib.util.module_from_spec(spec); spec.loader.exec_module(S)
base={'invokingUid':1000,'accountHome':'/h','cwd':'/h/p',
      'fs':{'/':{'kind':'dir','uid':0,'mode':'0755','dev':1},
            '/h':{'kind':'dir','uid':1000,'mode':'0755','dev':1},
            '/h/p':{'kind':'dir','uid':1000,'mode':'0755','dev':1,'vcs':True}}}
def run(d):
    try: return ('ok',S.discovery(d))
    except S.Reject as e: return ('reject',str(e))
    except Exception as e: return ('other',type(e).__name__+':'+str(e)[:80])
k,v=run(dict(base))
p('B5','a valid minimal older-shape observation still succeeds',k=='ok',k if k!='ok' else 'DiscoveryProvenanceV1 produced')
neg={
 'unknown-key':dict(base,config={}),
 'unknown-key-misspelled':dict(base,invokingUID=1000),
 'missing-required-fs':{kk:vv for kk,vv in base.items() if kk!='fs'},
 'missing-required-uid':{kk:vv for kk,vv in base.items() if kk!='invokingUid'},
 'missing-required-home':{kk:vv for kk,vv in base.items() if kk!='accountHome'},
 'missing-required-cwd':{kk:vv for kk,vv in base.items() if kk!='cwd'},
 'uid-bool':dict(base,invokingUid=True),
 'uid-string':dict(base,invokingUid='1000'),
 'uid-negative':dict(base,invokingUid=-1),
 'fs-not-dict':dict(base,fs=[]),
 'home-not-str':dict(base,accountHome=1),
 'cwd-not-str':dict(base,cwd=None),
 'ci-string':dict(base,ci='false'),
 'ci-int':dict(base,ci=1),
 'owner-int':dict(base,trustProjectOwner=1),
 'owner-string':dict(base,trustProjectOwner='yes'),
 'groups-not-list':dict(base,authorizedGroupIds=1000),
 'groups-bool-member':dict(base,authorizedGroupIds=[True]),
 'groups-str-member':dict(base,authorizedGroupIds=['1000']),
 'groups-negative':dict(base,authorizedGroupIds=[-5]),
 'explicitJoins-not-list':dict(base,explicitJoins={}),
 'configWorkspaceRoots-not-list':dict(base,configWorkspaceRoots='/x'),
 'explicitProject-not-str':dict(base,explicitProject=5),
 'explicitResolved-not-str':dict(base,explicitResolved=[]),
 'not-a-dict':['invokingUid'],
}
res={n:run(d) for n,d in neg.items()}
bad={n:r for n,r in res.items() if not (r[0]=='reject' and r[1]=='DISCOVERY_OBSERVATION_SHAPE')}
p('B5b','every unknown/missing key and wrong outer type is DISCOVERY_OBSERVATION_SHAPE (25 negatives)',
  not bad,bad if bad else {'negatives':len(neg)})
pos={
 'with-ci-false':dict(base,ci=False),
 'with-ci-true':dict(base,ci=True),
 'with-owner-trust':dict(base,trustProjectOwner=True),
 'with-groups':dict(base,authorizedGroupIds=[1000,0]),
 'with-empty-groups':dict(base,authorizedGroupIds=[]),
 'with-explicit-none':dict(base,explicitProject=None,explicitResolved=None),
 'with-explicit-joins':dict(base,explicitJoins=[]),
 'with-config-roots':dict(base,configWorkspaceRoots=[]),
}
badp={n:run(d) for n,d in pos.items()}
badp={n:r for n,r in badp.items() if r[0]!='ok'}
p('B5c','every optional key with a correct type still admits (8 positives, no regression)',
  not badp,badp if badp else {'positives':len(pos)})
p('B5d','instrument error is not a public D9 code and mints no request carrier',
  'DISCOVERY_OBSERVATION_SHAPE' not in Path(DC+'/workflows/command-inventory.v1.json').read_text()
  and 'DISCOVERY_OBSERVATION_SHAPE' not in nat,'absent from public inventory and native contract')
sl=Path(SUB+'/docs/v2/contracts/product-v1/security-and-lifecycle.md').read_text()
p('B5e','contract states the closed key set and that it is instrument-level, not D9',
  'DISCOVERY_OBSERVATION_SHAPE' in sl and 'not public D9 input refusals' in sl
  and 'synthetic trusted observation' in sl,'')
p('B5f','uid/gid reject bools explicitly (isinstance int would have accepted True)',
  S._int(True) is False and S._int(1) is True,'')

# ---------------- source-pin closure over the four suites
os.chdir('/tmp')
def check_pins(name,path,root):
    d=json.load(open(path))
    entries=d.get('files') or d.get('pins')
    bad=[];n=0
    if isinstance(entries,dict): it=[(k,v) for k,v in entries.items()]
    else: it=[(e.get('path') or e.get('file'),e) for e in entries]
    for rel,e in it:
        dig=e if isinstance(e,str) else (e.get('sha256') or e.get('digest'))
        fp=os.path.join(root,rel)
        if not os.path.exists(fp): bad.append((rel,'absent')); continue
        n+=1
        if sha(fp)!=dig: bad.append((rel,'digest'))
    return n,bad
tot=0;allbad=[]
for nm,pp,rt in [('foundation',DC+'/foundation/source-pins.v1.json',DC+'/foundation'),
                 ('security',DC+'/security/source-pins.v1.json',DC+'/security'),
                 ('native',DC+'/native/source-pins.v2.json',DC+'/native'),
                 ('workflows',DC+'/workflows/source-pins.v1.json',DC+'/workflows')]:
    n,bad=check_pins(nm,pp,rt); tot+=n; allbad+= [(nm,)+b for b in bad]
p('B6','all four source-pin sets resolve to current bytes',not allbad,{'pinned':tot,'bad':allbad[:8]})
p('B6b','the three changed models/checkers are pinned (re-pinned, not orphaned)',
  all(x in Path(DC+'/security/source-pins.v1.json').read_text() for x in ['security_lifecycle_model_v1.py'])
  and 'workflows_model.v1.py' in Path(DC+'/workflows/source-pins.v1.json').read_text()
  and 'check_workflows.v1.py' in Path(DC+'/workflows/source-pins.v1.json').read_text(),'')

json.dump(R,open('/tmp/opensip-design-corrections/post-reset-review.v5/probes/claude-probes-B.json','w'),indent=1)
print('\nB-group:',sum(1 for x in R if x['result']=='PASS'),'PASS',sum(1 for x in R if x['result']=='FAIL'),'FAIL of',len(R))
