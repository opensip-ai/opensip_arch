// Unit B2-b2's controls (M3-B r5 item 13; B2-b plan r4 section 1.2). Vectors
// from tools/security/discovery_scan_vectors.py (the B2-b0 current reference,
// contract successor 164); synthetic metadata otherwise. Nothing is read from
// a filesystem tree.
use super::*;
use crate::custody::project_chain::check_project_object_waived;
use opensip_identity::{JsonValue as V, parse_json};
use opensip_platform::CapturedAclPrincipal;

const VECTORS: &[u8] = include_bytes!("discovery_scan_vectors.json");
const SOURCE: &str = include_str!("discovery_scan.rs");
/// An ACE with a write right (any right outside the read-only set).
const WRITE_ACE: (u32, u32) = (crate::private_access::ACE_PERMIT, 1 << 2);

fn field<'v>(value: &'v V, key: &str) -> &'v V {
    let V::Object(fields) = value else {
        panic!("{value:?}")
    };
    fields.get(key).unwrap_or(&V::Null)
}
fn text(value: &V) -> &str {
    let V::String(s) = value else {
        panic!("{value:?}")
    };
    s
}
fn items(value: &V) -> &[V] {
    let V::Array(items) = value else {
        panic!("{value:?}")
    };
    items
}
fn int(value: &V) -> i128 {
    let V::Integer(i) = value else {
        panic!("{value:?}")
    };
    i.get()
}
fn string(s: &str) -> V {
    V::String(s.to_owned())
}
fn strings(values: &[String]) -> V {
    V::Array(values.iter().map(|s| string(s)).collect())
}
fn object(pairs: Vec<(&str, V)>) -> V {
    V::Object(pairs.into_iter().map(|(k, v)| (k.to_owned(), v)).collect())
}
fn integer(n: i128) -> V {
    V::Integer(opensip_identity::JsonInteger::new(n).unwrap())
}
fn optional(value: Option<&String>) -> V {
    value.map_or(V::Null, |s| string(s))
}

/// SLM's synthetic `fs` entry as the walker would hand it over.
fn entry(e: &V) -> ObservedEntry {
    let kind = match text(field(e, "kind")) {
        "dir" => 0o040000,
        "file" => 0o100000,
        "symlink" => 0o120000,
        _ => 0o010000,
    };
    let perm = match field(e, "mode") {
        V::String(s) => u32::from_str_radix(s, 8).unwrap(),
        V::Integer(i) => u32::try_from(i.get()).unwrap(),
        _ => 0,
    };
    let number = |key: &str, default: i128| match field(e, key) {
        V::Null => default,
        value => int(value),
    };
    let acl = if matches!(field(e, "aclUnreadable"), V::Bool(true)) {
        ObservedAcl::Unreadable
    } else {
        let entries = match field(e, "aclWrite") {
            V::Array(grants) => grants
                .iter()
                .map(|g| {
                    let (who, id) = text(g).split_once(':').unwrap();
                    let id: u32 = id.parse().unwrap();
                    CapturedAclEntry {
                        flags: WRITE_ACE.0,
                        rights: WRITE_ACE.1,
                        principal: if who == "uid" {
                            CapturedAclPrincipal::User(id)
                        } else {
                            CapturedAclPrincipal::Group(id)
                        },
                    }
                })
                .collect(),
            _ => Vec::new(),
        };
        ObservedAcl::Entries(entries)
    };
    let vcs = match field(e, "vcs") {
        V::Bool(true) => Some(ObservedVcs::Directory),
        V::Object(_) => Some(ObservedVcs::Indirection {
            target: match field(field(e, "vcs"), "target") {
                V::String(t) => Some(t.clone()),
                _ => None,
            },
        }),
        _ => None,
    };
    let absent = u32::MAX as i128;
    ObservedEntry {
        metadata: DescriptorMetadata {
            device: number("dev", 1) as u64,
            inode: 0,
            mode: kind | perm,
            uid: number("uid", absent) as u32,
            gid: number("gid", absent) as u32,
            links: number("nlink", if kind == 0o040000 { 2 } else { 1 }) as u64,
            size: number("size", 0) as u64,
            modified: (0, 0),
            changed: (0, 0),
            flags: 0,
        },
        acl,
        vcs,
    }
}

