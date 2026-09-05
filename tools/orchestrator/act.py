import re
#!/usr/bin/env python3
"""Generic COORD act tooling for leftover remasurements, driven by a JSON config.
Usage:
  act.py CONFIG draft   [TURN=n]   -> writes scratchpad/coordinator-decisions.D-NNN[.turnN].draft.md
  act.py CONFIG stageb  [TURN=n]   -> freezes the draft into artifacts (0444), writes Stage B prompt + dispatch
  act.py CONFIG entry   [TURN=n] [--apply] -> prints/appends the condensed COORD entry, prints commit file list
Config keys: newD, lineage (e.g. 'permission'), lineageTitle ('permission leftover-join'), row ('DR-105'), rowKind ('ROW'|'GATE'),
  subject (file name), subjectVersion (int), predecessorVersion (int), predecessorRecording ('D-171'), rejectedVersions ([{'v':7,'label':'Dual REJECT ...'}]),
  leftoverDesign ([...]), gate ('G09'), occupancy ({'file':..., 'version':4,'recording':'D-220','predVersion':3}), crossJoins ([{'name':'g09 leftover-join.v11','kind':'GATE','row':'DR-G09','file':..., 'recording':'D-257'}, ...]),
  namingParentGate ('G09'), doesNotLines ([...]), decisionExtra (str), extraFrozenRows ([[label,file],...]), unwrite ([...]), landsSentence (str or ''), rowToken ('OPEN'), otherTokens (str), whyExtra (str)
"""
import datetime as _dt
TODAY=_dt.date.today().isoformat()
import json,hashlib,os,re,subprocess,sys,textwrap
REPO='/Users/sb/code/opensip-ai/opensip'; os.chdir(REPO); A='docs/coop/artifacts/'; COORD='docs/coop/COORDINATOR-DECISIONS.md'; F08='docs/v2/architecture/08-decision-and-readiness-register.md'
SCR='/private/tmp/claude-501/-Users-sb-code-opensip-ai-opensip/dcbad0ae-7fad-4c78-89e7-e93d989f5501/scratchpad/'
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
def git(*a): return subprocess.check_output(['git',*a],text=True).strip()
def load(p): return json.load(open(p))
cfg=load(sys.argv[1]); mode=sys.argv[2]; TURN=int(os.environ.get('TURN','1')); T='' if TURN==1 else f'.turn{TURN}'
HEAD=git('rev-parse','HEAD'); LASTD=re.match(r'## (D-\d+)',[l for l in open(COORD) if l.startswith('## D-')][-1]).group(1)
NEW=cfg['newD']; assert int(NEW[2:])==int(LASTD[2:])+1, (NEW,LASTD)
P=lambda n: A+n
SUBJ=cfg['subject']; SV=cfg['subjectVersion']; PV=cfg['predecessorVersion']; PREC=cfg['predecessorRecording']; LT=cfg['lineageTitle']; ROW=cfg['row']
LD='`['+', '.join(cfg['leftoverDesign'])+']`'
subj=load(P(SUBJ)); JOINHEAD=subj['head']; assert subj['recordedInputs']['HEAD']==JOINHEAD
lastcommit=git('log','--format=%H','-1'); D_LAST_COMMIT=None
for line in subprocess.check_output(['git','log','--format=%H %s'],text=True).splitlines():
    if re.match(rf'^[0-9a-f]+ {LASTD}: ',line): D_LAST_COMMIT=line.split()[0]; break
assert D_LAST_COMMIT, ('no recording commit for',LASTD)
ADOPTED_AT=D_LAST_COMMIT; HYGNOTE=''
if JOINHEAD!=D_LAST_COMMIT:
    between=[l for l in subprocess.check_output(['git','log','--format=%H %s',f'{D_LAST_COMMIT}..{JOINHEAD}'],text=True).splitlines()]
    assert between and all(re.match(rf'^[0-9a-f]+ {LASTD} hygiene: ',l) for l in between), ('subject must pin the last heading commit or a following hygiene commit of it',JOINHEAD,D_LAST_COMMIT,between)
    hyg=[(l.split()[0],l.split(' ',1)[1]) for l in between]
    def _stat(h): return git('show','--stat','--format=','--shortstat',h).strip().splitlines()[-1].strip()
    _hk='d'+LASTD[2:]+'hygiene'; _hs=(f" leftover-join.v{SV} names that commit at basedOn.{_hk} (role begins `"+subj['basedOn'][_hk]['role'].split('. ')[0]+"`)." if _hk in subj.get('basedOn',{}) else '')
    HYGNOTE=' '.join(f"COORD hygiene commit `{h[:7]} {m}` follows the {LASTD} recording commit `{D_LAST_COMMIT[:7]}` ({_stat(h)}; COORDINATOR-DECISIONS.md only; no heading added; file 08 untouched). leftover-join.v{SV} pins HEAD at `{h}` (its head and recordedInputs.HEAD)." for h,m in hyg)+_hs
