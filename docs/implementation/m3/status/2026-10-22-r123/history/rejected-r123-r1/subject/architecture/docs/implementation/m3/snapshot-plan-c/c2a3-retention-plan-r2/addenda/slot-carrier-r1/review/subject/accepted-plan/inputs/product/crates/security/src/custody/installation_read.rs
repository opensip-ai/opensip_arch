// Law 458c r5 item 8 (unit 458c-b2): the observation kept for the
// installation readers. After item 5 admitted a complete I, the read
// session holds the fence, the retained chain, the account and the read
// receipt, and every later capture and recheck is charged to the
// observation session's own ledger before it runs (item 6). A capture opens
// only through the retained I and its retained descendants; nothing walks
// from the root again, and `NativeInstallationFence::try_acquire` and
// `inspect_directory_path` are never called. Each capture is a member read
// (item 5 step 3): its failures are values, so the full recheck (step 4)
// still runs after it, over the fence, the observation's required files and
// every file captured since. Any refusal latches the session. Between full
// rechecks, a capture's own recheck samples the held fence, its retained
// edges and its file. Never a write capability. Library only.
use super::installation_admission::{
    CustodyRefusal, Entry, Failure, GateRefusal, IoFailure, RequiredFile, flatten, judge_capture,
    missing, private_file, recheck_chain, recheck_files,
};
use super::installation_admission::ChainPolicy;
use super::installation_fence::{self, HeldFence};
use super::installation_session::{InstallationObservation, SessionRefusal};
use super::store_endpoint::{SelectedStoreEndpoint, validate_endpoint};
use super::read_premise::{ReadPremiseQualification, ReadPremiseReceipt};
use crate::private_access::{PrivateObjectKind, assess_private_descendant_capture};
use opensip_platform::{
    DescriptorAclCapture, DescriptorFilesystem, DescriptorMetadata, RetainedDirectory,
    WorkBudgetError, WorkCost, WorkFailure, WorkLedger, WorkReadFailure, WorkScope, capture_descriptor_acl_observed,
    descriptor_filesystem_observation_cost, descriptor_name_matches,
    descriptor_name_observation_cost, open_child_directory_cost, read_bounded_observed,
};
use std::{cell::RefCell, collections::BTreeSet, ffi::OsStr, fs::File, io};

/// A complete, admitted I held for its readers. Private, not Clone, not
/// Sync. The observation is fixed; the ledger, the receipt and the files
/// captured since change under one `RefCell`, borrowed only for the length
/// of one charged step.
pub(crate) struct ReadSession {
    observation: InstallationObservation,
    /// Supplied groups are never admitted on this path: every judgment is
    /// the owner's.
    groups: BTreeSet<u32>,
    state: RefCell<State>,
}
struct State {
    ledger: WorkLedger,
    latched: bool,
    receipt: ReadPremiseReceipt,
    captured: Vec<RequiredFile>,
    /// M3-B unit B1-b: optional members observed absent, each with its
    /// judged existing parents; each stays absent under the same owners.
    absent: Vec<AbsentObservation>,
}

/// A read session after its equivalent release (M3-B r5 item 12; unit
/// B2-b3a): no fence, no installation handle and no ledger, only this
/// invocation's read receipt. Its one lending is `discovery_root`.
pub(crate) struct ReleasedRead {
    receipt: ReadPremiseReceipt,
}
impl std::fmt::Debug for ReleasedRead {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("ReleasedRead").finish_non_exhaustive()
    }
}
impl ReleasedRead {
    /// The discovery walk's view of an admission made by this session
    /// (LD-B2B3-1): the admission's retained root, the receipt's omission
    /// premise and its check that a filesystem is H's. Nothing else.
    pub(crate) fn discovery_root<'a>(
        &'a self,
        admission: &'a super::project_admission::ProjectRootAdmission,
    ) -> super::project_chain::DiscoveryRoot<'a> {
        super::project_chain::DiscoveryRoot::lend_read(admission.chain(), self.receipt.qualification())
    }
}

/// What a charged step sees: the retained I, the invoking user and the
/// receipt's check that a filesystem is H's.
pub(super) struct Held<'a> {
    installation: &'a RetainedDirectory,
    uid: u32,
    home_filesystem: &'a dyn Fn(&DescriptorFilesystem) -> bool,
}

/// One capture: every retained edge below I, the retained file, its bytes
/// and its samples. Nothing here is a descriptor escape.
pub(crate) struct Capture {
    edges: Vec<Edge>,
    file: File,
    leaf: String,
    relative: String,
    metadata: DescriptorMetadata,
    filesystem: DescriptorFilesystem,
    raw: Vec<u8>,
}
struct Edge {
    directory: RetainedDirectory,
    relative: String,
    metadata: DescriptorMetadata,
    filesystem: DescriptorFilesystem,
}
/// M3-B unit B1-b (LD-B1B-2; Codex B1B-R1-RF-02): an optional member's
/// positive absence under judged parents. `edges` are the existing prefixes,
/// each judged as a capture judges it (private custody, exact name, H's
/// filesystem), with the full sample of that judgment; `absent` is the
/// relative path of the first absent component.
pub(crate) struct AbsentObservation {
    edges: Vec<(String, DescriptorMetadata)>,
    absent: String,
}
/// What one capture attempt found: the member, or (optional only) its
/// first absent component under judged parents.
enum Captured {
    Present(Capture),
    Absent(AbsentObservation),
}
impl Capture {
    pub(crate) fn raw(&self) -> &[u8] {
        &self.raw
    }
    pub(crate) fn filesystem(&self) -> &DescriptorFilesystem {
        &self.filesystem
    }
}

/// A tracking observation's refusal on the read session: the session's
/// own, or the observation's (law X2 item 8).
#[derive(Debug)]
pub(crate) enum TrackingSessionRefusal {
    Session(SessionRefusal),
    Tracking(super::git_tracking::Failure),
}

/// A namespace admission's or lease's refusal on the read session: the
/// session's own, or item 7's (law X2 item 8).
#[derive(Debug)]
pub(crate) enum NamespaceSessionRefusal {
    Session(SessionRefusal),
    Namespace(super::namespace_lease::Failure),
}

