from pathlib import Path
import json,hashlib,subprocess
F=Path(__file__).parent;W=Path('/Users/sb/code/opensip-ai/opensip-security-baseline-takeover');A=W.parent/'opensip_arch';P=W.parent/'opensip'
def pin(root,p):b=(root/p).read_bytes();return dict(path=p,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
oldpath='crates/security/tests/fixtures/journal-seal-cases.json';hostold='crates/host/tests/fixtures/replay-fixtures.json';hostnew='crates/host/tests/fixtures/replay-fixtures.current.json';newpath='crates/security/tests/fixtures/journal-seal-replay.current.json';old=json.loads((W/oldpath).read_text());base=json.loads((W/hostold).read_text());current=json.loads((W/hostnew).read_text());label=old['replay']['case']['label'];a=next(x for x in base['cases'] if x['label']==label);b=next(x for x in current['cases'] if x['label']==label);assert a==old['replay']['case'];assert all(old['replay']['objectPool'][k]==base['objectPool'][k] for k in a['objects']);assert all(old['replay']['blobPool'][k]==base['blobPool'][k] for k in a['blobs']);assert b['expected']['value']['result']=='ADMIT'
fixture=dict(case=b,objectPool={k:current['objectPool'][k] for k in b['objects']},blobPool={k:current['blobPool'][k] for k in b['blobs']});assert not (W/newpath).exists();(W/newpath).write_text(json.dumps(fixture,sort_keys=True,ensure_ascii=False,indent=2)+'\n')
p=W/'crates/security/src/journal_store.rs';s=p.read_text();oldcode='''        let f = fixture();
        let f = object(&object(&f).unwrap()["replay"]).unwrap();''';newcode='''        // The historical journal cases remain immutable. Replay the exact
        // corresponding current-schema companion, as the host replay owner
        // already does, rather than reinterpreting historical schema bytes.
        let current = opensip_identity::parse_json(include_bytes!(
            "../tests/fixtures/journal-seal-replay.current.json"
        ))
        .unwrap();
        let f = object(&current).unwrap();''';assert s.count(oldcode)==1;p.write_text(s.replace(oldcode,newcode))
p=W/'crates/security/src/custody/commit_session_tests.rs';s=p.read_text();oldcode='''    // Every other `.settle(` is the ordinary writer's own gate helper.
    let mut settle = count(".settle(");
    settle.remove("security/src/initial_installation.rs");
    assert_eq!(
        settle.keys().collect::<Vec<_>>(),
        ["security/src/custody/ordinary_writer.rs"]
    );''';newcode='''    // Other owners have private state-machine helpers named `settle`.
    // Admit only their exact existing `self.settle` call counts and private
    // signatures, never a whole-file exemption for a ledger call.
    let mut settle = count(".settle(");
    settle.remove("security/src/initial_installation.rs");
    for (file, signature, calls) in [
        (
            "components/src/supervisor.rs",
            "    fn settle(&mut self) {",
            3,
        ),
        (
            "host/src/archive_decoder/tar.rs",
            "    fn settle(&mut self) -> Result<(), DecodeError<C::Error>> {",
            2,
        ),
    ] {
        let source = fs::read_to_string(root.join(file)).unwrap();
        assert!(source.contains(signature), "{file}: private helper changed");
        let own_calls = source
            .lines()
            .filter(|line| !line.trim_start().starts_with("//"))
            .map(|line| line.matches("self.settle(").count())
            .sum::<usize>();
        assert_eq!(own_calls, calls, "{file}: private helper caller count");
        assert_eq!(settle.remove(file), Some(calls), "{file}: unexpected ledger or other settle call");
    }
    assert_eq!(settle, BTreeMap::from([("security/src/custody/ordinary_writer.rs".to_owned(), 9)]));''';assert s.count(oldcode)==1;p.write_text(s.replace(oldcode,newcode))
assert (W/oldpath).read_bytes()==(P/oldpath).read_bytes();assert (W/hostnew).read_bytes()==(P/hostnew).read_bytes();report=dict(standing='UNACCEPTED TEST-ONLY BASELINE REPAIR; NO CHECKS OR ACCEPTANCE YET',worktree=str(W),productBase=subprocess.check_output(['/usr/bin/git','rev-parse','HEAD'],cwd=W,text=True).strip(),architectureBase=subprocess.check_output(['/usr/bin/git','rev-parse','HEAD'],cwd=A,text=True).strip(),historicalJournalFixture=pin(W,oldpath),historicalHostFixture=pin(W,hostold),acceptedCurrentHostFixture=pin(W,hostnew),newCompanion=pin(W,newpath),logicalCase=label,currentRunId=b['runId'],objectCount=len(b['objects']),blobCount=len(b['blobs']),exactCurrentHostSubset=True,productionBehaviorChanged=False,privateCensusRun=False,unitAccepted=False,integrated=False,qualification=False);(F/'PREPARATION.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