HEADADV='' if HEAD==JOINHEAD else ("HEAD advanced from `"+JOINHEAD+"` ("+LASTD+") to `"+HEAD+"` by `"+git('log','-1','--format=%h %s',HEAD)+"` after dispatch; it touched neither COORDINATOR-DECISIONS.md nor file 08 and no recordedInputs digest of the subject moved.")
stemA=SUBJ[:-5]; CLA=stemA+'.review-independent.claude2.json'; CXA=stemA+'.review-independent.codex.json'
def verdict(n):
    d=load(P(n)); v=d['verdict']; mf=d.get('mustFixCount'); sf=d.get('shouldFixCount')
    if not isinstance(mf,int): mf=len(d.get('mustFix') or []) if isinstance(d.get('mustFix'),list) else (d.get('mustFix') if isinstance(d.get('mustFix'),int) else 0)
    if not isinstance(sf,int): sf=len(d.get('shouldFix') or []) if isinstance(d.get('shouldFix'),list) else (d.get('shouldFix') if isinstance(d.get('shouldFix'),int) else 0)
    ids=[]
    for k in ('blockers','mustFix','shouldFix','findings'):
        x=d.get(k)
        if isinstance(x,list): ids+=[i.get('id') for i in x if isinstance(i,dict) and i.get('id')]
    return v,mf,sf,list(dict.fromkeys(ids))
def shape(n,label):
    d=load(P(n)); onf=d.get('observationsNotFindings','__absent__'); obs=d.get('observations','__absent__'); adv=d.get('advisories','__absent__'); ac=d.get('advisoryCount')
    ids=[x.get('id') for x in onf if isinstance(x,dict) and x.get('id')] if isinstance(onf,list) else []
    if onf=='__absent__': o='no observationsNotFindings field'
    elif isinstance(onf,list) and not onf: o='an empty observationsNotFindings list'
    elif isinstance(onf,list) and all(isinstance(x,str) for x in onf):
        _mk=[re.match(r'^((?:O|OBS-?|ADV-?)\d+)[.:)]\s',x) for x in onf]
        if all(_mk): o=f'{len(onf)} observationsNotFindings string'+('s' if len(onf)!=1 else '')+' without an id member, each opening with an inline marker ('+', '.join(m.group(1)+'.' for m in _mk)+'); this entry does not treat those markers as identifiers'
        else: o=f'{len(onf)} unlabeled observationsNotFindings string'+('s' if len(onf)!=1 else '')+' (no identifiers)'
    elif isinstance(onf,list) and all(isinstance(x,dict) for x in onf):
        keysets=[list(x.keys()) for x in onf]; same=all(k==keysets[0] for k in keysets)
        members=(((('each with members ' if len(onf)>1 else 'with members ')+', '.join(keysets[0]))) if same else ('members vary per object: '+'; '.join('/'.join(k) for k in keysets)))
        if len(ids)==len(onf): o=f'{len(onf)} named observationsNotFindings object'+('s' if len(onf)!=1 else '')+' '+', '.join(ids)+' ('+members+'); no change requested; they carry those identifiers'
        else: o=f'{len(onf)} unlabeled observationsNotFindings object'+('s' if len(onf)!=1 else '')+' ('+members+'; no identifiers)'
    else: o='observationsNotFindings of unexpected shape'
    obs_ids=[x.get('id') for x in obs if isinstance(x,dict) and x.get('id')] if isinstance(obs,list) else []
    if obs=='__absent__': ob='no observations field'
    elif isinstance(obs,list) and not obs: ob='an empty observations list'
    elif isinstance(obs,list) and all(isinstance(x,dict) for x in obs):
        ks=[list(x.keys()) for x in obs]; same=all(k==ks[0] for k in ks)
        mem=(((('each with members ' if len(obs)>1 else 'with members ')+', '.join(ks[0]))) if same else ('members vary per object: '+'; '.join('/'.join(k) for k in ks)))
        if len(obs_ids)==len(obs): ob=f'{len(obs)} named observations object'+('s' if len(obs)!=1 else '')+' '+', '.join(obs_ids)+' ('+mem+'); no change requested; '+('they carry those identifiers' if len(obs)!=1 else 'it carries that identifier')
        else: ob=f'{len(obs)} unlabeled observations object'+('s' if len(obs)!=1 else '')+' ('+mem+'; no identifiers)'
    elif isinstance(obs,list) and all(isinstance(x,str) for x in obs): ob=f'{len(obs)} unlabeled observations string'+('s' if len(obs)!=1 else '')+' (no identifiers)'
    else: ob=f'observations of unexpected shape'
    ids=ids+obs_ids
    ad='no advisories field' if (adv=='__absent__' and ac is None) else ('zero advisories' if ((isinstance(adv,list) and not adv) or ac==0) else f'{len(adv)} advisories')
    return (f'{label} returned {o}. It returned {ob}. It returned {ad}.' if ';' in ob else f'{label} returned {o}. It returned {ob} and {ad}.'), ids, '; '.join([o,ob,ad])
def obsfield(n):
    d=load(P(n)); return 'observationsNotFindings' if isinstance(d.get('observationsNotFindings'),list) or 'observationsNotFindings' in d else ('observations' if 'observations' in d else 'observationsNotFindings')
