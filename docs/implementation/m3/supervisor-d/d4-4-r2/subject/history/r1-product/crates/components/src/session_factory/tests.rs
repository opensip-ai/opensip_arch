//! Explicit synthetic pre-C4 factory controls. Native CI-A3 and actual
//! provider-spoken composition are separate controls, not inferred here.
use super::*;
use crate::control_protocol::{Platform, SubprotocolTuple};
use opensip_platform::{WorkBudgetError, WorkLedger};
use std::{cell::Cell, rc::Rc};

struct NoSource(Rc<Cell<usize>>);
impl crate::provider_protocol::rust3::Rust3Source for NoSource {
    fn read(
        &mut self,
        _: &crate::provider_protocol::rust3::Rust3SourceEntry,
        _: u64,
        _: usize,
    ) -> io::Result<Vec<u8>> {
        self.0.set(self.0.get() + 1);
        Err(io::Error::other("source disclosure before acknowledgment"))
    }
}
impl crate::provider_protocol::ts2::SnapshotSource for NoSource {
    fn read(&mut self, _: &str, _: u64, _: usize) -> io::Result<Vec<u8>> {
        self.0.set(self.0.get() + 1);
        Err(io::Error::other("source disclosure before acknowledgment"))
    }
}

const HASH: &str = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
fn named(name: &'static str, path: &'static str) -> NamedMember<'static> {
    NamedMember {
        name,
        launch_path: Path::new(path),
    }
}
fn selection(version: i64) -> AdmittedSelection {
    AdmittedSelection {
        stable_id: "synthetic-admitted-provider".into(),
        manifest_digest: HASH.into(),
        platform: Platform {
            os: "macos".into(),
            arch: "aarch64".into(),
        },
        tuple: SubprotocolTuple {
            role: "analyzer".into(),
            role_subprotocol: if version == 3 {
                "rust-semantic"
            } else {
                "typescript-semantic"
            }
            .into(),
            subprotocol_version: version,
        },
    }
}
fn row(
    name: &'static str,
    path: &'static str,
    relative: &'static str,
    kind: MemberKind,
) -> MemberAuthority<'static> {
    MemberAuthority {
        member: named(name, path),
        kind,
        closure_member: relative,
        file_sha256: if kind == MemberKind::File {
            Some(HASH)
        } else {
            None
        },
    }
}
struct Fake<'a> {
    members: &'a [MemberAuthority<'static>],
    calls: Vec<String>,
    failure: Option<RecheckFailure>,
    wrong_path: bool,
}
impl LaunchRecheck for Fake<'_> {
    fn recheck(
        &mut self,
        name: &str,
        work: &mut WorkScope<'_>,
    ) -> Result<RecheckedMember, RecheckFailure> {
        self.calls.push(name.to_owned());
        if let Some(error) = self.failure.take() {
            return Err(error);
        }
        work.charge::<()>(WorkCost {
            objects: 0,
            edges: 1,
            bytes: 0,
        })
        .map_err(|error| match error {
            WorkFailure::Budget(budget) => RecheckFailure::Budget(budget),
            WorkFailure::Operation(()) => unreachable!(),
        })?;
        let member = self
            .members
            .iter()
            .find(|row| row.member.name == name)
            .unwrap();
        Ok(RecheckedMember {
            launch_path: if self.wrong_path {
                PathBuf::from("/different-member")
            } else {
                member.member.launch_path.to_path_buf()
            },
            closure_recheck: member.file_sha256.map(|hash| ClosureRecheck {
                member: member.closure_member.into(),
                device: 17,
                inode: 19,
                sha256: hash.into(),
            }),
        })
    }
}
#[derive(Clone, Copy)]
enum Change {
    None,
    Stable,
    Manifest,
    Tuple,
    Identity,
    Limit,
    Capabilities,
    MissingMember,
    MemberPath,
    BoundPath,
    RealizedHello,
}

