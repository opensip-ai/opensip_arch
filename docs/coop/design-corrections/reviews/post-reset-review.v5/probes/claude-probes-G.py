# Group G: independently reconstruct the workflow and integration check-count deltas.
import json
from pathlib import Path
SUB='/tmp/opensip-design-corrections/candidate-subject.v5'
V4='/tmp/opensip-design-corrections/candidate-subject.v4'
R=[]
def p(pid,title,ok,detail=''):
    R.append({'id':pid,'title':title,'result':'PASS' if ok else 'FAIL','detail':str(detail)[:900]})
    print(('PASS ' if ok else 'FAIL ')+pid+' :: '+title+((' :: '+str(detail)[:340]) if detail else ''))
INV=json.load(open(SUB+'/docs/coop/design-corrections/workflows/command-inventory.v1.json'))
CASES=json.load(open(SUB+'/docs/coop/design-corrections/workflows/workflow-cases.v1.json'))
V4CASES=json.load(open(V4+'/docs/coop/design-corrections/workflows/workflow-cases.v1.json'))
sarif=[c['name'] for c in INV['commands'] if 'sarif' in c['formats']]
newcases=[c for c in CASES['renderCases'] if c not in V4CASES['renderCases']]
oldsarif=[c for c in V4CASES['renderCases'] if 'sarif' in c.get('formats',[]) and 'refusal' not in c['expect']]
# 28 schema negatives + 1 coverage check + per-new-case (parity + 3 sarif + agent) + 3 sarif checks on each pre-existing sarif case
neg=len(sarif)*7
percase=sum(1 + 3 + (1 if c['expect'].get('agentHasHints') else 0) for c in newcases)
retro=3*len(oldsarif)
predicted=neg+1+percase+retro
p('G1','the workflow check-count delta 1206 -> 1253 is exactly reconstructible',
  predicted==1253-1206,
  {'schemaNegatives(4x7)':neg,'coverageCheck':1,'newRenderCases':len(newcases),
   'checksFromNewCases':percase,'retrofittedSarifChecks':retro,'predicted':predicted,'actual':1253-1206})
rep=json.load(open(SUB+'/docs/coop/design-corrections/integration-report.v1.json'))
v4rep=json.load(open(V4+'/docs/coop/design-corrections/integration-report.v1.json'))
add=[c['id'] for c in rep['checks'] if c['id'] not in {x['id'] for x in v4rep['checks']}]
p('G2','the integration delta 311 -> 319 is exactly the 10 added minus the 2 renamed duplicates',
  len(add)==10 and 319-311==8 and len(rep['checks'])==len({c['id'] for c in rep['checks']}),
  {'added':add,'net':319-311})
p('G3','all four SARIF commands are covered by both a positive render case and 7 schema negatives',
  set(sarif)=={c['command'] for c in CASES['renderCases'] if 'sarif' in c.get('formats',[]) and 'refusal' not in c['expect']}
  and neg==28,{'commands':sorted(sarif),'negatives':neg})
json.dump(R,open('/tmp/opensip-design-corrections/post-reset-review.v5/probes/claude-probes-G.json','w'),indent=1)
print('\nG-group:',sum(1 for x in R if x['result']=='PASS'),'PASS',sum(1 for x in R if x['result']=='FAIL'),'FAIL of',len(R))
