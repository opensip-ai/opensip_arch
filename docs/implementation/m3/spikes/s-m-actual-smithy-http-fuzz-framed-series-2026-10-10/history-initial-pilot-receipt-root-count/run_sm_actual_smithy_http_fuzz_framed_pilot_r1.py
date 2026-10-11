from pathlib import Path
import json, hashlib, os, sys, tempfile, time, collections, shutil

os.setpriority(os.PRIO_PROCESS, 0, 10)
B = Path('/tmp/opensip-implementation')
V = B / 'sm-framed-bin-profile-2026-10-10'
S = B / 'sm-framed-bin-profile-controls-r1-stage'
Q = B / 'reviews/grok-sm-framed-bin-profile-controls-r1'
C = Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06')
O = Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T')
destination = V / 'actual-smithy-http-fuzz-framed-pilot-r1.json'
assert not destination.exists()

def check(row):
    raw = Path(row['path']).read_bytes()
    assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256']
    return raw

def pin(path):
    raw = path.read_bytes()
    return dict(path=str(path), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())

state = json.loads((C / 'CURRENT-STATE.json').read_bytes())
publication = state['SMFramedBinProfileControlsPublication']
review = json.loads((Q / 'review.json').read_bytes())
subject = pin(S / 'subject.json')['sha256']
assert review['verdict'] == 'ACCEPT' and review['requiredFindings'] == []
assert review['subjectManifestSha256'] == publication['subjectManifest']['sha256'] == subject
assert review['controlsPassed'] == 6
source = json.loads((S / 'source.json').read_bytes())
for row in source['pythonSourcePins'] + [source['closedWrapperPin']]:
    check(row)
map_path = V / 'actual-smithy-http-fuzz-original-source-map-r1.json'
prepared = json.loads(map_path.read_bytes())
assert len(prepared['results']) == 1 and [r['ordinal'] for r in prepared['results']] == [12]
check(prepared['dependencyDataReceipt'])
audit_pin = dict(path=str(B / 'audit_sm_analysis_prepared_reads_r1.py'), bytes=2415,
                 sha256='687ca8eadde2abd5c5146c43000cd4584ea592e58551545fcc32406f806e8fb7')
check(audit_pin)
sys.path.insert(0, str(B))
from audit_sm_analysis_prepared_reads_r1 import audit
sys.path.insert(0, str(V))
from framed_bin_profile_graph_execution import execute_graph
root = Path(tempfile.mkdtemp(prefix='opensip-sm-actual-smithy-http-fuzz-framed-pilot-', dir=O))
root.chmod(0o700)
lane = O / 'opensip-lanes.lock'
owned = False
home = os.environ.get('HOME')
results = []
try:
    while True:
        try:
            lane.mkdir(); owned = True; break
        except FileExistsError:
            print('Waiting for ordinary actual Smithy fuzz analysis lane', flush=True)
            time.sleep(5)
    build = json.loads((B / 'sm-framed-analysis-2026-10-10/build.json').read_bytes())
    for entry in prepared['results']:
        for row in source['pythonSourcePins'] + [source['closedWrapperPin'], entry['sourceMap'], entry['unitCommandData'], entry['graph'], entry['packet']]:
            check(row)
        graph = json.loads(check(entry['graph']))
        output = root / str(entry['ordinal'])
        started = time.monotonic_ns()
        try:
            result = execute_graph(graph, entry['sourceMap'], output,
                                   source['closedWrapperPin'], build['sysroot'],
                                   Path(entry['cwd']), entry['unitCommandData'])
            read_audit = audit(entry['sourceMap'], result['unitResults'])
            record = dict(entry=entry, result=result, preparedReadSetAudit=read_audit,
                          wholeGraphNanos=time.monotonic_ns()-started,
                          unitStandings=dict(collections.Counter(u['standing'] for u in result['unitResults'])),
                          rootStandings=dict(collections.Counter(u['standing'] for u in result['rootResults'])),
                          compilerChildren=result['compilerChildren'], outcomeRecorded=True)
            print(dict(entry=entry['ordinal'], compilerChildren=result['compilerChildren'], roots=record['rootStandings']), flush=True)
        except Exception as error:
            record = dict(entry=entry, wholeGraphNanos=time.monotonic_ns()-started,
                          exceptionType=type(error).__name__, diagnostic=str(error),
                          outputRoot=str(output), outputRootExists=output.exists(),
                          compilerChildren=None if output.exists() else 0,
                          compilerChildPopulationUnresolved=output.exists(), outcomeRecorded=False)
            print(dict(entry=entry['ordinal'], exception=type(error).__name__, diagnostic=str(error)), flush=True)
        results.append(record)
        (V / 'actual-smithy-http-fuzz-framed-pilot-r1-progress.json').write_text(json.dumps(results, indent=2)+'\n')
    report = dict(standing='NEW ACTUAL ORIGINAL SMITHY HTTP FUZZ GRAPH ANALYSIS PILOT; INCOMPLETE ROOTS RETAINED; NOT FULL SMITHY COVERAGE',
                  preparedMapReceipt=pin(map_path), ownAcceptedExecutorSubject=subject,
                  root=str(root), results=results, attemptedGraphs=1, originalGraphUnits=59,
                  originalGraphRoots=5, actualObservedWorkspaceEntries=1, originalDeclaredWorkspaceEntries=25,
                  compilerChildren=sum(r['compilerChildren'] for r in results) if all(r['compilerChildren'] is not None for r in results) else None,
                  completeOriginalWorkloadCoverage=False, applicationExecuted=False,
                  buildScriptOrProcMacroExecuted=False, sourceRuntimeMetadataSysrootReadsSealed=False,
                  completeRuntimeCommand=False, fullCargoProfileEnvironment=False,
                  physicalPeakScratchMeasured=False, sourceAuthentication=False, nativeAdmission=False,
                  completeStatisticalSet=False, SMComplete=False, effectiveL=False, productQualification=False,
                  ownedLane=True, niceness=os.getpriority(os.PRIO_PROCESS, 0), HOMEUnchanged=os.environ.get('HOME') == home)
    destination.write_text(json.dumps(report, indent=2)+'\n')
    preserved = C / 'continuation-preserved/sm-actual-smithy-http-fuzz-framed-pilot-r1'
    shutil.copytree(root, preserved / 'raw')
    shutil.copyfile(destination, preserved / destination.name)
    shutil.copyfile(Path(__file__), preserved / Path(__file__).name)
finally:
    if owned:
        lane.rmdir()
    assert os.environ.get('HOME') == home
    assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
