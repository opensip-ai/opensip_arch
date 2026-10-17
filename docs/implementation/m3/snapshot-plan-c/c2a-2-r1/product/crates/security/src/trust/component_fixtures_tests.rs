// C2a-2's controls (C2a plan r4, section 4): the role-valid bodies with their
// declarations and supplied trees, the labelled release rows, the
// pre-existing builders' unchanged bytes, the signed release of every role
// through the initial core, and the predicate and label pins.
use super::*;

fn parse(raw: &[u8]) -> V {
    opensip_identity::parse_json(raw).unwrap()
}

/// Every role's body passes the real body validation, declares major 1,
/// keeps its role's command and capability rules, and lists exactly the
/// supplied files, with their lengths and digests, beside their directories.
#[test]
fn c2a2_every_role_body_is_role_valid_with_its_declaration_and_tree() {
    for (body, role) in every_role().iter().zip(ROLES) {
        let validated = crate::trust::component_manifest::validate(
            body,
            &crate::trust::component_manifest::Context::default(),
        )
        .unwrap_or_else(|e| panic!("{role}: {e:?}"));
        let kind = if role == "analyzer" { "provider" } else { role };
        assert_eq!(validated.closure_kind(), kind);
        let m = o(validated.value());
        assert_eq!(s(&m["role"]), role);
        assert_eq!(count(&m["closureProtocolMajor"]), 1);
        assert_eq!(m.contains_key("commands"), role == "analyzer");
        let platform = o(&a(&m["platforms"])[0]);
        assert_eq!(
            (s(&platform["os"]), s(&platform["arch"])),
            ("macos", "arm64")
        );
        let entries = a(&o(&platform["tree"])["entries"]);
        let mut files = Vec::new();
        for e in entries {
            let e = o(e);
            match s(&e["type"]) {
                "dir" => assert!(["bin", "lib"].contains(&s(&e["path"]))),
                "file" => files.push((
                    s(&e["path"]).to_owned(),
                    count(&e["length"]),
                    s(&e["sha256"]).to_owned(),
                )),
                other => panic!("{other}"),
            }
        }
        let supplied: Vec<_> = FILES
            .iter()
            .map(|(path, raw)| {
                (
                    (*path).to_owned(),
                    raw.len(),
                    digest_hex(&opensip_identity::raw_sha256(raw)),
                )
            })
            .collect();
        assert_eq!(files, supplied, "{role}");
    }
    // An absent declaration stays absent (C2PM-1's projection refuses it).
    let absent = body(&Synthetic {
        major: None,
        ..Synthetic::of("toolchain", "1.0.9")
    });
    assert!(!o(&parse(&absent)).contains_key("closureProtocolMajor"));
}

/// C2-T8's label half: every synthetic artifact row carries `LABEL`, which
/// is `scenario.rs`'s label; each row joins its body by digest, identity
/// and envelope, and is signed only by the public test-only TR-COMPONENT
/// signer under the existing synthetic root.
#[test]
fn c2a2_release_rows_carry_the_label_and_join_their_bodies() {
    assert!(include_str!("../scenario.rs").contains("const LABEL: &str = \"synthetic\";"));
    assert_eq!(LABEL, "synthetic");
    let root = quorum_root(1);
    for raw in every_role() {
        let (env, release) = release(
            &raw,
            COMPONENT_SIGNER,
            &root,
            &["macos-arm64", "linux-x86_64"],
        );
        let row = parse(release.as_bytes());
        let r = o(&row);
        let artifacts = a(&r["artifacts"]);
        assert_eq!(artifacts.len(), 2);
        assert!(
            artifacts
                .iter()
                .all(|x| s(&o(x)["archiveProfileId"]) == LABEL)
        );
        assert_eq!(
            s(&r["manifestDigest"]),
            digest_hex(&opensip_identity::raw_sha256(&raw))
        );
        assert_eq!(
            s(&r["envelopeDigest"]),
            digest_hex(&opensip_identity::raw_sha256(&env))
        );
        let body = parse(&raw);
        assert_eq!(r["version"], o(&body)["version"]);
        assert_eq!(r["stableId"], o(&body)["stableId"]);
        let envelope = parse(&env);
        assert_eq!(s(&o(&envelope)["role"]), COMPONENT_SIGNER.0);
        assert_eq!(
            a(&o(&envelope)["signatures"]).len(),
            COMPONENT_SIGNER.1.len()
        );
    }
    assert_eq!(COMPONENT_SIGNER, ("TR-COMPONENT", &[14usize, 15][..]));
    assert_eq!(INDEX_SIGNER, ("TR-INDEX", &[11usize, 12][..]));
}

