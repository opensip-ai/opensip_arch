#!/usr/bin/env python3
"""g09-leftover-join.v12 (G09 GATE join) from frozen leftover-join.v11: refresh the DR-105 ROW citation (permission leftover-join.v9 -> v12, D-283) and the DR-114 ROW citation (doctor-actor leftover-join.v11 -> v12, D-285). Occupancy v4 (D-220) unchanged. leftoverDesign unchanged. Re-pin live inputs. Precedent: g18 leftover-join.v5 -> v6 (D-276)."""
import json, collections, hashlib, subprocess, re, sys, os, datetime
REPO='/Users/sb/code/opensip-ai/opensip'; os.chdir(REPO); O=collections.OrderedDict
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
def git(*a): return subprocess.check_output(['git',*a],text=True).strip()
HEAD=git('rev-parse','HEAD'); COORD='docs/coop/COORDINATOR-DECISIONS.md'; F08='docs/v2/architecture/08-decision-and-readiness-register.md'
assert hashlib.sha256(subprocess.check_output(['git','show',f'HEAD:{COORD}'])).hexdigest()==sha(COORD), 'COORD differs from HEAD'
assert hashlib.sha256(subprocess.check_output(['git','show',f'HEAD:{F08}'])).hexdigest()==sha(F08), 'file 08 differs from HEAD'
heads=[l.rstrip('\n') for l in open(COORD) if l.startswith('## D-')]; LASTD=re.match(r'## (D-\d+)',heads[-1]).group(1)
A='docs/coop/artifacts/'; P=lambda n:A+n
LOG=subprocess.check_output(['git','log','--format=%H %s'],text=True).splitlines()
def commit_of(d):
    for line in LOG:
        if re.match(rf'^[0-9a-f]+ {d}: ',line): return line.split()[0]
    raise SystemExit('no recording commit for '+d)
def recorded(stem):
    """{version: D} of every non-CONTESTED '## D-NNN — Record <stem> leftover-join.vN ' heading."""
    out={}
    for h in heads:
        if 'CONTESTED' in h: continue
        m=re.match(rf'## (D-\d+) — Record {re.escape(stem)}[- ]leftover-join\.v(\d+) ',h)
        if m: out[int(m.group(2))]=m.group(1)
    return out
