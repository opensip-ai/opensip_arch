from pathlib import Path
import json,subprocess,hashlib,shutil
B=Path('/tmp/opensip-design-corrections');O=Path(__file__).parent;S=B/'source39-corrections-successor.v1/source'
L=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews')
P='/tmp/opensip-architecture-review-env/bin/python';rows=[]
for name,cmd in [('nested',[P,'-I','-B',str(O/'nested-probe.py')]),('jsconfig',[P,'-I','-B',str(B/'root-jsconfig-mode-correction.v1/probe.py'),str(S),str(O/'jsconfig')])]:
 r=subprocess.run(cmd,capture_output=True,text=True);(O/(name+'.stdout')).write_text(r.stdout);(O/(name+'.stderr')).write_text(r.stderr);assert r.returncode==0
 rows.append({'name':name,'command':cmd,'exitCode':r.returncode})
n=json.loads((O/'report.json').read_bytes());assert len(n['rows'])==4 and not any(r['raised'] for r in n['rows'])
assert n['rows'][2]['output']['units'][0]['memberPackageRoots']==['nested','nested/pkg']
assert n['rows'][3]['output']['units'][0]['rootPath']=='nested'
js=json.loads((O/'jsconfig/report.json').read_bytes());assert js['passed'] and len(js['rows'])==7
rel='docs/coop/design-corrections/native/native-cases.v2.json';base=json.loads((B/'candidate-subject.v39'/rel).read_bytes());now=json.loads((S/rel).read_bytes())
by={r['id']:r for r in now['cases']};old={r['id']:r for r in base['cases']}
assert len(by)==len(now['cases'])==len(old)+8
assert all(by[k]==v for k,v in old.items())
assert all(now['fixtures'][k]==v for k,v in base['fixtures'].items())
report={'standing':'Root original discriminator probes repeated after merging both actual Claude native patches to check integration. Trusted-marker reference scope only; no independent acceptance/product qualification.','commands':rows,'nestedFourReturn':True,'jsconfigSevenPass':True,'nativeCases':len(by),'allHistoricalNativeCasesAndFixturesPreserved':True,'newNativeCases':sorted(set(by)-set(old)),'modelSha256':js['modelSha256']}
(O/'assessment.json').write_text(json.dumps(report,indent=2)+'\n');shutil.copytree(O,L/O.name);print(json.dumps(report))
