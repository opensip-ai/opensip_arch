//! D4-4's pre-spawn session factory boundary (M3-D item 26; D4 plan r2).
//!
//! The host lends the operation's pinned closure capability through the
//! recheck seam. Components neither opens nor drops that capability. A
//! refusal is pre-spawn and has no supervision or settlement to decline.
use crate::supervisor::records::OwnerRoute;
use opensip_platform::{ClosureRecheck, WorkBudgetError, WorkScope};
use std::{io, path::PathBuf};

mod spec;
use crate::control_protocol::{AdmittedSelection, ControlContext};
use crate::provider_protocol::{
    cbor::Value,
    rust3::Rust3Sender,
    ts2::{DispatchContext, Ts2Sender},
};
use crate::supervisor::SessionSpec;
use opensip_platform::{LaunchSpec, VerifiedLaunch, WorkCost, WorkFailure};
use std::path::Path;

/// The promised closure's own corruption. Observation and work failures
/// remain separate, including an absent member's later missing-byte route.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CorruptCause {
    Absent,
    Type,
    Mode,
    Length,
    Digest,
    LinkTarget,
    Association,
    Binding,
}

#[derive(Debug)]
pub enum RecheckFailure {
    Budget(WorkBudgetError),
    Io {
        call: &'static str,
        error: io::Error,
    },
    Corrupt(CorruptCause),
}

/// CI-A3's bound path and the executable identity observed through the
/// retained handle. Directory members are checked but supply no executable
/// identity to `VerifiedLaunch`.
#[derive(Debug)]
pub struct RecheckedMember {
    pub launch_path: PathBuf,
    /// CI-A3-r4 gives a digest for files only. Directory checks retain their
    /// bound path without manufacturing a file digest. The executable must
    /// supply `Some` before the factory constructs a verified launch.
    pub closure_recheck: Option<ClosureRecheck>,
}

/// Implemented by the host over the operation's borrowed retained tree.
/// The operation keeps its capability alive through spawn and settlement.
pub trait LaunchRecheck {
    fn recheck(
        &mut self,
        member: &str,
        work: &mut WorkScope<'_>,
    ) -> Result<RecheckedMember, RecheckFailure>;
}

#[derive(Debug)]
pub enum FactoryRefusal {
    Recheck(RecheckFailure),
    Budget(WorkBudgetError),
    SpecInconsistent(&'static str),
}
impl From<RecheckFailure> for FactoryRefusal {
    fn from(value: RecheckFailure) -> Self {
        match value {
            RecheckFailure::Budget(budget) => Self::Budget(budget),
            other => Self::Recheck(other),
        }
    }
}
impl FactoryRefusal {
    /// J2 retains the typed cause for its detailed operational projection.
    /// In particular `Absent` selects missing bytes, while an observation
    /// I/O error establishes no closure corruption. Budget keeps its ledger
    /// failure and follows row 11's invariant route.
    pub fn route(&self) -> OwnerRoute {
        match self {
            Self::Recheck(RecheckFailure::Corrupt(_)) => OwnerRoute::ClosureBytesCorrupt,
            Self::Recheck(RecheckFailure::Io { .. }) => OwnerRoute::HostIo,
            Self::Recheck(RecheckFailure::Budget(_))
            | Self::Budget(_)
            | Self::SpecInconsistent(_) => OwnerRoute::HostInvariant,
        }
    }
}

/// Immutable codec output already assembled from C4's supplied projections.
/// The factory receives no snapshot source and cannot disclose source bytes.
// Retain the already-owned codec without another heap allocation. The fixed
// inline sum is included in the funded PreparedSession record's size.
#[allow(clippy::large_enum_variant)]
pub enum Provider {
    TypeScript {
        sender: Ts2Sender,
        context: DispatchContext,
    },
    Rust {
        sender: Rust3Sender,
    },
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum MemberKind {
    File,
    Directory,
}

#[derive(Clone, Copy)]
pub struct NamedMember<'a> {
    pub name: &'a str,
    pub launch_path: &'a Path,
}

/// A borrowed projection of a member of a selected admitted closure. This
/// data holder does not admit caller strings: production's host adapter must
/// obtain the association and row from the operation's admitted capability.
/// Before C4 production composition, tests identify synthetic inputs as such.
pub struct MemberAuthority<'a> {
    pub member: NamedMember<'a>,
    pub kind: MemberKind,
    pub closure_member: &'a str,
    pub file_sha256: Option<&'a str>,
}

