//! D4-4's accounted construction of D1a's exact role-specific launch spec.
//! No native call, custody check, work profile or launch authority is added.
//! Every owned representation is funded before allocation. The fixed-size
//! containers use explicit capacities, and joined arguments use one buffer.
use super::{Arg, ChildEnvironment, DescriptorSet, LaunchClass, LaunchSpec};
use crate::{WorkBudgetError, WorkCost, WorkFailure, WorkScope};
use std::{ffi::CString, os::unix::ffi::OsStrExt, path::Path};

type R<T> = Result<T, WorkFailure<&'static str>>;

fn heap(work: &mut WorkScope<'_>, bytes: usize) -> R<()> {
    work.charge(WorkCost {
        objects: 1,
        edges: 0,
        bytes,
    })
}
fn comparison(work: &mut WorkScope<'_>) -> R<()> {
    work.charge(WorkCost {
        objects: 0,
        edges: 1,
        bytes: 0,
    })
}
fn product(a: usize, b: usize) -> R<usize> {
    a.checked_mul(b)
        .ok_or(WorkFailure::Budget(WorkBudgetError::Arithmetic))
}
fn path<'a>(value: &'a Path, work: &mut WorkScope<'_>) -> R<&'a [u8]> {
    comparison(work)?;
    if !value.is_absolute() {
        return Err(WorkFailure::Operation("launch-path-absolute"));
    }
    let bytes = value.as_os_str().as_bytes();
    comparison(work)?;
    if bytes.contains(&0) {
        return Err(WorkFailure::Operation("launch-path-nul"));
    }
    Ok(bytes)
}
fn argument(parts: &[&[u8]], work: &mut WorkScope<'_>) -> R<Arg> {
    let size = parts
        .iter()
        .try_fold(1usize, |n, part| n.checked_add(part.len()))
        .ok_or(WorkFailure::Budget(WorkBudgetError::Arithmetic))?;
    heap(work, size)?;
    let mut bytes = Vec::with_capacity(size);
    for part in parts {
        bytes.extend_from_slice(part);
    }
    bytes.push(0);
    comparison(work)?;
    CString::from_vec_with_nul(bytes)
        .map(Arg::Fixed)
        .map_err(|_| WorkFailure::Operation("launch-argument-nul"))
}
fn text(value: &str, work: &mut WorkScope<'_>) -> R<String> {
    heap(work, value.len())?;
    Ok(value.to_owned())
}
fn environment(values: &[(&str, &str)], work: &mut WorkScope<'_>) -> R<ChildEnvironment> {
    heap(work, product(values.len(), size_of::<(String, String)>())?)?;
    let mut entries = Vec::with_capacity(values.len());
    for (key, value) in values {
        entries.push((text(key, work)?, text(value, work)?));
    }
    Ok(ChildEnvironment { entries })
}

impl LaunchSpec {
    /// D1a's Rust3 argv and closed environment, charged on the caller's
    /// borrowed operation scope. Any failure latches that same ledger.
    pub fn rust_accounted(
        provider: &Path,
        toolchain_root: &Path,
        work: &mut WorkScope<'_>,
    ) -> R<Self> {
        work.scope(|work| {
            let executable = path(provider, work)?;
            let toolchain = path(toolchain_root, work)?;
            heap(work, executable.len())?;
            let executable_path = provider.to_path_buf();
            heap(work, product(6, size_of::<Arg>())?)?;
            let mut argv = Vec::with_capacity(6);
            for parts in [
                executable,
                b"--protocol-stdio-v2",
                b"--toolchain-root",
                toolchain,
                b"--scratch-root",
            ] {
                argv.push(argument(&[parts], work)?);
            }
            argv.push(Arg::Scratch);
            let environment = environment(&[("LANG", "C"), ("LC_ALL", "C"), ("TZ", "UTC")], work)?;
            heap(work, size_of::<Self>())?;
            Ok(Self {
                class: LaunchClass::Provider,
                descriptors: DescriptorSet::Provider,
                executable: executable_path,
                argv,
                environment,
            })
        })
    }

