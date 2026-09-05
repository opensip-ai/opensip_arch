#!/usr/bin/env python3
"""g19-leftover-join.v5 (G19 GATE join) from frozen leftover-join.v4: refresh the DR-124 ROW citation from state-class leftover-join.v3 (D-183) to state-class leftover-join.v4 (D-284); occupancy v2 (D-222) unchanged; re-pin live inputs."""
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
# --- byte-checked record facts -------------------------------------------------------------
SC_V,SC_D=current_recorded('state-class'); assert (SC_V,SC_D)==(4,'D-284'),(SC_V,SC_D)
SC_OLD_V=3; SC_OLD_D=recording_of('state-class',SC_OLD_V); assert SC_OLD_D=='D-183',SC_OLD_D
OWN_D=recording_of('g19',4); assert OWN_D=='D-256',OWN_D
assert recording_of('g19',3)=='D-194'
G19_CUR=current_recorded('g19'); assert G19_CUR==(4,'D-256'),G19_CUR
OCC_D='D-222'; assert any(re.match(r'## D-222 — Record harness\.DR-G19\.state-class-authority\.preview-classes\.v2 ',h) for h in heads)
assert LASTD=='D-287' or int(LASTD[2:])>287, LASTD
v4=json.load(open(P('g19-leftover-join.v4.json')),object_pairs_hook=O)
assert v4['artifact']=='g19-leftover-join.v4' and v4['version']==4 and v4['registerRow']=='DR-G19'
OCC=v4['basedOn']['occupancyV2']['path']; assert OCC==P('harness.DR-G19.state-class-authority.preview-classes.v2.json') and sha(OCC)==v4['basedOn']['occupancyV2']['sha256']
assert v4['basedOn']['occupancyV2']['recording']==OCC_D and v4['basedOn']['d222']['commit']==commit_of(OCC_D)
assert v4['basedOn']['stateClassJoinV3']['recording']==SC_OLD_D and sha(P('state-class-leftover-join.v3.json'))==v4['basedOn']['stateClassJoinV3']['sha256']
assert 'findingDisposition' not in v4 and 'lands' not in v4
# D-256 entry pins the frozen predecessor digest; the file must still match it
d256_body=''.join(open(COORD).readlines()[[i for i,l in enumerate(open(COORD)) if l.startswith('## D-256 ')][0]:][:40])
assert sha(P('g19-leftover-join.v4.json')) in d256_body, 'D-256 entry does not pin the frozen g19-leftover-join.v4.json digest'
# DR-G19 row: named by D-086, live token OPEN
row=[l for l in open(F08) if l.startswith('| DR-G19 ')][0]; assert '(D-086;' in row and row.rstrip().endswith('| OPEN |'),row
def rev(path):
    d=json.load(open(path)); vd=d.get('verdict'); mf=d.get('mustFixCount'); sf=d.get('shouldFixCount')
    if not isinstance(mf,int): mf=len(d.get('mustFix') or []) if isinstance(d.get('mustFix'),list) else (d.get('mustFix') if isinstance(d.get('mustFix'),int) else 0)
    if not isinstance(sf,int): sf=len(d.get('shouldFix') or []) if isinstance(d.get('shouldFix'),list) else (d.get('shouldFix') if isinstance(d.get('shouldFix'),int) else 0)
    assert vd=='ACCEPT' and mf==0 and sf==0,(path,vd,mf,sf); return 'ACCEPT 0/0'
def pin(name, recording, role):
    stem=name[:-5]; c=P(stem+'.review-independent.claude2.json'); x=P(stem+'.review-independent.codex.json')
    return O([('path',P(name)),('sha256',sha(P(name))),('recording',recording),('reviews',O([('claude',O([('path',c),('sha256',sha(c)),('verdict',rev(c))])),('codex',O([('path',x),('sha256',sha(x)),('verdict',rev(x))]))])),('role',role)])
