#!/usr/bin/env python3
"""g15-leftover-join.v6 (G15 GATE join) from frozen leftover-join.v5: citation refresh of the DR-103 ROW leftover-join
(component-manifest leftover-join.v6, D-174 -> component-manifest leftover-join.v9, D-282). Occupancy v9 (D-214) unchanged.
packaging leftover-join.v4 (D-266) stays current DR-120 ROW leftover-join. leftoverDesign unchanged. Re-pin live inputs."""
import json, collections, hashlib, subprocess, re, sys, os, datetime
REPO='/Users/sb/code/opensip-ai/opensip'; os.chdir(REPO); O=collections.OrderedDict
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
def git(*a): return subprocess.check_output(['git',*a],text=True).strip()
HEAD=git('rev-parse','HEAD'); COORD='docs/coop/COORDINATOR-DECISIONS.md'; F08='docs/v2/architecture/08-decision-and-readiness-register.md'
assert hashlib.sha256(subprocess.check_output(['git','show',f'HEAD:{COORD}'])).hexdigest()==sha(COORD)
assert hashlib.sha256(subprocess.check_output(['git','show',f'HEAD:{F08}'])).hexdigest()==sha(F08)
COORD_TXT=open(COORD).read()
heads=[l for l in COORD_TXT.splitlines() if l.startswith('## D-')]; LASTD=re.match(r'## (D-\d+)',heads[-1]).group(1)
A='docs/coop/artifacts/'; P=lambda n:A+n
def commit_of(d):
    for line in subprocess.check_output(['git','log','--format=%H %s'],text=True).splitlines():
        if re.match(rf'^[0-9a-f]+ {d}: ',line): return line.split()[0]
    raise SystemExit('no commit for '+d)
def recorded(stem,ver,row_or_gate):
    """Return the D of the non-CONTESTED heading '## D-NNN — Record <stem>[- ]leftover-join.vN as <row> leftover remasurement'."""
    hits=[]
    for h in heads:
        if 'CONTESTED' in h: continue
        m=re.match(rf'## (D-\d+) — Record {stem}[- ]leftover-join\.v{ver} as {row_or_gate} leftover remasurement$',h)
        if m: hits.append(m.group(1))
    assert len(hits)==1,(stem,ver,hits); return hits[0]
def current_recorded(stem):
    best=None
    for h in heads:
        if 'CONTESTED' in h: continue
        m=re.match(rf'## (D-\d+) — Record {stem}[- ]leftover-join\.v(\d+) ',h)
        if m and (best is None or int(m.group(2))>best[0]): best=(int(m.group(2)),m.group(1))
    return best
def section(d):
    i=COORD_TXT.index(f'\n## {d} — '); j=COORD_TXT.find('\n## D-',i+1); return COORD_TXT[i:j if j>0 else None]
# ---- byte-checked record facts ----
CM_V,CM_D=current_recorded('component-manifest'); assert CM_V==9 and CM_D=='D-282',(CM_V,CM_D)
assert recorded('component-manifest',9,'DR-103')=='D-282'
PK_V,PK_D=current_recorded('packaging'); assert PK_V==4 and PK_D=='D-266',(PK_V,PK_D)
OWN_V,OWN_D=current_recorded('g15'); assert OWN_V==5 and OWN_D=='D-270',(OWN_V,OWN_D)
assert recorded('g15',5,'G15')=='D-270' and recorded('g15',4,'G15')=='D-261'
assert recorded('component-manifest',6,'DR-103')=='D-174'
OCC_D='D-214'; assert re.search(r'^## D-214 — Record harness\.DR-G15\.packaging-adapter-conformance\.v9 as G15 occupancy remasurement$',COORD_TXT,re.M)
assert int(LASTD[2:])>=287,LASTD
v5=json.load(open(P('g15-leftover-join.v5.json')),object_pairs_hook=O)
assert v5['artifact']=='g15-leftover-join.v5' and v5['version']==5 and v5['registerRow']=='DR-G15'
assert sha(P('g15-leftover-join.v5.json')) in section('D-270'), 'D-270 does not pin the frozen leftover-join.v5 bytes'
assert sha(P('component-manifest-leftover-join.v9.json')) in section('D-282'), 'D-282 does not pin the frozen component-manifest leftover-join.v9 bytes'
assert 'findingDisposition' not in v5 and 'lands' not in v5
assert v5['basedOn']['occupancyV9']['path']==P('harness.DR-G15.packaging-adapter-conformance.v9.json') and v5['basedOn']['occupancyV9']['recording']==OCC_D
assert v5['basedOn']['predecessorV4']['recording']=='D-261' and v5['basedOn']['cmljV6']['recording']=='D-174' and v5['basedOn']['packagingJoinV4']['recording']=='D-266'
assert v5['basedOn']['d269']['role']=='Last live heading at dispatch. Last-heading custody only.'
assert v5['head']==v5['recordedInputs']['HEAD']
for k,s_ in v5['recordedInputs'].items():
    if k not in ('HEAD',COORD,F08): assert sha(k)==s_,('predecessor pin moved',k)
