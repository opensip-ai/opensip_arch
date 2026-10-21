"""Scoped synthetic controls and actual Node differential, before pin promotion."""
from pathlib import Path
import os,subprocess,json,tempfile,hashlib,collections,re
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'scope-initial-r2';assert not B.exists();B.mkdir()
W=Path('/Users/sb/code/opensip-ai/opensip-native-owner-patterns-takeover');P=W.parent/'opensip'
R='/opt/homebrew/Cellar/rust/1.95.0/bin/'
T=Path(tempfile.mkdtemp(prefix='opensip-native-owner-scope-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700)
E=dict(os.environ,CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(B/'target'),TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip())
owner=json.loads((W.parent/'opensip_arch/docs/implementation/m1/source-selection-v2/owners/native/owner-pattern-successor.v1.json').read_text())
for id,p in [('urn:opensip:product-v1:native:evidence-schemas:v2','schemas/sources/native-v2.schema.json'),('opensip.product.relation-payload.2','schemas/sources/relation-payload-v2.schema.json')]:
 raw=(P/p).read_text();rows=[r for r in owner['schemaPatternRows'] if r['document']==id]
 grouped=collections.Counter((r['from'],r['to']) for r in rows)
 for (old,new),count in grouped.items():
  before='"pattern": '+json.dumps(old);after='"pattern": '+json.dumps(new)
  assert raw.count(before)==count
  raw=raw.replace(before,after)
 assert json.loads(raw)==json.loads((W/p).read_text());(W/p).write_text(raw)
paths=subprocess.check_output(['/usr/bin/git','diff','--name-only'],cwd=W,text=True).splitlines()
fmt=[]
for p in paths:
 if not p.endswith('.rs'):continue
 old=subprocess.check_output(['/usr/bin/git','show','HEAD:'+p],cwd=W)
 r=subprocess.run([R+'rustfmt','--edition','2024','--emit','stdout'],input=old,env=E,capture_output=True)
 clean=r.returncode==0 and r.stdout==old
 if clean:subprocess.run([R+'rustfmt','--edition','2024',str(W/p)],env=E,check=True)
 fmt.append(dict(path=p,baseClean=clean))
pins={p:hashlib.sha256((W/p).read_bytes()).hexdigest() for p in paths}
report=dict(standing='SYNTHETIC PROGRAM SCOPE CONTROLS ONLY; REGISTERED PINS/GENERATOR/BLIND REFRESH/UNIT ACCEPTANCE STILL OPEN',sourcePins=pins,rustfmtClassification=fmt,privateTMPDIR=str(T),TMPDIRMode='0700',runs=[],productQualification=False)
for name,args in [('native-owner-scope',[R+'cargo','test','--locked','--offline','-p','opensip-identity','--lib','native_owner_']),('inherited-property-key-pattern',[R+'cargo','test','--locked','--offline','-p','opensip-identity','--lib','python_pattern_property_keys_and_shape_annotations_remain_distinct']),('clippy',[R+'cargo','clippy','--locked','--offline','-p','opensip-identity','--all-targets','--','-D','warnings'])]:
 print(name,flush=True)
 with (B/(name+'.log')).open('wb') as out:r=subprocess.run(args,cwd=W,env=E,stdout=out,stderr=subprocess.STDOUT)
 text=(B/(name+'.log')).read_text(errors='replace');report['runs'].append(dict(name=name,exitCode=r.returncode,summaries=re.findall(r'^test result:.*$',text,re.M)));(B/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 assert r.returncode==0,(name,text[-5000:])
assert all(hashlib.sha256((W/p).read_bytes()).hexdigest()==h for p,h in pins.items())
report['allInitialScopeChecksPassed']=True;(B/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print('INITIAL SCOPE CONTROLS PASS',flush=True)
