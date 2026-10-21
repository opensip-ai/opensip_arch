from pathlib import Path
import os,json,datetime
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;phase=json.loads((F/'r2-verification-process.json').read_text());assert phase['status']=='failed' and phase['completed'][-1]==dict(script='check_host_regressions_r6.py',exitCode=1)
p=Path('crates/host/tests/factory_fixture.rs');s=p.read_text();old='''        fs::write(&self.path, serde_json::to_vec(&self.value).unwrap()).unwrap();''';new='''        // The supervisor may terminate the child immediately after a
        // deliberate protocol fault. Never truncate the last observation:
        // publish only a whole replacement while holding the audit mutex.
        let pending = self.path.with_extension("pending");
        fs::write(&pending, serde_json::to_vec(&self.value).unwrap()).unwrap();
        fs::rename(&pending, &self.path).unwrap();''';assert s.count(old)==1;p.write_text(s.replace(old,new,1))
(F/'root-peer-audit-publication-finding-r1.json').write_text(json.dumps(dict(id='LEAD-D4F-R2-AUDIT-1',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),standing='Observed test-harness failure, preserved; proposed atomic-publication correction requires fresh evidence.',failedReport='host-regressions-r6/report.json',failure='Rust3 spawned-peer control parsed EOF from peer-observation.json after settlement. Concurrent audit persist used truncating fs::write and child can be killed mid-publication.',correction='Under the existing shared audit mutex, write a complete pending sibling and atomically rename over observation. Readers see a complete prior or new snapshot; no retry or reclassification of the failed run.',sourceOrFactorySemanticsChanged=False,firstPartyPeerChanged=True,originalFailurePreserved=True,productQualification=False),indent=2)+'\n')
print('Corrected atomic whole-file peer observation publication; original435pass/1fail run remains failed evidence.')
