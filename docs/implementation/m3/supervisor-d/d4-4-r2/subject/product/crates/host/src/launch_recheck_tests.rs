//! Actual CI-3 installed fixture stores, not mocked native recheck results.
//! TestComponent is explicitly synthetic validated manifest evidence, not
//! trust admission or C4 selection. The provider-spoken controls spawn only the first-party compiled fixture.
use super::*;
use opensip_components::control_protocol::{Platform, SubprotocolTuple};
use opensip_components::session_factory::{IdentityAuthority, MemberAuthority};
use opensip_identity::{RegisteredSchemas, canonical_bytes, parse_json, raw_sha256};
use opensip_lifecycle::installation::{ComponentStore, install};
use opensip_lifecycle::retained_tree::{PinRequest, open_retained_tree, read_fixture};
use opensip_platform::{RetainedDirectory, WorkBudgetError, WorkLedger};
use opensip_security::{ClosureCandidate, SelectedPlatform, TestComponent, archive_profile as ap};
use std::os::unix::fs::{MetadataExt, PermissionsExt};
use std::{cell::Cell, rc::Rc};

#[path = "launch_recheck_ts2_fixture.rs"]
mod ts2_fixture;
#[path = "launch_recheck_wire_fixture.rs"]
mod wire_fixture;
use std::{
    fs::{self, File},
    path::{Path, PathBuf},
    sync::OnceLock,
};
const PLATFORM: SelectedPlatform<'static> = SelectedPlatform {
    os: "macos",
    arch: "arm64",
};
const DATA: &[u8] = b"D4 fixture provider bytes\n";
const ENVELOPE: &[u8] = br#"{"D4":"synthetic fixture envelope"}"#;
fn registry() -> &'static RegisteredSchemas {
    static REGISTRY: OnceLock<RegisteredSchemas> = OnceLock::new();
    REGISTRY.get_or_init(|| {
        let root = Path::new(env!("CARGO_MANIFEST_DIR")).join("../..");
        let sources: Vec<Vec<u8>> = RegisteredSchemas::source_requirements()
            .iter()
            .map(|row| fs::read(root.join(row.source_path())).unwrap())
            .collect();
        RegisteredSchemas::from_sources(&sources.iter().map(Vec::as_slice).collect::<Vec<_>>())
            .unwrap()
    })
}
fn writable(path: &Path) {
    if fs::symlink_metadata(path).is_ok_and(|meta| meta.is_dir()) {
        fs::set_permissions(path, fs::Permissions::from_mode(0o700)).unwrap();
        for entry in fs::read_dir(path).unwrap() {
            writable(&entry.unwrap().path());
        }
    }
}
struct Scratch(PathBuf);
impl Drop for Scratch {
    fn drop(&mut self) {
        writable(&self.0);
        let result = fs::remove_dir_all(&self.0);
        if !std::thread::panicking() {
            result.unwrap();
        }
    }
}
struct Fixture {
    root: PathBuf,
    store_path: PathBuf,
    store: ComponentStore,
    component: TestComponent,
    archive: PathBuf,
    _scratch: Scratch,
}
impl Fixture {
    fn new() -> Self {
        Self::with_provider(DATA, "adapter")
    }
    fn with_provider(data: &[u8], mode: &str) -> Self {
        Self::with_files(data, None, mode)
    }
    fn with_files(data: &[u8], node: Option<&[u8]>, mode: &str) -> Self {
        assert!(mode.bytes().all(|b| b.is_ascii_lowercase()));
        let root = std::env::temp_dir().join(format!(
            "opensip-d4-{mode}-{}",
            opensip_platform::request_entropy()
                .unwrap()
                .iter()
                .map(|byte| format!("{byte:02x}"))
                .collect::<String>()
        ));
        fs::create_dir(&root).unwrap();
        let scratch = Scratch(root.clone());
        fs::set_permissions(&root, fs::Permissions::from_mode(0o700)).unwrap();
        let store_path = root.join("components");
        fs::create_dir(&store_path).unwrap();
        fs::set_permissions(&store_path, fs::Permissions::from_mode(0o700)).unwrap();
        let directory =
            RetainedDirectory::from_retained_handle(File::open(&store_path).unwrap()).unwrap();
        let mut ledger = WorkLedger::snapshot_profile();
        ledger
            .scope(|work| {
                opensip_platform::append_owner_zero_allow_accounted(directory.as_file(), work)
            })
            .unwrap();
        let store = ledger
            .scope(|work| {
                ComponentStore::fixture(
                    directory,
                    &store_path,
                    fs::metadata(&store_path).unwrap().uid(),
                    work,
                )
            })
            .unwrap();
        let hash = raw_sha256(data);
        let mut rows = vec![
            ap::TreeRow {
                path: "entrypoint",
                mode: 0o777,
                kind: ap::RowKind::Symlink { target: "provider" },
            },
            ap::TreeRow {
                path: "provider",
                mode: 0o755,
                kind: ap::RowKind::File {
                    length: data.len() as u64,
                    sha256: hash,
                },
            },
        ];
        let mut contents = vec![("provider", data)];
        if let Some(node) = node {
            rows.push(ap::TreeRow {
                path: "node",
                mode: 0o755,
                kind: ap::RowKind::File {
                    length: node.len() as u64,
                    sha256: raw_sha256(node),
                },
            });
            rows.push(ap::TreeRow {
                path: "openssl.cnf",
                mode: 0o644,
                kind: ap::RowKind::File {
                    length: 0,
                    sha256: raw_sha256(b""),
                },
            });
            contents.extend([("node", node), ("openssl.cnf", &b""[..])]);
        }
        rows.sort_by_key(|r| r.path);
        contents.sort_by_key(|(path, _)| *path);
        let archive_bytes = ap::emit(&rows, &contents).unwrap();
        let archive = root.join("release.tar");
        fs::write(&archive, &archive_bytes).unwrap();
        let line = include_bytes!("../../security/tests/fixtures/manifest268-semantic.ndjson")
            .split(|b| *b == b'\n')
            .find(|b| !b.is_empty())
            .unwrap();
        let original: serde_json::Value = serde_json::from_slice(line).unwrap();
        let hex = original["raw"].as_str().unwrap();
        let raw: Vec<u8> = (0..hex.len())
            .step_by(2)
            .map(|i| u8::from_str_radix(&hex[i..i + 2], 16).unwrap())
            .collect();
        let mut body: serde_json::Value = serde_json::from_slice(&raw).unwrap();
        let object = body.as_object_mut().unwrap();
        object.remove("commands");
        object.insert("role".into(), serde_json::json!("toolchain"));
        object.insert("capabilities".into(), serde_json::json!([]));
        object.insert("permissions".into(), serde_json::json!([]));
        object.insert("closureProtocolMajor".into(), serde_json::json!(1));
        let entries: Vec<_> = rows.iter().map(|row| match row.kind {
            ap::RowKind::File {length,sha256} => serde_json::json!({"path":row.path,"mode":format!("{:04o}",row.mode),"type":"file","length":length,"sha256":digest_hex(&sha256)}),
            ap::RowKind::Symlink {target} => serde_json::json!({"path":row.path,"mode":format!("{:04o}",row.mode),"type":"symlink","target":target}),
            _ => unreachable!("first-party fixture uses only files and one alias"),
        }).collect();
        object.insert("platforms".into(), serde_json::json!([{"os":"macos","arch":"arm64","entrypoint":"provider","tree":{"entries":entries}}]));
        let body =
            canonical_bytes(&parse_json(&serde_json::to_vec(&body).unwrap()).unwrap()).unwrap();
        let archive_hash = digest_hex(&raw_sha256(&archive_bytes));
        let zero = "0".repeat(64);
        let release = parse_json(serde_json::to_string(&serde_json::json!({"artifacts":[{"archiveDigest":archive_hash,"archiveProfileId":ap::PROFILE_ID,"platform":"macos-arm64","sha256":archive_hash}],
            "envelopeDigest":digest_hex(&raw_sha256(ENVELOPE)),"hostCoreConstraint":{"includeMax":false,"includeMin":true,"max":"0.2.0","min":"0.1.0"},
            "manifestDigest":digest_hex(&raw_sha256(&body)),"manifestPreimageSha256":zero,"publisher":"opensip","sourceClass":"first-party",
            "stableId":"6f1c2c3e-0b6a-4a1c-9c2d-1f0e2a3b4c5d","version":"1.0.0"})).unwrap().as_bytes()).unwrap();
        let component = TestComponent::new(body, ENVELOPE.to_vec(), release).unwrap();
        let result = Self {
            root,
            store_path,
            store,
            component,
            archive,
            _scratch: scratch,
        };
        let candidate = result.candidate();
        let component = result.component.authenticated();
        ledger
            .scope(|work| {
                install(
                    &result.store,
                    &component,
                    &candidate,
                    PLATFORM,
                    &result.archive,
                    work,
                )
                .map_err(WorkFailure::Operation)
            })
            .unwrap();
        result
    }
    fn candidate(&self) -> ClosureCandidate<'_> {
        WorkLedger::snapshot_profile()
            .scope(|work| {
                opensip_security::component_candidate(
                    &self.component.authenticated(),
                    PLATFORM,
                    None,
                    registry(),
                    work,
                )
            })
            .unwrap()
    }
    fn tree_path(&self) -> PathBuf {
        self.store_path
            .join(
                self.candidate()
                    .closure()
                    .strip_prefix("closure2:")
                    .unwrap(),
            )
            .join("tree")
    }
    fn opened<T>(&self, then: impl FnOnce(&mut [RetainedTree<'_, '_>]) -> T) -> T {
        let candidate = self.candidate();
        let component = self.component.authenticated();
        let tree = WorkLedger::snapshot_profile()
            .scope(|work| {
                open_retained_tree(
                    &self.store,
                    &component,
                    &candidate,
                    PLATFORM,
                    PinRequest::UnderFence,
                    work,
                )
                .map_err(WorkFailure::Operation)
            })
            .unwrap();
        then(&mut [tree])
    }
    fn change(&self, action: impl FnOnce(&Path)) {
        let tree = self.tree_path();
        fs::set_permissions(&tree, fs::Permissions::from_mode(0o700)).unwrap();
        action(&tree.join("provider"));
        fs::set_permissions(&tree, fs::Permissions::from_mode(0o500)).unwrap();
    }
}
fn bindings() -> [Binding<'static>; 4] {
    [
        Binding {
            name: "alias",
            tree: 0,
            request: MemberRequest::File("entrypoint"),
        },
        Binding {
            name: "entrypoint",
            tree: 0,
            request: MemberRequest::Entrypoint,
        },
        Binding {
            name: "provider",
            tree: 0,
            request: MemberRequest::File("provider"),
        },
        Binding {
            name: "toolchain",
            tree: 0,
            request: MemberRequest::Directory(""),
        },
    ]
}
fn launch<'a>(provider: &'a Path, root: &'a Path) -> Launch<'a> {
    Launch::Rust {
        entrypoint: NamedMember {
            name: "entrypoint",
            launch_path: provider,
        },
        provider: NamedMember {
            name: "provider",
            launch_path: provider,
        },
        toolchain_root: NamedMember {
            name: "toolchain",
            launch_path: root,
        },
    }
}

