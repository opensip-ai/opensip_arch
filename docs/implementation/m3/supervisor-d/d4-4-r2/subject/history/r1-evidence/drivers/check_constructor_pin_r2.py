"""Frozen-source D4 constructor pin; not the future D5 general reachability checker."""
from pathlib import Path
import os,json,subprocess,re,hashlib,importlib.util,sys
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;W=Path('/Users/sb/code/opensip-ai/opensip-d4factory-takeover');B=F/'constructor-pin-r2';B.mkdir(exist_ok=False)
paths=sorted(set(subprocess.check_output(['git','ls-files','-c','-o','--exclude-standard'],cwd=W,text=True).splitlines()));rust=[p for p in paths if p.endswith('.rs')]
def pin(p):
 b=(W/p).read_bytes();return dict(path=p,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
expected={'crates/platform/src/process.rs':1,'crates/platform/src/process_tests.rs':10,'crates/platform/src/process_accounted.rs':1,'crates/components/src/supervisor_tests.rs':2,'crates/components/src/session_factory.rs':1}
spec=importlib.util.spec_from_file_location('d4_constructor_lexical_mask',W/'tools/check_operability.py');tool=importlib.util.module_from_spec(spec);sys.modules[spec.name]=tool;spec.loader.exec_module(tool)
rows=[]
for path in rust:
 source=(W/path).read_text()
 for match in re.finditer(r'\bfrom_recheck\b',tool.rust_code(source)):
  line=source.count('\n',0,match.start())+1;rows.append(dict(path=path,line=line,text=source.splitlines()[line-1],byteOffset=match.start()))
actual={p:sum(r['path']==p for r in rows) for p in set(r['path'] for r in rows)};assert actual==expected
platform=(W/'crates/platform/src/process.rs').read_text();factory=(W/'crates/components/src/session_factory.rs').read_text();accounted=(W/'crates/platform/src/process_accounted.rs').read_text()
assert 'pub fn from_recheck(spec: LaunchSpec, recheck: ClosureRecheck) -> Self {\n        Self { spec, recheck }\n    }'in platform
assert 'let launch = VerifiedLaunch::from_recheck(specification, executable);'in factory
assert factory.index('let checked = recheck') < factory.index('let launch = VerifiedLaunch::from_recheck')
assert '#[cfg(all(test, target_os = "macos"))]\n#[allow(unsafe_code)]\nmod process_tests;' in (W/'crates/platform/src/lib.rs').read_text()
assert '#[cfg(test)]\n#[path = "supervisor_tests.rs"]\npub(crate) mod tests;'in (W/'crates/components/src/supervisor.rs').read_text()
assert '#[cfg(test)]\nmod tests {'in accounted
assert accounted.index('#[cfg(test)]\nmod tests {') < accounted.index('VerifiedLaunch::from_recheck(')
assert 'pub fn into_test_fixture(mut self) -> Self {\n        self.spec.class = LaunchClass::TestFixture;\n        self\n    }'in platform
for row in rows:row['observedClass']='constructor-declaration' if row['path']=='crates/platform/src/process.rs' else 'production-factory-use' if row['path']=='crates/components/src/session_factory.rs' else 'cfg-test-use'
parents=['crates/platform/src/lib.rs','crates/components/src/supervisor.rs'];report=dict(standing='Current frozen-source D4 sole-constructor-use pin and inspected test module guards. This is not D5 general Cargo/cfg reachability/tool acceptance or qualification.',scannedRustFiles=len(rust),lexicalMaskTool=pin('tools/check_operability.py'),allIdentifierOccurrences=rows,occurrenceSourcePins=[pin(p)for p in sorted(expected)],guardSourcePins=[pin(p)for p in parents],observedProductionFactoryUses=1,testUses=13,constructorDeclarations=1,fixtureConversionDoesNotReconstruct=True,sourceInspectionPassed=True,D5GeneralStructuralGateComplete=False,implementationAccepted=False,productQualification=False)
(B/'report.json').write_text(json.dumps(report,indent=2)+'\n');print('FROZEN SOURCE PIN:15 IDENTIFIERS =1DECLARATION+1PRODUCTIONFACTORY+13TEST USES; D5 GENERAL GATE STILL OWED')
