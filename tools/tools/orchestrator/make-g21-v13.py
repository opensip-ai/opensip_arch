#!/usr/bin/env python3
"""g21-leftover-join.v13 (G21 GATE join) from frozen leftover-join.v12: refresh the DR-114 ROW citation from doctor-actor leftover-join.v11 (D-170) to doctor-actor leftover-join.v12 (D-285); occupancy v4 (D-218) unchanged; leftoverDesign [OBL-G21-FX-AUTHORING] unchanged; re-pin live inputs."""
import json, collections, hashlib, subprocess, re, sys, os, datetime
REPO='/Users/sb/code/opensip-ai/opensip'; os.chdir(REPO); O=collections.OrderedDict
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
def git(*a): return subprocess.check_output(['git',*a],text=True).strip()
HEAD=git('rev-parse','HEAD'); COORD='docs/coop/COORDINATOR-DECISIONS.md'; F08='docs/v2/architecture/08-decision-and-readiness-register.md'
assert hashlib.sha256(subprocess.check_output(['git','show',f'HEAD:{COORD}'])).hexdigest()==sha(COORD), 'COORD working tree differs from HEAD'
assert hashlib.sha256(subprocess.check_output(['git','show',f'HEAD:{F08}'])).hexdigest()==sha(F08), 'file 08 working tree differs from HEAD'
heads=[l for l in open(COORD) if l.startswith('## D-')]; LASTD=re.match(r'## (D-\d+)',heads[-1]).group(1)
A='docs/coop/artifacts/'; P=lambda n:A+n
def commit_of(d):
    for line in subprocess.check_output(['git','log','--format=%H %s'],text=True).splitlines():
        if re.match(rf'^[0-9a-f]+ {d}: ',line): return line.split()[0]
    raise SystemExit('no commit for '+d)
def current_recorded(stem):
    best=None
    for h in heads:
        if 'CONTESTED' in h: continue
        m=re.match(rf'## (D-\d+) — Record {stem}[- ]leftover-join\.v(\d+) ',h)
        if m and (best is None or int(m.group(2))>best[0]): best=(int(m.group(2)),m.group(1))
    return best
def recording_of(stem,ver):
    for h in heads:
        if 'CONTESTED' in h: continue
        m=re.match(rf'## (D-\d+) — Record {stem}[- ]leftover-join\.v{ver} ',h)
        if m: return m.group(1)
    raise SystemExit(f'no recording heading for {stem} leftover-join.v{ver}')
def heading_of(d):
    hs=[h for h in heads if h.startswith(f'## {d} ')]; assert len(hs)==1,(d,hs); return hs[0].rstrip('\n')
