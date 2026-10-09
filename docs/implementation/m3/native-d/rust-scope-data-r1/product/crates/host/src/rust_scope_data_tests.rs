use super::*;
use opensip_identity::parse_json;
fn field<'a>(v: &'a V, name: &str) -> &'a V {
    let V::Object(o) = v else { panic!("object") };
    &o[name]
}
fn string(v: &V) -> &str {
    let V::String(s) = v else { panic!("string") };
    s
}
fn array(v: &V) -> &[V] {
    let V::Array(a) = v else { panic!("array") };
    a
}
fn number(v: &V) -> u64 {
    let V::Integer(n) = v else { panic!("integer") };
    u64::try_from(n.get()).unwrap()
}
fn digest(v: &V) -> Option<[u8; 32]> {
    if matches!(v, V::Null) {
        return None;
    }
    let raw = string(v);
    assert_eq!(raw.len(), 64);
    Some(std::array::from_fn(|i| {
        u8::from_str_radix(&raw[i * 2..i * 2 + 2], 16).unwrap()
    }))
}
fn snapshot() -> String {
    format!("snapshot2:{}", "1".repeat(64))
}
fn file(path: &LogicalPath, bytes: u64) -> Entry<'_> {
    Entry {
        kind: "file",
        path,
        byte_length: Some(bytes),
        content_sha256: Some([0xcc; 32]),
    }
}
#[test]
fn exact_closed_rust3_lim_vector_and_domain() {
    let v = parse_json(include_bytes!("rust_scope_data/fixtures/vectors.json")).unwrap();
    let rows = array(field(&v, "manifestEntries"));
    let paths: Vec<_> = rows
        .iter()
        .map(|r| LogicalPath::parse(string(field(r, "path"))).unwrap())
        .collect();
    let entries: Vec<_> = rows
        .iter()
        .zip(&paths)
        .map(|(r, path)| Entry {
            kind: string(field(r, "kind")),
            path,
            byte_length: match field(r, "byteLength") {
                V::Null => None,
                n => Some(number(n)),
            },
            content_sha256: digest(field(r, "contentSha256")),
        })
        .collect();
    let data = rebuild(string(field(&v, "snapshotId")), &entries).unwrap();
    assert_eq!(data.subjects, *field(&v, "subjects"));
    assert_eq!(data.subject_count, 3);
    assert_eq!(
        data.subject_scope_commitment,
        string(field(&v, "subjectScopeCommitment"))
    );
    let request = field(&v, "stageRequestV3ByReference");
    let keys = array(field(
        field(request, "analysisDomain"),
        "requestedCoverageDomain",
    ));
    assert_eq!(
        domain_commitment(&data, keys).unwrap(),
        string(field(&v, "domainCommitment"))
    );
}
#[test]
fn exact_selection_utf8_order_zero_and_nonfile_exclusions() {
    let names = [
        "é.rs", "z.rs", "a.rs", "empty.rs", "UPPER.RS", "link.rs", "note.txt",
    ];
    let paths: Vec<_> = names
        .iter()
        .map(|s| LogicalPath::parse(s).unwrap())
        .collect();
    let entries = [
        file(&paths[0], 3),
        file(&paths[1], 2),
        file(&paths[2], 1),
        file(&paths[3], 0),
        file(&paths[4], 1),
        Entry {
            kind: "symlink",
            path: &paths[5],
            byte_length: None,
            content_sha256: None,
        },
        file(&paths[6], 1),
    ];
    let data = rebuild(&snapshot(), &entries).unwrap();
    let subjects = array(&data.subjects);
    assert_eq!(data.subject_count, 3);
    for (i, expected) in ["a.rs", "z.rs", "é.rs"].iter().enumerate() {
        assert_eq!(string(field(&subjects[i], "path")), *expected);
        assert_eq!(number(field(&subjects[i], "subjectOrdinal")), i as u64);
        assert_eq!(number(field(&subjects[i], "startByte")), 0);
    }
    let reversed: Vec<_> = entries.into_iter().rev().collect();
    assert_eq!(
        rebuild(&snapshot(), &reversed).unwrap().canonical_subjects,
        data.canonical_subjects
    );
}
#[test]
fn no_inline_256_cap_in_reference_data_recipe() {
    let paths: Vec<_> = (0..257)
        .map(|i| LogicalPath::parse(&format!("src/f-{i:03}.rs")).unwrap())
        .collect();
    let entries: Vec<_> = paths.iter().map(|p| file(p, 1)).collect();
    let data = rebuild(&snapshot(), &entries).unwrap();
    assert_eq!(data.subject_count, 257);
    assert_eq!(
        number(field(&array(&data.subjects)[256], "subjectOrdinal")),
        256
    );
}
#[test]
fn duplicate_empty_missing_fields_and_snapshot_shapes_refuse() {
    let p = LogicalPath::parse("src/lib.rs").unwrap();
    assert!(matches!(rebuild(&snapshot(), &[]), Err(ScopeError::Empty)));
    assert!(matches!(
        rebuild(&snapshot(), &[file(&p, 0)]),
        Err(ScopeError::Empty)
    ));
    assert!(matches!(
        rebuild(&snapshot(), &[file(&p, 1), file(&p, 2)]),
        Err(ScopeError::DuplicatePath)
    ));
    assert!(matches!(
        rebuild("snapshot2:not-a-hash", &[file(&p, 1)]),
        Err(ScopeError::SnapshotShape)
    ));
    assert!(matches!(
        rebuild(&format!("snapshot2:{}", "A".repeat(64)), &[file(&p, 1)]),
        Err(ScopeError::SnapshotShape)
    ));
    let mut entry = file(&p, 1);
    entry.byte_length = None;
    assert!(matches!(
        rebuild(&snapshot(), &[entry]),
        Err(ScopeError::MissingFileLength)
    ));
    let mut entry = file(&p, 1);
    entry.content_sha256 = None;
    assert!(matches!(
        rebuild(&snapshot(), &[entry]),
        Err(ScopeError::MissingFileDigest)
    ));
}
#[test]
fn snapshot_content_path_and_length_are_all_committed() {
    let p = LogicalPath::parse("a.rs").unwrap();
    let q = LogicalPath::parse("b.rs").unwrap();
    let first = rebuild(&snapshot(), &[file(&p, 1)]).unwrap();
    for data in [
        rebuild(&format!("snapshot2:{}", "2".repeat(64)), &[file(&p, 1)]).unwrap(),
        rebuild(&snapshot(), &[file(&q, 1)]).unwrap(),
        rebuild(&snapshot(), &[file(&p, 2)]).unwrap(),
        rebuild(
            &snapshot(),
            &[Entry {
                content_sha256: Some([0xdd; 32]),
                ..file(&p, 1)
            }],
        )
        .unwrap(),
    ] {
        assert_ne!(data.subjects, first.subjects);
        assert_ne!(
            data.subject_scope_commitment,
            first.subject_scope_commitment
        );
    }
}
#[test]
fn exact_requested_key_order_and_fields_are_committed() {
    let p = LogicalPath::parse("a.rs").unwrap();
    let data = rebuild(&snapshot(), &[file(&p, 1)]).unwrap();
    let a = object([("relation", V::String("calls".into()))]);
    let b = object([("relation", V::String("references".into()))]);
    let forward = domain_commitment(&data, &[a.clone(), b.clone()]).unwrap();
    assert_ne!(forward, domain_commitment(&data, &[b, a]).unwrap());
    assert_ne!(forward, domain_commitment(&data, &[]).unwrap());
    // Empty/illustrative keys are hash inputs only; they are not C-2 admission.
}
#[test]
fn canonical_cbor_shortest_uint_map_order_and_non_nfc_refusal() {
    assert_eq!(
        cbor(&integer(u64::MAX).unwrap()).unwrap(),
        [vec![0x1b], vec![0xff; 8]].concat()
    );
    assert_eq!(cbor(&integer(24).unwrap()).unwrap(), [0x18, 0x18]);
    assert_eq!(
        cbor(&object([
            ("b", integer(1).unwrap()),
            ("aa", integer(2).unwrap())
        ]))
        .unwrap(),
        [0xa2, 0x61, b'b', 1, 0x62, b'a', b'a', 2]
    );
    assert!(matches!(
        cbor(&V::Integer(JsonInteger::new(-1).unwrap())),
        Err(ScopeError::Integer)
    ));
    assert!(matches!(
        cbor(&V::String("e\u{301}".into())),
        Err(ScopeError::Text(opensip_identity::Cve1Error::NotNfc))
    ));
    let p = LogicalPath::parse("e\u{301}.rs").unwrap();
    assert!(matches!(
        rebuild(&snapshot(), &[file(&p, 1)]),
        Err(ScopeError::Text(opensip_identity::Cve1Error::NotNfc))
    ));
}
