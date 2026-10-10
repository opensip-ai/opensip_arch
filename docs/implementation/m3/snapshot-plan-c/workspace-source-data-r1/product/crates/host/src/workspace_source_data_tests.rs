use super::{CandidateIdError as E, CandidateSourceClass as C, classify_candidates};
use opensip_identity::{JsonValue as V, parse_json};

fn strings(v: &V) -> Vec<&str> {
    let V::Array(rows) = v else {
        panic!("expected array")
    };
    rows.iter()
        .map(|v| {
            let V::String(s) = v else {
                panic!("expected string")
            };
            s.as_str()
        })
        .collect()
}

#[test]
fn actual_retained_workspace_observations_preserve_path_nonmembers_and_separate_roots() {
    let V::Array(cases) = parse_json(include_bytes!(
        "workspace_source_data/fixtures/vectors.json"
    ))
    .unwrap() else {
        panic!("expected cases")
    };
    assert_eq!(cases.len(), 3);
    for case in cases {
        let V::Object(case) = case else {
            panic!("expected case")
        };
        let packages = strings(&case["packages"]);
        let members = strings(&case["workspaceMembers"]);
        let selected = strings(&case["selectedPackages"]);
        let actual = classify_candidates(&packages, &members, &selected).unwrap();
        let expected = strings(&case["expected"]);
        let labels = actual
            .iter()
            .map(|c| match c {
                C::SnapshotMember => "snapshot-member",
                C::DependencyClosureMember => "dependency-closure-member",
            })
            .collect::<Vec<_>>();
        assert_eq!(labels, expected);
    }
}

#[test]
fn complete_populations_refuse_duplicate_and_unknown_ids_even_without_selections() {
    assert_eq!(
        classify_candidates(&["a", "a"], &[], &[]),
        Err(E::DuplicatePackage)
    );
    assert_eq!(
        classify_candidates(&["a"], &["a", "a"], &[]),
        Err(E::DuplicateWorkspaceMember)
    );
    assert_eq!(
        classify_candidates(&["a"], &["b"], &[]),
        Err(E::UnknownWorkspaceMember)
    );
    assert_eq!(
        classify_candidates(&["a"], &[], &["b"]),
        Err(E::UnknownSelectedPackage)
    );
}

#[test]
fn exact_opaque_ids_do_not_use_path_prefix_name_or_unicode_normalization() {
    let ids = [
        "path+file:///same#same@1",
        "path+file:///same/sub#same@1",
        "é",
        "e\u{301}",
    ];
    assert_eq!(
        classify_candidates(&ids, &[ids[0], ids[2]], &ids),
        Ok(vec![
            C::SnapshotMember,
            C::DependencyClosureMember,
            C::SnapshotMember,
            C::DependencyClosureMember
        ])
    );
}

#[test]
fn membership_is_independent_of_package_order_and_retains_selected_occurrences() {
    let first = classify_candidates(&["a", "b", "c"], &["b", "a"], &["c", "b", "a", "b"]);
    let permuted = classify_candidates(&["c", "a", "b"], &["a", "b"], &["c", "b", "a", "b"]);
    assert_eq!(first, permuted);
    assert_eq!(
        first,
        Ok(vec![
            C::DependencyClosureMember,
            C::SnapshotMember,
            C::SnapshotMember,
            C::SnapshotMember
        ])
    );
}

#[test]
fn late_members_and_invalid_rows_are_not_truncated_at_activation_limits() {
    let storage = (0..20_000)
        .map(|i| format!("opaque-{i}"))
        .collect::<Vec<_>>();
    let mut ids = storage.iter().map(String::as_str).collect::<Vec<_>>();
    let last = ids[19_999];
    assert_eq!(
        classify_candidates(&ids, &[last], &[last, ids[0]]),
        Ok(vec![C::SnapshotMember, C::DependencyClosureMember])
    );
    ids.push(last);
    assert_eq!(
        classify_candidates(&ids, &[], &[]),
        Err(E::DuplicatePackage)
    );
}
