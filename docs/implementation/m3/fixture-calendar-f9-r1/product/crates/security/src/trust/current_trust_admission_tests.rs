use super::*;
use super::super::super::accepted_store_fixture::{self as fixture, RoleTarget, Spec};
use super::super::M::Collection;

fn reader(
    store: &fixture::AcceptedStore,
    drop: Option<[u8; 32]>,
) -> impl FnMut(Collection, [u8; 32], usize) -> Result<Vec<u8>, ()> + '_ {
    move |c, h, cap| {
        if Some(h) == drop {
            return Err(());
        }
        let raw = store.lookup(c, h).ok_or(())?;
        if raw.len() > cap {
            return Err(());
        }
        Ok(raw)
    }
}
fn observation_on(boot: &str, mono: i64, wall: &str) -> V {
    opensip_identity::parse_json(
        format!(r#"{{"bootId":"{boot}","mono":{mono},"wall":"{wall}"}}"#).as_bytes(),
    )
    .unwrap()
}
fn observation(mono: i64, wall: &str) -> V {
    observation_on("boot-1", mono, wall)
}
fn hour_later() -> V {
    observation(3607, "2026-10-02T01:00:00Z")
}
fn fenced(report: bool, obs: &V) -> ViewInputs<'_> {
    ViewInputs {
        mode: ReadMode::Fenced { report },
        observation: Some(obs),
        project_policy: None,
        core_closure: fixture::CORE_CLOSURE,
    }
}
fn utc(text: &str) -> i64 {
    crate::trust_time::timestamp_seconds(text).unwrap()
}
/// A reread at `at` (law X4T r11 item 6's instant, unit X4-F1).
fn reread_at(at: i64) -> ViewInputs<'static> {
    ViewInputs {
        mode: ReadMode::Reread { at },
        observation: None,
        project_policy: None,
        core_closure: fixture::CORE_CLOSURE,
    }
}
/// A reread at `hour_later`'s tEval, before any expiry.
fn reread() -> ViewInputs<'static> {
    reread_at(utc("2026-10-02T01:00:00Z"))
}
fn with_roles(core: RoleTarget, index: RoleTarget, component: RoleTarget) -> Spec {
    let mut spec = Spec::default();
    // ROLES order: BUNDLE, COMPONENT, CORE, INDEX, PROFILE, REPAIR.
    spec.roles[1] = component;
    spec.roles[2] = core;
    spec.roles[3] = index;
    spec
}
fn admit_store(
    store: &fixture::AcceptedStore,
    inputs: &ViewInputs<'_>,
) -> Result<AdmittedCurrentTrust, TrustRefusal> {
    let mut b = view_budget();
    admit_current_trust(&mut b, &store.store, &store.capsule, inputs, &mut reader(store, None))
}
fn admit(spec: &Spec, inputs: &ViewInputs<'_>) -> Result<AdmittedCurrentTrust, TrustRefusal> {
    admit_store(&fixture::generate(spec), inputs)
}
fn empty_policy_digest() -> [u8; 32] {
    let mut b = view_budget();
    policy::merge(&mut b, Source::Missing, Context::Global)
        .unwrap()
        .digest()
}
fn hash_of(v: &V) -> [u8; 32] {
    let V::String(h) = &object(v).unwrap()["sha256"] else {
        panic!("sha256")
    };
    super::super::super::decode_hex32(h).unwrap()
}

#[test]
fn an_accepted_store_is_admitted_with_its_epoch_and_standing() {
    for schema in [1, 2] {
        let obs = hour_later();
        let spec = Spec {
            state_schema: schema,
            ..Spec::default()
        };
        let view = admit(&spec, &fenced(false, &obs)).unwrap();
        assert_eq!(view.standing(), TrustStanding::InstallGateRequiredForNewProcess);
        assert_eq!(
            view.epoch(),
            &TrustEpoch {
                root_version: 1,
                index_snapshot_version: 1,
                revocation_version: 1,
                permission_policy_digest: empty_policy_digest(),
            }
        );
        assert!(view.revoked_subjects().is_empty());
        assert_eq!(view.role_states()[2], ("TR-CORE", "trusted"));
    }
}

#[test]
fn a_creator_only_installation_is_f_absent() {
    let store = fixture::generate(&Spec::default());
    let obs = hour_later();
    let mut b = view_budget();
    let refusal = admit_current_trust(
        &mut b,
        &store.store,
        &store.p0_capsule,
        &fenced(false, &obs),
        &mut reader(&store, None),
    )
    .unwrap_err();
    assert_eq!(refusal.row, TrustRow::NoAdmittedTimeContext);
    assert_eq!(refusal.row.code(), "TRUST.NO_ADMITTED_TIME_CONTEXT");
    assert_eq!(b.counters(), (0, 0, 0), "refused before any read");
}

fn with_field(capsule: &V, key: &str, value: V) -> V {
    let mut c = object(capsule).unwrap().clone();
    c.insert(key.into(), value);
    V::Object(c)
}

#[test]
fn only_the_p0_shape_is_f_absent() {
    let store = fixture::generate(&Spec::default());
    let obs = hour_later();
    let p0 = &store.p0_capsule;
    // A P0 capsule with one accepted role.
    let roles = object(&object(&store.capsule).unwrap()["roles"]).unwrap();
    let mut p0_roles = object(&object(p0).unwrap()["roles"]).unwrap().clone();
    p0_roles.insert("TR-CORE".into(), roles["TR-CORE"].clone());
    for (label, capsule) in [
        ("retained, history null", with_field(&store.capsule, "history", V::Null)),
        ("retained, heads null", with_field(&store.capsule, "heads", V::Null)),
        ("pre-acceptance with history", with_field(p0, "history", object(&store.capsule).unwrap()["history"].clone())),
        ("pre-acceptance, accepted role", with_field(p0, "roles", V::Object(p0_roles.clone()))),
    ] {
        let mut b = view_budget();
        let refusal = admit_current_trust(
            &mut b,
            &store.store,
            &capsule,
            &fenced(false, &obs),
            &mut reader(&store, None),
        )
        .unwrap_err();
        assert_eq!(refusal.row, TrustRow::Incomplete, "{label}: {}", refusal.cause);
        assert_eq!(b.counters(), (0, 0, 0), "{label}: refused before any read");
    }
}

#[test]
fn recovery_goes_through_the_role_machine_join() {
    use State::*;
    // ROLES order: BUNDLE, COMPONENT, CORE, INDEX, PROFILE, REPAIR.
    let roles = |bundle, component, core, index| {
        [bundle, component, core, index, Trusted, Unbootstrapped].map(|s| (s, s != Unbootstrapped))
    };
    for (states, subject) in [
        (roles(Trusted, Trusted, Recovery, Trusted), "core:recovery"),
        (roles(Trusted, Trusted, Trusted, Recovery), "index:recovery"),
        (roles(Trusted, Recovery, Trusted, Trusted), "component:recovery"),
    ] {
        let refusal = standing_of(&states).unwrap_err();
        assert_eq!(refusal.row, TrustRow::Continuation(subject.into()));
        assert_eq!(refusal.row.code(), "CONTINUE-CORE-NOT-TRUSTED");
    }
    // A bundle, profile or repair outside the join does not decide it.
    let mut states = roles(Recovery, Trusted, Trusted, Trusted);
    states[4] = (Recovery, true);
    states[5] = (Recovery, true);
    assert_eq!(
        standing_of(&states).unwrap(),
        TrustStanding::InstallGateRequiredForNewProcess
    );
    let states = roles(Recovery, Trusted, Trusted, Expired);
    assert_eq!(standing_of(&states).unwrap(), TrustStanding::ExistingOnly);
}

