"""Strict additive D4-4 inventory preview; preserve all accepted meanings, no repository writes."""
from pathlib import Path
import json,hashlib,copy,subprocess,os
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'inventory239-preview';assert not B.exists();P=Path('/Users/sb/code/opensip-ai/opensip');A=P.parent/'opensip_arch';W=P.parent/'opensip-d4factory-takeover'
def pin(root,path):
 b=(root/path).read_bytes();return dict(path=path,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
lock=json.loads((P/'design-lock.json').read_text());parent=lock['inventorySuccessors'][-1]['candidate'];assert parent['path'].endswith('.v238.json') and pin(A,parent['path'])==parent
raw=json.loads((A/parent['path']).read_text());prior={r['path']:r for r in raw['files']};new=copy.deepcopy(raw)
purpose={
'crates/components/src/provider_protocol/release_limits.rs':('opensip-components','codec','Pinned selected TS2 ten-member and Rust3 thirty-two-member Hello limit projections, independently checked against the selected handshake schema source; these constants are codec policy, not a new work profile.'),
'crates/components/src/session_factory.rs':('opensip-components','composition','Role-specific library session assembly from supplied admitted selection and separate authority projections, charged ControlContext and closed LaunchSpec assembly, actual codec-output validation, all-member association checks before final read-only rechecks, typed Budget/Io/Corrupt refusals, then sole production VerifiedLaunch construction. Owns neither C4 admission nor closure pins, spawn, Source custody, effects or settlement; operation retains CI capability through settlement and J2 remains the production caller.'),
'crates/components/src/session_factory/spec.rs':('opensip-components','validator','Charged comparison of the actual assembled control/codec output against independent selection, exact capability tokens, TS2 descriptor digest/field projections, Rust3 Plan identity and pinned Hello limits. Pristine sender includes realized-unsent Hello. Semantic map equality rejects duplicate keys without allocations. No authority, profile or source is minted.'),
'crates/components/src/session_factory/tests.rs':('opensip-components','test','Explicit synthetic pre-C4 factory controls over all eight Rust3 token profiles and TS2 descriptor/same-sender composition, independent field/member/spec differences, final recheck ordering and typed failure routes, and realized-unsent Hello refusal before any Source. Mock seam evidence is separate from actual native/store/provider-spoken controls and grants no C4/H/native admission.'),
'crates/host/src/launch_recheck.rs':('opensip-host','composition','D4-4 host LaunchRecheck over operation-borrowed CI-3 RetainedTree capabilities. Charged sorted role lookup and precheck of required kinds precede native launch_member. Resolved member labels come from the actual checked capability, optional file digests remain absent for directories, and checked path buffers move without unpriced copying. Budget and read I/O retain their owner partitions; no capability open/drop, source disclosure, spawning or production J2 wiring.'),
'crates/host/src/launch_recheck_tests.rs':('opensip-host','test','Actual profile-1 installed private first-party fixture stores with synthetic validated pre-C4 component/Plan inputs: physical member corruption, read-I/O injection, budget one-short before open/read, path binding, all named TS2 files, same checked sender composition, and real supervisor/codec controls against a SHA-pinned compiled peer under TestFixture. Retained peer reply bytes and valid-HelloAck baseline distinguish substitutions from EOF faults; source reads/snapshot bytes/Analyze stay zero. No signed/native/C4 admission, Linux, H settlement or qualification claim.'),
'crates/host/src/launch_recheck_wire_fixture.rs':('opensip-host','test','Explicit synthetic pre-C4 Rust3 Plan/request inputs from the public pinned D2b startup fixture with literal independent identity and capability authorities. Builds metadata only and supplies no Source, native Plan admission, trust or C4 selection.'),
'crates/host/src/launch_recheck_ts2_fixture.rs':('opensip-host','test','Explicit synthetic pre-C4 TS2 Plan/request and receiver projections matching public D2b fixture recipes, with separate literal A2 descriptor authorities and current sender output. No signed-descriptor verification, C4 selection, native admission or source custody is inferred from fixture consistency.'),
'crates/host/tests/factory_fixture.rs':('opensip-host','test','Harness-free compiled first-party D4-T3 peer, launched only as TestFixture using the exact factory-produced Rust3 or TS2 argv and retained member bytes. Private fixture mode selects closed deliberate control/identity/descriptor/token substitutions; records actual received frame names and flushed reply wire bytes. A matching HelloAck baseline unlocks only OpenUniverse before deliberate next-boundary refusal. Reads no repository bytes; not a native provider, production option or qualification executor.'),
'crates/host/tests/support/factory_ts2.rs':('opensip-host','test','Shared test-only literal synthetic TS2 provider/runtime descriptor field projections matching public D2b A2 fixtures. Used by host expected-authority and first-party peer construction; no signature validation, installed-runtime identity, native admission or new work policy is claimed.'),
'crates/platform/src/process_accounted.rs':('opensip-platform','adapter','Caller-funded exact closed TS2/Rust3 LaunchSpec construction, including raw native paths, fixed argv/environment, in-place NUL termination and explicit capacities, with literal independent price/parity and one-short/NUL controls. Test-only fixture class conversion invariant checks the full verified carrier. Selects no work profile, executable, admission or spawn policy.'),
}
paths=sorted(subprocess.check_output(['git','ls-files','-o','--exclude-standard'],cwd=W,text=True).splitlines());assert set(paths)==set(purpose) and len(paths)==11 and set(paths)&set(prior)=={'crates/components/src/session_factory.rs'};paths=[p for p in paths if p not in prior];assert len(paths)==10
rows=[]
for p in paths:
 package,role,description=purpose[p];r=dict(path=p,package=package,role=role,description='M3-D D4-4: '+description,generated=False,standing='proposed');new['files'].append(r);rows.append(r)
new['files'].sort(key=lambda r:r['path']);newmap={r['path']:r for r in new['files']};assert len(prior)==1422 and len(newmap)==1432 and len(new['files'])==1432
assert all(newmap[p]==r for p,r in prior.items());assert {k:v for k,v in new.items()if k!='files'}=={k:v for k,v in raw.items()if k!='files'}
indices={r['path']:i for i,r in enumerate(new['files'])};carry=[]
def physical(parent_pin,selector):
 assert pin(A,parent_pin['path'])==parent_pin;doc=json.loads((A/parent_pin['path']).read_text());parts=selector['jsonPointer'].split('/');assert len(parts)==4 and parts[1]=='files' and parts[3]=='description';return doc['files'][int(parts[2])]
def project(e):
 assert e['parent']==parent;row=physical(parent,e['selector']);assert row['description']==e['before'] and newmap[row['path']]==row
 return dict(path=row['path'],selector=dict(jsonPointer=f'/files/{indices[row["path"]]}/description'),before=e['before'],after=e['after'])
for e in lock['inventoryPassageInheritance']:carry.append(dict(origin='inherited',**project(e)))
assert len(carry)==150
records=[]
for binding in lock['contractSuccessors']:
 record_pin=binding['record'];assert pin(A,record_pin['path'])==record_pin;record=json.loads((A/record_pin['path']).read_text());records.append((record_pin,record))
 for e in record.get('passageOverrides',[]):
  if e['parent']==parent:carry.append(dict(origin='current-direct',contract=record_pin,**project(e)))
assert len(carry)==161 and len({r['path']for r in carry})==161
folds=[]
for record_pin,record in records:
 for e in record.get('passageSupersessions',[]):
  if e['parent']!=parent:continue
  path=physical(parent,e['selector'])['path'];current=next(r for r in carry if r['path']==path);assert current['after']==e['before'];sup=e['supersedes'];old_record=next(r for rp,r in records if rp==sup['record'])
  # A current supersession can target either an override OR a prior
  # supersession. This is required by accepted dispatch186 -> dispatch185.
  old=[x for key in ['passageOverrides','passageSupersessions'] for x in old_record.get(key,[]) if x['parent']==sup['parent'] and x['selector']==sup['selector']];assert len(old)==1 and old[0]['after']==e['before'] and physical(sup['parent'],sup['selector'])['path']==path
  current['after']=e['after'];current['foldedSupersession']=dict(record=record_pin,supersedes=sup,before=e['before'],after=e['after']);folds.append(path)
assert len(folds)==6 and len(set(folds))==6 and 'crates/components/src/provider_protocol.rs'in folds
for x in carry:assert newmap[x['path']]['description']==x['before']
B.mkdir();(B/'repository-file-inventory.v239.json').write_text(json.dumps(new,indent=2,ensure_ascii=False)+'\n')
report=dict(standing='PROPOSED strict10path additive inventory239 and exact161accepted meaning projection; all6current supersessions folded including supersession target; no repository mutation/binding/acceptance',parent=parent,candidate=pin(B,'repository-file-inventory.v239.json'),addedRows=rows,parentRows1422RetainedByValue=True,newRows=1432,materializedPriorRows=['crates/components/src/session_factory.rs'],allOtherFieldsUnchanged=True,packages=20,pendingDecisions=9,inheritedMeanings=150,currentDirectMeanings=11,totalMeanings=161,foldedCurrentSupersessions=folds,projections=carry,unitAccepted=False,inventoryBound=False,productQualification=False)
(B/'meaning-projection-preview.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');print('STRICT10 ADDITIONS/1432ROWS + PRIOR FACTORY ROW MATERIALIZED;150+11=161 MEANINGS; ALL6 CURRENT SUPERSESSIONS FOLDED; PREVIEWONLY')