def idsent(cl,cx,stage):
    if cl and not cx: return f"This entry names {'that Claude identifier' if len(cl)==1 else 'those Claude identifiers'}. It does not invent a Codex identifier. It does not claim that both reviewers' identifiers are preserved. Codex {stage} returned no observation identifiers."
    if cx and not cl: return f"This entry names {'that Codex identifier' if len(cx)==1 else 'those Codex identifiers'}. It does not invent a Claude identifier. It does not claim that both reviewers' identifiers are preserved. Claude {stage} returned no observation identifiers."
    if cl and cx: return "This entry names both reviewers' identifiers."
    return f"This entry does not invent identifiers. It does not claim that both reviewers' identifiers are preserved. Claude {stage} returned no observation identifiers. Codex {stage} returned no observation identifiers."
for n in (CLA,CXA):
    v,mf,sf,_=verdict(n); assert v=='ACCEPT' and mf==0 and sf==0,(n,v,mf,sf); assert oct(os.stat(P(n)).st_mode)[-3:]=='444'
sA_cl,idA_cl,tA_cl=shape(CLA,f'Claude Stage A leftover-join.v{SV}'); sA_cx,idA_cx,tA_cx=shape(CXA,f'Codex Stage A leftover-join.v{SV}')
branch='D-170 through D-235 and '+' and '.join(f'D-{n}' for n in list(range(237,272))+list(range(273,int(LASTD[2:])+1)))
OCCS=cfg.get('occupancies') or [dict(cfg['occupancy'],gate=cfg['gate'])]
occ=OCCS[0]; G=cfg['gate']; occ_file=occ['file']; occ_pred=occ.get('predFile')
def occ_current_sent(): return ' '.join(f"{o['gate']} occupancy v{o['version']} is the current {o['gate']} occupancy remasurement ({o['recording']})." for o in OCCS)
def occ_pred_sent(): return ' '.join(f"{o['gate']} occupancy v{o['predVersion']} is not current." for o in OCCS if o.get('predVersion'))
def occ_after(): return ', '.join(f"{o['gate']} occupancy v{o['version']} ({o['recording']})" for o in OCCS)
def occ_cited(): return ', '.join(f"{o['gate']} occupancy v{o['predVersion']}" for o in OCCS if o.get('predVersion'))
MULTI=len(OCCS)>1
def occ_remasured(): return ('The current occupancy remasurements remasured those already-named identifiers.' if MULTI else f"{OCCS[0]['gate']} occupancy v{OCCS[0]['version']} ({OCCS[0]['recording']}) remasured that already-named identifier.")
def _orlist(xs): return (', '.join(xs[:-1])+', or '+xs[-1]) if len(xs)>2 else ' or '.join(xs)
def occ_norewrite(): return ('Does not rewrite '+_orlist([f"{o['gate']} occupancy v{o['version']}" for o in OCCS])+'.') if MULTI else f"Does not rewrite occupancy v{OCCS[0]['version']}."
NP=cfg.get('namingParents')  # optional: [{'gates':'G12 and G21','rows':'DR-G12 and DR-G21','naming':'naming v6 (D-145)','namedBy':'D-086'}, ...]
def naming(not_clause):
    if not NP: return f"Naming parent of {G} is naming v6 (D-145){not_clause}. D-086 named DR-{G}."
    return '; '.join(f"{'Naming' if i==0 else 'naming'} parent of {n['gates']} is {n['naming']}" for i,n in enumerate(NP))+(f"; the naming parent is {not_clause[len(', '):]}" if not_clause else '')+'. '+' '.join(f"{x['by']} named {x['rows']}." for n in NP for x in (n.get('named') or [{'by':n['namedBy'],'rows':n['rows']}]))
