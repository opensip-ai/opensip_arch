from pathlib import Path
import os,subprocess,json,re,hashlib
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;W=Path('/Users/sb/code/opensip-ai/opensip-d4-3-takeover');P=W.parent/'opensip';R='/opt/homebrew/Cellar/rust/1.95.0/bin/';paths=['crates/host/src/invocation.rs','crates/host/src/invocation_tests.rs'];rows=[]
for p in paths:
 raw=subprocess.check_output(['git','show','HEAD:'+p],cwd=P);formatted=subprocess.check_output([R+'rustfmt','--edition','2024','--emit','stdout'],input=raw,cwd=W);rows.append(dict(path=p,baseFormatClean=raw==formatted,candidateSha256=hashlib.sha256((W/p).read_bytes()).hexdigest()))
subprocess.run(['git','diff','--check'],cwd=W,check=True)
closure=set(re.findall(r"\('(crates/[^']+)', \d+, '[0-9a-f]{64}'\)",(W/'tools/security/discovery_census.py').read_text()));assert len(closure)==19 and not closure.intersection(paths)
assert subprocess.check_output(['git','diff','--name-only'],cwd=W,text=True).splitlines()==paths
report=dict(formatting=rows,censusClosureEntries=len(closure),censusClosureUnchanged=True,privateCensusRun=False,packageManifestsUnchanged=True,allPassed=all(x['baseFormatClean'] for x in rows));(F/'final-static-checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));assert report['allPassed']
