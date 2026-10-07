use super::super::core_anchor::BindingError;
use super::super::core_authentication::AuthenticationError;
use super::super::core_authentication::tests::{
    COMPONENT_SIGNER, INDEX_SIGNER, Signed, Signer, Spec, signed_release,
};
use super::super::core_release_embedding::EmbeddedRootBinding;
use super::*;
use opensip_platform::WorkLedger;
use std::{
    ffi::OsString,
    fs,
    os::unix::fs::{MetadataExt, PermissionsExt},
    path::{Path, PathBuf},
    sync::atomic::AtomicBool,
};

/// Law 463 item 11: a test-only running image. The parent chain and the leaf
/// are opened and hashed like the live observation; status is given.
pub(super) struct InjectedImage {
    pub(super) status: u32,
    pub(super) cdhash: [u8; 20],
    pub(super) parents: RetainedDirectoryPath,
    pub(super) leaf: OsString,
    pub(super) file: File,
    pub(super) metadata: DescriptorMetadata,
    pub(super) sha256: [u8; 32],
    pub(super) length: usize,
}
fn native(e: io::Error) -> RunningImageError {
    RunningImageError::Native(e)
}
impl InjectedImage {
    fn open(exe: &Path, status: u32, work: &mut WorkScope<'_>) -> Result<Self, Failure> {
        let image = |e| R::Image(native(e));
        let parents = RetainedDirectoryPath::open_accounted(exe.parent().unwrap(), 256, work)
            .map_err(lift(image))?;
        let leaf = exe.file_name().unwrap().to_owned();
        let text = leaf.to_str().unwrap();
        let file = work.run(RetainedDirectory::open_regular_cost(text), |_| {
            parents
                .directory()
                .open_regular(text)
                .map_err(|e| WorkFailure::Operation(image(e)))
        })?;
        let raw = opensip_platform::read_bounded_accounted(&file, MAX_FILE_BYTES, work)
            .map_err(lift(|_| R::Image(RunningImageError::Limit)))?;
        let metadata = opensip_platform::capture_descriptor_acl_accounted(&file, work)
            .map_err(lift(|e| R::Acl(CoreMember::Executable, e)))?
            .metadata()
            .clone();
        Ok(Self {
            status,
            cdhash: [0; 20],
            parents,
            leaf,
            file,
            metadata,
            sha256: raw_sha256(&raw),
            length: raw.len(),
        })
    }
    pub(super) fn leaf_name_matches_accounted(
        &self,
        work: &mut WorkScope<'_>,
    ) -> Result<bool, WorkFailure<RunningImageError>> {
        opensip_platform::descriptor_name_matches_accounted(&self.file, &self.leaf, work).map_err(
            |f| match f {
                WorkFailure::Budget(b) => WorkFailure::Budget(b),
                WorkFailure::Operation(e) => WorkFailure::Operation(native(e)),
            },
        )
    }
    pub(super) fn recheck(
        &self,
        work: &mut WorkScope<'_>,
    ) -> Result<(), WorkFailure<RunningImageError>> {
        let lifted = |f: WorkFailure<io::Error>| match f {
            WorkFailure::Budget(b) => WorkFailure::Budget(b),
            WorkFailure::Operation(e) => WorkFailure::Operation(native(e)),
        };
        if !self
            .parents
            .recheck_exact_names_accounted(work)
            .map_err(lifted)?
        {
            return Err(WorkFailure::Operation(RunningImageError::Changed));
        }
        let text = self.leaf.to_str().unwrap();
        work.run(RetainedDirectory::open_regular_cost(text), |_| {
            let now = self
                .parents
                .directory()
                .open_regular(text)
                .and_then(|f| f.metadata())
                .map_err(|e| WorkFailure::Operation(native(e)))?;
            if (now.dev(), now.ino()) != (self.metadata.device, self.metadata.inode) {
                return Err(WorkFailure::Operation(RunningImageError::Changed));
            }
            Ok(())
        })
    }
}