#[test]
fn each_continuation_refusal_names_its_role_and_state() {
    use RoleTarget::*;
    let obs = hour_later();
    for (spec, subject) in [
        (with_roles(Revoked, Trusted, Trusted), "core:revoked"),
        (with_roles(QuorumLost, Trusted, Trusted), "core:quorum-lost"),
        (with_roles(Expired, Trusted, Trusted), "core:expired"),
        (with_roles(Trusted, QuorumLost, Trusted), "index:quorum-lost"),
        (with_roles(Trusted, Revoked, Trusted), "index:revoked"),
        (with_roles(Trusted, Unbootstrapped, Trusted), "index:unbootstrapped"),
        (with_roles(Trusted, Trusted, Unbootstrapped), "component:unbootstrapped"),
        (with_roles(Trusted, Trusted, StaleRevocation), "component:stale-revocation"),
    ] {
        let refusal = admit(&spec, &fenced(false, &obs)).unwrap_err();
        assert_eq!(refusal.row, TrustRow::Continuation(subject.into()), "{subject}");
        // The interim lead decision: one registered detail, the role in the subject.
        assert_eq!(refusal.row.code(), "CONTINUE-CORE-NOT-TRUSTED");
        assert_eq!(refusal.row.subject().as_deref(), Some(subject));
    }
}

#[test]
fn an_expired_or_stale_index_is_admitted_as_existing_only() {
    use RoleTarget::*;
    let obs = hour_later();
    for index in [Expired, StaleRevocation] {
        let view = admit(&with_roles(Trusted, index, Trusted), &fenced(false, &obs)).unwrap();
        assert_eq!(view.standing(), TrustStanding::ExistingOnly, "{index:?}");
    }
}

#[test]
fn time_is_admitted_on_the_fenced_read_only() {
    let obs = hour_later();
    // Fenced, not report-only: the floor write-ahead is proposed (X4T-b performs it).
    let view = admit(&Spec::default(), &fenced(false, &obs)).unwrap();
    let time = view.time().unwrap();
    assert_eq!(time.refusal, None);
    assert!(!time.report_only);
    assert_eq!(time.floor_write, time.evaluation);
    assert!(time.floor_write.is_some());
    // Report-only (read sessions, doctor): nothing is proposed for writing.
    let view = admit(&Spec::default(), &fenced(true, &obs)).unwrap();
    let time = view.time().unwrap();
    assert!(time.report_only);
    assert_eq!((time.floor_write, time.last_write, time.anchor_write), (None, None, false));
    // A reread never re-admits time.
    let view = admit(&Spec::default(), &reread()).unwrap();
    assert!(view.time().is_none());
}

#[test]
fn time_refusals_take_their_rows() {
    for (obs, row) in [
        // A payload issued after the wall clock plus a day.
        (
            observation(3607, "2026-09-01T00:00:00Z"),
            TrustRow::PayloadNotAdmissible("time"),
        ),
        // Another boot, the wall beyond the last accepted time plus 90 days.
        (
            observation_on("boot-2", 9, "2027-02-01T00:00:00Z"),
            TrustRow::ClockExcursion("beyond-horizon"),
        ),
        // Same boot: three days of wall for one hour of monotonic time.
        (
            observation(3607, "2026-10-05T00:00:00Z"),
            TrustRow::ClockExcursion("in-session"),
        ),
    ] {
        let refusal = admit(&Spec::default(), &fenced(false, &obs)).unwrap_err();
        assert_eq!(refusal.row, row, "{}", refusal.cause);
    }
    // The observation is required on a fenced read.
    let later = hour_later();
    let inputs = ViewInputs {
        observation: None,
        ..fenced(false, &later)
    };
    assert_eq!(admit(&Spec::default(), &inputs).unwrap_err().row, TrustRow::HostIo);
}

/// Item 6 (unit X4-F1): a reread evaluates S4's expiry and staleness at its
/// instant and applies them to the stored roles through EV-CLOCK. The default
/// store's list was issued 2026-10-01, so it is stale strictly after
/// 2026-12-30T00:00:00Z; its signing root expires at 2027-10-01T00:00:00Z.
#[test]
fn a_reread_fails_closed_once_its_instant_passes_an_expiry() {
    let stale = utc("2026-12-30T00:00:00Z");
    let expires = utc("2027-10-01T00:00:00Z");
    // Before: admitted on the stored states, and still no time admitted.
    for at in [utc("2026-10-02T01:00:00Z"), stale] {
        let view = admit(&Spec::default(), &reread_at(at)).unwrap();
        assert_eq!(
            view.standing(),
            TrustStanding::InstallGateRequiredForNewProcess,
            "{at}"
        );
        assert_eq!(view.role_states()[2], ("TR-CORE", "trusted"), "{at}");
        assert!(view.time().is_none() && view.handoff_clock().is_none());
    }
    // After: the continuation row, naming the role and its clocked state. A
    // reread's refusal is X4's callback error (item 9).
    for (at, subject) in [
        (stale + 1, "core:stale-revocation"),
        (expires - 1, "core:stale-revocation"),
        // EV-CLOCK: expiry wins over staleness.
        (expires, "core:expired"),
    ] {
        let refusal = admit(&Spec::default(), &reread_at(at)).unwrap_err();
        assert_eq!(
            refusal.row,
            TrustRow::Continuation(subject.into()),
            "{at}: {}",
            refusal.cause
        );
        assert_eq!(refusal.row.code(), "CONTINUE-CORE-NOT-TRUSTED");
    }
}

/// Item 6 (unit X4-F1): a fenced read keeps its clock. A reread's instant is
/// its tEval advanced by the monotonic seconds elapsed on the same boot,
/// whatever the reread's own wall clock says.
#[test]
fn the_handoff_clock_advances_by_monotonic_time_only() {
    let obs = hour_later();
    let view = admit(&Spec::default(), &fenced(false, &obs)).unwrap();
    let t_eval = view.time().unwrap().evaluation.unwrap();
    assert_eq!(t_eval, utc("2026-10-02T01:00:00Z"));
    let clock = view.handoff_clock().unwrap();
    assert_eq!(clock.advanced(&obs), Ok(t_eval));
    // The wall clock is never consulted: behind the handoff's, or ahead of
    // it, the instant is the same.
    for wall in [
        "2020-01-01T00:00:00Z",
        "2026-10-02T01:00:10Z",
        "2029-01-01T00:00:00Z",
    ] {
        assert_eq!(clock.advanced(&observation(3617, wall)), Ok(t_eval + 10), "{wall}");
    }
    // A monotonic reading below the handoff's, another boot, or no
    // observation at all has no instant.
    assert_eq!(
        clock.advanced(&observation(3606, "2026-10-02T02:00:00Z")),
        Err("monotonic")
    );
    assert_eq!(
        clock.advanced(&observation_on("boot-2", 3617, "2026-10-02T01:00:10Z")),
        Err("boot")
    );
    assert_eq!(clock.advanced(&V::Null), Err("observation"));
    // A report-only read keeps its clock too; a reread has none.
    let report = admit(&Spec::default(), &fenced(true, &obs)).unwrap();
    assert_eq!(report.handoff_clock(), Some(clock));
    assert!(admit(&Spec::default(), &reread()).unwrap().handoff_clock().is_none());
}

