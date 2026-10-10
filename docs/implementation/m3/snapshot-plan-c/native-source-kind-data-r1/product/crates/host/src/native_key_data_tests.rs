use super::*;

fn kind(value: &str) -> SourceKind {
    match value {
        "registry" => SourceKind::Registry,
        "git" => SourceKind::Git,
        "path" => SourceKind::Path,
        "vendored" => SourceKind::Vendored,
        _ => panic!("invalid independent fixture kind"),
    }
}

#[test]
fn independent_whole_preimage_and_raw_sha_vectors() {
    let fixture: serde_json::Value =
        serde_json::from_str(include_str!("native_key_data/fixtures/golden.json")).unwrap();
    for row in fixture["vectors"].as_array().unwrap() {
        let source = match row["source"].as_str().unwrap() {
            "snapshot-member" => SourceClass::SnapshotMember,
            "dependency-closure-member" => SourceClass::DependencyClosureMember,
            _ => panic!("invalid independent fixture source"),
        };
        let locator = row["snapshotManifestPath"]
            .as_str()
            .map(|p| LogicalPath::parse(p).unwrap());
        let (p, o) = owner(
            row["name"].as_str().unwrap(),
            row["version"].as_str().unwrap(),
            row["sourceId"].as_str().unwrap(),
            source,
            kind(row["sourceKind"].as_str().unwrap()),
            locator.as_ref(),
        )
        .unwrap();
        assert_eq!(
            p.canonical_preimage,
            row["packagePreimage"].as_str().unwrap().as_bytes()
        );
        assert_eq!(
            o.canonical_preimage,
            row["ownerPreimage"].as_str().unwrap().as_bytes()
        );
        assert_eq!(p.key, row["packageKey"].as_str().unwrap());
        assert_eq!(o.key, row["ownerKey"].as_str().unwrap());
        for (data, prefix) in [(&p, "pkg1-"), (&o, "own2-")] {
            assert_eq!(data.key.len(), 69);
            assert!(data.key.starts_with(prefix));
            assert!(
                data.key[5..]
                    .bytes()
                    .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
            );
            assert_eq!(LogicalPath::parse(&data.key).unwrap().as_str(), data.key);
        }
    }
}

#[test]
fn exact_unicode_scalar_bounds_not_utf8_or_normalized_values() {
    let name = "λ".repeat(256);
    let version = "🦀".repeat(256);
    let source = "原".repeat(4096);
    let data = package(&name, &version, &source).unwrap();
    assert!(data.canonical_preimage.len() > 4096);
    assert!(matches!(package("", "v", ""), Err(KeyError::NameLength)));
    assert!(matches!(
        package(&"λ".repeat(257), "v", ""),
        Err(KeyError::NameLength)
    ));
    assert!(matches!(package("n", "", ""), Err(KeyError::VersionLength)));
    assert!(matches!(
        package("n", &"🦀".repeat(257), ""),
        Err(KeyError::VersionLength)
    ));
    assert!(matches!(
        package("n", "v", &"原".repeat(4097)),
        Err(KeyError::SourceIdLength)
    ));
    assert_ne!(
        package("é", "v", "").unwrap().key,
        package("e\u{301}", "v", "").unwrap().key
    );
    assert_ne!(
        package(" name ", "not-semver", "").unwrap().key,
        package("name", "not-semver", "").unwrap().key
    );
}

#[test]
fn raw_tuple_boundary_and_source_spelling_are_preserved() {
    assert_ne!(
        package("ab", "c", "").unwrap().key,
        package("a", "bc", "").unwrap().key
    );
    assert_ne!(
        package("n", "v", "registry+https://x.invalid/i")
            .unwrap()
            .key,
        package("n", "v", "registry+https://x.invalid/i/")
            .unwrap()
            .key
    );
    assert_ne!(
        package("n", "v", "git+https://x.invalid/r#one")
            .unwrap()
            .key,
        package("n", "v", "git+https://x.invalid/r#two")
            .unwrap()
            .key
    );
    let p = package("n", "v", "").unwrap();
    assert_eq!(p.canonical_preimage, b"[\"n\",\"v\",\"\"]");
    let value = JsonValue::Array(vec![
        JsonValue::String("n".to_owned()),
        JsonValue::String("v".to_owned()),
        JsonValue::String(String::new()),
    ]);
    let frame = opensip_identity::hash_preimage("native.test-only-difference", &value).unwrap();
    assert_ne!(p.key, format!("pkg1-{}", digest_hex(&raw_sha256(&frame))));
}

