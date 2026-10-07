from pathlib import Path
b=Path('/tmp/opensip-implementation/f9-authoring');c=b/'product';base=Path('/Users/sb/code/opensip-ai/opensip')
def edit(rel,fn):
 p=c/rel;p.write_text(fn((base/rel).read_text()))
# Existing fixture interfaces retain explicit None for scripted clocks.
def root(s):
 s=s.replace('        None,\n    )\n}\n/// Unit X4-F2', '        None,\n        None,\n    )\n}\n/// Unit X4-F2')
 s=s.replace('    manifest_issued: Option<&\'static str>,\n) -> &\'static str {','    manifest_issued: Option<&\'static str>,\n    accepted_seconds: Option<i64>,\n) -> &\'static str {')
 s=s.replace('use accepted_store_fixture::{CORE_CLOSURE, Spec, generate};','use accepted_store_fixture::{CORE_CLOSURE, Spec, generate, generate_at};')
 s=s.replace('    let generated = generate(&Spec {','    let spec = Spec {')
 s=s.replace('        ..Spec::default()\n    });','        ..Spec::default()\n    };\n    let generated = match accepted_seconds {\n        Some(seconds) => generate_at(&spec, seconds),\n        None => generate(&spec),\n    };')
 s=s.replace('    revocation_version: i128,\n) -> (Vec<(String, Vec<u8>)>,', '    revocation_version: i128,\n    accepted_seconds: Option<i64>,\n) -> (Vec<(String, Vec<u8>)>,')
 return s
edit('crates/security/src/trust/root_payload.rs',root)
def read(s):
 s=s.replace('            issued,\n        );','            issued,\n            None,\n        );')
 # Existing shared interfaces accept an explicit calendar choice. No clock read in X9 wrappers.
 s=s.replace('        revocation_version: i128,\n    ) -> Result<&\'static str, String>', '        revocation_version: i128,\n        accepted_seconds: Option<i64>,\n    ) -> Result<&\'static str, String>')
 s=s.replace('        revocation_version: i128,\n    ) -> Result<(i128, i128), FencedRefusal>', '        revocation_version: i128,\n        accepted_seconds: Option<i64>,\n    ) -> Result<(i128, i128), FencedRefusal>')
 s=s.replace('self.publish_trust_fenced(revocations, revocation_version)','self.publish_trust_fenced(revocations, revocation_version, None)')
 s=s.replace('            revocation_version,\n        );','            revocation_version,\n            accepted_seconds,\n        );')
 return s
edit('crates/security/src/custody/installation_read_fixture.rs',read)
for rel in ['crates/security/src/crash_matrix_sites.rs','crates/security/src/crash_matrix_census.rs']:
 edit(rel,lambda s:s.replace('install_accepted_trust(Vec::new(), 1)','install_accepted_trust(Vec::new(), 1, None)'))
edit('crates/security/src/crash_matrix_support.rs',lambda s:s.replace('.install_accepted_trust(revocations, revocation_version)', '.install_accepted_trust(revocations, revocation_version, None)').replace('.publish_trust_fenced(revocations, revocation_version)', '.publish_trust_fenced(revocations, revocation_version, None)'))
# Native scenario fixtures: read only SystemTime, never platform observe_clock/scripted_wall.
# This module is already restricted to scenario-fixtures, no new feature gate.
def scenario(s):
 s=s.replace('at.install_accepted_trust(Vec::new(), 1)', 'at.install_accepted_trust(Vec::new(), 1, Some(fixture_wall_seconds()))')
 s=s.replace('.publish_trust_fenced(revocations, next)', '.publish_trust_fenced(revocations, next, Some(fixture_wall_seconds()))')
 s += '''\n// F9: only native-clock scenarios choose this calendar. X9's shared callers\n// continue to pass None, preserving clockEpoch, point ordinals and readings.\nfn fixture_wall_seconds() -> i64 {\n    i64::try_from(std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).expect("fixture wall after epoch").as_secs()).expect("fixture wall fits timestamp")\n}\n'''
 return s
edit('crates/security/src/scenario.rs',scenario)
# Routing opens the session on a scripted monitor: preserve the fixed date.
edit('crates/security/src/custody/installation_routing_tests.rs',lambda s:s.replace('write_accepted_trust_issued(i, store, schema.get(), Vec::new(), 1, None)', 'write_accepted_trust_issued(i, store, schema.get(), Vec::new(), 1, None, None)'))
print('Explicit calendar threaded: native scenarios select their date, scripted routing/X9/default helpers preserve None.')