/// Law X3d r8 item 13 (unit X3d-3): the core evaluator closure's preimages,
/// for the synthetic run candidate only: the closure descriptor (contract
/// successor EC1), the TR-CORE-signed inventory body (its `manifestDigest`)
/// and each tree member's bytes by logical path, read through this core's
/// retained tree root by exact names and judged as `open_release_file`
/// judges a release file. It lives in this shared fixture module, so it is
/// absent from every release build. Panics if a member cannot be read or is
/// not the inventory's, as every fixture does.
impl InitialCore {
    pub(crate) fn evaluator_closure_preimages(
        &self,
    ) -> (V, Vec<u8>, std::collections::BTreeMap<String, Vec<u8>>) {
        let inventory = self.release.authentication().core().inventory();
        let descriptor = Core::evaluator_descriptor(inventory.descriptor());
        let mut tree = std::collections::BTreeMap::new();
        let mut ledger = WorkLedger::new();
        for path in inventory.files()[self.platform].keys() {
            let components: Vec<&str> = path.split('/').collect();
            let (_, raw) = ledger
                .scope(|work| self.open_release_file(&components, work))
                .unwrap_or_else(|e| panic!("core tree member {path}: {e:?}"));
            let (sha256, length) = self.tree_file(path).expect("an inventory tree member");
            assert_eq!(
                (raw_sha256(&raw), raw.len() as i64),
                (sha256, length),
                "{path}"
            );
            tree.insert(path.clone(), raw);
        }
        (descriptor, inventory.raw().to_vec(), tree)
    }
}

pub(crate) fn platform() -> &'static str {
    COMPILED_PLATFORM.unwrap()
}
pub(crate) fn hex(b: &[u8]) -> String {
    b.iter().map(|b| format!("{b:02x}")).collect()
}

/// A signed release written under a canonical scratch directory as
/// `core/…`, every directory 0755 and file 0644, each with one owner
/// zero-rights ACL entry unless skipped. Shared with 462's tests.
pub(crate) struct Tree {
    pub(crate) base: PathBuf,
    pub(crate) core: PathBuf,
    pub(crate) signed: Signed,
    root_schema: u8,
}
impl Drop for Tree {
    fn drop(&mut self) {
        let _ = fs::remove_dir_all(&self.base);
    }
}
impl Tree {
    pub(crate) fn new(tag: &str, spec: &Spec, skip_acl: Option<&str>) -> Self {
        let signed = signed_release(spec);
        let base = fs::canonicalize(crate::test_scratch::temp_dir())
            .unwrap()
            .join(format!(
                "opensip-initial-core463-{tag}-{}",
                hex(&opensip_platform::request_entropy().unwrap())
            ));
        let core = base.join("core");
        let mut files: Vec<(String, Vec<u8>)> = vec![
            ("inventory.json".into(), signed.inventory.clone()),
            ("inventory.sig.json".into(), signed.inventory_env.clone()),
            (spec.entrypoint.into(), signed.exe.clone()),
        ];
        for (path, raw) in spec.tree_files {
            files.push(((*path).into(), raw.to_vec()));
        }
        for (name, raw) in &signed.bootstrap {
            files.push((format!("{}/{name}", spec.bootstrap), raw.clone()));
        }
        fs::create_dir(&base).unwrap();
        let mut directories = vec![String::new()];
        for (path, _) in &files {
            for (i, _) in path.match_indices('/') {
                if !directories.iter().any(|d| d == &path[..i]) {
                    directories.push(path[..i].into());
                }
            }
        }
        directories.sort();
        let mut ledger = WorkLedger::new();
        let mut protect = |relative: &str, file: &File, mode: u32| {
            file.set_permissions(fs::Permissions::from_mode(mode))
                .unwrap();
            if skip_acl != Some(relative) {
                ledger
                    .scope(|work| opensip_platform::append_owner_zero_allow_accounted(file, work))
                    .unwrap();
            }
        };
        for relative in &directories {
            let path = core.join(relative);
            fs::create_dir(&path).unwrap();
            protect(relative, &File::open(&path).unwrap(), 0o755);
        }
        for (relative, raw) in &files {
            let path = core.join(relative);
            fs::write(&path, raw).unwrap();
            protect(relative, &File::open(&path).unwrap(), 0o644);
        }
        Self {
            base,
            core,
            signed,
            root_schema: spec.root_schema,
        }
    }
    pub(crate) fn exe(&self) -> PathBuf {
        self.core.join("bin/opensip")
    }
    fn root(&self) -> EmbeddedRootBinding {
        EmbeddedRootBinding::new(self.root_schema, 1, &hex(&self.signed.root_digest))
    }
    pub(crate) fn release(
        &self,
        entrypoint: &'static str,
        bootstrap: &'static str,
    ) -> EmbeddedCoreRelease {
        EmbeddedCoreRelease::new(Some(self.root()), Some(entrypoint), Some(bootstrap))
    }
}
pub(crate) fn produce(
    release: &EmbeddedCoreRelease,
    exe: &Path,
    status: u32,
) -> (Result<InitialCore, Failure>, InitialInstallationAttempt) {
    produce_as(release, exe, status, platform(), None)
}
/// `produce` for a given compiled platform and ledger limits (law 462 tests).
pub(crate) fn produce_as(
    release: &EmbeddedCoreRelease,
    exe: &Path,
    status: u32,
    platform: &'static str,
    limits: Option<WorkCost>,
) -> (Result<InitialCore, Failure>, InitialInstallationAttempt) {
    let flag = AtomicBool::new(false);
    let mut attempt = InitialInstallationAttempt::for_tests(&flag, limits).unwrap();
    let produced = produce_with(&mut attempt, release, Some(platform), |work| {
        InjectedImage::open(exe, status, work).map(Image::Injected)
    });
    if produced.is_err() {
        assert!(attempt.is_latched());
    }
    (produced, attempt)
}
/// InitialCore on a caller's attempt through the injected image, for a
/// composition that allocates its own attempt (law 458c tests).
pub(crate) fn produce_on(
    attempt: &mut InitialInstallationAttempt,
    release: &EmbeddedCoreRelease,
    exe: &Path,
    platform: &'static str,
) -> Result<InitialCore, Failure> {
    produce_with(attempt, release, Some(platform), |work| {
        InjectedImage::open(exe, 1, work).map(Image::Injected)
    })
}
pub(crate) fn spec() -> Spec<'static> {
    Spec {
        platform: platform(),
        ..Spec::default()
    }
}
fn refused(tree: &Tree, release: &EmbeddedCoreRelease, status: u32) -> InitialCoreRefusal {
    refused_at(release, &tree.exe(), status)
}
fn refused_at(release: &EmbeddedCoreRelease, exe: &Path, status: u32) -> InitialCoreRefusal {
    match produce(release, exe, status).0 {
        Err(WorkFailure::Operation(refusal)) => refusal,
        other => panic!("{other:?}"),
    }
}
pub(crate) const STANDARD: (&str, &str) = ("bin/opensip", "trust/bootstrap");