PERM=recorded('permission'); DOC=recorded('doctor-actor'); OWN=recorded('g09')
assert PERM.get(9)=='D-171' and PERM.get(12)=='D-283' and max(PERM)==12, PERM
assert DOC.get(11)=='D-170' and DOC.get(12)=='D-285' and max(DOC)==12, DOC
assert OWN=={10:'D-189',11:'D-257'}, OWN
assert any(re.match(r'## D-220 — Record harness\.DR-G09\.permissions\.preview-scoped\.v4 as G09 occupancy remasurement',h) for h in heads)
assert any(re.match(r'## D-086 — ',h) for h in heads)
assert LASTD not in ('D-257','D-283','D-285','D-220','D-189'), LASTD
PJ9='permission leftover-join.v9'; PJ12='permission leftover-join.v12'; DJ11='doctor-actor leftover-join.v11'; DJ12='doctor-actor leftover-join.v12'
LD='[OBL-FX-AUTHORING]'; DR105='OBL-FX-AUTHORING, OBL-R10-AUTHORING, OBL-R6-AUTHORING, OBL-FC-C1, and OBL-BLK-1..4'
LIN_P='permission leftover-join and g09 leftover-join are different lineages; their version numbers are unrelated.'
LIN_D='doctor-actor leftover-join and g09 leftover-join are different lineages; their version numbers are unrelated.'
v11=json.load(open(P('g09-leftover-join.v11.json')),object_pairs_hook=O)
assert v11['artifact']=='g09-leftover-join.v11' and v11['version']==11 and v11['registerRow']=='DR-G09'
# ---- byte checks on the cited ROW joins and the occupancy ----
EIGHT=['OBL-FX-AUTHORING','OBL-R10-AUTHORING','OBL-R6-AUTHORING','OBL-FC-C1','OBL-BLK-1','OBL-BLK-2','OBL-BLK-3','OBL-BLK-4']
def ld_true(d): return [o['id'] for o in d['obligations'] if o.get('leftoverDesign') is True]
def ld_false(d): return [o['id'] for o in d['obligations'] if o.get('leftoverDesign') is False]
p9=json.load(open(P('permission-leftover-join.v9.json'))); p12=json.load(open(P('permission-leftover-join.v12.json')))
d11=json.load(open(P('doctor-actor-leftover-join.v11.json'))); d12=json.load(open(P('doctor-actor-leftover-join.v12.json')))
assert p12['artifact']=='permission-leftover-join.v12' and p12['registerRow']=='DR-105' and d12['artifact']=='doctor-actor-leftover-join.v12' and d12['registerRow']=='DR-114'
assert p9['summary']['leftoverDesign']==p12['summary']['leftoverDesign']==ld_true(p9)==ld_true(p12)==EIGHT, (p9['summary']['leftoverDesign'],p12['summary']['leftoverDesign'])
assert 'OBL-FX-INPUT-CORPUS' in ld_false(p12) and 'OBL-R10-R6-INPUT-CORPUS' in ld_false(p12) and 'OBL-FX-INPUT-CORPUS' in ld_false(p9) and 'OBL-R10-R6-INPUT-CORPUS' in ld_false(p9)
assert d11['summary']['leftoverDesign']==d12['summary']['leftoverDesign']==ld_true(d11)==ld_true(d12), (d11['summary']['leftoverDesign'],d12['summary']['leftoverDesign'])
assert {'OBL-FC-C1','OBL-BLK-1','OBL-BLK-2','OBL-BLK-3','OBL-BLK-4'}<=set(ld_true(d12))
o3=json.load(open(P('harness.DR-G09.permissions.preview-scoped.v3.json'))); o4=json.load(open(P('harness.DR-G09.permissions.preview-scoped.v4.json')))
assert o3['whatThisCloses']['leftoverDesignRemainingOnDR105']==o4['whatThisCloses']['leftoverDesignRemainingOnDR105']==EIGHT
assert o3['namedCorpusNotAuthored']==o4['namedCorpusNotAuthored']==v11['namedCorpusNotAuthored'] and len(o4['namedCorpusNotAuthored'])==14
assert v11['summary']['leftoverDesign']==['OBL-FX-AUTHORING'] and ld_true(v11)==['OBL-FX-AUTHORING']
# ---- finding landings, verified from this lineage's bytes ----
G={n:json.load(open(P(f'g09-leftover-join.v{n}.json'))) for n in range(4,12)}
def fd_ids(n): return [f['id'] for f in (G[n].get('findingDisposition') or [])]
def getp(d,path):
    cur=d
    for part in path.split('.'):
        if isinstance(cur,list): m=[x for x in cur if isinstance(x,dict) and x.get('id')==part]; cur=m[0] if m else None
        elif isinstance(cur,dict): cur=cur.get(part)
        else: cur=None
        if cur is None: return None
    return cur
assert 'lands' not in v11
LAND={}
for f in v11['findingDisposition']:
    n=int(re.search(r'V(\d+)',f['id']).group(1)); k=n+1
    assert f['id'] not in fd_ids(n) and f['id'] in fd_ids(k), (f['id'],n,k)
    for p in f['landedAt']:
        if f['id']=='G09LJ-V4-B2' and p=='basedOn.permissionJoinV7.review.verdict':
            assert getp(G[4],p)==getp(G[5],p) and getp(G[5],p)!=getp(G[6],p) and 'Codex not reviewed' in getp(G[5],p) and 'G09LJ-V5-B1' in fd_ids(6)
        else: assert getp(G[n],p)!=getp(G[k],p), (f['id'],p)
    LAND[f['id']]=k
def rev(path):
    d=json.load(open(path)); vd=d.get('verdict'); mf=d.get('mustFixCount'); sf=d.get('shouldFixCount')
    if not isinstance(mf,int): mf=len(d.get('mustFix') or []) if isinstance(d.get('mustFix'),list) else (d.get('mustFix') if isinstance(d.get('mustFix'),int) else 0)
    if not isinstance(sf,int): sf=len(d.get('shouldFix') or []) if isinstance(d.get('shouldFix'),list) else (d.get('shouldFix') if isinstance(d.get('shouldFix'),int) else 0)
    assert vd=='ACCEPT' and mf==0 and sf==0,(path,vd,mf,sf); return 'ACCEPT 0/0'
