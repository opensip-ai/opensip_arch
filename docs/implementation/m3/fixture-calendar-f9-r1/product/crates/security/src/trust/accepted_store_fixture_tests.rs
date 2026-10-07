use super::*;
use super::super::retained_metadata_index::Budget;

fn budget() -> Budget<'static, 'static> {
    Budget::new(65536, 131072, 268435456).unwrap()
}
fn map_store(
    store: &AcceptedStore,
) -> impl FnMut(Collection, [u8; 32], usize) -> Result<Vec<u8>, ()> + '_ {
    move |c, h, cap| {
        let raw = store.lookup(c, h).ok_or(())?;
        if raw.len() > cap {
            return Err(());
        }
        Ok(raw)
    }
}
fn all_targets() -> [RoleTarget; 6] {
    [
        RoleTarget::Trusted,
        RoleTarget::Revoked,
        RoleTarget::QuorumLost,
        RoleTarget::Trusted,
        RoleTarget::Expired,
        RoleTarget::StaleRevocation,
    ]
}

#[test]
fn every_record_passes_its_closed_shape_and_its_content_address() {
    let store = generate(&Spec::default());
    for file in &store.files {
        if file.collection.is_some() {
            let hash = digest_hex(&raw_sha256(&file.bytes));
            assert!(file.path.ends_with(&hash), "{} addressed by digest", file.path);
            let value = opensip_identity::parse_json(&file.bytes).unwrap();
            assert_eq!(canonical_bytes(&value).unwrap(), file.bytes, "{} canonical", file.path);
        }
    }
    let shaped = |prefix: &str, d: Definition| {
        let mut n = 0;
        for f in store.files.iter().filter(|f| f.path.starts_with(prefix)) {
            if shapes::admit(d, &f.bytes).is_ok() {
                n += 1;
            }
        }
        n
    };
    // P0's creation event plus the clock write plus four role acceptances.
    assert_eq!(shaped(&format!("trust/stores/{STORE}/events/"), Definition::TrustEventV1), 6);
    assert_eq!(shaped("trust/records/", Definition::RootAdmissionNodeV1), 1);
    assert_eq!(shaped("trust/records/", Definition::MetadataAdmissionNodeV1), 2);
    assert_eq!(shaped("trust/records/", Definition::RevocationHistoryNodeV1), 1);
    assert_eq!(shaped("trust/records/", Definition::TimeEvidenceV1), 1);
    assert_eq!(shaped("trust/records/", Definition::PayloadMetadataClosureV1), 1);
    let current = store
        .files
        .iter()
        .find(|f| f.path == format!("trust/stores/{STORE}/state.v1"))
        .unwrap();
    shapes::admit(Definition::TrustCapsuleV1, &current.bytes).unwrap();
    assert_eq!(
        opensip_identity::parse_json(&current.bytes).unwrap(),
        store.capsule
    );
}

#[test]
fn signed_documents_carry_real_quorum_signatures() {
    let store = generate(&Spec::default());
    let capsule = o(&store.capsule);
    let heads = o(&capsule["heads"]);
    // Each head's envelope signs exactly its body, by the role that owns it.
    for (head, role) in [("root", "ROOT"), ("catalog", "TR-INDEX"), ("revocation", "ROOT")] {
        let document = o(&o(&heads[head])["document"]);
        let hash = |r: &V| super::super::decode_hex32(match &o(r)["sha256"] {
            V::String(s) => s,
            _ => panic!(),
        })
        .unwrap();
        let body = store.lookup(Collection::Objects, hash(&document["body"])).unwrap();
        let envelope = store
            .lookup(Collection::Objects, hash(&document["envelope"]))
            .unwrap();
        let env = opensip_identity::parse_json(&envelope).unwrap();
        let env = o(&env);
        assert_eq!(env["role"], s(role), "{head} role");
        let subject = o(&env["subject"]);
        assert_eq!(
            subject["storedSha256"],
            s(&digest_hex(&raw_sha256(&body))),
            "{head} subject pins its body"
        );
        let message = crate::trust::envelope_message(&V::Object(env.clone())).unwrap();
        let V::Array(signatures) = &env["signatures"] else { panic!() };
        assert!(signatures.len() >= 2, "{head} quorum");
        let keys: BTreeMap<String, String> = match &o(&store.root)["keys"] {
            V::Array(a) => a
                .iter()
                .map(|k| match (&o(k)["keyId"], &o(k)["publicKey"]) {
                    (V::String(id), V::String(pk)) => (id.clone(), pk.clone()),
                    _ => panic!(),
                })
                .collect(),
            _ => panic!(),
        };
        for signature in signatures {
            use ed25519_dalek::{Signature, Verifier, VerifyingKey};
            let sig = o(signature);
            let (V::String(id), V::String(value)) = (&sig["keyId"], &sig["signature"]) else {
                panic!()
            };
            let pk: Vec<u8> = (0..64)
                .step_by(2)
                .map(|i| u8::from_str_radix(&keys[id][i..i + 2], 16).unwrap())
                .collect();
            let raw: Vec<u8> = (0..128)
                .step_by(2)
                .map(|i| u8::from_str_radix(&value[i..i + 2], 16).unwrap())
                .collect();
            VerifyingKey::from_bytes(&pk.try_into().unwrap())
                .unwrap()
                .verify(&message, &Signature::from_slice(&raw).unwrap())
                .unwrap_or_else(|_| panic!("{head} signature by {id}"));
        }
    }
}

