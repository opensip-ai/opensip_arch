from pathlib import Path
import os, json, hashlib, shutil, statistics

os.setpriority(os.PRIO_PROCESS, 0, 10)
B = Path('/tmp/opensip-implementation')
V = B / 'sm-framed-bin-profile-2026-10-10'
D = B / 'sm-actual-deno-framed-bin-series-r1-draft'
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

pilot = json.loads((V / 'actual-deno-framed-bin-pilot-r1.json').read_bytes())
samples = json.loads((V / 'actual-deno-framed-bin-samples-r1.json').read_bytes())
audit = json.loads((V / 'actual-deno-framed-bin-wire-audit-r1.json').read_bytes())
assert pilot['successfulBinaryAnalysis'] and samples['newCompilerChildren'] == 10
assert audit['compilerChildrenAudited'] == 11 and audit['allFrameAndWireCountsMatch']
assert samples['pilotReceipt'] == pin(V / 'actual-deno-framed-bin-pilot-r1.json')
assert audit['pilotReceipt'] == samples['pilotReceipt']
assert audit['sampleReceipt'] == pin(V / 'actual-deno-framed-bin-samples-r1.json')
assert [r['warmup'] for r in samples['runs']] == [True] * 3 + [False] * 7
assert all(r['pilotPopulationRepeated'] and r['pilotReadSetsRepeated'] for r in samples['runs'])
entry = pilot['entry']
assert samples['entry'] == entry
for name in ['actual-deno-framed-bin-pilot-r1.json', 'actual-deno-framed-bin-samples-r1.json', 'actual-deno-framed-bin-wire-audit-r1.json', 'actual-deno-original-source-maps-r1.json']:
    copy(V / name, 'receipts/' + name)
for label, root in [('pilot', Path(pilot['privateTMPDIR'])), ('samples', Path(samples['root']))]:
    for path in sorted(root.rglob('*')):
        if path.is_file():
            copy(path, 'raw/' + label + '/' + path.relative_to(root).as_posix())
for key in ['sourceMap', 'graph', 'unitCommandData', 'packet']:
    reference = entry[key]
    assert pin(Path(reference['path'])) == {k:reference[k] for k in ['path', 'bytes', 'sha256']}
    copy(Path(reference['path']), 'original-inputs/' + key + Path(reference['path']).suffix)
packet = json.loads(Path(entry['packet']['path']).read_bytes())
static_root = Path(packet['observationRoot'])
for path in sorted(static_root.iterdir()):
    if path.is_file():
        copy(path, 'original-static-collector/' + path.name)
if (static_root / 'queries').exists():
    for path in sorted((static_root / 'queries').rglob('*')):
        if path.is_file():
            copy(path, 'original-static-collector/queries/' + path.relative_to(static_root / 'queries').as_posix())
configuration = packet['configuration']
assert pin(Path(configuration['path'])) == {k:configuration[k] for k in ['path', 'bytes', 'sha256']}
copy(Path(configuration['path']), 'original-inputs/original-config.toml')
closed = B / 'sm-framed-bin-profile-controls-r1-stage'
source = json.loads((closed / 'source.json').read_bytes())
for name in ['source.json', 'subject.json', 'integration.json']:
    copy(closed / name, 'closed-controls/' + name)
for name in ['review.json', 'REVIEW.md']:
    copy(B / 'reviews/grok-sm-framed-bin-profile-controls-r1' / name, 'closed-controls/' + name)
for ordinal, row in enumerate(source['pythonSourcePins'] + [source['closedWrapperPin']]):
    assert all(pin(Path(row['path']))[k] == row[k] for k in ['bytes', 'sha256'])
    copy(Path(row['path']), 'closed-execution-inputs/' + str(ordinal) + '-' + Path(row['path']).name)
for name in ['run_sm_actual_deno_framed_bin_pilot_r1.py', 'run_sm_actual_deno_framed_bin_samples_r1.py', 'audit_sm_actual_deno_framed_bin_series_r1.py', 'audit_sm_analysis_prepared_reads_r1.py']:
    copy(B / name, 'runners/' + name)
