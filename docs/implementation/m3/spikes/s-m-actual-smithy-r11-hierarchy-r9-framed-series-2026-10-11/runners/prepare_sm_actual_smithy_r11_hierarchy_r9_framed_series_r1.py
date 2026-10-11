from pathlib import Path
import os, json, hashlib, shutil, statistics, tarfile, lzma, io

# Derived from prepare_sm_actual_smithy_http_fuzz_framed_series_r1.py for seven graphs.
# Size policy (lead decision 2026-10-11): per-child JSON/log/dep-info are archived; compiler metadata (.rmeta),
# incremental state and empty binary outputs stay external and whole-pinned (not self-contained, like the accepted
# static DATA archives). Source maps over the remote's 100 MiB file limit are stored as deterministic USTAR/xz (LFS).
os.setpriority(os.PRIO_PROCESS, 0, 10)
B = Path('/tmp/opensip-implementation')
V = B / 'sm-framed-bin-profile-2026-10-10'
L = B / 'sm-large-original-context-census-2026-10-10'
D = B / 'sm-actual-smithy-r11-hierarchy-r9-framed-series-r1-draft'
C = Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06')
LIMIT = 100 << 20
assert not D.exists()
D.mkdir()
external = []
packed_receipts = []

def pin(path):
    raw = path.read_bytes()
    return dict(path=str(path), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())

def copy(path, relative):
    reference = pin(path)
    destination = D / relative
    assert not destination.exists() and reference['bytes'] < LIMIT
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(path, destination)
    assert all(pin(destination)[k] == reference[k] for k in ['bytes', 'sha256'])
    return reference

def pack(path, relative):
    raw = path.read_bytes()
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode='w', format=tarfile.USTAR_FORMAT) as t:
        info = tarfile.TarInfo(path.name); info.size = len(raw); info.mtime = 0; info.mode = 0o444; info.uid = info.gid = 0; info.uname = info.gname = ''
        t.addfile(info, io.BytesIO(raw))
    packed = lzma.compress(buf.getvalue(), format=lzma.FORMAT_XZ, check=lzma.CHECK_CRC64, preset=6)
    destination = D / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(packed)
    with tarfile.open(destination, mode='r:xz') as t:
        assert t.extractfile(t.getmembers()[0]).read() == raw
    return dict(inner=dict(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest()), archive=relative, archiveBytes=len(packed))

def archive_raw(root, label):
    for path in sorted(root.rglob('*')):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if path.suffix in ('.json', '.log', '.d'):
            copy(path, 'raw/' + label + '/' + rel)
        else:
            external.append(pin(path))

pilot_path = V / 'actual-smithy-r11-hierarchy-r9-framed-pilots-r1.json'
sample_path = V / 'actual-smithy-r11-hierarchy-r9-framed-samples-r1.json'
audit_path = V / 'actual-smithy-r11-hierarchy-r9-framed-wire-audit-r1.json'
maps_path = V / 'actual-smithy-r11-hierarchy-r9-source-maps-r1.json'
pilot = json.loads(pilot_path.read_bytes()); samples = json.loads(sample_path.read_bytes()); audit = json.loads(audit_path.read_bytes()); maps = json.loads(maps_path.read_bytes())
assert pilot['compilerChildren'] == 412 and samples['totalCompilerChildren'] == 4120 and samples['totalGraphs'] == 70 and len(samples['series']) == 7
assert audit['compilerChildrenAudited'] == 4532 and audit['allFrameAndWireCountsMatch']
assert audit['pilotReceipt'] == samples['pilotReceipt'] == pin(pilot_path) and audit['sampleReceipt'] == pin(sample_path)
for path in [pilot_path, sample_path, audit_path, maps_path, L / 'actual-smithy-original-workspace-attempts-r11.json', L / 'actual-original-hierarchy-workspace-attempts-r9.json']:
    if path.stat().st_size < LIMIT:
        copy(path, 'receipts/' + path.name)
    else:
        packed_receipts.append(dict(name=path.name, **pack(path, 'receipts/' + path.name + '.tar.xz')))