/// Item 6 (unit X4-F1): the reread's EV-CLOCK follows law X4B r5 item 4's
/// mapping, and the role machine's join decides. A catalog expired alone
/// leaves TR-INDEX `Expired` and the view `ExistingOnly`, which admits
/// continuing work; TR-PROFILE and TR-REPAIR keep their stored states.
#[test]
fn a_rereads_clock_follows_x4b_item_4_and_the_role_machine() {
    use State::*;
    // ROLES order: BUNDLE, COMPONENT, CORE, INDEX, PROFILE, REPAIR.
    let stored = [Trusted, Trusted, Trusted, Trusted, Unbootstrapped, Trusted]
        .map(|s| (s, s != Unbootstrapped));
    let states = |roles: [(State, bool); 6]| roles.map(|(s, _)| s);
    assert_eq!(clock_roles(stored, (false, false, false)), stored);
    let catalog = clock_roles(stored, (false, true, false));
    assert_eq!(
        states(catalog),
        [Trusted, Trusted, Trusted, Expired, Unbootstrapped, Trusted]
    );
    assert_eq!(standing_of(&catalog).unwrap(), TrustStanding::ExistingOnly);
    let root = clock_roles(stored, (true, false, false));
    assert_eq!(
        states(root),
        [Expired, Expired, Expired, Expired, Unbootstrapped, Trusted]
    );
    assert_eq!(
        standing_of(&root).unwrap_err().row,
        TrustRow::Continuation("core:expired".into())
    );
    let stale = clock_roles(stored, (false, false, true));
    assert_eq!(
        states(stale),
        [
            StaleRevocation,
            StaleRevocation,
            StaleRevocation,
            StaleRevocation,
            Unbootstrapped,
            Trusted
        ]
    );
    assert_eq!(
        standing_of(&stale).unwrap_err().row,
        TrustRow::Continuation("core:stale-revocation".into())
    );
    // Expiry wins over staleness, from either state.
    assert_eq!(states(clock_roles(stored, (true, false, true)))[2], Expired);
    assert_eq!(states(clock_roles(stale, (true, false, true)))[2], Expired);
    // States EV-CLOCK never moves (it never preempts Recovery).
    for state in [Recovery, Revoked, QuorumLost, Unbootstrapped, Expired] {
        let roles = [(state, true); 6];
        assert_eq!(clock_roles(roles, (true, true, true)), roles, "{state:?}");
    }
}

// Law X4T r12 item 6 (unit X4-F2): expiry at the fenced read. X4T-0's
// default store cannot reach one there: its L is the list's issue time,
// 2026-10-01, so S4's plausibility bound stops W at the list's staleness.
// These stores use item 13's knobs. The acceptance's wall is 2026-10-02.

/// The bootstrap manifest's later issue time. The acceptance admits it (not
/// beyond its wall plus 24 h), so the store's L is 2026-10-03 and S4's
/// plausibility bound reaches 2027-01-01T00:00:00Z, past the list's
/// staleness, which is strictly after 2026-12-30T00:00:00Z.
const LATER: &str = "2026-10-03T00:00:00Z";
const STALE_AFTER: &str = "2026-12-30T00:00:00Z";
/// A fenced read's S4 observation on another boot than the acceptance's
/// anchor, so no continuity applies: tEval = max(F, W, A) = W here.
fn fenced_at(wall: &str) -> V {
    observation_on("boot-2", 9, wall)
}
/// A store through X4B's producer (on macOS), with the knobs given.
fn knobbed(
    manifest_issued: Option<&'static str>,
    root_expires: Option<&'static str>,
    catalog_expires: Option<&'static str>,
) -> fixture::AcceptedStore {
    let store = fixture::generate(&Spec {
        manifest_issued,
        root_expires,
        catalog_expires,
        ..Spec::default()
    });
    assert_eq!(store.produced, cfg!(target_os = "macos"));
    store
}
fn tokens(roles: [(State, bool); 6]) -> [(&'static str, &'static str); 6] {
    std::array::from_fn(|i| (ROLES[i], token(roles[i].0)))
}
fn carried_trusted(view: &AdmittedCurrentTrust) {
    for (role, state) in &view.role_states()[..4] {
        assert_eq!(*state, "trusted", "{role}");
    }
}

#[test]
fn a_fenced_read_refuses_a_list_already_stale_at_its_t_eval() {
    let store = knobbed(Some(LATER), None, None);
    // Exactly the list's issue time plus 90 days: S4's strict `>`.
    let obs = fenced_at(STALE_AFTER);
    let view = admit_store(&store, &fenced(false, &obs)).unwrap();
    assert_eq!(view.standing(), TrustStanding::InstallGateRequiredForNewProcess);
    carried_trusted(&view);
    let time = view.time().unwrap();
    assert_eq!(time.evaluation, Some(utc(STALE_AFTER)));
    assert_eq!(time.expired, Some((false, false, false)));
    // One second later, still inside the plausibility bound: the continuation
    // row, at the lease-free point (item 10).
    let obs = fenced_at("2026-12-30T00:00:01Z");
    let refusal = admit_store(&store, &fenced(false, &obs)).unwrap_err();
    assert_eq!(
        refusal.row,
        TrustRow::Continuation("core:stale-revocation".into()),
        "{}",
        refusal.cause
    );
    assert_eq!(refusal.row.code(), "CONTINUE-CORE-NOT-TRUSTED");
    assert_eq!(refusal.row.subject().as_deref(), Some("core:stale-revocation"));
}

#[test]
fn a_fenced_read_refuses_a_root_already_expired_at_its_t_eval() {
    // The signing root expires 2026-11-01, inside the default store's window.
    let store = knobbed(None, Some("2026-11-01T00:00:00Z"), None);
    let obs = fenced_at("2026-10-31T23:59:59Z");
    let view = admit_store(&store, &fenced(false, &obs)).unwrap();
    assert_eq!(view.standing(), TrustStanding::InstallGateRequiredForNewProcess);
    carried_trusted(&view);
    // At `expiresAt` (S4's `>=`): the continuation row, never S5's
    // `ROOT.FINAL_EXPIRED` (item 10, r12).
    let obs = fenced_at("2026-11-01T00:00:00Z");
    let refusal = admit_store(&store, &fenced(false, &obs)).unwrap_err();
    assert_eq!(refusal.row, TrustRow::Continuation("core:expired".into()), "{}", refusal.cause);
    assert_eq!(refusal.row.code(), "CONTINUE-CORE-NOT-TRUSTED");
    // Both states true: expiry wins, as `decide` orders them.
    let store = knobbed(Some(LATER), Some("2026-12-31T00:00:00Z"), None);
    for (wall, subject) in [
        ("2026-12-30T00:00:01Z", "core:stale-revocation"),
        ("2026-12-31T00:00:00Z", "core:expired"),
    ] {
        let obs = fenced_at(wall);
        let refusal = admit_store(&store, &fenced(false, &obs)).unwrap_err();
        assert_eq!(refusal.row, TrustRow::Continuation(subject.into()), "{wall}");
    }
}

