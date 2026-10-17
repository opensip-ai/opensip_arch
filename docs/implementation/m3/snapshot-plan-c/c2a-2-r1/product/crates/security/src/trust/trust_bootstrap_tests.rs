// Law X4B r5 item 10 (unit X4B-a), on scratch installations under the ACL
// test scratch. Every payload is a test-only signed release (the public
// quorum62 seeds) produced into an `InitialCore` through 463's injected-image
// test constructor; every P0 store is 467's own producer's. Nothing here
// opens the real account's I.
use super::super::super::super::core_authentication::tests::{
    COMPONENT_SIGNER, INDEX_SIGNER, Signer, Spec as ReleaseSpec,
};
use super::super::super::super::initial_core::tests::{STANDARD, Tree, produce, spec as release};
use super::super::floor_publication::fenced_first_read;
use super::super::{AdmittedCurrentTrust, ReadMode, TrustStanding, ViewInputs};
use super::*;
use crate::custody::installation_admission::observe_private_file;
use crate::custody::installation_fence::SuppliedInstallationFence;
use opensip_platform::{RetainedDirectoryPath, WorkFailure, WorkLedger};
use std::fs::{self, Permissions};
use std::os::unix::fs::{MetadataExt, PermissionsExt};
use std::path::{Path, PathBuf};
use std::sync::Arc;

const STORE: &str = "22222222222222222222222222222222";

/// A signed release produced into an InitialCore, and the payload acceptance
/// reads from it.
fn payload_of(tag: &str, spec: &ReleaseSpec<'_>) -> (BootstrapPayload, String) {
    let tree = Tree::new(tag, spec, None);
    let (core, mut attempt) = produce(&tree.release(STANDARD.0, STANDARD.1), &tree.exe(), 1);
    let core = core.unwrap();
    core.recheck(&mut attempt).unwrap();
    let closure = core.closure().to_owned();
    let payload = WorkLedger::new()
        .scope(|work| {
            BootstrapPayload::from_initial_core(&core, work).map_err(WorkFailure::Operation)
        })
        .unwrap();
    (payload, closure)
}
fn single(tag: &str) -> (BootstrapPayload, String) {
    payload_of(
        tag,
        &ReleaseSpec {
            link: false,
            ..release()
        },
    )
}

