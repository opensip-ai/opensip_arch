from pathlib import Path
import json,os,hashlib,subprocess,tempfile,time,struct,stat
B=Path(__file__).resolve().parent;D=B.parent;g=json.loads((D/'axum-unit-graph.json').read_text());m=json.loads((D/'axum-resolved-metadata.json').read_text());pkgs={p['id']:p for p in m['packages']};readiness=json.loads((D/'axum-unit-noexec-readiness.json').read_text());eligible=set(readiness['compilerEligibleUnits']);audit=json.loads((D/'axum-dependency-source-audit.json').read_text());runtime=json.loads((B/'build.json').read_text());exe=Path(runtime['executable']);assert hashlib.sha256(exe.read_bytes()).hexdigest()==runtime['sha256'];os.setpriority(os.PRIO_PROCESS,0,10);darwin=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());T=Path(tempfile.mkdtemp(prefix='opensip-sm-axum-compiler-',dir=darwin));T.chmod(0o700);output=T/'metadata';output.mkdir();prepared=T/'sources.bin';source_rows=[]
root=Path(json.loads((D/'axum-resolved-metadata-attempt.json').read_text())['originalLock']['path']).parent
expected=[]
for row in audit['rows']:
 for f in row['regularFiles']:expected.append((Path(row['root'])/f['path'],f))
for p in root.rglob('*'):
 if p.is_file():raw=p.read_bytes();expected.append((p,dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())))
with prepared.open('wb') as dest:
 dest.write(b'OPSMRUST1\0'+struct.pack('>Q',len(expected)))
 for p,r in sorted(expected):
  assert stat.S_ISREG(p.lstat().st_mode);fd=os.open(p,os.O_RDONLY|os.O_CLOEXEC|os.O_NOFOLLOW)
  with os.fdopen(fd,'rb') as f:before=os.fstat(f.fileno());raw=f.read();after=os.fstat(f.fileno());assert (before.st_size,before.st_mtime_ns,before.st_ctime_ns)==(after.st_size,after.st_mtime_ns,after.st_ctime_ns)
  assert len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256'];name=str(p).encode();dest.write(struct.pack('>Q',len(name))+name+struct.pack('>Q',len(raw))+raw);source_rows.append(dict(r,path=str(p)))
prepared.chmod(0o400);lane=darwin/'opensip-lanes.lock';owned=False
while True:
 try:lane.mkdir();owned=True;break
 except FileExistsError:print('Waiting for ordinary compiler observation lane',flush=True);time.sleep(5)
