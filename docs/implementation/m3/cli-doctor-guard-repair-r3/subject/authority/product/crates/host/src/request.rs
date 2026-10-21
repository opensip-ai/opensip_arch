use std::{collections::BTreeMap, sync::Arc};

/// A host-owned request capability. It exposes no identifier or mint authority.
/// It is neither deserializable nor independently constructible.
pub struct RequestContext {
    _private: u8,
}

#[derive(Debug, PartialEq, Eq)]
pub enum RequestAllocationError {
    EntropyUnavailable,
    CollisionExhausted,
}

/// Process-custody registry for the explicitly nonpersistent metadata host.
/// Durable host audit custody uses the separately implemented durable ingress.
///
/// Law M3-J1 r6 item 2 (unit J3a): it is also IE:77-79's "corresponding
/// operational ledger" for the invocation's one RequestId, which a host
/// serving one request per process keeps in process custody. Each RequestId
/// is a platform `RequestIdentity`, minted only by the CSPRNG draw, reserved
/// here with its uniqueness checked before any use and never released; the
/// host lends `&RequestIdentity` to the durable entry, and the envelope and
/// every record project the same reservation.
#[derive(Default)]
pub(crate) struct RequestAuthority {
    reservations: BTreeMap<[u8; 16], Arc<RequestContext>>,
    identities: BTreeMap<[u8; 16], opensip_platform::RequestIdentity>,
}
impl RequestAuthority {
    pub(crate) fn begin(&mut self) -> Result<Arc<RequestContext>, RequestAllocationError> {
        // `allocate` returns on the first draw it reserves, so the last
        // identity drawn is the reserved one.
        let mut drawn = None;
        let context = self.allocate(|| {
            let identity = opensip_platform::RequestIdentity::draw()
                .map_err(|_| RequestAllocationError::EntropyUnavailable)?;
            let bytes = identity.bytes();
            drawn = Some(identity);
            Ok(bytes)
        })?;
        let identity = drawn.expect("a reservation follows a draw");
        self.identities.insert(identity.bytes(), identity);
        Ok(context)
    }
    /// J1 item 2: the reserved `RequestIdentity` behind one of this
    /// registry's contexts, which the host lends to the durable entry (J1
    /// item 3; the pipeline's call is J3d's). A foreign or unreserved
    /// context has none. Read-only: it mints and reserves nothing.
    pub(crate) fn identity(
        &self,
        context: &RequestContext,
    ) -> Option<&opensip_platform::RequestIdentity> {
        let (id, _) = self
            .reservations
            .iter()
            .find(|(_, reserved)| std::ptr::eq(Arc::as_ptr(reserved), context))?;
        self.identities.get(id)
    }
    /// J3a-o: lend only this registry's genuine reserved platform identity.
    pub(crate) fn logging_scope(
        &self,
        context: &RequestContext,
    ) -> Option<opensip_operability::RequestScope> {
        let identity = self.identity(context)?;
        Some(opensip_operability::RequestScope::from(identity))
    }
    fn allocate(
        &mut self,
        mut draw: impl FnMut() -> Result<[u8; 16], RequestAllocationError>,
    ) -> Result<Arc<RequestContext>, RequestAllocationError> {
        for _ in 0..8 {
            let id = draw()?;
            if let std::collections::btree_map::Entry::Vacant(entry) = self.reservations.entry(id) {
                let context = Arc::new(RequestContext { _private: 1 });
                entry.insert(Arc::clone(&context));
                return Ok(context);
            }
        }
        Err(RequestAllocationError::CollisionExhausted)
    }
    pub(crate) fn project(&self, context: &RequestContext) -> Option<String> {
        self.reservations.iter().find_map(|(id, reserved)| {
            if !std::ptr::eq(Arc::as_ptr(reserved), context) {
                return None;
            }
            let mut text = String::from("req1_");
            use std::fmt::Write;
            for byte in id {
                write!(&mut text, "{byte:02x}").expect("String writes cannot fail");
            }
            Some(text)
        })
    }
}

/// How a command relates to the account installation before one exists
/// (owner.md §1a step 1 and §6). The match is exhaustive over the selected
/// command inventory, so a new command cannot enter the creator set silently.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum InstallationEntry {
    /// May mint the single-use creation intent: `authority ==
    /// "authoritative-default"` in inventory v3, minus `repair-verify`.
    Creator,
    /// Needs the installation. When it is positively absent the request is
    /// rejected with `REQUEST.PRECONDITION_FAILED` / `INSTALLATION.NOT_INITIALIZED`.
    NotInitializedWhenAbsent,
    /// Not a creator. Whether it needs the installation is decided by the
    /// command's own owner when that command is implemented.
    CommandOwnerDecides,
    /// Metadata, doctor, explicit ephemeral analysis and distribution
    /// commands never enter the creation or not-initialized rules.
    Outside,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum InstallationEntryError {
    /// `--ephemeral` on a command that does not accept it.
    EphemeralNotAccepted,
}