fn upward(u: &V) -> UpwardProvenance {
    UpwardProvenance {
        mode: text(field(u, "mode")).to_owned(),
        config_path: match field(u, "configPath") {
            V::String(s) => Some(s.clone()),
            _ => None,
        },
        walked: items(field(u, "walked"))
            .iter()
            .map(|w| WalkRow {
                path: text(field(w, "path")).to_owned(),
                custody: text(field(w, "custody")).to_owned(),
                candidate: text(field(w, "candidate")).to_owned(),
                boundary: match field(w, "boundary") {
                    V::String(s) => Some(s.clone()),
                    _ => None,
                },
            })
            .collect(),
        stop_reason: text(field(u, "stopReason")).to_owned(),
        vcs: match field(u, "vcs") {
            V::Null => None,
            v => Some(VcsRecord {
                kind: if text(field(v, "kind")) == "directory" {
                    "directory"
                } else {
                    "indirection"
                },
                target: match field(v, "target") {
                    V::String(s) => Some(s.clone()),
                    _ => None,
                },
            }),
        },
        explicit_path_was_symlink: match field(u, "explicitPathWasSymlink") {
            V::Bool(b) => Some(*b),
            _ => None,
        },
    }
}

/// The partial V3 provenance, in the reference's JSON shape (test-only: the
/// module has no serializer for it).
fn provenance(p: &DiscoveryProvenancePending) -> V {
    let u = &p.upward;
    object(vec![
        ("schemaVersion", integer(3)),
        ("mode", string(&u.mode)),
        ("ci", V::Bool(p.ci)),
        ("selectedRoot", string(&p.selected_root)),
        ("configPath", optional(u.config_path.as_ref())),
        (
            "walked",
            V::Array(
                u.walked
                    .iter()
                    .map(|w| {
                        object(vec![
                            ("path", string(&w.path)),
                            ("custody", string(&w.custody)),
                            ("candidate", string(&w.candidate)),
                            ("boundary", optional(w.boundary.as_ref())),
                        ])
                    })
                    .collect(),
            ),
        ),
        ("stopReason", string(&u.stop_reason)),
        ("custodyWaiver", p.custody_waiver.map_or(V::Null, string)),
        (
            "authorizedGroupIds",
            V::Array(
                p.authorized_group_ids
                    .iter()
                    .map(|g| integer(*g as i128))
                    .collect(),
            ),
        ),
        (
            "vcs",
            u.vcs.as_ref().map_or(V::Null, |v| {
                object(vec![
                    ("kind", string(v.kind)),
                    ("target", optional(v.target.as_ref())),
                    ("followed", V::Bool(false)),
                ])
            }),
        ),
        ("nestedRepositories", strings(&p.nested_repositories)),
        ("nestedProjects", strings(&p.nested_projects)),
        ("unitSource", string(p.unit_source)),
        (
            "units",
            V::Array(
                p.units
                    .iter()
                    .map(|r| {
                        object(vec![
                            ("path", string(&r.path)),
                            ("kind", string(r.kind)),
                            (
                                "markers",
                                V::Array(r.markers.iter().map(|m| string(m)).collect()),
                            ),
                        ])
                    })
                    .collect(),
            ),
        ),
        (
            "excludedUnits",
            V::Array(
                p.excluded_units
                    .iter()
                    .map(|r| {
                        object(vec![
                            ("path", string(&r.path)),
                            ("reason", string(&r.reason)),
                        ])
                    })
                    .collect(),
            ),
        ),
        (
            "prunedTrees",
            V::Array(
                p.pruned_trees
                    .iter()
                    .map(|t| {
                        object(vec![
                            ("path", string(&t.path)),
                            ("reason", string(t.reason.as_str())),
                            (
                                "markerCount",
                                t.marker_count.map_or(V::Null, |n| integer(n as i128)),
                            ),
                            ("markerCountBasis", string(t.basis.as_str())),
                        ])
                    })
                    .collect(),
            ),
        ),
        (
            "explicitPathWasSymlink",
            u.explicit_path_was_symlink.map_or(V::Null, V::Bool),
        ),
        ("warnings", strings(&p.warnings)),
        ("memberRepositories", strings(&p.member_repositories)),
        ("memberConfigs", strings(&p.member_configs)),
    ])
}