rej=cfg.get('rejectedVersions',[])
rej_sent=' '.join(f"leftover-join.v{r['v']} is CANDIDATE-NOT-APPLIED ({r['label']}) and is not current." for r in rej)
cross=cfg.get('crossJoins',[])
cross_sent=' '.join(f"{c['name']} remains the current {c['row']} {c['kind']} leftover-join ({c['recording']})." for c in cross)
HEADROW=cfg['gate'] if cfg.get('rowKind')=='GATE' and ',' not in cfg['gate'] and '-' not in cfg['gate'] else ROW
REFRESH=cfg.get('refreshCitations',[])
def _andlist(xs): return (', '.join(xs[:-1])+', and '+xs[-1]) if len(xs)>2 else ' and '.join(xs)
refresh_after=_andlist([f"{r['name']}.v{r['newVersion']} ({r['recording']})" for r in REFRESH])
refresh_cited=_andlist([f"{r['name']}.v{r['oldVersion']} ({r['oldRecording']}) as the current {r['row']} leftover-join" for r in REFRESH])
refresh_rows=''
refresh_nc=' '.join(f"{r['name']}.v{r['oldVersion']} is not recorded as current {r['row']} leftover-join." for r in REFRESH)
refresh_tail=(' '+refresh_nc) if REFRESH else ''
refresh_prompt=('\n'+'\n'.join(f"Do not record {r['name']}.v{r['oldVersion']} as current {r['row']} leftover-join." for r in REFRESH)) if REFRESH else ''
occ_unchanged_sent=' '.join(f"{o['gate']} occupancy v{o['version']} remains the current {o['gate']} occupancy remasurement ({o['recording']}); this successor does not remasure it." for o in OCCS) if cfg.get('occupancyUnchanged') else ''
why_core=(f"leftover remasurement after {refresh_after}. leftover-join.v{PV} cited {refresh_cited}. {occ_unchanged_sent} leftoverDesign remains {LD}." if (REFRESH and cfg.get('occupancyUnchanged')) else f"leftover remasurement after {occ_after()}. leftover-join.v{PV}\ncited {occ_cited()} as the specification. {occ_remasured()} leftoverDesign remains {LD}.")
cross_names=(', '.join(c['name'] for c in cross)+', ') if cross else ''
_ln=[LT]+[c['name'].rsplit('.v',1)[0] for c in cross]; lineages=(', '.join(_ln[:-1])+(', and ' if len(_ln)>2 else ' and ')+_ln[-1]) if len(_ln)>1 else _ln[0]
lineages_sent=(f"{lineages} are different lineages; their version numbers are unrelated." if len(_ln)>1 else f"{LT} is one lineage; its version numbers are unrelated to occupancy versions.")
# ---------- prior-turn facts (turns 1..TURN-1) ----------
T1=''; LANDS_SENT=''; PREV=''; T1OBS=''; UNWRITE_TURNS=''; PRIOR=[]
if TURN>1:
    for t in range(1,TURN):
        sfx='' if t==1 else f'.turn{t}'
        TD=P(f'coordinator-decisions.{NEW}{sfx}.draft.md'); TC=P(f'coordinator-decisions.{NEW}.review-adversarial.claude2{sfx}.json'); TX=P(f'coordinator-decisions.{NEW}.review-adversarial.codex{sfx}.json')
        for f in (TD,TC,TX): assert oct(os.stat(f).st_mode)[-3:]=='444', f
        clv=verdict(os.path.basename(TC)); cxv=verdict(os.path.basename(TX))
        bcl,bclids,bcls=shape(os.path.basename(TC),f'Claude Stage B turn {t}'); bcx,bcxids,bcxs=shape(os.path.basename(TX),f'Codex Stage B turn {t}')
        PRIOR.append(dict(t=t,TD=TD,TC=TC,TX=TX,clv=clv,cxv=cxv,bcl=bcl,bclids=bclids,bcls=bcls,bcx=bcx,bcxids=bcxids,bcxs=bcxs))
    last=PRIOR[-1]; LANDED=last['cxv'][3]+last['clv'][3]
    same=cfg.get('sameClass',[])
    LANDS_SENT='Lands '+', '.join(LANDED)+'.'+(' '+' '.join(f'{a} and {b} are the same class ({w}).' for a,b,w in same) if same else '')+(' All identifiers are named.' if len(LANDED)>1 else (' The identifier is named.' if LANDED else ''))
    earlier=[(pr['t'],pr['cxv'][3]+pr['clv'][3]) for pr in PRIOR[:-1] if pr['cxv'][3]+pr['clv'][3]]
    if earlier: LANDS_SENT+=' '+' '.join(f"{', '.join(ids)} (turn {t}) landed in the turn-{t+1} subject and {'are' if len(ids)>1 else 'is'} carried, not re-landed." for t,ids in earlier)
    T1OBS=' '+' '.join(pr['bcl']+' '+pr['bcx']+' '+idsent(pr['bclids'],pr['bcxids'],f"Stage B turn {pr['t']}") for pr in PRIOR)
    def vstr(v): return f"{v[0]} {v[1]}/{v[2]}"+((' '+', '.join(v[3])) if v[3] else '')
    T1=''
    for pr in PRIOR:
        t=pr['t']
        T1+=f"""Turn {t}: Claude {vstr(pr['clv'])}. Codex {vstr(pr['cxv'])}. Not Dual CONSENT.{' Every turn-'+str(t)+' finding is landed in the turn-'+str(t+1)+' subject.' if t<TURN-1 else ' Every turn-'+str(t)+' finding is landed in this turn-'+str(TURN)+' subject.'}

Stage B turn {t}:

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `{pr['TC']}` | `{sha(pr['TC'])}` | {vstr(pr['clv'])} |
| Codex | `{pr['TX']}` | `{sha(pr['TX'])}` | {vstr(pr['cxv'])} |

Stage B turn {t} observation disposition (no change requested; no identifiers invented):

| Source | Identifier | Standing |
|---|---|---|
| Claude Stage B turn {t} observationsNotFindings | {', '.join(pr['bclids']) if pr['bclids'] else 'none'} | {pr['bcls']} |
| Codex Stage B turn {t} observationsNotFindings | {', '.join(pr['bcxids']) if pr['bcxids'] else 'none'} | {pr['bcxs']} |

Frozen turn {t} draft
`{pr['TD']}`
`{sha(pr['TD'])}`
stays unmoved.

"""
    PREV=' '+' '.join(f"turn-{pr['t']} Claude {pr['clv'][0]}"+(' ('+' / '.join(pr['clv'][3])+')' if pr['clv'][3] else '')+f" `{sha(pr['TC'])}`; turn-{pr['t']} Codex {pr['cxv'][0]}"+(' ('+' / '.join(pr['cxv'][3])+')' if pr['cxv'][3] else '')+f" `{sha(pr['TX'])}`." for pr in PRIOR)
    objs=[]
    for pr in PRIOR:
        who=[w for w,v in (('Claude',pr['clv']),('Codex',pr['cxv'])) if v[0]=='OBJECT']
        if len(who)==2: objs.append(f"the turn-{pr['t']} OBJECTs")
        elif len(who)==1: objs.append(f"the turn-{pr['t']} {who[0]} OBJECT")
    UNWRITE_TURNS=(' Does not unwrite '+(', '.join(objs[:-1])+' or '+objs[-1] if len(objs)>1 else objs[0])+'.') if objs else ''