DR103_SET=["OBL-WINDOWS-PATH","OBL-ENVELOPE-MISMATCH","OBL-UNICODE-NORM","OBL-OD-1","OBL-OD-2"]
cm6=json.load(open(P('component-manifest-leftover-join.v6.json'))); cm9=json.load(open(P('component-manifest-leftover-join.v9.json')))
assert cm6['summary']['leftoverDesign']==cm9['summary']['leftoverDesign']==DR103_SET
assert [o['id'] for o in cm9['obligations'] if o['leftoverDesign']]==DR103_SET and cm9['registerRow']=='DR-103'
pk4=json.load(open(P('packaging-leftover-join.v4.json'))); assert pk4['summary']['leftoverDesign']==["OBL-ADAPTER-IMPL","OBL-AT-FX-AUTHORING"] and pk4['registerRow']=='DR-120'
occ9=json.load(open(P('harness.DR-G15.packaging-adapter-conformance.v9.json'))); assert sha(P('harness.DR-G15.packaging-adapter-conformance.v9.json'))==v5['basedOn']['occupancyV9']['sha256']
assert v5['summary']['leftoverDesign']==['OBL-AT-FX-AUTHORING']
f08row=[l for l in open(F08) if l.startswith('| DR-G15 ')]; assert len(f08row)==1 and 'named: harness.DR-G15.packaging-adapter-conformance (D-086;' in f08row[0] and f08row[0].rstrip().endswith('| OPEN |')
def rev(path):
    d=json.load(open(path)); vv=d.get('verdict'); mf=d.get('mustFixCount'); sf=d.get('shouldFixCount')
    if not isinstance(mf,int): mf=len(d.get('mustFix') or []) if isinstance(d.get('mustFix'),list) else (d.get('mustFix') if isinstance(d.get('mustFix'),int) else 0)
    if not isinstance(sf,int): sf=len(d.get('shouldFix') or []) if isinstance(d.get('shouldFix'),list) else (d.get('shouldFix') if isinstance(d.get('shouldFix'),int) else 0)
    assert vv=='ACCEPT' and mf==0 and sf==0,(path,vv,mf,sf); return 'ACCEPT 0/0'
def pin(name, recording, role):
    stem=name[:-5]; c=P(stem+'.review-independent.claude2.json'); x=P(stem+'.review-independent.codex.json')
    return O([('path',P(name)),('sha256',sha(P(name))),('recording',recording),('reviews',O([('claude',O([('path',c),('sha256',sha(c)),('verdict',rev(c))])),('codex',O([('path',x),('sha256',sha(x)),('verdict',rev(x))]))])),('role',role)])
def cust(d,role): return O([('recording',d),('commit',commit_of(d)),('role',role)])
def rq(c,k,old,new):
    cur=c[k]; assert old in cur,(k,old); c[k]=cur.replace(old,new)
