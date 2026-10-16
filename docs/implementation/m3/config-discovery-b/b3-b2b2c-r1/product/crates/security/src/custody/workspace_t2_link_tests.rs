// Unit B3-b2b2c's T2 link-map controls (M3-B r9 item 20's first control; B3-b
// plan r2 section 3 and amendment A3). The check lane runs
// tools/security/t2_link_controls.py first: it re-verifies each lead-readable
// Cargo and npm T2 workspace's stores and overlay against their pins and
// writes a minimal `vcs: none` reconstruction (the exact provider manifests
// and the carrier rendered from the overlay) under the lane's private
// temporary directory, never in a repository. These tests read it there and
// are run only by the lane (`--ignored`): no corpus byte is a fixture.

/// The four T2 workspaces with a D15 reader and the overlay digest each is
/// checked by (the reviewed T2 manifest's `overlayDigest`; Python has no
/// reader at M3, law item 20).
const T2_LINKED: [(&str, &str); 4] = [
    (
        "mr-rs-large-aws-lambda-tokio",
        "e8f4bf0311e6cac2afb9debedc968087a3157f4051d7964001b8c72ef482cbab",
    ),
    (
        "mr-rs-medium-serde-json",
        "68cb5d5b14445997755c5c49b4042f122592a2b516ab607416ab62e664aab2a9",
    ),
    (
        "mr-ts-large-smithy-powertools",
        "1006513e537c53f923ba51596da1732f68cee98dce44e005a5137dca15b9484f",
    ),
    (
        "mr-ts-very-large-smithy-sdk",
        "6bec503038e9b49f107ee0b1c9b2c60595a44956e14519b6c2c10bec6533b88e",
    ),
];

/// One reconstruction: its tree, its member mounts, the mounts that provide
/// a linked package (the ones the rendered carrier declares) and the
/// overlay's link map as (package, `<mount>/<directory>`).
struct Reconstruction {
    tree: PathBuf,
    ecosystem: String,
    members: BTreeSet<String>,
    providers: BTreeSet<String>,
    links: BTreeSet<(String, String)>,
}

/// The lane's reconstructions, each checked against its pinned overlay
/// digest: the overlay record's own SHA-256, and the link map read from it.
fn reconstructions() -> Vec<(&'static str, Reconstruction)> {
    let base = std::env::temp_dir().join("opensip-t2-link-controls");
    let mut found: Vec<String> = std::fs::read_dir(&base)
        .unwrap_or_else(|e| panic!("run tools/security/t2_link_controls.py first: {e}"))
        .map(|e| e.unwrap().file_name().into_string().unwrap())
        .collect();
    found.sort();
    let ids: Vec<&str> = T2_LINKED.iter().map(|(id, _)| *id).collect();
    assert_eq!(found, ids, "exactly the four linked T2 workspaces");
    T2_LINKED
        .iter()
        .map(|&(id, digest)| {
            let expected =
                parse_json(&std::fs::read(base.join(id).join("expected.json")).unwrap()).unwrap();
            let overlay = text(field(&expected, "overlay"));
            assert_eq!(
                opensip_identity::digest_hex(&opensip_identity::raw_sha256(overlay.as_bytes())),
                digest,
                "{id}: the overlay record is the pinned one"
            );
            let overlay = parse_json(overlay.as_bytes()).unwrap();
            let ecosystem = text(field(&expected, "ecosystem")).to_owned();
            let V::Object(map) = field(field(&overlay, "links"), &ecosystem) else {
                panic!("{id}: no {ecosystem} links")
            };
            let links: BTreeSet<(String, String)> = map
                .iter()
                .map(|(name, dir)| (name.clone(), text(dir).to_owned()))
                .collect();
            let members: BTreeSet<String> = items(field(&overlay, "members"))
                .iter()
                .map(|m| text(field(m, "mount")).to_owned())
                .collect();
            // A member declares itself only through an entry naming it (law
            // item 20): the carrier names each link's directory, so the
            // declared members are the providing mounts. A consumer-only
            // member is not declared, and is no boundary either.
            let providers: BTreeSet<String> = links
                .iter()
                .map(|(_, dir)| dir.split('/').next().unwrap().to_owned())
                .collect();
            assert!(
                providers.is_subset(&members),
                "{id}: a link outside the overlay members"
            );
            (
                id,
                Reconstruction {
                    tree: base.join(id).join("w"),
                    ecosystem,
                    members,
                    providers,
                    links,
                },
            )
        })
        .collect()
}