#[test]
fn equal_scoped_package_keys_distinct_manifest_or_source_owners() {
    let a = LogicalPath::parse("a/Cargo.toml").unwrap();
    let b = LogicalPath::parse("b/Cargo.toml").unwrap();
    let (pa, oa) = owner(
        "n",
        "v",
        "",
        SourceClass::SnapshotMember,
        SourceKind::Path,
        Some(&a),
    )
    .unwrap();
    let (pb, ob) = owner(
        "n",
        "v",
        "",
        SourceClass::SnapshotMember,
        SourceKind::Path,
        Some(&b),
    )
    .unwrap();
    assert_eq!(pa.key, pb.key);
    assert_ne!(oa.key, ob.key);
    let (_, dep) = owner(
        "n",
        "v",
        "",
        SourceClass::DependencyClosureMember,
        SourceKind::Path,
        Some(&a),
    )
    .unwrap();
    assert_ne!(oa.key, dep.key);
    let (_, again) = owner(
        "n",
        "v",
        "",
        SourceClass::SnapshotMember,
        SourceKind::Path,
        Some(&a),
    )
    .unwrap();
    assert_eq!(oa.key, again.key); // Content is deliberately outside the key recipe.
}

#[test]
fn all_selected_shape_refusals_before_owner_recipe() {
    let good = LogicalPath::parse("Cargo.toml").unwrap();
    let wrong = LogicalPath::parse("nested/Cargo.toml.bak").unwrap();
    for source in [
        SourceClass::SnapshotMember,
        SourceClass::DependencyClosureMember,
    ] {
        assert!(matches!(
            owner("n", "v", "", source, SourceKind::Path, None),
            Err(KeyError::OwnerShape)
        ));
        assert!(matches!(
            owner("n", "v", "", source, SourceKind::Path, Some(&wrong)),
            Err(KeyError::OwnerShape)
        ));
        assert!(matches!(
            owner("n", "v", "nonempty", source, SourceKind::Path, Some(&good)),
            Err(KeyError::OwnerShape)
        ));
        for kind in [SourceKind::Registry, SourceKind::Git, SourceKind::Vendored] {
            assert!(matches!(
                owner("n", "v", "s", source, kind, Some(&good)),
                Err(KeyError::OwnerShape)
            ));
        }
    }
    for kind in [SourceKind::Registry, SourceKind::Git, SourceKind::Vendored] {
        assert!(matches!(
            owner("n", "v", "s", SourceClass::SnapshotMember, kind, None),
            Err(KeyError::OwnerShape)
        ));
        assert!(
            owner(
                "n",
                "v",
                "s",
                SourceClass::DependencyClosureMember,
                kind,
                None
            )
            .is_ok()
        );
    }
}

#[test]
fn source_kind_is_shape_not_a_new_preimage_member_or_source_parser() {
    let (_, r) = owner(
        "n",
        "v",
        "exact raw source",
        SourceClass::DependencyClosureMember,
        SourceKind::Registry,
        None,
    )
    .unwrap();
    let (_, v) = owner(
        "n",
        "v",
        "exact raw source",
        SourceClass::DependencyClosureMember,
        SourceKind::Vendored,
        None,
    )
    .unwrap();
    assert_eq!(r.canonical_preimage, v.canonical_preimage);
    assert_eq!(r.key, v.key);
    assert!(r.canonical_preimage.ends_with(b",null]"));
    assert!(matches!(
        owner(
            "",
            "v",
            "s",
            SourceClass::DependencyClosureMember,
            SourceKind::Git,
            None
        ),
        Err(KeyError::NameLength)
    ));
    assert!(LogicalPath::parse("/Cargo.toml").is_err());
    assert!(LogicalPath::parse("a/../Cargo.toml").is_err());
    let lookalike = LogicalPath::parse("Ｃargo.toml").unwrap();
    assert!(matches!(
        owner(
            "n",
            "v",
            "",
            SourceClass::SnapshotMember,
            SourceKind::Path,
            Some(&lookalike)
        ),
        Err(KeyError::OwnerShape)
    ));
}