#[test]
fn native_adapter_rechecks_resolved_entrypoint_and_directory_without_fabricated_digest() {
    let fixture = Fixture::new();
    let root = fixture.tree_path();
    let provider = root.join("provider");
    let bindings = bindings();
    fixture.opened(|trees| {
        let mut ledger = WorkLedger::snapshot_profile();
        ledger
            .scope(|work| {
                let mut adapter =
                    Rechecker::new(trees, &bindings, &launch(&provider, &root), work).unwrap();
                let entry = adapter.recheck("entrypoint", work).unwrap();
                assert_eq!(entry.launch_path, provider);
                let identity = entry.closure_recheck.unwrap();
                assert_eq!(identity.member, "provider");
                assert_eq!(identity.sha256, digest_hex(&raw_sha256(DATA)));
                let alias = adapter.recheck("alias", work).unwrap();
                assert_eq!(alias.launch_path, provider);
                assert_eq!(alias.closure_recheck.unwrap().member, "provider");
                assert_eq!(
                    (identity.device, identity.inode),
                    (
                        fs::metadata(&provider).unwrap().dev(),
                        fs::metadata(&provider).unwrap().ino()
                    )
                );
                let directory = adapter.recheck("toolchain", work).unwrap();
                assert_eq!(directory.launch_path, root);
                assert!(directory.closure_recheck.is_none());
                Ok::<_, WorkFailure<()>>(())
            })
            .unwrap();
    });
}

