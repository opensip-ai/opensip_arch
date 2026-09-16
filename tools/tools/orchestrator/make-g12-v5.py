#!/usr/bin/env python3
"""g12-leftover-join.v5 (G12 GATE join) from frozen v4: refresh the DR-114 ROW citation doctor-actor leftover-join.v11 (D-170) -> doctor-actor leftover-join.v12 (D-285); occupancy v6 (D-221) unchanged; qualify bare tokens; re-pin live inputs."""
import json, collections, hashlib, subprocess, re, sys, os, datetime
REPO='/Users/sb/code/opensip-ai/opensip'; os.chdir(REPO); O=collections.OrderedDict
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
def git(*a): return subprocess.check_output(['git',*a],text=True).strip()
HEAD=git('rev-parse','HEAD'); COORD='docs/coop/COORDINATOR-DECISIONS.md'; F08='docs/v2/architecture/08-decision-and-readiness-register.md'
assert hashlib.sha256(subprocess.check_output(['git','show',f'HEAD:{COORD}'])).hexdigest()==sha(COORD), 'COORD working tree differs from HEAD'
heads=[l for l in open(COORD) if l.startswith('## D-')]; LASTD=re.match(r'## (D-\d+)',heads[-1]).group(1)
A='docs/coop/artifacts/'; P=lambda n:A+n
def commit_of(d):
    for line in subprocess.check_output(['git','log','--format=%H %s'],text=True).splitlines():
        if re.match(rf'^[0-9a-f]+ {d}: ',line): return line.split()[0]
    raise SystemExit('no commit for '+d)
def recorded(stem, ver):
    """D of the non-CONTESTED COORD heading that records <stem> leftover-join.v<ver>."""
    hits=[re.match(r'## (D-\d+)',h).group(1) for h in heads if 'CONTESTED' not in h and re.match(rf'## D-\d+ — Record {stem}[- ]leftover-join\.v{ver} ',h)]
    assert len(hits)==1,(stem,ver,hits); return hits[0]
def current_recorded(stem):
    best=None
    for h in heads:
        if 'CONTESTED' in h: continue
        m=re.match(rf'## (D-\d+) — Record {stem}[- ]leftover-join\.v(\d+) ',h)
        if m and (best is None or int(m.group(2))>best[0]): best=(int(m.group(2)),m.group(1))
    return best
