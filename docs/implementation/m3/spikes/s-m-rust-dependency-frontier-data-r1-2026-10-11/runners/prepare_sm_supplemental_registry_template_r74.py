from pathlib import Path
import os,json,hashlib,re,stat
os.setpriority(os.PRIO_PROCESS,0,10)
B=Path('/tmp/opensip-implementation');D=B/'sm-experimental-dependency-preparation-2026-10-10';base=json.loads((D/'registry-intake-template-r73.json').read_bytes());receipt=json.loads((D/'parameterized-public-intake-r73.json').read_bytes());assert receipt['exitCode']==0 and receipt['outcome']['success'];supp=Path(receipt['root']);additional=json.loads((supp/'intake.json').read_bytes());assert additional['archives']==71 and additional['versionRecords']==71 and additional['sourceAuthentication'] is False
source=Path(base['templateRoot']);dest=source.parent/'registry-intake-template-r74';assert not dest.exists();dest.mkdir(mode=0o700);rows={r['path']:dict(r,sourcePath=str(source/r['path']),provenance='Original checked raw template') for r in base['files']};overlaps=[]
expected={}
for p in (D/'missing-public-index-inputs-r73').glob('*.jsonl'):
 for line in p.read_bytes().splitlines():
  r=json.loads(line);expected[r['name']+'-'+r['vers']+'.crate']=r['cksum']
for r in additional['files']:
 rel=r['path'];old=rows.get(rel)
 if old:
  if rel.startswith('cache/'):
   assert old['bytes']==r['bytes'] and old['sha256']==r['sha256'];overlaps.append(dict(path=rel,action='Identical archive bytes retained once in this experimental copy',oldPin={k:old[k] for k in ['bytes','sha256']},newPin={k:r[k] for k in ['bytes','sha256']}))
  else:overlaps.append(dict(path=rel,action='Explicit newer anonymous public index bytes replace only this named experimental cache slot',oldPin={k:old[k] for k in ['bytes','sha256']},newPin={k:r[k] for k in ['bytes','sha256']}))
 rows[rel]=dict(r,sourcePath=str(supp/'registry'/rel),provenance='New anonymous public input checked by stock cache-intake control')
for rel,row in sorted(rows.items()):
 if rel.startswith('cache/') and Path(rel).name in expected:assert row['sha256']==expected[Path(rel).name]
 path=Path(row['sourcePath']);fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  a=os.fstat(fd);assert stat.S_ISREG(a.st_mode)
  with os.fdopen(fd,'rb',closefd=False) as f:raw=f.read()
  z=os.fstat(fd);assert(a.st_dev,a.st_ino,a.st_size,a.st_mtime_ns,a.st_ctime_ns)==(z.st_dev,z.st_ino,z.st_size,z.st_mtime_ns,z.st_ctime_ns)
 finally:os.close(fd)
 assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'];out=dest/rel;out.parent.mkdir(parents=True,exist_ok=True);fd=os.open(out,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o444)
 with os.fdopen(fd,'wb') as f:f.write(raw)
 assert out.read_bytes()==raw
result=dict(standing='UNREVIEWED SUPPLEMENTAL RAW CACHE COPY FOR FUTURE EXPERIMENT, NOT USED FOR CORPUS YET',originalTemplate=str(D/'registry-intake-template-r73.json'),newIntakeControl=str(supp/'intake.json'),templateRoot=str(dest),files=[dict(path=rel,bytes=r['bytes'],sha256=r['sha256'],sourcePath=r['sourcePath'],provenance=r['provenance']) for rel,r in sorted(rows.items())],overlaps=overlaps,bytes=sum(r['bytes'] for r in rows.values()),archiveFiles=sum(rel.startswith('cache/') for rel in rows),indexFiles=sum(rel.startswith('index/') for rel in rows),expandedSourcesCopied=False,sourceAuthentication=False,corpusResolutionRun=False,nativeAdmission=False,SMComplete=False)
(D/'registry-intake-template-r74.json').write_text(json.dumps(result,indent=2)+'\n');print({'templateFiles':len(rows),'bytes':result['bytes'],'archiveFiles':result['archiveFiles'],'indexFiles':result['indexFiles'],'explicitOverlaps':len(overlaps),'corpusResolutionRun':False})