#[test]
fn crc1_authenticated_initial_core_exposes_the_same_selected_role_ids() {
    let tree = Tree::new("crc1-positive", &spec(), None);
    let release = tree.release(STANDARD.0, STANDARD.1);
    let (core, _) = produce(&release, &tree.exe(), 0x0001_0301 | 0x4);
    let core = core.unwrap();
    let projection = Core::project_v3(&tree.signed.inventory, platform()).unwrap();
    let p = projection.core();
    assert_eq!(core.detector_closure(), p.detector_closure());
    assert_eq!(core.provider_closure(), p.provider_closure());
    assert_eq!(core.adapter_closure(), p.adapter_closure());
    assert_eq!(core.evaluator_closure(), p.evaluator_closure());
    assert_eq!(
        std::collections::BTreeSet::from([
            core.closure(),
            core.evaluator_closure(),
            core.detector_closure(),
            core.provider_closure(),
            core.adapter_closure()
        ])
        .len(),
        5
    );
}

#[test]
fn a_signed_tree_yields_the_closure_k_and_a_rechecked_receipt() {
    for (writer, expected) in [(2, StateWriter::Stage2), (1, StateWriter::Stage1)] {
        let flags = ["CS_HARD", "CS_KILL", "CS_RUNTIME", "CS_VALID"];
        let tree = Tree::new(
            "positive",
            &Spec {
                state_writer: writer,
                flags: &flags,
                ..spec()
            },
            None,
        );
        let release = tree.release(STANDARD.0, STANDARD.1);
        let (core, mut attempt) = produce(&release, &tree.exe(), 0x0001_0301 | 0x4);
        let core = core.unwrap();
        let expected_closure = Core::project_v3(&tree.signed.inventory, platform())
            .unwrap()
            .core()
            .closure()
            .to_owned();
        assert_eq!(core.closure(), expected_closure);
        assert_eq!(core.state_writer(), expected);
        assert_eq!(core.lineage(), attempt.lineage());
        assert_eq!((core.platform(), core.cdhash()), (platform(), [0; 20]));
        assert_eq!(core.flags, 0x0001_0301);
        // core and bin; trust and trust/bootstrap; the inventory and payload
        // pairs and ten members (two roots, revocation, component manifest,
        // catalog, five envelopes).
        assert_eq!(core.tree.len(), 2);
        assert_eq!(core.directories.len(), 2);
        assert_eq!(core.files.len(), 2 + 2 + 10);
        assert_retained(&core, &tree, Some("catalog.sig.json"), 1);
        assert!(format!("{core:?}").starts_with("InitialCore"));
        let produced = attempt.used();
        core.recheck(&mut attempt).unwrap();
        let rechecked = attempt.used();
        assert!(rechecked.edges > produced.edges);
        eprintln!(
            "463 budget writer {writer}: produce {produced:?}; recheck adds {:?}",
            WorkCost {
                objects: rechecked.objects - produced.objects,
                edges: rechecked.edges - produced.edges,
                bytes: rechecked.bytes - produced.bytes,
            }
        );
        // A foreign attempt refuses and latches.
        let flag = AtomicBool::new(false);
        let mut other = InitialInstallationAttempt::for_tests(&flag, None).unwrap();
        assert!(matches!(
            core.recheck(&mut other),
            Err(WorkFailure::Operation(R::WrongAttempt))
        ));
        assert!(other.is_latched());
    }
}