# --- byte-checked record facts ---
DA_V,DA_D=current_recorded('doctor-actor'); assert (DA_V,DA_D)==(12,'D-285'),(DA_V,DA_D)
OLD_DA_D=recorded('doctor-actor',11); assert OLD_DA_D=='D-170'
OWN_D=recorded('g12',4); assert OWN_D=='D-258'
V3_D=recorded('g12',3); assert V3_D=='D-190'
OCC_D='D-221'; assert any(re.match(r'## D-221 — Record harness\.DR-G12\.doctor-purge\.preview\.v6 ',h) for h in heads)
assert 'CONTESTED' not in [h for h in heads if h.startswith('## D-285 ')][0]
assert 'CONTESTED' not in [h for h in heads if h.startswith('## D-258 ')][0]
DAJ_OLD='doctor-actor leftover-join.v11'; DAJ=f'doctor-actor leftover-join.v{DA_V}'
DA_SET=["OBL-DOCTOR-FX-AUTHORING","OBL-JOIN-FX-AUTHORING","OBL-FC-C1","OBL-BLK-1","OBL-BLK-2","OBL-BLK-3","OBL-BLK-4"]
da11=json.load(open(P('doctor-actor-leftover-join.v11.json'))); da12=json.load(open(P(f'doctor-actor-leftover-join.v{DA_V}.json')))
tset=lambda d:[o['id'] for o in d['obligations'] if o.get('leftoverDesign') is True]
fset=lambda d:[o['id'] for o in d['obligations'] if o.get('leftoverDesign') is False]
assert da11['summary']['leftoverDesign']==da12['summary']['leftoverDesign']==DA_SET==tset(da11)==tset(da12)
assert 'OBL-DOCTOR-FC-INPUT-CORPUS' in fset(da12) and 'OBL-JOIN-FX-EXECUTION' in fset(da12) and 'OBL-DOCTOR-FC-INPUT-CORPUS' in fset(da11) and 'OBL-JOIN-FX-EXECUTION' in fset(da11)
assert da12['registerRow']=='DR-114' and da11['registerRow']=='DR-114'
o4=json.load(open(P('harness.DR-G12.doctor-purge.preview.v4.json'))); o6=json.load(open(P('harness.DR-G12.doctor-purge.preview.v6.json')))
FC=["FC-RO","FC-NC","FC-NN","FC-SCHEMA","FC-D9","FC-REDACT","FC-MODE","FC-CONSENT","FC-POSTREPORT","FC-DEGRADED","FC-HOSTILE","FC-REMEDIATION"]
assert o4['namedCorpusNotAuthored']==o6['namedCorpusNotAuthored']==FC
row=[l for l in open(F08) if l.startswith('| DR-G12 ')]; assert len(row)==1 and '(D-086;' in row[0] and '| OPEN |' in row[0]
v4=json.load(open(P('g12-leftover-join.v4.json')),object_pairs_hook=O)
assert v4['version']==4 and v4['summary']['leftoverDesign']==["OBL-DOCTOR-FX-AUTHORING"] and 'findingDisposition' not in v4 and 'lands' not in v4
assert v4['basedOn']['occupancyV6']['sha256']==sha(P('harness.DR-G12.doctor-purge.preview.v6.json')), 'occupancy v6 moved'
assert v4['basedOn']['doctorJoinV11']['sha256']==sha(P('doctor-actor-leftover-join.v11.json')), 'doctor-actor v11 moved'
def rev(path):
    d=json.load(open(path)); v=d.get('verdict'); mf=d.get('mustFixCount'); sf=d.get('shouldFixCount')
    if not isinstance(mf,int): mf=len(d.get('mustFix') or []) if isinstance(d.get('mustFix'),list) else (d.get('mustFix') if isinstance(d.get('mustFix'),int) else 0)
    if not isinstance(sf,int): sf=len(d.get('shouldFix') or []) if isinstance(d.get('shouldFix'),list) else (d.get('shouldFix') if isinstance(d.get('shouldFix'),int) else 0)
    assert v=='ACCEPT' and mf==0 and sf==0,(path,v,mf,sf); return 'ACCEPT 0/0'
def pin(name, recording, role):
    stem=name[:-5]; c=P(stem+'.review-independent.claude2.json'); x=P(stem+'.review-independent.codex.json')
    return O([('path',P(name)),('sha256',sha(P(name))),('recording',recording),('reviews',O([('claude',O([('path',c),('sha256',sha(c)),('verdict',rev(c))])),('codex',O([('path',x),('sha256',sha(x)),('verdict',rev(x))]))])),('role',role)])
def cust(d,role): return O([('recording',d),('commit',commit_of(d)),('role',role)])
def rq(c,k,old,new):
    cur=c[k]; assert old in cur,(k,old); c[k]=cur.replace(old,new)
