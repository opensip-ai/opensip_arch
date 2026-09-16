#!/usr/bin/env python3
"""D-295: record preview-product-boundary-successor.v{V} as DR-117 leftover remasurement.
Modes: draft (write Stage B draft to scratchpad), stageb (freeze draft + prompt + dispatch into artifacts), entry [--apply] (build/append the ADOPTED entry after dual CONSENT).
Env: TURN (default 1)."""
import json, re, os, sys, hashlib, subprocess, datetime, textwrap
REPO='/Users/sb/code/opensip-ai/opensip'; os.chdir(REPO); A='docs/coop/artifacts/'; P=lambda n: A+n
COORD='docs/coop/COORDINATOR-DECISIONS.md'; F08='docs/v2/architecture/08-decision-and-readiness-register.md'
SCR='/private/tmp/claude-501/-Users-sb-code-opensip-ai-opensip/dcbad0ae-7fad-4c78-89e7-e93d989f5501/scratchpad/'
NEW='D-295'; V=int(os.environ.get('PPBS_V','10')); SUBJ=f'preview-product-boundary-successor.v{V}.json'; PRED='preview-product-boundary-successor.v8.json'
REJ=[v for v in range(9,V)]
mode=sys.argv[1]; TURN=int(os.environ.get('TURN','1')); TS='' if TURN==1 else f'.turn{TURN}'
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
def git(*a): return subprocess.check_output(['git',*a],text=True).strip()
TODAY=datetime.date.today().isoformat(); HEAD=git('rev-parse','HEAD')
coord=open(COORD).read(); heads=[l for l in coord.split('\n') if l.startswith('## D-')]; LASTD=re.match(r'## (D-\d+)',heads[-1]).group(1); assert LASTD=='D-294', LASTD
def commit_of(d):
    for line in subprocess.check_output(['git','log','--format=%H %s'],text=True).splitlines():
        if re.match(rf'^[0-9a-f]+ {d}: ',line): return line.split()[0]
    raise SystemExit('no commit for '+d)
ADOPTED_AT=commit_of(LASTD); assert ADOPTED_AT==HEAD or (subprocess.call(['git','merge-base','--is-ancestor',ADOPTED_AT,HEAD])==0 and subprocess.check_output(['git','show',f'{ADOPTED_AT}:{COORD}'])==subprocess.check_output(['git','show',f'HEAD:{COORD}']))
assert oct(os.stat(P(SUBJ)).st_mode)[-3:]=='444'; SS=sha(P(SUBJ)); j=json.load(open(P(SUBJ))); assert j['head']==HEAD, ('subject pinned at another HEAD',j['head'],HEAD)
assert j['requiredNowUnchanged']==28 and j['file08StatusToken']=='OPEN' and j['status']=='CANDIDATE-NOT-APPLIED'
CLA=f'preview-product-boundary-successor.v{V}.review-independent.claude2.json'; CXA=f'preview-product-boundary-successor.v{V}.review-independent.codex.json'
def verdict(n):
    r=json.load(open(P(n))); v=r.get('verdict') or (r.get('decision') or {}).get('verdict');
    bl=len(r.get('blockers',[])); mf=len(r.get('mustFix',[])); sf=len(r.get('shouldFix',[])); return r,v,bl+mf,sf