#[test]
fn the_live_path_refuses_the_absent_embedding_before_any_native_call() {
    let flag = AtomicBool::new(false);
    let mut attempt = InitialInstallationAttempt::for_tests(&flag, None).unwrap();
    let lineage = attempt.used();
    assert_eq!(
        lineage,
        WorkCost {
            objects: 0,
            edges: 1,
            bytes: 16
        }
    );
    assert!(matches!(
        produce_initial_core(&mut attempt),
        Err(WorkFailure::Operation(R::EmbeddedRootAbsent))
    ));
    assert_eq!(attempt.used(), lineage);
    assert!(attempt.is_latched());
}

#[test]
fn each_absent_embedded_value_and_platform_refuses_with_its_detail() {
    let root = EmbeddedRootBinding::new(1, 1, &"0".repeat(64));
    let (e, b) = (Some(STANDARD.0), Some(STANDARD.1));
    for (release, platform, expected) in [
        (
            EmbeddedCoreRelease::new(None, e, b),
            Some("macos-aarch64"),
            "EmbeddedRootAbsent",
        ),
        (
            EmbeddedCoreRelease::new(Some(root), None, b),
            Some("macos-aarch64"),
            "EmbeddedEntrypointAbsent",
        ),
        (
            EmbeddedCoreRelease::new(Some(root), e, None),
            Some("macos-aarch64"),
            "EmbeddedBootstrapAbsent",
        ),
        (
            EmbeddedCoreRelease::new(Some(root), e, b),
            None,
            "PlatformUnavailable",
        ),
    ] {
        let flag = AtomicBool::new(false);
        let mut attempt = InitialInstallationAttempt::for_tests(&flag, None).unwrap();
        let before = attempt.used();
        let refusal = produce_with(&mut attempt, &release, platform, |_| unreachable!("native"));
        let Err(WorkFailure::Operation(refusal)) = refusal else {
            panic!("{refusal:?}")
        };
        assert_eq!(format!("{refusal:?}"), expected);
        // Only the admitted split is charged, and only once all three exist.
        let split = if platform.is_none() { 2 } else { 0 };
        assert_eq!(attempt.used().objects, before.objects + split);
        assert_eq!(attempt.used().edges, before.edges);
        assert!(attempt.is_latched());
    }
}

#[test]
fn the_entrypoint_must_name_the_image_and_its_directories() {
    let tree = Tree::new("entrypoint", &spec(), None);
    // The leaf differs.
    let release = tree.release("bin/other", STANDARD.1);
    assert!(matches!(refused(&tree, &release, 1), R::EntrypointName));
    // A directory differs.
    let release = tree.release("tools/opensip", STANDARD.1);
    assert!(matches!(refused(&tree, &release, 1), R::EntrypointName));
    // Deeper than the kernel path: the tree root would be `/` or above.
    let deep: &'static str = Box::leak(format!("{}opensip", "d/".repeat(24)).into_boxed_str());
    let release = tree.release(deep, STANDARD.1);
    assert!(matches!(refused(&tree, &release, 1), R::TreeRootBound));
}