measured = [r for r in samples['runs'] if not r['warmup']]
assert samples['medianInstrumentedAnalysisNanos'] == statistics.median(r['instrumentedAnalysisNanos'] for r in measured)
assert samples['maxInstrumentedAnalysisNanos'] == max(r['instrumentedAnalysisNanos'] for r in measured)
report = dict(unit='SM-ACTUAL-DENO-FRAMED-BIN-SERIES-r1', standing='UNREVIEWED ACTUAL ORIGINAL DENO BINARY SUBWORKSPACE PILOT AND SERIES',
              actualPilotCompilerChildren=1, actualSampleCompilerChildren=10, totalActualCompilerChildren=11,
              actualCompilerGraphs=11, warmups=3, measuredSamples=7,
              originalDenoDeclaredWorkspaceEntries=3, observedOriginalWorkspaceEntries=1,
              compilerChildrenIndependentlyWireAudited=11, allFrameAndWireCountsMatch=True,
              allBinaryAnalysesCompleted=True, binaryMetadataNonreusable=True, mappedReadSetsRepeat=True,
              originalStaticConfigurationArgumentsApplied=True, sameChildFramedMapAndAnalysis=True,
              mapDecodingExcludedFromInstrumentedAnalysis=True, observerInstrumentationIncluded=True,
              originalWholeSourceMap=entry['sourceMap'], ownClosedSupportSubject=pilot['ownAcceptedExecutorSubject'],
              medianInstrumentedAnalysisNanos=samples['medianInstrumentedAnalysisNanos'],
              maxInstrumentedAnalysisNanos=samples['maxInstrumentedAnalysisNanos'],
              newCargoSource=False, newCompilerSource=False, newGraphExecutor=False, controlsRerun=False,
              completeOriginalWorkloadCoverage=False, applicationExecuted=False,
              buildScriptOrProcMacroExecuted=False, sourceRuntimeMetadataSysrootReadsSealed=False,
              snapshot2Plan2Equivalent=False, completeRuntimeCommand=False, fullCargoProfileEnvironment=False,
              physicalPeakScratchMeasured=False, sourceAuthentication=False, nativeAdmission=False,
              completeStatisticalSet=False, productChange=False, SMComplete=False,
              effectiveL=False, productQualification=False, entirePlanComplete=False)
(D / 'draft-source.json').write_text(json.dumps(report, indent=2) + '\n')
(D / 'REPORT.md').write_text('Actual original Deno binary subworkspace pilot and series\n\nOne actual binary pilot and ten fresh graphs (three warmups, seven measured samples) complete eleven analyses. Each receives the original whole Deno source map once through the closed framed driver and verifies it in the same compiler child before analysis. An independent audit checks all eleven whole-map/frame/wire byte counts and phase ordering. Mapped read sets repeat. Binary metadata remains null and nonreusable; an empty output file is only a file observation. Original static configuration arguments, constructed environment/cwd, graph, query data and original lock observations are retained. No linking/application/build script/proc macro executes. The measured median instrumented analysis span is ' + str(samples['medianInstrumentedAnalysisNanos']) + ' ns and maximum is ' + str(samples['maxInstrumentedAnalysisNanos']) + ' ns; these exclude decoding/metadata and include observer instrumentation. They are not full F/T or SM8 internal-call timings.\n\nThis is one of three original Deno workspace entries and does not establish complete Deno workload coverage. The full source map is an input read set, not a claim that every project subject was typechecked. Runtime/metadata/sysroot read sealing, snapshot2/plan2 equivalence, source authentication/native owner/worker duties, physical peak and full S-M/effectiveL/product qualification remain open. RSS is informational. Closed six supporting controls are not replayed. Product/law/lock/inventory187/contracts161 unchanged; O7/D3/D13 closed. Exact independent review, own assent and actual design/implementation verification precede architecture-only support publication. Nothing pushed.\n')
copy(Path(__file__), 'runners/' + Path(__file__).name)
shutil.copytree(D, C / 'continuation-preserved' / D.name)
print('Prepared eleven actual Deno binary analyses with original source map and independent wire audit.')
