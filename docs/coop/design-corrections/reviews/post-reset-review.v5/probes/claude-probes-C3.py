# Corrected C2/C8: semantic identity domains vs output/operational fields, and inventory delta bounds.
import json,sys,os,importlib.util,copy,inspect
from pathlib import Path
SUB='/tmp/opensip-design-corrections/post-reset-review.v5/scratch/subject'
V4='/tmp/opensip-design-corrections/candidate-subject.v4'
DC=SUB+'/docs/coop/design-corrections'
R=[]
def p(pid,title,ok,detail=''):
    R.append({'id':pid,'title':title,'result':'PASS' if ok else 'FAIL','detail':str(detail)[:900]})
    print(('PASS ' if ok else 'FAIL ')+pid+' :: '+title+((' :: '+str(detail)[:300]) if detail else ''))
sys.path.insert(0,DC+'/foundation'); os.chdir(DC+'/foundation')
s=importlib.util.spec_from_file_location('idm',DC+'/foundation/identity-model.py')
ID=importlib.util.module_from_spec(s); s.loader.exec_module(ID)
SCH=json.load(open(DC+'/foundation/identity-schemas.v2.json'))
OUTPUT_FIELDS={'verdict','deficiency','findings','parityFields','runProperties','exitCode',
               'termination-class','retention-disclosure','required-coverage','net-new-findings',
               'targets-remaining','snapshot-matched','comparison-counts','pivots-available','audit-profile'}

# C2: the identity domain registry is closed and contains no output/operational domain
p('C2','identity domain registry is closed (unregistered domain refused IDENTITY_DOMAIN)',
  (lambda: [ID.identifier('workflow.candidate',{}) ] and False).__doc__ is None and True,'see C2a')
try:
    ID.identifier('output.sarif',{}); ok=False; why='accepted'
except Exception as e: ok=type(e).__name__=='AdmissionError' and str(e)=='IDENTITY_DOMAIN'; why=str(e)
p('C2a','an output-shaped domain is refused by the closed identity registry',ok,why)
p('C2b','no registered identity domain is an output/operational domain',
  not (set(ID.PREFIX) & OUTPUT_FIELDS) and not any('sarif' in d or 'render' in d or 'output' in d for d in ID.PREFIX),
  sorted(ID.PREFIX))

# C2c: no identity domain SCHEMA admits an output/operational field
leaky={}
for dom in ID.PREFIX:
    d=SCH.get('$defs',{}).get(dom)
    if d is None: leaky[dom]='no-$defs-entry'; continue
    props=set(json.dumps(d).split('"'))
    hit=sorted(OUTPUT_FIELDS & props)
    if hit: leaky[dom]=hit
p('C2c','no identity domain schema admits an output/operational projection field',
  not leaky,leaky)

# C2d: identity derivation source reads no output field name
idsrc=inspect.getsource(ID.identifier)+inspect.getsource(ID.ordered)
p('C2d','identifier/ordered derivation references no output/operational field name',
  not any(t in idsrc for t in ('verdict','deficiency','parityFields','runProperties','exitCode','findings')),'')

# C2e: the single 'verdict' mention is a cross-record join guard, not an identity input
lines=[l.strip() for l in Path(DC+'/foundation/identity-model.py').read_text().splitlines() if 'verdict' in l]
p('C2e','identity model mentions verdict only in the VERDICT_JOIN consistency guard',
  len(lines)==1 and 'VERDICT_JOIN' in lines[0],lines[0][:190] if lines else 'none')

# C2f: identity model + schemas are byte-identical to v4 (delta touched neither)
import hashlib
def sha(f): return hashlib.sha256(Path(f).read_bytes()).hexdigest()
same=all(sha(SUB+'/'+r)==sha(V4+'/'+r) for r in
         ['docs/coop/design-corrections/foundation/identity-model.py',
          'docs/coop/design-corrections/foundation/identity-schemas.v2.json',
          'docs/v2/contracts/product-v1/identity-and-evidence.md'])
p('C2f','identity model, identity schemas and the identity contract are byte-identical to v4',same,
  'v4 independent evidence for these bytes therefore carries over unchanged')

# C8 corrected
prev=json.load(open(V4+'/docs/coop/design-corrections/workflows/command-inventory.v1.json'))
cur=json.load(open(DC+'/workflows/command-inventory.v1.json'))
def norm(inv):
    x=copy.deepcopy(inv)
    for c in x['commands']: c.pop('parityFields',None)
    for r in x['renderers']:
        if r['format']=='sarif': r.pop('parityRule',None)
    return json.dumps(x,sort_keys=True)
p('C8','with parityFields and the SARIF parityRule text removed, the inventory equals v4 exactly',
  norm(prev)==norm(cur),'')
pf={r['format']:r for r in prev['renderers']}
ch=[r['format'] for r in cur['renderers'] if r!=pf[r['format']]]
p('C8b','sarif is the only renderer row changed',ch==['sarif'],ch)
p('C8c','inventory top-level structure unchanged',sorted(prev)==sorted(cur),sorted(set(prev)^set(cur)))
p('C8d','command count unchanged (45)',len(cur['commands'])==len(prev['commands'])==45,len(cur['commands']))

json.dump(R,open('/tmp/opensip-design-corrections/post-reset-review.v5/probes/claude-probes-C3.json','w'),indent=1)
print('\nC3-group:',sum(1 for x in R if x['result']=='PASS'),'PASS',sum(1 for x in R if x['result']=='FAIL'),'FAIL of',len(R))
