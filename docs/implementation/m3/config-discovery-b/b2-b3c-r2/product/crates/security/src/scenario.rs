//! Law X8 r3 item 4 (unit X8b): security's test seam for the behavioural
//! refusal cases B0 to B8. It exists only under the test-only
//! `scenario-fixtures` feature, which only storage's and host's
//! `[dev-dependencies]` enable (item 4a), and it is `#[doc(hidden)]`. The
//! plain host surface has no `scenario` (group J's E0432), and no release
//! build compiles it (item 4f).
//!
//! It offers (item 4c):
//! - [`ScenarioHome::create`]: a synthetic P0 installation under a 0700
//!   scratch home below the caller's scratch parent, made by the real
//!   creator path over 462's signed test trees with InitialCore's injected
//!   loaded image and the synthetic V2 profile set, and X4T-0's signed
//!   accepted store for its S, its roles Trusted. Every path in it carries
//!   the label `synthetic`;
//! - [`ScenarioHome::project`]: a scratch project root under the home;
//! - [`ScenarioHome::operation`]: the production chain to a
//!   `ProjectOperation` (X1, X2, X3a, X4's lease-free first read and
//!   monitor, X3b's floor step and carrier start, X2e's handoff), through
//!   the one composition the shared installation fixture holds;
//! - [`publish_revocation_fenced`]: the shared fenced `state.v1` publisher,
//!   refused in any process that `operation` ever handed a lease to
//!   (item 5a: only the helper process calls it);
//! - [`revocation_version`], [`ScenarioHome::paths`] and
//!   [`ScenarioHome::carrier_census`]: read-only;
//! - [`ScenarioHome::compose_analysis_carriers`] (M3-B unit B1-b): the
//!   analysis path's first phase on an ordinary writer's gate, a decision the
//!   caller makes over the captured carrier bytes (the host's resolver and
//!   pack admission, in the host's tests), and item 5 only when it admits;
//!   it reports what reached the registry and I;
//! - [`ScenarioHome::discover`] (M3-B unit B2-b3c; B2-b3 plan r3,
//!   LD-B2B3-12): the analysis path on an ordinary writer's gate with an
//!   explicit path and the owner waiver, the caller's resolution of the
//!   captured carriers (the host's resolver with its flag layer), item 5,
//!   then the shared composition's tracking, first registration and
//!   handoff, and S3's downward walk on the operation's discovery root. It
//!   returns plain records only.
//!
//! What it never does (item 4e): it constructs no authority type itself
//! (the one exception is the `ProjectOperation` the production chain
//! returns from `operation`), and it accepts no receipt, guard, gate,
//! monitor, session, permit, `ReplayedRun` or clock from the caller. It
//! exposes no `FinalGate`, monitor clock or barrier point, and it adds no
//! gate of its own inside a production item: every fixture gate it reaches
//! is on unit X9-1's shared site list (item 4b). Synthetic fixtures; no
//! compiler qualification is claimed (build plan line 886).
use crate::InstallationTermination;
use crate::custody::installation_read_fixture::{InstallationAt, ReadFixture};
use crate::custody::operation_handoff::ProjectOperation;
use crate::trust::ReadProducers;
use std::cell::RefCell;
use std::fs;
use std::os::unix::fs::{DirBuilderExt, PermissionsExt};
use std::path::{Path, PathBuf};
use std::sync::atomic::{AtomicBool, Ordering};

/// Set once `operation` has handed this process an operation lease, and
/// never cleared: a `ProjectOperation` is the production type, so this seam
/// cannot observe its release. `publish_revocation_fenced` refuses while it
/// is set (item 4c).
static LEASE_HANDED_OUT: AtomicBool = AtomicBool::new(false);

/// The label every scratch path of a scenario home carries.
const LABEL: &str = "synthetic";

