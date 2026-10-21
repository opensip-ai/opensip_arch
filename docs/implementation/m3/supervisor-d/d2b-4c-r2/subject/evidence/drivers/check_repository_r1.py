from pathlib import Path
import json,hashlib,subprocess,os,re,importlib.util,sys
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'repository-r1';B.mkdir(exist_ok=False)
W=Path('/Users/sb/code/opensip-ai/opensip-rust3-successor-takeover');A=W.parent/'opensip_arch';R='/opt/homebrew/Cellar/rust/1.95.0/bin/';PY='/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
assert json.loads((F/'source-census-r1/report.json').read_text())['sourceCheck']['passed']
paths=sorted(subprocess.check_output(['git','ls-files','-m','-o','--exclude-standard'],cwd=W,text=True).splitlines())
expected={r['path']for r in json.loads((F/'candidate-suites-r2/report.json').read_text())['sourcePins']}|{'tools/operability/exceptions.json'}
assert set(paths)==expected
assert all(p.startswith(('crates/components/src/provider_protocol/rust3','crates/components/tests/data/')) or p=='tools/operability/exceptions.json' for p in paths)
def pin(root,path):
 raw=(root/path).read_bytes();return dict(path=path,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
pins=[pin(W,p)for p in paths];report=dict(standing='Required repository/source/duty checks; no unit acceptance/qualification',sourcePins=pins,runs=[],unitAccepted=False,productQualification=False)
def save():(B/'report.json').write_text(json.dumps(report,indent=2)+'\n')
def run(name,args):
 with(B/(name+'.log')).open('wb')as out:r=subprocess.run(args,cwd=W,stdout=out,stderr=subprocess.STDOUT)
 report['runs'].append(dict(name=name,exitCode=r.returncode));save();assert r.returncode==0,name
save()
run('cargo-metadata',[R+'cargo','metadata','--locked','--offline','--format-version','1'])
(B/'metadata.json').write_bytes((B/'cargo-metadata.log').read_bytes())
run('package-edges',[PY,'-I','-B','tools/check_package_edges.py','--repository',str(W),'--metadata',str(B/'metadata.json'),'--inventory',str(A/'docs/implementation/m2/repository-file-inventory.v237.json'),'--lane','host','--architecture',str(A),'--lock',str(W/'design-lock.json'),'--package-policy',str(A/'docs/implementation/m3/operability/o1-package-policy-r1/package-policy.json')])
run('operability-source',[PY,'-I','-B','tools/check_operability.py','source','--repository',str(W)])
run('environment-exceptions',[PY,'-I','-B','tools/tests/test_environment_exceptions.py','-v'])
run('design-verifier',[PY,'-I','-B','tools/verify_design.py','--architecture',str(A),'--implementation',str(W)])
run('diff-check',['git','diff','--check'])
closure=set(re.findall(r"\('(crates/[^']+)', \d+, '[0-9a-f]{64}'\)",(W/'tools/security/discovery_census.py').read_text()))
assert len(closure)==19 and not closure&set(paths)
(B/'census-closure.json').write_text(json.dumps(dict(passed=True,closureFiles=19,changedPaths=paths,intersection=[],realBlindInvocations=0),indent=2)+'\n')
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec);sys.modules[name]=module;spec.loader.exec_module(module);return module
# Only public code, pins, constants and receipt bindings. Never a tree walk,
# corpus/store opening, reference loader, census mode or blind invocation.
dc=load('d2b4c_dc',W/'tools/security/discovery_census.py');sl=load('d2b4c_sl',W/'tools/security/snapshot_ledger_census.py')
binding=dc.receipt_bindings(W,A,dc.costs(W));companion=sl.Census(W,A,reference=(None,None)).bindings()
receipts=[]
for key,path,actual in [('discovery','crates/security/src/custody/discovery_census_held_out.json',binding),('companion','crates/security/src/snapshot_ledger_census_held_out.json',companion)]:
 expected_binding=json.loads((W/path).read_text())['bindings'];assert actual==expected_binding
 receipts.append(dict(kind=key,receipt=pin(W,path),currentBindingsMatch=True))