fn result(r: &DiscoveryResultPending) -> V {
    match r {
        DiscoveryResultPending::Accept(p) => object(vec![
            ("status", string("ACCEPT")),
            ("provenance", provenance(p)),
        ]),
        DiscoveryResultPending::Refuse {
            refusal,
            path,
            detail,
            provenance: p,
        } => {
            let d9 = refusal.d9();
            object(vec![
                ("status", string("REFUSE")),
                ("refusal", string(refusal.code())),
                ("path", optional(path.as_ref())),
                ("detail", string(detail)),
                (
                    "d9",
                    object(vec![
                        ("class", string(d9.class)),
                        ("exit", integer(d9.exit as i128)),
                        ("code", string(d9.code)),
                    ]),
                ),
                ("provenance", provenance(p)),
            ])
        }
    }
}

/// A vector's absolute scope key as the walker keys it: root-relative (M3-B
/// r6 item 12, unit B2-b3d). A key outside the root, which the core never
/// reads, is dropped.
fn relative_key(root: &str, path: &str) -> Option<String> {
    if path == root {
        return Some(String::new());
    }
    let under = format!("{}/", root.trim_end_matches('/'));
    path.strip_prefix(&under).map(str::to_owned)
}

fn run(case: &V) -> DiscoveryResultPending {
    let input = field(case, "input");
    let root = text(field(input, "root"));
    let scope = ObservedScope {
        entries: match field(input, "scope") {
            V::Object(fs) => fs
                .iter()
                .filter_map(|(p, e)| relative_key(root, p).map(|k| (k, entry(e))))
                .collect(),
            other => panic!("{other:?}"),
        },
    };
    let groups: Vec<u32> = items(field(input, "groups"))
        .iter()
        .map(|g| int(g) as u32)
        .collect();
    let groups = AuthorizedGroups::from_invocation(&groups).unwrap();
    let explicit = match field(input, "explicitProject") {
        V::String(s) => Some(std::path::PathBuf::from(s)),
        _ => None,
    };
    let waiver = ProjectOwnerWaiver::from_invocation(
        matches!(field(input, "waive"), V::Bool(true)),
        explicit.as_deref(),
    )
    .unwrap();
    let roots: Vec<String> = items(field(input, "roots"))
        .iter()
        .map(|r| text(r).to_owned())
        .collect();
    let source = match text(field(input, "source")) {
        "explicit-joins" => UnitSourceRequest::ExplicitJoins(roots),
        "config-workspace-roots" => UnitSourceRequest::ConfigWorkspaceRoots(roots),
        _ => UnitSourceRequest::Automatic,
    };
    let members = BTreeSet::new();
    discover(
        &scope,
        text(field(input, "root")),
        upward(field(input, "upward")),
        &DiscoveryInvocation {
            invoking_uid: int(field(input, "uid")) as u32,
            ci: matches!(field(input, "ci"), V::Bool(true)),
            groups: &groups,
            waiver: waiver.as_ref(),
            source,
            basis: if text(field(input, "basis")) == "not-enumerated" {
                MarkerCountBasis::NotEnumerated
            } else {
                MarkerCountBasis::ObservedInventory
            },
            member_roots: &members,
        },
    )
}

#[test]
fn every_current_reference_vector_is_reproduced() {
    let vectors = parse_json(VECTORS).unwrap();
    let source = &items(field(&vectors, "sources"))[0];
    assert_eq!(
        text(field(source, "path")),
        "docs/implementation/m3/config-discovery-b/b2-b-reference/reference/discovery_scan_reference.py"
    );
    assert_eq!(
        text(field(source, "sha256")),
        "6714575ccee1474e2d7c20c4e5e9b6c95b498ad155ec1e69fc9d6ba5f3e7e32b"
    );
    let cases = items(field(&vectors, "cases"));
    // 45 discovery cases reach `finish`; 19 refuse upward (B2-b3's); 34 controls,
    // eight of them the marker judgment order (r2, Codex B2B2-1).
    assert_eq!(cases.len(), 79);
    assert_eq!(items(field(&vectors, "upwardOnly")).len(), 19);
    let (mut accepted, mut refused) = (0, 0);
    for case in cases {
        let id = text(field(case, "id"));
        let got = run(case);
        assert_eq!(&result(&got), field(case, "expected"), "{id}");
        match boundary_inventory(&got) {
            Ok(inventory) => {
                accepted += 1;
                assert_eq!(&inventory.to_json(), field(case, "inventory"), "{id}");
            }
            Err(InventoryRefusal::NotAccepted) => {
                refused += 1;
                assert_eq!(field(case, "inventory"), &V::Null, "{id}");
            }
            Err(other) => panic!("{id}: {other:?}"),
        }
    }
    assert_eq!((accepted, refused), (65, 14));
}