/// Classify a parsed command. `ephemeral` is the explicit `--ephemeral`
/// flag; only `analyze` and `fit` accept it, and it takes them outside the
/// creator (it is not a creator permit or an automatic fallback).
pub fn installation_entry(
    command: opensip_contracts::generated::invocation::Inventory3CommandName,
    ephemeral: bool,
) -> Result<InstallationEntry, InstallationEntryError> {
    use InstallationEntry::*;
    use opensip_contracts::generated::invocation::Inventory3CommandName as C;
    let entry = match command {
        C::Analyze | C::Fit if ephemeral => return Ok(Outside),
        C::Default | C::Analyze | C::Fit | C::Audit => Creator,
        C::Import
        | C::BaselineUpgrade
        | C::RepairApply
        | C::RepairVerify
        | C::TestRun
        | C::NativePrepare => NotInitializedWhenAbsent,
        C::Help | C::Version | C::Completion | C::Doctor | C::Install | C::Update => Outside,
        C::Recommend
        | C::Query
        | C::BaselineAdopt
        | C::BaselineExport
        | C::BaselineShow
        | C::PolicyShow
        | C::PolicyInit
        | C::PolicyTest
        | C::Waive
        | C::Candidates
        | C::Inspect
        | C::ReviewBrief
        | C::ReviewJoin
        | C::RepairPreview
        | C::RepairRecover
        | C::Purge
        | C::AgentServe
        | C::TrustRecoveryChallenge
        | C::TrustRecoveryImport
        | C::TrustRefresh
        | C::TrustImport
        | C::TrustDoctor
        | C::StoreMigrate
        | C::StoreRollback
        | C::StoreGc
        | C::StoreStatus
        | C::CoreUpdate
        | C::CoreRepair
        | C::CoreRollback => CommandOwnerDecides,
    };
    if ephemeral {
        return Err(InstallationEntryError::EphemeralNotAccepted);
    }
    Ok(entry)
}

