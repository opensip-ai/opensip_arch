use crate::{
    JsonInteger, JsonValue as V, ProjectAllocationKind, ProjectIdMarker, ProjectRegistryDocument,
    ProjectRegistryStatus, ProjectRootPlatform, canonical_bytes, parse_json,
};
use alloc::{collections::BTreeMap, format, string::String, vec, vec::Vec};

fn row(i: u32, status: &str, kind: &str) -> V {
    let path: String = format!("/p{i}")
        .bytes()
        .map(|b| format!("{b:02x}"))
        .collect();
    parse_json(format!(
        r#"{{"projectId":"prj1-{i:064x}","namespaceId":"{i:08x}-0000-4000-8000-000000000000","status":"{status}","allocationKind":"{kind}","root":{{"platform":"macos","canonicalPathBytesHex":"{path}","volumeIdentity":{{"kind":"macos-apfs-volume-uuid-v1","value":"11111111111111111111111111111111"}},"inodeId":"{i}","birthSeconds":0,"birthNanoseconds":0}}}}"#
    ).as_bytes()).unwrap()
}
fn field<'a>(value: &'a mut V, name: &str) -> &'a mut V {
    let V::Object(map) = value else {
        panic!("fixture object")
    };
    map.get_mut(name).unwrap()
}
fn string(value: &str) -> V {
    V::String(value.into())
}
fn document(rows: Vec<V>) -> Vec<u8> {
    canonical_bytes(&V::Object(BTreeMap::from([
        (String::from("entries"), V::Array(rows)),
        (
            String::from("schemaVersion"),
            V::Integer(JsonInteger::new(2).unwrap()),
        ),
    ])))
    .unwrap()
}

#[test]
fn projection_preserves_exact_names_while_pending_reservations_remain_visible() {
    let raw = document(vec![
        row(1, "RESERVED", "random"),
        row(2, "ACTIVE", "adopt"),
        row(3, "RETIRED", "adopt"),
        row(4, "ABANDONED", "random"),
    ]);
    let d = ProjectRegistryDocument::decode(&raw).unwrap();
    assert_eq!(d.raw(), raw);
    assert!(d.has_reservations());
    assert_eq!(
        d.registered_namespace_values().collect::<Vec<_>>(),
        vec![
            "00000002-0000-4000-8000-000000000000",
            "00000003-0000-4000-8000-000000000000"
        ]
    );
    assert_eq!(
        d.entries()[1].allocation_kind(),
        ProjectAllocationKind::Adopt
    );
    assert_eq!(d.entries()[3].status(), ProjectRegistryStatus::Abandoned);
    let empty = ProjectRegistryDocument::decode(&document(vec![])).unwrap();
    assert!(!empty.has_reservations());
    assert_eq!(empty.registered_namespace_values().count(), 0);
}

#[test]
fn invalid_late_row_prevents_obtaining_any_partial_document() {
    let mut bad = row(2, "ACTIVE", "random");
    let V::Object(o) = &mut bad else {
        unreachable!()
    };
    o.remove("allocationKind");
    assert!(
        ProjectRegistryDocument::decode(&document(vec![row(1, "ACTIVE", "random"), bad])).is_err()
    );
    let mut bad = row(2, "ACTIVE", "random");
    let V::Object(o) = &mut bad else {
        unreachable!()
    };
    o.insert("callerAuthority".into(), V::Bool(true));
    assert!(
        ProjectRegistryDocument::decode(&document(vec![row(1, "ACTIVE", "random"), bad])).is_err()
    );
}

#[test]
fn terminal_project_history_can_repeat_but_live_project_cannot() {
    let first = row(1, "RETIRED", "random");
    let mut next = row(2, "ACTIVE", "adopt");
    *field(&mut next, "projectId") = string(&format!("prj1-{:064x}", 1));
    assert!(ProjectRegistryDocument::decode(&document(vec![first.clone(), next.clone()])).is_ok());
    let mut live = first;
    *field(&mut live, "status") = string("RESERVED");
    assert!(ProjectRegistryDocument::decode(&document(vec![live, next])).is_err());
}