LD='[OBL-DOCTOR-FX-AUTHORING]'; DIFF='doctor-actor leftover-join and g12 leftover-join are different lineages; their version numbers are unrelated.'
STEAL='OBL-JOIN-FX-AUTHORING, OBL-JOIN-FX-EXECUTION, OBL-FC-C1, or OBL-BLK-1..4'
v=O()
v['artifact']='g12-leftover-join.v5'; v['version']=5; v['date']=datetime.date.today().isoformat()
v['documentClass']=v4['documentClass']; v['registerRow']='DR-G12'
v['registerRowNote']=(f"registerRow is the already-named gate DR-G12 because this join remasures leftover-design of G12 after occupancy v6 ({OCC_D}) and after {DAJ} ({DA_D}). file08StatusToken is DR-G12's own live token (OPEN). leftover-join.v4 remains frozen and is not current after this successor is recorded. leftover-join.v3 remains frozen and is not current. D-086 named DR-G12 as required-now. {DAJ} remains the current DR-114 ROW leftover-join ({DA_D}; registerRow DR-114). {DAJ_OLD} is not current. This join does not retarget DR-114 leftover, does not steal {STEAL}, does not invent fixture bytes, does not invent a D9 code, does not take over G21, and does not SATISFY DR-114.")
for k in ['status','reviewStatus','sealRecommendation','binds']: v[k]=v4[k]
v['authorityClaim']=(f"This artifact PROPOSES an execution-remainder join successor for G12 leftovers. v5 remasures leftover-join.v4 after {DAJ} ({DA_D}). leftover-join.v4 remains frozen. leftoverDesign remains {LD}. Occupancy v6 ({OCC_D}) remains the current G12 occupancy remasurement. It does not SATISFY DR-114. It does not close leftover-design of OBL-DOCTOR-FX-AUTHORING. It does not invent fixture bytes. It does not invent a D9 code. It does not take over G21. It does not steal DR-114 leftover. It does not add a DR-G* row. It does not change live required-now 28. It does not execute fixtures. It applies nothing and does not authorize docs/v2/implementation/.")
v['purpose']=(f"Remasure leftover-join.v4 against live HEAD after {DAJ} ({DA_D}). Cite {DAJ} as the current DR-114 leftover-join; leftover-join.v4 cited {DAJ_OLD}. Cite occupancy v6 ({OCC_D}) as the current occupancy remasurement, as leftover-join.v4 did. Preserve leftoverDesign {LD}. Frozen leftover-join.v4 stays unmoved. Do not SATISFY DR-114. Do not invent fixture bytes. Do not steal {STEAL}. Do not take over G21.")
b=O((k,val) for k,val in v4['basedOn'].items())
b['g12v4']=O(b['g12v4']); assert 'v6' in b['g12v4']['role']
b['namedCatalog']=O(b['namedCatalog']); rq(b['namedCatalog'],'role','Named the twelve live G12 v4 namedCorpusNotAuthored FC classes.','Named the twelve live G12 occupancy v4 namedCorpusNotAuthored FC classes (list-identical in occupancy v6).')
b['doctorJoinV6']=O(b['doctorJoinV6']); rq(b['doctorJoinV6'],'role',f'Current DR-114 remainder is {DAJ_OLD} ({OLD_DA_D}).',f'{DAJ_OLD} was current at {OLD_DA_D}; not current after {DA_D}. Current DR-114 ROW leftover-join is {DAJ} ({DA_D}).')
b['doctorJoinV11']=O(b['doctorJoinV11']); b['doctorJoinV11']['role']=(f"Predecessor ROW leftover-join. Historical. Dual ACCEPT 0/0. {DAJ_OLD} was current at {OLD_DA_D}; not current after {DA_D}. Current DR-114 ROW leftover-join is {DAJ} ({DA_D}). leftoverDesign on {DAJ_OLD} includes OBL-DOCTOR-FX-AUTHORING, OBL-JOIN-FX-AUTHORING, OBL-FC-C1, and OBL-BLK-1..4 on DR-114 (list-identical in {DAJ}). OBL-JOIN-FX-EXECUTION is leftoverDesign false on {DAJ_OLD}. This GATE leftover-join does not steal that remainder. {DIFF} Not this artifact's version number.")
del b['d257']
b['predecessorV3']=O(b['predecessorV3']); b['predecessorV3']['role']=(f"Predecessor. Unmoved. Dual ACCEPT 0/0. Recorded as current G12 leftover-join at {V3_D}; not current after {OWN_D}. Cited occupancy v4 as the specification. leftover-join.v4 remasured occupancy v4 stale after occupancy v6 ({OCC_D}). Occupancy v6 remains the current occupancy remasurement. Not this artifact's version number.")
b['d'+LASTD[2:]]=cust(LASTD,"Last live heading at dispatch. Last-heading custody only.")
b['d'+OWN_D[2:]]=cust(OWN_D,"Recorded leftover-join.v4 as current G12 leftover-join. Not last-heading. Not this artifact's version number.")
b['d'+DA_D[2:]]=cust(DA_D,f"Recorded {DAJ} as current DR-114 leftover-join. Not last-heading. Not this artifact's version number.")
b['doctorJoinV'+str(DA_V)]=pin(f'doctor-actor-leftover-join.v{DA_V}.json',DA_D,f"Current DR-114 ROW leftover-join recorded at {DA_D}. leftoverDesign remains OBL-DOCTOR-FX-AUTHORING, OBL-JOIN-FX-AUTHORING, OBL-FC-C1, and OBL-BLK-1..4 on DR-114 (identical to {DAJ_OLD}). OBL-JOIN-FX-EXECUTION is leftoverDesign false on {DAJ}. This GATE leftover-join does not steal those leftovers. {DIFF} Not this artifact's version number.")
b['predecessorV4']=pin('g12-leftover-join.v4.json',OWN_D,f"Predecessor. Unmoved. Dual ACCEPT 0/0. Recorded as current G12 leftover-join at {OWN_D}. Cited {DAJ_OLD} as the current DR-114 leftover-join. Cited occupancy v6 as the current occupancy remasurement, which stands. This v5 remasures that DR-114 citation stale after {DA_D}. Not this artifact's version number.")
v['basedOn']=b
v['file08Pin']=O([('path',F08),('sha256',sha(F08))]); v['head']=HEAD; v['requiredNowUnchanged']=28; v['file08StatusToken']='OPEN'
v['leftoverDesignOpenStanding']=(f"The live DR-G12 token is OPEN. leftover-design of unnamed G12 initial states is stale as a naming claim after the twelve doctor FC INPUT/initial-state corpora and {DAJ} ({DA_D}). leftover-design of doctor fixture implementations remains. DR-114 leftovers remain on {DAJ} ({DA_D}) and are not stolen. DR-114 is not SATISFIED.")
v['namedCorpusNotAuthored']=v4['namedCorpusNotAuthored']
ri=O(v4['recordedInputs']); ri[COORD]=sha(COORD); ri[F08]=sha(F08); ri['HEAD']=HEAD
for n in ['g12-leftover-join.v4.json','g12-leftover-join.v4.review-independent.claude2.json','g12-leftover-join.v4.review-independent.codex.json',f'doctor-actor-leftover-join.v{DA_V}.json',f'doctor-actor-leftover-join.v{DA_V}.review-independent.claude2.json',f'doctor-actor-leftover-join.v{DA_V}.review-independent.codex.json']: ri[P(n)]=sha(P(n))
v['recordedInputs']=ri
v['remeasurementClause']=(f"If a cited file moves in a way that is not append-only COORD growth or COORD heading hygiene, with file 08, leftover-join.v4, leftover-join.v3, occupancy v6, occupancy v4, doctor-actor leftover-join v{DA_V}, doctor-actor leftover-join v11, and this draft unmoved, remasure before recording. recordedInputs.HEAD must equal the top-level head. This join does not unwrite D-086 or D-167 through {LASTD}. Frozen leftover-join.v4 of this lineage remains a historical measurement recorded at {OWN_D} after this successor is recorded. Frozen leftover-join.v3 of this lineage remains a historical measurement recorded at {V3_D}. Frozen occupancy v6 remains current G12 occupancy remasurement. Frozen {DAJ} remains current DR-114 ROW leftover-join.")
v['liveGateOwners']=v4['liveGateOwners']
obs=[]
for o in v4['obligations']:
    o=O(o); i=o['id']
    if i=='OBL-G12-INPUT-CORPUS': rq(o,'reason',f'{DAJ_OLD} ({OLD_DA_D}) measures OBL-DOCTOR-FC-INPUT-CORPUS leftoverDesign false on DR-114.',f'{DAJ} ({DA_D}) measures OBL-DOCTOR-FC-INPUT-CORPUS leftoverDesign false on DR-114, as {DAJ_OLD} ({OLD_DA_D}) did.')
    if i=='OBL-DR114-LEFTOVER-NOT-STOLEN':
        rq(o,'reason',f'{DAJ_OLD} ({OLD_DA_D}) still measures',f'{DAJ} ({DA_D}) still measures')
        rq(o,'reason','OBL-JOIN-FX-EXECUTION is leftoverDesign false on v11.',f'OBL-JOIN-FX-EXECUTION is leftoverDesign false on {DAJ}.')
    obs.append(o)
