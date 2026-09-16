#!/usr/bin/env python3
"""D-288 convention draft: cross-lineage leftover-join citations are custody at recording. Every measured row is computed from bytes."""
import json,re,os,sys,hashlib,subprocess,datetime,collections
REPO='/Users/sb/code/opensip-ai/opensip'; os.chdir(REPO); A='docs/coop/artifacts/'; P=lambda n:A+n
COORD='docs/coop/COORDINATOR-DECISIONS.md'; F08='docs/v2/architecture/08-decision-and-readiness-register.md'
SCR='/private/tmp/claude-501/-Users-sb-code-opensip-ai-opensip/dcbad0ae-7fad-4c78-89e7-e93d989f5501/scratchpad/'
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
def git(*a): return subprocess.check_output(['git',*a],text=True).strip()
HEAD=git('rev-parse','HEAD'); OVR=os.environ.get('NEW_OVERRIDE')
if not OVR: assert hashlib.sha256(subprocess.check_output(['git','show',f'HEAD:{COORD}'])).hexdigest()==sha(COORD)
c=subprocess.check_output(['git','show',f'HEAD:{COORD}'],text=True) if OVR else open(COORD).read(); heads=[l for l in c.splitlines() if l.startswith('## D-')]; LASTD=re.match(r'## (D-\d+)',heads[-1]).group(1)
NEW=OVR or f'D-{int(LASTD[2:])+1}'; assert int(LASTD[2:])>=292
TURN=int(os.environ.get('TURN','1')); TS='' if TURN==1 else f'.turn{TURN}'
LANDS={1:'',2:' Lands CLAUDE-D294-SF1, CLAUDE-D294-SF2, CLAUDE-D294-SF3, CODEX-D294-MF1, CODEX-D294-MF2, CODEX-D294-SF1, and CODEX-D294-SF2. All identifiers are named.',
 3:(' Turn 2 landed CLAUDE-D294-SF1 (grammar widened, measurement rule), CLAUDE-D294-SF2 (Decision 1, whichever kind), CLAUDE-D294-SF3 (Decision 2(a) and 3 ranges), CODEX-D294-MF1 (Decision 2(b), one trigger), CODEX-D294-MF2 (D-272 excluded from Decision 3), CODEX-D294-SF1 (D-286 mixed trigger, rationale), and CODEX-D294-SF2 (currentness sentence, measured inputs).'
    ' This turn lands CLAUDE-D294-T2-SF1 and CODEX-D294-T2-SF1 (the site count and the Sites column recomputed under the widened grammar, measured inputs), CLAUDE-D294-T2-SF2 (this Protocol line names every identifier), and CODEX-D294-T2-SF2 (D-287 has no cross-lineage citation to refresh, rationale). All identifiers are named; none was rejected.')}[TURN]
TODAY=datetime.date.today().isoformat()
def commit_of(d):
    for line in subprocess.check_output(['git','log','--format=%H %s'],text=True).splitlines():
        if re.match(rf'^[0-9a-f]+ {d}: ',line): return line.split()[0]
    raise SystemExit('no commit for '+d)
ADOPTED_AT=commit_of(LASTD); assert ADOPTED_AT==HEAD or (subprocess.call(['git','merge-base','--is-ancestor',ADOPTED_AT,HEAD])==0 and subprocess.check_output(['git','show',f'{ADOPTED_AT}:{COORD}'])==subprocess.check_output(['git','show',f'HEAD:{COORD}'])), 'HEAD is not the LASTD commit nor a COORD-identical descendant (hygiene) of it'
# recording D of every recorded leftover-join version (non-CONTESTED headings)
rec={}
for h in heads:
    if 'CONTESTED' in h: continue
    m=re.match(r'## (D-\d+) — Record ([a-z0-9\-]+?)[- ]leftover-join\.v(\d+) ',h)
    if m: rec[(m.group(2),int(m.group(3)))]=m.group(1)
cur={}
for (st,v),d in rec.items():
    if st not in cur or v>cur[st][0]: cur[st]=(v,d)
def ld(stem,v):
    j=json.load(open(P(f'{stem}-leftover-join.v{v}.json'))); s=j.get('summary',{})
    if isinstance(s,dict) and 'leftoverDesign' in s: return list(s['leftoverDesign'])
    return [o['id'] for o in j.get('obligations',[]) if isinstance(o,dict) and o.get('leftoverDesign') is True]
