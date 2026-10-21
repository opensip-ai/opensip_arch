from pathlib import Path
import json,hashlib,collections
W=Path('/Users/sb/code/opensip-ai/opensip-rust3-successor-takeover');F=Path(__file__).parent
D=json.loads((W/'crates/components/tests/data/trial07-integer-replay.v1.json').read_text());old=json.loads((F/'replay-progress-r2.json').read_text());selected={(x['rule'],x['id'])for x in old['cases']if x['standing'].startswith('PASS')}
upstream={'DEPSRC-SET-KEY-CONSTRAINTS':'C4 dependency-source admission before PlanId','DEPSRC-WIRE-REPRESENTABILITY':'C4 dependency-source admission/owner refusal precedence','PREPARED-V3-PATH-REPRESENTABILITY':'C4 prepared-output admission and selection','PREPARED-V3-WIRE-LIMIT':'C4 prepared-output admission/selection/fallback and precedence','PREPARED-V3-READ-AUTHORITY':'C4 prepared-output selection/read authority','RELATION-PAYLOAD-PATH-LAW':'H registered-record fact admission','PER-KEY-SCOPE2':'C4 descriptor minting and H coverage admission; D2b echoes checked separately'}
rules=[];counts=collections.Counter()
for rule,rows in D['vectors'].items():
 cases=[]
 for row in rows:
  inp=row['input'];i=row['id'];key=(rule,i)
  owned=(key in selected or rule=='HOST-SEND-SCHEDULE' and inp['send']['plan']['protocol']=='rust-semantic' or rule=='CHUNK-CUSTODY' or rule=='ANCHOR-FACT-REF-REFUSED' and inp['language']=='rust-semantic' or rule=='OWNER-PATTERN-EVALUATION' and (inp['owner']['call']=='startup-open-universe' or inp['owner']['call']=='validate' and inp['owner']['def']=='GeneratedFileV1'))
  if owned:
   disposition='rust3-scoped-predicate';reason='Actual Rust3 builder, receiver, schema, sender or accounting predicate; scope notes delimit current-context adapters.'
  elif rule in upstream:
   disposition='upstream-owner';reason=upstream[rule]
  elif rule=='OWNER-PATTERN-EVALUATION':
   assert inp['owner']['call']in ['validate','dependency-set','prepared-set'];disposition='upstream-owner';reason='C4 native evidence file-manifest/set or prepared-set admission; not a D2b wire schema consumer.'
  else:
   assert rule in ['TS2-LOGICAL-PATH-ADMISSION','TS2-MANIFEST-DIGEST'] or rule=='HOST-SEND-SCHEDULE' and inp['send']['plan']['protocol']=='typescript-semantic' or rule=='REQUEST-WIRE-ACCOUNTING' and inp['plan']['protocol']=='typescript-semantic' or rule in ['ANCHOR-WIRE-SPAN','ANCHOR-FACT-REF-REFUSED'] and inp['language']=='typescript-semantic' or rule=='PATH-SITE-SEGMENT-LAW' and inp['site']in ['jsRootFiles','programRootFiles'] or rule=='COMMIT-MAP' and inp['commitment']['$ownerCommit']['doc']!='rust2',(rule,i)
   disposition='ts2-separate';reason='TS2 separate implementation/replay; not a Rust3 result.'
  cases.append(dict(id=i,disposition=disposition,reason=reason));counts[disposition]+=1
 rules.append(dict(rule=rule,cases=cases))
assert len(rules)==31 and sum(counts.values())==352
assert dict(counts)=={'rust3-scoped-predicate':194,'ts2-separate':48,'upstream-owner':110},counts
out=dict(standing='UNACCEPTED D2b-4c replay scope proposal; full31rule partition, not fullproject qualification',authority='docs/implementation/m3/supervisor-d/d2b/PLAN-r3.md: LD-D2B-14 and duty allocation section3',sources=dict(originalAdmissionSha256='e93c69e57f24c8309544c5773b2394d2c8973d2dcb67da604afb2bb1edc06290',integerSelectionSha256='79d0ee27533f3c4a5ac2c3f90db9423412304a7148aeaec41582c892f56dc9ae'),counts=dict(counts),rawFloat=dict(rule='HOST-SEND-SCHEDULE',rawVectorSha256='3587eda94e92a75717fd24a4970c55764a43be3c9452b5c554f170d384fc4c97',disposition='rust3-scoped-predicate',proof='Original raw analysisOrdinal0.0 retained; JSON profile refuses float and real CBOR floatzero frame refused. No coercion.'),scopeNotes=[
'Historical illustrative Plan quantities, placeholder raw digests and native identities are not current C4 admission. Current stage/context duties require separate controls.',
'Small sender descriptions retain original quantities, mutations and typed echo values in independently built synthetic current C4 projections; one same-length nonempty .rs coordinate, actual zero-source hashes and native H joins replace historical placeholders. No source acquisition or C4 authority claimed.',
'39small sender cases use actual independent sender realization. The alternate-split case retains original24-byte numeric maximum at the production dependency greedy constructor; a current Hello cannot negotiate that test override.',
'Two symbolic multi-GiB sender cases retain original schedule quantities and exact9GiB total at production Sender charging and snapshot greedy constructor; no physical multi-GiB custody or complete current request admission claimed.',
'CHUNK-CUSTODY lawful fragmented abc stream admits canonical greedy host realization from its original bytes; original alternate split separately refuses as a host schedule. Wrong content reaches actual sender digest refusal; bad offset/empty entry reach actual greedy constructor.',
'OWNER-PATTERN startup cases retain exact original tested paths in current schema-shaped enclosing carriers. Generated-file cases retain original public generated fixture and exact path mutations. Native file-manifest/set calls remain C4.',
'REQUEST-WIRE-ACCOUNTING retains exact symbolic repeated coordinates, placeholder digests, original Hello/OpenUniverse and empty Analyze at production Recorder/sizers; current native/shape/Plan admission is not inferred.',
'Snapshot entry-bound actual builder controls expand symbolic pathScalars1 to distinct fNNNNNN coordinates only for cardinality. Other symbolic over-count cases exercise the shared production manifest-cardinality predicate before allocation.',
'COMMIT-MAP/raw digest use actual selected commitment recipes and retained preimages; illustrative entries are not full Coverage/context admission. Census returned commitment settlement remains H.',
'No upstream-owner or TS2-separate case is credited as a Rust3 pass or as completed project work.'
],rules=rules)
p=F/'replay-scope-prepared-r1.json';p.write_text(json.dumps(out,indent=2)+'\n');print(dict(counts));print('Prepared',p)