fn metadata(mode: u32, uid: u32) -> DescriptorMetadata {
    DescriptorMetadata {
        device: 1,
        inode: 1,
        mode,
        uid,
        gid: 20,
        links: 1,
        size: 10,
        modified: (0, 0),
        changed: (0, 0),
        flags: 0,
    }
}

#[test]
fn the_waiver_skips_only_the_owner_comparison() {
    let groups = BTreeSet::new();
    let waiver = ProjectOwnerWaiver::from_invocation(true, Some(std::path::Path::new("/h/w")))
        .unwrap()
        .unwrap();
    let judge = |m: &DescriptorMetadata,
                 acl: &[CapturedAclEntry],
                 waiver: Option<&ProjectOwnerWaiver>,
                 object| {
        check_project_object_waived(
            m,
            CapturedAclState::Entries(acl.len()),
            |i| acl.get(i).copied(),
            1000,
            &groups,
            object,
            waiver,
        )
    };
    for object in [ProjectObject::Directory, ProjectObject::ConfigurationFile] {
        let kind = if matches!(object, ProjectObject::Directory) {
            0o040755
        } else {
            0o100644
        };
        let foreign = metadata(kind, 1001);
        assert_eq!(
            judge(&foreign, &[], None, object),
            Err(super::super::Refusal::ForeignOwner)
        );
        assert_eq!(judge(&foreign, &[], Some(&waiver), object), Ok(()));
        // Mode and ACL checks still apply under the waiver.
        assert_eq!(
            judge(&metadata(kind | 0o002, 1001), &[], Some(&waiver), object),
            Err(super::super::Refusal::OthersWrite)
        );
        let acl = [CapturedAclEntry {
            flags: WRITE_ACE.0,
            rights: WRITE_ACE.1,
            principal: CapturedAclPrincipal::User(4242),
        }];
        assert_eq!(
            judge(&foreign, &acl, Some(&waiver), object),
            Err(super::super::Refusal::AclWrite)
        );
        // The legacy judge is the waived judge with no waiver.
        assert_eq!(
            super::super::project_chain::check_project_object(
                &foreign,
                CapturedAclState::Entries(0),
                |_| None,
                1000,
                &groups,
                object
            ),
            judge(&foreign, &[], None, object)
        );
    }
}

#[test]
fn the_pending_provenance_cannot_be_emitted_or_completed() {
    let code: String = SOURCE
        .lines()
        .map(|l| l.split("//").next().unwrap())
        .collect::<Vec<_>>()
        .join("\n");
    for forbidden in [
        "WorkspaceDeclaration",
        "fn complete",
        "Serialize",
        "serde",
        "impl DiscoveryProvenancePending",
        "workspaceDeclarations",
    ] {
        assert!(!code.contains(forbidden), "{forbidden}");
    }
    // Only the complete boundary inventory has a JSON projection.
    assert_eq!(code.matches("fn to_json").count(), 1);
    assert_eq!(code.matches("impl BoundaryInventory {").count(), 1);
}

#[test]
fn the_core_is_pure() {
    let code: String = SOURCE
        .lines()
        .map(|l| l.split("//").next().unwrap())
        .collect::<Vec<_>>()
        .join("\n");
    for forbidden in [
        "std::fs",
        "std::io",
        "std::env",
        "std::process",
        "std::net",
        "RetainedDirectory",
        "WorkScope",
        "unsafe",
    ] {
        assert!(!code.contains(forbidden), "{forbidden}");
    }
}

