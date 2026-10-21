from pathlib import Path
import os,json
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
p=Path('crates/host/Cargo.toml');s=p.read_text();needle='[dev-dependencies]\n';assert s.count(needle)==1;s=s.replace(needle,needle+'# D4-T3 runs compiled first-party peers under TestFixture, never Provider.\nopensip-platform = { path = "../platform", features = ["test-fixture"] }\n',1);p.write_text(s)
p=Path('crates/platform/src/process.rs');s=p.read_text();needle='''    pub fn recheck(&self) -> &ClosureRecheck {
        &self.recheck
    }
''';assert s.count(needle)==1;s=s.replace(needle,needle+'''
    /// Run an already checked launch as a first-party test binary (M3-D
    /// item 1; D4-T3). The caller must supply only compiled first-party
    /// fixture bytes. This consumes the verified carrier and changes its
    /// class alone: argv, scratch slot, descriptors, environment, executable
    /// and recheck stay identical. It neither rechecks nor constructs a new
    /// launch, and is absent from production's default/release API.
    #[cfg(all(debug_assertions, any(test, feature = "test-fixture")))]
    pub fn into_test_fixture(mut self) -> Self {
        self.spec.class = LaunchClass::TestFixture;
        self
    }
''',1);s=s.replace('/// only: the one item the `test-fixture` feature exposes (D3a-0).','/// only: exposed by the `test-fixture` feature (D3a-0).');p.write_text(s)
p=Path('crates/platform/src/process_tests.rs');s=p.read_text();s+='''
// D4-T3 needs the factory's exact checked closed spec, including its scratch
// slot, under item 1's TestFixture class. The conversion grants no new argv.
#[test]
#[cfg(debug_assertions)]
fn test_fixture_conversion_preserves_every_checked_launch_field() {
    let spec = LaunchSpec::rust(Path::new("/first-party/provider"), Path::new("/first-party/toolchain")).unwrap();
    let recheck = ClosureRecheck { member: "provider".into(), device: 17, inode: 19, sha256: "a".repeat(64) };
    let launch = VerifiedLaunch::from_recheck(spec, recheck);
    let mut expected = launch.clone();
    expected.spec.class = LaunchClass::TestFixture;
    let converted = launch.into_test_fixture();
    assert_eq!(converted, expected);
    assert_eq!(converted.spec().class(), LaunchClass::TestFixture);
}
''';p.write_text(s)
p=Path('crates/host/src/launch_recheck_tests.rs');s=p.read_text();needle='''            let mut supervision = Supervision::prepare(prepared.session, participant).unwrap();''';assert s.count(needle)==1;s=s.replace(needle,'''            let mut session = prepared.session;
            assert_eq!(session.launch.spec().class(), opensip_platform::LaunchClass::Provider);
            session.launch = session.launch.into_test_fixture();
            assert_eq!(session.launch.spec().class(), opensip_platform::LaunchClass::TestFixture);
            let mut supervision = Supervision::prepare(session, participant).unwrap();''',1);p.write_text(s)
f=Path(__file__).parent
for name in ['provider-spoken-r3','native-adapter-owning-r7','host-regressions-r2']:
 p=f/name/'report.json'
 if p.exists():
  raw=p.read_bytes();(p.parent/'report-before-class-correction.json').write_bytes(raw);j=json.loads(raw);j.update(runtimeAllPassed=j['allPassed'],allPassed=False,testLaunchClassConforming=False,standing='Runtime evidence retained, but provider-spoken cases used Provider rather than required TestFixture class. Not D4-T3 closure evidence. Successor uses exact verified carrier converted to TestFixture through a release-refused test-only API.');p.write_text(json.dumps(j,indent=2)+'\n')
print('Added release-refused TestFixture-only class conversion with exact full-carrier preservation control; corrected D4 peer launch class and prior evidence standing.')
