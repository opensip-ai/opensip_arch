from pathlib import Path
import subprocess,os,signal,json,time
F=Path(__file__).parent;O=F/'lane-r1';r=json.loads((O/'report.json').read_text());exe=None
for line in (O/'candidate-artifacts.jsonl').read_text().splitlines():
 j=json.loads(line)
 if j.get('reason')=='compiler-artifact' and j['target']['name']=='opensip_host' and j['profile']['test']:
  assert j['fresh'];exe=j['executable']
assert exe
rows={}
for line in subprocess.check_output(['/bin/ps','-ax','-o','pid=,ppid=,command='],text=True).splitlines():
 parts=line.strip().split(None,2)
 if len(parts)==3:rows[int(parts[0])]=(int(parts[1]),parts[2])
owned=[(pid,ppid,cmd) for pid,(ppid,cmd) in rows.items() if cmd.split()[0]==exe and str(F/'lane.py') in rows.get(ppid,(-1,''))[1]]
assert len(owned)<=1,owned
record=dict(standing='INVALID CANDIDATE BUILD: SHARED TARGET REUSED BASELINE IMAGE; NO CANDIDATE VALIDATION CLAIM',baselineValid=True,baselineReport=str(O/'report.json'),candidateDiscarded=True,candidateArtifactFreshFlag=True,reason='candidate image lacks both new tests; target shared across earlier-mtime worktrees',ownedProcessCancelled=owned)
(F/'invalid-shared-target-candidate.json').write_text(json.dumps(record,indent=2)+'\n')
for pid,ppid,cmd in owned:
 assert not any(parent==pid for parent,_ in rows.values()),'candidate host still owns a child; refuse cancellation'
 os.kill(pid,signal.SIGTERM)
print(json.dumps(record,indent=2))
