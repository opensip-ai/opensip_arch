from pathlib import Path
b=Path('/tmp/opensip-implementation/f9-authoring');p=b/'product/crates/security/src/trust/accepted_store_fixture_tests.rs'
s=Path('/Users/sb/code/opensip-ai/opensip/crates/security/src/trust/accepted_store_fixture_tests.rs').read_text()
s += r'''

// F9: moving the fixture basis leaves the fixed calendar control intact.
#[test]
fn f9_legacy_calendar_reproduces_every_retained_byte() {
    let seconds = crate::trust_time::timestamp_seconds("2026-10-02T00:00:00Z").unwrap();
    for spec in [Spec::default(), Spec { roles: all_targets(), state_schema: 2, ..Spec::default() }, Spec { roots: 4, ..Spec::default() }] {
        let fixed = generate(&spec);
        let explicit = generate_at(&spec, seconds);
        assert_eq!(fixed.produced, explicit.produced);
        assert_eq!(fixed.store, explicit.store);
        assert_eq!(fixed.capsule, explicit.capsule);
        assert_eq!(fixed.descriptor, explicit.descriptor);
        assert_eq!(fixed.p0_capsule, explicit.p0_capsule);
        assert_eq!(fixed.root, explicit.root);
        assert_eq!(fixed.root_body, explicit.root_body);
        assert_eq!(fixed.files.len(), explicit.files.len());
        for (a, b) in fixed.files.iter().zip(&explicit.files) {
            assert_eq!(a.path, b.path);
            assert_eq!(a.collection, b.collection);
            assert_eq!(a.bytes, b.bytes, "{}", a.path);
        }
    }
}

#[test]
fn f9_future_calendar_has_independent_golden_dates_and_bound_records() {
    let seconds = crate::trust_time::timestamp_seconds("2028-10-02T00:00:00Z").unwrap();
    let calendar = FixtureCalendar::at(seconds);
    assert_eq!(calendar.issued, "2028-10-01T00:00:00Z");
    assert_eq!(calendar.accepted, "2028-10-02T00:00:00Z");
    assert_eq!(calendar.root_expires, "2029-10-01T00:00:00Z");
    assert_eq!(calendar.catalog_expires, "2029-04-01T00:00:00Z");
    assert_eq!(calendar.expired, "2028-10-01T12:00:00Z");
    assert_eq!(calendar.stale, "2028-07-01T00:00:00Z");
    for spec in [Spec::default(), Spec { roles: all_targets(), state_schema: 2, ..Spec::default() }] {
        let store = generate_at(&spec, seconds);
        assert_eq!(o(&store.root)["expiresAt"], s("2029-10-01T00:00:00Z"));
        for file in &store.files {
            if file.collection.is_some() {
                assert!(file.path.ends_with(&digest_hex(&raw_sha256(&file.bytes))));
                assert_eq!(canonical_bytes(&opensip_identity::parse_json(&file.bytes).unwrap()).unwrap(), file.bytes);
            }
        }
        let mut b = budget();
        let bound = super::super::current_record_bindings::bind(&mut b, &store.store, &store.capsule, &store.descriptor, &mut map_store(&store)).unwrap();
        assert_eq!(bound.projection().capsule(), &store.capsule);
        let p0 = o(&store.p0_capsule);
        let mut b = budget();
        let evidence = super::super::publication_events::bind_events(&mut b, &store.descriptor, &p0["roles"], &p0["eventHead"], &mut map_store(&store)).unwrap();
        assert_eq!(evidence.roles(), &o(&store.capsule)["roles"]);
        let mut b = budget();
        let clock = super::super::admitted_trust_records::capsule_clock(&mut b, &store.capsule, &store.descriptor, None).unwrap();
        let head = super::super::ordinary_roots::bind_retained_head(&mut b, clock, &mut map_store(&store)).unwrap();
        assert_eq!(head.body(), store.root_body.as_slice());
        assert_eq!(head.root().value(), &store.root);
    }
}

#[test]
fn f9_future_calendar_preserves_chosen_role_states_and_explicit_issue_override() {
    let seconds = crate::trust_time::timestamp_seconds("2028-10-02T00:00:00Z").unwrap();
    let spec = Spec { roles: all_targets(), state_schema: 2, manifest_issued: Some("2028-10-03T00:00:00Z"), ..Spec::default() };
    let store = generate_at(&spec, seconds);
    let roles = o(&o(&store.capsule)["roles"]);
    for (name, target) in ROLES.iter().zip(spec.roles) {
        assert_eq!(o(&roles[*name])["state"], s(target.token()));
    }
    assert!(store.files.iter().any(|f| String::from_utf8_lossy(&f.bytes).contains("2028-10-03T00:00:00Z")));
    assert!(!store.files.iter().any(|f| String::from_utf8_lossy(&f.bytes).contains("2026-10-01T00:00:00Z")));
}
'''
s += (b/'producer-control.rs').read_text()
p.write_text(s);(b/p.name).write_text(s)
