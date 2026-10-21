from pathlib import Path
import os,json,hashlib,stat
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;P=Path('/Users/sb/code/opensip-ai/opensip');W=P.parent/'opensip-native-owner-patterns-takeover'
registry=json.loads((W/'tools/typescript-lanes.json').read_text());copied=[]
for row in registry['files']:
 target=W/row['path']
 if target.exists():
  raw=target.read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],row['path'];continue
 assert '/node_modules/' in row['path'] and not target.is_symlink()
 source=P/row['path'];assert stat.S_ISREG(source.lstat().st_mode);raw=source.read_bytes()
 assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],row['path']
 target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw);target.chmod(source.stat().st_mode&0o777);copied.append(row)
(F/'typescript-input-provisioning.json').write_text(json.dumps(dict(filesVerified=len(registry['files']),copied=copied,networkUsed=False,selectedRegistryUnchanged=True),indent=2)+'\n');print('verified',len(registry['files']),'copied',len(copied))