archive_raw(Path(pilot['root']), 'pilots')
archive_raw(Path(samples['root']), 'samples')
packed_maps = []
statistics_rows = []
for before, series in zip(pilot['results'], samples['series']):
    entry = before['entry']
    assert series['entry'] == entry and [r['warmup'] for r in series['runs']] == [True]*3 + [False]*7
    assert all(r['pilotPopulationRepeated'] and r['pilotMappedReadSetsRepeated'] and r['pilotMetadataHashesRepeated'] for r in series['runs'])
    measured = [r for r in series['runs'] if not r['warmup']]
    assert series['medianSumInstrumentedAnalysisNanos'] == statistics.median(r['sumInstrumentedAnalysisNanos'] for r in measured)
    statistics_rows.append(dict(ordinal=entry['ordinal'], manifest=entry['originalRelativeManifest'], graphUnits=entry['graphUnits'], analysedUnitsPerGraph=before['compilerChildren'], unavailableUnitsPerGraph=entry['graphUnits'] - before['compilerChildren'], rootStandings=before['rootStandings'], preparedDescriptorBytes=entry['preparedDescriptorBytes'], medianSumInstrumentedAnalysisNanos=series['medianSumInstrumentedAnalysisNanos'], maxSumInstrumentedAnalysisNanos=series['maxSumInstrumentedAnalysisNanos']))
    for key in ['graph', 'unitCommandData', 'packet']:
        reference = entry[key]
        assert pin(Path(reference['path'])) == {k: reference[k] for k in ['path', 'bytes', 'sha256']}
        copy(Path(reference['path']), 'original-inputs/' + str(entry['ordinal']) + '/' + key + Path(reference['path']).suffix)
    source_map = Path(entry['sourceMap']['path'])
    assert pin(source_map) == {k: entry['sourceMap'][k] for k in ['path', 'bytes', 'sha256']}
    if entry['sourceMap']['bytes'] < LIMIT:
        copy(source_map, 'original-inputs/' + str(entry['ordinal']) + '/sourceMap.bin')
    else:
        packed_maps.append(dict(ordinal=entry['ordinal'], **pack(source_map, 'original-inputs/' + str(entry['ordinal']) + '/sourceMap.bin.tar.xz')))
    packet = json.loads(Path(entry['packet']['path']).read_bytes())
    static_root = Path(packet['observationRoot'])
    for path in sorted(static_root.iterdir()):
        if path.is_file() and path.name != 'packet.json':
            copy(path, 'original-static-collectors/' + str(entry['ordinal']) + '/' + path.name)
    for path in sorted((static_root / 'queries').rglob('*')):
        if path.is_file():
            copy(path, 'original-static-collectors/' + str(entry['ordinal']) + '/queries/' + path.relative_to(static_root / 'queries').as_posix())
    configs = [packet['configuration']] if packet.get('configuration') else packet['configurationHierarchy']
    for index, configuration in enumerate(configs):
        assert pin(Path(configuration['path'])) == {k: configuration[k] for k in ['path', 'bytes', 'sha256']}
        copy(Path(configuration['path']), 'original-inputs/' + str(entry['ordinal']) + f'/original-config-{index}.toml')
    lock = packet['originalLock']
    assert pin(Path(lock['path'])) == {k: lock[k] for k in ['path', 'bytes', 'sha256']}
    copy(Path(lock['path']), 'original-inputs/' + str(entry['ordinal']) + '/original-Cargo.lock')
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
for name in ['prepare_sm_actual_smithy_r11_hierarchy_r9_source_maps_r1.py', 'run_sm_actual_smithy_r11_hierarchy_r9_framed_pilots_r1.py', 'run_sm_actual_smithy_r11_hierarchy_r9_framed_samples_r1.py', 'audit_sm_actual_smithy_r11_hierarchy_r9_framed_series_r1.py', 'audit_sm_analysis_prepared_reads_r1.py']:
    copy(B / name, 'runners/' + name)
for name in ['smithy-r11-hierarchy-r9-pilots-r1-driver.log', 'smithy-r11-hierarchy-r9-samples-r1-driver.log']:
    copy(V / name, 'runners/' + name)
