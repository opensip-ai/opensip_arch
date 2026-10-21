// Unit CI-2's controls (component installation plan r3, section 4): CI-T3,
// CI-T4, CI-T6 to CI-T8, CI-T13, CI-T14, CI-T18, CI-T19, CI-T22 (B_install),
// CI-T23 to CI-T26, CI-PT-2, CI-PT-3 and CI-PT-7. The fixture evidence is
// C2a-1's `TestComponent`: a body that passed the real body validation, with
// the test's own release row (LD-CI2-2). Every ledger is an explicitly
// identified test scope, never evidence for a production profile.
use super::*;
use opensip_identity::{
    JsonInteger, RegisteredSchemas, canonical_bytes, digest_hex, parse_json, raw_sha256,
};
use opensip_platform::WorkLedger;
use opensip_security::TestComponent;
use std::collections::BTreeMap;
use std::os::unix::fs::{MetadataExt, PermissionsExt};
use std::path::PathBuf;
use std::sync::OnceLock;

/// A stand-in for the verified envelope; C2a-2's signed fixtures carry real
/// ones.
pub(crate) const ENVELOPE: &[u8] = br#"{"test":"envelope stand-in"}"#;
pub(crate) const MACOS: SelectedPlatform<'static> = SelectedPlatform {
    os: "macos",
    arch: "arm64",
};

/// The registered schemas, read from the repository's sources once (as
/// C2a-1's controls read them).
pub(crate) fn registry() -> &'static RegisteredSchemas {
    static REGISTRY: OnceLock<RegisteredSchemas> = OnceLock::new();
    REGISTRY.get_or_init(|| {
        let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("../..");
        let raw: Vec<Vec<u8>> = RegisteredSchemas::source_requirements()
            .iter()
            .map(|p| std::fs::read(root.join(p.source_path())).unwrap())
            .collect();
        let refs: Vec<&[u8]> = raw.iter().map(Vec::as_slice).collect();
        RegisteredSchemas::from_sources(&refs).unwrap()
    })
}

/// One tree entry of a fixture.
#[derive(Clone, Debug)]
pub(crate) struct Spec {
    pub(crate) path: String,
    pub(crate) mode: u32,
    pub(crate) kind: SpecKind,
}
#[derive(Clone, Debug)]
pub(crate) enum SpecKind {
    File(Vec<u8>),
    Dir,
    Link(String),
}
pub(crate) fn file(path: &str, mode: u32, bytes: &[u8]) -> Spec {
    Spec {
        path: path.to_owned(),
        mode,
        kind: SpecKind::File(bytes.to_vec()),
    }
}
pub(crate) fn dir(path: &str, mode: u32) -> Spec {
    Spec {
        path: path.to_owned(),
        mode,
        kind: SpecKind::Dir,
    }
}
pub(crate) fn link(path: &str, target: &str) -> Spec {
    Spec {
        path: path.to_owned(),
        mode: 0o777,
        kind: SpecKind::Link(target.to_owned()),
    }
}
fn payload(n: usize, seed: u8) -> Vec<u8> {
    (0..n)
        .map(|i| (i as u8).wrapping_mul(31).wrapping_add(seed))
        .collect()
}
/// A nested tree with every kind, mixed depths and sibling branches.
pub(crate) fn nested() -> Vec<Spec> {
    vec![
        dir("bin", 0o755),
        file("bin/entry", 0o755, b"#!/bin/sh\nexit 0\n"),
        dir("a", 0o755),
        file("a-x", 0o644, &payload(70_000, 3)),
        dir("a/b", 0o700),
        dir("a/b/c", 0o755),
        file("a/b/c/deep.txt", 0o444, &payload(131_073, 9)),
        file("a/b/empty", 0o644, b""),
        file("a/z", 0o600, &payload(65_536, 1)),
        link("latest", "bin/entry"),
        dir("lib", 0o755),
        link("lib/up", "provider.js"),
        file("lib/provider.js", 0o644, b"// provider\n"),
    ]
}
/// A file-only tree (`D = 0`, `S = 0`).
pub(crate) fn file_only() -> Vec<Spec> {
    vec![
        file("entry", 0o755, b"#!/bin/sh\n"),
        file("data.bin", 0o644, &payload(200_000, 7)),
        file("z", 0o600, b"z"),
    ]
}

/// The removal of a test's scratch directory. Installed files carry no
/// write bit, so their directories are made writable first.
pub(crate) struct Scratch(pub(crate) PathBuf);
impl Drop for Scratch {
    fn drop(&mut self) {
        make_writable(&self.0);
        let removed = std::fs::remove_dir_all(&self.0);
        if !std::thread::panicking() {
            removed.unwrap();
        }
    }
}
pub(crate) fn make_writable(path: &std::path::Path) {
    if let Ok(meta) = std::fs::symlink_metadata(path)
        && meta.is_dir()
    {
        std::fs::set_permissions(path, std::fs::Permissions::from_mode(0o700)).unwrap();
        for entry in std::fs::read_dir(path).unwrap() {
            make_writable(&entry.unwrap().path());
        }
    }
}
fn scratch_dir() -> Scratch {
    let mut bytes = [0u8; 8];
    getrandom_fill(&mut bytes);
    let hex: String = bytes.iter().map(|b| format!("{b:02x}")).collect();
    let dir = std::env::temp_dir().join(format!("opensip-ci2-{hex}"));
    std::fs::create_dir(&dir).unwrap();
    std::fs::set_permissions(&dir, std::fs::Permissions::from_mode(0o700)).unwrap();
    Scratch(dir)
}
fn getrandom_fill(bytes: &mut [u8]) {
    let id = opensip_platform::request_entropy().unwrap();
    for (b, s) in bytes.iter_mut().zip(id.iter().cycle()) {
        *b = *s;
    }
}

fn int(n: i128) -> V {
    V::Integer(JsonInteger::new(n).unwrap())
}
fn obj(v: &mut V) -> &mut BTreeMap<String, V> {
    let V::Object(m) = v else { panic!("object") };
    m
}
fn sv(s: &str) -> V {
    V::String(s.to_owned())
}

/// The manifest body: CR-1's baseline (`manifest268-semantic.ndjson`,
/// `POS/full-security`) as a role-valid toolchain with C2PM-1's declaration,
/// and the selected `{macos, arm64}` row carrying `specs`.
pub(crate) fn body(specs: &[Spec]) -> V {
    body_with(specs, None)
}
/// `body`, with an optional second `{macos, x86_64}` row carrying `other`.
pub(crate) fn body_with(specs: &[Spec], other: Option<&[Spec]>) -> V {
    let line = include_bytes!("../../security/tests/fixtures/manifest268-semantic.ndjson")
        .split(|b| *b == b'\n')
        .find(|b| !b.is_empty())
        .unwrap();
    let q = parse_json(line).unwrap();
    let V::Object(q) = q else { panic!("object") };
    let V::String(hex) = &q["raw"] else {
        panic!("raw")
    };
    let raw: Vec<u8> = (0..hex.len())
        .step_by(2)
        .map(|i| u8::from_str_radix(&hex[i..i + 2], 16).unwrap())
        .collect();
    let mut v = parse_json(&raw).unwrap();
    let m = obj(&mut v);
    m.insert("role".to_owned(), sv("toolchain"));
    m.remove("commands");
    m.insert("capabilities".to_owned(), V::Array(vec![]));
    m.insert("permissions".to_owned(), V::Array(vec![]));
    m.insert("closureProtocolMajor".to_owned(), int(1));
    let entries_of = |specs: &[Spec]| -> Vec<V> {
        specs
            .iter()
            .map(|s| {
                let mut e = BTreeMap::new();
                e.insert("path".to_owned(), sv(&s.path));
                e.insert("mode".to_owned(), sv(&format!("{:04o}", s.mode)));
                match &s.kind {
                    SpecKind::File(bytes) => {
                        e.insert("type".to_owned(), sv("file"));
                        e.insert("length".to_owned(), int(bytes.len() as i128));
                        e.insert("sha256".to_owned(), sv(&digest_hex(&raw_sha256(bytes))));
                    }
                    SpecKind::Dir => {
                        e.insert("type".to_owned(), sv("dir"));
                    }
                    SpecKind::Link(target) => {
                        e.insert("type".to_owned(), sv("symlink"));
                        e.insert("target".to_owned(), sv(target));
                    }
                }
                V::Object(e)
            })
            .collect()
    };
    let entries = entries_of(specs);
    let entry = specs
        .iter()
        .find(|s| matches!(s.kind, SpecKind::File(_)))
        .map(|s| s.path.clone())
        .unwrap();
    let V::Array(platforms) = m.get_mut("platforms").unwrap() else {
        panic!("platforms")
    };
    platforms.truncate(1);
    let p = obj(&mut platforms[0]);
    p.insert("os".to_owned(), sv("macos"));
    p.insert("arch".to_owned(), sv("arm64"));
    p.insert("entrypoint".to_owned(), sv(&entry));
    let mut tree = BTreeMap::new();
    tree.insert("entries".to_owned(), V::Array(entries));
    p.insert("tree".to_owned(), V::Object(tree));
    if let Some(other) = other {
        let mut second = platforms[0].clone();
        let q = obj(&mut second);
        q.insert("arch".to_owned(), sv("x86_64"));
        let first = other
            .iter()
            .find(|s| matches!(s.kind, SpecKind::File(_)))
            .unwrap();
        q.insert("entrypoint".to_owned(), sv(&first.path));
        let mut tree = BTreeMap::new();
        tree.insert("entries".to_owned(), V::Array(entries_of(other)));
        q.insert("tree".to_owned(), V::Object(tree));
        platforms.push(second);
    }
    v
}

