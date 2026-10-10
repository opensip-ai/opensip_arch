from pathlib import Path
import os,json,sys,subprocess,hashlib,re
B=Path('/tmp/opensip-implementation');D=B/'sm-experimental-dependency-preparation-2026-10-10';PY='/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14';os.setpriority(os.PRIO_PROCESS,0,10)
start=int(sys.argv[1]);stop=int(sys.argv[2]);ledger=D/f'data-round-driver-{start}-{stop}.json';assert not ledger.exists();records=[]
def write():ledger.write_text(json.dumps(dict(standing='ACTUAL EXPERIMENTAL PUBLIC DATA/GRAPH PREPARATION, UNREVIEWED',driverRange=[start,stop],callerExploratoryIterationLimitNotLaw=True,rounds=records,sourceAuthentication=False,typecheckExecuted=False,completeStatisticalSet=False,nativeAdmission=False,SMComplete=False),indent=2)+'\n')
def run(script,*args,isolated_site=False):
 log=D/(script.stem+'-driver.log');assert not log.exists()
 with log.open('xb') as f:p=subprocess.run([PY,'-I',*(['-S'] if isolated_site else []),'-B',str(script),*args],stdin=subprocess.DEVNULL,stdout=f,stderr=subprocess.STDOUT,close_fds=True)
 raw=log.read_bytes();row=dict(script=str(script),scriptBytes=script.stat().st_size,scriptSha256=hashlib.sha256(script.read_bytes()).hexdigest(),args=list(args),exitCode=p.returncode,log=dict(path=str(log),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()));records[-1]['operations'].append(row);write()
 if p.returncode:raise RuntimeError(f'Retained preparation failure {script.name}, exit{p.returncode}; inspect {log}')
for n in range(start,stop+1):
 prior=json.loads((D/f'corpus-graph-attempts-r{n}.json').read_bytes());errors=[r['outcome']['error'] for r in prior['results'] if r.get('outcome') and not r['outcome']['success']]
 records.append(dict(round=n,operations=[],priorSuccessfulGraphs=prior['successfulGraphs'],missingDiagnosticFirstLines=sorted(set(e.splitlines()[0] for e in errors))));write()
 if not errors:print('All nine graphs resolved; typecheck/statistics still owed',flush=True);break
 if any(not re.fullmatch(r'no matching package named `([A-Za-z0-9_-]+)` found',e.splitlines()[0]) for e in errors):print('Retained non-missing-package resolver result; no invented fix',flush=True);break
 for old,new in [('prepare_sm_missing_public_index_inputs_r3.py',f'prepare_sm_missing_public_index_inputs_r{n}.py'),('prepare_sm_missing_public_archives_r3.py',f'prepare_sm_missing_public_archives_r{n}.py')]:
  p=B/new;assert not p.exists();s=(B/old).read_text().replace('missing-public-index-inputs-r3',f'missing-public-index-inputs-r{n}').replace('missing-public-archive-inputs-r3',f'missing-public-archive-inputs-r{n}').replace('corpus-graph-attempts-r3',f'corpus-graph-attempts-r{n}').replace('assert len(items)==335','assert len(items)==sum(i[\'publishedVersionRecords\'] for i in receipt[\'inputs\'])');p.write_text(s)
 run(B/f'prepare_sm_missing_public_index_inputs_r{n}.py');run(B/f'prepare_sm_missing_public_archives_r{n}.py');archive=json.loads((D/f'missing-public-archive-inputs-r{n}/receipt.json').read_bytes());assert archive['recordsRequested']==archive['successfulWholeChecksumMatches'];records[-1].update(archives=archive['recordsRequested'],archiveBytes=archive['bytes']);write()
 # Deriver is input-only orchestration; accepted entry/collector bytes/images stay fixed.
 run(B/'prepare_next_dependency_round.py',str(n));run(B/f'prepare_sm_public_intake_packet_r{n}.py');run(B/f'run_sm_parameterized_public_intake_r{n}.py');run(B/f'prepare_sm_supplemental_registry_template_r{n+1}.py');run(B/f'prepare_sm_corpus_graph_packets_r{n+1}.py');run(B/f'run_sm_corpus_graph_attempts_r{n+1}.py',isolated_site=True)
 result=json.loads((D/f'corpus-graph-attempts-r{n+1}.json').read_bytes());records[-1].update(nextGraphAttempts=9,nextSuccessfulGraphs=result['successfulGraphs'],complete=True);write();print('Retained public data round',n,'archives',archive['recordsRequested'],'next graph success',result['successfulGraphs'],'of9; typecheck/statistical set remains false',flush=True)
 # Repeated first diagnostic after complete intake requires inspection, never invent source/version edits.
 nextlines=sorted(set(r['outcome']['error'].splitlines()[0] for r in result['results'] if r.get('outcome') and not r['outcome']['success']))
 if set(nextlines)&set(records[-1]['missingDiagnosticFirstLines']):print('Repeated missing diagnostic after complete intake; inspect retained source/index association',flush=True);break
print('Data round driver finished bounded caller range; full project incomplete',flush=True)
