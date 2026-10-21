//! Synthetic native descriptors only; no acquisition/custody/Plan authority.
use super::*;
use opensip_identity::{JsonInteger, canonical_bytes, raw_sha256};
fn n(v: u64) -> J {
    J::Integer(JsonInteger::new(i128::from(v)).unwrap())
}
fn s(v: &str) -> J {
    J::String(v.into())
}
fn obj(v: Vec<(&str, J)>) -> J {
    J::Object(v.into_iter().map(|(k, v)| (k.into(), v)).collect())
}
fn reference_h(domain: &str, value: &J) -> String {
    let json = canonical_bytes(value).unwrap();
    let mut frame = b"opensip.product.v1\0".to_vec();
    frame.extend_from_slice(domain.as_bytes());
    frame.push(0);
    frame.extend_from_slice(&(json.len() as u64).to_be_bytes());
    frame.extend(json);
    digest_hex(&raw_sha256(&frame))
}
fn file(path: &str, length: u64) -> J {
    obj(vec![
        ("path", s(path)),
        ("byteLength", n(length)),
        ("contentSha256", s(&"a".repeat(64))),
    ])
}
struct Fixture {
    set: J,
    manifests: BTreeMap<String, J>,
    id: String,
}
impl Fixture {
    fn input(&self) -> Input<'_> {
        Input {
            set: &self.set,
            manifests: &self.manifests,
            set_id: &self.id,
        }
    }
    fn refresh(&mut self) {
        self.id = format!(
            "sha256:{}",
            reference_h("native.dependency-source-set.v1", &self.set)
        );
    }
}
type Spec<'a> = (&'a str, &'a str, &'a str, Vec<J>);
fn fixture(specs: Vec<Spec<'_>>) -> Fixture {
    let mut manifests = BTreeMap::new();
    let mut packages = Vec::new();
    for (name, version, source, rows) in specs {
        let count = rows.len() as u64;
        let bytes = rows.iter().fold(0_u64, |sum, row| {
            sum.saturating_add(number(field(row, "byteLength").unwrap()).unwrap())
        });
        let manifest = J::Array(rows);
        let digest = reference_h("native.dependency-file-manifest.v1", &manifest);
        manifests.insert(digest.clone(), manifest);
        packages.push(obj(vec![
            ("name", s(name)),
            ("version", s(version)),
            ("sourceId", s(source)),
            ("sourceKind", s("path")),
            ("lockChecksum", J::Null),
            ("fileManifestSha256", s(&digest)),
            ("fileCount", n(count)),
            ("totalBytes", n(bytes)),
            (
                "acquisition",
                obj(vec![
                    ("mode", s("in-snapshot-path")),
                    ("descriptorId", J::Null),
                    ("vendorPath", J::Null),
                ]),
            ),
            ("checksumVerification", s("not-applicable")),
            ("provenanceAssurance", s("declared")),
        ]));
    }
    let set = obj(vec![
        ("schemaVersion", n(1)),
        ("language", s("rust")),
        (
            "lockfileIdentity",
            obj(vec![
                ("path", s("Cargo.lock")),
                ("lockfileVersion", n(3)),
                ("contentSha256", s(&"b".repeat(64))),
            ]),
        ),
        ("packages", J::Array(packages)),
        (
            "completeness",
            obj(vec![
                ("state", s("complete")),
                ("missing", J::Array(vec![])),
            ]),
        ),
    ]);
    let mut f = Fixture {
        set,
        manifests,
        id: String::new(),
    };
    f.refresh();
    f
}
fn mixed(length: u64) -> Fixture {
    fixture(vec![
        (
            "a",
            "1",
            "source with spaces",
            vec![file("src/a.rs", 0), file("src/b.rs", length)],
        ),
        ("a", "10", "", vec![]),
        ("a", "2", "other", vec![file("src/a.rs", 3)]),
    ])
}
fn wm<'a>(v: &'a Value, k: &str) -> &'a Value {
    let Value::Map(v) = v else { panic!() };
    super::super::super::super::ts2::carrier::field(v, k).unwrap()
}
fn packages_mut(f: &mut Fixture) -> &mut Vec<J> {
    let J::Object(v) = &mut f.set else { panic!() };
    let J::Array(v) = v.get_mut("packages").unwrap() else {
        panic!()
    };
    v
}
fn replace(v: &mut J, k: &str, value: J) {
    let J::Object(v) = v else { panic!() };
    v.insert(k.into(), value);
}