#[test]
fn native_adapter_preserves_each_actual_member_corruption() {
    for (case, expected) in [
        (0, CorruptCause::Digest),
        (1, CorruptCause::Length),
        (2, CorruptCause::Mode),
        (3, CorruptCause::Type),
        (4, CorruptCause::Absent),
    ] {
        let fixture = Fixture::new();
        let root = fixture.tree_path();
        let provider = root.join("provider");
        let bindings = bindings();
        fixture.opened(|trees| { fixture.change(|path| match case {
            0|1=>{fs::set_permissions(path,fs::Permissions::from_mode(0o600)).unwrap();let mut bytes=DATA.to_vec();if case==0{bytes[0]^=1}else{bytes.pop();}fs::write(path,bytes).unwrap();fs::set_permissions(path,fs::Permissions::from_mode(0o500)).unwrap();},
            2=>fs::set_permissions(path,fs::Permissions::from_mode(0o400)).unwrap(),
            3=>{fs::remove_file(path).unwrap();fs::create_dir(path).unwrap();},
            _=>fs::remove_file(path).unwrap(),
        });
        let mut ledger=WorkLedger::snapshot_profile();ledger.scope(|work| {
            let mut adapter=Rechecker::new(trees,&bindings,&launch(&provider,&root),work).unwrap();
            assert!(matches!(adapter.recheck("provider",work),Err(RecheckFailure::Corrupt(actual))if actual==expected));
            Ok::<_,WorkFailure<()>>(())
        }).unwrap(); });
    }
}

#[test]
fn native_adapter_keeps_injected_read_io_distinct_from_corrupt() {
    let fixture = Fixture::new();
    let root = fixture.tree_path();
    let provider = root.join("provider");
    let bindings = bindings();
    fixture.opened(|trees| { let mut ledger=WorkLedger::snapshot_profile();ledger.scope(|work| {
        let mut adapter=Rechecker::new(trees,&bindings,&launch(&provider,&root),work).unwrap();let guard=read_fixture::fail_next_read();
        assert!(matches!(adapter.recheck("provider",work),Err(RecheckFailure::Io{call:"read",error})if error.kind()==std::io::ErrorKind::Other));assert!(guard.was_triggered());
        Ok::<_,WorkFailure<()>>(())
    }).unwrap(); });
}

#[test]
fn native_adapter_one_short_before_open_and_before_first_read_stays_budget() {
    // This two-row/root-file fixture has one host binding comparison, one
    // kind check and one committed-row lookup, then openat+fstat, then read.
    // Fixed literal prefixes 3 and 5 are independent of production prices.
    for limit in [3, 5] {
        let fixture = Fixture::new();
        let root = fixture.tree_path();
        let provider = root.join("provider");
        let bindings = bindings();
        fixture.opened(|trees| {
            let mut setup = WorkLedger::snapshot_profile();
            setup
                .scope(|work| {
                    let mut adapter =
                        Rechecker::new(trees, &bindings, &launch(&provider, &root), work).unwrap();
                    let mut budget = WorkLedger::with_limits(WorkCost {
                        objects: 100,
                        edges: limit,
                        bytes: 1 << 20,
                    })
                    .unwrap();
                    let guard = read_fixture::fail_next_read();
                    let result = budget.scope(|work| {
                        adapter
                            .recheck("provider", work)
                            .map_err(WorkFailure::Operation)
                    });
                    assert!(matches!(
                        result,
                        Err(WorkFailure::Operation(RecheckFailure::Budget(
                            WorkBudgetError::Edges
                        )))
                    ));
                    assert_eq!(budget.used().edges, limit);
                    assert!(!guard.was_triggered());
                    let result = WorkLedger::snapshot_profile().scope(|work| {
                        adapter
                            .recheck("provider", work)
                            .map_err(WorkFailure::Operation)
                    });
                    assert!(matches!(
                        result,
                        Err(WorkFailure::Operation(RecheckFailure::Budget(
                            WorkBudgetError::Closed
                        )))
                    ));
                    Ok::<_, WorkFailure<()>>(())
                })
                .unwrap();
        });
    }
}

#[test]
fn native_adapter_rejects_a_spelling_that_now_names_another_inode() {
    let fixture = Fixture::new();
    let root = fixture.tree_path();
    let provider = root.join("provider");
    let bindings = bindings();
    fixture.opened(|trees| {
        // The retained handles still name the originally verified objects;
        // the launch spelling now names a different, byte-identical file.
        fs::rename(&fixture.store_path, fixture.root.join("held-components")).unwrap();
        fs::create_dir_all(&root).unwrap();
        fs::write(&provider, DATA).unwrap();
        fs::set_permissions(&provider, fs::Permissions::from_mode(0o500)).unwrap();
        let mut ledger = WorkLedger::snapshot_profile();
        ledger
            .scope(|work| {
                let mut adapter =
                    Rechecker::new(trees, &bindings, &launch(&provider, &root), work).unwrap();
                assert!(matches!(
                    adapter.recheck("provider", work),
                    Err(RecheckFailure::Corrupt(CorruptCause::Binding))
                ));
                Ok::<_, WorkFailure<()>>(())
            })
            .unwrap();
    });
}

#[test]
fn native_adapter_missing_role_is_a_pre_recheck_spec_refusal() {
    let fixture = Fixture::new();
    let root = fixture.tree_path();
    let provider = root.join("provider");
    let bindings = [Binding {
        name: "provider",
        tree: 0,
        request: MemberRequest::File("provider"),
    }];
    fixture.opened(|trees| {
        let mut ledger = WorkLedger::snapshot_profile();
        let guard = read_fixture::fail_next_read();
        ledger
            .scope(|work| {
                assert!(matches!(
                    Rechecker::new(trees, &bindings, &launch(&provider, &root), work),
                    Err(FactoryRefusal::SpecInconsistent(
                        "launch-binding-not-selected"
                    ))
                ));
                assert!(!guard.was_triggered());
                Ok::<_, WorkFailure<()>>(())
            })
            .unwrap();
    });
}

