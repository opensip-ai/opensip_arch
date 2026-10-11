from pathlib import Path
import json, hashlib, os, sys, tempfile, time, statistics

os.setpriority(os.PRIO_PROCESS, 0, 10)
B = Path('/tmp/opensip-implementation')
V = B / 'sm-framed-bin-profile-2026-10-10'
S = B / 'sm-framed-bin-profile-controls-r1-stage'
Q = B / 'reviews/grok-sm-framed-bin-profile-controls-r1'
C = Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06')
O = Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T')
destination = V / 'actual-deno-framed-bin-samples-r1.json'
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
pilot_path = V / 'actual-deno-framed-bin-pilot-r1.json'
pilot = json.loads(pilot_path.read_bytes())
assert pilot['successfulBinaryAnalysis'] and pilot['compilerChildren'] == 1
assert pilot['ownAcceptedExecutorSubject'] == subject
entry = pilot['entry']
graph = json.loads(check(entry['graph']))
check(entry['sourceMap']); check(entry['unitCommandData']); check(entry['packet'])
audit_pin = dict(path=str(B / 'audit_sm_analysis_prepared_reads_r1.py'), bytes=2415,
                 sha256='687ca8eadde2abd5c5146c43000cd4584ea592e58551545fcc32406f806e8fb7')
check(audit_pin)
sys.path.insert(0, str(B))
from audit_sm_analysis_prepared_reads_r1 import audit
sys.path.insert(0, str(V))
from framed_bin_profile_graph_execution import execute_graph
baseline_reads = audit(entry['sourceMap'], pilot['result']['unitResults'])
expected = [(u['index'], u['standing']) for u in pilot['result']['unitResults']]
root = Path(tempfile.mkdtemp(prefix='opensip-sm-actual-deno-framed-bin-samples-', dir=O))
root.chmod(0o700)
lane = O / 'opensip-lanes.lock'
owned = False
home = os.environ.get('HOME')
runs = []
try:
    while True:
        try:
            lane.mkdir(); owned = True; break
        except FileExistsError:
            print('Waiting for ordinary original Deno sample lane', flush=True)
            time.sleep(5)
    build = json.loads((B / 'sm-framed-analysis-2026-10-10/build.json').read_bytes())
    for ordinal in range(10):
        for row in source['pythonSourcePins'] + [source['closedWrapperPin'], entry['sourceMap'], entry['unitCommandData']]:
            check(row)
        started = time.monotonic_ns()
        result = execute_graph(graph, entry['sourceMap'], root / str(ordinal),
                               source['closedWrapperPin'], build['sysroot'],
                               Path(entry['cwd']), entry['unitCommandData'])
        elapsed = time.monotonic_ns() - started
        reads = audit(entry['sourceMap'], result['unitResults'])
        child = result['unitResults'][0]
        repeated = [(u['index'], u['standing']) for u in result['unitResults']] == expected
        wire = [e for e in child['events'] if e['event'] == 'prepared_map_wire_verified']
        spans = [e['analysisElapsedNanos'] for e in child['events'] if e['event'] == 'after_analysis']
        record = dict(ordinal=ordinal, warmup=ordinal < 3, wholeGraphNanos=elapsed,
                      result=result, preparedReadSetAudit=reads,
                      pilotPopulationRepeated=repeated, pilotReadSetsRepeated=reads == baseline_reads)
        runs.append(record)
        (V / 'actual-deno-framed-bin-samples-r1-progress.json').write_text(json.dumps(runs, indent=2) + '\n')
        assert result['compilerChildren'] == 1 and repeated and reads == baseline_reads
        assert child['analysisCompleted'] and child['metadata'] is None and child['reusableLibraryMetadata'] is False
        assert len(wire) == 1 and wire[0]['mapSha256'] == entry['sourceMap']['sha256'] and wire[0]['mapBytes'] == entry['sourceMap']['bytes']
        assert len(spans) == 1 and type(spans[0]) is int and spans[0] > 0
        observation = child['observationInformational']
        assert 0 < observation['worker_ready_elapsed_nanos'] < observation['map_wire_verified_elapsed_nanos'] <= observation['map_decode_complete_elapsed_nanos'] <= observation['root_reaped_elapsed_nanos']
        assert spans[0] <= observation['root_reaped_elapsed_nanos']
        record['instrumentedAnalysisNanos'] = spans[0]
        print(dict(sample=ordinal, standing=child['standing'], readSetsRepeated=True), flush=True)
    measured = [r for r in runs if not r['warmup']]
    report = dict(standing='NEW ACTUAL ORIGINAL DENO SUBWORKSPACE BINARY SERIES; FULL DENO COVERAGE NOT INFERRED',
                  pilotReceipt=pin(pilot_path), entry=entry, root=str(root), runs=runs,
                  warmups=3, measuredSamples=7, newCompilerChildren=10,
                  medianWholeGraphNanos=statistics.median(r['wholeGraphNanos'] for r in measured),
                  maxWholeGraphNanos=max(r['wholeGraphNanos'] for r in measured),
                  medianInstrumentedAnalysisNanos=statistics.median(r['instrumentedAnalysisNanos'] for r in measured),
                  maxInstrumentedAnalysisNanos=max(r['instrumentedAnalysisNanos'] for r in measured),
                  readAuditSource=audit_pin, ownAcceptedExecutorSubject=subject,
                  sourceMapReceivedSameChild=True, pilotPopulationRepeated=True, pilotReadSetsRepeated=True,
                  observedOriginalWorkspaceEntries=1, declaredOriginalWorkspaceEntries=3,
                  completeOriginalWorkloadCoverage=False, sourceRuntimeMetadataSysrootReadsSealed=False,
                  applicationExecuted=False, buildScriptOrProcMacroExecuted=False,
                  metadataReusable=False, completeStatisticalSet=False,
                  physicalPeakScratchMeasured=False, sourceAuthentication=False, nativeAdmission=False,
                  SMComplete=False, effectiveL=False, productQualification=False,
                  ownedLane=True, niceness=os.getpriority(os.PRIO_PROCESS, 0), HOMEUnchanged=os.environ.get('HOME') == home)
    destination.write_text(json.dumps(report, indent=2) + '\n')
finally:
    if owned:
        lane.rmdir()
    assert os.environ.get('HOME') == home
    assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