/// The profile-1 archive of `specs` (CI-1's fixture-only emitter).
pub(crate) fn archive(specs: &[Spec]) -> Option<Vec<u8>> {
    let digests: Vec<[u8; 32]> = specs
        .iter()
        .map(|s| match &s.kind {
            SpecKind::File(b) => raw_sha256(b),
            _ => [0; 32],
        })
        .collect();
    let rows: Vec<TreeRow<'_>> = specs
        .iter()
        .zip(&digests)
        .map(|(s, d)| TreeRow {
            path: &s.path,
            mode: s.mode,
            kind: match &s.kind {
                SpecKind::File(b) => RowKind::File {
                    length: b.len() as u64,
                    sha256: *d,
                },
                SpecKind::Dir => RowKind::Dir,
                SpecKind::Link(t) => RowKind::Symlink { target: t },
            },
        })
        .collect();
    let payloads: Vec<(&str, &[u8])> = specs
        .iter()
        .filter_map(|s| match &s.kind {
            SpecKind::File(b) => Some((s.path.as_str(), b.as_slice())),
            _ => None,
        })
        .collect();
    ap::emit(&rows, &payloads).ok()
}

/// A catalog release row of the recovery catalog's shape, with one
/// profile-1 artifact for `macos-arm64`, bound to the body and archive.
pub(crate) fn release(raw: &[u8], archive: &[u8]) -> V {
    let z = "0".repeat(64);
    let a = digest_hex(&raw_sha256(archive));
    parse_json(
        format!(
            r#"{{"artifacts":[{{"archiveDigest":"{a}","archiveProfileId":"{p}","platform":"macos-arm64","sha256":"{a}"}}],"envelopeDigest":"{e}","hostCoreConstraint":{{"includeMax":false,"includeMin":true,"max":"0.2.0","min":"0.1.0"}},"manifestDigest":"{m}","manifestPreimageSha256":"{z}","publisher":"opensip","sourceClass":"first-party","stableId":"6f1c2c3e-0b6a-4a1c-9c2d-1f0e2a3b4c5d","version":"1.0.0"}}"#,
            p = ap::PROFILE_ID,
            e = digest_hex(&raw_sha256(ENVELOPE)),
            m = digest_hex(&raw_sha256(raw)),
        )
        .as_bytes(),
    )
    .unwrap()
}

/// One installable release: its store, its archive on disk, and its
/// evidence.
pub(crate) struct Fixture {
    pub(crate) store_path: PathBuf,
    pub(crate) store: ComponentStore,
    pub(crate) archive_path: PathBuf,
    pub(crate) archive: Vec<u8>,
    pub(crate) component: TestComponent,
    pub(crate) specs: Vec<Spec>,
    _scratch: Scratch,
}
impl Fixture {
    pub(crate) fn new(specs: Vec<Spec>) -> Self {
        Self::with(specs, |_| {})
    }
    /// A release with a second platform row, `{macos, x86_64}`, carrying
    /// `other`, and an artifact for its token.
    pub(crate) fn two_platforms(specs: Vec<Spec>, other: Vec<Spec>) -> Self {
        let mut f = Self::with(specs.clone(), |_| {});
        let raw = canonical_bytes(&body_with(&specs, Some(&other))).unwrap();
        let mut release = release(&raw, &f.archive);
        let V::Array(a) = obj(&mut release).get_mut("artifacts").unwrap() else {
            panic!()
        };
        let mut x86 = a[0].clone();
        obj(&mut x86).insert("platform".to_owned(), sv("macos-x86_64"));
        a.push(x86);
        f.component = TestComponent::new(raw, ENVELOPE.to_vec(), release).expect("a valid body");
        f
    }
    /// C2a-1's candidate of this release for `platform`.
    pub(crate) fn candidate_for(&self, platform: SelectedPlatform<'_>) -> ClosureCandidate<'_> {
        let mut ledger = WorkLedger::snapshot_profile();
        ledger
            .scope(|work| {
                opensip_security::component_candidate(
                    &self.component.authenticated(),
                    platform,
                    None,
                    registry(),
                    work,
                )
            })
            .unwrap()
    }
    /// `edit` may change the release row (CI-T3).
    pub(crate) fn with(specs: Vec<Spec>, edit: impl FnOnce(&mut V)) -> Self {
        let scratch = scratch_dir();
        let store_path = scratch.0.join("components");
        std::fs::create_dir(&store_path).unwrap();
        std::fs::set_permissions(&store_path, std::fs::Permissions::from_mode(0o700)).unwrap();
        let uid = std::fs::metadata(&store_path).unwrap().uid();
        let directory =
            RetainedDirectory::from_retained_handle(File::open(&store_path).unwrap()).unwrap();
        // Provisioning's private store carries the zero-rights owner allow
        // the custody rule requires.
        let mut ledger = WorkLedger::new();
        within(&mut ledger, |work| {
            opensip_platform::append_owner_zero_allow_accounted(directory.as_file(), work)
        })
        .unwrap();
        let store = within(&mut ledger, |work| {
            ComponentStore::fixture(directory, &store_path, uid, work)
        })
        .unwrap();
        // A tree beyond a profile capacity has no archive (CI-T5).
        let archive = archive(&specs).unwrap_or_default();
        let archive_path = scratch.0.join("release.tar");
        std::fs::write(&archive_path, &archive).unwrap();
        let raw = canonical_bytes(&body(&specs)).unwrap();
        let mut release = release(&raw, &archive);
        edit(&mut release);
        let component = TestComponent::new(raw, ENVELOPE.to_vec(), release).expect("a valid body");
        Self {
            store_path,
            store,
            archive_path,
            archive,
            component,
            specs,
            _scratch: scratch,
        }
    }
    pub(crate) fn candidate(&self) -> ClosureCandidate<'_> {
        let mut ledger = WorkLedger::snapshot_profile();
        ledger
            .scope(|work| {
                opensip_security::component_candidate(
                    &self.component.authenticated(),
                    MACOS,
                    None,
                    registry(),
                    work,
                )
            })
            .unwrap()
    }
    pub(crate) fn name(&self) -> String {
        self.candidate()
            .closure()
            .strip_prefix("closure2:")
            .unwrap()
            .to_owned()
    }
    pub(crate) fn generation(&self) -> PathBuf {
        self.store_path.join(self.name())
    }
    pub(crate) fn install_on(&self, ledger: &mut WorkLedger) -> Result<Installed, InstallFailure> {
        let candidate = self.candidate();
        within(ledger, |work| {
            install(
                &self.store,
                &self.component.authenticated(),
                &candidate,
                MACOS,
                &self.archive_path,
                work,
            )
        })
    }
    pub(crate) fn install(&self) -> Result<Installed, InstallFailure> {
        self.install_on(&mut WorkLedger::snapshot_profile())
    }
    /// The transaction run directly on `ledger`, with no reservation, so its
    /// actual charges show in `used()` (CI-T22).
    pub(crate) fn transaction_on(&self, ledger: &mut WorkLedger) -> Result<Installed, Failure> {
        let candidate = self.candidate();
        let component = self.component.authenticated();
        let evidence = evidence(&component, &candidate, MACOS).unwrap();
        let length = archive_length(&evidence.tree).unwrap();
        ledger.scope(|work| {
            transaction(
                &self.store,
                &evidence,
                &candidate,
                &self.archive_path,
                length,
                work,
            )
        })
    }
    pub(crate) fn evidence_bounds(&self) -> (WorkCost, WorkCost) {
        let candidate = self.candidate();
        let component = self.component.authenticated();
        let evidence = evidence(&component, &candidate, MACOS).unwrap();
        let length = archive_length(&evidence.tree).unwrap();
        let record = evidence.record.length();
        (
            install_bound(
                &evidence.tree,
                length,
                record,
                self.archive_path.as_os_str().len(),
            )
            .unwrap(),
            reinstall_bound(&evidence.tree, record).unwrap(),
        )
    }
    /// The store's entries, other than the archive's scratch siblings.
    pub(crate) fn store_entries(&self) -> Vec<String> {
        let mut names: Vec<String> = std::fs::read_dir(&self.store_path)
            .unwrap()
            .map(|e| e.unwrap().file_name().into_string().unwrap())
            .collect();
        names.sort();
        names
    }
    pub(crate) fn stages(&self) -> Vec<String> {
        self.store_entries()
            .into_iter()
            .filter(|n| n.starts_with(".opensip-stage-install-"))
            .collect()
    }
}