/// A copy of `from` at `to`, directories 0755 and files 0644, so custody
/// passes as for any project the invoking user owns.
fn copy_tree(from: &Path, to: &Path) {
    std::fs::create_dir(to).unwrap();
    std::fs::set_permissions(to, std::fs::Permissions::from_mode(0o755)).unwrap();
    let mut names: Vec<_> = std::fs::read_dir(from)
        .unwrap()
        .map(|e| e.unwrap())
        .collect();
    names.sort_by_key(|e| e.file_name());
    for entry in names {
        let kind = entry.file_type().unwrap();
        let target = to.join(entry.file_name());
        if kind.is_dir() {
            copy_tree(&entry.path(), &target);
        } else {
            assert!(
                kind.is_file(),
                "a reconstruction holds only directories and files"
            );
            std::fs::copy(entry.path(), &target).unwrap();
            std::fs::set_permissions(&target, std::fs::Permissions::from_mode(0o644)).unwrap();
        }
    }
}

/// The selection's provenance for an explicit `--project W`.
fn explicit_upward(w: &Path) -> UpwardProvenance {
    UpwardProvenance {
        mode: "explicit".to_owned(),
        config_path: None,
        walked: vec![WalkRow {
            path: w.to_str().unwrap().to_owned(),
            custody: "PASS".to_owned(),
            candidate: "ABSENT".to_owned(),
            boundary: Some("EXPLICIT".to_owned()),
        }],
        stop_reason: "EXPLICIT".to_owned(),
        vcs: None,
        explicit_path_was_symlink: Some(false),
    }
}

/// The derived links as (package, `<mount>/<directory>`), each of the
/// reconstruction's ecosystem and provided by its own mount.
fn derived(id: &str, r: &Reconstruction, links: &[LinkRow], w: &str) -> BTreeSet<(String, String)> {
    links
        .iter()
        .map(|l| {
            assert_eq!(l.ecosystem, r.ecosystem, "{id}");
            let member = l
                .provider_member
                .strip_prefix(w)
                .unwrap_or(&l.provider_member);
            let member = member.trim_start_matches('/');
            assert!(
                l.package_dir == member || l.package_dir.starts_with(&format!("{member}/")),
                "{id}: {} is outside its provider {member}",
                l.package_dir
            );
            (l.package_name.clone(), l.package_dir.clone())
        })
        .collect()
}

/// Item 6b's outcome and the members' placement supplied by the control, at
/// the link stage only (plan r2 section 3, (a); Codex NBO-1: never a
/// production placement bypass). Every other observation is the native one.
struct Supplied<'o, 'r, 'w, 's> {
    inner: NativeObservation<'r, 'w, 's>,
    members: &'o BTreeSet<String>,
}
impl super::super::workspace_declarations::WorkspaceObservation for Supplied<'_, '_, '_, '_> {
    type Error = Failure;
    fn entry(
        &mut self,
        rel: &str,
    ) -> Result<Option<crate::custody::discovery_scan::ObservedEntry>, Failure> {
        self.inner.entry(rel)
    }
    fn markers(&mut self, rel: &str) -> Result<Vec<(&'static str, bool)>, Failure> {
        // A member mount is placed as T2's assembly would hold it under
        // `git-conventional`; nothing else is.
        if self.members.contains(rel) {
            return Ok(vec![(".git", true)]);
        }
        self.inner.markers(rel)
    }
    fn children(&mut self, rel: &str) -> Result<Vec<String>, Failure> {
        self.inner.children(rel)
    }
    fn bytes(
        &mut self,
        rel: &str,
    ) -> Result<super::super::workspace_declarations::FileBytes, Failure> {
        self.inner.bytes(rel)
    }
    fn custody_entry(
        &mut self,
        rel: &str,
        object: crate::custody::project_chain::ProjectObject,
    ) -> Result<Option<crate::custody::discovery_scan::ObservedEntry>, Failure> {
        self.inner.custody_entry(rel, object)
    }
    fn member_verdict(
        &mut self,
        candidate: &str,
    ) -> Result<super::super::workspace_declarations::MemberOutcome, Failure> {
        assert!(
            self.members.contains(candidate),
            "only an overlay member is a candidate"
        );
        Ok(
            super::super::workspace_declarations::MemberOutcome::Admitted {
                gitlinks: Vec::new(),
            },
        )
    }
}

