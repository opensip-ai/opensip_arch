from pathlib import Path
import json,hashlib,collections
F=Path(__file__).parent;A=Path('/Users/sb/code/opensip-ai/opensip_arch');W=A.parent/'opensip-rust3-successor-takeover';p=A/'docs/coop/design-corrections/native/native-cases.v2.json';raw=p.read_bytes();sha=hashlib.sha256(raw).hexdigest();assert sha=='a08b8cc380a2d332a752405fde11df1d5d63b050c7297ec21820516702367ddc'
d=json.loads(raw);table=json.loads((W/'crates/components/tests/data/table-vectors.rust3.v1.json').read_text());table_ids={v['id']for v in table['nativeCases']};expected_table={c['id']for c in d['cases']if any(s['fn']=='protocol3_run'for s in c['steps'])};assert table_ids==expected_table and len(table_ids)==6
wire={'admit_provider_hello','admit_provider_hello_ack','admit_provider_fact_batch','provider_startup_exchange','protocol3_open_universe_event','provider_wire_limits'};defs={'DependencySourceManifestV3','DependencySourceSealV3','CoverageResultV3','ResolutionCompletenessV2'};out=[];counts=collections.Counter()
for case in d['cases']:
 steps=[]
 for i,step in enumerate(case['steps']):
  fn=step['fn'];args=step.get('args',{});status='outside-codec-executor';reason='No standalone D2b wire-input predicate called by this executor. Supporting fixture/oracle steps may feed a separately classified wire step.'
  if fn=='protocol3_run':status='inherited-table-replay';reason='Exact same6public case IDs in current vendored table vector nativeCases; owning test the_native_cases_replay_under_the_overlay passed in full407suite.'
  elif fn in wire:
   language=args.get('language','rust-semantic' if fn=='protocol3_open_universe_event' else None)
   if language=='typescript-semantic':status='ts2-separate';reason='TS2 codec; not a Rust3 result. Separate TS2 evidence still must be traced for a full project claim.'
   else:status='rust3-wire-scope-audit-pending';reason='Rust3 wire/startup predicate or context projection must be replayed at actual current owner; historical abstract events/host conversion/native admission cannot be claimed by a codec test.'
  elif fn=='validate'and args.get('def')in defs:status='shared-wire-schema-audit-pending';reason='Native schema also consumed transitively by Rust3 wire; test the selected schema predicate, preserving bool/integer distinctions. No generic C4/H validation inferred.'
  elif fn in ['negotiate','admit_requested_capabilities']:reason='Plan/provider capability selection (C4/D4); descriptor arrays/ownership tuples are not a D2b wire payload. Exact HelloAck echo has separate D2b wire controls.'
  if case['id']=='provider-wire-per-language-limit-maps-equal-the-published-inherited-values'and args.get('language')=='rust-semantic':status='rust3-scoped-predicate-pass';reason='Exact original32limit map compared with actual Request-built Hello limits; successor-owning-r8 test replay_native_cases_rust_limits_and_empty_dependency_shapes.'
  if case['id']=='startup-rust3-empty-dependency-manifest-and-seal-admit':status='rust3-scoped-predicate-pass';reason='Both exact original empty DependencySourceManifestV3/SealV3 payloads admitted by current selected schema paths; successor-owning-r8. No raw digest/custody/C4 proof inferred.'
  steps.append(dict(index=i,executor=fn,disposition=status,reason=reason));counts[status]+=1
 out.append(dict(id=case['id'],steps=steps))
assert len(out)==477 and len({c['id']for c in out})==477
report=dict(standing='UNACCEPTED EXHAUSTIVE SCOPE AUDIT PREPARATION. Audit all477pinned native cases, a strict superset of the named101wire/startup cases; no count-matching subset is treated as authoritative. Pending wire steps remain work, not passes.',source=dict(path=str(p),bytes=len(raw),sha256=sha),historicalSourcePinVerifiedIn='native-wire-owner-07/subject/tools/common.py: ARCH_PINS.nativeCases',cases=len(out),stepDispositions=dict(counts),inheritedTableEvidence=dict(path='crates/components/tests/data/table-vectors.rust3.v1.json',sha256=hashlib.sha256((W/'crates/components/tests/data/table-vectors.rust3.v1.json').read_bytes()).hexdigest(),caseIds=sorted(table_ids),scope='Only actual table/overlay outcomes; no generated-carrier admission, startup host conversion or native authority claimed.'),entries=out)
(F/'native-full-scope-audit-r1.json').write_text(json.dumps(report,indent=2)+'\n');print(dict(counts))
old=F/'native101-scope-audit-preparation-r1.json';r=json.loads(old.read_text());r['standing']='SUPERSEDED COUNT-MATCHING PREPARATION, NOT AN AUTHORITATIVE101SUBSET. Exhaustive477case audit native-full-scope-audit-r1.json replaces this selector to avoid dropping any wire case.';old.write_text(json.dumps(r,indent=2)+'\n')