# --- byte-checked record facts -------------------------------------------------------------
DA_V,DA_D=current_recorded('doctor-actor'); assert (DA_V,DA_D)==(12,'D-285'),(DA_V,DA_D)
DA_OLD_V=11; DA_OLD_D=recording_of('doctor-actor',DA_OLD_V); assert DA_OLD_D=='D-170',DA_OLD_D
OWN_D=recording_of('g21',12); assert OWN_D=='D-248',OWN_D
assert recording_of('g21',11)=='D-246' and recording_of('g21',9)=='D-244' and recording_of('g21',7)=='D-242' and recording_of('g21',4)=='D-196'
G21_CUR=current_recorded('g21'); assert G21_CUR==(12,'D-248'),G21_CUR
OCC_D='D-218'; assert heading_of(OCC_D).startswith('## D-218 — Record harness.DR-G21.component-failure-containment.v4 ')
assert heading_of('D-247').startswith('## D-247 — Record g21-fixture-corpus.v8 as G21 leftover-design per-D-002-platform copies of two CC-5 payloads')
assert int(LASTD[2:])>=287, LASTD
v12=json.load(open(P('g21-leftover-join.v12.json')),object_pairs_hook=O)
assert v12['artifact']=='g21-leftover-join.v12' and v12['version']==12 and v12['registerRow']=='DR-G21'
assert 'lands' not in v12 and len(v12['findingDisposition'])==1 and v12['findingDisposition'][0]['id']=='G21LJ-V3-SF1'
OCC=v12['basedOn']['occupancyV4']['path']; assert OCC==P('harness.DR-G21.component-failure-containment.v4.json') and sha(OCC)==v12['basedOn']['occupancyV4']['sha256']
assert v12['basedOn']['occupancyV4']['recording']==OCC_D and 'commit' not in v12['basedOn']['d218']
assert v12['basedOn']['doctorJoinV11']['recording']==DA_OLD_D and sha(P('doctor-actor-leftover-join.v11.json'))==v12['basedOn']['doctorJoinV11']['sha256']
assert v12['basedOn']['d247']['role']=='Last live heading at dispatch. Last-heading custody only.' and v12['basedOn']['d247']['commit']==commit_of('D-247')
# D-248 entry pins the frozen predecessor digest; the file must still match it
_i=[i for i,l in enumerate(open(COORD)) if l.startswith(f'## {OWN_D} ')][0]; d248_body=''.join(open(COORD).readlines()[_i:_i+40])
assert sha(P('g21-leftover-join.v12.json')) in d248_body, f'{OWN_D} entry does not pin the frozen g21-leftover-join.v12.json digest'
# DR-G21 row: named by D-086, live token OPEN
row=[l for l in open(F08) if l.startswith('| DR-G21 ')][0]; assert '(D-086;' in row and row.rstrip().endswith('| OPEN |'),row
def rev(path):
    d=json.load(open(path)); vd=d.get('verdict'); mf=d.get('mustFixCount'); sf=d.get('shouldFixCount')
    if not isinstance(mf,int): mf=len(d.get('mustFix') or []) if isinstance(d.get('mustFix'),list) else (d.get('mustFix') if isinstance(d.get('mustFix'),int) else 0)
    if not isinstance(sf,int): sf=len(d.get('shouldFix') or []) if isinstance(d.get('shouldFix'),list) else (d.get('shouldFix') if isinstance(d.get('shouldFix'),int) else 0)
    assert vd=='ACCEPT' and mf==0 and sf==0,(path,vd,mf,sf); return 'ACCEPT 0/0'
def pin(name, recording, role):
    stem=name[:-5]; c=P(stem+'.review-independent.claude2.json'); x=P(stem+'.review-independent.codex.json')
    return O([('path',P(name)),('sha256',sha(P(name))),('recording',recording),('reviews',O([('claude',O([('path',c),('sha256',sha(c)),('verdict',rev(c))])),('codex',O([('path',x),('sha256',sha(x)),('verdict',rev(x))]))])),('role',role)])
def cust(d,role): return O([('recording',d),('commit',commit_of(d)),('role',role)])
# leftoverDesign set on the DR-114 ROW join: identical between doctor-actor leftover-join.v11 and leftover-join.v12
DA12=json.load(open(P(f'doctor-actor-leftover-join.v{DA_V}.json'))); DA11=json.load(open(P(f'doctor-actor-leftover-join.v{DA_OLD_V}.json')))
DR114_LD=["OBL-DOCTOR-FX-AUTHORING","OBL-JOIN-FX-AUTHORING","OBL-FC-C1","OBL-BLK-1","OBL-BLK-2","OBL-BLK-3","OBL-BLK-4"]
assert DA12['summary']['leftoverDesign']==DR114_LD==DA11['summary']['leftoverDesign']
assert [o['id'] for o in DA12['obligations'] if o.get('leftoverDesign') is True]==DR114_LD
assert [o['id'] for o in DA11['obligations'] if o.get('leftoverDesign') is True]==DR114_LD
def _ld(j,i): return [o for o in j['obligations'] if o['id']==i][0]['leftoverDesign']
assert _ld(DA12,'OBL-JOIN-FX-EXECUTION') is False and _ld(DA11,'OBL-JOIN-FX-EXECUTION') is False
assert DA12['registerRow']=='DR-114' and DA12['artifact']==f'doctor-actor-leftover-join.v{DA_V}'
assert v12['summary']['leftoverDesign']==["OBL-G21-FX-AUTHORING"]==v12['leftoverDesignRemainingOnG21'] and v12['leftoverDesignClosedIfAcceptedAndRecorded']==[]
OCCJ=json.load(open(OCC)); assert OCCJ.get('namedCorpusWhenFixturesExist')==v12['namedCorpusWhenFixturesExist'], 'occupancy v4 namedCorpusWhenFixturesExist moved'
LD='[OBL-G21-FX-AUTHORING]'; DIFF='doctor-actor leftover-join and g21 leftover-join are different lineages; their version numbers are unrelated.'
DAJ=f'doctor-actor leftover-join.v{DA_V}'; DAJ_OLD=f'doctor-actor leftover-join.v{DA_OLD_V}'
DR114_TXT='OBL-DOCTOR-FX-AUTHORING, OBL-JOIN-FX-AUTHORING, OBL-FC-C1, and OBL-BLK-1..4'
def rq(c,k,old,new):
    cur=c[k]; assert old in cur,(k,old); c[k]=cur.replace(old,new)