/// The pre-existing builders keep every byte (LD-C2A-6): `component_release`
/// through the shared module equals the row its earlier literal wrote, and an
/// empty `components` list leaves a signed release unchanged.
#[test]
fn c2a2_pre_existing_builders_keep_their_bytes() {
    let root = quorum_root(1);
    for i in 0..4 {
        let raw = component_body(i);
        let (env, release) = component_release(i, &raw, COMPONENT_SIGNER, &root);
        let carrier = crate::trust::metadata::parse(&env).unwrap();
        let preimage = super::super::super::verified_envelopes::parse_carrier(&carrier)
            .unwrap()
            .preimage_digest();
        // The literal `component_release` wrote before C2a-2.
        let earlier = format!(
            r#"{{"artifacts":[{{"archiveDigest":"{z}","archiveProfileId":"p1","platform":"macos-arm64","sha256":"{z}"}}],"envelopeDigest":"{}","hostCoreConstraint":{{"includeMax":false,"includeMin":true,"max":"0.2.0","min":"0.1.0"}},"manifestDigest":"{}","manifestPreimageSha256":"{}","publisher":"opensip","sourceClass":"first-party","stableId":"6f1c2c3e-0b6a-4a1c-9c2d-1f0e2a3b4c5d","version":"1.0.{i}"}}"#,
            digest_hex(&opensip_identity::raw_sha256(&env)),
            digest_hex(&opensip_identity::raw_sha256(&raw)),
            digest_hex(&preimage),
            z = "0".repeat(64),
        );
        assert_eq!(release, earlier, "{i}");
        assert_eq!(
            env,
            sign(
                &raw,
                "manifest",
                "opensip.metadata.manifest.1",
                COMPONENT_SIGNER.0,
                &root,
                COMPONENT_SIGNER.1
            )
        );
    }
    let before = signed_release(&Spec::default());
    let again = signed_release(&Spec {
        components: &[],
        ..Spec::default()
    });
    assert_eq!(before.bootstrap, again.bootstrap);
    assert_eq!(
        (before.inventory, before.record),
        (again.inventory, again.record)
    );
}

/// A signed release listing one component of every role: each body and its
/// envelope are retained by name, and the catalog lists one labelled release
/// row per body, joined by digest.
#[test]
fn c2a2_signed_release_of_every_role() {
    let bodies = every_role();
    let signers = [Some(COMPONENT_SIGNER); 5];
    let signed = signed_release(&Spec {
        components: &bodies,
        component_signers: &signers,
        ..Spec::default()
    });
    let catalog = parse(&signed.bootstrap["catalog.json"]);
    let releases = a(&o(&catalog)["releases"]);
    assert_eq!(releases.len(), 5);
    for (i, raw) in bodies.iter().enumerate() {
        assert_eq!(&signed.bootstrap[&format!("component-{i}.json")], raw);
        let env = &signed.bootstrap[&format!("component-{i}.sig.json")];
        let r = o(&releases[i]);
        assert_eq!(
            s(&r["manifestDigest"]),
            digest_hex(&opensip_identity::raw_sha256(raw))
        );
        assert_eq!(
            s(&r["envelopeDigest"]),
            digest_hex(&opensip_identity::raw_sha256(env))
        );
        assert!(
            a(&r["artifacts"])
                .iter()
                .all(|x| s(&o(x)["archiveProfileId"]) == LABEL)
        );
    }
}

/// C2-T7, the source pin over the predicate: the module is included only
/// inside `core_authentication.rs`'s `tests` module, under exactly
/// `cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))`,
/// and names no key, root or feature source of its own.
#[test]
fn c2a2_the_fixtures_exist_only_under_the_joint_predicate() {
    let host = include_str!("core_authentication.rs");
    let gate = "#[cfg(any(test, feature = \"crash-matrix\", feature = \"scenario-fixtures\"))]\npub(super) mod tests {\n";
    assert_eq!(host.matches(gate).count(), 1);
    let tests = host.find(gate).unwrap();
    let include = host.find("include!(\"component_fixtures.rs\")").unwrap();
    assert!(include > tests);
    assert_eq!(host.matches("component_fixtures.rs").count(), 1);
    let module = include_str!("component_fixtures.rs");
    let production = &module[..module.find("#[cfg(test)]\nmod tests").unwrap()];
    for forbidden in [
        "SigningKey",
        "seed",
        "include_bytes!",
        "quorum-roots",
        "feature =",
        "cfg(",
        "std::env",
        "env!(",
    ] {
        assert!(!production.contains(forbidden), "{forbidden}");
    }
}