/// A project admission's refusal on the read session: the session's own
/// (receipt, latch or recheck), or the project admission's (law X2 item 8).
#[derive(Debug)]
pub(crate) enum ProjectSessionRefusal {
    Session(SessionRefusal),
    Project(super::project_admission::Failure),
}

impl ReadSession {
    pub(super) fn new(
        ledger: WorkLedger,
        receipt: ReadPremiseReceipt,
        observation: InstallationObservation,
    ) -> Self {
        Self {
            observation,
            groups: BTreeSet::new(),
            state: RefCell::new(State {
                ledger,
                latched: false,
                receipt,
                captured: Vec::new(),
                absent: Vec::new(),
            }),
        }
    }
    pub(crate) fn uid(&self) -> u32 {
        self.observation.account().uid()
    }
    pub(crate) fn installation(&self) -> &RetainedDirectory {
        self.observation.chain().installation()
    }
    pub(crate) fn is_latched(&self) -> bool {
        let state = self.state.borrow();
        state.latched || state.ledger.is_failed()
    }
    /// The session ledger's cumulative use.
    pub(crate) fn used(&self) -> WorkCost {
        self.state.borrow().ledger.used()
    }
    fn latch(&self) {
        self.state.borrow_mut().latched = true;
    }

    /// Law X3a r3 items 1 and 2: the selected store endpoint of this complete
    /// I, admitted from the observation's one read. The decoded values are
    /// validated in memory, charged on the session ledger, against the read
    /// receipt's selected core; then one full session recheck runs. No file
    /// is read. Any refusal latches the session.
    pub(crate) fn store_endpoint(&self) -> Result<SelectedStoreEndpoint<'_>, SessionRefusal> {
        let values = self
            .observation
            .endpoint()
            .ok_or(SessionRefusal::Gate(GateRefusal::Latched))?;
        let (closure, writer) = {
            let state = self.state.borrow();
            let (closure, writer) = state.receipt.selected_core();
            (closure.to_owned(), writer)
        };
        self.step(|_, work| validate_endpoint(values, &closure, writer, work))?;
        self.recheck()?;
        Ok(SelectedStoreEndpoint::new(values))
    }

    /// Law X2 r5 items 2 to 5 (unit X2b-1): select the project root by S3
    /// from `launch` (or examine `explicit` once), walk and judge its chain
    /// (X2a), sample its incarnation and marker, capture the registry once
    /// (R0) and classify, all on the session ledger under the held fence,
    /// with this receipt's premise and H-filesystem check and the explicit
    /// `--trust-group` set. The admission is then rechecked, and one full
    /// session recheck runs. Any refusal latches the session. The admission
    /// grants nothing yet (item 6a's tracking is unit X2b-2).
    pub(crate) fn admit_project_root(
        &self,
        launch: &std::path::Path,
        explicit: Option<&std::path::Path>,
        trust_groups: &BTreeSet<u32>,
    ) -> Result<super::project_admission::ProjectRootAdmission, ProjectSessionRefusal> {
        use super::project_admission::{admit_project_root, judged_registry};
        use super::project_chain::ProjectChainPolicy;
        let judged = judged_registry(self.observation.required())
            .cloned()
            .ok_or(ProjectSessionRefusal::Session(SessionRefusal::Gate(GateRefusal::Latched)))?;
        let admission = {
            let mut state = self.state.borrow_mut();
            let State {
                ledger,
                latched,
                receipt,
                ..
            } = &mut *state;
            if *latched || ledger.is_failed() {
                return Err(ProjectSessionRefusal::Session(SessionRefusal::Gate(
                    GateRefusal::Latched,
                )));
            }
            let qualification = receipt.qualification();
            let home_filesystem =
                |sample: &DescriptorFilesystem| qualification.is_home_filesystem(sample);
            let policy = ProjectChainPolicy::new(
                qualification.omission_premise(),
                &home_filesystem,
                trust_groups,
            );
            let account = self.observation.account();
            let installation = self.observation.chain().installation();
            let result = ledger.scope(|work| {
                let admission = admit_project_root(
                    self.observation.chain().home_spelling(),
                    account.uid(),
                    launch,
                    explicit,
                    installation,
                    &judged,
                    &policy,
                    work,
                )?;
                admission.recheck(account.uid(), installation, &judged, &policy, work)?;
                Ok(admission)
            });
            if result.is_err() {
                *latched = true;
            }
            result.map_err(ProjectSessionRefusal::Project)?
        };
        self.recheck().map_err(ProjectSessionRefusal::Session)?;
        Ok(admission)
    }

    /// M3-B unit B1-b (X2 r9 item 3a), the analysis path's first phase: S3
    /// selection retaining the judged `opensip.json`, the chain, incarnation
    /// and marker, then the configuration carriers (the interactive local
    /// carrier only when `local` says so), on the session ledger under the
    /// held fence. No registry is read: configuration resolution and pack
    /// admission run on the result before `complete_project_admission`.
    /// One full session recheck runs; any refusal latches the session.
    /// Selection records its upward provenance into `upward`, and `waiver`
    /// reaches the explicit root (M3-B unit B2-b3a).
    pub(crate) fn admit_project_carriers(
        &self,
        launch: &std::path::Path,
        explicit: Option<&std::path::Path>,
        trust_groups: &BTreeSet<u32>,
        local: super::project_admission::LocalCarrierPolicy,
        waiver: Option<&crate::grants::ProjectOwnerWaiver>,
        upward: &mut super::project_admission::UpwardRecord,
    ) -> Result<super::project_admission::CarrierAdmission, ProjectSessionRefusal> {
        use super::project_admission::admit_project_root_for_analysis;
        use super::project_chain::ProjectChainPolicy;
        let admission = {
            let mut state = self.state.borrow_mut();
            let State {
                ledger,
                latched,
                receipt,
                ..
            } = &mut *state;
            if *latched || ledger.is_failed() {
                return Err(ProjectSessionRefusal::Session(SessionRefusal::Gate(
                    GateRefusal::Latched,
                )));
            }
            let qualification = receipt.qualification();
            let home_filesystem =
                |sample: &DescriptorFilesystem| qualification.is_home_filesystem(sample);
            let policy = ProjectChainPolicy::new(
                qualification.omission_premise(),
                &home_filesystem,
                trust_groups,
            );
            let account = self.observation.account();
            let result = ledger.scope(|work| {
                admit_project_root_for_analysis(
                    self.observation.chain().home_spelling(),
                    account.uid(),
                    launch,
                    explicit,
                    waiver,
                    local,
                    &policy,
                    upward,
                    work,
                )
            });
            if result.is_err() {
                *latched = true;
            }
            result.map_err(ProjectSessionRefusal::Project)?
        };
        self.recheck().map_err(ProjectSessionRefusal::Session)?;
        Ok(admission)
    }

    /// The analysis path's second phase (X2 item 5): the one registry
    /// capture and classification, then the admission's recheck with the
    /// carriers' samples and absences, then one full session recheck. Any
    /// refusal latches the session.
    pub(crate) fn complete_project_admission(
        &self,
        carriers: super::project_admission::CarrierAdmission,
        trust_groups: &BTreeSet<u32>,
        waiver: Option<&crate::grants::ProjectOwnerWaiver>,
    ) -> Result<super::project_admission::ProjectRootAdmission, ProjectSessionRefusal> {
        use super::project_admission::judged_registry;
        use super::project_chain::ProjectChainPolicy;
        let judged = judged_registry(self.observation.required())
            .cloned()
            .ok_or(ProjectSessionRefusal::Session(SessionRefusal::Gate(GateRefusal::Latched)))?;
        let admission = {
            let mut state = self.state.borrow_mut();
            let State {
                ledger,
                latched,
                receipt,
                ..
            } = &mut *state;
            if *latched || ledger.is_failed() {
                return Err(ProjectSessionRefusal::Session(SessionRefusal::Gate(
                    GateRefusal::Latched,
                )));
            }
            let qualification = receipt.qualification();
            let home_filesystem =
                |sample: &DescriptorFilesystem| qualification.is_home_filesystem(sample);
            let policy = ProjectChainPolicy::new(
                qualification.omission_premise(),
                &home_filesystem,
                trust_groups,
            );
            let account = self.observation.account();
            let installation = self.observation.chain().installation();
            let result = ledger.scope(|work| {
                let admission = carriers.capture_registry(installation, &judged, work)?;
                admission.recheck_waived(account.uid(), installation, &judged, &policy, waiver, work)?;
                Ok(admission)
            });
            if result.is_err() {
                *latched = true;
            }
            result.map_err(ProjectSessionRefusal::Project)?
        };
        self.recheck().map_err(ProjectSessionRefusal::Session)?;
        Ok(admission)
    }

    /// The read session's equivalent release (M3-B r5 item 12; unit
    /// B2-b3a, LD-B2B3-1): the fence is unlocked and every retained
    /// installation handle closed (`InstallationObservation::release`), the
    /// session ledger and its captures dropped, and only this invocation's
    /// read receipt kept, for `ReleasedRead::discovery_root`. A latched or
    /// failed session still releases its fence and lends nothing.
    pub(crate) fn release(self) -> Result<ReleasedRead, SessionRefusal> {
        let Self {
            observation, state, ..
        } = self;
        let State {
            ledger,
            latched,
            receipt,
            ..
        } = state.into_inner();
        let released = observation.release();
        if latched || ledger.is_failed() {
            return Err(SessionRefusal::Gate(GateRefusal::Latched));
        }
        released.map_err(|error| SessionRefusal::Gate(GateRefusal::Io(IoFailure::Lock(error))))?;
        Ok(ReleasedRead { receipt })
    }

    /// Law X2 r7 item 6a (unit X2b-2): the tracking observation for an
    /// admitted project root, on the session ledger under the held fence,
    /// then its recheck, then one full session recheck. It reads the
    /// process environment only to refuse, and the fixed system sources.
    /// Any refusal latches the session.
    pub(crate) fn observe_project_tracking(
        &self,
        admission: &super::project_admission::ProjectRootAdmission,
        trust_groups: &BTreeSet<u32>,
    ) -> Result<super::git_tracking::TrackingObservation, TrackingSessionRefusal> {
        use super::git_tracking::{SYSTEM_SOURCES, process_environment};
        let sources: Vec<&std::path::Path> =
            SYSTEM_SOURCES.iter().map(std::path::Path::new).collect();
        self.observe_project_tracking_with(admission, trust_groups, &process_environment(), &sources)
    }
    /// `observe_project_tracking` over a given environment and system
    /// source list (the production entry passes the process environment
    /// and `SYSTEM_SOURCES`).
    pub(crate) fn observe_project_tracking_with(
        &self,
        admission: &super::project_admission::ProjectRootAdmission,
        trust_groups: &BTreeSet<u32>,
        environment: &[(std::ffi::OsString, std::ffi::OsString)],
        system_sources: &[&std::path::Path],
    ) -> Result<super::git_tracking::TrackingObservation, TrackingSessionRefusal> {
        use super::git_tracking::{TrackingInputs, observe_tracking, recheck_tracking};
        use super::project_chain::ProjectChainPolicy;
        let observation = {
            let mut state = self.state.borrow_mut();
            let State {
                ledger,
                latched,
                receipt,
                ..
            } = &mut *state;
            if *latched || ledger.is_failed() {
                return Err(TrackingSessionRefusal::Session(SessionRefusal::Gate(
                    GateRefusal::Latched,
                )));
            }
            let qualification = receipt.qualification();
            let home_filesystem =
                |sample: &DescriptorFilesystem| qualification.is_home_filesystem(sample);
            let policy = ProjectChainPolicy::new(
                qualification.omission_premise(),
                &home_filesystem,
                trust_groups,
            );
            let inputs = TrackingInputs {
                chain: admission.chain(),
                uid: self.observation.account().uid(),
                policy: &policy,
                home: self.observation.chain().home_spelling(),
                environment,
                system_sources,
            };
            let result = ledger.scope(|work| {
                let observed = observe_tracking(&inputs, work)?;
                recheck_tracking(&observed, &inputs, work)?;
                Ok(observed)
            });
            if result.is_err() {
                *latched = true;
            }
            result.map_err(TrackingSessionRefusal::Tracking)?
        };
        self.recheck().map_err(TrackingSessionRefusal::Session)?;
        Ok(observation)
    }

    /// Law X2 item 7 (unit X2d): admit the namespace of an Eligible root,
    /// with its tracking observation, under this session's held fence and
    /// on its ledger. N is R0's ACTIVE row's. No lock is taken: the target
    /// borrows this session, and `NamespaceTarget::lease_shared` takes
    /// SHARED-READ. Any refusal latches the session; the fence stays held.
    pub(crate) fn admit_namespace(
        &self,
        admission: super::project_admission::ProjectRootAdmission,
        tracking: super::git_tracking::TrackingObservation,
        inputs: &super::first_registration::ProjectInputs<'_>,
    ) -> Result<super::namespace_lease::NamespaceTarget<&Self>, NamespaceSessionRefusal> {
        super::namespace_lease::admit(
            self,
            super::namespace_lease::NamespaceSubject::Eligible {
                admission,
                tracking,
            },
            inputs,
        )
    }

    /// One charged step on the retained I. Every refusal, and every budget
    /// failure, latches the session.
    pub(super) fn step<R>(
        &self,
        action: impl FnOnce(&Held<'_>, &mut WorkScope<'_>) -> Result<R, Failure>,
    ) -> Result<R, SessionRefusal> {
        let mut state = self.state.borrow_mut();
        let State {
            ledger,
            latched,
            receipt,
            ..
        } = &mut *state;
        if *latched || ledger.is_failed() {
            return Err(SessionRefusal::Gate(GateRefusal::Latched));
        }
        let qualification = receipt.qualification();
        let home_filesystem =
            |sample: &DescriptorFilesystem| qualification.is_home_filesystem(sample);
        let held = Held {
            installation: self.installation(),
            uid: self.uid(),
            home_filesystem: &home_filesystem,
        };
        let result = ledger.scope(|work| action(&held, work));
        if result.is_err() {
            *latched = true;
        }
        result.map_err(|failure| SessionRefusal::Gate(flatten(failure)))
    }

    /// Item 5 step 4 over the held fence, the observation's required files
    /// and every file captured since: the receipt's rechecks, the full
    /// recheck set, and the receipt's rechecks again. Any refusal latches.
    pub(crate) fn recheck(&self) -> Result<(), SessionRefusal> {
        let mut state = self.state.borrow_mut();
        let State {
            ledger,
            latched,
            receipt,
            captured,
            absent,
        } = &mut *state;
        if *latched || ledger.is_failed() {
            return Err(SessionRefusal::Gate(GateRefusal::Latched));
        }
        *latched = true;
        let (qualification, mut rechecks) = receipt.split();
        rechecks.recheck().map_err(SessionRefusal::Receipt)?;
        let home_filesystem =
            |sample: &DescriptorFilesystem| qualification.is_home_filesystem(sample);
        let policy = ChainPolicy::new(qualification.omission_premise(), &home_filesystem);
        let observation = &self.observation;
        let (fence, fence_id) = observation.fence();
        let uid = observation.account().uid();
        let installation = observation.chain().installation();
        let files: Vec<RequiredFile> = observation
            .required()
            .iter()
            .chain(captured.iter())
            .cloned()
            .collect();
        ledger
            .scope(|work| {
                recheck_chain(
                    observation.account(),
                    observation.chain(),
                    fence,
                    fence_id,
                    &policy,
                    work,
                    |work| {
                        recheck_files(installation, uid, &files, work)?;
                        recheck_absent(installation, uid, absent, work)
                    },
                )
            })
            .map_err(|failure| SessionRefusal::Gate(flatten(failure)))?;
        rechecks.recheck().map_err(SessionRefusal::Receipt)?;
        *latched = false;
        Ok(())
    }

    /// The held fence alone, charged, between full rechecks: the locked
    /// descriptor still carries the name `lifecycle.fence`, and that name
    /// under the retained I is still the one-link regular file of the
    /// locked identity. That is what keeps first-party writers out; the
    /// carrier's custody (owner, mode, ACL) is the full recheck's (item 5
    /// step 4). Any refusal latches.
    pub(crate) fn recheck_held(&self) -> Result<(), SessionRefusal> {
        let (fence, fence_id) = self.observation.fence();
        self.step(|held, work| {
            let carrier = || Entry::File(super::installation_fence::CARRIER.to_owned());
            let named = work.run(descriptor_name_observation_cost(), |_| {
                fence
                    .name_matches(OsStr::new(super::installation_fence::CARRIER))
                    .map_err(|error| WorkFailure::Operation(GateRefusal::Io(IoFailure::Lock(error))))
            })?;
            if !named {
                return refused(GateRefusal::Custody(CustodyRefusal::FenceChanged));
            }
            let cost = super::installation_admission::plus(&[
                RetainedDirectory::open_regular_cost(super::installation_fence::CARRIER),
                STATUS,
            ]);
            let current = work.run(cost, |_| {
                let file = held
                    .installation
                    .open_regular(super::installation_fence::CARRIER)
                    .map_err(|error| WorkFailure::Operation(open_refusal(carrier(), error)))?;
                file.metadata().map_err(|error| {
                    WorkFailure::Operation(GateRefusal::Io(IoFailure::Open {
                        entry: carrier(),
                        error,
                    }))
                })
            })?;
            use std::os::unix::fs::MetadataExt;
            if (current.dev(), current.ino()) != fence_id
                || current.nlink() != 1
                || !current.is_file()
            {
                return refused(GateRefusal::Custody(CustodyRefusal::FenceChanged));
            }
            Ok(())
        })
    }

    /// A charged sample of I's filesystem, which must be H's.
    pub(crate) fn installation_filesystem(&self) -> Result<DescriptorFilesystem, SessionRefusal> {
        self.step(|held, work| {
            sample_admitted(held.installation.as_file(), Entry::Installation, held, work)
        })
    }
    /// A charged sample of the fence carrier's filesystem, which must be H's.
    pub(crate) fn fence_filesystem(&self) -> Result<DescriptorFilesystem, SessionRefusal> {
        let (fence, _) = self.observation.fence();
        self.step(|held, work| {
            let entry = Entry::File(super::installation_fence::CARRIER.to_owned());
            let sample = work.run(descriptor_filesystem_observation_cost(), |_| {
                fence.observe_filesystem().map_err(|error| {
                    WorkFailure::Operation(GateRefusal::Io(IoFailure::Filesystem {
                        entry: entry.clone(),
                        error,
                    }))
                })
            })?;
            admitted(sample, entry, held)
        })
    }

    /// Item 5 step 3 for one reader: a bounded capture of `prefixes/leaf`
    /// under the retained I, every native step charged before it runs. A
    /// failed capture is a value, so step 4's full recheck still runs after
    /// it; the capture's failure stays the cause, and the session latches.
    /// A captured file joins the files step 4 rechecks from then on.
    pub(crate) fn capture(
        &self,
        prefixes: &[&str],
        leaf: &str,
        cap: usize,
    ) -> Result<Capture, SessionRefusal> {
        self.capture_with(prefixes, leaf, cap, &|_| {})
    }
    pub(crate) fn capture_with(
        &self,
        prefixes: &[&str],
        leaf: &str,
        cap: usize,
        interpose: &dyn Fn(Phase),
    ) -> Result<Capture, SessionRefusal> {
        let attempted =
            self.step(|held, work| read_capture(held, prefixes, leaf, cap, false, interpose, work))?;
        match self.settle_capture(attempted)? {
            Some(capture) => Ok(capture),
            None => unreachable!("a required capture never observes absence"),
        }
    }

    /// A capture attempt's settlement (shared by `capture_with` and
    /// `capture_optional`): a captured file joins step 4's files and an
    /// observed absence its absences, then one full recheck; a failed
    /// capture still runs the full recheck, stays the cause, and latches.
    fn settle_capture(
        &self,
        attempted: Result<Captured, GateRefusal>,
    ) -> Result<Option<Capture>, SessionRefusal> {
        match attempted {
            Ok(Captured::Present(capture)) => {
                self.state
                    .borrow_mut()
                    .captured
                    .push(RequiredFile::new(&capture.relative, capture.metadata.clone()));
                self.recheck()?;
                Ok(Some(capture))
            }
            Ok(Captured::Absent(observation)) => {
                self.state.borrow_mut().absent.push(observation);
                self.recheck()?;
                Ok(None)
            }
            Err(refusal) => {
                // The earlier failure is the cause when both fail.
                let _ = self.recheck();
                self.latch();
                Err(SessionRefusal::Gate(refusal))
            }
        }
    }

    /// M3-B unit B1-b (MB item 2, LD-B1B-2): an optional member under I,
    /// such as `host/settings.json`, through the same judged walk as
    /// `capture`. Before each component is opened, a charged no-follow
    /// absence lookup runs under its judged parent; the first absent one is
    /// recorded with the judged parents and joins step 4's recheck, and
    /// nothing is created. A parent that fails a judgment refuses, as in
    /// `capture`, and latches the session.
    pub(crate) fn capture_optional(
        &self,
        prefixes: &[&str],
        leaf: &str,
        cap: usize,
    ) -> Result<Option<Capture>, SessionRefusal> {
        let attempted =
            self.step(|held, work| read_capture(held, prefixes, leaf, cap, true, &|_| {}, work))?;
        self.settle_capture(attempted)
    }

    /// A capture's own recheck, between full rechecks: the held fence, then
    /// every retained edge still private with its identity and on H's
    /// filesystem, then the retained file still private with its metadata,
    /// still the file at its name, and on its filesystem. Any refusal
    /// latches.
    pub(crate) fn recheck_capture(&self, capture: &Capture) -> Result<(), SessionRefusal> {
        self.recheck_held()?;
        self.step(|held, work| {
            let mut parent = held.installation;
            for edge in &capture.edges {
                let entry = || Entry::File(edge.relative.clone());
                let observed = judge_directory(&edge.directory, &edge.relative, held.uid, work)?
                    .map_err(WorkFailure::Operation)?;
                let reopened = work.run(
                    open_child_directory_cost(OsStr::new(last(&edge.relative))),
                    |_| Ok(parent.open_child_directory(OsStr::new(last(&edge.relative)))),
                )?;
                let reopened = reopened
                    .map_err(|error| WorkFailure::Operation(open_refusal(entry(), error)))?;
                let again = judge_directory(&reopened, &edge.relative, held.uid, work)?
                    .map_err(WorkFailure::Operation)?;
                named(edge.directory.as_file(), last(&edge.relative), entry(), work)?
                    .map_err(WorkFailure::Operation)?;
                if identity(observed.metadata()) != identity(&edge.metadata)
                    || identity(again.metadata()) != identity(&edge.metadata)
                {
                    return changed();
                }
                let sample = sample_admitted(edge.directory.as_file(), entry(), held, work)?;
                if sample != edge.filesystem {
                    return refused(GateRefusal::Filesystem(entry()));
                }
                parent = &edge.directory;
            }
            let entry = || Entry::File(capture.relative.clone());
            let now = judge_file(&capture.file, &capture.relative, held.uid, work)?
                .map_err(WorkFailure::Operation)?;
            if *now.metadata() != capture.metadata {
                return changed();
            }
            let reopened = work.run(RetainedDirectory::open_regular_cost(&capture.leaf), |_| {
                Ok(parent.open_regular(&capture.leaf))
            })?;
            let reopened =
                reopened.map_err(|error| WorkFailure::Operation(open_refusal(entry(), error)))?;
            let current = judge_file(&reopened, &capture.relative, held.uid, work)?
                .map_err(WorkFailure::Operation)?;
            if identity(current.metadata()) != identity(&capture.metadata) {
                return changed();
            }
            named(&capture.file, &capture.leaf, entry(), work)?.map_err(WorkFailure::Operation)?;
            let sample = sample_admitted(&capture.file, entry(), held, work)?;
            if sample != capture.filesystem {
                return refused(GateRefusal::Filesystem(entry()));
            }
            Ok(())
        })
    }

    /// Charged samples of every filesystem contributing to a capture: I,
    /// the fence carrier, each retained edge and the file. Pre-profile
    /// evidence only; copied samples carry no custody.
    pub(crate) fn capture_filesystems(
        &self,
        capture: &Capture,
    ) -> Result<Vec<DescriptorFilesystem>, SessionRefusal> {
        let mut values = vec![self.installation_filesystem()?, self.fence_filesystem()?];
        for edge in &capture.edges {
            values.push(self.step(|held, work| {
                sample_admitted(
                    edge.directory.as_file(),
                    Entry::File(edge.relative.clone()),
                    held,
                    work,
                )
            })?);
        }
        values.push(self.step(|held, work| {
            sample_admitted(&capture.file, Entry::File(capture.relative.clone()), held, work)
        })?);
        Ok(values)
    }

    /// Law X3a r5 item 4 (unit X3a-2): a charged sample of the filesystem
    /// of one file the observation read once, for the endpoint readers'
    /// samples. The file is opened no-follow by its name under the retained
    /// I and judged private, as the full recheck's required-file limb does;
    /// it must still carry the full sample the session retained (else
    /// `required-files-changed`), and its filesystem must be H's. No byte
    /// is read and nothing joins the recheck set. Any refusal latches.
    pub(crate) fn required_filesystem(
        &self,
        relative: &str,
    ) -> Result<DescriptorFilesystem, SessionRefusal> {
        let Some(retained) = self
            .observation
            .required()
            .iter()
            .find(|file| file.relative() == relative)
        else {
            self.latch();
            return Err(SessionRefusal::Gate(GateRefusal::Latched));
        };
        self.step(|held, work| {
            let (file, metadata) = private_file(held.installation, relative, held.uid, work)
                .map_err(|failure| match failure {
                    WorkFailure::Operation(GateRefusal::Incomplete(_)) => {
                        WorkFailure::Operation(GateRefusal::Custody(CustodyRefusal::Changed))
                    }
                    failure => failure,
                })?;
            if metadata != *retained.metadata() {
                return changed();
            }
            sample_admitted(&file, Entry::File(relative.to_owned()), held, work)
        })
    }
}

