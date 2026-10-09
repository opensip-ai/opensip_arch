from pathlib import Path
import json,hashlib,os,stat
B=Path(__file__).resolve().parent;r=json.loads((B/'results.json').read_text());summaries=[]
for w in r['workloads']:
 inventory=json.loads((B/'evidence'/f"{w['id']}-input-inventory.json").read_text());root=Path(inventory['virtualRoot']);assert root.parts[:5]==('/','Users','sb','code','.opensip-implementation-cache')and root.parts[5:7]==('t2-corpus-c8cc48e1','store');allowed={str(root/row['path']):row for row in inventory['files']};allowed.update({row['path']:row for row in inventory['libraries']});paths=set()
 for q in w['runs']:
  observed=json.loads(Path(q['stdout']).read_text());assert set(observed['readPaths'])<=allowed.keys();paths.update(observed['readPaths'])
 utf8bytes=0;boms=[]
 for name in sorted(paths):
  row=allowed[name];p=Path(name);info=p.lstat();assert stat.S_ISREG(info.st_mode);fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC)
  with os.fdopen(fd,'rb')as f:
   before=os.fstat(f.fileno());assert(info.st_dev,info.st_ino)==(before.st_dev,before.st_ino);raw=f.read();after=os.fstat(f.fileno());assert(before.st_size,before.st_mtime_ns,before.st_ctime_ns)==(after.st_size,after.st_mtime_ns,after.st_ctime_ns)
  assert len(raw)==row['bytes']and hashlib.sha256(raw).hexdigest()==row['sha256'];raw.decode('utf8','strict');assert not raw.startswith((b'\xff\xfe',b'\xfe\xff'));utf8bytes+=len(raw)
  if raw.startswith(b'\xef\xbb\xbf'):boms.append(name)
 summaries.append(dict(id=w['id'],distinctActualReadPaths=len(paths),allReadPathsInExactSealedOrCompilerInventory=True,allReobservedHashesMatched=True,allActuallyReadBytesValidUtf8=True,utf8ReadBytes=utf8bytes,utf8BomPaths=boms,utf16ActualReadPaths=0))
(B/'readset-audit.json').write_text(json.dumps(dict(standing='UNREVIEWED READONLY CURRENT SELECTED DEV INPUT AUDIT; NO GENERAL ENCODING OR SECURITY ADMISSION CLAIM',workloads=summaries,heldOutSourceInspected=False,repositoryCodeExecuted=False),indent=2)+'\n');print(json.dumps(summaries,indent=2))