def shape(n,label):
    r,v,mf,sf=verdict(n)
    fld='observationsNotFindings' if 'observationsNotFindings' in r else ('observations' if 'observations' in r else None)
    items=r.get(fld) if fld else None; adv=r.get('advisories'); advn=len(adv) if isinstance(adv,list) else (adv if isinstance(adv,int) else None)
    if not fld or not items:
        s=f"{label} returned "+("no observationsNotFindings field and no observations field" if not fld else f"an empty {fld} list")+("; no advisories field" if adv is None else f"; {advn} advisories"); ids=[]
    else:
        if all(isinstance(x,dict) for x in items):
            keys=sorted(set(k for x in items for k in x.keys())); ids=[x.get('id') for x in items if x.get('id')]
            s=f"{label} returned {len(items)} {'named ' if ids else 'unlabeled '}{fld} object{'s' if len(items)!=1 else ''} (with members {', '.join(keys)}{'; no identifiers' if not ids else ''})"+(f" {', '.join(ids)}" if ids else '')
        else:
            ids=[m.group(1) for x in items if isinstance(x,str) for m in [re.match(r'^\s*([A-Z]{1,4}-?\d+)[.:]',x)] if m]
            s=f"{label} returned {len(items)} {fld} string{'s' if len(items)!=1 else ''}"+(f" with inline markers {', '.join(ids)}" if ids else ' (no identifiers)')
        other='observations' if fld=='observationsNotFindings' else 'observationsNotFindings'
        s+=f"; no {other} field" if other not in r else f"; also a {other} field with {len(r.get(other) or [])} items"
        s+=("; no advisories field" if adv is None else f"; {advn} advisories")
    advids=[a.get('id') for a in (adv if isinstance(adv,list) else []) if isinstance(a,dict) and a.get('id')]
    if advids: s=s.replace(f'; {advn} advisories', f"; {advn} advisories {', '.join(advids)}")
    g=r.get('gradeRuling') or {}; ruling=g.get('ruling') if isinstance(g,dict) else None
    return s,ids+advids,ruling,g
def NUMW(n): return {0:'zero',1:'one',2:'two',3:'three',4:'four',5:'five',6:'six',7:'seven',8:'eight',9:'nine',10:'ten',11:'eleven',12:'twelve'}.get(n,str(n))
rA,vA,mfA,sfA=verdict(CLA); rX,vX,mfX,sfX=verdict(CXA)
assert vA=='ACCEPT' and mfA==0 and sfA==0 and vX=='ACCEPT' and mfX==0 and sfX==0, ('Stage A not dual ACCEPT 0/0',vA,mfA,sfA,vX,mfX,sfX)
for n in (CLA,CXA): assert oct(os.stat(P(n)).st_mode)[-3:]=='444', n
sA,idA,gA,gAo=shape(CLA,f'Claude Stage A preview-product-boundary-successor.v{V}'); sX,idX,gX,gXo=shape(CXA,f'Codex Stage A preview-product-boundary-successor.v{V}')
def idsent():
    both=[i for i in (idA,idX) if i]
    if not both: return 'Neither Stage A review returned an identifier; this entry names none.'
    parts=[]
    if idA: parts.append(f"the Claude identifier{'s' if len(idA)>1 else ''} {', '.join(idA)}")
    if idX: parts.append(f"the Codex identifier{'s' if len(idX)>1 else ''} {', '.join(idX)}")
    return 'This entry names '+' and '.join(parts)+'; no identifier is invented.'