#[test]
fn namespace_is_never_reused_even_by_terminal_rows() {
    let mut next = row(2, "ABANDONED", "random");
    *field(&mut next, "namespaceId") = string("00000001-0000-4000-8000-000000000000");
    assert!(
        ProjectRegistryDocument::decode(&document(vec![row(1, "RETIRED", "random"), next]))
            .is_err()
    );
    assert!(
        ProjectRegistryDocument::decode(&document(vec![
            row(2, "RETIRED", "random"),
            row(1, "ABANDONED", "adopt")
        ]))
        .is_err()
    );
}

#[test]
fn native_root_identity_and_locator_are_separate_live_uniqueness_checks() {
    for duplicate in ["inodeId", "canonicalPathBytesHex"] {
        let mut second = row(2, "ACTIVE", "random");
        *field(field(&mut second, "root"), duplicate) = string(if duplicate == "inodeId" {
            "1"
        } else {
            "2f7031"
        });
        assert!(
            ProjectRegistryDocument::decode(&document(vec![row(1, "RESERVED", "random"), second]))
                .is_err()
        );
    }
}

#[test]
fn raw_posix_root_bytes_and_full_native_integer_ranges_survive_decode() {
    let mut r = row(1, "ACTIVE", "random");
    let root = field(&mut r, "root");
    *field(root, "canonicalPathBytesHex") = string("2fff");
    *field(root, "inodeId") = string("18446744073709551615");
    *field(root, "birthSeconds") = V::Integer(JsonInteger::new(i64::MIN.into()).unwrap());
    *field(root, "birthNanoseconds") = V::Integer(JsonInteger::new(999_999_999).unwrap());
    let d = ProjectRegistryDocument::decode(&document(vec![r])).unwrap();
    let r = d.entries()[0].root();
    assert_eq!(r.platform(), ProjectRootPlatform::Macos);
    assert_eq!(r.path_bytes(), b"/\xff");
    assert_eq!(r.volume_uuid_bytes(), &[0x11; 16]);
    assert_eq!(r.volume_kind().as_str(), "macos-apfs-volume-uuid-v1");
    assert_eq!(r.inode(), u64::MAX);
    assert_eq!(r.birth_seconds(), i64::MIN);
    assert_eq!(r.birth_nanoseconds(), 999_999_999);
}

#[test]
fn canonical_document_is_required_without_silent_normalization() {
    let raw = document(vec![]);
    let mut newline = raw.clone();
    newline.push(b'\n');
    assert!(ProjectRegistryDocument::decode(&newline).is_err());
    assert!(ProjectRegistryDocument::decode(b"{\"schemaVersion\":2,\"entries\":[]}").is_err());
    assert!(
        ProjectRegistryDocument::decode(
            b"{\"entries\":[],\"schemaVersion\":2,\"schemaVersion\":2}"
        )
        .is_err()
    );
    assert!(ProjectRegistryDocument::decode(b"{\"entries\":[],\"schemaVersion\":true}").is_err());
    assert!(ProjectRegistryDocument::decode(&raw).is_ok());
}

#[test]
fn marker_is_exact_ascii_frame_not_json_or_a_trimmed_identifier() {
    let id = format!("prj1-{:064x}", 0xabcdefu32);
    let raw = format!("opensip-project-id-v1\n{id}\n");
    assert_eq!(raw.len(), crate::PROJECT_MARKER_SIZE);
    assert_eq!(
        ProjectIdMarker::decode(raw.as_bytes())
            .unwrap()
            .project_id(),
        id
    );
    for bad in [
        raw.replace('\n', "\r\n"),
        raw.trim_end().into(),
        format!("{raw}\n"),
        raw.to_uppercase(),
        id,
    ] {
        assert!(ProjectIdMarker::decode(bad.as_bytes()).is_err());
    }
}