fn selected(fixture: &Fixture) -> AdmittedSelection {
    AdmittedSelection {
        stable_id: "6f1c2c3e-0b6a-4a1c-9c2d-1f0e2a3b4c5d".into(),
        manifest_digest: digest_hex(&raw_sha256(fixture.component.authenticated().body())),
        platform: Platform {
            os: "macos".into(),
            arch: "arm64".into(),
        },
        tuple: SubprotocolTuple {
            role: "analyzer".into(),
            role_subprotocol: "rust-semantic".into(),
            subprotocol_version: 3,
        },
    }
}
fn members<'a>(provider: &'a Path, root: &'a Path, hash: &'a str) -> [MemberAuthority<'a>; 3] {
    [
        MemberAuthority {
            member: NamedMember {
                name: "entrypoint",
                launch_path: provider,
            },
            kind: MemberKind::File,
            closure_member: "provider",
            file_sha256: Some(hash),
        },
        MemberAuthority {
            member: NamedMember {
                name: "provider",
                launch_path: provider,
            },
            kind: MemberKind::File,
            closure_member: "provider",
            file_sha256: Some(hash),
        },
        MemberAuthority {
            member: NamedMember {
                name: "toolchain",
                launch_path: root,
            },
            kind: MemberKind::Directory,
            closure_member: "",
            file_sha256: None,
        },
    ]
}
struct NoSource(Rc<Cell<usize>>);
impl opensip_components::provider_protocol::rust3::Rust3Source for NoSource {
    fn read(
        &mut self,
        _: &opensip_components::provider_protocol::rust3::Rust3SourceEntry,
        _: u64,
        _: usize,
    ) -> std::io::Result<Vec<u8>> {
        self.0.set(self.0.get() + 1);
        Err(std::io::Error::other("unexpected snapshot disclosure"))
    }
}

#[test]
fn actual_native_factory_composes_the_checked_sender_without_source_disclosure() {
    let fixture = Fixture::new();
    let root = fixture.tree_path();
    let provider = root.join("provider");
    let bindings = bindings();
    let selection = selected(&fixture);
    let hash = digest_hex(&raw_sha256(DATA));
    let members = members(&provider, &root, &hash);
    let (codec, identity, caps) = wire_fixture::rust();
    let authority = Authorities {
        selection: &selection,
        capabilities: &caps,
        entrypoint: "entrypoint",
        members: &members,
        identity: IdentityAuthority::Rust {
            expected_identity: &identity,
        },
    };
    fixture.opened(|trees| {
        let result = WorkLedger::snapshot_profile()
            .scope(|work| {
                prepare_session(
                    SessionInput {
                        selection: selection.clone(),
                        provider: codec,
                        launch: launch(&provider, &root),
                        memory_budget_bytes: 1 << 30,
                    },
                    trees,
                    &bindings,
                    &authority,
                    work,
                )
                .map_err(WorkFailure::Operation)
            })
            .unwrap();
        assert_eq!(result.session.launch.spec().executable(), provider);
        assert_eq!(result.session.launch.recheck().sha256, hash);
        let Provider::Rust { sender } = result.provider else {
            panic!()
        };
        let table = opensip_components::provider_protocol::table::Table::load(
            opensip_components::provider_protocol::table::Protocol::Rust3,
        )
        .unwrap();
        let reads = Rc::new(Cell::new(0));
        assert!(
            opensip_components::provider_protocol::rust3::Rust3Participant::from_sender(
                &table,
                sender,
                Box::new(NoSource(reads.clone()))
            )
            .is_ok()
        );
        assert_eq!(reads.get(), 0);
    });
}

#[test]
fn actual_native_factory_preserves_corruption_and_read_io_routes() {
    // Each observation crosses the real installed-store adapter AND the
    // factory. An adapter-only error is not evidence for the factory route.
    for case in 0..6 {
        let fixture = Fixture::new();
        let root = fixture.tree_path();
        let provider = root.join("provider");
        let bindings = bindings();
        let selection = selected(&fixture);
        let hash = digest_hex(&raw_sha256(DATA));
        let members = members(&provider, &root, &hash);
        let (codec, identity, caps) = wire_fixture::rust();
        let authority = Authorities {
            selection: &selection,
            capabilities: &caps,
            entrypoint: "entrypoint",
            members: &members,
            identity: IdentityAuthority::Rust {
                expected_identity: &identity,
            },
        };
        fixture.opened(|trees| {
            if case < 5 {
                fixture.change(|path| match case {
                    0 | 1 => {
                        fs::set_permissions(path, fs::Permissions::from_mode(0o600)).unwrap();
                        let mut bytes = DATA.to_vec();
                        if case == 0 { bytes[0] ^= 1; } else { bytes.pop(); }
                        fs::write(path, bytes).unwrap();
                        fs::set_permissions(path, fs::Permissions::from_mode(0o500)).unwrap();
                    }
                    2 => fs::set_permissions(path, fs::Permissions::from_mode(0o400)).unwrap(),
                    3 => { fs::remove_file(path).unwrap(); fs::create_dir(path).unwrap(); }
                    4 => fs::remove_file(path).unwrap(),
                    _ => unreachable!(),
                });
            }
            let read_guard = (case == 5).then(read_fixture::fail_next_read);
            let result = WorkLedger::snapshot_profile().scope(|work| {
                prepare_session(
                    SessionInput {
                        selection: selection.clone(), provider: codec,
                        launch: launch(&provider, &root), memory_budget_bytes: 1 << 30,
                    }, trees, &bindings, &authority, work,
                ).map_err(WorkFailure::Operation)
            });
            // Err is the only returned value: no launch escapes this boundary.
            let refusal = match result {
                Err(WorkFailure::Operation(refusal)) => refusal,
                _ => panic!("native refusal must survive factory composition, case {case}"),
            };
            use opensip_components::supervisor::records::OwnerRoute;
            if case == 5 {
                assert_eq!(refusal.route(), OwnerRoute::HostIo);
                assert!(matches!(refusal, FactoryRefusal::Recheck(RecheckFailure::Io { call: "read", error }) if error.kind() == std::io::ErrorKind::Other));
                assert!(read_guard.as_ref().unwrap().was_triggered());
            } else {
                let expected = [CorruptCause::Digest, CorruptCause::Length, CorruptCause::Mode, CorruptCause::Type, CorruptCause::Absent][case];
                assert_eq!(refusal.route(), OwnerRoute::ClosureBytesCorrupt);
                assert!(matches!(refusal, FactoryRefusal::Recheck(RecheckFailure::Corrupt(actual)) if actual == expected));
            }
        });
    }
}

struct Boundary<'a, R> {
    inner: R,
    first: &'a Cell<Option<usize>>,
}
impl<R: LaunchRecheck> LaunchRecheck for Boundary<'_, R> {
    fn recheck(
        &mut self,
        name: &str,
        work: &mut WorkScope<'_>,
    ) -> Result<RecheckedMember, RecheckFailure> {
        if self.first.get().is_none() {
            self.first.set(Some(work.used().edges));
        }
        self.inner.recheck(name, work)
    }
}

