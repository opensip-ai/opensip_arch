# D1 corrected: the preservation report concerns REPOSITORY bytes, not snapshot bytes (read-only check).
import json,hashlib,os
from pathlib import Path
SUB='/tmp/opensip-design-corrections/candidate-subject.v5'
REPO='/Users/sb/code/opensip-ai/opensip_arch'
DC=SUB+'/docs/coop/design-corrections'
R=[]
def p(pid,title,ok,detail=''):
    R.append({'id':pid,'title':title,'result':'PASS' if ok else 'FAIL','detail':str(detail)[:900]})
    print(('PASS ' if ok else 'FAIL ')+pid+' :: '+title+((' :: '+str(detail)[:320]) if detail else ''))
def sha(f): return hashlib.sha256(Path(f).read_bytes()).hexdigest()
hp=json.load(open(DC+'/historical-preservation-report.v5.json'))
bad=[];insnap=0
for e in hp['files']:
    fp=os.path.join(REPO,e['path'])
    if not os.path.exists(fp): bad.append((e['path'],'absent-in-repo')); continue
    a=sha(fp)
    if a!=e['currentSha256']: bad.append((e['path'],'current-mismatch'))
    if e['openingSha256']!=e['currentSha256'] or not e['unchanged']: bad.append((e['path'],'declared-changed'))
    if os.path.exists(os.path.join(SUB,e['path'])): insnap+=1
p('D1','all 31 historically preserved files verify byte-unchanged in the repository',
  not bad and hp['unchanged']==31 and hp['changed']==[],{'bad':bad[:6],'unchanged':hp['unchanged'],'changed':hp['changed']})
p('D1e','preservation report covers repository history outside the frozen review subject',
  insnap==0,{'alsoInSnapshot':insnap})
# none of them is a product contract or a design-corrections artifact
p('D1f','no preserved historical file is a current product contract or correction artifact',
  not any(f['path'].startswith(('docs/v2/contracts/product-v1/','docs/coop/design-corrections/')) for f in hp['files']),
  sorted({f['path'].split('/')[2] if f['path'].count('/')>2 else f['path'] for f in hp['files']})[:8])
json.dump(R,open('/tmp/opensip-design-corrections/post-reset-review.v5/probes/claude-probes-D2.json','w'),indent=1)
print('\nD2-group:',sum(1 for x in R if x['result']=='PASS'),'PASS',sum(1 for x in R if x['result']=='FAIL'),'FAIL of',len(R))
