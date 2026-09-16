"""Measure exact line delivery through public Read tool results; no comprehension claim."""
from pathlib import Path
import argparse,json,hashlib,re
p=argparse.ArgumentParser();p.add_argument('--runtime',type=Path,required=True);p.add_argument('--snapshot',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();assert not a.out.exists();a.out.mkdir()
raw=(a.runtime/'public-events.jsonl').read_bytes();events=[json.loads(x) for x in raw.splitlines()];pending={};sources={};receipts=[]
def source(path):
 q=Path(path).resolve()
 if not q.is_relative_to(a.snapshot.resolve()) or not q.is_file():return None
 rel=q.relative_to(a.snapshot.resolve()).as_posix()
 if rel not in sources:
  b=q.read_bytes();sources[rel]={'sha256':hashlib.sha256(b).hexdigest(),'lines':b.decode().splitlines(),'delivered':set(),'reads':0}
 return rel
for index,e in enumerate(events):
 for b in e.get('message',{}).get('content',[]):
  if b.get('type')=='tool_use' and b.get('name')=='Read':
   rel=source(b['input'].get('file_path',''))
   if rel:pending[b['id']]={'path':rel,'args':b['input'],'event':index}
  elif b.get('type')=='tool_result' and b.get('tool_use_id') in pending:
   req=pending.pop(b['tool_use_id']);rel=req['path'];s=sources[rel];s['reads']+=1;content=b.get('content','');exact=[];mismatch=[]
   if isinstance(content,list):content='\n'.join(x.get('text','') for x in content if isinstance(x,dict))
   for line in content.splitlines():
    m=re.match(r'^\s*(\d+)\t(.*)$',line)
    if not m:continue
    n=int(m[1]);text=m[2]
    if 1<=n<=len(s['lines']) and text==s['lines'][n-1]:exact.append(n);s['delivered'].add(n)
    else:mismatch.append(n)
   receipts.append({'path':rel,'toolUseEvent':req['event'],'toolResultEvent':index,'request':req['args'],'exactDeliveredLines':exact,'nonmatchingNumberedLines':mismatch,'resultIsError':b.get('is_error',False),'resultCharacters':len(content)})
def ranges(nums):
 out=[]
 for x in nums:
  if out and x==out[-1][1]+1:out[-1][1]=x
  else:out.append([x,x])
 return out
rows=[]
for rel,s in sorted(sources.items()):
 missing=set(range(1,len(s['lines'])+1))-s['delivered'];rows.append({'path':rel,'sha256':s['sha256'],'totalLines':len(s['lines']),'exactDeliveredLines':len(s['delivered']),'readCalls':s['reads'],'uncoveredRanges':ranges(sorted(missing)),'completeThroughReadDelivery':not missing})
report={'standing':'Public Read tool exact-line delivery audit at captured event boundary. Does not prove comprehension or complete review. Bash/other delivery is uncounted and must be assessed separately; uncovered here is not automatically a reviewer omission. Active session may subsequently complete reads.','runtime':str(a.runtime),'snapshot':str(a.snapshot),'publicEventsSha256':hashlib.sha256(raw).hexdigest(),'eventCount':len(events),'files':rows,'readReceipts':receipts,'pendingReadCalls':list(pending.values())};(a.out/'audit.json').write_text(json.dumps(report,indent=2)+'\n');(a.out/'public-events.captured.jsonl').write_bytes(raw)
core=[r for r in rows if r['path'].startswith('docs/v2/contracts/product-v1/')];print(json.dumps({'events':len(events),'files':len(rows),'fullyDeliveredFiles':sum(r['completeThroughReadDelivery'] for r in rows),'core':core,'nonmatchingReadResults':sum(bool(r['nonmatchingNumberedLines']) for r in receipts)},indent=2))
