from pathlib import Path
import json,hashlib,shutil
B=Path('/tmp/opensip-design-corrections'); root=B/'dependency-totality-successor.v1/source'; out=B/'root-source36-prose-completion.v1'
a=B/'claude-dependency-totality-author.v1'; assert (a/'process-completion.json').exists() and json.loads((a/'process-completion.json').read_bytes())['exitCode']==0
assert not out.exists(); out.mkdir()
F=root/'docs/coop/design-corrections/foundation'; edits=[]
p=F/'evaluator-projection-registry.v1.json'; raw=p.read_bytes(); d=json.loads(raw); assert d['historySubjectOrder']=={'order':'strict unique path UTF-8','uniqueKey':'path'}
old='  "historySubjectOrder": {\n    "order": "strict unique path UTF-8",\n    "uniqueKey": "path"\n  },'
new='  "historySubjectOrder": {\n    "order": "existing sequence (producer order)",\n    "duplicatePaths": "allowed; retain every matching row at its original ordinal"\n  },'
assert raw.decode().count(old)==1; edits.append((p,raw,raw.decode().replace(old,new).encode()))
p=F/'atom-evaluation-contract.v1.md';raw=p.read_bytes();old='**Runtime:** wrapper complete + payload window';new='**Runtime polarity:** an unfiltered `exists` tests whether a consumable mapped runtime observation exists, so either `observed-hit` or `observable-unhit` can satisfy it. An `observability` filter restricts the matching polarity set before applying the quantifier; unobservable and unmapped rows never enter that set. This is the projection registry `importQuantifiers` law, and does not equate an unhit observation with an execution hit.\n\n**Runtime:** wrapper complete + payload window'
assert raw.decode().count(old)==1;edits.append((p,raw,raw.decode().replace(old,new).encode()))
rows=[]
for p,b,c in edits:
 rel=p.relative_to(root)
 for kind,raw in [('before',b),('after',c)]:
  q=out/kind/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(raw)
 rows.append({'path':rel.as_posix(),'beforeSha256':hashlib.sha256(b).hexdigest(),'afterSha256':hashlib.sha256(c).hexdigest()})
for p,b,c in edits: assert p.read_bytes()==b
for p,b,c in edits:p.write_bytes(c)
(out/'assessment.json').write_text(json.dumps({'standing':'Root post-author prose/registry consistency corrections, no changed runtime algorithm or schema validation keywords, no frozen source edits. Independent review pending.','changes':rows,'rationale':['historySubjectOrder contradicted both the same registry HISTORY_SUBJECT_SEQUENCE_ORDINALS and atom section6 / HistoryPayloadV1 sequence owner. Align stale registry entry to existing law.','State existing importQuantifiers runtime polarity rule in prose without reference to consumer-specific inputs, expected outputs or failures.'],'sourceAcceptance':False},indent=2)+'\n')
shutil.copytree(out,Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews')/out.name)
print('Applied two guarded root prose consistency corrections to isolated successor only')