# ---------- measured inputs ----------
rows=[(SUBJ,sha(P(SUBJ))),(CLA,sha(P(CLA))),(CXA,sha(P(CXA)))]
for r in rej:
    rf=f"{cfg['lineage']}-leftover-join.v{r['v']}.json"; rows.append((f"Frozen leftover-join.v{r['v']} ({r['label']}; CANDIDATE-NOT-APPLIED; unrecorded; not current; not this subject)",sha(P(rf))))
    for who,suf in (('Claude','claude2'),('Codex','codex')):
        rv=P(f"{cfg['lineage']}-leftover-join.v{r['v']}.review-independent.{suf}.json")
        if os.path.exists(rv): rows.append((f"Frozen leftover-join.v{r['v']} Stage A {who} {verdict(os.path.basename(rv))[0]} {verdict(os.path.basename(rv))[1]}/{verdict(os.path.basename(rv))[2]}",sha(rv)))
pf=f"{cfg['lineage']}-leftover-join.v{PV}.json"; rows.append((f"Frozen leftover-join.v{PV} ({PREC}; current {ROW} leftover-join at draft time; not this subject)",sha(P(pf))))
for who,suf in (('Claude','claude2'),('Codex','codex')):
    rv=P(f"{cfg['lineage']}-leftover-join.v{PV}.review-independent.{suf}.json")
    if os.path.exists(rv): rows.append((f"Frozen leftover-join.v{PV} Stage A {who} {verdict(os.path.basename(rv))[0]} {verdict(os.path.basename(rv))[1]}/{verdict(os.path.basename(rv))[2]}",sha(rv)))
for o in OCCS:
    rows.append((f"Frozen {o['gate']} occupancy v{o['version']} ({o['recording']}; current {o['gate']} occupancy; not this subject)",sha(P(o['file']))))
    if o.get('predFile'): rows.append((f"Frozen {o['gate']} occupancy v{o['predVersion']} (predecessor occupancy; not current; not this subject)",sha(P(o['predFile']))))
