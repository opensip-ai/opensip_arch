from pathlib import Path
import json, hashlib
# U-5b current interpretation (as U-5a round 2 required): each cold runner is a byte copy of an accepted runner, so its
# result file carries the accepted runner's `standing` text verbatim. That inherited text is obsolete for these files;
# this record gives each component's current label. Measurement bytes are unchanged.
W = Path(__file__).resolve().parent; sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
LABEL = 'cold OpenSIP state, page cache recorded (never claimed flushed); fresh empty per-run TMPDIR as the disposable cache; new process per run'
RES = {'sm3': 'sm3/results.json', 'replay': 'replay/sized-replay-results-cold-rust.json', 'sm4': 'sm4/bsabsent-static-profile-series-cold-rust.json', 'sm5': 'sm5/sm5-two-part-results-r2.json', 'sm7': 'sm7/sm7-results-r3.json'}
FIG = {'sm3': 'SM-3 (Rust start)', 'replay': 'SM-9 at the eight Rust row sizes (synthetic under D-1)', 'sm4': 'SM-4 (U-1 static-profile whole graph, build-script outputs absent)', 'sm5': 'SM-5 (two parts, one span)', 'sm7': 'SM-7 (r3, every NE 9.2 dependency field)'}
rows = {}
for k, rel in RES.items():
    d = json.loads((W / rel).read_text()); row = dict(figure=FIG[k], result=dict(path=rel, sha256=sha(W / rel)), resetLabel=LABEL, inheritedStanding=d.get('standing'), inheritedStandingObsolete=True,
                                                  currentStanding='UNREVIEWED U-5b COLD-RESET SERIES (PLAN-r3 D-7, U-5); LEAD macOS PRELIMINARY, NOT D12; NO F, T, OUTCOME OR PLACEHOLDER FILL')
    if k == 'replay': row.update(SM9LowerBoundOnly=False, lowerBoundEstablished=False, D1Label='synthetic SM-9 under D-1: workload source-count scenario, one fact, finding and fingerprint per counted source; no real-workload bound')
    if k == 'sm4': row.update(childEnvironmentNote='compiler children run with their constructed command environment (no inherited TMPDIR); the per-run TMPDIR is the parent runner\'s only; every run already writes a fresh output root; the reset contributes the state-absent check and the page-cache record')
    if k in ('sm5', 'sm7'): row.update(generatedLockSetsAreSizingStandIns=True)
    rows[k] = row
(W / 'cold-rust-interpretation.json').write_text(json.dumps(dict(standing='U-5b CURRENT INTERPRETATION OF THE COLD RUST-ROW SERIES', components=rows), indent=1) + '\n'); print('written')