#[test]
fn the_reference_binders_accept_the_generated_store() {
    for spec in [
        Spec::default(),
        Spec {
            roles: all_targets(),
            state_schema: 2,
            ..Spec::default()
        },
    ] {
        let store = generate(&spec);
        // current_record_bindings::bind over the capsule and its descriptor.
        let mut b = budget();
        let bound = super::super::current_record_bindings::bind(
            &mut b,
            &store.store,
            &store.capsule,
            &store.descriptor,
            &mut map_store(&store),
        )
        .unwrap();
        assert_eq!(bound.projection().capsule(), &store.capsule);
        // publication_events::bind_events, from P0's roles and event head.
        let p0 = o(&store.p0_capsule);
        let mut b = budget();
        let evidence = super::super::publication_events::bind_events(
            &mut b,
            &store.descriptor,
            &p0["roles"],
            &p0["eventHead"],
            &mut map_store(&store),
        )
        .unwrap();
        assert_eq!(evidence.roles(), &o(&store.capsule)["roles"]);
        assert_eq!(evidence.event_head(), &o(&store.capsule)["eventHead"]);
        // bind_retained_head through the capsule clock.
        let mut b = budget();
        let clock = super::super::admitted_trust_records::capsule_clock(
            &mut b,
            &store.capsule,
            &store.descriptor,
            None,
        )
        .unwrap();
        let head =
            super::super::ordinary_roots::bind_retained_head(&mut b, clock, &mut map_store(&store))
                .unwrap();
        assert_eq!(head.body(), store.root_body.as_slice());
        assert_eq!(head.root().value(), &store.root);
    }
}

/// X4T-a3: an n-root recorded chain. The closure lists roots 1 to n, the
/// head is root n with its counters, every link carries both key sets, and
/// the reference binders accept the store.
#[test]
fn a_recorded_rotation_lists_the_chain_with_the_head_last() {
    for n in [2, 3] {
        let store = generate(&Spec {
            roots: n,
            ..Spec::default()
        });
        let capsule = o(&store.capsule);
        let head = o(&o(&capsule["heads"])["root"]);
        let version = V::Integer(JsonInteger::new(n as i128).unwrap());
        assert_eq!(o(&head["binding"])["rootVersion"], version);
        assert_eq!(o(&o(&capsule["clock"])["record"])["rootVersion"], version);
        assert_eq!(o(&store.root)["rootVersion"], version);
        let lookup = |collection, r: &V| {
            let V::String(h) = &o(r)["sha256"] else { panic!() };
            store
                .lookup(collection, super::super::decode_hex32(h).unwrap())
                .unwrap()
        };
        let admission =
            opensip_identity::parse_json(&lookup(Collection::Records, &head["admission"])).unwrap();
        assert_eq!(o(&admission)["root"], head["document"]);
        let closure =
            opensip_identity::parse_json(&lookup(Collection::Records, &o(&admission)["parent"]))
                .unwrap();
        let V::Array(chain) = &o(&closure)["rootChain"] else { panic!() };
        assert_eq!(chain.len(), n);
        assert_eq!(chain.last(), Some(&head["document"]));
        for (k, doc) in chain.iter().enumerate() {
            let body = opensip_identity::parse_json(&lookup(Collection::Objects, &o(doc)["body"]))
                .unwrap();
            assert_eq!(o(&body)["rootVersion"], V::Integer(JsonInteger::new(k as i128 + 1).unwrap()));
            let envelope =
                opensip_identity::parse_json(&lookup(Collection::Objects, &o(doc)["envelope"]))
                    .unwrap();
            let V::Array(signatures) = &o(&envelope)["signatures"] else { panic!() };
            assert_eq!(signatures.len(), if k == 0 { 3 } else { 6 }, "root {k}");
        }
        // The list is signed under root n.
        let revocation = o(&o(&capsule["heads"])["revocation"]);
        let list = opensip_identity::parse_json(&lookup(
            Collection::Objects,
            &o(&revocation["document"])["body"],
        ))
        .unwrap();
        assert_eq!(o(&list)["rootVersion"], version);
        let mut b = budget();
        let bound = super::super::current_record_bindings::bind(
            &mut b,
            &store.store,
            &store.capsule,
            &store.descriptor,
            &mut map_store(&store),
        )
        .unwrap();
        assert_eq!(bound.projection().capsule(), &store.capsule);
        let mut b = budget();
        let clock = super::super::admitted_trust_records::capsule_clock(
            &mut b,
            &store.capsule,
            &store.descriptor,
            None,
        )
        .unwrap();
        let head =
            super::super::ordinary_roots::bind_retained_head(&mut b, clock, &mut map_store(&store))
                .unwrap();
        assert_eq!(head.root().value(), &store.root);
        assert_eq!(head.body(), store.root_body.as_slice());
    }
}