#[test]
#[ignore = "T2 link-map control (a), run by the check lane over its verified reconstruction"]
fn t2_vcs_none_reconstructions_give_the_overlay_link_maps_with_supplied_members() {
    // Plan r2 section 3 (a): each reader carrier's declarations, with the
    // overlay's members supplied at the link stage, give exactly the
    // overlay's link map, checked by its digest.
    churned(|| {
        for (id, r) in reconstructions() {
            let (_s, home, _githome) = scratch();
            let w = home.join("w");
            copy_tree(&r.tree, &w);
            let premise = premise();
            let groups = BTreeSet::new();
            let volume = any_volume;
            let policy = ProjectChainPolicy::new(Some(&premise), &volume, &groups);
            let inputs = DecisionInputs {
                invoking_uid: uid(),
                groups: &groups,
                waiver: None,
                no_repository: true,
                array: &[],
                array_source: ArraySource::ConfigWorkspaceRoots,
            };
            let decision = WorkLedger::discovery_profile()
                .scope(|work| {
                    let chain =
                        walk_project_chain(&home, &w, uid(), &policy, work).map_err(invariant)?;
                    let root =
                        DiscoveryRoot::for_tests(chain.root(), chain.spelling(), Some(&premise));
                    let bound: Bindings = std::cell::RefCell::new(BTreeMap::new());
                    let mut obs = Supplied {
                        inner: NativeObservation::new(
                            &root,
                            uid(),
                            &groups,
                            None,
                            None,
                            &bound,
                            work,
                        ),
                        members: &r.providers,
                    };
                    phase_one(&mut obs, &inputs)
                })
                .unwrap_or_else(|e| panic!("{id}: {e:?}"));
            let PhaseOne::Decided(Decision::Members {
                members,
                declarations,
                links,
                ..
            }) = decision
            else {
                panic!("{id}: branch B decides its members")
            };
            let admitted: BTreeSet<String> = members.into_iter().map(|m| m.path).collect();
            assert_eq!(
                admitted, r.providers,
                "{id}: every providing member is declared"
            );
            let row = declarations
                .iter()
                .find(|d| d.state == super::super::workspace_declarations::ReaderState::Read)
                .unwrap_or_else(|| panic!("{id}: the carrier is read"));
            assert!(row.unresolved.is_empty(), "{id}: {:?}", row.unresolved);
            assert_eq!(
                derived(id, &r, &links, ""),
                r.links,
                "{id}: the overlay's link map"
            );
        }
    });
}

#[test]
#[ignore = "T2 link-map control (b), run by the check lane over its verified reconstruction"]
fn t2_reconstructions_with_conventional_git_members_link_through_discovery() {
    // Plan r2 section 3 (b): the same reconstructions, each member given a
    // synthetic conventional `.git` with an empty valid index, through the
    // unchanged product discovery: item 6b admits every member, the links
    // are the overlay's, and the record is complete.
    churned(|| {
        for (id, r) in reconstructions() {
            let (_s, home, githome) = scratch();
            let w = home.join("w");
            copy_tree(&r.tree, &w);
            for member in &r.members {
                git(&githome, &w.join(member), &["init", "-q"]);
                git(&githome, &w.join(member), &["read-tree", "--empty"]);
                assert!(
                    w.join(member).join(".git/index").is_file(),
                    "{id}: an empty index"
                );
            }
            let discovery = discover_at(
                &home,
                &w,
                &explicit_upward(&w),
                UnitSourceRequest::Automatic,
                None,
            )
            .unwrap_or_else(|e| panic!("{id}: {e:?}"));
            let native = w.to_str().unwrap().to_owned();
            let DiscoveryResultV3::Accept(provenance) = &discovery.result else {
                panic!("{id}: {:?}", discovery.result)
            };
            let admitted: BTreeSet<String> = provenance
                .members
                .iter()
                .map(|m| {
                    m.path
                        .strip_prefix(&format!("{native}/"))
                        .unwrap()
                        .to_owned()
                })
                .collect();
            assert_eq!(
                admitted, r.providers,
                "{id}: item 6b admits every declared member"
            );
            for m in &provenance.members {
                assert!(
                    m.declared_by
                        .iter()
                        .all(|d| matches!(d, Declarer::Reader { .. }))
                        && !m.declared_by.is_empty(),
                    "{id}: declared by its reader"
                );
            }
            // A consumer-only member, undeclared, stays a nested repository.
            let nested: BTreeSet<String> = provenance
                .core
                .nested_repositories
                .iter()
                .map(|p| p.strip_prefix(&format!("{native}/")).unwrap().to_owned())
                .collect();
            let undeclared: BTreeSet<String> =
                r.members.difference(&r.providers).cloned().collect();
            assert_eq!(nested, undeclared, "{id}: no declared member is a boundary");
            let rows: Vec<_> = provenance
                .declarations
                .iter()
                .filter(|d| d.state == super::super::workspace_declarations::ReaderState::Read)
                .collect();
            assert_eq!(rows.len(), 1, "{id}: one carrier read");
            assert!(
                rows[0].unresolved.is_empty(),
                "{id}: {:?}",
                rows[0].unresolved
            );
            assert_eq!(
                derived(id, &r, &discovery.links, &native),
                r.links,
                "{id}: the overlay's link map"
            );
            // The record is complete: its V3 serialization carries the D15 fields.
            let json = discovery.result.to_json();
            let prov = field(&json, "provenance");
            assert_eq!(
                items(field(prov, "memberRepositories")).len(),
                r.providers.len(),
                "{id}"
            );
            assert_eq!(items(field(prov, "workspaceDeclarations")).len(), 2, "{id}");
        }
    });
}
