import json,hashlib,shutil,copy,sys,importlib.util,subprocess
from pathlib import Path
sys.dont_write_bytecode=True
ARCH=Path('/Users/sb/code/opensip-ai/opensip_arch'); REV=Path('/tmp/opensip-implementation/m1-contract-binding-review-01'); MIR=REV/'mirror'
spec=importlib.util.spec_from_file_location('vd',REV/'work/tools/verify_design.py'); M=importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
LOCK0=json.loads((REV/'work/design-lock.json').read_bytes())
cs=LOCK0['contractSuccessor']
rec0=json.loads((ARCH/cs['record']['path']).read_bytes())
man0=json.loads((ARCH/cs['subjectManifest']['path']).read_bytes())
paths={r['path'] for r in LOCK0['approvals'].values()}|{r['path'] for r in LOCK0['inputs']}|{r['path'] for r in LOCK0['inventorySuccessor'].values()}|{r['path'] for r in cs.values()}|{r['path'] for r in man0['files']}|{r['path'] for r in rec0['parents']}|{rec0['previousCandidate']['path']}
def reset():
    if MIR.exists(): shutil.rmtree(MIR)
    for p in paths:
        (MIR/p).parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(ARCH/p,MIR/p)
def write(p,obj=None,raw=None):
    raw=raw if raw is not None else (json.dumps(obj,indent=2)+"\n").encode()
    (MIR/p).parent.mkdir(parents=True,exist_ok=True); (MIR/p).write_bytes(raw)
    return {"path":p,"sha256":hashlib.sha256(raw).hexdigest(),"bytes":len(raw)}
def rebind(rec=None,man_mut=None,rev_mut=None,as_mut=None,lock_mut=None):
    lock=copy.deepcopy(LOCK0)
    rec=rec if rec is not None else copy.deepcopy(rec0)
    rp=write(cs['record']['path'],rec)
    man=copy.deepcopy(man0); man['files']=[rp if r['path']==rp['path'] else r for r in man['files']]
    if man_mut: man_mut(man)
    mp=write(cs['subjectManifest']['path'],man)
    rev=json.loads((ARCH/cs['review']['path']).read_bytes()); rev['subjectManifestSha256']=mp['sha256']
    if rev_mut: rev_mut(rev)
    vp=write(cs['review']['path'],rev)
    a=json.loads((ARCH/cs['assent']['path']).read_bytes()); a.update(subjectManifest=copy.deepcopy(mp),actualClaudeReview=copy.deepcopy(vp),acceptedSuccessor=copy.deepcopy(rp))
    if as_mut: as_mut(a)
    ap=write(cs['assent']['path'],a)
    lock['contractSuccessor']=dict(record=rp,subjectManifest=mp,review=vp,assent=ap)
    if lock_mut: lock_mut(lock)
    return lock
results=[]
def run(name,lock,expect):
    try: M.verify(MIR,lock); out="PASS"
    except M.DesignError as e: out="REFUSE:"+str(e)
    except Exception as e: out=f"OTHER:{type(e).__name__}:{str(e)[:60]}"
    ok=(out=="PASS")==(expect=="PASS")
    results.append((name,expect,out,ok)); print("OK " if ok else "!! ",name,"| expect",expect,"|",out)
def ov(i,**kw):
    r=copy.deepcopy(rec0); r['passageOverrides'][i].update(kw); return r
