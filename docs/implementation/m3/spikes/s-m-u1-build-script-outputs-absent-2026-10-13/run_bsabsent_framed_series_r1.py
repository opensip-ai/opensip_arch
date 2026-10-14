from pathlib import Path
import os, json, hashlib, sys, tempfile, time, statistics
# U-1 (S-M report plan): SM-4 coverage series with build-script outputs absent. The CLOSED framed driver image and root
# observer (sm-framed-analysis controls stage pins) run through the U-1 executor VARIANT over the nine entries' VARIANT
# static command data and source maps (producer variant: commands for libraries blocked only by build scripts, with
# OUT_DIR removed), 3 warmups + 7 measured per entry, whole-graph span and summed instrumented analysis per run.
# Controls: population and metadata hashes repeat across the ten runs; every unit the accepted framed series analysed
# reproduces its accepted metadata hash. No build script or proc-macro runs; nothing is trimmed or rebounded.
os.setpriority(os.PRIO_PROCESS, 0, 10)
B = Path('/tmp/opensip-implementation'); V = B / 'sm-command-data-bsabsent-2026-10-13'; F = B / 'sm-framed-analysis-2026-10-10'; S = B / 'sm-framed-analysis-controls-r1-stage'
O = Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T'); A = Path('/Users/sb/code/opensip-ai/opensip_arch'); SERIES = A / 'docs/implementation/m3/spikes/s-m-actual-framed-analysis-series-2026-10-10'
dest = V / 'bsabsent-framed-series-r1.json'; assert not dest.exists()
def check(row): raw = Path(row['path']).read_bytes(); assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256'], row['path']; return raw
def pin(p): raw = Path(p).read_bytes(); return dict(path=str(p), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
source = json.loads((S / 'source.json').read_bytes()); wrapper = source['compiledImage']; check(wrapper); check(source['rootObserverSource']); check(source['driverSource'])
executor = pin(V / 'framed_profile_graph_execution_bsabsent.py'); closed_executor = source['graphExecutorSource']; check(closed_executor)
audit_source = dict(path=str(B / 'audit_sm_analysis_prepared_reads_r1.py'), bytes=2415, sha256='687ca8eadde2abd5c5146c43000cd4584ea592e58551545fcc32406f806e8fb7'); check(audit_source)
closed = json.loads((B / 'sm-graph-metadata-controls-r1-stage/source.json').read_bytes())
maps_pin = pin(V / 'bsabsent-command-source-maps-r1.json'); prepared = json.loads(check(maps_pin)); assert len(prepared['results']) == 9
accepted = {s['ordinal']: s for s in json.loads((SERIES / 'actual-framed-analysis-samples-r1.json').read_bytes())['series']}
root = Path(tempfile.mkdtemp(prefix='opensip-sm-bsabsent-framed-series-', dir=O)); root.chmod(0o700); lane = O / 'opensip-lanes.lock'; owned = False; home = os.environ.get('HOME'); series = []
while True:
    try: lane.mkdir(); owned = True; break
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    sys.path.insert(0, str(B)); from audit_sm_analysis_prepared_reads_r1 import audit
    sys.path.insert(0, str(F)); sys.path.insert(0, str(V)); from framed_profile_graph_execution_bsabsent import execute_graph
    for entry in prepared['results']:
        graph = json.loads(check(entry['graph'])); r = root / str(entry['ordinal']); r.mkdir(mode=0o700); samples = []; first = None
        for ordinal in range(10):
            check(executor); check(wrapper); check(entry['sourceMap']); check(entry['unitCommandData'])
            started = time.monotonic_ns(); result = execute_graph(graph, entry['sourceMap'], r / str(ordinal), wrapper, closed['sysroot'], Path(entry['cwd']), entry['unitCommandData']); elapsed = time.monotonic_ns() - started
            population = {u['index']: (u['standing'], u.get('reason')) for u in result['unitResults']}
            if first is None: first = population
            reads = audit(entry['sourceMap'], result['unitResults'])
            samples.append(dict(ordinal=ordinal, warmup=ordinal < 3, wholeGraphNanos=elapsed, result=result, preparedReadSetAudit=reads, populationRepeatsFirstRun=population == first))
            print(entry['ordinal'], ordinal, result['compilerChildren'], elapsed, flush=True)
        for sample in samples:
            spans = []
            for unit in sample['result']['unitResults']:
                if not unit['compilerLaunched']: continue
                ev = [e for e in unit['events'] if e['event'] == 'after_analysis']
                if len(ev) == 1: spans.append(ev[0]['analysisElapsedNanos'])
            sample['sumInstrumentedAnalysisNanos'] = sum(spans)
        analysed = sorted(i for i, (st, _) in first.items() if st == 'analysis-and-metadata-completed')
        hashes = {str(i): sorted({u['metadata']['sha256'] for s in samples for u in s['result']['unitResults'] if u['index'] == i and u.get('metadata')}) for i in analysed}
        acc = accepted[entry['ordinal']]; acc_hashes = acc['metadataHashSets']
        accepted_units_repeat = all(hashes.get(i) == h for i, h in acc_hashes.items())
        units = graph['units']; new_units = [i for i in analysed if str(i) not in acc_hashes]
        measured = [s for s in samples if not s['warmup']]
        series.append(dict(id=entry['id'], ordinal=entry['ordinal'], graph=entry['graph'], sourceMap=entry['sourceMap'], unitCommandData=entry['unitCommandData'], runs=samples, warmups=3, measuredSamples=7,
                           compilerChildren=sum(s['result']['compilerChildren'] for s in samples), populationRepeated=all(s['populationRepeatsFirstRun'] for s in samples), readSetsRepeated=all(s['preparedReadSetAudit'] == samples[0]['preparedReadSetAudit'] for s in samples),
                           metadataHashSets=hashes, metadataRepeatForEveryAnalyzedUnit=all(len(h) == 1 for h in hashes.values()), acceptedSeriesUnitsReproduceAcceptedMetadata=accepted_units_repeat,
                           analysedUnits=len(analysed), newlyAnalysedUnits=[dict(index=i, name=units[i]['target']['name'], packageId=units[i]['pkg_id'], firstParty=units[i]['pkg_id'].startswith('path+')) for i in new_units],
                           incompleteUnits=sorted(i for i, (st, _) in first.items() if st == 'incomplete'),
                           medianWholeGraphNanos=statistics.median(s['wholeGraphNanos'] for s in measured), maxWholeGraphNanos=max(s['wholeGraphNanos'] for s in measured),
                           medianSumInstrumentedAnalysisNanos=statistics.median(s['sumInstrumentedAnalysisNanos'] for s in measured), maxSumInstrumentedAnalysisNanos=max(s['sumInstrumentedAnalysisNanos'] for s in measured),
                           acceptedMedianWholeGraphNanos=acc['medianWholeGraphNanos']))
        report = dict(standing='UNREVIEWED U-1 SM-4 COVERAGE SERIES (BUILD-SCRIPT OUTPUTS ABSENT); NOT FULL S-M', root=str(root), series=series, totalCompilerChildren=sum(s['compilerChildren'] for s in series),
                      executorPin=executor, closedExecutorPin=closed_executor, wrapperPin=wrapper, readAuditSource=audit_source, preparedMaps=maps_pin, buildScriptOrProcMacroExecuted=False,
                      ownedLaneForEntireSet=True, niceness=os.getpriority(os.PRIO_PROCESS, 0), HOMEUnchanged=os.environ.get('HOME') == home, SMComplete=False, LG1Met=False, effectiveL=False, productQualification=False)
        dest.write_text(json.dumps(report, indent=1) + '\n')
    print('U-1 series complete', flush=True)
finally:
    if owned: lane.rmdir()
    assert os.environ.get('HOME') == home and not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
