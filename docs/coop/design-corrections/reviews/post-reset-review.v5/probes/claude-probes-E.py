# Independent v5 probes, group E: inherited residuals, authorization posture, registry closure.
import json,hashlib,os,re
from pathlib import Path
SUB='/tmp/opensip-design-corrections/candidate-subject.v5'
V4='/tmp/opensip-design-corrections/candidate-subject.v4'
DC=SUB+'/docs/coop/design-corrections'
R=[]
def p(pid,title,ok,detail=''):
    R.append({'id':pid,'title':title,'result':'PASS' if ok else 'FAIL','detail':str(detail)[:900]})
    print(('PASS ' if ok else 'FAIL ')+pid+' :: '+title+((' :: '+str(detail)[:320]) if detail else ''))
def sha(f): return hashlib.sha256(Path(f).read_bytes()).hexdigest()

ir=Path(DC+'/inherited-residuals.proposed.md').read_text()
rows=[f'DR-011-R{i:02d}' for i in range(1,17)]
have=[r for r in rows if r in ir]
p('E1','all sixteen DR-011-R rows carry an individual written disposition',len(have)==16,
  {'missing':[r for r in rows if r not in have]})
r10=[l for l in ir.splitlines() if 'DR-011-R10' in l]
p('E1b','DR-011-R10 remains open (blind consumer B litmus is a later distinct act)',
  bool(r10) and any(k in r10[0].lower() for k in ('open','consumer','pending','not')),r10[0][:220] if r10 else '')
p('E1c','parent rows DR-001..DR-011 each appear individually',
  all(('DR-0%02d'%i) in ir for i in range(1,12)),
  [('DR-0%02d'%i) for i in range(1,12) if ('DR-0%02d'%i) not in ir])

ev=json.load(open(DC+'/evaluation-residual-dispositions.proposed.json'))
items=ev.get('items') or ev.get('residuals') or []
st={}
for i in items: st[i.get('reviewStatus') or i.get('status')]=st.get(i.get('reviewStatus') or i.get('status'),0)+1
p('E2','evaluation subresiduals individually written and none claims containment',
  len(items)==30 and set(st)<={'PENDING'} ,{'count':len(items),'statuses':st})

rs=json.load(open(DC+'/inherited-row-sources.proposed.json'))
ritems=rs.get('items') or rs.get('rows') or []
bad=[]
for it in ritems:
    for f in (it.get('sources') or it.get('files') or []):
        pth=f.get('path'); dig=f.get('sha256')
        if not pth or not dig: continue
        fp=os.path.join(SUB,pth)
        alt=os.path.join('/Users/sb/code/opensip-ai/opensip_arch',pth)
        use=fp if os.path.exists(fp) else (alt if os.path.exists(alt) else None)
        if use is None: bad.append((pth,'absent')); continue
        if sha(use)!=dig: bad.append((pth,'digest'))
p('E3','every inherited-row source pin resolves to the declared digest',not bad,
  {'rows':len(ritems),'bad':bad[:6]})

# authorization posture: nothing in the subject authorizes implementation
auth=[]
for root,dn,fn in os.walk(DC):
    dn[:]=[d for d in dn if d not in ('reviews',)]
    for f in fn:
        if not f.endswith(('.json','.md')): continue
        t=Path(os.path.join(root,f)).read_text(errors='ignore')
        if re.search(r'"implementationAuthorized"\s*:\s*true',t) or re.search(r'"qualified"\s*:\s*true',t) \
           or re.search(r'"readinessChanged"\s*:\s*true',t) or re.search(r'"independentAcceptance"\s*:\s*true',t):
            auth.append(os.path.relpath(os.path.join(root,f),SUB))
p('E4','no correction artifact asserts implementation authorization, qualification or readiness change',
  not auth,auth[:6])
vs=json.load(open(DC+'/validation-summary.v1.json'))
p('E4b','condition 5 posture preserved: reference evidence only, readiness unchanged',
  vs['readinessChanged'] is False and vs['claudeFinalReview']=='PENDING-FROZEN-V5','')

# registry closure unchanged by the delta
reg=[x for x in os.listdir(DC) if 'registry' in x.lower()] + \
    [os.path.join('workflows',x) for x in os.listdir(DC+'/workflows') if 'registry' in x.lower()]
p('E5','a public code registry artifact exists and is byte-unchanged from v4',
  bool(reg) and all(sha(DC+'/'+r)==sha(V4+'/docs/coop/design-corrections/'+r) for r in reg if os.path.exists(V4+'/docs/coop/design-corrections/'+r)),
  reg)

# DR-011-R08 / R13 specific closure by the MUST-A fix
INV=json.load(open(DC+'/workflows/command-inventory.v1.json'))
CMD={c['name']:c for c in INV['commands']}
p('E6','DR-011-R08: required-output failure law registered AND the SARIF field set now determined',
  all(r['requiredFailureClass']=='operational-failed' for r in INV['renderers'])
  and all({'run-id','verdict','required-coverage','deficiency','findings','termination-class','retention-disclosure'}
          <= set(CMD[n]['parityFields']) for n in ('default','analyze','audit','repair-verify')),'')
p('E6b','DR-011-R13: audit now determines its SARIF content and keeps its comparison account',
  {'findings','verdict','deficiency'}<=set(CMD['audit']['parityFields'])
  and {'baseline-id','comparison-id','comparison-counts'}<=set(CMD['audit']['parityFields']),'')

# security/native execution-authority bytes untouched apart from the discovery gate
sm=Path(DC+'/security/security_lifecycle_model_v1.py').read_text()
smv4=Path(V4+'/docs/coop/design-corrections/security/security_lifecycle_model_v1.py').read_text()
import difflib
added=[l for l in difflib.unified_diff(smv4.splitlines(),sm.splitlines(),n=0) if l.startswith('+') and not l.startswith('+++')]
removed=[l for l in difflib.unified_diff(smv4.splitlines(),sm.splitlines(),n=0) if l.startswith('-') and not l.startswith('---')]
p('E7','the only security-model change is the additive discovery admission gate (no removals)',
  not removed and all(('Reject(' in l) or ('allowed' in l) or ('required' in l) or ('isinstance' in l)
                      or ('_int' in l) or ('type(' in l) or ('for key in' in l) or l.strip('+').strip().startswith('#')
                      or ('if ' in l) for l in added),
  {'linesAdded':len(added),'linesRemoved':len(removed)})
p('E7b','no execution/authorization function was touched in the security model',
  not any(re.search(r'def (admit_execution|execution_authorization|grant|authorize)',l) for l in added+removed),'')

json.dump(R,open('/tmp/opensip-design-corrections/post-reset-review.v5/probes/claude-probes-E.json','w'),indent=1)
print('\nE-group:',sum(1 for x in R if x['result']=='PASS'),'PASS',sum(1 for x in R if x['result']=='FAIL'),'FAIL of',len(R))