reset()
run("baseline mirror, original lock",copy.deepcopy(LOCK0),"PASS")
run("baseline rebind with identical content (indent2 bytes)",rebind(),"PASS")
# selectors
run("line 0",rebind(ov(0,selector={"line":0})),"REFUSE")
run("line negative -1",rebind(ov(0,selector={"line":-1})),"REFUSE")
run("line float 885.0",rebind(ov(0,selector={"line":885.0})),"REFUSE")
run("line past EOF",rebind(ov(0,selector={"line":10**6})),"REFUSE")
run("line+pointer selector",rebind(ov(0,selector={"line":885,"jsonPointer":"/x"})),"REFUSE")
run("empty selector",rebind(ov(0,selector={})),"REFUSE")
run("pointer on markdown parent",rebind(ov(0,selector={"jsonPointer":"/x"})),"REFUSE")
run("pointer through string /files/7/description/x",rebind(ov(2,selector={"jsonPointer":"/files/7/description/x"})),"REFUSE")
run("pointer through string trailing slash",rebind(ov(2,selector={"jsonPointer":"/files/7/description/"})),"REFUSE")
run("pointer leading-zero index /files/07",rebind(ov(2,selector={"jsonPointer":"/files/07/description"})),"REFUSE")
run("pointer +7 index",rebind(ov(2,selector={"jsonPointer":"/files/+7/description"})),"REFUSE")
run("pointer unicode digit index",rebind(ov(2,selector={"jsonPointer":"/files/٧/description"})),"REFUSE")
run("pointer without slash",rebind(ov(2,selector={"jsonPointer":"files/7/description"})),"REFUSE")
run("pointer non-string",rebind(ov(2,selector={"jsonPointer":7})),"REFUSE")
run("pointer empty whole-doc",rebind(ov(2,selector={"jsonPointer":""})),"REFUSE")
run("pointer to non-string value",rebind(ov(2,selector={"jsonPointer":"/files/7"})),"REFUSE")
run("pointer wrong index /files/8",rebind(ov(2,selector={"jsonPointer":"/files/8/description"})),"REFUSE")
# before/after
b=rec0['passageOverrides'][0]['before']
run("stale before one char",rebind(ov(0,before=b[:-1]+"X")),"REFUSE")
run("before with trailing newline",rebind(ov(0,before=b+"\n")),"REFUSE")
run("before non-string",rebind(ov(0,before=None)),"REFUSE")
run("after empty",rebind(ov(0,after="")),"REFUSE")
run("after equals before",rebind(ov(0,after=b)),"REFUSE")
run("after non-string",rebind(ov(0,after=1)),"REFUSE")
# override shape
r=copy.deepcopy(rec0); r['passageOverrides'][0]['note']="x"; run("override extra field",rebind(r),"REFUSE")
r=copy.deepcopy(rec0); del r['passageOverrides'][0]['after']; run("override missing after",rebind(r),"REFUSE")
r=copy.deepcopy(rec0); r['passageOverrides']="" ; run("overrides empty string",rebind(r),"REFUSE")
r=copy.deepcopy(rec0); del r['passageOverrides']; run("overrides missing",rebind(r),"REFUSE")
r=copy.deepcopy(rec0); r['passageOverrides']=[]; run("overrides empty list (allowed)",rebind(r),"PASS")
r=copy.deepcopy(rec0); r['passageOverrides'].append(copy.deepcopy(r['passageOverrides'][2])); run("duplicate override identical",rebind(r),"REFUSE")
r=copy.deepcopy(rec0); d=copy.deepcopy(r['passageOverrides'][0]); d['after']="other"; r['passageOverrides'].append(d); run("duplicate selector conflicting after",rebind(r),"REFUSE")
r=copy.deepcopy(rec0); r['passageOverrides'][0]['parent']['bytes']=112851; run("override parent bytes mismatch",rebind(r),"REFUSE")
r=copy.deepcopy(rec0); r['passageOverrides'][0]['parent']['extra']=1; run("override parent extra key",rebind(r),"REFUSE")
r=copy.deepcopy(rec0); r['passageOverrides'][0]['parent']={"path":"docs/v2/architecture/08-decision-and-readiness-register.md","sha256":"de21a7e09096f2cf7b22f2700128e59581795278e46b80542745f5ca812395fe","bytes":130283}; run("override parent accepted input but not record parent",rebind(r),"REFUSE")
r=copy.deepcopy(rec0); r['passageOverrides'][0]['parent']['bytes']=112850.0; run("ADV override parent bytes float equal",rebind(r),"PASS?")
# line vs pointer aliasing of the same JSON passage
inv=(MIR/'docs/v2/architecture/repository-file-inventory.v1.json').read_text().split('\n')
ln=[i+1 for i,l in enumerate(inv) if json.dumps(rec0['passageOverrides'][2]['before'])[1:-1] in l]
r=copy.deepcopy(rec0); r['passageOverrides'].append({"parent":copy.deepcopy(r['passageOverrides'][2]['parent']),"selector":{"line":ln[0]},"before":inv[ln[0]-1],"after":"    \"description\": \"conflicting\","})
run("ADV same JSON passage via line and pointer, conflicting afters",rebind(r),"PASS?")
# parents
r=copy.deepcopy(rec0); r['parents'].reverse(); run("parents unsorted",rebind(r),"REFUSE")
r=copy.deepcopy(rec0); r['parents'].insert(1,copy.deepcopy(r['parents'][0])); run("parents duplicate",rebind(r),"REFUSE")
r=copy.deepcopy(rec0); r['parents']=[]; run("parents empty",rebind(r),"REFUSE")
r=copy.deepcopy(rec0); r['parents'][0]['sha256']="0"*64; run("parent sha differs from accepted",rebind(r),"REFUSE")
BASEPATHS=set(paths)
other=write("docs/coop/aaa-unaccepted.json",{"x":1}); paths.add("docs/coop/aaa-unaccepted.json")
r=copy.deepcopy(rec0); r['parents'].insert(0,other); r['parents'].sort(key=lambda x:x['path']); run("unaccepted parent (sorted)",rebind(r),"REFUSE")
r=copy.deepcopy(rec0); r['parents'].insert(0,dict(other)); r['passageOverrides'][0]['parent']=dict(other); r['parents'].sort(key=lambda x:x['path']); run("override targeting unaccepted parent",rebind(r),"REFUSE")
r=copy.deepcopy(rec0); r['parents'][1]['bytes']=26011.0; run("ADV parent bytes float",rebind(r),"REFUSE")
# candidates / subject
r=copy.deepcopy(rec0); r['candidates'].pop(); run("candidate omitted",rebind(r),"REFUSE")
r=copy.deepcopy(rec0); r['candidates'][0]['sha256']="0"*64; run("candidate pin differs",rebind(r),"REFUSE")
r=copy.deepcopy(rec0); r['candidates'].append(copy.deepcopy(cs['record'])); r['candidates'].sort(key=lambda x:x['path']); run("record listed as candidate",rebind(r),"REFUSE")
def man_extra(m): m['files'].append(other); m['files'].sort(key=lambda x:x['path'])
run("subject has extra member not in candidates",rebind(man_mut=man_extra),"REFUSE")
def man_parent(m):
    m['files'].append(copy.deepcopy(rec0['parents'][0])); m['files'].sort(key=lambda x:x['path'])