def cust(d,role): return O([('recording',d),('commit',commit_of(d)),('role',role)])
# leftoverDesign set on the DR-124 ROW join: identical between state-class leftover-join.v3 and leftover-join.v4
SC4=json.load(open(P(f'state-class-leftover-join.v{SC_V}.json'))); SC3=json.load(open(P('state-class-leftover-join.v3.json')))
DR124_LD=["OBL-G19-FX-AUTHORING","OBL-GRANT-JOURNAL","OBL-INHERIT-BLOCKED","OBL-MONOTONIC"]
assert SC4['summary']['leftoverDesign']==DR124_LD==SC3['summary']['leftoverDesign']
assert [o['id'] for o in SC4['obligations'] if o.get('leftoverDesign') is True]==DR124_LD
assert [o['id'] for o in SC3['obligations'] if o.get('leftoverDesign') is True]==DR124_LD
assert SC4['registerRow']=='DR-124' and SC4['artifact']==f'state-class-leftover-join.v{SC_V}'
assert v4['summary']['leftoverDesign']==["OBL-G19-FX-AUTHORING"]
OCCJ=json.load(open(OCC)); assert OCCJ.get('namedCorpusNotAuthored')==v4['namedCorpusNotAuthored'], 'occupancy v2 namedCorpusNotAuthored moved'
LD='[OBL-G19-FX-AUTHORING]'; DIFF='state-class leftover-join and g19 leftover-join are different lineages; their version numbers are unrelated.'
SCJ=f'state-class leftover-join.v{SC_V}'; SCJ_OLD=f'state-class leftover-join.v{SC_OLD_V}'
DR124_TXT='OBL-G19-FX-AUTHORING, OBL-GRANT-JOURNAL, OBL-INHERIT-BLOCKED, and OBL-MONOTONIC'
def rq(c,k,old,new):
    cur=c[k]; assert old in cur,(k,old); c[k]=cur.replace(old,new)
# --- successor -----------------------------------------------------------------------------
v=O()
v['artifact']='g19-leftover-join.v5'; v['version']=5; v['date']=datetime.date.today().isoformat()
v['documentClass']=v4['documentClass']; v['registerRow']='DR-G19'
v['registerRowNote']=(f"registerRow is the already-named gate DR-G19 because this join remasures leftover-design of G19 after occupancy v2 ({OCC_D}) and after {SCJ} ({SC_D}). file08StatusToken is DR-G19's own live token (OPEN). leftover-join.v4 remains frozen and is not current after this successor is recorded. leftover-join.v3 remains frozen and is not current. D-086 named DR-G19 as required-now. {SCJ} remains the current DR-124 ROW leftover-join ({SC_D}; registerRow DR-124). {SCJ_OLD} is not current. This join does not retarget DR-124 leftover, does not steal OBL-GRANT-JOURNAL, OBL-INHERIT-BLOCKED, or OBL-MONOTONIC, does not invent fixture bytes, does not take over G27, and does not SATISFY DR-124. "+DIFF)
for k in ['status','reviewStatus','sealRecommendation','binds']: v[k]=v4[k]
v['authorityClaim']=(f"This artifact PROPOSES an execution-remainder join successor for G19 leftovers. v5 remasures leftover-join.v4 after {SCJ} ({SC_D}). leftover-join.v4 remains frozen. leftoverDesign remains {LD}. Occupancy v2 ({OCC_D}) remains the current G19 occupancy remasurement. It does not SATISFY DR-124. It does not close leftover-design of OBL-G19-FX-AUTHORING. It does not invent fixture bytes. It does not invent a grant-journal. It does not steal DR-124 leftover. It does not take over G27. It does not add a DR-G* row. It does not change live required-now 28. It does not execute fixtures. It lands no new finding. It applies nothing and does not authorize docs/v2/implementation/.")
v['purpose']=(f"Remasure leftover-join.v4 against live HEAD after {SCJ} ({SC_D}). Cite {SCJ} as the current DR-124 leftover-join; leftover-join.v4 cited {SCJ_OLD}. Cite occupancy v2 ({OCC_D}) as the current occupancy remasurement, as leftover-join.v4 did. Preserve leftoverDesign {LD}. Frozen leftover-join.v4 stays unmoved. Do not SATISFY DR-124. Do not invent fixture bytes. Do not steal OBL-GRANT-JOURNAL, OBL-INHERIT-BLOCKED, or OBL-MONOTONIC. Do not take over G27.")
b=O()
for k,val in v4['basedOn'].items():
    if k=='d255': continue   # stale last-heading custody; replaced by the live last heading below
    b[k]=O(val) if isinstance(val,dict) else val