grade=(f"Both Stage A reviews answered the grade question (D-005 form): Claude 2 `{gA}`, Codex `{gX}`. " if gA and gX else "The grade question was answered by "+(f"Claude 2 only (`{gA}`). " if gA else f"Codex only (`{gX}`). " if gX else "neither review. "))
sustained=(gA=='SUSTAINED FOR APPLICATION' and gX=='SUSTAINED FOR APPLICATION')
grade+=("This entry records those rulings as reviewer judgments; recording them opens no Class A and lifts no reservation." if sustained else "This entry records the rulings as given; the application-grade limb is not established by this entry.")
joins=[(k,v) for k,v in j['basedOn'].items() if isinstance(v,dict) and 'Join' in k and v.get('path')]
joinsent='; '.join(f"{os.path.basename(v['path']).replace('.json','')} ({v.get('recording','')})" for k,v in joins)
branch='D-170 through D-235 and D-237 through D-271 and D-273 through '+LASTD
doesnot=["mark any row SATISFIED.","SATISFY DR-117.","SATISFY DR-131.","SATISFY DR-133.","SATISFY DR-101.","open D-056 Class A.","lift D-137's express reservation.","decide which artifact a later D-056 Class A opening names.","replace, apply, or succeed product-boundary-successor-contract.v8 (D-116).","reopen leftover-design of unnamed EE classes (closed at D-159).","steal or close leftover-design of OBL-G29-FX-AUTHORING or OBL-G30-FX-AUTHORING.","steal leftover-design of OBL-FX-AUTHORING, OBL-G14-FX-AUTHORING, OBL-G16-FX-AUTHORING, OBL-G21-FX-AUTHORING, OBL-THRESHOLDS, OBL-MATRIX-CORPUS, or OBL-G13-RESERVED.","pin QUALIFIED.","name G13 into required-now.","invent fixture bytes, the DR-131 pack, a D9 code, a section 7.1 recipe, or a D-006 unit.","record preview-product-boundary-successor.v8 as current after this successor is recorded.","record preview-product-boundary-successor.v7 or v6 as current."]+[f"record preview-product-boundary-successor.v{v} (rejected at Stage A, unrecorded) as current." for v in REJ]+["edit file 08.","add a DR-G* row or change live required-now 28.","authorize `docs/v2/implementation/`.","edit COORD except the append-only adoption of this entry after CONSENT."]
doesnot_md='\n'.join(f"> **Does not** {d}" for d in doesnot)
lands=os.environ.get('LANDS','')
ADVSENT=''
for _who,_r in (('Claude',rA),('Codex',rX)):
    _ids=[a.get('id') for a in (_r.get('advisories') or []) if isinstance(a,dict) and a.get('id')]
    if _ids: ADVSENT+=f" {_who} Stage A advisor{'ies' if len(_ids)>1 else 'y'} {', '.join(_ids)} travel{'' if len(_ids)>1 else 's'} as honesty work."
