// M3-B r5 item 23 (unit B3-a): the invocation's authorization records and
// S3.1's backup custody choice. Each record is built only from a primitive
// value the invocation parse holds (SL:127-130): there is no `From`,
// `TryFrom`, `Default`, `Deserialize` or configuration constructor, and no
// record is `Clone`, so a record is consumed where it is used. Applicability
// is the consumers' (project custody, B2-b and B3-b); this module applies
// none of it. Execution, mutation and recovery grants are not M3's. Library
// only: pure, no I/O, no environment.
use crate::InstallationTermination;
use crate::initial_installation::BackupClassification;
use std::collections::BTreeSet;
use std::path::{Path, PathBuf};

/// SLS `authorizedGroupIds` `maxItems`: distinct gids one invocation may
/// authorize.
pub(crate) const MAX_AUTHORIZED_GROUPS: usize = 64;

/// Why an invocation value cannot become a record.
#[derive(Debug, PartialEq, Eq)]
pub(crate) enum GrantRefusal {
    /// More than 64 distinct `--trust-group` gids (LD-B3A-2: an internal
    /// refusal; the public row is the CLI's, M4).
    TooManyGroups { count: usize },
    /// `--trust-project-owner` without an explicit `--project` path
    /// (SLM:832-833).
    OwnerWaiverWithoutExplicitProject,
    /// A storage-policy record id that is not 64 lowercase hex digits.
    PolicyRecordId,
}
impl GrantRefusal {
    /// The existing public row, where M3 has one.
    pub(crate) fn termination(&self) -> Option<InstallationTermination> {
        match self {
            Self::OwnerWaiverWithoutExplicitProject => {
                Some(InstallationTermination::ProjectExplicitPath)
            }
            Self::TooManyGroups { .. } | Self::PolicyRecordId => None,
        }
    }
}

/// The explicitly authorized `--trust-group` set (S3). A gid named twice
/// authorizes once (LD-B3A-3); provenance keeps first-occurrence order (SLS
/// `x-opensip-order: sequence`).
#[derive(Debug, PartialEq, Eq)]
pub(crate) struct AuthorizedGroups {
    provenance: Vec<u32>,
    set: BTreeSet<u32>,
}
impl AuthorizedGroups {
    pub(crate) fn from_invocation(gids: &[u32]) -> Result<Self, GrantRefusal> {
        let mut provenance = Vec::new();
        let mut set = BTreeSet::new();
        for &gid in gids {
            if set.insert(gid) {
                provenance.push(gid);
            }
        }
        if provenance.len() > MAX_AUTHORIZED_GROUPS {
            return Err(GrantRefusal::TooManyGroups {
                count: provenance.len(),
            });
        }
        Ok(Self { provenance, set })
    }
    pub(crate) fn contains(&self, gid: u32) -> bool {
        self.set.contains(&gid)
    }
    /// The distinct gids in first-occurrence order, for provenance.
    pub(crate) fn provenance(&self) -> &[u32] {
        &self.provenance
    }
    /// The set project custody judges group and ACL grants against.
    pub(crate) fn as_set(&self) -> &BTreeSet<u32> {
        &self.set
    }
}

/// `--trust-project-owner` with its explicit `--project` root. It waives only
/// the owner check, on that root's directories and its `opensip.json`; never
/// on marker files, member Git evidence or `local.json` (SLM:636, 665,
/// 669-680; MB item 23). Its consumers apply that scope.
#[derive(Debug, PartialEq, Eq)]
pub(crate) struct ProjectOwnerWaiver {
    explicit_root: PathBuf,
}
impl ProjectOwnerWaiver {
    pub(crate) fn from_invocation(
        trust_project_owner: bool,
        explicit_project: Option<&Path>,
    ) -> Result<Option<Self>, GrantRefusal> {
        match (trust_project_owner, explicit_project) {
            (false, _) => Ok(None),
            (true, None) => Err(GrantRefusal::OwnerWaiverWithoutExplicitProject),
            (true, Some(root)) => Ok(Some(Self {
                explicit_root: root.to_path_buf(),
            })),
        }
    }
    /// The explicit root's spelling, as the invocation gave it.
    pub(crate) fn explicit_root(&self) -> &Path {
        &self.explicit_root
    }
}

/// This invocation's `--allow-backup-custody`. It is consumed only by the
/// S3.1 choice, and is not a network-export or shared-storage grant.
#[derive(Debug, PartialEq, Eq)]
pub(crate) struct BackupCustodyAcknowledgement {
    _invocation: (),
}
impl BackupCustodyAcknowledgement {
    pub(crate) fn from_invocation(allow_backup_custody: bool) -> Option<Self> {
        allow_backup_custody.then_some(Self { _invocation: () })
    }
}