(B/'public-bindings.json').write_text(json.dumps(dict(discovery=binding,companion=companion),indent=2)+'\n')
(B/'public-binding-comparison.json').write_text(json.dumps(dict(passed=True,receipts=receipts,allFourPublicDataPins=[pin(W,p)for p in ['crates/security/src/custody/discovery_census.json','crates/security/src/custody/discovery_census_held_out.json','crates/security/src/snapshot_ledger_census.json','crates/security/src/snapshot_ledger_census_held_out.json']],realBlindInvocations=0,privateContentInspected=False),indent=2)+'\n')
plan=(A/'docs/implementation/m3/supervisor-d/d2b/PLAN-r3.md').read_text();section=plan[plan.index('## 3. The duty allocation'):plan.index('## 4. Checks')]
c=json.loads((W/'schemas/wire/native-carriers-v1.json').read_text());ad={r['id']:r['appliesTo']for r in c['admission']};rows=[]
for line in section.splitlines():
 cells=[x.strip()for x in line.strip().strip('|').split('|')]
 if len(cells)!=3 or cells[0]in ('Carrier row','---'):continue
 for name in cells[0].split(','):
  name=name.strip().strip('`*');rows.append(dict(id=name,appliesTo=ad.get(name),owner=cells[2]))
assert len(rows)==55 and len({r['id']for r in rows})==55 and {r['id']for r in rows}==set(ad)
S='crates/components/src/provider_protocol/rust3/send/';P='crates/components/src/provider_protocol/'
refs={
 'FRAME-LIMIT':[(S+'schedule.rs','next_totals'),(S+'participant.rs','received'),(P[:-1]+'.rs','next_fragment_len')],
 'ECHO-SNAPSHOT2':[(S+'policy.rs','open'),(S+'snapshot.rs','build'),(S+'sender.rs','check')],
 'ECHO-PLAN2':[(S+'policy.rs','open'),(S+'prepared.rs','build'),(S+'sender.rs','check')],
 'ECHO-OPEN-UNIVERSE':[(S+'policy.rs','open'),(S+'sender.rs','check')],
 'RAW-MANIFEST-DIGEST':[(P[:-1]+'.rs','manifest_digest'),(S+'snapshot.rs','build'),(S+'dependency.rs','build'),(S+'prepared.rs','build')],
 'RUST3-SNAPSHOT-ENTRY-TYPES':[(S+'snapshot.rs','value'),(S+'snapshot.rs','build')],
 'CHUNK-CUSTODY':[(S+'snapshot.rs','chunk'),(S+'dependency.rs','chunk'),(S+'prepared.rs','chunk'),(S+'sender.rs','realize'),(S+'sender.rs','check')],
 'SEAL-AGGREGATES':[(S+'snapshot.rs','build'),(S+'dependency.rs','build'),(S+'prepared.rs','build'),(S+'sender.rs','realize')],
 'CANONICAL-PATH-ADMISSION':[(P+'ts2/carrier.rs','lexical_ok'),(S+'snapshot.rs','build'),(S+'dependency.rs','build')],
 'PATH-SITE-SEGMENT-LAW':[(P+'ts2/carrier.rs','lexical_ok'),(S+'snapshot.rs','build'),(S+'dependency.rs','build')],
 'DEPSRC-CUSTODY':[(S+'dependency.rs','build'),(S+'dependency.rs','native_hash')],
 'PACKAGE-KEY-JOIN':[(S+'dependency.rs','package_key'),(S+'dependency.rs','build')],
 'PREPARED-V3-ENTRY':[(S+'prepared.rs','entry'),(S+'prepared.rs','build')],
 'REQUEST-WIRE-ACCOUNTING':[(S+'request.rs','build'),(S+'request.rs','record_chunks'),(S+'schedule.rs','new'),(S+'schedule.rs','next_totals')],
 'HOST-SEND-SCHEDULE':[(S+'sender.rs','realize'),(S+'sender.rs','check'),(S+'sender.rs','check_cancel'),(S+'sender.rs','charged')],
 'OWNER-PATTERN-EVALUATION':[(P+'rust3/schema_work.rs','admit_extern'),(P+'ts2/carrier.rs','check')],
 'DISPATCH-STAGE-CORRELATION':[(S+'domain.rs','derive'),(S+'domain.rs','stage_request'),(S+'request.rs','build')],
 'RUST3-DOMAIN-COMMITMENT':[(S+'domain.rs','derive'),(S+'domain.rs','analysis_commitment')],
 'RUST3-SUBJECTS':[(S+'domain.rs','derive')],
 'PER-KEY-SCOPE2':[(S+'domain.rs','derive')],
 'RUST3-PLAN-STAGE-BYTES':[(S+'domain.rs','stage_request'),(S+'sender.rs','check')],
 'UNIVERSE-NATIVE-IDENTITY':[(S+'domain.rs','derive'),(S+'domain.rs','generic_universe_commitment'),(S+'policy.rs','open')],
 'CANCEL-NULLABILITY':[(S+'sender.rs','cancel_payload'),(S+'sender.rs','check_cancel'),(S+'participant.rs','pump')],
}
R=P+'rust3/'
refs.update({
 'RUST3-FRAME-PRECHECK':[(R+'receive.rs','admit')],
 'ACCEPTED-EQUALS-SEAL':[(R+'receive.rs','admit')],
 'FP-CANDIDATE':[(R+'receive.rs','candidate')],
 'RELATION-PAYLOAD-CBOR':[(R+'receive.rs','candidate')],
 'ANCHOR-WIRE-SPAN':[(R+'receive.rs','candidate')],
 'ANCHOR-FACT-REF-REFUSED':[(R+'receive.rs','candidate')],
 'OCCUPANCY-JOIN':[(R+'receive.rs','fact_batch')],
 'RUST3-SPOOL':[(R+'receive.rs','receive'),(R+'receive.rs','take_candidate_spool')],
 'COMMIT-MAP':[(R+'receive.rs','coverage'),(R+'receive.rs','terminal_coverage'),(R+'receive.rs','complete')],
 'CANCELLED-ECHO':[(R+'receive.rs','admit')],
 'RUST3-CANCEL-TYPES':[(R+'receive.rs','admit')],
 'RUST3-PROVIDER-FAULT':[(R+'receive.rs','admit')],
 'RUST3-BUDGET-EXHAUSTED':[(R+'receive.rs','admit')],
})
refs['PER-KEY-SCOPE2'] += [(R+'receive.rs','entry_echoes'),(R+'census.rs','empty_scope'),(R+'census.rs','returned')]
refs['OWNER-PATTERN-EVALUATION'] += [(R+'census.rs','shape'),(R+'schemas.rs','check_selected_payload')]
refs['RUST3-SUBJECTS'] += [(S+'domain.rs','subjects'),(R+'receive.rs','new')]
refs['DISPATCH-STAGE-CORRELATION'] += [(R+'receive.rs','fact_batch'),(R+'receive.rs','admit')]
owned=[];other=[]
for row in rows:
 if row['id']in refs:
  row['sourcePredicates']=[]
  for path,fn in refs[row['id']]:
   raw=(W/path).read_bytes();assert re.search(r'fn\s+'+re.escape(fn)+r'\s*(?:<[^>]*>)?\s*\(',raw.decode()),(path,fn)
   row['sourcePredicates'].append(dict(path=path,function=fn,sha256=hashlib.sha256(raw).hexdigest()))
  owned.append(row)
 else:other.append(row)
assert len(owned)==36
(B/'duty-table.json').write_text(json.dumps(dict(passed=True,carrierIds=55,listedOnce=True,indexedRust3Rows=owned,otherOwners=other,semanticProof='Function locations are a review index only, not semantic proof. Current actual predicates, owning runtime and compiled mutation controls require independent review. C4 selection/admission, H facts/census settlement and production/qualification duties remain separate.'),indent=2)+'\n')
assert all(pin(W,p['path'])==p for p in pins)
report.update(allPassed=True,carrierIds=55,indexedRust3Rows=36,realBlindInvocations=0,publicReceiptBindingsCurrent=True,closureFilesUnchanged=True);save();print('REPOSITORY/PUBLICBINDINGS/55DUTYIDS(36RUST3INDEXED) PASS; NO UNIT ACCEPTANCE')
