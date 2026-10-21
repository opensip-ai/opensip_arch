from pathlib import Path
import json,hashlib,subprocess,os,re,importlib.util,sys
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
os.environ.update(CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR='/tmp/opensip-implementation/d4factory-takeover-2026-10-21/target')
F=Path(__file__).parent;B=F/'repository-r1';B.mkdir(exist_ok=False)
W=Path('/Users/sb/code/opensip-ai/opensip-d4factory-takeover');A=W.parent/'opensip_arch';R='/opt/homebrew/Cellar/rust/1.95.0/bin/';PY='/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
assert json.loads((F/'source-census-r1/report.json').read_text())['sourceCheck']['passed']
paths=sorted(subprocess.check_output(['git','ls-files','-m','-o','--exclude-standard'],cwd=W,text=True).splitlines())
expected={r['path']for r in json.loads((F/'native-clippy-r8/report.json').read_text())['sourcePins']}|{'tools/operability/exceptions.json'}
assert set(paths)==expected

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
run('package-edges',[PY,'-I','-B','tools/check_package_edges.py','--repository',str(W),'--metadata',str(B/'metadata.json'),'--inventory',str(A/'docs/implementation/m2/repository-file-inventory.v238.json'),'--lane','host','--architecture',str(A),'--lock',str(W/'design-lock.json'),'--package-policy',str(A/'docs/implementation/m3/operability/o1-package-policy-r1/package-policy.json')])
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

assert all(pin(W,p['path'])==p for p in pins)
report.update(allPassed=True,realBlindInvocations=0,publicReceiptBindingsCurrent=True,closureFilesUnchanged=True);save();print('REPOSITORY/SOURCE/PACKAGE/DESIGN/PUBLICBINDING CHECKS PASS; NO PRIVATE OR BLIND INVOCATION')
