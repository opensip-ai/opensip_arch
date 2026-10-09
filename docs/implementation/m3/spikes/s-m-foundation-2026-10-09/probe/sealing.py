from pathlib import Path
import os,sys,json,hashlib,struct,time,stat
root=Path(sys.argv[1]);label=sys.argv[2];start=time.monotonic_ns();rows=[];excluded=[];total=0
for directory,dirs,files in os.walk(root,followlinks=False):
 for name in list(dirs):
  p=Path(directory)/name
  if p.is_symlink():excluded.append(dict(path=str(p.relative_to(root)),kind='symlink-directory'));dirs.remove(name)
 for name in files:
  p=Path(directory)/name;info=p.lstat();rel=str(p.relative_to(root))
  if not stat.S_ISREG(info.st_mode):excluded.append(dict(path=rel,kind='nonregular'));continue
  h=hashlib.sha256();fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC)
  with os.fdopen(fd,'rb') as f:
   before=os.fstat(f.fileno());assert (info.st_dev,info.st_ino)==(before.st_dev,before.st_ino)
   while chunk:=f.read(1024*1024):h.update(chunk)
   after=os.fstat(f.fileno());assert (before.st_size,before.st_mtime_ns,before.st_ctime_ns)==(after.st_size,after.st_mtime_ns,after.st_ctime_ns)
  rows.append(dict(path=rel,sha256=h.hexdigest(),bytes=info.st_size));total+=info.st_size
rows.sort(key=lambda r:r['path'].encode('utf-8'));excluded.sort(key=lambda r:r['path'].encode('utf-8'))
def can(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def digest(v):return hashlib.sha256(can(v)).hexdigest()
def framed(domain,raw):return b'opensip.product.v1\0'+domain.encode('ascii')+b'\0'+struct.pack('>Q',len(raw))+raw
# Fixed synthetic reference hashes are timing inputs, not admitted records.
seed=digest(dict(prototype=label));snapshot=dict(schemaVersion=2,projectId='prj1-'+seed,sourceInventory=rows,resolvedConfigDigest=seed,scopeDigest=seed,vcsDigest=seed);snapshotRaw=can(snapshot);snapshotFramed=framed('snapshot',snapshotRaw);snapshotDigest=hashlib.sha256(snapshotFramed).hexdigest()
plan=dict(schemaVersion=2,snapshotId='snapshot2:'+snapshotDigest,capabilityManifestId=seed,semanticClosures=[],analysisSpecDigest=seed,resolvedConfigDigest=seed,nativeContextDigests=[],importIds=[],policyDigest=seed,waiverDigest=seed,scopeDigest=seed,budget=dict(unit='work-units',limit=1),semanticGrantDigest=seed,capabilityManifestBytesDigest=seed);planRaw=can(plan);planDigest=hashlib.sha256(framed('plan',planRaw)).hexdigest();elapsed=time.monotonic_ns()-start
print(json.dumps(dict(id=label,elapsedNanos=elapsed,regularInventoryRows=len(rows),totalRegularBytes=total,inventoryCanonicalBytes=len(can(rows)),snapshotEquivalentDescriptorBytes=len(snapshotRaw),planEquivalentDescriptorBytes=len(planRaw),inventoryDigest=digest(rows),snapshotEquivalentDigest=snapshotDigest,planEquivalentDigest=planDigest,nonregularExcluded=excluded,bounds=dict(snapshotRowsWithin100000=len(rows)<=100000,snapshotDescriptorWithin4194304=len(snapshotRaw)<=4194304,totalWithin8589934592=total<=8589934592,tsSnapshotEntriesWithin200000=len(rows)<=200000,tsChunkBound1048576=1048576),referenceRecordsSynthetic=True,identityAdmissionClaimed=False,SM5PlaceholderFilled=False,SM6PlaceholderFilled=False),sort_keys=True))
