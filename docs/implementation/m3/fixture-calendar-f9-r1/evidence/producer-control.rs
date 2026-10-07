
#[test]
fn f9_future_calendar_preserves_real_producer_expiry_and_staleness_controls() {
    use RoleTarget::*;
    let seconds = crate::trust_time::timestamp_seconds("2028-10-02T00:00:00Z").unwrap();
    for carried in [
        [Trusted, Trusted, Trusted, Expired],
        [Expired; 4],
        [StaleRevocation; 4],
    ] {
        let mut spec = Spec::default();
        spec.roles[..4].copy_from_slice(&carried);
        let store = generate_at(&spec, seconds);
        assert!(store.produced, "calendar must preserve the real producer path");
        let roles = o(&o(&store.capsule)["roles"]);
        for (name, target) in ROLES.iter().zip(spec.roles) {
            assert_eq!(o(&roles[*name])["state"], s(target.token()));
        }
        let mut b = budget();
        super::super::current_record_bindings::bind(&mut b, &store.store, &store.capsule, &store.descriptor, &mut map_store(&store)).unwrap();
    }
}