struct Site {
    root: PathBuf,
    fence: SuppliedInstallationFence,
    uid: u32,
    store: V,
}
impl Drop for Site {
    fn drop(&mut self) {
        let _ = fs::remove_dir_all(&self.root);
    }
}
/// A creator-only installation: 467's P0 publication under a fenced I.
fn p0_site(closure: &str) -> Site {
    let id = digest_hex(&raw_sha256(&opensip_platform::request_entropy().unwrap()));
    let root = crate::test_scratch::acl_scratch().join(format!("opensip-x4ba-{id}"));
    fs::create_dir(&root).unwrap();
    fs::set_permissions(&root, Permissions::from_mode(0o700)).unwrap();
    let root = fs::canonicalize(root).unwrap();
    let uid = fs::metadata(&root).unwrap().uid();
    fs::write(root.join("lifecycle.fence"), b"").unwrap();
    fs::set_permissions(root.join("lifecycle.fence"), Permissions::from_mode(0o600)).unwrap();
    let inputs = super::super::super::super::initial_publication::Inputs {
        store: STORE,
        state_schema: 1,
        core_closure: closure,
        platform: "macos-aarch64",
        staging_name: "dddddddddddddddddddddddddddddddd",
        boot_id: "boot-0",
        mono: 5,
        wall: "2026-10-01T00:00:00Z",
        request_id: "req1_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        step_id: 0,
        execution_id: "exec1_bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    };
    let p0 = WorkLedger::new()
        .scope(|work| super::super::super::super::initial_publication::build(&inputs, work))
        .unwrap();
    let mut store = V::Null;
    for file in p0.files {
        let mut dir = root.clone();
        for component in &file.path[..file.path.len() - 1] {
            dir.push(component);
            if !dir.exists() {
                fs::create_dir(&dir).unwrap();
            }
            fs::set_permissions(&dir, Permissions::from_mode(0o700)).unwrap();
        }
        let path = root.join(file.path.join("/"));
        if file.path.last().map(String::as_str) == Some("state.v1") {
            let capsule = opensip_identity::parse_json(&file.bytes).unwrap();
            store = map(&capsule).unwrap()["store"].clone();
        }
        fs::write(&path, &file.bytes).unwrap();
        fs::set_permissions(&path, Permissions::from_mode(0o600)).unwrap();
    }
    let path = Arc::new(RetainedDirectoryPath::open(&root, 128).unwrap());
    let fence =
        SuppliedInstallationFence::try_acquire(path, uid, &std::collections::BTreeSet::new())
            .unwrap()
            .unwrap();
    Site {
        root,
        fence,
        uid,
        store,
    }
}
fn current_path(site: &Site) -> PathBuf {
    site.root.join(format!("trust/stores/{STORE}/state.v1"))
}
/// The session's one read of `state.v1`, as X3a's gate retains it.
fn bound(site: &Site) -> RetainedCurrentTrust {
    WorkLedger::new()
        .scope(|work| {
            let relative = format!("trust/stores/{STORE}/state.v1");
            let sample =
                observe_private_file(site.fence.directory(), &relative, site.uid, work).unwrap();
            let raw = fs::read(current_path(site)).unwrap();
            RetainedCurrentTrust::bind(
                site.fence.directory(),
                site.uid,
                &site.store,
                &raw,
                &sample,
                work,
            )
            .map_err(WorkFailure::Operation)
        })
        .unwrap()
}
fn observation(wall: &str) -> V {
    opensip_identity::parse_json(
        format!(r#"{{"bootId":"boot-1","mono":7,"wall":"{wall}"}}"#).as_bytes(),
    )
    .unwrap()
}
fn invocation() -> V {
    obj([
        ("executionId", s("exec1_eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")),
        ("requestId", s("req1_ffffffffffffffffffffffffffffffff")),
        ("stepId", integer(0)),
    ])
}
fn run<T>(
    limits: Option<WorkCost>,
    f: impl FnOnce(&mut WorkScope<'_>) -> Result<T, TrustRefusal>,
) -> Result<T, TrustRefusal> {
    let mut ledger = match limits {
        Some(l) => WorkLedger::with_limits(l).unwrap(),
        None => WorkLedger::new(),
    };
    ledger
        .scope(|work| f(work).map_err(WorkFailure::Operation))
        .map_err(|e| match e {
            WorkFailure::Operation(refusal) => refusal,
            WorkFailure::Budget(b) => TrustRefusal {
                row: TrustRow::Budget,
                cause: format!("{b:?}"),
            },
        })
}
fn accept(
    site: &Site,
    owner: &mut RetainedCurrentTrust,
    payload: &BootstrapPayload,
    obs: &V,
) -> Result<TimeAdmission, TrustRefusal> {
    run(None, |work| {
        accept_bootstrap(work, &site.fence, owner, payload, obs, &invocation())
    })
}
/// Item 1 step 2.3: the one confirming admission, on the same clock sample.
fn confirm(
    site: &Site,
    owner: &mut RetainedCurrentTrust,
    obs: &V,
    closure: &str,
) -> Result<AdmittedCurrentTrust, TrustRefusal> {
    let inputs = ViewInputs {
        mode: ReadMode::Fenced { report: false },
        observation: Some(obs),
        project_policy: None,
        core_closure: closure,
    };
    run(None, |work| {
        fenced_first_read(work, &site.fence, owner, &inputs, &invocation())
    })
}
/// Every trust file under I, by collection and digest.
fn files(root: &Path) -> BTreeMap<(Collection, [u8; 32]), Vec<u8>> {
    let mut out = BTreeMap::new();
    let mut stack = vec![root.join("trust")];
    while let Some(dir) = stack.pop() {
        for entry in fs::read_dir(&dir).unwrap() {
            let path = entry.unwrap().path();
            if path.is_dir() {
                stack.push(path);
                continue;
            }
            let rel = path
                .strip_prefix(root)
                .unwrap()
                .to_string_lossy()
                .into_owned();
            let collection = if rel.starts_with("trust/records/") {
                Collection::Records
            } else if rel.starts_with("trust/objects/") {
                Collection::Objects
            } else if rel.starts_with("trust/publications/") {
                Collection::Publications
            } else if rel.contains("/events/") {
                Collection::Events
            } else {
                continue;
            };
            let bytes = fs::read(&path).unwrap();
            out.insert((collection, raw_sha256(&bytes)), bytes);
        }
    }
    out
}
fn sha(v: &V) -> [u8; 32] {
    hex32(&map(v).unwrap()["sha256"]).unwrap()
}
fn role<'v>(capsule: &'v V, name: &str) -> &'v BTreeMap<String, V> {
    map(&map(&map(capsule).unwrap()["roles"]).unwrap()[name]).unwrap()
}
/// The current descriptor's role events, as (role, event, to) in order.
fn role_events(site: &Site, capsule: &V) -> Vec<(String, String, String)> {
    let all = files(&site.root);
    let publication = &map(capsule).unwrap()["publication"];
    let descriptor =
        opensip_identity::parse_json(&all[&(Collection::Publications, sha(publication))]).unwrap();
    let mut out = Vec::new();
    for row in list(&map(&descriptor).unwrap()["events"]).unwrap() {
        let row = map(row).unwrap();
        if row["roleChange"] == V::Null {
            continue;
        }
        let event =
            opensip_identity::parse_json(&all[&(Collection::Events, sha(&row["event"]))]).unwrap();
        let e = map(&event).unwrap();
        out.push((
            text(&e["role"]).unwrap().to_owned(),
            text(&e["event"]).unwrap().to_owned(),
            text(&e["to"]).unwrap().to_owned(),
        ));
    }
    out
}
fn events_of(all: &[(String, String, String)], name: &str) -> Vec<(String, String)> {
    all.iter()
        .filter(|(r, _, _)| r == name)
        .map(|(_, e, to)| (e.clone(), to.clone()))
        .collect()
}
fn ev(event: &str, to: &str) -> (String, String) {
    (event.into(), to.into())
}
fn tree_files(site: &Site) -> usize {
    files(&site.root).len()
}

#[test]
fn p0_is_accepted_and_the_one_confirming_admission_admits_it() {
    crate::test_scratch::settled(|| {
        let (payload, closure) = single("x4ba-accept");
        let site = p0_site(&closure);
        let p0 = fs::read(current_path(&site)).unwrap();
        let mut owner = bound(&site);
        let obs = observation("2026-10-02T00:00:00Z");
        let time = accept(&site, &mut owner, &payload, &obs).unwrap();
        // S4 step 2: tEval = max(W, A) = W; F := tEval, L := A, anchor := obs.
        let capsule = owner.capsule().clone();
        let record = map(&map(&map(&capsule).unwrap()["clock"]).unwrap()["record"]).unwrap();
        assert_eq!(record["evalHighWater"], s("2026-10-02T00:00:00Z"));
        assert_eq!(record["lastAccepted"], s("2026-10-01T00:00:00Z"));
        assert_eq!(record["anchor"], obs);
        assert_eq!(
            time.last_write,
            Some(timestamp_seconds("2026-10-01T00:00:00Z").unwrap())
        );
        // The pointer is the confirmed new state.v1, and the owner is it.
        let now = fs::read(current_path(&site)).unwrap();
        assert_eq!(owner.raw(), now.as_slice());
        assert_eq!(owner.confirmed().unwrap().raw(), now.as_slice());
        assert_eq!(
            map(&capsule).unwrap()["previous"],
            s(&digest_hex(&raw_sha256(&p0)))
        );
        // Item 4: each carried role from a single EV-PRESENT-PAYLOAD.
        let all = role_events(&site, &capsule);
        for name in ["TR-BUNDLE", "TR-COMPONENT", "TR-CORE", "TR-INDEX"] {
            assert_eq!(
                events_of(&all, name),
                [ev("EV-PRESENT-PAYLOAD", "ST-TRUSTED")],
                "{name}"
            );
            let r = role(&capsule, name);
            assert_eq!(r["state"], s("ST-TRUSTED"), "{name}");
            let accepted = map(&r["accepted"]).unwrap();
            assert_eq!(
                accepted["catalog"] != V::Null,
                name == "TR-INDEX",
                "{name} catalog"
            );
        }
        for name in ["TR-PROFILE", "TR-REPAIR"] {
            assert!(events_of(&all, name).is_empty(), "{name}");
            assert_eq!(role(&capsule, name)["state"], s("ST-UNBOOTSTRAPPED"));
            assert_eq!(role(&capsule, name)["accepted"], V::Null);
        }
        // The confirming admission admits it and writes nothing.
        let confirmed = owner.confirmed().unwrap().clone();
        let view = confirm(&site, &mut owner, &obs, &closure).unwrap();
        assert_eq!(
            view.standing(),
            TrustStanding::InstallGateRequiredForNewProcess
        );
        assert_eq!(view.epoch().root_version, 1);
        assert_eq!(view.epoch().revocation_version, 1);
        assert_eq!(view.epoch().index_snapshot_version, 1);
        assert_eq!(owner.confirmed(), Some(&confirmed));
        assert_eq!(fs::read(current_path(&site)).unwrap(), now);
        // The confirming admission's tEval is max(F, W, A) = F.
        assert_eq!(
            view.time().unwrap().evaluation,
            Some(timestamp_seconds("2026-10-02T00:00:00Z").unwrap())
        );
    });
}

#[test]
fn the_reread_and_the_reference_binders_accept_what_acceptance_wrote() {
    crate::test_scratch::settled(|| {
        let (payload, closure) = single("x4ba-binders");
        let site = p0_site(&closure);
        let mut owner = bound(&site);
        let obs = observation("2026-10-02T00:00:00Z");
        accept(&site, &mut owner, &payload, &obs).unwrap();
        // X4T-a's native reread: capture_p2, bind, bind_trace,
        // bind_retained_head, the Budget::load members and accepted.by.
        let inputs = ViewInputs {
            mode: ReadMode::Reread {
                at: timestamp_seconds("2026-10-02T00:00:00Z").unwrap(),
            },
            observation: None,
            project_policy: None,
            core_closure: &closure,
        };
        let view = {
            let mut b = super::super::view_budget();
            super::super::admit_native(&mut b, &site.fence, &site.store, &inputs).unwrap()
        };
        assert_eq!(
            view.standing(),
            TrustStanding::InstallGateRequiredForNewProcess
        );
        assert_eq!(
            view.role_states(),
            [
                ("TR-BUNDLE", "trusted"),
                ("TR-COMPONENT", "trusted"),
                ("TR-CORE", "trusted"),
                ("TR-INDEX", "trusted"),
                ("TR-PROFILE", "unbootstrapped"),
                ("TR-REPAIR", "unbootstrapped"),
            ]
        );
        // Every record passes its closed shape and its content address.
        for ((collection, digest), raw) in files(&site.root) {
            assert_eq!(raw_sha256(&raw), digest);
            let value = opensip_identity::parse_json(&raw).unwrap();
            assert_eq!(
                canonical_bytes(&value).unwrap(),
                raw,
                "{collection:?} canonical"
            );
        }
    });
}

#[test]
fn the_fresh_install_time_rules_take_max_of_wall_and_admitted_time() {
    crate::test_scratch::settled(|| {
        let (payload, closure) = single("x4ba-time");
        // W behind A (within 24 h): tEval = A.
        let site = p0_site(&closure);
        let mut owner = bound(&site);
        let obs = observation("2026-09-30T12:00:00Z");
        accept(&site, &mut owner, &payload, &obs).unwrap();
        let record = map(&map(&map(owner.capsule()).unwrap()["clock"]).unwrap()["record"])
            .unwrap()
            .clone();
        assert_eq!(record["evalHighWater"], s("2026-10-01T00:00:00Z"));
        assert_eq!(record["lastAccepted"], s("2026-10-01T00:00:00Z"));
        assert_eq!(record["anchor"], obs);
        confirm(&site, &mut owner, &obs, &closure).unwrap();
        // A payload issued beyond W + 24 h is not admissible; nothing written.
        let site = p0_site(&closure);
        let before = tree_files(&site);
        let mut owner = bound(&site);
        let err = accept(
            &site,
            &mut owner,
            &payload,
            &observation("2026-09-29T23:59:59Z"),
        )
        .unwrap_err();
        assert_eq!(err.row, TrustRow::PayloadNotAdmissible("time"));
        assert_eq!(tree_files(&site), before);
        assert!(owner.confirmed().is_none());
        // W > A + 90 d: CLOCK-EXCURSION-FORWARD beyond-horizon; nothing written.
        let err = accept(
            &site,
            &mut owner,
            &payload,
            &observation("2026-12-30T00:00:01Z"),
        )
        .unwrap_err();
        assert_eq!(err.row, TrustRow::ClockExcursion("beyond-horizon"));
        assert_eq!(tree_files(&site), before);
        // Exactly A + 90 d is admitted.
        accept(
            &site,
            &mut owner,
            &payload,
            &observation("2026-12-30T00:00:00Z"),
        )
        .unwrap();
    });
}

#[test]
fn an_expired_catalog_is_present_then_clock_and_existing_only() {
    crate::test_scratch::settled(|| {
        let (payload, closure) = payload_of(
            "x4ba-expired",
            &ReleaseSpec {
                link: false,
                catalog_expires: "2026-10-10T00:00:00Z",
                ..release()
            },
        );
        let site = p0_site(&closure);
        let mut owner = bound(&site);
        let obs = observation("2026-10-20T00:00:00Z");
        accept(&site, &mut owner, &payload, &obs).unwrap();
        let capsule = owner.capsule().clone();
        let all = role_events(&site, &capsule);
        assert_eq!(
            events_of(&all, "TR-INDEX"),
            [
                ev("EV-PRESENT-PAYLOAD", "ST-TRUSTED"),
                ev("EV-CLOCK", "ST-EXPIRED")
            ]
        );
        let index = role(&capsule, "TR-INDEX");
        assert_eq!(index["state"], s("ST-EXPIRED"));
        // accepted.by names the first event, the one that accepted it.
        let files = files(&site.root);
        let by = &map(&index["accepted"]).unwrap()["by"];
        let event = opensip_identity::parse_json(&files[&(Collection::Events, sha(by))]).unwrap();
        assert_eq!(map(&event).unwrap()["event"], s("EV-PRESENT-PAYLOAD"));
        for name in ["TR-BUNDLE", "TR-COMPONENT", "TR-CORE"] {
            assert_eq!(role(&capsule, name)["state"], s("ST-TRUSTED"), "{name}");
        }
        let view = confirm(&site, &mut owner, &obs, &closure).unwrap();
        assert_eq!(view.standing(), TrustStanding::ExistingOnly);
    });
}

#[test]
fn an_expired_root_expires_every_carried_role_and_the_core_takes_the_continuation_row() {
    crate::test_scratch::settled(|| {
        let (payload, closure) = payload_of(
            "x4ba-root-expired",
            &ReleaseSpec {
                link: false,
                root_expires: Some("2026-10-15T00:00:00Z"),
                ..release()
            },
        );
        let site = p0_site(&closure);
        let mut owner = bound(&site);
        let obs = observation("2026-10-20T00:00:00Z");
        accept(&site, &mut owner, &payload, &obs).unwrap();
        let capsule = owner.capsule().clone();
        let all = role_events(&site, &capsule);
        for name in ["TR-BUNDLE", "TR-COMPONENT", "TR-CORE", "TR-INDEX"] {
            assert_eq!(
                events_of(&all, name),
                [
                    ev("EV-PRESENT-PAYLOAD", "ST-TRUSTED"),
                    ev("EV-CLOCK", "ST-EXPIRED")
                ],
                "{name}"
            );
        }
        // The acceptance is durable; the confirming admission refuses on
        // X4T's continuation row.
        let err = confirm(&site, &mut owner, &obs, &closure).unwrap_err();
        assert_eq!(err.row, TrustRow::Continuation("core:expired".into()));
        assert_eq!(fs::read(current_path(&site)).unwrap(), owner.raw());
    });
}

#[test]
fn a_stale_revocation_is_present_then_clock_and_stale() {
    crate::test_scratch::settled(|| {
        let (payload, closure) = payload_of(
            "x4ba-stale",
            &ReleaseSpec {
                link: false,
                revocation_issued: "2026-06-01T00:00:00Z",
                ..release()
            },
        );
        let site = p0_site(&closure);
        let mut owner = bound(&site);
        let obs = observation("2026-10-02T00:00:00Z");
        accept(&site, &mut owner, &payload, &obs).unwrap();
        let capsule = owner.capsule().clone();
        let all = role_events(&site, &capsule);
        for name in ["TR-BUNDLE", "TR-COMPONENT", "TR-CORE", "TR-INDEX"] {
            assert_eq!(
                events_of(&all, name),
                [
                    ev("EV-PRESENT-PAYLOAD", "ST-TRUSTED"),
                    ev("EV-CLOCK", "ST-STALE-REVOCATION")
                ],
                "{name}"
            );
        }
        let err = confirm(&site, &mut owner, &obs, &closure).unwrap_err();
        assert_eq!(
            err.row,
            TrustRow::Continuation("core:stale-revocation".into())
        );
    });
}

#[test]
fn a_revoked_counted_signer_below_the_threshold_refuses_and_writes_nothing() {
    crate::test_scratch::settled(|| {
        // RF-1: the list revokes one of a document's two counted signers
        // (key 11 of the catalog's TR-INDEX pair; key 14 of the component
        // manifest's TR-COMPONENT pair). With it excluded the quorum is one of
        // two: not admissible, and nothing is written.
        for (tag, revoke, subject) in [
            ("x4ba-revoked-catalog", &[11usize][..], "catalog"),
            ("x4ba-revoked-component", &[14usize][..], "component"),
        ] {
            let (payload, closure) = payload_of(
                tag,
                &ReleaseSpec {
                    link: false,
                    revoke,
                    ..release()
                },
            );
            let site = p0_site(&closure);
            let before = tree_files(&site);
            let p0 = fs::read(current_path(&site)).unwrap();
            let mut owner = bound(&site);
            let err = accept(
                &site,
                &mut owner,
                &payload,
                &observation("2026-10-02T00:00:00Z"),
            )
            .unwrap_err();
            assert_eq!(err.row, TrustRow::PayloadNotAdmissible(subject), "{tag}");
            assert_eq!(tree_files(&site), before, "{tag}");
            assert_eq!(fs::read(current_path(&site)).unwrap(), p0, "{tag}");
            assert!(owner.confirmed().is_none(), "{tag}");
        }
    });
}

/// The catalog signed by all three TR-INDEX keys: one revoked key leaves
/// the threshold of two met, so the document is admissible and revoked.
const THREE_INDEX: &[Signer<'static>] = &[("TR-INDEX", &[11, 12, 13])];

#[test]
fn a_revoked_document_whose_quorum_survives_is_present_then_revoke_with_revoked_by() {
    crate::test_scratch::settled(|| {
        let (payload, closure) = payload_of(
            "x4ba-revoked",
            &ReleaseSpec {
                link: false,
                revoke: &[11],
                catalog_signers: THREE_INDEX,
                ..release()
            },
        );
        let site = p0_site(&closure);
        let mut owner = bound(&site);
        let obs = observation("2026-10-02T00:00:00Z");
        accept(&site, &mut owner, &payload, &obs).unwrap();
        let capsule = owner.capsule().clone();
        let all = role_events(&site, &capsule);
        assert_eq!(
            events_of(&all, "TR-INDEX"),
            [
                ev("EV-PRESENT-PAYLOAD", "ST-TRUSTED"),
                ev("EV-REVOKE", "ST-REVOKED")
            ]
        );
        let index = role(&capsule, "TR-INDEX");
        assert_eq!(index["state"], s("ST-REVOKED"));
        let condition = map(&index["conditionEvidence"]).unwrap();
        let files = files(&site.root);
        let event = opensip_identity::parse_json(
            &files[&(Collection::Events, sha(&condition["revokedBy"]))],
        )
        .unwrap();
        assert_eq!(map(&event).unwrap()["event"], s("EV-REVOKE"));
        assert_ne!(
            map(&index["accepted"]).unwrap()["by"],
            condition["revokedBy"]
        );
        for name in ["TR-BUNDLE", "TR-COMPONENT", "TR-CORE"] {
            assert_eq!(role(&capsule, name)["state"], s("ST-TRUSTED"), "{name}");
        }
        let err = confirm(&site, &mut owner, &obs, &closure).unwrap_err();
        assert_eq!(err.row, TrustRow::IndexContinuation("index:revoked".into()));
    });
}

#[test]
fn expired_and_revoked_is_three_events_ending_revoked() {
    crate::test_scratch::settled(|| {
        let (payload, closure) = payload_of(
            "x4ba-expired-revoked",
            &ReleaseSpec {
                link: false,
                revoke: &[11],
                catalog_signers: THREE_INDEX,
                catalog_expires: "2026-10-10T00:00:00Z",
                ..release()
            },
        );
        let site = p0_site(&closure);
        let mut owner = bound(&site);
        accept(
            &site,
            &mut owner,
            &payload,
            &observation("2026-10-20T00:00:00Z"),
        )
        .unwrap();
        let capsule = owner.capsule().clone();
        assert_eq!(
            events_of(&role_events(&site, &capsule), "TR-INDEX"),
            [
                ev("EV-PRESENT-PAYLOAD", "ST-TRUSTED"),
                ev("EV-CLOCK", "ST-EXPIRED"),
                ev("EV-REVOKE", "ST-REVOKED")
            ]
        );
        assert_eq!(role(&capsule, "TR-INDEX")["state"], s("ST-REVOKED"));
    });
}

#[test]
fn an_inactive_or_rejected_entry_records_no_event() {
    for entry in [BootstrapEntry::Inactive, BootstrapEntry::Rejected] {
        for (expired, stale, revoked) in [(false, false, false), (true, true, true)] {
            assert!(bootstrap_sequence(entry, expired, stale, revoked).is_empty());
        }
    }
    assert_eq!(
        bootstrap_sequence(BootstrapEntry::Admissible, true, true, false),
        [
            (BootstrapEvent::Present, State::Trusted),
            (BootstrapEvent::Clock, State::Expired)
        ]
    );
    assert_eq!(
        bootstrap_sequence(BootstrapEntry::Admissible, false, false, false),
        [(BootstrapEvent::Present, State::Trusted)]
    );
}

#[test]
fn a_bootstrap_without_a_catalog_or_with_one_outside_its_role_writes_nothing() {
    crate::test_scratch::settled(|| {
        const NONE: &[Signer<'static>] = &[];
        const WRONG: &[Signer<'static>] = &[("TR-INDEX", &[14, 15])];
        for (tag, signers) in [("x4ba-no-catalog", NONE), ("x4ba-wrong-keys", WRONG)] {
            let (payload, closure) = payload_of(
                tag,
                &ReleaseSpec {
                    link: false,
                    catalog_signers: signers,
                    ..release()
                },
            );
            let site = p0_site(&closure);
            let before = tree_files(&site);
            let p0 = fs::read(current_path(&site)).unwrap();
            let mut owner = bound(&site);
            let err = accept(
                &site,
                &mut owner,
                &payload,
                &observation("2026-10-02T00:00:00Z"),
            )
            .unwrap_err();
            assert_eq!(err.row, TrustRow::PayloadNotAdmissible("catalog"), "{tag}");
            assert_eq!(tree_files(&site), before, "{tag}");
            assert_eq!(fs::read(current_path(&site)).unwrap(), p0, "{tag}");
        }
        // A component manifest signed outside its role refuses the same way.
        const WRONG_COMPONENT: &[Option<Signer<'static>>] = &[Some(("TR-COMPONENT", &[11, 12]))];
        let (payload, closure) = payload_of(
            "x4ba-wrong-component",
            &ReleaseSpec {
                link: false,
                component_signers: WRONG_COMPONENT,
                ..release()
            },
        );
        let site = p0_site(&closure);
        let mut owner = bound(&site);
        let err = accept(
            &site,
            &mut owner,
            &payload,
            &observation("2026-10-02T00:00:00Z"),
        )
        .unwrap_err();
        assert_eq!(err.row, TrustRow::PayloadNotAdmissible("component"));
    });
}

#[test]
fn no_component_manifest_leaves_the_component_unbootstrapped() {
    crate::test_scratch::settled(|| {
        let (payload, closure) = payload_of(
            "x4ba-no-component",
            &ReleaseSpec {
                link: false,
                component_signers: &[],
                ..release()
            },
        );
        let site = p0_site(&closure);
        let mut owner = bound(&site);
        let obs = observation("2026-10-02T00:00:00Z");
        accept(&site, &mut owner, &payload, &obs).unwrap();
        let capsule = owner.capsule().clone();
        assert!(events_of(&role_events(&site, &capsule), "TR-COMPONENT").is_empty());
        assert_eq!(
            role(&capsule, "TR-COMPONENT")["state"],
            s("ST-UNBOOTSTRAPPED")
        );
        let err = confirm(&site, &mut owner, &obs, &closure).unwrap_err();
        assert_eq!(
            err.row,
            TrustRow::ComponentContinuation("component:unbootstrapped".into())
        );
        let _ = (INDEX_SIGNER, COMPONENT_SIGNER);
    });
}

#[test]
fn a_crash_before_the_pointer_leaves_p0_and_a_rerun_accepts() {
    crate::test_scratch::settled(|| {
        let (payload, closure) = single("x4ba-crash");
        let site = p0_site(&closure);
        let p0 = fs::read(current_path(&site)).unwrap();
        let mut owner = bound(&site);
        let obs = observation("2026-10-02T00:00:00Z");
        // Every dependency written, the pointer never replaced: the files a
        // crash before the rename leaves, unreferenced.
        let built = run(None, |work| {
            build_acceptance(&owner, &payload, &obs, &invocation(), work)
        })
        .unwrap();
        for file in &built.files {
            let path = site.root.join(file.path_for_tests().join("/"));
            let mut dir = site.root.clone();
            for component in file.path_for_tests().split_last().unwrap().1 {
                dir.push(component);
                if !dir.exists() {
                    fs::create_dir(&dir).unwrap();
                    fs::set_permissions(&dir, Permissions::from_mode(0o700)).unwrap();
                }
            }
            if !path.exists() {
                fs::write(&path, file.bytes()).unwrap();
                fs::set_permissions(&path, Permissions::from_mode(0o600)).unwrap();
            }
        }
        assert_eq!(fs::read(current_path(&site)).unwrap(), p0);
        // The next first write runs acceptance again: equal bytes are equal
        // names, so every present record is admitted, and P0 is replaced.
        accept(&site, &mut owner, &payload, &obs).unwrap();
        assert_eq!(fs::read(current_path(&site)).unwrap(), built.capsule_raw());
        confirm(&site, &mut owner, &obs, &closure).unwrap();
        // A rerun at another instant writes fresh names beside them.
        let site = p0_site(&closure);
        let mut owner = bound(&site);
        let other = run(None, |work| {
            build_acceptance(
                &owner,
                &payload,
                &observation("2026-10-03T00:00:00Z"),
                &invocation(),
                work,
            )
        })
        .unwrap();
        assert_ne!(other.capsule_raw(), built.capsule_raw());
        accept(
            &site,
            &mut owner,
            &payload,
            &observation("2026-10-03T00:00:00Z"),
        )
        .unwrap();
    });
}

#[test]
fn a_changed_retained_state_file_refuses_before_any_write() {
    crate::test_scratch::settled(|| {
        let (payload, closure) = single("x4ba-changed");
        let site = p0_site(&closure);
        let mut owner = bound(&site);
        let before = tree_files(&site);
        // Rewrite state.v1 with its own bytes: a new file, a new sample.
        let path = current_path(&site);
        let raw = fs::read(&path).unwrap();
        fs::remove_file(&path).unwrap();
        fs::write(&path, &raw).unwrap();
        fs::set_permissions(&path, Permissions::from_mode(0o600)).unwrap();
        let err = accept(
            &site,
            &mut owner,
            &payload,
            &observation("2026-10-02T00:00:00Z"),
        )
        .unwrap_err();
        assert_eq!(err.row, TrustRow::RequiredFilesChanged);
        assert_eq!(tree_files(&site), before);
    });
}

#[test]
fn a_short_ledger_is_the_budget_row_and_leaves_p0() {
    crate::test_scratch::settled(|| {
        let (payload, closure) = single("x4ba-budget");
        let site = p0_site(&closure);
        let p0 = fs::read(current_path(&site)).unwrap();
        let mut owner = bound(&site);
        let obs = observation("2026-10-02T00:00:00Z");
        let err = run(
            Some(WorkCost {
                objects: 64,
                edges: 4096,
                bytes: 1 << 20,
            }),
            |work| accept_bootstrap(work, &site.fence, &mut owner, &payload, &obs, &invocation()),
        )
        .unwrap_err();
        assert_eq!(err.row, TrustRow::Budget);
        assert_eq!(fs::read(current_path(&site)).unwrap(), p0);
    });
}

#[test]
fn only_a_p0_predecessor_and_the_embedded_binding_are_accepted() {
    crate::test_scratch::settled(|| {
        let (payload, closure) = single("x4ba-predecessor");
        let site = p0_site(&closure);
        let mut owner = bound(&site);
        let obs = observation("2026-10-02T00:00:00Z");
        accept(&site, &mut owner, &payload, &obs).unwrap();
        // An accepted store is never accepted again.
        let err = accept(&site, &mut owner, &payload, &obs).unwrap_err();
        assert_eq!(err.row, TrustRow::HostIo);
        // A payload whose root is not the embedded binding refuses.
        let mut other = WorkLedger::new()
            .scope(|work| {
                BootstrapPayload::from_parts(
                    obj([
                        ("rootDigest", s(&"0".repeat(64))),
                        ("rootSchema", integer(1)),
                        ("rootVersion", integer(1)),
                    ]),
                    payload.manifest.clone(),
                    payload.inventory.clone(),
                    &closure,
                    payload.blobs.values().cloned(),
                    work,
                )
                .map_err(WorkFailure::Operation)
            })
            .unwrap();
        let site = p0_site(&closure);
        let mut owner = bound(&site);
        let err = accept(&site, &mut owner, &other, &obs).unwrap_err();
        assert_eq!(err.row, TrustRow::PayloadNotAdmissible("root"));
        // A tampered manifest envelope fails its signature.
        other.binding = payload.binding.clone();
        let mut envelope = map(&parse(&other.manifest.1, "payload").unwrap())
            .unwrap()
            .clone();
        envelope.insert("namespace".into(), s("other"));
        other.manifest.1 = canonical_bytes(&V::Object(envelope)).unwrap();
        let err = accept(&site, &mut owner, &other, &obs).unwrap_err();
        assert_eq!(err.row, TrustRow::PayloadNotAdmissible("payload"));
    });
}

#[test]
fn a_multi_link_root_chain_is_authenticated_and_recorded_in_full() {
    crate::test_scratch::settled(|| {
        // The default release rotates root 1 to root 2 (one link).
        let (payload, closure) = payload_of("x4ba-link", &release());
        let site = p0_site(&closure);
        let mut owner = bound(&site);
        let obs = observation("2026-10-02T00:00:00Z");
        accept(&site, &mut owner, &payload, &obs).unwrap();
        let capsule = owner.capsule().clone();
        let heads = map(&map(&capsule).unwrap()["heads"]).unwrap();
        let binding = map(&map(&heads["root"]).unwrap()["binding"]).unwrap();
        assert_eq!(binding["rootVersion"], integer(2));
        let record = map(&map(&map(&capsule).unwrap()["clock"]).unwrap()["record"]).unwrap();
        assert_eq!(record["rootVersion"], integer(2));
        // The closure lists the whole chain, as the manifest does.
        let files = files(&site.root);
        let admission = &map(&heads["root"]).unwrap()["admission"];
        let node =
            opensip_identity::parse_json(&files[&(Collection::Records, sha(admission))]).unwrap();
        let parent = &map(&node).unwrap()["parent"];
        let closure_record =
            opensip_identity::parse_json(&files[&(Collection::Records, sha(parent))]).unwrap();
        assert_eq!(
            list(&map(&closure_record).unwrap()["rootChain"])
                .unwrap()
                .len(),
            2
        );
        // Law X4T r10 item 3 (X4T-a3, closing judgment call 12): the reader
        // takes root 1, the closure's first `rootChain` document, as the
        // accepted root and `heads.root` (root 2) as the signing root, so the
        // confirming admission admits the rotated store at the final root's
        // epoch and floor.
        let view = confirm(&site, &mut owner, &obs, &closure).unwrap();
        assert_eq!(view.epoch().root_version, 2);
        assert_eq!(view.floors().root_version, Some(2));
    });
}

// ------------------------------------------- X4B-b: item 1 step 2, the read

/// A signed release produced into an `InitialCore`, kept whole: the write
/// receipt's running core, the F-absent branch's only payload source.
fn core_of(tag: &str, spec: &ReleaseSpec<'_>) -> (super::super::super::super::InitialCore, String) {
    let tree = Tree::new(tag, spec, None);
    let (core, mut attempt) = produce(&tree.release(STANDARD.0, STANDARD.1), &tree.exe(), 1);
    let core = core.unwrap();
    core.recheck(&mut attempt).unwrap();
    let closure = core.closure().to_owned();
    (core, closure)
}
/// The operation monitor's first read body, on this site's fence.
fn first_read(
    site: &Site,
    owner: &mut RetainedCurrentTrust,
    obs: &V,
    closure: &str,
    mode: ReadMode,
    source: &BootstrapSource<'_>,
) -> Result<AdmittedCurrentTrust, TrustRefusal> {
    let inputs = ViewInputs {
        mode,
        observation: Some(obs),
        project_policy: None,
        core_closure: closure,
    };
    run(None, |work| {
        bootstrapping_first_read(work, &site.fence, owner, &inputs, &invocation(), source)
    })
}
const LIVE: ReadMode = ReadMode::Fenced { report: false };
fn f_absent(cause: &str) -> TrustRefusal {
    TrustRefusal {
        row: TrustRow::NoAdmittedTimeContext,
        cause: cause.into(),
    }
}

#[test]
fn f_absent_is_accepted_inside_the_first_read_and_the_confirming_view_is_returned() {
    crate::test_scratch::settled(|| {
        // The default release rotates root 1 to root 2 (X4T r11 item 3).
        let (core, closure) = core_of("x4bb-accept", &release());
        let site = p0_site(&closure);
        let p0 = fs::read(current_path(&site)).unwrap();
        let mut owner = bound(&site);
        let p0_sample = owner.sample().clone();
        let obs = observation("2026-10-02T00:00:00Z");
        let source = BootstrapSource::running_core(&core);
        let view = first_read(&site, &mut owner, &obs, &closure, LIVE, &source).unwrap();
        // The returned view is the confirming admission's, over the
        // confirmed retained state.v1: the accepted roles, root 2's epoch.
        assert_eq!(
            view.standing(),
            TrustStanding::InstallGateRequiredForNewProcess
        );
        assert_eq!(view.epoch().root_version, 2);
        assert_eq!(
            view.role_states(),
            [
                ("TR-BUNDLE", "trusted"),
                ("TR-COMPONENT", "trusted"),
                ("TR-CORE", "trusted"),
                ("TR-INDEX", "trusted"),
                ("TR-PROFILE", "unbootstrapped"),
                ("TR-REPAIR", "unbootstrapped"),
            ]
        );
        // Exactly one confirmed publication, the acceptance, on P0: the
        // confirming admission (tEval = max(F, W, A) = F) wrote nothing.
        let now = fs::read(current_path(&site)).unwrap();
        assert_ne!(now, p0);
        assert_eq!(owner.confirmations().len(), 1);
        let accepted = &owner.confirmations()[0];
        assert_eq!(accepted.predecessor(), &p0_sample);
        assert_eq!(accepted.raw(), now.as_slice());
        assert_eq!(owner.raw(), now.as_slice());
        // Item 3: tEval, F, L and the anchor come from this read's sample.
        let record = map(&map(&map(owner.capsule()).unwrap()["clock"]).unwrap()["record"]).unwrap();
        assert_eq!(record["evalHighWater"], s("2026-10-02T00:00:00Z"));
        assert_eq!(record["lastAccepted"], s("2026-10-01T00:00:00Z"));
        assert_eq!(record["anchor"], obs);
        assert_eq!(
            view.time().unwrap().evaluation,
            Some(timestamp_seconds("2026-10-02T00:00:00Z").unwrap())
        );
        // A later first read finds F present: the branch is never entered
        // (an unreached source would refuse), and nothing is written.
        let again = first_read(
            &site,
            &mut owner,
            &obs,
            &closure,
            LIVE,
            &BootstrapSource::unreached(),
        )
        .unwrap();
        assert_eq!(again.epoch(), view.epoch());
        assert_eq!(owner.confirmations().len(), 1);
        assert_eq!(fs::read(current_path(&site)).unwrap(), now);
    });
}

#[test]
fn a_report_only_or_unfenced_read_never_bootstraps() {
    crate::test_scratch::settled(|| {
        let (core, closure) = core_of("x4bb-report", &release());
        let source = BootstrapSource::running_core(&core);
        let obs = observation("2026-10-02T00:00:00Z");
        let site = p0_site(&closure);
        let before = tree_files(&site);
        let p0 = fs::read(current_path(&site)).unwrap();
        let mut owner = bound(&site);
        // Report-only (458c's mode): F absent is reported as is.
        let err = first_read(
            &site,
            &mut owner,
            &obs,
            &closure,
            ReadMode::Fenced { report: true },
            &source,
        )
        .unwrap_err();
        assert_eq!(err.row, TrustRow::NoAdmittedTimeContext);
        // An unfenced reread is not a first read at all.
        let reread = ReadMode::Reread {
            at: timestamp_seconds("2026-10-02T00:00:00Z").unwrap(),
        };
        let err = first_read(&site, &mut owner, &obs, &closure, reread, &source).unwrap_err();
        assert_eq!(err.row, TrustRow::HostIo);
        assert_eq!(err.cause, "\"fenced-read-mode\"");
        assert_eq!(tree_files(&site), before);
        assert_eq!(fs::read(current_path(&site)).unwrap(), p0);
        assert!(owner.confirmations().is_empty());
    });
}

#[test]
fn an_acceptance_refusal_ends_the_read_with_no_confirming_admission() {
    crate::test_scratch::settled(|| {
        // No catalog: item 2's refusal, before any write.
        const NONE: &[Signer<'static>] = &[];
        let (core, closure) = core_of(
            "x4bb-no-catalog",
            &ReleaseSpec {
                link: false,
                catalog_signers: NONE,
                ..release()
            },
        );
        let source = BootstrapSource::running_core(&core);
        let site = p0_site(&closure);
        let before = tree_files(&site);
        let p0 = fs::read(current_path(&site)).unwrap();
        let mut owner = bound(&site);
        let obs = observation("2026-10-02T00:00:00Z");
        let err = first_read(&site, &mut owner, &obs, &closure, LIVE, &source).unwrap_err();
        assert_eq!(err.row, TrustRow::PayloadNotAdmissible("catalog"));
        assert_eq!(tree_files(&site), before);
        assert_eq!(fs::read(current_path(&site)).unwrap(), p0);
        assert!(owner.confirmations().is_empty());
        // Item 3 on the read's own sample: W beyond A + 90 d.
        let (core, closure) = core_of("x4bb-horizon", &release());
        let source = BootstrapSource::running_core(&core);
        let site = p0_site(&closure);
        let before = tree_files(&site);
        let mut owner = bound(&site);
        let far = observation("2027-01-01T00:00:00Z");
        let err = first_read(&site, &mut owner, &far, &closure, LIVE, &source).unwrap_err();
        assert_eq!(err.row, TrustRow::ClockExcursion("beyond-horizon"));
        assert_eq!(tree_files(&site), before);
        assert!(owner.confirmations().is_empty());
        // No component manifest: the acceptance is recorded, and the one
        // confirming admission refuses on its continuation row.
        let (core, closure) = core_of(
            "x4bb-no-component",
            &ReleaseSpec {
                link: false,
                component_signers: &[],
                ..release()
            },
        );
        let source = BootstrapSource::running_core(&core);
        let site = p0_site(&closure);
        let mut owner = bound(&site);
        let err = first_read(&site, &mut owner, &obs, &closure, LIVE, &source).unwrap_err();
        assert_eq!(
            err.row,
            TrustRow::ComponentContinuation("component:unbootstrapped".into())
        );
        assert_eq!(owner.confirmations().len(), 1);
    });
}

#[test]
fn a_first_refusal_other_than_f_absent_runs_no_acceptance() {
    crate::test_scratch::settled(|| {
        let (core, closure) = core_of("x4bb-changed", &release());
        let source = BootstrapSource::running_core(&core);
        let site = p0_site(&closure);
        let mut owner = bound(&site);
        let before = tree_files(&site);
        // Rewrite state.v1 with its own bytes: a new file, a new sample.
        let path = current_path(&site);
        let raw = fs::read(&path).unwrap();
        fs::remove_file(&path).unwrap();
        fs::write(&path, &raw).unwrap();
        fs::set_permissions(&path, Permissions::from_mode(0o600)).unwrap();
        let obs = observation("2026-10-02T00:00:00Z");
        let err = first_read(&site, &mut owner, &obs, &closure, LIVE, &source).unwrap_err();
        assert_eq!(err.row, TrustRow::RequiredFilesChanged);
        assert_eq!(tree_files(&site), before);
        assert!(owner.confirmations().is_empty());
    });
}

#[test]
fn the_sequence_accepts_once_and_confirms_once_and_a_second_f_absent_is_the_invariant() {
    // (admissions run, acceptances run) for each scripted outcome.
    type Script = (Vec<Result<u8, TrustRefusal>>, Result<(), TrustRefusal>);
    let play = |(mut admissions, accepted): Script| {
        admissions.reverse();
        let mut counts = (0, 0);
        let mut accepted = Some(accepted);
        let result = first_read_sequence(
            &mut counts,
            |counts| {
                counts.0 += 1;
                admissions.pop().expect("no third admission")
            },
            |counts| {
                counts.1 += 1;
                accepted.take().unwrap()
            },
        );
        (result, counts)
    };
    let incomplete = || TrustRefusal {
        row: TrustRow::Incomplete,
        cause: "x".into(),
    };
    // A view: nothing else runs.
    assert_eq!(play((vec![Ok(1)], Ok(()))), (Ok(1), (1, 0)));
    // Any refusal but F absent: returned as is, nothing else runs.
    assert_eq!(
        play((vec![Err(incomplete())], Ok(()))),
        (Err(incomplete()), (1, 0))
    );
    // F absent, then an acceptance refusal: no confirming admission.
    assert_eq!(
        play((vec![Err(f_absent("p0"))], Err(incomplete()))),
        (Err(incomplete()), (1, 1))
    );
    // F absent, accepted, then the one confirming admission's result.
    assert_eq!(
        play((vec![Err(f_absent("p0")), Ok(2)], Ok(()))),
        (Ok(2), (2, 1))
    );
    assert_eq!(
        play((vec![Err(f_absent("p0")), Err(incomplete())], Ok(()))),
        (Err(incomplete()), (2, 1))
    );
    // A second F absent is the host invariant row; no third admission.
    let (result, counts) = play((vec![Err(f_absent("p0")), Err(f_absent("again"))], Ok(())));
    assert_eq!(counts, (2, 1));
    let refusal = result.unwrap_err();
    assert_eq!(refusal.row, TrustRow::Invariant);
    assert!(
        refusal.cause.contains("second-f-absent"),
        "{}",
        refusal.cause
    );
    assert_eq!(TrustRow::Invariant.code(), "HOST.INVARIANT_VIOLATED");
    assert_eq!(TrustRow::Invariant.subject(), None);
}

#[test]
fn only_the_write_receipt_lends_a_source_and_only_the_lease_free_read_uses_it() {
    // Source pins: the read side has no bootstrap lending, and the branch is
    // reached only through the lease-free point's first read.
    let premise = include_str!("../custody/read_premise.rs");
    let write = premise.find("impl PlatformReceipt<Write>").unwrap();
    let lend = premise.find("pub(crate) fn bootstrap_source").unwrap();
    assert_eq!(premise.matches("fn bootstrap_source").count(), 1);
    assert!(lend > write);
    assert!(premise[write..lend].find("\nimpl ").is_none());
    let live = include_str!("live_observation.rs");
    assert_eq!(live.matches("bootstrapping_first_read(").count(), 1);
    let handoff = include_str!("../custody/operation_handoff.rs");
    assert_eq!(handoff.matches("fenced_operation_read(").count(), 1);
    let this = include_str!("trust_bootstrap.rs");
    assert_eq!(this.matches("accept_bootstrap(work").count(), 1);
    // The test-only source exists in no non-test build.
    assert!(this.contains("#[cfg(test)]\n    pub(crate) fn unreached()"));
    for reader in [
        include_str!("../custody/installation_session.rs"),
        include_str!("../custody/read_premise.rs"),
    ] {
        assert!(!reader.contains("fenced_operation_read"));
        assert!(!reader.contains("bootstrapping_first_read"));
    }
}

/// C2-T6's C2a-2 leg (M3-C r8 item 8; C2a plan r4, LD-C2A-6): a signed release
/// with one synthetic component of every role, each declaring C2PM-1's major,
/// is produced into an InitialCore, accepted onto a P0 installation, and read
/// back from the accepted store by the full ordinary reader (each body
/// validated under its host context). C2a-1's bridge lends each verified
/// component, and its candidate projects for every role (the analyzer under
/// a test-selected subprotocol). Retention (C2a-3's verifier) is not claimed.
#[test]
fn c2a2_every_role_admits_through_the_ordinary_reader_into_a_candidate() {
    use super::super::super::super::core_authentication::tests::components::{ROLES, every_role};
    use super::super::super::super::ordinary_metadata as MD;
    use crate::component_closure::{AnalyzerSubprotocol, SelectedPlatform, component_candidate};
    crate::test_scratch::settled(|| {
        let bodies = every_role();
        let signers = [Some(COMPONENT_SIGNER); 5];
        let (payload, closure) = payload_of(
            "c2a2-every-role",
            &ReleaseSpec {
                link: false,
                components: &bodies,
                component_signers: &signers,
                ..release()
            },
        );
        let site = p0_site(&closure);
        let mut owner = bound(&site);
        let obs = observation("2026-10-02T00:00:00Z");
        accept(&site, &mut owner, &payload, &obs).unwrap();
        let store = files(&site.root);
        // The accepted ordinary-inert closure and its signing root.
        let inert: Vec<&Vec<u8>> = store
            .iter()
            .filter(|((c, _), raw)| {
                *c == Collection::Records
                    && opensip_identity::parse_json(raw).is_ok_and(|v| {
                        map(&v).is_ok_and(|m| m.get("scope") == Some(&s("ordinary-inert")))
                    })
            })
            .map(|(_, raw)| raw)
            .collect();
        assert_eq!(inert.len(), 1);
        let closure_ref = reference(inert[0]);
        let closure_value = opensip_identity::parse_json(inert[0]).unwrap();
        let chain = list(&map(&closure_value).unwrap()["rootChain"]).unwrap();
        let signing_root_ref = chain.last().unwrap().clone();
        let root_body = &store[&(
            Collection::Objects,
            sha(&map(&signing_root_ref).unwrap()["body"]),
        )];
        let root = super::super::super::super::admit(
            &crate::trust::metadata::parse(root_body).unwrap(),
            [true, true],
        )
        .unwrap();
        let contexts: BTreeMap<String, MD::HostContext> =
            list(&map(&closure_value).unwrap()["members"])
                .unwrap()
                .iter()
                .filter(|m| map(m).unwrap()["slot"] == s("manifests"))
                .map(|m| {
                    (
                        text(&map(m).unwrap()["path"]).unwrap().to_owned(),
                        MD::HostContext {
                            approved_exceptions: BTreeSet::new(),
                            host_classifications: BTreeMap::new(),
                            live_names: Vec::new(),
                        },
                    )
                })
                .collect();
        assert_eq!(contexts.len(), 5);
        let mut capture =
            |c: Collection, h: [u8; 32], _cap: usize| store.get(&(c, h)).cloned().ok_or(());
        let mut budget = Budget::new(65_536, 131_072, 268_435_456).unwrap();
        let evidence = MD::prepare(
            &mut budget,
            &closure_ref,
            &signing_root_ref,
            &root,
            &BTreeSet::new(),
            &contexts,
            &mut capture,
        )
        .unwrap();
        let selected = AnalyzerSubprotocol::selected_for_tests(1);
        let platform = SelectedPlatform {
            os: "macos",
            arch: "arm64",
        };
        let mut kinds = Vec::new();
        for component in evidence.admitted_components() {
            let role = text(&map(component.manifest()).unwrap()["role"])
                .unwrap()
                .to_owned();
            let analyzer = (role == "analyzer").then_some(&selected);
            let candidate = WorkLedger::new()
                .scope(|work| {
                    component_candidate(
                        &component,
                        platform,
                        analyzer,
                        crate::component_closure::tests::registry(),
                        work,
                    )
                })
                .unwrap_or_else(|f| panic!("{role}: {f:?}"));
            assert!(candidate.closure().starts_with("closure2:"));
            assert_eq!(candidate.manifest_digest(), raw_sha256(component.body()));
            assert_eq!(candidate.blobs().count(), 2);
            kinds.push(component.closure_kind());
        }
        kinds.sort_unstable();
        let mut want: Vec<&str> = ROLES
            .iter()
            .map(|r| if *r == "analyzer" { "provider" } else { r })
            .collect();
        want.sort_unstable();
        assert_eq!(kinds, want);
    });
}