#[test]
fn dependency_manifest_uses_complete_tuple_order_and_distinct_native_and_wire_hashes() {
    let policy = Policy::load().unwrap();
    let f = mixed(1_048_577);
    let built = build(&policy, &f.input(), 7).unwrap();
    let expected = Value::Array(vec![
        map(vec![
            ("path", t("src/a.rs")),
            ("byteLength", Value::Unsigned(0)),
            ("contentSha256", t(&"a".repeat(64))),
            ("packageKey", t("a 1 source with spaces")),
        ]),
        map(vec![
            ("path", t("src/b.rs")),
            ("byteLength", Value::Unsigned(1_048_577)),
            ("contentSha256", t(&"a".repeat(64))),
            ("packageKey", t("a 1 source with spaces")),
        ]),
        map(vec![
            ("path", t("src/a.rs")),
            ("byteLength", Value::Unsigned(3)),
            ("contentSha256", t(&"a".repeat(64))),
            ("packageKey", t("a 2 other")),
        ]),
    ]);
    assert_eq!(wm(&built.manifest, "entries"), &expected);
    let raw = digest_hex(&raw_sha256(&cbor::encode(&expected)));
    assert_eq!(wm(&built.manifest, "manifestSha256"), &t(&raw));
    assert_eq!(wm(&built.seal, "manifestSha256"), &t(&raw));
    assert_eq!(wm(&built.seal, "entryCount"), &Value::Unsigned(3));
    assert_eq!(wm(&built.seal, "totalBytes"), &Value::Unsigned(1_048_580));
    assert_eq!(wm(&built.seal, "totalChunkCount"), &Value::Unsigned(3));
    assert_eq!((built.bytes, built.chunks), (1_048_580, 3));
    assert_eq!(wm(&built.seal, "dependencySourceSetId"), &t(&f.id));
    let mut wrong = f.id.clone();
    wrong.replace_range(7..8, "f");
    if wrong == f.id {
        wrong.replace_range(7..8, "0");
    }
    assert!(matches!(
        build(
            &policy,
            &Input {
                set_id: &wrong,
                ..f.input()
            },
            7
        ),
        Err(Refusal::Join("dependency set identity"))
    ));
}

#[test]
fn dependency_empty_set_and_zero_file_packages_still_require_complete_join() {
    let policy = Policy::load().unwrap();
    for f in [fixture(vec![]), fixture(vec![("zero", "1", "", vec![])])] {
        let built = build(&policy, &f.input(), 7).unwrap();
        assert_eq!(wm(&built.manifest, "entries"), &Value::Array(vec![]));
        assert_eq!(
            wm(&built.manifest, "manifestSha256"),
            &t("76be8b528d0075f7aae98d6fa57a6d3c83ae480a8469e668d7b0af968995ac71")
        );
        assert_eq!((built.bytes, built.chunks), (0, 0));
        assert_eq!(wm(&built.seal, "entryCount"), &Value::Unsigned(0));
    }
    let mut missing = fixture(vec![("zero", "1", "", vec![])]);
    missing.manifests.clear();
    assert!(matches!(
        build(&policy, &missing.input(), 7),
        Err(Refusal::Join("missing retained file manifest"))
    ));
}

