#!/usr/bin/env python3
"""Generic Stage A review prompt + dispatch writer. Usage: make-prompt-generic.py CONFIG.json
Config: subject (file), title ('doctor-actor leftover-join.v12'), speakerV ('v12'), frozen ([[label,file],...]), row ('DR-114'), rowKind ('ROW'|'GATE'), gate ('G12'),
  namingParent (str), predecessorV (11), predecessorRecording ('D-170'), predecessorVersionsNotCurrent (str), occupancyLines ([str]), crossLines ([str]), leftoverDesign ([...]),
  doNotSatisfy ([...]), doNotInvent (str), doNotSteal (str), doNotRecord ([str]), extraFacts ([str]), attacks ([str]), landsLine (str), tokenNote (str), lineagesLine (str), fileToken ('OPEN')"""
import json,hashlib,os,re,subprocess,sys
REPO='/Users/sb/code/opensip-ai/opensip'; os.chdir(REPO); A='docs/coop/artifacts/'
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
def git(*a): return subprocess.check_output(['git',*a],text=True).strip()
c=json.load(open(sys.argv[1]))
HEAD=git('rev-parse','HEAD'); LASTD=re.match(r'## (D-\d+)',[l for l in open('docs/coop/COORDINATOR-DECISIONS.md') if l.startswith('## D-')][-1]).group(1)
S=A+c['subject']; assert oct(os.stat(S).st_mode)[-3:]=='444'; SHA=sha(S); v=json.load(open(S)); assert v['head']==HEAD,'subject HEAD pin != live HEAD'
stem=c['subject'][:-5]; LD='`['+', '.join(c['leftoverDesign'])+']`'
frozen='\n'.join(f"Frozen {lab} stays unmoved at\n`{sha(A+f)}`." for lab,f in c['frozen'])

def _adopt_commit(d):
    for l in subprocess.check_output(['git','log','--format=%H %s'],text=True).splitlines():
        if re.match(rf'^[0-9a-f]+ {d}: ',l): return l.split()[0]
    raise SystemExit('no recording commit for '+d)
_AD=_adopt_commit(LASTD)
if HEAD==_AD: HEADROLE=f"{LASTD} ADOPTED"
else:
    _between=subprocess.check_output(['git','log','--format=%H %s',f'{_AD}..{HEAD}'],text=True).splitlines()
    assert _between and all(re.match(rf'^[0-9a-f]+ {LASTD} hygiene: ',l) for l in _between), ('HEAD is neither the adoption commit nor a following hygiene commit',_between)
    HEADROLE=f"{LASTD} hygiene commit `{HEAD[:7]} "+_between[0].split(' ',1)[1]+f"`; {LASTD} ADOPTED at `{_AD}`"

prompt=f"""# Adversarial review — {c['title']}

Independent, refute not confirm.

**SUBJECT:** `docs/coop/artifacts/{c['subject']}`
Expected sha256:
`{SHA}`
Mode 0444. If the subject moves, REJECT.

{frozen}

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/{stem}.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/{stem}.review-independent.codex.json`

Do not edit the subject. Do not commit. Do not edit file 08 or COORD.
{' '.join('Do not SATISFY '+r+'.' for r in c['doNotSatisfy'])}
Do not open Class A. Do not execute {c['gate']}.
{c['doNotInvent']}
{c['doNotSteal']}
Do not occupy the identifier.
{chr(10).join(c['doNotRecord'])}
Do not flatten DR-118 `DECIDED-V1-NOT-INTEGRATED` to `OPEN`.
Do not flatten DR-107 `PROPOSED-CLOSED-FOR-REVIEW` to `OPEN`.
Do not read the other reviewer.

HEAD is `{HEAD}` ({HEADROLE}).
Last heading is {LASTD}. Required-now is 28.

This is leftover remasurement, not SATISFIED-GRADE.
Speaker labels this {c['speakerV']} ({c['title']}). leftover-join.v{c['predecessorV']} stays unmoved.
leftoverDesign remains {LD}.
This is a {c['row']} {c['rowKind']} leftover-join. {c['namingParent']}
{chr(10).join(c['occupancyLines'])}
leftover-join.v{c['predecessorV']} remains the current recorded {c['row']} leftover-join at draft time ({c['predecessorRecording']}).
After this successor is recorded, leftover-join.v{c['predecessorV']} is not current. {c.get('predecessorVersionsNotCurrent','')}
{chr(10).join(c['crossLines'])}
{c['lineagesLine']}
{c.get('tokenNote','')}
{chr(10).join(c.get('extraFacts',[]))}
predecessorV{c['predecessorV']}.recording must be {c['predecessorRecording']}.
{c['landsLine']}
basedOn.d{LASTD[2:]}.role is last-heading custody only.
file08StatusToken is `{c['fileToken']}`.

Attack:
{chr(10).join('- '+a for a in c['attacks'])}
- last-heading basedOn.role is not last-heading custody only
- predecessorV{c['predecessorV']} omits recording {c['predecessorRecording']}
- predecessorV{c['predecessorV']}.role carries unfounded Landed in this lineage
- records leftover-join.v{c['predecessorV']} as not current at draft time without the successor-recorded qualifier
- records leftover-join.v{c['predecessorV']} as current after this successor
- changes live required-now 28
- cited digests or recording commits do not match live bytes / git log
- subject moved
- occupies the identifier
- authorizes docs/v2/implementation/

ACCEPT only if no MUST-FIX or SHOULD-FIX.
Final chat: ACCEPT or REJECT.
"""
pp=A+stem+'.review-prompt.md'; assert not os.path.exists(pp); open(pp,'w').write(prompt); os.chmod(pp,0o444)
dispatch=f"""Adversarial review of {c['title']}. Stage A. Independent, refute not confirm.

Read docs/coop/artifacts/{stem}.review-prompt.md
and execute it.

SUBJECT sha256 must be
{SHA}
Mode 0444. If the subject moved, REJECT.

Write only your review JSON path from that prompt.
Do not edit the subject. Do not commit. Do not edit file 08 or COORD.

leftover-join.v{c['predecessorV']} remains the current recorded {c['row']} leftover-join at draft time ({c['predecessorRecording']}).
{chr(10).join(c['occupancyLines'])}
{chr(10).join(c['crossLines'])}
leftoverDesign remains {LD}.
file08StatusToken {c['fileToken']}.
Speaker labels this {c['speakerV']} ({c['title']}).
{c['lineagesLine']}

ACCEPT only if no MUST-FIX or SHOULD-FIX.
Final chat: ACCEPT or REJECT.
"""
dp=A+'_dispatch.'+stem+'.txt'; open(dp,'w').write(dispatch)
print('prompt',pp,sha(pp)); print('dispatch',dp,len(dispatch)); print('subject',SHA)
