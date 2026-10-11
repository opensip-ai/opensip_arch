from pathlib import Path
import os, json, hashlib, shutil, statistics

os.setpriority(os.PRIO_PROCESS, 0, 10)
B = Path('/tmp/opensip-implementation')
V = B / 'sm-framed-bin-profile-2026-10-10'
D = B / 'sm-actual-smithy-http-fuzz-framed-series-r1-draft'
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

pilot_path = V / 'actual-smithy-http-fuzz-framed-pilot-r1.json'
sample_path = V / 'actual-smithy-http-fuzz-framed-samples-r1.json'
pilot = json.loads(pilot_path.read_bytes())
samples = json.loads(sample_path.read_bytes())
audit = json.loads((V / 'actual-smithy-http-fuzz-framed-wire-audit-r1.json').read_bytes())
assert pilot['compilerChildren'] == 29 and samples['totalCompilerChildren'] == 290
assert samples['totalGraphs'] == 10 and len(samples['series']) == 1
assert audit['compilerChildrenAudited'] == 319 and audit['allFrameAndWireCountsMatch']
assert audit['pilotReceipt'] == samples['pilotReceipt'] == pin(pilot_path)
assert audit['sampleReceipt'] == pin(sample_path)
for name in ['actual-smithy-http-fuzz-framed-pilot-r1.json', 'actual-smithy-http-fuzz-framed-samples-r1.json', 'actual-smithy-http-fuzz-framed-wire-audit-r1.json', 'actual-smithy-http-fuzz-original-source-map-r1.json']:
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
for name in ['run_sm_actual_smithy_http_fuzz_framed_pilot_r1.py', 'run_sm_actual_smithy_http_fuzz_framed_samples_r1.py', 'audit_sm_actual_smithy_http_fuzz_framed_series_r1.py', 'audit_sm_analysis_prepared_reads_r1.py', 'prepare_sm_actual_smithy_http_fuzz_original_source_map_r1.py']:
    copy(B / name, 'runners/' + name)
history = V / 'history-http-pilot-root-count-authoring-r1'
for path in sorted(history.rglob('*')):
    if path.is_file():
        copy(path, 'history-initial-pilot-receipt-root-count/' + path.relative_to(history).as_posix())
report = dict(unit='SM-ACTUAL-SMITHY-HTTP-FUZZ-FRAMED-SERIES-r1', standing='UNREVIEWED ORIGINAL SMITHY HTTP FUZZ GRAPH PILOT AND ELIGIBLE UNIT SERIES',
              actualPilotCompilerChildren=29, actualSampleCompilerChildren=290, totalActualCompilerChildren=319,
              actualPilotGraphs=1, actualSampleGraphs=10, totalActualGraphs=11,
              warmupsPerSeries=3, measuredSamplesPerSeries=7, measuredSeries=1,
              originalGraphUnits=59, eligibleUnitsPerGraph=29, unavailableUnitsPerGraph=30,
              originalGraphRoots=1, unavailableRootsPerGraph=1,
              originalSmithyDeclaredWorkspaceEntries=25, observedOriginalWorkspaceEntries=1,
              compilerChildrenIndependentlyWireAudited=319, allFrameAndWireCountsMatch=True,
              allEligibleAnalysesCompleted=True, mappedReadSetsRepeat=True, metadataHashesRepeat=True,
              originalUnavailableUnitAndRootPopulationsPreserved=True,
              originalStaticConfigurationArgumentsApplied=True, sameChildFramedMapAndAnalysis=True,
              mapDecodingExcludedFromInstrumentedAnalysis=True, observerInstrumentationIncluded=True,
              ownClosedSupportSubject=pilot['ownAcceptedExecutorSubject'],
              seriesStatistics=[dict(ordinal=s['entry']['ordinal'], medianSumInstrumentedAnalysisNanos=s['medianSumInstrumentedAnalysisNanos'], maxSumInstrumentedAnalysisNanos=s['maxSumInstrumentedAnalysisNanos']) for s in samples['series']],
              initialDraftReceiptRootCountCorrectedFromGraph=True,
              newCargoSource=False, newCompilerSource=False, newGraphExecutor=False, controlsRerun=False,
              completeOriginalWorkloadCoverage=False, applicationExecuted=False,
              buildScriptOrProcMacroExecuted=False, sourceRuntimeMetadataSysrootReadsSealed=False,
              snapshot2Plan2Equivalent=False, completeRuntimeCommand=False, fullCargoProfileEnvironment=False,
              physicalPeakScratchMeasured=False, sourceAuthentication=False, nativeAdmission=False,
              completeStatisticalSet=False, productChange=False, SMComplete=False,
              effectiveL=False, productQualification=False, entirePlanComplete=False)
(D / 'draft-source.json').write_text(json.dumps(report, indent=2)+'\n')
(D / 'REPORT.md').write_text("Original Smithy HTTP fuzz pilot and eligible analysis series\n\nOne original graph contains59units andone binary root.29 library units complete analysis;30 units andthe root remain unavailable. Onepilot andtenfresh samplegraphs (threewarmups/seven measured) complete319 compiler analyses. Metadata,readsets,eligible/unavailable populations repeat; independent wholemap/frame/wire/phase/readcall audit coversall319. Wholemap/staticcommand/graph/INFOenv/originalconfig/packet/lock andraw child/metadata/root observations retained.\n\nThe initial unreviewed pilot receipt mistakenly statedfive roots bycopying an earliergraph count. Exactinitialreceipt andrunner retained; correctedreceipt uses actualgraph root list[4],one root. Rawcompiler observations andgraph bytes unchanged; no rerun or upgraded result. Onlyone of25 originalSmithyworkspaces represented. Closed6 controls andexecutors unchanged,not replayed. Instrumented spans exclude decode/metadata andinclude observer; nofull F/T/SM8/physicalpeak/profile/readseal/snapshot2-plan2/sourceauth/native/effectiveL/SM/qualification inference. Product/law/lock unchanged; exactreview,ownassent andfreshverification required before architecture-onlysupport publication. No push.\n")
copy(Path(__file__), 'runners/' + Path(__file__).name)
shutil.copytree(D, C / 'continuation-preserved' / D.name)
print('Prepared/preserved11 actual Smithy HTTP graphs,319 eligible analyses andunavailable root.')