#[test]
fn a_boundary_inventory_needs_an_accepted_result() {
    let groups = AuthorizedGroups::from_invocation(&[]).unwrap();
    let members = BTreeSet::new();
    let mut scope = ObservedScope::default();
    scope.entries.insert(
        String::new(),
        ObservedEntry {
            metadata: metadata(0o040755, 1000),
            acl: ObservedAcl::Entries(Vec::new()),
            vcs: None,
        },
    );
    let upward = UpwardProvenance {
        mode: "explicit".to_owned(),
        config_path: None,
        walked: Vec::new(),
        stop_reason: "EXPLICIT".to_owned(),
        vcs: None,
        explicit_path_was_symlink: Some(false),
    };
    let refused = discover(
        &scope,
        "/h/w",
        upward,
        &DiscoveryInvocation {
            invoking_uid: 1000,
            ci: false,
            groups: &groups,
            waiver: None,
            source: UnitSourceRequest::ExplicitJoins(vec!["../x".to_owned()]),
            basis: MarkerCountBasis::NotEnumerated,
            member_roots: &members,
        },
    );
    assert!(
        matches!(&refused, DiscoveryResultPending::Refuse { detail, .. } if detail == "JOIN_PATH_GRAMMAR")
    );
    assert_eq!(
        boundary_inventory(&refused),
        Err(InventoryRefusal::NotAccepted)
    );
}

#[test]
fn the_waiver_reaches_the_explicit_chain_and_never_a_marker() {
    let groups = AuthorizedGroups::from_invocation(&[]).unwrap();
    let members = BTreeSet::new();
    let waiver = ProjectOwnerWaiver::from_invocation(true, Some(std::path::Path::new("/h/w")))
        .unwrap()
        .unwrap();
    let observed = |mode, uid| ObservedEntry {
        metadata: metadata(mode, uid),
        acl: ObservedAcl::Entries(Vec::new()),
        vcs: None,
    };
    let mut scope = ObservedScope::default();
    scope
        .entries
        .insert(String::new(), observed(0o040755, 1001));
    scope
        .entries
        .insert("u".to_owned(), observed(0o040755, 1001));
    scope
        .entries
        .insert("u/package.json".to_owned(), observed(0o100644, 1001));
    scope
        .entries
        .insert("u/Cargo.toml".to_owned(), observed(0o100644, 1000));
    let run = |waiver| {
        discover(
            &scope,
            "/h/w",
            UpwardProvenance {
                mode: "explicit".to_owned(),
                config_path: None,
                walked: Vec::new(),
                stop_reason: "EXPLICIT".to_owned(),
                vcs: None,
                explicit_path_was_symlink: Some(false),
            },
            &DiscoveryInvocation {
                invoking_uid: 1000,
                ci: false,
                groups: &groups,
                waiver,
                source: UnitSourceRequest::ExplicitJoins(vec!["u".to_owned()]),
                basis: MarkerCountBasis::NotEnumerated,
                member_roots: &members,
            },
        )
    };
    // Without the waiver, the foreign-owned chain refuses.
    let DiscoveryResultPending::Refuse {
        refusal, detail, ..
    } = run(None)
    else {
        panic!()
    };
    assert_eq!(
        (refusal, detail.as_str()),
        (DiscoveryRefusal::RootCustodyRefused, "FOREIGN_OWNER")
    );
    // With it, the chain is admitted, while the foreign-owned marker is not.
    let DiscoveryResultPending::Accept(p) = run(Some(&waiver)) else {
        panic!()
    };
    assert_eq!(p.custody_waiver, Some("trustProjectOwner"));
    assert_eq!(p.units.len(), 1);
    assert_eq!(p.units[0].markers, ["Cargo.toml"]);
    assert_eq!(
        p.excluded_units,
        [ExcludedUnit {
            path: "/h/w/u".to_owned(),
            reason: "MARKER_CUSTODY:package.json:FOREIGN_OWNER".to_owned(),
        }]
    );
}

