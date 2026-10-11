from pathlib import Path
import os, json, hashlib, shutil, statistics

os.setpriority(os.PRIO_PROCESS, 0, 10)
B = Path('/tmp/opensip-implementation')
V = B / 'sm-framed-bin-profile-2026-10-10'
D = B / 'sm-actual-smithy-fuzz-framed-series-r1-draft'
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

pilot_path = V / 'actual-smithy-fuzz-framed-pilots-r1.json'
sample_path = V / 'actual-smithy-fuzz-framed-samples-r2.json'
pilot = json.loads(pilot_path.read_bytes())
samples = json.loads(sample_path.read_bytes())
audit = json.loads((V / 'actual-smithy-fuzz-framed-wire-audit-r1.json').read_bytes())
assert pilot['compilerChildren'] == 39 and samples['totalCompilerChildren'] == 390
assert samples['totalGraphs'] == 20 and len(samples['series']) == 2
assert audit['compilerChildrenAudited'] == 429 and audit['allFrameAndWireCountsMatch']
assert audit['pilotReceipt'] == samples['pilotReceipt'] == pin(pilot_path)
assert audit['sampleReceipt'] == pin(sample_path)
for name in ['actual-smithy-fuzz-framed-pilots-r1.json', 'actual-smithy-fuzz-framed-samples-r2.json', 'actual-smithy-fuzz-framed-wire-audit-r1.json', 'actual-smithy-fuzz-original-source-maps-r1.json']:
    copy(V / name, 'receipts/' + name)
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
        if path.is_file():
            copy(path, 'original-static-collectors/' + str(entry['ordinal']) + '/' + path.name)
    if (static_root / 'queries').exists():
        for path in sorted((static_root / 'queries').rglob('*')):
            if path.is_file():
                copy(path, 'original-static-collectors/' + str(entry['ordinal']) + '/queries/' + path.relative_to(static_root / 'queries').as_posix())
    configuration = packet['configuration']
    assert pin(Path(configuration['path'])) == {k:configuration[k] for k in ['path', 'bytes', 'sha256']}
    copy(Path(configuration['path']), 'original-inputs/' + str(entry['ordinal']) + '/original-config.toml')
closed = B / 'sm-framed-bin-profile-controls-r1-stage'
source = json.loads((closed / 'source.json').read_bytes())
for name in ['source.json', 'subject.json', 'integration.json']:
    copy(closed / name, 'closed-controls/' + name)
for name in ['review.json', 'REVIEW.md']:
    copy(B / 'reviews/grok-sm-framed-bin-profile-controls-r1' / name, 'closed-controls/' + name)
for ordinal, row in enumerate(source['pythonSourcePins'] + [source['closedWrapperPin']]):
    assert all(pin(Path(row['path']))[k] == row[k] for k in ['bytes', 'sha256'])
    copy(Path(row['path']), 'closed-execution-inputs/' + str(ordinal) + '-' + Path(row['path']).name)
for name in ['run_sm_actual_smithy_fuzz_framed_pilots_r1.py', 'run_sm_actual_smithy_fuzz_framed_samples_r1.py', 'run_sm_actual_smithy_fuzz_framed_samples_r2.py', 'audit_sm_actual_smithy_fuzz_framed_series_r1.py', 'audit_sm_analysis_prepared_reads_r1.py', 'prepare_sm_actual_smithy_fuzz_original_source_maps_r1.py']:
    copy(B / name, 'runners/' + name)
history = V / 'history-smithy-sample-parent-directory-r1'
assert json.loads((history / 'failure.json').read_bytes())['compilerChildren'] == 0
for path in sorted(history.rglob('*')):
    if path.is_file():
        copy(path, 'history-prelaunch-sampler-failure/' + path.relative_to(history).as_posix())