assert v4['basedOn']['d255']['role']=='Last live heading at dispatch. Last-heading custody only.'
rq(b['stateClassJoinV2'],'role',f"Not current. Current DR-124 ROW leftover-join is {SCJ_OLD} ({SC_OLD_D}).",f"Not current. {SCJ_OLD} was current at {SC_OLD_D}; not current after {SC_D}. Current DR-124 ROW leftover-join is {SCJ} ({SC_D}).")
b['stateClassJoinV3']['role']=(f"Predecessor ROW leftover-join. Historical. Dual ACCEPT 0/0. Recorded as current DR-124 leftover-join at {SC_OLD_D}. Measured {DR124_TXT} leftoverDesign true on DR-124. {SCJ_OLD} was current at {SC_OLD_D}; not current after {SC_D}. Current DR-124 ROW leftover-join is {SCJ} ({SC_D}). "+DIFF+" Not this artifact's version number.")
b['predecessorV3']['role']=(f"Predecessor of leftover-join.v4. Unmoved. Dual ACCEPT 0/0. Recorded as current G19 leftover-join at D-194; not current after {OWN_D}. Cited occupancy v1 as the specification. leftover-join.v4 remasured occupancy v1 stale after occupancy v2 ({OCC_D}). Occupancy v2 remains the current occupancy remasurement. Not this artifact's version number.")
b['d'+OWN_D[2:]]=cust(OWN_D,"Recorded leftover-join.v4 as current G19 leftover-join. Not last-heading. Not this artifact's version number.")
b['predecessorV4']=pin('g19-leftover-join.v4.json',OWN_D,f"Predecessor. Unmoved. Dual ACCEPT 0/0. Recorded as current G19 leftover-join at {OWN_D}. Cited {SCJ_OLD} as the current DR-124 leftover-join. This v5 remasures that citation stale after {SC_D}. Not this artifact's version number.")
b['d'+SC_D[2:]]=cust(SC_D,f"Recorded {SCJ} as current DR-124 leftover-join. Not last-heading. Not this artifact's version number.")
b['stateClassJoinV'+str(SC_V)]=pin(f'state-class-leftover-join.v{SC_V}.json',SC_D,f"Current DR-124 ROW leftover-join recorded at {SC_D}. leftoverDesign remains {DR124_TXT} (identical to {SCJ_OLD}). This GATE leftover-join does not steal those leftovers. "+DIFF+" Not this artifact's version number.")
b['d'+LASTD[2:]]=cust(LASTD,"Last live heading at dispatch. Last-heading custody only.")
v['basedOn']=b
v['file08Pin']=O([('path',F08),('sha256',sha(F08))]); v['head']=HEAD; v['requiredNowUnchanged']=28; v['file08StatusToken']='OPEN'
v['leftoverDesignOpenStanding']=(f"The live DR-G19 token is OPEN. leftover-design of unnamed G19 initial states is stale as a naming claim after g19-input-corpus.v2. leftover-design of G19 fixture implementations remains. leftover-design of OBL-GRANT-JOURNAL, OBL-INHERIT-BLOCKED, and OBL-MONOTONIC remains on {SCJ} ({SC_D}) / DR-124. A grant-journal is not invented. DR-124 leftover is not stolen. DR-124 is not SATISFIED.")
v['namedCorpusNotAuthored']=v4['namedCorpusNotAuthored']
ri=O(v4['recordedInputs']); ri[COORD]=sha(COORD); ri[F08]=sha(F08); ri['HEAD']=HEAD
for n in ['g19-leftover-join.v4.json','g19-leftover-join.v4.review-independent.claude2.json','g19-leftover-join.v4.review-independent.codex.json',f'state-class-leftover-join.v{SC_V}.json',f'state-class-leftover-join.v{SC_V}.review-independent.claude2.json',f'state-class-leftover-join.v{SC_V}.review-independent.codex.json']: ri[P(n)]=sha(P(n))
v['recordedInputs']=ri
v['remeasurementClause']=(f"If a cited file moves in a way that is not append-only COORD growth or COORD heading hygiene, with file 08, leftover-join.v4, leftover-join.v3, occupancy v2, occupancy v1, {SCJ}, {SCJ_OLD}, and this draft unmoved, remasure before recording. recordedInputs.HEAD must equal the top-level head. This join does not unwrite D-086 or D-167 through {LASTD}. Frozen leftover-join.v4 of this lineage remains a historical measurement recorded at {OWN_D} after this successor is recorded. Frozen leftover-join.v3 of this lineage remains a historical measurement recorded at D-194. Frozen occupancy v2 remains current G19 occupancy remasurement. Frozen {SCJ} remains current DR-124 leftover-join.")
v['liveGateOwners']=v4['liveGateOwners']
obs=[]
for o in v4['obligations']:
    o=O(o); i=o['id']
    if i=='OBL-DR124-LEFTOVER-NOT-STOLEN':
        rq(o,'reason',f"{SCJ_OLD} ({SC_OLD_D}) still measures {DR124_TXT} leftoverDesign true on DR-124.",f"{SCJ} ({SC_D}) still measures {DR124_TXT} leftoverDesign true on DR-124.")
    obs.append(o)
