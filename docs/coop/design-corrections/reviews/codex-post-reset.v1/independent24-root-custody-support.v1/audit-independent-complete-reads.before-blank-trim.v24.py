"""Audit exact public read-file deliveries; no inference about comprehension."""
from pathlib import Path
import argparse, hashlib, json, re
p=argparse.ArgumentParser();p.add_argument('--transcript',type=Path,required=True);p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
rows=[json.loads(x) for x in a.transcript.read_text().splitlines() if x]
results={x['tool_call_id']:x.get('content') for x in rows if x.get('type')=='tool_result'}
rels=['docs/v2/contracts/product-v1/'+x+'.md' for x in ('identity-and-evidence','security-and-lifecycle','native-evidence','workflows-and-surfaces','admission-and-qualification')]+['docs/coop/design-corrections/workflows/query-projection-contract.v3.md']
report=[]
for rel in rels:
 source=a.source/rel; lines=source.read_text().splitlines();covered=set();calls=[]
 for row in rows:
  if row.get('type')!='assistant':continue
  for call in row.get('tool_calls',[]):
   if call.get('name')!='read_file':continue
   arg=call['arguments'];arg=json.loads(arg) if isinstance(arg,str) else arg
   if Path(arg.get('target_file','')).resolve()!=source.resolve():continue
   content=results.get(call['id']);offset=arg.get('offset',1)
   if not isinstance(content,str):calls.append({'id':call['id'],'exactDelivery':False,'reason':'No string result'});continue
   delivered=re.sub(r'^\d+→','',content,flags=re.M).splitlines()
   exact=delivered==lines[offset-1:offset-1+len(delivered)]
   calls.append({'id':call['id'],'offset':offset,'lines':len(delivered),'exactDelivery':exact})
   if exact:covered.update(range(offset,min(len(lines)+1,offset+len(delivered))))
 missing=sorted(set(range(1,len(lines)+1))-covered)
 report.append({'path':rel,'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'lineCount':len(lines),'calls':calls,'missingLines':missing,'complete':not missing})
j={'standing':'Exact public tool-delivery audit only. Substantive review and comprehension require separate root assessment.','transcriptSha256':hashlib.sha256(a.transcript.read_bytes()).hexdigest(),'files':report,'passed':all(r['complete'] for r in report)}
assert not a.out.exists();a.out.write_text(json.dumps(j,indent=2)+'\n');print(json.dumps(j,indent=2))
raise SystemExit(not j['passed'])