pub enum Launch<'a> {
    TypeScript {
        entrypoint: NamedMember<'a>,
        node: NamedMember<'a>,
        openssl_config: NamedMember<'a>,
        provider: NamedMember<'a>,
        broker_context: &'a str,
    },
    Rust {
        entrypoint: NamedMember<'a>,
        provider: NamedMember<'a>,
        toolchain_root: NamedMember<'a>,
    },
}

/// Separate admitted values against which actual assembled output is
/// checked. These are not derived from that output or from its input copy.
pub struct Authorities<'a> {
    pub selection: &'a AdmittedSelection,
    pub capabilities: &'a [String],
    pub entrypoint: &'a str,
    /// Strict ascending name order; the factory funds and checks the order.
    pub members: &'a [MemberAuthority<'a>],
    pub identity: IdentityAuthority<'a>,
}
pub enum IdentityAuthority<'a> {
    TypeScript {
        provider_sha256: &'a str,
        runtime_sha256: &'a str,
        provider_fields: &'a crate::provider_protocol::ts2::DescriptorFields,
        runtime_fields: &'a crate::provider_protocol::ts2::DescriptorFields,
    },
    Rust {
        expected_identity: &'a Value,
    },
}

/// A fully checked library session. It spawns nothing and grants neither
/// C4/native admission nor H settlement. The operation retains its closure
/// pins through the later supervisor's settlement (CI-A3-f).
pub struct PreparedSession {
    pub session: SessionSpec,
    pub control: ControlContext,
    pub provider: Provider,
}
type MemberRoles<'a> = [Option<(NamedMember<'a>, MemberKind, bool)>; 4];

fn work_failure(value: WorkFailure<&'static str>) -> FactoryRefusal {
    match value {
        WorkFailure::Budget(budget) => FactoryRefusal::Budget(budget),
        WorkFailure::Operation(key) => FactoryRefusal::SpecInconsistent(key),
    }
}
fn check(
    work: &mut WorkScope<'_>,
    key: &'static str,
    test: impl FnOnce() -> bool,
) -> Result<(), FactoryRefusal> {
    work.charge::<&'static str>(WorkCost {
        objects: 0,
        edges: 1,
        bytes: 0,
    })
    .map_err(work_failure)?;
    if test() {
        Ok(())
    } else {
        Err(FactoryRefusal::SpecInconsistent(key))
    }
}
fn member<'b, 'a>(
    authorities: &'b Authorities<'a>,
    name: &str,
    work: &mut WorkScope<'_>,
) -> Result<&'b MemberAuthority<'a>, FactoryRefusal> {
    let mut low = 0;
    let mut high = authorities.members.len();
    // The empty-slice probe has the same one-edge price as D4's other probes.
    if authorities.members.is_empty() {
        check(work, "launch-member-not-selected", || false)?;
    }
    while low < high {
        let middle = low + (high - low) / 2;
        work.charge::<&'static str>(WorkCost {
            objects: 0,
            edges: 1,
            bytes: 0,
        })
        .map_err(work_failure)?;
        match authorities.members[middle]
            .member
            .name
            .as_bytes()
            .cmp(name.as_bytes())
        {
            std::cmp::Ordering::Less => low = middle + 1,
            std::cmp::Ordering::Greater => high = middle,
            std::cmp::Ordering::Equal => return Ok(&authorities.members[middle]),
        }
    }
    Err(FactoryRefusal::SpecInconsistent(
        "launch-member-not-selected",
    ))
}

/// Assemble and validate first, then perform every bound member recheck as
/// the last operation before the sole production VerifiedLaunch constructor.
/// No source interface, spawn function or effect capability is accepted.
pub fn prepare(
    selection: AdmittedSelection,
    provider: Provider,
    launch: Launch<'_>,
    memory_budget_bytes: u64,
    authorities: &Authorities<'_>,
    recheck: &mut dyn LaunchRecheck,
    work: &mut WorkScope<'_>,
) -> Result<PreparedSession, FactoryRefusal> {
    work.scope(|work| {
        prepare_inner(
            selection,
            provider,
            launch,
            memory_budget_bytes,
            authorities,
            recheck,
            work,
        )
        .map_err(|error| match error {
            FactoryRefusal::Budget(budget) => WorkFailure::Budget(budget),
            other => WorkFailure::Operation(other),
        })
    })
    .map_err(|error| match error {
        WorkFailure::Budget(budget) => FactoryRefusal::Budget(budget),
        WorkFailure::Operation(other) => other,
    })
}