    /// D1a's TS2 argv and closed environment, with a single funded joined
    /// OpenSSL argument and no temporary absolute-path CString.
    // Keep the funded argv allocation before the fallible argument work so
    // a refused prefix has the same priced and allocated representations.
    #[allow(clippy::vec_init_then_push)]
    pub fn typescript_accounted(
        node: &Path,
        openssl_config: &Path,
        entry: &Path,
        broker_context: &str,
        work: &mut WorkScope<'_>,
    ) -> R<Self> {
        work.scope(|work| {
            let node_bytes = path(node, work)?;
            let config_bytes = path(openssl_config, work)?;
            let entry_bytes = path(entry, work)?;
            comparison(work)?;
            if broker_context.as_bytes().contains(&0) {
                return Err(WorkFailure::Operation("broker-context-nul"));
            }
            heap(work, node_bytes.len())?;
            let executable = node.to_path_buf();
            heap(work, product(5, size_of::<Arg>())?)?;
            let mut argv = Vec::with_capacity(5);
            argv.push(argument(&[node_bytes], work)?);
            argv.push(argument(&[b"--no-addons"], work)?);
            argv.push(argument(&[b"--no-global-search-paths"], work)?);
            argv.push(argument(&[b"--openssl-config=", config_bytes], work)?);
            argv.push(argument(&[entry_bytes], work)?);
            let environment = environment(
                &[
                    ("LC_ALL", "C"),
                    ("LANG", "C"),
                    ("TZ", "UTC"),
                    ("UV_THREADPOOL_SIZE", "4"),
                    ("OPENSIP_BROKER_CONTEXT", broker_context),
                ],
                work,
            )?;
            heap(work, size_of::<Self>())?;
            Ok(Self {
                class: LaunchClass::Provider,
                descriptors: DescriptorSet::Provider,
                executable,
                argv,
                environment,
            })
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::WorkLedger;
    use std::os::unix::ffi::OsStrExt;

    #[test]
    fn accounted_specs_preserve_exact_closed_argv_environment_and_raw_paths() {
        for provider in [
            Path::new("/store/provider"),
            Path::new(std::ffi::OsStr::from_bytes(b"/store/\xff-provider")),
        ] {
            let mut ledger = WorkLedger::new();
            let actual = ledger
                .scope(|work| {
                    LaunchSpec::rust_accounted(provider, Path::new("/store/toolchain"), work)
                })
                .unwrap();
            assert_eq!(
                actual,
                LaunchSpec::rust(provider, Path::new("/store/toolchain")).unwrap()
            );
            assert_eq!(ledger.used().objects, 15);
            assert_eq!(ledger.used().edges, 9);
        }
        let mut ledger = WorkLedger::new();
        let actual = ledger
            .scope(|work| {
                LaunchSpec::typescript_accounted(
                    Path::new("/store/node"),
                    Path::new("/store/empty.cnf"),
                    Path::new("/store/provider.js"),
                    "{\"broker\":[]}",
                    work,
                )
            })
            .unwrap();
        assert_eq!(
            actual,
            LaunchSpec::typescript(
                Path::new("/store/node"),
                Path::new("/store/empty.cnf"),
                Path::new("/store/provider.js"),
                "{\"broker\":[]}"
            )
            .unwrap()
        );
        assert_eq!(ledger.used().objects, 19);
        assert_eq!(ledger.used().edges, 12);
    }

    #[test]
    fn invalid_input_and_work_failure_latch_the_callers_ledger() {
        let mut ledger = WorkLedger::new();
        let refused = ledger.scope(|work| {
            LaunchSpec::rust_accounted(Path::new("relative"), Path::new("/toolchain"), work)
        });
        assert_eq!(refused, Err(WorkFailure::Operation("launch-path-absolute")));
        assert_eq!(
            ledger.used(),
            WorkCost {
                objects: 0,
                edges: 1,
                bytes: 0
            }
        );
        assert!(ledger.is_failed());
        assert_eq!(
            ledger.charge::<()>(WorkCost::default()),
            Err(WorkFailure::Budget(WorkBudgetError::Closed))
        );
    }

    #[test]
    fn independently_enumerated_rust_representations_fit_exactly_and_each_one_short_refuses() {
        // An independent literal inventory of the resulting representations,
        // including C terminators and the scratch enum slot (no scratch path
        // exists before spawn). This calls none of the production price code.
        let strings: [&[u8]; 5] = [
            b"/s/p\0",
            b"--protocol-stdio-v2\0",
            b"--toolchain-root\0",
            b"/s/t\0",
            b"--scratch-root\0",
        ];
        let environment: [&str; 6] = ["LANG", "C", "LC_ALL", "C", "TZ", "UTC"];
        let exact = WorkCost {
            objects: 15,
            edges: 9,
            bytes: size_of::<LaunchSpec>()
                + 4
                + 6 * size_of::<Arg>()
                + 3 * size_of::<(String, String)>()
                + strings.iter().map(|v| v.len()).sum::<usize>()
                + environment.iter().map(|v| v.len()).sum::<usize>(),
        };
        let mut funded = WorkLedger::with_limits(exact).unwrap();
        funded
            .scope(|work| LaunchSpec::rust_accounted(Path::new("/s/p"), Path::new("/s/t"), work))
            .unwrap();
        assert_eq!(funded.used(), exact);
        for (limit, expected) in [
            (
                WorkCost {
                    objects: exact.objects - 1,
                    ..exact
                },
                WorkBudgetError::Objects,
            ),
            (
                WorkCost {
                    edges: exact.edges - 1,
                    ..exact
                },
                WorkBudgetError::Edges,
            ),
            (
                WorkCost {
                    bytes: exact.bytes - 1,
                    ..exact
                },
                WorkBudgetError::Bytes,
            ),
        ] {
            let mut ledger = WorkLedger::with_limits(limit).unwrap();
            let result = ledger.scope(|work| {
                LaunchSpec::rust_accounted(Path::new("/s/p"), Path::new("/s/t"), work)
            });
            assert_eq!(result, Err(WorkFailure::Budget(expected)));
            assert!(ledger.is_failed());
            let prefix = ledger.used();
            assert_ne!(prefix, exact);
            assert_eq!(
                ledger.scope(|work| LaunchSpec::rust_accounted(
                    Path::new("/s/p"),
                    Path::new("/s/t"),
                    work
                )),
                Err(WorkFailure::Budget(WorkBudgetError::Closed))
            );
            assert_eq!(ledger.used(), prefix);
        }
    }

    #[test]
    fn typescript_joined_argument_and_utf8_environment_have_exact_owned_prices() {
        let strings: [&[u8]; 5] = [
            b"/s/n\0",
            b"--no-addons\0",
            b"--no-global-search-paths\0",
            b"--openssl-config=/s/e\0",
            b"/s/p\0",
        ];
        let environment = [
            "LC_ALL",
            "C",
            "LANG",
            "C",
            "TZ",
            "UTC",
            "UV_THREADPOOL_SIZE",
            "4",
            "OPENSIP_BROKER_CONTEXT",
            "{\"x\":\"λ\"}",
        ];
        let exact = WorkCost {
            objects: 19,
            edges: 12,
            bytes: size_of::<LaunchSpec>()
                + 4
                + 5 * size_of::<Arg>()
                + 5 * size_of::<(String, String)>()
                + strings.iter().map(|v| v.len()).sum::<usize>()
                + environment.iter().map(|v| v.len()).sum::<usize>(),
        };
        let mut ledger = WorkLedger::with_limits(exact).unwrap();
        let actual = ledger
            .scope(|work| {
                LaunchSpec::typescript_accounted(
                    Path::new("/s/n"),
                    Path::new("/s/e"),
                    Path::new("/s/p"),
                    environment[9],
                    work,
                )
            })
            .unwrap();
        assert_eq!(
            actual,
            LaunchSpec::typescript(
                Path::new("/s/n"),
                Path::new("/s/e"),
                Path::new("/s/p"),
                environment[9]
            )
            .unwrap()
        );
        assert_eq!(ledger.used(), exact);
        let mut short = WorkLedger::with_limits(WorkCost {
            bytes: exact.bytes - 1,
            ..exact
        })
        .unwrap();
        assert_eq!(
            short.scope(|work| LaunchSpec::typescript_accounted(
                Path::new("/s/n"),
                Path::new("/s/e"),
                Path::new("/s/p"),
                environment[9],
                work
            )),
            Err(WorkFailure::Budget(WorkBudgetError::Bytes))
        );
        assert!(short.is_failed());
        let mut invalid = WorkLedger::new();
        assert_eq!(
            invalid.scope(|work| LaunchSpec::typescript_accounted(
                Path::new("/s/n"),
                Path::new("/s/e"),
                Path::new("/s/p"),
                "bad\0context",
                work
            )),
            Err(WorkFailure::Operation("broker-context-nul"))
        );
        assert_eq!(
            invalid.used(),
            WorkCost {
                objects: 0,
                edges: 7,
                bytes: 0
            }
        );
    }
    // D4-T3 needs the factory's exact checked closed spec, including its scratch
    // slot, under item 1's TestFixture class. The conversion grants no new argv.
    #[test]
    #[cfg(debug_assertions)]
    fn test_fixture_conversion_preserves_every_checked_launch_field() {
        use crate::process::{ClosureRecheck, VerifiedLaunch};
        let spec = LaunchSpec::rust(
            Path::new("/first-party/provider"),
            Path::new("/first-party/toolchain"),
        )
        .unwrap();
        let recheck = ClosureRecheck {
            member: "provider".into(),
            device: 17,
            inode: 19,
            sha256: "a".repeat(64),
        };
        let launch = VerifiedLaunch::from_recheck(spec, recheck);
        let mut expected = launch.clone();
        expected.spec.class = LaunchClass::TestFixture;
        let converted = launch.into_test_fixture();
        assert_eq!(converted, expected);
        assert_eq!(converted.spec().class(), LaunchClass::TestFixture);
    }
}
