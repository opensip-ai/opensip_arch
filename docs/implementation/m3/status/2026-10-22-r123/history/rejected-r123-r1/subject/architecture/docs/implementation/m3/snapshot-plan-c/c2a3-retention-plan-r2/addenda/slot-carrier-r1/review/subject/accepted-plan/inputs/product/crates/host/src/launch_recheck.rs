//! D4-4's host adapter over the operation's already-open CI-3 capabilities.
//! It opens no store or capability, drops no pin, and spawns nothing. The
//! operation must keep its trees through the supervisor's settlement.
use opensip_components::control_protocol::AdmittedSelection;
use opensip_components::session_factory::{
    self as factory, Authorities, CorruptCause, FactoryRefusal, Launch, LaunchRecheck, MemberKind,
    NamedMember, PreparedSession, Provider, RecheckFailure, RecheckedMember,
};
use opensip_identity::digest_hex;
use opensip_lifecycle::retained_tree::{MemberRequest, RetainedTree, TreeReadFailure};
use opensip_platform::{ClosureRecheck, WorkCost, WorkFailure, WorkScope};

/// A role's explicit member request in one selected operation-held closure.
/// C4 owns selecting the admitted closures and their association with roles.
pub(crate) struct Binding<'a> {
    pub name: &'a str,
    pub tree: usize,
    pub request: MemberRequest<'a>,
}
pub(crate) struct SessionInput<'a> {
    pub selection: AdmittedSelection,
    pub provider: Provider,
    pub launch: Launch<'a>,
    pub memory_budget_bytes: u64,
}

