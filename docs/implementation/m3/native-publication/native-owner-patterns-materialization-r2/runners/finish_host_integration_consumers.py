"""Apply only after full-r2 terminal: two stale consumers and accepted CI pin."""
from pathlib import Path
import os,json,hashlib,subprocess
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;W=Path('/Users/sb/code/opensip-ai/opensip-native-owner-patterns-takeover');P=W.parent/'opensip'
report=json.loads((F/'full-r2/report.json').read_text())
assert report['selectedGenerationInputsStillExact']==352 and report['selectedGeneratedOutputsStillExact']==8
host=next(r for r in report['runs'] if r['name']=='owning-host')
assert set(host['failedTests'])=={'scenario_fixtures_stays_out_of_release_manifests','synthetic_b1_another_runs_replay_does_not_bind','synthetic_b8_an_altered_claimed_output_never_replays'}
for p,h in report['sourcePins'].items():assert hashlib.sha256((W/p).read_bytes()).hexdigest()==h
rel='crates/host/tests/admission_tests.rs';path=W/rel
before=path.read_bytes();assert before==(P/rel).read_bytes()
text=before.decode()
assert text.count('tests/fixtures/replay-fixtures.current.json')==2
text=text.replace('tests/fixtures/replay-fixtures.current.json','tests/fixtures/replay-fixtures.native-owner-r1.json')
old='manifests.push((path, matches!(name, "opensip-security" | "opensip-storage")));'
assert old in text
text=text.replace(old,'''// Accepted component-install plan r3 LD-CIP-3 also owns lifecycle's
        // never-default forwards; the same dependency/default pin applies.
        manifests.push((
            path,
            matches!(name, "opensip-security" | "opensip-storage" | "opensip-lifecycle"),
        ));''')
text=text.replace('[features] outside security and storage','[features] outside security, storage and lifecycle')
text=text.replace('/// in `[features]` of security and storage (never `default`) and in','/// in `[features]` of security, storage and lifecycle (never `default`) and in')
text=text.replace('/// by security and storage and enabled from storage\'s and host\'s\n/// `[dev-dependencies]`.','/// by security and storage. Accepted component-install plan r3 LD-CIP-3\n/// also permits lifecycle\'s never-default forwarding declarations. Enabling\n/// the fixture remains restricted to `[dev-dependencies]`.')
assert 'outside security and storage' not in text
path.write_text(text)
proof=dict(path=rel,beforeSha256=hashlib.sha256(before).hexdigest(),afterSha256=hashlib.sha256(path.read_bytes()).hexdigest(),fixtureReadChanges=1,fixtureDocumentationChanges=1,manifestGuardChange='Add only already-accepted lifecycle fixture feature declaration owner; default/dependency rejection paths and per-manifest feature_pin algorithm unchanged.',productionPathsChanged=False,unitAccepted=False)
(F/'host-integration-consumer-correction.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps(proof,indent=2))