(D / 'external-output-pins.json').write_text(json.dumps(dict(standing='COMPILER METADATA/INCREMENTAL/BINARY OUTPUTS RETAINED EXTERNALLY AND WHOLE-PINNED; NOT SELF-CONTAINED', files=external), indent=2) + '\n')
unavailable = maps['unavailableBeforeLaunch']
report = dict(unit='SM-ACTUAL-SMITHY-R11-HIERARCHY-R9-FRAMED-SERIES-r1',
              standing='UNREVIEWED ORIGINAL SMITHY aws/rust-runtime AND SIX ORIGINAL MULTI-CONFIGURATION TOOL WORKSPACE PILOTS AND ELIGIBLE SERIES; CANARY-RUNNER UNAVAILABLE BEFORE LAUNCH',
              actualGraphsSeries=7, actualPilotCompilerChildren=412, actualSampleCompilerChildren=4120, totalActualCompilerChildren=4532,
              actualPilotGraphs=7, actualSampleGraphs=70, totalActualGraphs=77, warmupsPerSeries=3, measuredSamplesPerSeries=7, measuredSeries=7,
              originalGraphUnits=sum(r['graphUnits'] for r in statistics_rows), analysedUnitsPerSeriesSum=412,
              unavailableBeforeLaunchGraphs=len(unavailable), unavailableBeforeLaunchDescriptorBytes=unavailable[0]['preparedDescriptorBytes'],
              preparedDescriptorBoundBytes=4 << 20, compilerChildrenIndependentlyWireAudited=4532, allFrameAndWireCountsMatch=True,
              allLaunchedAnalysesCompleted=True, mappedReadSetsRepeat=True, metadataHashesRepeat=True, rootPopulationsRepeat=True,
              originalUnavailableUnitAndRootPopulationsPreserved=True, descriptorCheckedBeforeLaunch=True, sourcesTrimmed=False, descriptorBoundChanged=False,
              originalPinnedLocksPreserved=True, originalConfigurationHierarchiesPreserved=True, sameChildFramedMapAndAnalysis=True,
              mapDecodingExcludedFromInstrumentedAnalysis=True, observerInstrumentationIncluded=True,
              externalOutputPinnedFiles=len(external), packedSourceMaps=len(packed_maps),
              concurrentReadOnlyReviewAndIntegrationWorkDuringSeries=True,
              ownClosedSupportSubject=pilot['ownAcceptedExecutorSubject'], seriesStatistics=statistics_rows, sourceMapArchives=packed_maps, receiptArchives=packed_receipts,
              newCargoSource=False, newCompilerSource=False, newGraphExecutor=False, controlsRerun=False,
              completeOriginalWorkloadCoverage=False, applicationExecuted=False, buildScriptOrProcMacroExecuted=False,
              sourceRuntimeMetadataSysrootReadsSealed=False, snapshot2Plan2Equivalent=False, completeRuntimeCommand=False,
              fullCargoProfileEnvironment=False, physicalPeakScratchMeasured=False, sourceAuthentication=False, nativeAdmission=False,
              completeStatisticalSet=False, productChange=False, SMComplete=False, effectiveL=False, productQualification=False, entirePlanComplete=False)
(D / 'draft-source.json').write_text(json.dumps(report, indent=2) + '\n')
lines = '\n'.join(f"- ordinal {r['ordinal']} `{r['manifest']}`: {r['graphUnits']} units, {r['analysedUnitsPerGraph']} analysed per graph, roots {r['rootStandings']}, descriptor {r['preparedDescriptorBytes']} B, measured median {r['medianSumInstrumentedAnalysisNanos']} ns" for r in statistics_rows)
(D / 'REPORT.md').write_text(f"""Original Smithy r11 / hierarchy r9 seven-graph pilots and eligible analysis series

After the lock-derived public dependency intake, original Smithy `aws/rust-runtime` and the original multi-configuration tool workspaces produced static graphs. Seven graphs have prepared descriptors under the closed driver's unchanged 4194304-byte bound, checked before launch. `tools/ci-cdk/canary-runner` (ordinal 24) has a {report['unavailableBeforeLaunchDescriptorBytes']}-byte descriptor and is unavailable before launch; nothing was trimmed and the bound was not changed.

One pilot and ten fresh sample graphs per series (3 warmups, 7 measured) complete 4532 compiler analyses: every launched child completed. Unit/root populations, mapped read sets and metadata hashes repeat. An independent wire/frame/phase/read-call audit covers all 4532 children.

{lines}

Per-child JSON, logs and dep-info are archived; compiler metadata, incremental state and empty binary outputs ({len(external)} files) stay external and whole-pinned, so the archive is not self-contained. Source maps and the sample receipt that exceed the remote's 100 MiB file limit are stored as deterministic USTAR/xz archives whose single member keeps the pinned bytes. Read-only review and integration work ran concurrently on the same machine during part of the series, so timings are informational. The closed framed driver, executor, observer and controls are unchanged and not replayed. Spans exclude map decoding and include observer instrumentation. No full coverage, F/T/SM8, physical peak, profile, read seal, snapshot2/plan2, source authentication, native admission, effective L, full S-M or qualification inference. Product, law and lock unchanged; exact review, own assent and fresh verification required before architecture-only publication. No push.
""")
copy(Path(__file__), 'runners/' + Path(__file__).name)
shutil.copytree(D, C / 'continuation-preserved' / D.name)
print(json.dumps(dict(members=sum(1 for _ in D.rglob('*') if _.is_file()), external=len(external), packedMaps=len(packed_maps)), indent=2))