/// Law 458c item 6 for the trust readers' own accounting: their retained
/// budget charges this session's one ledger. A refused charge latches the
/// session; a closed session refuses every charge.
pub(crate) trait LedgerSink {
    fn charge(&self, cost: WorkCost) -> Result<(), WorkBudgetError>;
    fn is_closed(&self) -> bool;
    fn close(&self);
}
impl LedgerSink for ReadSession {
    fn charge(&self, cost: WorkCost) -> Result<(), WorkBudgetError> {
        self.step(|_, work| work.charge(cost))
            .map_err(|refusal| match refusal {
                SessionRefusal::Gate(GateRefusal::Budget(budget)) => budget,
                _ => WorkBudgetError::Closed,
            })
    }
    fn is_closed(&self) -> bool {
        self.is_latched()
    }
    fn close(&self) {
        self.latch();
    }
}

/// The trust readers' view of the held I (law 458c item 8): the retained I,
/// the invoking user with no supplied groups, the charged held-fence
/// recheck and the charged fence-carrier sample.
impl HeldFence for ReadSession {
    fn directory(&self) -> &RetainedDirectory {
        self.installation()
    }
    fn supplied_actor(&self) -> (u32, &BTreeSet<u32>) {
        (self.uid(), &self.groups)
    }
    fn recheck(&self) -> Result<(), installation_fence::Error> {
        self.recheck_held().map_err(installation_fence::Error::Session)
    }
    fn observe_filesystem(&self) -> Result<DescriptorFilesystem, installation_fence::Error> {
        self.fence_filesystem()
            .map_err(installation_fence::Error::Session)
    }
}