#[test]
fn all_rows_count_toward_capacity_including_abandoned_history() {
    let rows = (1..=4096)
        .map(|i| row(i, "ABANDONED", "random"))
        .collect::<Vec<_>>();
    assert!(ProjectRegistryDocument::decode(&document(rows.clone())).is_ok());
    let mut excess = rows;
    excess.push(row(4097, "ABANDONED", "random"));
    assert!(ProjectRegistryDocument::decode(&document(excess)).is_err());
}

#[test]
fn legacy_version_or_device_root_is_never_silently_upgraded() {
    assert!(ProjectRegistryDocument::decode(b"{\"entries\":[],\"schemaVersion\":1}").is_err());
    for retain_volume in [false, true] {
        let mut r = row(1, "ACTIVE", "random");
        let V::Object(root) = field(&mut r, "root") else {
            unreachable!()
        };
        root.insert("deviceId".into(), string("2049"));
        if !retain_volume {
            root.remove("volumeIdentity");
        }
        assert!(ProjectRegistryDocument::decode(&document(vec![r])).is_err());
    }
}

#[test]
fn volume_identity_requires_closed_supported_nonzero_native_bytes() {
    let valid = field(
        field(&mut row(1, "ACTIVE", "random"), "root"),
        "volumeIdentity",
    )
    .clone();
    let mut invalid = vec![
        V::Null,
        string("11111111111111111111111111111111"),
        V::Array(vec![]),
    ];
    for value in [
        "",
        "00000000000000000000000000000000",
        "ABCDEF0123456789abcdef0123456789",
        "1111111111111111111111111111111",
        "111111111111111111111111111111111",
        "1111111111111111111111111111111g",
    ] {
        let mut volume = valid.clone();
        *field(&mut volume, "value") = string(value);
        invalid.push(volume);
    }
    for kind in ["", "linux-volume-uuid-v1", "macos-apfs-volume-uuid-v2"] {
        let mut volume = valid.clone();
        *field(&mut volume, "kind") = string(kind);
        invalid.push(volume);
    }
    for absent in ["kind", "value"] {
        let V::Object(mut o) = valid.clone() else {
            unreachable!()
        };
        o.remove(absent);
        invalid.push(V::Object(o));
    }
    let V::Object(mut extra) = valid else {
        unreachable!()
    };
    extra.insert("qualified".into(), V::Bool(true));
    invalid.push(V::Object(extra));
    for volume in invalid {
        let mut r = row(1, "ACTIVE", "random");
        *field(field(&mut r, "root"), "volumeIdentity") = volume;
        assert!(ProjectRegistryDocument::decode(&document(vec![r])).is_err());
    }
    let mut r = row(1, "ACTIVE", "random");
    *field(field(&mut r, "root"), "platform") = string("linux");
    assert!(ProjectRegistryDocument::decode(&document(vec![r])).is_err());
}

#[test]
fn different_volumes_disambiguate_inode_birth_but_never_duplicate_live_locator() {
    let first = row(1, "ACTIVE", "random");
    let mut second = row(2, "RESERVED", "adopt");
    let root = field(&mut second, "root");
    *field(root, "inodeId") = string("1");
    *field(field(root, "volumeIdentity"), "value") = string("000102030405060708090a0b0c0d0e0f");
    let d =
        ProjectRegistryDocument::decode(&document(vec![first.clone(), second.clone()])).unwrap();
    assert_eq!(
        d.entries()[1].root().volume_uuid_bytes(),
        &[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    );
    *field(field(&mut second, "root"), "canonicalPathBytesHex") = string("2f7031");
    assert!(ProjectRegistryDocument::decode(&document(vec![first, second])).is_err());
}

#[test]
fn invalid_terminal_volume_still_refuses_the_whole_document() {
    for status in ["RETIRED", "ABANDONED"] {
        let mut last = row(2, status, "random");
        *field(field(field(&mut last, "root"), "volumeIdentity"), "value") =
            string("00000000000000000000000000000000");
        assert!(
            ProjectRegistryDocument::decode(&document(vec![row(1, "ACTIVE", "random"), last]))
                .is_err()
        );
    }
}