try:
 rows=[];done={};remaining=set(eligible)
 while remaining:
  ready=sorted(i for i in remaining if all(d['index'] in done for d in g['units'][i]['dependencies']));assert ready,'unit cycle'
  for i in ready:
   remaining.remove(i);u=g['units'][i];deps=u['dependencies'];failed=[d['index'] for d in deps if done[d['index']]['exitCode']!=0]
   if failed:row=dict(index=i,pkg_id=u['pkg_id'],standing='INCOMPLETE dependency did not compile',failedDependencies=failed,exitCode=None);rows.append(row);done[i]=row;continue
   assert u['target']['kind']==['lib'] and u['mode']=='check' and u['platform'] is None;assert u['target']['crate_types']==['lib'];pkg=pkgs[u['pkg_id']];artifact=output/('lib'+u['target']['name']+'_'+str(i)+'.rmeta');args=[str(exe),'--prepared-map',str(prepared),'--spike-emit-metadata','--crate-name',u['target']['name'],'--crate-type','lib','--edition',u['target']['edition'],'--sysroot',runtime['sysroot'],'--emit','metadata',u['target']['src_path'],'-o',str(artifact),'-L','dependency='+str(output),'-C','metadata=opensip_spike_unit_'+str(i),'-C','opt-level='+u['profile']['opt_level'],'-C','debug-assertions='+('yes' if u['profile']['debug_assertions'] else 'no'),'-C','overflow-checks='+('yes' if u['profile']['overflow_checks'] else 'no'),'-C','panic='+u['profile']['panic'],'-C','debuginfo='+str(u['profile']['debuginfo']),'-C','split-debuginfo='+u['profile']['split_debuginfo']]
   if pkg['source'] is not None:args+=['--cap-lints','allow'] # exact Cargo upstream dependency policy, not product lint weakening
   for feature in u['features']:args+=['--cfg','feature='+json.dumps(feature)]
   for dep in deps:
    assert not dep.get('noprelude',False);args+=['--extern',dep['extern_crate_name']+'='+done[dep['index']]['artifact']['path']]
   E=dict(PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',TMPDIR=str(T));
   if 'HOME' in os.environ:E['HOME']=os.environ['HOME']
   version=pkg['version'].split('-',1);parts=version[0].split('.');E.update(CARGO_MANIFEST_DIR=str(Path(pkg['manifest_path']).parent),CARGO_MANIFEST_PATH=pkg['manifest_path'],CARGO_CRATE_NAME=u['target']['name'],CARGO_PKG_NAME=pkg['name'],CARGO_PKG_VERSION=pkg['version'],CARGO_PKG_VERSION_MAJOR=parts[0],CARGO_PKG_VERSION_MINOR=parts[1],CARGO_PKG_VERSION_PATCH=parts[2],CARGO_PKG_VERSION_PRE=version[1] if len(version)>1 else '',CARGO_PKG_AUTHORS=':'.join(pkg['authors']),CARGO_PKG_DESCRIPTION=pkg['description'] or '',CARGO_PKG_HOMEPAGE=pkg['homepage'] or '',CARGO_PKG_REPOSITORY=pkg['repository'] or '',CARGO_PKG_LICENSE=pkg['license'] or '',CARGO_PKG_LICENSE_FILE=pkg['license_file'] or '',CARGO_PKG_README=pkg['readme'] or '',CARGO_PKG_RUST_VERSION=pkg['rust_version'] or '')
   stdout=B/(str(i)+'.stdout');stderr=B/(str(i)+'.stderr');start=time.monotonic_ns()
   with stdout.open('wb') as o,stderr.open('wb') as e:
    child=subprocess.Popen(args,cwd=T,env=E,stdout=o,stderr=e);priority=os.getpriority(os.PRIO_PROCESS,child.pid);assert priority==10;code=child.wait()
   events=[json.loads(x) for x in stdout.read_text().splitlines()];analysis=any(x['event']=='after_analysis' for x in events);row=dict(index=i,pkg_id=u['pkg_id'],args=args,constructedPackageEnvironment={k:v for k,v in E.items() if k.startswith('CARGO_')},exitCode=code,afterAnalysis=analysis,elapsedNanos=time.monotonic_ns()-start,observedNiceness=priority,stdout=str(stdout),stderr=str(stderr),expandedAstFunctionHeaderObservations=sum(x['event']=='expanded_ast_function_header_observation' for x in events),effectiveExportObservations=sum(x['event']=='effective_export_observation' for x in events),definitionObservations=sum(x['event']=='local_definition_observation' for x in events),importObservations=sum(x['event']=='import_observation' for x in events),sourceFileObservations=sum(x['event']=='source_file_observation' for x in events),itemVisibilityObservations=sum(x['event']=='item_visibility_observation' for x in events),artifact=None)
   if code==0:assert analysis and artifact.is_file();raw=artifact.read_bytes();row['artifact']=dict(path=str(artifact),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
   rows.append(row);done[i]=row;print(i,u['target']['name'],'PASS' if code==0 else 'INCOMPLETE',flush=True)
 v=dict(standing='UNREVIEWED ACTUAL PRIVATE PREPARED-SOURCE CARGO-UNIT COMPILER OBSERVATIONS; NOT C2 CONTEXT/PLAN OR FULL WORKLOAD',rows=rows,compilerEligibleUnits=len(eligible),successfulUnits=sum(r['exitCode']==0 for r in rows),incompleteUnits=sum(r['exitCode']!=0 for r in rows),excludedUnits=readiness['directExcludedUnits']+readiness['transitivelyIncompleteUnits'],runtime=runtime,preparedSourceFiles=len(source_rows),preparedSourceMapSha256=hashlib.sha256(prepared.read_bytes()).hexdigest(),privateTMPDIR=str(T),sourceMapBoundaryOnly=True,repositoryBuildScriptOrProcMacroExecuted=False,metadataArtifactsEmitted=True,actualC2Context=False,actualFactCandidates=False,completeSymbolCensus=False,sourceAdmission=False,fullSM=False);(B/'results-all32.json').write_text(json.dumps(v,indent=2)+'\n');print('Compiler unit set complete',v['successfulUnits'],'successes',flush=True)
finally:
 if owned:lane.rmdir()
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
