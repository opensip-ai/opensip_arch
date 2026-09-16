"""Retain only the actual completed public application review; never apply."""
from pathlib import Path
import hashlib,json,sys,importlib.util
B=Path('/tmp/opensip-design-corrections');S=B/'application-stage.v45.2';R=B/'application-review.v45';L=Path('/Users/sb/code/opensip-ai/opensip_arch');H=S/'support';O=Path(__file__).parent
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
c=load(R/'process-completion.json');assert c['exitCode']==0
result=load(R/'result.json');assert result['is_error'] is False
excluded=load(B/'root-application-origin-preparation.v1/excluded-origins.v1.json')['sessionIds'];sid=result['session_id'];assert sid not in excluded
process=load(R/'process.json');assert '--resume' not in process['command'];assert sha(R/'prompt.md')==process['promptSha256']
events=(R/'public-events.jsonl').read_text();init=[json.loads(s) for s in events.splitlines() if json.loads(s).get('type')=='system'];assert len(init)==1 and init[0]['session_id']==sid and init[0]['model']=='claude-opus-5'
sys.path.insert(0,str(H));sp=importlib.util.spec_from_file_location('actual_application_retainer',H/'retain-application-review.successor.v1.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
bound=load(B/'application45-review-binding.v1/bound-review-receipt.json')
receipt=m.run_retain(root=L,stage=S,version='v45',bound=bound,src=R,claude_log_text=events)
dest=Path(receipt['dest']);custody=load(dest/('codex-retention-custody.json' if (dest/'codex-retention-custody.json').exists() else 'custody.json'))
for row in custody['files']:
 p=dest/row['path'];assert sha(p)==row['sha256'] and p.stat().st_size==row['bytes']
assert sha(dest/custody['toolBlocks']['path'])==custody['toolBlocks']['sha256']
report={'standing':'Actual completed fresh Claude application review retained from public-only launch events; all retained custody rows verified. Substantive root assessment remains separate.','receipt':receipt,'reviewSha256':sha(dest/'review.json'),'custodySha256':sha(dest/('codex-retention-custody.json' if (dest/'codex-retention-custody.json').exists() else 'custody.json')),'allRetainedRowsVerified':len(custody['files']),'actualPublicEventsSource':str(R/'public-events.jsonl'),'publicEventsSha256':sha(R/'public-events.jsonl'),'privateSessionLogsRead':False,'freshOriginExclusions':excluded,'passed':True}
(O/'retention-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