#[test]
fn a_catalog_expired_alone_at_the_fenced_read_is_admitted_existing_only() {
    let store = knobbed(None, None, Some("2026-11-01T00:00:00Z"));
    let obs = fenced_at("2026-10-31T23:59:59Z");
    let view = admit_store(&store, &fenced(false, &obs)).unwrap();
    assert_eq!(view.standing(), TrustStanding::InstallGateRequiredForNewProcess);
    let obs = fenced_at("2026-11-01T00:00:00Z");
    let view = admit_store(&store, &fenced(false, &obs)).unwrap();
    assert_eq!(view.standing(), TrustStanding::ExistingOnly);
    assert_eq!(
        view.role_states(),
        [
            ("TR-BUNDLE", "trusted"),
            ("TR-COMPONENT", "trusted"),
            ("TR-CORE", "trusted"),
            ("TR-INDEX", "expired"),
            ("TR-PROFILE", "unbootstrapped"),
            ("TR-REPAIR", "unbootstrapped"),
        ]
    );
    // The time admission still carries S4's three states, and the handoff
    // clock is set for the operation's rereads.
    let time = view.time().unwrap();
    assert_eq!(time.expired, Some((false, true, false)));
    assert_eq!(time.evaluation, Some(utc("2026-11-01T00:00:00Z")));
    assert!(view.handoff_clock().is_some());
}

/// Item 6 (r12): the fenced read's clock is X4-F1's mapping and transition
/// (`clock_roles`, then `standing_of`) over the stored roles at tEval, and
/// report-only computes the same states, standing and refusal. All three
/// instants lie inside one store's plausibility window.
#[test]
fn the_fenced_reads_clock_is_x4f1s_mapping_and_transition_and_report_only_agrees() {
    use State::*;
    const CATALOG: &str = "2026-11-01T00:00:00Z";
    const ROOT: &str = "2026-12-31T00:00:00Z";
    let store = knobbed(Some(LATER), Some(ROOT), Some(CATALOG));
    // The stored roles, as the acceptance recorded them.
    let stored = [Trusted, Trusted, Trusted, Trusted, Unbootstrapped, Unbootstrapped]
        .map(|s| (s, s != Unbootstrapped));
    for wall in [
        LATER,
        "2026-10-31T23:59:59Z",
        CATALOG,
        STALE_AFTER,
        "2026-12-30T00:00:01Z",
        "2026-12-30T23:59:59Z",
        ROOT,
        "2027-01-01T00:00:00Z",
    ] {
        let t = utc(wall);
        let expired = (t >= utc(ROOT), t >= utc(CATALOG), t > utc(STALE_AFTER));
        let clocked = clock_roles(stored, expired);
        let obs = fenced_at(wall);
        for report in [false, true] {
            let got = admit_store(&store, &fenced(report, &obs));
            match standing_of(&clocked) {
                Ok(standing) => {
                    let view = got.unwrap_or_else(|e| panic!("{wall} {report}: {e:?}"));
                    assert_eq!(view.standing(), standing, "{wall} {report}");
                    assert_eq!(view.role_states(), tokens(clocked), "{wall} {report}");
                    assert_eq!(view.time().unwrap().expired, Some(expired), "{wall}");
                    assert_eq!(view.time().unwrap().report_only, report, "{wall}");
                }
                Err(expected) => {
                    let refusal = got.unwrap_err();
                    assert_eq!(refusal.row, expected.row, "{wall} {report}: {}", refusal.cause);
                }
            }
        }
    }
}

/// Item 6 (r12): each read clocks its own capsule's stored states once. After
/// a fenced read admitted `ExistingOnly`, a reread at T = tEval gives the same
/// states and standing; a reread past the list's staleness refuses from its
/// own stored states (X4-F1).
#[test]
fn a_reread_after_a_clocked_fenced_read_clocks_its_own_stored_states() {
    let store = knobbed(None, None, Some("2026-11-01T00:00:00Z"));
    let obs = fenced_at("2026-11-01T00:00:00Z");
    let first = admit_store(&store, &fenced(false, &obs)).unwrap();
    assert_eq!(first.standing(), TrustStanding::ExistingOnly);
    let t_eval = first.time().unwrap().evaluation.unwrap();
    let clock = first.handoff_clock().unwrap();
    let at = clock.advanced(&obs).unwrap();
    assert_eq!(at, t_eval);
    let again = admit_store(&store, &reread_at(at)).unwrap();
    assert_eq!(again.standing(), first.standing());
    assert_eq!(again.role_states(), first.role_states());
    assert!(again.time().is_none());
    // Past staleness, by monotonic time on the same boot: the reread's own
    // EV-CLOCK over the stored (all trusted) roles refuses.
    let elapsed = utc("2026-12-30T00:00:01Z") - t_eval;
    let later = observation_on("boot-2", 9 + elapsed, "2020-01-01T00:00:00Z");
    let at = clock.advanced(&later).unwrap();
    let refusal = admit_store(&store, &reread_at(at)).unwrap_err();
    assert_eq!(refusal.row, TrustRow::Continuation("core:stale-revocation".into()));
}

#[test]
fn the_policy_digest_is_the_effective_digest_on_both_reads() {
    let obs = hour_later();
    let first = admit(&Spec::default(), &fenced(false, &obs)).unwrap();
    let again = admit(&Spec::default(), &reread()).unwrap();
    assert_eq!(first.epoch(), again.epoch());
    assert_eq!(first.epoch().permission_policy_digest, empty_policy_digest());
}

#[test]
fn accepted_by_must_name_a_loaded_event_of_that_role() {
    let store = fixture::generate(&Spec::default());
    let mut b = view_budget();
    let bindings = current_record_bindings::bind(
        &mut b,
        &store.store,
        &store.capsule,
        &store.descriptor,
        &mut reader(&store, None),
    )
    .unwrap();
    let check = |b: &mut super::super::Budget, capsule: &V| {
        check_accepted_by(b, capsule, &store.descriptor, bindings.trace(), &mut reader(&store, None))
    };
    check(&mut b, &store.capsule).unwrap();
    let roles = object(&object(&store.capsule).unwrap()["roles"]).unwrap();
    let core_by = object(&roles["TR-CORE"]).unwrap()["accepted"].clone();
    let core_by = object(&core_by).unwrap()["by"].clone();
    // TR-INDEX's acceptance pointed at TR-CORE's event refuses.
    let mut tampered = object(&store.capsule).unwrap().clone();
    let mut r = object(&tampered["roles"]).unwrap().clone();
    let mut index = object(&r["TR-INDEX"]).unwrap().clone();
    let mut accepted = object(&index["accepted"]).unwrap().clone();
    accepted.insert("by".into(), core_by.clone());
    index.insert("accepted".into(), V::Object(accepted.clone()));
    r.insert("TR-INDEX".into(), V::Object(index.clone()));
    tampered.insert("roles".into(), V::Object(r.clone()));
    let refusal = check(&mut b, &V::Object(tampered.clone())).unwrap_err();
    assert_eq!(refusal.row, TrustRow::Incomplete);
    // An event that was never loaded refuses too.
    let mut stranger = object(&core_by).unwrap().clone();
    stranger.insert("sha256".into(), V::String("ab".repeat(32)));
    accepted.insert("by".into(), V::Object(stranger));
    index.insert("accepted".into(), V::Object(accepted));
    r.insert("TR-INDEX".into(), V::Object(index));
    tampered.insert("roles".into(), V::Object(r));
    let mut fresh = view_budget();
    let refusal = check(&mut fresh, &V::Object(tampered)).unwrap_err();
    assert_eq!(refusal.row, TrustRow::Incomplete);
}

