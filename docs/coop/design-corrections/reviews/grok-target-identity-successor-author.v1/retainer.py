"""Strict public-only retention of explicitly named coauthor tasks.

Not blind or final independent acceptance. Input paths and substantive standing
remain distinct from authenticated public message custody.
"""
from pathlib import Path
from urllib.parse import quote
import argparse,hashlib,json,shutil,sys
B=Path('/tmp/opensip-design-corrections');ROOT=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews')
ALLOWED={'grok-proof-output-contract-audit.v1','grok-proof-output-derivation-author.v1','grok-closure-kind-correction-review.v1','grok-target-identity-successor-author.v1'}
ap=argparse.ArgumentParser();ap.add_argument('name',choices=sorted(ALLOWED));a=ap.parse_args();S=B/a.name;D=ROOT/a.name
assert not D.exists()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads(p.read_text())
safe=lambda d:{k:d[k] for k in ('text','stopReason','sessionId','requestId','usage','num_turns','modelUsage') if k in d}
proc=load(S/'process.json');r=load(S/'response.raw.json');prompt=(S/'prompt.txt').read_text()
assert r['stopReason'] in ('end_turn','cancelled') and 'COAUTHOR' in prompt
assert (S/'stderr.log').stat().st_size==0
sys.path.insert(0,str(B/'application-successor-root.v1'))
import retain_public as P
cwd=Path(proc['command'][proc['command'].index('--cwd')+1]).resolve()
up=Path('/Users/sb/.grok/sessions')/quote(str(cwd),safe='')/r['sessionId']/'updates.jsonl'
stream=up.read_text();prior_matched=0;automatic_notices=[]
if proc['freshSession']:
    assert '--resume' not in proc['command']
    public,account=P.public_grok_update_blocks(stream,r['sessionId'],prompt.strip())
else:
    origin=Path(proc['coauthorOrigin']['path']);op=load(origin/'process.json');first=load(origin/'response.raw.json')
    assert op['freshSession'] and '--resume' not in op['command']
    assert 'COAUTHOR' in (origin/'prompt.txt').read_text()
    assert sha(origin/'process.json')==proc['coauthorOrigin']['processSha256']
    assert first['sessionId']==r['sessionId']==proc['sessionId']==proc['coauthorOrigin']['sessionId']
    assert proc['command'][proc['command'].index('--resume')+1]==r['sessionId']
    assert Path(op['command'][op['command'].index('--cwd')+1]).resolve()==cwd
    chain=[];node=S;seen=set()
    while node.resolve()!=origin.resolve():
        assert str(node.resolve()) not in seen;seen.add(str(node.resolve()));chain.append(node)
        q=load(node/'process.json');response=load(node/'response.raw.json')
        assert q['sessionId']==response['sessionId']==r['sessionId'] and not q['freshSession']
        assert response['stopReason'] in ('end_turn','cancelled') and 'COAUTHOR' in (node/'prompt.txt').read_text()
        node=Path(q['previousContinuation'])
    chain=[origin]+list(reversed(chain))
    lines=stream.splitlines(True);starts=[];texts=[]
    authorized_prompts=[(d/'prompt.txt').read_text().strip() for d in chain]
    for i,line in enumerate(lines):
        u=json.loads(line)['params']['update']
        if u['sessionUpdate']=='user_message_chunk':
            c=u.get('content',{});assert c.get('type')=='text';text=c['text']
            if any(pr in text for pr in authorized_prompts):
                starts.append(i);texts.append(text)
            else:
                digest=hashlib.sha256(text.encode()).hexdigest()
                assert digest=='5d27861a89b2cdacc524d8ac5ac9c2359ac123d16924a0bf5db66a6a824e431c', 'Unrecognized additional coauthor user-message chunk'
                assert a.name=='grok-target-identity-successor-author.v1'
                automatic_notices.append({'sha256':digest,'text':text,'standing':'Exact reviewed CLI background-command completion notice; not a new human/root task or private compaction summary.'})
    assert len(starts)==len(chain)
    for i,d in enumerate(chain):
        pr=(d/'prompt.txt').read_text().strip();assert pr in texts[i]
        segment=''.join(lines[0 if i==0 else starts[i]:starts[i+1] if i+1<len(starts) else len(lines)])
        # P's fresh-segment decoder permits exactly one author prompt. The one
        # exact reviewed CLI completion notice is retained separately, not silently
        # treated as another human task or discarded without an account.
        selected_lines=[]
        for line in segment.splitlines(True):
            event=json.loads(line);u=event['params']['update']
            if u['sessionUpdate']=='user_message_chunk':
                text=u.get('content',{}).get('text','')
                if hashlib.sha256(text.encode()).hexdigest()=='5d27861a89b2cdacc524d8ac5ac9c2359ac123d16924a0bf5db66a6a824e431c':
                    assert event['params']['sessionId']==r['sessionId'] and automatic_notices
                    continue
            selected_lines.append(line)
        pub,acc=P.public_grok_update_blocks(''.join(selected_lines),r['sessionId'],pr)
        if d!=S:
            retained=[json.loads(line) for line in (ROOT/d.name/'public-tools-and-responses.jsonl').read_text().splitlines() if line]
            assert pub==retained and safe(load(d/'response.raw.json'))==load(ROOT/d.name/'response.public.json');prior_matched+=1
        else:public,account=pub,acc
