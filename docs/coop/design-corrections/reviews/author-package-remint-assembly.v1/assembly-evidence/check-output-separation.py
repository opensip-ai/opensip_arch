from pathlib import Path
import subprocess,json
B=Path('/tmp/opensip-design-corrections');O=Path(__file__).parent;P=B/'claude-author-package-successor.v2';S=B/'claude-author-remint.v1/source';PY='/tmp/opensip-architecture-review-env/bin/python'
before=O/'author_portable.before.py';after=P/'author_portable.py'
script="import importlib.util,sys;s=importlib.util.spec_from_file_location('portable',sys.argv.pop(1));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);a=m.arguments('no-write argument probe');print(a.out)"
rows=[]
for label,path in [('source-child',S/'must-not-create'),('package-child',P/'must-not-create'),('helper-child',P/'author-helpers/must-not-create'),('separate',O/'allowed-fresh-output')]:
 assert not path.exists();rec={'case':label,'out':str(path)}
 for name,mod in [('before',before),('after',after)]:
  p=subprocess.run([PY,'-I','-B','-c',script,str(mod),'--source',str(S),'--package',str(P),'--out',str(path)],capture_output=True,text=True)
  rec[name]={'exitCode':p.returncode,'stderr':p.stderr}
 assert rec['before']['exitCode']==0
 assert (rec['after']['exitCode']==0)==(label=='separate');assert not path.exists();rows.append(rec)
(O/'output-separation-controls.json').write_text(json.dumps({'standing':'Argument-only controls create no output and preserve all inputs','controls':rows,'passed':True},indent=2)+'\n');print('PASS: three input overlaps refused before mutation; separate fresh output admitted')