#[test]
fn each_member_x4t_a_opens_is_required() {
    let store = fixture::generate(&Spec::default());
    let c = object(&store.capsule).unwrap();
    let heads = object(&c["heads"]).unwrap();
    let head = |n: &str| object(&heads[n]).unwrap();
    let doc = |n: &str| object(&head(n)["document"]).unwrap();
    let obs = hour_later();
    for (label, digest) in [
        ("root admission", hash_of(&head("root")["admission"])),
        ("catalog body", hash_of(&doc("catalog")["body"])),
        ("catalog envelope", hash_of(&doc("catalog")["envelope"])),
        ("catalog admission", hash_of(&head("catalog")["admission"])),
        ("revocation admission", hash_of(&head("revocation")["admission"])),
        ("history", hash_of(&c["history"])),
        ("time evidence", hash_of(&object(&c["clock"]).unwrap()["timeEvidence"])),
    ] {
        let mut b = view_budget();
        let refusal = admit_current_trust(
            &mut b,
            &store.store,
            &store.capsule,
            &fenced(false, &obs),
            &mut reader(&store, Some(digest)),
        )
        .unwrap_err();
        assert_eq!(refusal.row, TrustRow::Incomplete, "{label}: {}", refusal.cause);
    }
}

#[test]
fn the_view_cost_is_measured_and_within_the_ceiling() {
    let store = fixture::generate(&Spec {
        roles: [RoleTarget::Trusted; 6],
        ..Spec::default()
    });
    let obs = hour_later();
    let mut b = view_budget();
    // Every distinct record the view reads, by collection and digest.
    let mut read = std::collections::BTreeMap::new();
    let mut recording = |c, h, cap| {
        let raw = reader(&store, None)(c, h, cap)?;
        read.insert((c, h), raw.len());
        Ok(raw)
    };
    admit_current_trust(
        &mut b,
        &store.store,
        &store.capsule,
        &fenced(false, &obs),
        &mut recording,
    )
    .unwrap();
    let (objects, edges, bytes) = b.counters();
    // The charge is linear: one object and exactly its stored bytes per
    // distinct record retained, with no second charge for decoded trees.
    assert_eq!((objects, bytes), (read.len(), read.values().sum()));
    assert!(objects <= TRUST_VIEW_COST.0, "objects {objects}");
    assert!(edges <= TRUST_VIEW_COST.1, "edges {edges}");
    assert!(bytes <= TRUST_VIEW_COST.2, "bytes {bytes}");
    // Pinned: the measured cost of this six-role store.
    assert_eq!((objects, edges, bytes), MEASURED);
}
/// Item 11: one six-role view of the generated store, measured. X4T-a3 adds
/// two edges: the chain anchor's closure and first root body, both already
/// retained, so no object or byte.
const MEASURED: (usize, usize, usize) = (23, 46, 35_371);
/// Item 11: the default store's view through the native fence, measured.
/// X4T-a3 adds the same two loads. A native load always revisits its
/// location, so each charges six edges (the load, two for each of `trust/`
/// and its collection, and the file) and still no object or byte.
/// X4B-c: the default store is X4B's producer's (law X4B r5 item 9). Its
/// payload carries one TR-COMPONENT manifest, so the closure check opens two
/// more objects (`component-0.json` and its envelope, 3,193 bytes), the
/// catalog gains that manifest's release row, and every role document has
/// three signatures: two objects, 26 edges and 4,877 bytes more than the
/// constructed store's (31, 265, 36_008).
#[cfg(target_os = "macos")]
const NATIVE_MEASURED: (usize, usize, usize) = (33, 291, 40_885);
#[cfg(target_os = "macos")]
const _: () = assert!(
    NATIVE_MEASURED.0 <= TRUST_VIEW_COST.0
        && NATIVE_MEASURED.1 <= TRUST_VIEW_COST.1
        && NATIVE_MEASURED.2 <= TRUST_VIEW_COST.2
);

#[test]
fn bounds_refuse_on_the_budget_row() {
    // A 33-event descriptor is refused before it is bound.
    let event = V::Object(Default::default());
    let mut d = std::collections::BTreeMap::new();
    d.insert(
        "events".to_owned(),
        V::Array(vec![event.clone(); MAX_VIEW_EVENTS + 1]),
    );
    assert_eq!(
        check_event_bound(&V::Object(d.clone())).unwrap_err().row,
        TrustRow::Budget
    );
    d.insert("events".to_owned(), V::Array(vec![event; MAX_VIEW_EVENTS]));
    check_event_bound(&V::Object(d)).unwrap();
    // A chain beyond ChainBudget is the budget row, never an S5 code.
    assert_eq!(chain_row(&ChainError::Limit), TrustRow::Budget);
    assert_eq!(TrustRow::Budget.code(), "WORK.BUDGET_EXHAUSTED");
    // A view over its ledger refuses on the budget row; it is never truncated.
    let store = fixture::generate(&Spec::default());
    let obs = hour_later();
    let mut b = super::super::Budget::new(8, 2048, 112 << 20).unwrap();
    let refusal = admit_current_trust(
        &mut b,
        &store.store,
        &store.capsule,
        &fenced(false, &obs),
        &mut reader(&store, None),
    )
    .unwrap_err();
    assert_eq!(refusal.row, TrustRow::Budget, "{}", refusal.cause);
    assert_eq!(VIEW_CHAIN.max_links, 16);
    assert_eq!(VIEW_CHAIN.max_stored_bytes, 16 << 20);
}

#[test]
fn the_closure_total_excludes_the_chain() {
    // The generated store records no chain beyond its root head.
    let store = fixture::generate(&Spec::default());
    let mut b = view_budget();
    let bindings = current_record_bindings::bind(
        &mut b,
        &store.store,
        &store.capsule,
        &store.descriptor,
        &mut reader(&store, None),
    )
    .unwrap();
    let roles = check_accepted_by(
        &mut b,
        &store.capsule,
        &store.descriptor,
        bindings.trace(),
        &mut reader(&store, None),
    )
    .unwrap();
    let (input, _) = authenticate(
        &mut b,
        &store.capsule,
        &store.descriptor,
        &roles,
        &mut reader(&store, None),
    )
    .unwrap();
    assert_eq!(chain_bytes(&input), 0);
    // A closure over 40 MiB refuses even when the chain is small; a closure
    // at 40 MiB with a full chain does not.
    assert_eq!(closure_total(MAX_CLOSURE_BYTES + 1, 0).unwrap_err().row, TrustRow::Budget);
    assert_eq!(
        closure_total(MAX_CLOSURE_BYTES + (10 << 20), 1 << 20).unwrap_err().row,
        TrustRow::Budget
    );
    closure_total(MAX_CLOSURE_BYTES + VIEW_CHAIN.max_stored_bytes, VIEW_CHAIN.max_stored_bytes)
        .unwrap();
}

