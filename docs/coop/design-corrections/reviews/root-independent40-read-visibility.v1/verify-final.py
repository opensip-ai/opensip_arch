from pathlib import Path
import json,re,hashlib,shutil
B=Path('/tmp/opensip-design-corrections');R=B/'claude-independent-design.v40';S=B/'candidate-subject.v40';O=Path(__file__).parent;L=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews');H=lambda b:hashlib.sha256(b).hexdigest()
assert json.loads((R/'process-completion.json').read_bytes())['exitCode']==0 and (R/'review.json').exists()
ev=[json.loads(x) for x in (R/'public-events.jsonl').read_text().splitlines()];ledger=[json.loads(x) for x in (R/'receipts/read-ledger.jsonl').read_text().splitlines()];targets={r['path']:r for r in ledger if r['kind']=='fresh40Read' and 'complete' in r.get('note','') and r.get('range','').startswith('1-')};uses={};got={p:set() for p in targets};errors=[];eof=[]
for e in ev:
 for b in e.get('message',{}).get('content',[]):
  if b.get('type')=='tool_use' and b.get('name')=='Read':
   path=b['input'].get('file_path','')
   for rel in targets:
    if path.endswith('/'+rel):uses[b['id']]=rel
  if b.get('type')=='tool_result' and b.get('tool_use_id') in uses:
   rel=uses[b['tool_use_id']];c=b.get('content','');c=c if isinstance(c,str) else '\n'.join(x.get('text','') for x in c if isinstance(x,dict));src=(S/rel).read_text().splitlines()
   for line in c.splitlines():
    m=re.match(r'^\s*(\d+)\t(.*)$',line)
    if not m:continue
    n=int(m.group(1));v=m.group(2)
    if 1<=n<=len(src) and v==src[n-1]:got[rel].add(n)
    elif n==len(src)+1 and v=='':eof.append({'path':rel,'line':n})
    else:errors.append({'path':rel,'line':n,'readId':b['tool_use_id']})
rows=[]
for rel,r in targets.items():
 raw=(S/rel).read_bytes();assert H(raw)==r['sha256'];count=len(raw.decode().splitlines());assert count==r['lines'];missing=sorted(set(range(1,count+1))-got[rel]);rows.append({'path':rel,'sha256':H(raw),'lines':count,'visibleExactLines':len(got[rel]),'missing':missing})
d={'standing':'Audit of public Read-event exact line visibility for complete reads claimed in final ledger. Not comprehension proof, complete delta/probe audit, source acceptance or product qualification. Initial provisional EOF artifacts separately classified here.','publicEventsSha256':H((R/'public-events.jsonl').read_bytes()),'readLedgerSha256':H((R/'receipts/read-ledger.jsonl').read_bytes()),'reviewSha256':H((R/'review.json').read_bytes()),'rows':rows,'syntheticBlankEofLines':eof,'errors':errors,'passed':not errors and all(not r['missing'] for r in rows)}
assert not (O/'verification.json').exists();(O/'verification.json').write_text(json.dumps(d,indent=2)+'\n');shutil.copytree(O,L/O.name);print(json.dumps(d));raise SystemExit(not d['passed'])
