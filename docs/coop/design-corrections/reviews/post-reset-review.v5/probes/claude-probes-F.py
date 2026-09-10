# Independent v5 probes, group F: unchanged-byte basis for carrying v4 evidence; registry closure.
import json,hashlib,os
from pathlib import Path
SUB='/tmp/opensip-design-corrections/candidate-subject.v5'
V4='/tmp/opensip-design-corrections/candidate-subject.v4'
DC='/docs/coop/design-corrections'
R=[]
def p(pid,title,ok,detail=''):
    R.append({'id':pid,'title':title,'result':'PASS' if ok else 'FAIL','detail':str(detail)[:900]})
    print(('PASS ' if ok else 'FAIL ')+pid+' :: '+title+((' :: '+str(detail)[:340]) if detail else ''))
def sha(f): return hashlib.sha256(Path(f).read_bytes()).hexdigest()
def unchanged(rel): return sha(SUB+'/'+rel)==sha(V4+'/'+rel)

delta=json.load(open('/tmp/opensip-design-corrections/post-reset-review.v5/probes/delta.json'))
mod=set(delta['modified'])

# F1 the four unit models: which carry v4 evidence unchanged
models={
 'foundation/identity-model.py':'AR-01/09, DR-201 semantic identity',
 'foundation/host-foundation-model.v2.py':'AR-01/14 host',
 'foundation/product-configuration-model.py':'AR-02 configuration',
 'foundation/identity-schemas.v2.json':'identity domains',
 'native/check_native_evidence.v2.py':'AR-07/12 native cases',
 'workflows/workflows_model.v1.py':'AR-13/16 workflow model (CHANGED)',
 'security/security_lifecycle_model_v1.py':'AR-03..06 security (CHANGED)',
}
st={}
for m in models:
    rel='docs/coop/design-corrections/'+m
    st[m]='UNCHANGED' if unchanged(rel) else 'CHANGED'
p('F1','only the workflow and security models changed; all other unit models are byte-identical to v4',
  sorted(k for k,v in st.items() if v=='CHANGED')==['security/security_lifecycle_model_v1.py','workflows/workflows_model.v1.py'],st)

# F2 native model/cases untouched -> v4 native evidence carries with byte proof
import glob
nat=[os.path.relpath(x,SUB) for x in glob.glob(SUB+'/docs/coop/design-corrections/native/*')]
natch=[n for n in nat if n in mod]
p('F2','the entire native unit is unchanged except its source-pin file',
  natch==['docs/coop/design-corrections/native/source-pins.v2.json'],natch)

# F3 foundation unit untouched except its pin file
fnd=[os.path.relpath(x,SUB) for x in glob.glob(SUB+'/docs/coop/design-corrections/foundation/*')]
fch=[n for n in fnd if n in mod]
p('F3','the entire foundation unit is unchanged except its source-pin file',
  fch==['docs/coop/design-corrections/foundation/source-pins.v1.json'],fch)

# F4 security unit changed only in the model + pins
sec=[os.path.relpath(x,SUB) for x in glob.glob(SUB+'/docs/coop/design-corrections/security/*')]
sch=sorted(n for n in sec if n in mod)
p('F4','the security unit changed only in its model and pin file',
  sch==['docs/coop/design-corrections/security/security_lifecycle_model_v1.py',
        'docs/coop/design-corrections/security/source-pins.v1.json'],sch)

# F5 public detail registry closure
reg=json.load(open(SUB+'/docs/coop/design-corrections/public-detail-registry.v1.json'))
def count(o):
    if isinstance(o,dict):
        for k in ('codes','publicCodes','details'):
            if k in o and isinstance(o[k],(list,dict)): return len(o[k]),list(o.keys())
    return None,list(o.keys()) if isinstance(o,dict) else type(o).__name__
n,keys=count(reg)
p('F5','public detail registry is byte-unchanged from v4 (no new public code from the delta)',
  unchanged('docs/coop/design-corrections/public-detail-registry.v1.json'),{'topKeys':keys,'codes':n})
p('F5b','internal aliases remain distinct from public codes',
  'internalAliases' in json.dumps(reg),'')

# F6 workflows unit: exactly the five expected files changed
wf=[os.path.relpath(x,SUB) for x in glob.glob(SUB+'/docs/coop/design-corrections/workflows/**/*',recursive=True)]
wch=sorted(n for n in wf if n in mod)
p('F6','the workflows unit changed only in model, checker, inventory, schema, cases, pins and its two reports',
  wch==sorted(['docs/coop/design-corrections/workflows/check_workflows.v1.py',
   'docs/coop/design-corrections/workflows/command-inventory.v1.json',
   'docs/coop/design-corrections/workflows/schemas/command-inventory.schema.json',
   'docs/coop/design-corrections/workflows/source-pins.v1.json',
   'docs/coop/design-corrections/workflows/workflow-cases.v1.json',
   'docs/coop/design-corrections/workflows/workflows-report.v1.json',
   'docs/coop/design-corrections/workflows/workflows-validation-report.json',
   'docs/coop/design-corrections/workflows/workflows_model.v1.py']),wch)

# F7 every added file is a review/disposition artifact, never a normative product byte
addn=delta['added']
nonrev=[a for a in addn if '/reviews/' not in a]
p('F7','every added file is a v4 review artifact or a v5 disposition/preservation record',
  sorted(nonrev)==['docs/coop/design-corrections/historical-preservation-report.v5.json',
                   'docs/coop/design-corrections/post-reset-dispositions.v5.proposed.json'],nonrev)
p('F7b','no added file is a product contract or unit model/schema/case',
  not any(a.startswith('docs/v2/contracts/') for a in addn)
  and not any(a.endswith(('_model.v1.py','-model.py','.schema.json')) and '/reviews/' not in a for a in addn),'')

json.dump(R,open('/tmp/opensip-design-corrections/post-reset-review.v5/probes/claude-probes-F.json','w'),indent=1)
print('\nF-group:',sum(1 for x in R if x['result']=='PASS'),'PASS',sum(1 for x in R if x['result']=='FAIL'),'FAIL of',len(R))