/// A synthetic installation under a scratch home. The one `create` made owns
/// its scratch tree and removes it on drop; one `open`ed by its paths (in a
/// helper process) owns nothing. It holds paths, and the signed test trees
/// of the operations it handed out, which live as long as it does.
pub struct ScenarioHome {
    at: InstallationAt,
    trees: RefCell<Vec<ReadProducers>>,
    _owned: Option<ReadFixture>,
}
impl std::fmt::Debug for ScenarioHome {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("ScenarioHome")
            .field("home", &self.at.home)
            .field("store", &self.at.store)
            .finish_non_exhaustive()
    }
}
/// M3-B unit B1-b (Codex B1B-R2-RF-02): what the analysis carrier
/// composition reached.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct CarrierCompositionOutcome {
    /// The caller's decision over the captured carriers admitted.
    pub admitted: bool,
    /// Item 5's registry capture ran (only after an admitting decision).
    pub registry_captured: bool,
    /// `project-registry.v2` is byte-identical afterwards: no RESERVED row.
    pub registry_unchanged: bool,
    /// Every member of I and of the project root is the same path and
    /// size afterwards, but the fence carrier: no lease, journal or marker.
    pub members_unchanged: bool,
    /// The writer, and with it the fence, was released: a new writer opens.
    pub writer_released: bool,
}

/// M3-B unit B2-b3c: one discovery the host's flag rows ask for. The waiver
/// is built from `trust_project_owner` and `explicit` by its own typed
/// constructor, exactly as an invocation builds it.
#[derive(Debug, Clone, Copy)]
pub struct DiscoveryRequest<'a> {
    pub launch: &'a Path,
    pub explicit: Option<&'a Path>,
    pub trust_project_owner: bool,
}
/// M3-B unit B2-b3c: what a discovery reached and recorded, as plain values.
/// It lends no authority.
#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct DiscoveryRecords {
    /// The resolution of the captured carriers ran (after phase 1).
    pub resolved: bool,
    /// Item 5 ran (after an admitting resolution).
    pub phase_two: bool,
    /// The downward walk ran (after the handoff released the fence).
    pub walked: bool,
    /// The upward mode and stop (`DiscoveryProvenanceV3`).
    pub mode: Option<String>,
    pub stop: Option<String>,
    pub custody_waiver: Option<String>,
    pub unit_source: Option<String>,
    /// Units and excluded units, spelled as found.
    pub units: Vec<String>,
    pub excluded: Vec<(String, String)>,
    /// A discovery refusal: its code and detail.
    pub refusal: Option<(String, String)>,
    /// The resolution's own refusal, as the caller reported it.
    pub resolution_refusal: Option<String>,
    /// The accepted result's `AdmittedBoundaryInventoryV3`, canonical JSON.
    pub inventory: Option<String>,
    /// The operation's end (r2, Codex B2B3C-R1-RF-1): whether its end step
    /// was entered, whether a capacity rollover ran, and the end-path
    /// failure's row, disclosed beside the discovery outcome it does not
    /// change.
    pub end_entered: bool,
    pub end_rolled_over: bool,
    pub end_failure: Option<String>,
}

/// Every regular file and directory under `root`, with its size.
fn members(root: &Path) -> Vec<(PathBuf, u64)> {
    let mut out = Vec::new();
    let mut stack = vec![root.to_path_buf()];
    while let Some(path) = stack.pop() {
        let Ok(meta) = fs::symlink_metadata(&path) else {
            continue;
        };
        if path
            .file_name()
            .is_some_and(|name| name == "lifecycle.fence")
        {
            continue;
        }
        out.push((path.clone(), if meta.is_dir() { 0 } else { meta.len() }));
        if meta.is_dir()
            && let Ok(entries) = fs::read_dir(&path)
        {
            for entry in entries.flatten() {
                stack.push(entry.path());
            }
        }
    }
    out.sort();
    out
}

