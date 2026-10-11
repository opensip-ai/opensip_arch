from pathlib import Path
import json, hashlib

V = Path('/tmp/opensip-implementation/sm-framed-bin-profile-2026-10-10')
destination = V / 'actual-smithy-http-fuzz-framed-wire-audit-r1.json'
assert not destination.exists()

def pin(path):
    raw = path.read_bytes()
    return dict(path=str(path), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())

pilot_path = V / 'actual-smithy-http-fuzz-framed-pilot-r1.json'
sample_path = V / 'actual-smithy-http-fuzz-framed-samples-r1.json'
pilot = json.loads(pilot_path.read_bytes())
samples = json.loads(sample_path.read_bytes())
assert samples['pilotReceipt'] == pin(pilot_path)
assert samples['completedSeries'] == 1 and samples['totalGraphs'] == 10 and samples['totalCompilerChildren'] == 290
assert pilot['compilerChildren'] == 29
rows = []
for baseline, series in zip(pilot['results'], samples['series']):
    assert series['entry'] == baseline['entry']
    entry = series['entry']
    assert pin(Path(entry['sourceMap']['path'])) == entry['sourceMap']
    expected = [(u['index'], u['standing'], u.get('reason')) for u in baseline['result']['unitResults']]
    metadata = {u['index']:u['metadata']['sha256'] for u in baseline['result']['unitResults'] if u.get('metadata')}
    assert [r['warmup'] for r in series['runs']] == [True]*3+[False]*7
    for label, result in [('pilot', baseline['result'])] + [(str(r['ordinal']), r['result']) for r in series['runs']]:
        assert [(u['index'], u['standing'], u.get('reason')) for u in result['unitResults']] == expected
        assert {u['index']:u['metadata']['sha256'] for u in result['unitResults'] if u.get('metadata')} == metadata
        assert all(u['standing'] == 'unavailable' for u in result['rootResults'])
        source_map = entry['sourceMap']
        frames = (source_map['bytes']+(1<<20)-1)//(1<<20)
        header = json.dumps(dict(format='OPSMRUST1', bytes=source_map['bytes'], sha256=source_map['sha256']), sort_keys=True, separators=(',', ':')).encode()
        wire_bytes = source_map['bytes']+4*frames+4+len(header)
        for child in result['unitResults']:
            if not child['compilerLaunched']:
                continue
            assert child['analysisCompleted'] and child['standing'] == 'analysis-and-metadata-completed'
            assert child['metadata'] is not None and child['reusableLibraryMetadata']
            assert pin(Path(child['metadata']['path'])) == child['metadata']
            wire = [e for e in child['events'] if e['event'] == 'prepared_map_wire_verified']
            assert len(wire) == 1 and wire[0]['mapSha256'] == source_map['sha256'] and wire[0]['mapBytes'] == source_map['bytes'] and wire[0]['contentFrames'] == frames
            obs = child['observationInformational']
            assert obs['wire_bytes_written'] == wire_bytes
            assert 0 < obs['worker_ready_elapsed_nanos'] < obs['map_wire_verified_elapsed_nanos'] <= obs['map_decode_complete_elapsed_nanos'] <= obs['root_reaped_elapsed_nanos']
            analyses = [e for e in child['events'] if e['event'] == 'after_analysis']
            assert len(analyses) == 1 and 0 < analyses[0]['analysisElapsedNanos'] <= obs['root_reaped_elapsed_nanos']
            reads = [e for e in child['events'] if e['event'] == 'prepared_source_read']
            assert len(reads) == analyses[0]['readCalls']
            rows.append(dict(entry=entry['ordinal'], run=label, unit=child['index'], mapBytes=source_map['bytes'], contentFrames=frames, wireBytes=wire_bytes, readCalls=len(reads), deniedReadCalls=sum(not e['preparedMapEntryPresent'] for e in reads), analysisElapsedNanos=analyses[0]['analysisElapsedNanos']))
assert len(rows) == 319
report = dict(pilotReceipt=pin(pilot_path), sampleReceipt=pin(sample_path), compilerChildrenAudited=319,
              allFrameAndWireCountsMatch=True, unitAndUnavailableRootPopulationsRepeat=True,
              metadataHashesRepeat=True, observations=rows, completeOriginalWorkloadCoverage=False,
              sourceAuthentication=False, nativeAdmission=False, physicalPeakScratchMeasured=False, SMComplete=False)
destination.write_text(json.dumps(report, indent=2)+'\n')
print('Audited 319 compiler children; unavailable fuzz roots remain unavailable.')
