from pathlib import Path
import os,subprocess,tempfile,json,hashlib
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent; P=Path('/Users/sb/code/opensip-ai/opensip'); W=P.parent/'opensip-native-owner-patterns-takeover'; A=P.parent/'opensip_arch'
T=Path(tempfile.mkdtemp(prefix='opensip-native-generation-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip())); T.chmod(0o700)
E=dict(os.environ,TMPDIR=str(T)); py='/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/Resources/Python.app/Contents/MacOS/Python'
cache='/tmp/opensip-implementation/d2b0b-materialization-r1/generation-r1/'
report=dict(privateTMPDIR=str(T),mode='0700',runs=[],unitAccepted=False,blindRefreshComplete=False)
for name,write in [('generation-r1',True),('generation-check-r1',False)]:
 args=[py,'-I','-B',str(P/'tools/generate_contracts.py'),'--root',str(W),'--architecture',str(A),'--output',str(F/name),'--node',cache+'tool-node','--generator',cache+'tool-generator','--python',py]
 if write:args.append('--write')
 print(name,flush=True)
 with (F/(name+'.log')).open('wb') as out:r=subprocess.run(args,env=E,cwd=W,stdout=out,stderr=subprocess.STDOUT)
 report['runs'].append(dict(name=name,exitCode=r.returncode));(F/'generation-report.json').write_text(json.dumps(report,indent=2)+'\n')
 assert r.returncode==0,(name,(F/(name+'.log')).read_text()[-5000:])
 report['runs'][-1]['selectionResult']=json.loads((F/name/'selection-result.json').read_text())
 (F/'generation-report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2),flush=True)