#[test]
fn nested_causes_take_their_typed_rows() {
    use super::super::M::Error as M;
    use ordinary_metadata::{Error as Meta, catalog::Error as Catalog};
    use ordinary_quorums::Error as Q;
    let deep = |m| {
        Meta::Catalog(Catalog::Quorums(Q::Retained(ordinary_inventory::Error::Bundle(
            ordinary_bundle::Error::Input(m),
        ))))
    };
    for m in [M::ObjectLimit, M::ByteLimit, M::EdgeLimit, M::Closed] {
        assert_eq!(metadata_row(&deep(m)), TrustRow::Budget);
    }
    for m in [M::Cap, M::Capture, M::Missing, M::Digest, M::Reference] {
        assert_eq!(metadata_row(&deep(m)), TrustRow::Incomplete);
    }
    assert_eq!(budget_row(&M::Cap), TrustRow::Incomplete);
    assert_eq!(
        roots_row(&ordinary_roots::Error::Shared(Q::Input(M::Missing))),
        TrustRow::Incomplete
    );
    assert_eq!(
        roots_row(&ordinary_roots::Error::Shared(Q::Retained(
            ordinary_inventory::Error::Input(M::ByteLimit)
        ))),
        TrustRow::Budget
    );
    assert_eq!(
        metadata_row(&Meta::Catalog(Catalog::Schema(recovery_catalog::Error::Quorums(
            incoming_recovery_quorums::Error::Retained(retained_recovery_payload::Error::Input(
                M::EdgeLimit
            ))
        )))),
        TrustRow::Budget
    );
    // A failed document or quorum stays not admissible.
    assert_eq!(
        roots_row(&ordinary_roots::Error::Shared(Q::RetainedQuorum)),
        TrustRow::PayloadNotAdmissible("shared")
    );
    assert_eq!(
        metadata_row(&Meta::Catalog(Catalog::Quorums(Q::Retained(
            ordinary_inventory::Error::MemberSet
        )))),
        TrustRow::PayloadNotAdmissible("inventory")
    );
}

// Law X4T r10 item 12 (X4T-a3): recorded rotations.
fn rotated(roots: usize) -> Spec {
    Spec {
        roots,
        ..Spec::default()
    }
}
fn closure_of(store: &fixture::AcceptedStore) -> V {
    let heads = &object(&store.capsule).unwrap()["heads"];
    let admission = &object(&object(heads).unwrap()["root"]).unwrap()["admission"];
    let raw = store.lookup(Collection::Records, hash_of(admission)).unwrap();
    let admission = opensip_identity::parse_json(&raw).unwrap();
    let raw = store
        .lookup(Collection::Records, hash_of(&object(&admission).unwrap()["parent"]))
        .unwrap();
    opensip_identity::parse_json(&raw).unwrap()
}
fn authenticated(
    store: &fixture::AcceptedStore,
) -> Result<OrdinaryClockInput, TrustRefusal> {
    let mut b = view_budget();
    let bindings = current_record_bindings::bind(
        &mut b,
        &store.store,
        &store.capsule,
        &store.descriptor,
        &mut reader(store, None),
    )
    .unwrap();
    let roles = check_accepted_by(
        &mut b,
        &store.capsule,
        &store.descriptor,
        bindings.trace(),
        &mut reader(store, None),
    )
    .unwrap();
    authenticate(&mut b, &store.capsule, &store.descriptor, &roles, &mut reader(store, None))
        .map(|(input, _)| input)
}

#[test]
fn a_recorded_rotation_is_admitted_from_its_first_root_at_the_final_roots_epoch() {
    let obs = hour_later();
    for n in [1, 2, 3] {
        let store = fixture::generate(&rotated(n));
        let closure = closure_of(&store);
        let V::Array(chain) = &object(&closure).unwrap()["rootChain"] else {
            panic!("rootChain")
        };
        let heads = &object(&store.capsule).unwrap()["heads"];
        let head_document = &object(&object(heads).unwrap()["root"]).unwrap()["document"];
        assert_eq!(chain.len(), n);
        assert_eq!(chain.last(), Some(head_document), "{n}: the chain ends on the head");
        // Root 1 is the accepted root; heads.root is the signing root; the
        // links after the first are evaluated from it.
        let input = authenticated(&store).unwrap();
        let roots = &input.times.proof.roots;
        assert_eq!(roots.original_accepted_ref(), &chain[0], "{n}: accepted root");
        assert_eq!(input.head.document(), head_document, "{n}: signing root");
        assert_eq!(object(input.head.root().value()).unwrap()["rootVersion"], store_version(n));
        assert_eq!(roots.chain().links().len(), n - 1, "{n}: links");
        assert_eq!(roots.chain().accepted_version(), n as i64, "{n}: chain end");
        assert_eq!(roots.presented_first().state(), &QuorumState::Met);
        // Item 11: N..M-1's bodies and envelopes are the chain's bytes; the
        // head's are the closure's.
        let chain_raw: usize = chain[..n - 1]
            .iter()
            .flat_map(|doc| ["body", "envelope"].map(|k| object(doc).unwrap()[k].clone()))
            .map(|r| store.lookup(Collection::Objects, hash_of(&r)).unwrap().len())
            .sum();
        assert_eq!(chain_bytes(&input), chain_raw, "{n}: chain bytes");
        // The epoch's rootVersion and the rootVersion floor are the final
        // root's, on the fenced read and on a reread; a one-root store is r9's.
        for inputs in [fenced(false, &obs), fenced(true, &obs), reread()] {
            let view = admit_store(&store, &inputs).unwrap();
            assert_eq!(view.epoch().root_version, n as i64, "{n}: epoch");
            assert_eq!(view.floors().root_version, Some(n as i64), "{n}: floor");
            assert_eq!(view.standing(), TrustStanding::InstallGateRequiredForNewProcess);
        }
    }
}
fn store_version(n: usize) -> V {
    V::Integer(opensip_identity::JsonInteger::new(n as i128).unwrap())
}