impl ScenarioHome {
    /// Publish a synthetic P0 installation under a new 0700 directory below
    /// `parent`, the caller's scratch parent, and install X4T-0's signed
    /// accepted store for its S (revocation list version 1, no entries).
    /// Panics if the fixture cannot be made, as every fixture does.
    pub fn create(parent: &Path) -> Self {
        let draw: String = opensip_platform::request_entropy()
            .expect("entropy")
            .iter()
            .map(|b| format!("{b:02x}"))
            .collect();
        let scratch = parent.join(format!("x8-{LABEL}-{draw}"));
        fs::DirBuilder::new()
            .mode(0o700)
            .create(&scratch)
            .unwrap_or_else(|e| panic!("scenario scratch {}: {e}", scratch.display()));
        let fixture = ReadFixture::new_in(&format!("x8-{LABEL}"), Some(&scratch));
        let at = fixture.at();
        at.install_accepted_trust(Vec::new(), 1, Some(fixture_wall_seconds()))
            .unwrap_or_else(|e| panic!("accepted store: {e}"));
        Self {
            at,
            trees: RefCell::new(Vec::new()),
            _owned: Some(fixture),
        }
    }
    /// A scenario home another process created, by its paths (item 5a's
    /// helper process). It owns nothing and removes nothing.
    pub fn open(home: &Path, installation: &Path, store: &str) -> Self {
        Self {
            at: InstallationAt {
                home: home.to_owned(),
                installation: installation.to_owned(),
                store: store.to_owned(),
            },
            trees: RefCell::new(Vec::new()),
            _owned: None,
        }
    }
    /// The scratch H.
    pub fn home(&self) -> &Path {
        &self.at.home
    }
    /// I, under the scratch H.
    pub fn installation(&self) -> &Path {
        &self.at.installation
    }
    /// The store S the creator drew.
    pub fn store(&self) -> &str {
        &self.at.store
    }
    /// A scratch project root `H/code/<name>`, 0755 with no ACL, as on a
    /// stock Mac. Panics if it cannot be made or already exists.
    pub fn project(&self, name: &str) -> PathBuf {
        let code = self.at.home.join("code");
        if !code.exists() {
            fs::create_dir(&code).unwrap();
            fs::set_permissions(&code, fs::Permissions::from_mode(0o755)).unwrap();
        }
        let root = code.join(name);
        fs::create_dir(&root).unwrap_or_else(|e| panic!("project {name}: {e}"));
        fs::set_permissions(&root, fs::Permissions::from_mode(0o755)).unwrap();
        root
    }
    /// The production chain to `root`'s `ProjectOperation` under an
    /// `APPEND_WRITE` lease (item 4c): X1's write admission, X2's root
    /// admission, first registration when the root is a first-use candidate,
    /// namespace and lease, X3a's endpoint, X4's lease-free monitor and first
    /// read, X3b's floor step and carrier start, then X2e's handoff. A
    /// refusal is its row (X3d r6 item 9's vocabulary), with the writer and
    /// its fence released.
    pub fn operation(&self, root: &Path) -> Result<ProjectOperation, InstallationTermination> {
        let (operation, trees) = self.at.operation(
            root,
            crate::custody::namespace_lease::WriterLease::AppendWrite,
        )?;
        LEASE_HANDED_OUT.store(true, Ordering::SeqCst);
        self.trees.borrow_mut().push(trees);
        Ok(operation)
    }
    /// The analysis carrier composition (M3-B unit B1-b; X2 r9 item 3a's
    /// order): an ordinary writer on this I, the analysis path's first
    /// phase for `root` (selection retaining `opensip.json`, the chain,
    /// incarnation, marker and carriers; `interactive` decides the local
    /// carrier), then `decide` over the captured carrier bytes, then item 5
    /// only when it returns true. The writer is then dropped. Nothing here
    /// registers a project or takes a lease.
    pub fn compose_analysis_carriers(
        &self,
        root: &Path,
        interactive: bool,
        decide: impl FnOnce(Option<&[u8]>, Option<&[u8]>) -> bool,
    ) -> Result<CarrierCompositionOutcome, String> {
        use crate::custody::project_admission::LocalCarrierPolicy;
        let registry = self.at.installation.join("project-registry.v2");
        let registry_before = fs::read(&registry).map_err(|e| e.to_string())?;
        let members_before = (members(&self.at.installation), members(root));
        let groups = std::collections::BTreeSet::new();
        let local = if interactive {
            LocalCarrierPolicy::Interactive
        } else {
            LocalCarrierPolicy::NonInteractive
        };
        let (admitted, registry_captured) = {
            let (mut writer, _trees) = self.at.writer()?;
            let carriers = writer
                .admit_project_carriers(
                    root,
                    None,
                    &groups,
                    local,
                    None,
                    &mut crate::custody::project_admission::UpwardRecord::default(),
                )
                .map_err(|refusal| format!("{refusal:?}"))?;
            let project = carriers.carriers().project().map(|c| c.bytes().to_vec());
            let local = carriers.carriers().local().map(|c| c.bytes().to_vec());
            if decide(project.as_deref(), local.as_deref()) {
                writer
                    .complete_project_admission(carriers, &groups, None)
                    .map_err(|refusal| format!("{refusal:?}"))?;
                (true, true)
            } else {
                drop(carriers);
                (false, false)
            }
        };
        Ok(CarrierCompositionOutcome {
            admitted,
            registry_captured,
            registry_unchanged: fs::read(&registry).map_err(|e| e.to_string())? == registry_before,
            members_unchanged: (members(&self.at.installation), members(root)) == members_before,
            writer_released: self.at.writer().is_ok(),
        })
    }
    /// M3-B unit B2-b3c (B2-b3 plan r3, LD-B2B3-12): one discovery on an
    /// ordinary writer, in law order: analysis phase 1 with the explicit path
    /// and the typed owner waiver; `resolve` over the captured carriers (the
    /// host's resolver with its flag layer and pack admission), returning the
    /// winning `discovery.workspaceRoots`, none, or a refusal; item 5 with the
    /// waiver; tracking, first registration when the root is a first-use
    /// candidate, and the handoff, as the shared composition makes them; then
    /// the operation's discovery root, S3's walk and the core on a fresh
    /// discovery ledger, with the unit source chosen before traversal; then
    /// the operation's end. A selection or resolution refusal ends the
    /// discovery there, the writer released, with nothing further observed.
    /// Other refusals are `Err`.
    pub fn discover(
        &self,
        request: &DiscoveryRequest<'_>,
        resolve: impl FnOnce(Option<&[u8]>, Option<&[u8]>) -> Result<Option<Vec<String>>, String>,
    ) -> Result<DiscoveryRecords, String> {
        use crate::custody::discovery_rule::MarkerCountBasis;
        use crate::custody::discovery_scan::{
            DiscoveryInvocation, DiscoveryResultPending, UnitSourceRequest, boundary_inventory,
        };
        use crate::custody::discovery_walk::discover_downward;
        use crate::custody::first_registration::{ProjectInputs, ProjectWriteRefusal, Seam};
        use crate::custody::namespace_lease::{NamespaceSubject, WriterLease};
        use crate::custody::operation_handoff::JournalOutcome;
        use crate::custody::project_admission::{Classification, LocalCarrierPolicy, UpwardRecord};
        use crate::grants::{AuthorizedGroups, ProjectOwnerWaiver};
        use opensip_platform::{WorkFailure, WorkLedger};
        use std::os::unix::fs::MetadataExt;
        let groups = std::collections::BTreeSet::new();
        let authorized = AuthorizedGroups::from_invocation(&[]).map_err(|e| format!("{e:?}"))?;
        let waiver =
            ProjectOwnerWaiver::from_invocation(request.trust_project_owner, request.explicit)
                .map_err(|e| format!("{e:?}"))?;
        let uid = fs::metadata(&self.at.home)
            .map_err(|e| e.to_string())?
            .uid();
        let explicit = request.explicit.is_some();
        let mut records = DiscoveryRecords {
            custody_waiver: waiver.as_ref().map(|_| "trustProjectOwner".to_owned()),
            ..DiscoveryRecords::default()
        };
        let mut upward = UpwardRecord::default();
        let (mut writer, trees) = self.at.writer()?;
        // 1. Phase 1, recording selection's upward provenance.
        let carriers = match writer.admit_project_carriers(
            request.launch,
            request.explicit,
            &groups,
            LocalCarrierPolicy::NonInteractive,
            waiver.as_ref(),
            &mut upward,
        ) {
            Ok(carriers) => carriers,
            Err(ProjectWriteRefusal::Project(WorkFailure::Operation(refusal))) => {
                let Some((code, detail, _)) = upward.discovery_refusal(&refusal, explicit) else {
                    return Err(format!("{refusal:?}"));
                };
                records.refusal = Some((code.code().to_owned(), detail.to_owned()));
                records.mode = Some(if explicit { "explicit" } else { "walk" }.to_owned());
                return Ok(records);
            }
            Err(refusal) => return Err(format!("{refusal:?}")),
        };
        // 2. The caller's resolution and pack admission.
        records.resolved = true;
        let project = carriers.carriers().project().map(|c| c.bytes().to_vec());
        let local = carriers.carriers().local().map(|c| c.bytes().to_vec());
        let roots = match resolve(project.as_deref(), local.as_deref()) {
            Ok(roots) => roots,
            Err(refusal) => {
                records.resolution_refusal = Some(refusal);
                return Ok(records);
            }
        };
        let selected = carriers.selected().clone();
        // 3. Item 5.
        let admission = writer
            .complete_project_admission(carriers, &groups, waiver.as_ref())
            .map_err(|refusal| format!("{refusal:?}"))?;
        records.phase_two = true;
        let provenance = upward
            .provenance(&selected)
            .ok_or_else(|| "a selection spelling is not UTF-8".to_owned())?;
        records.mode = Some(provenance.mode.clone());
        records.stop = Some(provenance.stop_reason.clone());
        // 4. The shared composition's tracking, first registration and handoff.
        let inputs = ProjectInputs {
            trust_groups: &groups,
            environment: &[],
            system_sources: &[],
        };
        let tracking = writer
            .observe_project_tracking_with(&admission, &inputs)
            .map_err(|refusal| format!("{refusal:?}"))?;
        let subject = if matches!(
            admission.classification(),
            Classification::FirstUseCandidate
        ) {
            NamespaceSubject::Registered(
                writer
                    .register_first_use_with(admission, tracking, &inputs, &Seam::live())
                    .map_err(|refusal| format!("{refusal:?}"))?,
            )
        } else {
            NamespaceSubject::Eligible {
                admission,
                tracking,
            }
        };
        let drawn = |prefix: &str| -> Result<String, String> {
            let bytes = opensip_platform::request_entropy().map_err(|e| format!("{e:?}"))?;
            Ok(bytes
                .iter()
                .fold(prefix.to_owned(), |id, b| format!("{id}{b:02x}")))
        };
        let invocation = crate::trust::TrustInvocation::new(&drawn("req1_")?, &drawn("exec1_")?, 0)
            .ok_or_else(|| "invocation".to_owned())?;
        let operation = writer
            .begin_operation(subject, WriterLease::AppendWrite, &inputs, &invocation)
            .map_err(|refusal| format!("{refusal:?}"))?;
        LEASE_HANDED_OUT.store(true, Ordering::SeqCst);
        self.trees.borrow_mut().push(trees);
        // 5. The walk and the core, the source chosen before traversal.
        let source = match roots {
            Some(roots) => UnitSourceRequest::ConfigWorkspaceRoots(roots),
            None => UnitSourceRequest::Automatic,
        };
        let members = std::collections::BTreeSet::new();
        let invocation = DiscoveryInvocation {
            invoking_uid: uid,
            ci: false,
            groups: &authorized,
            waiver: waiver.as_ref(),
            source,
            basis: MarkerCountBasis::NotEnumerated,
            member_roots: &members,
        };
        let result = {
            let root = operation.discovery_root();
            WorkLedger::discovery_profile()
                .scope(|work| discover_downward(&root, provenance, &invocation, work))
        };
        // 6. The end, disclosed beside the discovery outcome.
        let end = operation.end(JournalOutcome::Certain);
        records.end_entered = end.entered();
        records.end_rolled_over = matches!(
            end,
            crate::custody::operation_handoff::OperationEnd::RolledOver { .. }
        );
        records.end_failure = end.failure().map(|failure| format!("{:?}", failure.row()));
        records.walked = true;
        let result = match result {
            Ok(result) => result,
            Err(WorkFailure::Operation(refusal)) => match refusal.discovery_refusal() {
                Some((code, detail)) => {
                    records.refusal = Some((code.code().to_owned(), detail));
                    return Ok(records);
                }
                None => return Err(format!("{refusal:?}")),
            },
            Err(failure) => return Err(format!("{failure:?}")),
        };
        let provenance = match &result {
            DiscoveryResultPending::Accept(provenance) => provenance,
            DiscoveryResultPending::Refuse {
                refusal,
                detail,
                provenance,
                ..
            } => {
                records.refusal = Some((refusal.code().to_owned(), detail.clone()));
                provenance
            }
        };
        records.unit_source = Some(provenance.unit_source.to_owned());
        records.units = provenance.units.iter().map(|u| u.path.clone()).collect();
        records.excluded = provenance
            .excluded_units
            .iter()
            .map(|u| (u.path.clone(), u.reason.clone()))
            .collect();
        // An accepted result's inventory must convert; a locator fault is an
        // instrument error, never a missing inventory (r2, Codex
        // B2B3C-R1-NBO-1).
        if matches!(result, DiscoveryResultPending::Accept(_)) {
            let inventory = boundary_inventory(&result).map_err(|e| format!("{e:?}"))?;
            let bytes = opensip_identity::canonical_bytes(&inventory.to_json())
                .map_err(|e| format!("{e:?}"))?;
            records.inventory = Some(String::from_utf8(bytes).map_err(|e| e.to_string())?);
        }
        Ok(records)
    }
    /// The read-only paths of a project root and its namespace N (item 4c).
    /// Nothing is opened or checked.
    pub fn paths(&self, root: &Path, namespace: &str) -> ScenarioPaths {
        let i = &self.at.installation;
        let s = &self.at.store;
        let dot_opensip = root.join(".opensip");
        let namespace_dir = i.join("host/projects").join(namespace);
        let lineage = fs::read(i.join("selection.pair"))
            .ok()
            .and_then(|raw| opensip_identity::DecodedSelectionV1::decode(&raw).ok())
            .map(|pair| {
                i.join(format!(
                    "transitions/lineage/{s}/{}/{}.node",
                    pair.store_generation(),
                    pair.state_schema()
                ))
            });
        ScenarioPaths {
            root: root.to_owned(),
            marker: dot_opensip.join("project-id.v1"),
            dot_opensip,
            writer_lease: namespace_dir.join("writer.lease"),
            readers_lease: namespace_dir.join("readers.lease"),
            namespace: namespace_dir,
            selection: i.join("selection.pair"),
            store_marker: i.join(format!("stores/{s}/store-instance.v1")),
            lineage,
        }
    }
    /// A read-only count of N's carrier records by kind (item 4c). A
    /// namespace with no carrier file counts nothing.
    pub fn carrier_census(&self, namespace: &str) -> Result<CarrierCensus, String> {
        let path = self
            .at
            .installation
            .join("host/projects")
            .join(namespace)
            .join("grant-journal.sqlite");
        let mut census = CarrierCensus::default();
        if !path.exists() {
            return Ok(census);
        }
        let c = rusqlite::Connection::open_with_flags(
            &path,
            rusqlite::OpenFlags::SQLITE_OPEN_READ_ONLY
                | rusqlite::OpenFlags::SQLITE_OPEN_NO_MUTEX
                | rusqlite::OpenFlags::SQLITE_OPEN_NOFOLLOW,
        )
        .map_err(|e| format!("carrier: {e}"))?;
        let mut statement = c
            .prepare("SELECT record_type, count(*) FROM grant_journal_v3 GROUP BY record_type")
            .map_err(|e| format!("carrier: {e}"))?;
        let rows = statement
            .query_map([], |r| Ok((r.get::<_, String>(0)?, r.get::<_, i64>(1)?)))
            .map_err(|e| format!("carrier: {e}"))?;
        for row in rows {
            let (kind, count) = row.map_err(|e| format!("carrier: {e}"))?;
            let count = u64::try_from(count).map_err(|e| format!("carrier: {e}"))?;
            match kind.as_str() {
                "SEAL" => census.seal = count,
                "REV" => census.rev = count,
                "CLN" => census.cln = count,
                "TERMINAL" => census.terminal = count,
                _ => census.other += count,
            }
        }
        Ok(census)
    }
}

