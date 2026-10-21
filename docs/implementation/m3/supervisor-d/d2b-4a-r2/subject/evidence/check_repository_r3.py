from pathlib import Path
import json,hashlib,subprocess,os,tempfile,re
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'repository-r3';B.mkdir(exist_ok=False);W=Path('/Users/sb/code/opensip-ai/opensip-d2b4a-takeover');A=W.parent/'opensip_arch';R='/opt/homebrew/Cellar/rust/1.95.0/bin/';PY='/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14';T=Path(tempfile.mkdtemp(prefix='n-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700);os.setpriority(os.PRIO_PROCESS,0,10);E=dict(os.environ,CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(F/'target'),TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip())
r=subprocess.run([R+'rustfmt','--edition','2024',str(W/'crates/components/src/provider_protocol/rust3/receive_tests.rs')],cwd=W,env=E,capture_output=True);(B/'format.log').write_bytes(r.stdout+r.stderr);assert r.returncode==0
paths=sorted(subprocess.check_output(['/usr/bin/git','ls-files','-m','-o','--exclude-standard'],cwd=W,text=True).splitlines());pins=[]
for p in paths:
 raw=(W/p).read_bytes();pins.append(dict(path=p,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
report=dict(standing='D2B4A REQUIRED REPOSITORY CHECKS; NO UNIT ACCEPTANCE',sourcePins=pins,runs=[],unitAccepted=False,productQualification=False)
def save():(B/'report.json').write_text(json.dumps(report,indent=2)+'\n')
def run(name,args):
 print(name,flush=True)
 with (B/(name+'.log')).open('wb')as out:r=subprocess.run(args,cwd=W,env=E,stdout=out,stderr=subprocess.STDOUT)
 report['runs'].append(dict(name=name,exitCode=r.returncode));save();assert r.returncode==0,name
run('cargo-metadata',[R+'cargo','metadata','--locked','--offline','--format-version','1']);(B/'metadata.json').write_bytes((B/'cargo-metadata.log').read_bytes())
run('package-edges',[PY,'-I','-B','tools/check_package_edges.py','--repository',str(W),'--metadata',str(B/'metadata.json'),'--inventory',str(A/'docs/implementation/m2/repository-file-inventory.v235.json'),'--lane','host','--architecture',str(A),'--lock',str(W/'design-lock.json'),'--package-policy',str(A/'docs/implementation/m3/operability/o1-package-policy-r1/package-policy.json')])
run('operability-source',[PY,'-I','-B','tools/check_operability.py','source','--repository',str(W)])
run('environment-exceptions',[PY,'-I','-B','tools/tests/test_environment_exceptions.py','-v'])
# A public-source closure check only; no private rows/caches or blind modes.
closure=set(re.findall(r"\('(crates/[^']+)', \d+, '[0-9a-f]{64}'\)",(W/'tools/security/discovery_census.py').read_text()));hit=sorted(closure&set(paths));assert len(closure)>=10 and not hit;(B/'census-closure.json').write_text(json.dumps(dict(passed=True,closureFiles=len(closure),changedPaths=paths,intersection=hit,realBlindInvocations=0),indent=2)+'\n')
# Reconcile EVERY admission ID once with the accepted plan, and map this
# receive unit's 23 rows to concrete source predicates; semantics are judged
# by the independent full-unit review, not proved by a string search.
plan=(A/'docs/implementation/m3/supervisor-d/d2b/PLAN-r3.md').read_text();section=plan[plan.index('## 3. The duty allocation'):plan.index('## 4. Checks')];c=json.loads((W/'schemas/wire/native-carriers-v1.json').read_text());ad={row['id']:row['appliesTo']for row in c['admission']};rows=[]
for line in section.splitlines():
 cells=[x.strip()for x in line.strip().strip('|').split('|')]
 if len(cells)!=3 or cells[0]in ('Carrier row','---'):continue
 for i in [x.strip().strip('`*')for x in cells[0].split(',')]:rows.append(dict(id=i,appliesTo=ad.get(i),owner=cells[2]))
listed=[r['id']for r in rows];assert len(listed)==len(set(listed))and set(listed)==set(ad)
receive='crates/components/src/provider_protocol/rust3/receive.rs';schemas='crates/components/src/provider_protocol/rust3/schemas.rs';carrier='crates/components/src/provider_protocol/ts2/carrier.rs';work='crates/components/src/provider_protocol/rust3/schema_work.rs';accounting='crates/components/src/provider_protocol/rust3/accounting.rs';observations='crates/components/src/provider_protocol/rust3/observations.rs'
refs={
 'RUST3-FRAME-PRECHECK':[(schemas,'check_envelope'),(receive,'admit')],
 'ECHO-SNAPSHOT2':[(receive,'admit'),(receive,'pre_analyze_unavailable')],
 'ECHO-PLAN2':[(receive,'admit'),(receive,'pre_analyze_unavailable')],
 'ECHO-OPEN-UNIVERSE':[(receive,'admit')],
 'RAW-MANIFEST-DIGEST':[(receive,'admit')],
 'ACCEPTED-EQUALS-SEAL':[(receive,'admit')],
 'CANONICAL-PATH-ADMISSION':[(carrier,'lexical_ok'),(receive,'candidate')],
 'PATH-SITE-SEGMENT-LAW':[(carrier,'lexical_ok'),(receive,'candidate')],
 'OWNER-PATTERN-EVALUATION':[(work,'admit_extern'),(schemas,'check_payload')],
 'DISPATCH-STAGE-CORRELATION':[(receive,'admit'),(receive,'fact_batch'),(receive,'coverage')],
 'PER-KEY-SCOPE2':[(receive,'entry_echoes')],
 'UNIVERSE-NATIVE-IDENTITY':[(receive,'entry_echoes'),(receive,'candidate')],
 'FP-CANDIDATE':[(receive,'candidate')],
 'RELATION-PAYLOAD-CBOR':[(receive,'candidate'),(receive,'contains_bytes')],
 'ANCHOR-WIRE-SPAN':[(receive,'candidate'),(carrier,'order_ok')],
 'ANCHOR-FACT-REF-REFUSED':[(receive,'candidate')],
 'OCCUPANCY-JOIN':[(receive,'fact_batch')],
 'RUST3-SPOOL':[(accounting,'prepare'),(receive,'receive')],
 'COMMIT-MAP':[(receive,'commit'),(receive,'coverage'),(receive,'terminal_coverage'),(receive,'complete')],
 'CANCELLED-ECHO':[(receive,'admit')],
 'RUST3-CANCEL-TYPES':[(receive,'admit')],
 'RUST3-PROVIDER-FAULT':[(observations,'matches'),(receive,'admit')],
 'RUST3-BUDGET-EXHAUSTED':[(receive,'admit')],
}
owned=[];other=[]
for row in rows:
 owner=row['owner'];mine=row['appliesTo']in('both','rust-semantic')and(('admission'in owner and not owner.startswith('H:')and'(Plan side'not in owner)or owner.startswith('each consumer')or row['id']=='RUST3-FRAME-PRECHECK')
 if mine:
  assert row['id']in refs,row['id'];row['sourcePredicates']=[]
  for path,fn in refs[row['id']]:
   raw=(W/path).read_bytes();text=raw.decode();assert re.search(r'fn\s+'+re.escape(fn)+r'\s*(?:<[^>]*>)?\s*\(',text),(path,fn);row['sourcePredicates'].append(dict(path=path,function=fn,sha256=hashlib.sha256(raw).hexdigest()))
  owned.append(row)
 else:other.append(row)
assert set(refs)=={r['id']for r in owned};(B/'duty-table.json').write_text(json.dumps(dict(passed=True,carrierIds=len(ad),listedOnce=True,receiveRows=owned,otherOwners=other,semanticProof='Independent review of actual predicates and owning/mutation evidence remains required; mapping alone grants no admission.'),indent=2)+'\n')
for row in pins:assert hashlib.sha256((W/row['path']).read_bytes()).hexdigest()==row['sha256']
report.update(allPassed=True,closureFilesUnchanged=True,realBlindInvocations=0,carrierIds=len(ad),receiveRows=len(owned));save();print('REPOSITORY CHECKS/DUTY ALLOCATION PASS; NO UNIT ACCEPTANCE',flush=True)