v['obligations']=obs; v['summary']=v4['summary']
v['doesNotCloseLeftoverAlone']=("This candidate does not SATISFY DR-124 and does not make G19 QUALIFIED. OBL-G19-FX-AUTHORING remains leftover-design. OBL-G19-INPUT-CORPUS initial-state naming is measured closed. A grant-journal is not invented. The file 08 token stays OPEN. Not SATISFIED.")
v['proposedLaterWork']=list(v4['proposedLaterWork'])
dn=list(v4['doesNot']); assert "Does not record leftover-join.v3 as current after this successor is recorded." in dn
dn=[x for x in dn if x!="Does not record leftover-join.v3 as current after this successor is recorded."]
v['doesNot']=dn+["Does not record leftover-join.v4 as current after this successor is recorded.","Does not record leftover-join.v3 as current G19 leftover-join.",f"Does not record {SCJ_OLD} as current DR-124 leftover-join.","Does not land or re-land any finding."]
pr=O(v4['parentReview']); assert pr['path']==P('harness.DR-G19.state-class-authority.preview-classes.v2.review-independent.claude2.json') and sha(pr['path'])==pr['sha256'] and sha(pr['codex']['path'])==pr['codex']['sha256']
rq(pr,'role','not leftover-join.v3.','not leftover-join.v4.'); v['parentReview']=pr
# --- write ---------------------------------------------------------------------------------
out=sys.argv[1] if len(sys.argv)>1 else '/private/tmp/claude-501/-Users-sb-code-opensip-ai-opensip/dcbad0ae-7fad-4c78-89e7-e93d989f5501/scratchpad/g19-leftover-join.v5.json'
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
QUAL=r'(leftover-join\.|leftover-join |corpus |occupancy |Occupancy |contract\.|naming |catalog |this |This |at |Frozen |frozen |remasurement |G19 |harness\.[^ ]*\.)$'
for p,s in walk(d):
    if p.endswith('.path') or p.startswith('.recordedInputs'): continue
    for m in re.finditer(r'[Tt]his v\d+',s):
        if m.group(0).lower()!='this v5': hits.append((p,'SPEAKER',s[max(0,m.start()-50):m.end()+40]))
    for m in re.finditer(r'(?<![\w.\-/])v\d+\b',s):
        if not re.search(QUAL,s[max(0,m.start()-26):m.start()]) and m.group(0)!='v5': hits.append((p,'BARE',s[max(0,m.start()-60):m.end()+30]))
    if re.search(r'\b(unchanged|identical|carried unchanged)\b',s) and 'identical to '+SCJ_OLD not in s and 'requiredNowUnchanged' not in p: hits.append((p,'CLAIM',s[:120]))
bad=[k for k,s_ in ri.items() if k!='HEAD' and os.path.exists(k) and sha(k)!=s_]
assert ri['HEAD']==d['head']
print('wrote',out,len(raw),'bytes; HEAD',HEAD[:10],'; last heading',LASTD,'; state-class v',SC_V,SC_D,'; own predecessor recording',OWN_D,'; digest mismatches',bad); print('audit hits:',len(hits)); [print('  ',h) for h in hits]