#[test]
fn a_case_variant_directory_is_not_the_embedded_name() {
    let tree = Tree::new("case", &spec(), None);
    fs::rename(tree.core.join("bin"), tree.core.join("Bin")).unwrap();
    let release = tree.release(STANDARD.0, STANDARD.1);
    let exe = tree.core.join("Bin/opensip");
    assert!(matches!(refused_at(&release, &exe, 1), R::EntrypointName));
    // The same in the bootstrap path.
    let tree = Tree::new("case-bootstrap", &spec(), None);
    fs::rename(tree.core.join("trust"), tree.core.join("Trust")).unwrap();
    let release = tree.release(STANDARD.0, STANDARD.1);
    let refusal = refused(&tree, &release, 1);
    assert!(
        matches!(
            refusal,
            R::Name(CoreMember::Bootstrap) | R::Absent(CoreMember::Bootstrap)
        ),
        "{refusal:?}"
    );
}

#[test]
fn custody_refuses_an_omitted_acl_group_write_links_and_symlinks() {
    let release = |tree: &Tree| tree.release(STANDARD.0, STANDARD.1);
    for (skip, member) in [
        ("", CoreMember::Tree),
        ("bin", CoreMember::Tree),
        ("bin/opensip", CoreMember::Executable),
        ("trust", CoreMember::Bootstrap),
        ("inventory.sig.json", CoreMember::Inventory),
        ("trust/bootstrap/payload.json", CoreMember::Payload),
        ("trust/bootstrap/revocation.json", CoreMember::Member),
    ] {
        let tree = Tree::new("acl", &spec(), Some(skip));
        let refusal = refused(&tree, &release(&tree), 1);
        assert!(
            matches!(refusal, R::Custody(m, Refusal::AclUnreadable) if m == member),
            "{skip}: {refusal:?}"
        );
    }
    let tree = Tree::new("group", &spec(), None);
    fs::set_permissions(
        tree.core.join("inventory.json"),
        fs::Permissions::from_mode(0o664),
    )
    .unwrap();
    assert!(matches!(
        refused(&tree, &release(&tree), 1),
        R::Custody(CoreMember::Inventory, Refusal::GroupWrite)
    ));
    let tree = Tree::new("group-dir", &spec(), None);
    fs::set_permissions(
        tree.core.join("trust/bootstrap"),
        fs::Permissions::from_mode(0o775),
    )
    .unwrap();
    assert!(matches!(
        refused(&tree, &release(&tree), 1),
        R::Custody(CoreMember::Bootstrap, Refusal::GroupWrite)
    ));
    let tree = Tree::new("link", &spec(), None);
    fs::hard_link(
        tree.core.join("trust/bootstrap/payload.json"),
        tree.base.join("payload-link"),
    )
    .unwrap();
    assert!(matches!(
        refused(&tree, &release(&tree), 1),
        R::Custody(CoreMember::Payload, Refusal::HardLinked)
    ));
    let tree = Tree::new("symlink", &spec(), None);
    fs::rename(
        tree.core.join("inventory.json"),
        tree.base.join("inventory.json"),
    )
    .unwrap();
    std::os::unix::fs::symlink(
        tree.base.join("inventory.json"),
        tree.core.join("inventory.json"),
    )
    .unwrap();
    assert!(matches!(
        refused(&tree, &release(&tree), 1),
        R::Custody(CoreMember::Inventory, Refusal::Symlink)
    ));
}

/// Law 463 r9 item 2: the retained pairs are the tree's bytes with their
/// references; the catalog pair names `catalog` when admitted, and the
/// component-manifest pairs follow `members.manifests` order.
fn assert_retained(core: &InitialCore, tree: &Tree, catalog: Option<&str>, components: usize) {
    let documents = core.bootstrap_documents();
    let check = |document: &DocumentBytes, name: &str| {
        let raw = &tree.signed.bootstrap[name];
        assert_eq!(document.path(), name);
        assert_eq!(document.raw(), raw.as_slice());
        assert_eq!(document.bytes(), raw.len());
        assert_eq!(document.sha256(), raw_sha256(raw));
    };
    match (documents.catalog(), catalog) {
        (Some(pair), Some(envelope)) => {
            check(pair.body(), "catalog.json");
            check(pair.envelope(), envelope);
        }
        (None, None) => {}
        (got, want) => panic!("catalog {:?} want {want:?}", got.map(|p| p.body().path())),
    }
    assert_eq!(documents.manifests().len(), components);
    for (i, pair) in documents.manifests().iter().enumerate() {
        check(pair.body(), &format!("component-{i}.json"));
        check(pair.envelope(), &format!("component-{i}.sig.json"));
    }
}
fn produced(tree: &Tree) -> InitialCore {
    let release = tree.release(STANDARD.0, STANDARD.1);
    let (core, mut attempt) = produce(&release, &tree.exe(), 1);
    let core = core.unwrap();
    core.recheck(&mut attempt).unwrap();
    core
}

