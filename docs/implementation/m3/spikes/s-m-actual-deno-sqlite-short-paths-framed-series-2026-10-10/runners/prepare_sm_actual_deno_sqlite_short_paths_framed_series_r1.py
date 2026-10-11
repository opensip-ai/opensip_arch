from pathlib import Path
import os, json, hashlib, shutil, statistics

# Derived from prepare_sm_actual_smithy_http_fuzz_framed_series_r1.py.
# Adds the shorter-layout packet/collector/map receipts and retains the earlier long-path zero-analysis
# pilot/sampler failures as labelled history (the long-path 125 MB map body is pinned, not recopied).
os.setpriority(os.PRIO_PROCESS, 0, 10)
B = Path('/tmp/opensip-implementation')
V = B / 'sm-framed-bin-profile-2026-10-10'
L = B / 'sm-large-original-context-census-2026-10-10'
D = B / 'sm-actual-deno-sqlite-short-paths-framed-series-r1-draft'
C = Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06')
assert not D.exists()
D.mkdir()

def pin(path):
    raw = path.read_bytes()
    return dict(path=str(path), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())

def copy(path, relative):
    reference = pin(path)
    destination = D / relative
    assert not destination.exists()
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(path, destination)
    assert all(pin(destination)[k] == reference[k] for k in ['bytes', 'sha256'])
    return reference

pilot_path = V / 'actual-deno-sqlite-short-paths-framed-pilot-r1.json'
sample_path = V / 'actual-deno-sqlite-short-paths-framed-samples-r1.json'
map_receipt_path = V / 'actual-deno-sqlite-short-paths-source-map-r1.json'
collector_path = L / 'actual-deno-sqlite-short-paths-collector-r1.json'
packet_receipt_path = L / 'deno-sqlite-short-paths-packet-r1.json'
pilot = json.loads(pilot_path.read_bytes())
samples = json.loads(sample_path.read_bytes())
audit = json.loads((V / 'actual-deno-sqlite-short-paths-framed-wire-audit-r1.json').read_bytes())
prepared = json.loads(map_receipt_path.read_bytes())['results'][0]
collector = json.loads(collector_path.read_bytes())
assert pilot['compilerChildren'] == 7 and samples['totalCompilerChildren'] == 70
assert samples['totalGraphs'] == 10 and len(samples['series']) == 1
assert audit['compilerChildrenAudited'] == 77 and audit['allFrameAndWireCountsMatch']
assert audit['pilotReceipt'] == samples['pilotReceipt'] == pin(pilot_path)
assert audit['sampleReceipt'] == pin(sample_path)
assert prepared['preparedDescriptorBytes'] == pilot['preparedDescriptorBytes'] <= prepared['preparedDescriptorBoundBytes'] == 4 << 20
assert prepared['descriptorCheckedBeforeLaunch'] and prepared['everyLongLayoutRowRetained'] and not prepared['sourcesTrimmed'] and not prepared['descriptorBoundChanged']
assert collector['successfulGraphs'] == 1 and collector['actualCollectorRoots'] == 1
lock = collector['results'][0]['lockObservation']
assert lock['originalLockPreserved'] and not lock['generatedExperimentalLock'] and lock['equalsPinnedOriginalLock']
for path in [pilot_path, sample_path, V / 'actual-deno-sqlite-short-paths-framed-wire-audit-r1.json', map_receipt_path]:
    copy(path, 'receipts/' + path.name)
for path in [collector_path, packet_receipt_path]:
    copy(path, 'receipts/' + path.name)
for label, root in [('pilots', Path(pilot['root'])), ('samples', Path(samples['root']))]:
    for path in sorted(root.rglob('*')):
        if path.is_file():
            copy(path, 'raw/' + label + '/' + path.relative_to(root).as_posix())
