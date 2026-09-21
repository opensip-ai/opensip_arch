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
        r#"{{"projectId":"prj1-{i:064x}","namespaceId":"{i:08x}-0000-4000-8000-000000000000","status":"{status}","allocationKind":"{kind}","root":{{"platform":"macos","canonicalPathBytesHex":"{path}","deviceId":"0","inodeId":"{i}","birthSeconds":0,"birthNanoseconds":0}}}}"#
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
            V::Integer(JsonInteger::new(1).unwrap()),
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
    *field(root, "platform") = string("linux");
    *field(root, "canonicalPathBytesHex") = string("2fff");
    *field(root, "deviceId") = string("18446744073709551615");
    *field(root, "inodeId") = string("18446744073709551615");
    *field(root, "birthSeconds") = V::Integer(JsonInteger::new(i64::MIN.into()).unwrap());
    *field(root, "birthNanoseconds") = V::Integer(JsonInteger::new(999_999_999).unwrap());
    let d = ProjectRegistryDocument::decode(&document(vec![r])).unwrap();
    let r = d.entries()[0].root();
    assert_eq!(r.platform(), ProjectRootPlatform::Linux);
    assert_eq!(r.path_bytes(), b"/\xff");
    assert_eq!(r.device(), u64::MAX);
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
    assert!(ProjectRegistryDocument::decode(b"{\"schemaVersion\":1,\"entries\":[]}").is_err());
    assert!(
        ProjectRegistryDocument::decode(
            b"{\"entries\":[],\"schemaVersion\":1,\"schemaVersion\":1}"
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
