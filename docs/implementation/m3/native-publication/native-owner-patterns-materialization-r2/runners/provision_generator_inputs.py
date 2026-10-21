from pathlib import Path
import os,json,hashlib,stat
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent; P=Path('/Users/sb/code/opensip-ai/opensip');W=P.parent/'opensip-native-owner-patterns-takeover'
closure=json.loads((W/'tools/contracts/generator-closure.json').read_text())
copied=[]
for row in closure['files']:
 target=W/row['path']
 if target.exists():
  raw=target.read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],row['path']
  continue
 assert not target.is_symlink()
 assert row['path'].startswith(('tools/contracts/node_modules/','tools/contracts/python-packages/')),row['path']
 source=P/row['path'];info=source.lstat();assert stat.S_ISREG(info.st_mode)
 raw=source.read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],row['path']
 target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw);copied.append(row)
(F/'generator-input-provisioning.json').write_text(json.dumps(dict(copied=copied,all352InputsVerified=True,previousAttemptCopiedNodeInputsBeforeMissingPythonDirectoryRefusal=True,networkUsed=False,selectedClosureUnchanged=True),indent=2)+'\n')
print('copied',len(copied),'exact selected missing inputs')