def walk(o,p=''):
    if isinstance(o,dict):
        for k,v in o.items(): yield from walk(v,p+'.'+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): yield from walk(v,p+f'[{i}]')
    elif isinstance(o,str): yield p,o
pat=re.compile(r'([a-z0-9\-]+?)[- ]leftover-join[ .]v(\d+)')
PRESENT=re.compile(r'\b(remains?|is|are) (the )?current\b|\bstill measures?\b|\b[Cc]urrent\b.{0,80}?\b(is|are|remains?)\b|\b[Cc]ites?\b.{0,120}?\bas the current\b'); HIST=re.compile(r'\b[Cc]ited\b|was current|Does not record|must not|not current after|not recorded as current|historically')
rows=[]  # (stem,v,row,kind,path,sha,field,sentence,cstem,cv,crec,curv,curd)
for stem,(v,d) in sorted(cur.items()):
    f=P(f'{stem}-leftover-join.v{v}.json'); j=json.load(open(f)); row=str(j.get('registerRow')); kind='GATE' if row.startswith('DR-G') else 'ROW'
    for p,s in walk(j):
        if p.endswith('.path') or p.startswith('.recordedInputs'): continue
        for sent in re.split(r'(?<=[.!?])\s+', s.replace('\n',' ')):
            if not PRESENT.search(sent) or HIST.search(sent): continue
            for m in pat.finditer(sent):
                cst,cv=m.group(1),int(m.group(2))
                if cst==stem or cst not in cur or cv>=cur[cst][0]: continue
                if re.search(rf'{re.escape(cst)}[- ]leftover-join[ .]v{cur[cst][0]}\b', sent): continue  # the sentence itself names the current successor; the older mention is history
                rows.append((stem,v,row,kind,f,sha(f),p.lstrip('.'),sent.strip(),cst,cv,rec.get((cst,cv),'unrecorded'),cur[cst][0],cur[cst][1]))
pairs=collections.OrderedDict()
for r in rows: pairs.setdefault((r[0],r[1],r[8],r[9]),[]).append(r)
def flags(stem,v):
    j=json.load(open(P(f'{stem}-leftover-join.v{v}.json'))); return {o['id']:o.get('leftoverDesign') for o in j.get('obligations',[]) if isinstance(o,dict) and 'id' in o}
proj={}
for k,rs in pairs.items():
    assert ld(k[2],k[3])==ld(k[2],cur[k[2]][0]), k
    assert rec.get((k[2],k[3])) and all(r[10]==rec[(k[2],k[3])] for r in rs), k
    named=sorted(set(i for r in rs for i in re.findall(r'\bOBL-[A-Z0-9\-]+',r[7])))
    fo,fn=flags(k[2],k[3]),flags(k[2],cur[k[2]][0])
    same=all(((i in fo)==(i in fn)) and (fo.get(i)==fn.get(i)) for i in named)
    jo=json.load(open(P(f'{k[2]}-leftover-join.v{k[3]}.json'))); jn=json.load(open(P(f'{k[2]}-leftover-join.v{cur[k[2]][0]}.json')))
    for fld in ('registerRow','file08StatusToken','liveGateOwners'):
        if fld in jo: same=same and (jo.get(fld)==jn.get(fld))
    def obl(j,i):
        m=[o for o in j.get('obligations',[]) if isinstance(o,dict) and o.get('id')==i]; return m[0] if m else None
    for i in named:
        a,b=obl(jo,i),obl(jn,i)
        if (a is None)!=(b is None): same=False
        elif a is not None:
            for fld in ('leftoverDesign','existingGate','rideStanding','executionObligationOwnerToday'): same=same and (a.get(fld)==b.get(fld))
    for r in rs:
        m=re.search(r'still measures? (.*?) leftoverDesign (true|false)', r[7])
        if m:
            want=(m.group(2)=='true')
            for i in re.findall(r'\bOBL-[A-Z0-9\-]+', m.group(1)): same=same and (fn.get(i)==want)
    proj[k]=([i+(' (present in both, same value)' if i in fo else ' (absent in both)') for i in named],same)
    assert same, ('content projection differs',k,named)