v['obligations']=obs; v['summary']=v4['summary']
v['doesNotCloseLeftoverAlone']=(f"This candidate does not SATISFY DR-114 and does not make G12 QUALIFIED. OBL-DOCTOR-FX-AUTHORING remains leftover-design. OBL-G12-INPUT-CORPUS initial-state naming is measured closed. DR-114 leftovers remain on {DAJ} ({DA_D}) and are not stolen. The file 08 token stays OPEN. Not SATISFIED.")
v['proposedLaterWork']=list(v4['proposedLaterWork'])
dn=list(v4['doesNot'])
i3=dn.index('Does not record leftover-join.v3 as current after this successor is recorded.')
dn[i3:i3+1]=["Does not record leftover-join.v4 as current after this successor is recorded.","Does not record leftover-join.v3 as current G12 leftover-join."]
dn.append(f"Does not record {DAJ_OLD} as current DR-114 leftover-join.")
v['doesNot']=dn
pr=O(v4['parentReview']); assert pr['sha256']==sha(pr['path']) and pr['codex']['sha256']==sha(pr['codex']['path'])
rq(pr,'role','not leftover-join.v3.','not leftover-join.v4.'); v['parentReview']=pr
assert list(v)==list(v4), 'top-level key order changed'
out=sys.argv[1] if len(sys.argv)>1 else '/private/tmp/claude-501/-Users-sb-code-opensip-ai-opensip/dcbad0ae-7fad-4c78-89e7-e93d989f5501/scratchpad/g12-leftover-join.v5.json'
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
QUAL=r'(leftover-join\.|leftover-join |occupancy |Occupancy |This |Frozen |frozen |remasurement |naming |harness\.[^ ]*\.)$'
for p,s in walk(d):
    if p.endswith('.path') or p.startswith('.recordedInputs'): continue
    for m in re.finditer(r'[Tt]his v\d+',s):
        if m.group(0).lower()!='this v5': hits.append((p,'SPEAKER',s[max(0,m.start()-50):m.end()+40]))
    for m in re.finditer(r'(?<![\w.\-/])v\d+\b',s):
        if not re.search(QUAL,s[max(0,m.start()-26):m.start()]) and m.group(0)!='v5': hits.append((p,'BARE',s[max(0,m.start()-60):m.end()+30]))
    if re.search(r'\bG12 v\d',s): hits.append((p,'BARE-G12',s))
bad=[k for k,s_ in ri.items() if k!='HEAD' and os.path.exists(k) and sha(k)!=s_]
assert d['recordedInputs']['HEAD']==d['head']
print('wrote',out,len(raw),'bytes; HEAD',HEAD[:10],'; last heading',LASTD,'; doctor-actor v',DA_V,DA_D,'; own pred',OWN_D,'; digest mismatches',bad); print('audit hits:',len(hits)); [print('  ',h) for h in hits]
