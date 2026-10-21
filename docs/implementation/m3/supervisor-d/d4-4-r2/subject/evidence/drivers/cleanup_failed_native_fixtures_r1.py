from pathlib import Path
import json,hashlib,shutil,os
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;rows=json.loads((F/'failed-fixture-cleanup-audit-r1.json').read_bytes());assert len(rows)==4
B=F/'preserved-native-fixture-validation-r2';B.mkdir(exist_ok=False)
for row in rows:
 p=Path(row['path']);assert p.parent.name=='n-c3uzpaz7'and p.name.startswith('opensip-d4-')and p.stat().st_uid==os.getuid()and not p.is_symlink()
 assert sorted(x.name for x in p.iterdir())==['components','release.tar']and not(p/'components').is_symlink()and not list((p/'components').iterdir())
 b=(p/'release.tar').read_bytes();assert len(b)==row['archiveBytes']and hashlib.sha256(b).hexdigest()==row['archiveSha256']
if rows:shutil.copyfile(Path(rows[0]['path'])/'release.tar',B/'release.tar')
for row in rows:shutil.rmtree(row['path']);assert not Path(row['path']).exists()
(B/'cleanup.json').write_text(json.dumps(dict(removed=rows,archivePreserved=True,scope='Only four exact task-owned preinstall fixtures with empty stores, no generation and byte-exact public fixture archive; parent temp/worktrees and other paths untouched.'),indent=2)+'\n');print('Preserved public fixture archive and removed4verified task-owned failed preinstall scratch directories.')