def pin(name, recording, role):
    stem=name[:-5]; c=P(stem+'.review-independent.claude2.json'); x=P(stem+'.review-independent.codex.json')
    return O([('path',P(name)),('sha256',sha(P(name))),('recording',recording),('reviews',O([('claude',O([('path',c),('sha256',sha(c)),('verdict',rev(c))])),('codex',O([('path',x),('sha256',sha(x)),('verdict',rev(x))]))])),('role',role)])
def cust(d,role): return O([('recording',d),('commit',commit_of(d)),('role',role)])
def rq(c,k,old,new):
    cur=c[k]; assert old in cur,(k,old); c[k]=cur.replace(old,new)
# ---- build ----
v=O()
v['artifact']='g09-leftover-join.v12'; v['version']=12; v['date']=datetime.date.today().isoformat()
v['documentClass']=v11['documentClass']; v['registerRow']='DR-G09'
v['registerRowNote']=(f"registerRow is the already-named gate DR-G09 because this join remasures leftover-design of G09 after occupancy v4 (D-220) and after {PJ12} (D-283) and {DJ12} (D-285). file08StatusToken is DR-G09's own live token (OPEN). leftover-join.v11 remains frozen and is not current after this successor is recorded. leftover-join.v10 remains frozen and is not current. D-086 named DR-G09 as required-now. {PJ12} remains the current DR-105 ROW leftover-join (D-283; registerRow DR-105). {DJ12} remains the current DR-114 ROW leftover-join (D-285; registerRow DR-114). {PJ9} and {DJ11} are not current. This join does not retarget DR-105 leftover, does not steal OBL-R10-AUTHORING, OBL-R6-AUTHORING, OBL-FC-C1, or OBL-BLK-1..4, does not steal the DR-114 remainder, does not invent fixture bytes, does not invent a decision-record envelope, and does not SATISFY DR-105.")
for k in ['status','reviewStatus','sealRecommendation','binds']: v[k]=v11[k]
v['authorityClaim']=(f"This artifact PROPOSES an execution-remainder join successor for G09 leftovers. v12 remasures leftover-join.v11 after {PJ12} (D-283) and {DJ12} (D-285). leftover-join.v11 remains frozen. leftoverDesign remains {LD}. Occupancy v4 (D-220) remains the current G09 occupancy remasurement. It does not SATISFY DR-105. It does not close leftover-design of OBL-FX-AUTHORING. It does not invent fixture bytes. It does not invent a decision-record envelope. It does not steal DR-105 leftover. It does not steal the DR-114 remainder. It does not add a DR-G* row. It does not change live required-now 28. It does not execute fixtures. It lands no new finding. It applies nothing and does not authorize docs/v2/implementation/.")
v['purpose']=(f"Remasure leftover-join.v11 against live HEAD after {PJ12} (D-283) and {DJ12} (D-285). Cite {PJ12} as the current DR-105 leftover-join; leftover-join.v11 cited {PJ9}. Cite {DJ12} as the current DR-114 leftover-join; leftover-join.v11 cited {DJ11}. Cite occupancy v4 (D-220) as the current occupancy remasurement, as leftover-join.v11 did. Preserve leftoverDesign {LD}. Frozen leftover-join.v11 stays unmoved. Do not SATISFY DR-105. Do not invent fixture bytes. Do not invent a decision-record envelope. Do not steal OBL-R10-AUTHORING, OBL-R6-AUTHORING, OBL-FC-C1, or OBL-BLK-1..4.")
b=O()
for k,val in v11['basedOn'].items():
    if k=='d256': continue  # stale last-heading custody of leftover-join.v11; replaced by d<LASTD> below (g18 v5->v6, g16 v4->v5, g08 v4->v5 precedent)
    b[k]=O(val) if isinstance(val,dict) else val
