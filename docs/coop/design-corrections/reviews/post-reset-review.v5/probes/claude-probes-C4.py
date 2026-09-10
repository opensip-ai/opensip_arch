# C2c refinement: distinguish the SEMANTIC evaluation verdict (legitimately identity-bearing)
# from OUTPUT-PROJECTION / OPERATIONAL fields (must never be identity-bearing).
import json,hashlib
from pathlib import Path
SUB='/tmp/opensip-design-corrections/post-reset-review.v5/scratch/subject'
V4='/tmp/opensip-design-corrections/candidate-subject.v4'
DC=SUB+'/docs/coop/design-corrections'
R=[]
def p(pid,title,ok,detail=''):
    R.append({'id':pid,'title':title,'result':'PASS' if ok else 'FAIL','detail':str(detail)[:900]})
    print(('PASS ' if ok else 'FAIL ')+pid+' :: '+title+((' :: '+str(detail)[:320]) if detail else ''))
SCH=json.load(open(DC+'/foundation/identity-schemas.v2.json'))
DOMS=['fact','snapshot','closure','import','plan','subject-scope','coverage','view','execution-plan',
      'finding-fingerprint','finding','proof-bundle','semantic-evidence','evaluation-seal','run',
      'cache-key','regeneration-key','policy-derivation']
# Strictly output-projection / operational names introduced or touched by the v5 delta
OUTPUT_ONLY={'parityFields','runProperties','exitCode','termination-class','retention-disclosure',
             'required-coverage','net-new-findings','targets-remaining','snapshot-matched',
             'comparison-counts','pivots-available','audit-profile','baseline-id','comparison-id',
             'rule-deficiencies','deficiency','format','results'}
leak={}
for d in DOMS:
    toks=set(json.dumps(SCH['$defs'][d]).split('"'))
    hit=sorted(OUTPUT_ONLY & toks)
    if hit: leak[d]=hit
p('C2c','no identity domain admits an output-projection or operational field',not leak,leak)

# the three domains carrying `verdict` carry the SEMANTIC evaluation verdict, as a closed enum
det={}
for d in ('proof-bundle','evaluation-seal','policy-derivation'):
    node=SCH['$defs'][d]
    v=node.get('properties',{}).get('verdict')
    det[d]={'present':v is not None,'enum':v.get('enum') if isinstance(v,dict) else None}
p('C2c2','proof-bundle/evaluation-seal/policy-derivation verdict is a closed semantic enum, not a rendered value',
  all(x['present'] and x['enum'] for x in det.values()),det)

# the run domain carries no exit code / renderer / delivery field
runtoks=set(json.dumps(SCH['$defs']['run']).split('"'))
p('C2c3','the run identity domain carries no exit code, renderer or delivery field',
  not (runtoks & {'exitCode','format','sarif','renderer','delivery','runProperties'}),
  sorted(runtoks & {'exitCode','format','sarif','renderer','delivery','runProperties'}))

# and none of this moved in the delta
def sha(f): return hashlib.sha256(Path(f).read_bytes()).hexdigest()
p('C2c4','identity schemas byte-identical to v4 (verdict-in-seal predates the delta)',
  sha(SUB+'/docs/coop/design-corrections/foundation/identity-schemas.v2.json')==
  sha(V4+'/docs/coop/design-corrections/foundation/identity-schemas.v2.json'),'')

# the workflow parity `verdict` is a projection OF the seal verdict, not a second authority
wf=Path(SUB+'/docs/v2/contracts/product-v1/workflows-and-surfaces.md').read_text()
p('C2c5','the workflow contract treats the parity verdict as a projection, never a minted authority',
  'manufacture a Control verdict' in wf or 'never a fabricated Run' in wf,'')

json.dump(R,open('/tmp/opensip-design-corrections/post-reset-review.v5/probes/claude-probes-C4.json','w'),indent=1)
print('\nC4-group:',sum(1 for x in R if x['result']=='PASS'),'PASS',sum(1 for x in R if x['result']=='FAIL'),'FAIL of',len(R))