#[test]
fn dependency_manifest_refuses_missing_rebound_counts_hashes_paths_and_package_keys() {
    let policy = Policy::load().unwrap();
    let mut missing = mixed(1);
    missing.manifests.clear();
    assert!(build(&policy, &missing.input(), 7).is_err());
    for (key, value, expected) in [
        ("fileCount", n(1), "dependency file count"),
        ("totalBytes", n(9), "dependency package bytes"),
    ] {
        let mut f = mixed(1);
        replace(&mut packages_mut(&mut f)[0], key, value);
        f.refresh();
        assert!(matches!(build(&policy,&f.input(),7),Err(Refusal::Join(code))if code==expected));
    }
    let mut f = mixed(1);
    packages_mut(&mut f).swap(0, 1);
    f.refresh();
    assert!(matches!(
        build(&policy, &f.input(), 7),
        Err(Refusal::Join("dependency package order"))
    ));
    let mut f = mixed(1);
    let duplicate = packages_mut(&mut f)[0].clone();
    packages_mut(&mut f).insert(1, duplicate);
    f.refresh();
    assert!(build(&policy, &f.input(), 7).is_err());
    for bad in ["name with space", "name\twith-tab", ""] {
        let mut f = mixed(1);
        replace(&mut packages_mut(&mut f)[0], "name", s(bad));
        f.refresh();
        assert!(build(&policy, &f.input(), 7).is_err());
    }
    for rows in [
        vec![file("../outside", 1)],
        vec![file("src/a", 1), file("src/a", 1)],
        vec![file("src/b", 1), file("src/a", 1)],
        vec![file("src//a", 1)],
    ] {
        let f = fixture(vec![("a", "1", "", rows)]);
        assert!(build(&policy, &f.input(), 7).is_err());
    }
    let mut f = mixed(1);
    let hash = text(field(&packages_mut(&mut f)[0], "fileManifestSha256").unwrap())
        .unwrap()
        .to_owned();
    let J::Array(rows) = f.manifests.get_mut(&hash).unwrap() else {
        panic!()
    };
    replace(&mut rows[0], "contentSha256", s(&"c".repeat(64)));
    assert!(matches!(
        build(&policy, &f.input(), 7),
        Err(Refusal::Join("dependency file manifest H"))
    ));
    // A raw digest of the JSON array is not its native framed H identity.
    let mut f = mixed(1);
    let hash = text(field(&packages_mut(&mut f)[0], "fileManifestSha256").unwrap())
        .unwrap()
        .to_owned();
    let manifest = f.manifests.remove(&hash).unwrap();
    let raw = digest_hex(&raw_sha256(&canonical_bytes(&manifest).unwrap()));
    f.manifests.insert(raw.clone(), manifest);
    replace(&mut packages_mut(&mut f)[0], "fileManifestSha256", s(&raw));
    f.refresh();
    assert!(matches!(
        build(&policy, &f.input(), 7),
        Err(Refusal::Join("dependency file manifest H"))
    ));
}

#[test]
fn dependency_bounds_are_inclusive_and_chunks_follow_exact_greedy_coordinates() {
    let mut policy = Policy::load().unwrap();
    let f = mixed(1_048_577);
    let built = build(&policy, &f.input(), 24).unwrap();
    let size = cbor::encode(&schedule::envelope(
        24,
        "DependencySourceManifest",
        built.manifest.clone(),
    ))
    .len() as u64;
    policy.limits.insert("maxFramePayloadBytes".into(), size);
    assert!(build(&policy, &f.input(), 24).is_ok());
    policy
        .limits
        .insert("maxFramePayloadBytes".into(), size - 1);
    assert!(matches!(
        build(&policy, &f.input(), 24),
        Err(Refusal::Bound("dependency manifest envelope"))
    ));
    let mut policy = Policy::load().unwrap();
    policy.limits.insert("maxDependencySourceEntries".into(), 3);
    assert!(build(&policy, &f.input(), 7).is_ok());
    policy.limits.insert("maxDependencySourceEntries".into(), 2);
    assert!(matches!(
        build(&policy, &f.input(), 7),
        Err(Refusal::Bound("dependency entries"))
    ));
    let mut policy = Policy::load().unwrap();
    policy
        .limits
        .insert("maxDependencySourcePackages".into(), 2);
    assert!(matches!(
        build(&policy, &f.input(), 7),
        Err(Refusal::Bound("dependency packages"))
    ));
    let policy = Policy::load().unwrap();
    let maximum = policy.limit("maxDependencySourceTotalBytes").unwrap();
    let fmax = fixture(vec![("a", "1", "", vec![file("a", maximum)])]);
    assert_eq!(build(&policy, &fmax.input(), 7).unwrap().bytes, maximum);
    let over = fixture(vec![("a", "1", "", vec![file("a", maximum), file("b", 1)])]);
    assert!(matches!(
        build(&policy, &over.input(), 7),
        Err(Refusal::Bound("dependency bytes"))
    ));
    let Value::Array(entries) = wm(&built.manifest, "entries") else {
        panic!()
    };
    let entry = &entries[1];
    assert!(chunk(&policy, &f.id, entry, 0, 0, vec![1; 1_048_576]).is_ok());
    assert!(chunk(&policy, &f.id, entry, 1, 1_048_576, vec![2]).is_ok());
    for (index, offset, bytes) in [
        (0, 0, vec![0]),
        (1, 1_048_575, vec![0]),
        (1, 1_048_576, vec![]),
        (2, 2_097_152, vec![0]),
        (u64::MAX, 0, vec![0]),
    ] {
        assert!(chunk(&policy, &f.id, entry, index, offset, bytes).is_err());
    }
    assert!(chunk(&policy, &f.id, &entries[0], 0, 0, vec![]).is_err());
}
