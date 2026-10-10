from pathlib import Path
import json,hashlib,shutil,collections,os
os.setpriority(os.PRIO_PROCESS,0,10)
B=Path('/tmp/opensip-implementation');V=B/'sm-command-data-2026-10-10';S=B/'sm-actual-command-pilots-r1-draft';assert not S.exists();S.mkdir()
def pin(p):b=p.read_bytes();return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def check(r):p=Path(r['path']);assert pin(p)=={k:r[k] for k in ['bytes','sha256']};return p
def copy(p,rel):t=S/rel;t.parent.mkdir(parents=True,exist_ok=True);assert not t.exists();shutil.copyfile(p,t);assert pin(p)==pin(t)
m=json.loads((V/'actual-command-source-maps-r1.json').read_bytes());rt=json.loads((V/'actual-lint-command-profile-pilots-r1.json').read_bytes());assert len(m['results'])==len(rt['results'])==9 and rt['totalCompilerChildren']==79
for n in ['actual-command-source-maps-r1.json','actual-lint-command-profile-pilots-r1.json']:copy(V/n,n)
receipt=check(m['dependencyDataReceipt']);copy(receipt,'collector-data/actual-command-data-attempts-r1.json');cr=json.loads(receipt.read_bytes());summary=[];unit=collections.Counter();roots=collections.Counter()
for e,r in zip(m['results'],rt['results']):
 i=e['ordinal'];assert i==r['ordinal'] and e['graph']==r['graph'] and e['unitCommandData']==r['unitCommandData'] and e['sourceMap']==r['preparedMap'] and e['excluded']==[]
 for k in ['graph','packet','unitCommandData','sourceMap']:copy(check(e[k]),f'inputs/{i}/{k}.'+('bin' if k=='sourceMap' else 'json'))
 pkt=json.loads(check(e['packet']).read_bytes());member=Path(pkt['memberRoot'])
 for f in pkt['originalFiles']:assert pin(member/f['path'])=={k:f[k] for k in ['bytes','sha256']}
 collector=Path(e['packet']['root'])
 for p in sorted(collector.rglob('*')):
  if p.is_file() and 'home' not in p.relative_to(collector).parts:copy(p,f'actual-collector/{i}/'+p.relative_to(collector).as_posix())
 result=r['result'];output=Path(rt['root'])/str(i)
 if result is None:assert not output.exists() and r['executionRefusedBeforeLaunch'];counts={};rs={};children=0
 else:
  counts=dict(collections.Counter(u['standing'] for u in result['unitResults']));rs=dict(collections.Counter(u['standing'] for u in result['rootResults']));children=result['compilerChildren'];unit.update(counts);roots.update(rs)
  for p in sorted(output.rglob('*')):
   if p.is_file():copy(p,f'actual-pilots/{i}/'+p.relative_to(output).as_posix())
 graph=json.loads(check(e['graph']).read_bytes());cmd=json.loads(check(e['unitCommandData']).read_bytes());summary.append(dict(id=e['id'],ordinal=i,graphUnits=len(graph['units']),graphRoots=len(graph['roots']),staticCommandRows=sum(u['staticCargoCommandConstructed'] for u in cmd['units']),compilerChildren=children,unitStandings=counts,rootStandings=rs,executionRefusedBeforeLaunch=r.get('executionRefusedBeforeLaunch'),preparedFiles=e['preparedFiles'],sourceContentBytes=e['sourceContentBytes']))
for n in ['source.json','subject.json','integration.json']:copy(B/'sm-lint-command-profile-controls-r1-stage'/n,'closed-parent-reference/'+n)
for n in ['REVIEW.md','review.json']:copy(B/'reviews/grok-sm-lint-command-profile-controls-r1'/n,'closed-parent-reference/'+n)
for n in ['prepare_sm_actual_command_data_packets_r1.py','run_sm_actual_command_data_attempts_r1.py','prepare_sm_actual_command_source_maps_r1.py','run_sm_actual_lint_command_profile_pilots_r1.py']:
 if (B/n).exists():copy(B/n,'runners/'+n)