/// Run `body` in a scope of `ledger` and return its own result, even when it
/// latched the ledger (the scope then reports `Closed`).
pub(crate) fn within<T>(ledger: &mut WorkLedger, body: impl FnOnce(&mut WorkScope<'_>) -> T) -> T {
    let mut out = None;
    drop(ledger.scope::<_, ()>(|work| {
        out = Some(body(work));
        Ok(())
    }));
    out.unwrap()
}

/// Run `body` with the transaction's seam hook set to `hook`.
pub(crate) fn with_seam<T>(
    hook: impl FnMut(&'static str) -> io::Result<()> + 'static,
    body: impl FnOnce() -> T,
) -> T {
    seams::HOOK.with(|h| *h.borrow_mut() = Some(Box::new(hook)));
    let out = body();
    seams::HOOK.with(|h| *h.borrow_mut() = None);
    out
}
fn fail_at(step: &'static str) -> impl FnMut(&'static str) -> io::Result<()> {
    move |s| {
        if s == step {
            Err(io::Error::other(format!("injected at {s}")))
        } else {
            Ok(())
        }
    }
}

fn mode_of(path: &std::path::Path) -> u32 {
    std::fs::symlink_metadata(path).unwrap().mode() & 0o7777
}

// ---- A normal installation (CI-T18, CI-T23, CI-T24) ----

#[test]
fn ci_t24_a_nested_tree_installs_verifies_and_publishes() {
    let f = Fixture::new(nested());
    assert_eq!(f.install().unwrap(), Installed::Published);
    let g = f.generation();
    assert_eq!(
        f.store_entries(),
        vec![f.name()],
        "no stage is left after a publication"
    );
    for s in &f.specs {
        let p = g.join("tree").join(&s.path);
        match &s.kind {
            SpecKind::File(bytes) => assert_eq!(&std::fs::read(&p).unwrap(), bytes, "{}", s.path),
            SpecKind::Dir => assert!(std::fs::symlink_metadata(&p).unwrap().is_dir()),
            SpecKind::Link(t) => assert_eq!(std::fs::read_link(&p).unwrap().to_str().unwrap(), t),
        }
    }
    assert_eq!(mode_of(&g), 0o700);
    assert_eq!(mode_of(&g.join("tree")), 0o500);
    assert_eq!(mode_of(&g.join(RECORD)), 0o400);
    assert_eq!(mode_of(&g.join(PIN)), 0o600);
    assert_eq!(std::fs::metadata(g.join(PIN)).unwrap().len(), 0);
}

#[test]
fn ci_t18_installed_modes_follow_ld_ci_10() {
    let specs = vec![
        file("w", 0o200, b"write-only signed"),
        dir("d", 0o600),
        file("d/x", 0o100, b"execute-only signed"),
        file("e", 0o750, b"exec"),
        link("l", "w"),
    ];
    let f = Fixture::new(specs);
    f.install().unwrap();
    let t = f.generation().join("tree");
    assert_eq!(mode_of(&t.join("w")), 0o400);
    assert_eq!(
        std::fs::read(t.join("w")).unwrap(),
        b"write-only signed",
        "0200 installs readable"
    );
    assert_eq!(mode_of(&t.join("d")), 0o500);
    assert_eq!(
        std::fs::read(t.join("d/x")).unwrap(),
        b"execute-only signed",
        "0600 dir is traversed"
    );
    assert_eq!(mode_of(&t.join("d/x")), 0o500);
    assert_eq!(mode_of(&t.join("e")), 0o500);
    assert_eq!(
        std::fs::read_link(t.join("l")).unwrap().to_str().unwrap(),
        "w"
    );
}

#[test]
fn ci_t18_staging_is_0700_and_finalized_bottom_up_branch_locally() {
    // At the "verified" seam (after V1, before step 4) the stage holds
    // staging modes; at "finalized" every final mode is set.
    let f = Fixture::new(nested());
    let store = f.store_path.clone();
    type Seen = std::rc::Rc<std::cell::RefCell<Vec<(&'static str, u32, u32)>>>;
    let seen: Seen = Default::default();
    let log = seen.clone();
    with_seam(
        move |step| {
            if step == "verified" || step == "finalized" {
                let stage = std::fs::read_dir(&store)
                    .unwrap()
                    .map(|e| e.unwrap().path())
                    .find(|p| {
                        p.file_name()
                            .unwrap()
                            .to_str()
                            .unwrap()
                            .starts_with(".opensip-stage-install-")
                    })
                    .unwrap();
                log.borrow_mut().push((
                    step,
                    mode_of(&stage.join("tree/a/b")),
                    mode_of(&stage.join("tree/a/z")),
                ));
            }
            Ok(())
        },
        || f.install().unwrap(),
    );
    assert_eq!(
        *seen.borrow(),
        vec![("verified", 0o700, 0o600), ("finalized", 0o500, 0o400)]
    );
}

#[test]
fn ci_t23_the_stage_is_a_store_sibling_and_never_a_generation() {
    let f = Fixture::new(nested());
    let r = with_seam(fail_at("prerequisites"), || f.install());
    assert!(matches!(
        r,
        Err(InstallFailure::Io(InstallIo::Call { call: "seam", .. }))
    ));
    let stages = f.stages();
    assert_eq!(stages.len(), 1, "the stage stays inert, in the store");
    assert_eq!(f.store_entries(), stages, "nothing was published");
    // The lookup and the open never return a stage.
    let candidate = f.candidate();
    let mut ledger = WorkLedger::snapshot_profile();
    let opened = within(&mut ledger, |work| {
        crate::retained_tree::open_retained_tree(
            &f.store,
            &f.component.authenticated(),
            &candidate,
            MACOS,
            PinRequest::UnderFence,
            work,
        )
        .map(|_| ())
    });
    assert!(matches!(opened, Err(TreeReadFailure::NotInstalled)));
}

// ---- Admission (CI-T3, CI-T4, CI-T6) ----

#[test]
fn ci_t3_digest_split_profile_and_archive_digest_refuse() {
    let set = |key: &'static str, value: &'static str| {
        move |r: &mut V| {
            let V::Array(a) = obj(r).get_mut("artifacts").unwrap() else {
                panic!()
            };
            obj(&mut a[0]).insert(key.to_owned(), sv(value));
        }
    };
    let other = "1".repeat(64);
    let leaked: &'static str = Box::leak(other.into_boxed_str());
    let f = Fixture::with(nested(), set("sha256", leaked));
    assert!(matches!(
        f.install(),
        Err(InstallFailure::Admission(
            AdmissionRefusal::ArtifactDigestSplit
        ))
    ));
    let f = Fixture::with(nested(), set("archiveProfileId", "synthetic"));
    assert!(matches!(
        f.install(),
        Err(InstallFailure::Admission(AdmissionRefusal::Profile))
    ));
    let f = Fixture::with(nested(), |r| {
        let V::Array(a) = obj(r).get_mut("artifacts").unwrap() else {
            panic!()
        };
        let m = obj(&mut a[0]);
        m.insert("sha256".to_owned(), sv(&"2".repeat(64)));
        m.insert("archiveDigest".to_owned(), sv(&"2".repeat(64)));
    });
    assert!(matches!(
        f.install(),
        Err(InstallFailure::Admission(AdmissionRefusal::ArchiveDigest))
    ));
    assert_eq!(
        f.store_entries().len(),
        1,
        "an archive-digest refusal leaves only the inert stage"
    );
    assert!(f.stages().len() == 1);
}

#[test]
fn ci_t4_a_platform_with_no_row_refuses_and_the_alias_is_only_a_lookup() {
    let f = Fixture::new(nested());
    let candidate = f.candidate();
    for platform in [
        SelectedPlatform {
            os: "freebsd",
            arch: "arm64",
        },
        SelectedPlatform {
            os: "macos",
            arch: "riscv",
        },
    ] {
        assert!(matches!(
            evidence(&f.component.authenticated(), &candidate, platform),
            Err(AdmissionRefusal::PlatformUnsupported)
        ));
    }
    let component = f.component.authenticated();
    let e = evidence(&component, &candidate, MACOS).unwrap();
    assert_eq!(e.record.platform, "macos-arm64");
    // The alias appears in the record's `platform` only: it is the
    // artifact's token, never a closure, profile or grant id.
    assert!(!e.record.closure_id.contains("macos"));
}

#[test]
fn ci_t6_archive_changed_and_read_attempts_refuse() {
    let f = Fixture::new(nested());
    let path = f.archive_path.clone();
    let r = with_seam(
        move |step| {
            if step == "streamed" {
                let file = std::fs::OpenOptions::new().write(true).open(&path).unwrap();
                file.set_modified(std::time::SystemTime::UNIX_EPOCH)
                    .unwrap();
            }
            Ok(())
        },
        || f.install(),
    );
    assert!(matches!(
        r,
        Err(InstallFailure::Admission(AdmissionRefusal::ArchiveChanged))
    ));
    // Short reads spend the envelope `2·⌈L/64 KiB⌉ + 2` before the end.
    let f = Fixture::new(nested());
    seams::READ_CAP.with(|c| *c.borrow_mut() = Some(4096));
    let r = f.install();
    seams::READ_CAP.with(|c| *c.borrow_mut() = None);
    assert!(
        matches!(
            r,
            Err(InstallFailure::Admission(
                AdmissionRefusal::ArchiveReadAttempts
            ))
        ),
        "{r:?}"
    );
}

#[test]
fn ci_t2_and_ci_t5_length_and_capacity_refuse_before_any_member() {
    // A wrong-length archive refuses before any stage exists.
    let f = Fixture::new(nested());
    let mut longer = f.archive.clone();
    longer.extend_from_slice(&[0; 512]);
    std::fs::write(&f.archive_path, &longer).unwrap();
    assert!(matches!(
        f.install(),
        Err(InstallFailure::Admission(AdmissionRefusal::Archive(
            ArchiveRefusal::Length { .. }
        )))
    ));
    assert!(f.store_entries().is_empty(), "nothing staged");
    // A 101-byte path refuses `archive-capacity` before any read.
    let long = format!("{}/{}", "d".repeat(50), "f".repeat(50));
    let f = Fixture::new(vec![dir(&"d".repeat(50), 0o755), file(&long, 0o644, b"x")]);
    std::fs::remove_file(&f.archive_path).unwrap();
    assert!(matches!(
        f.install(),
        Err(InstallFailure::Admission(AdmissionRefusal::Capacity(
            ap::Capacity::PathExceedsUstarName
        )))
    ));
}

// ---- Failure points and recovery (CI-T7, CI-T19, CI-T25, CI-T26) ----

#[test]
fn ci_t7_a_failure_at_every_step_publishes_nothing_and_cleans_nothing() {
    for step in [
        "staged",
        "streamed",
        "verified",
        "finalized",
        "prerequisites",
    ] {
        let f = Fixture::new(nested());
        let r = with_seam(fail_at(step), || f.install());
        assert!(matches!(r, Err(InstallFailure::Io(_))), "{step}: {r:?}");
        assert_eq!(
            f.stages().len(),
            1,
            "{step}: one inert stage, never cleaned up"
        );
        assert!(!f.generation().exists(), "{step}: nothing published");
    }
}

#[test]
fn ci_t19_crash_prefixes_restart_absent_or_verifying() {
    // Before the rename every prefix restarts absent; after it, the name is
    // present and verifies.
    for (step, present) in [
        ("verified", false),
        ("finalized", false),
        ("prerequisites", false),
        ("renamed", true),
    ] {
        let f = Fixture::new(nested());
        let r = with_seam(fail_at(step), || f.install());
        assert!(r.is_err(), "{step}");
        assert_eq!(f.generation().exists(), present, "{step}");
        let candidate = f.candidate();
        let mut ledger = WorkLedger::snapshot_profile();
        let opened = within(&mut ledger, |work| {
            crate::retained_tree::open_retained_tree(
                &f.store,
                &f.component.authenticated(),
                &candidate,
                MACOS,
                PinRequest::UnderFence,
                work,
            )
            .map(|_| ())
        });
        if present {
            opened.unwrap();
            // A later installation finds it and takes the no-op path.
            assert_eq!(f.install().unwrap(), Installed::AlreadyInstalled);
        } else {
            assert!(
                matches!(opened, Err(TreeReadFailure::NotInstalled)),
                "{step}"
            );
        }
    }
}

#[test]
fn ci_t25_a_lost_race_ends_the_act() {
    let f = Fixture::new(nested());
    let target = f.generation();
    let r = with_seam(
        move |step| {
            if step == "prerequisites" {
                std::fs::create_dir(&target).unwrap();
            }
            Ok(())
        },
        || f.install(),
    );
    assert!(
        matches!(
            r,
            Err(InstallFailure::Io(InstallIo::Publication(
                DirectoryRenameClass::LostRace
            )))
        ),
        "{r:?}"
    );
    assert_eq!(f.stages().len(), 1, "the stage stays inert");
    assert_eq!(
        std::fs::read_dir(f.generation()).unwrap().count(),
        0,
        "the winner is not verified or touched"
    );
}

#[test]
fn ci_t26_the_suffix_is_reserved_exactly_and_a_shortfall_refuses_before_the_rename() {
    // The reservation's arguments, as a source pin.
    let source = include_str!("installation.rs");
    assert_eq!(
        source
            .matches("let postchecks = exclusive_publication_cost()\n        .checked_add(directory_barrier_cost())")
            .count(),
        1
    );
    assert_eq!(
        source
            .matches("work.effect(WorkCost::default(), postchecks,")
            .count(),
        1
    );
    // Run the bare transaction on a ledger funded to just before the
    // suffix: the reservation refuses, by law 468's route, and nothing is
    // published.
    let f = Fixture::new(file_only());
    let mut full = WorkLedger::snapshot_profile();
    f.transaction_on(&mut full).unwrap();
    let used = full.used();
    let suffix = exclusive_publication_cost()
        .checked_add(directory_barrier_cost())
        .unwrap();
    let g = Fixture::new(file_only());
    let mut short = WorkLedger::with_limits(WorkCost {
        objects: used.objects,
        edges: used.edges - 1,
        bytes: used.bytes,
    })
    .unwrap();
    let r = g.transaction_on(&mut short);
    assert!(matches!(r, Err(WorkFailure::Budget(_))), "{r:?}");
    assert!(!g.generation().exists(), "nothing published");
    assert_eq!(g.stages().len(), 1, "no cleanup after a latched failure");
    assert!(short.is_failed());
    assert!(suffix.edges > 0);
}

// ---- Re-install (CI-T8) ----

#[test]
fn ci_t8_reinstall_of_a_verifying_generation_is_a_no_op_and_of_a_corrupt_one_refuses() {
    let f = Fixture::new(nested());
    f.install().unwrap();
    let before = std::fs::read(f.generation().join("tree/a-x")).unwrap();
    assert_eq!(f.install().unwrap(), Installed::AlreadyInstalled);
    assert!(f.stages().is_empty(), "nothing staged");
    // Corrupt one byte: re-install refuses as corrupt and replaces nothing.
    let p = f.generation().join("tree/a-x");
    std::fs::set_permissions(&p, std::fs::Permissions::from_mode(0o600)).unwrap();
    let mut bytes = before.clone();
    bytes[0] ^= 1;
    std::fs::write(&p, &bytes).unwrap();
    std::fs::set_permissions(&p, std::fs::Permissions::from_mode(0o400)).unwrap();
    assert!(matches!(
        f.install(),
        Err(InstallFailure::Corrupt(TreeReadFailure::Digest { .. }))
    ));
    assert_eq!(std::fs::read(&p).unwrap(), bytes, "nothing rewrites it");
    assert!(f.stages().is_empty());
}

// ---- Custody (CI-T14) ----

#[test]
fn ci_t14_a_foreign_acl_on_the_store_refuses_custody() {
    let f = Fixture::new(nested());
    let status = std::process::Command::new("/bin/chmod")
        .args(["+a", "everyone allow list"])
        .arg(&f.store_path)
        .status()
        .unwrap();
    assert!(status.success());
    assert!(matches!(
        f.install(),
        Err(InstallFailure::Io(InstallIo::Custody(_)))
    ));
    assert!(f.store_entries().is_empty(), "nothing staged");
}

// ---- Work (CI-T22's B_install half; CI-PT-7) ----

/// An independent enumeration of `B_install`'s exact rows for a fixture:
/// every object and byte, and every edge but the two variable classes
/// (comparisons and read attempts), which are bounded separately.
fn exact_rows(f: &Fixture) -> (WorkCost, usize) {
    let st = opensip_platform::component_tree::status_read_cost();
    let fopen = opensip_platform::component_tree::open_regular_no_follow_cost();
    let one = NATIVE_CALL;
    let mut total = WorkCost::default();
    let mut add = |c: WorkCost, k: usize| total = total.checked_add(times(c, k).unwrap()).unwrap();
    let n = f.specs.len();
    let d = f
        .specs
        .iter()
        .filter(|s| matches!(s.kind, SpecKind::Dir))
        .count();
    let candidate = f.candidate();
    let component = f.component.authenticated();
    let e = evidence(&component, &candidate, MACOS).unwrap();
    let r = e.record.length();
    // Step 1.
    add(owned_record(65), 1);
    add(st, 1);
    add(descriptor_acl_capture_cost(), 1);
    add(owned_record(f.archive_path.as_os_str().len()), 1);
    add(fopen, 1);
    add(st, 2);
    // Step 2.
    add(private_directory_stage_cost(), 1);
    add(opensip_platform::append_owner_zero_allow_cost(), 1);
    add(descriptor_acl_capture_cost(), 1);
    add(create_exclusive_directory_cost("tree"), 1);
    add(buffer_cost(), 1);
    add(index_buffer_cost(n).unwrap(), 4);
    add(
        one,
        f.specs
            .iter()
            .filter(|s| matches!(s.kind, SpecKind::File(_)))
            .count(),
    );
    let mut variable = 0usize;
    for s in &f.specs {
        let comps: Vec<&str> = s.path.split('/').collect();
        for seg in &comps[..comps.len() - 1] {
            add(descend_cost(seg.len()), 1);
        }
        let name = comps[comps.len() - 1];
        match &s.kind {
            SpecKind::File(b) => {
                add(create_exclusive_regular_cost(name), 1);
                add(one, b.len().div_ceil(65_536));
                add(fopen, 2);
                add(one, 2);
                variable += envelope(b.len() as u64) as usize;
            }
            SpecKind::Dir => {
                add(create_exclusive_directory_cost(name), 1);
                add(descend_cost(name.len()), 3);
                add(one, 1);
                add(directory_barrier_cost(), 1);
            }
            SpecKind::Link(t) => {
                add(one, 1);
                add(owned_record(t.len()), 1);
                add(one, 2);
                add(owned_record(101), 2);
            }
        }
    }
    let listing = n + 3 * (d + 1);
    add(descend_cost(4), 3);
    add(one, listing * 2);
    add(st, n * 2);
    add(st, 1);
    add(one, 1);
    add(directory_barrier_cost(), 1);
    add(create_exclusive_regular_cost("generation.json"), 1);
    add(owned_record(r), 1);
    add(one, r.div_ceil(65_536) + 2);
    add(create_exclusive_regular_cost("pin.lock"), 1);
    add(one, 1);
    add(directory_barrier_cost(), 1);
    add(fopen, 2);
    add(exclusive_publication_cost(), 1);
    add(directory_barrier_cost(), 1);
    variable += envelope(f.archive.len() as u64) as usize + envelope(r as u64) as usize;
    variable += 2 * sort_comparisons(n).unwrap();
    (total, variable)
}

#[test]
fn ci_t22_actual_charges_are_within_b_install_for_each_tree_shape() {
    let metadata_heavy = vec![
        dir("x", 0o755),
        dir("x/y", 0o755),
        dir("x/y/z", 0o755),
        dir("x/y/z/w", 0o755),
        file("x/y/z/w/e0", 0o644, b""),
        file("e1", 0o644, b""),
        file("e2", 0o755, b""),
        link("l1", "e1"),
        link("x/l2", "y/z/w/e0"),
        link("x/y/z/l3", "w/e0"),
    ];
    for specs in [file_only(), nested(), metadata_heavy] {
        let f = Fixture::new(specs);
        let (bound, reinstall) = f.evidence_bounds();
        let mut ledger = WorkLedger::snapshot_profile();
        seams::WRITES.with(|w| *w.borrow_mut() = 0);
        f.transaction_on(&mut ledger).unwrap();
        let actual = ledger.used();
        // Exactly one P-1 attempt per 64 KiB chunk: no write is retried.
        let r = {
            let candidate = f.candidate();
            let component = f.component.authenticated();
            evidence(&component, &candidate, MACOS)
                .unwrap()
                .record
                .length()
        };
        let chunks: usize = f
            .specs
            .iter()
            .map(|s| match &s.kind {
                SpecKind::File(b) => b.len().div_ceil(READ_CHUNK),
                _ => 0,
            })
            .sum::<usize>()
            + r.div_ceil(READ_CHUNK);
        assert_eq!(seams::WRITES.with(|w| *w.borrow()), chunks);
        assert!(
            actual.objects <= bound.objects
                && actual.edges <= bound.edges
                && actual.bytes <= bound.bytes
        );
        // The independent enumeration: objects and bytes exactly; edges
        // exactly but for comparisons and read attempts, within their bounds.
        let (fixed, variable) = exact_rows(&f);
        assert_eq!((actual.objects, actual.bytes), (fixed.objects, fixed.bytes));
        assert!(
            actual.edges >= fixed.edges && actual.edges <= fixed.edges + variable,
            "{actual:?} {fixed:?} {variable}"
        );
        assert_eq!(
            (bound.objects, bound.bytes),
            (fixed.objects, fixed.bytes),
            "B_install's fixed rows are exact"
        );
        assert_eq!(
            bound.edges,
            fixed.edges + variable,
            "B_install's variable rows are their worst cases"
        );
        // The re-install path runs within its own bound, which the reserved
        // admission bound covers.
        let mut ledger = WorkLedger::snapshot_profile();
        assert_eq!(
            f.transaction_on(&mut ledger).unwrap(),
            Installed::AlreadyInstalled
        );
        let used = ledger.used();
        assert!(
            used.objects <= reinstall.objects
                && used.edges <= reinstall.edges
                && used.bytes <= reinstall.bytes
        );
    }
}

#[test]
fn ci_t22_b_install_beyond_the_allowance_refuses_install_budget_before_acquisition() {
    let f = Fixture::new(nested());
    let (b, r) = f.evidence_bounds();
    let bound = WorkCost {
        objects: b.objects.max(r.objects),
        edges: b.edges.max(r.edges),
        bytes: b.bytes.max(r.bytes),
    };
    let mut ledger = WorkLedger::with_limits(WorkCost {
        objects: bound.objects,
        edges: bound.edges - 1,
        bytes: bound.bytes,
    })
    .unwrap();
    assert!(matches!(
        f.install_on(&mut ledger),
        Err(InstallFailure::Admission(AdmissionRefusal::InstallBudget))
    ));
    assert!(f.store_entries().is_empty(), "nothing acquired or staged");
    // Exactly the admission bound suffices: B_install, or the re-install
    // path's where that is larger (LD-CI2-3).
    let g = Fixture::new(nested());
    let (gb, gr) = g.evidence_bounds();
    assert_eq!(gb, b);
    let admit = WorkCost {
        objects: gb.objects.max(gr.objects),
        edges: gb.edges.max(gr.edges),
        bytes: gb.bytes.max(gr.bytes),
    };
    let mut ledger = WorkLedger::with_limits(admit).unwrap();
    assert_eq!(g.install_on(&mut ledger).unwrap(), Installed::Published);
}

#[test]
fn ci_t22_exhaustion_at_executed_rows_publishes_nothing() {
    // The bare transaction on ledgers short by one unit in each dimension
    // fails by law 468's route at some executed row, and publishes nothing.
    let f = Fixture::new(nested());
    let mut full = WorkLedger::snapshot_profile();
    f.transaction_on(&mut full).unwrap();
    let used = full.used();
    for short in [
        WorkCost {
            objects: used.objects - 1,
            ..used
        },
        WorkCost {
            bytes: used.bytes - 1,
            ..used
        },
        WorkCost {
            edges: used.edges / 2,
            ..used
        },
        WorkCost {
            edges: used.edges / 10,
            ..used
        },
    ] {
        let g = Fixture::new(nested());
        let mut ledger = WorkLedger::with_limits(short).unwrap();
        assert!(matches!(
            g.transaction_on(&mut ledger),
            Err(WorkFailure::Budget(_))
        ));
        assert!(!g.generation().exists());
    }
}

#[test]
fn ci_pt7_the_ordering_charges_each_buffer_and_comparison_first() {
    for n in [1usize, 2, 8, 9, 100_000] {
        let mut ledger = WorkLedger::snapshot_profile();
        let mut comparisons = 0usize;
        let order = ledger
            .scope::<_, ()>(|work| {
                let before = work.used();
                let order = charged_sort::<()>(n, work, |a, b| {
                    comparisons += 1;
                    (a % 7, a) < (b % 7, b)
                })?;
                let used = work.used();
                assert_eq!(used.objects - before.objects, 2, "two buffers");
                assert_eq!(used.bytes - before.bytes, 2 * n * 4);
                assert_eq!(used.edges - before.edges, comparisons);
                Ok(order)
            })
            .unwrap();
        assert!(comparisons <= sort_comparisons(n).unwrap(), "{n}");
        assert!(
            order
                .windows(2)
                .all(|w| (w[0] % 7, w[0]) < (w[1] % 7, w[1]))
        );
    }
    // One unit short of the scratch buffer refuses before it; one comparison
    // short refuses before that comparison.
    let n = 64;
    let buffer = index_buffer_cost(n).unwrap();
    let mut ledger = WorkLedger::with_limits(WorkCost {
        objects: 1,
        edges: 1000,
        bytes: 1 << 20,
    })
    .unwrap();
    let mut called = 0;
    let r = ledger.scope::<_, ()>(|work| {
        charged_sort::<()>(n, work, |a, b| {
            called += 1;
            a < b
        })
    });
    assert!(matches!(
        r,
        Err(WorkFailure::Budget(WorkBudgetError::Objects))
    ));
    assert_eq!(
        called, 0,
        "no comparison before the scratch buffer is funded"
    );
    let mut ledger = WorkLedger::with_limits(WorkCost {
        objects: 2,
        edges: 5,
        bytes: 2 * buffer.bytes,
    })
    .unwrap();
    let mut called = 0;
    let r = ledger.scope::<_, ()>(|work| {
        charged_sort::<()>(n, work, |a, b| {
            called += 1;
            a < b
        })
    });
    assert!(matches!(
        r,
        Err(WorkFailure::Budget(WorkBudgetError::Edges))
    ));
    assert_eq!(
        called, 5,
        "the sixth comparison is refused before it is made"
    );
}

#[test]
fn the_member_and_component_orders_differ_where_they_must() {
    let mut paths = ["a/b", "a-x", "a", "Z"];
    paths.sort_by(|a, b| a.as_bytes().cmp(b.as_bytes()));
    assert_eq!(paths, ["Z", "a", "a-x", "a/b"], "member order");
    paths.sort_by(|a, b| component_cmp(a, b));
    assert_eq!(
        paths,
        ["Z", "a", "a/b", "a-x"],
        "component order keeps a's subtree contiguous"
    );
}

// ---- The record (CI-PT-2) and source pins (CI-PT-3, CI-T11, CI-T13) ----

#[test]
fn ci_pt2_the_record_length_and_bytes_are_the_canonical_encoding() {
    for specs in [nested(), file_only()] {
        let f = Fixture::new(specs);
        let candidate = f.candidate();
        let component = f.component.authenticated();
        let e = evidence(&component, &candidate, MACOS).unwrap();
        let bytes = e.record.encode();
        assert_eq!(bytes.len(), e.record.length());
        let canonical = canonical_bytes(&parse_json(&bytes).unwrap()).unwrap();
        assert_eq!(canonical, bytes);
        let V::Object(m) = parse_json(&bytes).unwrap() else {
            panic!()
        };
        assert_eq!(
            m.keys().map(String::as_str).collect::<Vec<_>>(),
            [
                "archiveDigest",
                "archiveProfileId",
                "catalogRelease",
                "closureId",
                "componentManifestDigest",
                "platform"
            ]
        );
    }
    // Escapes count exactly.
    let r = Record {
        archive_digest: "a\"b\\c\n\u{1}é",
        envelope_digest: "e",
        manifest_digest: "m",
        stable_id: "s",
        version: "v",
        closure_id: "c",
        component_manifest_digest: [b'0'; 64],
        platform: "p",
    };
    let bytes = r.encode();
    assert_eq!(bytes.len(), r.length());
    assert_eq!(
        canonical_bytes(&parse_json(&bytes).unwrap()).unwrap(),
        bytes
    );
}

#[test]
fn source_pins_access_mode_fixture_store_and_no_network_or_spawn() {
    let installation = include_str!("installation.rs");
    let retained = include_str!("retained_tree.rs");
    // CI-PT-3: one access mode, chosen before the open; no retry in another.
    assert_eq!(installation.matches("FINALIZE_ACCESS").count(), 2);
    assert!(!installation.contains("Access::ReadWrite"));
    // CI-T11: the fixture store only under the joint predicate.
    let predicate =
        "#[cfg(any(test, feature = \"crash-matrix\", feature = \"scenario-fixtures\"))]";
    let at = installation.find("pub fn fixture(").unwrap();
    assert_eq!(
        installation[..at]
            .trim_end()
            .lines()
            .next_back()
            .unwrap()
            .trim(),
        predicate
    );
    assert_eq!(installation.matches(predicate).count(), 1);
    // CI-T13: no socket, URL or spawn; no environment read.
    for source in [
        installation,
        retained,
        include_str!("../../platform/src/component_tree.rs"),
    ] {
        let code: String = source
            .lines()
            .filter(|l| !l.trim_start().starts_with("//"))
            .collect::<Vec<_>>()
            .join("\n");
        for forbidden in [
            "std::net",
            "TcpStream",
            "UdpSocket",
            "http:",
            "https:",
            "std::process",
            "Command::",
            "spawn(",
            "std::env",
            "let _ =",
        ] {
            assert!(!code.contains(forbidden), "{forbidden}");
        }
    }
}

#[test]
fn the_buffer_price_equals_snap_s() {
    let ours = include_str!("installation.rs");
    let snap = include_str!("../../host/src/snapshot.rs");
    let body = |s: &str, head: &str| {
        let at = s.find(head).unwrap() + head.len();
        let end = at + s[at..].find("\n}\n").unwrap();
        s[at..end].split_whitespace().collect::<Vec<_>>().join(" ")
    };
    assert_eq!(
        body(ours, "pub(crate) fn buffer_cost() -> WorkCost {"),
        body(snap, "pub(crate) fn buffer_cost() -> WorkCost {")
    );
}

#[test]
fn ci_t24_v2_refuses_a_wrong_final_mode_record_or_pin_before_the_rename() {
    let stage_of = |store: &std::path::Path| {
        std::fs::read_dir(store)
            .unwrap()
            .map(|e| e.unwrap().path())
            .find(|p| {
                p.file_name()
                    .unwrap()
                    .to_str()
                    .unwrap()
                    .starts_with(".opensip-stage-install-")
            })
            .unwrap()
    };
    type Tamper = fn(&std::path::Path);
    let cases: [(Tamper, &str); 4] = [
        (
            |s| {
                std::fs::set_permissions(s.join("tree/a/z"), std::fs::Permissions::from_mode(0o600))
                    .unwrap()
            },
            "mode",
        ),
        (
            |s| {
                std::fs::set_permissions(s.join(RECORD), std::fs::Permissions::from_mode(0o600))
                    .unwrap();
                std::fs::write(s.join(RECORD), b"{}").unwrap();
                std::fs::set_permissions(s.join(RECORD), std::fs::Permissions::from_mode(0o400))
                    .unwrap();
            },
            "association",
        ),
        (|s| std::fs::remove_file(s.join(PIN)).unwrap(), "pin"),
        (|s| std::fs::write(s.join(PIN), b"x").unwrap(), "pin"),
    ];
    for (tamper, expect) in cases {
        let f = Fixture::new(nested());
        let store = f.store_path.clone();
        let r = with_seam(
            move |step| {
                if step == "finalized" {
                    tamper(&stage_of(&store));
                }
                Ok(())
            },
            || f.install(),
        );
        let fault = match r {
            Err(InstallFailure::Io(InstallIo::Verify(fault))) => fault,
            other => panic!("{expect}: {other:?}"),
        };
        match expect {
            "mode" => assert!(matches!(fault, TreeFault::Mode { .. }), "{fault:?}"),
            "association" => assert!(matches!(fault, TreeFault::Association), "{fault:?}"),
            _ => assert!(matches!(fault, TreeFault::Pin), "{fault:?}"),
        }
        assert!(
            !f.generation().exists(),
            "{expect}: refused before the rename"
        );
    }
}

#[test]
fn finalize_sets_each_mode_before_its_barrier() {
    // Every metadata change precedes the barrier that covers it (LAW item 4
    // step 4): a source pin over the finalization walk.
    let source = include_str!("installation.rs");
    let at = source.find("fn finalize(").unwrap();
    let walk = &source[at..at + source[at..].find("\n}\n").unwrap()];
    let mode = walk
        .find("ct::set_mode(file.file(), installed_mode(&row), work)")
        .unwrap();
    let barrier = walk.find("ct::barrier_file(file.file(), work)").unwrap();
    assert!(mode < barrier);
    let dmode = walk
        .find("ct::set_mode(level.directory.as_file(), 0o500, work)")
        .unwrap();
    let dbar = walk
        .find(".confirm_directory_barrier_accounted(work)")
        .unwrap();
    assert!(dmode < dbar);
    assert!(!walk.contains("check_listing"), "no readdir in step 4");
}

#[test]
fn a_candidate_of_another_platform_refuses_at_installation() {
    // The same body's other platform row: the candidate's Blobs are not this
    // tree's file rows, so nothing is staged under its name.
    let f = Fixture::two_platforms(nested(), vec![file("only", 0o755, b"x86")]);
    let other = f.candidate_for(SelectedPlatform {
        os: "macos",
        arch: "x86_64",
    });
    let mut ledger = WorkLedger::snapshot_profile();
    let r = within(&mut ledger, |work| {
        install(
            &f.store,
            &f.component.authenticated(),
            &other,
            MACOS,
            &f.archive_path,
            work,
        )
    });
    assert!(
        matches!(
            r,
            Err(InstallFailure::Admission(AdmissionRefusal::Evidence))
        ),
        "{r:?}"
    );
    assert!(
        !f.store_path
            .join(other.closure().strip_prefix("closure2:").unwrap())
            .exists()
    );
    // The matching candidate installs.
    assert_eq!(f.install().unwrap(), Installed::Published);
}

// ---- CI2-R1-RF-3: allocations funded first, and bounded live handles ----

/// Every allocation site of the production sources, each with the statement
/// that funds it immediately before it (a source-order guard), and no other
/// allocation. Error carriers (`io::Error::new` after a refusal) are not
/// work: the act has already ended. Stack-of-levels and parent-chain growth
/// is funded by each `desc` charge, made before its push.
#[test]
fn every_allocation_is_funded_immediately_before_it() {
    let sites: [(&str, &str, &str); 9] = [
        (
            "installation.rs",
            "    work.charge(buffer)?;",
            "    let mut from = Vec::with_capacity(n);",
        ),
        (
            "installation.rs",
            "    work.charge(buffer)?;",
            "    let mut to = Vec::with_capacity(n);",
        ),
        (
            "installation.rs",
            "    work.charge(buffer_cost())?;",
            "    let mut buffer = vec![0u8; READ_CHUNK];",
        ),
        (
            "installation.rs",
            "    work.charge(owned_record(record.length()))?;",
            "    let bytes = record.encode();",
        ),
        (
            "retained_tree.rs",
            "    work.charge(inst::buffer_cost()).map_err(budget)?;",
            "    let mut buffer = vec![0u8; READ_CHUNK];",
        ),
        (
            "retained_tree.rs",
            "        .map_err(budget)?;",
            "    let expected = evidence.record.encode();",
        ),
        // Unit CI-3L (CI-A3-b, -d): the store path, each hop temporary and
        // the launch-path buffer.
        (
            "installation.rs",
            "    work.charge(store_path_cost(length))?;",
            "    let mut bytes = Vec::with_capacity(length);",
        ),
        (
            "retained_tree.rs",
            "                work.charge(heap(length)).map_err(budget)?;",
            "                let mut joined = String::with_capacity(length);",
        ),
        (
            "retained_tree.rs",
            "        work.charge(heap(length)).map_err(budget)?;",
            "        let mut bytes = Vec::with_capacity(length);",
        ),
    ];
    let source = |name: &str| match name {
        "installation.rs" => include_str!("installation.rs"),
        _ => include_str!("retained_tree.rs"),
    };
    for (file, funding, site) in sites {
        let lines: Vec<&str> = source(file).lines().collect();
        let at = lines
            .iter()
            .position(|l| *l == site)
            .unwrap_or_else(|| panic!("{file}: {site}"));
        assert_eq!(lines[at - 1], funding, "{file}: {site}");
    }
    // `Record::encode` reserves exactly `R`, which its callers funded.
    assert!(
        include_str!("installation.rs")
            .contains("        let mut out = Vec::with_capacity(self.length());")
    );
    // No other allocating construct appears outside the tests.
    for file in ["installation.rs", "retained_tree.rs"] {
        let code = source(file);
        let code = &code[..code.rfind("#[cfg(test)]\n#[path").unwrap()];
        let count = |p: &str| code.matches(p).count();
        let expected: [(&str, usize); 6] = match file {
            "installation.rs" => [
                ("Vec::with_capacity(", 4),
                ("String::with_capacity(", 0),
                ("vec![", 2),
                (".encode()", 1),
                (".to_vec()", 0),
                ("Box::new(", 0),
            ],
            _ => [
                ("Vec::with_capacity(", 1),
                ("String::with_capacity(", 1),
                ("vec![", 1),
                (".encode()", 1),
                (".to_vec()", 0),
                ("Box::new(", 0),
            ],
        };
        for (pattern, n) in expected {
            assert_eq!(count(pattern), n, "{file}: {pattern}");
        }
    }
}

/// Live descriptors of this process.
pub(crate) fn live_handles() -> usize {
    std::fs::read_dir("/dev/fd").unwrap().count()
}

/// Run the test `name` alone in a child process of this test binary, so no
/// other test's descriptors enter its counts; inside the child, run `body`.
pub(crate) fn isolated(name: &str, body: impl FnOnce()) {
    const CHILD: &str = "OPENSIP_TEST_CI2_ISOLATED";
    if std::env::var_os(CHILD).is_some() {
        body();
        return;
    }
    let out = std::process::Command::new(std::env::current_exe().unwrap())
        .args(["--exact", name, "--test-threads=1", "--nocapture"])
        .env(CHILD, "1")
        .output()
        .unwrap();
    assert!(
        out.status.success() && String::from_utf8_lossy(&out.stdout).contains("1 passed"),
        "{}\n{}",
        String::from_utf8_lossy(&out.stdout),
        String::from_utf8_lossy(&out.stderr)
    );
}

#[test]
fn ci_t22_live_handles_stay_bounded_on_a_large_tree() {
    isolated(
        "installation::tests::ci_t22_live_handles_stay_bounded_on_a_large_tree",
        large_tree_handles,
    );
}
fn large_tree_handles() {
    // 50,000 entries: 100 directories, each with two files and 497 symlinks.
    // (The identity reader's 4 MiB body cap bounds a manifest's entry
    // count below the shape's 100,000; this is near the largest body.)
    let mut specs = Vec::new();
    for d in 0..100 {
        let dir_path = format!("d{d:03}");
        specs.push(dir(&dir_path, 0o755));
        specs.push(file(&format!("{dir_path}/f0"), 0o644, b"0"));
        specs.push(file(&format!("{dir_path}/f1"), 0o755, b"1"));
        for s in 0..497 {
            specs.push(link(&format!("{dir_path}/s{s:03}"), "f0"));
        }
    }
    assert_eq!(specs.len(), 50_000);
    let f = Fixture::new(specs);
    let baseline = live_handles();
    let peak = std::rc::Rc::new(std::cell::Cell::new(0usize));
    let calls = std::rc::Rc::new(std::cell::Cell::new(0usize));
    let (p, c) = (peak.clone(), calls.clone());
    with_seam(
        move |step| {
            if matches!(step, "member" | "row" | "final-row") {
                c.set(c.get() + 1);
                if c.get() % 97 == 0 {
                    p.set(p.get().max(live_handles()));
                }
            }
            Ok(())
        },
        || assert_eq!(f.install().unwrap(), Installed::Published),
    );
    assert!(
        calls.get() >= 150_000,
        "every member and row was sampled from"
    );
    // The store, the stage, `tree/`, the archive and its buffer's file, the
    // current member's parent chain or branch stack (depth 2 here), and one
    // entry's own handle: never one per entry.
    assert!(
        peak.get() <= baseline + 12,
        "peak {} over baseline {baseline}",
        peak.get()
    );
}

#[test]
fn every_charge_precedes_its_work_in_the_installer_and_reader() {
    // A source-order guard (the pre-submission checklist's item 1) over the
    // whole installer and reader: in each function, each charge precedes the
    // work it funds.
    let sources = [
        include_str!("installation.rs"),
        include_str!("retained_tree.rs"),
    ];
    let body = |function: &str| -> &str {
        let source = sources
            .iter()
            .find(|s| s.contains(function))
            .unwrap_or_else(|| panic!("{function}"));
        let at = source.find(function).unwrap();
        &source[at..at + source[at..].find("\n}\n").unwrap()]
    };
    for (function, charge, work) in [
        (
            "pub(crate) fn descend(",
            "work.charge(descend_cost(name.len()))?;",
            ".open_child_directory(",
        ),
        (
            "pub(crate) fn check_listing_of(",
            "work.charge(",
            ".visit_entry_names::<()>(",
        ),
        (
            "pub(crate) fn read_verified(",
            "work.charge(READ)?;",
            "reader.read(buffer)",
        ),
        (
            "pub(crate) fn charged_sort<E>(",
            "work.charge(COMPARISON)?;",
            "if less(from[j], from[i])",
        ),
        (
            "pub(crate) fn charged_find<E>(",
            "work.charge(COMPARISON)?;",
            "match component_cmp(",
        ),
        (
            "fn associate(",
            "work.charge(COMPARISON)?;",
            "if blob.path() != row.path",
        ),
        (
            "fn stream(",
            "work.charge(READ)?;",
            ".read(&mut buffer[end..end + room])",
        ),
        (
            "pub(crate) fn check_record(",
            "work.charge(READ)?;",
            "reader.read(buffer)",
        ),
        (
            "fn record_file(",
            "work.charge(owned_record(record.length()))?;",
            "record.encode()",
        ),
        (
            "fn transaction(",
            "work.charge(owned_record(NAME_BYTES + 1))?;",
            "ct::entry_status(&store.directory",
        ),
        (
            "fn transaction(",
            "work.charge(owned_record(archive.as_os_str().len()))?;",
            "ct::open_archive(archive, work)",
        ),
        (
            "pub(crate) fn walk(",
            "work.charge(owned_record(ct::LINK_BUFFER))?;",
            "ct::read_link(",
        ),
        (
            "pub(crate) fn open_with<'s, 'a>(",
            "work.charge(owned_record(evidence.record.length()))",
            "evidence.record.encode()",
        ),
        (
            "pub(crate) fn open_with<'s, 'a>(",
            "work.charge(owned_record(inst::NAME_BYTES + 1))",
            "descend(&store.directory, evidence.name",
        ),
    ] {
        let b = body(function);
        let c = b
            .find(charge)
            .unwrap_or_else(|| panic!("{function}: {charge}"));
        let w = b.find(work).unwrap_or_else(|| panic!("{function}: {work}"));
        assert!(c < w, "{function}: `{work}` precedes `{charge}`");
    }
}

#[test]
fn the_platform_token_table_is_the_catalogs_list_in_order() {
    // The pre-submission checklist's item 4: the S8 alias table, member by
    // member and in order, against the recovery catalog's own list, so a
    // same-cardinality substitution or a source-side addition both fail.
    let catalog = include_str!("../../security/src/trust/recovery_catalog.rs");
    let at = catalog.find(".contains(&s)").unwrap();
    let open = catalog[..at].rfind('[').unwrap();
    let listed: Vec<&str> = catalog[open + 1..at - 1]
        .split(',')
        .map(|t| t.trim().trim_matches('"'))
        .collect();
    let ours: Vec<&str> = [
        ("macos", "arm64"),
        ("macos", "x86_64"),
        ("linux", "arm64"),
        ("linux", "x86_64"),
    ]
    .iter()
    .map(|&(os, arch)| platform_token(SelectedPlatform { os, arch }).unwrap())
    .collect();
    assert_eq!(listed, ours);
    for (os, arch) in [
        ("windows", "x86_64"),
        ("macos", "aarch64"),
        ("linux", "riscv64"),
    ] {
        assert!(platform_token(SelectedPlatform { os, arch }).is_none());
    }
}