assert v11['basedOn']['d256']['role']=="Last live heading at dispatch. Last-heading custody only."
rq(b['permissionJoinV6'],'role',f"Current DR-105 ROW leftover-join is {PJ9} (D-171).",f"{PJ9} was current at D-171; not current after D-283. Current DR-105 ROW leftover-join is {PJ12} (D-283).")
rq(b['permissionJoinV7'],'role',"D-171 froze permission leftover-join v7/v8 and recorded permission leftover-join v9 as current.",f"D-171 froze permission leftover-join v7/v8 and recorded {PJ9} as then-current; {PJ9} is not current after D-283. Current DR-105 ROW leftover-join is {PJ12} (D-283).")
b['permissionJoinV9']['role']=(f"Predecessor ROW leftover-join. Historical. Dual ACCEPT 0/0. Recorded as current DR-105 leftover-join at D-171. leftoverDesign remains {DR105} (list-identical in {PJ12}). Not current. Current DR-105 ROW leftover-join is {PJ12} (D-283). {LIN_P} Not this artifact's version number.")
b['doctorActorJoinV11']['role']=(f"Predecessor ROW leftover-join. Historical. Dual ACCEPT 0/0. Recorded as current DR-114 leftover-join at D-170. leftoverDesign includes OBL-FC-C1 and OBL-BLK-1..4 on DR-114 (list-identical in {DJ12}). Not current. Current DR-114 ROW leftover-join is {DJ12} (D-285). {LIN_D} Not this artifact's version number.")
b['predecessorV10']['role']=("Predecessor. Unmoved. Dual ACCEPT 0/0. Recorded as current G09 leftover-join at D-189; not current after D-257. Cited occupancy v3 as the specification. leftover-join.v11 remasured occupancy v3 stale after occupancy v4 (D-220). Occupancy v4 remains the current occupancy remasurement. Not this artifact's version number.")
b['d257']=cust('D-257',"Recorded leftover-join.v11 as current G09 leftover-join. Not last-heading. Not this artifact's version number.")
b['predecessorV11']=pin('g09-leftover-join.v11.json','D-257',f"Predecessor. Unmoved. Dual ACCEPT 0/0. Recorded as current G09 leftover-join at D-257. Cited occupancy v4 (D-220) as the current occupancy remasurement, {PJ9} as the current DR-105 leftover-join, and {DJ11} as the current DR-114 leftover-join. This v12 remasures those two ROW citations stale after D-283 and D-285. Not this artifact's version number.")
b['d283']=cust('D-283',f"Recorded {PJ12} as current DR-105 leftover-join. Not last-heading. Not this artifact's version number.")
b['permissionJoinV12']=pin('permission-leftover-join.v12.json','D-283',f"Current DR-105 ROW leftover-join recorded at D-283. leftoverDesign remains {DR105} (identical to {PJ9}). This GATE leftover-join does not steal those leftovers. {LIN_P} Not this artifact's version number.")
b['d285']=cust('D-285',f"Recorded {DJ12} as current DR-114 leftover-join. Not last-heading. Not this artifact's version number.")
b['doctorActorJoinV12']=pin('doctor-actor-leftover-join.v12.json','D-285',f"Current DR-114 ROW leftover-join recorded at D-285. leftoverDesign includes OBL-FC-C1 and OBL-BLK-1..4 on DR-114 (identical to {DJ11}). This GATE leftover-join does not steal that remainder. {LIN_D} Not this artifact's version number.")
b['d'+LASTD[2:]]=cust(LASTD,"Last live heading at dispatch. Last-heading custody only.")
v['basedOn']=b
v['file08Pin']=O([('path',F08),('sha256',sha(F08))]); v['head']=HEAD; v['requiredNowUnchanged']=28; v['file08StatusToken']='OPEN'
f08=open(F08).read(); row=[l for l in f08.splitlines() if l.startswith('| DR-G09 ')]; assert len(row)==1 and row[0].rstrip().endswith('| OPEN |') and '(D-086;' in row[0], row
v['leftoverDesignOpenStanding']=(f"The live DR-G09 token is OPEN. leftover-design of unnamed FX INPUT manifests is stale as a naming claim after the fourteen FX INPUT-manifest corpora and {PJ9} (D-171); {PJ12} (D-283) still measures OBL-FX-INPUT-CORPUS leftoverDesign false on DR-105. leftover-design of unnamed R-10/R-6 initial states is stale as a naming claim after permission-r6-r10-input-corpus.v2 and {PJ9} (D-171); {PJ12} (D-283) still measures OBL-R10-R6-INPUT-CORPUS leftoverDesign false on DR-105. leftover-design of FX decision-record implementations remains. leftover-design of R-10 and R-6 implementations remains on DR-105 ({PJ12}, D-283). A decision-record envelope is not invented. DR-105 leftover is not stolen. DR-105 is not SATISFIED.")
v['namedCorpusNotAuthored']=v11['namedCorpusNotAuthored']; v['namedRaceByteSetsNotAuthored']=v11['namedRaceByteSetsNotAuthored']
ri=O(v11['recordedInputs']); ri[COORD]=sha(COORD); ri[F08]=sha(F08); ri['HEAD']=HEAD
for n in ['g09-leftover-join.v11.json','g09-leftover-join.v11.review-independent.claude2.json','g09-leftover-join.v11.review-independent.codex.json','permission-leftover-join.v12.json','permission-leftover-join.v12.review-independent.claude2.json','permission-leftover-join.v12.review-independent.codex.json','doctor-actor-leftover-join.v12.json','doctor-actor-leftover-join.v12.review-independent.claude2.json','doctor-actor-leftover-join.v12.review-independent.codex.json']: ri[P(n)]=sha(P(n))
v['recordedInputs']=ri
v['remeasurementClause']=(f"If a cited file moves in a way that is not append-only COORD growth or COORD heading hygiene, with file 08, leftover-join.v11, leftover-join.v10, occupancy v4, occupancy v3, permission leftover-join v12, permission leftover-join v9, doctor-actor leftover-join v12, doctor-actor leftover-join v11, and this draft unmoved, remasure before recording. recordedInputs.HEAD must equal the top-level head. This join does not unwrite D-086 or D-167 through {LASTD}. Frozen leftover-join.v11 of this lineage remains a historical measurement recorded at D-257 after this successor is recorded. Frozen leftover-join.v10 of this lineage remains a historical measurement recorded at D-189. Frozen occupancy v4 remains current G09 occupancy remasurement. Frozen permission leftover-join v12 remains current DR-105 ROW leftover-join. Frozen doctor-actor leftover-join v12 remains current DR-114 ROW leftover-join.")
v['liveGateOwners']=v11['liveGateOwners']
obs=[]
for o in v11['obligations']:
    o=O(o); i=o['id']
    if i=='OBL-G09-INPUT-CORPUS': rq(o,'reason',f"{PJ9} (D-171) measures OBL-FX-INPUT-CORPUS leftoverDesign false on DR-105.",f"{PJ12} (D-283) measures OBL-FX-INPUT-CORPUS leftoverDesign false on DR-105, as {PJ9} (D-171) did.")
    if i=='OBL-R10-R6-INPUT-CORPUS': rq(o,'reason',f"{PJ9} (D-171) measures OBL-R10-R6-INPUT-CORPUS leftoverDesign false on DR-105.",f"{PJ12} (D-283) measures OBL-R10-R6-INPUT-CORPUS leftoverDesign false on DR-105, as {PJ9} (D-171) did.")
    if i=='OBL-DR105-LEFTOVER-NOT-STOLEN':
        rq(o,'reason',f"{PJ9} (D-171) still measures {DR105} leftoverDesign true on DR-105.",f"{PJ12} (D-283) still measures {DR105} leftoverDesign true on DR-105.")
        rq(o,'reason',f"{DJ11} (D-170) still measures OBL-FC-C1 and OBL-BLK-1..4 leftoverDesign true on DR-114.",f"{DJ12} (D-285) still measures OBL-FC-C1 and OBL-BLK-1..4 leftoverDesign true on DR-114.")
    obs.append(o)