fn rust_case(
    mask: u8,
    change: Change,
    failure: Option<RecheckFailure>,
) -> (Result<PreparedSession, FactoryRefusal>, Vec<String>, bool) {
    let (mut sender, mut identity, mut caps) =
        crate::provider_protocol::rust3::factory_fixture_for_test(mask);
    let expected = selection(3);
    let mut actual = expected.clone();
    let mut members = [
        row(
            "entrypoint",
            "/s/provider",
            "bin/provider",
            MemberKind::File,
        ),
        row("provider", "/s/provider", "bin/provider", MemberKind::File),
        row("toolchain", "/s/toolchain", "", MemberKind::Directory),
    ];
    match change {
        Change::RealizedHello => {
            sender
                .realize_next(&mut NoSource(Rc::new(Cell::new(0))))
                .unwrap();
            assert!(!sender.hello_sent());
        }
        Change::Stable => actual.stable_id.push('x'),
        Change::Manifest => actual.manifest_digest = "b".repeat(64),
        Change::Tuple => actual.tuple.subprotocol_version = 2,
        Change::Identity => {
            let Value::Map(fields) = &mut identity else {
                panic!()
            };
            let (_, value) = fields
                .iter_mut()
                .find(|(_, value)| matches!(value, Value::Text(_)))
                .unwrap();
            let Value::Text(value) = value else { panic!() };
            value.push('x');
        }
        Change::Limit => {
            let Value::Map(hello) = sender.factory_hello_mut_for_test().unwrap() else {
                panic!()
            };
            let (_, Value::Map(limits)) =
                hello.iter_mut().find(|(key, _)| key == "limits").unwrap()
            else {
                panic!()
            };
            limits[0].1 = Value::Unsigned(1);
        }
        Change::Capabilities => caps.push("invented-signed-token".into()),
        Change::MemberPath => members[1].member.launch_path = Path::new("/not-selected"),
        _ => {}
    }
    let authorities = Authorities {
        selection: &expected,
        capabilities: &caps,
        entrypoint: "entrypoint",
        members: if matches!(change, Change::MissingMember) {
            &members[..2]
        } else {
            &members
        },
        identity: IdentityAuthority::Rust {
            expected_identity: &identity,
        },
    };
    let mut fake = Fake {
        members: &members,
        calls: Vec::new(),
        failure,
        wrong_path: matches!(change, Change::BoundPath),
    };
    let mut ledger = WorkLedger::new();
    let result = ledger.scope(|work| {
        prepare(
            actual,
            Provider::Rust { sender },
            Launch::Rust {
                entrypoint: named("entrypoint", "/s/provider"),
                provider: named("provider", "/s/provider"),
                toolchain_root: named("toolchain", "/s/toolchain"),
            },
            1 << 30,
            &authorities,
            &mut fake,
            work,
        )
        .map_err(WorkFailure::Operation)
    });
    let result = result.map_err(|error| match error {
        WorkFailure::Operation(error) => error,
        WorkFailure::Budget(error) => FactoryRefusal::Budget(error),
    });
    (result, fake.calls, ledger.is_failed())
}

#[test]
fn all_eight_rust_profiles_validate_before_all_named_final_rechecks() {
    for mask in 0..8 {
        let (result, calls, failed) = rust_case(mask, Change::None, None);
        let prepared = result.unwrap_or_else(|error| panic!("mask{mask}: {error:?}"));
        assert_eq!(calls, ["entrypoint", "provider", "toolchain"]);
        assert!(!failed);
        assert_eq!(
            prepared.session.launch.spec().executable(),
            Path::new("/s/provider")
        );
        assert_eq!(prepared.session.launch.recheck().sha256, HASH);
        assert_eq!(
            prepared.control.policy().stable_id(),
            selection(3).stable_id
        );
        let Provider::Rust { sender } = prepared.provider else {
            panic!()
        };
        assert!(!sender.hello_sent());
        let table = crate::provider_protocol::table::Table::load(
            crate::provider_protocol::table::Protocol::Rust3,
        )
        .unwrap();
        let reads = Rc::new(Cell::new(0));
        assert!(
            crate::provider_protocol::rust3::Rust3Participant::from_sender(
                &table,
                sender,
                Box::new(NoSource(reads.clone()))
            )
            .is_ok()
        );
        assert_eq!(reads.get(), 0);
    }
}

