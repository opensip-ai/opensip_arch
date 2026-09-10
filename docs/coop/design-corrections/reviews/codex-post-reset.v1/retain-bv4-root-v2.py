from pathlib import Path
import hashlib,json,os,shutil
root=Path.cwd();ev=root/'docs/coop/design-corrections/reviews/codex-post-reset.v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
mp=root/'docs/coop/design-corrections/reviews/candidate-subject.v13.json';assert sha(mp)=='8e6670f74d6e0bbed50b6c4914b3c7b29f627221f1591f4add5567f652f4c023'
m=json.loads(mp.read_text());base={r['path']:r for r in m['files']}
for name in ['bv4-final-source-recheck.v2','bv4-public-recheck.v2']:
 src=Path('/tmp/opensip-design-corrections')/name;dest=ev/name;assert not dest.exists();dest.mkdir();captured=[];account=None
 if (src/'work').is_dir():
  files={str(p.relative_to(src/'work')):p for p in (src/'work').rglob('*') if p.is_file()}
  assert files.keys()==base.keys();same=[];changed=[]
  for rel,p in files.items():
   r={'path':rel,'sha256':sha(p),'bytes':p.stat().st_size,'beforeSha256':base[rel]['sha256']}
   if r['sha256']==base[rel]['sha256'] and r['bytes']==base[rel]['bytes']:same.append(rel)
   else:changed.append(r);captured.append(p)
  assert len(changed)==14
  account={'baseManifestSha256':sha(mp),'unchangedFiles':sorted(same),'changedFiles':sorted(changed,key=lambda r:r['path']),'addedFiles':[],'deletedFiles':[]}
 for directory,dirs,names in os.walk(src):
  dp=Path(directory)
  if dp==src and 'work' in dirs:dirs.remove('work')
  captured.extend(dp/n for n in names)
 rows=[]
 for p in sorted(captured):
  assert not p.is_symlink();q=dest/p.relative_to(src);q.parent.mkdir(parents=True,exist_ok=True);before=sha(p);shutil.copyfile(p,q);assert before==sha(q)==sha(p)
  rows.append({'path':str(q.relative_to(dest)),'sha256':sha(q),'bytes':q.stat().st_size})
 if account:(dest/'source-copy-account.json').write_text(json.dumps(account,indent=2)+'\n')
 (dest/'custody.json').write_text(json.dumps({'standing':'Root assessment diagnostics on released actual-Claude v2; not independent acceptance, host execution or qualification. Existing source copy retains only one root fixture extraction beyond released v2. Original report outcome labels and limits preserved.','source':str(src),'files':rows,'sourceCopyAccount':({'path':'source-copy-account.json','sha256':sha(dest/'source-copy-account.json')} if account else None)},indent=2)+'\n')
 print(name,len(rows),'retained files')
src=Path(__file__).parent/'bv4-author-v2-source-diffs';dest=ev/src.name;assert not dest.exists();shutil.copytree(src,dest)
print('Retained all ten exact source diffs and their hash index.')