for before, series in zip(pilot['results'], samples['series']):
    entry = before['entry']
    assert series['entry'] == entry
    assert [r['warmup'] for r in series['runs']] == [True]*3+[False]*7
    assert all(r['pilotPopulationRepeated'] and r['pilotMappedReadSetsRepeated'] and r['pilotMetadataHashesRepeated'] for r in series['runs'])
    measured = [r for r in series['runs'] if not r['warmup']]
    assert series['medianSumInstrumentedAnalysisNanos'] == statistics.median(r['sumInstrumentedAnalysisNanos'] for r in measured)
    assert series['maxSumInstrumentedAnalysisNanos'] == max(r['sumInstrumentedAnalysisNanos'] for r in measured)
    assert all(u['standing'] == 'unavailable' for u in before['result']['rootResults'])
    for key in ['sourceMap', 'graph', 'unitCommandData', 'packet']:
        reference = entry[key]
        assert pin(Path(reference['path'])) == {k:reference[k] for k in ['path', 'bytes', 'sha256']}
        copy(Path(reference['path']), 'original-inputs/' + str(entry['ordinal']) + '/' + key + Path(reference['path']).suffix)
    packet = json.loads(Path(entry['packet']['path']).read_bytes())
    static_root = Path(packet['observationRoot'])
    for path in sorted(static_root.iterdir()):
        if path.is_file() and path.name != 'packet.json':
            copy(path, 'original-static-collectors/' + str(entry['ordinal']) + '/' + path.name)
    if (static_root / 'queries').exists():
        for path in sorted((static_root / 'queries').rglob('*')):
            if path.is_file():
                copy(path, 'original-static-collectors/' + str(entry['ordinal']) + '/queries/' + path.relative_to(static_root / 'queries').as_posix())
    configuration = packet['configuration']
    assert pin(Path(configuration['path'])) == {k:configuration[k] for k in ['path', 'bytes', 'sha256']}
    copy(Path(configuration['path']), 'original-inputs/' + str(entry['ordinal']) + '/original-config.toml')
    original_lock = packet['originalLock']
    assert pin(Path(original_lock['path'])) == {k:original_lock[k] for k in ['path', 'bytes', 'sha256']}
    copy(Path(original_lock['path']), 'original-inputs/' + str(entry['ordinal']) + '/original-Cargo.lock')
closed = B / 'sm-framed-bin-profile-controls-r1-stage'
source = json.loads((closed / 'source.json').read_bytes())
for name in ['source.json', 'subject.json', 'integration.json']:
    copy(closed / name, 'closed-controls/' + name)
for name in ['review.json', 'REVIEW.md']:
    copy(B / 'reviews/grok-sm-framed-bin-profile-controls-r1' / name, 'closed-controls/' + name)
for ordinal, row in enumerate(source['pythonSourcePins'] + [source['closedWrapperPin']]):
    assert all(pin(Path(row['path']))[k] == row[k] for k in ['bytes', 'sha256'])
    copy(Path(row['path']), 'closed-execution-inputs/' + str(ordinal) + '-' + Path(row['path']).name)
copy(B / 'sm-framed-analysis-2026-10-10/driver.rs', 'closed-execution-inputs/driver.rs')
for name in ['prepare_sm_deno_sqlite_short_paths_packet_r1.py', 'run_sm_actual_deno_sqlite_short_paths_collector_r1.py',
             'prepare_sm_actual_deno_sqlite_short_paths_source_map_r1.py', 'run_sm_actual_deno_sqlite_short_paths_framed_pilot_r1.py',
             'run_sm_actual_deno_sqlite_short_paths_framed_samples_r1.py', 'audit_sm_actual_deno_sqlite_short_paths_framed_series_r1.py',
             'audit_sm_analysis_prepared_reads_r1.py', 'run_sm_actual_other_large_workspace_attempts_r10.py',
             'prepare_sm_actual_deno_sqlite_original_source_map_r1.py']:
    copy(B / name, 'runners/' + name)
