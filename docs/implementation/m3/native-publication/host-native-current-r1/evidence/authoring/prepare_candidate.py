from pathlib import Path
import subprocess,os,json,shutil,hashlib
B=Path(__file__).resolve().parent;P=Path('/Users/sb/code/opensip-ai/opensip');W=P.parent/'opensip-host-native-current';E=dict(os.environ,GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
for k in ['GIT_CONFIG_COUNT','GIT_DIR','GIT_WORK_TREE']:E.pop(k,None)
assert not W.exists();head=subprocess.check_output(['/usr/bin/git','rev-parse','HEAD'],cwd=P,env=E).decode().strip();assert head=='366fe49fc60a0899e36a5461e176758a2e9ec5e7'
subprocess.run(['/usr/bin/git','worktree','add','--detach',str(W),head],cwd=P,env=E,check=True)
paths=[]
for root in [B/'pooled-candidates',B/'native-context-candidate']:
 for f in sorted(root.glob('*-fixtures.current.json')):
  rel='crates/host/tests/fixtures/'+f.name;assert not(W/rel).exists();shutil.copyfile(f,W/rel);paths.append(rel)
assert len(paths)==10
p=W/'crates/host/src/native_owner_tests.rs';before=p.read_bytes();text=p.read_text();changes=[]
for rel in paths:
 new=Path(rel).name;old=new.replace('.current.json','.json');count=text.count(old);assert count>0,old;text=text.replace(old,new);changes.append(dict(original=old,current=new,includes=count))
p.write_text(text);assert(P/'crates/host/src/native_owner_tests.rs').read_bytes()==before
report=dict(standing='ISOLATED UNREVIEWED CURRENT NATIVE COMPANIONS; NO RUNTIME PASS YET',productBase=head,worktree=str(W),newFiles=paths,includeChanges=changes,historicalDocumentsModified=False,guardModified=False,inventoryPrepared=False)
(B/'candidate-preparation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