/// An admitted storage-policy record's id: 64 lowercase hex digits.
#[derive(Debug, PartialEq, Eq)]
pub(crate) struct PolicyRecordId(String);
impl PolicyRecordId {
    pub(crate) fn parse(text: &str) -> Result<Self, GrantRefusal> {
        let lowercase_hex = |b: &u8| b.is_ascii_digit() || (b'a'..=b'f').contains(b);
        if text.len() == 64 && text.as_bytes().iter().all(lowercase_hex) {
            Ok(Self(text.to_owned()))
        } else {
            Err(GrantRefusal::PolicyRecordId)
        }
    }
    pub(crate) fn as_str(&self) -> &str {
        &self.0
    }
}

/// The workflow contract's `consentSource`. Typed only: its consumers are
/// M5's.
#[derive(Debug, PartialEq, Eq)]
pub(crate) enum ConsentSource {
    PreExistingPolicy { record: PolicyRecordId },
    InteractiveConsent,
}
impl ConsentSource {
    /// The workflow spelling.
    pub(crate) fn workflow(&self) -> &'static str {
        match self {
            Self::PreExistingPolicy { .. } => "pre-existing-policy",
            Self::InteractiveConsent => "interactive-consent",
        }
    }
    /// The grant's authorization mode it maps to (SL:1110).
    pub(crate) fn grant_mode(&self) -> &'static str {
        match self {
            Self::PreExistingPolicy { .. } => "policy-record",
            Self::InteractiveConsent => "interactive-explicit",
        }
    }
}

/// What admitted the first source-derived write into a project store.
#[derive(Debug, PartialEq, Eq)]
pub(crate) enum StorageWriteBasis<'a> {
    Ephemeral,
    NotRequired,
    /// UNKNOWN is disclosed as unknown, never as not-backed-up.
    UnknownDisclosed,
    InvocationFlag,
    AdmittedPolicyRecord(&'a PolicyRecordId),
}

/// S3.1's decision (SLM `storage_write_admission`).
#[derive(Debug, PartialEq, Eq)]
pub(crate) enum StorageWriteChoice<'a> {
    Admit(StorageWriteBasis<'a>),
    /// `REQUEST.PRECONDITION_FAILED` / `storage.backup-choice-required`.
    Refuse {
        ci: bool,
    },
}
impl StorageWriteChoice<'_> {
    /// The choice never writes a policy file.
    pub(crate) const POLICY_FILE_WRITTEN: bool = false;
    /// The choice never changes a root identity.
    pub(crate) const ROOT_IDENTITY_CHANGED: bool = false;

    /// The reference's `choice` spelling.
    pub(crate) fn choice(&self) -> String {
        match self {
            Self::Admit(StorageWriteBasis::Ephemeral) => "ephemeral".to_owned(),
            Self::Admit(StorageWriteBasis::NotRequired) => "not-required".to_owned(),
            Self::Admit(StorageWriteBasis::UnknownDisclosed) => "unknown-disclosed".to_owned(),
            Self::Admit(StorageWriteBasis::InvocationFlag) => "invocation-flag".to_owned(),
            Self::Admit(StorageWriteBasis::AdmittedPolicyRecord(id)) => {
                format!("admitted-policy-record:{}", id.as_str())
            }
            Self::Refuse { ci: true } => "interactive-prompt-unavailable".to_owned(),
            Self::Refuse { ci: false } => "interactive-choice-required".to_owned(),
        }
    }
    /// The existing public row a refusal ends in.
    pub(crate) fn termination(&self) -> Option<InstallationTermination> {
        match self {
            Self::Admit(_) => None,
            Self::Refuse { .. } => Some(InstallationTermination::BackupChoiceRequired),
        }
    }
}

/// S3.1 before the first source-derived write, in the reference's order:
/// ephemeral; then NOT_BACKED_UP or UNKNOWN; then this invocation's
/// acknowledgement; then an admitted storage-policy record; else refuse.
/// `ephemeral` is the host's `Durability::Ephemeral` (LD-B3A-1).
pub(crate) fn storage_write_choice(
    backup: BackupClassification,
    ephemeral: bool,
    acknowledgement: Option<BackupCustodyAcknowledgement>,
    admitted_policy: Option<&PolicyRecordId>,
    ci: bool,
) -> StorageWriteChoice<'_> {
    if ephemeral {
        return StorageWriteChoice::Admit(StorageWriteBasis::Ephemeral);
    }
    match backup {
        BackupClassification::NotBackedUp => {
            return StorageWriteChoice::Admit(StorageWriteBasis::NotRequired);
        }
        BackupClassification::Unknown => {
            return StorageWriteChoice::Admit(StorageWriteBasis::UnknownDisclosed);
        }
        BackupClassification::BackedUp => {}
    }
    if acknowledgement.is_some() {
        return StorageWriteChoice::Admit(StorageWriteBasis::InvocationFlag);
    }
    if let Some(id) = admitted_policy {
        return StorageWriteChoice::Admit(StorageWriteBasis::AdmittedPolicyRecord(id));
    }
    StorageWriteChoice::Refuse { ci }
}

#[cfg(test)]
#[path = "grants_tests.rs"]
mod tests;