LD='[OBL-AT-FX-AUTHORING]'; DIFF='component-manifest leftover-join and g15 leftover-join are different lineages; their version numbers are unrelated.'
CMJ='component-manifest leftover-join.v9'; CMOLD='component-manifest leftover-join.v6'; FIVE='OBL-WINDOWS-PATH, OBL-ENVELOPE-MISMATCH, OBL-UNICODE-NORM, OBL-OD-1, and OBL-OD-2'
v=O()
v['artifact']='g15-leftover-join.v6'; v['version']=6; v['date']=datetime.date.today().isoformat()
v['documentClass']=v5['documentClass']; v['registerRow']='DR-G15'
v['registerRowNote']=(f"registerRow is the already-named gate DR-G15 because this join remasures leftover-design of G15 after occupancy v9 ({OCC_D}), after packaging leftover-join.v4 ({PK_D}), and after {CMJ} ({CM_D}). file08StatusToken is DR-G15's own live token (OPEN). leftover-join.v5 remains frozen and is not current after this successor is recorded. leftover-join.v4 remains frozen and is not current. D-086 named DR-G15 as required-now. packaging leftover-join.v4 remains the current DR-120 ROW leftover-join ({PK_D}; registerRow DR-120). {CMJ} remains the current DR-103 ROW leftover-join ({CM_D}; registerRow DR-103). {CMOLD} is not current after {CM_D}. leftoverNameNote is absent. This join does not retarget DR-120 leftover, does not steal DR-103 leftover, does not invent an adapter implementation, and does not SATISFY DR-120 or DR-103.")
for k in ['status','reviewStatus','sealRecommendation','binds']: v[k]=v5[k]
v['authorityClaim']=(f"This artifact PROPOSES an execution-remainder join successor for G15 leftovers. v6 remasures leftover-join.v5 after {CMJ} ({CM_D}). leftover-join.v5 remains frozen. leftoverDesign remains {LD}. It does not SATISFY DR-120. It does not SATISFY DR-103. It does not close leftover-design of OBL-AT-FX-AUTHORING or OBL-ADAPTER-IMPL. It does not invent an adapter implementation. It does not invent a numeric threshold. It does not invent an envelope. It does not mint a Rust adapter as slice-1 required. It does not add a DR-G* row. It does not change live required-now 28. It does not execute fixtures. It applies nothing and does not authorize docs/v2/implementation/.")
v['purpose']=(f"Remasure leftover-join.v5 against live HEAD after {CMJ} ({CM_D}). Cite occupancy v9 ({OCC_D}) as the current occupancy remasurement. Cite {CMJ} as the current DR-103 leftover-join; leftover-join.v5 cited {CMOLD}. Cite packaging leftover-join.v4 ({PK_D}) as the current DR-120 leftover-join, as leftover-join.v5 did. Preserve leftoverDesign {LD}. Frozen leftover-join.v5 stays unmoved. Do not SATISFY DR-120 or DR-103. Do not invent fixture bytes. Do not steal OBL-ADAPTER-IMPL, OBL-WINDOWS-PATH, OBL-ENVELOPE-MISMATCH, OBL-UNICODE-NORM, OBL-OD-1, or OBL-OD-2.")
b=O()
for k,val in v5['basedOn'].items():
    if k=='d269': continue  # stale last-heading custody entry; replaced by the live last-heading entry below (g18 leftover-join.v6 precedent, D-276)
    b[k]=O(val) if isinstance(val,dict) else val