#[test]
fn chosen_role_states_are_published_with_their_evidence() {
    let store = generate(&Spec {
        roles: all_targets(),
        state_schema: 1,
        ..Spec::default()
    });
    let roles = o(&o(&store.capsule)["roles"]);
    for (role, target) in ROLES.iter().zip(all_targets()) {
        let r = o(&roles[*role]);
        assert_eq!(r["state"], s(target.token()), "{role}");
        let accepted = o(&r["accepted"]);
        assert_eq!(
            accepted["catalog"] != V::Null,
            *role == "TR-INDEX",
            "{role} catalog"
        );
        let condition = o(&r["conditionEvidence"]);
        assert_eq!(
            condition["revokedBy"] != V::Null,
            target == RoleTarget::Revoked,
            "{role} revokedBy"
        );
        assert_eq!(
            condition["quorumLostBy"] != V::Null,
            target == RoleTarget::QuorumLost,
            "{role} quorumLostBy"
        );
        // Every accepted standing names the event that accepted it.
        let by = o(&accepted["by"]);
        let V::String(h) = &by["sha256"] else { panic!() };
        let raw = store
            .lookup(Collection::Events, super::super::decode_hex32(h).unwrap())
            .unwrap();
        let event = opensip_identity::parse_json(&raw).unwrap();
        assert_eq!(o(&event)["role"], s(role));
        assert_eq!(o(&event)["to"], s("ST-TRUSTED"));
    }
    // Unbootstrapped roles stay blank.
    let store = generate(&Spec::default());
    let roles = o(&o(&store.capsule)["roles"]);
    for role in ["TR-PROFILE", "TR-REPAIR"] {
        assert_eq!(roles[role], blank_role(), "{role}");
    }
}

#[test]
#[should_panic(expected = "accepted role history")]
fn a_store_with_no_accepted_role_is_not_offered() {
    generate(&Spec {
        roles: [RoleTarget::Unbootstrapped; 6],
        state_schema: 1,
        ..Spec::default()
    });
}

