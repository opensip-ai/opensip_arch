from pathlib import Path
import json,hashlib,os,stat,sys,struct
A=Path('/Users/sb/code/opensip-ai/opensip_arch');P=A.parent/'opensip';B=Path(__file__).resolve().parent;sys.path.insert(0,str(P/'tools/quality'));from corpus import manifest_document
raw=(A/'docs/implementation/m3/corpus/t2-corpus-manifest.draft.json').read_bytes();assert hashlib.sha256(raw).hexdigest()=='c8cc48e1549a05e9d563728fcac776ceca6c2ba63fa2004779385bd2fa4b7578';m=manifest_document(raw);by_id={r['id']:r for r in m['repositories']};ids=m['counts']['tsjs']['medium']['devIds'];assert len(ids)==6 and all(by_id[i]['heldOut'] is False for i in ids)
base=A/'docs/implementation/m3/spikes/s-m-ts-cohort-2026-10-09/evidence';sealing=json.loads((A/'docs/implementation/m3/spikes/s-m-foundation-2026-10-09/sealing-results.json').read_text());previous={w['id']:w for w in sealing['workloads']};results=[]
def canonical(value):return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
for id_ in ids:
 inv=json.loads((base/f'{id_}-input-inventory.json').read_text());root=Path(inv['virtualRoot']);rows=[];excluded=[]
 for directory,dirs,files in os.walk(root,followlinks=False):
  for name in list(dirs):
   p=Path(directory)/name
   if p.is_symlink():excluded.append(dict(path=p.relative_to(root).as_posix(),kind='symlink-directory'));dirs.remove(name)
  for name in files:
   p=Path(directory)/name;info=p.lstat();rel=p.relative_to(root).as_posix()
   if not stat.S_ISREG(info.st_mode):excluded.append(dict(path=rel,kind='nonregular'));continue
   assert len(rel)<=4096 and all(0<len(s)<=255 and s not in ['.','..'] for s in rel.split('/')) and '\\' not in rel and '\0' not in rel
   fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC)
   with os.fdopen(fd,'rb')as f:
    before=os.fstat(f.fileno());assert (info.st_dev,info.st_ino)==(before.st_dev,before.st_ino);data=f.read();after=os.fstat(f.fileno());assert (before.st_size,before.st_mtime_ns,before.st_ctime_ns)==(after.st_size,after.st_mtime_ns,after.st_ctime_ns);assert len(data)==before.st_size
   rows.append(dict(path=rel,bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
 rows.sort(key=lambda r:r['path'].encode());excluded.sort(key=lambda r:r['path'].encode());assert rows==inv['files'] and excluded==inv['nonregularExcluded'];shape=previous[id_]['shape'];total=sum(r['bytes']for r in rows);inventory=canonical(rows);assert hashlib.sha256(inventory).hexdigest()==shape['inventoryDigest'] and len(inventory)==shape['inventoryCanonicalBytes'] and total==shape['totalRegularBytes']
 seed=hashlib.sha256(canonical(dict(prototype=id_))).hexdigest();descriptor=dict(schemaVersion=2,projectId='prj1-'+seed,sourceInventory=rows,resolvedConfigDigest=seed,scopeDigest=seed,vcsDigest=seed);encoded=canonical(descriptor);assert len(encoded)==shape['snapshotEquivalentDescriptorBytes'];framed=b'opensip.product.v1\0snapshot\0'+struct.pack('>Q',len(encoded))+encoded;assert hashlib.sha256(framed).hexdigest()==shape['snapshotEquivalentDigest']
 chunks=sum((r['bytes']+1048575)//1048576 for r in rows);node_modules=[r for r in rows if 'node_modules'in r['path'].split('/')]
 report=dict(id=id_,commit=by_id[id_]['commit'],heldOut=False,scope='REPOSITORY-ONLY ALL RETAINED REGULAR FILES; includes dependency fixture bytes tracked inT2; no separately acquired dependency tree',entries=len(rows),bytes=total,sourceInventoryDescriptorBytes=len(inventory),snapshotEquivalentDescriptorBytes=len(encoded),regularRows=rows,nonregularExcluded=excluded,pinnedNodeModulesFixtureRows=len(node_modules),pinnedNodeModulesFixtureBytes=sum(r['bytes']for r in node_modules),chunkMaxBytes=1048576,nonemptyContentChunks=chunks,zeroByteFiles=sum(r['bytes']==0 for r in rows),TS2EntriesWithin200000=len(rows)<=200000,snapshot2RowsWithin100000=len(rows)<=100000,snapshot2DescriptorWithin4194304=len(encoded)<=4194304,snapshot2BytesWithin8589934592=total<=8589934592,snapshotPlanIdentitiesAdmitted=False,wholeWorkspaceProfileSelected=False)
 results.append(report);print(id_,len(rows),total,len(encoded),'repository-only',flush=True)
(B/'results.json').write_text(json.dumps(dict(schemaVersion=1,standing='UNREVIEWED PRELIMINARY SM6 REPOSITORY-ONLY FIGURE COMPLETENESS CANDIDATE; NO PRODUCTION SOURCE ADMISSION',workloads=results,SM6FigureCompletenessProposed=True,SM6PlaceholderFilled=False,SMComplete=False,LG1Met=False,effectiveL=False,productQualification=False,dependencyTreeAcquired=False,repositoryCodeExecuted=False,heldOutSourceInspected=False),indent=2)+'\n')
assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