#[test]
fn actual_factory_one_short_native_open_and_read_keep_budget_route() {
    // Observe the CPU assembly boundary only to place the deliberately
    // restrictive test budget. This is not a price oracle or sourced profile.
    // The independent native prefixes are two binding comparisons + one kind
    // comparison + one row lookup, then openat/fstat, then the first read.
    for native_prefix in [4, 6] {
        let fixture = Fixture::new();
        let root = fixture.tree_path();
        let provider = root.join("provider");
        let bindings = bindings();
        let selection = selected(&fixture);
        let hash = digest_hex(&raw_sha256(DATA));
        let members = members(&provider, &root, &hash);
        let (codec, identity, caps) = wire_fixture::rust();
        let authority = Authorities {
            selection: &selection,
            capabilities: &caps,
            entrypoint: "entrypoint",
            members: &members,
            identity: IdentityAuthority::Rust {
                expected_identity: &identity,
            },
        };
        fixture.opened(|trees| {
            let first = Cell::new(None);
            let mut ledger = WorkLedger::snapshot_profile();
            ledger
                .scope(|work| {
                    let inner =
                        Rechecker::new(trees, &bindings, &launch(&provider, &root), work).unwrap();
                    let mut observer = Boundary {
                        inner,
                        first: &first,
                    };
                    factory::prepare(
                        selection.clone(),
                        codec,
                        launch(&provider, &root),
                        1 << 30,
                        &authority,
                        &mut observer,
                        work,
                    )
                    .map_err(WorkFailure::Operation)
                })
                .unwrap();
            let limit = first.get().unwrap() + native_prefix;
            let (codec, _, _) = wire_fixture::rust();
            let mut short = WorkLedger::with_limits(WorkCost {
                objects: 65536,
                edges: limit,
                bytes: 1 << 26,
            })
            .unwrap();
            let guard = read_fixture::fail_next_read();
            let result = short.scope(|work| {
                prepare_session(
                    SessionInput {
                        selection: selection.clone(),
                        provider: codec,
                        launch: launch(&provider, &root),
                        memory_budget_bytes: 1 << 30,
                    },
                    trees,
                    &bindings,
                    &authority,
                    work,
                )
                .map_err(WorkFailure::Operation)
            });
            assert!(matches!(
                result,
                Err(WorkFailure::Operation(FactoryRefusal::Budget(
                    WorkBudgetError::Edges
                )))
            ));
            assert_eq!(short.used().edges, limit);
            assert!(!guard.was_triggered());
        });
    }
}

/// The lane builds the registered harness-free first-party target, pins its
/// bytes, then writes this sidecar beside the host test executable. This
/// cannot point to a repository member or unpinned executable silently.
fn compiled_factory_peer() -> (Vec<u8>, PathBuf) {
    let path = std::env::current_exe()
        .unwrap()
        .parent()
        .unwrap()
        .join("factory_fixture.json");
    let record: serde_json::Value = serde_json::from_slice(
        &fs::read(path).expect("lane must build and pin factory_fixture first"),
    )
    .unwrap();
    let binary = Path::new(record["path"].as_str().unwrap());
    let bytes = fs::read(binary).unwrap();
    assert_eq!(
        digest_hex(&raw_sha256(&bytes)),
        record["sha256"].as_str().unwrap()
    );
    (
        bytes,
        PathBuf::from(record["evidenceDirectory"].as_str().unwrap()),
    )
}

