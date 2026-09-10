# Corrected re-runs of B4 / B6 (prior failures were probe defects: wrapped prose, wrong pin root).
import json,os,hashlib,re
from pathlib import Path
SUB='/tmp/opensip-design-corrections/post-reset-review.v5/scratch/subject'
DC=SUB+'/docs/coop/design-corrections'
R=[]
def p(pid,title,ok,detail=''):
    R.append({'id':pid,'title':title,'result':'PASS' if ok else 'FAIL','detail':str(detail)[:900]})
    print(('PASS ' if ok else 'FAIL ')+pid+' :: '+title+((' :: '+str(detail)[:300]) if detail else ''))
def sha(f): return hashlib.sha256(Path(f).read_bytes()).hexdigest()
def flat(s): return re.sub(r'\s+',' ',s)

wf=Path(SUB+'/docs/v2/contracts/product-v1/workflows-and-surfaces.md').read_text()
sec=wf.split('### Numeric comparisons and metric redistribution (FW-11)')
body=flat(sec[1]) if len(sec)==2 else ''
need=['same metric definition','supplied diff scope','comparison base','reported incompatible',
      'never presented as an improvement','redistribution, not evidence of behavioral improvement',
      'Typed scope/policy/waiver/evidence deltas remain distinct from code changes']
miss=[n for n in need if n not in body]
p('B4','FW-11 comparability restated in the owning workflow contract (whitespace-normalised)',
  len(sec)==2 and not miss,{'missing':miss})

# B6 corrected: pin paths are repository-root relative
tot=0;allbad=[];per={}
for nm,pp in [('foundation',DC+'/foundation/source-pins.v1.json'),
              ('security',DC+'/security/source-pins.v1.json'),
              ('native',DC+'/native/source-pins.v2.json'),
              ('workflows',DC+'/workflows/source-pins.v1.json')]:
    d=json.load(open(pp)); entries=d.get('files') or d.get('pins'); n=0; bad=[]
    for e in entries:
        fp=os.path.join(SUB,e['path'])
        if not os.path.exists(fp): bad.append((e['path'],'absent')); continue
        n+=1
        if sha(fp)!=e['sha256']: bad.append((e['path'],'digest-mismatch'))
    per[nm]={'pins':len(entries),'resolved':n,'bad':bad}
    tot+=len(entries); allbad+=[(nm,)+b for b in bad]
p('B6','all four source-pin sets resolve to current subject bytes',not allbad,
  {'totalPins':tot,'per':{k:{'pins':v['pins'],'bad':len(v['bad'])} for k,v in per.items()},'bad':allbad[:8]})

# B6c: every changed model/checker/schema/case file is covered by some pin set (no unpinned drift)
changed=[c for c in json.load(open('/tmp/opensip-design-corrections/post-reset-review.v5/probes/delta.json'))['modified']]
allpins=set()
for pp in [DC+'/foundation/source-pins.v1.json',DC+'/security/source-pins.v1.json',
           DC+'/native/source-pins.v2.json',DC+'/workflows/source-pins.v1.json']:
    d=json.load(open(pp)); allpins|={e['path'] for e in (d.get('files') or d.get('pins'))}
code=[c for c in changed if c.endswith(('.py','.json','.md')) and '/reviews/' not in c
      and not c.endswith(('source-pins.v1.json','source-pins.v2.json','validation-summary.v1.json',
                          'integration-report.v1.json','workflows-report.v1.json',
                          'workflows-validation-report.json','README.md'))]
unpinned=[c for c in code if c not in allpins]
p('B6c','every changed normative/model/schema/case file is pinned by a suite',
  not unpinned,{'changedConsidered':code,'unpinned':unpinned})

# B6d: pins are self-consistent across suites (same path -> same digest)
bydigest={}
conflict=[]
for pp in [DC+'/foundation/source-pins.v1.json',DC+'/security/source-pins.v1.json',
           DC+'/native/source-pins.v2.json',DC+'/workflows/source-pins.v1.json']:
    d=json.load(open(pp))
    for e in (d.get('files') or d.get('pins')):
        if e['path'] in bydigest and bydigest[e['path']]!=e['sha256']: conflict.append(e['path'])
        bydigest[e['path']]=e['sha256']
p('B6d','no cross-suite pin disagreement on a shared path',not conflict,conflict[:5])

json.dump(R,open('/tmp/opensip-design-corrections/post-reset-review.v5/probes/claude-probes-B2.json','w'),indent=1)
print('\nB2-group:',sum(1 for x in R if x['result']=='PASS'),'PASS',sum(1 for x in R if x['result']=='FAIL'),'FAIL of',len(R))