for c in cross: rows.append((f"Frozen {c['name']} ({c['recording']}; current {c['row']} {c['kind']} leftover-join; not this subject)",sha(P(c['file']))))
for lab,f in cfg.get('extraFrozenRows',[]): rows.append((lab,sha(P(f))))
for pr in PRIOR: rows+= [(f"Frozen turn {pr['t']} {NEW} draft (not this subject)",sha(pr['TD'])),(f"Frozen {NEW} turn {pr['t']} Claude review (not this subject)",sha(pr['TC'])),(f"Frozen {NEW} turn {pr['t']} Codex review (not this subject)",sha(pr['TX']))]
rows+=[('COORDINATOR-DECISIONS.md',sha(COORD)),('file 08',sha(F08)),('HEAD (live at draft time)',HEAD)]
if HEAD!=JOINHEAD: rows.append((f'leftover-join.v{SV} HEAD pin (Stage A measurement HEAD; {LASTD} commit)',JOINHEAD))
uw=sorted(set(cfg['unwrite']), key=lambda d:int(d[2:])); unwrite=(', '.join(uw[:-1])+', or '+uw[-1]) if len(uw)>2 else ' or '.join(uw)
doesnot='\n'.join('> **Does not** '+x for x in cfg['doesNotLines'])
obs_sent=f"{sA_cl} {sA_cx} {idsent(idA_cl,idA_cx,'Stage A')}"
lands_join=cfg.get('landsSentence','')
draft=f"""# {NEW} — Record {LT}.v{SV} as {HEADROW} leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** {TODAY}
> **Protocol:** D-000 new cycle, turn {TURN} of 3.{(' '+LANDS_SENT) if TURN>1 else ''}
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `{SUBJ}`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> {branch}. D-272 is CONTESTED and is not on this
> no-cell-edit adoption branch. Not a three-limb act. Not a
> required-now successor. Not SATISFIED-GRADE. This is
> coordinator decision **{NEW}**, not a register row.
> **Does not** mark any row SATISFIED.
{doesnot}
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

{LASTD} is ADOPTED at
`{ADOPTED_AT}`.
HEAD is `{HEAD}`.
Last live heading is {LASTD}. Required-now is 28.
{HEADADV}{HYGNOTE}

Stage A dual independent ACCEPT 0/0 of the frozen
leftover-join (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `{P(CLA)}` | `{sha(P(CLA))}` | ACCEPT 0/0 |
| Codex | `{P(CXA)}` | `{sha(P(CXA))}` | ACCEPT 0/0 |

Stage A observation disposition (no change requested; no identifiers invented):

| Source | Identifier | Standing |
|---|---|---|
| Claude leftover-join.v{SV} {obsfield(CLA)} | {', '.join(idA_cl) if idA_cl else 'none'} | {tA_cl} |
| Codex leftover-join.v{SV} {obsfield(CXA)} | {', '.join(idA_cx) if idA_cx else 'none'} | {tA_cx} |

{T1}Measured inputs:

| Path | sha256 |
|---|---|
""" + '\n'.join(f'| {a} | `{b}` |' for a,b in rows) + f"""

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, leftover-join.v{PV},
leftover-join.v{SV}, {occ_after()}, {cross_names}both Stage A verdicts,{((' the frozen turn 1 draft and its Stage B verdicts,') if len(PRIOR)==1 else (' the frozen turn '+' and turn '.join(str(pr['t']) for pr in PRIOR)+' drafts and their Stage B verdicts,')) if TURN>1 else ''} and this
draft unmoved, remasure before adoption. Append-only COORD after
this remasurement, with those files unmoved, is
**PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; {ROW} remains
`{cfg['rowToken']}`; {cfg['otherTokens']} DR-107 remains
`PROPOSED-CLOSED-FOR-REVIEW`; DR-118 remains
`DECIDED-V1-NOT-INTEGRATED`. {naming(f', not leftover-join.v{PV} or leftover-join.v{SV}')}
leftover-join.v{SV} is the {ROW} leftover-join under review.
leftover-join.v{PV} remains the current recorded {ROW} leftover-join
at draft time ({PREC}). {rej_sent} After this successor is recorded,
leftover-join.v{PV} is not current. {occ_current_sent()} {occ_pred_sent()} {cross_sent}{refresh_tail}
leftoverDesign remains {LD}.
{lineages_sent} {cfg.get('tokenNote','')}

This is a leftover remasurement COORD draft. It does not
claim that D-056 gates 2 and 3 do not hold.

## Why this entry exists

{(LANDS_SENT+' ') if TURN>1 else ''}Dual independent ACCEPT 0/0 now exists of leftover-join.v{SV}
{why_core}
This entry records leftover-join.v{SV} ({ROW}). It is not
SATISFIED-GRADE. Frozen leftover-join.v{PV} stays unmoved.
leftover-join.v{PV} remains current at draft time.{((' Frozen turn 1 draft stays unmoved.') if len(PRIOR)==1 else (' Frozen turn '+' and turn '.join(str(pr['t']) for pr in PRIOR)+' drafts stay unmoved.')) if TURN>1 else ''} {cfg.get('whyExtra','')}

## Decision

1. Record
   `{SUBJ}`
   as {HEADROW} leftover remasurement after {LASTD}. The candidate
   binds NOTHING. Both independent Stage A reviewers of
   leftover-join.v{SV} returned 0 blockers and 0 SHOULD-FIX.{(' '+LANDS_SENT) if TURN>1 else ''}
   leftover-join.v{PV} remains current at draft time. After this
   successor is recorded, leftover-join.v{PV} is not current. {rej_sent}
   {occ_current_sent()} {occ_pred_sent().replace('is not current','is not recorded as current occupancy')} {cross_sent}{refresh_tail}
2. {ROW} stays `{cfg['rowToken']}`. leftover-design of
   {', '.join(cfg['leftoverDesign'])} remains on leftover-join.v{SV}. {cfg['decisionExtra']}
   Gate 1 Class A is not opened. Not SATISFIED. Required-now stays 28. Condition-4
   effect is zero. {naming(f', not leftover-join.v{SV}')} {obs_sent} {lands_join} basedOn.d{LASTD[2:]}.role is last-heading custody only.{T1OBS} Does not execute {G}. {occ_norewrite()} Does not edit
   file 08. Does not authorize `docs/v2/implementation/`.

## Readiness effect

Zero SATISFIED. Condition 2 stays 5 of 32. Condition 4 stays
MET on the naming half (28 of 28). Condition 5 last.

## Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn: C-{NEW.replace('-','')}.
Does not unwrite {unwrite}.{UNWRITE_TURNS}
"""
assert not re.search(r'\{[A-Z_]+\}',draft)
DRAFT_SCR=SCR+f'coordinator-decisions.{NEW}{T}.draft.md'
if mode=='draft':
    draft=re.sub(r'(?<=\S)  +(?=\S)',' ',draft); draft=re.sub(r' +\n','\n',draft)
    open(DRAFT_SCR,'w').write(draft); print('wrote',DRAFT_SCR,len(draft)); sys.exit(0)