#[test]
fn actual_factory_spawned_peer_substitutions_refuse_before_source_or_analyze() {
    use opensip_components::provider_protocol::{
        rust3::Rust3Participant,
        table::{Protocol, Table},
    };
    use opensip_components::{
        control_protocol::RefusalFamily as RF,
        supervisor::{
            Cause, Limits, Supervision,
            records::{OwnerRoute, settlement_route},
        },
    };
    let (binary, evidence) = compiled_factory_peer();
    for (mode, expected) in [
        ("stable", Cause::ControlRefusal(RF::Rf3)),
        ("manifest", Cause::ControlRefusal(RF::Rf3)),
        ("tuple", Cause::ControlRefusal(RF::Rf4)),
        ("effect", Cause::ControlRefusal(RF::Rf6)),
        ("identity", Cause::ProviderProtocol),
        ("tokens", Cause::ProviderProtocol),
        ("baseline", Cause::ProviderProtocol),
    ] {
        let fixture = Fixture::with_provider(&binary, mode);
        let root = fixture.tree_path();
        let provider = root.join("provider");
        let bindings = bindings();
        let selection = selected(&fixture);
        let hash = digest_hex(&raw_sha256(&binary));
        let members = members(&provider, &root, &hash);
        let (codec, identity, caps) = wire_fixture::rust();
        let authority = Authorities {
            selection: &selection,
            capabilities: &caps,
            entrypoint: "entrypoint",
            members: &members,
            identity: IdentityAuthority::Rust {
                expected_identity: &identity,
            },
        };
        fixture.opened(|trees| {
            let prepared = WorkLedger::snapshot_profile()
                .scope(|work| {
                    prepare_session(
                        SessionInput {
                            selection: selection.clone(),
                            provider: codec,
                            launch: launch(&provider, &root),
                            memory_budget_bytes: Limits::RELEASE.resident_memory,
                        },
                        trees,
                        &bindings,
                        &authority,
                        work,
                    )
                    .map_err(WorkFailure::Operation)
                })
                .unwrap();
            assert_eq!(prepared.session.launch.spec().executable(), provider);
            let Provider::Rust { sender } = prepared.provider else {
                panic!("Rust peer")
            };
            let table = Table::load(Protocol::Rust3).unwrap();
            let reads = Rc::new(Cell::new(0));
            let participant =
                Rust3Participant::from_sender(&table, sender, Box::new(NoSource(reads.clone())))
                    .unwrap();
            let mut session = prepared.session;
            assert_eq!(
                session.launch.spec().class(),
                opensip_platform::LaunchClass::Provider
            );
            session.launch = session.launch.into_test_fixture();
            assert_eq!(
                session.launch.spec().class(),
                opensip_platform::LaunchClass::TestFixture
            );
            let mut supervision = Supervision::prepare(session, participant).unwrap();
            let mut scratch =
                opensip_platform::ScratchRoot::create_in(File::open(&fixture.root).unwrap().into())
                    .unwrap();
            // The operation's trees remain borrowed and alive until the
            // actual child has been supervised through its settlement.
            supervision.run(&mut scratch).unwrap();
            let settlement = supervision.take_settlement().unwrap();
            let observed: serde_json::Value = serde_json::from_slice(
                &fs::read(fixture.root.join("peer-observation.json"))
                    .expect("actual child observation"),
            )
            .unwrap();
            fs::write(
                evidence.join(format!("{mode}.json")),
                serde_json::to_vec_pretty(&serde_json::json!({
                    "mode":mode, "firstCause":format!("{:?}",settlement.first_cause()),
                    "ownerRoute":format!("{:?}",settlement_route(&settlement)),
                    "sourceReads":reads.get(), "peer":observed,
                }))
                .unwrap(),
            )
            .unwrap();
            assert_eq!(settlement.first_cause(), expected, "{mode}: {settlement:?}");
            assert_eq!(
                settlement_route(&settlement),
                OwnerRoute::ProviderProtocol,
                "{mode}"
            );
            assert_eq!(
                reads.get(),
                0,
                "{mode}: immutable Source must never be consulted"
            );
            assert_eq!(observed["sourceBytes"], 0, "{mode}: {observed}");
            assert_eq!(observed["analyze"], 0, "{mode}: {observed}");
            let frames = observed["providerReceived"].as_array().unwrap();
            assert!(
                frames.iter().all(|name| {
                    let name = name.as_str().unwrap();
                    !name.starts_with("Snapshot")
                        && !name.starts_with("DependencySource")
                        && name != "Analyze"
                }),
                "{mode}: {observed}"
            );
            assert!(
                observed["controlSent"]
                    .as_array()
                    .unwrap()
                    .contains(&serde_json::json!("helloAck")),
                "{mode}: {observed}"
            );
            if matches!(mode, "identity" | "tokens" | "baseline") {
                use opensip_components::provider_protocol::{
                    cbor::{Profile, Value},
                    read_frame,
                };
                assert!(frames.contains(&serde_json::json!("Hello")));
                let replies = observed["providerSent"].as_array().unwrap();
                assert_eq!(
                    replies.len(),
                    1,
                    "{mode}: a positive flushed HelloAck witness is required"
                );
                let hex = replies[0]["wireHex"].as_str().unwrap();
                let bytes: Vec<u8> = (0..hex.len())
                    .step_by(2)
                    .map(|i| u8::from_str_radix(&hex[i..i + 2], 16).unwrap())
                    .collect();
                let reply = read_frame(&mut bytes.as_slice(), Profile::Rust3, 32, None)
                    .unwrap()
                    .unwrap();
                fn field<'a>(value: &'a Value, key: &str) -> &'a Value {
                    let Value::Map(rows) = value else {
                        panic!("map")
                    };
                    &rows.iter().find(|(name, _)| name == key).unwrap().1
                }
                assert_eq!(
                    field(reply.value(), "frameType"),
                    &Value::Text("HelloAck".into())
                );
                let payload = field(reply.value(), "payload");
                if mode == "identity" {
                    assert_eq!(
                        field(payload, "providerBuildId"),
                        &Value::Text("wrong-provider".into())
                    );
                }
                if mode == "tokens" {
                    assert_eq!(field(payload, "capabilities"), &Value::Array(vec![]));
                }
                assert_eq!(
                    frames.contains(&serde_json::json!("OpenUniverse")),
                    mode == "baseline",
                    "{mode}: unmodified Ack alone must unlock the next metadata frame"
                );
            }
        });
    }
}

impl opensip_components::provider_protocol::ts2::SnapshotSource for NoSource {
    fn read(&mut self, _: &str, _: u64, _: usize) -> std::io::Result<Vec<u8>> {
        self.0.set(self.0.get() + 1);
        Err(std::io::Error::other(
            "source disclosure before acknowledgment",
        ))
    }
}

