from pathlib import Path
import hashlib
b=Path('/tmp/opensip-implementation/f9-authoring');p=b/'product/crates/security/src/trust/accepted_store_fixture.rs';s=Path('/Users/sb/code/opensip-ai/opensip/crates/security/src/trust/accepted_store_fixture.rs').read_text();assert hashlib.sha256(s.encode()).hexdigest() == '2de46d7b855141872fc7d73df66a97a07aacb0b4f8210ae652c179f84e73f15f';assert 'struct FixtureCalendar' not in s
new='''// F9: explicit owned test dates. These reproduce the legacy calendar's
// relative offsets; they do not change production trust/freshness policy.
struct FixtureCalendar {
    issued: String,
    accepted: String,
    root_expires: String,
    catalog_expires: String,
    expired: String,
    stale: String,
}
impl FixtureCalendar {
    fn at(accepted_seconds: i64) -> Self {
        let issued = accepted_seconds.checked_sub(86_400).expect("fixture issue time");
        let format = |seconds| crate::trust_time::format_timestamp(seconds).expect("fixture calendar");
        Self {
            issued: format(issued),
            accepted: format(accepted_seconds),
            root_expires: format(issued.checked_add(365 * 86_400).expect("fixture root horizon")),
            catalog_expires: format(issued.checked_add(182 * 86_400).expect("fixture catalog horizon")),
            expired: format(issued.checked_add(43_200).expect("fixture expired time")),
            stale: format(issued.checked_sub(92 * 86_400).expect("fixture stale time")),
        }
    }
}

/// F9 test-only signed store for an explicit clock instant, not a production
/// issuer or trusted clock constructor. Caller chooses native or scripted time.
/// Every dated source document is signed before retained records are computed.
pub(crate) fn generate_at(spec: &Spec, accepted_seconds: i64) -> AcceptedStore {
    let calendar = FixtureCalendar::at(accepted_seconds);
    generate_with_calendar(spec, Some(&calendar))
}

'''
s=s.replace('pub(crate) fn generate(spec: &Spec) -> AcceptedStore {','pub(crate) fn generate(spec: &Spec) -> AcceptedStore {\n    generate_with_calendar(spec, None)\n}\n\n'+new+'fn generate_with_calendar(spec: &Spec, calendar: Option<&FixtureCalendar>) -> AcceptedStore {')
s=s.replace('produce(spec)', 'produce(spec, calendar)').replace('construct(spec)\n','construct(spec, calendar)\n')
s=s.replace('fn p0_publication(spec: &Spec, sid: &str) -> P0 {','fn p0_publication(spec: &Spec, sid: &str, calendar: Option<&FixtureCalendar>) -> P0 {').replace('wall: "2026-10-01T00:00:00Z",','wall: calendar.map(|c| c.issued.as_str()).unwrap_or(ISSUED),')
s=s.replace('fn signed_chain(spec: &Spec, final_expires: Option<&str>)','fn signed_chain(spec: &Spec, final_expires: Option<&str>, calendar: Option<&FixtureCalendar>)').replace('    let first = quorum_root(1);','    let mut first = quorum_root(1);\n    if let Some(c) = calendar {\n        let V::Object(root) = &mut first else { panic!("public fixture root"); };\n        root.insert("issuedAt".into(), s(&c.issued));\n        root.insert("expiresAt".into(), s(&c.root_expires));\n    }')
s=s.replace('fn construct(spec: &Spec) -> AcceptedStore {','fn construct(spec: &Spec, calendar: Option<&FixtureCalendar>) -> AcceptedStore {\n    let issued = calendar.map(|c| c.issued.as_str()).unwrap_or(ISSUED);\n    let accepted = calendar.map(|c| c.accepted.as_str()).unwrap_or(ACCEPTED);')
s=s.replace('p0_publication(spec, &sid)', 'p0_publication(spec, &sid, calendar)').replace('signed_chain(spec, spec.root_expires)','signed_chain(spec, spec.root_expires, calendar)')
s=s.replace('spec.catalog_expires.unwrap_or(CATALOG_EXPIRES)','spec.catalog_expires.unwrap_or_else(|| calendar.map(|c| c.catalog_expires.as_str()).unwrap_or(CATALOG_EXPIRES))')
s=s.replace('spec.manifest_issued.unwrap_or(ISSUED)','spec.manifest_issued.unwrap_or(issued)').replace('manifest_issued.max(ACCEPTED)','manifest_issued.max(accepted)')
# Only document literal timestamps, not the preserved legacy constants/comments.
s=s.replace('"revokedAt":"2026-10-01T00:00:00Z"','"revokedAt":"{issued}"').replace('"issuedAt":"2026-10-01T00:00:00Z"','"issuedAt":"{issued}"').replace('s("2026-10-01T00:00:00Z")','s(issued)')
s=s.replace('let anchor = anchor();','let anchor = anchor(calendar);').replace('fn anchor() -> V {','fn anchor(calendar: Option<&FixtureCalendar>) -> V {').replace('s("2026-10-02T00:00:00Z")','s(calendar.map(|c| c.accepted.as_str()).unwrap_or(ACCEPTED))').replace('&anchor(),','&anchor(calendar),')
s=s.replace('fn produce(spec: &Spec) -> Option<AcceptedStore> {','fn produce(spec: &Spec, calendar: Option<&FixtureCalendar>) -> Option<AcceptedStore> {\n    let normal_issued = calendar.map(|c| c.issued.as_str()).unwrap_or(ISSUED);')
s=s.replace('knobs.root_expired.then_some(EXPIRED).or(spec.root_expires),','knobs.root_expired.then_some(calendar.map(|c| c.expired.as_str()).unwrap_or(EXPIRED)).or(spec.root_expires),\n        calendar,')
s=s.replace('        "2026-07-01T00:00:00Z"\n    } else {\n        "2026-10-01T00:00:00Z"','        calendar.map(|c| c.stale.as_str()).unwrap_or("2026-07-01T00:00:00Z")\n    } else {\n        normal_issued')
# Catalog/payload issue remains normal even when revocation intentionally stale.
prod=s.index('fn produce(spec:');s=s[:prod]+s[prod:].replace('"issuedAt":"{issued}","releases"','"issuedAt":"{normal_issued}","releases"').replace('spec.manifest_issued.unwrap_or(issued)','spec.manifest_issued.unwrap_or(normal_issued)')
s=s.replace('            EXPIRED\n        } else {','            calendar.map(|c| c.expired.as_str()).unwrap_or(EXPIRED)\n        } else {')
p.write_text(s);(b/'accepted_store_fixture.rs').write_text(s)
print('Explicit calendar authored in isolated snapshot; caller wiring and controls still required.')