b['cmljV4']['role']=(f"Predecessor ROW leftover-join. Historical. Measured {FIVE} leftoverDesign true. Not current. {CMOLD} was current at D-174; not current after {CM_D}. Current DR-103 ROW leftover-join is {CMJ} ({CM_D}). "+DIFF+" Not this artifact's version number.")
for r_ in ('claude','codex'): assert rev(b['cmljV6']['reviews'][r_]['path'])=='ACCEPT 0/0' and sha(b['cmljV6']['reviews'][r_]['path'])==b['cmljV6']['reviews'][r_]['sha256']
b['cmljV6']['role']=(f"Predecessor ROW leftover-join. Historical. Dual ACCEPT 0/0. {CMOLD} was current at D-174; not current after {CM_D}. Current DR-103 ROW leftover-join is {CMJ} ({CM_D}). leftoverDesign remains {FIVE} (the same five on {CMJ}). This GATE leftover-join does not steal those leftovers. "+DIFF+" Not this artifact's version number.")
b['predecessorV4']['role']=(f"Predecessor. Unmoved. Dual ACCEPT 0/0. Recorded as current G15 leftover-join at D-261; not current after {OWN_D}. Cited packaging leftover-join.v3 as the current DR-120 leftover-join. leftover-join.v5 remasured packaging leftover-join.v3 stale after packaging leftover-join.v4 ({PK_D}). packaging leftover-join.v4 remains the current DR-120 leftover-join. Not this artifact's version number.")
b['d270']=cust(OWN_D,"Recorded leftover-join.v5 as current G15 leftover-join. Not last-heading. Not this artifact's version number.")
b['predecessorV5']=pin('g15-leftover-join.v5.json',OWN_D,f"Predecessor. Unmoved. Dual ACCEPT 0/0. Recorded as current G15 leftover-join at {OWN_D}. Cited {CMOLD} as the current DR-103 leftover-join. This v6 remasures that citation stale after {CMJ} ({CM_D}). Not this artifact's version number.")
b['d282']=cust(CM_D,f"Recorded {CMJ} as current DR-103 leftover-join. Not last-heading. Not this artifact's version number.")
b['cmljV9']=pin('component-manifest-leftover-join.v9.json',CM_D,f"Current DR-103 ROW leftover-join recorded at {CM_D}. leftoverDesign remains {FIVE} (identical to {CMOLD}). This GATE leftover-join does not steal those leftovers. "+DIFF+" Not this artifact's version number.")
b['d'+LASTD[2:]]=cust(LASTD,"Last live heading at dispatch. Last-heading custody only.")
v['basedOn']=b
v['file08Pin']=O([('path',F08),('sha256',sha(F08))]); v['head']=HEAD; v['requiredNowUnchanged']=28; v['file08StatusToken']='OPEN'
v['leftoverDesignOpenStanding']=(f"The live DR-G15 token is OPEN. leftover-design of an unauthored G15 specification is stale as an authoring claim after occupancy v9 ({OCC_D}). leftover-design of unnamed AT-N classes is stale as a naming claim after at-named-corpus-catalog.v1. leftover-design of unnamed G15 initial states is stale as a naming claim after g15-input-corpus.v1. leftover-design of AT fixture implementations remains. leftover-design of adapter implementations remains on packaging leftover-join.v4 / DR-120. leftover-design of Windows-path, ENVELOPE_MISMATCH, unicode-norm, OD-1, and OD-2 remains on {CMJ} / DR-103. leftoverNameNote is absent. DR-120 is not SATISFIED. DR-103 is not SATISFIED.")
v['namedCorpusNotAuthored']=v5['namedCorpusNotAuthored']
ri=O(v5['recordedInputs']); ri[COORD]=sha(COORD); ri[F08]=sha(F08); ri['HEAD']=HEAD
for n in ['g15-leftover-join.v5.json','g15-leftover-join.v5.review-independent.claude2.json','g15-leftover-join.v5.review-independent.codex.json','component-manifest-leftover-join.v9.json','component-manifest-leftover-join.v9.review-independent.claude2.json','component-manifest-leftover-join.v9.review-independent.codex.json']: ri[P(n)]=sha(P(n))
v['recordedInputs']=ri
v['remeasurementClause']=(f"If a cited file moves in a way that is not append-only COORD growth or COORD heading hygiene, with file 08, leftover-join.v5, leftover-join.v4, occupancy v9, occupancy v7, packaging leftover-join v4, packaging leftover-join v3, packaging leftover-join v2, component-manifest leftover-join v9, component-manifest leftover-join v6, component-manifest leftover-join v4, and this draft unmoved, remasure before recording. recordedInputs.HEAD must equal the top-level head. This join does not unwrite D-086 or D-167 through {LASTD}. Frozen leftover-join.v5 of this lineage remains a historical measurement recorded at {OWN_D} after this successor is recorded. Frozen leftover-join.v4 of this lineage remains a historical measurement recorded at D-261. Frozen occupancy v9 remains current G15 occupancy remasurement. Frozen packaging leftover-join v4 remains current DR-120 leftover-join. Frozen component-manifest leftover-join v9 remains current DR-103 leftover-join.")
v['liveGateOwners']=v5['liveGateOwners']
obs=[]
for o in v5['obligations']:
    o=O(o); i=o['id']
    if i=='OBL-DR103-LEFTOVER-NOT-STOLEN':
        assert o['reason'].startswith('component-manifest leftover-join.v6 (D-174) still measures ')
        o['reason']=(f"{CMJ} ({CM_D}) still measures {FIVE} leftoverDesign true on DR-103. This join does not steal those leftovers, does not invent an envelope, and does not SATISFY DR-103.")
    if i=='OBL-DR120-LEFTOVER-NOT-STOLEN': assert o['reason'].startswith(f'packaging leftover-join.v4 ({PK_D}) still measures ')
    obs.append(o)
