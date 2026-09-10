"""Continue a genuinely fresh-origin review without relabelling a coauthor."""
from pathlib import Path
import argparse,json,hashlib,subprocess,datetime,importlib.util
p=argparse.ArgumentParser();p.add_argument('--origin',type=Path,required=True);p.add_argument('--previous',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--role',choices=['blind-consumer','independent-design-review','independent-application-review'],required=True);p.add_argument('--max-turns',type=int,default=120);p.add_argument('--reasoning-effort',choices=['high'],default='high');a=p.parse_args();assert 1 <= a.max_turns <= 240
origin=a.origin.resolve();previous=a.previous.resolve();out=a.out.resolve();proc=json.loads((origin/'process.json').read_text());prior=json.loads((previous/'response.raw.json').read_text())
assert proc['freshSession'] is True and '--resume' not in proc['command']
assert 'coauthor' not in proc.get('standing','').lower()
first=json.loads((origin/'response.raw.json').read_text());session=first['sessionId']
helper=Path(__file__).parent/'public-review-response.v1.py'
espec=importlib.util.spec_from_file_location('public_review_response',helper); E=importlib.util.module_from_spec(espec); espec.loader.exec_module(E)
public_prior,prior_status=E.observed_response(prior,session)
if prior_status=='usage-balance-exhausted':
    # Exact partial-error custody must already exist; no forged end_turn or SID.
    live=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews')/previous.name
    assert json.loads((live/'response.public.json').read_text())==public_prior
    account=json.loads((live/'session-account.json').read_text())
    assert account['completed'] is False and account['observedStatus']=='usage-balance-exhausted'
    assert account['sessionId']==session and account['privateFieldsRetained'] is False
    assert (live/'process.json').read_bytes()==(previous/'process.json').read_bytes()
    assert Path(account['freshOrigin']['path']).resolve()==origin
    assert account['freshOrigin']['processSha256']==hashlib.sha256((origin/'process.json').read_bytes()).hexdigest()
else:
    assert prior_status in ('end_turn','cancelled')
assert out.is_dir() and (out/'prompt.txt').is_file() and not (out/'process.json').exists()
cwd=proc['command'][proc['command'].index('--cwd')+1]
command=['/Users/sb/.grok/bin/grok','--cwd',cwd,'--resume',session,'--permission-mode','acceptEdits','--no-subagents','--disable-web-search','--reasoning-effort',a.reasoning_effort,'--max-turns',str(a.max_turns),'--output-format','json','--prompt-file',str(out/'prompt.txt')]
with (out/'response.raw.json').open('xb') as stdout,(out/'stderr.log').open('xb') as stderr:child=subprocess.Popen(command,stdout=stdout,stderr=stderr,start_new_session=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
(out/'process.json').write_text(json.dumps({'pid':child.pid,'command':command,'startedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sessionId':session,'freshSession':False,'freshOrigin':{'path':str(origin),'processSha256':sha(origin/'process.json'),'sessionId':session},'previousContinuation':str(previous),'previousObservedStatus':prior_status,'publicResponseGuardSha256':sha(helper),'standing':'Actual Grok '+a.role+' continuation of verified fresh review origin; not a new session or automatic acceptance.'},indent=2)+'\n');print(child.pid)
