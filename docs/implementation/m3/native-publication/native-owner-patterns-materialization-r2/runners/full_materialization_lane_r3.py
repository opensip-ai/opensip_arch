"""Reverify the only additional path after complete r2: host integration tests.

Retain exact r2 results for unchanged owning sources. Do not rerun unrelated
passed suites or conceal r2's three host failures.
"""
from pathlib import Path
import os,subprocess,json,hashlib,tempfile,re
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'full-r3';assert not B.exists();B.mkdir()
W=Path('/Users/sb/code/opensip-ai/opensip-native-owner-patterns-takeover');A=W.parent/'opensip_arch'
R='/opt/homebrew/Cellar/rust/1.95.0/bin/'
old=json.loads((F/'full-r2/report.json').read_text());assert old['selectedGenerationInputsStillExact']==352
assert [r['name'] for r in old['runs'] if r['exitCode']] == ['owning-host']
for p,h in old['sourcePins'].items():assert hashlib.sha256((W/p).read_bytes()).hexdigest()==h
rel='crates/host/tests/admission_tests.rs'
correction=json.loads((F/'host-integration-consumer-correction.json').read_text())
assert hashlib.sha256((W/rel).read_bytes()).hexdigest()==correction['afterSha256']
paths=sorted(subprocess.check_output(['/usr/bin/git','diff','--name-only'],cwd=W,text=True).splitlines()+subprocess.check_output(['/usr/bin/git','ls-files','--others','--exclude-standard'],cwd=W,text=True).splitlines())
assert set(paths)==set(old['sourcePins'])|{rel} and len(paths)==42
pins={p:hashlib.sha256((W/p).read_bytes()).hexdigest() for p in paths}
T=Path(tempfile.mkdtemp(prefix='opensip-native-final-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700)
E=dict(os.environ,PATH='/opt/homebrew/bin:'+R+':/usr/bin:/bin',CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(F/'registered-initial-r1/target'),TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip())
report=dict(old,standing='FINAL COMPLETE MATERIALIZATION CHECK COMPOSITION: R2 ALL OWNING SOURCES EXACT PLUS R3 HOST INTEGRATION CORRECTION',sourcePins=pins,r2Evidence=str(F/'full-r2/report.json'),r2SourcePinsExact=True,onlyPathAddedSinceR2=rel,reusedChecksReason='All 41 r2 paths remain byte-exact; only host integration test source changes. Full host owning and all-target warning-denied Clippy rerun. Other r2 owning, TS, source/package/environment/design and feature results retained with exact input correspondence.',runs=[dict(r,reusedFrom='full-r2/report.json') for r in old['runs'] if r['name'] not in ['owning-host','clippy']],allPassed=False,privateTMPDIR=str(T),TMPDIRMode='0700')
def save():(B/'report.json').write_text(json.dumps(report,indent=2)+'\n')
save()
for name,args in [
 ('owning-host',[R+'cargo','test','--locked','--offline','--no-fail-fast','-p','opensip-host']),
 ('clippy',[R+'cargo','clippy','--locked','--offline',*[v for p in ['identity','contracts','components','host','security','storage','evaluator','lifecycle'] for v in ['-p','opensip-'+p]],'--all-targets','--','-D','warnings'])]:
    print(name,flush=True)
    with (B/(name+'.log')).open('wb') as out:r=subprocess.run(args,cwd=W,env=E,stdout=out,stderr=subprocess.STDOUT)
    output=(B/(name+'.log')).read_text(errors='replace')
    report['runs'].append(dict(name=name,args=args,exitCode=r.returncode,summaries=re.findall(r'^test result:.*$',output,re.M),failedTests=re.findall(r'^test (\S+) \.\.\. FAILED$',output,re.M)));save()
def clean(raw):
    proc=subprocess.run([R+'rustfmt','--edition','2024','--emit','stdout'],input=raw,env=E,capture_output=True)
    return proc.returncode==0 and proc.stdout==raw
before=subprocess.check_output(['/usr/bin/git','show','HEAD:'+rel],cwd=W)
row=dict(path=rel,baseClean=clean(before),candidateClean=clean((W/rel).read_bytes()))
report['rustfmtClassification']=old['rustfmtClassification']+[row]
report['formatPassed']=all(r['candidateClean'] for r in report['rustfmtClassification'] if r['baseClean'])
for p,h in pins.items():assert hashlib.sha256((W/p).read_bytes()).hexdigest()==h
closure=json.loads((W/'tools/contracts/generator-closure.json').read_text())
for r in closure['files']:
    raw=(W/r['path']).read_bytes();assert len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256']
for r in json.loads((F/'generated-output-audit.json').read_text())['outputs']:
    raw=(W/r['path']).read_bytes();assert len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256']
report.update(sourcePinsUnchanged=True,allPassed=all(r['exitCode']==0 for r in report['runs']) and report['formatPassed'])
save();print(json.dumps(dict(allPassed=report['allPassed'],failures=[r['name'] for r in report['runs'] if r['exitCode']]),indent=2),flush=True)
