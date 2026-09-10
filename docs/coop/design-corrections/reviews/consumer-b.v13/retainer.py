"""Retain fresh Grok review public events across CLI compaction.
Read the authenticated append-only update stream, never retain thought chunks,
compaction summaries, raw responses or raw tool-output metadata.
"""
from pathlib import Path
from urllib.parse import quote
import collections, hashlib, json, sys


def public_from_updates(rows, session_id, prompt):
    public=[];names=collections.Counter();starts=[];event_ids=[];calls=set()
    for row in rows:
        pars=row['params']
        assert pars['sessionId']==session_id
        u=pars['update'];kind=u['sessionUpdate']
        if kind=='user_message_chunk':
            c=u.get('content',{})
            if c.get('type')=='text' and prompt in c.get('text',''):starts.append(len(public))
            continue
        if kind=='agent_message_chunk':
            c=u.get('content',{})
            if c.get('type')=='text':public.append({'type':'assistant','content':c['text']})
            else:continue
        elif kind=='tool_call':
            tid=u['toolCallId'];assert tid not in calls;calls.add(tid)
            name=u.get('_meta',{}).get('x.ai/tool',{}).get('name') or u['title']
            public.append({'type':'assistant','tool_calls':[{'id':tid,'name':name,'arguments':json.dumps(u['rawInput'],ensure_ascii=False)}]});names[name]+=1
        elif kind=='tool_call_update' and u.get('status') in ('completed','failed'):
            content=[]
            for item in u.get('content',[]):
                c=item.get('content',{})
                if item.get('type')=='content' and c.get('type')=='text':content.append(c['text'])
            public.append({'type':'tool_result','tool_call_id':u['toolCallId'],'content':'\n'.join(content),'publicStatus':u['status']})
        else:
            continue
        event_ids.append(pars.get('_meta',{}).get('eventId'))
    assert starts==[0], ('Fresh prompt must appear exactly once before public activity',starts)
    return public,names,event_ids


def main():
    name,role=sys.argv[1:];assert role in ('independent-design-review','blind-consumer','independent-application-review')
    tmp=Path('/tmp/opensip-design-corrections')/name
    out=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews')/name
    assert not out.exists()
    proc=json.loads((tmp/'process.json').read_text());assert proc.get('freshSession') is True and '--resume' not in proc['command']
    raw=json.loads((tmp/'response.raw.json').read_text());assert raw['stopReason'] in ('end_turn','cancelled')
    safe={k:raw[k] for k in ('text','stopReason','sessionId','requestId','usage','num_turns','modelUsage') if k in raw}
    cwd=Path(proc['command'][proc['command'].index('--cwd')+1]).resolve()
    session=Path('/Users/sb/.grok/sessions')/quote(str(cwd),safe='')/raw['sessionId']
    source=session/'updates.jsonl';updates=source.read_bytes();rows=[json.loads(x) for x in updates.splitlines() if x]
    prompt=(tmp/'prompt.txt').read_text().strip()
    sys.path.insert(0,str(Path('/tmp/opensip-design-corrections/application-successor-root.v1')))
    import retain_public as P
    public,selection=P.public_grok_update_blocks(updates.decode('utf-8'),raw['sessionId'],prompt)
    names=selection['toolCalls'];ids=selection['eventIds']
    history=[json.loads(x) for x in (session/'chat_history.jsonl').read_text().splitlines() if x]
    models=sorted({x['model_id'] for x in history if x.get('type')=='assistant' and x.get('model_id')})
    account={'sessionId':raw['sessionId'],'models':models,'numTurns':raw['num_turns'],'toolCalls':dict(names),'publicBlocks':len(public),'promptFoundExactlyOnce':True,'freshSession':True,'standing':'Actual Grok '+role+' from fresh origin; full public event stream retained across any compaction. Custody is not substantive acceptance.','completed':raw['stopReason']=='end_turn','stopReason':raw['stopReason'],'publicEventSource':'authenticated session updates.jsonl','eventIds':ids,'sourceBytes':len(updates),'sourceSha256':hashlib.sha256(updates).hexdigest(),'compactionsObserved':sum(x['params']['update']['sessionUpdate']=='auto_compact_completed' for x in rows),'privateFieldsRetained':False,'strictSelectorSha256':hashlib.sha256(Path(P.__file__).read_bytes()).hexdigest()}
    out.mkdir()
    (out/'response.public.json').write_text(json.dumps(safe,indent=2)+'\n');(out/'assessment.md').write_text(safe['text']+'\n')
    for n in ('prompt.txt','process.json','stderr.log'):(out/n).write_bytes((tmp/n).read_bytes())
    (out/'retainer.py').write_bytes(Path(__file__).read_bytes())
    (out/'public-tools-and-responses.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in public))
    (out/'session-account.json').write_text(json.dumps(account,indent=2)+'\n')
    custody=[{'path':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(out.iterdir()) if p.is_file()]
    (out/'custody.json').write_text(json.dumps({'files':custody},indent=2)+'\n')
    print(json.dumps({'out':str(out),'turns':raw['num_turns'],'toolCalls':dict(names),'compactions':account['compactionsObserved']}))

if __name__=='__main__':main()