/// One status read with a buffer no smaller than the native `stat`.
const STATUS: WorkCost = WorkCost {
    objects: 0,
    edges: 1,
    bytes: 512,
};
fn refused<T>(refusal: GateRefusal) -> Result<T, Failure> {
    Err(WorkFailure::Operation(refusal))
}
fn changed<T>() -> Result<T, Failure> {
    refused(GateRefusal::Custody(CustodyRefusal::Changed))
}
fn identity(metadata: &DescriptorMetadata) -> (u64, u64) {
    (metadata.device, metadata.inode)
}
fn last(relative: &str) -> &str {
    relative.rsplit('/').next().unwrap_or(relative)
}
/// A name that is absent, or not the kind it must hold, is a structural
/// finding (the incomplete row); any other open error is host I/O.
fn open_refusal(entry: Entry, error: io::Error) -> GateRefusal {
    if missing(&error) {
        GateRefusal::Incomplete(super::installation_admission::IncompleteRefusal::Missing(entry))
    } else {
        GateRefusal::Io(IoFailure::Open { entry, error })
    }
}

/// A private directory below I, judged by the owner's predicate on a
/// charged capture. A capture failure or a custody refusal is a value.
fn judge_directory(
    directory: &RetainedDirectory,
    relative: &str,
    uid: u32,
    work: &mut WorkScope<'_>,
) -> Result<Result<DescriptorAclCapture, GateRefusal>, Failure> {
    let entry = || Entry::File(relative.to_owned());
    let capture = match capture_descriptor_acl_observed(directory.as_file(), work)? {
        Ok(capture) => capture,
        Err(error) => {
            return Ok(Err(GateRefusal::Io(IoFailure::Capture {
                entry: entry(),
                error,
            })));
        }
    };
    Ok(
        assess_private_descendant_capture(PrivateObjectKind::Directory, uid, &capture)
            .map(|()| capture)
            .map_err(|refusal| {
                GateRefusal::Custody(CustodyRefusal::Private {
                    entry: entry(),
                    refusal,
                })
            }),
    )
}
/// A private regular file below I, judged by the owner's predicate on a
/// charged capture (the required-file limb's predicate). A capture failure
/// or a custody refusal is a value.
fn judge_file(
    file: &File,
    relative: &str,
    uid: u32,
    work: &mut WorkScope<'_>,
) -> Result<Result<DescriptorAclCapture, GateRefusal>, Failure> {
    let capture = match capture_descriptor_acl_observed(file, work)? {
        Ok(capture) => capture,
        Err(error) => {
            return Ok(Err(GateRefusal::Io(IoFailure::Capture {
                entry: Entry::File(relative.to_owned()),
                error,
            })));
        }
    };
    Ok(judge_capture(&capture, relative, uid).map(|_| capture))
}
/// The descriptor's own name still `expected`, charged. A mismatch is a
/// custody refusal and an error host I/O, both values.
fn named(
    file: &File,
    expected: &str,
    entry: Entry,
    work: &mut WorkScope<'_>,
) -> Result<Result<(), GateRefusal>, Failure> {
    let matched = work.run(descriptor_name_observation_cost(), |_| {
        Ok::<_, Failure>(descriptor_name_matches(file, OsStr::new(expected)))
    })?;
    Ok(match matched {
        Ok(true) => Ok(()),
        Ok(false) => Err(GateRefusal::Custody(CustodyRefusal::NameChanged(entry))),
        Err(error) => Err(GateRefusal::Io(IoFailure::Open { entry, error })),
    })
}
/// A charged filesystem sample that must be H's (the install filesystem
/// row). Latching: used only by rechecks and samples.
fn sample_admitted(
    file: &File,
    entry: Entry,
    held: &Held<'_>,
    work: &mut WorkScope<'_>,
) -> Result<DescriptorFilesystem, Failure> {
    match sample(file, entry.clone(), work)? {
        Ok(sample) => admitted(sample, entry, held),
        Err(refusal) => refused(refusal),
    }
}
fn sample(
    file: &File,
    entry: Entry,
    work: &mut WorkScope<'_>,
) -> Result<Result<DescriptorFilesystem, GateRefusal>, Failure> {
    let observed = work.run(descriptor_filesystem_observation_cost(), |_| {
        Ok::<_, Failure>(opensip_platform::observe_filesystem(file))
    })?;
    Ok(observed.map_err(|error| GateRefusal::Io(IoFailure::Filesystem { entry, error })))
}
fn admitted(
    sample: DescriptorFilesystem,
    entry: Entry,
    held: &Held<'_>,
) -> Result<DescriptorFilesystem, Failure> {
    if (held.home_filesystem)(&sample) {
        Ok(sample)
    } else {
        refused(GateRefusal::Filesystem(entry))
    }
}

