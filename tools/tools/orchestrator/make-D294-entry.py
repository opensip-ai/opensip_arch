#!/usr/bin/env python3
"""Build (and with --apply append) the ADOPTED COORD entry for the D-294 convention act from the CONSENT-turn draft.
Usage: TURN=<n> python3 make-D294-entry.py [--apply]"""
import json, re, os, sys, hashlib, subprocess, datetime, textwrap
REPO='/Users/sb/code/opensip-ai/opensip'; os.chdir(REPO); A='docs/coop/artifacts/'; P=lambda n: A+n
COORD='docs/coop/COORDINATOR-DECISIONS.md'; F08='docs/v2/architecture/08-decision-and-readiness-register.md'
SCR='/private/tmp/claude-501/-Users-sb-code-opensip-ai-opensip/dcbad0ae-7fad-4c78-89e7-e93d989f5501/scratchpad/'
NEW='D-294'; TURN=int(os.environ.get('TURN','1')); TS='' if TURN==1 else f'.turn{TURN}'
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
TODAY=datetime.date.today().isoformat()
coord=open(COORD).read(); heads=[l for l in coord.split('\n') if l.startswith('## D-')]; assert heads[-1].startswith('## D-293 '), heads[-1]
DRAFT=P(f'coordinator-decisions.{NEW}{TS}.draft.md'); assert oct(os.stat(DRAFT).st_mode)[-3:]=='444'; DS=sha(DRAFT); d=open(DRAFT).read()
CLB=f'coordinator-decisions.{NEW}.review-adversarial.claude2{TS}.json'; CXB=f'coordinator-decisions.{NEW}.review-adversarial.codex{TS}.json'
def verdict(n):
    j=json.load(open(P(n))); v=j.get('verdict') or (j.get('decision') or {}).get('verdict'); mf=len(j.get('mustFix',[])); sf=len(j.get('shouldFix',[])); return v,mf,sf
for n in (CLB,CXB):
    v,mf,sf=verdict(n); assert v=='CONSENT' and mf==0 and sf==0,(n,v,mf,sf); assert oct(os.stat(P(n)).st_mode)[-3:]=='444'
# prior turns: verdicts and ids
prior=[]
for t in range(1,TURN):
    ts='' if t==1 else f'.turn{t}'
    for who,base in (('Claude 2','claude2'),('Codex','codex')):
        f=P(f'coordinator-decisions.{NEW}.review-adversarial.{base}{ts}.json'); j=json.load(open(f))
        ids=[x.get('id') for k in ('mustFix','shouldFix') for x in j.get(k,[]) if isinstance(x,dict) and x.get('id')]
        prior.append(f"turn-{t} {who} {j.get('verdict')} ({', '.join(ids)}; `{sha(f)}`)")
title=re.match(r'# D-294 — (.+)',d).group(1).strip()
def section(name):
    m=re.search(rf'^## {re.escape(name)}\n(.*?)(?=^## |\Z)',d,re.S|re.M); assert m,name; return m.group(1).strip('\n')
decision=section('Decision'); readiness=section('Readiness effect'); revers=section('Reversibility')
# counts and pairs from the facts file written by the generator
facts=json.load(open(SCR+'D288-facts.json')); nj,npair,ns=facts['counts']
joins=sorted(set(c[4] for c in facts['citing']))
NUM={8:'eight',10:'ten'}
pairs=[f"{k[0]} leftover-join.v{k[1]} → {k[2]} leftover-join.v{k[3]}" for k,rs in facts['pairs']]
def bullet(label,body): return textwrap.fill(f'**{label}:** '+body,width=66,initial_indent='- ',subsequent_indent='  ',break_long_words=False,break_on_hyphens=False)
status=(f"**ADOPTED {TODAY}.** Turn {TURN} of 3: CONSENT from both independent reviewers, 0 MUST-FIX, 0 SHOULD-FIX. Claude 2 (`artifacts/{CLB}`, `{sha(P(CLB))}`) CONSENT. Codex (`artifacts/{CXB}`, `{sha(P(CXB))}`) CONSENT. Subject `coordinator-decisions.{NEW}{TS}.draft.md` `{DS}`."
        +(" Prior turns: "+'; '.join(prior)+'.' if prior else ''))
dtype=("RULE-GOVERNED. Records the reading convention for cross-lineage leftover-join citations (custody at recording, not standing currency claims) that D-293 adopted in principle and authorized for this dual-CONSENT cycle. "
       "Same no-cell-edit branch as D-170 through D-235 and D-237 through D-271 and D-273 through D-293. D-272 is CONTESTED and is not on that branch. Not a remasurement. Not a three-limb act. Not SATISFIED-GRADE. Not a D-000 amendment.")
subject=(f"`{DRAFT}` `{DS}`; its measured inputs are the {NUM.get(nj,nj)} citing leftover-joins "+', '.join(f"`{os.path.basename(j)}` `{sha(j)[:16]}…`" for j in joins)
         +f" (full digests in the draft's tables); file 08 `{sha(F08)}`.")
measured=(f"{NUM.get(nj,nj)} current leftover-joins carry {NUM.get(npair,npair)} present-tense cross-lineage citations of superseded sibling versions at {ns} sites: "+'; '.join(pairs)
          +". For every pair the cited version's and the current successor's leftoverDesign partitions are byte-identical and every projected field the draft names is equal wherever the cited version carries it; none requires a successor on that ground.")
body=[f"## {NEW} — {title}","",bullet('Date',TODAY),bullet('Status',status),bullet('Decision type',dtype),bullet('Subject',subject),bullet('Measured at draft time',measured),
      "- **Decision:**", textwrap.indent(decision,'  '), bullet('Readiness effect',re.sub(r'\s+',' ',readiness)), bullet('Reversibility',re.sub(r'\s+',' ',revers)), bullet('Commit',f"C-{NEW.replace('-','')}.")]
entry='\n'.join(body)+'\n'
assert not re.search(r'\{[^{}\n]{1,40}\}',entry) and 'turn 1 of 3' not in entry.lower() or TURN==1
tracked=set(subprocess.check_output(['git','ls-files'],text=True).split('\n'))
files=[COORD]
for t in range(1,TURN+1):
    ts='' if t==1 else f'.turn{t}'
    files+=[P(f'coordinator-decisions.{NEW}{ts}.draft.md'),P(f'coordinator-decisions.{NEW}{ts}.review-prompt.md'),P(f'coordinator-decisions.{NEW}.review-adversarial.claude2{ts}.json'),P(f'coordinator-decisions.{NEW}.review-adversarial.codex{ts}.json')]
files=[f for f in dict.fromkeys(files) if os.path.exists(f) and (f==COORD or f not in tracked or subprocess.call(['git','diff','--quiet','HEAD','--',f])!=0)]
if '--apply' in sys.argv:
    cur=open(COORD).read(); assert f'## {NEW} ' not in cur
    cur=cur if cur.endswith('\n') else cur+'\n'
    open(COORD,'w').write(cur+'\n---\n\n'+entry); print('APPENDED',NEW,'new COORD sha',sha(COORD))
else: print(entry)
print('\nCOMMIT FILES:'); [print(' ',f) for f in files]
open(SCR+f'commit-files.{NEW}.txt','w').write('\n'.join(files)+'\n')
