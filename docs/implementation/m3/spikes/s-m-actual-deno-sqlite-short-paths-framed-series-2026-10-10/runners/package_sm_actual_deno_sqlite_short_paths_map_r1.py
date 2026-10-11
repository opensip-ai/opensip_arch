from pathlib import Path
import json,hashlib,tarfile,lzma,io,shutil
# The 125374162-byte map exceeds the 100 MiB per-file limit of the architecture repository's remote.
# Store it as a deterministic xz tar (LFS-tracked by docs/implementation/**/*.tar.xz); inner bytes and pin unchanged.
B=Path('/tmp/opensip-implementation');D=B/'sm-actual-deno-sqlite-short-paths-framed-series-r1-draft';C=Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06')
raw_path=D/'original-inputs/27/sourceMap.bin';raw=raw_path.read_bytes();src=json.loads((D/'draft-source.json').read_bytes())
receipt=json.loads((D/'receipts/actual-deno-sqlite-short-paths-source-map-r1.json').read_bytes())['results'][0]['sourceMap'];assert len(raw)==receipt['bytes'] and hashlib.sha256(raw).hexdigest()==receipt['sha256']
buf=io.BytesIO()
with tarfile.open(fileobj=buf,mode='w',format=tarfile.USTAR_FORMAT) as t:
 info=tarfile.TarInfo('sourceMap.bin');info.size=len(raw);info.mtime=0;info.mode=0o444;info.uid=info.gid=0;info.uname=info.gname='';t.addfile(info,io.BytesIO(raw))
packed=lzma.compress(buf.getvalue(),format=lzma.FORMAT_XZ,check=lzma.CHECK_CRC64,preset=6)
out=D/'original-inputs/27/sourceMap.bin.tar.xz';assert not out.exists();out.write_bytes(packed)
with tarfile.open(out,mode='r:xz') as t:
 members=t.getmembers();assert [m.name for m in members]==['sourceMap.bin'];assert t.extractfile(members[0]).read()==raw
raw_path.unlink()
src.update(sourceMapStoredAs='original-inputs/27/sourceMap.bin.tar.xz',sourceMapArchiveBytes=len(packed),sourceMapArchiveSha256=hashlib.sha256(packed).hexdigest(),sourceMapInnerBytes=len(raw),sourceMapInnerSha256=receipt['sha256'],sourceMapPackedBecauseRemoteFileLimit=True)
(D/'draft-source.json').write_text(json.dumps(src,indent=2)+'\n')
r=(D/'REPORT.md').read_text();r=r.rstrip('\n')+f"\n\nThe 125374162-byte prepared map exceeds the architecture remote's 100 MiB per-file limit, so the subject stores it as `original-inputs/27/sourceMap.bin.tar.xz` ({len(packed)} bytes): a deterministic USTAR/xz archive with one member, `sourceMap.bin`, whose bytes keep SHA-256 `{receipt['sha256']}`.\n";(D/'REPORT.md').write_text(r)
shutil.copyfile(Path(__file__),D/'runners'/Path(__file__).name)
P=C/'continuation-preserved'/D.name;shutil.rmtree(P);shutil.copytree(D,P)
print(len(packed),hashlib.sha256(packed).hexdigest())