# --- successor -----------------------------------------------------------------------------
v=O()
v['artifact']='g21-leftover-join.v13'; v['version']=13; v['date']=datetime.date.today().isoformat()
v['documentClass']=v12['documentClass']; v['registerRow']='DR-G21'
v['registerRowNote']=(f"registerRow is the already-named gate DR-G21 because this join remasures leftover-design of G21 after g21-fixture-corpus.v8 (D-247) and after {DAJ} ({DA_D}). file08StatusToken is DR-G21's own live token (OPEN). leftover-join.v12 remains frozen and is not current after this successor is recorded. leftover-join.v11 (D-246) remains frozen and is not current. leftover-join.v10 remains frozen and is not current. leftover-join.v9 (D-244) remains frozen and is not current. leftover-join.v7 (D-242) remains frozen and is not current. leftover-join.v4 (D-196) remains frozen and is not current. leftover-join.v5 and leftover-join.v6 remain split. leftover-join.v8 remains Dual REJECT 0/1 G21LJ-V8-SF1. leftover-join.v10 remains split Claude REJECT 0/1 G21LJ-V10-SF1 / Codex ACCEPT 0/0. D-086 named DR-G21 as required-now. {DAJ} remains the current DR-114 ROW leftover-join ({DA_D}; registerRow DR-114). {DAJ_OLD} is not current. This file is the GATE leftover-join whose registerRow is DR-G21. This join does not retarget DR-114 leftover, does not reopen DR-102 SATISFIED, does not close leftover-design of OBL-G21-FX-AUTHORING, does not invent a D-002 platform list, does not claim CC-5 fully authored, and does not SATISFY DR-114 or DR-133. "+DIFF)
for k in ['status','reviewStatus','sealRecommendation','binds']: v[k]=v12[k]
v['authorityClaim']=(f"This artifact PROPOSES an execution-remainder join successor for G21 leftovers. v13 remasures leftover-join.v12 after {DAJ} ({DA_D}). leftover-join.v12 remains frozen. leftoverDesign remains {LD} for remaining unauthored G21 classes, including remaining CC-5 injections. Occupancy v4 ({OCC_D}) remains the current G21 occupancy remasurement. leftover-design of NT-1 and NT-2 implementations, of per-D-002-platform copies of those implementations, of the two CC-5 prefix injections at g21-fixture-corpus.v7 (D-245), and of per-D-002-platform copies of those two CC-5 payloads at g21-fixture-corpus.v8 (D-247) remains stale as an authoring claim, as leftover-join.v12 measured. Frozen corpus v3, corpus v4, corpus v5, and corpus v6 remain split and are not current. It does not SATISFY DR-114. It does not SATISFY DR-133. It does not reopen DR-102 SATISFIED. It does not close leftover-design of OBL-G21-FX-AUTHORING. It does not invent a D-002 platform list. It does not claim CC-5 fully authored. It does not classify non-object top level as CC-5. It does not steal DR-114 leftover. It does not add a DR-G* row. It does not change live required-now 28. It does not execute fixtures. It lands no new finding. It applies nothing and does not authorize docs/v2/implementation/.")
v['purpose']=(f"Remasure leftover-join.v12 against live HEAD after {DAJ} ({DA_D}). Cite {DAJ} as the current DR-114 leftover-join; leftover-join.v12 cited {DAJ_OLD}. Cite occupancy v4 ({OCC_D}) as the current occupancy remasurement, as leftover-join.v12 did. Preserve leftoverDesign {LD} for remaining unauthored G21 classes, including remaining CC-5 injections. Frozen leftover-join.v12 stays unmoved. Do not SATISFY DR-114. Do not SATISFY DR-133. Do not reopen DR-102 SATISFIED. Do not invent a D-002 platform list. Do not claim CC-5 fully authored. Do not steal DR-114 leftover.")
b=O()
for k,val in v12['basedOn'].items(): b[k]=O(val) if isinstance(val,dict) else val
rq(b['doctorJoinV6'],'role',f"Not current. Current DR-114 remainder is {DAJ_OLD} ({DA_OLD_D}).",f"Not current. {DAJ_OLD} was current at {DA_OLD_D}; not current after {DA_D}. Current DR-114 ROW leftover-join is {DAJ} ({DA_D}).")
b['doctorJoinV11']['role']=(f"Predecessor ROW leftover-join. Historical. Dual ACCEPT 0/0. Recorded as current DR-114 leftover-join at {DA_OLD_D}. Measured {DR114_TXT} leftoverDesign true on DR-114; OBL-JOIN-FX-EXECUTION leftoverDesign false there. {DAJ_OLD} was current at {DA_OLD_D}; not current after {DA_D}. Current DR-114 ROW leftover-join is {DAJ} ({DA_D}). This GATE leftover-join does not steal that remainder. "+DIFF+" Not this artifact's version number.")
rq(b['predecessorV4'],'role','Landed in this lineage at v4.','Landed in this lineage at leftover-join.v4.')
rq(b['predecessorV7'],'role','Landed in this lineage at v7.','Landed in this lineage at leftover-join.v7.')
rq(b['predecessorV9'],'role','Landed in this lineage at v9.','Landed in this lineage at leftover-join.v9.')
rq(b['predecessorV11'],'role','This v12 remasures leftover-design of those copies stale after corpus v8 (D-247). Landed in this lineage at v11.','leftover-join.v12 remasured leftover-design of those copies stale after corpus v8 (D-247). Landed in this lineage at leftover-join.v11.')
rq(b['corpusV7'],'role','Frozen corpus v3 through v6 remain split and are not current.','Frozen corpus v3 through corpus v6 remain split and are not current.')
rq(b['corpusV8'],'role','Frozen corpus v3 through v6 remain split and are not current.','Frozen corpus v3 through corpus v6 remain split and are not current.')
# D-247 was last-heading custody at leftover-join.v12; it is the corpus v8 recording and is kept as recording custody (heading byte-checked above).
b['d247']['role']="Recorded g21-fixture-corpus.v8 as G21 leftover-design per-D-002-platform copies of the two CC-5 payloads. Not last-heading. Not this artifact's version number."
b['d'+OWN_D[2:]]=cust(OWN_D,"Recorded leftover-join.v12 as current G21 leftover-join. Not last-heading. Not this artifact's version number.")
b['predecessorV12']=pin('g21-leftover-join.v12.json',OWN_D,f"Predecessor. Unmoved. Dual ACCEPT 0/0. Recorded as current G21 leftover-join at {OWN_D}. Cited {DAJ_OLD} as the current DR-114 leftover-join. This v13 remasures that citation stale after {DA_D}. Not this artifact's version number.")
b['d'+DA_D[2:]]=cust(DA_D,f"Recorded {DAJ} as current DR-114 leftover-join. Not last-heading. Not this artifact's version number.")
b['doctorJoinV'+str(DA_V)]=pin(f'doctor-actor-leftover-join.v{DA_V}.json',DA_D,f"Current DR-114 ROW leftover-join recorded at {DA_D}. leftoverDesign remains {DR114_TXT} (identical to {DAJ_OLD}). OBL-JOIN-FX-EXECUTION is leftoverDesign false on {DAJ}. This GATE leftover-join does not steal those leftovers. "+DIFF+" Not this artifact's version number.")
b['d'+LASTD[2:]]=cust(LASTD,"Last live heading at dispatch. Last-heading custody only.")
v['basedOn']=b
v['file08Pin']=O([('path',F08),('sha256',sha(F08))]); v['head']=HEAD; v['requiredNowUnchanged']=28; v['file08StatusToken']='OPEN'
lo=v12['leftoverDesignOpenStanding']
old_da=f"leftover-design of {DR114_TXT} remains on {DAJ_OLD} ({DA_OLD_D}) / DR-114. OBL-JOIN-FX-EXECUTION is leftoverDesign false on v11."
assert old_da in lo,'leftoverDesignOpenStanding DR-114 sentence moved'
v['leftoverDesignOpenStanding']=lo.replace(old_da,f"leftover-design of {DR114_TXT} remains on {DAJ} ({DA_D}) / DR-114. OBL-JOIN-FX-EXECUTION is leftoverDesign false on {DAJ}.")
v['leftoverDesignClosedIfAcceptedAndRecorded']=v12['leftoverDesignClosedIfAcceptedAndRecorded']
v['leftoverDesignRemainingOnG21']=v12['leftoverDesignRemainingOnG21']
v['namedCorpusWhenFixturesExist']=v12['namedCorpusWhenFixturesExist']
ri=O(v12['recordedInputs']); ri[COORD]=sha(COORD); ri[F08]=sha(F08); ri['HEAD']=HEAD
for n in ['g21-leftover-join.v12.json','g21-leftover-join.v12.review-independent.claude2.json','g21-leftover-join.v12.review-independent.codex.json',f'doctor-actor-leftover-join.v{DA_V}.json',f'doctor-actor-leftover-join.v{DA_V}.review-independent.claude2.json',f'doctor-actor-leftover-join.v{DA_V}.review-independent.codex.json']: ri[P(n)]=sha(P(n))
v['recordedInputs']=ri
v['remeasurementClause']=(f"If a cited file moves in a way that is not append-only COORD growth or COORD heading hygiene, with file 08, leftover-join.v1 through leftover-join.v12 of this lineage, occupancy v4, corpus v1, corpus v2, corpus v3 through corpus v6, corpus v7, corpus v8, the eight corpus v8 fixture files, {DAJ}, {DAJ_OLD}, and this draft unmoved, remasure before recording. recordedInputs.HEAD must equal the top-level head. This join does not unwrite D-086 or D-167 through {LASTD}. Frozen leftover-join.v12 of this lineage remains a historical measurement recorded at {OWN_D} after this successor is recorded. Frozen leftover-join.v11 of this lineage remains a historical measurement recorded at D-246. Frozen leftover-join.v10 of this lineage remains split Claude REJECT 0/1 G21LJ-V10-SF1 / Codex ACCEPT 0/0. Frozen leftover-join.v9 of this lineage remains a historical measurement recorded at D-244. Frozen leftover-join.v8 of this lineage remains dual REJECT 0/1 G21LJ-V8-SF1. Frozen leftover-join.v7 of this lineage remains a historical measurement recorded at D-242. Frozen corpus v3 through corpus v6 remain split. Frozen occupancy v4 remains current G21 occupancy remasurement. Frozen {DAJ} remains current DR-114 leftover-join.")
v['liveGateOwners']=v12['liveGateOwners']
obs=[]
for o in v12['obligations']:
    o=O(o); i=o['id']
    if i=='OBL-DR114-LEFTOVER-NOT-STOLEN':
        rq(o,'reason',f"{DAJ_OLD} ({DA_OLD_D}) still measures {DR114_TXT} leftoverDesign true on DR-114. OBL-JOIN-FX-EXECUTION is leftoverDesign false on v11.",f"{DAJ} ({DA_D}) still measures {DR114_TXT} leftoverDesign true on DR-114. OBL-JOIN-FX-EXECUTION is leftoverDesign false on {DAJ}.")
    obs.append(o)
