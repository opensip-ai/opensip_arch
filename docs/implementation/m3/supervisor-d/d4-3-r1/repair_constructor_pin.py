from pathlib import Path
import hashlib,json,sys
F=Path(__file__).parent;W=Path('/Users/sb/code/opensip-ai/opensip-d4-3-takeover');p=W/'crates/host/src/invocation_tests.rs';s=p.read_text();sha=hashlib.sha256((W/'crates/host/src/invocation.rs').read_bytes()).digest();needle='''    let source = include_str!("invocation.rs");''';assert s.count(needle)==1
insert='''    let source = include_str!("invocation.rs");
    // The closed module has one reviewed construction path. A source hash
    // pins that complete constructor inventory, including Self expressions,
    // aliases and whitespace/comment variants a spelling count cannot see.
    // Any edit requires item25 review and a deliberate replacement of this
    // hash; it is not a claim to parse arbitrary future Rust constructors.
    assert_eq!(
        opensip_identity::raw_sha256(source.as_bytes()),
        ['''+', '.join(str(b) for b in sha)+'''],
        "the reviewed admission constructor inventory changed; re-review item25 before updating the pin"
    );
    let implementation = source.split("impl AdmittedRequest {").nth(1).unwrap()
        .split("/// M3-D r5 item 25").next().unwrap();
    assert_eq!(implementation.matches("Self {").count(), 1,
        "each fresh construction must classify before any handover");'''
s=s.replace(needle,insert);destination=(F/'repaired-invocation_tests.rs') if '--stage-only' in sys.argv else p;destination.write_text(s)
(F/'constructor-pin-repair.json').write_text(json.dumps(dict(sourceSha256=sha.hex(),standing='UNREVIEWED TEST-ONLY RF-1 REPAIR',finding='D4-3-PRE-R1-RF-1',method='Pin complete reviewed production module bytes plus the one Self construction and ordered admission/classification/handover; future source changes require item25 review, not general Rust constructor parsing',productionSourceChanged=False),indent=2)+'\n')
