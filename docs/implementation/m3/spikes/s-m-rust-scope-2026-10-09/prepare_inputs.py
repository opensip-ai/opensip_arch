from pathlib import Path
import json,hashlib,sys,stat,os,struct,importlib.util
B=Path(__file__).resolve().parent;A=Path('/Users/sb/code/opensip-ai/opensip_arch');P=A.parent/'opensip';C=Path('/Users/sb/code/.opensip-implementation-cache');sys.path.insert(0,str(P/'tools/quality'));from corpus import manifest_document;from store import verify
raw=(A/'docs/implementation/m3/corpus/t2-corpus-manifest.draft.json').read_bytes();assert hashlib.sha256(raw).hexdigest()=='c8cc48e1549a05e9d563728fcac776ceca6c2ba63fa2004779385bd2fa4b7578'
m=manifest_document(raw);entries={r['id']:r for r in m['repositories']};medium=m['counts']['rust']['medium']['devIds'];large=['rs-large-smithy-rs','poly-large-rspack','poly-very-large-deno'];ids=medium+large;assert len(set(ids))==10 and all(entries[i]['heldOut']is False for i in ids)
accepted=json.loads(Path('/tmp/opensip-implementation/sm-sealing-typed-2026-10-09/results.json').read_text());prepared={w['id']:w['shape']['regularRows']for w in accepted['workloads']};template=json.loads(Path('/tmp/opensip-implementation/sm-sealing-typed-2026-10-09/control-template.json').read_text())['snapshot'];vectors=json.loads((A/'docs/implementation/m3/native-successors-fa/rust3-lim/evidence/vectors.json').read_text());keys=vectors['stageRequestV3ByReference']['analysisDomain']['requestedCoverageDomain'];spec=importlib.util.spec_from_file_location('codec',B/'scope_codec.py');codec=importlib.util.module_from_spec(spec);spec.loader.exec_module(codec)
def inventory(root):
 rows=[];excluded=[]
 for directory,dirs,files in os.walk(root,followlinks=False):
  for name in list(dirs):
   path=Path(directory)/name
   if path.is_symlink():excluded.append(path.relative_to(root).as_posix());dirs.remove(name)
  for name in files:
   p=Path(directory)/name;before=p.lstat();rel=p.relative_to(root).as_posix()
   if not stat.S_ISREG(before.st_mode):excluded.append(rel);continue
   fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC);h=hashlib.sha256()
   with os.fdopen(fd,'rb')as f:
    opened=os.fstat(f.fileno());assert (before.st_dev,before.st_ino)==(opened.st_dev,opened.st_ino)
    while chunk:=f.read(1048576):h.update(chunk)
    after=os.fstat(f.fileno());assert (opened.st_size,opened.st_mtime_ns,opened.st_ctime_ns)==(after.st_size,after.st_mtime_ns,after.st_ctime_ns)
   rows.append(dict(path=rel,sha256=h.hexdigest(),bytes=opened.st_size))
 return sorted(rows,key=lambda r:r['path'].encode()),sorted(excluded)
reports=[]
for i in ids+['mr-rs-medium-serde-json']:
 if i in prepared:rows=prepared[i];excluded=[];source='new typed sealing prepared regular rows; see its exact nonregular excluded lists'
 else:
  root=C/'t2-corpus-c8cc48e1/store'/entries[i]['treeDigest']['value'];proof=verify(root,entries[i]);rows,excluded=inventory(root);source='verified T2 development regular tree, no-follow source enumeration'
 snap=dict(template,sourceInventory=rows);sr=json.dumps(snap,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode();sid='snapshot2:'+hashlib.sha256(b'opensip.product.v1\0snapshot\0'+struct.pack('>Q',len(sr))+sr).hexdigest();manifest=[dict(kind='file',path=r['path'],byteLength=r['bytes'],contentSha256=r['sha256'])for r in rows];subjects=codec.derive(sid,manifest);scope=codec.commitment('opensip.rust-provider.subject-scope.v2',subjects);domain=[dict(k,subjectScopeCommitment=scope)for k in keys];packet=dict(standing='UNREVIEWED SYNTHETIC SNAPSHOT/ILLUSTRATIVE REQUEST KEY PREIMAGE; NOT ACCEPTED TRANSPORT MANIFEST OR C2 VALUE',id=i,snapshotId=sid,manifestEntries=manifest,requestedCoverageDomain=domain,source=source,nonregularExcluded=excluded,heldOut=False,subjectCount=len(subjects),scopeCommitment=scope,SM12FigureComplete=False,SM14FigureComplete=False,sourceAdmissionClaimed=False);(B/(i+'-input.json')).write_text(json.dumps(packet,indent=2)+'\n');reports.append(dict(id=i,subjectCount=len(subjects),regularRows=len(rows),snapshotEquivalentId=sid))
(B/'inputs.json').write_text(json.dumps(dict(standing='UNREVIEWED11DEVREADSET SCOPE PREPARATION, SUI CONDITIONAL NOT MEASURED',workloads=reports,sourceManifestSha256=hashlib.sha256(raw).hexdigest(),actualAcceptedTransportManifest=False,actualNativeWorker=False,coverageKeysValidatedC2Values=False,SM12FigureComplete=False,SM14FigureComplete=False),indent=2)+'\n');print(json.dumps(reports,indent=2))