#[test]
fn a_closure_chain_not_ending_on_the_head_is_incomplete() {
    use fixture::ChainEnd::*;
    let obs = hour_later();
    for (roots, end, cause) in [
        (1, OtherEnvelope, "FinalIdentity"),
        (2, OtherEnvelope, "FinalIdentity"),
        (2, Short, "FinalIdentity"),
        (3, Short, "FinalIdentity"),
        // The closed shape refuses an empty rootChain before the join.
        (1, Empty, "Shape"),
        (3, Empty, "Shape"),
    ] {
        let store = fixture::generate(&Spec {
            roots,
            chain_end: end,
            ..Spec::default()
        });
        for inputs in [fenced(false, &obs), reread()] {
            let refusal = admit_store(&store, &inputs).unwrap_err();
            assert_eq!(refusal.row, TrustRow::Incomplete, "{roots} {end:?}: {}", refusal.cause);
            assert_eq!(refusal.cause, cause, "{roots} {end:?}");
            assert_eq!(refusal.row.code(), "CONFIG.CUSTODY_REFUSED");
            assert_eq!(refusal.row.subject().as_deref(), Some("installation-incomplete"));
        }
    }
    // Every closure-join refusal of the root owner is the incomplete row.
    for e in [
        ordinary_roots::Error::EmptyChain,
        ordinary_roots::Error::FinalIdentity,
        ordinary_roots::Error::FirstIdentity,
        ordinary_roots::Error::Shape,
    ] {
        assert_eq!(roots_row(&e), TrustRow::Incomplete, "{e:?}");
    }
}

#[test]
fn a_first_root_below_its_own_threshold_refuses() {
    let obs = hour_later();
    let signer = |i| key_id(&fixture::generate(&Spec::default()), i);
    for (label, spec) in [
        // Root 1's own envelope carries one of its two required signatures.
        (
            "one signature",
            Spec {
                roots: 2,
                root_signers: vec![(0, &[0])],
                ..Spec::default()
            },
        ),
        // Root 1 is signed by keys 0, 1 and 2; the list (signed under root 2)
        // revokes 1 and 2, which are excluded before its threshold is judged.
        (
            "revoked keys excluded",
            Spec {
                roots: 2,
                revocations: vec![("keyId", signer(1)), ("keyId", signer(2))],
                ..Spec::default()
            },
        ),
    ] {
        let refusal = admit(&spec, &fenced(false, &obs)).unwrap_err();
        assert_eq!(refusal.row, TrustRow::PayloadNotAdmissible("root"), "{label}: {}", refusal.cause);
        assert_eq!(refusal.cause, "Times(Rooted(Roots(FirstQuorum)))", "{label}");
        assert_eq!(refusal.row.code(), "PAYLOAD-NOT-ADMISSIBLE");
    }
}

#[test]
fn a_link_failure_takes_its_s5_row_naming_the_link() {
    let obs = hour_later();
    let signer = |i| key_id(&fixture::generate(&Spec::default()), i);
    for (label, spec, code, subject) in [
        // Root 2 signed only by its own keys: no continuity from root 1.
        (
            "continuity",
            Spec {
                roots: 2,
                root_signers: vec![(1, &[20, 21, 22])],
                ..Spec::default()
            },
            "ROOT.CHAIN_OLD_THRESHOLD",
            "link:0",
        ),
        // Root 2 signed only by root 1's keys: no possession.
        (
            "possession",
            Spec {
                roots: 2,
                root_signers: vec![(1, &[0, 1, 2])],
                ..Spec::default()
            },
            "ROOT.CHAIN_NEW_THRESHOLD",
            "link:0",
        ),
        // Root 3 carries one of root 2's keys: the second link fails.
        (
            "second link continuity",
            Spec {
                roots: 3,
                root_signers: vec![(2, &[20, 23, 24, 25])],
                ..Spec::default()
            },
            "ROOT.CHAIN_OLD_THRESHOLD",
            "link:1",
        ),
        // Revoked keys are excluded: root 2's keys 20 and 21 are revoked by
        // the list root 3 signs, so root 2's possession misses its threshold.
        (
            "revoked possession",
            Spec {
                roots: 3,
                revocations: vec![("keyId", signer(20)), ("keyId", signer(21))],
                ..Spec::default()
            },
            "ROOT.CHAIN_NEW_THRESHOLD",
            "link:0",
        ),
    ] {
        let refusal = admit(&spec, &fenced(false, &obs)).unwrap_err();
        assert_eq!(
            refusal.row,
            TrustRow::Root(code, subject.into()),
            "{label}: {}",
            refusal.cause
        );
        assert_eq!(refusal.row.code(), code);
        assert_eq!(refusal.row.subject().as_deref(), Some(subject));
    }
}

#[test]
fn the_revocation_list_is_verified_under_the_signing_root() {
    let obs = hour_later();
    // Law X4T r11 item 4: a list signed by root 2 (M) on a 1-to-2 store is
    // admitted, with its entries carried.
    let unused = key_id(&fixture::generate(&Spec::default()), 26);
    let view = admit(
        &Spec {
            roots: 2,
            revocations: vec![("keyId", unused.clone())],
            ..Spec::default()
        },
        &fenced(false, &obs),
    )
    .unwrap();
    assert_eq!(view.revoked_subjects(), [("keyId".to_owned(), unused)].as_slice());
    assert_eq!(view.epoch().revocation_version, 1);
    // A list signed by root 1's keys only does not meet root 2's quorum.
    let refusal = admit(
        &Spec {
            roots: 2,
            revocation_signers: Some(&[0, 1]),
            ..Spec::default()
        },
        &fenced(false, &obs),
    )
    .unwrap_err();
    assert!(
        matches!(refusal.row, TrustRow::PayloadNotAdmissible(_)),
        "{:?}: {}",
        refusal.row,
        refusal.cause
    );
}

fn key_id(store: &fixture::AcceptedStore, i: usize) -> String {
    let keys = &object(&store.root).unwrap()["keys"];
    let V::Array(keys) = keys else { panic!("keys") };
    let V::String(id) = &object(&keys[i]).unwrap()["keyId"] else {
        panic!("keyId")
    };
    id.clone()
}

#[test]
fn a_revoked_closure_component_refuses_by_kind_and_subject() {
    let obs = hour_later();
    // Root key 2 signed the root envelope (with 0 and 1, threshold 2).
    let signer = key_id(&fixture::generate(&Spec::default()), 2);
    for (kind, subject) in [
        ("release", fixture::CORE_CLOSURE.to_owned()),
        ("keyId", signer),
        ("namespace", "opensip".to_owned()),
        ("catalogSnapshot", "1".to_owned()),
    ] {
        let spec = Spec {
            revocations: vec![(kind, subject.clone())],
            ..Spec::default()
        };
        for inputs in [fenced(false, &obs), reread()] {
            let refusal = admit(&spec, &inputs).unwrap_err();
            let want = format!("{kind}:{subject}");
            assert_eq!(refusal.row, TrustRow::Continuation(want.clone()), "{}", refusal.cause);
            assert_eq!(refusal.row.code(), "CONTINUE-CORE-NOT-TRUSTED");
            assert_eq!(refusal.row.subject(), Some(want));
        }
    }
}