#[cfg(target_os = "macos")]
#[test]
fn capture_p2_accepts_the_written_store_through_the_native_fence() {
    use crate::custody::installation_fence::SuppliedInstallationFence;
    use opensip_platform::RetainedDirectoryPath;
    use std::fs::{self, Permissions};
    use std::os::unix::fs::{MetadataExt, PermissionsExt};
    use std::sync::Arc;
    let id = digest_hex(&raw_sha256(&opensip_platform::request_entropy().unwrap()));
    let root = crate::test_scratch::acl_scratch().join(format!("opensip-accepted-store-{id}"));
    fs::create_dir(&root).unwrap();
    fs::set_permissions(&root, Permissions::from_mode(0o700)).unwrap();
    let root = fs::canonicalize(root).unwrap();
    let uid = fs::metadata(&root).unwrap().uid();
    fs::write(root.join("lifecycle.fence"), b"").unwrap();
    fs::set_permissions(root.join("lifecycle.fence"), Permissions::from_mode(0o600)).unwrap();
    let store = generate(&Spec {
        roles: all_targets(),
        state_schema: 1,
        ..Spec::default()
    });
    store.write(&root);
    let path = Arc::new(RetainedDirectoryPath::open(&root, 128).unwrap());
    let fence = SuppliedInstallationFence::try_acquire(path, uid, &std::collections::BTreeSet::new())
        .unwrap()
        .unwrap();
    let mut b = budget();
    let current = super::super::native_current::capture_p2(&mut b, &fence, &store.store);
    let current = current.unwrap();
    assert_eq!(current.descriptor().value(), &store.descriptor);
    assert_eq!(current.bindings().projection().capsule(), &store.capsule);
    current.recheck().unwrap();
    drop(current);
    drop(fence);
    let _ = fs::remove_dir_all(&root);
}

#[test]
fn no_production_source_reaches_the_constructor() {
    // The module is declared only under the shared fixture gates' joint
    // predicate (law X8 r3 item 4b; unit X9-1 pins every such site in
    // `crash_matrix_sites.rs`): `cfg(test)`, or a test-only feature that no
    // manifest enables and that never reaches a release build. No other file
    // names it.
    let root = Path::new(env!("CARGO_MANIFEST_DIR")).join("src");
    let declaration = std::fs::read_to_string(root.join("trust/root_payload.rs")).unwrap();
    let at = declaration.find("mod accepted_store_fixture").unwrap();
    assert!(
        declaration[..at].trim_end().ends_with(
            r#"#[cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))]"#
        ),
        "declared only under the joint predicate"
    );
    let mut stack = vec![root];
    while let Some(dir) = stack.pop() {
        for entry in std::fs::read_dir(dir).unwrap() {
            let path = entry.unwrap().path();
            if path.is_dir() {
                stack.push(path);
                continue;
            }
            let name = path.file_name().unwrap().to_string_lossy().into_owned();
            // The X9-1 site pin names it in its list.
            if name.starts_with("accepted_store_fixture")
                || name == "root_payload.rs"
                || name == "crash_matrix_sites.rs"
            {
                continue;
            }
            // X4T r5 item 12 (and r9, X4T-b): X4T-a's and X4T-b's tests use the
            // generator. Each file is included only under cfg(test), which is
            // checked here.
            let tested = [
                ("current_trust_admission_tests.rs", "current_trust_admission.rs"),
                ("floor_publication_tests.rs", "floor_publication.rs"),
            ];
            if let Some((tests, owner)) = tested.iter().find(|(tests, _)| name == *tests) {
                let owner = std::fs::read_to_string(path.with_file_name(owner)).unwrap();
                let at = owner.find(&format!("include!(\"{tests}\")")).unwrap();
                assert!(
                    owner[..at].trim_end().ends_with("#[cfg(test)]\nmod tests {"),
                    "{tests} is included only under cfg(test)"
                );
                continue;
            }
            let text = std::fs::read_to_string(&path).unwrap_or_default();
            assert!(
                !text.contains("accepted_store_fixture"),
                "{} names the test constructor",
                path.display()
            );
        }
    }
}

/// X4B-c: the roles in `ROLES` order, from (bundle, component, core, index).
fn carried(b: RoleTarget, c: RoleTarget, k: RoleTarget, i: RoleTarget) -> [RoleTarget; 6] {
    [b, c, k, i, RoleTarget::Unbootstrapped, RoleTarget::Unbootstrapped]
}

