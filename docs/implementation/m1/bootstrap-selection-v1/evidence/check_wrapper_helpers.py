"""Real filesystem and subprocess controls for the unselected developer wrapper.
No approval fixture or positive activation is introduced.
"""
from pathlib import Path
import importlib.util,json,hashlib,subprocess,sys,selectors,os
B=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('wrapper',B/'product/tools/check_typescript.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
work=B/'helper-controls';work.mkdir()
root=work/'inputs';root.mkdir();(root/'regular').write_bytes(b'exact');(root/'linked').symlink_to('regular');(root/'dir').mkdir();os.mkfifo(root/'pipe')
rows=[]
def test(name,fn):
 try:fn();rows.append({'case':name,'passed':True})
 except Exception as e:rows.append({'case':name,'passed':False,'error':repr(e)})
def refusal(fn):
 try:fn()
 except (ValueError,FileNotFoundError):return
 raise AssertionError('accepted')
for name in ['', '../outside','/absolute','a//b','a/./b','a\\b','a\0b','linked','dir','pipe']:
 test('path-'+repr(name),lambda name=name:refusal(lambda:m.local(root,name)))
pin={'path':'regular','bytes':5,'sha256':hashlib.sha256(b'exact').hexdigest()}
test('exact-pin',lambda: (_ for _ in ()).throw(AssertionError('bytes')) if m.pinned(root,pin)!=b'exact' else None)
for name,change in [('changed-digest',{'sha256':'0'*64}),('changed-length',{'bytes':6}),('bool-length',{'bytes':True}),('unknown-pin-field',{'extra':True})]:
 test(name,lambda change=change:refusal(lambda:m.pinned(root,{**pin,**change})))
# Parent and descendant both hold stdout. EOF after group termination proves
# the descendant does not retain that output descriptor after parent reaping.
code="import subprocess,sys,time; child=subprocess.Popen([sys.executable,'-c','import time; time.sleep(300)']); print(child.pid,flush=True); time.sleep(300)"
p=subprocess.Popen([sys.executable,'-I','-B','-c',code],stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
selector=selectors.DefaultSelector();selector.register(p.stdout,selectors.EVENT_READ)
try:
 assert selector.select(5),'parent did not become ready'
 child=int(p.stdout.readline());m.terminate(p);assert p.returncode==-9
 assert selector.select(5),'descendant retained stdout'
 assert p.stdout.read()==b''
 rows.append({'case':'terminate-reaps-parent-and-closes-descendant-output','passed':True,'parentExit':p.returncode,'descendantPid':child})
 m.terminate(p)
 rows.append({'case':'terminate-already-reaped-group','passed':True})
finally:
 selector.close()
 if p.poll() is None:m.terminate(p)
 p.stdout.close();p.stderr.close()
result={'cases':rows,'passed':all(r['passed'] for r in rows),'scope':'Pure helper and real process-group behavior only; no selected registry/public positive activation.'};(B/'helper-controls.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'cases':len(rows),'passed':result['passed']}));assert result['passed']