#[test]
fn actual_ts2_factory_spawned_peer_substitutions_refuse_before_source_or_analyze() {
    use opensip_components::provider_protocol::{
        table::{Protocol, Table},
        ts2::Ts2Participant,
    };
    use opensip_components::{
        control_protocol::RefusalFamily as RF,
        supervisor::{
            Cause, Limits, Supervision,
            records::{OwnerRoute, settlement_route},
        },
    };
    let (binary, evidence) = compiled_factory_peer();
    for (mode, expected) in [
        ("stable", Cause::ControlRefusal(RF::Rf3)),
        ("manifest", Cause::ControlRefusal(RF::Rf3)),
        ("tuple", Cause::ControlRefusal(RF::Rf4)),
        ("effect", Cause::ControlRefusal(RF::Rf6)),
        ("identity", Cause::ProviderProtocol),
        ("tokens", Cause::ProviderProtocol),
        ("providerdigest", Cause::ProviderProtocol),
        ("runtimedigest", Cause::ProviderProtocol),
        ("baseline", Cause::ProviderProtocol),
    ] {
        const JS: &[u8] = b"// first-party inert D4 provider fixture\n";
        let fixture = Fixture::with_files(JS, Some(&binary), mode);
        let root = fixture.tree_path();
        let provider = root.join("provider");
        let node = root.join("node");
        let config = root.join("openssl.cnf");
        let bindings = [
            Binding {
                name: "entrypoint",
                tree: 0,
                request: MemberRequest::Entrypoint,
            },
            Binding {
                name: "node",
                tree: 0,
                request: MemberRequest::File("node"),
            },
            Binding {
                name: "openssl",
                tree: 0,
                request: MemberRequest::File("openssl.cnf"),
            },
            Binding {
                name: "provider",
                tree: 0,
                request: MemberRequest::File("provider"),
            },
        ];
        let mut selection = selected(&fixture);
        selection.tuple.role_subprotocol = "typescript-semantic".into();
        selection.tuple.subprotocol_version = 2;
        let js_hash = digest_hex(&raw_sha256(JS));
        let node_hash = digest_hex(&raw_sha256(&binary));
        let config_hash = digest_hex(&raw_sha256(b""));
        let members = [
            MemberAuthority {
                member: NamedMember {
                    name: "entrypoint",
                    launch_path: &provider,
                },
                kind: MemberKind::File,
                closure_member: "provider",
                file_sha256: Some(&js_hash),
            },
            MemberAuthority {
                member: NamedMember {
                    name: "node",
                    launch_path: &node,
                },
                kind: MemberKind::File,
                closure_member: "node",
                file_sha256: Some(&node_hash),
            },
            MemberAuthority {
                member: NamedMember {
                    name: "openssl",
                    launch_path: &config,
                },
                kind: MemberKind::File,
                closure_member: "openssl.cnf",
                file_sha256: Some(&config_hash),
            },
            MemberAuthority {
                member: NamedMember {
                    name: "provider",
                    launch_path: &provider,
                },
                kind: MemberKind::File,
                closure_member: "provider",
                file_sha256: Some(&js_hash),
            },
        ];
        let input = ts2_fixture::typescript();
        let authority = Authorities {
            selection: &selection,
            capabilities: &input.capabilities,
            entrypoint: "entrypoint",
            members: &members,
            identity: IdentityAuthority::TypeScript {
                provider_sha256: &input.provider_digest,
                runtime_sha256: &input.runtime_digest,
                provider_fields: &input.provider_fields,
                runtime_fields: &input.runtime_fields,
            },
        };
        fixture.opened(|trees| {
            let prepared = WorkLedger::snapshot_profile()
                .scope(|work| {
                    prepare_session(
                        SessionInput {
                            selection: selection.clone(),
                            provider: input.provider,
                            launch: Launch::TypeScript {
                                entrypoint: NamedMember {
                                    name: "entrypoint",
                                    launch_path: &provider,
                                },
                                node: NamedMember {
                                    name: "node",
                                    launch_path: &node,
                                },
                                openssl_config: NamedMember {
                                    name: "openssl",
                                    launch_path: &config,
                                },
                                provider: NamedMember {
                                    name: "provider",
                                    launch_path: &provider,
                                },
                                broker_context: "D4-first-party-fixture",
                            },
                            memory_budget_bytes: Limits::RELEASE.resident_memory,
                        },
                        trees,
                        &bindings,
                        &authority,
                        work,
                    )
                    .map_err(WorkFailure::Operation)
                })
                .unwrap();
            assert_eq!(prepared.session.launch.spec().executable(), node);
            assert_eq!(prepared.session.launch.recheck().sha256, node_hash);
            let Provider::TypeScript { sender, context } = prepared.provider else {
                panic!("TS2 peer")
            };
            let table = Table::load(Protocol::Ts2).unwrap();
            let reads = Rc::new(Cell::new(0));
            let participant = Ts2Participant::from_sender(
                &table,
                context,
                sender,
                Box::new(NoSource(reads.clone())),
            )
            .unwrap();
            let mut session = prepared.session;
            assert_eq!(
                session.launch.spec().class(),
                opensip_platform::LaunchClass::Provider
            );
            session.launch = session.launch.into_test_fixture();
            assert_eq!(
                session.launch.spec().class(),
                opensip_platform::LaunchClass::TestFixture
            );
            let mut supervision = Supervision::prepare(session, participant).unwrap();
            let mut scratch =
                opensip_platform::ScratchRoot::create_in(File::open(&fixture.root).unwrap().into())
                    .unwrap();
            // The operation's trees remain borrowed and alive until the
            // actual child has been supervised through its settlement.
            supervision.run(&mut scratch).unwrap();
            let settlement = supervision.take_settlement().unwrap();
            let observed: serde_json::Value = serde_json::from_slice(
                &fs::read(fixture.root.join("peer-observation.json"))
                    .expect("actual child observation"),
            )
            .unwrap();
            fs::write(
                evidence.join(format!("ts2-{mode}.json")),
                serde_json::to_vec_pretty(&serde_json::json!({
                    "mode":mode, "firstCause":format!("{:?}",settlement.first_cause()),
                    "ownerRoute":format!("{:?}",settlement_route(&settlement)),
                    "sourceReads":reads.get(), "peer":observed,
                }))
                .unwrap(),
            )
            .unwrap();
            assert_eq!(settlement.first_cause(), expected, "{mode}: {settlement:?}");
            assert_eq!(
                settlement_route(&settlement),
                OwnerRoute::ProviderProtocol,
                "{mode}"
            );
            assert_eq!(
                reads.get(),
                0,
                "{mode}: immutable Source must never be consulted"
            );
            assert_eq!(observed["sourceBytes"], 0, "{mode}: {observed}");
            assert_eq!(observed["analyze"], 0, "{mode}: {observed}");
            let frames = observed["providerReceived"].as_array().unwrap();
            assert!(
                frames.iter().all(|name| {
                    let name = name.as_str().unwrap();
                    !name.starts_with("Snapshot")
                        && !name.starts_with("DependencySource")
                        && name != "Analyze"
                }),
                "{mode}: {observed}"
            );
            assert!(
                observed["controlSent"]
                    .as_array()
                    .unwrap()
                    .contains(&serde_json::json!("helloAck")),
                "{mode}: {observed}"
            );
            if matches!(
                mode,
                "identity" | "tokens" | "baseline" | "providerdigest" | "runtimedigest"
            ) {
                use opensip_components::provider_protocol::{
                    cbor::{Profile, Value},
                    read_frame,
                };
                assert!(frames.contains(&serde_json::json!("Hello")));
                let replies = observed["providerSent"].as_array().unwrap();
                assert_eq!(
                    replies.len(),
                    1,
                    "{mode}: a positive flushed HelloAck witness is required"
                );
                let hex = replies[0]["wireHex"].as_str().unwrap();
                let bytes: Vec<u8> = (0..hex.len())
                    .step_by(2)
                    .map(|i| u8::from_str_radix(&hex[i..i + 2], 16).unwrap())
                    .collect();
                let reply = read_frame(&mut bytes.as_slice(), Profile::Ts2, 32, None)
                    .unwrap()
                    .unwrap();
                fn field<'a>(value: &'a Value, key: &str) -> &'a Value {
                    let Value::Map(rows) = value else {
                        panic!("map")
                    };
                    &rows.iter().find(|(name, _)| name == key).unwrap().1
                }
                assert_eq!(
                    field(reply.value(), "frameType"),
                    &Value::Text("HelloAck".into())
                );
                let payload = field(reply.value(), "payload");
                if mode == "identity" {
                    assert_eq!(
                        field(payload, "providerBuildId"),
                        &Value::Text("wrong-provider".into())
                    );
                }
                if mode == "tokens" {
                    assert_eq!(field(payload, "capabilities"), &Value::Array(vec![]));
                }
                if mode == "providerdigest" {
                    assert_eq!(
                        field(payload, "providerDescriptorSha256"),
                        &Value::Text("0".repeat(64))
                    );
                }
                if mode == "runtimedigest" {
                    assert_eq!(
                        field(payload, "runtimeDescriptorSha256"),
                        &Value::Text("0".repeat(64))
                    );
                }
                assert_eq!(
                    frames.contains(&serde_json::json!("OpenUniverse")),
                    mode == "baseline",
                    "{mode}: unmodified Ack alone must unlock the next metadata frame"
                );
            }
        });
    }
}