#[test]
fn selected_nsk1_table_and_every_disallowed_acquisition_pair() {
    use AcquisitionMode as A;
    use OriginalSourceFamily as F;
    use SourceKind as K;
    let table = [
        (F::Registry, [Some(K::Registry), Some(K::Vendored), None]),
        (
            F::SparseRegistry,
            [Some(K::Registry), Some(K::Vendored), None],
        ),
        (F::Git, [Some(K::Git), Some(K::Vendored), None]),
        (F::Path, [None, None, Some(K::Path)]),
    ];
    for (family, expected) in table {
        for (mode, expected) in [
            A::ImportedDescriptor,
            A::InSnapshotVendored,
            A::InSnapshotPath,
        ]
        .into_iter()
        .zip(expected)
        {
            for advertised in [K::Registry, K::Git, K::Path, K::Vendored] {
                let result = classify_source_kind_data(Some(family), Some(mode), Some(advertised));
                match expected {
                    None => assert_eq!(result, Err(SourceKindDataError::InvalidCombination)),
                    Some(kind) if kind == advertised => assert_eq!(result, Ok(kind)),
                    Some(_) => {
                        assert_eq!(result, Err(SourceKindDataError::ConflictingAdvertisedKind))
                    }
                }
            }
        }
    }
}

#[test]
fn missing_source_kind_inputs_do_not_default_to_registry_vendored_or_path() {
    use AcquisitionMode as A;
    use OriginalSourceFamily as F;
    assert_eq!(
        classify_source_kind_data(
            None,
            Some(A::ImportedDescriptor),
            Some(SourceKind::Registry)
        ),
        Err(SourceKindDataError::MissingFamily)
    );
    assert_eq!(
        classify_source_kind_data(Some(F::Registry), None, Some(SourceKind::Registry)),
        Err(SourceKindDataError::MissingAcquisition)
    );
    assert_eq!(
        classify_source_kind_data(Some(F::Registry), Some(A::ImportedDescriptor), None),
        Err(SourceKindDataError::MissingAdvertisedKind)
    );
}

#[test]
fn acquisition_labels_do_not_modify_raw_package_or_owner_preimages() {
    use AcquisitionMode as A;
    use OriginalSourceFamily as F;
    let raw = "sparse+https://index.crates.io/";
    let imported = classify_source_kind_data(
        Some(F::SparseRegistry),
        Some(A::ImportedDescriptor),
        Some(SourceKind::Registry),
    )
    .unwrap();
    let vendored = classify_source_kind_data(
        Some(F::SparseRegistry),
        Some(A::InSnapshotVendored),
        Some(SourceKind::Vendored),
    )
    .unwrap();
    let (p1, o1) = owner(
        "same",
        "1.2.3",
        raw,
        SourceClass::DependencyClosureMember,
        imported,
        None,
    )
    .unwrap();
    let (p2, o2) = owner(
        "same",
        "1.2.3",
        raw,
        SourceClass::DependencyClosureMember,
        vendored,
        None,
    )
    .unwrap();
    assert_eq!(
        p1.canonical_preimage,
        b"[\"same\",\"1.2.3\",\"sparse+https://index.crates.io/\"]"
    );
    assert_eq!(p1.key, p2.key);
    assert_eq!(o1.canonical_preimage, o2.canonical_preimage);
    assert_eq!(o1.key, o2.key);
    assert!(
        owner(
            "same",
            "1.2.3",
            raw,
            SourceClass::SnapshotMember,
            vendored,
            None
        )
        .is_err()
    );
}