v['obligations']=obs; v['summary']=v12['summary']
v['doesNotCloseLeftoverAlone']=v12['doesNotCloseLeftoverAlone']
v['proposedLaterWork']=list(v12['proposedLaterWork'])
dn=list(v12['doesNot']); _old="Does not record leftover-join.v11 as current after this successor is recorded."; assert _old in dn
dn=[("Does not record leftover-join.v11 as current G21 leftover-join." if x==_old else x) for x in dn]
v['doesNot']=dn+["Does not record leftover-join.v12 as current after this successor is recorded.",f"Does not record {DAJ_OLD} as current DR-114 leftover-join.","Does not land or re-land any finding."]
fd=[]
for f in v12['findingDisposition']:
    f=O(f); assert f['id']=='G21LJ-V3-SF1' and f['disposition']=='ACCEPTED' and f['landed']=="Landed in this lineage at v4. Unmoved. Not this artifact's version number."
    f['disposition']='ACCEPTED. Landed in this lineage at leftover-join.v4. This v13 does not re-land it.'
    f['landed']="Landed in this lineage at leftover-join.v4. Unmoved. Not this artifact's version number."
    fd.append(f)
v['findingDisposition']=fd
pr=O(v12['parentReview']); assert pr['path']==P('harness.DR-G21.component-failure-containment.v4.review-independent.claude2.json') and sha(pr['path'])==pr['sha256'] and sha(pr['codex']['path'])==pr['codex']['sha256']
assert pr['role']=="Independent dual ACCEPT 0/0 of the current occupancy of the already-named identifier. Naming parent is D-145 / naming v6, not leftover-join.v11."
pr['role']="Independent dual ACCEPT 0/0 of the current occupancy of the already-named identifier. Naming parent is naming v6 (D-145), not leftover-join.v12. D-086 named DR-G21."
v['parentReview']=pr
af=O(v12['appliesFindingsOf']); assert list(af.keys())==['idCollisionNote','v5','v6','v8','v10']
assert af['idCollisionNote']=="Claude v5 used G21LJ-V5-M1 and G21LJ-V5-SF1, landed at v6. Claude v6 used G21LJ-V6-SF1, landed at v7. Claude v8 and Codex v8 used G21LJ-V8-SF1 as one class, landed at v9. Claude v10 used G21LJ-V10-SF1, landed at v11. This v12 remasures leftover-design after corpus v8. It does not reopen G21LJ-V10-SF1."
af['idCollisionNote']=(f"Claude's review of leftover-join.v5 used G21LJ-V5-M1 and G21LJ-V5-SF1, landed at leftover-join.v6. Claude's review of leftover-join.v6 used G21LJ-V6-SF1, landed at leftover-join.v7. Claude's and Codex's reviews of leftover-join.v8 used G21LJ-V8-SF1 as one class, landed at leftover-join.v9. Claude's review of leftover-join.v10 used G21LJ-V10-SF1, landed at leftover-join.v11. leftover-join.v12 remasured leftover-design after corpus v8 (D-247). This v13 remasures the DR-114 ROW citation after {DAJ} ({DA_D}). This v13 does not reopen G21LJ-V10-SF1.")
def af_edit(key,idx,old,new):
    e=O(af[key][idx]); rq(e,'landed',old,new); af[key]=list(af[key]); af[key][idx]=e
