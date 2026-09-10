"""Strict public-only custody for the explicitly authorized target-identity design coauthor.
No blind/independent review standing is assigned. Reuses the checked public selector.
"""
from pathlib import Path
from urllib.parse import quote
import hashlib,json,shutil,sys
B=Path('/tmp/opensip-design-corrections');N='grok-target-identity-design-options.v1';S=B/N
D=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews')/N
assert not D.exists()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(S/'input-manifest.json')=='1fd136a131abd5f1b72348e19df831fec38f1c5cc083f26cc9d18908c1968388'
for r in json.loads((S/'input-manifest.json').read_text())['files']:
 p=S/r['path'];assert p.resolve().is_relative_to(S.resolve())
 assert sha(p)==r['sha256'] and p.stat().st_size==r['bytes']
proc=json.loads((S/'process.json').read_text());assert proc['freshSession'] is True and '--resume' not in proc['command']
raw=json.loads((S/'response.raw.json').read_text());assert raw['stopReason']=='end_turn'
assert (S/'stderr.log').stat().st_size==0
prompt=(S/'prompt.txt').read_text();assert 'NEW DESIGN COAUTHOR' in prompt
cwd=Path(proc['command'][proc['command'].index('--cwd')+1]).resolve()
up=Path('/Users/sb/.grok/sessions')/quote(str(cwd),safe='')/raw['sessionId']/'updates.jsonl'
sys.path.insert(0,str(B/'application-successor-root.v1'))
import retain_public as P
public,account=P.public_grok_update_blocks(up.read_text(),raw['sessionId'],prompt.strip())
safe={k:raw[k] for k in ('text','stopReason','sessionId','requestId','usage','num_turns','modelUsage') if k in raw}
account={**account,'sessionId':raw['sessionId'],'numTurns':raw['num_turns'],'stopReason':raw['stopReason'],'completed':True,'freshSession':True,'standing':'Actual Grok DESIGN COAUTHOR in a fresh session. Not a blind consumer or independent acceptance. Input and public custody only.','selectorSha256':sha(Path(P.__file__))}
D.mkdir()
(D/'response.public.json').write_text(json.dumps(safe,indent=2)+'\n')
(D/'assessment.md').write_text(safe.get('text','')+'\n')
(D/'public-tools-and-responses.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in public))
(D/'session-account.json').write_text(json.dumps(account,indent=2)+'\n')
for n in ('prompt.txt','process.json','stderr.log','input-manifest.json'):shutil.copy2(S/n,D/n)
shutil.copytree(S/'inputs',D/'inputs');shutil.copytree(S/'output',D/'authored')
shutil.copy2(Path(__file__),D/'retainer.py');shutil.copy2(Path(P.__file__),D/'retain_public.py')
(D/'retained-files.json').write_text(json.dumps({'files':[{'path':str(p.relative_to(D)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(D.rglob('*')) if p.is_file() and p.name!='retained-files.json']},indent=2)+'\n')
print(json.dumps({'out':str(D),'sessionId':raw['sessionId'],'numTurns':raw['num_turns'],'publicBlocks':len(public),'standing':account['standing']}))