v['obligations']=obs; v['summary']=v5['summary']
v['doesNotCloseLeftoverAlone']=(f"This candidate does not SATISFY DR-120 or DR-103 and does not make G15 QUALIFIED. OBL-AT-FX-AUTHORING remains leftover-design. OBL-G15-NAMED-CATALOG naming is measured closed. OBL-G15-INPUT-CORPUS initial-state naming is measured closed. OBL-G15-HARNESS-SPEC authoring is measured closed; G15 execution remains qualification. OBL-ADAPTER-IMPL remains leftover-design on packaging leftover-join.v4 / DR-120. {FIVE} remain leftover-design on {CMJ} / DR-103. Not SATISFIED.")
v['proposedLaterWork']=list(v5['proposedLaterWork'])
dn=[]
for s in v5['doesNot']:
    if s=='Does not record leftover-join.v4 as current after this successor is recorded.':
        dn.append('Does not record leftover-join.v5 as current after this successor is recorded.'); dn.append('Does not record leftover-join.v4 as current G15 leftover-join.')
    else: dn.append(s)
assert 'Does not record component-manifest leftover-join.v4 as current DR-103 leftover-join.' in dn
dn.append(f'Does not record {CMOLD} as current DR-103 leftover-join.')
v['doesNot']=dn
pr=O(v5['parentReview']); assert pr['path']==P('harness.DR-G15.packaging-adapter-conformance.v9.review-independent.claude2.json') and sha(pr['path'])==pr['sha256'] and sha(pr['codex']['path'])==pr['codex']['sha256']
assert pr['role'].endswith(', not leftover-join.v4. D-086 named the identifier.')
pr['role']="Independent dual ACCEPT 0/0 of the current occupancy of the already-named identifier. Naming parent is naming v6 (D-145), not leftover-join.v5. D-086 named the identifier."
v['parentReview']=pr
assert list(v.keys())==list(v5.keys()),'top-level key order must match the predecessor'
out=sys.argv[1] if len(sys.argv)>1 else '/private/tmp/claude-501/-Users-sb-code-opensip-ai-opensip/dcbad0ae-7fad-4c78-89e7-e93d989f5501/scratchpad/g15-leftover-join.v6.json'
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
QUAL=r'(leftover-join\.|leftover-join |corpus |occupancy |Occupancy |catalog |this |This |at |Frozen |frozen |remasurement |naming |G15 |harness\.[^ ]*\.)$'
for p,s in walk(d):
    if p.endswith('.path') or p.startswith('.recordedInputs'): continue
    for m in re.finditer(r'[Tt]his v\d+',s):
        if m.group(0).lower()!='this v6': hits.append((p,'SPEAKER',s[max(0,m.start()-50):m.end()+40]))
    for m in re.finditer(r'(?<![\w.\-/])v\d+\b',s):
        if not re.search(QUAL,s[max(0,m.start()-26):m.start()]) and m.group(0)!='v6': hits.append((p,'BARE',s[max(0,m.start()-60):m.end()+30]))
    for m in re.finditer(r'(unchanged|identical)',s):
        pass  # claims of identity are asserted above from bytes (DR103_SET on cm v6 == cm v9)
bad=[k for k,s_ in ri.items() if k!='HEAD' and os.path.exists(k) and sha(k)!=s_]
print('wrote',out,len(raw),'bytes; HEAD',HEAD[:10],'; last heading',LASTD,'; cm v',CM_V,CM_D,'; own pred',OWN_V,OWN_D,'; digest mismatches',bad); print('audit hits:',len(hits)); [print('  ',h) for h in hits]