af_edit('v5',0,"ACCEPTED at v6 as leftoverDesign scoped to per-D-002-platform copies of NT-1/NT-2.","ACCEPTED at leftover-join.v6 as leftoverDesign scoped to per-D-002-platform copies of NT-1/NT-2.")
af_edit('v5',0,"This v12 remasures that CC-5-copy remainder stale after corpus v8 (D-247).","leftover-join.v12 remasured that CC-5-copy remainder stale after corpus v8 (D-247). This v13 carries that measurement.")
af_edit('v6',0,"Landed at v7 against corpus v1 authoredCatalog.executionRemains.","Landed at leftover-join.v7 against corpus v1 authoredCatalog.executionRemains.")
af_edit('v6',0,"This v12 recites corpus v8 authoredCatalog.executionRemains as candidate-buffer digest, subsequent-session view, host-projection goldens, and EV-5 diagnostic/audit bytes.","leftover-join.v12 recited corpus v8 authoredCatalog.executionRemains as candidate-buffer digest, subsequent-session view, host-projection goldens, and EV-5 diagnostic/audit bytes; this v13 carries that recital.")
af_edit('v8',0,"Landed in this lineage at v9.","Landed in this lineage at leftover-join.v9.")
af_edit('v10',0,"Landed in this lineage at v11.","Landed in this lineage at leftover-join.v11.")
af_edit('v10',0,"This v12 recites corpus v8 authoredCatalog.executionRemains including EV-5 diagnostic/audit bytes.","leftover-join.v12 recited corpus v8 authoredCatalog.executionRemains including EV-5 diagnostic/audit bytes; this v13 carries that recital.")
v['appliesFindingsOf']=af
assert list(v.keys())==list(v12.keys()), 'top-level field order drifted from the predecessor'
# --- write ---------------------------------------------------------------------------------
out=sys.argv[1] if len(sys.argv)>1 else '/private/tmp/claude-501/-Users-sb-code-opensip-ai-opensip/dcbad0ae-7fad-4c78-89e7-e93d989f5501/scratchpad/g21-leftover-join.v13.json'
raw=json.dumps(v,indent=2,ensure_ascii=False)+'\n'
json.loads(raw,object_pairs_hook=lambda ps: (_ for _ in ()).throw(SystemExit('dup keys')) if len([k for k,_ in ps])!=len(set(k for k,_ in ps)) else dict(ps))
open(out,'w').write(raw)
# --- audit ---------------------------------------------------------------------------------
d=json.loads(raw); hits=[]
def walk(x,p=''):
    if isinstance(x,dict):
        for k,vv in x.items(): yield from walk(vv,p+'.'+k)
    elif isinstance(x,list):
        for i,vv in enumerate(x): yield from walk(vv,p+f'[{i}]')
    elif isinstance(x,str): yield p,x
