from pathlib import Path
import os, json, hashlib, sys, tempfile, time
# U-7 (S-M report plan PLAN-r2): large-workload site census. Runs the accepted site-walk v2 image (U-3) as the wrapper
# through the UNCHANGED closed framed-bin executor (sm-framed-bin-profile controls stage pins) over the prepared entries of
# the five accepted large-workload framed series (Smithy fuzz, Smithy http-fuzz, Smithy r11 hierarchy, Deno bin, Deno
# SQLite short paths), twice each (run 0 counts, run 1 checks determinism), and checks each run repeats the accepted
# pilot's unit population. Sites are compiler observations, not candidates. No timing statistic is claimed.
os.setpriority(os.PRIO_PROCESS, 0, 10)
B = Path('/tmp/opensip-implementation'); V = B / 'sm-framed-bin-profile-2026-10-10'; SC = B / 'sm-framed-bin-profile-controls-r1-stage'
H = Path(__file__).resolve().parent; O = Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T')
dest = H / 'large-site-census-r1.json'; assert not dest.exists()
def pin(p): raw = Path(p).read_bytes(); return dict(path=str(p), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
def check(row): assert pin(row['path']) == row, row['path']; return Path(row['path']).read_bytes()
source = json.loads((SC / 'source.json').read_bytes())
for row in source['pythonSourcePins']: check(row)
census_build = json.loads((B / 'sm-rust-site-census-v2-2026-10-13/producer/build.json').read_text())
wrapper = dict(path=census_build['executable'], bytes=census_build['bytes'], sha256=census_build['sha256']); check(wrapper)
assert census_build['siteWalkSource']['sha256'] == pin(B / 'sm-rust-site-census-v2-2026-10-13/producer/site_walk.rs')['sha256']
build = json.loads((B / 'sm-framed-analysis-2026-10-10/build.json').read_bytes())
PILOTS = ['actual-smithy-fuzz-framed-pilots-r1.json', 'actual-smithy-http-fuzz-framed-pilot-r1.json', 'actual-smithy-r11-hierarchy-r9-framed-pilots-r1.json',
          'actual-deno-framed-bin-pilot-r1.json', 'actual-deno-sqlite-short-paths-framed-pilot-r1.json']
entries = []
for name in PILOTS:
    p = json.loads((V / name).read_bytes()); results = p['results'] if 'results' in p else [dict(entry=p['entry'], result=p['result'])]
    for r in results: entries.append(dict(pilot=pin(V / name), entry=r['entry'], expected=[(u['index'], u['standing'], u.get('reason')) for u in r['result']['unitResults']]))
sys.path.insert(0, str(V)); from framed_bin_profile_graph_execution import execute_graph
lane = O / 'opensip-lanes.lock'; owned = False; home = os.environ.get('HOME'); records = []
while True:
    try: lane.mkdir(); owned = True; break
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    root = Path(tempfile.mkdtemp(prefix='opensip-sm-large-site-census-', dir=O)); root.chmod(0o700)
    for k, e in enumerate(entries):
        entry = e['entry']; graph = json.loads(check(entry['graph'])); runs = []
        for n in range(2):
            for row in source['pythonSourcePins'] + [wrapper, entry['sourceMap'], entry['unitCommandData'], entry['graph']]: check(row)
            result = execute_graph(graph, entry['sourceMap'], root / f'{k}-{n}', wrapper, build['sysroot'], Path(entry['cwd']), entry['unitCommandData'])
            units = []
            for u in result['unitResults']:
                gu = graph['units'][u['index']]
                row = dict(index=u['index'], packageId=gu['pkg_id'], targetKind=gu['target']['kind'], firstParty=gu['pkg_id'].startswith('path+'), standing=u['standing'], reason=u.get('reason'), compilerLaunched=u['compilerLaunched'])
                if u['compilerLaunched']:
                    walks = [x for x in u['events'] if x['event'] == 'site_walk']; spans = [x for x in u['events'] if x['event'] == 'after_analysis']
                    row.update(siteWalkEvents=len(walks), afterAnalysisEvents=len(spans), siteWalk=walks[0] if walks else None, informationalRSSNative=u['observationInformational']['rss_native'])
                units.append(row)
            runs.append(dict(run=n, compilerChildren=result['compilerChildren'], units=units))
        strip = lambda r: [{a: b for a, b in (u['siteWalk'] or {}).items() if a != 'walkElapsedNanos'} for u in r['units'] if u['compilerLaunched']]
        populations = [[(u['index'], u['standing'], u['reason']) for u in r['units']] for r in runs]
        records.append(dict(id=entry['id'], ordinal=entry['ordinal'], cwd=entry['cwd'], pilot=e['pilot'], graph=entry['graph'], sourceMap=entry['sourceMap'], runs=runs,
                            acceptedPilotPopulationRepeated=all(p == e['expected'] for p in populations), siteCountsDeterministic=strip(runs[0]) == strip(runs[1])))
        report = dict(standing='UNREVIEWED OUTSIDE-PRODUCT LARGE-WORKLOAD RUST SITE CENSUS (U-7; SM-13 DECOMPOSITION INPUT); SITES ARE NOT CANDIDATES', root=str(root), results=records,
                      wrapperPin=wrapper, siteWalkBuild=census_build, executorPins=source['pythonSourcePins'], pilots=[pin(V / n) for n in PILOTS],
                      compilerChildren=sum(r['compilerChildren'] for x in records for r in x['runs']), ownedLaneForEntireSet=True, niceness=os.getpriority(os.PRIO_PROCESS, 0), timingStatisticClaimed=False,
                      stageListChosen=False, requestedKeysChosen=False, emissionFactorsChosen=False, censusKindsChosen=False, batchingChosen=False, nativeAdmission=False, SMComplete=False, LG1Met=False, effectiveL=False, productQualification=False)
        dest.write_text(json.dumps(report, indent=1) + '\n'); print(k, entry['id'], entry['ordinal'], records[-1]['acceptedPilotPopulationRepeated'], records[-1]['siteCountsDeterministic'], flush=True)
finally:
    if owned: lane.rmdir()
    assert os.environ.get('HOME') == home and not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