#[test]
fn actual_ts2_factory_rechecks_each_distinct_native_file_before_launch() {
    let (binary, _) = compiled_factory_peer();
    for target in ["node", "openssl.cnf", "provider"] {
        const JS: &[u8] = b"// first-party inert D4 provider fixture\n";
        let fixture = Fixture::with_files(JS, Some(&binary), "adapter");
        let root = fixture.tree_path();
        let provider = root.join("provider");
        let node = root.join("node");
        let config = root.join("openssl.cnf");
        let bindings = [
            Binding {
                name: "entrypoint",
                tree: 0,
                request: MemberRequest::Entrypoint,
            },
            Binding {
                name: "node",
                tree: 0,
                request: MemberRequest::File("node"),
            },
            Binding {
                name: "openssl",
                tree: 0,
                request: MemberRequest::File("openssl.cnf"),
            },
            Binding {
                name: "provider",
                tree: 0,
                request: MemberRequest::File("provider"),
            },
        ];
        let mut selection = selected(&fixture);
        selection.tuple.role_subprotocol = "typescript-semantic".into();
        selection.tuple.subprotocol_version = 2;
        let js_hash = digest_hex(&raw_sha256(JS));
        let node_hash = digest_hex(&raw_sha256(&binary));
        let config_hash = digest_hex(&raw_sha256(b""));
        let members = [
            MemberAuthority {
                member: NamedMember {
                    name: "entrypoint",
                    launch_path: &provider,
                },
                kind: MemberKind::File,
                closure_member: "provider",
                file_sha256: Some(&js_hash),
            },
            MemberAuthority {
                member: NamedMember {
                    name: "node",
                    launch_path: &node,
                },
                kind: MemberKind::File,
                closure_member: "node",
                file_sha256: Some(&node_hash),
            },
            MemberAuthority {
                member: NamedMember {
                    name: "openssl",
                    launch_path: &config,
                },
                kind: MemberKind::File,
                closure_member: "openssl.cnf",
                file_sha256: Some(&config_hash),
            },
            MemberAuthority {
                member: NamedMember {
                    name: "provider",
                    launch_path: &provider,
                },
                kind: MemberKind::File,
                closure_member: "provider",
                file_sha256: Some(&js_hash),
            },
        ];
        let input = ts2_fixture::typescript();
        let authority = Authorities {
            selection: &selection,
            capabilities: &input.capabilities,
            entrypoint: "entrypoint",
            members: &members,
            identity: IdentityAuthority::TypeScript {
                provider_sha256: &input.provider_digest,
                runtime_sha256: &input.runtime_digest,
                provider_fields: &input.provider_fields,
                runtime_fields: &input.runtime_fields,
            },
        };
        fixture.opened(|trees| {
            fixture.change(|_| {
                let path=root.join(target);
                let original=fs::metadata(&path).unwrap().mode() & 0o777;
                fs::set_permissions(&path,fs::Permissions::from_mode(0o600)).unwrap();
                let mut bytes=fs::read(&path).unwrap();
                if bytes.is_empty(){bytes.push(1)}else{bytes[0]^=1;}
                fs::write(&path,bytes).unwrap();
                fs::set_permissions(&path,fs::Permissions::from_mode(original)).unwrap();
            });
            let result=WorkLedger::snapshot_profile().scope(|work|{
                prepare_session(SessionInput{
                    selection:selection.clone(),provider:input.provider,
                    launch:Launch::TypeScript{entrypoint:NamedMember{name:"entrypoint",launch_path:&provider},node:NamedMember{name:"node",launch_path:&node},openssl_config:NamedMember{name:"openssl",launch_path:&config},provider:NamedMember{name:"provider",launch_path:&provider},broker_context:"D4-first-party-fixture"},
                    memory_budget_bytes:1<<30,
                },trees,&bindings,&authority,work).map_err(WorkFailure::Operation)
            });
            let refusal=match result{Err(WorkFailure::Operation(error))=>error,_=>panic!("{target}: a changed member must refuse before any launch escapes")};
            let expected=if target=="openssl.cnf"{CorruptCause::Length}else{CorruptCause::Digest};
            assert_eq!(refusal.route(),opensip_components::supervisor::records::OwnerRoute::ClosureBytesCorrupt);
            assert!(matches!(refusal,FactoryRefusal::Recheck(RecheckFailure::Corrupt(actual))if actual==expected),"{target}");
            assert!(!fixture.root.join("peer-observation.json").exists());
        });
    }
}

#[test]
fn actual_native_factory_requires_cms_entrypoint_operation_before_reads() {
    for request in [
        MemberRequest::File("provider"),
        MemberRequest::File("entrypoint"),
        MemberRequest::Directory(""),
    ] {
        let fixture = Fixture::new();
        let root = fixture.tree_path();
        let provider = root.join("provider");
        let mut bindings = bindings();
        let selection = selected(&fixture);
        let hash = digest_hex(&raw_sha256(DATA));
        let members = members(&provider, &root, &hash);
        let (codec, identity, caps) = wire_fixture::rust();
        let authority = Authorities {
            selection: &selection,
            capabilities: &caps,
            entrypoint: "entrypoint",
            members: &members,
            identity: IdentityAuthority::Rust {
                expected_identity: &identity,
            },
        };

        bindings
            .iter_mut()
            .find(|row| row.name == "entrypoint")
            .unwrap()
            .request = request;
        fixture.opened(|trees| {
            let guard = read_fixture::fail_next_read();
            let result = WorkLedger::snapshot_profile().scope(|work| {
                prepare_session(
                    SessionInput {
                        selection: selection.clone(),
                        provider: codec,
                        launch: launch(&provider, &root),
                        memory_budget_bytes: 1 << 30,
                    },
                    trees,
                    &bindings,
                    &authority,
                    work,
                )
                .map_err(WorkFailure::Operation)
            });
            assert!(matches!(
                result,
                Err(WorkFailure::Operation(FactoryRefusal::SpecInconsistent(
                    "launch-binding-entrypoint"
                )))
            ));
            assert!(
                !guard.was_triggered(),
                "generic-file substitution must fail before any physical read"
            );
            assert!(!fixture.root.join("peer-observation.json").exists());
        });
    }
}