report = dict(unit='SM-ACTUAL-SMITHY-FUZZ-FRAMED-SERIES-r1', standing='UNREVIEWED TWO ACTUAL ORIGINAL SMITHY FUZZ GRAPH PILOTS AND ELIGIBLE UNIT SERIES',
              actualPilotCompilerChildren=39, actualSampleCompilerChildren=390, totalActualCompilerChildren=429,
              actualPilotGraphs=2, actualSampleGraphs=20, totalActualGraphs=22,
              warmupsPerSeries=3, measuredSamplesPerSeries=7, measuredSeries=2,
              originalGraphUnits=95, eligibleUnitsPerTwoGraphs=39, unavailableUnitsPerTwoGraphs=56,
              originalGraphRoots=10, unavailableRootsPerTwoGraphs=10,
              originalSmithyDeclaredWorkspaceEntries=25, observedOriginalWorkspaceEntries=2,
              compilerChildrenIndependentlyWireAudited=429, allFrameAndWireCountsMatch=True,
              allEligibleAnalysesCompleted=True, mappedReadSetsRepeat=True, metadataHashesRepeat=True,
              originalUnavailableUnitAndRootPopulationsPreserved=True,
              originalStaticConfigurationArgumentsApplied=True, sameChildFramedMapAndAnalysis=True,
              mapDecodingExcludedFromInstrumentedAnalysis=True, observerInstrumentationIncluded=True,
              ownClosedSupportSubject=pilot['ownAcceptedExecutorSubject'],
              seriesStatistics=[dict(ordinal=s['entry']['ordinal'], medianSumInstrumentedAnalysisNanos=s['medianSumInstrumentedAnalysisNanos'], maxSumInstrumentedAnalysisNanos=s['maxSumInstrumentedAnalysisNanos']) for s in samples['series']],
              historicalPrelaunchSamplerFailures=1, historicalCompilerChildren=0,
              newCargoSource=False, newCompilerSource=False, newGraphExecutor=False, controlsRerun=False,
              completeOriginalWorkloadCoverage=False, applicationExecuted=False,
              buildScriptOrProcMacroExecuted=False, sourceRuntimeMetadataSysrootReadsSealed=False,
              snapshot2Plan2Equivalent=False, completeRuntimeCommand=False, fullCargoProfileEnvironment=False,
              physicalPeakScratchMeasured=False, sourceAuthentication=False, nativeAdmission=False,
              completeStatisticalSet=False, productChange=False, SMComplete=False,
              effectiveL=False, productQualification=False, entirePlanComplete=False)
(D / 'draft-source.json').write_text(json.dumps(report, indent=2)+'\n')
(D / 'REPORT.md').write_text('Actual original Smithy fuzz graphs and eligible analysis series\n\nTwo original event-stream/types fuzz workspace static graphs contain 95 units and ten binary roots. Of these, 39 units are eligible and complete metadata analysis; 56 units and all ten roots remain unavailable due to actual expansion/target context and their dependencies. Two pilots and twenty fresh sample graphs (three warmups/seven measured samples per entry) complete 22 graphs and 429 compiler analyses. Metadata hashes, mapped read sets, eligible/unavailable unit populations and all unavailable root populations repeat. An independent audit checks all429 same-child whole-map/frame/wire counts, phase ordering and read-call counts. Original whole maps, static graph/command/INFOenv/config/packet/lock data, raw child events/stdout/stderr/metadata and private root observations are retained.\n\nInstrumented analysis spans exclude map decoding/metadata and include observer work; host graph time includes preparation/dispatch. These are not complete F/T/SM8 internal-call measurements. No application, linking, build script or proc macro executes. Only two of25 declared original Smithy workspace entries are represented; the whole source maps are read-set inputs, not complete typecheck coverage. Full profile/source/runtime/metadata/sysroot sealing, snapshot2/plan2 equivalence, physical peak, native admission, full S-M/effectiveL and product qualification remain open.\n\nThe first sampling orchestrator failed before output-root creation because the per-entry parent directory was missing; zero compiler children launched. Exact old runner/failure/empty-root observation are retained. A separate corrected runner creates that parent and produces the twenty new sample graphs; the closed executor is unchanged and no old result is upgraded. Closed six supporting controls are not replayed. Product/law/lock/inventory187/contracts161 unchanged; O7/D3/D13 closed. Exact independent review, own assent and actual design/implementation verification precede architecture-only support publication. No push.\n')
copy(Path(__file__), 'runners/' + Path(__file__).name)
shutil.copytree(D, C / 'continuation-preserved' / D.name)
print('Prepared/preserved 22 actual Smithy graphs, 429 eligible analyses and unchanged unavailable roots.')