copy(V / 'deno-sqlite-short-paths-samples-r1-driver.log', 'runners/deno-sqlite-short-paths-samples-r1-driver.log')
# Retained long-path failures: zero completed analyses; never upgraded.
history = 'history-long-path-zero-analysis-failures/'
old_pilot_path = V / 'actual-deno-sqlite-framed-pilot-r1.json'
old_pilot = json.loads(old_pilot_path.read_bytes())
assert old_pilot['compilerChildren'] == 5 and old_pilot['results'][0]['unitStandings'].get('analysis-and-metadata-completed', 0) == 0
copy(old_pilot_path, history + 'pilot/' + old_pilot_path.name)
copy(V / 'actual-deno-sqlite-original-source-map-r1.json', history + 'pilot/actual-deno-sqlite-original-source-map-r1.json')
for name in ['run_sm_actual_deno_sqlite_framed_pilot_r1.py', 'audit_sm_actual_deno_sqlite_framed_series_r1.py']:
    copy(B / name, history + 'runners/' + name)
preserved_pilot = C / 'continuation-preserved/sm-actual-deno-sqlite-framed-pilot-r1/raw'
for path in sorted(preserved_pilot.rglob('*')):
    if path.is_file():
        copy(path, history + 'pilot/raw/' + path.relative_to(preserved_pilot).as_posix())
failed = C / 'continuation-preserved/sm-actual-deno-sqlite-framed-failed-sample-r1'
for path in sorted(failed.rglob('*')):
    if path.is_file() and path.name != 'source-map.bin':
        copy(path, history + 'sampler/' + path.relative_to(failed).as_posix())
long_map = json.loads((V / 'actual-deno-sqlite-original-source-map-r1.json').read_bytes())['results'][0]['sourceMap']
report = dict(unit='SM-ACTUAL-DENO-SQLITE-SHORT-PATHS-FRAMED-SERIES-r1',
              standing='UNREVIEWED ORIGINAL DENO SQLITE SHORT-PATH GRAPH PILOT AND ELIGIBLE UNIT SERIES; LONG-PATH ZERO-ANALYSIS FAILURES RETAINED',
              actualPilotCompilerChildren=7, actualSampleCompilerChildren=70, totalActualCompilerChildren=77,
              actualPilotGraphs=1, actualSampleGraphs=10, totalActualGraphs=11,
              warmupsPerSeries=3, measuredSamplesPerSeries=7, measuredSeries=1,
              originalGraphUnits=25, eligibleUnitsPerGraph=7, unavailableUnitsPerGraph=18,
              originalGraphRoots=1, unavailableRootsPerGraph=1,
              shortLayoutCollectorRoots=1, shortLayoutCollectorInformationQueries=collector['compilerInformationQueries'],
              preparedMapFiles=prepared['preparedFiles'], preparedMapBytes=prepared['sourceMap']['bytes'],
              preparedDescriptorBytes=prepared['preparedDescriptorBytes'], preparedDescriptorBoundBytes=4 << 20,
              historicalLongPathDescriptorBytes=4292558,
              historicalLongPathCompilerChildrenLaunched=10, historicalLongPathCompletedAnalyses=0,
              historicalLongPathSourceMapBytes=long_map['bytes'],
              compilerChildrenIndependentlyWireAudited=77, allFrameAndWireCountsMatch=True,
              allEligibleAnalysesCompleted=True, mappedReadSetsRepeat=True, metadataHashesRepeat=True,
              originalUnavailableUnitAndRootPopulationsPreserved=True,
              shortLayoutGraphAndCommandDataEqualLongLayoutModuloPrivatePaths=True,
              everyLongLayoutMapRowRetained=True, descriptorCheckedBeforeLaunch=True,
              originalPinnedLockPreserved=True, generatedExperimentalLock=False,
              originalStaticConfigurationArgumentsApplied=True, sameChildFramedMapAndAnalysis=True,
              mapDecodingExcludedFromInstrumentedAnalysis=True, observerInstrumentationIncluded=True,
              historicalFailuresRetained=True, historicalFailuresUpgraded=False,
              ownClosedSupportSubject=pilot['ownAcceptedExecutorSubject'],
              seriesStatistics=[dict(ordinal=s['entry']['ordinal'], medianSumInstrumentedAnalysisNanos=s['medianSumInstrumentedAnalysisNanos'], maxSumInstrumentedAnalysisNanos=s['maxSumInstrumentedAnalysisNanos']) for s in samples['series']],
              sourcesTrimmed=False, descriptorBoundChanged=False,
              newCargoSource=False, newCompilerSource=False, newGraphExecutor=False, controlsRerun=False,
              canonicalNativeSnapshotDescriptorMeasured=False,
              completeOriginalWorkloadCoverage=False, applicationExecuted=False,
              buildScriptOrProcMacroExecuted=False, sourceRuntimeMetadataSysrootReadsSealed=False,
              snapshot2Plan2Equivalent=False, completeRuntimeCommand=False, fullCargoProfileEnvironment=False,
              physicalPeakScratchMeasured=False, sourceAuthentication=False, nativeAdmission=False,
              completeStatisticalSet=False, productChange=False, SMComplete=False,
              effectiveL=False, productQualification=False, entirePlanComplete=False)