#[test]
fn entries_naming_no_closure_component_are_admitted_and_carried() {
    let obs = hour_later();
    // Key 25 signs nothing in the store; the kinds must match as well.
    let unused = key_id(&fixture::generate(&Spec::default()), 25);
    let revocations = vec![
        ("release", format!("closure2:{}", "d".repeat(64))),
        ("keyId", unused),
        ("namespace", "elsewhere".to_owned()),
        ("catalogSnapshot", "2".to_owned()),
        // The running core's closure named under another kind.
        ("namespace", fixture::CORE_CLOSURE.to_owned()),
    ];
    let spec = Spec {
        revocations: revocations.clone(),
        ..Spec::default()
    };
    let view = admit(&spec, &fenced(false, &obs)).unwrap();
    let carried: Vec<_> = revocations
        .into_iter()
        .map(|(k, s)| (k.to_owned(), s))
        .collect();
    assert_eq!(view.revoked_subjects(), carried.as_slice());
    // A different running core is checked too: the input is never optional.
    let other = format!("closure2:{}", "d".repeat(64));
    let inputs = ViewInputs {
        core_closure: &other,
        ..fenced(false, &obs)
    };
    let refusal = admit(&spec, &inputs).unwrap_err();
    assert_eq!(refusal.row, TrustRow::Continuation(format!("release:{other}")));
}

#[test]
fn rows_carry_their_registered_codes() {
    for (row, code, subject) in [
        (TrustRow::Incomplete, "CONFIG.CUSTODY_REFUSED", Some("installation-incomplete")),
        (
            TrustRow::ClockExcursion("in-session"),
            "CLOCK-EXCURSION-FORWARD",
            Some("in-session"),
        ),
        (
            TrustRow::Root("ROOT.CHAIN_GAP", "link:2".into()),
            "ROOT.CHAIN_GAP",
            Some("link:2"),
        ),
        (TrustRow::StateSchemaUnsupported, "STATE.SCHEMA_UNSUPPORTED", None),
        (TrustRow::HostIo, "HOST.IO_FAILURE", None),
    ] {
        assert_eq!(row.code(), code);
        assert_eq!(row.subject().as_deref(), subject);
    }
}

#[cfg(target_os = "macos")]
#[test]
fn the_native_read_admits_the_written_store_and_rechecks_state_v1() {
    use crate::custody::installation_fence::SuppliedInstallationFence;
    use opensip_identity::{digest_hex, raw_sha256};
    use opensip_platform::RetainedDirectoryPath;
    use std::fs::{self, Permissions};
    use std::os::unix::fs::{MetadataExt, PermissionsExt};
    use std::sync::Arc;
    let id = digest_hex(&raw_sha256(&opensip_platform::request_entropy().unwrap()));
    let root = crate::test_scratch::acl_scratch().join(format!("opensip-x4ta-{id}"));
    fs::create_dir(&root).unwrap();
    fs::set_permissions(&root, Permissions::from_mode(0o700)).unwrap();
    let root = fs::canonicalize(root).unwrap();
    let uid = fs::metadata(&root).unwrap().uid();
    fs::write(root.join("lifecycle.fence"), b"").unwrap();
    fs::set_permissions(root.join("lifecycle.fence"), Permissions::from_mode(0o600)).unwrap();
    let store = fixture::generate(&Spec::default());
    store.write(&root);
    let path = Arc::new(RetainedDirectoryPath::open(&root, 128).unwrap());
    let fence =
        SuppliedInstallationFence::try_acquire(path, uid, &std::collections::BTreeSet::new())
            .unwrap()
            .unwrap();
    let obs = hour_later();
    for inputs in [fenced(true, &obs), reread()] {
        let mut b = view_budget();
        let view = admit_native(&mut b, &fence, &store.store, &inputs).unwrap();
        // Item 11: the native read's measured charge, within the ceiling. Its
        // excess over the in-memory read is the held directories and state.v1.
        assert_eq!(b.counters(), NATIVE_MEASURED);
        assert_eq!(view.standing(), TrustStanding::InstallGateRequiredForNewProcess);
        assert_eq!(view.epoch().permission_policy_digest, empty_policy_digest());
    }
    // A replaced history record is an incomplete installation.
    let c = object(&store.capsule).unwrap();
    let history = hash_of(&c["history"]);
    let file = store
        .files
        .iter()
        .find(|f| f.collection == Some(Collection::Records) && raw_sha256(&f.bytes) == history)
        .unwrap();
    fs::write(root.join(&file.path), b"{}").unwrap();
    let mut b = view_budget();
    let refusal = admit_native(&mut b, &fence, &store.store, &reread()).unwrap_err();
    assert_eq!(refusal.row, TrustRow::Incomplete, "{}", refusal.cause);
    drop(fence);
    let _ = fs::remove_dir_all(&root);
}


// F9: native filesystem/fence with an explicit future observation, not OS clock qualification.
#[cfg(target_os = "macos")]
#[test]
fn f9_native_fenced_read_admits_a_refreshed_store_after_the_old_calendar_expires() {
    use crate::custody::installation_fence::SuppliedInstallationFence;
    use opensip_identity::{digest_hex, raw_sha256};
    use opensip_platform::RetainedDirectoryPath;
    use std::fs::{self, Permissions};
    use std::os::unix::fs::{MetadataExt, PermissionsExt};
    use std::sync::Arc;
    let id = digest_hex(&raw_sha256(&opensip_platform::request_entropy().unwrap()));
    let root = crate::test_scratch::acl_scratch().join(format!("opensip-x4ta-{id}"));
    fs::create_dir(&root).unwrap();
    fs::set_permissions(&root, Permissions::from_mode(0o700)).unwrap();
    let root = fs::canonicalize(root).unwrap();
    let uid = fs::metadata(&root).unwrap().uid();
    fs::write(root.join("lifecycle.fence"), b"").unwrap();
    fs::set_permissions(root.join("lifecycle.fence"), Permissions::from_mode(0o600)).unwrap();
    let store = fixture::generate_at(&Spec::default(), utc("2028-10-02T00:00:00Z"));
    store.write(&root);
    let path = Arc::new(RetainedDirectoryPath::open(&root, 128).unwrap());
    let fence =
        SuppliedInstallationFence::try_acquire(path, uid, &std::collections::BTreeSet::new())
            .unwrap()
            .unwrap();
    let obs = observation(3607, "2028-10-02T01:00:00Z");
    for inputs in [fenced(true, &obs), reread_at(utc("2028-10-02T01:00:00Z"))] {
        let mut b = view_budget();
        let view = admit_native(&mut b, &fence, &store.store, &inputs).unwrap();
        // Item 11: the native read's measured charge, within the ceiling. Its
        // excess over the in-memory read is the held directories and state.v1.
        assert_eq!(b.counters(), NATIVE_MEASURED);
        assert_eq!(view.standing(), TrustStanding::InstallGateRequiredForNewProcess);
        assert_eq!(view.epoch().permission_policy_digest, empty_policy_digest());
    }
    // A replaced history record is an incomplete installation.
    let c = object(&store.capsule).unwrap();
    let history = hash_of(&c["history"]);
    let file = store
        .files
        .iter()
        .find(|f| f.collection == Some(Collection::Records) && raw_sha256(&f.bytes) == history)
        .unwrap();
    fs::write(root.join(&file.path), b"{}").unwrap();
    let mut b = view_budget();
    let refusal = admit_native(&mut b, &fence, &store.store, &reread_at(utc("2028-10-02T01:00:00Z"))).unwrap_err();
    assert_eq!(refusal.row, TrustRow::Incomplete, "{}", refusal.cause);
    drop(fence);
    let _ = fs::remove_dir_all(&root);
}