/// The not-initialized rule (owner.md §6). Apply it only after the request's
/// earlier admission checks, which keep their precedence. `installation_absent`
/// must come from the security observation's positive absence, never from a
/// failed or unreadable observation. A creator proceeds to creation instead.
pub fn installation_precondition(
    entry: InstallationEntry,
    installation_absent: bool,
) -> Option<opensip_contracts::generated::evidence::Common4DomainDetailCode> {
    (entry == InstallationEntry::NotInitializedWhenAbsent && installation_absent).then_some(
        opensip_contracts::generated::evidence::Common4DomainDetailCode::InstallationNotInitialized,
    )
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn foreign_and_unreserved_contexts_cannot_project() {
        let mut a = RequestAuthority::default();
        let mut b = RequestAuthority::default();
        let x = a.allocate(|| Ok([1; 16])).unwrap();
        let y = b.allocate(|| Ok([1; 16])).unwrap();
        assert!(a.project(&y).is_none());
        assert!(b.project(&x).is_none());
        assert!(a.project(&RequestContext { _private: 1 }).is_none());
        assert_eq!(
            a.project(&x).unwrap(),
            "req1_01010101010101010101010101010101"
        );
        assert_eq!(a.reservations.len(), 1);
    }
    /// Law M3-J1 r6 item 2 (unit J3a), J-C2's host half: the identity the
    /// registry lends is the one its projection renders, so the envelope's
    /// `requestId` and P0's `invocation.requestId` (which the intent records
    /// from the lent identity) are one RequestId. A foreign context lends
    /// nothing.
    #[test]
    fn the_lent_identity_is_the_projected_request_id() {
        let mut a = RequestAuthority::default();
        let mut b = RequestAuthority::default();
        let x = a.begin().unwrap();
        let y = b.begin().unwrap();
        let lent = a.identity(&x).unwrap();
        let rendered = lent
            .bytes()
            .iter()
            .fold("req1_".to_owned(), |text, byte| format!("{text}{byte:02x}"));
        assert_eq!(a.project(&x).unwrap(), rendered);
        assert!(a.identity(&y).is_none());
        assert!(b.identity(&x).is_none());
        assert!(a.identity(&RequestContext { _private: 1 }).is_none());
        assert_ne!(b.identity(&y).unwrap().bytes(), lent.bytes());
        assert_eq!((a.reservations.len(), a.identities.len()), (1, 1));
        // A context reserved through a forced draw has no lent identity.
        let forced = a.allocate(|| Ok([9; 16])).unwrap();
        assert!(a.project(&forced).is_some() && a.identity(&forced).is_none());
    }
    #[test]
    fn logging_scopes_require_the_owned_platform_reservation() {
        let mut a = RequestAuthority::default();
        let mut b = RequestAuthority::default();
        let x = a.begin().unwrap();
        let y = b.begin().unwrap();
        let before = (a.reservations.len(), a.identities.len());
        assert!(a.logging_scope(&x).is_some());
        assert!(a.logging_scope(&x).is_some());
        assert!(a.logging_scope(&y).is_none());
        assert!(b.logging_scope(&x).is_none());
        assert!(a.logging_scope(&RequestContext { _private: 1 }).is_none());
        assert_eq!((a.reservations.len(), a.identities.len()), before);
        let forced = a.allocate(|| Ok([7; 16])).unwrap();
        assert!(a.project(&forced).is_some());
        assert!(a.logging_scope(&forced).is_none());
    }

    #[test]
    fn collision_budget_and_error_do_not_publish_or_replace() {
        let mut a = RequestAuthority::default();
        let first = a.allocate(|| Ok([0; 16])).unwrap();
        let mut draws = 0;
        assert!(matches!(
            a.allocate(|| {
                draws += 1;
                Ok([0; 16])
            }),
            Err(RequestAllocationError::CollisionExhausted)
        ));
        assert_eq!(draws, 8);
        assert_eq!(a.reservations.len(), 1);
        assert!(a.project(&first).is_some());
        assert!(matches!(
            a.allocate(|| Err(RequestAllocationError::EntropyUnavailable)),
            Err(RequestAllocationError::EntropyUnavailable)
        ));
        assert_eq!(a.reservations.len(), 1);
        let mut calls = 0;
        let second = a
            .allocate(|| {
                calls += 1;
                Ok([if calls < 3 { 0 } else { 2 }; 16])
            })
            .unwrap();
        assert_eq!(calls, 3);
        assert_ne!(a.project(&first), a.project(&second));
    }
    #[test]
    fn only_the_four_authoritative_default_commands_may_create() {
        use opensip_contracts::generated::invocation::Inventory3CommandName as C;
        let all: Vec<C> = serde_json::from_value(serde_json::json!([
            "default",
            "recommend",
            "analyze",
            "fit",
            "audit",
            "query",
            "import",
            "baseline-adopt",
            "baseline-export",
            "baseline-show",
            "baseline-upgrade",
            "policy-show",
            "policy-init",
            "policy-test",
            "waive",
            "candidates",
            "inspect",
            "review-brief",
            "review-join",
            "repair-preview",
            "repair-apply",
            "repair-verify",
            "repair-recover",
            "test-run",
            "install",
            "update",
            "doctor",
            "purge",
            "agent-serve",
            "help",
            "version",
            "completion",
            "trust-recovery-challenge",
            "trust-recovery-import",
            "trust-refresh",
            "trust-import",
            "trust-doctor",
            "store-migrate",
            "store-rollback",
            "store-gc",
            "store-status",
            "native-prepare",
            "core-update",
            "core-repair",
            "core-rollback"
        ]))
        .unwrap();
        assert_eq!(all.len(), 45);
        let named = |entry: InstallationEntry| -> Vec<String> {
            all.iter()
                .filter(|c| installation_entry(**c, false) == Ok(entry))
                .map(|c| c.to_string())
                .collect()
        };
        assert_eq!(
            named(InstallationEntry::Creator),
            ["default", "analyze", "fit", "audit"]
        );
        assert_eq!(
            named(InstallationEntry::NotInitializedWhenAbsent),
            [
                "import",
                "baseline-upgrade",
                "repair-apply",
                "repair-verify",
                "test-run",
                "native-prepare"
            ]
        );
        assert_eq!(
            named(InstallationEntry::Outside),
            [
                "install",
                "update",
                "doctor",
                "help",
                "version",
                "completion"
            ]
        );
        assert_eq!(
            named(InstallationEntry::CommandOwnerDecides).len(),
            45 - 4 - 6 - 6
        );
    }
    #[test]
    fn ephemeral_leaves_the_creator_only_where_accepted() {
        use opensip_contracts::generated::invocation::Inventory3CommandName as C;
        assert_eq!(
            installation_entry(C::Analyze, true),
            Ok(InstallationEntry::Outside)
        );
        assert_eq!(
            installation_entry(C::Fit, true),
            Ok(InstallationEntry::Outside)
        );
        for command in [C::Default, C::Audit, C::Import, C::Help, C::RepairVerify] {
            assert_eq!(
                installation_entry(command, true),
                Err(InstallationEntryError::EphemeralNotAccepted)
            );
        }
    }
    #[test]
    fn not_initialized_applies_only_to_non_creators_that_need_the_installation() {
        use InstallationEntry::*;
        for entry in [
            Creator,
            NotInitializedWhenAbsent,
            CommandOwnerDecides,
            Outside,
        ] {
            assert_eq!(installation_precondition(entry, false), None);
        }
        assert_eq!(
            installation_precondition(NotInitializedWhenAbsent, true).map(|d| d.to_string()),
            Some("INSTALLATION.NOT_INITIALIZED".to_string())
        );
        for entry in [Creator, CommandOwnerDecides, Outside] {
            assert_eq!(installation_precondition(entry, true), None);
        }
    }
}