r=copy.deepcopy(rec0); r['candidates'].append(copy.deepcopy(rec0['parents'][0])); r['candidates'].sort(key=lambda x:x['path'])
run("candidate overwrites parent path (same bytes)",rebind(r,man_mut=man_parent),"REFUSE")
(MIR/'docs/implementation/m1/metadata-v2/fixtures.json').write_bytes(b'{}'); run("candidate bytes tampered",rebind(),"REFUSE"); shutil.copyfile(ARCH/'docs/implementation/m1/metadata-v2/fixtures.json',MIR/'docs/implementation/m1/metadata-v2/fixtures.json')
pc=rec0['previousCandidate']['path']; (MIR/pc).write_bytes(b'{}'); run("previousCandidate bytes tampered",rebind(),"REFUSE"); shutil.copyfile(ARCH/pc,MIR/pc)
r=copy.deepcopy(rec0); r['previousCandidate']['note']=1; run("previousCandidate extra key",rebind(r),"REFUSE")
r=copy.deepcopy(rec0); r['previousCandidate']=None; run("previousCandidate null",rebind(r),"REFUSE")
r=copy.deepcopy(rec0); r['passageDeletions']=[{"parent":"x"}]; run("ADV unknown record field ignored",rebind(r),"PASS?")
r=copy.deepcopy(rec0); r['schemaVersion']=99; run("ADV record schemaVersion unchecked",rebind(r),"PASS?")
# collision of candidate with accepted overlay path that is not input/parent
src=json.loads((ARCH/LOCK0['approvals']['sourceManifest']['path']).read_bytes()); app=json.loads((ARCH/LOCK0['approvals']['applicationManifest']['path']).read_bytes())
inputs={x['path'] for x in LOCK0['inputs']}|{x['path'] for x in rec0['parents']}
victim=sorted(x['path'] for x in src['files']+app['files'] if x['path'] not in inputs and x['path'].endswith('.json') and not x['path'].startswith('docs/implementation'))[0]
vp=write(victim,{"rewritten":True}); paths.add(victim)
r=copy.deepcopy(rec0); r['candidates'].append(vp); r['candidates'].sort(key=lambda x:x['path'])
def man_v(m): m['files'].append(vp); m['files'].sort(key=lambda x:x['path'])
run(f"ADV candidate rewrites accepted non-parent overlay path {victim}",rebind(r,man_mut=man_v),"PASS?")
# review / assent joins with downstream rebinding
run("review verdict ACCEPT-UNIT",rebind(rev_mut=lambda d:d.update(verdict="ACCEPT-UNIT")),"REFUSE")
run("review findings",rebind(rev_mut=lambda d:d.update(requiredFindings=[{"id":"x"}])),"REFUSE")
run("review findings missing",rebind(rev_mut=lambda d:d.pop("requiredFindings")),"REFUSE")
run("review names other manifest",rebind(rev_mut=lambda d:d.update(subjectManifestSha256="0"*64)),"REFUSE")
run("assent status",rebind(as_mut=lambda d:d.update(status="ACCEPTED-UNIT")),"REFUSE")
run("assent rootSubstantiveAssent 1",rebind(as_mut=lambda d:d.update(rootSubstantiveAssent=1)),"REFUSE")
run("assent findings missing",rebind(as_mut=lambda d:d.pop("requiredUnitFindings")),"REFUSE")
run("assent review sha differs",rebind(as_mut=lambda d:d['actualClaudeReview'].update(sha256='0'*64)),"REFUSE")
run("assent review path differs",rebind(as_mut=lambda d:d['actualClaudeReview'].update(path="x.json")),"REFUSE")
run("assent manifest bytes differs",rebind(as_mut=lambda d:d['subjectManifest'].update(bytes=1)),"REFUSE")
run("assent successor sha differs",rebind(as_mut=lambda d:d['acceptedSuccessor'].update(sha256="0"*64)),"REFUSE")
run("assent successor missing",rebind(as_mut=lambda d:d.pop('acceptedSuccessor')),"REFUSE")
run("assent successor list",rebind(as_mut=lambda d:d.update(acceptedSuccessor=[])),"REFUSE")
run("ADV assent join pin bytes float (lax ==)",rebind(as_mut=lambda d:d['acceptedSuccessor'].update(bytes=float(d['acceptedSuccessor']['bytes']))),"PASS?")
run("lock pin extra key",rebind(lock_mut=lambda l:l['contractSuccessor']['review'].update(note=1)),"REFUSE")
run("lock contractSuccessor non-object",rebind(lock_mut=lambda l:l.update(contractSuccessor=[])),"REFUSE")
paths=set(BASEPATHS)
# version compatibility
def v(ver,drop=(),extra=None):
    l=copy.deepcopy(LOCK0); l['schemaVersion']=ver
    for k in drop: l.pop(k)
    return l
reset()
run("v2 lock (no contract) on real mirror",v(2,("contractSuccessor",)),"PASS")
run("v1 lock (no successors)",v(1,("contractSuccessor","inventorySuccessor")),"PASS")
run("v2 with contractSuccessor",v(2),"REFUSE")
run("v1 with inventorySuccessor",v(1,("contractSuccessor",)),"REFUSE")
run("v3 without inventorySuccessor",v(3,("inventorySuccessor",)),"REFUSE")
run("v3 without contractSuccessor",v(3,("contractSuccessor",)),"REFUSE")
run("v3.0 float",v(3.0),"REFUSE")
run("v4",v(4),"REFUSE")
json.dump([dict(name=a,expect=b,observed=c,matchesExpectation=d) for a,b,c,d in results],open(REV/'probe-results.json','w'),indent=2)
print("mismatches:",sum(not x[3] for x in results),"of",len(results))
