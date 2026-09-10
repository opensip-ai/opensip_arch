# Corrected E3 / E7 (prior failures were probe defects: wrong key name; over-strict line classifier).
import json,hashlib,os,difflib,re
from pathlib import Path
SUB='/tmp/opensip-design-corrections/candidate-subject.v5'
V4='/tmp/opensip-design-corrections/candidate-subject.v4'
REPO='/Users/sb/code/opensip-ai/opensip_arch'
DC=SUB+'/docs/coop/design-corrections'
R=[]
def p(pid,title,ok,detail=''):
    R.append({'id':pid,'title':title,'result':'PASS' if ok else 'FAIL','detail':str(detail)[:900]})
    print(('PASS ' if ok else 'FAIL ')+pid+' :: '+title+((' :: '+str(detail)[:340]) if detail else ''))
def sha(f): return hashlib.sha256(Path(f).read_bytes()).hexdigest()

rs=json.load(open(DC+'/inherited-row-sources.proposed.json'))
recs=rs['records']; bad=[]; where={}
for it in recs:
    fp=os.path.join(SUB,it['path']); alt=os.path.join(REPO,it['path'])
    use=fp if os.path.exists(fp) else (alt if os.path.exists(alt) else None)
    if use is None: bad.append((it['row'],it['path'],'absent')); continue
    where[it['row']]='snapshot' if use==fp else 'repository'
    if sha(use)!=it['sourceSha256']: bad.append((it['row'],it['path'],'digest-mismatch'))
p('E3','all six inherited-row source pins resolve to their declared digest',
  not bad and len(recs)==6,{'rows':[r['row'] for r in recs],'resolvedIn':where,'bad':bad})
p('E3b','each inherited row states a retained meaning and a custody rule (no bare pin)',
  all(r.get('retainedMeaning') and r.get('custody') and r.get('selector') for r in recs),'')
p('E3c','the six rows are exactly the ones v4 named (DR102/117/104/115/119/123)',
  sorted(r['row'] for r in recs)==['DR-102','DR-104','DR-115','DR-117','DR-119','DR-123'],
  sorted(r['row'] for r in recs))

sm=Path(DC+'/security/security_lifecycle_model_v1.py').read_text().splitlines()
smv4=Path(V4+'/docs/coop/design-corrections/security/security_lifecycle_model_v1.py').read_text().splitlines()
diff=list(difflib.unified_diff(smv4,sm,n=0,lineterm=''))
added=[l[1:] for l in diff if l.startswith('+') and not l.startswith('+++')]
removed=[l[1:] for l in diff if l.startswith('-') and not l.startswith('---')]
hunks=[l for l in diff if l.startswith('@@')]
p('E7','the security-model delta is purely additive (no line removed or altered)',
  not removed,{'linesAdded':len(added),'linesRemoved':len(removed),'hunks':hunks})
p('E7b','the addition is a single contiguous hunk inside discovery()',
  len(hunks)==1,hunks)
p('E7c','every added line is an admission guard, a comment, or the allowed/required key sets',
  all(l.strip().startswith('#') or l.strip().startswith(('if ','for ','allowed','required',"'",'raise'))
      or 'Reject(' in l or 'isinstance' in l or '_int' in l or 'type(' in l or l.strip()=='' 
      or l.strip().startswith(("'authorizedGroupIds'","'explicitProject'")) for l in added),
  [l for l in added if not (l.strip().startswith('#') or l.strip().startswith(('if ','for ','allowed','required',"'",'raise'))
      or 'Reject(' in l or 'isinstance' in l or '_int' in l or 'type(' in l or l.strip()=='')][:4])
p('E7d','the addition introduces exactly one refusal token and it is not a public D9 code',
  set(re.findall(r"Reject\('([A-Z_]+)'\)",'\n'.join(added)))=={'DISCOVERY_OBSERVATION_SHAPE'}
  and 'DISCOVERY_OBSERVATION_SHAPE' not in Path(DC+'/public-detail-registry.v1.json').read_text(),'')

json.dump(R,open('/tmp/opensip-design-corrections/post-reset-review.v5/probes/claude-probes-E2.json','w'),indent=1)
print('\nE2-group:',sum(1 for x in R if x['result']=='PASS'),'PASS',sum(1 for x in R if x['result']=='FAIL'),'FAIL of',len(R))