#[test]
fn the_bootstrap_may_carry_a_catalog_and_component_manifests_or_neither() {
    let two = [Some(COMPONENT_SIGNER), Some(COMPONENT_SIGNER)];
    let case = |catalog_signers: &'static [Signer<'static>], component_signers| Spec {
        catalog_signers,
        component_signers,
        ..spec()
    };
    // Each release and the bootstrap members InitialCore opens.
    let cases = [
        // Both, with two component manifests.
        (case(&[INDEX_SIGNER], &two), 12),
        // Neither: the r8 shape. The catalog body is never opened.
        (case(&[], &[]), 6),
        // A catalog and no component manifest.
        (case(&[INDEX_SIGNER], &[]), 8),
        // Component manifests and no catalog envelope.
        (case(&[], &two), 10),
    ];
    for (i, (release, members)) in cases.iter().enumerate() {
        let (catalog_signers, component_signers) =
            (release.catalog_signers, release.component_signers);
        let tree = Tree::new(&format!("r9-{i}"), release, None);
        let core = produced(&tree);
        assert_eq!(core.files.len(), 2 + 2 + members, "case {i}");
        let catalog = (!catalog_signers.is_empty()).then_some("catalog.sig.json");
        assert_retained(&core, &tree, catalog, component_signers.len());
    }
    // An unadmitted catalog is not opened: removing it changes nothing
    // InitialCore reads.
    let tree = Tree::new(
        "r9-unopened",
        &Spec {
            catalog_signers: &[],
            component_signers: &[],
            ..spec()
        },
        None,
    );
    fs::remove_file(tree.core.join("trust/bootstrap/catalog.json")).unwrap();
    assert!(produced(&tree).bootstrap_documents().catalog().is_none());
}

#[test]
fn which_keys_signed_a_catalog_or_component_envelope_are_not_judged() {
    // Pairing is by stored digest only (item 9); X4B judges signatures,
    // quorums and roles. Each header names its routed role, signed here by
    // the other role's keys.
    let tree = Tree::new(
        "r9-roles",
        &Spec {
            catalog_signers: &[("TR-INDEX", &[14, 15])],
            component_signers: &[Some(("TR-COMPONENT", &[11, 12]))],
            ..spec()
        },
        None,
    );
    assert_retained(&produced(&tree), &tree, Some("catalog.sig.json"), 1);
    // A header whose role is not its kind's route is a malformed carrier,
    // which the existing manifest index refuses for every listed envelope.
    let tree = Tree::new(
        "r9-route",
        &Spec {
            catalog_signers: &[COMPONENT_SIGNER],
            ..spec()
        },
        None,
    );
    let refusal = refused(&tree, &tree.release(STANDARD.0, STANDARD.1), 1);
    assert!(
        matches!(
            refusal,
            R::Release(ReleaseError::Authentication(AuthenticationError::Core(
                BindingError::Budget(M::Error::Route)
            )))
        ),
        "{refusal:?}"
    );
}