/// Step 4's limb for optional members observed absent: each judged parent
/// is reopened by its exact name, judged again by private custody, and must
/// keep the full sample of its original judgment; then the absent component
/// must still be absent. A vanished, replaced or re-permissioned parent is a
/// change, never a vacuous absence.
fn recheck_absent(
    installation: &RetainedDirectory,
    uid: u32,
    absent: &[AbsentObservation],
    work: &mut WorkScope<'_>,
) -> Result<(), Failure> {
    let changed = || GateRefusal::Custody(CustodyRefusal::Changed);
    for observation in absent {
        let mut parents: Vec<RetainedDirectory> = Vec::with_capacity(observation.edges.len());
        for (relative, metadata) in &observation.edges {
            let entry = || Entry::File(relative.clone());
            let component = last(relative);
            let base = parents.last().unwrap_or(installation);
            let opened = work.run(open_child_directory_cost(OsStr::new(component)), |_| {
                Ok::<_, Failure>(base.open_child_directory(OsStr::new(component)))
            })?;
            let directory = match opened {
                Ok(directory) => directory,
                Err(error) if missing(&error) => return Err(WorkFailure::Operation(changed())),
                Err(error) => return Err(WorkFailure::Operation(open_refusal(entry(), error))),
            };
            let capture = match judge_directory(&directory, relative, uid, work)? {
                Ok(capture) => capture,
                Err(refusal) => return Err(WorkFailure::Operation(refusal)),
            };
            if let Err(refusal) = named(directory.as_file(), component, entry(), work)? {
                return Err(WorkFailure::Operation(refusal));
            }
            if capture.metadata() != metadata {
                return Err(WorkFailure::Operation(changed()));
            }
            parents.push(directory);
        }
        let base = parents.last().unwrap_or(installation);
        let entry = Entry::File(observation.absent.clone());
        match absent_under(base, last(&observation.absent), entry, work)? {
            Ok(true) => {}
            Ok(false) => return Err(WorkFailure::Operation(changed())),
            Err(refusal) => return Err(WorkFailure::Operation(refusal)),
        }
    }
    Ok(())
}