#[test]
fn each_independent_spec_or_membership_difference_refuses_before_recheck() {
    for change in [
        Change::Stable,
        Change::Manifest,
        Change::Tuple,
        Change::Identity,
        Change::Limit,
        Change::Capabilities,
        Change::MissingMember,
        Change::MemberPath,
        Change::RealizedHello,
    ] {
        let (result, calls, failed) = rust_case(7, change, None);
        let Err(FactoryRefusal::SpecInconsistent(_)) = result else {
            panic!("not a spec refusal")
        };
        assert!(calls.is_empty());
        assert!(failed);
    }
}

#[test]
fn recheck_budget_io_and_each_corruption_keep_their_own_route_and_cause() {
    for cause in [
        CorruptCause::Absent,
        CorruptCause::Type,
        CorruptCause::Mode,
        CorruptCause::Length,
        CorruptCause::Digest,
        CorruptCause::LinkTarget,
        CorruptCause::Association,
        CorruptCause::Binding,
    ] {
        let (result, calls, failed) =
            rust_case(0, Change::None, Some(RecheckFailure::Corrupt(cause)));
        let Err(error) = result else { panic!() };
        assert_eq!(error.route(), OwnerRoute::ClosureBytesCorrupt);
        assert!(
            matches!(error, FactoryRefusal::Recheck(RecheckFailure::Corrupt(actual)) if actual == cause)
        );
        assert_eq!(calls, ["entrypoint"]);
        assert!(failed);
    }
    let (result, _, _) = rust_case(
        0,
        Change::None,
        Some(RecheckFailure::Budget(WorkBudgetError::Edges)),
    );
    let Err(error) = result else { panic!() };
    assert_eq!(error.route(), OwnerRoute::HostInvariant);
    assert!(matches!(
        error,
        FactoryRefusal::Budget(WorkBudgetError::Edges)
    ));
    let (result, _, _) = rust_case(
        0,
        Change::None,
        Some(RecheckFailure::Io {
            call: "read",
            error: io::Error::from_raw_os_error(5),
        }),
    );
    let Err(error) = result else { panic!() };
    assert_eq!(error.route(), OwnerRoute::HostIo);
    assert!(
        matches!(error, FactoryRefusal::Recheck(RecheckFailure::Io { call: "read", error }) if error.raw_os_error() == Some(5))
    );
}

#[test]
fn returned_binding_difference_cannot_produce_a_verified_launch() {
    let (result, calls, failed) = rust_case(0, Change::BoundPath, None);
    assert!(matches!(
        result,
        Err(FactoryRefusal::SpecInconsistent("rechecked-launch-path"))
    ));
    assert_eq!(calls, ["entrypoint"]);
    assert!(failed);
}