REJSENT=''.join(f" Frozen preview-product-boundary-successor.v{v} was REJECTED at Stage A by both reviewers and is unrecorded; its findings landed at preview-product-boundary-successor.v{V}; it stays frozen; do not record it as current." for v in REJ)
draft=f"""# {NEW} — Record preview-product-boundary-successor.v{V} as DR-117 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** {TODAY}
> **Protocol:** D-000 new cycle, turn {TURN} of 3.{(' '+lands) if lands else ''}
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `{SUBJ}`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> {branch}. D-272 is CONTESTED and is not on that
> no-cell-edit adoption branch. Not a three-limb act. Not a
> required-now successor. Not SATISFIED-GRADE. This is
> coordinator decision **{NEW}**, not a register row.
{doesnot_md}

{LASTD} is ADOPTED at
`{ADOPTED_AT}`.
HEAD is `{HEAD}`.
Last live heading is {LASTD}. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
successor (not this draft):

| Reviewer | Path | sha256 | Verdict | Grade ruling |
|---|---|---|---|---|
| Claude 2 | `{P(CLA)}` | `{sha(P(CLA))}` | ACCEPT 0/0 | {gA or 'none'} |
| Codex | `{P(CXA)}` | `{sha(P(CXA))}` | ACCEPT 0/0 | {gX or 'none'} |

Stage A observation disposition (no change requested; no identifiers invented):

| Source | Identifiers | Standing |
|---|---|---|
| Claude | {', '.join(idA) or 'none'} | {sA} |
| Codex | {', '.join(idX) or 'none'} | {sX} |

{idsent()}

## Subject

`{P(SUBJ)}` `{SS}` — the DR-117 preview-scoped successor candidate, the candidate limb of the programme the owner adopted at D-293 Decision 5. It re-cites, at the versions current at HEAD, the twelve leftover-joins preview-product-boundary-successor.v8 (D-207) cited at versions since superseded: {joinsent}. Its fourteen enforcement-evidence classes equal preview-product-boundary-successor.v8's after normalizing the 42 sites it refreshed (40 cross-lineage currency citations and two EE-3a leftoverDesign partition sentences, enumerated in its `enforcementEvidence.classesRefresh`); its seven dispositions and p1p2g3Mapping equal preview-product-boundary-successor.v8's without normalization (both asserted at generation). It states the relationship to product-boundary-successor-contract.v8 (D-116): distinct lineages; neither applied; the preview-scoped candidate does not replace, apply, or succeed the contract; which of the two a later Class A opening names is not decided in the record and is not decided by the subject.

Under D-294, its cross-lineage citations are custody at this recording: a later successor of any cited join does not, by itself, make preview-product-boundary-successor.v{V} stale.

## Decision

Record preview-product-boundary-successor.v{V} as DR-117 leftover remasurement after {LASTD}. The candidate binds NOTHING. DR-117 stays `OPEN`. leftover-design of unnamed EE classes remains closed at D-159. Remainder is named-gate execution. leftover-design of OBL-G29-FX-AUTHORING and OBL-G30-FX-AUTHORING remains on g29 leftover-join.v4 (D-254) and g30 leftover-join.v4 (D-255). Does not steal those leftovers. Does not SATISFY DR-117. D-056 Eligibility gates 2 and 3 continue to hold for DR-117 (D-159). Gate 1 Class A remains false under D-137's express reservation; preview-product-boundary-successor.v{V} does not withdraw that reservation, and this entry does not lift it. Venue for the lift is the owner-controlled opening entry D-293 Decision 5 reserves, which follows this recording. {grade} Gates 4 and 5 are not performed. Not eligible in kind. Not SATISFIED. Required-now stays 28. Condition-4 effect is zero. Frozen preview-product-boundary-successor.v8 becomes a historical measurement as of HEAD `df1301a` / required-now 28 once this entry is adopted; it stays frozen; do not record it as current. Frozen preview-product-boundary-successor.v7 remains a historical measurement as of HEAD `5d5d778` / required-now 26.{REJSENT}{ADVSENT} Standing CLAUDE-PPBS-V3-ADV-1 venue limb stands. Does not invent fixture bytes or the DR-131 pack. Does not rewrite G13, G14, G29, G30, G31, or G32. Does not name G13 into required-now. Does not edit file 08. Does not invent a D9 code. Does not authorize `docs/v2/implementation/`.

## Readiness effect

Zero SATISFIED. Condition 2 stays 5 of 32. Condition 4 stays MET on the naming half (28 of 28). Condition 5 last.

## Reversibility

Total only before a later dependent leftover rewrite, Class A reservation lift, SATISFIED cycle, or file-08 cell rewrite. Overturn: C-{NEW.replace('-','')}. Does not unwrite D-116, D-137, D-157, D-158, D-159, D-168, D-207, D-240, D-254, D-255, D-273, D-274, D-277, D-278, D-283, D-285, D-287, D-288, D-292, D-293, or D-294.
"""
draft=re.sub(r'(?<=\S)  +(?=\S)',' ',draft)
bad=re.findall(r'\{[^{}\n]{1,40}\}',draft); assert not bad, bad; assert not re.search(r'\bThis v\d\b',draft)
out=SCR+f'coordinator-decisions.{NEW}{TS}.draft.md'; open(out,'w').write(draft)
if mode=='draft': print(draft); print('wrote',out,len(draft)); sys.exit()
CLB=f'coordinator-decisions.{NEW}.review-adversarial.claude2{TS}.json'; CXB=f'coordinator-decisions.{NEW}.review-adversarial.codex{TS}.json'
if mode=='stageb':
    DST=P(f'coordinator-decisions.{NEW}{TS}.draft.md'); assert not os.path.exists(DST); open(DST,'w').write(draft); os.chmod(DST,0o444); DS=sha(DST)
    prior=''
    if TURN>1:
        lines=[]
        for t in range(1,TURN):
            ts='' if t==1 else f'.turn{t}'
            for who,base in (('Claude','claude2'),('Codex','codex')):
                rf=P(f'coordinator-decisions.{NEW}.review-adversarial.{base}{ts}.json')
                if os.path.exists(rf):
                    rj=json.load(open(rf)); ids=[f.get('id') for k in ('mustFix','shouldFix') for f in rj.get(k,[]) if isinstance(f,dict) and f.get('id')]
                    lines.append(f"turn-{t} {who} {rj.get('verdict')}"+(f" ({' / '.join(ids)})" if ids else ''))
                else: lines.append(f"turn-{t} {who} review not returned (reviewer unavailable)")
            df=P(f'coordinator-decisions.{NEW}{ts}.draft.md'); lines.append(f"turn-{t} subject remains frozen at `{df}` `{sha(df)}`")
        prior='\n'+'; '.join(lines)+'.\n'
    prompt=f"""# Adversarial review — {NEW} turn {TURN}

Independent, refute not confirm.

**SUBJECT:** `{DST}`
Expected sha256:
`{DS}`
Mode 0444. If the subject moves, OBJECT.

**WRITE ONLY:**
- Claude 2: `{P(CLB)}`
- Codex: `{P(CXB)}`{prior}
Do not edit the subject. Do not commit. Do not edit file 08 or COORD.
Do not mark any row SATISFIED. Do not SATISFY DR-117, DR-131, DR-133, or DR-101. Do not open D-056 Class A. Do not lift D-137's reservation.
Do not flatten DR-118 `DECIDED-V1-NOT-INTEGRATED` to `OPEN`. Do not flatten DR-107 `PROPOSED-CLOSED-FOR-REVIEW` to `OPEN`.
Do not invent identifiers. Do not claim both reviewers' identifiers are preserved unless both returned identifiers.
Do not read the other reviewer's current-turn review.

HEAD is `{HEAD}`. {LASTD} is ADOPTED at `{ADOPTED_AT}`. Last heading is {LASTD}. Required-now is 28.
Live COORD sha256 is `{sha(COORD)}`; file 08 sha256 is `{sha(F08)}`.

preview-product-boundary-successor.v8 remains the current recorded DR-117 leftover remasurement at draft time (D-207). After this successor is recorded, preview-product-boundary-successor.v8 is not current.
The frozen subject of Stage A is `{P(SUBJ)}` `{SS}`; both Stage A reviews are ACCEPT 0/0 (paths and digests in the draft's table). Re-verify those digests and verdicts from the files.
{sA}. {sX}. {idsent()}
The draft records the Stage A grade rulings as reviewer judgments; check that it neither opens Class A nor lifts D-137's reservation on their strength.
Under D-294 (ADOPTED), the subject's twelve cross-lineage citations are custody at this recording; check each is the version current at HEAD.
The no-cell-edit branch is {branch}. D-272 is CONTESTED and is not on that adoption branch. The branch must not span D-236.

CONSENT only if no MUST-FIX or SHOULD-FIX.
Final chat: CONSENT or OBJECT.
"""
    pp=P(f'coordinator-decisions.{NEW}{TS}.review-prompt.md'); assert not os.path.exists(pp); open(pp,'w').write(prompt); os.chmod(pp,0o444)
    dispatch=f"""Adversarial review of {NEW} COORD draft. Turn {TURN} of 3.

Read {pp}
and execute it. Refute, do not confirm.

SUBJECT sha256 must be
{DS}
Mode 0444. If the subject moved, OBJECT.

Write only your review JSON path from that prompt.
Do not edit the subject. Do not commit. Do not edit file 08 or COORD. Do not read the other reviewer's current-turn review.
{sA}. {sX}. Do not invent identifiers.
CONSENT only if no MUST-FIX or SHOULD-FIX.
Final chat: CONSENT or OBJECT.
"""
    dp=P(f'_dispatch.{NEW}'+('' if TURN==1 else f'-t{TURN}')+'.txt'); open(dp,'w').write(dispatch)
    print('draft',DST,DS); print('prompt',pp,sha(pp)); print('dispatch',dp,len(dispatch)); sys.exit()
