"""Strict additive preview; fold current explicit dispatch supersession; no repository writes."""
from pathlib import Path
import json,hashlib,copy,subprocess,os
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'inventory238-preview';assert not B.exists();P=Path('/Users/sb/code/opensip-ai/opensip');A=P.parent/'opensip_arch';W=P.parent/'opensip-rust3-successor-takeover'
def pin(root,path):
 b=(root/path).read_bytes();return dict(path=path,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
lock=json.loads((P/'design-lock.json').read_text());parent=lock['inventorySuccessors'][-1]['candidate'];assert parent['path'].endswith('.v237.json')and pin(A,parent['path'])==parent
raw=json.loads((A/parent['path']).read_text());prior={r['path']:r for r in raw['files']};new=copy.deepcopy(raw)
paths=sorted(subprocess.check_output(['git','ls-files','-o','--exclude-standard'],cwd=W,text=True).splitlines());assert len(paths)==12 and not set(paths)&set(prior)
purpose={
'census.rs':('codec','Source-bound FA-2 census request and selected CompleteV3 admission, native-H D-empty checks against supplied scope cells, source-checked metadata/item decomposition using the same selected schema evaluator, nativeSubjectId and canonical examined-path order, count and exact original-node byte bounds, path membership and typed over-bound validation. C4 owns selection and admitted inputs; H owns returned symbol-scope settlement; no schema owner or native inventory mint.'),
'census_tests.rs':('test','Public synthetic census request/return controls: typed complete/over-bound and original-buffer handoff, exact nullable/token selection, order/duplicate/membership and clean-terminal count refusals, exact4MiB/+1 received bytes and100000/+1 path/row predicates. Row shape cardinality is explicitly separate from received-byte admissibility; no native/source admission or qualification.'),
'replay_tests.rs':('test','Hash-pinned public Rust3 trial07 and successor predicate replays, exact original rawfloat0.0 refusal, original received-preimage commitment tests and complete31rule/353case ownership partition. Supplemental native input audit records actual current RCA-1/profile refusals without relabeling old64character compiler commits or crediting historical later outcomes; illustrative/current-context adapters confer no C4/H authority or reference-wide conformance.'),
'accounting_replay_tests.rs':('test','Exact historical20Rust3 request-accounting quantities through actual Recorder, envelope/chunk sizers and production manifest-count predicate, including64MiB/+1frame and9GiB/+1request. Original duplicate symbolic coordinates, placeholder identities/digests and empty Analyze remain mechanical inputs, not current C4/Plan admission; no GiB dummy chunk allocation.'),
'participant_successor_tests.rs':('test','Nonblocking fake-pipe/custody successor composition for all8Rust3token combinations, typed complete/over-bound and null census, original buffers moved once afterZeroExit/EOF, clean terminal D-empty zero counts, nonsymbol exact counts/scopes, pendingAnalyze before oneCancel and typed input-rejected fault normalization. No spawn, native admission, census settlement or production qualification.'),
'sender_replay_tests.rs':('test','Historical Rust3 send/custody predicates:39small actual independent sender transcripts over explicit synthetic current projections, original24byte override at the actual greedy constructor and2symbolicGiB charging/greedy cases. Preserves typed echo/mutation values and originalabc custody data, distinguishing lawful fragmented bytes from canonical greedy host schedule; no physicalGiB custody or original wholePlan conformance claimed.'),
'native-rust3-profile-cases.v1.json':('fixture','Exact public native-case literal views and shared-schema bool negatives, extracted from the pinned historical source. Current RCA-1/profile refusals are recorded separately from historical expected outcomes: no64to40compiler-commit conversion, private fact JSON projection accepted as wire, or whole-executor/native conformance claim.'),
'native-wire-public-fixtures.v1.json':('fixture','Pinned public native-case Rust limit map and empty dependency manifest/seal inputs with original case metadata. Rust branch and selected schema predicate evidence only, not TS2 results, native-H/custody admission or qualification.'),
'rust3-lim-vectors.v1.json':('fixture','Byte-exact pinned accepted RUST3-LIM successor vectors. Rust3 subject/scope/domain recipes and reference metadata are replayed at owning predicates; illustrative PlanStage/Coverage placeholders do not establish current C2/C4 admission.'),
'rust3-trial07-replay-scope.v1.json':('fixture','Complete hash-pinned31rule/353original-case historical trial07 scope partition:194integer Rust3 scoped predicates plus separate rawfloat refusal,48TS2 and110C4/H owner-external cases. Lists exact adapters and limits; owner-external cases are not codec passes or completed project work.'),
'trial07-accounting-fixtures.v1.json':('fixture','Exact retained public historical Hello/OpenUniverse/prepared fixtures with source pin, used only by request byte accounting. Old compiler identities, placeholder manifests, symbolic repeated paths and minimal Analyze are not current admitted carriers/Plan/source authority.'),
'trial07-prepared-fixture.v1.json':('fixture','Public historical prepGenerated extraction retained by JSON value from the pinned native-case source, for original prepared entry and digest/join mutation controls. Synthetic native projections and supplied custody do not establish C4 selection, freshness, read authority or source admission.'),
}
rows=[]
for p in paths:
 role,text=purpose[Path(p).name];r=dict(path=p,package='opensip-components',role=role,description='M3-D D2b-4c: '+text,generated=False,standing='proposed');new['files'].append(r);rows.append(r)
new['files'].sort(key=lambda r:r['path']);newmap={r['path']:r for r in new['files']};assert len(prior)==1410 and len(newmap)==1422 and len(new['files'])==1422
assert all(newmap[p]==r for p,r in prior.items());assert {k:v for k,v in new.items()if k!='files'}=={k:v for k,v in raw.items()if k!='files'}
indices={r['path']:i for i,r in enumerate(new['files'])};carry=[]
def physical(parent_pin,selector):
 assert pin(A,parent_pin['path'])==parent_pin;doc=json.loads((A/parent_pin['path']).read_text());parts=selector['jsonPointer'].split('/');assert len(parts)==4 and parts[1]=='files'and parts[3]=='description';return doc['files'][int(parts[2])]
def project(e):
 assert e['parent']==parent;row=physical(parent,e['selector']);assert row['description']==e['before']and newmap[row['path']]==row
 return dict(path=row['path'],selector=dict(jsonPointer=f'/files/{indices[row["path"]]}/description'),before=e['before'],after=e['after'])
for e in lock['inventoryPassageInheritance']:carry.append(dict(origin='inherited',**project(e)))
assert len(carry)==145
records=[]
for binding in lock['contractSuccessors']:
 record_pin=binding['record'];assert pin(A,record_pin['path'])==record_pin;record=json.loads((A/record_pin['path']).read_text());records.append((record_pin,record))
 for e in record.get('passageOverrides',[]):
  if e['parent']==parent:carry.append(dict(origin='current-direct',contract=record_pin,**project(e)))
assert len(carry)==150 and len({r['path']for r in carry})==150
folds=[]
for record_pin,record in records:
 for e in record.get('passageSupersessions',[]):
  if e['parent']!=parent:continue
  path=physical(parent,e['selector'])['path'];current=next(r for r in carry if r['path']==path);assert current['after']==e['before'];sup=e['supersedes'];old_record=next(r for rp,r in records if rp==sup['record']);old=next(x for x in old_record['passageOverrides']if x['parent']==sup['parent']and x['selector']==sup['selector']);assert old['after']==e['before']and physical(sup['parent'],sup['selector'])['path']==path
  current['after']=e['after'];current['foldedSupersession']=dict(record=record_pin,supersedes=sup,before=e['before'],after=e['after']);folds.append(path)
assert folds==['crates/components/src/provider_protocol.rs']and len(carry)==150
for x in carry:assert newmap[x['path']]['description']==x['before']
B.mkdir();(B/'repository-file-inventory.v238.json').write_text(json.dumps(new,indent=2,ensure_ascii=False)+'\n')
report=dict(standing='PROPOSED strict12path additive inventory238 and exact150accepted meaning projection; explicit185dispatch supersession folded, no repository mutation/binding/acceptance',parent=parent,candidate=pin(B,'repository-file-inventory.v238.json'),addedRows=rows,parentRows1410RetainedByValue=True,newRows=1422,allOtherFieldsUnchanged=True,packages=20,pendingDecisions=9,inheritedMeanings=145,currentDirectMeanings=5,totalMeanings=150,foldedCurrentSupersessions=folds,projections=carry,unitAccepted=False,inventoryBound=False,productQualification=False)
(B/'meaning-projection-preview.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');print('STRICT12 ADDITIONS/1422ROWS;145+5=150 MEANINGS;185DISPATCHFOLDED; PREVIEWONLY')
