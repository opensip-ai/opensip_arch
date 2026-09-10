"""Retain public deliveries for a verified fresh-origin blind continuation.

All previous public segments must match previously retained bytes semantically.
Only public assistant/tool fields are emitted by the already checked selector.
"""
from pathlib import Path
from urllib.parse import quote
import argparse, hashlib, json, sys, shutil
BASE=Path('/tmp/opensip-design-corrections')
ROOT=Path('/Users/sb/code/opensip-ai/opensip_arch')
HELPERS=BASE/'application-successor-root.v1'
sys.path.insert(0,str(HELPERS))
import retain_public as P

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def safe_response(d):
    return {k:d[k] for k in ('text','stopReason','sessionId','requestId','usage','num_turns','modelUsage') if k in d}

def split_segments(text, prompts):
    lines=text.splitlines(True);starts=[];texts=[]
    for i,line in enumerate(lines):
        r=json.loads(line)
        u=r['params']['update']
        if u['sessionUpdate']=='user_message_chunk':
            c=u.get('content',{})
            assert c.get('type')=='text','Nontext user prompt'
            starts.append(i);texts.append(c.get('text',''))
    assert len(starts)==len(prompts),'Unexpected user message count'
    for text,prompt in zip(texts,prompts):
        assert prompt.strip() in text,'Prompt order/membership mismatch'
    return [''.join(lines[0 if i==0 else start:starts[i+1] if i+1<len(starts) else len(lines)]) for i,start in enumerate(starts)]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--name',required=True);a=ap.parse_args()
    current=(BASE/a.name).resolve();assert current.parent==BASE.resolve()
    cp=load(current/'process.json');assert cp.get('freshSession') is False
    origin=Path(cp['freshOrigin']['path']).resolve();op=load(origin/'process.json')
    assert op.get('freshSession') is True and '--resume' not in op['command']
    assert 'coauthor' not in op.get('standing','').lower()
    assert load(origin/'response.raw.json')['stopReason'] in ('end_turn','cancelled')
    assert sha(origin/'process.json')==cp['freshOrigin']['processSha256']
    sid=load(origin/'response.raw.json')['sessionId']
    chain=[];seen=set();node=current
    while node!=origin:
        assert str(node) not in seen,'Continuation cycle';seen.add(str(node))
        p=load(node/'process.json');d=load(node/'response.raw.json')
        assert p.get('freshSession') is False and '--resume' in p['command']
        assert 'coauthor' not in p.get('standing','').lower()
        assert Path(p['freshOrigin']['path']).resolve()==origin
        assert p['freshOrigin']['processSha256']==sha(origin/'process.json')
        assert p['sessionId']==d['sessionId']==p['freshOrigin']['sessionId']==sid
        assert Path(p['command'][p['command'].index('--cwd')+1]).resolve()==Path(op['command'][op['command'].index('--cwd')+1]).resolve()
        assert p['command'][p['command'].index('--resume')+1]==sid
        assert d['stopReason'] in ('end_turn','cancelled')
        chain.append(node);node=Path(p['previousContinuation']).resolve()
    chain=[origin]+list(reversed(chain))
    assert chain[-1]==current
    cwd=Path(op['command'][op['command'].index('--cwd')+1]).resolve()
    source=Path('/Users/sb/.grok/sessions')/quote(str(cwd),safe='')/sid/'updates.jsonl'
    raw_text=source.read_text();prompts=[(x/'prompt.txt').read_text() for x in chain]
    segments=split_segments(raw_text,prompts);decoded=[];accounts=[]
    for directory,segment,prompt in zip(chain,segments,prompts):
        public,account=P.public_grok_update_blocks(segment,sid,prompt)
        decoded.append(public);accounts.append(account)
        if directory!=current:
            prior=ROOT/'docs/coop/design-corrections/reviews'/directory.name
            retained=[json.loads(x) for x in (prior/'public-tools-and-responses.jsonl').read_text().splitlines() if x]
            assert public==retained,'Prior retained public delivery changed: '+directory.name
            assert safe_response(load(directory/'response.raw.json'))==load(prior/'response.public.json')
    out=ROOT/'docs/coop/design-corrections/reviews'/current.name
    assert not out.exists(),'Never overwrite retained continuation'
    final=load(current/'response.raw.json');safe=safe_response(final)
    assert final['sessionId']==sid
    assert (current/'stderr.log').stat().st_size==0,'Nonempty stderr requires separate public-error assessment'
    account={**accounts[-1],'sessionId':sid,'numTurns':final['num_turns'],'stopReason':final['stopReason'],'completed':final['stopReason']=='end_turn','freshSession':False,'freshOrigin':cp['freshOrigin'],'standing':'Actual Grok blind reconstruction continuation of verified fresh origin. Additional kit-only team inputs must be assessed separately; public custody is not acceptance.','allPriorPublicSegmentsMatched':True,'publicSegmentCount':len(chain),'authenticatedWholeStreamSha256':hashlib.sha256(raw_text.encode()).hexdigest(),'segments':[{'path':str(d),'processSha256':sha(d/'process.json'),'promptSha256':sha(d/'prompt.txt'),'publicBlocks':len(p)} for d,p in zip(chain,decoded)]}
    out.mkdir()
    (out/'response.public.json').write_text(json.dumps(safe,indent=2)+'\n')
    (out/'assessment.md').write_text(safe.get('text','')+'\n')
    (out/'public-tools-and-responses.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in decoded[-1]))
    (out/'session-account.json').write_text(json.dumps(account,indent=2)+'\n')
    for n in ('prompt.txt','process.json','stderr.log'):shutil.copy2(current/n,out/n)
    shutil.copy2(Path(__file__),out/'retainer.py')
    for n in ('retain_public.py','review_envelope.py','coverage_contract.py'):shutil.copy2(HELPERS/n,out/n)
    custody=[{'path':p.name,'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(out.iterdir()) if p.is_file()]
    (out/'custody.json').write_text(json.dumps({'files':custody},indent=2)+'\n')
    print(json.dumps({'out':str(out),'sessionId':sid,'numTurns':final['num_turns'],'publicBlocks':len(decoded[-1]),'priorSegmentsMatched':len(chain)-1}))

if __name__=='__main__':main()