if mode=='stageb':
    DST=P(f'coordinator-decisions.{NEW}{T}.draft.md')
    if not os.path.exists(DST): open(DST,'w').write(open(DRAFT_SCR).read()); os.chmod(DST,0o444)
    assert oct(os.stat(DST).st_mode)[-3:]=='444'; DSHA=sha(DST)
    TURNNOTE=''
    if TURN>1: TURNNOTE=' '.join(f"Turn-{pr['t']} subject remains frozen at `{pr['TD']}` `{sha(pr['TD'])}`." for pr in PRIOR)+f" Prior verdicts:{PREV} Every prior-turn finding is landed (turn-{TURN-1} findings in this turn-{TURN} subject; earlier findings in the following turn's subject); do not re-land them. You MAY read all frozen prior-turn reviews.\n"
    idl=''
    if idA_cl: idl+='Do not omit '+', '.join(idA_cl)+f'. Do not recast Claude Stage A leftover-join.v{SV} observationsNotFindings objects as strings.\n'
    if idA_cx: idl+='Do not omit '+', '.join(idA_cx)+'.\n'
    prompt=f"""# Adversarial review — {NEW}{(' turn '+str(TURN)) if TURN>1 else ''}

Independent, refute not confirm.

**SUBJECT:** `{DST}`
Expected sha256:
`{DSHA}`
Mode 0444. If the subject moves, OBJECT.

**WRITE ONLY:**
- Claude 2: `{P('coordinator-decisions.'+NEW+'.review-adversarial.claude2'+T+'.json')}`
- Codex: `{P('coordinator-decisions.'+NEW+'.review-adversarial.codex'+T+'.json')}`
{TURNNOTE}
Do not edit the subject. Do not commit. Do not edit file 08 or COORD.
Do not mark any row SATISFIED. {cfg['stageBDoNot']}
Do not flatten DR-118 `DECIDED-V1-NOT-INTEGRATED` to `OPEN`.
Do not flatten DR-107 `PROPOSED-CLOSED-FOR-REVIEW` to `OPEN`.
Do not invent identifiers.
Do not claim both reviewers' identifiers are preserved unless both returned identifiers.
{idl}Do not record leftover-join.v{PV} as not current at draft time.
{cfg.get('stageBExtra','')}{refresh_prompt}
Do not reopen DR-119 SATISFIED.
Do not read the other reviewer's current-turn review.

HEAD is `{HEAD}`. {LASTD} is ADOPTED at `{ADOPTED_AT}`. Last heading is {LASTD}. {HYGNOTE}
Required-now is 28.

leftover-join.v{PV} remains the current recorded {ROW} leftover-join at draft time ({PREC}).
After this successor is recorded, leftover-join.v{PV} is not current.
{rej_sent}
{occ_current_sent()}
{cross_sent}{refresh_tail}
leftoverDesign remains {LD}.
{naming('')}
file08StatusToken is `{cfg['rowToken']}`.
{lineages_sent}
{lands_join}

Claude Stage A leftover-join.v{SV} returned {tA_cl}.
Codex Stage A leftover-join.v{SV} returned {tA_cx}.

This is a leftover remasurement COORD draft. Do not claim that D-056
gates 2 and 3 do not hold.

The no-cell-edit branch is D-170 through D-235 and D-237 through
D-271 and D-273 through {LASTD}. D-272 is CONTESTED and is not on that
adoption branch. The branch must not span D-236.

CONSENT only if no MUST-FIX or SHOULD-FIX.
Final chat: CONSENT or OBJECT.
"""
    pp=P(f'coordinator-decisions.{NEW}{T}.review-prompt.md'); assert not os.path.exists(pp); open(pp,'w').write(prompt); os.chmod(pp,0o444)
    dispatch=f"""Adversarial review of {NEW} COORD draft. Turn {TURN} of 3.

Read {pp}
and execute it. Refute, do not confirm.

SUBJECT sha256 must be
{DSHA}
Mode 0444. If the subject moved, OBJECT.

Write only your review JSON path from that prompt.
Do not edit the subject. Do not commit. Do not edit file 08 or COORD.

leftover-join.v{PV} remains the current recorded {ROW} leftover-join at draft time ({PREC}).
{rej_sent}
{occ_current_sent()}
{cross_sent}{refresh_tail}
leftoverDesign remains {LD}.
file08StatusToken {cfg['rowToken']}.

Claude Stage A leftover-join.v{SV} returned {tA_cl}.
Codex Stage A leftover-join.v{SV} returned {tA_cx}.
Do not invent identifiers. Do not claim both reviewers' identifiers are preserved unless both returned identifiers.

CONSENT only if no MUST-FIX or SHOULD-FIX.
Final chat: CONSENT or OBJECT.
"""
    dp=P(f'_dispatch.{NEW}'+('' if TURN==1 else f'-t{TURN}')+'.txt'); open(dp,'w').write(dispatch)
    print('draft',DST,DSHA); print('prompt',pp,sha(pp)); print('dispatch',dp,len(dispatch)); sys.exit(0)