#[test]
fn the_inventory_drops_units_already_explained_by_a_nested_boundary() {
    let groups = AuthorizedGroups::from_invocation(&[]).unwrap();
    let members = BTreeSet::new();
    let observed = |mode, vcs| ObservedEntry {
        metadata: metadata(mode, 1000),
        acl: ObservedAcl::Entries(Vec::new()),
        vcs,
    };
    let mut scope = ObservedScope::default();
    scope
        .entries
        .insert(String::new(), observed(0o040755, None));
    scope
        .entries
        .insert("package.json".to_owned(), observed(0o100644, None));
    // A nested repository holding a marker, and a nested project holding one.
    scope.entries.insert(
        "r".to_owned(),
        observed(0o040755, Some(ObservedVcs::Directory)),
    );
    scope
        .entries
        .insert("r/package.json".to_owned(), observed(0o100644, None));
    scope
        .entries
        .insert("p".to_owned(), observed(0o040755, None));
    scope
        .entries
        .insert("p/opensip.json".to_owned(), observed(0o100644, None));
    scope
        .entries
        .insert("p/Cargo.toml".to_owned(), observed(0o100644, None));
    let result = discover(
        &scope,
        "/h/w",
        UpwardProvenance {
            mode: "cwd-default".to_owned(),
            config_path: None,
            walked: Vec::new(),
            stop_reason: "HOME".to_owned(),
            vcs: None,
            explicit_path_was_symlink: None,
        },
        &DiscoveryInvocation {
            invoking_uid: 1000,
            ci: false,
            groups: &groups,
            waiver: None,
            source: UnitSourceRequest::Automatic,
            basis: MarkerCountBasis::NotEnumerated,
            member_roots: &members,
        },
    );
    let DiscoveryResultPending::Accept(p) = &result else {
        panic!("{result:?}")
    };
    let reasons: Vec<(&str, &str)> = p
        .excluded_units
        .iter()
        .map(|r| (r.path.as_str(), r.reason.as_str()))
        .collect();
    assert_eq!(
        reasons,
        [
            ("/h/w/p", "INSIDE_NESTED_PROJECT"),
            ("/h/w/r", "INSIDE_NESTED_REPOSITORY")
        ]
    );
    let inventory = boundary_inventory(&result).unwrap();
    // Already explained by their boundaries, so not repeated as custody exclusions.
    assert!(inventory.custody_excluded_units.is_empty());
    assert_eq!(
        (inventory.nested_repositories, inventory.nested_projects),
        (vec!["r".to_owned()], vec!["p".to_owned()])
    );
}

#[test]
fn discovery_judges_a_files_acl_before_its_links_and_size_and_the_legacy_judge_keeps_its_order() {
    let groups = BTreeSet::new();
    let acl = [CapturedAclEntry {
        flags: WRITE_ACE.0,
        rights: WRITE_ACE.1,
        principal: CapturedAclPrincipal::User(4242),
    }];
    for (links, size) in [(2, 10), (1, super::super::MAX_CONFIG_BYTES + 1)] {
        let file = DescriptorMetadata {
            links,
            size,
            ..metadata(0o100644, 1000)
        };
        let legacy = super::super::project_chain::check_project_object(
            &file,
            CapturedAclState::Entries(1),
            |i| acl.get(i).copied(),
            1000,
            &groups,
            ProjectObject::ConfigurationFile,
        );
        assert!(matches!(
            legacy,
            Err(super::super::Refusal::HardLinked | super::super::Refusal::TooLarge)
        ));
        let discovery = reference_order(
            &file,
            CapturedAclState::Entries(1),
            &acl,
            1000,
            &groups,
            ProjectObject::ConfigurationFile,
            None,
        );
        assert_eq!(discovery, Err(super::super::Refusal::AclWrite));
        let unreadable = reference_order(
            &file,
            CapturedAclState::NotReturned,
            &[],
            1000,
            &groups,
            ProjectObject::ConfigurationFile,
            None,
        );
        assert_eq!(unreadable, Err(super::super::Refusal::AclUnreadable));
        // With a clean ACL, links and size still refuse in that order.
        let clean = reference_order(
            &file,
            CapturedAclState::Entries(0),
            &[],
            1000,
            &groups,
            ProjectObject::ConfigurationFile,
            None,
        );
        assert_eq!(
            clean,
            Err(if links != 1 {
                super::super::Refusal::HardLinked
            } else {
                super::super::Refusal::TooLarge
            })
        );
    }
}