fn prepare_inner(
    selection: AdmittedSelection,
    provider: Provider,
    launch: Launch<'_>,
    memory_budget_bytes: u64,
    authorities: &Authorities<'_>,
    recheck: &mut dyn LaunchRecheck,
    work: &mut WorkScope<'_>,
) -> Result<PreparedSession, FactoryRefusal> {
    for pair in authorities.members.windows(2) {
        check(work, "launch-member-order", || {
            pair[0].member.name.as_bytes() < pair[1].member.name.as_bytes()
        })?;
    }
    let control = ControlContext::for_session_accounted(&selection, work).map_err(work_failure)?;
    let (specification, paths): (LaunchSpec, MemberRoles<'_>) = match launch {
        Launch::TypeScript {
            entrypoint,
            node,
            openssl_config,
            provider,
            broker_context,
        } => (
            LaunchSpec::typescript_accounted(
                node.launch_path,
                openssl_config.launch_path,
                provider.launch_path,
                broker_context,
                work,
            )
            .map_err(work_failure)?,
            [
                Some((entrypoint, MemberKind::File, false)),
                Some((node, MemberKind::File, true)),
                Some((openssl_config, MemberKind::File, false)),
                Some((provider, MemberKind::File, false)),
            ],
        ),
        Launch::Rust {
            entrypoint,
            provider,
            toolchain_root,
        } => (
            LaunchSpec::rust_accounted(provider.launch_path, toolchain_root.launch_path, work)
                .map_err(work_failure)?,
            [
                Some((entrypoint, MemberKind::File, false)),
                Some((provider, MemberKind::File, true)),
                Some((toolchain_root, MemberKind::Directory, false)),
                None,
            ],
        ),
    };
    spec::validate(&control, &provider, authorities, work)?;
    check(work, "selected-entrypoint", || {
        paths[0].is_some_and(|(path, _, _)| path.name == authorities.entrypoint)
    })?;
    // Membership and path checks are complete before the first recheck.
    let mut admitted = [None; 4];
    for (index, (path, kind, is_executable)) in paths.iter().flatten().enumerate() {
        let selected = member(authorities, path.name, work)?;
        check(work, "launch-member-kind", || selected.kind == *kind)?;
        check(work, "launch-member-path", || {
            selected.member.launch_path == path.launch_path
        })?;
        check(work, "launch-member-digest", || {
            selected.file_sha256.is_some() == (*kind == MemberKind::File)
        })?;
        if *is_executable {
            check(work, "assembled-executable", || {
                specification.executable() == path.launch_path
            })?;
        }
        admitted[index] = Some(selected);
    }
    check(work, "launch-profile", || {
        matches!(
            (&provider, &paths[2]),
            (Provider::Rust { .. }, Some((_, MemberKind::Directory, _)))
                | (Provider::TypeScript { .. }, Some((_, MemberKind::File, _)))
        )
    })?;
    // Fund the returned owned record before the final rechecks. Its buffers
    // were individually funded by their owners; moving them copies no bytes.
    work.charge::<&'static str>(WorkCost {
        objects: 1,
        edges: 0,
        bytes: size_of::<PreparedSession>(),
    })
    .map_err(work_failure)?;
    let mut executable = None;
    for ((path, kind, is_executable), selected) in paths
        .into_iter()
        .flatten()
        .zip(admitted.into_iter().flatten())
    {
        let checked = recheck
            .recheck(path.name, work)
            .map_err(FactoryRefusal::from)?;
        check(work, "rechecked-launch-path", || {
            checked.launch_path == path.launch_path
        })?;
        match (kind, checked.closure_recheck) {
            (MemberKind::File, Some(identity)) => {
                check(work, "rechecked-member", || {
                    identity.member == selected.closure_member
                })?;
                check(work, "rechecked-digest", || {
                    Some(identity.sha256.as_str()) == selected.file_sha256
                })?;
                if is_executable {
                    executable = Some(identity);
                }
            }
            (MemberKind::Directory, None) => {}
            _ => return Err(FactoryRefusal::SpecInconsistent("rechecked-member-kind")),
        }
    }
    let executable = executable.ok_or(FactoryRefusal::SpecInconsistent("executable-recheck"))?;
    let launch = VerifiedLaunch::from_recheck(specification, executable);
    Ok(PreparedSession {
        session: SessionSpec {
            launch,
            selection,
            memory_budget_bytes,
        },
        control,
        provider,
    })
}

#[cfg(test)]
mod tests;