if mode=='entry':
    for n in (CLB,CXB):
        r=json.load(open(P(n))); v=r.get('verdict'); mf=len(r.get('mustFix',[])); sf=len(r.get('shouldFix',[])); assert v=='CONSENT' and mf==0 and sf==0,(n,v,mf,sf); assert oct(os.stat(P(n)).st_mode)[-3:]=='444'
    DRAFT=P(f'coordinator-decisions.{NEW}{TS}.draft.md'); assert oct(os.stat(DRAFT).st_mode)[-3:]=='444'
    prior=[]
    for t in range(1,TURN):
        ts='' if t==1 else f'.turn{t}'
        for who,base in (('Claude 2','claude2'),('Codex','codex')):
            f=P(f'coordinator-decisions.{NEW}.review-adversarial.{base}{ts}.json'); rj=json.load(open(f)); ids=[x.get('id') for k in ('mustFix','shouldFix') for x in rj.get(k,[]) if isinstance(x,dict) and x.get('id')]
            prior.append(f"turn-{t} {who} {rj.get('verdict')} ({', '.join(ids)}; `{sha(f)}`)")
    def bullet(label,body): return textwrap.fill(f'**{label}:** '+body,width=66,initial_indent='- ',subsequent_indent='  ',break_long_words=False,break_on_hyphens=False)
    status=(f"**ADOPTED {TODAY}.** Turn {TURN} of 3: CONSENT from both independent reviewers, 0 MUST-FIX, 0 SHOULD-FIX. Claude 2 (`artifacts/{CLB}`, `{sha(P(CLB))}`) CONSENT. Codex (`artifacts/{CXB}`, `{sha(P(CXB))}`) CONSENT. Subject `coordinator-decisions.{NEW}{TS}.draft.md` `{sha(DRAFT)}`. Frozen successor `{SUBJ}` `{SS}` Stage A Claude ACCEPT `{sha(P(CLA))}` 0/0, grade ruling {gA or 'none'}; Stage A Codex ACCEPT `{sha(P(CXA))}` 0/0, grade ruling {gX or 'none'}."+(" Prior turns: "+'; '.join(prior)+'.' if prior else ''))
    dtype=f"RULE-GOVERNED. Records independent dual ACCEPT of `{SUBJ}` (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as {branch}. D-272 is CONTESTED and is not on that branch. Not a three-limb act. Not SATISFIED-GRADE."
    dsec=re.search(r'^## Decision\n(.*?)(?=^## )',draft,re.S|re.M).group(1).strip()
    rsec=re.search(r'^## Readiness effect\n(.*?)(?=^## )',draft,re.S|re.M).group(1).strip(); vsec=re.search(r'^## Reversibility\n(.*)',draft,re.S|re.M).group(1).strip()
    entry='\n'.join([f"## {NEW} — Record preview-product-boundary-successor.v{V} as DR-117 leftover remasurement","",bullet('Date',TODAY),bullet('Status',status),bullet('Decision type',dtype),bullet('Subject',f"`{P(SUBJ)}` `{SS}`."),bullet('Decision',dsec),bullet('Readiness effect',rsec),bullet('Reversibility',vsec),bullet('Commit',f"C-{NEW.replace('-','')}.")])+'\n'
    tracked=set(subprocess.check_output(['git','ls-files'],text=True).split('\n'))
    files=[COORD,P(SUBJ),P(f'preview-product-boundary-successor.v{V}.review-prompt.md'),P(CLA),P(CXA)]
    for t in range(1,TURN+1):
        ts='' if t==1 else f'.turn{t}'
        files+=[P(f'coordinator-decisions.{NEW}{ts}.draft.md'),P(f'coordinator-decisions.{NEW}{ts}.review-prompt.md'),P(f'coordinator-decisions.{NEW}.review-adversarial.claude2{ts}.json'),P(f'coordinator-decisions.{NEW}.review-adversarial.codex{ts}.json')]
    files=[f for f in dict.fromkeys(files) if os.path.exists(f) and (f==COORD or f not in tracked or subprocess.call(['git','diff','--quiet','HEAD','--',f])!=0)]
    if '--apply' in sys.argv:
        cur=open(COORD).read(); assert f'## {NEW} ' not in cur; cur=cur if cur.endswith('\n') else cur+'\n'
        open(COORD,'w').write(cur+'\n---\n\n'+entry); print('APPENDED',NEW,'new COORD sha',sha(COORD))
    else: print(entry)
    print('\nCOMMIT FILES:'); [print(' ',f) for f in files]
    open(SCR+f'commit-files.{NEW}.txt','w').write('\n'.join(files)+'\n')