#[test]
fn the_listed_envelopes_pair_one_to_one_with_the_r9_body_set() {
    let refuses = |tag: &str, spec: Spec<'_>| {
        let tree = Tree::new(tag, &spec, None);
        let refusal = refused(&tree, &tree.release(STANDARD.0, STANDARD.1), 1);
        assert!(
            matches!(refusal, R::BootstrapEnvelopeSet),
            "{tag}: {refusal:?}"
        );
    };
    // A second envelope over the index-0 root body.
    refuses(
        "envelopes",
        Spec {
            extra_envelope: true,
            ..spec()
        },
    );
    // A second catalog envelope.
    refuses(
        "envelopes-catalog",
        Spec {
            catalog_signers: &[INDEX_SIGNER, ("TR-INDEX", &[12, 13])],
            ..spec()
        },
    );
    // A component manifest without its envelope, alone or beside a paired one.
    refuses(
        "envelopes-component",
        Spec {
            component_signers: &[None],
            ..spec()
        },
    );
    refuses(
        "envelopes-component-2",
        Spec {
            component_signers: &[Some(COMPONENT_SIGNER), None],
            ..spec()
        },
    );
    // A retained body or envelope that is not the listed bytes.
    for name in [
        "component-0.json",
        "component-0.sig.json",
        "catalog.json",
        "catalog.sig.json",
    ] {
        let tree = Tree::new("envelopes-bytes", &spec(), None);
        let path = tree.core.join("trust/bootstrap").join(name);
        let mut raw = fs::read(&path).unwrap();
        raw.push(b'\n');
        fs::write(&path, raw).unwrap();
        let refusal = refused(&tree, &tree.release(STANDARD.0, STANDARD.1), 1);
        assert!(
            matches!(refusal, R::BootstrapEnvelopeSet),
            "{name}: {refusal:?}"
        );
    }
}

#[test]
fn the_r9_members_stay_within_the_member_bound() {
    // Two roots, the revocation, 62 component manifests and their 65
    // envelopes are 130 members; one more component manifest refuses.
    for (count, admitted) in [(62, true), (63, false)] {
        let signers = vec![Some(COMPONENT_SIGNER); count];
        let tree = Tree::new(
            "r9-bound",
            &Spec {
                catalog_signers: &[],
                component_signers: &signers,
                ..spec()
            },
            None,
        );
        let release = tree.release(STANDARD.0, STANDARD.1);
        let (core, _attempt) = produce(&release, &tree.exe(), 1);
        match core {
            Ok(core) => {
                assert!(admitted);
                assert_eq!(core.files.len(), 2 + 2 + MAX_MEMBERS);
                assert_eq!(core.bootstrap_documents().manifests().len(), count);
            }
            Err(WorkFailure::Operation(R::BootstrapLocator)) => assert!(!admitted),
            Err(other) => panic!("{count}: {other:?}"),
        }
    }
}

#[test]
fn the_recheck_reaches_the_r9_members() {
    for name in ["component-0.sig.json", "catalog.json"] {
        let tree = Tree::new("r9-recheck", &spec(), None);
        let release = tree.release(STANDARD.0, STANDARD.1);
        let (core, mut attempt) = produce(&release, &tree.exe(), 1);
        let core = core.unwrap();
        let path = tree.core.join("trust/bootstrap").join(name);
        fs::set_permissions(&path, fs::Permissions::from_mode(0o664)).unwrap();
        assert!(matches!(
            core.recheck(&mut attempt),
            Err(WorkFailure::Operation(R::Custody(
                CoreMember::Member,
                Refusal::GroupWrite
            )))
        ));
    }
    // An r9 member is judged by the core-tree custody predicate when opened.
    let tree = Tree::new("r9-acl", &spec(), Some("trust/bootstrap/component-0.json"));
    let refusal = refused(&tree, &tree.release(STANDARD.0, STANDARD.1), 1);
    assert!(
        matches!(
            refusal,
            R::Custody(CoreMember::Member, Refusal::AclUnreadable)
        ),
        "{refusal:?}"
    );
}

#[test]
fn the_entrypoint_bytes_and_bootstrap_path_join_the_release() {
    let tree = Tree::new("bytes", &spec(), None);
    fs::write(tree.exe(), b"TEST-ONLY-A-DIFFERENT-IMAGE").unwrap();
    let release = tree.release(STANDARD.0, STANDARD.1);
    assert!(matches!(refused(&tree, &release, 1), R::EntrypointBytes));
    // The directory the inventory names is not the embedded one.
    let tree = Tree::new("bootstrap", &spec(), None);
    fs::rename(
        tree.core.join("trust/bootstrap"),
        tree.core.join("trust/boot"),
    )
    .unwrap();
    let release = tree.release(STANDARD.0, "trust/boot");
    assert!(matches!(refused(&tree, &release, 1), R::BootstrapPath));
    // And an embedded path with no directory refuses as absent.
    let release = tree.release(STANDARD.0, "trust/bootstrap");
    assert!(matches!(
        refused(&tree, &release, 1),
        R::Absent(CoreMember::Bootstrap)
    ));
}

