# Independent v5 probes, group D: historical preservation, governance-artifact consistency after the delta.
import json,hashlib,os,re
from pathlib import Path
SUB='/tmp/opensip-design-corrections/candidate-subject.v5'
V4='/tmp/opensip-design-corrections/candidate-subject.v4'
DC=SUB+'/docs/coop/design-corrections'
R=[]
def p(pid,title,ok,detail=''):
    R.append({'id':pid,'title':title,'result':'PASS' if ok else 'FAIL','detail':str(detail)[:900]})
    print(('PASS ' if ok else 'FAIL ')+pid+' :: '+title+((' :: '+str(detail)[:300]) if detail else ''))
def sha(f): return hashlib.sha256(Path(f).read_bytes()).hexdigest()
delta=json.load(open('/tmp/opensip-design-corrections/post-reset-review.v5/probes/delta.json'))

# D1 historical preservation report is true against the frozen bytes
hp=json.load(open(DC+'/historical-preservation-report.v5.json'))
bad=[]
for e in hp['files']:
    fp=os.path.join(SUB,e['path'])
    if not os.path.exists(fp): bad.append((e['path'],'absent')); continue
    a=sha(fp)
    if a!=e['currentSha256'] or a!=e['openingSha256'] or not e['unchanged']: bad.append((e['path'],'mismatch'))
p('D1','all 31 historical files verify unchanged against the frozen subject bytes',
  not bad and hp['unchanged']==31 and hp['changed']==[] ,{'bad':bad[:5],'unchanged':hp['unchanged'],'changed':hp['changed']})
p('D1b','no historically preserved file appears in the v4->v5 delta',
  not (set(e['path'] for e in hp['files']) & set(delta['modified']+delta['added'])),'')
p('D1c','the delta removed nothing',delta['removed']==[],delta['removed'])

# D2 the five product contracts + index: only three changed, exactly as claimed
C='docs/v2/contracts/product-v1/'
contracts=['README.md','admission-and-qualification.md','identity-and-evidence.md','native-evidence.md',
           'security-and-lifecycle.md','workflows-and-surfaces.md']
status={c:('CHANGED' if sha(SUB+'/'+C+c)!=sha(V4+'/'+C+c) else 'UNCHANGED') for c in contracts}
p('D2','exactly native-evidence, security-and-lifecycle and workflows-and-surfaces changed',
  sorted(k for k,v in status.items() if v=='CHANGED')==['native-evidence.md','security-and-lifecycle.md','workflows-and-surfaces.md'],status)

# D3 governance artifacts unchanged AND still true after the delta
gov=['D-372-corrections.proposed.md','current-source-map.proposed.md','inherited-residuals.proposed.md',
     'evaluation-residual-dispositions.proposed.json','qualification-gates.proposed.json',
     'correction-crosswalk.proposed.json','inherited-row-sources.proposed.json']
unch=[g for g in gov if sha(DC+'/'+g)==sha(V4+'/docs/coop/design-corrections/'+g)]
p('D3','all seven governance artifacts byte-unchanged from v4',len(unch)==len(gov),
  sorted(set(gov)-set(unch)))

d372=Path(DC+'/D-372-corrections.proposed.md').read_text()
INV=json.load(open(DC+'/workflows/command-inventory.v1.json'))
sarif=sorted(c['name'] for c in INV['commands'] if 'sarif' in c['formats'])
p('D3b','D-372 claim "SARIF exactly for default, analyze, audit and repair-verify" still true',
  'advertises SARIF exactly for default, analyze, audit and repair-verify' in d372
  and sarif==['analyze','audit','default','repair-verify'],sarif)
p('D3c','D-372 claim "advisory-only commands do not gain SARIF or a verdict" still true',
  'advisory-only commands do not gain SARIF or a verdict' in d372
  and not [c['name'] for c in INV['commands'] if c.get('advisory') and ('sarif' in c['formats'] or 'verdict' in c['parityFields'])],
  [c['name'] for c in INV['commands'] if c.get('advisory') and 'verdict' in c['parityFields']])

