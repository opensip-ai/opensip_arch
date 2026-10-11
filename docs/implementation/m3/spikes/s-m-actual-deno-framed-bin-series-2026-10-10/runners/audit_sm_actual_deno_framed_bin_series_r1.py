from pathlib import Path
import json, hashlib

B = Path('/tmp/opensip-implementation')
V = B / 'sm-framed-bin-profile-2026-10-10'
destination = V / 'actual-deno-framed-bin-wire-audit-r1.json'
assert not destination.exists()

def pin(path):
    raw = path.read_bytes()
    return dict(path=str(path), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())

pilot_path = V / 'actual-deno-framed-bin-pilot-r1.json'
sample_path = V / 'actual-deno-framed-bin-samples-r1.json'
pilot = json.loads(pilot_path.read_bytes())
samples = json.loads(sample_path.read_bytes())
assert samples['pilotReceipt'] == pin(pilot_path)
assert pilot['successfulBinaryAnalysis'] and pilot['compilerChildren'] == 1
assert samples['newCompilerChildren'] == 10 and len(samples['runs']) == 10
assert [r['warmup'] for r in samples['runs']] == [True] * 3 + [False] * 7
entry = pilot['entry']
assert samples['entry'] == entry
assert pin(Path(entry['sourceMap']['path'])) == entry['sourceMap']
rows = []
for label, result in [('pilot', pilot['result'])] + [(str(r['ordinal']), r['result']) for r in samples['runs']]:
    assert result['compilerChildren'] == 1
    child = result['unitResults'][0]
    assert child['standing'] == 'analysis-completed-binary' and child['analysisCompleted']
    assert child['metadata'] is None and child['reusableLibraryMetadata'] is False
    events = child['events']
    wire = [e for e in events if e['event'] == 'prepared_map_wire_verified']
    assert len(wire) == 1
    source_map = entry['sourceMap']
    assert wire[0]['mapSha256'] == source_map['sha256'] and wire[0]['mapBytes'] == source_map['bytes']
    frames = (source_map['bytes'] + (1 << 20) - 1) // (1 << 20)
    header = json.dumps(dict(format='OPSMRUST1', bytes=source_map['bytes'], sha256=source_map['sha256']), sort_keys=True, separators=(',', ':')).encode()
    expected_bytes = source_map['bytes'] + 4 * frames + 4 + len(header)
    observation = child['observationInformational']
    assert wire[0]['contentFrames'] == frames and observation['wire_bytes_written'] == expected_bytes
    assert 0 < observation['worker_ready_elapsed_nanos'] < observation['map_wire_verified_elapsed_nanos'] <= observation['map_decode_complete_elapsed_nanos'] <= observation['root_reaped_elapsed_nanos']
    analyses = [e for e in events if e['event'] == 'after_analysis']
    assert len(analyses) == 1 and 0 < analyses[0]['analysisElapsedNanos'] <= observation['root_reaped_elapsed_nanos']
    reads = [e for e in events if e['event'] == 'prepared_source_read']
    assert len(reads) == analyses[0]['readCalls']
    rows.append(dict(run=label, mapBytes=source_map['bytes'], contentFrames=frames,
                     wireBytes=expected_bytes, readCalls=len(reads),
                     deniedReadCalls=sum(not e['preparedMapEntryPresent'] for e in reads),
                     analysisElapsedNanos=analyses[0]['analysisElapsedNanos']))
report = dict(pilotReceipt=pin(pilot_path), sampleReceipt=pin(sample_path),
              compilerChildrenAudited=11, allFrameAndWireCountsMatch=True,
              allBinaryMetadataNonreusable=True, observations=rows,
              completeOriginalWorkloadCoverage=False, physicalPeakScratchMeasured=False,
              sourceAuthentication=False, nativeAdmission=False, SMComplete=False)
destination.write_text(json.dumps(report, indent=2) + '\n')
print('Independently audited eleven original Deno binary children; full Deno coverage remains open.')