/// X4B-c (law X4B r5 item 9): every request item 4's sequences reach is
/// X4B's producer's store. Each role's events are exactly its sequence, in
/// dispatch order, `accepted.by` names its EV-PRESENT-PAYLOAD and
/// `revokedBy` its EV-REVOKE, and the reference binders accept the store
/// (item 10's round trip).
#[cfg(target_os = "macos")]
#[test]
fn x4b_produces_every_request_its_sequences_reach() {
    use RoleTarget::*;
    const P: &str = "EV-PRESENT-PAYLOAD";
    const C: &str = "EV-CLOCK";
    const R: &str = "EV-REVOKE";
    let cases: Vec<(&str, Spec, [&[&str]; 4])> = vec![
        ("default", Spec::default(), [&[P], &[P], &[P], &[P]]),
        (
            "no component manifest",
            Spec {
                roles: carried(Trusted, Unbootstrapped, Trusted, Trusted),
                ..Spec::default()
            },
            [&[P], &[], &[P], &[P]],
        ),
        (
            "expired catalog",
            Spec {
                roles: carried(Trusted, Trusted, Trusted, Expired),
                ..Spec::default()
            },
            [&[P], &[P], &[P], &[P, C]],
        ),
        (
            "expired root",
            Spec {
                roles: carried(Expired, Expired, Expired, Expired),
                ..Spec::default()
            },
            [&[P, C], &[P, C], &[P, C], &[P, C]],
        ),
        (
            "stale revocation",
            Spec {
                roles: carried(StaleRevocation, StaleRevocation, StaleRevocation, StaleRevocation),
                ..Spec::default()
            },
            [&[P, C], &[P, C], &[P, C], &[P, C]],
        ),
        (
            "expired catalog and stale revocation",
            Spec {
                roles: carried(StaleRevocation, StaleRevocation, StaleRevocation, Expired),
                ..Spec::default()
            },
            [&[P, C], &[P, C], &[P, C], &[P, C]],
        ),
        (
            "revoked core",
            Spec {
                roles: carried(Trusted, Trusted, Revoked, Trusted),
                ..Spec::default()
            },
            [&[P], &[P], &[P, R], &[P]],
        ),
        (
            "expired and revoked",
            Spec {
                roles: carried(Expired, Revoked, Revoked, Expired),
                ..Spec::default()
            },
            [&[P, C], &[P, C, R], &[P, C, R], &[P, C]],
        ),
        (
            "revoked bundle on a rotated chain",
            Spec {
                roles: carried(Revoked, Trusted, Trusted, Trusted),
                roots: 2,
                ..Spec::default()
            },
            [&[P, R], &[P], &[P], &[P]],
        ),
        (
            "a successor list naming nothing carried",
            Spec {
                store: Some("33333333333333333333333333333333".into()),
                state_schema: 2,
                revocations: vec![("release", "closure2:".to_owned() + &"e".repeat(64))],
                revocation_version: 2,
                ..Spec::default()
            },
            [&[P], &[P], &[P], &[P]],
        ),
    ];
    for (label, spec, sequences) in cases {
        let store = generate(&spec);
        assert!(store.produced, "{label}: produced");
        let capsule = o(&store.capsule);
        let roles = o(&capsule["roles"]);
        let event = |r: &V| {
            let V::String(h) = &o(r)["sha256"] else { panic!() };
            let raw = store
                .lookup(Collection::Events, super::super::decode_hex32(h).unwrap())
                .unwrap();
            opensip_identity::parse_json(&raw).unwrap()
        };
        let V::Array(rows) = &o(&store.descriptor)["events"] else { panic!() };
        for (i, role) in ROLES.iter().enumerate() {
            let r = o(&roles[*role]);
            assert_eq!(r["state"], s(spec.roles[i].token()), "{label}: {role}");
            let mine: Vec<V> = rows
                .iter()
                .map(|row| event(&o(row)["event"]))
                .filter(|e| o(e).get("role") == Some(&s(role)))
                .collect();
            let names: Vec<&V> = mine.iter().map(|e| &o(e)["event"]).collect();
            let want: Vec<V> = sequences.get(i).map_or(&[][..], |w| *w).iter().map(|n| s(n)).collect();
            let want: Vec<&V> = want.iter().collect();
            assert_eq!(names, want, "{label}: {role} sequence");
            if want.is_empty() {
                assert_eq!(roles[*role], blank_role(), "{label}: {role} blank");
                continue;
            }
            assert_eq!(event(&o(&r["accepted"])["by"]), mine[0], "{label}: {role} accepted.by");
            let revoked_by = &o(&r["conditionEvidence"])["revokedBy"];
            if spec.roles[i] == Revoked {
                assert_eq!(event(revoked_by), *mine.last().unwrap(), "{label}: {role} revokedBy");
            } else {
                assert_eq!(*revoked_by, V::Null, "{label}: {role} revokedBy");
            }
        }
        let mut b = budget();
        let bound = super::super::current_record_bindings::bind(
            &mut b,
            &store.store,
            &store.capsule,
            &store.descriptor,
            &mut map_store(&store),
        )
        .unwrap();
        assert_eq!(bound.projection().capsule(), &store.capsule, "{label}");
        let p0 = o(&store.p0_capsule);
        let mut b = budget();
        let evidence = super::super::publication_events::bind_events(
            &mut b,
            &store.descriptor,
            &p0["roles"],
            &p0["eventHead"],
            &mut map_store(&store),
        )
        .unwrap();
        assert_eq!(evidence.roles(), &capsule["roles"], "{label}");
        let mut b = budget();
        let clock = super::super::admitted_trust_records::capsule_clock(
            &mut b,
            &store.capsule,
            &store.descriptor,
            None,
        )
        .unwrap();
        let head =
            super::super::ordinary_roots::bind_retained_head(&mut b, clock, &mut map_store(&store))
                .unwrap();
        assert_eq!(head.root().value(), &store.root, "{label}");
    }
    // S4 step 2 on the fixture's one sample: tEval = F = W, L = A.
    let store = generate(&Spec::default());
    let record = o(&o(&o(&store.capsule)["clock"])["record"]);
    assert_eq!(record["evalHighWater"], s("2026-10-02T00:00:00Z"));
    assert_eq!(record["lastAccepted"], s("2026-10-01T00:00:00Z"));
}

