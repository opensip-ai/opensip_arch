"""Strict public update retention for an authenticated fresh-origin review chain.
Whole-prompt equality prevents an embedded original charter from being mistaken
for a second launch; unknown, reordered and duplicate user messages still refuse."""
from pathlib import Path
from urllib.parse import quote
import argparse, hashlib, json, shutil, sys

p = argparse.ArgumentParser()
p.add_argument('name')
p.add_argument('role', choices=['blind-consumer', 'independent-design-review', 'independent-application-review'])
a = p.parse_args()
B = Path('/tmp/opensip-design-corrections')
LIVE = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews')
S = B / a.name
D = LIVE / a.name
assert S.parent == B and not D.exists()
load = lambda p: json.loads(p.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
safe = lambda r: {k:r[k] for k in ('text','stopReason','sessionId','requestId','usage','num_turns','modelUsage') if k in r}
proc = load(S/'process.json')
raw = load(S/'response.raw.json')
assert not proc['freshSession'] and raw['stopReason'] in ('end_turn','cancelled')
assert 'coauthor' not in proc.get('standing','').lower()
origin = Path(proc['freshOrigin']['path']).resolve()
op = load(origin/'process.json')
sid = load(origin/'response.raw.json')['sessionId']
assert op['freshSession'] and '--resume' not in op['command']
assert sha(origin/'process.json') == proc['freshOrigin']['processSha256']
cwd = Path(op['command'][op['command'].index('--cwd')+1]).resolve()
chain = []
node = S
seen = set()
while node.resolve() != origin:
    assert node.resolve() not in seen
    seen.add(node.resolve())
    q = load(node/'process.json'); r = load(node/'response.raw.json')
    assert not q['freshSession'] and q['sessionId'] == r['sessionId'] == sid
    assert r['stopReason'] in ('end_turn','cancelled')
    assert q['freshOrigin']['sessionId'] == sid
    assert Path(q['freshOrigin']['path']).resolve() == origin
    assert q['freshOrigin']['processSha256'] == sha(origin/'process.json')
    assert q['command'][q['command'].index('--resume')+1] == sid
    assert Path(q['command'][q['command'].index('--cwd')+1]).resolve() == cwd
    assert 'coauthor' not in q.get('standing','').lower()
    chain.append(node)
    node = Path(q['previousContinuation'])
chain = [origin] + list(reversed(chain))
stream = (Path('/Users/sb/.grok/sessions')/quote(str(cwd),safe='')/sid/'updates.jsonl').read_text()
lines = stream.splitlines(True)
prompts = [(d/'prompt.txt').read_text().strip() for d in chain]
assert all(prompts)
starts = []
for i, line in enumerate(lines):
    row = json.loads(line)
    assert row['params']['sessionId'] == sid
    u = row['params']['update']
    if u['sessionUpdate'] == 'user_message_chunk':
        c = u.get('content',{})
        assert c.get('type') == 'text'
        matches = [j for j,pr in enumerate(prompts) if pr == c['text'].strip()]
        assert matches == [len(starts)], 'Unknown, reordered or duplicate public prompt'
        starts.append(i)
assert len(starts) == len(chain)
sys.path.insert(0,str(B/'application-successor-root.v1'))
import retain_public as P
for i,d in enumerate(chain):
    segment = ''.join(lines[0 if i == 0 else starts[i]:starts[i+1] if i+1 < len(starts) else len(lines)])
    pub, account = P.public_grok_update_blocks(segment,sid,prompts[i])
    if d != S:
        prior = LIVE/d.name
        assert pub == [json.loads(x) for x in (prior/'public-tools-and-responses.jsonl').read_text().splitlines() if x]
        assert safe(load(d/'response.raw.json')) == load(prior/'response.public.json')
    else:
        public = pub
D.mkdir()
(D/'response.public.json').write_text(json.dumps(safe(raw),indent=2)+'\n')
(D/'assessment.md').write_text(raw.get('text','')+'\n')
(D/'public-tools-and-responses.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in public))
(D/'session-account.json').write_text(json.dumps({**account,'sessionId':sid,'numTurns':raw['num_turns'],'stopReason':raw['stopReason'],'completed':raw['stopReason']=='end_turn','freshSession':False,'freshOrigin':proc['freshOrigin'],'priorPublicSegmentsMatched':len(chain)-1,'standing':'Actual Grok '+a.role+' continuation of authenticated fresh origin. Custody is not substantive acceptance.','originalStreamSha256':hashlib.sha256(stream.encode()).hexdigest(),'selectorSha256':sha(Path(P.__file__)),'privateFieldsRetained':False},indent=2)+'\n')
for n in ('prompt.txt','process.json','stderr.log'):
    shutil.copyfile(S/n,D/n)
shutil.copyfile(Path(__file__),D/'retainer.py')
(D/'custody.json').write_text(json.dumps({'files':[{'path':x.name,'sha256':sha(x),'bytes':x.stat().st_size} for x in sorted(D.iterdir()) if x.is_file()]},indent=2)+'\n')
print(json.dumps({'out':str(D),'turns':raw['num_turns'],'publicBlocks':len(public),'priorPublicSegmentsMatched':len(chain)-1}))