/// Test seam: points inside one capture where a test changes the tree.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum Phase {
    /// After the prefix at this index was opened, before it is judged.
    AfterDirectory(usize),
    AfterOpen,
    BeforeRead,
    AfterRead,
}

/// The capture itself. Only a budget failure leaves the scope; every other
/// failure is returned as a value, so the ledger stays open for step 4.
fn read_capture(
    held: &Held<'_>,
    prefixes: &[&str],
    leaf: &str,
    cap: usize,
    optional: bool,
    interpose: &dyn Fn(Phase),
    work: &mut WorkScope<'_>,
) -> Result<Result<Captured, GateRefusal>, Failure> {
    macro_rules! value {
        ($attempt:expr) => {
            match $attempt {
                Ok(value) => value,
                Err(refusal) => return Ok(Err(refusal)),
            }
        };
    }
    let mut edges: Vec<Edge> = Vec::with_capacity(prefixes.len());
    let mut relative = String::new();
    for (index, component) in prefixes.iter().enumerate() {
        if !relative.is_empty() {
            relative.push('/');
        }
        relative.push_str(component);
        let entry = || Entry::File(relative.clone());
        let parent = edges.last().map_or(held.installation, |edge| &edge.directory);
        if optional && value!(absent_under(parent, component, entry(), work)?) {
            return Ok(Ok(Captured::Absent(observed_absent(&edges, relative))));
        }
        let opened = work.run(open_child_directory_cost(OsStr::new(component)), |_| {
            Ok::<_, Failure>(parent.open_child_directory(OsStr::new(component)))
        })?;
        interpose(Phase::AfterDirectory(index));
        let directory = value!(opened.map_err(|error| open_refusal(entry(), error)));
        let capture = value!(judge_directory(&directory, &relative, held.uid, work)?);
        // Exactly this name, not a case-folded alias of it.
        value!(named(directory.as_file(), component, entry(), work)?);
        let filesystem = value!(sample(directory.as_file(), entry(), work)?);
        if !(held.home_filesystem)(&filesystem) {
            return Ok(Err(GateRefusal::Filesystem(entry())));
        }
        edges.push(Edge {
            directory,
            relative: relative.clone(),
            metadata: capture.metadata().clone(),
            filesystem,
        });
    }
    if !relative.is_empty() {
        relative.push('/');
    }
    relative.push_str(leaf);
    let entry = || Entry::File(relative.clone());
    let parent = edges.last().map_or(held.installation, |edge| &edge.directory);
    if optional && value!(absent_under(parent, leaf, entry(), work)?) {
        return Ok(Ok(Captured::Absent(observed_absent(&edges, relative))));
    }
    let opened = work.run(RetainedDirectory::open_regular_cost(leaf), |_| {
        Ok::<_, Failure>(parent.open_regular(leaf))
    })?;
    interpose(Phase::AfterOpen);
    let file = value!(opened.map_err(|error| open_refusal(entry(), error)));
    let before = value!(judge_file(&file, &relative, held.uid, work)?);
    if before.metadata().size > cap as u64 {
        return Ok(Err(GateRefusal::Io(IoFailure::Read {
            entry: entry(),
            error: WorkReadFailure::Bound,
        })));
    }
    value!(named(&file, leaf, entry(), work)?);
    let filesystem = value!(sample(&file, entry(), work)?);
    if !(held.home_filesystem)(&filesystem) {
        return Ok(Err(GateRefusal::Filesystem(entry())));
    }
    interpose(Phase::BeforeRead);
    let raw = value!(
        read_bounded_observed(&file, cap, work)?.map_err(|error| GateRefusal::Io(
            IoFailure::Read {
                entry: entry(),
                error,
            }
        ))
    );
    interpose(Phase::AfterRead);
    let after = value!(judge_file(&file, &relative, held.uid, work)?);
    value!(named(&file, leaf, entry(), work)?);
    if after.metadata() != before.metadata() {
        return Ok(Err(GateRefusal::Custody(CustodyRefusal::Changed)));
    }
    // The name under the retained parent still holds this same file.
    let reopened = work.run(RetainedDirectory::open_regular_cost(leaf), |_| {
        Ok::<_, Failure>(parent.open_regular(leaf))
    })?;
    let reopened = value!(reopened.map_err(|error| open_refusal(entry(), error)));
    let current = value!(judge_file(&reopened, &relative, held.uid, work)?);
    if identity(current.metadata()) != identity(after.metadata()) {
        return Ok(Err(GateRefusal::Custody(CustodyRefusal::Changed)));
    }
    Ok(Ok(Captured::Present(Capture {
        edges,
        file,
        leaf: leaf.to_owned(),
        relative,
        metadata: after.metadata().clone(),
        filesystem,
        raw,
    })))
}