input_accounts=[]
for name in ('input-manifest.json','inputs/input-manifest.json','inputs/retained-files.json'):
    mf=S/name
    if not mf.exists():continue
    body=load(mf);base=mf.parent if mf.parent.name=='inputs' else S
    for row in body['files']:
        p=base/row['path'];assert p.resolve().is_relative_to(base.resolve())
        assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256']
    input_accounts.append({'manifest':name,'sha256':sha(mf),'filesVerified':len(body['files']),'standing':'Input manifest/file verification at retention; any launch pin is separately in the exact prompt/receipt.'})
D.mkdir();(D/'response.public.json').write_text(json.dumps(safe(r),indent=2)+'\n');(D/'assessment.md').write_text(r.get('text','')+'\n')
(D/'public-tools-and-responses.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in public))
(D/'session-account.json').write_text(json.dumps({**account,'sessionId':r['sessionId'],'numTurns':r['num_turns'],'stopReason':r['stopReason'],'freshSession':proc['freshSession'],'completed':r['stopReason']=='end_turn','priorPublicSegmentsMatched':prior_matched,'standing':'Actual Grok COAUTHOR. No blind consumer or final independent acceptance standing.','inputAccounts':input_accounts,'automaticPublicNotices':automatic_notices,'originalAuthenticatedStreamSha256':hashlib.sha256(stream.encode()).hexdigest(),'selectorNoticeExclusion':'Only the exact reviewed public CLI completion notice is excluded from the one-prompt segment decoder and fully retained above; unknown extra prompts refuse.','selectorSha256':sha(Path(P.__file__))},indent=2)+'\n')
for name in ('prompt.txt','process.json','stderr.log','input-manifest.json','source-copy-verification.json'):
    if (S/name).exists():shutil.copy2(S/name,D/name)
if (S/'inputs').exists():shutil.copytree(S/'inputs',D/'inputs')
shutil.copytree(S/'output',D/'authored')
shutil.copy2(Path(__file__),D/'retainer.py')
for name in ('retain_public.py','review_envelope.py','coverage_contract.py'):shutil.copy2(B/'application-successor-root.v1'/name,D/name)
(D/'retained-files.json').write_text(json.dumps({'files':[{'path':str(p.relative_to(D)),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(D.rglob('*')) if p.is_file() and p.name!='retained-files.json']},indent=2)+'\n')
print(json.dumps({'name':a.name,'publicBlocks':len(public),'priorPublicSegmentsMatched':prior_matched,'numTurns':r['num_turns'],'stopReason':r['stopReason'],'standing':'coauthor only'}))