/// X4B-c: a request no acceptance reaches keeps this module's construction:
/// QuorumLost, an accepted TR-PROFILE or TR-REPAIR, an uncarried TR-INDEX,
/// a lone expired core or stale role, the unlawful X4T-a3 stores, and a
/// caller's own list entry that would revoke a role requested Trusted.
#[test]
fn a_request_no_acceptance_reaches_is_constructed() {
    use RoleTarget::*;
    let cases: Vec<(&str, Spec)> = vec![
        ("all targets", Spec { roles: all_targets(), ..Spec::default() }),
        ("six trusted", Spec { roles: [Trusted; 6], ..Spec::default() }),
        ("quorum lost", Spec { roles: carried(Trusted, Trusted, QuorumLost, Trusted), ..Spec::default() }),
        ("expired core alone", Spec { roles: carried(Trusted, Trusted, Expired, Trusted), ..Spec::default() }),
        ("stale component alone", Spec { roles: carried(Trusted, StaleRevocation, Trusted, Trusted), ..Spec::default() }),
        ("no index", Spec { roles: carried(Trusted, Trusted, Trusted, Unbootstrapped), ..Spec::default() }),
        ("other envelope", Spec { chain_end: ChainEnd::OtherEnvelope, ..Spec::default() }),
        ("replaced root signers", Spec { roots: 2, root_signers: vec![(1, &[20, 21, 22])], ..Spec::default() }),
        ("replaced list signers", Spec { roots: 2, revocation_signers: Some(&[0, 1]), ..Spec::default() }),
        ("a list revoking the core", Spec { revocations: vec![("release", CORE_CLOSURE.to_owned())], ..Spec::default() }),
    ];
    for (label, spec) in cases {
        let store = generate(&spec);
        assert!(!store.produced, "{label}: constructed");
        let roles = o(&o(&store.capsule)["roles"]);
        for (role, target) in ROLES.iter().zip(spec.roles) {
            assert_eq!(o(&roles[*role])["state"], s(target.token()), "{label}: {role}");
        }
    }
}

/// X4B-c: the producer's store builder is reached only by the producer's
/// own `build_acceptance` and by this test-only generator.
#[test]
fn only_the_producer_and_the_generator_call_the_store_builder() {
    let root = Path::new(env!("CARGO_MANIFEST_DIR")).join("src");
    let mut stack = vec![root];
    let mut callers = Vec::new();
    while let Some(dir) = stack.pop() {
        for entry in std::fs::read_dir(dir).unwrap() {
            let path = entry.unwrap().path();
            if path.is_dir() {
                stack.push(path);
                continue;
            }
            let text = std::fs::read_to_string(&path).unwrap_or_default();
            let n = text.matches(concat!("build_over_p0", "(")).count();
            if n > 0 {
                let name = path.file_name().unwrap().to_string_lossy().into_owned();
                callers.push((name, n));
            }
        }
    }
    callers.sort();
    assert_eq!(
        callers,
        [
            ("accepted_store_fixture.rs".to_owned(), 1),
            ("trust_bootstrap.rs".to_owned(), 2),
        ]
    );
}


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