N_PAIRS=len(pairs); N_JOINS=len(set((r[0],r[1]) for r in rows)); N_SITES=len(rows)
citing=sorted(set((r[0],r[1],r[2],r[3],r[4],r[5]) for r in rows), key=lambda x:x[0])
sup=[('component-manifest',6,'D-174',9,'D-282'),('permission',9,'D-171',12,'D-283'),('state-class',3,'D-183',4,'D-284'),('doctor-actor',11,'D-170',12,'D-285'),('exact-bytes',5,'D-172',7,'D-286'),('distribution-core',7,'D-173',9,'D-287'),('g09',11,'D-257',12,'D-288'),('g12',4,'D-258',5,'D-289'),('g15',5,'D-270',6,'D-290'),('g19',4,'D-256',5,'D-291'),('g21',12,'D-248',13,'D-292')]
for st,ov,od,nv,nd in sup: assert rec[(st,ov)]==od and cur[st]==(nv,nd),(st,rec.get((st,ov)),cur[st])
ROWNAME={'component-manifest':'DR-103','permission':'DR-105','state-class':'DR-124','doctor-actor':'DR-114','exact-bytes':'DR-G07','distribution-core':'DR-101','g18':'DR-G18','g16':'DR-G16','g08':'DR-G08','g09':'DR-G09','g12':'DR-G12','g15':'DR-G15','g19':'DR-G19','g21':'DR-G21'}
def name(stem): return f'{stem} leftover-join'
branch='D-170 through D-235 and '+' and '.join(f'D-{n}' for n in list(range(237,272))+list(range(273,int(LASTD[2:])+1)))
# ---------- draft ----------
tbl_c='\n'.join(f"| `{f}` | `{s}` | {row} ({kind}) |" for st,v,row,kind,f,s in citing)
tbl_p='\n'.join(f"| {name(k[0])}.v{k[1]} | {name(k[2])}.v{k[3]} ({rec[(k[2],k[3])]}) | {name(k[2])}.v{cur[k[2]][0]} ({cur[k[2]][1]}) | {len(rs)} | `{rs[0][6]}`: \"{rs[0][7]}\" | `[{', '.join(ld(k[2],k[3]))}]` (identical in both) | {', '.join(proj[k][0]) if proj[k][0] else 'none named — partition equality only'} |" for k,rs in pairs.items())
tbl_s='\n'.join(f"| {name(st)}.v{ov} ({od}) | {name(st)}.v{nv} ({nd}) | {ROWNAME[st]} | `[{', '.join(ld(st,nv))}]` (identical to v{ov}) |" for st,ov,od,nv,nd in sup)
kept='lifecycle leftover-join.v4 (D-275), monorepo leftover-join.v4 (D-277), and signed-index leftover-join.v4 (D-280)'
N_ROWCITES=sum(1 for k in pairs if k[0] in ('component-manifest','doctor-actor','permission','state-class','lifecycle','monorepo','signed-index','packaging'))
n_joins=len(citing); n_pairs=len(pairs); n_sites=len(rows); NUM={1:'One',2:'Two',3:'Three',4:'Four',5:'Five',6:'Six',7:'Seven',8:'Eight',9:'Nine',10:'Ten',11:'Eleven',12:'Twelve'}
draft=f"""# {NEW} — Cross-lineage leftover-join citations are custody at recording, not standing currency claims

> **Status:** DRAFT — under review.
> **Date:** {TODAY}
> **Protocol:** D-000 new cycle, turn {TURN} of 3.{LANDS}
> **Decision type:** RULE-GOVERNED. Records the reading convention for
> cross-lineage leftover-join citations that D-276, D-278, and D-281
> applied, chosen over the version-number reading that D-269 practised.
> Same no-cell-edit branch as
> {branch}. D-272 is CONTESTED and is not on this
> no-cell-edit adoption branch. Not a remasurement. Not a three-limb
> act. Not a required-now successor. Not SATISFIED-GRADE. Not a
> D-000 amendment. This is coordinator decision **{NEW}**, not a
> register row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-101, DR-103, DR-105, DR-107, DR-112, DR-114,
> DR-117, DR-118, DR-120, DR-121, DR-124, DR-131, or DR-133.
> **Does not** reopen DR-102, DR-104, DR-115, DR-119, or DR-123 SATISFIED.
> **Does not** edit file 08.
> **Does not** edit, move, or re-freeze any frozen artifact.
> **Does not** record any leftover-join as current that is not current
> at draft time, or any superseded leftover-join as current.
> **Does not** amend D-000 or D-056.
> **Does not** open D-056 Class A.
> **Does not** pin QUALIFIED.
> **Does not** invent fixture bytes or observation bytes.
> **Does not** decide any reserved number, list, owner, or Class A
> question.
> **Does not** add a DR-G* row or change live required-now 28.
> **Does not** flatten DR-118 `DECIDED-V1-NOT-INTEGRATED`
> to `OPEN`.
> **Does not** flatten DR-107 `PROPOSED-CLOSED-FOR-REVIEW`
> to `OPEN`.
> **Does not** unwrite D-261, D-264, D-269, D-270, D-276, D-278, D-281,
> or D-282 through D-292.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

{LASTD} is ADOPTED at
`{ADOPTED_AT}`.
HEAD is `{HEAD}`.
Last live heading is {LASTD}. Required-now is 28.

## Why this entry exists

D-282 through D-287 recorded successors of five ROW leftover-joins and one GATE leftover-join (exact-bytes, DR-G07), and D-288 through D-292 recorded successors of the five GATE leftover-joins that had named the ROW successors' predecessors as current (version-number reading, this orchestrator):

| Superseded | Current successor | Row | leftoverDesign |
|---|---|---|---|
{tbl_s}

{NUM[n_joins]} leftover-joins that are current at draft time carry a
present-tense sentence naming a since-superseded sibling as the current
leftover-join of its row: {NUM[n_pairs].lower()} citations (citing join, cited
version) at {NUM.get(n_sites,str(n_sites)).lower()} sites. After D-288 through D-292 none of them is a
GATE join naming a ROW join; they are ROW joins naming superseded GATE
joins (the direction D-276, D-278, and D-281 kept current) and two ROW
joins naming a superseded ROW join — a direction D-282 and D-285 also
tolerated: D-282 superseded component-manifest leftover-join.v6 while
expressly keeping packaging leftover-join.v4 current, and D-285
superseded doctor-actor leftover-join.v11 while expressly keeping
permission leftover-join.v12 current, each of those ROW joins naming the
superseded version as current.

The record holds both readings of such a sentence. D-276, D-278, and
D-281 kept {kept} current while each already named a superseded GATE
leftover-join as current; D-276 records "lifecycle leftover-join.v4
remains the current DR-107 leftover-join" in the same act that
superseded the g18 leftover-join.v5 that lifecycle leftover-join.v4
names. D-269, D-270, D-271, D-274, D-276, D-278, D-281, and D-288 through
D-292 did the opposite for GATE joins: each recorded a GATE successor
after a ROW join it named was superseded (D-270 after packaging
leftover-join.v4, D-271 after platform-tcb leftover-join.v9, D-274 after
language-quality leftover-join.v5, per each successor's own
basedOn.predecessor role). D-269, for example,
recorded g20 leftover-join.v6 after D-267 superseded the sdk
leftover-join.v5 that g20 leftover-join.v4 named, with the G20 occupancy
unchanged ("Occupancy v2 is the current
G20 occupancy remasurement. Occupancy v1 is not current. sdk
leftover-join.v6 remains the current DR-125 leftover-join. sdk
leftover-join.v5 is not current."). D-261, D-264, D-282, D-283, and D-285
were occupancy remasurements that refreshed their cross-citations in
passing. D-284 and D-286 were both occupancy-driven and
citation-driven: state-class leftover-join.v4 remasures leftover-join.v3
after occupancy v2 (D-222) and g19 leftover-join.v4 (D-256), and
exact-bytes leftover-join.v7's predecessor role names two stale inputs
it remasures — occupancy v3 after occupancy v4 (D-210) and
component-manifest leftover-join.v4 after component-manifest
leftover-join.v9 (D-282). D-287 was an occupancy remasurement with no
cross-lineage leftover-join citation to refresh.

Without a stated reading, every ROW successor re-flags the GATE joins
that cite it and every GATE successor re-flags the ROW joins that cite
it, and each such successor re-flags its own citers in turn. The
citations at issue carry no measured content of their own: in all
{NUM[n_pairs].lower()} cases the cited version and its current successor hold
byte-identical leftoverDesign partitions, and every obligation identifier
the citing sentences name has the same presence in both and, where
present, the same leftoverDesign value, so the leftover-design custody
the citing join relies on has not moved. This entry states the
reading the record already applies so that later hunts measure
staleness by content, not by version number.

## Measured inputs

Citing leftover-joins (all current at draft time; unmoved by this entry):

| Path | sha256 | Row (kind) |
|---|---|---|
{tbl_c}

Present-tense cross-lineage citations of a superseded sibling (measured
from the bytes above; the quoted sentence is the first such site in
each file; "sites" counts every present-tense site for that pair):

| Citing | Cites as current | Current successor | Sites | First site | leftoverDesign of cited version | Obligation ids the citing sentences name |
|---|---|---|---|---|---|---|
{tbl_p}

| Path | sha256 |
|---|---|
| `docs/coop/COORDINATOR-DECISIONS.md` | `{sha(COORD)}` |
| file 08 | `{sha(F08)}` |
| HEAD (live at draft time) | `{HEAD}` |

The measurement rule used above: a sentence is a present-tense
cross-lineage citation when it names another lineage's leftover-join
version, in dotted (`leftover-join.vN`) or spaced (`leftover-join vN`)
spelling with the lineage stem immediately before `leftover-join`, and
asserts currency in any of these forms: `remains`/`remain`/`is`/`are`
followed by optional `the` and `current`; the inverted predicate
`[the] current <row> leftover-join is/are/remains <X> leftover-join.vN`;
or `Cite <X> leftover-join.vN as the current …` (a purpose-field
statement of the join's own act) — or `still measure(s)` — without a
historical marker and without also naming that
lineage's current successor in the same sentence ("cited", "was current", "not
current after", "does not record … as current", "must not",
"historically"). A version token without the lineage stem immediately before
`leftover-join` (for example "Current G23 GATE leftover-join is
leftover-join.v8") is not counted as a site under this rule, although
it reads the same way. Sentences
that only pin a path or a digest (recordedInputs, `.path` members) are
not citations under this rule. A citing join's own predecessors are not
cross-lineage.

If a cited file moves in a way that is not append-only COORD growth or
COORD heading hygiene, with file 08 and the {NUM[n_joins].lower()} citing leftover-joins
unmoved, remasure before adoption. Append-only COORD after this
remasurement, with those files unmoved, is **PASS-NO-SCOPE-EFFECT**
and is not a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remasurement at draft time: required-now 28 of 28 named; owners
32 of 32; last gate row DR-G32; Condition 2 is 5 of 32; DR-107 remains
`PROPOSED-CLOSED-FOR-REVIEW`; DR-118 remains
`DECIDED-V1-NOT-INTEGRATED`. Every leftover-join the tables above name as a citing join or as a
current successor is the current recorded leftover-join of its lineage
at draft time; every version the tables name as cited-then-superseded
is not current.

This is a reading convention. It does not claim that D-056 gates 2 and
3 do not hold.

## Decision

1. **Reading (symmetric).** In a recorded leftover-join, a sentence
   that names another lineage's leftover-join version (dotted or spaced
   spelling, stem immediately before `leftover-join`) and asserts
   currency — `remains`/`remain`/`is`/`are` [`the`] `current`; the
   inverted `[the] current <row> leftover-join is/are/remains X
   leftover-join.vN`; `Cite X leftover-join.vN as the current …`; or
   `still measure(s)` — for example "X leftover-join.vN remains the
   current <row> leftover-join (D-mmm)" — is custody at
   that join's own recording heading: it records which sibling was
   current when the join was recorded. It is not a standing claim about
   live HEAD. This reading applies alike whichever kind, ROW or GATE, the
   citing join and the cited join are (a GATE join naming a GATE join
   reads the same way: g25 leftover-join.v5 says "Current G23 GATE
   leftover-join is leftover-join.v8 (D-240)" — a direction example,
   not a counted site, since the token carries no lineage stem). A later successor of X does not, by itself, make the citing
   join stale, not current, or in need of a successor.
2. **What still requires a successor.** A recorded leftover-join needs
   a successor when (a) an occupancy it cites as the specification is
   superseded — the occupancy-stale class recorded, for example, at
   D-261, D-264, and D-282 through D-287; or (b) a sibling successor
   changes any value the citing join relies on, measured from the two
   files' bytes by the projection below; or (c) its own lineage is superseded. The test for (b) is
   mechanical: the cited version's and the successor's leftoverDesign
   partitions (summary.leftoverDesign, else the obligations with
   leftoverDesign true) are byte-identical; the cited join's
   `registerRow`, `file08StatusToken`, and `liveGateOwners` equal the
   successor's wherever the cited version carries the field (a field the successor
   adds is not a value the citer relied on);
   every obligation identifier named in the citing sentences has the
   same presence in both and, where present, equal `leftoverDesign`,
   `existingGate`, `rideStanding`, and `executionObligationOwnerToday`;
   and every "still measures … leftoverDesign true/false" sentence
   asserts the value the successor holds. A successor is required
   whenever any of those projected values changes. Under (b), all {NUM[n_pairs].lower()} citations
   measured above pass; none requires a successor on this ground.
   Triggers (a) and (c) carry no status-token exception: a join on a
   SATISFIED row whose consumed occupancy is superseded still needs a
   successor. A hunt that flags a join on version number alone, with
   every projected value equal, flags nothing.
3. **Refresh.** A successor issued for any reason refreshes its
   cross-lineage citations to the versions current at its dispatch and
   labels the superseded ones as not current, as the successors recorded
   at D-249 through D-271 and D-273 through D-287 did wherever they
   carried such citations (D-272 is CONTESTED and parked; it adopts nothing). No frozen artifact is edited to achieve this.
4. **Standing at draft time.** The {NUM[n_joins].lower()} citing leftover-joins remain
   current. The eleven successors recorded by D-282 through D-292 remain
   current. The superseded versions named above are not current. Zero
   SATISFIED. Required-now stays 28. Condition 2 stays 5 of 32.
   Condition-4 effect is zero. File 08 is untouched.
5. **Scope.** This entry governs the reading of cross-lineage citation
   currency from this heading forward. D-269 stays recorded and is not
   unwritten; g20 leftover-join.v6 remains current. It does not amend
   D-000 or D-056, does not decide any reserved number, list, owner, or Class A
   question, binds no fixture bytes, and does not edit file 08 or any
   artifact. Does not authorize `docs/v2/implementation/`.

## Readiness effect

Zero SATISFIED. Condition 2 stays 5 of 32. Condition 4 stays
MET on the naming half (28 of 28). Condition 5 last.

## Reversibility

Total. Overturn: C-{NEW.replace('-','')}. Overturning restores the version-number reading
and re-flags the {NUM[n_joins].lower()} citing leftover-joins; it edits no artifact. Does
not unwrite D-261, D-264, D-269, D-270, D-276, D-278, D-281, or D-282
through D-292.
"""
draft=re.sub(r'(?<=\S)  +(?=\S)',' ',draft); draft=re.sub(r' +\n','\n',draft)
out=SCR+f'coordinator-decisions.{NEW}.draft.md'; open(out,'w').write(draft); print('wrote',out,len(draft))
json.dump({'new':NEW,'counts':[n_joins,n_pairs,n_sites],'pairs':[[list(k),[list(r) for r in rs]] for k,rs in pairs.items()],'citing':[list(x) for x in citing],'sup':sup},open(SCR+'D288-facts.json','w'),indent=1)
if '--freeze' in sys.argv:
    DST=P(f'coordinator-decisions.{NEW}{TS}.draft.md'); assert not os.path.exists(DST); open(DST,'w').write(draft); os.chmod(DST,0o444); DS=sha(DST)
    CLB=f'coordinator-decisions.{NEW}.review-adversarial.claude2{TS}.json'; CXB=f'coordinator-decisions.{NEW}.review-adversarial.codex{TS}.json'
    joins=', '.join(f"`{f}`" for st,v,row,kind,f,sh in citing)
    prompt=f"""# Adversarial review — {NEW} (turn {TURN} of 3)

Independent, refute not confirm.

**SUBJECT:** `{DST}`
Expected sha256:
`{DS}`
Mode 0444. If the subject moves, OBJECT.

**WRITE ONLY:**
- Claude 2: `{P(CLB)}`
- Codex: `{P(CXB)}`

Do not edit the subject. Do not commit. Do not edit file 08 or COORD.
Do not edit, move, or re-freeze any artifact.
Do not mark any row SATISFIED. Do not SATISFY DR-101, DR-103, DR-105, DR-107, DR-112, DR-114, DR-117, DR-118, DR-120, DR-121, DR-124, DR-131, or DR-133.
Do not flatten DR-118 `DECIDED-V1-NOT-INTEGRATED` to `OPEN`.
Do not flatten DR-107 `PROPOSED-CLOSED-FOR-REVIEW` to `OPEN`.
Do not invent identifiers. Do not invent a verdict for the other reviewer.
Do not read the other reviewer.

HEAD is `{HEAD}` ({LASTD} ADOPTED). Last heading is {LASTD}. Required-now is 28.
Live COORD sha256 is `{sha(COORD)}`; file 08 sha256 is `{sha(F08)}`.

This is a reading-convention COORD draft, not a remasurement. It has no Stage A subject. Its measured inputs are the {NUM[n_joins].lower()} current leftover-joins it names: {joins}.
Re-measure every table row from those bytes: each quoted sentence, each recording heading in COORDINATOR-DECISIONS.md, and each leftoverDesign partition of the cited version and its current successor (summary.leftoverDesign where present, else the obligations with leftoverDesign true).
Re-measure the draft's precedent claims against the D-261, D-264, D-269, D-270, D-276, D-278, D-281, and D-282 through D-286 entries.
If the draft's reading is outside the orchestrator's delegated authority under D-000, say so as a MUST-FIX naming the D-000 clause.
If the draft states a claim its cited bytes contradict, say so.

The no-cell-edit branch is D-170 through D-235 and D-237 through D-271 and D-273 through {LASTD}. D-272 is CONTESTED and is not on that adoption branch. The branch must not span D-236.

CONSENT only if no MUST-FIX or SHOULD-FIX.
Final chat: CONSENT or OBJECT.
"""
    pp=P(f'coordinator-decisions.{NEW}{TS}.review-prompt.md'); assert not os.path.exists(pp); open(pp,'w').write(prompt); os.chmod(pp,0o444)
    hist=''
    if TURN>1:
        lines=[]
        for who,base in (('Claude 2','claude2'),('Codex','codex')):
            for t in range(1,TURN):
                ts='' if t==1 else f'.turn{t}'; rf=P(f'coordinator-decisions.{NEW}.review-adversarial.{base}{ts}.json')
                if not os.path.exists(rf): continue
                rj=json.load(open(rf)); ids=[f.get('id') for k in ('mustFix','shouldFix') for f in rj.get(k,[]) if isinstance(f,dict) and f.get('id')]
                lines.append(f"turn-{t} {who} {rj.get('verdict')}"+(f" ({' / '.join(ids)})" if ids else ''))
        frozen=[]
        for t in range(1,TURN):
            ts='' if t==1 else f'.turn{t}'; df=P(f'coordinator-decisions.{NEW}{ts}.draft.md')
            if os.path.exists(df): frozen.append(f"`{df}` `{sha(df)}`")
        hist=('\nPrior turns: '+'; '.join(lines)+'. This turn answers every named finding; re-check each against the new bytes and say which stand.'+(' Prior subjects remain frozen on disk and are not this turn\'s subject: '+'; '.join(frozen)+'.' if frozen else '')+'\n') if lines else ''
    dispatch=f"""Adversarial review of {NEW} COORD draft. Turn {TURN} of 3.

Read {pp}
and execute it. Refute, do not confirm.

SUBJECT sha256 must be
{DS}
Mode 0444. If the subject moved, OBJECT.

Write only your review JSON path from that prompt.
Do not edit the subject. Do not commit. Do not edit file 08 or COORD.

This is a reading-convention COORD draft (RULE-GOVERNED), not a remasurement: it has no Stage A subject. D-293 (ADOPTED 2026-08-28, a user-made entry) adopted this convention in principle and authorized this dual-CONSENT cycle; it did not adopt the draft's text. Re-measure every table row of the draft from the named leftover-join bytes and COORD headings as the prompt instructs; check the projection fields the draft names (registerRow, file08StatusToken, liveGateOwners, and per named obligation leftoverDesign, existingGate, rideStanding, executionObligationOwnerToday) against the cited and successor versions; check every precedent claim against the named entries.
Do not invent identifiers. Do not invent a verdict for the other reviewer.{hist}
CONSENT only if no MUST-FIX or SHOULD-FIX.
Final chat: CONSENT or OBJECT.
"""
    dp=P(f'_dispatch.{NEW}'+('' if TURN==1 else f'-t{TURN}')+'.txt'); open(dp,'w').write(dispatch)
    print('draft',DST,DS); print('prompt',pp,sha(pp)); print('dispatch',dp,len(dispatch))