QUAL=r'(leftover-join\.|leftover-join |corpus |occupancy |Occupancy |contract\.|naming |catalog |this |This |at |Frozen |frozen |remasurement |G21 |harness |harness\.[^ ]*\.)$'
for p,s in walk(d):
    if p.endswith('.path') or p.startswith('.recordedInputs'): continue
    for m in re.finditer(r'[Tt]his v\d+',s):
        if m.group(0).lower()!='this v13': hits.append((p,'SPEAKER',s[max(0,m.start()-50):m.end()+40]))
    for m in re.finditer(r'(?<![\w.\-/])v\d+\b',s):
        if not re.search(QUAL,s[max(0,m.start()-26):m.start()]) and m.group(0)!='v13': hits.append((p,'BARE',s[max(0,m.start()-60):m.end()+30]))
    if re.search(r'\b(unchanged|identical|carried unchanged)\b',s) and 'identical to '+DAJ_OLD not in s and 'requiredNowUnchanged' not in p: hits.append((p,'CLAIM',s[:120]))
bad=[k for k,s_ in ri.items() if k!='HEAD' and os.path.exists(k) and sha(k)!=s_]
assert ri['HEAD']==d['head'] and bad==[], bad
print('wrote',out,len(raw),'bytes; HEAD',HEAD[:10],'; last heading',LASTD,'; doctor-actor v',DA_V,DA_D,'; own predecessor recording',OWN_D,'; digest mismatches',bad); print('audit hits:',len(hits)); [print('  ',h) for h in hits]