fn charge(work: &mut WorkScope<'_>, cost: WorkCost) -> Result<(), FactoryRefusal> {
    work.charge::<()>(cost).map_err(|error| match error {
        WorkFailure::Budget(budget) => FactoryRefusal::Budget(budget),
        WorkFailure::Operation(()) => unreachable!(),
    })
}
fn check(
    work: &mut WorkScope<'_>,
    key: &'static str,
    test: impl FnOnce() -> bool,
) -> Result<(), FactoryRefusal> {
    charge(
        work,
        WorkCost {
            objects: 0,
            edges: 1,
            bytes: 0,
        },
    )?;
    if test() {
        Ok(())
    } else {
        Err(FactoryRefusal::SpecInconsistent(key))
    }
}
fn find(
    bindings: &[Binding<'_>],
    name: &str,
    work: &mut WorkScope<'_>,
) -> Result<Option<usize>, FactoryRefusal> {
    if bindings.is_empty() {
        charge(
            work,
            WorkCost {
                objects: 0,
                edges: 1,
                bytes: 0,
            },
        )?;
        return Ok(None);
    }
    let (mut low, mut high) = (0, bindings.len());
    while low < high {
        let middle = low + (high - low) / 2;
        charge(
            work,
            WorkCost {
                objects: 0,
                edges: 1,
                bytes: 0,
            },
        )?;
        match bindings[middle].name.as_bytes().cmp(name.as_bytes()) {
            std::cmp::Ordering::Less => low = middle + 1,
            std::cmp::Ordering::Greater => high = middle,
            std::cmp::Ordering::Equal => return Ok(Some(middle)),
        }
    }
    Ok(None)
}

/// Refusals from the retained capability preserve the owner partition;
/// a read failure proves no corrupt digest, and budget keeps its own latch.
fn tree_failure(error: TreeReadFailure) -> RecheckFailure {
    match error {
        TreeReadFailure::Budget(budget) => RecheckFailure::Budget(budget),
        TreeReadFailure::Io { call, error } => RecheckFailure::Io { call, error },
        TreeReadFailure::NotInstalled | TreeReadFailure::Absent { .. } => {
            RecheckFailure::Corrupt(CorruptCause::Absent)
        }
        TreeReadFailure::Type { .. } => RecheckFailure::Corrupt(CorruptCause::Type),
        TreeReadFailure::Mode { .. } => RecheckFailure::Corrupt(CorruptCause::Mode),
        TreeReadFailure::Length { .. } => RecheckFailure::Corrupt(CorruptCause::Length),
        TreeReadFailure::Digest { .. } => RecheckFailure::Corrupt(CorruptCause::Digest),
        TreeReadFailure::LinkTarget { .. } => RecheckFailure::Corrupt(CorruptCause::LinkTarget),
        TreeReadFailure::Binding => RecheckFailure::Corrupt(CorruptCause::Binding),
        // Launch can only yield Association here. Open-time Pin/Custody/
        // Extra failures never produce a retained capability in the first
        // place; retain a fail-closed association route if that changes.
        TreeReadFailure::Association
        | TreeReadFailure::Pin
        | TreeReadFailure::Extra { .. }
        | TreeReadFailure::Custody(_) => RecheckFailure::Corrupt(CorruptCause::Association),
    }
}
pub(crate) struct Rechecker<'op, 'store, 'data, 'bindings> {
    trees: &'op mut [RetainedTree<'store, 'data>],
    bindings: &'bindings [Binding<'bindings>],
}
impl<'op, 'store, 'data, 'bindings> Rechecker<'op, 'store, 'data, 'bindings> {
    pub(crate) fn new(
        trees: &'op mut [RetainedTree<'store, 'data>],
        bindings: &'bindings [Binding<'bindings>],
        launch: &Launch<'_>,
        work: &mut WorkScope<'_>,
    ) -> Result<Self, FactoryRefusal> {
        for pair in bindings.windows(2) {
            check(work, "launch-binding-order", || {
                pair[0].name.as_bytes() < pair[1].name.as_bytes()
            })?;
        }
        for binding in bindings {
            check(work, "launch-binding-tree", || binding.tree < trees.len())?;
        }
        let required: [Option<(NamedMember<'_>, MemberKind)>; 4] = match launch {
            Launch::TypeScript {
                entrypoint,
                node,
                openssl_config,
                provider,
                ..
            } => [
                Some((*entrypoint, MemberKind::File)),
                Some((*node, MemberKind::File)),
                Some((*openssl_config, MemberKind::File)),
                Some((*provider, MemberKind::File)),
            ],
            Launch::Rust {
                entrypoint,
                provider,
                toolchain_root,
            } => [
                Some((*entrypoint, MemberKind::File)),
                Some((*provider, MemberKind::File)),
                Some((*toolchain_root, MemberKind::Directory)),
                None,
            ],
        };
        for (role, (member, kind)) in required.into_iter().flatten().enumerate() {
            let index = find(bindings, member.name, work)?.ok_or(
                FactoryRefusal::SpecInconsistent("launch-binding-not-selected"),
            )?;
            if role == 0 {
                // The selected CMS entrypoint is the owner's operation,
                // not a caller-labelled File request (even when its bytes
                // happen to match). This check precedes every native read.
                check(work, "launch-binding-entrypoint", || {
                    matches!(bindings[index].request, MemberRequest::Entrypoint)
                })?;
            }
            check(work, "launch-binding-kind", || {
                matches!(
                    (kind, bindings[index].request),
                    (
                        MemberKind::File,
                        MemberRequest::Entrypoint | MemberRequest::File(_)
                    ) | (MemberKind::Directory, MemberRequest::Directory(_))
                )
            })?;
        }
        charge(
            work,
            WorkCost {
                objects: 1,
                edges: 0,
                bytes: size_of::<Self>(),
            },
        )?;
        Ok(Self { trees, bindings })
    }
}
impl LaunchRecheck for Rechecker<'_, '_, '_, '_> {
    fn recheck(
        &mut self,
        name: &str,
        work: &mut WorkScope<'_>,
    ) -> Result<RecheckedMember, RecheckFailure> {
        let index = find(self.bindings, name, work)
            .map_err(|error| match error {
                FactoryRefusal::Budget(budget) => RecheckFailure::Budget(budget),
                _ => RecheckFailure::Corrupt(CorruptCause::Association),
            })?
            .ok_or(RecheckFailure::Corrupt(CorruptCause::Association))?;
        let binding = &self.bindings[index];
        // The native owner resolves aliases, verifies bytes/mode/kind from
        // retained handles, and binds this absolute path as its last step.
        let member = self.trees[binding.tree]
            .launch_member(binding.request, work)
            .map_err(tree_failure)?;
        let closure_recheck = if let Some(hash) = member.sha256() {
            let relative = member
                .member()
                .ok_or(RecheckFailure::Corrupt(CorruptCause::Association))?;
            work.charge::<()>(WorkCost {
                objects: 1,
                edges: 0,
                bytes: relative.len(),
            })
            .map_err(|error| match error {
                WorkFailure::Budget(budget) => RecheckFailure::Budget(budget),
                WorkFailure::Operation(()) => unreachable!(),
            })?;
            let relative = relative.to_owned();
            work.charge::<()>(WorkCost {
                objects: 1,
                edges: 0,
                bytes: 64,
            })
            .map_err(|error| match error {
                WorkFailure::Budget(budget) => RecheckFailure::Budget(budget),
                WorkFailure::Operation(()) => unreachable!(),
            })?;
            Some(ClosureRecheck {
                member: relative,
                device: member.device(),
                inode: member.inode(),
                sha256: digest_hex(&hash),
            })
        } else {
            None
        };
        work.charge::<()>(WorkCost {
            objects: 1,
            edges: 0,
            bytes: size_of::<RecheckedMember>(),
        })
        .map_err(|error| match error {
            WorkFailure::Budget(budget) => RecheckFailure::Budget(budget),
            WorkFailure::Operation(()) => unreachable!(),
        })?;
        Ok(RecheckedMember {
            launch_path: member.into_path(),
            closure_recheck,
        })
    }
}

pub(crate) fn prepare_session(
    input: SessionInput<'_>,
    trees: &mut [RetainedTree<'_, '_>],
    bindings: &[Binding<'_>],
    authorities: &Authorities<'_>,
    work: &mut WorkScope<'_>,
) -> Result<PreparedSession, FactoryRefusal> {
    work.scope(|work| {
        let mut recheck =
            Rechecker::new(trees, bindings, &input.launch, work).map_err(WorkFailure::Operation)?;
        factory::prepare(
            input.selection,
            input.provider,
            input.launch,
            input.memory_budget_bytes,
            authorities,
            &mut recheck,
            work,
        )
        .map_err(WorkFailure::Operation)
    })
    .map_err(|error| match error {
        WorkFailure::Budget(budget) => FactoryRefusal::Budget(budget),
        WorkFailure::Operation(error) => error,
    })
}

#[cfg(all(test, target_os = "macos"))]
#[path = "launch_recheck_tests.rs"]
mod tests;