#[test]
fn the_embedded_root_flags_and_revocation_bind_the_release() {
    let tree = Tree::new("root", &spec(), None);
    let wrong = EmbeddedCoreRelease::new(
        Some(EmbeddedRootBinding::new(1, 1, &"0".repeat(64))),
        Some(STANDARD.0),
        Some(STANDARD.1),
    );
    assert!(matches!(
        refused(&tree, &wrong, 1),
        R::Release(ReleaseError::Authentication(AuthenticationError::Core(
            BindingError::Binding("root-binding")
        )))
    ));
    let flags = ["CS_HARD", "CS_VALID"];
    let tree = Tree::new(
        "flags",
        &Spec {
            flags: &flags,
            ..spec()
        },
        None,
    );
    let release = tree.release(STANDARD.0, STANDARD.1);
    assert!(matches!(refused(&tree, &release, 0x1), R::CodeSigningFlags));
    assert!(matches!(
        refused(&tree, &release, 0x100),
        R::CodeSigningFlags
    ));
    assert!(produce(&release, &tree.exe(), 0x101).0.is_ok());
    let tree = Tree::new(
        "revoked",
        &Spec {
            revoke: &[8, 9],
            ..spec()
        },
        None,
    );
    let release = tree.release(STANDARD.0, STANDARD.1);
    assert!(matches!(
        refused(&tree, &release, 1),
        R::Release(ReleaseError::Quorum(EnvelopeKind::Inventory))
    ));
}

#[test]
fn a_mutation_after_admission_makes_the_recheck_refuse() {
    let tree = Tree::new("mutation", &spec(), None);
    let release = tree.release(STANDARD.0, STANDARD.1);
    let (core, mut attempt) = produce(&release, &tree.exe(), 1);
    let core = core.unwrap();
    let payload = tree.core.join("trust/bootstrap/payload.json");
    fs::set_permissions(&payload, fs::Permissions::from_mode(0o664)).unwrap();
    assert!(matches!(
        core.recheck(&mut attempt),
        Err(WorkFailure::Operation(R::Custody(
            CoreMember::Payload,
            Refusal::GroupWrite
        )))
    ));
    assert!(attempt.is_latched());
    fs::set_permissions(&payload, fs::Permissions::from_mode(0o644)).unwrap();
    // The same bytes rewritten in place change the file's status.
    let envelope = tree.core.join("trust/bootstrap/revocation.sig.json");
    let raw = fs::read(&envelope).unwrap();
    let (core, mut attempt) = produce(&release, &tree.exe(), 1);
    let core = core.unwrap();
    std::thread::sleep(std::time::Duration::from_millis(10));
    fs::write(&envelope, &raw).unwrap();
    assert!(matches!(
        core.recheck(&mut attempt),
        Err(WorkFailure::Operation(R::Changed(CoreMember::Member)))
    ));
    // A replaced file changes its directory, which the recheck reaches first.
    let (core, mut attempt) = produce(&release, &tree.exe(), 1);
    let core = core.unwrap();
    fs::remove_file(&envelope).unwrap();
    fs::write(&envelope, &raw).unwrap();
    assert!(matches!(
        core.recheck(&mut attempt),
        Err(WorkFailure::Operation(R::Changed(CoreMember::Bootstrap)))
    ));
}

#[test]
fn only_a_release_entry_naming_this_closure_refuses() {
    let closure = format!("closure2:{}", "ab".repeat(32));
    let entry = |kind: &str, subject: &str| {
        opensip_identity::parse_json(
            format!(
                r#"{{"reason":"defect","revokedAt":"2026-10-01T00:00:00Z","subject":"{subject}","subjectKind":"{kind}"}}"#
            )
            .as_bytes(),
        )
        .unwrap()
    };
    assert!(refuse_revoked_release(&[], &closure).is_ok());
    let others = [
        entry("release", &format!("closure2:{}", "cd".repeat(32))),
        entry("keyId", &closure),
        entry("namespace", &closure),
        entry("catalogSnapshot", &closure),
    ];
    assert!(refuse_revoked_release(&others, &closure).is_ok());
    let mut named = others.to_vec();
    named.push(entry("release", &closure));
    assert!(matches!(
        refuse_revoked_release(&named, &closure),
        Err(R::ReleaseRevoked)
    ));
}
