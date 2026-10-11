from pathlib import Path
import os, json, hashlib, sys, tempfile, time, statistics, shutil

os.setpriority(os.PRIO_PROCESS, 0, 10)
B = Path('/tmp/opensip-implementation')
V = B / 'sm-framed-bin-profile-2026-10-10'
S = B / 'sm-framed-bin-profile-controls-r1-stage'
Q = B / 'reviews/grok-sm-framed-bin-profile-controls-r1'
C = Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06')
O = Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T')
destination = V / 'actual-smithy-fuzz-framed-samples-r1.json'
assert not destination.exists()

def check(row):
    raw = Path(row['path']).read_bytes()
    assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256']
    return raw

def pin(path):
    raw = path.read_bytes()
    return dict(path=str(path), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())

state = json.loads((C / 'CURRENT-STATE.json').read_bytes())
review = json.loads((Q / 'review.json').read_bytes())
subject = pin(S / 'subject.json')['sha256']
assert review['verdict'] == 'ACCEPT' and review['requiredFindings'] == [] and review['controlsPassed'] == 6
assert review['subjectManifestSha256'] == state['SMFramedBinProfileControlsPublication']['subjectManifest']['sha256'] == subject
source = json.loads((S / 'source.json').read_bytes())
for row in source['pythonSourcePins'] + [source['closedWrapperPin']]:
    check(row)
pilot_path = V / 'actual-smithy-fuzz-framed-pilots-r1.json'
pilot = json.loads(pilot_path.read_bytes())
assert pilot['compilerChildren'] == 39 and len(pilot['results']) == 2
assert all(r['outcomeRecorded'] for r in pilot['results'])
audit_pin = dict(path=str(B / 'audit_sm_analysis_prepared_reads_r1.py'), bytes=2415,
                 sha256='687ca8eadde2abd5c5146c43000cd4584ea592e58551545fcc32406f806e8fb7')
check(audit_pin)
sys.path.insert(0, str(B))
from audit_sm_analysis_prepared_reads_r1 import audit
sys.path.insert(0, str(V))
from framed_bin_profile_graph_execution import execute_graph
root = Path(tempfile.mkdtemp(prefix='opensip-sm-actual-smithy-fuzz-framed-samples-', dir=O))
root.chmod(0o700)
lane = O / 'opensip-lanes.lock'
owned = False
home = os.environ.get('HOME')
series = []
try:
    while True:
        try:
            lane.mkdir(); owned = True; break
        except FileExistsError:
            print('Waiting for ordinary Smithy fuzz sample lane', flush=True)
            time.sleep(5)
    build = json.loads((B / 'sm-framed-analysis-2026-10-10/build.json').read_bytes())
    for before in pilot['results']:
        entry = before['entry']
        graph = json.loads(check(entry['graph']))
        expected = [(u['index'], u['standing'], u.get('reason')) for u in before['result']['unitResults']]
        expected_metadata = {u['index']:u['metadata']['sha256'] for u in before['result']['unitResults'] if u.get('metadata')}
        runs = []
        for ordinal in range(10):
            for row in source['pythonSourcePins'] + [source['closedWrapperPin'], entry['sourceMap'], entry['unitCommandData'], entry['graph']]:
                check(row)
            started = time.monotonic_ns()
            result = execute_graph(graph, entry['sourceMap'], root / str(entry['ordinal']) / str(ordinal),
                                   source['closedWrapperPin'], build['sysroot'], Path(entry['cwd']), entry['unitCommandData'])
            elapsed = time.monotonic_ns()-started
            reads = audit(entry['sourceMap'], result['unitResults'])
            repeated = [(u['index'], u['standing'], u.get('reason')) for u in result['unitResults']] == expected
            metadata = {u['index']:u['metadata']['sha256'] for u in result['unitResults'] if u.get('metadata')}
            read_repeat = reads == before['preparedReadSetAudit']
            metadata_repeat = metadata == expected_metadata
            run = dict(ordinal=ordinal, warmup=ordinal < 3, result=result, wholeGraphNanos=elapsed,
                       preparedReadSetAudit=reads, pilotPopulationRepeated=repeated,
                       pilotMappedReadSetsRepeated=read_repeat, pilotMetadataHashesRepeated=metadata_repeat)
            runs.append(run)
            (V / 'actual-smithy-fuzz-framed-samples-r1-progress.json').write_text(json.dumps(dict(series=series, currentEntry=entry['ordinal'], currentRuns=runs), indent=2)+'\n')
            assert repeated and read_repeat and metadata_repeat and result['compilerChildren'] == before['compilerChildren']
            spans = []
            for child in result['unitResults']:
                if not child['compilerLaunched']:
                    continue
                wire = [e for e in child['events'] if e['event'] == 'prepared_map_wire_verified']
                assert len(wire) == 1 and wire[0]['mapSha256'] == entry['sourceMap']['sha256'] and wire[0]['mapBytes'] == entry['sourceMap']['bytes']
                analyses = [e['analysisElapsedNanos'] for e in child['events'] if e['event'] == 'after_analysis']
                assert len(analyses) == 1 and 0 < analyses[0] <= child['observationInformational']['root_reaped_elapsed_nanos']
                spans.extend(analyses)
            run['sumInstrumentedAnalysisNanos'] = sum(spans)
            print(dict(entry=entry['ordinal'], sample=ordinal, children=result['compilerChildren'], populationReadSetsMetadataRepeat=True), flush=True)
        measured = [r for r in runs if not r['warmup']]
        series.append(dict(entry=entry, runs=runs, warmups=3, measuredSamples=7,
                           compilerChildren=sum(r['result']['compilerChildren'] for r in runs),
                           medianSumInstrumentedAnalysisNanos=statistics.median(r['sumInstrumentedAnalysisNanos'] for r in measured),
                           maxSumInstrumentedAnalysisNanos=max(r['sumInstrumentedAnalysisNanos'] for r in measured),
                           unavailableRootPopulationPreserved=True, completeOriginalWorkloadCoverage=False))
        report = dict(pilotReceipt=pin(pilot_path), ownAcceptedExecutorSubject=subject, root=str(root), series=series,
                      completedSeries=len(series), totalGraphs=sum(len(s['runs']) for s in series),
                      totalCompilerChildren=sum(s['compilerChildren'] for s in series),
                      eligibleUnitPopulationRepeated=True, mappedReadSetsRepeated=True, metadataHashesRepeated=True,
                      completeOriginalWorkloadCoverage=False, applicationExecuted=False, buildScriptOrProcMacroExecuted=False,
                      sourceRuntimeMetadataSysrootReadsSealed=False, completeRuntimeCommand=False,
                      fullCargoProfileEnvironment=False, sourceAuthentication=False, nativeAdmission=False,
                      physicalPeakScratchMeasured=False, completeStatisticalSet=False, SMComplete=False,
                      effectiveL=False, productQualification=False, ownedLane=True, niceness=os.getpriority(os.PRIO_PROCESS,0),
                      HOMEUnchanged=os.environ.get('HOME') == home)
        destination.write_text(json.dumps(report, indent=2)+'\n')
    assert report['completedSeries'] == 2 and report['totalGraphs'] == 20 and report['totalCompilerChildren'] == 390
    preserved = C / 'continuation-preserved/sm-actual-smithy-fuzz-framed-samples-r1'
    shutil.copytree(root, preserved / 'raw')
    shutil.copyfile(destination, preserved / destination.name)
    shutil.copyfile(Path(__file__), preserved / Path(__file__).name)
finally:
    if owned:
        lane.rmdir()
    assert os.environ.get('HOME') == home and not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