/// The read-only paths `ScenarioHome::paths` names: the project root, its
/// `.opensip` directory and marker, N's directory and lease files, and the
/// selected store endpoint's files (the selection pair, S's marker, and the
/// lineage node of the selected generation, if the pair decodes).
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ScenarioPaths {
    pub root: PathBuf,
    pub dot_opensip: PathBuf,
    pub marker: PathBuf,
    pub namespace: PathBuf,
    pub writer_lease: PathBuf,
    pub readers_lease: PathBuf,
    pub selection: PathBuf,
    pub store_marker: PathBuf,
    pub lineage: Option<PathBuf>,
}

/// N's carrier records by kind; `other` counts every other kind.
#[derive(Debug, Clone, Copy, Default, PartialEq, Eq)]
pub struct CarrierCensus {
    pub seal: u64,
    pub rev: u64,
    pub cln: u64,
    pub terminal: u64,
    pub other: u64,
}

/// The revocation version of `state.v1` before and after a publication.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct RevocationVersions {
    pub before: u64,
    pub after: u64,
}

/// Item 5a's publication, through the shared fenced publisher (item 4b): a
/// write gate takes I's fence by its production walk; X4T-0's signed
/// accepted store for S is published with a revocation list naming
/// `subjects`, each `(subjectKind, subject)`, at the next list version, by
/// the trust owner's protocol with `state.v1` replaced last; the fence is
/// released. An empty `subjects` is a revocation that names nothing in any
/// closure. Returns the revocation version before and after.
///
/// It refuses, writing nothing, in a process that `operation` ever handed
/// an operation lease (law X4 r7 item 2: no trust write under a lease), and
/// for a subject kind the revocation list does not have (the invariant row
/// either way). Its other refusals are the publisher's rows.
pub fn publish_revocation_fenced(
    home: &ScenarioHome,
    subjects: &[(&str, &str)],
) -> Result<RevocationVersions, InstallationTermination> {
    use InstallationTermination as T;
    if LEASE_HANDED_OUT.load(Ordering::SeqCst) {
        return Err(T::Invariant);
    }
    let mut revocations = Vec::new();
    for (kind, subject) in subjects {
        let kind: &'static str = match *kind {
            "release" => "release",
            "keyId" => "keyId",
            "namespace" => "namespace",
            "catalogSnapshot" => "catalogSnapshot",
            _ => return Err(T::Invariant),
        };
        revocations.push((kind, (*subject).to_owned()));
    }
    let (_, current) = home.at.current_trust_values().map_err(|_| T::Invariant)?;
    let next = current.checked_add(1).ok_or(T::Invariant)?;
    let (before, after) = home
        .at
        .publish_trust_fenced(revocations, next, Some(fixture_wall_seconds()))
        .map_err(|refusal| refusal.termination())?;
    let version = |v: i128| u64::try_from(v).map_err(|_| T::Invariant);
    Ok(RevocationVersions {
        before: version(before)?,
        after: version(after)?,
    })
}

/// The revocation version of `trust/stores/S/state.v1`, read by name (0
/// while the capsule carries no retained clock record). Read-only: it takes
/// no fence, writes nothing, admits nothing and returns no authority type.
/// Panics if the home's `state.v1` cannot be read, which is a broken
/// scenario home.
pub fn revocation_version(home: &ScenarioHome) -> u64 {
    let (_, version) = home
        .at
        .current_trust_values()
        .unwrap_or_else(|e| panic!("revocation version: {e}"));
    u64::try_from(version).unwrap_or_else(|e| panic!("revocation version: {e}"))
}

#[cfg(test)]
#[path = "scenario_tests.rs"]
mod tests;

// F9: only native-clock scenarios choose this calendar. X9's shared callers
// continue to pass None, preserving clockEpoch, point ordinals and readings.
fn fixture_wall_seconds() -> i64 {
    i64::try_from(
        std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .expect("fixture wall after epoch")
            .as_secs(),
    )
    .expect("fixture wall fits timestamp")
}