#[test]
fn typescript_checks_verified_descriptor_fields_and_digests_before_rechecks() {
    for corrupt in 0..6 {
        let (mut sender, mut context) = crate::provider_protocol::ts2::factory_fixture_for_test();
        let (_, authority) = crate::provider_protocol::ts2::factory_fixture_for_test();
        match corrupt {
            5 => {
                sender
                    .realize_next(&mut NoSource(Rc::new(Cell::new(0))))
                    .unwrap();
                assert!(!sender.hello_sent());
            }
            1 => context.expected_provider_descriptor_sha256 = "b".repeat(64),
            2 => context.expected_runtime_descriptor_sha256 = "b".repeat(64),
            3 => {
                let field = context.provider_descriptor.values_mut().next().unwrap();
                *field = Value::Null;
            }
            4 => {
                let field = context.runtime_descriptor.values_mut().next().unwrap();
                *field = Value::Null;
            }
            _ => {}
        }
        let expected = selection(2);
        let members = [
            row("config", "/s/empty.cnf", "empty.cnf", MemberKind::File),
            row(
                "entrypoint",
                "/s/provider.js",
                "provider.js",
                MemberKind::File,
            ),
            row("node", "/s/node", "node", MemberKind::File),
            row(
                "provider",
                "/s/provider.js",
                "provider.js",
                MemberKind::File,
            ),
        ];
        let authorities = Authorities {
            selection: &expected,
            capabilities: &authority.capabilities,
            entrypoint: "entrypoint",
            members: &members,
            identity: IdentityAuthority::TypeScript {
                provider_sha256: &authority.expected_provider_descriptor_sha256,
                runtime_sha256: &authority.expected_runtime_descriptor_sha256,
                provider_fields: &authority.provider_descriptor,
                runtime_fields: &authority.runtime_descriptor,
            },
        };
        let mut fake = Fake {
            members: &members,
            calls: Vec::new(),
            failure: None,
            wrong_path: false,
        };
        let mut ledger = WorkLedger::new();
        let result = ledger.scope(|work| {
            prepare(
                expected.clone(),
                Provider::TypeScript { sender, context },
                Launch::TypeScript {
                    entrypoint: named("entrypoint", "/s/provider.js"),
                    node: named("node", "/s/node"),
                    openssl_config: named("config", "/s/empty.cnf"),
                    provider: named("provider", "/s/provider.js"),
                    broker_context: "{}",
                },
                1 << 30,
                &authorities,
                &mut fake,
                work,
            )
            .map_err(WorkFailure::Operation)
        });
        if corrupt == 0 {
            let Ok(prepared) = result else {
                panic!("valid TS2 factory refused")
            };
            assert_eq!(fake.calls, ["entrypoint", "node", "config", "provider"]);
            let Provider::TypeScript { sender, context } = prepared.provider else {
                panic!()
            };
            let table = crate::provider_protocol::table::Table::load(
                crate::provider_protocol::table::Protocol::Ts2,
            )
            .unwrap();
            let reads = Rc::new(Cell::new(0));
            assert!(
                crate::provider_protocol::ts2::Ts2Participant::from_sender(
                    &table,
                    context,
                    sender,
                    Box::new(NoSource(reads.clone()))
                )
                .is_ok()
            );
            assert_eq!(reads.get(), 0);
        } else {
            assert!(matches!(
                result,
                Err(WorkFailure::Operation(FactoryRefusal::SpecInconsistent(_)))
            ));
            assert!(fake.calls.is_empty());
        }
    }
}

#[test]
fn participants_refuse_a_realized_unsent_hello_without_reading_source() {
    let reads = Rc::new(Cell::new(0));
    let (mut rust, _, _) = crate::provider_protocol::rust3::factory_fixture_for_test(0);
    rust.realize_next(&mut NoSource(reads.clone())).unwrap();
    assert!(!rust.hello_sent());
    let rust_table = crate::provider_protocol::table::Table::load(
        crate::provider_protocol::table::Protocol::Rust3,
    )
    .unwrap();
    assert!(
        crate::provider_protocol::rust3::Rust3Participant::from_sender(
            &rust_table,
            rust,
            Box::new(NoSource(reads.clone()))
        )
        .is_err()
    );
    let (mut ts, context) = crate::provider_protocol::ts2::factory_fixture_for_test();
    ts.realize_next(&mut NoSource(reads.clone())).unwrap();
    assert!(!ts.hello_sent());
    let ts_table = crate::provider_protocol::table::Table::load(
        crate::provider_protocol::table::Protocol::Ts2,
    )
    .unwrap();
    assert!(
        crate::provider_protocol::ts2::Ts2Participant::from_sender(
            &ts_table,
            context,
            ts,
            Box::new(NoSource(reads.clone()))
        )
        .is_err()
    );
    assert_eq!(reads.get(), 0);
}