assert obs[4]['id']=='OBL-FX-AUTHORING' and obs[4]['leftoverDesign'] is True
v['obligations']=obs; v['summary']=v11['summary']
v['doesNotCloseLeftoverAlone']=v11['doesNotCloseLeftoverAlone']
v['proposedLaterWork']=v11['proposedLaterWork']
dn=list(v11['doesNot']); j=dn.index("Does not record leftover-join.v10 as current after this successor is recorded.")
dn[j:j+1]=["Does not record leftover-join.v11 as current after this successor is recorded.","Does not record leftover-join.v10 as current G09 leftover-join."]
assert dn[-1]=="Does not record occupancy v3 as current occupancy."
dn+=[f"Does not record {PJ9} as current DR-105 leftover-join.",f"Does not record {DJ11} as current DR-114 leftover-join.","Does not land or re-land any finding."]
v['doesNot']=dn
fd=[]
for f in v11['findingDisposition']:
    f=O(f); assert f['disposition']=='ACCEPTED'; k=LAND[f['id']]
    if f['id']=='G09LJ-V4-B2': f['disposition']=f"ACCEPTED. Landed in this lineage at leftover-join.v5 (basedOn.permissionJoinV7.review.codex) and leftover-join.v6 (basedOn.permissionJoinV7.review.verdict, repaired under G09LJ-V5-B1). This v12 does not re-land it."
    else: f['disposition']=f"ACCEPTED. Landed in this lineage at leftover-join.v{k}. This v12 does not re-land it."
    fd.append(f)