(D / 'draft-source.json').write_text(json.dumps(report, indent=2)+'\n')
median = report['seriesStatistics'][0]['medianSumInstrumentedAnalysisNanos']
(D / 'REPORT.md').write_text(f"""Original Deno SQLite short-path pilot and eligible analysis series

The original Deno workspace entry `tests/sqlite_extension/Cargo.toml` (ordinal 27) has one static graph: 25 units and one cdylib root, index 22. In the earlier long private layout its absolute-path prepared descriptor was 4292558 bytes, over the closed driver's unchanged 4194304-byte bound. That pilot launched five compiler children and the later sampler five more. None completed analysis. Those ten zero-analysis children, their receipts, runners and the unused 55-analysis audit are retained under `history-long-path-zero-analysis-failures/` and are not upgraded.

A shorter private layout copies all 14920 original pinned files unchanged, with the original pinned `Cargo.lock` preserved (no generated lock) and the original configuration unchanged. Only the absolute private paths differ. A fresh one-packet collector run, using the closed collector image and an owned ordinary lane, produced a graph and static command data equal to the long-layout ones modulo those private paths, with 7 information queries. A fresh source map retains every one of the 16298 long-layout rows (14920 original plus 1378 expanded registry files). Its descriptor, 3680124 bytes, was computed with the closed driver's formula and checked against the bound before any launch. No source was trimmed and the bound was not changed.

One pilot and ten fresh sample graphs (3 warmups, 7 measured) complete 77 compiler analyses: 7 eligible library units per graph. 18 units and the root stay unavailable, with their original reasons. Populations, mapped read sets and metadata hashes repeat. An independent whole-map/frame/wire/phase/read-call audit covers all 77 children. The measured median of summed instrumented analysis is {median} ns.

The closed framed driver, executor, observer and controls are unchanged and not replayed. The short private layout is not a canonical native snapshot, so this neither shows nor refutes a native descriptor bound outcome. Only one Deno workspace entry is represented. Spans exclude map decoding and include observer instrumentation. No full F/T/SM8, physical peak, profile, read seal, snapshot2/plan2, source authentication, native admission, effective L, full S-M or qualification inference. Product, law and lock are unchanged. Exact review, own assent and fresh verification are required before an architecture-only support publication. No push.
""")
copy(Path(__file__), 'runners/' + Path(__file__).name)
shutil.copytree(D, C / 'continuation-preserved' / D.name)
print('Prepared/preserved 11 actual Deno SQLite short-path graphs, 77 eligible analyses, unavailable root and retained long-path failures.')
