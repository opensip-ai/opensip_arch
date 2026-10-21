"""Reviewable strict additive preview only; no architecture/lock mutation."""
from pathlib import Path
import json,hashlib,copy,subprocess
F=Path(__file__).parent;B=F/'inventory237-preview';assert not B.exists()
P=Path('/Users/sb/code/opensip-ai/opensip');A=P.parent/'opensip_arch';W=P.parent/'opensip-rust3-send-takeover'
def pin(root,path):
 raw=(root/path).read_bytes();return dict(path=path,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
lock=json.loads((P/'design-lock.json').read_text());parent=lock['inventorySuccessors'][-1]['candidate'];assert parent['path'].endswith('.v236.json')and pin(A,parent['path'])==parent
raw=json.loads((A/parent['path']).read_text());prior={r['path']:r for r in raw['files']};new=copy.deepcopy(raw)
paths=sorted(subprocess.check_output(['git','ls-files','-o','--exclude-standard'],cwd=W,text=True).splitlines());assert len(paths)==18 and not set(paths)&set(prior)
purpose={
 'send.rs':'Rust3 send module and scoped public Plan/projection, Request/schedule, Sender/custody and D3a participant exports. Library interfaces consume supplied admitted values; no production factory/caller or admission authority.',
 'dependency.rs':'Dependency host manifest/chunk/seal builders: exact constructed package keys and package tuple/path order, complete retained native file-manifest H/count/byte joins and set identity, distinct raw deterministic-CBOR wire digest, empty sets and unchanged greedy/profile bounds. Acquisition and set admission remain C4/custody duties.',
 'domain.rs':'Fresh host Rust subjects and requested Coverage domains from the sealed snapshot and selected Plan projections, complete per-key C4 scope2 joins, exact C2 literal stages, unchanged scope/domain commitments, inline V2 and negotiated reference V3 at all counts, and whole Analyze sizing before repeated subject copies. No scope mint, C4 admission or worker reconstruction.',
 'policy.rs':'Source-derived closed32 Rust3 policy (retained24 plus eight native limits), exact selected-capability Hello and native OpenUniverse builders with verified identity and set-id joins. Preserves absence and signed token order; no local defaults, provider selection or execution/source authority.',
 'prepared.rs':'Complete selected inert prepared-set manifest/chunk/seal builders, every exact row including failed rows, native complete-set H, contiguous ordinals, generated-blob equality, raw blob/content fields and unchanged count/byte/greedy bounds. C4 owns freshness, selection/fallback and read authority; no row filtering or execution.',
 'request.rs':'Complete Rust3 request construction from supplied immutable Plan projections: strict canonical input checks and joins, all host families in canonical order, checked aggregate budgets and exact slot hashes/coordinates/final-entry digests/seal counts, maximal Cancel reservation and pre-materialization Analyze sizing. No source reads or spawn; C4 owns Plan admission/refusal routing.',
 'schedule.rs':'Checked Rust3 deterministic-CBOR envelope/chunk measurement and immutable slot recording, including greedy count arithmetic, frame/request byte and frame-count limits, one exact maximal Cancel reserve and refusal before slot append. No dummy chunk allocation or source/Plan admission.',
 'sender.rs':'Independent host realization from frozen Plan values and bounded custody reads; exact immutable-slot type/sequence/coordinates/bytes/hash/seal/final-content checks before sent state, strict actual envelopes and defensive totals, one typed correlation-echo user Cancel and latched refusals. Participant owns acknowledgment and physical pending-write gates.',
 'snapshot.rs':'Sealed snapshot host entry/manifest/chunk/seal builders with exact file/symlink types, strict path order, raw deterministic-CBOR manifest digest, checked counts/bytes/greedy coordinates and complete envelope sizing before copying symlink bytes. C1 retains custody and snapshot admission.',
 'participant.rs':'Rust3 D3a participant: table acknowledgment gates before source transfer, one nonblocking pipe operation per step, complete pending writes before Cancel, response frame/payload preallocation accounting, host/protocol fault separation, original raw candidate buffers moved once only after valid terminal/ZeroExit/EOF, and discard/late-fault invalidation. Base participant preserves the explicit reference/census worker-admission gate until4c.',
}
rows=[]
for path in paths:
 name=Path(path).name
 if name.endswith('_tests.rs'):
  key=name.replace('_tests.rs','.rs');description='M3-D D2b-4b public synthetic controls for '+key+': '+purpose[key]+' Fixtures and fake pipes/custody establish no native Plan/source/provider/production admission or qualification.';role='test'
 else:description='M3-D D2b-4b: '+purpose[name];role='adapter'if name=='participant.rs'else'codec'
 row=dict(path=path,package='opensip-components',role=role,description=description,generated=False,standing='proposed');rows.append(row);new['files'].append(row)
new['files'].sort(key=lambda r:r['path']);newmap={r['path']:r for r in new['files']};assert len(newmap)==1410 and len(prior)==1392
assert all(newmap[p]==r for p,r in prior.items());assert {k:v for k,v in new.items()if k!='files'}=={k:v for k,v in raw.items()if k!='files'}
indices={r['path']:i for i,r in enumerate(new['files'])};carry=[]
def project(e):
 assert e['parent']==parent
 pointer=e['selector']['jsonPointer'].split('/');assert len(pointer)==4 and pointer[1]=='files'and pointer[3]=='description'
 row=raw['files'][int(pointer[2])];assert row['description']==e['before']and newmap[row['path']]==row
 return dict(path=row['path'],selector=dict(jsonPointer=f'/files/{indices[row["path"]]}/description'),before=e['before'],after=e['after'])
for e in lock['inventoryPassageInheritance']:carry.append(dict(origin='inherited',**project(e)))
assert len(carry)==138
for binding in lock['contractSuccessors']:
 record=json.loads((A/binding['record']['path']).read_text())
 assert not any(e['parent']==parent for e in record.get('passageSupersessions',[]))
 for e in record.get('passageOverrides',[]):
  if e['parent']==parent:carry.append(dict(origin='current-direct',contract=binding['record'],**project(e)))
assert len(carry)==145 and len({r['path']for r in carry})==145
B.mkdir();(B/'repository-file-inventory.v237.json').write_text(json.dumps(new,indent=2,ensure_ascii=False)+'\n')
report=dict(standing='PROPOSED strict own18path additive inventory237 for complete4b independent code/inventory review; not acceptance/publication/binding',parent=parent,candidate=pin(B,'repository-file-inventory.v237.json'),addedRows=rows,parentRows1392RetainedByValue=True,newRows=1410,allOtherFieldsUnchanged=True,packages=20,pendingDecisions=9,inheritedMeanings=138,currentDirectMeanings=7,totalMeanings=145,projections=carry,unitAccepted=False,inventoryBound=False,productQualification=False)
(B/'meaning-projection-preview.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');print('STRICT18 ADDITIONS/1410ROWS;138+7=145 MEANINGS; PREVIEWONLY')