v['findingDisposition']=fd
pr=O(v11['parentReview']); rq(pr,'role',"not leftover-join.v10.","not leftover-join.v11."); v['parentReview']=pr
assert pr['sha256']==sha(pr['path']) and pr['codex']['sha256']==sha(pr['codex']['path'])
assert list(v.keys())==list(v11.keys()), 'top-level key order changed'
out=sys.argv[1] if len(sys.argv)>1 else '/private/tmp/claude-501/-Users-sb-code-opensip-ai-opensip/dcbad0ae-7fad-4c78-89e7-e93d989f5501/scratchpad/g09-leftover-join.v12.json'
raw=json.dumps(v,indent=2,ensure_ascii=False)+'\n'
json.loads(raw,object_pairs_hook=lambda ps: (_ for _ in ()).throw(SystemExit('dup keys')) if len([k for k,_ in ps])!=len(set(k for k,_ in ps)) else dict(ps))
open(out,'w').write(raw)
d=json.loads(raw); hits=[]
def walk(x,p=''):
    if isinstance(x,dict):
        for k,vv in x.items(): yield from walk(vv,p+'.'+k)
    elif isinstance(x,list):
        for i,vv in enumerate(x): yield from walk(vv,p+f'[{i}]')
    elif isinstance(x,str): yield p,x
QUAL=r'(leftover-join\.|leftover-join |corpus |occupancy |Occupancy |contract\.|naming |catalog |this |This |at |Frozen |frozen |remasurement |G09 |harness\.[^ ]*\.|tables\.)$'
for p,s in walk(d):
    if p.endswith('.path') or p.startswith('.recordedInputs'): continue
    for m in re.finditer(r'[Tt]his v\d+',s):
        if m.group(0).lower()!='this v12': hits.append((p,'SPEAKER',s[max(0,m.start()-50):m.end()+40]))
    for m in re.finditer(r'(?<![\w.\-/])v\d+\b',s):
        if not re.search(QUAL,s[max(0,m.start()-26):m.start()]) and m.group(0)!='v12': hits.append((p,'BARE',s[max(0,m.start()-60):m.end()+30]))
    if re.search(r'\bv1[01]\b(?! of this lineage)',s) and 'leftover-join.v1' not in s and 'leftover-join v1' not in s: hits.append((p,'BARE-OWN',s[:120]))
bad=[k for k,s_ in ri.items() if k!='HEAD' and os.path.exists(k) and sha(k)!=s_]
assert not bad, ('recordedInputs digest mismatch',bad)
print('wrote',out,len(raw),'bytes; HEAD',HEAD[:10],'; last heading',LASTD,'; date',v['date'],'; landings',LAND); print('audit hits:',len(hits)); [print('  ',h) for h in hits]
