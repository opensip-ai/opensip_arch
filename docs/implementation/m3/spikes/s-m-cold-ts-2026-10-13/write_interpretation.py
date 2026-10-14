from pathlib import Path
import json, hashlib
# U-5a current interpretation (Codex SM-COLD-TS-R1-RF-01). The cold runners are byte-copies of accepted runners, so their
# generated result files inherit the parents' `standing`/label strings. Those files are kept verbatim; this record is the
# CURRENT interpretation and supersedes every inherited classification field it names.
W = Path(__file__).resolve().parent
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
COLD = 'cold OpenSIP state, page cache recorded (never claimed flushed); Q0 9.2 cold reset before every run (U-5a)'
files = {'sm1': 'sm1/results.json', 'sealing': 'sealing/results.json', 'transfer': 'transfer/results.json', 'cohort': 'cohort/results.json',
         'synthesized': 'synthesized/results.json', 'replay': 'replay/sized-replay-results-cold-ts.json'}
out = dict(standing='CURRENT INTERPRETATION OF THE U-5a GENERATED RESULTS; SUPERSEDES INHERITED CLASSIFICATION FIELDS NAMED BELOW', components={})
for name, rel in files.items():
    row = dict(result=dict(path=rel, sha256=sha(W / rel)), resultKeptVerbatim=True, resetLabel=COLD, inheritedStandingIsParentRunnerText=True)
    if name == 'replay':
        r = json.loads((W / rel).read_text())
        assert r['SM9LowerBoundOnly'] is True and 'LOWER-BOUND' in r['standing'] and 'no page-cache record' in r['resetLabel']
        row.update(obsoleteInheritedFields=dict(standing=r['standing'], SM9LowerBoundOnly=r['SM9LowerBoundOnly'], resetLabel=r['resetLabel']),
                   currentStanding='Synthetic SM-9 under the accepted S-M report plan D-1: workload source-count scenarios (one exists/file fact, finding and fingerprint per counted source) at the six TS row sizes; no real-workload bound is established (Codex SM-REPLAY-SIZED-R1-RF-01); any F, T or outcome built on it is conditional on D-1',
                   SM9LowerBoundOnly=False, lowerBoundEstablished=False, realWorkloadInference=False)
    out['components'][name] = row
(W / 'cold-ts-interpretation.json').write_text(json.dumps(out, indent=1) + '\n')
print('interpretation written')