/// One charged no-follow absence lookup under a judged parent.
fn absent_under(
    parent: &RetainedDirectory,
    name: &str,
    entry: Entry,
    work: &mut WorkScope<'_>,
) -> Result<Result<bool, GateRefusal>, Failure> {
    match parent.observe_child_absent_accounted(OsStr::new(name), work) {
        Ok(absent) => Ok(Ok(absent)),
        Err(WorkFailure::Budget(budget)) => Err(WorkFailure::Budget(budget)),
        Err(WorkFailure::Operation(error)) => Ok(Err(GateRefusal::Io(IoFailure::Open { entry, error }))),
    }
}
fn observed_absent(edges: &[Edge], relative: String) -> AbsentObservation {
    AbsentObservation {
        edges: edges
            .iter()
            .map(|edge| (edge.relative.clone(), edge.metadata.clone()))
            .collect(),
        absent: relative,
    }
}

/// Law X2 item 7 (unit X2d): the read session holds the fence for its
/// namespace steps. Each step runs on the session ledger with the read
/// receipt's premise, then one full session recheck, while the fence is
/// held. Any refusal latches the session and drops what the step returned,
/// so no project lock outlives it.
impl super::namespace_lease::FenceHolder for &ReadSession {
    type Refusal = NamespaceSessionRefusal;
    fn fenced<R>(
        &mut self,
        inputs: &super::first_registration::ProjectInputs<'_>,
        action: impl FnOnce(
            &super::namespace_lease::Held<'_, '_>,
            &mut WorkScope<'_>,
        ) -> Result<R, super::namespace_lease::Failure>,
    ) -> Result<R, NamespaceSessionRefusal> {
        use super::project_admission::judged_registry;
        use super::project_chain::ProjectChainPolicy;
        let session: &ReadSession = self;
        let judged = judged_registry(session.observation.required()).ok_or(
            NamespaceSessionRefusal::Session(SessionRefusal::Gate(GateRefusal::Latched)),
        )?;
        let value = {
            let mut state = session.state.borrow_mut();
            let State {
                ledger,
                latched,
                receipt,
                ..
            } = &mut *state;
            if *latched || ledger.is_failed() {
                return Err(NamespaceSessionRefusal::Session(SessionRefusal::Gate(
                    GateRefusal::Latched,
                )));
            }
            let qualification = receipt.qualification();
            let home_filesystem =
                |sample: &DescriptorFilesystem| qualification.is_home_filesystem(sample);
            let policy = ProjectChainPolicy::new(
                qualification.omission_premise(),
                &home_filesystem,
                inputs.trust_groups,
            );
            let held = super::namespace_lease::Held {
                installation: session.installation(),
                uid: session.uid(),
                home: session.observation.chain().home_spelling(),
                judged,
                policy: &policy,
                inputs,
                durable: None,
            };
            let result = ledger.scope(|work| action(&held, work));
            if result.is_err() {
                *latched = true;
            }
            result.map_err(NamespaceSessionRefusal::Namespace)?
        };
        session
            .recheck()
            .map_err(NamespaceSessionRefusal::Session)?;
        Ok(value)
    }
}

#[cfg(test)]
mod tests {
    include!("installation_read_tests.rs");
}