s=dict(unit='SM-ACTUAL-COMMAND-PILOTS-r1',standing='NEW ACTUAL NINE STATIC CARGO COMMAND COLLECTION AND PARTIAL PROFILE PILOTS; UNREVIEWED',manifestEntries=9,requiredWorkloads=8,graphUnits=sum(r['graphUnits'] for r in summary),graphRoots=sum(r['graphRoots'] for r in summary),staticCommandsConstructed=sum(r['staticCommandRows'] for r in summary),collectorRoots=9,collectorInformationQueries=36,pilotEntriesLaunched=7,pilotEntriesRefusedBeforeLaunch=2,compilerChildren=79,unitStandings=dict(unit),rootStandings=dict(roots),entries=summary,closedExecutorSource=rt['executorPin'],closedWrapperImage=next(r['result']['wrapperPin'] for r in rt['results'] if r['result']),closedCargoImage=json.loads((B/'sm-command-data-controls-r1-stage/source.json').read_bytes())['compiledCargoImage'],supportingOnly=True,staticProfileCheckCfgArgumentsApplied=True,constructedPackageEnvironmentCwdCapLintsUsed=True,acceptedParentsUnchanged=True,newCompilerSource=False,newGraphExecutor=False,controlsRerun=False,applicationExecuted=False,completeRuntimeCommand=False,fullCargoProfileEnvironment=False,physicalPeakScratchMeasured=False,completeStatisticalSet=False,sourceAuthentication=False,nativeAdmission=False,productChange=False,SMComplete=False,effectiveL=False,productQualification=False,entirePlanComplete=False)
assert s['graphUnits']==591 and s['graphRoots']==47 and s['staticCommandsConstructed']==178 and s['unitStandings']['analysis-and-metadata-completed']==79
(S/'draft-source.json').write_text(json.dumps(s,indent=2)+'\n');(S/'REPORT.md').write_text('''# Actual static Cargo command collection and partial profile pilots

Nine new actual offline collector executions preserve the exact original nine-entry/eight-workload selection. Thirty-six INFO queries resolve591units47roots and construct178 static Cargo command rows, including one binary row. BuildRunner is initialized for static DATA only; its compile/dry_run/job queue is never called. Full collector packets/queries/graphs/command data/source maps/original byte checks are retained. Fresh raw cache copies are content totals, not physical peak scratch or authenticated source closure.

The exact independently accepted long-lint static-profile executor attempts all nine entries. NAPI and Axum refuse before any output directory or child because actual Cargo manifest lint spellings contain hyphens outside this parser's explicit grammar. Their unchanged command inputs and refusals are retained. Seven other entries launch79children; every launched analysis completes and emits whole-pinned reusable library metadata. Unavailable units/roots are retained, never counted as analyzed. Binary/expansion/script targets remain unavailable. Static profile/check-cfg/cap arguments and actual package env/cwd are used; operational source/output/incremental/extern/search paths are rebound to checked source maps and private outputs. No application/build script/proc macro executes.

This packet does not amend native RustflagsProjectionV1, normalize lint names, suppress diagnostics or change source/features/lock selection. The separately prepared Cargo manifest hyphen spelling variant and any later retry are outside scope and require their own acceptance. Accepted controls are not rerun; earlier pilots remain closed and unchanged. Metadata/sysroot/runtime sealing, native authentication, full profile/runtime, physical peak resource accounting, statistical qualification, S-M/effective L/product qualification remain false. Product/law/lock/inventory187/contracts161 unchanged; O7/D3/D13 closed. Independent exact review and lead assent plus actual design/implementation verification precede architecture-only publication; no push.
''')
C=Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06');f=C/'CURRENT-STATE.json';st=json.loads(f.read_bytes());st['SMActualCommandPilotsPreparation']=dict(draft=str(S),compilerChildren=79,staticCommandsConstructed=178,collectorInformationQueries=36,pilotEntriesRefusedBeforeLaunch=2,reviewed=False,SMComplete=False);f.write_text(json.dumps(st,indent=2)+'\n');shutil.copytree(S,C/'continuation-preserved'/S.name,dirs_exist_ok=True);print(json.dumps({k:s[k] for k in ['graphUnits','graphRoots','staticCommandsConstructed','compilerChildren','unitStandings','rootStandings']},indent=2))