# D4 DR-G17 gate row remains an unperformed gate and is now design-determinate
q=json.load(open(DC+'/qualification-gates.proposed.json'))
g17=[i for i in q['items'] if i['id']=='DR-G17'][0]
p('D4','DR-G17 remains DESIGN-CONTRACT-PENDING-REVIEW, not qualified, not demonstrated',
  g17['standing']=='DESIGN-CONTRACT-PENDING-REVIEW' and g17['qualified'] is False
  and g17['demonstrated'] is False and g17['implementationHarnessAuthored'] is False,
  {k:g17[k] for k in ('standing','qualified','demonstrated','implementationHarnessAuthored')})
p('D4b','G17 threshold "omission only by not advertising, never silent semantic loss" now holds in the inventory',
  'never by silent semantic loss' in g17['thresholdDisposition']
  and all(set(['findings','verdict'])<=set(c['parityFields']) for c in INV['commands'] if 'sarif' in c['formats']),'')
p('D4c','no qualification gate was flipped to qualified/demonstrated by this delta',
  not any(i.get('qualified') or i.get('demonstrated') for i in q['items']),
  [i['id'] for i in q['items'] if i.get('qualified') or i.get('demonstrated')])

# D5 FW-11 owner text unchanged in the source map while the workflow contract restates it
sm=Path(DC+'/current-source-map.proposed.md').read_text()
wfmd=Path(SUB+'/'+C+'workflows-and-surfaces.md').read_text()
p('D5','FW-11 source-map row unchanged and the workflow contract now restates it (no fork)',
  'FW-11 weakened safeguards/metric redistribution' in sm
  and 'Architecture13 §6 restrictions remain binding' in sm
  and '### Numeric comparisons and metric redistribution (FW-11)' in wfmd
  and 'architecture13 §6 comparability restriction is binding here' in wfmd.replace('\n',' ').replace('  ',' '),'')

# D6 readiness / condition 5 untouched
vs=json.load(open(DC+'/validation-summary.v1.json'))
p('D6','validation summary still declares readinessChanged false and no product qualification',
  vs['readinessChanged'] is False and 'no product qualification' in vs['standing'],vs['standing'][:90])
p('D6b','validation summary counts match the reproduced reports',
  vs['workflows']['checksPassed']==1253 and vs['integration']['checksPassed']==319
  and vs['foundation']['checksPassed']==397 and vs['security']['casesPassed']==444
  and vs['native']['casesPassed']==101,
  {k:(vs[k].get('checksPassed') or vs[k].get('casesPassed')) for k in ('foundation','security','native','workflows','integration')})
p('D6c','dispositions file claims neither independent acceptance nor implementation authorization',
  json.load(open(DC+'/post-reset-dispositions.v5.proposed.json'))['independentAcceptance'] is False
  and json.load(open(DC+'/post-reset-dispositions.v5.proposed.json'))['implementationAuthorized'] is False,'')

# D7 coordination-document currency (observation)
nr=Path(DC+'/reviews/NEXT-REVIEW.md').read_text()
stale = ('workflows1206' in nr or 'integration311' in nr or '2a2168c3006174ab5d130054144374698f2026686a0daab7ed1eca38c365c2e2' in nr)
p('D7','NEXT-REVIEW.md currency vs the v5 subject it ships in',not stale,
  'stale: still describes the v4 review as active and cites workflows1206/integration311 and the v4 manifest'
  if stale else 'current')
p('D7b','the authoritative counts file (validation-summary) IS current, so no normative contradiction',
  vs['workflows']['checksPassed']==1253 and vs['claudeFinalReview']=='PENDING-FROZEN-V5',vs['claudeFinalReview'])

json.dump(R,open('/tmp/opensip-design-corrections/post-reset-review.v5/probes/claude-probes-D.json','w'),indent=1)
print('\nD-group:',sum(1 for x in R if x['result']=='PASS'),'PASS',sum(1 for x in R if x['result']=='FAIL'),'FAIL of',len(R))
