from pathlib import Path,PurePosixPath
import os,json,hashlib,tarfile,shutil,posixpath
B=Path(__file__).resolve().parent;commit='f2d3ce0bd7f24a49f8f72d9000448f8838c4e850';archive=B/f'cargo-{commit}.tar.gz';original=B/'original';assert not original.exists()or not list(original.iterdir());original.mkdir(exist_ok=True);raw=archive.read_bytes();members=[]
with tarfile.open(archive,'r:gz')as t:
 for m in t.getmembers():
  p=PurePosixPath(m.name);assert p.parts[0]=='cargo-'+commit and not p.is_absolute() and '..'not in p.parts;assert m.isfile()or m.isdir()or m.issym(),(m.name,m.type)
  if m.issym():
   target=PurePosixPath(posixpath.normpath(posixpath.join(str(p.parent),m.linkname)));assert not PurePosixPath(m.linkname).is_absolute()and target.parts[0]=='cargo-'+commit and '..'not in target.parts,(m.name,m.linkname)
  members.append(m)
 t.extractall(original,members=members,filter='data')
root=original/('cargo-'+commit);rows=[];links=[]
for p in sorted(root.rglob('*')):
 if p.is_symlink():
  assert p.resolve().is_relative_to(root.resolve());links.append(dict(path=p.relative_to(root).as_posix(),target=os.readlink(p)));continue
 if p.is_file():b=p.read_bytes();rows.append(dict(path=p.relative_to(root).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
receipts=[]
for family in ['native-registry-alias-source-r1','native-config-carrier-source-r1','native-compiler-runtime-source-r1','native-package-download-source-r1']:
 base=B.parent/family
 for p in sorted(base.rglob('*.rs')):
  rel=p.relative_to(base);assert (root/rel).is_file();assert p.read_bytes()==(root/rel).read_bytes(),str(rel);receipts.append(dict(originalReceipt=str(p),path=rel.as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
assert len(receipts)>=10
candidate=B/'compatible-producer';assert not candidate.exists();shutil.copytree(root,candidate,symlinks=True)
report=dict(standing='UNREVIEWED PINNED UPSTREAM SOURCE PREPARATION; no producer build/profile/Tool/admission',upstreamCommit=commit,url=f'https://codeload.github.com/rust-lang/cargo/tar.gz/{commit}',archive=dict(path=str(archive),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()),originalRoot=str(root),candidateRoot=str(candidate),files=rows,internalSymlinks=links,matchedEarlierPrimarySourceReceipts=receipts,repositorySourceExecuted=False,cargoRun=False,sourceProfilePublished=False,actualNativeWorker=False,sourceAdmissionImplemented=False,productQualification=False)
(B/'source-receipt.json').write_text(json.dumps(report,indent=2)+'\n');print('Retained complete source tree:',len(rows),'regular files,',len(links),'validated internal symlinks;',len(receipts),'earlier exact primary-source copies match; isolated producer preparation ready.')