if mode=='entry':
    CLB=f'coordinator-decisions.{NEW}.review-adversarial.claude2{T}.json'; CXB=f'coordinator-decisions.{NEW}.review-adversarial.codex{T}.json'
    for n in (CLB,CXB):
        v,mf,sf,_=verdict(n); assert v=='CONSENT' and mf==0 and sf==0,(n,v,mf,sf); assert oct(os.stat(P(n)).st_mode)[-3:]=='444'
    DRAFT=P(f'coordinator-decisions.{NEW}{T}.draft.md'); assert oct(os.stat(DRAFT).st_mode)[-3:]=='444'
    sB_cl,idB_cl,_=shape(CLB,'Claude Stage B'); sB_cx,idB_cx,_=shape(CXB,'Codex Stage B')
    def bullet(label,body): return textwrap.fill(f'**{label}:** '+body,width=66,initial_indent='- ',subsequent_indent='  ',break_long_words=False,break_on_hyphens=False)
    status=(f"**ADOPTED {TODAY}.** Turn {TURN} of 3: CONSENT from both independent reviewers, 0 MUST-FIX, 0 SHOULD-FIX. Claude 2 (`artifacts/{CLB}`, `{sha(P(CLB))}`) CONSENT. Codex (`artifacts/{CXB}`, `{sha(P(CXB))}`) CONSENT. Subject `coordinator-decisions.{NEW}{T}.draft.md` `{sha(DRAFT)}`.{PREV} Frozen leftover-join `{SUBJ}` `{sha(P(SUBJ))}` Stage A Claude ACCEPT `{sha(P(CLA))}` 0/0; Stage A Codex ACCEPT `{sha(P(CXA))}` 0/0.")
    dtype=(f"RULE-GOVERNED. Records independent dual ACCEPT of `{SUBJ}` (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as {branch}. D-272 is CONTESTED and is not on this no-cell-edit adoption branch. Not a three-limb act. Not SATISFIED-GRADE.")
    decision=(f"Record leftover-join.v{SV} as {HEADROW} leftover remasurement after {LASTD}.{(' '+LANDS_SENT) if TURN>1 else ''} The candidate binds NOTHING. {ROW} stays `{cfg['rowToken']}`. leftover-design of {', '.join(cfg['leftoverDesign'])} remains on leftover-join.v{SV}. leftover-join.v{PV} remains current at draft time. After this successor is recorded, leftover-join.v{PV} is not current. {rej_sent} {occ_current_sent()} {occ_pred_sent().replace('is not current','is not recorded as current occupancy')} {cross_sent}{refresh_tail} {cfg['decisionExtra']} Gate 1 Class A is not opened. Not SATISFIED. Required-now stays 28. Condition-4 effect is zero. {naming(f', not leftover-join.v{SV}')} {obs_sent} {lands_join} basedOn.d{LASTD[2:]}.role is last-heading custody only. {sB_cl} {sB_cx} {idsent(idB_cl,idB_cx,'Stage B')}{T1OBS} Does not execute {G}. {occ_norewrite()} Does not edit file 08. Does not authorize `docs/v2/implementation/`.")
    entry='\n'.join([f"## {NEW} — Record {LT}.v{SV} as {HEADROW} leftover remasurement","",bullet('Date',TODAY),bullet('Status',status),bullet('Decision type',dtype),bullet('Subject',f"`{P(SUBJ)}` `{sha(P(SUBJ))}`."),bullet('Decision',decision),bullet('Readiness effect','Zero SATISFIED. Condition 2 stays 5 of 32. Condition 4 stays MET on the naming half (28 of 28). Condition 5 last.'),bullet('Reversibility',f"Total only before a later dependent leftover rewrite, SATISFIED cycle, or file-08 cell rewrite. Overturn: C-{NEW.replace('-','')}. Does not unwrite {unwrite}."+UNWRITE_TURNS),bullet('Commit',f"C-{NEW.replace('-','')}."),''])
    tracked=set(subprocess.check_output(['git','ls-files'],text=True).split('\n'))
    files=[COORD]+[P(n) for n in [f'coordinator-decisions.{NEW}.draft.md',f'coordinator-decisions.{NEW}.review-adversarial.claude2.json',f'coordinator-decisions.{NEW}.review-adversarial.codex.json',f'coordinator-decisions.{NEW}.review-prompt.md']+[n for t in range(2,TURN+1) for n in (f'coordinator-decisions.{NEW}.turn{t}.draft.md',f'coordinator-decisions.{NEW}.review-adversarial.claude2.turn{t}.json',f'coordinator-decisions.{NEW}.review-adversarial.codex.turn{t}.json',f'coordinator-decisions.{NEW}.turn{t}.review-prompt.md')]+[SUBJ,CLA,CXA,stemA+'.review-prompt.md']]
    for r in rej:
        for suf in ('.json','.review-independent.claude2.json','.review-independent.codex.json','.review-prompt.md'):
            f=P(f"{cfg['lineage']}-leftover-join.v{r['v']}"+suf)
            if os.path.exists(f): files.append(f)
    files=[f for f in dict.fromkeys(files) if os.path.exists(f) and (f==COORD or f not in tracked or subprocess.call(['git','diff','--quiet','HEAD','--',f])!=0)]
    if '--apply' in sys.argv:
        cur=open(COORD).read(); assert cur.endswith('- **Commit:** C-'+LASTD.replace('-','')+'.\n'); assert f'## {NEW} ' not in cur
        open(COORD,'w').write(cur+'\n'+entry); print('APPENDED',NEW,'new COORD sha',sha(COORD))
    else: print(entry)
    print('\nCOMMIT FILES:'); [print(' ',f) for f in files]
    open(SCR+f'commit-files.{NEW}.txt','w').write('\n'.join(files)+'\n')
